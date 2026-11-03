#!/usr/bin/env python3
"""Lean completion gate for the test workflow.

Design goals:
- The spec package is read-only. Runtime state lives in <project>/.gate/wf-testing/.
- P0 is checked against the plan/stable smoke list, not only against rows that happen to exist.
- Report / execute / writeback receipts are separate, so a writeback cannot overwrite a report verdict.
- Coverage parsing only reads case documents, never evidence notes.

Usage:
  python test_gate.py --package-root <wf-testing> --project-root <project>
    [--mode execute|report|writeback|coverage|review] [--scope <模块路径片段>]

Exit: 0 = PASS, 1 = CONDITIONAL/FAIL/BLOCKED, 2 = usage.

Scope（步后门）:
  - execute：应带 --scope（如 16-ASN 或 functional/16）；缺则尝试从 activeContext/计划 §0 推断；仍无则 BLOCKED。
  - report：忽略 --scope，扫各轨现行台账；计数只认本轮装填（排除「未本轮验证」）。
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

# execute 上与检查矩阵 optional 对齐：可记 fail 但不单独拉垮步后 verdict
EXECUTE_SOFT_CHECKS = frozenset({"coverage-map", "p0-missing"})

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

PACKAGE_NAME = "wf-testing"
RECEIPT_DIR = Path(".gate") / PACKAGE_NAME

def default_project_root(package_root: Path) -> Path:
    """Walk up to the project root marked by activeContext.md."""
    for p in (package_root, *package_root.parents):
        if (p / "activeContext.md").is_file():
            return p
    return package_root.parent


def declared_workroot(project_root: Path):
    for name in ("project-profile.md", "env-baseline.md"):
        f = project_root / name
        if not f.is_file():
            continue
        try:
            m = re.search(r"^\|\s*workroot\s*\|\s*`?([^`|]+?)`?\s*\|", f.read_text(encoding="utf-8"), re.M)
            if m:
                val = m.group(1).strip()
                if val.startswith("默认") or "非标准" in val:
                    continue
                return project_root / val.rstrip("/")
        except Exception:
            pass
    return None

def find_test_root(project_root: Path) -> Path:
    """Resolve test workroot from the baseline, then the package convention."""
    w = declared_workroot(project_root)
    if w: return w
    if (project_root / "wf").is_dir():
        return project_root / "docs" / "testing"
    return project_root / "docs"
STATUSES = {"未执行", "通过", "失败", "阻塞", "待实现", "不适用", "未本轮验证"}
FAIL_STATUSES = {"失败", "阻塞", "待实现"}
STALE_STATUS = "未本轮验证"
CASE_ID_RE = re.compile(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d+\b")
# 覆盖门只抓“结构性空话”的高信号子集；完整清单在rules/tools/validate_testcase.py
COVERAGE_FILLER_RE = re.compile(
    r"按场景数据|同业务详情/列表/弹层|展示值可记录|本步结果可在页面核对|提交结果可回查"
)


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


def subsection(text: str, heading: str) -> str:
    """Extract a ### heading block (used by analysis/plan sub-sections)."""
    m = re.search(rf"^#{{2,3}}\s*{re.escape(heading)}(?:\s|$).*$", text, re.M)
    if not m:
        return ""
    start = m.end()
    nxt = re.search(r"^#{2,3}\s", text[start:], re.M)
    return text[start:start + nxt.start()] if nxt else text[start:]


def h2_section(text: str, prefix: str) -> str:
    for key, value in sections(text).items():
        if key.startswith(f"## {prefix}"):
            return value
    return ""


def get_cell(row: list[str], headers: list[str], name: str) -> str:
    try:
        i = headers.index(name)
    except ValueError:
        return ""
    return row[i].strip() if i < len(row) else ""


def is_blank_cell(s: str) -> bool:
    s = s.strip()
    return s in {"", "—", "-", "…", "...", "待补"} or (s.startswith("{") and s.endswith("}"))


def has_matrix_marker(s: str) -> bool:
    s = s.strip()
    return s.startswith("有") or s.startswith("N/A") or s.startswith("不适用")


def find_analysis(test_root: Path) -> Path | None:
    direct = test_root / "test-analysis.md"
    if direct.is_file():
        return direct
    if not test_root.is_dir():
        return None
    for p in test_root.rglob("*.md"):
        if not is_current(p):
            continue
        if p.name in ("test-analysis.md", "分析短表.md"):
            return p
    return None


