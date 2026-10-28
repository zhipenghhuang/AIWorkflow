#!/usr/bin/env python3
# 同源脚本：三包内容一致；改一处需同步另外两包。
"""Static quality gate for 技能/*/SKILL.md.

Usage: python check_skills.py <package-root> [--strict]

Checks (no LLM calls, no token cost):
- frontmatter name/description; description has Chinese trigger
- <= 500 lines
- at least 2 method markers (步骤/清单/检查/阈值/反例/输出/自检/DoD)
- skill name referenced somewhere in workflows/agents/rules/skills
- duplicate skill names
Exit 0 = pass; with --strict, warnings also fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

METHOD_MARKERS = ("步骤", "清单", "检查", "阈值", "反例", "输出", "自检", "DoD", "判定")
CJK = re.compile(r"[\u4e00-\u9fff]")


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    data: dict[str, str] = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def main() -> int:
    if len(sys.argv) < 2:
        print("USAGE: check_skills.py <package-root> [--strict]")
        return 2
    root = Path(sys.argv[1]).resolve()
    strict = "--strict" in sys.argv
    skill_root = root / "技能"
    if not skill_root.is_dir():
        print("SKILL_DIR_MISSING")
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    names: dict[str, Path] = {}
    skills: list[tuple[str, Path, str]] = []

    for p in sorted(skill_root.glob("*/SKILL.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        fm = frontmatter(text)
        name = fm.get("name", "")
        desc = fm.get("description", "")
        rel = p.relative_to(root)
        if not name:
            errors.append(f"{rel}: frontmatter 缺少 name")
        elif name in names:
            errors.append(f"{rel}: name 重复（{names[name]}）")
        else:
            names[name] = rel
        if not desc:
            errors.append(f"{rel}: frontmatter 缺少 description")
        elif not CJK.search(desc):
            warnings.append(f"{rel}: description 缺中文触发词")
        lines = len(text.splitlines())
        if lines > 500:
            errors.append(f"{rel}: {lines} 行 > 500（拆 references/）")
        markers = [m for m in METHOD_MARKERS if m in text]
        if len(markers) < 2:
            warnings.append(f"{rel}: 方法标记不足（{','.join(markers) or '无'}）")
        skills.append((name or p.parent.name, p, text))

    corpus = ""
    for sub in ("workflows", "agents", "规则", "技能"):
        d = root / sub
        if not d.is_dir():
            continue
        for f in d.rglob("*"):
            if f.is_file() and f.suffix in (".md", ".yaml") and f.name != "SKILL.md":
                corpus += f.read_text(encoding="utf-8", errors="replace")
    for name, p, _ in skills:
        if name and name not in corpus:
            warnings.append(f"{p.relative_to(root)}: 未被 workflows/agents/规则/技能 引用")

    if warnings:
        for w in warnings:
            print(f"WARN_SKILL: {w}")
    if errors:
        for e in errors:
            print(f"ERROR_SKILL: {e}")
        print(f"SKILL_CHECK_FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    if strict and warnings:
        print(f"SKILL_CHECK_FAILED: {len(warnings)} warning(s) (strict)")
        return 1
    print(f"SKILL_CHECK_OK ({len(skills)} skill(s), {len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
