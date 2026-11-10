#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate step packets vs workflows (state machine + skill loop)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

SECTIONS = [
    "## 1. 元信息",
    "## 2. 本步目标",
    "## 3. 本步硬约束",
    "## 4. 本步门",
    "## 5. 本步动作",
    "## 6. 技能指向",
    "## 7. 模板与证据",
    "## 8. 完成与退出",
    "## 9. 回执",
]


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate_step_packets.py <package-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    fail = 0
    for ypath in sorted((root / "workflows").glob("*.yaml")):
        data = yaml.safe_load(ypath.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or "workflow" not in data:
            print(f"FAIL: bad yaml {ypath.name}")
            fail += 1
            continue
        wid = data["workflow"].get("id") or ypath.stem
        chain = root / f"workflows/{wid}.md"
        if not chain.is_file():
            print(f"FAIL: missing chain {wid}.md")
            fail += 1
        for step in data.get("steps") or []:
            if not isinstance(step, dict) or "id" not in step:
                continue
            sid = step["id"]
            rel = f"rules/packets/{wid}/{sid}.md"
            path = root / rel
            mr = step.get("must_read") or []
            first = str(mr[0]).replace("\\", "/") if mr else ""
            if first == "rules/packets/_shared/closeout.md":
                if not (root / first).is_file():
                    print(f"FAIL: {wid}/{sid} missing shared closeout")
                    fail += 1
                continue
            if not mr:
                print(f"FAIL: {wid}/{sid} missing must_read")
                fail += 1
            elif first != rel:
                print(f"FAIL: {wid}/{sid} must_read[0]={first} != {rel}")
                fail += 1
            if not path.is_file():
                print(f"FAIL: missing packet {rel}")
                fail += 1
                continue
            text = path.read_text(encoding="utf-8")
            for h in SECTIONS:
                if h not in text:
                    print(f"FAIL: {rel} missing section {h}")
                    fail += 1
            if "此处不复述" in text:
                print(f"FAIL: {rel} thin hard-constraints")
                fail += 1
            if "不打开 skill 也能做完" in text or "不打开 skill" in text:
                print(f"FAIL: {rel} implies skipping skills")
                fail += 1
            # skill bodies must not be embedded
            if re.search(r"### 来自 `[^`]+` 的必做（已写入本包）", text):
                print(f"FAIL: {rel} embeds skill body into packet")
                fail += 1
            if text.count("#### 0. 必做") >= 1:
                print(f"FAIL: {rel} embeds skill #### sections")
                fail += 1
            if "打开 → 执行 → 回本包" not in text and "打开→执行→回" not in text:
                # every packet should describe the skill loop in §6 area
                if "## 6. 技能指向" in text and "本步无技能指向" not in text:
                    if "必开" not in text and "条件开" not in text:
                        print(f"FAIL: {rel} skill section missing loop language")
                        fail += 1
            head = text.split("## 6.")[0]
            sec6 = re.search(r"## 6\..*?(?=\n## 7\.)", text, re.S)
            listed = set(re.findall(r"\| `([a-z0-9-]+)` \|", sec6.group(0))) if sec6 else set()
            refs = set(re.findall(r"§6[^`\n]{0,10}`([a-z0-9-]+)`", head))
            refs |= set(re.findall(r"`skills/([a-z0-9-]+)/SKILL\.md`", head))
            for name in sorted(refs - listed):
                print(f"FAIL: {rel} SKILL_REF_NOT_IN_SECTION6: {name}")
                fail += 1
            if "reads=" in text and rel not in text:
                print(f"FAIL: {rel} receipt missing self path")
                fail += 1
            # 编排笔记/动作清单里不得留未展开缩写与未填占位（AI 无法解析）
            for pat, why in (
                (r"\bREF[。；，）]", "未展开缩写 REF（改写成真实路径）"),
                (r"[=＝]\s*[。；]", "占位符未填（形如 `xx=。`）"),
                (r"按装填", "残句（应为「按计划 §x 装填」）"),
            ):
                if re.search(pat, text):
                    print(f"FAIL: {rel} {why}")
                    fail += 1
            # 自足性硬检：不得留空指针；不得把本步规则外指到大手册/他步。
            for bad, why in (
                ("本包对应节", "空指针（无对应标题）"),
                ("文档治理（本步动作已写清", "空指针（文档治理被中性化）"),
                ("本包实施预检", "空指针（实施预检被中性化）"),
                ("派子代理时按本包 §5 子代理纪律", "空指针（子代理纪律无对应节）"),
            ):
                if bad in text:
                    print(f"FAIL: {rel} {why}: {bad}")
                    fail += 1
            for m in re.finditer(r"`(rules/(?!packets/|templates/|tools/|core/)[^`]+)`", text):
                print(f"FAIL: {rel} external rule ref: {m.group(1)}（写进本包规则卡，勿外指）")
                fail += 1
    print(f"SUMMARY fail={fail}")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
