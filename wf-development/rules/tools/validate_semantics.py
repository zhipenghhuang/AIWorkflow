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


def approx_tokens(text: str) -> int:
    """Rough CJK-aware estimate: ~3.6 UTF-8 bytes per token."""
    return max(1, int(len(text.encode("utf-8")) / 3.6))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--max-tokens", type=int, default=12000)
    ap.add_argument("--soft-tokens", type=int, default=8000)
    ap.add_argument("--verbose", action="store_true", help="输出 HEAVY 提示")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    infos: list[str] = []

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
            # §6 empty but §5/§8 demands skill closure
            sec6 = re.search(r"## 6\..*?(?=\n## 7\.)", text, re.S)
            if sec6 and "本步无技能指向" in sec6.group(0):
                if "本步必开技能" in text:
                    warnings.append(f"SKILL_CONTRADICTION: {wid}/{sid} §6 无技能但 §5 标必开")
            # budget: packet + mandatory (必开) skills only; 条件/模板不计入最坏值
            m_must = re.search(r"本步必开技能[^\n]*", text)
            must_skills = set()
            if m_must:
                must_skills = set(re.findall(r"`([a-z0-9-]+)`", m_must.group(0)))
            total = len(text.encode("utf-8"))
            for name in must_skills:
                sp = root / "skills" / name / "SKILL.md"
                if sp.is_file():
                    total += len(sp.read_bytes())
            tok = int(total / 3.6)
            if tok > args.max_tokens:
                warnings.append(
                    f"BUDGET: {wid}/{sid} ~{tok} tokens > {args.max_tokens}（超重步上限，须拆）"
                )
            elif tok > args.soft_tokens:
                infos.append(
                    f"HEAVY: {wid}/{sid} ~{tok} tokens（重步；默认允许，超 12k 才拆）"
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
