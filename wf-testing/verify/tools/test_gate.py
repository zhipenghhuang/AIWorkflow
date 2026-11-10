#!/usr/bin/env python3
"""Test gate for the analysis-driven workflow.

Modes:
  coverage  analysis + plan structure/completeness
  execute   batch execution records (scenario/result/evidence/P0)
  report    report ↔ plan ↔ records consistency and exit verdict
  writeback platform writeback receipt

Analysis is mandatory. Plan is the schedule; the intent/risk detail lives in analysis.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PACKAGE_NAME = "wf-testing"
RECEIPT_DIR = Path(".gate") / PACKAGE_NAME
STATUSES = {"未执行", "通过", "失败", "阻塞", "待实现", "不适用", "未本轮验证"}
FAIL_STATUSES = {"失败", "阻塞", "待实现"}
INT_ID_RE = re.compile(r"\bINT-[A-Z0-9-]+\b")
# 原文锚点：章节/AC/路由/方法/互补源分隔；禁只写文档名
SOURCE_ANCHOR_RE = re.compile(
    r"[§#/]|AC[-_]?\w+|INT[-_]?\w+|F[-_]?\d+|R[-_]?\d+|"
    r"\b(?:GET|POST|PUT|PATCH|DELETE)\b|原型|契约|OpenAPI|路由|第\s*\d+",
    re.I,
)
# P0 证伪/反向场景标记（场景名/原文/缺口；找问题用，非刷词过闸）
FALSIFY_RE = re.compile(
    r"负向|禁止|拒绝|越权|非法|无权限|未授权|证伪|反向|边界|异常|幂等|恢复|"
    r"空值|重复提交|错误码|阻断|门禁|冲突|过期|假通过|拦截|不可放行|不可确认|"
    r"无\s*token|未登录|坏指纹|重放|deny|forbidden|unauthorized|negative|invalid",
    re.I,
)
NA_FALSIFY_RE = re.compile(
    r"(?:证伪|负向|反向).{0,16}(?:N/?A|不适用)|(?:N/?A|不适用).{0,16}(?:证伪|负向|反向)",
    re.I,
)
# 通过态 Oracle 过弱：无对照原文/分析的可观测断言
WEAK_ORACLE_RE = re.compile(
    r"^(?:通过|ok|okay|pass|正常|成功|符合预期|符合要求|无报错|没报错|看起来?对|"
    r"页面正常|页面正常显示|功能正常|功能正常显示|显示正常|展示正常|数据正常|数据正确|"
    r"结果正常|结果正确|字段齐(?:全)?|数据齐全|数据完整|字段完整|一切正常|无异常|没问题|可用|生效|符合设计)"
    r"[.。!！]*$",
    re.I,
)

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def sections(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    current = ""
    buf: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current:
                out[current] = "\n".join(buf)
            current = line.strip()
            buf = [line]
        else:
            buf.append(line)
    if current:
        out[current] = "\n".join(buf)
    return out


def subsection(text: str, heading: str) -> str:
    m = re.search(rf"^#{{2,3}}\s*{re.escape(heading)}(?:\s|$).*$", text, re.M)
    if not m:
        return ""
    start = m.end()
    nxt = re.search(r"^#{2,3}\s", text[start:], re.M)
    return text[start:start + nxt.start()] if nxt else text[start:]


def h2(text: str, prefix: str) -> str:
    for key, value in sections(text).items():
        if key.startswith(f"## {prefix}"):
            return value
    return ""


def tables(block: str) -> list[tuple[list[str], list[list[str]]]]:
    lines = block.splitlines()
    out: list[tuple[list[str], list[list[str]]]] = []
    i = 0
    while i < len(lines) - 1:
        line = lines[i].strip()
        nxt = lines[i + 1].strip()
        if line.startswith("|") and re.match(r"^\|[\s:|-]+\|$", nxt):
            headers = [c.strip() for c in line.strip().strip("|").split("|")]
            rows: list[list[str]] = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append([c.strip() for c in lines[j].strip().strip("|").split("|")])
                j += 1
            out.append((headers, rows))
            i = j
        else:
            i += 1
    return out


def pick_table(block: str, required: list[str]) -> tuple[list[str], list[list[str]]] | None:
    for headers, rows in tables(block):
        joined = " ".join(headers)
        if all(r in joined for r in required):
            return headers, rows
    return None


def cell(row: list[str], headers: list[str], name: str) -> str:
    try:
        i = headers.index(name)
    except ValueError:
        i = next((j for j, h in enumerate(headers) if h.startswith(name)), -1)
    return row[i].strip() if 0 <= i < len(row) else ""


def is_blank(s: str) -> bool:
    s = (s or "").strip()
    return s in {"", "—", "-", "…", "...", "待补", "待确认"} or (s.startswith("{") and s.endswith("}"))


def has_open_gap(s: str) -> bool:
    """True only when a conclusion explicitly leaves a gap open."""
    s = (s or "").strip()
    if not s or s in {"—", "-", "…", "...", "无", "0"}:
        return False
    if re.search(r"(无|0|零)\s*(未接受|未解释|未覆盖)?\s*(个|项)?\s*缺口|缺口\s*[:：]?\s*(0|无|零)\s*(个|项)?", s):
        return False
    return "缺口" in s


def is_p0(s: str) -> bool:
    return bool(re.search(r"(^|[/,，\s])P0([/,，\s]|$)", (s or "").strip(), re.I)) or (s or "").strip().upper() == "P0"


def is_test_disp(s: str) -> bool:
    """处置=测；「不测」不得误入必测集。"""
    s = (s or "").strip()
    if not s or s.startswith("不测"):
        return False
    return s.startswith("测") or s.upper().startswith("TEST")


def source_anchored(s: str) -> bool:
    """原文/依据须有可回指锚点（章节/AC/路由/方法或 A / B 多源）。"""
    t = (s or "").strip()
    if is_blank(t):
        return False
    if SOURCE_ANCHOR_RE.search(t):
        return True
    # 多源常用「主读 / 互补」
    return ("/" in t or "／" in t or "、" in t) and len(t) >= 5


def looks_falsify(scene: str, source: str = "", gap: str = "") -> bool:
    blob = f"{scene} {source} {gap}"
    return bool(FALSIFY_RE.search(blob) or NA_FALSIFY_RE.search(blob))


def is_concrete_int(iid: str) -> bool:
    """具体意图 ID：至少 INT-段-段（如 INT-240-CHK / INT-G240-00）；禁把簇名 INT-240 当台账行。"""
    return bool(re.fullmatch(r"INT-[A-Z0-9]+(?:-[A-Z0-9]+)+", (iid or "").strip()))


def intent_ref_ok(ref: str, intents: dict[str, Any] | set[str]) -> bool:
    """INT 引用可解析：精确命中，或簇前缀能落到台账中的具体 INT-* 子项。"""
    keys = intents.keys() if isinstance(intents, dict) else intents
    ref = (ref or "").strip()
    if not ref:
        return False
    if ref in keys:
        return True
    if any(str(k).startswith(ref + "-") for k in keys):
        return True
    return False


def longest_int_refs(text: str) -> list[str]:
    """提取 INT-*，同起点只保留最长匹配，避免 INT-240-CHK 被拆成 INT-240。"""
    raw = INT_ID_RE.findall(text or "")
    if not raw:
        return []
    # 长前缀优先：若 A 是 B 的前缀则丢 A
    uniq = sorted(set(raw), key=lambda s: (-len(s), s))
    kept: list[str] = []
    for cand in uniq:
        if any(k != cand and k.startswith(cand + "-") for k in uniq):
            continue
        kept.append(cand)
    return kept


def weak_oracle(s: str) -> bool:
    """True = Oracle 不可作为通过依据（空或口头通过）。"""
    t = (s or "").strip()
    return is_blank(t) or bool(WEAK_ORACLE_RE.match(t))


def conditional_acceptor_ok(text: str) -> bool:
    """CONDITIONAL：§4 缺口表须有非空接受人行（禁全文碰巧出现「接受人」）。"""
    block = h2(text, "4.")
    if not block:
        return False
    for headers, rows in tables(block):
        if not any("接受人" in h for h in headers):
            continue
        for row in rows:
            if not row or not row[0] or row[0] in ("类型", "项", "缺口", "—"):
                continue
            if not is_blank(cell(row, headers, "接受人")):
                return True
    return False


def _tokens(s: str) -> set[str]:
    """轻量对账 token：INT/AC/路径/中文词块；过滤过短噪声。"""
    raw = (s or "").strip()
    if not raw:
        return set()
    parts = re.findall(r"[A-Za-z][A-Za-z0-9_-]{1,}|\d+(?:\.\d+)?|[\u4e00-\u9fff]{2,}", raw)
    return {p.lower() for p in parts if p and p.lower() not in {"oracle", "预期", "通过", "失败", "结果"}}


def analysis_aligned(source: str, oracle: str, meta: dict[str, str] | None) -> bool:
    """场景原文/Oracle 与分析台账有可对账交集；无分析行则跳过。

    通用词（状态/页面等）单独命中不算；须 ≥2 个交集，或至少 1 个较长/带锚点 token。
    """
    if not meta:
        return True
    scene_tok = _tokens(f"{source} {oracle}")
    if not scene_tok:
        return False
    analysis_tok = _tokens(
        f"{meta.get('source', '')} {meta.get('oracle', '')} {meta.get('unaccept', '')} {meta.get('intent', '')}"
    )
    if not analysis_tok:
        return True  # 分析行空字段由 coverage 另拦；此处不叠罚
    shared = scene_tok & analysis_tok
    if not shared:
        return False
    weak = {"状态", "页面", "结果", "成功", "失败", "字段", "按钮", "列表", "详情", "接口", "数据", "用户"}
    strong = {t for t in shared if t not in weak and (len(t) >= 3 or any(ch.isdigit() for ch in t) or "-" in t or "_" in t)}
    return len(shared) >= 2 or bool(strong)


def to_int(s: str) -> int:
    m = re.search(r"-?\d+", (s or "").replace(",", ""))
    return int(m.group(0)) if m else 0


def worst_status(old: str, new: str) -> str:
    rank = {"失败": 6, "阻塞": 5, "待实现": 4, "未本轮验证": 3, "未执行": 3, "通过": 2, "不适用": 1, "": 0}
    return new if rank.get(new, 0) >= rank.get(old, 0) else old


def terminal_status(status: str) -> bool:
    return status in {"通过", "失败", "阻塞", "待实现", "不适用"}


def is_current(path: Path) -> bool:
    return not any(part in path.parts for part in ("_archive", ".draft", "evidence", "证据", "资料", "materials"))


def default_project_root(package_root: Path) -> Path:
    for p in (package_root, *package_root.parents):
        if (p / "activeContext.md").is_file():
            return p
    return package_root.parent


def declared_workroot(project_root: Path) -> Path | None:
    for name in ("env-baseline.md", "project-profile.md"):
        f = project_root / name
        if not f.is_file():
            continue
        try:
            m = re.search(r"^\|\s*workroot\s*\|\s*`?([^`|]+?)`?\s*\|", read(f), re.M)
            if m:
                val = m.group(1).strip()
                if val.startswith("默认") or "非标准" in val:
                    continue
                return project_root / val.rstrip("/")
        except Exception:
            pass
    return None


def find_workroot(project_root: Path) -> Path:
    w = declared_workroot(project_root)
    if w:
        return w
    if (project_root / "wf").is_dir():
        return project_root / "docs" / "testing"
    return project_root / "docs"


def declared_current_ver(project_root: Path) -> str | None:
    """Resolve current iteration folder name from baseline / activeContext / INDEX."""
    for name in ("env-baseline.md", "project-profile.md"):
        f = project_root / name
        if not f.is_file():
            continue
        try:
            text = read(f)
            m = re.search(r"^\|\s*当前版本/主题\s*\|\s*`?([^`|]+?)`?\s*\|", text, re.M)
            if m:
                val = m.group(1).strip()
                if val and val not in ("无", "—", "-", "{版本或迭代主题；无则写「无」}"):
                    return val.split("；")[0].strip().strip("`")
        except Exception:
            pass
    ac = project_root / "activeContext.md"
    if ac.is_file():
        try:
            text = read(ac)
            m = re.search(r"(?:当前版本|迭代|ver)\s*[:=：]\s*`?([^\s`|]+)`?", text, re.I)
            if m:
                return m.group(1).strip()
            m = re.search(r"`([^`]+/)?(V?[\w.-]+)/(?:test-plan|test-analysis)\.md`", text)
            if m:
                return (m.group(2) or "").strip() or None
        except Exception:
            pass
    return None


def find_test_root(project_root: Path) -> Path:
    """Iteration folder containing test-plan/analysis; fallback workroot for legacy flat layout."""
    wr = find_workroot(project_root)
    if (wr / "test-plan.md").is_file() or (wr / "test-analysis.md").is_file():
        return wr
    ver = declared_current_ver(project_root)
    if ver:
        cand = wr / ver
        if cand.is_dir() and (
            (cand / "test-plan.md").is_file() or (cand / "test-analysis.md").is_file()
        ):
            return cand
    # Prefer a single child dir that holds the plan
    hits = [
        p
        for p in wr.iterdir()
        if p.is_dir() and not p.name.startswith(("_", ".")) and (p / "test-plan.md").is_file()
    ] if wr.is_dir() else []
    if len(hits) == 1:
        return hits[0]
    return wr


def resolve_evidence(record: Path, test_root: Path, evidence: str) -> bool:
    ev = (evidence or "").strip().strip("`").strip()
    if not ev or ev in ("—", "-", "无"):
        return False
    p = Path(ev)
    if p.is_absolute():
        return p.exists()
    for base in (record.parent, record.parent.parent, test_root, test_root.parent):
        if (base / ev).exists():
            return True
    name = p.name
    return bool(name) and any(x.is_file() and x.name == name for x in test_root.rglob(name))


def has_matrix_marker(s: str) -> bool:
    t = (s or "").strip()
    return bool(re.search(r"INT-[A-Z0-9-]+|SC-[A-Z0-9-]+|SMK-[A-Z0-9-]+|N/A|不适用", t, re.I))


# ---------- analysis (intent + coverage matrices) ----------
def parse_analysis_v2(path: Path) -> dict[str, Any]:
    text = read(path)
    issues: list[str] = []
    intents: dict[str, dict[str, str]] = {}
    p0_ids: set[str] = set()
    p1_ids: set[str] = set()
    p2_ids: set[str] = set()
    if not re.search(r"analysis_format\**\s*[:：]\s*`?intent-v1`?", text[:4000], re.I):
        issues.append("缺 analysis_format=intent-v1")
    for key in ("## 0.", "## 1.", "## 2.", "## 3.", "## 4.", "## 5.", "## 6."):
        if key not in text:
            issues.append(f"分析缺 {key} 标题")

    # §1 source + chapter + basis
    block1 = h2(text, "1.")
    # Shape A（模板）：来源/总数/已映射/N/A/缺口
    # Shape B（迭代压缩）：来源/…/设计点行(提取)/已映射策略/缺口 — 仍须可核对合计与缺口
    t_src = pick_table(block1, ["来源", "总数", "已映射", "N/A", "缺口"])
    t_src_b = None if t_src else pick_table(block1, ["来源", "缺口"])
    if t_src:
        headers, rows = t_src
        for row in rows:
            if not row or not row[0] or row[0] in ("来源", "—"):
                continue
            for name in ("总数", "已映射", "N/A", "缺口"):
                if is_blank(cell(row, headers, name)):
                    issues.append(f"§1「{row[0]}」缺 {name}")
            gap = cell(row, headers, "缺口")
            gap_n = to_int(gap)
            if gap_n > 0 and not re.search(r"接受|已接受|accepted", gap, re.I):
                issues.append(f"§1「{row[0]}」仍有未接受缺口 {gap}")
            total = to_int(cell(row, headers, "总数"))
            mapped = to_int(cell(row, headers, "已映射"))
            na = to_int(cell(row, headers, "N/A"))
            if total and mapped > total:
                issues.append(f"§1「{row[0]}」已映射 {mapped} > 总数 {total}")
            if total and mapped + na + gap_n != total:
                issues.append(f"§1「{row[0]}」总数 {total} ≠ 已映射 {mapped} + N/A {na} + 缺口 {gap_n}")
    elif t_src_b:
        headers, rows = t_src_b
        # 压缩表：须有可计数列（设计点行/提取/总数 任一）+ 映射策略/已映射 + 缺口
        count_h = next((h for h in headers if re.search(r"总数|设计点行|提取", h)), "")
        map_h = next((h for h in headers if re.search(r"已映射|映射策略", h)), "")
        if not count_h or not map_h:
            issues.append("§1 来源盘点表缺计数列或映射列（需 总数/设计点行 + 已映射/映射策略 + 缺口）")
        for row in rows:
            if not row or not row[0] or row[0] in ("来源", "—"):
                continue
            gap = cell(row, headers, "缺口")
            if is_blank(gap):
                issues.append(f"§1「{row[0]}」缺 缺口")
            gap_n = to_int(gap)
            if gap_n > 0 and not re.search(r"接受|已接受|accepted", gap, re.I):
                issues.append(f"§1「{row[0]}」仍有未接受缺口 {gap}")
            total = to_int(cell(row, headers, count_h)) if count_h else 0
            mapped_raw = cell(row, headers, map_h) if map_h else ""
            mapped = to_int(mapped_raw)
            if mapped == 0 and mapped_raw and not re.match(r"^\d+", mapped_raw.strip()):
                # 非数字映射策略（如 §2.1.1 DP-240）视为已映射=总数（缺口另计）
                mapped = total if total and gap_n == 0 else mapped
            if total and mapped > total:
                issues.append(f"§1「{row[0]}」已映射 {mapped} > 总数 {total}")
    else:
        issues.append("§1 来源盘点表缺失（需 来源/总数/已映射/N/A/缺口，或压缩表：来源/设计点行/映射策略/缺口）")

    chapter_refs: list[tuple[str, str]] = []
    t_ch = pick_table(block1, ["章节/标题", "可测内容", "落点"])
    if not t_ch:
        issues.append("§1.2 章节回执缺失（需 章节/标题/可测内容/意图/落点）")
    else:
        headers, rows = t_ch
        for row in rows:
            if not row or not row[0] or row[0] in ("章节/标题", "—"):
                continue
            for name in ("可测内容", "意图", "落点"):
                if is_blank(cell(row, headers, name)):
                    issues.append(f"§1.2「{row[0]}」缺 {name}")
            intent_text = cell(row, headers, "意图")
            if not (INT_ID_RE.search(intent_text) or re.search(r"无|N/A|不适用", intent_text)):
                issues.append(f"§1.2「{row[0]}」意图列须写 INT-* 或 无/N/A+理由")
            for ref in longest_int_refs(intent_text):
                chapter_refs.append((row[0], ref))

    t_basis = pick_table(block1, ["依据ID", "来源", "意图ID", "结论"])
    basis_refs: list[tuple[str, str]] = []
    if not t_basis:
        issues.append("§1.3 依据覆盖表缺失（需 依据ID/来源/意图ID/结论）")
    else:
        headers, rows = t_basis
        basis_text = " ".join(" ".join(r) for r in rows)
        for row in rows:
            if not row or not row[0] or row[0] in ("依据ID", "—"):
                continue
            for name in ("来源", "意图ID", "结论"):
                if is_blank(cell(row, headers, name)):
                    issues.append(f"§1.3「{row[0]}」缺 {name}")
            verdict = cell(row, headers, "结论")
            if verdict and not (verdict.startswith("已覆盖") or verdict.startswith("N/A") or verdict.startswith("不适用")):
                issues.append(f"§1.3「{row[0]}」结论不可判定：{verdict}")
            if verdict.startswith("已覆盖"):
                basis_refs.append((row[0], cell(row, headers, "意图ID")))
                page = cell(row, headers, "页面/路由/状态")
                api = cell(row, headers, "接口/字段/权限/错误码")
                if is_blank(page) and is_blank(api):
                    issues.append(f"§1.3「{row[0]}」页面/路由 与 接口/字段 至少填一处")

    # §2 intent ledger
    block2 = h2(text, "2.")
    t_int = pick_table(block2, ["INT", "来源", "意图", "Oracle", "优先级", "处置"])
    if not t_int:
        issues.append("§2.1 意图台账缺失（需 INT/来源/意图/Oracle/优先级/处置）")
    else:
        headers, rows = t_int
        for row in rows:
            if not row or not row[0] or row[0] in ("INT", "—"):
                continue
            iid = row[0].strip()
            if not is_concrete_int(iid):
                issues.append(f"§2.1 台账行 ID 须为具体 INT-*-*（禁簇名）：{iid}")
                continue
            intents[iid] = {
                "pri": cell(row, headers, "优先级"),
                "disp": cell(row, headers, "处置"),
                "owner": cell(row, headers, "接受人"),
                "source": cell(row, headers, "来源"),
                "intent": cell(row, headers, "意图"),
                "oracle": cell(row, headers, "Oracle"),
                "unaccept": cell(row, headers, "不可接受失败"),
            }
            for name in ("来源", "意图", "Oracle", "优先级", "处置"):
                if is_blank(cell(row, headers, name)):
                    issues.append(f"§2.1 {iid} 缺 {name}")
            if weak_oracle(cell(row, headers, "Oracle")):
                issues.append(f"§2.1 {iid} Oracle 过弱（须可观测断言，禁「通过/正常」）")
            pri = cell(row, headers, "优先级")
            disp = cell(row, headers, "处置")
            if is_p0(pri):
                p0_ids.add(iid)
                if is_blank(cell(row, headers, "不可接受失败")):
                    issues.append(f"§2.1 {iid} P0 缺不可接受失败")
            elif "P1" in pri.upper():
                p1_ids.add(iid)
            elif "P2" in pri.upper():
                p2_ids.add(iid)
            else:
                issues.append(f"§2.1 {iid} 优先级须为 P0/P1/P2：{pri or '空'}")
            if "N/A" in disp.upper() or "不适用" in disp:
                if is_blank(cell(row, headers, "接受人")):
                    issues.append(f"§2.1 {iid} N/A 缺接受人")
                if is_p0(pri):
                    issues.append(f"§2.1 {iid} P0 不得 N/A（P0 必须执行；确不适用请降级并写 §4 接受人）")
        if not intents:
            issues.append("§2.1 意图台账无数据行")

    # 链接 SSOT = §2.1 意图台账 only；设计点只映射到台账，不得当第二套台账
    t_ac = pick_table(block2, ["来源条目", "类型", "意图", "处置"])

    for basis_id, vp in basis_refs:
        for ref in longest_int_refs(vp) or [
            x.strip("` ") for x in re.split(r"[/,，、;\s]+", vp) if x.strip("` ")
        ]:
            if ref.startswith(("N/A", "不适用", "—")):
                continue
            if not INT_ID_RE.fullmatch(ref):
                continue
            if not intent_ref_ok(ref, intents):
                issues.append(f"§1.3「{basis_id}」意图ID {ref} 不在 §2.1 台账")

    for ch, ref in chapter_refs:
        if not intent_ref_ok(ref, intents):
            issues.append(f"§1.2「{ch}」意图 {ref} 不在 §2.1 台账")

    if not t_ac:
        issues.append("§2.1 AC/设计点账本缺失（需 来源条目/类型/意图/处置）")
    else:
        headers, rows = t_ac
        for row in rows:
            if not row or not row[0] or row[0] in ("来源条目", "—", "DP"):
                continue
            ac_intent = cell(row, headers, "意图") or cell(row, headers, "意图簇")
            for name in ("类型", "处置"):
                if is_blank(cell(row, headers, name)):
                    issues.append(f"§2.1.1「{row[0]}」缺 {name}")
            if is_blank(ac_intent):
                issues.append(f"§2.1.1「{row[0]}」缺 意图/意图簇")
            disp = cell(row, headers, "处置")
            if ("N/A" in disp.upper() or "不适用" in disp) and is_blank(cell(row, headers, "缺口/接受人")):
                issues.append(f"§2.1.1「{row[0]}」N/A 缺接受人")
            if disp.startswith("测") and not disp.startswith("不测") and not INT_ID_RE.search(ac_intent):
                issues.append(f"§2.1.1「{row[0]}」处置=测 但未写 INT")
            for ref in longest_int_refs(ac_intent):
                if ref in intents:
                    continue
                if not is_concrete_int(ref):
                    issues.append(
                        f"§2.1.1「{row[0]}」意图写了簇名 {ref}，须改为具体 INT-*-* 并在 §2.1 建台账行"
                    )
                else:
                    issues.append(f"§2.1.1「{row[0]}」意图 {ref} 不在 §2.1 台账（须先建 Oracle/优先级行）")
            refs = longest_int_refs(ac_intent)
            if disp.startswith("测") and not disp.startswith("不测") and refs:
                mapped = [intents[r] for r in refs if r in intents]
                if mapped and not any(is_test_disp(m.get("disp", "")) for m in mapped):
                    issues.append(
                        f"§2.1.1「{row[0]}」处置=测 但映射的 INT 在 §2.1 均非处置=测（台账处置矛盾）"
                    )

    # §2.2 coverage matrix
    block22 = subsection(text, "2.2")
    t22 = pick_table(block22, ["模块/流程", "负向/禁止"])
    if not t22:
        issues.append("§2.2 模块×面矩阵缺失或表头不可读")
    else:
        headers, rows = t22
        for col in ("主路径", "状态/分支", "边界/异常", "权限/数据域", "并发/幂等", "审计/历史", "通知/附件", "迁移/兼容", "非功能", "视觉/UI", "集成/状态轴", "计算/算例", "负向/禁止"):
            if not any(col in h for h in headers):
                issues.append(f"§2.2 覆盖矩阵缺列「{col}」")
        for row in rows:
            if not row or not row[0] or row[0] in ("模块/流程", "—"):
                continue
            for j, val in enumerate(row[1:], 1):
                if is_blank(val):
                    issues.append(f"§2.2「{row[0]}」第{j}列为空")
                elif not has_matrix_marker(val):
                    issues.append(f"§2.2「{row[0]}」第{j}列未写 INT/场景 或 N/A+依据")

    # §2.3 method matrix
    block23 = subsection(text, "2.3")
    t23 = pick_table(block23, ["规则/计算", "算例"])
    if not t23:
        issues.append("§2.3 方法×规则矩阵缺失或表头不可读")
    else:
        headers, rows = t23
        for col in ("等价类", "边界", "判定表/组合", "状态迁移", "场景", "算例", "意图"):
            if not any(col in h for h in headers):
                issues.append(f"§2.3 方法矩阵缺列「{col}」")
        for row in rows:
            if not row or not row[0] or row[0] in ("规则/计算", "—"):
                continue
            for j, val in enumerate(row[1:], 1):
                if is_blank(val):
                    issues.append(f"§2.3「{row[0]}」第{j}列为空")
                elif not has_matrix_marker(val):
                    issues.append(f"§2.3「{row[0]}」第{j}列未写 INT 或 N/A+依据")

    # §2.4 detail matrix
    block24 = subsection(text, "2.4")
    t24 = pick_table(block24, ["细节维", "适用", "意图/场景"])
    if not t24:
        issues.append("§2.4 细节设计覆盖表缺失（需 细节维/适用/意图/场景）")
    else:
        headers, rows = t24
        seen = {row[0].split()[0] for row in rows if row and row[0] and row[0] not in ("细节维", "—")}
        for dim in [f"D{i:02d}" for i in range(1, 14)] + ["S6", "S7", "S11"]:
            if dim not in seen:
                issues.append(f"§2.4 缺细节维 {dim}")
        for row in rows:
            if not row or not row[0] or row[0] in ("细节维", "—"):
                continue
            apply = cell(row, headers, "适用")
            ref = cell(row, headers, "意图/场景") or cell(row, headers, "意图")
            gap = cell(row, headers, "缺口或依据") or cell(row, headers, "缺口/理由")
            if apply not in ("是", "否"):
                issues.append(f"§2.4「{row[0]}」适用未填 是/否")
            elif apply == "是" and is_blank(ref):
                issues.append(f"§2.4「{row[0]}」适用但缺意图/场景")
            elif apply == "否" and is_blank(gap):
                issues.append(f"§2.4「{row[0]}」不适用但缺依据")

    # §3 risk
    block3 = h2(text, "3.")
    t_risk = pick_table(block3, ["RISK", "不可接受失败", "优先级"])
    if not t_risk:
        issues.append("§3 风险清单缺失或表头不可读")
    else:
        headers, rows = t_risk
        for row in rows:
            if not row or not row[0] or row[0] in ("RISK", "—"):
                continue
            for name in ("不可接受失败", "优先级"):
                if is_blank(cell(row, headers, name)):
                    issues.append(f"§3 {row[0]} 缺 {name}")
    t_scan = pick_table(block3, ["类别", "是否适用"])
    if not t_scan:
        issues.append("§3.1 风险扫描表缺失")
    else:
        headers, rows = t_scan
        seen = 0
        for row in rows:
            if not row or not row[0] or row[0] in ("类别", "—"):
                continue
            seen += 1
            if cell(row, headers, "是否适用") not in ("是", "否"):
                issues.append(f"§3.1「{row[0]}」是否适用须填 是/否")
        if seen < 8:
            issues.append(f"§3.1 风险扫描仅 {seen} 类")

    # §5 impact + core chains
    block5 = h2(text, "5.")
    t_imp = pick_table(block5, ["层级", "模块/接口/数据/事件"])
    levels = {"直接改动", "邻接模块", "上游供给", "下游消费", "共享数据", "事件/异步", "回归锚点"}
    if not t_imp:
        issues.append("§5.1 影响面矩阵缺失或表头不可读")
    else:
        headers, rows = t_imp
        got_levels = {cell(row, headers, "层级") for row in rows if row and row[0] not in ("层级", "—")}
        for lv in levels:
            if lv not in got_levels:
                issues.append(f"§5.1 影响面缺层级「{lv}」（不适用写 N/A+依据+接受人）")
        for row in rows:
            if not row or not row[0] or row[0] in ("层级", "—"):
                continue
            for name in ("模块/接口/数据/事件", "依据", "受影响意图", "覆盖/回归", "责任人"):
                if is_blank(cell(row, headers, name)):
                    issues.append(f"§5.1「{row[0]}」缺 {name}")

    t_core = pick_table(block5, ["链路 ID", "关键步骤"])
    if not t_core:
        issues.append("§5.3 核心链路表缺失或表头不可读")
    else:
        headers, rows = t_core
        for row in rows:
            if not row or not row[0] or row[0] in ("链路 ID", "—"):
                continue
            for name in ("业务目标", "入口", "关键步骤", "关联意图", "P0 冒烟", "状态"):
                if is_blank(cell(row, headers, name)):
                    issues.append(f"§5.3「{row[0]}」缺 {name}")
            status = cell(row, headers, "状态")
            if status not in ("已覆盖", "N/A", "不适用"):
                issues.append(f"§5.3「{row[0]}」状态未闭环：{status or '空'}")

    # §6 sufficiency
    t6 = pick_table(h2(text, "6."), ["检查", "通过条件"])
    if not t6:
        issues.append("§6 覆盖充分性表缺失（需 检查/通过条件/结论）")
    else:
        headers, rows = t6
        for row in rows:
            if not row or not row[0] or row[0] in ("检查", "—"):
                continue
            conclusion = row[2].strip() if len(row) > 2 else ""
            if is_blank(conclusion) or has_open_gap(conclusion):
                issues.append(f"§6「{row[0]}」未闭环：{conclusion or '空'}")

    return {"path": str(path), "issues": issues, "intents": intents,
            "ids": set(intents.keys()), "p0_ids": p0_ids, "p1_ids": p1_ids, "p2_ids": p2_ids}


# ---------- plan ----------
def parse_plan(path: Path) -> dict[str, Any]:
    text = read(path)
    issues: list[str] = []
    tier = "lite" if re.search(r"plan_tier\s*=\s*lite|测试计划（轻量）", text[:3000], re.I) else "full"
    if not re.search(r"plan_format\**\s*[:：]\s*`?schedule-v1`?", text[:4000], re.I):
        issues.append("缺 plan_format=schedule-v1")
    for key in (("## 0.", "## 1.", "## 2.", "## 3.", "## 4.") if tier == "lite" else ("## 0.", "## 1.", "## 2.", "## 3.", "## 4.", "## 5.", "## 6.")):
        if key not in text:
            issues.append(f"计划缺 {key} 标题")
    if "test-analysis.md" not in text:
        issues.append("计划未引用 test-analysis.md")
    if "env-baseline.md" not in text:
        issues.append("计划未引用 env-baseline.md（环境基线）")
    if not re.search(r"suite", text, re.I):
        issues.append("计划缺 suite 声明")
    if "接口" in text and not re.search(r"depth", text, re.I):
        issues.append("计划含接口但缺 depth 声明")
    if tier != "lite":
        block4 = h2(text, "4.")
        if block4 and not all(k in block4 for k in ("P0", "缺口", "准出")):
            issues.append("§4 准入/准出缺 P0/缺口/准出关键口径")
        t_track = pick_table(h2(text, "2."), ["轨道", "纳入"])
        if not t_track:
            issues.append("§2 轨道表缺失（需 轨道/纳入）")
        elif not any(row and row[0] and row[0] not in ("轨道", "—") for row in t_track[1]):
            issues.append("§2 轨道表无数据行")
        block3 = h2(text, "3.")
        t_round = pick_table(block3, ["轮次", "目标"])
        if not t_round:
            issues.append("§3 轮次表缺失（需 轮次/目标）")
        elif not any(row and row[0] and row[0] not in ("轮次", "—") for row in t_round[1]):
            issues.append("§3 轮次表无数据行")
        t_batch = pick_table(block3, ["批次", "执行形态"])
        if not t_batch:
            issues.append("§3.1 批次表缺失（需 批次/执行形态；单模块可一行直跑+串行）")
        else:
            headers, rows = t_batch
            data_rows = [row for row in rows if row and row[0] and row[0] not in ("批次", "—")]
            if not data_rows:
                issues.append("§3.1 批次表无数据行")
            # 扇出只在「同一并行波次」内计：并行组=串行/空 → 各行独立，不跨批误伤
            wave: dict[str, list[tuple[str, str, str]]] = {}
            for row in data_rows:
                mode = cell(row, headers, "执行形态")
                if is_blank(mode):
                    issues.append(f"§3.1「{row[0]}」缺执行形态")
                    continue
                pg = (cell(row, headers, "并行组") or "").strip()
                iso = cell(row, headers, "隔离套") or cell(row, headers, "隔离套/账号/写域")
                if re.search(r"PG[-_]?\w*", pg or "", re.I):
                    if is_blank(iso) or re.fullmatch(r"串行|共享|共享[·.]?串行", (iso or "").strip()):
                        issues.append(f"§3.1「{row[0]}」有 {pg} 但隔离套不可核验（须互斥账号/profile/port/写域）")
                if re.search(r"脚本", mode) and not re.search(r"直跑|模块子代理|拆分", mode):
                    continue
                mod = cell(row, headers, "模块/域") or cell(row, headers, "模块")
                if is_blank(mod):
                    continue
                # 串行/空并行组：每行独自一波，允许直跑
                if not pg or re.fullmatch(r"串行|—|-|独立", pg):
                    wave_key = f"serial::{row[0]}"
                else:
                    wave_key = pg
                wave.setdefault(wave_key, []).append((str(row[0]), mod.strip(), mode.strip()))
            for wkey, fanout in wave.items():
                if wkey.startswith("serial::"):
                    continue
                uniq_mods = {m for _, m, _ in fanout}
                if len(uniq_mods) < 2:
                    continue
                for bid, _mod, mode in fanout:
                    if not re.search(r"模块子代理|拆分", mode):
                        issues.append(
                            f"§3.1「{bid}」同并行组({wkey})≥2 装填模块时执行形态应为模块子代理/拆分（当前={mode}）"
                        )
    else:
        b3 = h2(text, "3.")
        if not b3 or not all(k in b3 for k in ("轮次", "准入", "准出")):
            issues.append("轻量计划 §3 缺轮次/准入/准出")
        elif not re.search(r"串行|并行|直跑|模块子代理|拆分|脚本|PG-", b3):
            issues.append("轻量计划 §3 缺批次/并行口径（至少写直跑/串行）")
    if tier != "lite":
        t_imp = pick_table(h2(text, "1."), ["类型", "范围/链路", "覆盖/回归轮次"])
        if not t_imp:
            issues.append("§1.4 影响面/核心链路摘要缺失（需 类型/范围/链路/覆盖轮次）")
        else:
            headers, rows = t_imp
            got = {cell(row, headers, "类型") for row in rows if row and row[0] not in ("类型", "—")}
            for lv in ("直接改动", "邻接", "上游", "下游", "共享数据/权限", "核心链路"):
                if lv not in got:
                    issues.append(f"§1.4 缺「{lv}」行（不适用写 N/A+依据）")
        t_env = None
        for headers, rows in tables(h2(text, "2.")):
            if [h.strip() for h in headers] == ["项", "值"]:
                t_env = (headers, rows)
                break
        if not t_env:
            issues.append("§2.2 环境基线表缺失（需 项/值 表：环境基线/环境/构建/账号/数据）")
        else:
            headers, rows = t_env
            kv = {row[0].strip(): (row[1].strip() if len(row) > 1 else "") for row in rows if row and row[0]}
            for label in ("环境基线", "环境 / BaseURL", "构建 / 版本", "账号 / 角色 / 数据域", "数据 / 造数", "开跑前核验"):
                if is_blank(kv.get(label, "")):
                    issues.append(f"§2.2 环境基线缺「{label}」")
    if tier == "full" and "探索式" in text:
        # T1+ 计划需有章程行或 N/A；仅做结构提示，语义由计划门确认。
        if "S6" not in text or "S7" not in text or "S11" not in text:
            issues.append("§3.2 探索式/§4.3 功能收口探针缺 S6/S7/S11")
    if tier == "full":
        t_probe = pick_table(block4, ["轴", "最小探针", "着落"])
        if not t_probe:
            issues.append("§4.3 功能收口探针表缺失（需 轴/最小探针/着落）")
        else:
            headers, rows = t_probe
            for axis in ("S6", "S7", "S11"):
                hit = next((row for row in rows if cell(row, headers, "轴").strip().startswith(axis)), None)
                if hit is None:
                    issues.append(f"§4.3 缺 {axis} 收口行")
                elif is_blank(cell(hit, headers, "着落")):
                    issues.append(f"§4.3 {axis} 缺着落（写 INT/章程/不测+接受人）")
    return {"path": str(path), "issues": issues, "tier": tier}


# ---------- records ----------
def find_records(test_root: Path, scope: str | None = None) -> list[Path]:
    out: list[Path] = []
    if not test_root.is_dir():
        return out
    for p in test_root.rglob("*.md"):
        if not is_current(p) or "执行记录" not in p.name:
            continue
        if scope and not any(t in str(p).replace("\\", "/") for t in [x.strip() for x in re.split(r"[,;|]", scope) if x.strip()]):
            continue
        out.append(p)
    return sorted(set(out))


def parse_record(path: Path, test_root: Path, analysis: dict[str, Any] | None = None) -> dict[str, Any]:
    text = read(path)
    issues: list[str] = []
    counts = {s: 0 for s in STATUSES}
    by_pri = {"P0": 0, "P1": 0, "P2": 0, "其他": 0}
    by_pri_status: dict[str, dict[str, int]] = {p: {s: 0 for s in STATUSES} for p in by_pri}
    intent_ids: set[str] = set()
    intent_results: dict[str, str] = {}
    intent_priority: dict[str, str] = {}
    intent_falsify: dict[str, bool] = {}
    intent_misaligned: list[str] = []
    orphan_intents: list[str] = []
    p0_fail: list[str] = []
    missing_evidence: list[str] = []
    blocked_bad: list[str] = []
    analysis_ids = set((analysis or {}).get("ids") or [])
    analysis_intents = (analysis or {}).get("intents") or {}

    if not (re.search(r"record_format\**\s*[:：]\s*`?intent-v1`?", text[:4000], re.I) or "场景与结果" in text):
        issues.append(f"{path.name}: 非执行记录格式")
    if "env-baseline" not in text:
        issues.append(f"{path.name}: 未引用 env-baseline.md（环境基线）")
    if "原文对账" not in text:
        issues.append(f"{path.name}: 缺 §0 原文对账行（开跑按原文目录对账分析漏项）")

    table = None
    for headers, rows in tables(text):
        if "SC" in headers and "结果" in " ".join(headers):
            table = (headers, rows)
            break
    if not table:
        issues.append(f"{path.name}: 未找到场景表（需 SC/INT/场景/结果/证据）")
    else:
        headers, rows = table
        is_api = any("EP" in h for h in headers)
        if not is_api and not any("步骤" in h for h in headers):
            issues.append(f"{path.name}: 缺「步骤」列（功能执行记录须 3～7 短步，供第二人复核）")
        seen = 0
        for row in rows:
            if not row or not row[0] or row[0] in ("SC", "—"):
                continue
            seen += 1
            sc = row[0].strip()
            source = cell(row, headers, "原文/依据") or cell(row, headers, "原文/契约")
            scene = cell(row, headers, "场景")
            steps = cell(row, headers, "步骤")
            oracle = (
                cell(row, headers, "预期/Oracle")
                or cell(row, headers, "Oracle")
                or cell(row, headers, "预期")
            )
            if is_blank(source):
                issues.append(f"{path.name}: {sc} 缺原文/依据（执行仍须对照原始文档）")
            elif not source_anchored(source):
                issues.append(f"{path.name}: {sc} 原文/依据过粗（须章节/AC/路由/接口或主读/互补，禁只写文档名）")
            status = cell(row, headers, "结果")
            evidence = cell(row, headers, "证据")
            defect = cell(row, headers, "缺陷")
            pri = cell(row, headers, "优先级")
            actual = cell(row, headers, "实际/差异") or cell(row, headers, "实际")
            intent = cell(row, headers, "INT/AC") or cell(row, headers, "INT")
            if not INT_ID_RE.search(intent):
                issues.append(f"{path.name}: {sc} 缺 INT-* 意图")
            if status in ("失败", "待实现") and is_blank(defect):
                issues.append(f"{path.name}: {sc} {status} 缺缺陷号/处置（须入库或拟提交，禁失败无账）")
            if not is_api and status in ("通过", "失败", "阻塞", "待实现"):
                if is_blank(steps):
                    issues.append(f"{path.name}: {sc} 缺步骤（执行记录须可复核，3～7 短步）")
                else:
                    n_steps = len(re.findall(r"\d+\s*[.、)）]", steps)) or steps.count("→") + 1
                    if n_steps < 2:
                        issues.append(f"{path.name}: {sc} 步骤过少（至少 2 个动作；建议 3～7）")
            if status == "通过" and weak_oracle(oracle):
                issues.append(f"{path.name}: {sc} 通过但 Oracle 过弱/缺失（须对照原文/分析的可观测断言，禁「通过/正常」）")
            for m in INT_ID_RE.findall(intent):
                intent_ids.add(m)
                old = intent_results.get(m, "")
                intent_results[m] = worst_status(old, status)
                if is_p0(pri):
                    intent_priority[m] = "P0"
                if looks_falsify(scene, source, oracle):
                    intent_falsify[m] = True
                if analysis_ids and m not in analysis_ids:
                    orphan_intents.append(f"{sc}:{m}")
                elif status == "通过" and m in analysis_intents and not analysis_aligned(source, oracle, analysis_intents.get(m)):
                    intent_misaligned.append(f"{sc}:{m}")
            if status not in STATUSES:
                issues.append(f"{path.name}: {sc} 结果不可识别：{status or '空'}")
                continue
            counts[status] += 1
            key = "P0" if is_p0(pri) else ("P1" if "P1" in pri.upper() else ("P2" if "P2" in pri.upper() else "其他"))
            by_pri[key] += 1
            by_pri_status[key][status] += 1
            if status in FAIL_STATUSES:
                if is_blank(evidence):
                    missing_evidence.append(f"{sc}:缺证据")
                elif not resolve_evidence(path, test_root, evidence):
                    missing_evidence.append(f"{sc}:证据不存在 {evidence}")
                if status == "阻塞" and not re.search(r"尝试|恢复|卡点|穷尽", actual or "", re.I):
                    blocked_bad.append(f"{sc}:阻塞缺已尝试/恢复条件")
            if key == "P0" and status in ("失败", "阻塞", "待实现", "未执行", "未本轮验证"):
                p0_fail.append(f"{sc}:{status}")
            if key == "P0" and status == "通过":
                if is_blank(evidence):
                    missing_evidence.append(f"{sc}:P0 通过缺证据")
                elif not resolve_evidence(path, test_root, evidence):
                    missing_evidence.append(f"{sc}:P0 通过证据不存在 {evidence}")
        if seen == 0:
            issues.append(f"{path.name}: 场景表无数据行")

    # 执行记录 §3/§4 的意图结论表（若存在，与场景表双向核对）
    itable = None
    for headers, rows in tables(text):
        joined = " ".join(headers)
        if "INT" in headers and "结论" in joined and "SC" not in headers:
            itable = (headers, rows)
            break
    if itable:
        headers, rows = itable
        for row in rows:
            if not row or not row[0] or row[0] in ("INT", "—"):
                continue
            iid = row[0].strip()
            if not INT_ID_RE.fullmatch(iid):
                continue
            status = cell(row, headers, "结论")
            pri = cell(row, headers, "优先级")
            gap = cell(row, headers, "缺口/接受人") or cell(row, headers, "缺口") or cell(row, headers, "接受人")
            if looks_falsify("", "", gap):
                intent_falsify[iid] = True
            if status not in STATUSES:
                issues.append(f"{path.name}: 意图 {iid} 结论不可识别：{status or '空'}")
                continue
            intent_ids.add(iid)
            intent_results[iid] = worst_status(intent_results.get(iid, ""), status)
            if is_p0(pri):
                intent_priority[iid] = "P0"
                if status in ("失败", "阻塞", "待实现", "未执行", "未本轮验证"):
                    p0_fail.append(f"{iid}:{status}")

    return {"path": str(path), "issues": issues, "counts": counts, "by_pri": by_pri,
            "by_pri_status": by_pri_status, "intent_ids": intent_ids,
            "intent_results": intent_results, "intent_priority": intent_priority,
            "intent_falsify": intent_falsify,
            "intent_misaligned": intent_misaligned, "orphan_intents": orphan_intents,
            "p0_fail": p0_fail, "missing_evidence": missing_evidence, "blocked_bad": blocked_bad}


def aggregate(records: list[Path], test_root: Path, analysis: dict[str, Any] | None = None) -> dict[str, Any]:
    counts = {s: 0 for s in STATUSES}
    by_pri = {"P0": 0, "P1": 0, "P2": 0, "其他": 0}
    by_pri_status: dict[str, dict[str, int]] = {p: {s: 0 for s in STATUSES} for p in by_pri}
    issues: list[str] = []
    intent_ids: set[str] = set()
    intent_results: dict[str, str] = {}
    intent_priority: dict[str, str] = {}
    intent_falsify: dict[str, bool] = {}
    intent_misaligned: list[str] = []
    orphan_intents: list[str] = []
    p0_fail: list[str] = []
    missing_evidence: list[str] = []
    blocked_bad: list[str] = []
    for rec in records:
        p = parse_record(rec, test_root, analysis)
        issues += p["issues"]
        for k in counts:
            counts[k] += p["counts"].get(k, 0)
        for k in by_pri:
            by_pri[k] += p["by_pri"].get(k, 0)
        for pri, st in p["by_pri_status"].items():
            for s, n in st.items():
                by_pri_status[pri][s] += n
        intent_ids |= p["intent_ids"]
        for iid, status in p["intent_results"].items():
            intent_results[iid] = worst_status(intent_results.get(iid, ""), status)
        intent_priority.update(p["intent_priority"])
        for iid, flag in p.get("intent_falsify", {}).items():
            if flag:
                intent_falsify[iid] = True
        intent_misaligned += p.get("intent_misaligned", [])
        orphan_intents += p.get("orphan_intents", [])
        p0_fail += p["p0_fail"]
        missing_evidence += p["missing_evidence"]
        blocked_bad += p["blocked_bad"]
    p0_no_falsify = sorted(
        iid for iid, pri in intent_priority.items()
        if pri == "P0"
        and intent_results.get(iid) == "通过"
        and not intent_falsify.get(iid)
    )
    return {"counts": counts, "by_pri": by_pri, "by_pri_status": by_pri_status, "issues": issues,
            "intent_ids": intent_ids, "intent_results": intent_results, "intent_priority": intent_priority,
            "intent_falsify": intent_falsify, "p0_no_falsify": p0_no_falsify,
            "intent_misaligned": sorted(set(intent_misaligned)),
            "orphan_intents": sorted(set(orphan_intents)),
            "p0_fail": p0_fail, "missing_evidence": missing_evidence, "blocked_bad": blocked_bad}


# ---------- report ----------
def parse_verdict(text: str) -> tuple[str, str]:
    m = re.search(r"准出评估\s*[|｜:：]\s*\**\s*(通过|有条件通过|不通过|阻塞|PASS|CONDITIONAL|FAIL|BLOCKED)", text, re.I)
    if m:
        raw = m.group(1).upper()
        return {"通过": "PASS", "PASS": "PASS", "有条件通过": "CONDITIONAL", "CONDITIONAL": "CONDITIONAL",
                "不通过": "FAIL", "FAIL": "FAIL", "阻塞": "BLOCKED", "BLOCKED": "BLOCKED"}[raw], ""
    m = re.search(r"verdict\s*=\s*(PASS|CONDITIONAL|FAIL|BLOCKED)", text, re.I)
    if m:
        return m.group(1).upper(), ""
    return "", "未找到准出评估/verdict"


def stats_from_report(text: str) -> dict[str, dict[str, int]] | None:
    block = h2(text, "2.")
    t = pick_table(block, ["优先级", "场景数", "通过", "失败"])
    if not t:
        return None
    headers, rows = t
    out: dict[str, dict[str, int]] = {}
    for row in rows:
        if not row or not row[0] or row[0] in ("优先级", "—"):
            continue
        key = "P0" if is_p0(row[0]) else ("P1" if "P1" in row[0].upper() else ("P2" if "P2" in row[0].upper() else "其他"))
        if any(x in row[0] for x in ("合计", "总计")):
            continue
        out[key] = {name: to_int(cell(row, headers, name)) for name in ("场景数", "通过", "失败", "阻塞", "待实现", "N/A", "未执行", "未本轮验证")}
    return out


def intent_stats_from_report(text: str) -> dict[str, dict[str, int]] | None:
    block = h2(text, "2.")
    t = pick_table(block, ["优先级", "意图数", "已测", "未测"])
    if not t:
        return None
    headers, rows = t
    out: dict[str, dict[str, int]] = {}
    for row in rows:
        if not row or not row[0] or row[0] in ("优先级", "—") or any(x in row[0] for x in ("合计", "总计")):
            continue
        key = "P0" if is_p0(row[0]) else ("P1" if "P1" in row[0].upper() else ("P2" if "P2" in row[0].upper() else "其他"))
        out[key] = {name: to_int(cell(row, headers, name)) for name in ("意图数", "已测", "通过", "失败", "阻塞", "待实现", "N/A", "未测")}
    return out


def parse_report(path: Path, analysis: dict[str, Any], recs: dict[str, Any]) -> dict[str, Any]:
    text = read(path)
    issues: list[str] = []
    if not re.search(r"report_format\**\s*[:：]\s*`?intent-v1`?", text[:4000], re.I):
        issues.append("报告缺 report_format=intent-v1")
    for key in ("## 0.", "## 1.", "## 2.", "## 3.", "## 4.", "## 5."):
        if key not in text:
            issues.append(f"报告缺 {key} 标题")
    if not analysis.get("intents"):
        issues.append("分析无意图台账，报告不可判定")
    verdict, reason = parse_verdict(text)
    if not verdict:
        issues.append(reason)
    if not re.search(r"runId|运行ID|版本\s*/\s*构建", text, re.I):
        issues.append("报告缺 runId/构建声明")
    if "env-baseline" not in text:
        issues.append("报告缺 env-baseline.md / 环境基线声明")
    if not re.search(r"suite", text, re.I):
        issues.append("报告缺 suite 声明")
    if "接口" in text and not re.search(r"depth", text, re.I):
        issues.append("报告含接口但缺 depth 声明")
    block23 = subsection(text, "2.3")
    if not block23:
        issues.append("报告缺 §2.3 覆盖与收口探针")
    else:
        for token in (
            "来源",
            "章节回执",
            "原文对账",
            "依据覆盖",
            "设计点账本",
            "模块×面",
            "方法×规则",
            "细节维",
            "影响面",
            "核心链路",
            "S6",
            "S7",
            "S11",
            "探索式",
            "P0 意图",
            "风险清单",
        ):
            if token not in block23:
                issues.append(f"报告 §2.3 缺「{token}」")
        t23 = pick_table(block23, ["项", "结论"])
        if not t23:
            issues.append("报告 §2.3 覆盖与收口表缺失（需 项/结论）")
        else:
            headers, rows = t23
            for label in ("原文对账", "设计点账本", "细节维", "影响面", "核心链路", "S6", "S7", "S11"):
                hit = next((row for row in rows if label in cell(row, headers, "项")), None)
                if hit is None:
                    issues.append(f"报告 §2.3 缺「{label}」行")
                elif is_blank(cell(hit, headers, "结论")):
                    issues.append(f"报告 §2.3「{label}」无结论")
    if verdict in ("PASS", "CONDITIONAL") and recs["p0_fail"]:
        issues.append("P0 未过但报告写通过/有条件通过")
    if verdict == "PASS" and any(recs["counts"].get(k, 0) for k in ("失败", "阻塞", "待实现", "未执行", "未本轮验证")):
        issues.append("执行记录有失败/阻塞/待实现/未执行/未本轮验证但报告写 PASS")
    if verdict == "BLOCKED" and any(recs["counts"].get(k, 0) for k in ("失败", "待实现")):
        issues.append("有失败/待实现但报告写 BLOCKED（失败与阻塞并存应优先 FAIL）")
    if verdict == "CONDITIONAL" and not conditional_acceptor_ok(text):
        issues.append("有条件通过须在报告 §4 缺口表写非空接受人（禁仅正文碰巧出现「接受人」）")
    if verdict in ("PASS", "CONDITIONAL") and recs.get("p0_no_falsify"):
        issues.append("P0 仅正向通过无证伪/负向（或 N/A+接受）：" + "、".join(recs["p0_no_falsify"][:6]))
    if recs.get("orphan_intents"):
        issues.append("执行记录 INT 不在分析台账（须先回写分析）：" + "、".join(recs["orphan_intents"][:6]))
    if recs.get("intent_misaligned"):
        issues.append("通过场景与分析来源/Oracle 无可对账交集：" + "、".join(recs["intent_misaligned"][:6]))

    stats = stats_from_report(text)
    if stats is None:
        issues.append("报告 §2.1 场景统计表缺失")
    elif not stats:
        issues.append("报告 §2.1 场景统计表无数据行")
    else:
        for pri in ("P0", "P1", "P2"):
            expected = recs.get("by_pri_status", {}).get(pri, {})
            got = stats.get(pri, {})
            mapping = {"场景数": "总", "通过": "通过", "失败": "失败", "阻塞": "阻塞", "待实现": "待实现", "N/A": "不适用", "未执行": "未执行", "未本轮验证": "未本轮验证"}
            got_total = got.get("场景数", 0)
            expected_total = recs["by_pri"].get(pri, 0)
            if expected_total != got_total:
                issues.append(f"报告 §2.1 {pri} 场景数={got_total} 与执行记录 {expected_total} 不一致")
            for label, key in mapping.items():
                if label == "场景数":
                    continue
                if got.get(label, 0) != expected.get(key, 0):
                    issues.append(f"报告 §2.1 {pri} {label}={got.get(label, 0)} 与执行记录 {expected.get(key, 0)} 不一致")
    istats = intent_stats_from_report(text)
    if istats is None:
        issues.append("报告 §2.2 意图结论表缺失")
    elif not istats:
        issues.append("报告 §2.2 意图结论表无数据行")
    else:
        intents = analysis.get("intents", {})
        for pri in ("P0", "P1", "P2"):
            group = {iid: m for iid, m in intents.items() if (is_p0(m.get("pri", "")) and pri == "P0")
                     or (pri == "P1" and "P1" in m.get("pri", "").upper())
                     or (pri == "P2" and "P2" in m.get("pri", "").upper())}
            expected_total = len(group)
            tested = sum(1 for iid in group
                         if terminal_status(recs.get("intent_results", {}).get(iid, ""))
                         and recs.get("intent_results", {}).get(iid, "") != "不适用")
            na = sum(1 for m in group.values() if "N/A" in m.get("disp", "").upper() or "不适用" in m.get("disp", ""))
            untested = max(0, expected_total - tested - na)
            got = istats.get(pri, {})
            for label, exp in (("意图数", expected_total), ("已测", tested), ("N/A", na), ("未测", untested)):
                if got.get(label, 0) != exp:
                    issues.append(f"报告 §2.2 {pri} {label}={got.get(label, 0)} 与预期 {exp} 不一致")
    if recs["missing_evidence"]:
        issues.append("证据缺失：" + "、".join(recs["missing_evidence"][:6]))
    if recs["blocked_bad"]:
        issues.append("阻塞缺已尝试/恢复条件：" + "、".join(recs["blocked_bad"][:4]))
    required = {iid for iid, meta in analysis.get("intents", {}).items()
                if is_test_disp(meta.get("disp", ""))}
    missing_all = sorted(required - recs.get("intent_ids", set()))
    unterminal = sorted(iid for iid in required
                        if not terminal_status(recs.get("intent_results", {}).get(iid, "")))
    if missing_all:
        issues.append("意图未出现在执行记录：" + "、".join(missing_all[:8]))
    if unterminal:
        issues.append("意图未终态：" + "、".join(unterminal[:8]))
    if verdict in ("PASS", "CONDITIONAL") and (missing_all or unterminal):
        issues.append("存在未测/未终态意图但报告写通过/有条件通过")
    p0_required = {
        iid for iid in analysis.get("p0_ids", set())
        if is_test_disp(analysis.get("intents", {}).get(iid, {}).get("disp", ""))
    }
    missing_p0 = sorted(p0_required - recs.get("intent_ids", set()))
    if missing_p0:
        issues.append("P0 意图未出现在执行记录：" + "、".join(missing_p0[:8]))
    return {"issues": issues, "verdict": verdict}


# ---------- writeback ----------
def parse_writeback(test_root: Path) -> dict[str, Any]:
    receipts: list[Path] = []
    if test_root.is_dir():
        for p in test_root.rglob("*.md"):
            if not is_current(p):
                continue
            if "回执" in p.name or "回写" in p.name or "缺陷" in p.name or "BUG" in p.name.upper():
                receipts.append(p)
    if not receipts:
        return {"issues": ["未找到回写凭据"], "path": None}
    receipt = max(receipts, key=lambda p: p.stat().st_mtime)
    text = read(receipt)
    issues = []
    if not re.search(r"(BUG[-_]?\d+|#\d+)", text, re.I):
        issues.append("回写凭据缺平台单号")
    if "备注" not in text:
        issues.append("回写凭据缺备注")
    if not re.search(r"状态|resolution", text, re.I):
        issues.append("回写凭据缺状态")
    if not re.search(r"附件|fileId|无附件", text, re.I):
        issues.append("回写凭据缺附件回查")
    if "已回写" in text and not re.search(r"(noteId|备注ID|actionId|回写时间|回执)", text, re.I):
        issues.append("声称已回写但缺回执")
    return {"issues": issues, "path": str(receipt)}


def write_receipt(project_root: Path, mode: str, data: dict[str, Any]) -> Path:
    out_dir = project_root / RECEIPT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{mode}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    if mode != "writeback":
        (out_dir / "completion.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package-root", default=str(Path(__file__).resolve().parents[2]))
    ap.add_argument("--project-root", default=None)
    ap.add_argument("--mode", choices=["execute", "report", "writeback", "coverage"], default="report")
    ap.add_argument("--scope", default="")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", default=True)
    ap.add_argument("--allow-legacy", action="store_true")
    args = ap.parse_args()

    package_root = Path(args.package_root).resolve()
    project_root = Path(args.project_root).resolve() if args.project_root else default_project_root(package_root)
    if not (package_root / "AGENTS.md").is_file():
        print(f"PACKAGE_ROOT_INVALID: {package_root}")
        return 2
    test_root = find_test_root(project_root)
    analysis_path = test_root / "test-analysis.md"
    plan_path = test_root / "test-plan.md"

    checks: list[dict[str, Any]] = []
    blocked: list[str] = []
    counts = {s: 0 for s in STATUSES}
    by_pri = {"P0": 0, "P1": 0, "P2": 0, "其他": 0}
    p0_fail: list[str] = []
    p0_missing: list[str] = []
    source_hashes: dict[str, str] = {}
    analysis: dict[str, Any] = {"issues": [], "ids": set(), "p0_ids": set(), "intents": {}}
    recs: dict[str, Any] = {"issues": [], "counts": counts, "by_pri": by_pri,
                            "by_pri_status": {p: {s: 0 for s in STATUSES} for p in by_pri},
                            "intent_ids": set(), "intent_results": {}, "intent_priority": {},
                            "intent_falsify": {}, "p0_no_falsify": [],
                            "intent_misaligned": [], "orphan_intents": [],
                            "p0_fail": [], "missing_evidence": [], "blocked_bad": []}
    reported_verdict = ""
    conditional_accepted = False
    p0_no_falsify: list[str] = []

    if args.mode in ("coverage", "execute", "report"):
        env_path = project_root / "env-baseline.md"
        if not env_path.is_file():
            blocked.append("缺少 env-baseline.md（环境基线）")
            checks.append({"id": "env-baseline", "status": "blocked", "detail": "missing"})
        else:
            env_text = read(env_path)
            env_missing = [h for h in ("## 项目身份", "## 1.", "## 4.", "## 8.") if h not in env_text]
            checks.append({"id": "env-baseline", "status": "fail" if env_missing else "pass",
                           "detail": ("缺 " + "、".join(env_missing)) if env_missing else str(env_path)})
            source_hashes[str(env_path)] = hashlib.sha256(env_path.read_bytes()).hexdigest()
        if not analysis_path.is_file():
            blocked.append("缺少 test-analysis.md")
            checks.append({"id": "analysis-structure", "status": "blocked", "detail": "missing"})
        else:
            analysis = parse_analysis_v2(analysis_path)
            checks.append({"id": "analysis-structure", "status": "fail" if analysis["issues"] else "pass",
                           "detail": analysis["issues"][:14] or f"intents={len(analysis['ids'])} p0={len(analysis['p0_ids'])}"})
            source_hashes[str(analysis_path)] = hashlib.sha256(analysis_path.read_bytes()).hexdigest()
        if not plan_path.is_file():
            blocked.append("缺少 test-plan.md")
            checks.append({"id": "plan-structure", "status": "blocked", "detail": "missing"})
        else:
            plan = parse_plan(plan_path)
            checks.append({"id": "plan-structure", "status": "fail" if plan["issues"] else "pass",
                           "detail": plan["issues"][:12] or f"tier={plan['tier']}"})
            source_hashes[str(plan_path)] = hashlib.sha256(plan_path.read_bytes()).hexdigest()

    if args.mode in ("execute", "report"):
        scope = (args.scope or "").strip() or None
        if args.mode == "execute" and not scope:
            blocked.append("execute 须 --scope")
            checks.append({"id": "scope-required", "status": "blocked", "detail": "missing --scope"})
        records = find_records(test_root, scope if args.mode == "execute" else None)
        if not records:
            blocked.append("未找到执行记录（*执行记录.md）")
            checks.append({"id": "execution-record", "status": "blocked", "detail": "missing"})
        else:
            recs = aggregate(records, test_root, analysis)
            checks.append({"id": "execution-record", "status": "fail" if recs["issues"] else "pass",
                           "detail": recs["issues"][:10] or f"records={len(records)}"})
            checks.append({"id": "evidence-exists", "status": "fail" if recs["missing_evidence"] else "pass",
                           "detail": recs["missing_evidence"][:10]})
            checks.append({"id": "blocked-reasons", "status": "fail" if recs["blocked_bad"] else "pass",
                           "detail": recs["blocked_bad"][:10]})
            orphan = list(recs.get("orphan_intents") or [])
            misaligned = list(recs.get("intent_misaligned") or [])
            checks.append({
                "id": "intent-analysis-link",
                "status": "fail" if (orphan or misaligned) else "pass",
                "detail": (orphan[:6] + misaligned[:6]) or "INT linked to analysis",
            })
            p0_fail += recs["p0_fail"]
            p0_no_falsify = list(recs.get("p0_no_falsify") or [])
            checks.append({"id": "p0-status", "status": "fail" if p0_fail else "pass", "detail": p0_fail[:10]})
            checks.append({
                "id": "p0-falsify",
                "status": "fail" if p0_no_falsify else "pass",
                "detail": p0_no_falsify[:10] if p0_no_falsify else "P0 has falsify/N/A",
            })
            counts = recs["counts"]
            by_pri = recs["by_pri"]
            for rec in records:
                source_hashes[str(rec)] = hashlib.sha256(rec.read_bytes()).hexdigest()
            if args.mode == "report":
                required = {iid for iid, meta in analysis.get("intents", {}).items()
                            if is_test_disp(meta.get("disp", ""))}
                if not required:
                    checks.append({
                        "id": "intent-coverage",
                        "status": "fail",
                        "detail": "§2.1 无处置=测意图（禁止用设计点冒充覆盖）",
                    })
                    checks.append({"id": "intent-conclusion", "status": "fail", "detail": "no testable intents"})
                else:
                    missing = sorted(required - recs["intent_ids"])
                    unterminal = sorted(iid for iid in required
                                        if not terminal_status(recs["intent_results"].get(iid, "")))
                    checks.append({"id": "intent-coverage", "status": "fail" if missing else "pass",
                                   "detail": missing[:10] if missing else f"all {len(required)} intents present"})
                    checks.append({"id": "intent-conclusion", "status": "fail" if unterminal else "pass",
                                   "detail": unterminal[:10] if unterminal else "all intents terminal"})
                p0_required = {
                    iid for iid in analysis.get("p0_ids", set())
                    if is_test_disp(analysis.get("intents", {}).get(iid, {}).get("disp", ""))
                }
                p0_missing += sorted(p0_required - recs["intent_ids"])
                checks.append({"id": "p0-missing", "status": "fail" if p0_missing else "pass",
                               "detail": p0_missing[:10] if p0_missing else "P0 intents present"})
            else:
                unterminal = sorted(iid for iid, st in recs["intent_results"].items()
                                    if not terminal_status(st))
                checks.append({"id": "intent-conclusion", "status": "fail" if unterminal else "pass",
                               "detail": unterminal[:10] if unterminal else "batch intents terminal"})
                checks.append({"id": "intent-coverage", "status": "pass", "detail": "execute: scope batch only"})
                checks.append({"id": "p0-missing", "status": "pass", "detail": "execute: scope batch only"})
        smoke = test_root / "smoke-checklist.md"
        if not smoke.is_file():
            smoke = find_workroot(project_root) / "smoke-checklist.md"
        if smoke.is_file():
            source_hashes[str(smoke)] = hashlib.sha256(smoke.read_bytes()).hexdigest()

    if args.mode == "report":
        report = test_root / "test-report.md"
        if not report.is_file():
            blocked.append("缺少 test-report.md")
            checks.append({"id": "report-structure", "status": "blocked", "detail": "missing"})
        else:
            parsed = parse_report(report, analysis, recs)
            checks.append({"id": "report-structure", "status": "fail" if parsed["issues"] else "pass",
                           "detail": parsed["issues"][:10] or "ok"})
            reported_verdict = parsed["verdict"]
            checks.append({"id": "report-verdict", "status": "pass" if reported_verdict else "fail",
                           "detail": reported_verdict or "missing"})
            report_text = read(report)
            conditional_accepted = (
                reported_verdict == "CONDITIONAL" and conditional_acceptor_ok(report_text)
            )
            if reported_verdict == "CONDITIONAL" and not conditional_accepted:
                checks.append({
                    "id": "conditional-acceptor",
                    "status": "fail",
                    "detail": "§4 缺口表无非空接受人",
                })
            else:
                checks.append({
                    "id": "conditional-acceptor",
                    "status": "pass",
                    "detail": "ok" if reported_verdict != "CONDITIONAL" else "§4 acceptor present",
                })
            source_hashes[str(report)] = hashlib.sha256(report.read_bytes()).hexdigest()

    if args.mode == "writeback":
        parsed = parse_writeback(test_root)
        checks.append({"id": "writeback-receipt", "status": "fail" if parsed["issues"] else "pass",
                       "detail": parsed["issues"] or parsed["path"]})

    hard_fail = [c for c in checks if c.get("status") == "fail"]
    blocked_checks = [c for c in checks if c.get("status") == "blocked"]
    if args.mode == "coverage":
        verdict = "BLOCKED" if (blocked or blocked_checks) else ("FAIL" if hard_fail else "PASS")
    elif args.mode == "execute":
        # 高标准：分析/计划/环境/记录/证据/链接/终态/证伪 任一结构失败 → FAIL（禁下批）
        # 仅当过程完整且产品有红灯 → CONDITIONAL（可下批继续找缺陷，缺陷须入库）
        process_ids = {
            "env-baseline", "analysis-structure", "plan-structure",
            "execution-record", "evidence-exists", "blocked-reasons",
            "intent-analysis-link", "intent-conclusion", "p0-falsify", "scope-required",
        }
        process_fail = [c for c in hard_fail if c.get("id") in process_ids]
        incomplete = any(counts.get(k, 0) for k in ("未执行", "未本轮验证"))
        if blocked or blocked_checks:
            verdict = "BLOCKED"
        elif process_fail or incomplete:
            # 分析/链接/证据/终态不齐 = 过程未关，禁下批；不能因有产品红就降成 CONDITIONAL。
            verdict = "FAIL"
        elif p0_fail or any(counts.get(k, 0) for k in ("失败", "阻塞", "待实现")):
            verdict = "CONDITIONAL"
            checks.append({
                "id": "batch-advance",
                "status": "pass",
                "detail": f"过程完整+产品失败→CONDITIONAL；可标下批找缺陷，须入库：{(p0_fail or ['见 counts'])[:6]}",
            })
        elif hard_fail:
            verdict = "FAIL"
        else:
            verdict = "PASS"
    elif args.mode == "writeback":
        verdict = "BLOCKED" if (blocked or blocked_checks) else ("FAIL" if hard_fail else "PASS")
    else:
        if blocked or blocked_checks:
            verdict = "BLOCKED"
        elif hard_fail or p0_fail or p0_missing:
            verdict = "FAIL"
        elif reported_verdict == "BLOCKED":
            verdict = "BLOCKED"
        elif reported_verdict == "FAIL":
            verdict = "FAIL"
        elif reported_verdict == "CONDITIONAL":
            verdict = "CONDITIONAL" if conditional_accepted else "FAIL"
        elif any(counts.get(k, 0) for k in ("失败", "阻塞", "待实现", "未执行", "未本轮验证")):
            verdict = "FAIL"
        elif reported_verdict == "PASS":
            verdict = "PASS"
        else:
            verdict = "FAIL"

    h = hashlib.sha256()
    smoke_hash = test_root / "smoke-checklist.md"
    if not smoke_hash.is_file():
        smoke_hash = find_workroot(project_root) / "smoke-checklist.md"
    for p in (analysis_path, plan_path, smoke_hash):
        if p.is_file():
            h.update(read(p).encode("utf-8", errors="replace"))
    now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    completion = {
        "gate_version": "3.5",
        "package": PACKAGE_NAME,
        "mode": args.mode,
        "scope": args.scope or "",
        "gate_id": f"{args.mode}-{h.hexdigest()[:12]}",
        "verdict": verdict,
        "counts": counts,
        "by_priority": by_pri,
        "p0_fail": p0_fail,
        "p0_missing": p0_missing,
        "reported_verdict": reported_verdict,
        "conditional_accepted": conditional_accepted,
        "source_hashes": source_hashes,
        "checks": checks,
        "blocked": blocked,
        "timestamp": now,
    }
    if args.json:
        print(json.dumps(completion, ensure_ascii=False, indent=2))
    else:
        print("=== 完成门（测试规范）===")
        print(f"verdict: {verdict}")
        if args.scope:
            print(f"scope: {args.scope}")
        print("counts: " + " ".join(f"{k}={counts.get(k,0)}" for k in ("通过", "失败", "阻塞", "待实现", "不适用", "未执行")))
        for c in checks:
            print(f"- {c['id']}: {c.get('status')} {str(c.get('detail', ''))[:200]}")
        if blocked:
            print("blocked:")
            for b in blocked[:8]:
                print(f"  - {b}")
    out = write_receipt(project_root, args.mode, completion)
    print(f"written: {out}")
    # execute/report：PASS/CONDITIONAL 均可进入下一停点（report 的 CONDITIONAL 须已有接受人）。
    if args.mode in ("execute", "report"):
        return 0 if verdict in ("PASS", "CONDITIONAL") else 1
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())