def parse_analysis(test_root: Path) -> dict[str, Any]:
    """Hard checks for the new verification-point analysis format.

    Legacy analysis files (no §2.2) are reported as legacy and skipped, so old
    instances do not suddenly fail; new templates are gated hard.
    """
    p = find_analysis(test_root)
    if p is None:
        return {"path": None, "issues": ["缺少 test-analysis.md（或旧分析短表）"], "legacy": False, "ids": set()}
    text = read(p)
    is_new = bool(re.search(r"^#{2,3}\s*2\.2(?:\s|$)", text, re.M)) or "模块×面" in text
    if not is_new:
        return {"path": str(p), "issues": [], "legacy": True, "ids": set()}

    issues: list[str] = []
    ids: set[str] = set()
    # §2 verification point table
    block2 = h2_section(text, "2.")
    t2 = pick_table(block2, ["单元ID", "方法", "归属"])
    if not t2:
        issues.append("§2 验证点表缺少 类型/方法/归属/Oracle 列")
    else:
        headers, rows = t2
        for row in rows:
            if not row or not row[0] or row[0] in ("单元ID", "—"):
                continue
            ids.add(row[0].strip())
            typ = get_cell(row, headers, "类型")
            pri = get_cell(row, headers, "优先级")
            method = get_cell(row, headers, "方法")
            owner = get_cell(row, headers, "归属")
            oracle = get_cell(row, headers, "Oracle（可观测）") or get_cell(row, headers, "Oracle")
            needs_method = ("负向" in typ) or ("计算" in typ) or pri.startswith("P0") or "GATE" in row[0]
            if needs_method and (is_blank_cell(method) or is_blank_cell(owner) or is_blank_cell(oracle)):
                issues.append(f"§2 验证点「{row[0]}」缺方法/归属/Oracle")

    # §2.2 module x surface matrix
    block22 = subsection(text, "2.2")
    t22 = pick_table(block22, ["模块/切片", "负向/禁止"])
    if not t22:
        issues.append("§2.2 模块×面矩阵缺失或表头不可读")
    else:
        headers, rows = t22
        for row in rows:
            if not row or not row[0] or row[0] in ("模块/切片", "—"):
                continue
            for j, val in enumerate(row[1:], 1):
                if is_blank_cell(val):
                    issues.append(f"§2.2「{row[0]}」第{j}列为空")
                elif not has_matrix_marker(val):
                    issues.append(f"§2.2「{row[0]}」第{j}列未写 有/N/A+依据")

    # §2.3 method x rule matrix
    block23 = subsection(text, "2.3")
    t23 = pick_table(block23, ["规则/计算", "算例"])
    if not t23:
        issues.append("§2.3 方法×规则矩阵缺失或表头不可读")
    else:
        headers, rows = t23
        for row in rows:
            if not row or not row[0] or row[0] in ("规则/计算", "—"):
                continue
            for j, val in enumerate(row[1:], 1):
                if j < len(headers) and headers[j] == "验证点":
                    if is_blank_cell(val):
                        issues.append(f"§2.3「{row[0]}」缺验证点")
                    continue
                if is_blank_cell(val):
                    issues.append(f"§2.3「{row[0]}」第{j}列为空")
                elif not has_matrix_marker(val):
                    issues.append(f"§2.3「{row[0]}」第{j}列未写 有/N/A+依据")

    # §3.1 change impact
    block31 = subsection(text, "3.1")
    t31 = pick_table(block31, ["变更点 ID", "回归点"])
    if not t31:
        issues.append("§3.1 变更影响矩阵缺失或表头不可读")
    else:
        headers, rows = t31
        for row in rows:
            if not row or not row[0] or row[0] in ("变更点 ID", "—"):
                continue
            for j, val in enumerate(row[1:], 1):
                if is_blank_cell(val):
                    issues.append(f"§3.1「{row[0]}」第{j}列为空")
            status = get_cell(row, headers, "状态")
            if status not in ("已覆盖", "N/A", "不适用"):
                issues.append(f"§3.1「{row[0]}」状态未闭环：{status or '空'}")

    # §6 design document matrix
    block6 = h2_section(text, "6.")
    t6 = pick_table(block6, ["主读章节", "状态"])
    if not t6:
        issues.append("§6 设计文档覆盖矩阵缺失或表头不可读")
    else:
        headers, rows = t6
        for row in rows:
            if not row or not row[0] or row[0] in ("主读章节", "—"):
                continue
            status = get_cell(row, headers, "状态")
            if status not in ("已覆盖", "N/A", "不适用"):
                issues.append(f"§6「{row[0]}」状态未闭环：{status or '空'}")

    # §7.1 sufficiency
    block71 = subsection(text, "7.1")
    t71 = pick_table(block71, ["检查", "通过条件"])
    if not t71:
        issues.append("§7.1 覆盖充分性表缺失或表头不可读")
    else:
        headers, rows = t71
        for row in rows:
            if not row or not row[0] or row[0] in ("检查", "—"):
                continue
            conclusion = row[2].strip() if len(row) > 2 else ""
            if is_blank_cell(conclusion) or "缺口" in conclusion:
                issues.append(f"§7.1「{row[0]}」未闭环：{conclusion or '空'}")

    # §7.2 core chains
    block72 = subsection(text, "7.2")
    t72 = pick_table(block72, ["链路 ID", "关键步骤"])
    if not t72:
        issues.append("§7.2 核心链路表缺失或表头不可读")
    else:
        headers, rows = t72
        for row in rows:
            if not row or not row[0] or row[0] in ("链路 ID", "—"):
                continue
            case = get_cell(row, headers, "用例")
            status = get_cell(row, headers, "状态")
            if is_blank_cell(case) or case in ("待生成", "—") or status not in ("已覆盖", "N/A", "不适用"):
                issues.append(f"§7.2「{row[0]}」未闭环：用例={case or '空'} 状态={status or '空'}")

    return {"path": str(p), "issues": issues, "legacy": False, "ids": ids}


def parse_plan_structure(plan: Path) -> dict[str, Any]:
    text = read(plan)
    is_new = bool(re.search(r"^#{2,3}\s*3\.8(?:\s|$)", text, re.M)) or "版本级四卷" in text
    if not is_new:
        return {"issues": [], "legacy": True}
    issues: list[str] = []
    block37 = subsection(text, "3.7")
    t37 = pick_table(block37, ["模块/流程", "批次"])
    if not t37:
        issues.append("§3.7 执行矩阵缺少「批次」列")
    else:
        headers, rows = t37
        for row in rows:
            if not row or not row[0] or row[0] in ("模块/流程", "—"):
                continue
            if is_blank_cell(get_cell(row, headers, "批次")):
                issues.append(f"§3.7「{row[0]}」缺批次")

    block38 = subsection(text, "3.8")
    t38 = pick_table(block38, ["卷", "验证角度", "状态"])
    if not t38:
        issues.append("§3.8 四卷表缺失或表头不可读")
    else:
        headers, rows = t38
        got = {get_cell(row, headers, "卷").split()[0] for row in rows if row and row[0]}
        for v in ("V1", "V2", "V3", "V4"):
            if v not in got:
                issues.append(f"§3.8 缺 {v} 卷行（不适用也应写 N/A+依据）")
        for row in rows:
            if not row or not row[0]:
                continue
            for col in ("卷", "验证角度", "负责人", "验证点范围", "出口", "状态"):
                if is_blank_cell(get_cell(row, headers, col)):
                    issues.append(f"§3.8「{row[0]}」缺 {col}")

    block39 = subsection(text, "3.9")
    t39 = pick_table(block39, ["批次", "卷/阶段", "并行组"])
    if not t39:
        issues.append("§3.9 批次表缺失或表头不可读")
    else:
        headers, rows = t39
        if not rows:
            issues.append("§3.9 批次表无数据行")
        groups: dict[str, list[dict[str, str]]] = {}
        for row in rows:
            if not row or not row[0] or row[0] in ("批次", "—"):
                continue
            for col in ("批次", "卷/阶段", "模块/域", "装填用例", "执行形态", "并行组", "隔离套/账号/写域", "依赖/门", "合并/核验点"):
                val = get_cell(row, headers, col)
                if col == "并行组" and val in ("—", "-", "串行", "SERIAL"):
                    continue
                if is_blank_cell(val):
                    issues.append(f"§3.9「{row[0]}」缺 {col}")
            pg = get_cell(row, headers, "并行组")
            if pg and pg not in ("—", "-", "串行", "SERIAL"):
                groups.setdefault(pg, []).append({
                    "batch": get_cell(row, headers, "批次"),
                    "module": get_cell(row, headers, "模块/域"),
                    "mode": get_cell(row, headers, "执行形态"),
                    "iso": get_cell(row, headers, "隔离套/账号/写域"),
                    "gate": get_cell(row, headers, "依赖/门"),
                })
        for pg, items in groups.items():
            if len(items) > 3:
                issues.append(f"§3.9 {pg} 有 {len(items)} 个批次，超过并发上限 3")
            modules = [i["module"] for i in items]
            if len(modules) != len(set(modules)):
                issues.append(f"§3.9 {pg} 同模块多批次，台账/证据会冲突；须串行或拆 DraftPath")
            ui_items = [i for i in items if ("模块子代理" in i["mode"] or "拆分" in i["mode"])]
            if len(ui_items) > 2 and not any(("资源确认" in i["gate"] or "用户确认" in i["gate"]) for i in ui_items):
                issues.append(f"§3.9 {pg} UI 子代理 {len(ui_items)} 个，超过默认浏览器并发 2；3 个需在依赖/门写资源确认/用户确认")
            for item in ui_items:
                if not re.search(r"profile|port|:\d+|browser", item["iso"], re.I):
                    issues.append(f"§3.9 {item['batch']} UI 隔离未写 profile/port：{item['iso'] or '空'}")
            seen: dict[str, str] = {}
            for item in items:
                for token in re.split(r"[\/、,，;；]+", item["iso"]):
                    token = token.strip()
                    if not token or token in ("—", "-", "串行", "SERIAL", "不适用"):
                        continue
                    if token in seen:
                        issues.append(f"§3.9 {pg} 共享隔离 token「{token}」：{seen[token]} / {item['batch']}，须串行")
                    else:
                        seen[token] = item["batch"]
    return {"issues": issues, "legacy": False}


