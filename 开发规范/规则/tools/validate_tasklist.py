#!/usr/bin/env python3
"""Validate a task-list Markdown file generated from 任务清单模板.md.

Usage: python validate_tasklist.py <task-list.md> [--lenient]

Checks:
- required sections and summary-table columns
- unique task IDs, valid status
- every task has a task card with 验收标准/改动范围/验证/完成定义
- dependency references resolve; no self-dependency
- every summary row has a requirement point (R-xx)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "## 1. 范围与约束",
    "## 2. 任务总表",
    "## 3. 任务卡",
    "## 4. 覆盖矩阵",
    "## 5. 检查点",
    "## 6. 变更记录",
]
REQUIRED_COLUMNS = ["ID", "阶段", "任务", "要求点", "优先级", "风险", "依赖", "并行", "负责人", "预估", "状态"]
STATUSES = {"未开始", "进行中", "阻塞", "待验收", "完成", "取消"}
ID_RE = re.compile(r"^T-\d+$")
RP_RE = re.compile(r"\bR-\d+\b")


def split_row(line: str) -> list[str]:
    # Split a Markdown table row on unescaped pipes.
    cells: list[str] = []
    buf: list[str] = []
    escaped = False
    for ch in line.strip().strip("|"):
        if escaped:
            buf.append(ch)
            escaped = False
        elif ch == "\\":
            escaped = True
        elif ch == "|":
            cells.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    cells.append("".join(buf).strip())
    return cells


def main() -> int:
    if len(sys.argv) < 2:
        print("USAGE: validate_tasklist.py <task-list.md> [--lenient]")
        return 2
    path = Path(sys.argv[1])
    lenient = "--lenient" in sys.argv
    if not path.exists():
        print(f"TASKLIST_MISSING: {path}")
        return 1
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"MISSING_SECTION: {section}")

    # Summary table
    lines = text.splitlines()
    header_idx = None
    header: list[str] = []
    for i, line in enumerate(lines):
        if line.strip().startswith("|") and "ID" in line and "状态" in line and "任务" in line:
            header = split_row(line)
            header_idx = i
            break
    if header_idx is None:
        errors.append("MISSING_SUMMARY_TABLE: no table with ID/任务/状态")
        header = []
    else:
        for col in REQUIRED_COLUMNS:
            if col not in header:
                errors.append(f"MISSING_COLUMN: {col}")
        if len(header) != len(REQUIRED_COLUMNS):
            warnings.append(f"COLUMN_COUNT: header has {len(header)} columns, template expects {len(REQUIRED_COLUMNS)}")

    rows: list[list[str]] = []
    if header_idx is not None:
        for line in lines[header_idx + 2:]:
            if not line.strip().startswith("|"):
                if rows:
                    break
                continue
            rows.append(split_row(line))
    ids: list[str] = []
    for row in rows:
        if not row or not row[0]:
            continue
        tid = row[0].strip("` ")
        if not ID_RE.match(tid):
            errors.append(f"BAD_ID: {tid!r} (expect T-01)")
            continue
        ids.append(tid)
        if len(row) < len(REQUIRED_COLUMNS):
            errors.append(f"BAD_ROW: {tid}: expected {len(REQUIRED_COLUMNS)} cells, got {len(row)}")
            continue
        status = row[header.index("状态")] if "状态" in header else ""
        if status and status not in STATUSES and not status.startswith("{"):
            errors.append(f"BAD_STATUS: {tid}: {status!r}")
        rp = row[header.index("要求点")] if "要求点" in header else ""
        if not RP_RE.search(rp) and not rp.startswith("{"):
            warnings.append(f"NO_RP: {tid}: {rp!r}")
        dep = row[header.index("依赖")] if "依赖" in header else ""
        for ref in re.findall(r"T-\d+", dep):
            if ref == tid:
                errors.append(f"SELF_DEPENDENCY: {tid}")
            elif ref not in ids and ref not in [r[0].strip("` ") for r in rows]:
                errors.append(f"UNKNOWN_DEPENDENCY: {tid} -> {ref}")

    if len(ids) != len(set(ids)):
        errors.append("DUPLICATE_ID: summary table has duplicate IDs")

    # Task cards
    card_ids = re.findall(r"^###\s+(T-\d+)\b", text, flags=re.M)
    for tid in ids:
        if tid not in card_ids:
            errors.append(f"MISSING_CARD: {tid}")
    for tid in card_ids:
        if tid not in ids:
            errors.append(f"ORPHAN_CARD: {tid} not in summary table")
            continue
        start = text.find(f"### {tid}")
        next_card = text.find("\n### ", start + 1)
        block = text[start: next_card if next_card != -1 else len(text)]
        for key in ("验收标准", "改动范围", "验证", "完成定义"):
            if key not in block:
                errors.append(f"CARD_FIELD: {tid}: missing {key}")

    # Coverage matrix should mention at least one RP if summary has RPs.
    if "## 4. 覆盖矩阵" in text and not RP_RE.search(text.split("## 4. 覆盖矩阵", 1)[1].split("## 5.", 1)[0]):
        warnings.append("COVERAGE_EMPTY: no R-xx in 覆盖矩阵")

    for w in warnings:
        print(f"WARN: {w}")
    if errors and not lenient:
        for e in errors:
            print(f"ERROR: {e}")
        print(f"TASKLIST_VALIDATION_FAILED: {len(errors)} error(s)")
        return 1
    if errors and lenient:
        for e in errors:
            print(f"WARN(lenient): {e}")
    print(f"TASKLIST_VALIDATION_OK: {len(ids)} task(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
