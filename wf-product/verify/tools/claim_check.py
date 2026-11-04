#!/usr/bin/env python3
"""Claim lock: 没有本轮门禁回执，不允许任何“完成/通过/准出”表述。

背景：门禁回执（completion.json）会写 BLOCKED，但模型仍可能在对话/文档里写
“已完成/已通过”。本脚本把“能不能这么写”变成一个可执行、可粘贴的一行结论。

Usage:
  python claim_check.py --project-root . [--receipt .gate/wf-development/completion.json]
                        [--max-age-hours 24] [--json]

输出：
  CLAIM: ALLOWED <verdict> <gate_id>
  CLAIM: DENIED - <原因1>; <原因2>

规则：
  1. verdict 必须是 COMPLETE / READY / PASS（测试轨 PASS，产品轨 READY）。
  2. receipt.blocked 必须为空，checks 里不得有 fail/blocked。
  3. 代码文件（排除 docs/.gate/inbound/规范包/var）在回执生成后不得再改动。
  4. 回执必须晚于 task_started_at（本轮任务）。
退出码 0=ALLOWED，1=DENIED，2=用法/环境错误。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ALLOWED_VERDICTS = {"COMPLETE", "READY", "PASS", "PASSED", "通过"}
BAD_CHECK_STATUS = {"fail", "failed", "blocked", "error"}
SKIP_DIR_PREFIXES = (
    ".gate/", "docs/", "inbound/", "var/", "node_modules/", ".git/",
    "wf-product/", "wf-development/", "wf-testing/", "wf/",
)
SKIP_SUFFIXES = (".md", ".txt", ".log", ".png", ".jpg", ".jpeg", ".webp", ".pyc")
EMPTY_TREE = {"", "HEAD"}


def run_git(root: Path, *args: str) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30,
        )
    except Exception:
        return ""
    return out.stdout if out.returncode == 0 else ""


def changed_paths(root: Path) -> list[str]:
    """Return working-tree changed/untracked paths (NUL-safe)."""
    raw = run_git(root, "status", "--porcelain", "-z", "--untracked-files=all")
    if not raw:
        return []
    parts = raw.split("\x00")
    paths: list[str] = []
    index = 0
    while index < len(parts):
        entry = parts[index]
        index += 1
        if len(entry) < 4:
            continue
        code, path = entry[:2], entry[3:]
        if code.startswith("R") or code.startswith("C"):
            index += 1  # skip the original path of a rename/copy
        if path:
            paths.append(path)
    return paths


def is_code_file(path: str) -> bool:
    normalized = path.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    if not normalized:
        return False
    if any(normalized.startswith(prefix) for prefix in SKIP_DIR_PREFIXES):
        return False
    if normalized.lower().endswith(SKIP_SUFFIXES):
        return False
    return True


def parse_iso(value: str) -> datetime | None:
    text = (value or "").strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except Exception:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(description="Claim lock for workflow completion gate")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--receipt", default=".gate/wf-product/completion.json")
    parser.add_argument("--mode", default="prd", help="产品轨结论对应门：prd/review/design-review/uat/change/writeback")
    parser.add_argument("--max-age-hours", type=float, default=0.0,
                        help="0 = 不按回执年龄限制（默认）；>0 时超过该小时的旧回执直接 DENIED")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    receipt_path = Path(args.receipt)
    if not receipt_path.is_absolute():
        receipt_path = root / receipt_path
    problems: list[str] = []

    if not receipt_path.is_file():
        problems.append(f"缺少门禁回执 {args.receipt}（先运行 verify/Invoke-Gate.ps1）")
        return report(problems, {}, args.json)

    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        problems.append(f"回执不可解析: {exc}")
        return report(problems, {}, args.json)

    receipt_mode = str(receipt.get("mode") or "").strip()
    if args.mode and receipt_mode and args.mode != receipt_mode:
        problems.append(f"回执 mode={receipt_mode} 与本次声明 mode={args.mode} 不一致")

    verdict = str(receipt.get("verdict") or receipt.get("result") or "").strip().upper()
    if verdict not in ALLOWED_VERDICTS:
        problems.append(f"verdict={verdict or '空'}，只允许 {sorted(ALLOWED_VERDICTS)}")

    blocked = receipt.get("blocked") or []
    if isinstance(blocked, list) and blocked:
        problems.append(f"回执仍列 {len(blocked)} 项阻断: {blocked[0]}")

    checks = receipt.get("checks") or []
    bad_checks = [c for c in checks if isinstance(c, dict) and str(c.get("status", "")).lower() in BAD_CHECK_STATUS]
    if bad_checks:
        problems.append("检查未过: " + ", ".join(f"{c.get('id')}={c.get('status')}" for c in bad_checks[:4]))

    stamp = parse_iso(str(receipt.get("timestamp") or receipt.get("generated_at") or ""))
    if stamp is None:
        problems.append("回执缺少可解析 timestamp")
    else:
        started = parse_iso(str(receipt.get("task_started_at") or ""))
        if started and stamp < started:
            problems.append(f"回执 timestamp({stamp.isoformat()}) 早于 task_started_at({started.isoformat()})")
        if args.max_age_hours > 0:
            age_hours = (datetime.now(timezone.utc) - stamp.astimezone(timezone.utc)).total_seconds() / 3600
            if age_hours > args.max_age_hours:
                problems.append(f"回执已过期 {age_hours:.1f}h > {args.max_age_hours}h")

        # 产物在回执后改动 => gate_id 的内容哈希对不上。
        artifact = str(receipt.get("artifact") or "").strip()
        gate_id = str(receipt.get("gate_id") or "")
        m = re.search(r"-([0-9a-f]{12})$", gate_id)
        if artifact and m:
            art_path = Path(artifact)
            if not art_path.is_absolute():
                art_path = root / art_path
            if not art_path.is_file():
                problems.append(f"回执产物不存在: {artifact}")
            else:
                raw = art_path.read_text(encoding="utf-8-sig", errors="replace")
                stable = re.sub(r"(?m)^\s*gate_id\s*:.*(?:\r?\n|$)", "", raw)
                stable = re.sub(r"(?m)^\s*\|[^\n]*gate_id[^\n]*\|\s*$", "", stable)
                digest = hashlib.sha256(stable.encode("utf-8", errors="replace")).hexdigest()[:12]
                if digest != m.group(1):
                    problems.append(f"回执后产物已改动: {artifact}（重新跑门禁）")

    # Freshness: 代码在回执之后被改动 => 回执不再代表当前工作区。
    if stamp is not None:
        stale: list[str] = []
        for rel in changed_paths(root):
            if not is_code_file(rel):
                continue
            full = root / rel
            if not full.is_file():
                continue
            mtime = datetime.fromtimestamp(full.stat().st_mtime, tz=stamp.astimezone().tzinfo)
            if mtime > stamp:
                stale.append(f"{rel} ({mtime.strftime('%m-%d %H:%M')})")
        if stale:
            problems.append(
                f"{len(stale)} 个代码文件在门禁后改动，回执已过期: {', '.join(stale[:3])}"
                "（重新跑门禁）"
            )

    return report(problems, receipt, args.json)


def report(problems: list[str], receipt: dict, as_json: bool) -> int:
    verdict = str(receipt.get("verdict") or receipt.get("result") or "").strip() or "-"
    gate_id = str(receipt.get("gate_id") or "").strip() or "-"
    if as_json:
        print(json.dumps({"ok": not problems, "verdict": verdict, "gate_id": gate_id,
                          "problems": problems}, ensure_ascii=False, indent=2))
    elif problems:
        print("CLAIM: DENIED - " + "; ".join(problems))
        if receipt:
            print(f"  (receipt verdict={verdict} gate_id={gate_id})")
        print("  只能表述：未完成 / 阻塞 / 部分完成（并给原因）；不得写完成、通过、可提测、已修复。")
    else:
        mode = str(receipt.get("mode") or "-")
        print(f"CLAIM: ALLOWED {verdict} {gate_id} mode={mode}")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
