#!/usr/bin/env python3
# 同源脚本：产品/开发/测试三包一致；改一处需同步。
"""Check a 收尾/报告 file for the mandatory 遵守自检 block.

Usage: python check_compliance.py --report <file>

Exit 0 = pass; 1 = missing/invalid. No LLM calls, no token cost.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

MODES = {"execute", "analyze", "stop"}

# 头块标记：任一单行不得叠放两个及以上（收尾标题互斥算一类）
_HEADER_MARKERS = (
    "【任务收尾】",
    "【执行收尾】",
    "【生成收尾】",
    "【验证回执】",
    "【开发自验】",
    "【遵守自检】",
)
_TITLE_MARKERS = ("【任务收尾】", "【执行收尾】", "【生成收尾】")
_REPORT_LEAD = re.compile(
    r"汇报[：:][ \t]*(?:\n+[ \t]*(?:```[^\n]*\n)?)?[ \t]*\*\*[^*]+\*\*[ \t]*[（(]"
)


def _check_header_lines(text: str, errors: list[str]) -> None:
    for line in text.splitlines():
        hits = [m for m in _HEADER_MARKERS if m in line]
        if not hits:
            continue
        titles = [h for h in hits if h in _TITLE_MARKERS]
        others = [h for h in hits if h not in _TITLE_MARKERS]
        if len(titles) > 1 or (titles and others) or len(others) > 1:
            errors.append(
                "标题/【验证回执】/【遵守自检】（及【开发自验】）须各占一行，禁粘行"
            )
            return


def _check_report_lead(text: str, errors: list[str], warnings: list[str]) -> None:
    if not re.search(r"【(?:任务|执行|生成)收尾】", text):
        return
    if not re.search(r"汇报[：:]", text):
        warnings.append("完整收尾建议含「汇报：」+ 结论说明体导语")
        return
    if not _REPORT_LEAD.search(text):
        errors.append("汇报须以 **短名**（结论态…）导语起笔（可紧随汇报：换行或 text 围栏内）")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    args = ap.parse_args()
    path = Path(args.report)
    if not path.is_file():
        print(f"REPORT_MISSING: {path}")
        return 1
    text = path.read_text(encoding="utf-8", errors="replace")
    errors: list[str] = []
    warnings: list[str] = []

    if "【验证回执】" not in text:
        errors.append("缺少【验证回执】")
    m = re.search(r"【遵守自检】([^\n]+)", text)
    if not m:
        errors.append("缺少【遵守自检】")
    else:
        body = m.group(1)
        for key in ("route=", "mode=", "reads="):
            if key not in body:
                errors.append(f"【遵守自检】缺少 {key}")
        mm = re.search(r"mode=([a-z]+)", body)
        if mm and mm.group(1) not in MODES:
            errors.append(f"mode={mm.group(1)} 不在 execute/analyze/stop")
        for key in ("gates=", "sync=", "skip=", "deviation="):
            if key not in body:
                warnings.append(f"【遵守自检】建议补 {key}")

    _check_header_lines(text, errors)
    _check_report_lead(text, errors, warnings)

    if re.search(r"【(?:任务|执行|生成)收尾】", text) and "运行态：" not in text:
        warnings.append("完整收尾建议含「运行态：」行（本轮进程/工具去向）")

    for e in errors:
        print(f"ERROR_COMPLIANCE: {e}")
    for w in warnings:
        print(f"WARN_COMPLIANCE: {w}")
    if errors:
        print(f"COMPLIANCE_FAILED: {len(errors)} error(s)")
        return 1
    print(f"COMPLIANCE_OK ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
