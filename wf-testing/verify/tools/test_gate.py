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
FAIL_DETAIL_LABELS = (
    "**问题标题**", "**分类", "**一句话影响**", "**最小复现**", "**环境**",
    "**测试数据", "**问题**", "**复现**", "**实际**", "**预期**",
    "**接口判定**", "**设计对照**", "**入口指纹**", "**技术附记**",
)
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


def failure_details(block: str) -> dict[str, str]:
    """Map SC id -> `### SC-...` failure-detail section (last wins)."""
    out: dict[str, str] = {}
    cur = ""
    buf: list[str] = []
    for line in block.splitlines():
        m = re.match(r"^###\s*(SC-[A-Z0-9-]+)\b", line.strip(), re.I)
        if m:
            if cur:
                out[cur] = "\n".join(buf)
            cur = norm_id(m.group(1))
            buf = [line]
        elif cur:
            buf.append(line)
    if cur:
        out[cur] = "\n".join(buf)
    return out


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


def table_rows(table: tuple[list[str], list[list[str]]] | None) -> list[list[str]]:
    """Real data rows of a parsed table (skip blank / separator-like first cells)."""
    if not table:
        return []
    _headers, rows = table
    out: list[list[str]] = []
    for row in rows:
        if not row:
            continue
        head = (row[0] or "").strip()
        if not head or head in ("—", "-", "…", "...", "---"):
            continue
        if all(not (c or "").strip() for c in row):
            continue
        out.append(row)
    return out


def is_blank(s: str) -> bool:
    s = (s or "").strip()
    return s in {"", "—", "-", "…", "...", "待补", "待确认"} or (s.startswith("{") and s.endswith("}"))


def norm_id(value: str) -> str:
    """Strip Markdown emphasis/backticks before ID comparison.

    Templates format IDs as `SC-001` / `INT-001-PAY`; the parser must not
    require the author to remove Markdown just to pass the gate.
    """
    return (value or "").strip().strip("`*_ ")


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


def pri_key(s: str) -> str:
    """Normalize a priority cell to P0/P1/P2 (empty when unparsable)."""
    t = (s or "").strip()
    if is_p0(t):
        return "P0"
    u = t.upper()
    if "P0" in u:
        return "P0"
    if "P1" in u:
        return "P1"
    if "P2" in u:
        return "P2"
    return ""


def is_na_disp(s: str) -> bool:
    """True for dispositions that mean 'not tested' (N/A / 不适用 / 不测)."""
    t = (s or "").strip()
    return "N/A" in t.upper() or "不适用" in t or t.startswith("不测")


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
    return bool(re.fullmatch(r"INT-[A-Z0-9]+(?:-[A-Z0-9]+)+", norm_id(iid)))


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


ORACLE_SIGNALS = (
    r"[=＝≥≤<>]|等于|不超过|至少|大于|小于|不超",
    r"状态|可查|显示|拒绝|阻断|不变|保留|不出现|可下钻|可复制|可见|可达|打开|禁用|提示|下一步|撤销|幂等",
    r"[元分件次条行张%％天笔]|字段|数量|金额|日期|批次|编号|入口|页面",
)


def strong_oracle(s: str) -> bool:
    """Oracle 须可判定：含数值；或 ≥24 字且有状态/字段/比较/引号标识；或足够具体的长句。"""
    t = (s or "").strip()
    if len(t) < 10:
        return False
    if re.search(r"\d", t):
        return True
    anchored = bool(re.search(r"状态|可查|显示|拒绝|阻断|不变|保留|可下钻|可见|可达|禁用|提示|下一步", t))
    anchored = anchored or bool(re.search(r"[元分件次条行张%％天笔]|字段|数量|金额|日期|批次|编号|入口|页面", t))
    anchored = anchored or bool(re.search(r"[=＝≥≤<>]|等于|不超过|至少|大于|小于", t))
    anchored = anchored or ("「" in t and "」" in t)
    return (len(t) >= 24 and anchored) or len(t) >= 40


def expand_int_ranges(s: str) -> str:
    """Expand INT-X-01~09 / INT-X-01～09 to explicit ids so batch coverage is exact."""

    def repl(m: re.Match[str]) -> str:
        prefix, a, b = m.group(1), int(m.group(2)), int(m.group(3))
        if b < a or b - a > 200:
            return m.group(0)
        width = len(m.group(2))
        return "、".join(f"INT-{prefix}-{i:0{width}d}" for i in range(a, b + 1))

    return re.sub(
        r"INT-([A-Z0-9]+)-(\d{2,})\s*[~～至]\s*(?:INT-[A-Z0-9]+-)?(\d{2,})",
        repl,
        s,
    )


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


