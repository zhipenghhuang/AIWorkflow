#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Semantic checks that structural validators cannot see.

Covers: duplicate entry phrases, packet identity/edge fields, residual text,
empty-skill vs mandatory-skill contradiction, read budget, unreachable steps.

Usage: python validate_semantics.py <package-root> [--max-tokens 8000]
Exit: 0 = ok (warnings allowed), 1 = errors.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

RESIDUE = ("//", "→。", "→；", "→ /")
REQUIRED_PACKET_MARKS = ("- **角色**：", "- **上游**：", "- **后续**：", "- **失败去向**：")
# 每步读链上限（packet + 必开技能整卡）。重步含 2～4 个方法技能，单列上限；
# 其余步沿用默认。预算约束技能长度/拆分，不把技能截成行窗。packet 另有 7k 上限。
STEP_CAPS = {"build": 22000, "implement": 22000, "execute": 22000, "init": 18000}
STEP_SOFT = {"build": 16000, "implement": 16000, "execute": 16000, "init": 14000}
PACKET_CAP = 7000


def approx_tokens(text: str) -> int:
    """Rough CJK-aware estimate: ~3.6 UTF-8 bytes per token."""
    return max(1, int(len(text.encode("utf-8")) / 3.6))


def skill_full_bytes(root: Path, name: str) -> int:
    """Bytes actually read for a must-open skill: the whole SKILL.md."""
    sp = root / "skills" / name / "SKILL.md"
    if not sp.is_file():
        return 0
    return len(sp.read_text(encoding="utf-8").encode("utf-8"))



# 术语回归守卫：历史“路径 ASCII 化”曾把中文术语误替换成路径词，
# 导致规则/模板读不懂、AI 按错语义执行。命中即报错，不静默。
TERM_ALLOW_WORKROOT = ("输入", "测试用例", "执行台账", "测试脚本", "变更记录", "计划执行看板", "说明-")
TERM_ALLOW_CAP = ("槽位", "绑定", "装配")


