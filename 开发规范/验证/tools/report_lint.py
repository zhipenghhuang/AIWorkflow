#!/usr/bin/env python3
"""Lint a dev task report against .gate/开发规范/completion.json.

Checks:
- report contains 【验证回执】 with verdict=... gate=...
- verdict matches completion.json; gate matches gate_id; task (if present) matches
- verdict != COMPLETE: positive completion words are rejected, but 未完成/未通过/未修复/不正常 are allowed
- verdict == COMPLETE: receipt includes checks= and unverified=; numbers match completion when available
- scans the whole report, not only the 汇报 line
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

POSITIVE = re.compile(r"(完成|通过|已修复|正常|全部通过|已解决)")
NEG_PREFIX = "未不无非"


def positive_words(line: str) -> list[str]:
    out = []
    for m in POSITIVE.finditer(line):
        i = m.start()
        if i > 0 and line[i - 1] in NEG_PREFIX:
            continue
        out.append(m.group(0))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    ap.add_argument("--completion", default=".gate/开发规范/completion.json")
    args = ap.parse_args()

    report = Path(args.report)
    completion = Path(args.completion)
    if not report.is_file():
        print(f"REPORT_NOT_FOUND: {report}")
        return 2
    if not completion.is_file():
        print(f"COMPLETION_NOT_FOUND: {completion} (先运行 Invoke-Gate.ps1)")
        return 1

    text = report.read_text(encoding="utf-8-sig", errors="replace")
    try:
        data = json.loads(completion.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        print(f"COMPLETION_INVALID: {exc}")
        return 1

    errors: list[str] = []
    if data.get("package") != "开发规范":
        errors.append(f"completion.json 属于 {data.get('package')}，不是开发规范；请重跑开发门")
    verdict = str(data.get("verdict", "UNKNOWN"))
    gate_id = str(data.get("gate_id") or data.get("commit") or "unknown")
    task_id = str(data.get("task_id") or "")

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
        if task_id and "task=" in receipt and task_id not in receipt:
            errors.append(f"回执 task= 与 completion.json 不一致（应为 {task_id}）")
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
            if line.strip().startswith("【验证回执】"):
                continue
            # 固定骨架标签本身含“完成”，不是结论措辞。
            scan_line = line.replace("完成了什么", "").replace("完成情况", "")
            words = positive_words(scan_line)
            if words:
                errors.append(f"verdict={verdict} 但正文出现完成类措辞：{line.strip()[:120]}")
                break

    # 数值对账：只做可解析的 checks=通过/总数、unverified=数量
    if "checks=" in receipt:
        mm = re.search(r"checks=(\d+)\s*/\s*(\d+)", receipt)
        if mm:
            passed, total = int(mm.group(1)), int(mm.group(2))
            checks = data.get("checks") or []
            if total != len(checks):
                errors.append(f"回执 checks 总数={total} 与 completion.checks={len(checks)} 不一致")
            actual_pass = sum(1 for c in checks if isinstance(c, dict) and c.get("status") == "pass")
            if passed != actual_pass:
                errors.append(f"回执 checks 通过={passed} 与 completion 通过={actual_pass} 不一致")

    if errors:
        for e in errors:
            print(f"REPORT_LINT_FAIL: {e}")
        return 1
    print(f"REPORT_LINT_OK: verdict={verdict}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
