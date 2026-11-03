#!/usr/bin/env python3
"""Validate a product PRD v2.

Usage: python validate_prd.py <PRD.md>

Checks:
- frontmatter keys: doc_id/title/status/version/owner/updated
- sections 0-16
- at least one Mermaid flowchart; stateDiagram only when the PRD declares state/flow content
- F-/R-/A-/AC- IDs present
- traceability matrix columns F/R/A/AC
- decision table Q/C with 责任人/期限
Warnings:
- no prototype link
- technical architecture wording (should live in dev 方案/ADR)
- TBD without owner/date

Exit 0 = pass (warnings allowed); 1 = errors; 2 = usage.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [f"## {i}." for i in range(0, 17)]
FRONTMATTER_KEYS = ["doc_id", "title", "status", "version", "owner", "updated"]


def has_cols(block: str, cols: list[str]) -> bool:
    lines = block.splitlines()
    for i, line in enumerate(lines[:-1]):
        if not line.strip().startswith("|"):
            continue
        if not re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(any(c in cell for cell in cells) for c in cols):
            return True
    return False


def main() -> int:
    if len(sys.argv) < 2:
        print("USAGE: validate_prd.py <PRD.md>")
        return 2
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"FILE_NOT_FOUND: {path}")
        return 2
    text = path.read_text(encoding="utf-8-sig")
    errors: list[str] = []
    warnings: list[str] = []

    if not text.startswith("---"):
        errors.append("FRONTMATTER: 缺少 YAML frontmatter")
    else:
        end = text.find("\n---", 3)
        fm = text[3:end] if end > 0 else ""
        for key in FRONTMATTER_KEYS:
            if not re.search(rf"^{re.escape(key)}\s*:", fm, re.M):
                errors.append(f"FRONTMATTER: 缺少 {key}")

    for s in REQUIRED_SECTIONS:
        if s not in text:
            errors.append(f"MISSING_SECTION: {s}")

    if not re.search(r"```mermaid\s*\n\s*(flowchart|graph)", text):
        errors.append("MERMAID: 缺少 flowchart 主流程")
    # State machine is only required for stateful products; a report/filter/export
    # feature should not have to fabricate a state diagram.
    stateful = re.search(r"(状态机|状态流转|生命周期|审批流|订单状态|工单状态|状态迁移|status\s*flow)", text, re.I)
    has_state = bool(re.search(r"```mermaid\s*\n\s*stateDiagram", text))
    if stateful and not has_state:
        errors.append("MERMAID: 有状态/流转内容，但缺少 stateDiagram 状态机")
    elif not stateful and not has_state:
        warnings.append("MERMAID: 未检测到状态流转，已跳过 stateDiagram（如确有状态请补）")

    for prefix in ["F-", "R-", "A-", "AC-"]:
        if not re.search(rf"\b{prefix}\d+", text):
            errors.append(f"IDS: 缺少 {prefix}xx 编号")

    if not has_cols(text, ["需求 F", "规则 R", "验收场景 A", "AC"]):
        errors.append("TRACEABILITY: 追溯矩阵需含 需求F/规则R/验收场景A/AC 列")
    else:
        # Header-only matrix is not traceability. Require at least one data row
        # with F/R/A/AC values.
        lines = text.splitlines()
        for i, line in enumerate(lines[:-1]):
            if not line.strip().startswith("|") or not re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(any(c in cell for cell in cells) for c in ["需求 F", "规则 R", "验收场景 A", "AC"]):
                j = i + 2
                good = 0
                while j < len(lines) and lines[j].strip().startswith("|"):
                    vals = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                    if len(vals) >= 4 and all(vals[k] for k in range(4)):
                        good += 1
                    j += 1
                if good == 0:
                    errors.append("TRACEABILITY: 追溯矩阵无有效数据行（F/R/A/AC 不能为空）")
                break
    if not has_cols(text, ["类型", "问题/决策", "责任人", "期限"]):
        warnings.append("DECISIONS: 待确认/决策表建议含 类型/问题/责任人/期限")

    if "原型" not in text:
        warnings.append("PROTOTYPE: 未见原型链接/路径")
    if re.search(r"(技术架构|技术栈|数据库设计|API 设计|部署拓扑)", text):
        warnings.append("TECH_BOUNDARY: 出现技术架构措辞，确认未越界（技术方案归开发）")
    if re.search(r"待确认", text) and not re.search(r"(责任人|期限|owner|due)", text):
        warnings.append("TBD: 有待确认项但未见责任人/期限")

    for w in warnings:
        print(f"WARN: {w}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        print(f"PRD_VALIDATION_FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PRD_VALIDATION_OK: {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