def parse_report_structure(text: str) -> dict[str, Any]:
    is_new = "卷结论" in text or "批次与并行" in text
    if not is_new:
        return {"issues": [], "legacy": True}
    issues: list[str] = []
    block4 = h2_section(text, "4.")
    for key, required in (
        ("卷结论", ["卷", "应结论", "结论率"]),
        ("验证点结论", ["验证点类型", "应结论", "结论率"]),
        ("批次与并行", ["批次", "执行形态", "合并结果"]),
    ):
        t = pick_table(block4, required)
        if not t:
            issues.append(f"报告 §4 缺「{key}」表")
    block6 = h2_section(text, "6.")
    if not re.search(r"设计文档|变更影响|核心链路", block6):
        issues.append("报告 §6 缺设计文档/变更影响/核心链路覆盖行")
    block61 = subsection(text, "6.1")
    if not pick_table(block61, ["门槛项", "证据"]):
        issues.append("报告 §6.1 门槛-证据映射缺失")
    return {"issues": issues, "legacy": False}



def is_current(path: Path) -> bool:
    return not any(part in path.parts for part in ("_archive", "_archive", ".draft", "资料", "materials", "证据", "evidence"))


def scope_tokens(scope: str | None) -> list[str]:
    if not scope:
        return []
    return [t.strip().replace("\\", "/") for t in re.split(r"[,;|]", scope) if t.strip()]


def path_in_scope(path: Path, scope: str | None) -> bool:
    tokens = scope_tokens(scope)
    if not tokens:
        return True
    rel = str(path).replace("\\", "/")
    return any(t in rel for t in tokens)


def infer_scope(project_root: Path) -> str:
    """Best-effort module hint for execute when --scope omitted."""
    test_root = find_test_root(project_root)
    for p in (project_root / "activeContext.md", test_root / "test-plan.md"):
        if not p.is_file():
            continue
        text = read(p)
        # functional/16-ASN… or 16-ASN发货
        m = re.search(r"(?:functional|功能测试)[/\\](\d{2}-[^\s`|/]+)", text)
        if m:
            return m.group(1).rstrip("*/）)")
        m = re.search(r"\bM(\d{2})\b", text)
        if m:
            return m.group(1)  # e.g. 16 matches …/16-…
        m = re.search(r"开跑\s*\*?\*?M?(\d{2})", text)
        if m:
            return m.group(1)
    return ""


def resolve_evidence(ledger: Path, evidence: str) -> bool:
    if not evidence:
        return False
    evidence = evidence.strip().strip("`").strip()
    if not evidence or evidence in ("—", "-", "无"):
        return False
    p = Path(evidence)
    if p.is_absolute():
        return p.exists()
    for base in (ledger.parent, *ledger.parents):
        if (base / evidence).exists():
            return True
        # 台账写「functional/evidence/…」时相对 {workroot}/
        if base.name in ("testing", "docs") and (base / evidence).exists():
            return True
    test_root = next((b for b in ledger.parents if (b / "test-plan.md").exists()), None)
    if test_root and (test_root / evidence).exists():
        return True
    return False


def parse_report_verdict(text: str) -> tuple[str, str]:
    line = next((ln for ln in text.splitlines() if "准出评估" in ln), "")
    if not line:
        return "", "未找到准出评估行"
    raw = line.replace("**", "").replace("`", "")
    # Template left all options in place: do not guess.
    if sum(1 for w in ("有条件通过", "不通过", "通过") if w in raw) >= 3:
        return "", "准出评估未选择唯一结论"
    if all(w in raw.upper() for w in ("PASS", "CONDITIONAL", "FAIL", "BLOCKED")):
        return "", "准出评估未选择唯一结论"
    if "有条件" in raw or "CONDITIONAL" in raw.upper():
        return "CONDITIONAL", ""
    if re.search(r"不通过(?!项)|未通过|部分通过|\bFAIL\b", raw, re.I):
        return "FAIL", ""
    if "阻塞" in raw or "未验证" in raw or "BLOCKED" in raw.upper():
        return "BLOCKED", ""
    if "通过" in raw or re.search(r"\bPASS\b", raw, re.I):
        return "PASS", ""
    return "", "准出评估不可识别"


def to_int(s: str) -> int:
    m = re.search(r"-?\d+", s.replace(",", ""))
    return int(m.group(0)) if m else 0