def track_record_substance(path: Path, kind: str) -> bool:
    """Q18：正式轨关账认正文；空文件/缺要件不算。"""
    try:
        body = read(path).strip()
    except Exception:
        return False
    if len(body) < 80:
        return False
    if kind == "exploratory":
        return ("章程" in body) and (("覆盖" in body) or ("会话" in body) or ("风险点" in body))
    if kind == "api":
        has_ep = ("契约" in body) or bool(re.search(r"\bEP[-_A-Z0-9]", body))
        has_sc = ("场景" in body) or bool(re.search(r"\bSC[-_A-Z0-9]", body))
        rows = [ln for ln in body.splitlines() if ln.strip().startswith("|")]
        return has_ep and has_sc and len(rows) >= 6 and bool(re.search(r"\bSC[-_][A-Z0-9]", body))
    if kind == "pre-release":
        rows = [ln for ln in body.splitlines() if ln.strip().startswith("|")]
        has_hdr = any(("必测面" in ln and "结果" in ln) for ln in rows)
        data = [ln for ln in rows if not re.match(r"^\|\s*[-: ]+\|", ln) and "必测面" not in ln]
        graded = [ln for ln in data if re.search(r"达标|未达标|缺口|待测", ln)]
        return has_hdr and len(graded) >= 3
    return True


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
    src_specs: list[tuple[str, int, int, int]] = []
    chapter_rows = basis_rows = ac_rows = 0
    detail_yes = 0
    pending_gaps: list[str] = []
    p0_exemption = False
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
        src_data = table_rows(t_src)
        if not src_data:
            issues.append("§1 来源盘点无数据行（每条来源至少一行）")
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
            src_specs.append((row[0], total, mapped, na))
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
        if not table_rows(t_src_b):
            issues.append("§1 来源盘点无数据行（每条来源至少一行）")
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
            src_specs.append((row[0], total, mapped, 0))
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
        chapter_data = table_rows(t_ch)
        chapter_rows = len(chapter_data)
        if not chapter_data:
            issues.append("§1.2 章节回执无数据行（主读每个章节/标题至少一行）")
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
        basis_data = table_rows(t_basis)
        basis_rows = len(basis_data)
        if not basis_data:
            issues.append("§1.3 依据覆盖无数据行（PRD/方案/原型/接口逐条至少一行）")
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
            iid = norm_id(row[0])
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
            elif not strong_oracle(cell(row, headers, "Oracle")):
                issues.append(
                    f"§2.1 {iid} Oracle 不可判定（须含数值/比较/状态或字段单位等 ≥2 类信号）"
                )
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
            elif disp.startswith("不测"):
                if is_blank(cell(row, headers, "接受人")):
                    issues.append(f"§2.1 {iid} 处置=不测 缺接受人")
                if is_p0(pri):
                    issues.append(f"§2.1 {iid} P0 不得处置=不测（P0 必须执行）")
            elif not is_test_disp(disp):
                issues.append(f"§2.1 {iid} 处置须为 测/N/A/不测：{disp or '空'}")
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
        ac_data = table_rows(t_ac)
        ac_rows = len(ac_data)
        if not ac_data:
            issues.append("§2.1.1 AC/设计点账本无数据行（每个 AC/设计点至少一行）")
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
            elif disp.startswith("不测") and is_blank(cell(row, headers, "缺口/接受人")):
                issues.append(f"§2.1.1「{row[0]}」不测 缺接受人")
            elif not (disp.startswith("测") or "N/A" in disp.upper() or "不适用" in disp or disp.startswith("不测")):
                issues.append(f"§2.1.1「{row[0]}」处置须为 测/N/A/不测：{disp or '空'}")
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

    # 来源声明 ↔ 账本行数：章节/AC/设计点的自报计数必须被实际账本行支撑
    ledger_rows = chapter_rows + basis_rows + ac_rows
    ledger_specs = [(n, t, m, na) for (n, t, m, na) in src_specs
                    if re.search(r"章节|PRD|F/R|AC|设计", n, re.I)]
    ledger_mapped = sum(m for _n, _t, m, _na in ledger_specs)
    if ledger_mapped > ledger_rows:
        issues.append(
            f"§1.1 章节/AC/设计点声明已映射 {ledger_mapped}，但 §1.2/§1.3/§2.1.1 合计仅 {ledger_rows} 行（来源计数与账本不符）"
        )
    for name, total, mapped, na in src_specs:
        target = mapped if mapped else max(0, total - na)
        if not total or not target:
            continue
        if re.search(r"章节|PRD|F/R", name, re.I) and chapter_rows < target:
            issues.append(f"§1「{name}」声明 {target} 项，但 §1.2 仅 {chapter_rows} 行（章节回执不齐）")
        elif re.search(r"\bAC\b|AC/", name, re.I) and (basis_rows + ac_rows) < target:
            issues.append(f"§1「{name}」声明 {target} 项，但 §1.3+§2.1.1 仅 {basis_rows + ac_rows} 行（依据/设计点账本不齐）")

    # §2.2 coverage matrix
    block22 = subsection(text, "2.2")
    t22 = pick_table(block22, ["模块/流程", "负向/禁止"])
    if not t22:
        issues.append("§2.2 模块×面矩阵缺失或表头不可读")
    else:
        headers, rows = t22
        if not table_rows(t22):
            issues.append("§2.2 覆盖矩阵无模块/流程行（空格=覆盖缺口）")
        for col in ("主路径", "状态/分支", "边界/异常", "权限/数据域", "并发/幂等", "审计/历史", "通知/附件", "迁移/兼容", "非功能", "视觉/UI", "集成/状态轴", "计算/算例", "负向/禁止"):
            if not any(col in h for h in headers):
                issues.append(f"§2.2 覆盖矩阵缺列「{col}」")
        for row in rows:
            if not row or not row[0] or row[0] in ("模块/流程", "—"):
                continue
            row_has_int = False
            for j, val in enumerate(row[1:], 1):
                if is_blank(val):
                    issues.append(f"§2.2「{row[0]}」第{j}列为空")
                elif not has_matrix_marker(val):
                    issues.append(f"§2.2「{row[0]}」第{j}列未写 INT/场景 或 N/A+依据")
                else:
                    if re.search(r"INT-[A-Z0-9-]+|SC-[A-Z0-9-]+|SMK-[A-Z0-9-]+", val, re.I):
                        row_has_int = True
                    for ref in longest_int_refs(val):
                        if not intent_ref_ok(ref, intents):
                            issues.append(f"§2.2「{row[0]}」第{j}列 INT {ref} 不在 §2.1 台账")
            if not row_has_int:
                issues.append(f"§2.2「{row[0]}」整行 N/A（至少一个面须有 INT/场景）")

    # §2.3 method matrix
    block23 = subsection(text, "2.3")
    t23 = pick_table(block23, ["规则/计算", "算例"])
    if not t23:
        issues.append("§2.3 方法×规则矩阵缺失或表头不可读")
    else:
        headers, rows = t23
        if p0_ids and not table_rows(t23):
            issues.append("§2.3 方法矩阵无规则行（有 P0/关键规则时必须逐方法有落点）")
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
                else:
                    for ref in longest_int_refs(val):
                        if not intent_ref_ok(ref, intents):
                            issues.append(f"§2.3「{row[0]}」第{j}列 INT {ref} 不在 §2.1 台账")
            method_cols = ("等价类", "边界", "判定表/组合", "状态迁移", "场景", "算例")
            if not any("INT-" in cell(row, headers, name).upper() for name in method_cols):
                issues.append(f"§2.3「{row[0]}」方法列无 INT（只填意图列不算方法覆盖）")

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
            elif apply == "是":
                detail_yes += 1
                if is_blank(ref):
                    issues.append(f"§2.4「{row[0]}」适用但缺意图/场景")
                elif not re.search(r"INT-[A-Z0-9-]+|SC-[A-Z0-9-]+|SMK-[A-Z0-9-]+", ref, re.I):
                    issues.append(f"§2.4「{row[0]}」适用但意图/场景无法指到 ID（须写 INT-*/SC-*/SMK-*）")
                else:
                    for ir in longest_int_refs(ref):
                        if not intent_ref_ok(ir, intents):
                            issues.append(f"§2.4「{row[0]}」意图 {ir} 不在 §2.1 台账")
            elif is_blank(gap):
                issues.append(f"§2.4「{row[0]}」不适用但缺依据")

    # §3 risk
    block3 = h2(text, "3.")
    t_risk = pick_table(block3, ["RISK", "不可接受失败", "优先级"])
    if not t_risk:
        issues.append("§3 风险清单缺失或表头不可读")
    else:
        headers, rows = t_risk
        if not table_rows(t_risk):
            issues.append("§3 风险清单无数据行（至少登记本轮主要风险）")
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
        cats: list[str] = []
        for row in rows:
            if not row or not row[0] or row[0] in ("类别", "—"):
                continue
            seen += 1
            cats.append(row[0])
            if cell(row, headers, "是否适用") not in ("是", "否"):
                issues.append(f"§3.1「{row[0]}」是否适用须填 是/否")
        if seen < 8:
            issues.append(f"§3.1 风险扫描仅 {seen} 类")
        for key in ("资金", "状态", "幂等", "跨系统", "权限", "数据", "外部依赖", "历史", "业务语义", "可观测", "UX"):
            if not any(key in c for c in cats):
                issues.append(f"§3.1 风险扫描缺类别「{key}」")

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

    t_delta = pick_table(block5, ["变更点 ID", "变更摘要", "状态"])
    if not t_delta:
        issues.append("§5.2 变更影响追溯缺失（需 变更点 ID/变更摘要/状态）")
    else:
        headers, rows = t_delta
        if not table_rows(t_delta):
            issues.append("§5.2 变更影响追溯无数据行")
        for row in rows:
            if not row or not row[0] or row[0] in ("变更点 ID", "—"):
                continue
            status = cell(row, headers, "状态")
            if status not in ("已覆盖", "缺口", "N/A", "不适用"):
                issues.append(f"§5.2「{row[0]}」状态须为 已覆盖/缺口/N/A/不适用：{status or '空'}")

    t_core = pick_table(block5, ["链路 ID", "关键步骤"])
    if not t_core:
        issues.append("§5.3 核心链路表缺失或表头不可读")
    else:
        headers, rows = t_core
        if not table_rows(t_core):
            issues.append("§5.3 核心链路无数据行（至少一条主业务链）")
        for row in rows:
            if not row or not row[0] or row[0] in ("链路 ID", "—"):
                continue
            for name in ("业务目标", "入口", "关键步骤", "关联意图", "P0 冒烟", "状态"):
                if is_blank(cell(row, headers, name)):
                    issues.append(f"§5.3「{row[0]}」缺 {name}")
            status = cell(row, headers, "状态")
            if status not in ("已覆盖", "N/A", "不适用"):
                issues.append(f"§5.3「{row[0]}」状态未闭环：{status or '空'}")

    # §4 gaps / ambiguities
    block4 = h2(text, "4.")
    t_gap = pick_table(block4, ["ID", "问题", "状态"])
    if t_gap:
        headers, rows = t_gap
        for row in rows:
            if not row or not row[0] or row[0] in ("ID", "—"):
                continue
            status = cell(row, headers, "状态")
            if not status or status in ("—", "-", "…", "..."):
                issues.append(f"§4「{row[0]}」缺状态/接受人")
            if re.search(r"待确认|未确认|未关|开放", status):
                pending_gaps.append(f"{row[0]}:{status}")
        p0_exemption = any(
            "P0" in line and re.search(r"接受|accepted", line, re.I) for line in block4.splitlines()
        )
    elif not re.search(r"无\s*(未关|缺口|歧义)?", block4):
        issues.append("§4 歧义/冲突/缺口缺失（需表，或明确写「无」）")

    # §6 sufficiency
    t6 = pick_table(h2(text, "6."), ["检查", "通过条件"])
    if not t6:
        issues.append("§6 覆盖充分性表缺失（需 检查/通过条件/结论）")
    else:
        headers, rows = t6
        got_checks: list[str] = []
        for row in rows:
            if not row or not row[0] or row[0] in ("检查", "—"):
                continue
            got_checks.append(row[0])
            conclusion = row[2].strip() if len(row) > 2 else ""
            if is_blank(conclusion) or has_open_gap(conclusion):
                issues.append(f"§6「{row[0]}」未闭环：{conclusion or '空'}")
        for name in ("来源/章节", "依据覆盖", "意图", "覆盖矩阵", "方法矩阵", "细节维", "风险", "影响面", "变更追溯", "核心链路", "结论"):
            if not any(name in c for c in got_checks):
                issues.append(f"§6 缺检查项「{name}」")

    return {"path": str(path), "issues": issues, "intents": intents,
            "ids": set(intents.keys()), "p0_ids": p0_ids, "p1_ids": p1_ids, "p2_ids": p2_ids,
            "detail_yes": detail_yes, "chapter_rows": chapter_rows, "basis_rows": basis_rows,
            "ac_rows": ac_rows,
            "pending_gaps": pending_gaps, "p0_exemption": p0_exemption}


