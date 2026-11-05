#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
PACKS = ["wf-development", "wf-product", "wf-testing"]


def main() -> None:
    coverage_bad = 0
    thin_hard = 0
    dup_howto = 0
    pointer_hits = 0
    empty_howto = 0
    agent_frontend_ptr = 0
    samples: list[tuple[int, str]] = []

    for pack in PACKS:
        root = ROOT / pack
        agents = (root / "AGENTS.md").read_text(encoding="utf-8")
        # runtime pointer anti-pattern: tell AI to open frontend-gate as sole source mid-step
        if re.search(r"只认[^。\n]*frontend-gate\.md", agents):
            agent_frontend_ptr += 1
            print("AGENTS_RUNTIME_PTR", pack)
        for y in sorted((root / "workflows").glob("*.yaml")):
            data = yaml.safe_load(y.read_text(encoding="utf-8"))
            wid = data["workflow"].get("id") or y.stem
            for step in data.get("steps") or []:
                sid = step["id"]
                rel = f"rules/packets/{wid}/{sid}.md"
                mr = step.get("must_read") or []
                if not mr or str(mr[0]).replace("\\", "/") != rel or not (root / rel).is_file():
                    coverage_bad += 1
                    print("COVER_BAD", pack, wid, sid)

        for p in sorted((root / "rules" / "packets").rglob("*.md")):
            t = p.read_text(encoding="utf-8")
            if "此处不复述" in t or "继承开局卡" in t:
                thin_hard += 1
            # only flag true top-level duplicates (demoted #### across skills is OK)
            if t.count("## 0.5 ") >= 2 or t.count("## 0. 必做") >= 2:
                dup_howto += 1
            n = len(
                re.findall(
                    r"命中则加载|实施质量门\s*§|只认 `rules/|打开 `skills/|详见 `rules/",
                    t,
                )
            )
            if n:
                pointer_hits += 1
                samples.append((n, str(p.relative_to(ROOT))))
            if "无单独技能映射时" in t:
                empty_howto += 1

    print("coverage_bad", coverage_bad)
    print("thin_hard", thin_hard)
    print("dup_howto", dup_howto)
    print("pointer_packets", pointer_hits)
    print("empty_howto", empty_howto)
    print("agents_frontend_ptr", agent_frontend_ptr)
    print("--- top pointer packets ---")
    for n, p in sorted(samples, key=lambda x: -x[0])[:15]:
        print(n, p)


if __name__ == "__main__":
    main()