def term_regressions(root: Path) -> list[str]:
    cn = "\u4e00-\u9fa5"
    p1 = re.compile(r"\{workroot\}/([" + cn + r"][^/\s`，。；|）)]*)")
    p2 = re.compile(r"[" + cn + r"](?:rules|skills|templates|capabilities)/")
    p3 = re.compile(r"(?:rules|skills|templates|capabilities)/([" + cn + r"][^/\s`，。；|）)]*)")
    out: list[str] = []
    for f in sorted(root.rglob("*")):
        if not f.is_file() or f.suffix not in (".md", ".yaml"):
            continue
        if any(part in f.parts for part in (".draft", ".state", ".gate", "__pycache__")):
            continue
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            bad = False
            for m in p1.finditer(line):
                if not m.group(1).startswith(TERM_ALLOW_WORKROOT):
                    bad = True
            if p2.search(line):
                bad = True
            for m in p3.finditer(line):
                if m.group(1).startswith(TERM_ALLOW_CAP):
                    continue
                bad = True
            if bad:
                out.append(
                    f"TERM_REGRESSION: {f.relative_to(root)}:{i} 疑似术语被替换成路径词："
                    f"{line.strip()[:80]}"
                )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--max-tokens", type=int, default=16000)
    ap.add_argument("--soft-tokens", type=int, default=12000)
    ap.add_argument("--verbose", action="store_true", help="输出 HEAVY 提示")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    infos: list[str] = []

    errors.extend(term_regressions(root))

    entry_owner: dict[str, str] = {}

    cold = root / "rules" / "core" / "cold-start.md"
    if not cold.is_file():
        errors.append("COLD_START_MISSING: rules/core/cold-start.md")
    else:
        ctext = cold.read_text(encoding="utf-8")
        for heading in ("## 1. 新会话顺序", "## 2. 续跑", "## 3. 回执"):
            if heading not in ctext:
                errors.append(f"COLD_START_SECTION: 缺 {heading}")
        if "本卡不再回指 AGENTS" not in ctext and "不再回指 AGENTS" not in ctext:
            errors.append("COLD_START_ENTRY: 开局卡须声明入口已是 AGENTS、不再回指")
    glob = root / "rules" / "core" / "global-rules.md"
    if not glob.is_file():
        errors.append("GLOBAL_RULES_MISSING: rules/core/global-rules.md")
    else:
        gtext = glob.read_text(encoding="utf-8")
        for marker in ("## 1. 开工判定", "## 7. 读法与技能", "## 11. 冲突与例外"):
            if marker not in gtext:
                errors.append(f"GLOBAL_RULES_SECTION: 缺 {marker}")
    for y in sorted((root / "workflows").glob("*.yaml")):
        data = yaml.safe_load(y.read_text(encoding="utf-8")) or {}
        wid = (data.get("workflow") or {}).get("id") or y.stem
        for phrase in (data.get("entry_points") or {}):
            key = str(phrase).strip()
            if key in entry_owner and entry_owner[key] != wid:
                errors.append(
                    f"DUP_ENTRY: '{key}' 同时登记在 {entry_owner[key]} 与 {wid}"
                )
            entry_owner[key] = wid

    for y in sorted((root / "workflows").glob("*.yaml")):
        data = yaml.safe_load(y.read_text(encoding="utf-8")) or {}
        wid = (data.get("workflow") or {}).get("id") or y.stem
        steps = [s for s in (data.get("steps") or []) if isinstance(s, dict) and "id" in s]
        ids = [s["id"] for s in steps]
        # unreachable: previous step jumps over it and nobody targets it
        for i, step in enumerate(steps):
            sid = step["id"]
            targeted = any(str(s.get("next") or "") == sid for s in steps)
            if i == 0 or targeted:
                continue
            prev = steps[i - 1]
            if prev.get("next") and prev["next"] != sid:
                errors.append(
                    f"UNREACHABLE: {wid}/{sid} 被 {prev['id']}.next={prev['next']} 越过，且无其它入边"
                )
        for step in steps:
            sid = step["id"]
            packet = root / f"rules/packets/{wid}/{sid}.md"
            if not packet.is_file():
                continue
            text = packet.read_text(encoding="utf-8")
            for other in set(re.findall(r"rules/packets/([a-z0-9-]+)/", text)):
                if other != wid:
                    warnings.append(
                        f"CROSS_CHAIN: {wid}/{sid} 引用了其它链 {other} 的包；除非诊断需要，跨链应走路由/handoff"
                    )
            for mark in REQUIRED_PACKET_MARKS:
                if mark not in text:
                    errors.append(f"PACKET_ID: {wid}/{sid} 缺 {mark.strip()}")
            for bad in RESIDUE:
                if bad in text:
                    errors.append(f"RESIDUE: {wid}/{sid} 含 '{bad}'")
            for line in text.splitlines():
                if "可跳过" in line and "不可跳过" not in line:
                    errors.append(
                        f"SKIP_LOOPHOLE: {wid}/{sid} 含无条件「可跳过」：{line.strip()[:60]}"
                        "（改为 when/hitl_when 为假 + when_eval，或用户同意记 skip=）"
                    )
            # §6 empty but §5/§8 demands skill closure
            sec6 = re.search(r"## 6\..*?(?=\n## 7\.)", text, re.S)
            if sec6 and "本步无技能指向" in sec6.group(0):
                if "本步必开技能" in text:
                    warnings.append(f"SKILL_CONTRADICTION: {wid}/{sid} §6 无技能但 §5 标必开")
            # budget: packet + all §6 skills（worst case; 条件未命中时实际更低）
            listed_skills = set()
            if sec6:
                listed_skills = set(re.findall(r"\| `([a-z0-9-]+)` \|", sec6.group(0)))
            total = len(text.encode("utf-8"))
            for name in listed_skills:
                total += skill_full_bytes(root, name)
            tok = int(total / 3.6)
            cap = STEP_CAPS.get(sid, args.max_tokens)
            soft = STEP_SOFT.get(sid, args.soft_tokens)
            pkt_tok = int(len(text.encode("utf-8")) / 3.6)
            if pkt_tok > PACKET_CAP:
                warnings.append(
                    f"PACKET_BUDGET: {wid}/{sid} 步骤卡 ~{pkt_tok} tokens > {PACKET_CAP}（卡体须瘦身）"
                )
            if tok > cap:
                warnings.append(
                    f"BUDGET: {wid}/{sid} ~{tok} tokens > {cap}（超重步上限，须拆）"
                )
            elif tok > soft:
                infos.append(
                    f"HEAVY: {wid}/{sid} ~{tok} tokens（重步；默认允许，超 {cap} 才拆）"
                )

    for w in warnings:
        print(f"WARN  {w}")
    if args.verbose:
        for i in infos:
            print(f"INFO  {i}")
    for e in errors:
        print(f"FAIL  {e}")
    print(f"SUMMARY errors={len(errors)} warnings={len(warnings)} heavy={len(infos)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
