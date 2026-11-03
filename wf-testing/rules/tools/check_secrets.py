#!/usr/bin/env python3
# 同源脚本：三包内容一致；改一处需同步另外两包。
"""Scan a package tree for hardcoded credentials.

Usage: python check_secrets.py <package-root>

Checks literal password/token assignments and `env || 'literal'` fallbacks.
Prints file:line and variable name only; never prints the value.
Exit 0 = no suspect; 1 = suspect found; 2 = usage/error.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", ".draft", ".state", ".gate", "__pycache__", "node_modules", ".venv"}
TEXT_EXTS = {".md", ".yaml", ".yml", ".json", ".py", ".ps1", ".mjs", ".js", ".bat", ".txt"}
PLACEHOLDERS = {
    "password", "passwd", "pwd", "secret", "token", "changeme", "change-me",
    "example", "yourpassword", "your-password", "******", "xxxxxx", "todo",
    "placeholder", "test", "demo",
}
ASSIGN = re.compile(
    r"(?i)\b(password|passwd|pwd|secret|api[_-]?key|access[_-]?token|auth[_-]?token|token)\b"
    r"\s*[:=]\s*['\"]([^'\"]{6,})['\"]"
)
FALLBACK = re.compile(
    r"(?i)\b(password|passwd|pwd|secret|api[_-]?key|access[_-]?token|auth[_-]?token|token)\b"
    r"\s*=.*?\|\|\s*['\"]([^'\"]{6,})['\"]"
)


def suspect_value(value: str) -> bool:
    v = value.strip()
    if not v:
        return False
    if any(ch in v for ch in "{}<>"):
        return False
    if "process.env" in v or "env." in v:
        return False
    return v.lower() not in PLACEHOLDERS


def scan(root: Path) -> list[tuple[Path, int, str]]:
    hits: list[tuple[Path, int, str]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTS:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for pattern in (ASSIGN, FALLBACK):
                m = pattern.search(line)
                if m and suspect_value(m.group(2)):
                    hits.append((path, lineno, m.group(1)))
                    break
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"SECRET_CHECK_USAGE: not a directory: {root}")
        return 2
    hits = scan(root)
    for path, lineno, name in hits:
        print(f"SECRET_SUSPECT: {path.relative_to(root)}:{lineno}: {name}=<redacted>")
    if hits:
        print(f"SECRET_CHECK_FAILED: {len(hits)} suspect(s)")
        return 1
    print("SECRET_CHECK_OK (no hardcoded password/token literal found)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