# ---------- plan ----------
def parse_plan(path: Path) -> dict[str, Any]:
    text = read(path)
    issues: list[str] = []
    state = ""
    version_release = ""
    outing = ""
    risk_tier = ""
    counts: dict[str, int] = {}
    suite = ""
    depth = ""
    batch_intents: set[str] = set()
    batch_all = False
    batches: dict[str, set[str]] = {}
    batch_all_ids: set[str] = set()
    tracks: dict[str, str] = {}
    charter_rows = 0
    charter_done = 0
    mtier = re.search(r"plan_tier\s*=\s*(full|lite)", text[:3000], re.I)
    tier = (mtier.group(1).lower() if mtier
            else ("lite" if "测试计划（轻量）" in text[:3000] else "full"))
    if not re.search(r"plan_format\**\s*[:：]\s*`?schedule-v1`?", text[:4000], re.I):
        issues.append("缺 plan_format=schedule-v1")
    for key in (("## 0.", "## 1.", "## 2.", "## 3.", "## 4.") if tier == "lite" else ("## 0.", "## 1.", "## 2.", "## 3.", "## 4.", "## 5.", "## 6.")):
        if key not in text:
            issues.append(f"计划缺 {key} 标题")
    if "test-analysis.md" not in text:
        issues.append("计划未引用 test-analysis.md")
    if "env-baseline.md" not in text:
        issues.append("计划未引用 env-baseline.md（环境基线）")

    # §0 one-page state: release/outing/risk/counts
    t0 = pick_table(h2(text, "0."), ["项", "值"])
    kv0: dict[str, str] = {}
    if t0:
        headers0, rows0 = t0
        for row in rows0:
            if row and row[0]:
                kv0[row[0].strip()] = (row[1].strip() if len(row) > 1 else "")
    state = kv0.get("计划状态", "")
    if not state:
        mstate = re.search(r"计划状态[^\n：:]*[：:]\s*([^\s/|]+)", text)
        if mstate:
            state = mstate.group(1).strip()
    if not state:
        issues.append("§0 缺计划状态（草稿/已确认/执行中/变更中/待关闭/已关闭）")
    version_release = ""
    ver_cell = next((v for k, v in kv0.items() if "版本准出" in k), "")
    if ver_cell:
        version_release = "是" if "是" in ver_cell else ("否" if "否" in ver_cell else "")
    elif tier == "lite":
        m = re.search(r"版本准出\s*[=:：]\s*(是|否)", text[:3000])
        if m:
            version_release = m.group(1)
    if not version_release:
        issues.append("§0 缺版本准出声明（是/否）")
    outing = ""
    outing_cell = next((v for k, v in kv0.items() if "准出口径" in k), "")
    if outing_cell:
        if "补丁" in outing_cell:
            outing = "补丁"
        elif "发版" in outing_cell:
            outing = "发版"
        elif "迭代" in outing_cell or "提测" in outing_cell:
            outing = "迭代"
    elif tier == "lite":
        m = re.search(r"准出口径\s*[=:：]\s*(迭代|提测|发版|补丁)", text[:3000])
        if m:
            outing = "补丁" if m.group(1) == "补丁" else ("发版" if m.group(1) == "发版" else "迭代")
    if not outing:
        issues.append("§0 缺准出口径（迭代/提测｜发版｜补丁）")
    risk_tier = ""
    for key, val in kv0.items():
        if "风险档" in key:
            mt = re.search(r"T[0-3]", val)
            if mt:
                risk_tier = mt.group(0)
            break
    if not risk_tier:
        if tier == "lite":
            risk_tier = "T0"
        else:
            issues.append("§0 缺风险档 T0～T3")
    counts: dict[str, int] = {}
    analysis_cell = next((v for k, v in kv0.items() if "分析文件" in k), "")
    if not analysis_cell:
        mline = re.search(r"分析[：:][^\n]*", text)
        if mline:
            analysis_cell = mline.group(0)
    if not analysis_cell:
        issues.append("§0 缺分析文件/计数行")
    else:
        n = re.search(r"意图\s*`?(\d+)", analysis_cell)
        m3 = re.search(r"P0\s*/\s*P1\s*/\s*P2\s*=\s*`?(\d+)\s*/\s*(\d+)\s*/\s*(\d+)", analysis_cell)
        if not m3:
            m3 = re.search(r"P0\s*`?(\d+)`?\s*/\s*P1\s*`?(\d+)`?\s*/\s*P2\s*`?(\d+)", analysis_cell)
        na = re.search(r"N/A\s*`?(\d+)", analysis_cell)
        if n and m3 and na:
            counts = {"total": int(n.group(1)), "P0": int(m3.group(1)),
                      "P1": int(m3.group(2)), "P2": int(m3.group(3)), "N/A": int(na.group(1))}
        else:
            issues.append("§0 分析计数不可解析（需 意图 N；P0/P1/P2；N/A）")

    suite = ""
    depth = ""
    ms = re.search(r"suite\s*[=:：]\s*`?([a-zA-Z]+)", text)
    if ms:
        suite = ms.group(1).lower()
    if suite not in {"core", "module", "full"}:
        issues.append("计划缺有效 suite 声明（core/module/full）")
    md = re.search(r"depth\s*[=:：]\s*`?([a-zA-Z不适用]+)", text)
    if md:
        depth = md.group(1)
    if "接口" in text:
        if depth not in {"core", "standard", "full", "不适用"}:
            issues.append("计划含接口但缺有效 depth 声明（core/standard/full/不适用）")
        if depth == "core" and "补丁口径" not in text:
            issues.append("接口 depth=core 仅限补丁口径（计划标「补丁口径」）")
    if suite == "core" and "补丁口径" not in text:
        issues.append("功能 suite=core 仅限补丁口径（计划标「补丁口径」）")

    pre_level = ""
    mpr = re.search(r"发布前风险级\s*[=:：]\s*`?([^\s`|；;]+)", text)
    if mpr:
        pre_level = re.sub(r"(级|风险)$", "", mpr.group(1).strip().strip("`"))
        if pre_level.startswith("高"):
            pre_level = "高"
        elif pre_level.startswith("标准"):
            pre_level = "标准"
        elif pre_level.startswith("基础"):
            pre_level = "基础"

    block4 = h2(text, "4.")
    if tier != "lite":
        if block4 and not all(k in block4 for k in ("P0", "缺口", "准出")):
            issues.append("§4 准入/准出缺 P0/缺口/准出关键口径")
        t_track = pick_table(h2(text, "2."), ["轨道", "纳入"])
        if not t_track:
            issues.append("§2 轨道表缺失（需 轨道/纳入）")
        elif not any(row and row[0] and row[0] not in ("轨道", "—") for row in t_track[1]):
            issues.append("§2 轨道表无数据行")
        else:
            headers, rows = t_track
            for row in table_rows(t_track):
                name = cell(row, headers, "轨道")
                if name:
                    tracks[name] = cell(row, headers, "纳入")
                    tracks[name + "::scope"] = cell(row, headers, "范围")
            # 迭代/提测/发版：正式轨默认硬纳入；整轨否仅 multi-track §0 白名单+接受人（补丁口径不强制）
            if outing in ("迭代", "提测", "发版"):
                label = "发版" if outing == "发版" else "迭代/提测"
                soft_na = re.compile(
                    r"小改|无\s*NFR|无NFR|无接口文档|UI已|功能已|无可探索|时间紧|"
                    r"本期不做|无运行时变更|顺手|内嵌探针|有接口面"
                )

                def _find_track(*needles: str) -> tuple[str, str, str]:
                    for k, v in tracks.items():
                        if "::" in k:
                            continue
                        if any(n in k for n in needles):
                            return k, v or "", tracks.get(k + "::scope", "") or ""
                    return "", "", ""

                def _na_ok(blob: str, kind: str) -> bool:
                    if "接受人" not in blob:
                        return False
                    if soft_na.search(blob):
                        return False
                    if kind == "api":
                        return bool(re.search(
                            r"无服务端|无HTTP|无RPC|无WebSocket|无\s*WS|无消息契约|无契约面|无后端|纯静态",
                            blob, re.I,
                        ))
                    if kind == "prerelease":
                        return bool(re.search(r"永不部署|无运行时交付|无运行时产品|纯文档", blob))
                    if kind == "exploratory":
                        return bool(re.search(r"补丁口径|\bT0\b|无运行时交付|无运行时产品|纯文档", blob))
                    if kind == "regression":
                        return bool(re.search(r"零变更|无邻接", blob))
                    return False

                fn_name, fn_inc, fn_scope = _find_track("功能")
                if not fn_name:
                    issues.append(f"{label}计划 §2 缺功能轨道（必须纳入）")
                elif "是" not in fn_inc:
                    issues.append(f"{label}功能轨必须纳入=是（不得整轨否冒充准出）")

                api_name, api_inc, api_scope = _find_track("接口")
                if not api_name:
                    issues.append(f"{label}计划 §2 缺接口轨道（默认纳入；否仅§0白名单+接受人）")
                else:
                    api_blob = f"{api_inc} {api_scope}"
                    if "是" in api_inc:
                        if depth not in {"core", "standard", "full"}:
                            issues.append("接口纳入=是 须 depth=core|standard|full（迭代≥standard；发版 full）")
                        elif depth == "core" and "补丁口径" not in text:
                            issues.append("接口 depth=core 仅限补丁口径")
                    elif "否" in api_inc:
                        if not _na_ok(api_blob, "api"):
                            issues.append(
                                "接口纳入=否 仅认§0白名单（无服务端/HTTP/RPC/WS/契约面等）+接受人；"
                                "禁无接口文档/UI已测/内嵌探针"
                            )
                    else:
                        issues.append("§2 接口「纳入」须为是或否")

                reg_name, reg_inc, reg_scope = _find_track("回归")
                if not reg_name:
                    issues.append(f"{label}计划 §2 缺回归轨道（必须纳入）")
                elif "是" not in reg_inc:
                    if not _na_ok(f"{reg_inc} {reg_scope}", "regression"):
                        issues.append("回归纳入=否 仅认零变更+零邻接+接受人（极少）")

                exp_name, exp_inc, exp_scope = _find_track("探索")
                if risk_tier in ("T1", "T2", "T3") or outing == "发版":
                    if not exp_name:
                        issues.append(f"T1+/发版 {label}计划 §2 缺探索式轨道（必须纳入）")
                    else:
                        exp_blob = f"{exp_inc} {exp_scope}"
                        if "是" in exp_inc:
                            pass
                        elif "否" in exp_inc:
                            if not _na_ok(exp_blob, "exploratory"):
                                issues.append(
                                    "T1+/发版 探索纳入=否 仅认§0白名单（T0/补丁口径或无运行时交付）+接受人；"
                                    "禁功能测完/无可探索面"
                                )
                        else:
                            issues.append("§2 探索式「纳入」须为是或否")

                pr_name, pr_inc, pr_scope = _find_track("发布前")
                if not pr_name:
                    issues.append(f"{label}计划 §2 缺发布前轨道（必须纳入，或§0白名单否+接受人）")
                else:
                    blob = f"{pr_inc} {pr_scope}"
                    if "是" in pr_inc:
                        if pre_level not in ("基础", "标准", "高"):
                            issues.append("发布前纳入=是 须声明风险级=基础|标准|高（分级见 tracks/pre-release）")
                    elif "否" in pr_inc:
                        if not _na_ok(blob, "prerelease"):
                            issues.append(
                                "发布前纳入=否 仅认§0白名单（永不部署/无运行时交付等）+接受人；"
                                "禁小改/无NFR/无运行时变更；小改用风险级=基础"
                            )
                    else:
                        issues.append("§2 发布前「纳入」须为是或否")
                if pre_level == "不适用" and pr_name and "是" in pr_inc:
                    issues.append("发布前纳入=是 时风险级不得为不适用")
        block3 = h2(text, "3.")
        t_round = pick_table(block3, ["轮次", "目标"])
        if not t_round:
            issues.append("§3 轮次表缺失（需 轮次/目标）")
        elif not any(row and row[0] and row[0] not in ("轮次", "—") for row in t_round[1]):
            issues.append("§3 轮次表无数据行")
        else:
            headers, rows = t_round
            for row in table_rows(t_round):
                for name in ("目标", "出口"):
                    if is_blank(cell(row, headers, name)):
                        issues.append(f"§3「{row[0]}」缺 {name}")
        t_batch = pick_table(block3, ["批次", "执行形态"])
        if not t_batch:
            issues.append("§3.1 批次表缺失（需 批次/执行形态；单模块可一行直跑+串行）")
        else:
            headers, rows = t_batch
            batch_data = table_rows(t_batch)
            if not batch_data:
                issues.append("§3.1 批次表无数据行")
            # 扇出只在「同一并行波次」内计：并行组=串行/空 → 各行独立，不跨批误伤
            wave: dict[str, list[tuple[str, str, str]]] = {}
            for row in batch_data:
                mode = cell(row, headers, "执行形态")
                if is_blank(mode):
                    issues.append(f"§3.1「{row[0]}」缺执行形态")
                    continue
                mod = cell(row, headers, "模块/域") or cell(row, headers, "模块")
                if is_blank(mod):
                    issues.append(f"§3.1「{row[0]}」缺模块/域")
                scope_cell = cell(row, headers, "意图范围")
                bid = norm_id(str(row[0]))
                row_ints = set(longest_int_refs(expand_int_ranges(scope_cell)))
                if "全部" in scope_cell:
                    batch_all = True
                    batch_all_ids.add(bid)
                if len(row_ints) > 35 and not re.search(r"模块子代理|拆分", mode or ""):
                    issues.append(
                        f"§3.1「{bid}」意图 {len(row_ints)} > 35，须拆批或形态=模块子代理/拆分"
                    )
                batch_intents.update(row_ints)
                batches[bid] = row_ints
                pg = (cell(row, headers, "并行组") or "").strip()
                iso = cell(row, headers, "隔离套") or cell(row, headers, "隔离套/账号/写域")
                if re.search(r"PG[-_]?\w*", pg or "", re.I):
                    if is_blank(iso) or re.fullmatch(r"串行|共享|共享[·.]?串行", (iso or "").strip()):
                        issues.append(f"§3.1「{row[0]}」有 {pg} 但隔离套不可核验（须互斥账号/profile/port/写域）")
                if re.search(r"脚本", mode) and not re.search(r"直跑|模块子代理|拆分", mode):
                    continue
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
            # 独立记录轨（接口/探索/发布前）：§2 纳入=是 → §3.1 须有对应批次（multi-track §0）
            if outing != "补丁":
                batch_blobs = [
                    " ".join([
                        cell(r, headers, "批次"),
                        cell(r, headers, "模块/域") or cell(r, headers, "模块"),
                        cell(r, headers, "意图范围"),
                    ])
                    for r in table_rows(t_batch)
                ]
                for kw, pat, label in (
                    ("接口", r"接口|\bAPI\b|EP-\d+", "接口/契约"),
                    ("探索", r"探索", "探索式"),
                    ("发布前", r"发布前", "发布前"),
                ):
                    inc = next((v for k, v in tracks.items() if "::" not in k and kw in k), "")
                    if "是" not in (inc or ""):
                        continue
                    hit = any(re.search(pat, b, re.I) for b in batch_blobs)
                    if kw == "发布前" and not hit:
                        hit = any(
                            re.search(r"性能", b, re.I) and re.search(r"安全", b, re.I)
                            for b in batch_blobs
                        )
                    if not hit:
                        issues.append(
                            f"§3.1 缺「{label}」轨道批（§2 纳入=是；须独立批次，模块/域写轨道词或 EP 编号）"
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
            for row in table_rows(t_imp):
                for name in ("关联意图", "覆盖/回归轮次", "责任人"):
                    if is_blank(cell(row, headers, name)):
                        issues.append(f"§1.4「{row[0]}」缺 {name}")
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
        # T1+ 计划需有章程行或 N/A；金额/风险级由计划门确认。
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
    # §3.2 charters: T1+ full plan must list enough charters
    if tier == "full" and outing != "补丁" and risk_tier in ("T1", "T2", "T3"):
        t_charter = pick_table(subsection(text, "3.2"), ["轴", "章程"])
        if not t_charter:
            issues.append("§3.2 探索式章程表缺失（T1+ 须 ≥3 条，T2/T3 ≥4 条，或 N/A+依据+接受人）")
        else:
            headers, rows = t_charter
            charter_rows = len(table_rows(t_charter))
            for row in table_rows(t_charter):
                if is_blank(cell(row, headers, "章程")):
                    issues.append(f"§3.2「{row[0]}」缺章程")
                st = cell(row, headers, "状态")
                if re.search(r"已跑|完成|闭环", st):
                    charter_done += 1
            need = 4 if risk_tier in ("T2", "T3") else 3
            if charter_rows < need:
                issues.append(f"§3.2 探索章程仅 {charter_rows} 条，{risk_tier} 须 ≥{need} 条")
    if tier == "full":
        for label in ("构建封板", "数据快照"):
            if not re.search(rf"^\|\s*{label}\s*\|\s*\S", text, re.M):
                issues.append(f"§2.2 缺「{label}」行（开跑封板/数据快照须可追溯）")
        m_data = re.search(r"^\|\s*数据 / 造数\s*\|\s*(.+?)\s*\|\s*$", text, re.M)
        data_cell = m_data.group(1) if m_data else ""
        if data_cell and not re.search(r"无需造数|无造数|不适用", data_cell) \
                and re.search(r"造数|构数|配方|REG-|runId|seed", data_cell):
            has_data_batch = False
            t_dbatch = pick_table(subsection(text, "3.1"), ["批次", "执行形态"])
            if t_dbatch:
                h_d, _r_d = t_dbatch
                for r_d in table_rows(t_dbatch):
                    blob = " ".join([
                        cell(r_d, h_d, "批次"),
                        cell(r_d, h_d, "模块/域") or cell(r_d, h_d, "模块"),
                        cell(r_d, h_d, "执行形态"),
                    ])
                    if re.search(r"造数|数据准备|DATA", blob, re.I):
                        has_data_batch = True
                        break
            if not has_data_batch:
                issues.append(
                    "§3.1 缺数据准备批（§2.2 有造数项：须先设执行形态含「造数」的批次，一次造齐后续复用）"
                )
        smk_ids = set(re.findall(r"SMK-\d+", text))
        if not re.search(r"\|\s*SMK\s*ID\s*\|", text) or len(smk_ids) < 6:
            issues.append("§3.3 冒烟清单缺失或不足 6 条（SMK 须有入口/期望，R0 前生成）")
    return {"path": str(path), "issues": issues, "tier": tier, "state": state,
            "version_release": version_release, "outing": outing, "risk_tier": risk_tier,
            "counts": counts, "suite": suite, "depth": depth,
            "batch_intents": batch_intents, "batch_all": batch_all,
            "batches": batches, "batch_all_ids": batch_all_ids, "tracks": tracks,
            "charter_rows": charter_rows, "charter_done": charter_done}


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
    orphan_intents: list[str] = []
    p0_fail: list[str] = []
    missing_evidence: list[str] = []
    blocked_bad: list[str] = []
    analysis_ids = set((analysis or {}).get("ids") or [])
    analysis_intents = (analysis or {}).get("intents") or {}
    scene_ids: set[str] = set()
    scene_intent_ids: set[str] = set()
    itable_ids: set[str] = set()
    reconcile_open = 0
    mb = re.search(r"批次[^\n]*?(B-[A-Z0-9-]+)", text)
    batch_id = norm_id(mb.group(1)) if mb else ""

    def eff_pri(iid: str, recorded: str) -> str:
        ap = pri_key(analysis_intents.get(iid, {}).get("pri", ""))
        return ap or pri_key(recorded) or "其他"

    if not (re.search(r"record_format\**\s*[:：]\s*`?intent-v1`?", text[:4000], re.I) or "场景与结果" in text):
        issues.append(f"{path.name}: 非执行记录格式")
    if "env-baseline" not in text:
        issues.append(f"{path.name}: 未引用 env-baseline.md（环境基线）")
    if "原文对账" not in text:
        issues.append(f"{path.name}: 缺 §0 原文对账行（开跑按原文目录对账分析漏项）")
    else:
        rec_line = ""
        for mline in re.finditer(r"[^\n]*原文对账[^\n]*", text):
            if "未关" in mline.group(0):
                rec_line = mline.group(0)
                break
        if not rec_line:
            mline = re.search(r"[^\n]*原文对账[^\n]*", text)
            rec_line = mline.group(0) if mline else ""
        if rec_line:
            mo = re.search(r"未关\s*[:：]?\s*`?\s*(\d+)", rec_line)
            if not mo:
                issues.append(f"{path.name}: 原文对账缺「未关 N」（未关 0 或缺口接受人）")
            else:
                reconcile_open = int(mo.group(1))
                if reconcile_open > 0 and not re.search(r"接受|accepted", rec_line, re.I):
                    issues.append(f"{path.name}: 原文对账未关 {reconcile_open} 但未写接受人")
            mn = re.search(r"可验收单元\s*(?:[（(][^）)\n]{0,60}[）)])?\s*[:：]?\s*`?\s*(\d+)", rec_line)
            if not mn:
                issues.append(f"{path.name}: 原文对账缺「可验收单元 N」")
            else:
                n_units = int(mn.group(1))
                mc = re.search(r"已覆盖\s*`?\s*(\d+)", rec_line)
                ma = re.search(r"补录\s*`?\s*(\d+)", rec_line)
                covered = int(mc.group(1)) if mc else 0
                added = int(ma.group(1)) if ma else 0
                if n_units <= 0:
                    issues.append(f"{path.name}: 原文对账可验收单元须 >0")
                elif covered + added < n_units:
                    issues.append(f"{path.name}: 原文对账 已覆盖 {covered} + 补录 {added} < 可验收单元 {n_units}")

    mref = re.search(r"原文\s*/\s*对照[^\n]*", text)
    if not mref:
        issues.append(f"{path.name}: 缺 §0「原文 / 对照」行（主读 + 对照；有互补源则写）")
    section0 = text.split("## 1.", 1)[0]
    if not re.search(r"test-analysis\.md", section0, re.I):
        issues.append(f"{path.name}: §0 缺分析索引（须写 test-analysis.md 命中节）")

    table = None
    scene_status: dict[str, str] = {}
    scene_evidence: dict[str, str] = {}
    fail_scs: set[str] = set()
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
            sc = norm_id(row[0])
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
            if is_blank(scene):
                issues.append(f"{path.name}: {sc} 缺场景描述")
            if is_blank(pri):
                issues.append(f"{path.name}: {sc} 缺优先级（须与 §2.1 台账一致）")
            if not INT_ID_RE.search(intent):
                issues.append(f"{path.name}: {sc} 缺 INT-* 意图")
            scene_ids.add(sc)
            if not is_api and status in ("通过", "失败", "阻塞", "待实现"):
                if is_blank(steps):
                    issues.append(f"{path.name}: {sc} 缺步骤（执行记录须可复核，3～7 短步）")
                else:
                    n_steps = len(re.findall(r"\d+\s*[.、)）]", steps)) or steps.count("→") + 1
                    if n_steps < 3:
                        issues.append(f"{path.name}: {sc} 步骤过少（功能记录须 3～7 短步，当前 {n_steps}）")
                    elif n_steps > 7:
                        issues.append(f"{path.name}: {sc} 步骤过多（功能记录须 3～7 短步，当前 {n_steps}）")
            if status == "通过" and weak_oracle(oracle):
                issues.append(f"{path.name}: {sc} 通过但 Oracle 过弱/缺失（须对照原文/分析的可观测断言，禁「通过/正常」）")
            for m in INT_ID_RE.findall(intent):
                intent_ids.add(m)
                scene_intent_ids.add(m)
                old = intent_results.get(m, "")
                intent_results[m] = worst_status(old, status)
                ap = pri_key(analysis_intents.get(m, {}).get("pri", ""))
                if pri and ap and pri_key(pri) != ap:
                    issues.append(
                        f"{path.name}: {sc} 优先级 {pri} 与分析 §2.1 {analysis_intents[m]['pri']} 不一致（先回写分析再记；P0 以台账记账）"
                    )
                if eff_pri(m, pri) == "P0":
                    intent_priority[m] = "P0"
                if status == "不适用" and is_test_disp(analysis_intents.get(m, {}).get("disp", "")):
                    issues.append(f"{path.name}: {sc} 分析处置=测但场景记不适用（{m}）")
                if looks_falsify(scene, source, oracle):
                    intent_falsify[m] = True
                if analysis_ids and m not in analysis_ids:
                    orphan_intents.append(f"{sc}:{m}")
            if status not in STATUSES:
                issues.append(f"{path.name}: {sc} 结果不可识别：{status or '空'}")
                continue
            scene_status[sc] = status
            scene_evidence[sc] = evidence
            if status in ("失败", "待实现"):
                fail_scs.add(sc)
            if status in ("通过", "失败", "阻塞", "待实现") and is_blank(actual):
                issues.append(f"{path.name}: {sc} 缺实际/差异（现场执行结果）")
            counts[status] += 1
            first_int = INT_ID_RE.findall(intent)[0] if INT_ID_RE.findall(intent) else ""
            key = eff_pri(first_int, pri) if first_int else (pri_key(pri) or "其他")
            by_pri[key] += 1
            by_pri_status[key][status] += 1
            if status in FAIL_STATUSES:
                if is_blank(evidence):
                    missing_evidence.append(f"{sc}:缺证据")
                elif not resolve_evidence(path, test_root, evidence):
                    missing_evidence.append(f"{sc}:证据不存在 {evidence}")
                if status == "阻塞":
                    actual_txt = actual or ""
                    has_try = re.search(r"尝试|穷尽|造数|换样|换角|换入口|建号|赋权|已试", actual_txt, re.I)
                    has_recover = re.search(r"恢复|卡点", actual_txt, re.I)
                    if not (has_try and has_recover):
                        blocked_bad.append(f"{sc}:阻塞须含已尝试(含自助手段)与卡点/恢复条件")
            if key == "P0" and status in ("失败", "阻塞", "待实现", "未执行", "未本轮验证"):
                p0_fail.append(f"{sc}:{status}")
            if key == "P0" and status == "通过":
                if is_blank(evidence):
                    missing_evidence.append(f"{sc}:P0 通过缺证据")
                elif not resolve_evidence(path, test_root, evidence):
                    missing_evidence.append(f"{sc}:P0 通过证据不存在 {evidence}")
        if seen == 0:
            issues.append(f"{path.name}: 场景表无数据行")

    if fail_scs:
        details = failure_details(h2(text, "2.") + "\n" + h2(text, "3."))
        for sc in sorted(fail_scs):
            sec = details.get(sc, "")
            if not sec:
                issues.append(f"{path.name}: {sc} 失败/待实现缺 §2/§3 失败详情块（交单素材）")
                continue
            missing = [label for label in FAIL_DETAIL_LABELS if label not in sec]
            if missing:
                issues.append(f"{path.name}: {sc} 失败详情缺 " + "、".join(missing))
            ms = re.search(r"surface\**\s*[：:=]\s*(ui|api|ui\+api)\b", sec, re.I)
            if not ms:
                issues.append(f"{path.name}: {sc} 失败详情缺 surface=ui|api|ui+api")
            elif ms.group(1).lower() in ("ui", "ui+api") and scene_status.get(sc) == "失败":
                evidence = scene_evidence.get(sc, "")
                if not re.search(r"\.(?:png|jpe?g|webp)\b|截图", sec + " " + evidence, re.I):
                    issues.append(
                        f"{path.name}: {sc} surface={ms.group(1)} 须有断言点截图"
                        "（§2/§3 证据或 §1 证据）"
                    )
            elif ms.group(1).lower() == "api":
                if not re.search(r"无\s*UI|无菜单|无页面|仅接口|纯接口|无可见控件|纯\s*API|仅\s*API", sec, re.I):
                    issues.append(f"{path.name}: {sc} surface=api 须一句无 UI 面依据")
            mcat = re.search(r"分类[^\n]*[:：]\s*`?([^；;\n|]+)", sec)
            category = mcat.group(1).strip().strip("`") if mcat else ""
            if category.startswith("产品缺陷"):
                if "**相符证明**" not in sec:
                    issues.append(f"{path.name}: {sc} 产品缺陷缺相符证明（classification §2）")
                if "**证据**" not in sec:
                    issues.append(f"{path.name}: {sc} 产品缺陷缺证据（相符证明须绑定证据）")

    # 功能记录 §1.1：正向/负向/状态/权限/幂等/UI 至少给 SC 或 N/A+依据
    if table and not is_api:
        for cat in ("正向", "关键负向/失败", "状态/非法跃迁", "权限/数据域", "幂等/并发/恢复/对账", "UI/视觉"):
            mline = re.search(rf"(?m)^\s*[-*]\s*{re.escape(cat)}\s*[:：]\s*(.+)$", text)
            if not mline:
                issues.append(f"{path.name}: 缺 §1.1 场景覆盖说明「{cat}」")
                continue
            val = mline.group(1).strip()
            if not val or val in ("—", "-", "…"):
                issues.append(f"{path.name}: §1.1「{cat}」未写 SC 或 N/A+依据")
                continue
            scs = [norm_id(x) for x in re.findall(r"SC-[A-Z0-9-]+", val, re.I)]
            for sc in scs:
                if sc not in scene_ids:
                    issues.append(f"{path.name}: §1.1「{cat}」引用不存在的场景 {sc}")
            if not scs and not re.search(r"N/A|不适用", val, re.I):
                issues.append(f"{path.name}: §1.1「{cat}」须写 SC-* 或 N/A+依据")
            if re.search(r"N/A|不适用", val, re.I) and not re.search(r"依据|理由", val):
                issues.append(f"{path.name}: §1.1「{cat}」N/A 须写依据")
            # UI/视觉：禁用「API 主断言/脚本/契约」充无页面面 N/A
            if cat == "UI/视觉" and re.search(r"N/A|不适用", val, re.I):
                weak = re.search(
                    r"API\s*主断言|字段级主断言|本批\s*API|以\s*API|脚本优先|契约自|前端\s*bundle|bundle\s*契约",
                    val,
                    re.I,
                )
                ok_fact = re.search(
                    r"无\s*UI|无页面|无菜单|无可见|仅接口|纯接口|纯\s*API|仅\s*API|无前端|用户确认|当轮确认|接受人",
                    val,
                    re.I,
                )
                if weak and not ok_fact:
                    issues.append(
                        f"{path.name}: §1.1「UI/视觉」不得以「API 主断言/脚本/契约」充 N/A（无页面面写事实句，或当轮用户确认）"
                    )

    # 接口记录 §2.1：每个 EP 的适用维有 SC 或 不适用+依据
    if table and is_api:
        t_dim = pick_table(subsection(text, "2.1"), ["EP", "维度", "处置"])
        if not t_dim:
            issues.append(f"{path.name}: 缺 §2.1 维度适用性（EP/维度/处置）")
        else:
            dh, _dr = t_dim
            for row in table_rows(t_dim):
                disp = cell(row, dh, "处置")
                if not disp or disp in ("—", "-", "…"):
                    issues.append(f"{path.name}: §2.1「{row[0]}」缺处置")
                    continue
                scs = [norm_id(x) for x in re.findall(r"SC-[A-Z0-9-]+", disp, re.I)]
                for sc in scs:
                    if sc not in scene_ids:
                        issues.append(f"{path.name}: §2.1「{row[0]}」引用不存在的场景 {sc}")
                if not scs and not re.search(r"N/A|不适用", disp, re.I):
                    issues.append(f"{path.name}: §2.1「{row[0]}」须写 SC-* 或 不适用+依据")
                if re.search(r"N/A|不适用", disp, re.I) and not re.search(r"依据|理由", disp):
                    issues.append(f"{path.name}: §2.1「{row[0]}」不适用须写依据")

    # 执行记录 §3 意图结论表：必须以场景为证
    itable = None
    for headers, rows in tables(text):
        joined = " ".join(headers)
        if "INT" in headers and "结论" in joined and "SC" not in headers:
            itable = (headers, rows)
            break
    if not itable:
        issues.append(f"{path.name}: 缺 §3 意图结论表（INT/场景 ID/结论；无场景的结论不算执行）")
    else:
        headers, rows = itable
        if not any("场景" in h for h in headers):
            issues.append(f"{path.name}: §3 意图结论表缺「场景 ID」列（结论须回指 §1 场景）")
        for row in table_rows(itable):
            iid = norm_id(row[0])
            if not INT_ID_RE.fullmatch(iid):
                continue
            itable_ids.add(iid)
            status = cell(row, headers, "结论")
            pri = cell(row, headers, "优先级")
            gap = cell(row, headers, "缺口/接受人") or cell(row, headers, "缺口") or cell(row, headers, "接受人")
            if looks_falsify("", "", gap):
                intent_falsify[iid] = True
            if status not in STATUSES:
                issues.append(f"{path.name}: 意图 {iid} 结论不可识别：{status or '空'}")
                continue
            scene_ref = cell(row, headers, "场景 ID") or cell(row, headers, "场景")
            sc_refs = set(re.findall(r"SC-[A-Z0-9-]+", scene_ref, re.I))
            if status == "不适用":
                if is_blank(gap):
                    issues.append(f"{path.name}: 意图 {iid} N/A 缺依据/接受人")
                if is_test_disp(analysis_intents.get(iid, {}).get("disp", "")):
                    issues.append(f"{path.name}: 意图 {iid} 分析处置=测但结论记不适用（须回写分析 N/A+接受人）")
            elif not sc_refs:
                issues.append(f"{path.name}: 意图 {iid} 结论 {status} 未指向场景（场景 ID 必填）")
            else:
                missing_sc = sorted(sc for sc in sc_refs if sc not in scene_ids)
                if missing_sc:
                    issues.append(f"{path.name}: 意图 {iid} 引用的场景不存在：{'、'.join(missing_sc[:3])}")
            ap = pri_key(analysis_intents.get(iid, {}).get("pri", ""))
            if pri and ap and pri_key(pri) != ap:
                issues.append(
                    f"{path.name}: 意图 {iid} 优先级 {pri} 与分析 §2.1 {analysis_intents[iid]['pri']} 不一致（先回写分析再记；P0 以台账记账）"
                )
            intent_ids.add(iid)
            intent_results[iid] = worst_status(intent_results.get(iid, ""), status)
            if eff_pri(iid, pri) == "P0":
                intent_priority[iid] = "P0"
                if status in ("失败", "阻塞", "待实现", "未执行", "未本轮验证"):
                    p0_fail.append(f"{iid}:{status}")
        for iid in sorted(scene_intent_ids - itable_ids):
            issues.append(f"{path.name}: 场景已执行但 §3 意图结论缺 {iid}")

    return {"path": str(path), "issues": issues, "counts": counts, "by_pri": by_pri,
            "by_pri_status": by_pri_status, "intent_ids": intent_ids,
            "scene_intent_ids": scene_intent_ids, "itable_ids": itable_ids,
            "reconcile_open": reconcile_open, "batch_id": batch_id,
            "intent_results": intent_results, "intent_priority": intent_priority,
            "intent_falsify": intent_falsify,
            "orphan_intents": orphan_intents,
            "p0_fail": p0_fail, "missing_evidence": missing_evidence, "blocked_bad": blocked_bad}


def aggregate(records: list[Path], test_root: Path, analysis: dict[str, Any] | None = None) -> dict[str, Any]:
    counts = {s: 0 for s in STATUSES}
    by_pri = {"P0": 0, "P1": 0, "P2": 0, "其他": 0}
    by_pri_status: dict[str, dict[str, int]] = {p: {s: 0 for s in STATUSES} for p in by_pri}
    issues: list[str] = []
    intent_ids: set[str] = set()
    scene_intent_ids: set[str] = set()
    reconcile_open = 0
    intent_results: dict[str, str] = {}
    intent_priority: dict[str, str] = {}
    intent_falsify: dict[str, bool] = {}
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
        scene_intent_ids |= p.get("scene_intent_ids", set())
        reconcile_open += int(p.get("reconcile_open", 0))
        for iid, status in p["intent_results"].items():
            intent_results[iid] = worst_status(intent_results.get(iid, ""), status)
        intent_priority.update(p["intent_priority"])
        for iid, flag in p.get("intent_falsify", {}).items():
            if flag:
                intent_falsify[iid] = True
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
            "intent_ids": intent_ids, "scene_intent_ids": scene_intent_ids,
            "reconcile_open": reconcile_open,
            "intent_results": intent_results, "intent_priority": intent_priority,
            "intent_falsify": intent_falsify, "p0_no_falsify": p0_no_falsify,
            "orphan_intents": sorted(set(orphan_intents)),
            "p0_fail": p0_fail, "missing_evidence": missing_evidence, "blocked_bad": blocked_bad}


