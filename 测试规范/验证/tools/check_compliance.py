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

    if re.search(r"【(?:任务|执行|生成)收尾】", text) and "运行态：" not in text:
        warnings.append("完整收尾建议含「运行态：」行（本轮进程/浏览器去向）")

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
