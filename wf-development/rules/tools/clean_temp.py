#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Conservative temp cleaner for a project that installed this package.

Default is dry-run: prints what would be removed. Use --apply to delete.
Never touches source, docs, inbound/, _archive/, or gate receipts (*.json).
"""
from __future__ import annotations

import argparse
import shutil
import time
from pathlib import Path

SKIP_DIR_NAMES = {".git", "node_modules", ".venv", "venv"}
SKIP_TOP = {"inbound", "docs", "_archive"}


def age_days(path: Path) -> float:
    try:
        return (time.time() - path.stat().st_mtime) / 86400
    except OSError:
        return 0.0


def iter_targets(root: Path, days: float, reset_frontend: bool):
    for p in root.rglob("__pycache__"):
        if p.is_dir() and not (set(p.parts) & SKIP_DIR_NAMES):
            yield ("pycache", p)
    for p in root.rglob("*.pyc"):
        if p.is_file() and p.parent.name != "__pycache__":
            yield ("pyc", p)
    for name in (".draft",):
        for p in root.rglob(name):
            if p.is_dir() and not (set(p.parts) & SKIP_DIR_NAMES):
                if p.parts and p.parts[0] in SKIP_TOP:
                    continue
                if age_days(p) >= days:
                    yield (name.lstrip("."), p)
    logs = root / ".gate" / "logs"
    if logs.is_dir():
        for p in logs.rglob("*"):
            if p.is_file() and age_days(p) >= days:
                yield ("gate-log", p)
    if reset_frontend:
        front = root / ".gate" / "frontend"
        if front.is_dir():
            yield ("frontend", front)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--days", type=float, default=7.0)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--reset-frontend", action="store_true")
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    seen: set[Path] = set()
    plan = []
    for kind, path in iter_targets(root, args.days, args.reset_frontend):
        if path in seen:
            continue
        seen.add(path)
        plan.append((kind, path))

    total = 0
    for kind, path in plan:
        if path.is_dir():
            size = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
            n = sum(1 for f in path.rglob("*") if f.is_file())
        else:
            size = path.stat().st_size if path.exists() else 0
            n = 1
        total += size
        print(f"[{kind}] {path.relative_to(root)}  files={n}  {size / 1024:.1f}KB")

    print(f"SUMMARY targets={len(plan)} size={total / 1024:.1f}KB mode={'apply' if args.apply else 'dry-run'}")
    if not args.apply:
        print("未删除任何文件；确认后加 --apply。")
        return 0
    for kind, path in plan:
        try:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
        except OSError as exc:
            print(f"SKIP {path}: {exc}")
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
