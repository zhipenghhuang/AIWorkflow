#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Safely retarget agent reads to cold-start + step packet (no DOTALL)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

NEW_READS = (
    "reads:\n"
    "  - rules/core/cold-start.md（仅新会话/切包）\n"
    "  - 当前 workflow step 的 must_read[0]（rules/packets/<wf>/<step>.md；本步唯一正文）\n"
    "  - 若步骤包 §6 点名：再开那一个模板\n"
)


def fix_agent(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text

    # IMPORTANT: no DOTALL — '.' must not cross lines
    text2, n = re.subn(
        r"(?m)^reads:\n(?:[ \t]+-[^\n]*\n)+",
        NEW_READS,
        text,
        count=1,
    )
    if n == 0:
        return False
    text = text2

    out: list[str] = []
    for line in text.splitlines(keepends=True):
        raw = line.rstrip("\r\n")
        eol = "\n"
        if "read-index" in raw:
            raw = raw.replace(
                "中段只认 rule_card + read-index 当前行",
                "中段只认 rule_card + 当前步骤包",
            )
            raw = raw.replace(
                "rules/read-index.md（当前 step 行）",
                "当前步骤包（YAML must_read）",
            )
            raw = raw.replace(
                "rules/read-index.md（onboard.* 或 skill-audit.*）",
                "当前步骤包（YAML must_read）",
            )
            raw = raw.replace("+ read-index MUST", "")
            raw = raw.replace("read-index MUST", "步骤包")
            raw = re.sub(r"rules/read-index\.md[^\n]*", "当前步骤包", raw)
        if "步内方法只认当前 step 的 skills" in raw:
            indent = re.match(r"^[ \t]*", raw).group(0)
            raw = (
                f"{indent}- 步内方法只认当前步骤包 §5（技能已嵌入）；"
                "禁通读 rules/read-index/playbook。"
            )
        if raw.lstrip().startswith("-") and "rules/playbooks/" in raw:
            raw = re.sub(
                r"rules/playbooks/[a-z0-9-]+\.md",
                "（playbook 维护素材，默认不读）",
                raw,
            )
        out.append(raw + eol)
    text = "".join(out)

    if "must:" in text:
        must_body = text.split("must:", 1)[1][:900]
        if "当前步骤包" not in must_body and "步骤包" not in must_body:
            text = re.sub(
                r"(?m)^must:\n",
                "must:\n"
                "  - 步内方法只认当前步骤包 §5；硬约束认 cold-start；完成只认 Claim/HITL。\n",
                text,
                count=1,
            )

    if text != orig:
        # sanity: never shrink below 60% of original
        if len(text) < len(orig) * 0.6:
            raise RuntimeError(f"refusing to truncate {path}: {len(orig)}->{len(text)}")
        path.write_text(text, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    n = 0
    for pack in ("wf-development", "wf-product", "wf-testing"):
        for p in sorted((ROOT / pack / "agents").glob("*.yaml")):
            if fix_agent(p):
                lines = len(p.read_text(encoding="utf-8").splitlines())
                print(f"fixed {p.relative_to(ROOT)} ({lines} lines)")
                n += 1
    print(f"done {n}")


if __name__ == "__main__":
    main()