# ---------- report ----------
def parse_verdict(text: str) -> tuple[str, str]:
    if re.search(r"verdict\s*=\s*(?:PASS|CONDITIONAL|FAIL|BLOCKED)\s*\|\s*(?:PASS|CONDITIONAL|FAIL|BLOCKED)", text, re.I):
        return "", "verdict 仍是占位符（须填单一结论）"
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


def parse_report(path: Path, analysis: dict[str, Any], recs: dict[str, Any],
                 plan: dict[str, Any] | None = None) -> dict[str, Any]:
    text = read(path)
    plan = plan or {}
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
    report_suite = ""
    report_depth = ""
    ms = re.search(r"suite\s*[=:：]\s*`?([a-zA-Z]+)", text)
    if ms:
        report_suite = ms.group(1).lower()
    if not report_suite:
        t1 = pick_table(h2(text, "1."), ["项", "值"])
        if t1:
            headers1, rows1 = t1
            for row in rows1:
                label = cell(row, headers1, "项")
                if "suite" in label.lower() or "档位" in label:
                    parts = [p.strip().strip("`") for p in re.split(r"[/｜|]", cell(row, headers1, "值"))]
                    if parts and parts[0].lower() in {"core", "module", "full"}:
                        report_suite = parts[0].lower()
                    if len(parts) > 1 and parts[1] in {"core", "standard", "full", "不适用"}:
                        report_depth = parts[1]
                    break
    if not report_suite:
        issues.append("报告缺 suite 声明")
    elif report_suite not in {"core", "module", "full"}:
        issues.append(f"报告 suite 不可识别：{report_suite}")
    elif plan.get("suite") and report_suite != plan["suite"]:
        issues.append(f"报告 suite={report_suite} 与计划 {plan['suite']} 不一致")
    if "接口" in text:
        if not report_depth:
            md = re.search(r"depth\s*[=:：]\s*`?([a-zA-Z不适用]+)", text)
            if md:
                report_depth = md.group(1)
        if not report_depth:
            issues.append("报告含接口但缺 depth 声明")
        elif report_depth not in {"core", "standard", "full", "不适用"}:
            issues.append(f"报告 depth 不可识别：{report_depth}")
        elif plan.get("depth") and report_depth != plan["depth"]:
            issues.append(f"报告 depth={report_depth} 与计划 {plan['depth']} 不一致")
    if verdict == "PASS" and analysis.get("pending_gaps"):
        issues.append("分析 §4 仍有待确认缺口，报告不得写 PASS：" + "、".join(analysis["pending_gaps"][:4]))
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
            detail_hit = next((row for row in rows if "细节维" in cell(row, headers, "项")), None)
            if detail_hit is not None:
                val = cell(detail_hit, headers, "结论")
                mnum = re.search(r"(\d+)\s*/\s*(\d+)", val)
                yes_n = int(analysis.get("detail_yes", 0))
                if mnum:
                    got_n, den = int(mnum.group(1)), int(mnum.group(2))
                    if den != 16:
                        issues.append(f"报告 §2.3 细节维分母={den}，应为 16（D01–D13+S6/S7/S11）")
                    if got_n > yes_n:
                        issues.append(f"报告 §2.3 细节维覆盖 {got_n} > 分析适用 {yes_n}（虚报）")
                    elif verdict == "PASS" and got_n < yes_n:
                        issues.append(f"报告 §2.3 细节维覆盖 {got_n}/{yes_n} 未全覆盖但写 PASS")
                elif verdict == "PASS":
                    issues.append("报告 §2.3 细节维须写 x/16（当前无法核对）")
            if recs.get("reconcile_open") and verdict == "PASS":
                issues.append(f"执行记录原文对账仍有未关 {recs['reconcile_open']} 项，报告不得写 PASS")
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
        results = recs.get("intent_results", {})
        for pri in ("P0", "P1", "P2"):
            group = {iid: m for iid, m in intents.items() if (is_p0(m.get("pri", "")) and pri == "P0")
                     or (pri == "P1" and "P1" in m.get("pri", "").upper())
                     or (pri == "P2" and "P2" in m.get("pri", "").upper())}
            expected_total = len(group)
            tested = sum(1 for iid in group
                         if terminal_status(results.get(iid, "")) and results.get(iid, "") != "不适用")
            na = sum(1 for m in group.values() if is_na_disp(m.get("disp", "")))
            untested = max(0, expected_total - tested - na)
            passed = sum(1 for iid in group if results.get(iid) == "通过")
            failed = sum(1 for iid in group if results.get(iid) == "失败")
            blocked = sum(1 for iid in group if results.get(iid) == "阻塞")
            pending = sum(1 for iid in group if results.get(iid) == "待实现")
            got = istats.get(pri, {})
            for label, exp in (("意图数", expected_total), ("已测", tested), ("通过", passed),
                               ("失败", failed), ("阻塞", blocked), ("待实现", pending),
                               ("N/A", na), ("未测", untested)):
                if got.get(label, 0) != exp:
                    issues.append(f"报告 §2.2 {pri} {label}={got.get(label, 0)} 与执行记录 {exp} 不一致")
    if recs["missing_evidence"]:
        issues.append("证据缺失：" + "、".join(recs["missing_evidence"][:6]))
    if recs["blocked_bad"]:
        issues.append("阻塞缺已尝试/恢复条件：" + "、".join(recs["blocked_bad"][:4]))
    required = {iid for iid, meta in analysis.get("intents", {}).items()
                if is_test_disp(meta.get("disp", ""))}
    scene_ok = set(recs.get("scene_intent_ids", set()))
    missing_all = sorted(required - scene_ok)
    unterminal = sorted(iid for iid in required
                        if not terminal_status(recs.get("intent_results", {}).get(iid, "")))
    if missing_all:
        issues.append("意图无场景执行（§3 声明不能替代场景）：" + "、".join(missing_all[:8]))
    if unterminal:
        issues.append("意图未终态：" + "、".join(unterminal[:8]))
    if verdict in ("PASS", "CONDITIONAL") and (missing_all or unterminal):
        issues.append("存在未测/未终态意图但报告写通过/有条件通过")
    p0_required = {
        iid for iid in analysis.get("p0_ids", set())
        if is_test_disp(analysis.get("intents", {}).get(iid, {}).get("disp", ""))
    }
    missing_p0 = sorted(p0_required - scene_ok)
    if missing_p0:
        issues.append("P0 意图无场景执行：" + "、".join(missing_p0[:8]))
    if verdict == "PASS" and plan.get("outing") == "发版":
        if report_suite != "full":
            issues.append("计划准出口径=发版，报告 PASS 须 suite=full")
        if "接口" in text and report_depth != "full":
            issues.append("计划准出口径=发版，报告 PASS 须 depth=full（含接口时）")
    return {"issues": issues, "verdict": verdict}


