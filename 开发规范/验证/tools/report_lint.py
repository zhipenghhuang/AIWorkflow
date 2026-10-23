#!/usr/bin/env python3
"""Lint a dev task report against .gate/completion.json.

Usage: python report_lint.py --report <report.md> [--completion <completion.json>]

Checks:
- report contains 【验证回执】 with verdict=... gate=...
- verdict matches completion.json
- verdict != COMPLETE: no 完成/通过/已修复/正常 in the 汇报/完成了什么 lines
- verdict == COMPLETE: receipt includes checks= and unverified=
Exit: 0 pass, 1 fail, 2 usage.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

FORBIDDEN = ("完成", "通过", "已修复", "正常", "全部通过", "已解决")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    ap.add_argument("--completion", default=".gate/completion.json")
    args = ap.parse_args()

    report = Path(args.report)
    completion = Path(args.completion)
    if not report.is_file():
        print(f"REPORT_NOT_FOUND: {report}")
        return 2
    if not completion.is_file():
        print(f"COMPLETION_NOT_FOUND: {completion} (先运行 Invoke-Gate.ps1)")
        return 1

    text = report.read_text(encoding="utf-8", errors="replace")
    data = json.loads(completion.read_text(encoding="utf-8"))
    errors: list[str] = []
    if data.get("package") != "开发规范":
        errors.append(f"completion.json 属于 {data.get('package')}，不是开发规范；请重跑开发门")
    verdict = str(data.get("verdict", "UNKNOWN"))
    gate_id = str(data.get("gate_id") or data.get("commit") or "unknown")

    m = re.search(r"【验证回执】(.+)", text)
    if not m:
        errors.append("缺少【验证回执】行")
        receipt = ""
    else:
        receipt = m.group(1)
        if f"verdict={verdict}" not in receipt:
            errors.append(f"回执 verdict 与 completion.json 不一致（report={receipt[:80]}...）")
        if "gate=" not in receipt:
            errors.append("回执缺少 gate= 标识")
        elif gate_id != "unknown" and gate_id not in receipt:
            errors.append(f"回执 gate= 与 completion.json 不一致（应为 {gate_id}）")
        if verdict == "COMPLETE":
            if "checks=" not in receipt:
                errors.append("COMPLETE 回执缺少 checks=")
            if "unverified=" not in receipt:
                errors.append("COMPLETE 回执缺少 unverified=")
        else:
            if "unverified=" not in receipt and "blocked=" not in receipt:
                errors.append("非 COMPLETE 回执缺少 unverified=/blocked=")

    if verdict != "COMPLETE":
        for line in text.splitlines():
            if ("汇报" in line or "完成了什么" in line) and any(w in line for w in FORBIDDEN):
                errors.append(f"verdict={verdict} 但汇报行出现完成类措辞：{line.strip()[:120]}")
                break

    if errors:
        for e in errors:
            print(f"REPORT_LINT_FAIL: {e}")
        return 1
    print(f"REPORT_LINT_OK: verdict={verdict}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
