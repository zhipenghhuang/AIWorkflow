#!/usr/bin/env python3
# 同源脚本：产品/开发/测试三包一致；改一处需同步。
"""Check a 收尾/报告 file for the mandatory 遵守自检 block and six-point layout.

Checks: title/receipt/self-check one per line; 汇报（可直接复制）block; 1～6
sections in order; point 2/4/6 fixed sub-fields; appendix 资料补强/工作记忆/运行态.
Pure reports without a 收尾 title only get receipt/self-check checks.

Usage: python check_compliance.py --report <file>

Exit 0 = pass; 1 = missing/invalid. No LLM calls, no token cost.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

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
_TITLE_RE = re.compile(r"【(?:任务|执行|生成)收尾】")
_REPORT_LABEL = re.compile(r"汇报(?:（可直接复制）)?[：:]")
_REPORT_LEAD = re.compile(
    r"汇报(?:（可直接复制）)?[：:][ \t]*(?:\n+[ \t]*(?:```[^\n]*\n)?)?[ \t]*\*\*[^*]+\*\*[ \t]*[（(]"
)
_SECTION_RE = re.compile(
    r"(?m)^\s*([1-6])\.\s*(完成了什么|改了哪些文件|如何验证|假设与未决项|还存在什么问题或风险|当前进度与下一步)"
)
_SECTION_LABELS = {
    1: ("影响：",),
    2: ("文件：", "未提交：", "建议动作：", "待提交摘要：", "git：", ".gitignore：", "文档归档："),
    4: ("假设：", "待你确认", "默认（不回复即执行）：", "回复：", "可转发产品："),
    6: ("当前：", "下一步：", "优先级：", "建议：", "不建议：", "完成标志："),
}
_DECISION_LABELS = ("事项：", "选项：", "建议：", "影响/默认：")
_APPENDIX_LABELS = ("资料补强：", "工作记忆：", "运行态：")


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
    if not _TITLE_RE.search(text):
        return
    if not _REPORT_LABEL.search(text):
        errors.append("完整收尾须有「汇报（可直接复制）：」块（不得并入第 1 点）")
        return
    if not _REPORT_LEAD.search(text):
        errors.append("汇报须以 **短名**（结论态…）导语起笔（可紧随汇报：换行或 text 围栏内）")
    start = _REPORT_LABEL.search(text)
    if start:
        end = text.find("1. 完成了什么", start.end())
        body = text[start.end(): end if end >= 0 else len(text)]
        if "`" in body:
            warnings.append("汇报块含行内反引号；汇报层禁路径/命令/标识，明细层可用")


def _check_sections(text: str, errors: list[str]) -> None:
    if not _TITLE_RE.search(text):
        return
    receipt_match = re.search(r"【验证回执】([^\n]+)", text)
    if receipt_match:
        receipt = receipt_match.group(1)
        for key in ("结论=", "校验=", "检查="):
            if key not in receipt:
                errors.append(f"【验证回执】缺少 {key}")
        if "未验证=" not in receipt and "待确认=" not in receipt:
            errors.append("【验证回执】缺少 未验证= 或 待确认=")
    matches = list(_SECTION_RE.finditer(text))
    nums = [int(m.group(1)) for m in matches]
    if nums != [1, 2, 3, 4, 5, 6]:
        errors.append("1～6 点须齐全、按顺序各起一行；当前=" + (",".join(map(str, nums)) or "无"))
        return
    pos = [m.start() for m in matches]
    sections: dict[int, str] = {}
    for index, match in enumerate(matches):
        end = pos[index + 1] if index + 1 < len(pos) else len(text)
        sections[int(match.group(1))] = text[match.start():end]

    for number, labels in _SECTION_LABELS.items():
        body = sections.get(number, "")
        for label in labels:
            if label not in body:
                errors.append(f"第 {number} 点缺少「{label}」")

    point4 = sections.get(4, "")
    if "待你确认" in point4 and "待你确认：无" not in point4:
        for label in _DECISION_LABELS:
            if label not in point4:
                errors.append(f"第 4 点决策项缺少「{label}」")

    point6 = sections.get(6, "")
    if "下一步：" in point6:
        if "1）" not in point6:
            errors.append("第 6 点下一步须至少 1 个动作（1）…）")
        for label in ("执行：", "产出："):
            if label not in point6:
                errors.append(f"第 6 点下一步缺少「{label}」")

    appendix_marker = "附：运行与沉淀"
    point6 = sections.get(6, "")
    if appendix_marker not in point6:
        errors.append("第 6 点后缺少「附：运行与沉淀」")
        appendix = ""
    else:
        point6, appendix = point6.split(appendix_marker, 1)
        sections[6] = point6
    for label in _APPENDIX_LABELS:
        if label not in appendix:
            errors.append(f"附录缺少「{label}」")


_EXEC_MODES = {"脚本", "直跑", "模块子代理", "拆分", "na", "无"}


def _is_testing_execute(body: str) -> bool:
    """True when receipt is for wf-testing execute step (economy fields required)."""
    packet = ""
    mp = re.search(r"packet=([^|]+)", body)
    if mp:
        packet = mp.group(1).strip()
    if "packets/testing/execute" in packet.replace("\\", "/"):
        return True
    route = ""
    mr = re.search(r"route=([^|]+)", body)
    if mr:
        route = mr.group(1).strip().lower()
    return bool(re.search(r"(?:^|[/:])testing(?:$|[/:])", route)) and bool(
        re.search(r"(?:^|[/:])execute(?:$|[/:])", route)
    )


def _check_self_check(text: str, errors: list[str], warnings: list[str]) -> None:
    m = re.search(r"【遵守自检】([^\n]+)", text)
    if not m:
        errors.append("缺少【遵守自检】")
        return
    body = m.group(1)
    for key in ("route=", "mode=", "packet=", "global=", "skills=", "reads=", "gates=", "confirm=", "sync=", "skip=", "deviation="):
        if key not in body:
            errors.append(f"【遵守自检】缺少 {key}")
    mp = re.search(r"packet=([^|]+)", body)
    if mp and "rules/packets/" not in mp.group(1) and mp.group(1).strip() not in ("na", "无"):
        errors.append("【遵守自检】packet= 须指向 rules/packets/...")
    mg = re.search(r"global=([^|]+)", body)
    if mg and mg.group(1).strip() not in ("ok",) and not mg.group(1).strip().startswith("dev:"):
        errors.append("global= 须为 ok 或 dev:<原因>")
    mm = re.search(r"mode=([a-z]+)", body)
    if mm and mm.group(1) not in MODES:
        errors.append(f"mode={mm.group(1)} 不在 execute/analyze/stop")
    sync_match = re.search(r"sync=([^|]+)", body)
    if sync_match:
        sync_body = sync_match.group(1).strip()
        # Soft: version/release/facade-ish sync without cold-layer marker → warn (doc-facade-sync §2.1)
        if (
            sync_body not in ("无", "na", "无门面变化")
            and "冷层" not in sync_body
            and re.search(r"版本|VERSION|bump|发布|上线|门面|部署", sync_body, re.I)
        ):
            warnings.append(
                "【遵守自检】sync= 含版本/发布/门面类表述时建议含 冷层:ok|na|deferred:<因>（见 doc-facade-sync）"
            )
        # Soft: SSOT bumped (ac=ok) but no cold-layer marker → incomplete facade sync
        if re.search(r"\bac=ok\b", sync_body) and "冷层" not in sync_body:
            warnings.append(
                "【遵守自检】sync= 含 ac=ok（产品版本 SSOT 已变）时须含 冷层:ok|na|deferred:<因>（禁空写；见 doc-facade-sync）"
            )

    # Economy receipt: required for testing/execute; optional elsewhere (warn if half-filled).
    has_exec_mode = "exec_mode=" in body
    has_pg = "pg=" in body
    has_econ = "econ=" in body
    if _is_testing_execute(body):
        if not has_exec_mode:
            errors.append("【遵守自检】testing/execute 须含 exec_mode=")
        if not has_pg:
            errors.append("【遵守自检】testing/execute 须含 pg=（无并行写 pg=na）")
        if not has_econ:
            warnings.append("【遵守自检】testing/execute 建议含 econ=（脚本优先;同页簇;造数一次 或 na）")
        em = re.search(r"exec_mode=([^|]+)", body)
        if em:
            val = em.group(1).strip()
            # allow compound like 脚本（本批）— take first token
            token = re.split(r"[;；,\s（(]", val, maxsplit=1)[0].strip()
            if token and token not in _EXEC_MODES:
                warnings.append(
                    f"exec_mode={token} 非标准枚举（脚本|直跑|模块子代理|拆分|na）；若有意请留 deviation="
                )
    elif has_exec_mode or has_pg or has_econ:
        if not (has_exec_mode and has_pg):
            warnings.append("【遵守自检】出现部分经济字段时建议成对写 exec_mode= 与 pg=")


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
    _check_header_lines(text, errors)
    _check_report_lead(text, errors, warnings)
    _check_sections(text, errors)
    _check_self_check(text, errors, warnings)

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
