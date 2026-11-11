#!/usr/bin/env python3
"""Lint a dev task report against .gate/wf-development/completion.json.

Checks:
- report contains 【验证回执】 with a Chinese conclusion (通过/部分通过/阻塞/未验证)
  or legacy verdict=...
- report contains the six-point closeout layout and the fixed sub-fields
- report contains a 汇报（可直接复制）block with a **short-name** lead
- report contains a 待你确认 section (无待确认写「待你确认：无」)
- conclusion maps to completion.json verdict; gate matches gate_id; task (if present) matches
- verdict != COMPLETE: positive completion words are rejected, but scoped phrases
  (部分完成/阶段完成/文档阶段完成/部分verify/有条件通过) and negatives are allowed
- verdict == COMPLETE: receipt includes checks= and unverified=
- scans the whole report, not only the 汇报 line
- --format-only: skip completion.json / gate mapping; check the closeout layout only
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
SCOPED_OK = re.compile(r"(部分通过|部分完成|阶段完成|文档阶段完成|部分验证|有条件通过|主路径通过|冒烟通过|定向通过|单测通过|测试通过|构建通过|检查通过|评审通过)")
VERDICT_MAP = {
    "通过": "COMPLETE",
    "部分通过": "PARTIAL",
    "阻塞": "BLOCKED",
    "未验证": "NOT_VERIFIED",
}
TITLE_RE = re.compile(r"【(?:任务|执行|生成)收尾】")
REPORT_LABEL = re.compile(r"汇报(?:（可直接复制）)?[：:]")
REPORT_LEAD = re.compile(
    r"汇报(?:（可直接复制）)?[：:][ \t]*(?:\n+[ \t]*(?:```[^\n]*\n)?)?[ \t]*\*\*[^*]+\*\*[ \t]*[（(]"
)
SECTION_RE = re.compile(
    r"(?m)^\s*([1-6])\.\s*(完成了什么|改了哪些文件|如何验证|假设与未决项|还存在什么问题或风险|当前进度与下一步)"
)
SECTION_LABELS = {
    1: ("影响：",),
    2: ("文件：", "未提交：", "建议动作：", "待提交摘要：", "git：", ".gitignore：", "文档归档："),
    4: ("假设：", "待你确认", "默认（不回复即执行）：", "回复：", "可转发产品："),
    6: ("当前：", "下一步：", "优先级：", "建议：", "不建议：", "完成标志："),
}
DECISION_LABELS = ("事项：", "选项：", "建议：", "影响/默认：")
APPENDIX_LABELS = ("资料补强：", "工作记忆：", "运行态：")


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


def check_layout(text: str, errors: list[str], warnings: list[str]) -> None:
    if not TITLE_RE.search(text):
        errors.append("缺少【任务收尾】/【执行收尾】/【生成收尾】标题")
        return

    receipt_match = re.search(r"【验证回执】([^\n]+)", text)
    if receipt_match:
        receipt = receipt_match.group(1)
        for key in ("结论=", "校验=", "检查="):
            if key not in receipt:
                errors.append(f"【验证回执】缺少 {key}")
        if "未验证=" not in receipt and "待确认=" not in receipt:
            errors.append("【验证回执】缺少 未验证= 或 待确认=")

    if not REPORT_LABEL.search(text):
        errors.append("完整收尾须有「汇报（可直接复制）：」块（不得并入第 1 点）")
    elif not REPORT_LEAD.search(text):
        errors.append("汇报须以 **短名**（结论态…）导语起笔（可紧随汇报：换行或 text 围栏内）")

    start = REPORT_LABEL.search(text)
    if start:
        end = text.find("1. 完成了什么", start.end())
        body = text[start.end(): end if end >= 0 else len(text)]
        if "`" in body:
            warnings.append("汇报块含行内反引号；汇报层禁路径/命令/标识，明细层可用")

    matches = list(SECTION_RE.finditer(text))
    nums = [int(m.group(1)) for m in matches]
    if nums != [1, 2, 3, 4, 5, 6]:
        errors.append("1～6 点须齐全、按顺序各起一行；当前=" + (",".join(map(str, nums)) or "无"))
        return

    pos = [m.start() for m in matches]
    sections: dict[int, str] = {}
    for index, match in enumerate(matches):
        end = pos[index + 1] if index + 1 < len(pos) else len(text)
        sections[int(match.group(1))] = text[match.start():end]

    for number, labels in SECTION_LABELS.items():
        body = sections.get(number, "")
        for label in labels:
            if label not in body:
                errors.append(f"第 {number} 点缺少「{label}」")

    point4 = sections.get(4, "")
    if "待你确认" in point4 and "待你确认：无" not in point4:
        for label in DECISION_LABELS:
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
    for label in APPENDIX_LABELS:
        if label not in appendix:
            errors.append(f"附录缺少「{label}」")


def check_self_check(text: str, errors: list[str]) -> None:
    sc = re.search(r"【遵守自检】([^\n]+)", text)
    if not sc:
        errors.append("缺少【遵守自检】行（route/mode/reads/gates/sync/skip/deviation）")
        return
    body = sc.group(1)
    for key in ("route=", "mode=", "reads=", "gates=", "global=", "sync=", "skip=", "deviation="):
        if key not in body:
            errors.append(f"【遵守自检】缺少 {key}")
    sync_match = re.search(r"sync=([^|]+)", body)
    if sync_match:
        sync_body = sync_match.group(1).strip()
        if (
            sync_body not in ("无", "na", "无门面变化")
            and "冷层" not in sync_body
            and re.search(r"版本|VERSION|bump|发布|上线|门面|部署", sync_body, re.I)
        ):
            warnings.append(
                "【遵守自检】sync= 含版本/发布/门面类表述时建议含 冷层:ok|na|deferred:<因>（见 doc-facade-sync）"
            )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    ap.add_argument("--completion", default=".gate/wf-development/completion.json")
    ap.add_argument("--format-only", action="store_true", help="只检查收尾版式，不读取 completion.json")
    args = ap.parse_args()

    report = Path(args.report)
    completion = Path(args.completion)
    if not report.is_file():
        print(f"REPORT_NOT_FOUND: {report}")
        return 2

    text = report.read_text(encoding="utf-8-sig", errors="replace")
    errors: list[str] = []
    warnings: list[str] = []

    check_layout(text, errors, warnings)
    check_self_check(text, errors)

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
        if args.format_only:
            if mapped not in set(VERDICT_MAP.values()):
                errors.append(f"回执结论={conclusion} 不在 通过/部分通过/阻塞/未验证")
        elif mapped:
            if not completion.is_file():
                errors.append(f"COMPLETION_NOT_FOUND: {completion} (先运行 Invoke-Gate.ps1，或加 --format-only)")
            else:
                try:
                    data = json.loads(completion.read_text(encoding="utf-8-sig"))
                except Exception as exc:
                    errors.append(f"COMPLETION_INVALID: {exc}")
                    data = {}
                if data.get("package") != "wf-development":
                    errors.append(f"completion.json 属于 {data.get('package')}，不是 wf-development；请重跑开发门")
                verdict = str(data.get("verdict", "UNKNOWN"))
                gate_id = str(data.get("gate_id") or data.get("commit") or "unknown")
                task_id = str(data.get("task_id") or "")
                if mapped != verdict:
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
                if verdict != "COMPLETE":
                    for line in text.splitlines():
                        if line.strip().startswith("【验证回执】"):
                            continue
                        if "完成标志" in line:
                            continue
                        scan_line = line.replace("完成了什么", "").replace("完成情况", "").replace("完成标志", "")
                        words = positive_words(scan_line)
                        if words:
                            errors.append(f"verdict={verdict} 但正文出现完成类措辞：{line.strip()[:120]}")
                            break
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

    for e in errors:
        print(f"REPORT_LINT_FAIL: {e}")
    for w in warnings:
        print(f"WARN_REPORT_LINT: {w}")
    if errors:
        return 1
    print("REPORT_LINT_OK: format only" if args.format_only else "REPORT_LINT_OK: verdict checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
