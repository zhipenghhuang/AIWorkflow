#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate a project guide (current-state reference).

Checks the document contract, not prose quality:
- required current-state sections
- status/owner/last_reviewed frontmatter
- no version-history rows or history/process wording
- markdown table column consistency
- relative links resolve
- optional size warning

Usage:
  python rules/tools/validate_project_guide.py {workroot}/project-guide.md --strict
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = (
    ("项目概览", ("项目概览", "项目概述")),
    ("用户与角色", ("用户与角色", "角色与权限", "用户角色")),
    ("功能地图", ("功能地图", "功能清单")),
    ("核心业务链路", ("核心业务链路", "核心流程")),
    ("功能详述", ("功能详述", "功能说明")),
    ("跨模块规则", ("跨模块规则", "通用规则")),
    ("非功能要求", ("非功能要求", "非功能")),
    ("术语表", ("术语表", "术语")),
    ("当前版本与边界", ("当前版本与边界", "当前版本")),
    ("关联文档", ("关联文档", "相关文档")),
)

# 只拦“历史/过程/证据”词；不拦“当前版本”“未发布”等正常状态词。
HISTORY_WORDS = (
    "已废弃",
    "旧版",
    "迁移前",
    "本次修改",
    "本次修复",
    "本次变更",
    "回写",
    "验收记录",
    "修复记录",
    "实现进度",
    "变更记录",
    "版本记录",
    "修订记录",
    "已删除",
)

VERSION_ROW = re.compile(
    r"^\|\s*v?\d+\.\d+(?:\.\d+)?(?:[-._][A-Za-z0-9]+)?\s*\|",
    re.IGNORECASE,
)
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_frontmatter(lines: list[str]) -> tuple[dict[str, str], int]:
    if not lines or lines[0].strip() != "---":
        return {}, 0
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, 0
    data: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" in line and not line.lstrip().startswith("#"):
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip("'\"")
    return data, end + 1


def cells(line: str) -> int:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return len(s.split("|"))


def check_tables(lines: list[str]) -> list[str]:
    issues: list[str] = []
    i = 0
    while i < len(lines):
        if not lines[i].startswith("|"):
            i += 1
            continue
        start = i
        while i < len(lines) and lines[i].startswith("|"):
            i += 1
        if i - start < 2:
            continue
        header = cells(lines[start])
        # delimiter row: | --- | :---: |
        if not re.match(r"^\|[\s:\-|]+\|?\s*$", lines[start + 1]):
            continue
        for j in range(start + 2, i):
            if cells(lines[j]) != header:
                issues.append(
                    f"L{j + 1}: table column mismatch (header={header}, row={cells(lines[j])})"
                )
    return issues


def check_links(lines: list[str], path: Path) -> list[str]:
    issues: list[str] = []
    for i, line in enumerate(lines, 1):
        for raw in LINK.findall(line):
            target = raw.strip().split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if "{" in target or "}" in target:
                continue
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            p = (path.parent / target).resolve()
            if not p.exists():
                issues.append(f"L{i}: link target not found: {target}")
    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate a project guide (current-state reference).")
    ap.add_argument("path", help="project guide markdown path")
    ap.add_argument("--strict", action="store_true", help="treat missing/invalid frontmatter as error")
    ap.add_argument("--max-kb", type=int, default=400, help="size warning threshold in KB")
    args = ap.parse_args()

    path = Path(args.path)
    if not path.is_file():
        print(f"FAIL project-guide: not found: {path}")
        return 1

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors: list[str] = []
    warnings: list[str] = []

    meta, body_start = parse_frontmatter(lines)
    for key in ("status", "owner", "last_reviewed"):
        if not meta.get(key):
            (errors if args.strict else warnings).append(f"frontmatter missing: {key}")
    status = (meta.get("status") or "").lower()
    if status and status not in {"current", "published", "active"}:
        errors.append(f"frontmatter status must be current/published/active, got: {meta.get('status')}")
    reviewed = meta.get("last_reviewed") or ""
    if reviewed and not DATE.match(reviewed):
        warnings.append(f"last_reviewed is not YYYY-MM-DD: {reviewed}")

    body = lines[body_start:]
    headings = [ln.strip() for ln in body if ln.startswith("## ")]
    for label, alternatives in REQUIRED_SECTIONS:
        if not any(any(alt in h for alt in alternatives) for h in headings):
            errors.append(f"missing section: {label}")

    for i, line in enumerate(body, body_start + 1):
        if VERSION_ROW.match(line):
            errors.append(f"L{i}: version-history row is not allowed in a current-state doc")
        for word in HISTORY_WORDS:
            if word in line:
                errors.append(f"L{i}: history/process wording not allowed: {word}")

    errors.extend(check_tables(body))
    errors.extend(check_links(body, path))

    size_kb = max(1, len(text.encode("utf-8")) // 1024)
    if size_kb > args.max_kb:
        warnings.append(f"size {size_kb} KB > {args.max_kb} KB; prune or split only if needed")

    for w in warnings:
        print(f"WARN project-guide: {w}")
    for e in errors:
        print(f"FAIL project-guide: {e}")
    if errors:
        print(f"PROJECT_GUIDE FAILED ({len(errors)} error(s), {len(warnings)} warning(s))")
        return 1
    print(
        f"PROJECT_GUIDE OK ({path.name}; sections={len(headings)}; "
        f"{size_kb} KB; {len(warnings)} warning(s))"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
