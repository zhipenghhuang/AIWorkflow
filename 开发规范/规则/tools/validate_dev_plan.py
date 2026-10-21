#!/usr/bin/env python3
"""Validate a 开发计划 Markdown file.

Usage: python validate_dev_plan.py <dev-plan.md> [--lenient]

Checks sections, stage table, status values, current stage, gate tokens,
and basic next-action/link presence.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SECTIONS = [
    "## 0. 一页状态",
    "## 1. 阶段与门",
    "## 2. 输入与范围",
    "## 3. 需求分析",
    "## 4. 技术方案",
    "## 5. 任务与排期",
    "## 6. 执行与验证",
    "## 7. 提测与缺陷",
    "## 8. 发布与交接",
    "## 9. 风险、依赖、决策",
    "## 10. 变更记录",
    "## 11. 关联文档",
]
COLUMNS = ["阶段", "技能", "状态", "负责人", "输入", "动作", "产出", "门", "证据", "下一步"]
STATUSES = {"未开始", "进行中", "阻塞", "待评审", "完成", "不适用"}
STAGE_RE = re.compile(r"S\d{1,2}\s")
GATE_RE = re.compile(r"G\d{1,2}\b")


def split_row(line: str) -> list[str]:
    cells, buf, escaped = [], [], False
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
        print("USAGE: validate_dev_plan.py <dev-plan.md> [--lenient]")
        return 2
    path = Path(sys.argv[1])
    lenient = "--lenient" in sys.argv
    if not path.exists():
        print(f"DEV_PLAN_MISSING: {path}")
        return 1
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    for section in SECTIONS:
        if section not in text:
            errors.append(f"MISSING_SECTION: {section}")

    # Current status
    for key in ("当前阶段", "健康度", "下一步 3 件事"):
        if key not in text:
            errors.append(f"MISSING_STATUS: {key}")
    if not re.search(r"健康度[：:]\s*(绿|黄|红)", text):
        warnings.append("HEALTH: 健康度未填 绿/黄/红")

    # Stage table
    lines = text.splitlines()
    header_idx = None
    header: list[str] = []
    for i, line in enumerate(lines):
        if line.strip().startswith("|") and "阶段" in line and "状态" in line and "门" in line:
            header = split_row(line)
            header_idx = i
            break
    if header_idx is None:
        errors.append("MISSING_STAGE_TABLE: no table with 阶段/状态/门")
    else:
        for col in COLUMNS:
            if col not in header:
                errors.append(f"MISSING_COLUMN: {col}")
        rows: list[list[str]] = []
        for line in lines[header_idx + 2:]:
            if not line.strip().startswith("|"):
                if rows:
                    break
                continue
            rows.append(split_row(line))
        stage_names: list[str] = []
        for row in rows:
            if len(row) < len(COLUMNS):
                errors.append(f"BAD_STAGE_ROW: expected {len(COLUMNS)} cells, got {len(row)}")
                continue
            stage = row[header.index("阶段")] if "阶段" in header else row[0]
            skill = row[header.index("技能")] if "技能" in header else ""
            status = row[header.index("状态")] if "状态" in header else ""
            gate = row[header.index("门")] if "门" in header else ""
            evidence = row[header.index("证据")] if "证据" in header else ""
            stage_names.append(stage)
            if not skill:
                errors.append(f"NO_SKILL: {stage}")
            if status and status not in STATUSES and not status.startswith("{"):
                errors.append(f"BAD_STATUS: {stage}: {status!r}")
            if gate and not GATE_RE.search(gate) and not gate.startswith("{"):
                warnings.append(f"GATE_FORMAT: {stage}: {gate!r}")
            if not evidence or evidence in {"{链接}", "{…}", ""}:
                warnings.append(f"NO_EVIDENCE: {stage}: {evidence!r}")
        if not rows:
            errors.append("EMPTY_STAGE_TABLE")
        # Current stage consistency (lenient: allow placeholder)
        m = re.search(r"当前阶段[：:]\s*([^\n]+)", text)
        if m and stage_names and not lenient:
            cur = m.group(1).strip()
            if not any(s and (s in cur or cur in s) for s in stage_names):
                errors.append(f"CURRENT_STAGE_NOT_IN_TABLE: {cur!r}")

    # Gate coverage
    for i in range(10):
        if f"G{i}" not in text:
            warnings.append(f"GATE_MISSING: G{i}")

    for w in warnings:
        print(f"WARN: {w}")
    if errors and not lenient:
        for e in errors:
            print(f"ERROR: {e}")
        print(f"DEV_PLAN_VALIDATION_FAILED: {len(errors)} error(s)")
        return 1
    if errors and lenient:
        for e in errors:
            print(f"WARN(lenient): {e}")
    print("DEV_PLAN_VALIDATION_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
