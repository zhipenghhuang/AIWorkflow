#!/usr/bin/env python3
"""Validate a 开发计划 Markdown file.

Usage: python validate_dev_plan.py <dev-plan.md> [--lenient]

Checks sections, stage table, status values, current stage, gate tokens,
multi-wave (W{n} / G{n}-W{k}) hints, and basic next-action/link presence.
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
    "## 12. 执行日志（只追加）",
    "## 13. 迭代索引与归档",
    "## 14. 质量指标（DORA + 交付质量）",
    "## 15. 追溯矩阵（PRD F/A/AC → RP/AC → 任务 → 测试 → 发布）",
]
COLUMNS = ["阶段", "技能", "状态", "负责人", "输入", "动作", "产出", "门", "证据", "下一步"]
STATUSES = {"未开始", "进行中", "部分完成", "阻塞", "待评审", "完成", "不适用"}
STAGE_RE = re.compile(r"S\d{1,2}\s")
GATE_RE = re.compile(r"G\d{1,2}\b")
WAVE_RE = re.compile(r"\bW\d+\b|波次")
GATE_WAVE_RE = re.compile(r"G\d{1,2}\s*[-–]?\s*W\d+", re.I)
STAGE_NUM_RE = re.compile(r"S\d{1,2}")


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

    def section_block(title: str) -> str:
        if title not in text:
            return ""
        return text.split(title, 1)[1].split("\n## ", 1)[0]

    exec_log = section_block("## 12. 执行日志（只追加）")
    if exec_log and not re.search(r"(?m)^\|\s*(?:\d{4}-\d{2}-\d{2}|日期)", exec_log):
        warnings.append("EXEC_LOG: §12 执行日志无日期行（只追加）")
    trace = section_block("## 15. 追溯矩阵（PRD F/A/AC → RP/AC → 任务 → 测试 → 发布）")
    if trace and not re.search(r"\b(?:F|R|A|AC|RP|T)-\d+", trace):
        warnings.append("TRACE: §15 追溯矩阵无 F/R/A/AC/RP/T 编号")

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
            # Allow "进行中（W3）" style: primary token must be a known status
            status_token = status.split("（")[0].split("(")[0].strip() if status else ""
            if status and status not in STATUSES and status_token not in STATUSES and not status.startswith("{"):
                errors.append(f"BAD_STATUS: {stage}: {status!r}")
            if gate and not GATE_RE.search(gate) and not gate.startswith("{"):
                warnings.append(f"GATE_FORMAT: {stage}: {gate!r}")
            if not evidence or evidence in {"{链接}", "{…}", ""}:
                warnings.append(f"NO_EVIDENCE: {stage}: {evidence!r}")
            # Multi-wave: S2～S5 marked 完成 must carry wave labels in the row
            stage_num = STAGE_NUM_RE.search(stage or "")
            if (
                stage_num
                and stage_num.group(0) in {"S2", "S3", "S4", "S5"}
                and status_token == "完成"
                and WAVE_RE.search(text)
                and not WAVE_RE.search("|".join(row))
            ):
                warnings.append(
                    f"MULTI_WAVE_BARE_DONE: {stage}: 启用波次时 S2～S5 标完成须在行内标注 Wn"
                )
        if not rows:
            errors.append("EMPTY_STAGE_TABLE")
        # Current stage consistency (lenient: allow placeholder; allow S2-W3 / S2（W3）)
        m = re.search(r"当前阶段[：:]\s*([^\n]+)", text)
        if m and stage_names and not lenient:
            cur = m.group(1).strip()
            cur_num = STAGE_NUM_RE.search(cur)
            matched = any(s and (s in cur or cur in s) for s in stage_names)
            if not matched and cur_num:
                sn = cur_num.group(0)
                matched = any(sn in (s or "") for s in stage_names)
            if not matched:
                errors.append(f"CURRENT_STAGE_NOT_IN_TABLE: {cur!r}")

    # Multi-wave control plane
    if WAVE_RE.search(text) and not GATE_WAVE_RE.search(text):
        warnings.append(
            "MULTI_WAVE_GATES: 启用波次时建议门结论写 G{n}-W{k}（见 development-plan §3.1）"
        )

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
