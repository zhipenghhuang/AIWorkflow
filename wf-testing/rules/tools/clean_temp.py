#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Conservative temp cleaner for a project that installed this package.

Default is dry-run: prints what would be removed. Use --apply to delete.
Never touches source files, inbound/, _archive/, or gate receipts.
--reset-frontend archives .gate/frontend before rebuilding it.
"""
from __future__ import annotations

import argparse
import shutil
import time
from datetime import datetime
from pathlib import Path

SKIP_DIR_NAMES = {".git", "node_modules", ".venv", "venv"}
SKIP_PATH_PARTS = {"inbound", "_archive"}


def rel_parts(root: Path, path: Path) -> tuple[str, ...]:
    try:
        return path.relative_to(root).parts
    except ValueError:
        return path.parts


def newest_mtime(path: Path) -> float:
    try:
        newest = path.stat().st_mtime
    except OSError:
        return 0.0
    if path.is_dir():
        for child in path.rglob("*"):
            try:
                if child.is_file():
                    newest = max(newest, child.stat().st_mtime)
            except OSError:
                pass
    return newest


def age_days(path: Path) -> float:
    return (time.time() - newest_mtime(path)) / 86400


def iter_targets(root: Path, days: float, reset_frontend: bool,
                 archive_keep: int, archive_days: float):
    for p in root.rglob("__pycache__"):
        if p.is_dir() and not (set(p.parts) & SKIP_DIR_NAMES):
            if not (set(rel_parts(root, p)) & SKIP_PATH_PARTS):
                yield ("pycache", p)
    for p in root.rglob("*.pyc"):
        if p.is_file() and p.parent.name != "__pycache__":
            if not (set(rel_parts(root, p)) & SKIP_PATH_PARTS):
                yield ("pyc", p)
    for p in root.rglob(".draft"):
        if p.is_dir() and not (set(p.parts) & SKIP_DIR_NAMES):
            if set(rel_parts(root, p)) & SKIP_PATH_PARTS:
                continue
            if age_days(p) >= days:
                yield ("draft", p)
    logs = root / ".gate" / "logs"
    if logs.is_dir():
        for p in logs.rglob("*"):
            if p.is_file() and age_days(p) >= days:
                yield ("gate-log", p)
    if reset_frontend:
        front = root / ".gate" / "frontend"
        if front.is_dir():
            yield ("frontend", front)
    archive = root / ".gate" / "archive"
    if archive.is_dir():
        task_dirs = [d for d in archive.iterdir() if d.is_dir()]
        task_dirs.sort(key=newest_mtime, reverse=True)
        keep = set(task_dirs[:archive_keep]) if archive_keep > 0 else set()
        for d in task_dirs:
            by_keep = archive_keep > 0 and d not in keep
            by_age = archive_days > 0 and age_days(d) >= archive_days
            if by_keep or by_age:
                yield ("gate-archive", d)


def archive_frontend(root: Path) -> str:
    front = root / ".gate" / "frontend"
    if not front.is_dir():
        return ""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    base = root / ".gate" / "archive" / f"manual-{stamp}"
    i = 1
    while base.exists():
        base = root / ".gate" / "archive" / f"manual-{stamp}-{i}"
        i += 1
    dest = base / "frontend"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(front), str(dest))
    front.mkdir(parents=True, exist_ok=True)
    return str(dest.relative_to(root))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--days", type=float, default=7.0)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--reset-frontend", action="store_true",
                    help="归档 .gate/frontend 后重建空目录（不删除证据）")
    ap.add_argument("--gate-archive-keep", type=int, default=0,
                    help="保留最近 N 个任务归档；0=不按数量清理")
    ap.add_argument("--gate-archive-days", type=float, default=0.0,
                    help="清理早于 N 天的任务归档；0=不按天数清理")
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    seen: set[Path] = set()
    plan = []
    for kind, path in iter_targets(root, args.days, args.reset_frontend,
                                   args.gate_archive_keep, args.gate_archive_days):
        if path in seen:
            continue
        seen.add(path)
        plan.append((kind, path))

    archive = root / ".gate" / "archive"
    if archive.is_dir():
        dirs = [d for d in archive.iterdir() if d.is_dir()]
        size = sum(f.stat().st_size for d in dirs for f in d.rglob("*") if f.is_file())
        print(f"[gate-archive] tasks={len(dirs)} size={size / 1024 / 1024:.1f}MB "
              f"keep={args.gate_archive_keep} days={args.gate_archive_days}")

    total = 0
    for kind, path in plan:
        if path.is_dir():
            size = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
            n = sum(1 for f in path.rglob("*") if f.is_file())
        else:
            size = path.stat().st_size if path.exists() else 0
            n = 1
        total += size
        suffix = " 将归档后重建" if kind == "frontend" else ""
        print(f"[{kind}] {path.relative_to(root)}  files={n}  {size / 1024:.1f}KB{suffix}")

    print(f"SUMMARY targets={len(plan)} size={total / 1024:.1f}KB mode={'apply' if args.apply else 'dry-run'}")
    if not args.apply:
        print("未删除任何文件；确认后加 --apply。")
        return 0
    for kind, path in plan:
        try:
            if kind == "frontend":
                dest = archive_frontend(root)
                print(f"ARCHIVED {path.relative_to(root)} -> {dest}")
            elif path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
        except OSError as exc:
            print(f"SKIP {path}: {exc}")
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