# ---------- writeback ----------
def _is_writeback_receipt_name(name: str) -> bool:
    """只认文件名含回执/回写；禁靠「缺陷/BUG」误匹配其它 md。"""
    return ("回执" in name) or ("回写" in name)


def _writeback_receipt_allowed(path: Path) -> bool:
    """认固定名写回回执.md；存量 functional|api|evidence；拒 .draft/_archive 与按日散落。"""
    parts = set(path.parts)
    if parts & {"_archive", ".draft"}:
        return False
    if not _is_writeback_receipt_name(path.name):
        return False
    # 正式：固定名（本轮覆盖）；拒 缺陷回归-写回回执-yyyyMMdd 等散落
    if path.name == "写回回执.md":
        return not (parts & {"functional", "api", "evidence", "证据", "defects"})
    if parts & {"evidence", "证据"}:
        return True
    if ("functional" in parts or "api" in parts) and is_current(path):
        return True
    return False


def _writeback_receipt_rank(path: Path) -> tuple:
    """优先 {ver}/写回回执.md，再存量 functional|api，再 evidence；同级取较新 mtime。"""
    parts = path.parts
    if path.name == "写回回执.md":
        # 版本根固定名优于子夹内同名残留
        tier = 0 if not ({"functional", "api", "evidence", "证据", "defects"} & set(parts)) else 1
    elif "functional" in parts or "api" in parts:
        tier = 2
    elif "evidence" in parts or "证据" in parts:
        tier = 3
    else:
        tier = 4
    try:
        mtime = path.stat().st_mtime
    except OSError:
        mtime = 0.0
    return (tier, -mtime)