def parse_ledger(path: Path) -> dict[str, Any]:
    text = read(path)
    sec = sections(text)
    summary_block = next(
        (v for k, v in sec.items() if "域结论与汇总" in k or "模块结论与汇总" in k or "汇总" in k),
        text,
    )
    result_block = next((v for k, v in sec.items() if "结果表" in k), text)
    # Prefer 本轮装填表（首张含总数/通过/失败）；兼容旧单表台账
    summary = pick_table(summary_block, ["总数", "通过", "失败"])
    results = pick_table(result_block, ["用例 ID", "结果"])
    issues: list[str] = []
    if re.search(r"\{\…\}|\{\.\.\.\}", text):
        issues.append(f"{path}: 仍有模板占位符")
    counts = {
        "total": 0, "pass": 0, "fail": 0, "blocked": 0, "not_run": 0,
        "pending": 0, "na": 0, "stale": 0,
    }
    p0_fail: list[str] = []
    evidence_missing: list[str] = []
    blocked_bad: list[str] = []
    ids: set[str] = set()

    if results:
        headers, rows = results
        idx = {h: i for i, h in enumerate(headers)}
        def cell(row: list[str], name: str, default: str = "") -> str:
            i = idx.get(name)
            return row[i] if i is not None and i < len(row) else default
        for row in rows:
            cid = cell(row, "用例 ID")
            status = cell(row, "结果")
            if not cid:
                continue
            ids.add(cid)
            if not status:
                issues.append(f"{cid or row[0]}: 结果为空")
                continue
            if status not in STATUSES:
                issues.append(f"{cid or row[0]}: 未知结果状态 {status}")
                continue
            priority = cell(row, "用例优先级") or cell(row, "优先级")
            evidence = cell(row, "证据路径")
            summary_text = cell(row, "摘要")
            if status == STALE_STATUS:
                counts["stale"] += 1
                # 未本轮验证：不计本轮通过率；但计划 P0 不得停留在此态
                if "P0" in priority:
                    p0_fail.append(f"{cid}:未本轮验证")
                continue
            counts["total"] += 1
            if status == "通过":
                counts["pass"] += 1
            elif status == "失败":
                counts["fail"] += 1
            elif status == "阻塞":
                counts["blocked"] += 1
            elif status == "未执行":
                counts["not_run"] += 1
            elif status == "待实现":
                counts["pending"] += 1
            elif status == "不适用":
                counts["na"] += 1
            if "P0" in priority and status != "通过":
                if status == "不适用" and re.search(r"(依据|不适用|原因)", summary_text):
                    pass
                else:
                    p0_fail.append(f"{cid}:{status}")
            if status in FAIL_STATUSES:
                if not evidence or evidence in ("—", "-", "无"):
                    evidence_missing.append(f"{cid}: 缺证据")
                elif not resolve_evidence(path, evidence):
                    evidence_missing.append(f"{cid}: 证据不存在 {evidence}")
                if status == "阻塞" and not re.search(r"(尝试|恢复|卡点|穷尽)", summary_text):
                    blocked_bad.append(f"{cid}: 阻塞缺已尝试/恢复条件")
        if counts["total"] == 0 and counts["stale"] == 0:
            issues.append(f"{path}: 结果表无可识别用例（结果为空/未知）")
    else:
        issues.append(f"{path}: 未找到 §2 结果表（用例 ID/结果）")

    if summary:
        headers, rows = summary
        if rows:
            row = rows[0]
            idx = {h: i for i, h in enumerate(headers)}
            def cell(name: str) -> str:
                i = idx.get(name)
                return row[i] if i is not None and i < len(row) else "0"
            declared = {
                "total": to_int(cell("总数")), "pass": to_int(cell("通过")),
                "fail": to_int(cell("失败")), "blocked": to_int(cell("阻塞")),
                "not_run": to_int(cell("未执行")), "pending": to_int(cell("待实现")),
                "na": to_int(cell("不适用")),
            }
            for k, v in declared.items():
                if v != counts.get(k, 0):
                    issues.append(f"{path}: {k} 汇总={v} 本轮结果表={counts.get(k, 0)}")
    else:
        issues.append(f"{path}: 未找到 §1 汇总表（总数/通过/失败）")

    return {"path": str(path), "counts": counts, "issues": issues, "p0_fail": p0_fail,
            "evidence_missing": evidence_missing, "blocked_bad": blocked_bad, "ids": ids}


def parse_report(path: Path, ledger_counts: dict[str, int]) -> dict[str, Any]:
    text = read(path)
    sec = sections(text)
    count_block = next((v for k, v in sec.items() if "统计" in k or "轮次" in k), text)
    counts = pick_table(count_block, ["总数", "通过", "失败"])
    issues: list[str] = []
    if re.search(r"\{\…\}|\{\.\.\.\}", text):
        issues.append("报告仍有模板占位符")
    verdict, verdict_issue = parse_report_verdict(text)
    if verdict_issue:
        issues.append(verdict_issue)
    if verdict == "PASS" and any(ledger_counts.get(k, 0) for k in ("fail", "blocked", "pending", "not_run")):
        issues.append("台账有失败/阻塞/待实现/未执行但报告写通过")
    if counts:
        headers, rows = counts
        if rows:
            row = rows[0]
            idx = {h: i for i, h in enumerate(headers)}
            def cell(name: str) -> str:
                i = idx.get(name)
                return row[i] if i is not None and i < len(row) else "0"
            declared = {
                "total": to_int(cell("总数")), "pass": to_int(cell("通过")),
                "fail": to_int(cell("失败")), "blocked": to_int(cell("阻塞")),
                "not_run": to_int(cell("未执行")), "pending": to_int(cell("待实现")),
                "na": to_int(cell("不适用")),
            }
            for k, v in declared.items():
                if v != ledger_counts.get(k, 0):
                    issues.append(f"报告 {k}={v} 与台账 {ledger_counts.get(k, 0)} 不一致")
    else:
        issues.append("报告未找到 §4 统计表（总数/通过/失败）")
    receipt = re.search(r"【验证回执】\s*verdict\s*=\s*([A-Za-z]+)", text, re.I)
    receipt_verdict = receipt.group(1).upper() if receipt else ""
    if receipt_verdict and verdict and receipt_verdict != verdict:
        issues.append(f"报告回执 verdict={receipt_verdict} 与准出评估={verdict} 不一致")
    return {"path": str(path), "issues": issues, "verdict": verdict,
            "receipt_verdict": receipt_verdict}


def check_exit_hard_items(text: str) -> list[str]:
    """准出硬项：未关闭 S1/S2、探索章程未完成。缺少字段按缺口处理。"""
    issues: list[str] = []
    m = re.search(r"未关闭\s*S1/S2\s*[=:：]\s*(\d+)", text)
    if not m:
        issues.append("缺少「未关闭 S1/S2=n」")
    elif int(m.group(1)) > 0:
        issues.append(f"未关闭 S1/S2={m.group(1)}")
    m = re.search(r"章程[:：]\s*计划\s*(\d+)[，,]\s*完成\s*(\d+)[，,]\s*未完成\s*(\d+)", text)
    if not m:
        issues.append("缺少「章程：计划/完成/未完成」")
    elif int(m.group(3)) > 0:
        issues.append(f"探索章程未完成={m.group(3)}")
    return issues


