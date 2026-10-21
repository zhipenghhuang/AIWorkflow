#!/usr/bin/env python3
"""Validate a product PRD v2.

Usage: python validate_prd.py <PRD.md>

Checks:
- frontmatter keys: doc_id/title/status/version/owner/updated
- sections 0-16
- at least one Mermaid flowchart and one stateDiagram
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
    text = path.read_text(encoding="utf-8")
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

    if len(re.findall(r"```mermaid", text)) < 2:
        errors.append("MERMAID: 至少 2 个 Mermaid 块（主流程 + 状态机）")
    if not re.search(r"```mermaid\s*\n\s*(flowchart|graph)", text):
        errors.append("MERMAID: 缺少 flowchart 主流程")
    if not re.search(r"```mermaid\s*\n\s*stateDiagram", text):
        errors.append("MERMAID: 缺少 stateDiagram 状态机")

    for prefix in ["F-", "R-", "A-", "AC-"]:
        if not re.search(rf"\b{prefix}\d+", text):
            errors.append(f"IDS: 缺少 {prefix}xx 编号")

    if not has_cols(text, ["需求 F", "规则 R", "验收场景 A", "AC"]):
        errors.append("TRACEABILITY: 追溯矩阵需含 需求F/规则R/验收场景A/AC 列")
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
