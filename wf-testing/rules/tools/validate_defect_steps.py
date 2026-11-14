#!/usr/bin/env python3
"""Validate defect-channel steps before platform create/PUT.

Usage:
  python validate_defect_steps.py <steps.html|steps.txt|->
  (- = stdin)

Checks (defect 十段 only; 盯办八块 → exit 0 with SKIP):
- ten blocks present, ordered, unique, non-empty
- 摘要四行 / 环境三行 / 构造+全码 / 复现≥3步 / 实际·预期各≥2条
- 设计对照: 原文或「无设计文档」+ 设计应然/现网/差别/方案理解核对
- 技术附记: route/落点/surface/入口指纹/依据/判定
- 标题去前缀后 ≤56 字; surface= / 入口指纹=
- ban evidence/|docs/ path leak; HTML: 10×<p>, tag pairs, no <br>\n, no </p><p>

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

# 块内最少有效字符（去标签/去块名后）；防「有块无内容」
MIN_CHARS = {
    "【提交摘要】": 60,
    "【环境】": 20,
    "【测试数据/业务主键】": 10,
    "【问题】": 20,
    "【复现】": 30,
    "【实际】": 15,
    "【预期】": 15,
    "【接口判定】": 4,
    "【设计对照】": 20,
    "【技术附记】": 10,
}

WATCH_MARK = re.compile(r"通道\s*[：:=].*盯办|平台盯办|【卡点】|【已尝试】|【请求】")
NUM_STEP = re.compile(r"^\s*(?:\d+[.、)]|[-*]\s*\d+[.、)])\s*\S", re.M)
TITLE_PREFIX = re.compile(r"^\s*(?:\[[^\]]*\]\s*)+")


def load(arg: str) -> str:
    if arg == "-":
        return sys.stdin.read()
    p = Path(arg)
    if not p.is_file():
        raise FileNotFoundError(str(p))
    return p.read_text(encoding="utf-8")


def strip_tags(s: str) -> str:
    """HTML→可统计文本：<br> 保留行意，</p> 保留块间空行，其余标签变空格。"""
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</p\s*>", "\n\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    return s


def slices(plain: str) -> tuple[dict[str, str], list[str]]:
    """Return block→content and structural errors (missing/dup/order)."""
    errs: list[str] = []
    pos = []
    for b in BLOCKS:
        idx = [m.start() for m in re.finditer(re.escape(b), plain)]
        if not idx:
            errs.append(f"missing_block:{b}")
            pos.append(None)
            continue
        if len(idx) > 1:
            errs.append(f"duplicate_block:{b}")
        pos.append(idx[0])
    present = [(i, p) for i, p in enumerate(pos) if p is not None]
    for (i1, p1), (i2, p2) in zip(present, present[1:]):
        if p2 < p1:
            errs.append(f"block_order:{BLOCKS[i2]}_before_{BLOCKS[i1]}")
    out: dict[str, str] = {}
    for i, b in enumerate(BLOCKS):
        start = pos[i]
        if start is None:
            continue
        start += len(b)
        ends = [p for p in pos if p is not None and p > start]
        end = min(ends) if ends else len(plain)
        out[b] = plain[start:end]
    return out, errs


def field(text: str, name: str) -> str:
    m = re.search(rf"{re.escape(name)}\s*[：:=]\s*(.+)", text)
    return m.group(1).strip() if m else ""


def count_lines(text: str) -> int:
    return len(NUM_STEP.findall(text))


def validate(text: str) -> list[str]:
    errs: list[str] = []
    if WATCH_MARK.search(text):
        return []  # caller prints SKIP

    html = "<" in text and re.search(r"<p\b", text, re.I)
    plain = strip_tags(text) if html else text

    blocks, struct_errs = slices(plain)
    errs.extend(struct_errs)

    for b, content in blocks.items():
        body = content.strip()
        if len(body) < MIN_CHARS.get(b, 8):
            errs.append(f"thin_block:{b}({len(body)}<{MIN_CHARS.get(b, 8)})")

    abstract = blocks.get("【提交摘要】", "")
    for k in ("执行结果", "缺陷类型", "问题标题", "严重程度", "优先级"):
        if not re.search(rf"{k}\s*[：:]", abstract):
            errs.append(f"missing_field:{k}")
    if not re.search(r"一句话影响\s*[：:]", abstract):
        errs.append("missing_field:一句话影响")
    if not re.search(r"最小复现\s*[：:]", abstract):
        errs.append("missing_field:最小复现")

    title = field(abstract, "问题标题").split("<br")[0].strip()
    title = TITLE_PREFIX.sub("", title).strip()
    if title and len(title) > 56:
        errs.append(f"title_too_long:{len(title)}>56")

    env = blocks.get("【环境】", "")
    if not re.search(r"环境URL\s*=", env):
        errs.append("missing_field:环境URL=")
    if not re.search(r"账号角色\s*[：:=]", env):
        errs.append("missing_field:账号角色")
    if not re.search(r"版本|构建|见\s*§0|见记录", env):
        errs.append("missing_field:版本·构建")

    data = blocks.get("【测试数据/业务主键】", "")
    if not re.search(r"构造|列名\s*=|全码|业务码", data):
        errs.append("data:need_构造_or_全码")

    repro = blocks.get("【复现】", "")
    if count_lines(repro) < 3:
        errs.append(f"repro:steps<3({count_lines(repro)})")
    if not re.search(r"前置|复现频率|每次|间歇", repro):
        errs.append("repro:need_前置_or_频率")

    for name in ("【实际】", "【预期】"):
        n = count_lines(blocks.get(name, ""))
        if n < 2:
            errs.append(f"{name}:items<2({n})")

    api = blocks.get("【接口判定】", "")
    if len(api.strip()) < 4:
        errs.append("empty:【接口判定】（无接口也写「本轮无相关接口」）")

    design = blocks.get("【设计对照】", "")
    has_yuanwen = bool(re.search(r"原文\s*[：:]", design))
    has_no_doc = "无设计文档" in design
    if not (has_yuanwen or has_no_doc):
        errs.append("design:need_原文_or_无设计文档")
    for k in ("设计应然", "差别", "方案理解核对"):
        if not re.search(rf"{k}\s*[：:]", design):
            errs.append(f"design:missing:{k}")
    if "现网" not in design and "本轮" not in design:
        errs.append("design:missing:现网/本轮")

    tech = blocks.get("【技术附记】", "")
    for k in ("route", "落点", "surface", "入口指纹", "依据", "判定"):
        if not re.search(rf"{k}\s*[=:：]", tech):
            errs.append(f"tech:missing:{k}=")

    if not re.search(r"surface\s*=", text, re.I):
        errs.append("missing_field:surface=")
    if not re.search(r"入口指纹\s*=", text):
        errs.append("missing_field:入口指纹=")

    surface = ""
    ms = re.search(r"surface\s*=\s*(ui\+api|ui|api)\b", text, re.I)
    if ms:
        surface = ms.group(1).lower()
    if surface in ("ui", "ui+api"):
        if not re.search(r"菜单|页面|列表|详情|表单|按钮|点击|输入|选择|勾选|打开|「|」|Tab|区域|弹窗|提示", repro):
            errs.append("repro:ui_need_ui_steps")
        if re.search(r"\b(?:GET|POST|PUT|PATCH|DELETE)\s+/", repro, re.I):
            errs.append("repro:ui_should_not_be_api_chain")
    if surface == "ui+api":
        if not re.search(r"\b(?:GET|POST|PUT|PATCH|DELETE)\s+/", api, re.I):
            errs.append("api:ui_plus_api_need_method_path")
        if "本轮无相关接口" in api:
            errs.append("api:ui_plus_api_cannot_be_no_api")
    if surface == "api":
        if not re.search(r"无\s*UI|无菜单|无页面|仅接口|纯接口|无可见控件|纯\s*API|仅\s*API", text, re.I):
            errs.append("api:need_no_ui_evidence")
        if not re.search(r"\b(?:GET|POST|PUT|PATCH|DELETE)\s+/", repro, re.I):
            errs.append("repro:api_need_request_chain")

    if re.search(r"evidence/[A-Za-z0-9_\-./]+", text) or re.search(
        r"(?<![A-Za-z])docs/[A-Za-z0-9_\-./]+", text
    ):
        errs.append("path_leak:evidence_or_docs")

    if html:
        opens = len(re.findall(r"<p\b[^>]*>", text, re.I))
        closes = len(re.findall(r"</p\s*>", text, re.I))
        if opens != len(BLOCKS):
            errs.append(f"html:p_count={opens}≠{len(BLOCKS)}")
        if closes != opens:
            errs.append(f"html:p_unclosed({closes}/{opens})")
        b_open = len(re.findall(r"<b\b[^>]*>", text, re.I))
        b_close = len(re.findall(r"</b\s*>", text, re.I))
        if b_open != b_close:
            errs.append(f"html:b_unclosed({b_close}/{b_open})")
        if re.search(r"<br\s*/?>\s*<br\s*/?>", text, re.I):
            errs.append("html:double_br")
        if re.search(r"</p>\s*<p>", text, re.I) and not re.search(r"</p>\n<p>", text, re.I):
            errs.append("html:paragraphs_glued")
        if re.search(r"</p>\n\n+<p>", text, re.I):
            errs.append("html:double_newline_between_blocks")
        if re.search(r"<p>\s*</p>", text, re.I):
            errs.append("html:empty_paragraph")

    for name in ("【实际】", "【预期】"):
        chunk = blocks.get(name, "").strip()
        if len(chunk) >= 12 and not re.search(
            r"(\d|[=＝]|字段|code|status|message|原文|「|」|错误|提示)", chunk, re.I
        ):
            errs.append(f"thin_signal:{name}")

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
        blocks, _ = slices(strip_tags(text) if "<p" in text else text)
        sizes = " ".join(f"{k.strip('【】')}={len(v.strip())}" for k, v in blocks.items())
        print(f"OK: defect steps structure+thickness ({sizes})")
        return 0
    for e in errs:
        print(f"ERROR: {e}")
    print(f"TOTAL_ERRORS: {len(errs)}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
