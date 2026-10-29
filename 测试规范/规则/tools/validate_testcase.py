#!/usr/bin/env python3
"""Validate a module test-case document (index + structured cases).

Usage: python validate_testcase.py <module-testcase.md> [--legacy]

`--legacy`：把“模板化空话/场景空话”降为 WARN，用于审计历史资产；
新生成/新修改用例默认严格（ERROR），避免“结构对齐但不可执行”。

Checks (errors):
- required sections 0-5
- module overview table has required columns
- overview IDs and detail IDs match
- every detail case has preconditions / data / steps / expected / cleanup / evidence / traceability
- step table has 位置/操作/数据/中间预期
- expected table has 可观测判定面/失败判定
- at least one P0-Smoke case

Warnings:
- no F-/A-/AC- traceability IDs in overview
- fewer than 3 steps / more than 10 steps

Errors (filler / non-executable phrasing):
- banned step/location boilerplate that blocks follow-along execution

Exit 0 = pass (warnings allowed); 1 = errors; 2 = usage.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

CASE_ID = re.compile(r"\b([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d+)\b")
CASE_HEADING = re.compile(r"^###\s+([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d+)\s+(.+)$", re.M)
REQUIRED_SECTIONS = [
    "## 0. 模块信息",
    "## 1. 模块用例总览",
    "## 2. 用例详情",
    "## 3. 设计点覆盖映射",
    "## 4. 覆盖摘要",
    "## 5. 评审与变更",
]
# High-signal empty steps that previously led to freelanced execute paths.
BANNED_FILLERS = [
    "以模块文档头部入口为准",
    "本步结果可在页面核对",
    "禁臆造未验证路由",
    # 2026-10 实际资产审计新增：这些短语会让用例“看起来结构化、实际不可跟做”
    "按场景数据",
    "同业务详情/列表/弹层",
    "展示值可记录并与手算/前置对照",
    "提交结果可回查（成功提示或状态更新）",
    "样本见前置",
]
GENERIC_SCENARIO = "在模块入口验证「"


def section(text: str, start: str, end: str | None) -> str:
    i = text.find(start)
    if i < 0:
        return ""
    i += len(start)
    j = text.find(end, i) if end else -1
    return text[i:j] if j >= 0 else text[i:]


def numbered_rows(block: str) -> int:
    """只数表格里的编号数据行，不把正文编号/预期表混进步骤数。"""
    return sum(1 for ln in block.splitlines() if re.match(r"^\|\s*\d+\s*\|", ln))


def table_headers(block: str) -> list[list[str]]:
    headers: list[list[str]] = []
    lines = block.splitlines()
    for i, line in enumerate(lines[:-1]):
        if not line.strip().startswith("|"):
            continue
        nxt = lines[i + 1].strip()
        if not re.match(r"^\|[\s:|-]+\|$", nxt):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        headers.append(cells)
    return headers


def has_cols(headers: list[list[str]], cols: list[str]) -> bool:
    return any(all(any(col in cell for cell in h) for col in cols) for h in headers)


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    legacy = "--legacy" in sys.argv
    if not args:
        print("USAGE: validate_testcase.py <module-testcase.md> [--legacy]")
        return 2
    path = Path(args[0])
    if not path.exists():
        print(f"FILE_NOT_FOUND: {path}")
        return 2
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    for s in REQUIRED_SECTIONS:
        if s not in text:
            errors.append(f"MISSING_SECTION: {s}")

    overview = section(text, "## 1. 模块用例总览", "## 2. 用例详情")
    details = section(text, "## 2. 用例详情", "## 3. 设计点覆盖映射")
    if overview:
        h = table_headers(overview)
        required = ["用例 ID", "标题", "优先级", "类型", "关联需求", "步骤数", "脚本", "最近结果"]
        if not has_cols(h, required):
            errors.append("OVERVIEW_COLUMNS: 需要 用例ID/标题/优先级/类型/关联需求AC/步骤数/脚本/最近结果")
        if "P0-Smoke" not in overview:
            errors.append("NO_P0_SMOKE: 模块总览至少 1 条 P0-Smoke")
        if not re.search(r"(F-\d+|A-\d+|AC-\d+)", overview):
            warnings.append("TRACEABILITY_IDS: 总览未见 F-/A-/AC- 编号（可先用设计点过渡）")

    overview_ids = set(re.findall(r"^\|\s*([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d+)\s*\|", overview, re.M))
    detail_ids = {m.group(1) for m in CASE_HEADING.finditer(details)}

    if not detail_ids:
        errors.append("NO_CASES: §2 未找到 `### {ID} {标题}` 用例")
    for cid in sorted(detail_ids - overview_ids):
        errors.append(f"CASE_NOT_IN_OVERVIEW: {cid}")
    for cid in sorted(overview_ids - detail_ids):
        errors.append(f"CASE_NOT_IN_DETAILS: {cid}")

    # split detail blocks
    matches = list(CASE_HEADING.finditer(details))
    for idx, m in enumerate(matches):
        cid = m.group(1)
        start = m.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(details)
        block = details[start:end]
        for label in ["**前置条件**", "**测试数据**", "**清理", "**证据要求**", "**追溯**"]:
            if label not in block:
                errors.append(f"{cid}: MISSING {label}")
        if "**步骤" not in block:
            errors.append(f"{cid}: MISSING **步骤**")
            continue
        if "**预期" not in block:
            errors.append(f"{cid}: MISSING **预期**")
        h = table_headers(block)
        if not has_cols(h, ["位置", "操作", "数据", "中间预期"]):
            errors.append(f"{cid}: STEP_TABLE 需要 位置/操作/数据/中间预期")
        if not has_cols(h, ["判定面", "失败判定"]):
            errors.append(f"{cid}: EXPECTED_TABLE 需要 可观测判定面/失败判定")
        step_block = section(block, "**步骤", "**预期")
        exp_block = section(block, "**预期", "**清理")
        step_rows = numbered_rows(step_block)
        exp_rows = numbered_rows(exp_block)
        if step_rows < 3:
            warnings.append(f"{cid}: 步骤少于 3 步（确认是否过粗）")
        if step_rows > 10:
            warnings.append(f"{cid}: 步骤超过 10 步（考虑拆条）")
        if exp_rows == 0:
            errors.append(f"{cid}: EXPECTED_ROWS: 预期表没有编号判定行")
        elif exp_rows < step_rows and "合并" not in block:
            warnings.append(
                f"{cid}: EXPECTED_ROWS: 预期 {exp_rows} 行 < 步骤 {step_rows} 行；"
                "须逐步同号，或写明哪些步骤合并判定"
            )
        for phrase in BANNED_FILLERS:
            if phrase in block:
                msg = f"{cid}: FILLER_STEP: 含空话「{phrase}」——须写清场景载体入口/动作"
                (warnings if legacy else errors).append(msg)
        # Soft: whole-cell “执行批量” without a named business action nearby
        if re.search(r"\|\s*执行批量\s*\|", block) and not re.search(
            r"(分配|审批|关闭|提交|确认|导入|导出|催办|移交)", block
        ):
            errors.append(f"{cid}: FILLER_STEP: 「执行批量」未点名业务动作（分配/审批等）")
        if GENERIC_SCENARIO in block:
            warnings.append(
                f"{cid}: GENERIC_SCENARIO: 一句话场景仍是「在模块入口验证…」模板句，"
                "建议写谁在什么场景做什么（不单独阻断，但评审应修）"
            )

    if not re.search(r"## 5\. 评审与变更", text):
        errors.append("MISSING_SECTION: ## 5. 评审与变更")

    for w in warnings:
        print(f"WARN: {w}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        print(f"TESTCASE_VALIDATION_FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"TESTCASE_VALIDATION_OK: {len(detail_ids)} case(s), {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