def parse_coverage(root: Path, scope: str | None = None, valid_vp_ids: set[str] | None = None) -> dict[str, Any]:
    valid_vp_ids = valid_vp_ids or set()
    issues: list[str] = []
    missing: list[str] = []
    vp_issues: list[str] = []
    oracle_issues: list[str] = []
    seen = 0
    files = 0
    legacy_cases = 0
    base = root / "functional"
    if not base.is_dir():
        base = root / "功能测试"
    if not base.is_dir():
        return {"issues": issues, "missing": missing, "vp_issues": vp_issues, "oracle_issues": oracle_issues, "seen": 0, "files": 0, "legacy_cases": 0}
    for p in base.rglob("*.md"):
        if not is_current(p) or not path_in_scope(p, scope):
            continue
        if any(x in p.name for x in ("台账", "报告", "证据", "evidence", "评审", "计划", "测试分析表", "分析短表", "需求理解", "索引", "README")):
            continue
        if "用例" not in p.name and "testcase" not in p.name.lower():
            continue
        files += 1
        text = read(p)
        if COVERAGE_FILLER_RE.search(text):
            issues.append(
                f"{p.relative_to(root)}: 用例含模板化空话（按场景数据/同业务详情…），"
                "结构对齐≠可跟做；先按 validate_testcase.py 整改"
            )
        if "设计点覆盖映射" not in text:
            missing.append(f"{p.relative_to(root)}: 缺少「设计点覆盖映射」")
            continue
        seen += 1
        sec = sections(text)
        block = next((v for k, v in sec.items() if "设计点覆盖映射" in k), "")
        table = pick_table(block, ["设计点"])
        if not table:
            issues.append(f"{p.relative_to(root)}: §3 映射表不可读")
            continue
        headers, rows = table
        vp_idx = next((i for i, h in enumerate(headers) if "验证点" in h), None)
        if vp_idx is not None:
            for row in rows:
                if not row or not row[0] or row[0] in ("ID", "—"):
                    continue
                vp = row[vp_idx].strip() if vp_idx < len(row) else ""
                if is_blank_cell(vp) or vp in ("—", "待补"):
                    vp_issues.append(f"{p.relative_to(root)}: 用例「{row[0]}」缺验证点")
                elif valid_vp_ids and vp not in valid_vp_ids:
                    vp_issues.append(f"{p.relative_to(root)}: 用例「{row[0]}」验证点「{vp}」不在分析表 §2")
        else:
            legacy_cases += 1
        if vp_idx is not None:
            block_matches = list(re.finditer(r"^###\s+([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d+)\b.*$", text, re.M))
            for bi, bm in enumerate(block_matches):
                bstart = bm.start()
                bend = block_matches[bi + 1].start() if bi + 1 < len(block_matches) else len(text)
                case_block = text[bstart:bend]
                om = re.search(r"Oracle\s*来源\s*[|：:]\s*([^|\n]+)", case_block)
                oval = om.group(1).strip() if om else ""
                if not om or is_blank_cell(oval) or oval in ("—", "待补", "无"):
                    oracle_issues.append(f"{p.relative_to(root)}: 用例「{bm.group(1)}」缺有效「Oracle 来源」")
        case_ids = set(re.findall(r"^###\s+([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d+)\b", text, re.M))
        for row in rows:
            if len(row) < 2:
                continue
            point = row[0].strip()
            mapping = " ".join(row[1:]).strip()
            if not point or point in ("设计点", "—", "-"):
                continue
            if not mapping or mapping in ("—", "-", "待补"):
                issues.append(f"{p.relative_to(root)}: 设计点「{point}」无映射")
                continue
            mapped_ids = set(CASE_ID_RE.findall(mapping))
            if case_ids and mapped_ids and not (mapped_ids & case_ids):
                issues.append(f"{p.relative_to(root)}: 设计点「{point}」映射到不存在的用例")
        # §4 深度档/视觉摘要存在性（语义达标由评审量规；机器只拦「没写」）
        summary = next((v for k, v in sec.items() if "覆盖摘要" in k or "缺口" in k), "")
        summary_src = summary or text
        if not re.search(r"深度档", summary_src):
            issues.append(f"{p.relative_to(root)}: §4 缺少「深度档自检」（映射无空≠深度够）")
        if not re.search(r"视觉基础|视觉/UI|无\s*UI", summary_src):
            issues.append(f"{p.relative_to(root)}: §4 缺少「视觉基础」行（或明示无 UI）")
    return {"issues": issues, "missing": missing, "vp_issues": vp_issues, "oracle_issues": oracle_issues, "seen": seen, "files": files, "legacy_cases": legacy_cases}


def extract_p0_ids(*texts: str) -> set[str]:
    ids: set[str] = set()
    for text in texts:
        for line in text.splitlines():
            if not re.search(r"P0-(?:Smoke|HighRisk)|P0\b", line, re.I):
                continue
            ids.update(x for x in CASE_ID_RE.findall(line)
                       if not x.startswith(("DP-", "RQ-", "AC-", "F-", "R-", "TP-")))
    return ids