_REGRESSION_WRITEBACK = re.compile(r"回归写回|回归范围卡|回归结论|resolve_fixed", re.I)
_REGRESSION_SIGNAL = re.compile(r"回归|复测", re.I)
_STATUS_ACTION = re.compile(r"关闭|激活|(?<!方案)解决|close|activate", re.I)


def _filled(val: str) -> bool:
    v = (val or "").strip()
    return bool(v) and v not in ("—", "-", "无") and "{" not in v and not v.startswith(("…", "..."))


def _regression_card_issues(text: str) -> list[str]:
    """回归写回须暴露构建/范围/冒烟/影响面/未覆盖；未跑或未覆盖须有接受人。"""
    if not (_REGRESSION_WRITEBACK.search(text)
            or (_REGRESSION_SIGNAL.search(text) and _STATUS_ACTION.search(text))):
        return []
    issues: list[str] = []
    m = re.search(r"构建\s*[=:：]\s*([^\n]*)", text)
    if not _filled(m.group(1) if m else ""):
        issues.append("回归写回缺构建")
    if not re.search(r"回归范围\s*[=:：]\s*(默认|扩大)(?=\s|$|[；;，,。.（(）)])", text, re.M):
        issues.append("回归写回缺范围（默认|扩大）")
    checks = (
        ("冒烟", r"冒烟\s*[=:：]\s*([^\n]*)", r"^(未跑|未执行|未另跑|N/?A|不适用)"),
        ("影响面", r"影响面\s*[=:：]\s*([^\n]*)", r"^(无|未跑|未执行|未测|N/?A|不适用)"),
    )
    for label, pattern, no_run in checks:
        m = re.search(pattern, text)
        val = m.group(1).strip() if m else ""
        if not _filled(val):
            issues.append(f"回归写回缺{label}")
        elif re.match(no_run, val, re.I) and not re.search(r"接受人|确认人|用户确认", val):
            issues.append(f"{label}未跑/未覆盖须写接受人")
    m = re.search(r"未覆盖\s*[=:：]\s*([^\n]*)", text) or re.search(r"豁免\s*[=:：]\s*([^\n]*)", text)
    val = m.group(1).strip() if m else ""
    if not val or "{" in val or val.startswith(("…", "...")):
        issues.append("回归写回缺未覆盖/豁免结论")
    elif not val.startswith("无") and not re.search(r"接受人|确认人|用户确认", val):
        issues.append("未覆盖项须写接受人")
    return issues


