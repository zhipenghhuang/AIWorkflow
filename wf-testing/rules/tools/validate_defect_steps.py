#!/usr/bin/env python3
"""Validate defect-channel steps before platform create/PUT.

Usage:
  python validate_defect_steps.py <steps.html|steps.txt|->
  (- = stdin)

Checks (defect 十段 only; 盯办八块 → exit 0 with SKIP):
- ten block headers present
- 问题标题 / 一句话影响 / 最小复现
- 环境URL=
- 设计对照: 原文： or 无设计文档；且 设计应然 / 现网 / 差别
- surface= / 入口指纹=
- ban evidence/|docs/ path leak; HTML: no <br>\\n, no </p><p>

Exit 0 = pass (or SKIP watch); 1 = errors; 2 = usage.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BLOCKS = (
    "【提交摘要】",
    "【环境】",
    "【测试数据/业务主键】",
    "【问题】",
    "【复现】",
    "【实际】",
    "【预期】",
    "【接口判定】",
    "【设计对照】",
    "【技术附记】",
)

WATCH_MARK = re.compile(r"通道\s*[：:=].*盯办|平台盯办|【卡点】|【已尝试】|【请求】")


def load(arg: str) -> str:
    if arg == "-":
        return sys.stdin.read()
    p = Path(arg)
    if not p.is_file():
        raise FileNotFoundError(str(p))
    return p.read_text(encoding="utf-8")


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", " ", s)


def validate(text: str) -> list[str]:
    errs: list[str] = []
    if WATCH_MARK.search(text):
        return []  # caller prints SKIP

    for b in BLOCKS:
        if b not in text:
            errs.append(f"missing_block:{b}")

    for k in ("问题标题", "一句话影响", "最小复现"):
        if not re.search(rf"{k}\s*[：:]", text):
            errs.append(f"missing_field:{k}")

    if not re.search(r"环境URL\s*=", text):
        errs.append("missing_field:环境URL=")

    has_yuanwen = bool(re.search(r"原文\s*[：:]", text))
    has_no_doc = "无设计文档" in text
    if not (has_yuanwen or has_no_doc):
        errs.append("design:need_原文_or_无设计文档")
    for k in ("设计应然", "差别"):
        if not re.search(rf"{k}\s*[：:]", text):
            errs.append(f"design:missing:{k}")
    if not re.search(r"现网", text):
        errs.append("design:missing:现网")

    if not re.search(r"surface\s*=", text, re.I):
        errs.append("missing_field:surface=")
    if not re.search(r"入口指纹\s*=", text):
        errs.append("missing_field:入口指纹=")

    if re.search(r"evidence/[A-Za-z0-9_\-./]+", text) or re.search(
        r"(?<![A-Za-z])docs/[A-Za-z0-9_\-./]+", text
    ):
        errs.append("path_leak:evidence_or_docs")

    if "<" in text:
        if re.search(r"<br\s*/?>\s*\n", text, re.I):
            errs.append("html:br_followed_by_newline")
        if re.search(r"</p>\s*<p>", text, re.I) and not re.search(r"</p>\n<p>", text, re.I):
            errs.append("html:paragraphs_glued")
        if re.search(r"</p>\n\n+<p>", text, re.I):
            errs.append("html:double_newline_between_blocks")

    plain = strip_tags(text)
    # thin实际/预期: require digit or key=value style signal in those blocks
    for name in ("实际", "预期"):
        m = re.search(
            rf"【{name}】(.*?)(?=【|\Z)",
            plain,
            re.S,
        )
        chunk = (m.group(1) if m else "").strip()
        if len(chunk) < 12:
            errs.append(f"thin:【{name}】")
        elif not re.search(r"(\d|[=＝]|字段|code|status|message)", chunk, re.I):
            errs.append(f"thin_signal:【{name}】")

    return errs


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python validate_defect_steps.py <steps.html|txt|->", file=sys.stderr)
        return 2
    try:
        text = load(sys.argv[1])
    except FileNotFoundError as e:
        print(f"ERROR: file not found {e}", file=sys.stderr)
        return 2

    if WATCH_MARK.search(text) and "【提交摘要】" in text and "【卡点】" in text:
        print("SKIP: watch/盯办 channel (not 十段 gate)")
        return 0

    errs = validate(text)
    if not errs:
        print("OK: defect steps structure+thickness markers")
        return 0
    for e in errs:
        print(f"ERROR: {e}")
    print(f"TOTAL_ERRORS: {len(errs)}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
