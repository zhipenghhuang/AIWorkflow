#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deep audit: state-machine regions, packets, skill loops, contradictions."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
PACKS = ["wf-development", "wf-product", "wf-testing"]

# Import region map from builder if possible
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from build_step_packets import (  # type: ignore
        CONDITIONAL_SKILLS,
        EXPLICIT,
        REGIONS,
        resolve_skills_for_step,
        list_skill_dirs,
        parse_readme_skill_rows,
    )
except Exception as e:  # pragma: no cover
    print("IMPORT_FAIL", e)
    raise


def main() -> int:
    fail = 0
    warn = 0
    for pack in PACKS:
        root = ROOT / pack
        skill_dirs = list_skill_dirs(root)
        readme_rows = parse_readme_skill_rows(root)
        cold = (root / "rules/core/cold-start.md").read_text(encoding="utf-8")
        if "打开→按必做执行" not in cold and "打开→执行" not in cold and "技能闭环" not in cold:
            print(f"FAIL {pack}: cold-start missing skill-loop language")
            fail += 1
        if "不打开 skill 也能" in cold:
            print(f"FAIL {pack}: cold-start allows skipping skills")
            fail += 1

        for ypath in sorted((root / "workflows").glob("*.yaml")):
            data = yaml.safe_load(ypath.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or "workflow" not in data:
                continue
            wid = data["workflow"].get("id") or ypath.stem
            steps = [s for s in (data.get("steps") or []) if isinstance(s, dict) and "id" in s]
            by_id = {s["id"]: s for s in steps}
            ids = list(by_id)

            chain = root / f"rules/packets/{wid}/_chain.md"
            if not chain.is_file():
                print(f"FAIL {pack}/{wid}: missing _chain.md")
                fail += 1
            else:
                ct = chain.read_text(encoding="utf-8")
                for sid in ids:
                    if f"`{sid}`" not in ct and sid not in ct:
                        print(f"FAIL {pack}/{wid}: _chain missing step {sid}")
                        fail += 1

            # region coverage: every region step exists; every step in a regioned wf appears in some region
            regs = REGIONS.get(pack, {}).get(wid, [])
            covered: set[str] = set()
            for rid, title, sids in regs:
                rpath = root / f"rules/packets/{wid}/_region-{rid}.md"
                if not rpath.is_file():
                    print(f"FAIL {pack}/{wid}: missing _region-{rid}.md")
                    fail += 1
                    continue
                rt = rpath.read_text(encoding="utf-8")
                alive = []
                for sid in sids:
                    if sid not in by_id:
                        print(f"FAIL {pack}/{wid}: region {rid} lists missing step {sid}")
                        fail += 1
                        continue
                    alive.append(sid)
                    covered.add(sid)
                    if f"`{sid}`" not in rt:
                        print(f"FAIL {pack}/{wid}/_region-{rid}: missing step row {sid}")
                        fail += 1
                if not alive:
                    print(f"FAIL {pack}/{wid}: region {rid} empty after filter")
                    fail += 1
            if regs:
                orphan = [s for s in ids if s not in covered]
                if orphan:
                    # Long-chain region maps must cover every step (no silent skips).
                    print(f"FAIL {pack}/{wid}: steps not in any region: {orphan}")
                    fail += 1

            # entry points land on existing steps
            ep = data.get("entry_points") or {}
            if isinstance(ep, dict):
                for k, v in ep.items():
                    if str(v) not in by_id:
                        print(f"FAIL {pack}/{wid}: entry_point '{k}' -> missing step {v}")
                        fail += 1

            # orch notes (rebuild source) — required once YAML notes are thin
            orch_path = root / f"rules/packets/{wid}/_orch.yaml"
            orch_steps: dict = {}
            if orch_path.is_file():
                od = yaml.safe_load(orch_path.read_text(encoding="utf-8")) or {}
                if isinstance(od.get("steps"), dict):
                    orch_steps = od["steps"]
            else:
                # thin YAML without orch = rebuild will wipe howto
                thin_n = sum(
                    1
                    for s in steps
                    if str(s.get("notes") or "").strip().startswith("只读 must_read")
                )
                if thin_n and thin_n == len(steps):
                    print(f"FAIL {pack}/{wid}: thin YAML notes but missing _orch.yaml")
                    fail += 1

            for step in steps:
                sid = step["id"]
                rel = f"rules/packets/{wid}/{sid}.md"
                path = root / rel
                mr = step.get("must_read") or []
                if not mr or str(mr[0]).replace("\\", "/") != rel:
                    print(f"FAIL {pack}/{wid}/{sid}: must_read mismatch {mr}")
                    fail += 1
                if not path.is_file():
                    print(f"FAIL {pack}/{wid}/{sid}: missing packet")
                    fail += 1
                    continue
                text = path.read_text(encoding="utf-8")
                for h in (
                    "## 5. 本步工作规则",
                    "## 6. 技能指向",
                    "## 8. 完成信号",
                    "## 9. 回执字段",
                ):
                    if h not in text:
                        print(f"FAIL {rel}: missing {h}")
                        fail += 1
                if "打开→执行→回" not in text and "打开 → 执行 → 回" not in text:
                    if "本步无技能指向" not in text:
                        print(f"FAIL {rel}: missing skill-loop language")
                        fail += 1
                if "### 来自 `" in text and "已写入本包" in text:
                    print(f"FAIL {rel}: embeds skill body")
                    fail += 1
                if text.count("#### 0. 必做") >= 1:
                    print(f"FAIL {rel}: embedded skill sections")
                    fail += 1
                if "勿另开技能" in text or "已嵌入的对应技能节" in text:
                    print(f"FAIL {rel}: stale language that skips real skill open")
                    fail += 1

                # frontend hard-gate completeness on implement-like steps
                if "### 前端硬门" in text:
                    for needle in (
                        "## 2. 必产物",
                        "parity-matrix",
                        "## 3. 必命令",
                        "frontend_parity.py",
                        "## 4. 验收底线",
                        "## 5. 禁做",
                    ):
                        if needle not in text:
                            print(f"FAIL {rel}: frontend-gate embed missing `{needle}`")
                            fail += 1

                # revive notes from orch for skill resolution after YAML thin
                step_for_skills = dict(step)
                if orch_steps.get(sid):
                    step_for_skills["notes"] = orch_steps[sid]
                skills = resolve_skills_for_step(
                    root, pack, wid, sid, step_for_skills, skill_dirs, readme_rows
                )
                key = f"{wid}/{sid}"
                explicit = EXPLICIT.get(pack, {}).get(key)
                expect = explicit if explicit is not None else skills
                for sk in expect or []:
                    if sk not in skill_dirs:
                        print(f"FAIL {rel}: skill dir missing {sk}")
                        fail += 1
                        continue
                    if f"`{sk}`" not in text and sk not in text:
                        print(f"FAIL {rel}: packet does not point to skill {sk}")
                        fail += 1
                    if sk not in CONDITIONAL_SKILLS:
                        m = re.search(rf"\| `{re.escape(sk)}` \| ([^|]+) \|", text)
                        if not m or "必开" not in m.group(1):
                            print(f"FAIL {rel}: skill {sk} should be 必开")
                            fail += 1

                # §5 howto should not be empty boilerplate-only when orch has rich notes
                if orch_steps.get(sid) and len(str(orch_steps[sid])) > 40:
                    if "### 本步动作清单" not in text:
                        print(f"FAIL {rel}: missing 动作清单 despite orch notes")
                        fail += 1

                for item in mr[1:]:
                    p = root / str(item).replace("\\", "/")
                    if not p.is_file():
                        print(f"FAIL {rel}: must_read template missing {item}")
                        fail += 1

                nxt = step.get("next")
                if nxt and str(nxt) not in by_id:
                    print(f"FAIL {pack}/{wid}/{sid}: next={nxt} missing")
                    fail += 1

        # critical main-chain explicit maps present
        critical = {
            "wf-development": ["change/implement", "change/verify", "change/clarify"],
            "wf-product": ["prd/prd", "change/apply"],
            "wf-testing": ["testing/execute", "testing/analyze"],
        }
        for key in critical.get(pack, []):
            if key not in EXPLICIT.get(pack, {}):
                print(f"WARN {pack}: missing EXPLICIT map {key}")
                warn += 1

    print(f"SUMMARY fail={fail} warn={warn}")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