def parse_writeback(test_root: Path) -> dict[str, Any]:
    receipts: list[Path] = []
    if test_root.is_dir():
        for p in test_root.rglob("*.md"):
            if _writeback_receipt_allowed(p):
                receipts.append(p)
    if not receipts:
        return {"issues": ["未找到回写凭据"], "path": None}
    receipt = sorted(receipts, key=_writeback_receipt_rank)[0]
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
    if re.search(r"(?:\|\s*submit\s*\||动作\s*[=:：]\s*submit|新建|建单|提交到平台|platform_submit)", text, re.I):
        if not re.search(r"来源\s*[=:：]\s*(记录投影|现网补采)", text):
            issues.append("新建/平台交单回执缺 来源=记录投影|现网补采")
        if not re.search(r"surface\s*[=:：]\s*(ui|api|ui\+api)", text, re.I):
            issues.append("新建/平台交单回执缺 surface=ui|api|ui+api")
        if not re.search(r"十段\s*[=:：]\s*(齐|缺)", text):
            issues.append("新建/平台交单回执缺 十段=齐|缺")
    issues.extend(_regression_card_issues(text))
    return {"issues": issues, "path": str(receipt)}


def write_receipt(project_root: Path, mode: str, data: dict[str, Any]) -> Path:
    out_dir = project_root / RECEIPT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{mode}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    if mode not in ("writeback", "materials"):
        (out_dir / "completion.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def cross_check_plan_analysis(analysis: dict[str, Any], plan: dict[str, Any],
                              plan_text: str = "") -> list[str]:
    """Plan must be a schedule of the confirmed analysis, not an independent document."""
    issues: list[str] = []
    counts = plan.get("counts") or {}
    intents = analysis.get("intents", {})
    p0 = len(analysis.get("p0_ids", set()))
    p1 = len(analysis.get("p1_ids", set()))
    p2 = len(analysis.get("p2_ids", set()))
    na = sum(1 for m in intents.values() if is_na_disp(m.get("disp", "")))
    if counts:
        for label, exp in (("total", len(intents)), ("P0", p0), ("P1", p1), ("P2", p2), ("N/A", na)):
            if counts.get(label) != exp:
                issues.append(f"计划 §0 {label}={counts.get(label)} 与分析 {exp} 不一致")
    if plan.get("tier") == "lite" and plan.get("version_release") == "是":
        issues.append("轻量计划不得声明版本准出=是（应使用完整计划）")
    if plan.get("version_release") == "是" and plan.get("outing") == "补丁":
        issues.append("版本准出=是 与准出口径=补丁 冲突")
    if plan.get("version_release") == "否" and plan.get("outing") in ("迭代", "发版"):
        issues.append("版本准出=否 时准出口径应为补丁")
    if plan.get("version_release") == "是" and plan.get("outing") == "发版":
        if plan.get("suite") != "full":
            issues.append("准出口径=发版 须 suite=full")
        if plan.get("depth") and plan.get("depth") != "full":
            issues.append("准出口径=发版 且范围含接口时 须 depth=full")
    if (plan.get("tier") == "full" and plan.get("version_release") == "是"
            and not p0 and not analysis.get("p0_exemption")):
        issues.append("完整/版本计划的分析无 P0 意图（须至少 1 条 P0；确不适用在 §4 写 P0+接受人）")
    if (plan.get("tier") == "full" and plan.get("version_release") == "是"
            and plan.get("risk_tier") in ("T1", "T2", "T3")
            and any("功能" in k and "是" in (v or "") for k, v in (plan.get("tracks") or {}).items())
            and int(analysis.get("detail_yes", 0)) == 0):
        issues.append("T1+ 功能计划的分析细节维全部为否（至少一个适用维，或调整轨道/口径）")
    required = {iid for iid, meta in intents.items() if is_test_disp(meta.get("disp", ""))}
    if plan.get("tier") == "full" and required and not plan.get("batch_all"):
        missing = sorted(required - set(plan.get("batch_intents", set())))
        if missing:
            issues.append("计划 §3.1 批次意图范围未覆盖：" + "、".join(missing[:8]))
    return issues


