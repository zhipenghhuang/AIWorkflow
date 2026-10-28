#!/usr/bin/env python3
"""Validate a handoff package folder.

Usage: python validate_handoff.py <package-dir>
Exit 0 = OK; 1 = errors; 2 = usage/path error.

Checks:
- required files: 00-交接说明.md, 01-交接清单.md, 04-回执/接收回执.md
- 00 has the required metadata fields and sections
- 01 has a manifest table with 包内路径 and at least one row
- every 02-文档/03-证据/04-回执 path mentioned in 01 exists
- package folder name looks like HO-yyyyMMdd-NN-TYPE-FROM2TO (TO=DEV|QA|ALL|DEVQA|...)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED = [
    "00-交接说明.md",
    "01-交接清单.md",
    "04-回执/接收回执.md",
]
META = ["交接 ID", "类型", "发起方", "接收方", "版本", "状态", "日期", "回执截止"]
SECTIONS = ["接收方要做的事", "验收/完成标准", "回执要求"]
ID_RE = re.compile(r"^HO-\d{8}-\d{2,3}-[A-Z]{2,5}-[A-Z]{2,4}2[A-Z]{2,12}$")


def split_row(line: str) -> list[str]:
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
        print("USAGE: validate_handoff.py <package-dir>")
        return 2
    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"HANDOFF_PATH_MISSING: {root}")
        return 2

    errors: list[str] = []
    for rel in REQUIRED:
        if not (root / rel).is_file():
            errors.append(f"MISSING_FILE: {rel}")

    brief = root / "00-交接说明.md"
    text = brief.read_text(encoding="utf-8") if brief.is_file() else ""
    for key in META:
        if not re.search(rf"\|\s*{re.escape(key)}\s*\|", text):
            errors.append(f"MISSING_META: 00-交接说明.md: {key}")
    for sec in SECTIONS:
        if not re.search(rf"^#+\s*.*{re.escape(sec)}", text, flags=re.M):
            errors.append(f"MISSING_SECTION: 00-交接说明.md: {sec}")

    if not ID_RE.match(root.name):
        errors.append(f"BAD_PACKAGE_ID: {root.name} (expect HO-yyyyMMdd-NN-TYPE-FROM2TO; multi-recv use ALL or DEVQA)")
    if text:
        m = re.search(r"\|\s*交接 ID\s*\|\s*`?([^|`]+)`?", text)
        if m and m.group(1).strip() != root.name:
            errors.append(f"ID_MISMATCH: folder={root.name} brief={m.group(1).strip()}")

    manifest = root / "01-交接清单.md"
    mtext = manifest.read_text(encoding="utf-8") if manifest.is_file() else ""
    header = None
    header_idx = None
    lines = mtext.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("|") and "包内路径" in line and "必读" in line:
            header = split_row(line)
            header_idx = i
            break
    if header is None:
        errors.append("MISSING_MANIFEST_TABLE: 01-交接清单.md (need 包内路径/必读)")
    else:
        rows = 0
        path_col = header.index("包内路径")
        for line in lines[header_idx + 2:]:
            if not line.strip().startswith("|"):
                if rows:
                    break
                continue
            cells = split_row(line)
            if len(cells) <= path_col:
                continue
            raw = cells[path_col].strip().strip("`").replace("\\", "/")
            if not raw or raw.startswith("{"):
                continue
            rows += 1
            if raw.startswith(("02-文档/", "03-证据/", "04-回执/")):
                if not (root / raw).exists():
                    errors.append(f"MANIFEST_PATH_MISSING: {raw}")
        if rows == 0:
            errors.append("EMPTY_MANIFEST: 01-交接清单.md has no file rows")

    if errors:
        for e in errors:
            print(e)
        print(f"HANDOFF_VALIDATION_FAILED: {len(errors)} issue(s)")
        return 1
    print(f"HANDOFF_VALIDATION_OK: {root.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