def find_review_records(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    out: list[Path] = []
    for p in root.rglob("*.md"):
        if not is_current(p):
            continue
        name = p.name
        # 合卷/计划：评审-*.md；单域 C 命名：{NN}-{短名}-评审-{戳}.md
        if (
            name.startswith("评审-")
            or name.startswith("评审_")
            or "-评审-" in name
            or "用例评审" in name
        ):
            out.append(p)
    return sorted(out, key=lambda p: p.stat().st_mtime, reverse=True)


def parse_review(path: Path) -> dict[str, Any]:
    text = read(path)
    issues: list[str] = []
    secs = sections(text)

    required_heads = ("评审对象", "依据", "结论")
    for head in required_heads:
        if not any(head in k for k in secs):
            issues.append(f"缺少章节含「{head}」")

    conclusion = ""
    for key, block in secs.items():
        if "结论" in key and "处理" not in key:
            if re.search(r"放行执行", block):
                conclusion = "放行执行"
            elif re.search(r"有条件放行", block):
                conclusion = "有条件放行"
            elif re.search(r"需修后放行", block):
                conclusion = "需修后放行"
            break
    if not conclusion:
        # fallback：整批结论 / 结论 行
        if re.search(r"(整批)?结论[：:\*\s]{0,12}放行执行", text):
            conclusion = "放行执行"
        elif re.search(r"(整批)?结论[：:\*\s]{0,12}有条件放行", text):
            conclusion = "有条件放行"
        elif re.search(r"(整批)?结论[：:\*\s]{0,12}需修后放行", text):
            conclusion = "需修后放行"
        else:
            issues.append("结论不可解析（须为 放行执行/需修后放行/有条件放行）")

    if not re.search(r"独立性|评审者\s*\|\s*|≠\s*生成|已隔离", text):
        issues.append("缺少独立性声明（评审者≠生成写手/已隔离）")

    if not re.search(r"严重度|阻断|A1|量规|评分卡", text):
        issues.append("缺少量规/严重度/评分卡痕迹")

    blocker_open = False
    if conclusion in ("放行执行", "有条件放行"):
        # 缺口表若仍有未处理「阻断」行且结论放行 → fail
        for _headers, rows in tables(text):
            if not rows:
                continue
            for row in rows:
                joined = "|".join(row)
                if "阻断" in joined and not re.search(r"无|—|-|已关闭|通过", joined):
                    # heuristic: severity column contains 阻断
                    if row and row[0].strip() == "阻断":
                        blocker_open = True
                        break
            if blocker_open:
                break
        if blocker_open and conclusion == "放行执行":
            issues.append("结论=放行执行但缺口表仍有未消化阻断项")
        if conclusion == "有条件放行" and not re.search(r"接受人", text):
            issues.append("有条件放行缺少接受人")

    if conclusion == "需修后放行":
        # allow PASS only if §处理/复核 all 通过 — else FAIL (not yet released)
        fix_sec = next((b for k, b in secs.items() if "处理" in k or "复核" in k), "")
        if fix_sec and re.search(r"通过", fix_sec) and not re.search(r"(未通过|不通过|部分通过|未过|未复核)", fix_sec):
            conclusion = "放行执行"  # recheck closed
        else:
            issues.append("结论=需修后放行（阻断未清，不得声称评审通过）")

    return {
        "path": str(path),
        "conclusion": conclusion,
        "issues": issues,
        "blocker_open": blocker_open,
    }


def write_receipt(project_root: Path, mode: str, data: dict[str, Any], primary: bool = True) -> Path:
    out_dir = project_root / RECEIPT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{mode}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    if primary:
        (out_dir / "completion.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package-root", default=str(Path(__file__).resolve().parents[2]))
    ap.add_argument("--project-root", default=None)
    ap.add_argument("--mode", choices=["execute", "report", "writeback", "coverage", "review"], default="report")
    ap.add_argument("--scope", default="", help="步后门范围（execute 推荐）；report 忽略。例: 16-ASN 或 functional/16")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="旧格式 analysis/plan/case/report 也按 FAIL 处理（新项目建议开启）")
    args = ap.parse_args()

    package_root = Path(args.package_root).resolve()
    project_root = Path(args.project_root).resolve() if args.project_root else default_project_root(package_root)
    if not (package_root / "AGENTS.md").is_file():
        print(f"PACKAGE_ROOT_INVALID: {package_root} (AGENTS.md not found)")
        return 2
    if project_root == package_root or package_root in project_root.parents:
        print("PROJECT_ROOT_INVALID: 项目根不能是规范包本身或在规范包内；运行态只写项目根 .gate/")
        return 2

    test_root = find_test_root(project_root)
    checks: list[dict[str, Any]] = []
    blocked: list[str] = []
    aggregate = {
        "total": 0, "pass": 0, "fail": 0, "blocked": 0, "not_run": 0,
        "pending": 0, "na": 0, "stale": 0,
    }
    p0_fail: list[str] = []
    p0_missing: list[str] = []
    reported_verdict = ""
    receipt_verdict = ""
    review_conclusion = ""

    # report = 准出门全仓；execute = 步后门需 scope
    scope: str | None = None
    if args.mode == "report":
        scope = None
    elif args.mode in ("execute", "coverage"):
        scope = (args.scope or "").strip() or None
        if args.mode == "execute" and not scope:
            inferred = infer_scope(project_root)
            if inferred:
                scope = inferred
                checks.append({"id": "scope-inferred", "status": "pass", "detail": scope})
            else:
                blocked.append("execute 须 --scope（模块路径片段，如 16-ASN）；无法从 activeContext/计划推断")
                checks.append({"id": "scope-required", "status": "blocked", "detail": "missing --scope"})

    if args.mode == "review":
        records = find_review_records(test_root)
        if not records:
            blocked.append("未找到用例评审记录（docs/testing/**/评审-*.md 或 **-评审-*.md）")
            checks.append({"id": "review-record", "status": "blocked", "detail": "missing"})
        else:
            latest = records[0]
            parsed = parse_review(latest)
            review_conclusion = parsed["conclusion"]
            checks.append({"id": "review-record", "status": "pass", "detail": parsed["path"]})
            checks.append({
                "id": "review-structure",
                "status": "fail" if parsed["issues"] else "pass",
                "detail": parsed["issues"][:10] or "ok",
            })
            released = review_conclusion in ("放行执行", "有条件放行") and not parsed["issues"]
            checks.append({
                "id": "review-verdict",
                "status": "pass" if released else "fail",
                "detail": review_conclusion or "missing",
            })
            # soft: coverage receipt if present
            cov_receipt = project_root / RECEIPT_DIR / "coverage.json"
            if cov_receipt.is_file():
                try:
                    cov = json.loads(read(cov_receipt))
                    cov_v = str(cov.get("verdict", ""))
                    checks.append({
                        "id": "coverage-receipt",
                        "status": "pass" if cov_v == "PASS" else "fail",
                        "detail": f"coverage.json verdict={cov_v}",
                    })
                except Exception:
                    checks.append({"id": "coverage-receipt", "status": "skip", "detail": "unreadable"})
            else:
                checks.append({"id": "coverage-receipt", "status": "skip", "detail": "no coverage.json yet"})

    elif args.mode in ("execute", "report", "coverage"):
        plan = test_root / "test-plan.md"
        if args.mode in ("execute", "report"):
            if not plan.is_file():
                blocked.append("缺少 docs/testing/test-plan.md")
                checks.append({"id": "plan-exists", "status": "blocked", "detail": "missing"})
            else:
                checks.append({"id": "plan-exists", "status": "pass", "detail": str(plan)})

        # New-format analysis/plan gates. Legacy files are skipped (visible in checks),
        # so existing instances keep running until migrated; new templates are hard-gated.
        analysis = parse_analysis(test_root)
        checks.append({
            "id": "analysis-structure",
            "status": "fail" if analysis["issues"] else "pass",
            "detail": analysis["issues"][:12] or analysis.get("path") or "ok",
        })
        if analysis.get("legacy"):
            checks.append({"id": "analysis-legacy", "status": "skip", "detail": "legacy analysis; new matrices not gated"})
        if plan.is_file():
            plan_struct = parse_plan_structure(plan)
            checks.append({
                "id": "plan-structure",
                "status": "fail" if plan_struct["issues"] else "pass",
                "detail": plan_struct["issues"][:12] or "ok",
            })
            if plan_struct.get("legacy"):
                checks.append({"id": "plan-legacy", "status": "skip", "detail": "legacy plan; four volumes/batches not gated"})

        if args.mode in ("execute", "report") and not any(c.get("id") == "scope-required" for c in checks):
            all_ledgers = [p for p in test_root.rglob("*.md") if "台账" in p.name and is_current(p)] if test_root.is_dir() else []
            # execute+scope：只扫本模块台账；report：全仓
            ledgers = [p for p in all_ledgers if path_in_scope(p, scope)] if args.mode == "execute" else all_ledgers
            ledger_ids: set[str] = set()
            if not ledgers:
                msg = "未找到 Scope 内执行台账" if args.mode == "execute" and scope else "未找到执行台账（docs/testing/**/*台账*.md）"
                blocked.append(msg)
                checks.append({"id": "ledger-counts", "status": "blocked", "detail": f"scope={scope or '*'}"})
            else:
                evidence_missing: list[str] = []
                blocked_bad: list[str] = []
                ledger_issues: list[str] = []
                for ledger in ledgers:
                    parsed = parse_ledger(ledger)
                    ledger_ids |= parsed["ids"]
                    for k in aggregate:
                        aggregate[k] += parsed["counts"].get(k, 0)
                    p0_fail += parsed["p0_fail"]
                    evidence_missing += parsed["evidence_missing"]
                    blocked_bad += parsed["blocked_bad"]
                    ledger_issues += parsed["issues"]
                checks.append({"id": "ledger-counts", "status": "fail" if ledger_issues else "pass",
                               "detail": (ledger_issues[:10] or f"ledgers={len(ledgers)} scope={scope or '*'}")})
                checks.append({"id": "evidence-exists", "status": "fail" if evidence_missing else "pass", "detail": evidence_missing[:10]})
                checks.append({"id": "blocked-reasons", "status": "fail" if blocked_bad else "pass", "detail": blocked_bad[:10]})
                checks.append({"id": "p0-status", "status": "fail" if p0_fail else "pass", "detail": p0_fail[:10]})
                plan_text = read(plan) if plan.is_file() else ""
                smoke = test_root / "smoke-checklist.md"
                smoke_text = read(smoke) if smoke.is_file() else ""
                planned_p0 = extract_p0_ids(plan_text, smoke_text)
                # execute：只要求「本 Scope 台账内出现的计划 P0」齐终态；全仓计划 P0 留给 report
                if args.mode == "execute":
                    scoped_planned = {x for x in planned_p0 if any(x in i or i in x for i in ledger_ids)} or set()
                    # 更稳：本 scope 台账里标了 P0 的缺终态已在 p0_fail；p0-missing 仅提示计划全集（soft）
                    p0_missing = sorted(planned_p0 - ledger_ids) if not scope else sorted(planned_p0 - ledger_ids)
                    soft = bool(p0_missing)
                    checks.append({
                        "id": "p0-missing",
                        "status": ("fail" if soft else "pass"),
                        "detail": f"{p0_missing[:10] if soft else 'scoped ok'} (execute: soft)",
                    })
                    _ = scoped_planned  # reserved for future tighten
                else:
                    p0_missing = sorted(planned_p0 - ledger_ids)
                    checks.append({"id": "p0-missing", "status": "fail" if p0_missing else "pass",
                                   "detail": p0_missing[:10] if p0_missing else "all planned P0 present"})

        if args.mode == "report":
            report = test_root / "test-report.md"
            if not report.is_file():
                blocked.append("缺少 docs/testing/test-report.md")
                checks.append({"id": "report-counts", "status": "blocked", "detail": "missing"})
                checks.append({"id": "report-verdict", "status": "blocked", "detail": "missing report"})
            else:
                parsed = parse_report(report, aggregate)
                checks.append({"id": "report-counts", "status": "fail" if parsed["issues"] else "pass", "detail": parsed["issues"][:10]})
                rep_struct = parse_report_structure(read(report))
                checks.append({"id": "report-structure", "status": "fail" if rep_struct["issues"] else "pass",
                               "detail": rep_struct["issues"][:10] or "ok"})
                if rep_struct.get("legacy"):
                    checks.append({"id": "report-legacy", "status": "skip", "detail": "legacy report; volume/point/batch tables not gated"})
                reported_verdict = parsed["verdict"]
                receipt_verdict = parsed["receipt_verdict"]
                checks.append({"id": "report-verdict", "status": "pass" if reported_verdict else "fail",
                               "detail": reported_verdict or "准出评估缺失/不可识别"})
                checks.append({"id": "p0-vs-verdict", "status": "fail" if p0_fail and reported_verdict in ("PASS", "CONDITIONAL") else "pass",
                               "detail": "P0-Smoke/P0-HighRisk 未过但报告写通过/有条件通过" if p0_fail and reported_verdict in ("PASS", "CONDITIONAL") else "consistent"})
                if "## 5." in read(report):
                    hard = check_exit_hard_items(read(report))
                    checks.append({"id": "exit-hard-items", "status": "fail" if hard else "pass", "detail": hard[:10]})
                else:
                    checks.append({"id": "exit-hard-items", "status": "skip", "detail": "报告未含 §5；准出硬项需人工核"})
                if not receipt_verdict:
                    checks.append({"id": "report-receipt", "status": "skip", "detail": "报告暂无回执；复跑时必须一致"})

        cov_scope = scope if args.mode in ("execute", "coverage") else None
        cov = parse_coverage(test_root, cov_scope, analysis.get("ids", set())) if test_root.is_dir() else {"issues": [], "missing": [], "vp_issues": [], "oracle_issues": [], "seen": 0, "files": 0, "legacy_cases": 0}
        if cov.get("legacy_cases"):
            checks.append({"id": "case-vp-legacy", "status": "skip",
                           "detail": f"legacy cases without verification-point column: {cov['legacy_cases']}"})
        checks.append({"id": "case-vp", "status": "fail" if cov.get("vp_issues") else "pass",
                       "detail": cov.get("vp_issues", [])[:10] or "ok"})
        checks.append({"id": "case-oracle", "status": "fail" if cov.get("oracle_issues") else "pass",
                       "detail": cov.get("oracle_issues", [])[:10] or "ok"})
        cov_issues = list(cov["issues"])
        if args.mode in ("report", "coverage"):
            cov_issues += cov["missing"]
            if cov["files"] > 0 and cov["seen"] == 0:
                cov_issues.append("功能测试资产缺少设计点覆盖映射（覆盖三闸）")
        cov_detail: Any = cov_issues[:10] if cov_issues else "ok"
        if args.mode == "execute":
            cov_detail = f"{cov_detail} (execute: soft)"
        checks.append({"id": "coverage-map", "status": "fail" if cov_issues else "pass", "detail": cov_detail})
    else:
        receipts = [p for p in test_root.rglob("*.md") if ("回执" in p.name or "回写" in p.name) and is_current(p)] if test_root.is_dir() else []
        if not receipts:
            blocked.append("未找到回写回执（{workroot}/**/*回执*.md）")
            checks.append({"id": "writeback-receipt", "status": "blocked", "detail": "missing"})
        else:
            receipt = max(receipts, key=lambda p: p.stat().st_mtime)
            text = read(receipt)
            issues = []
            if not re.search(r"(BUG[-_]?\d+|#\d+)", text, re.I):
                issues.append("回执缺少平台单号")
            if "备注" not in text:
                issues.append("回执缺少备注")
            if "状态" not in text:
                issues.append("回执缺少状态")
            if "附件" not in text:
                issues.append("回执缺少附件回查")
            if "已回写" in text and "待回写" not in text and not re.search(r"(noteId|备注ID|回写时间|回执)", text, re.I):
                issues.append("声称已回写但缺少回执/noteId/时间")
            if "待回写" in text and not re.search(r"(export|无权限|待回写|原因)", text, re.I):
                issues.append("待回写缺少 export/无权限/原因")
            checks.append({"id": "writeback-receipt", "status": "fail" if issues else "pass", "detail": issues or str(receipt)})

    if args.strict:
        for c in checks:
            if str(c.get("id", "")).endswith("-legacy"):
                c["status"] = "fail"
                c["detail"] = f"strict: {c.get('detail', '')}"
    soft_ids = EXECUTE_SOFT_CHECKS if args.mode == "execute" else frozenset()
    failed = [c for c in checks if c.get("status") == "fail" and c.get("id") not in soft_ids]
    soft_failed = [c for c in checks if c.get("status") == "fail" and c.get("id") in soft_ids]
    blocked_checks = [c for c in checks if c.get("status") == "blocked"]
    if args.mode == "coverage":
        verdict = "FAIL" if failed else "PASS"
    elif args.mode == "review":
        if blocked or blocked_checks:
            verdict = "BLOCKED"
        elif failed:
            verdict = "FAIL"
        elif review_conclusion == "有条件放行":
            verdict = "CONDITIONAL"
        else:
            verdict = "PASS"
    elif args.mode == "writeback":
        verdict = "BLOCKED" if blocked or blocked_checks else ("FAIL" if failed else "PASS")
    elif args.mode == "execute":
        # 步后门：只认 Scope 内台账硬检查；历史他模块/计划全集 P0 缺失不拉垮
        if blocked or blocked_checks:
            verdict = "BLOCKED"
        elif failed or p0_fail:
            verdict = "FAIL"
        elif any(aggregate.get(k, 0) for k in ("fail", "blocked", "pending", "not_run")):
            verdict = "CONDITIONAL"
        else:
            verdict = "PASS"
    else:
        # report 准出门：全仓硬
        if blocked or blocked_checks:
            verdict = "BLOCKED"
        elif failed or p0_fail or p0_missing:
            verdict = "FAIL"
        elif reported_verdict == "BLOCKED":
            verdict = "BLOCKED"
        elif reported_verdict == "FAIL":
            verdict = "FAIL"
        elif reported_verdict == "CONDITIONAL":
            verdict = "CONDITIONAL"
        elif any(aggregate.get(k, 0) for k in ("fail", "blocked", "pending", "not_run")):
            verdict = "FAIL"
        elif not reported_verdict:
            verdict = "FAIL"
        else:
            verdict = "PASS"

    now_dt = datetime.now(timezone.utc).astimezone()
    now = now_dt.isoformat(timespec="seconds")
    # gate_id 只标识“输入快照”（计划/冒烟/台账），不哈希报告本身：
    # 报告是门输出，回填 verdict/gate 后再哈希会自指、永远无法与最终门一致。
    h = hashlib.sha256()
    for p in [test_root / "test-plan.md", test_root / "smoke-checklist.md"]:
        if p.is_file():
            h.update(read(p).encode("utf-8", errors="replace"))
    ledger_files = sorted(test_root.rglob("*.md")) if test_root.is_dir() else []
    for p in ledger_files:
        if "台账" in p.name and is_current(p):
            h.update(read(p).encode("utf-8", errors="replace"))
    gate_id = f"{args.mode}-{h.hexdigest()[:12]}"
    completion = {
        "gate_version": "2.2",
        "package": PACKAGE_NAME,
        "mode": args.mode,
        "scope": scope or "",
        "gate_id": gate_id,
        "verdict": verdict,
        "counts": aggregate,
        "p0_fail": p0_fail,
        "p0_missing": p0_missing,
        "soft_failed": [c.get("id") for c in soft_failed],
        "reported_verdict": reported_verdict,
        "receipt_verdict": receipt_verdict,
        "review_conclusion": review_conclusion,
        "checks": checks,
        "blocked": blocked,
        "timestamp": now,
    }

    if args.json:
        print(json.dumps(completion, ensure_ascii=False, indent=2))
    else:
        print("=== 完成门（测试规范）===")
        print(f"verdict: {verdict}")
        if scope:
            print(f"scope: {scope}")
        print(
            f"counts: total={aggregate['total']} pass={aggregate['pass']} fail={aggregate['fail']} "
            f"blocked={aggregate['blocked']} pending={aggregate['pending']} stale={aggregate.get('stale', 0)}"
        )
        for c in checks:
            print(f"- {c['id']}: {c.get('status')} {str(c.get('detail', ''))[:160]}")
        if blocked:
            print("blocked:")
            for b in blocked[:8]:
                print(f"  - {b}")

    out = write_receipt(project_root, args.mode, completion, primary=args.mode != "writeback")
    print(f"written: {out}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