def check_materials(project_root: Path, version: str, materials_dir: str) -> tuple[list[dict], list[str]]:
    """材料库发布校验（materials-validate）：README/INDEX 齐、文件全登记、无草稿/证据/密钥、链接自包含。"""
    checks: list[dict] = []
    blocked: list[str] = []
    root = (project_root / materials_dir).resolve() if materials_dir else project_root / "docs" / "materials"
    if not version and not materials_dir:
        blocked.append("未指定材料库版本（-Version {ver}）")
        checks.append({"id": "materials-version", "status": "blocked", "detail": "missing"})
        return checks, blocked
    ver_dir = root / version if version else root
    if not ver_dir.is_dir():
        blocked.append(f"材料库目录不存在：{ver_dir}")
        checks.append({"id": "materials-dir", "status": "blocked", "detail": str(ver_dir)})
        return checks, blocked
    checks.append({"id": "materials-dir", "status": "pass", "detail": str(ver_dir)})

    readme = ver_dir / "README.md"
    index = root / "INDEX.md"
    checks.append({"id": "materials-readme", "status": "pass" if readme.is_file() else "fail",
                   "detail": str(readme) if readme.is_file() else "缺少版本 README.md"})
    checks.append({"id": "materials-index", "status": "pass" if index.is_file() else "fail",
                   "detail": str(index) if index.is_file() else "缺少 docs/materials/INDEX.md"})
    index_text = read(index) if index.is_file() else ""

    skip_parts = {".draft", "evidence", "证据", "_archive", "__pycache__", ".git"}
    secret_re = re.compile(
        r"(?i)(api[_-]?key\s*[:=]\s*\S+|secret[_-]?key\s*[:=]\s*\S+|"
        r"access[_-]?token\s*[:=]\s*\S+|password\s*[:=]\s*\S+|"
        r"BEGIN (?:RSA|OPENSSH|EC) PRIVATE KEY|AKIA[0-9A-Z]{16})"
    )
    link_re = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
    files = [p for p in ver_dir.rglob("*") if p.is_file()]
    unregistered: list[str] = []
    drafts: list[str] = [
        d.relative_to(root).as_posix()
        for d in ver_dir.rglob("*")
        if d.is_dir() and any(part in skip_parts for part in d.relative_to(ver_dir).parts)
    ]
    secrets: list[str] = []
    for p in files:
        rel = p.relative_to(root).as_posix()
        if any(part in skip_parts for part in p.relative_to(ver_dir).parts):
            drafts.append(rel)
        if p.name != "README.md" and rel not in index_text and p.name not in index_text:
            unregistered.append(rel)
        if p.suffix.lower() in {".md", ".txt", ".yaml", ".yml", ".json", ".csv"}:
            text = read(p)
            if secret_re.search(text):
                secrets.append(rel)
    checks.append({"id": "materials-registered", "status": "fail" if unregistered else "pass",
                   "detail": unregistered[:10] or "all files registered"})
    checks.append({"id": "materials-no-draft", "status": "fail" if drafts else "pass",
                   "detail": drafts[:10] or "no draft/evidence dirs"})
    checks.append({"id": "materials-secrets", "status": "fail" if secrets else "pass",
                   "detail": secrets[:10] or "no secret patterns"})

    broken: list[str] = []
    for doc in (readme, index):
        if not doc.is_file():
            continue
        for target in link_re.findall(read(doc)):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0].strip()
            if not clean:
                continue
            if not (doc.parent / clean).exists() and not (root / clean).exists():
                broken.append(f"{doc.name} → {clean}")
    checks.append({"id": "materials-links", "status": "fail" if broken else "pass",
                   "detail": broken[:10] or "links resolve"})
    return checks, blocked


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package-root", default=str(Path(__file__).resolve().parents[2]))
    ap.add_argument("--project-root", default=None)
    ap.add_argument("--mode", choices=["execute", "report", "writeback", "coverage", "materials"], default="report")
    ap.add_argument("--scope", default="")
    ap.add_argument("--version", default="", help="materials 模式：材料库版本目录名")
    ap.add_argument("--materials-dir", default="", help="materials 模式：材料库根（默认 docs/materials）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", default=True,
                    help="兼容开关；门默认全严格，无放宽模式")
    args = ap.parse_args()

    package_root = Path(args.package_root).resolve()
    project_root = Path(args.project_root).resolve() if args.project_root else default_project_root(package_root)
    if not (package_root / "AGENTS.md").is_file():
        print(f"PACKAGE_ROOT_INVALID: {package_root}")
        return 2
    test_root = find_test_root(project_root)
    analysis_path = test_root / "test-analysis.md"
    plan_path = test_root / "test-plan.md"

    if args.mode == "materials":
        version = args.version or (declared_current_ver(project_root) or "")
        checks, blocked = check_materials(project_root, version, args.materials_dir)
        hard_fail = [c for c in checks if c.get("status") == "fail"]
        verdict = "BLOCKED" if blocked else ("FAIL" if hard_fail else "PASS")
        now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
        completion = {
            "gate_version": "3.6",
            "package": PACKAGE_NAME,
            "mode": "materials",
            "version": version,
            "verdict": verdict,
            "checks": checks,
            "blocked": blocked,
            "timestamp": now,
        }
        if args.json:
            print(json.dumps(completion, ensure_ascii=False, indent=2))
        else:
            print("=== 材料库校验（materials-validate）===")
            print(f"verdict: {verdict}")
            print(f"version: {version or '(未指定)'}")
            for c in checks:
                print(f"- {c['id']}: {c.get('status')} {str(c.get('detail', ''))[:200]}")
            if blocked:
                print("blocked:")
                for b in blocked[:8]:
                    print(f"  - {b}")
        out = write_receipt(project_root, "materials", completion)
        print(f"written: {out}")
        return 0 if verdict == "PASS" else 1

    checks: list[dict[str, Any]] = []
    blocked: list[str] = []
    counts = {s: 0 for s in STATUSES}
    by_pri = {"P0": 0, "P1": 0, "P2": 0, "其他": 0}
    p0_fail: list[str] = []
    p0_missing: list[str] = []
    source_hashes: dict[str, str] = {}
    analysis: dict[str, Any] = {"issues": [], "ids": set(), "p0_ids": set(), "intents": {},
                                "detail_yes": 0, "pending_gaps": [], "p0_exemption": False}
    plan: dict[str, Any] = {"issues": [], "tier": "full", "state": "", "version_release": "",
                            "outing": "", "risk_tier": "", "counts": {}, "suite": "", "depth": "",
                            "batch_intents": set(), "batch_all": False, "charter_rows": 0, "charter_done": 0}
    plan_text = ""
    recs: dict[str, Any] = {"issues": [], "counts": counts, "by_pri": by_pri,
                            "by_pri_status": {p: {s: 0 for s in STATUSES} for p in by_pri},
                            "intent_ids": set(), "scene_intent_ids": set(), "reconcile_open": 0,
                            "intent_results": {}, "intent_priority": {},
                            "intent_falsify": {}, "p0_no_falsify": [],
                            "orphan_intents": [],
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
            env_missing = [h for h in ("## 项目身份", "## 1.", "## 8.") if h not in env_text]
            if "## 4." not in env_text and "## 2.2" not in env_text:
                env_missing.append("## 4./## 2.2（测试账号与角色）")
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
            plan_text = read(plan_path)
            checks.append({"id": "plan-structure", "status": "fail" if plan["issues"] else "pass",
                           "detail": plan["issues"][:12] or f"tier={plan['tier']}"})
            source_hashes[str(plan_path)] = hashlib.sha256(plan_path.read_bytes()).hexdigest()
            if analysis.get("intents"):
                link_issues = cross_check_plan_analysis(analysis, plan, plan_text)
                checks.append({"id": "plan-analysis-link", "status": "fail" if link_issues else "pass",
                               "detail": link_issues[:8] or "plan linked to analysis"})
            if args.mode == "coverage" and plan_path.is_file():
                touched = [n for n in ("api-client", "api-fuzz", "sec-scan") if n in plan_text]
                if touched:
                    cap = find_workroot(project_root) / "capabilities" / "00-能力清单.md"
                    cap_issues: list[str] = []
                    if not cap.is_file():
                        cap_issues.append("缺 capabilities/00-能力清单.md")
                    else:
                        cap_text = read(cap)
                        for name in touched:
                            row_line = next(
                                (ln for ln in cap_text.splitlines()
                                 if ln.startswith("|") and f"`{name}`" in ln),
                                "",
                            )
                            if not row_line:
                                cap_issues.append(f"{name} 未登记")
                            elif "available" not in row_line and not (
                                "degraded" in row_line and "accepted=" in row_line
                            ):
                                cap_issues.append(f"{name} 未标 accepted=（降级须回写）")
                    checks.append({
                        "id": "capability-degrade",
                        "status": "fail" if cap_issues else "pass",
                        "detail": cap_issues[:6] or f"degraded-accepted={touched}",
                    })

    if args.mode in ("execute", "report"):
        state_ok = plan.get("state") in ("已确认", "执行中", "待关闭")
        checks.append({"id": "plan-state", "status": "pass" if state_ok else "fail",
                       "detail": plan.get("state") or "empty"})

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
            checks.append({
                "id": "intent-analysis-link",
                "status": "fail" if orphan else "pass",
                "detail": orphan[:6] or "INT linked to analysis",
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
                    scene_ok = set(recs.get("scene_intent_ids", set()))
                    missing = sorted(required - scene_ok)
                    unterminal = sorted(iid for iid in required
                                        if not terminal_status(recs.get("intent_results").get(iid, "")))
                    checks.append({"id": "intent-coverage", "status": "fail" if missing else "pass",
                                   "detail": missing[:10] if missing else f"all {len(required)} intents have scenes"})
                    checks.append({"id": "intent-scenes", "status": "fail" if missing else "pass",
                                   "detail": missing[:10] if missing else "every intent has a scene"})
                    checks.append({"id": "intent-conclusion", "status": "fail" if unterminal else "pass",
                                   "detail": unterminal[:10] if unterminal else "all intents terminal"})
                p0_required = {
                    iid for iid in analysis.get("p0_ids", set())
                    if is_test_disp(analysis.get("intents", {}).get(iid, {}).get("disp", ""))
                }
                p0_missing += sorted(p0_required - set(recs.get("scene_intent_ids", set())))
                checks.append({"id": "p0-missing", "status": "fail" if p0_missing else "pass",
                               "detail": p0_missing[:10] if p0_missing else "P0 intents have scenes"})
            else:
                unterminal = sorted(iid for iid, st in recs["intent_results"].items()
                                    if not terminal_status(st))
                checks.append({"id": "intent-conclusion", "status": "fail" if unterminal else "pass",
                               "detail": unterminal[:10] if unterminal else "batch intents terminal"})
                checks.append({"id": "intent-coverage", "status": "pass", "detail": "execute: scope batch only"})
                checks.append({"id": "p0-missing", "status": "pass", "detail": "execute: scope batch only"})
        if args.mode == "report":
            tracks = plan.get("tracks") or {}

            def track_on(name: str) -> bool:
                return any(name in k and "是" in (v or "") for k, v in tracks.items())

            current_md = [p for p in test_root.rglob("*.md") if is_current(p)] if test_root.is_dir() else []

            def rel(p: Path) -> str:
                return str(p).replace("\\", "/")

            missing_tracks: list[str] = []
            if track_on("功能") and not any("/functional/" in rel(p) and "执行记录" in p.name for p in current_md):
                missing_tracks.append("功能（functional/ 执行记录）")
            if track_on("接口"):
                api_recs = [p for p in current_md if "/api/" in rel(p) and "执行记录" in p.name]
                api_ok = [p for p in api_recs if track_record_substance(p, "api")]
                api_bad = [p.name for p in api_recs if p not in api_ok]
                if not api_ok:
                    missing_tracks.append("接口（api/ 实质执行记录）")
                if api_bad:
                    missing_tracks.append("接口空壳：" + "、".join(api_bad[:3]))
            if track_on("探索"):
                exp_recs = [p for p in current_md if "探索记录" in p.name]
                exp_ok = [p for p in exp_recs if track_record_substance(p, "exploratory")]
                exp_bad = [p.name for p in exp_recs if p not in exp_ok]
                if not exp_ok:
                    missing_tracks.append("探索式（实质探索记录）")
                if exp_bad:
                    missing_tracks.append("探索空壳：" + "、".join(exp_bad[:3]))
                done = int(plan.get("charter_done") or 0)
                if done and len(exp_ok) < done:
                    missing_tracks.append(f"探索已跑{done}但实质记录{len(exp_ok)}")
            if track_on("发布前"):
                pr_scheme = [p for p in current_md if "/pre-release/" in rel(p) and p.name.endswith("测试方案.md")]
                pr_report = [p for p in current_md if "/pre-release/" in rel(p) and p.name.endswith("test-report.md")]
                scheme_ok = [p for p in pr_scheme if track_record_substance(p, "pre-release")]
                report_ok = [p for p in pr_report if track_record_substance(p, "pre-release")]
                if not report_ok:
                    missing_tracks.append("发布前（实质 test-report）")
                if not scheme_ok:
                    missing_tracks.append("发布前（实质测试方案）")
                pr_bad = [p.name for p in (pr_scheme + pr_report) if not track_record_substance(p, "pre-release")]
                if pr_bad:
                    missing_tracks.append("发布前空壳：" + "、".join(pr_bad[:3]))
            checks.append({"id": "track-records",
                           "status": "fail" if missing_tracks else "pass",
                           "detail": missing_tracks[:6] or "tracks have substance records"})

        if args.mode == "execute":
            plan_batches = plan.get("batches") or {}
            batch_all_ids = plan.get("batch_all_ids") or set()
            if plan_batches:
                batch_issues: list[str] = []
                for rec in records:
                    rp = parse_record(rec, test_root, analysis)
                    bid = rp.get("batch_id", "")
                    if not bid:
                        batch_issues.append(f"{rec.name} 未标批次 ID（§0 轮次/批次）")
                        break
                    if bid not in plan_batches:
                        batch_issues.append(f"{bid} 不在计划 §3.1")
                        break
                    need = plan_batches.get(bid, set())
                    if bid in batch_all_ids or not need:
                        continue
                    got = set(rp.get("scene_intent_ids", set()))
                    missing = sorted(need - got)
                    if missing:
                        batch_issues.append(f"{bid} 意图未跑齐：{'、'.join(missing[:6])}")
                        break
                    extra = sorted(got - need)
                    if extra:
                        batch_issues.append(f"{bid} 出现批次外意图：{'、'.join(extra[:6])}")
                        break
                checks.append({"id": "batch-coverage",
                               "status": "fail" if batch_issues else "pass",
                               "detail": batch_issues[:4] or "batch intents covered"})

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
            parsed = parse_report(report, analysis, recs, plan)
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
            "env-baseline", "analysis-structure", "plan-structure", "plan-analysis-link",
            "plan-state", "execution-record", "evidence-exists", "blocked-reasons",
            "intent-analysis-link", "intent-conclusion", "p0-falsify", "scope-required",
            "batch-coverage",
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
        "gate_version": "3.6",
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


