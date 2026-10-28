#!/usr/bin/env python3
"""Lint a dev task report against .gate/开发规范/completion.json.

Checks:
- report contains 【验证回执】 with a Chinese conclusion (通过/部分通过/阻塞/未验证)
  or legacy verdict=...
- report contains a 待你确认 section (无待确认写「待你确认：无」)
- conclusion maps to completion.json verdict; gate matches gate_id; task (if present) matches
- verdict != COMPLETE: positive completion words are rejected, but scoped phrases
  (部分完成/阶段完成/文档阶段完成/部分验证/有条件通过) and negatives are allowed
- verdict == COMPLETE: receipt includes checks= and unverified=
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

POSITIVE = re.compile(r"(已完成|全部完成|整体完成|已通过|全部通过|已修复|已解决|正常(?=[。；，!?]|$)|完成(?=[。；，!?]|$)|通过(?=[。；，!?]|$))")
NEG_PREFIX = "未不无非"
SCOPED_OK = re.compile(r"(部分完成|阶段完成|文档阶段完成|部分验证|有条件通过)")
VERDICT_MAP = {
    "通过": "COMPLETE",
    "部分通过": "PARTIAL",
    "阻塞": "BLOCKED",
    "未验证": "NOT_VERIFIED",
}


def positive_words(line: str) -> list[str]:
    line = SCOPED_OK.sub("", line)
    out = []
    for m in POSITIVE.finditer(line):
        i = m.start()
        if i > 0 and line[i - 1] in NEG_PREFIX:
            continue
        out.append(m.group(0))
    return out


def receipt_value(receipt: str, cn_key: str, en_key: str) -> str:
    m = re.search(rf"{cn_key}=([^|]+)", receipt)
    if m:
        return m.group(1).strip()
    m = re.search(rf"{en_key}=([^|]+)", receipt)
    return m.group(1).strip() if m else ""


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
        conclusion = receipt_value(receipt, "结论", "verdict")
        mapped = VERDICT_MAP.get(conclusion, conclusion)
        if not mapped:
            errors.append("回执缺少结论=通过/部分通过/阻塞/未验证")
        elif mapped != verdict:
            errors.append(f"回执结论={conclusion} 与 completion.json verdict={verdict} 不一致")
        if not (("校验=" in receipt) or ("gate=" in receipt)):
            errors.append("回执缺少 校验= 或 gate= 标识")
        elif gate_id != "unknown" and gate_id not in receipt:
            errors.append(f"回执校验= 与 completion.json 不一致（应为 {gate_id}）")
        if task_id and "task=" in receipt and task_id not in receipt:
            errors.append(f"回执 task= 与 completion.json 不一致（应为 {task_id}）")
        if verdict == "COMPLETE":
            if not (("检查=" in receipt) or ("checks=" in receipt)):
                errors.append("通过回执缺少 检查= 或 checks=")
            if not (("未验证=" in receipt) or ("unverified=" in receipt)):
                errors.append("通过回执缺少 未验证= 或 unverified=")
        else:
            if not (("未验证=" in receipt) or ("unverified=" in receipt) or ("blocked=" in receipt)):
                errors.append("非通过回执缺少 未验证=/unverified=/blocked=")

    if "【任务收尾】" in text and not re.search(r"待你确认（需拍板|：无", text):
        errors.append("缺少第 4 点待你确认表；无待确认写「待你确认：无」")

    if "【任务收尾】" in text:
        sc = re.search(r"【遵守自检】(.+)", text)
        if not sc:
            errors.append("缺少【遵守自检】行（route/mode/reads/gates/sync/skip/deviation）")
        else:
            body = sc.group(1)
            for key in ("route=", "mode=", "reads="):
                if key not in body:
                    errors.append(f"【遵守自检】缺少 {key}")

    if verdict != "COMPLETE":
        for line in text.splitlines():
            if line.strip().startswith("【验证回执】"):
                continue
            if "完成标志" in line:
                continue
            # 固定骨架标签本身含“完成”，不是结论措辞。
            scan_line = line.replace("完成了什么", "").replace("完成情况", "").replace("完成标志", "")
            words = positive_words(scan_line)
            if words:
                errors.append(f"verdict={verdict} 但正文出现完成类措辞：{line.strip()[:120]}")
                break

    # 数值对账：只做可解析的 检查=/checks=通过/总数
    checks_text = receipt_value(receipt, "检查", "checks") if receipt else ""
    mm = re.search(r"(\d+)\s*/\s*(\d+)", checks_text)
    if mm:
        passed, total = int(mm.group(1)), int(mm.group(2))
        checks = data.get("checks") or []
        if total != len(checks):
            errors.append(f"回执检查总数={total} 与 completion.checks={len(checks)} 不一致")
        actual_pass = sum(1 for c in checks if isinstance(c, dict) and c.get("status") == "pass")
        if passed != actual_pass:
            errors.append(f"回执检查通过={passed} 与 completion 通过={actual_pass} 不一致")

    if errors:
        for e in errors:
            print(f"REPORT_LINT_FAIL: {e}")
        return 1
    print(f"REPORT_LINT_OK: verdict={verdict}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
