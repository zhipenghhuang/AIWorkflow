#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate self-contained step packets; rewrite workflows with clean must_read (PyYAML)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


class _Dumper(yaml.SafeDumper):
    pass


def _str_representer(dumper, data: str):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


_Dumper.add_representer(str, _str_representer)


def load_gates_table(root: Path) -> dict[str, str]:
    p = root / "rules" / "gates.md"
    out: dict[str, str] = {}
    if not p.is_file():
        return out
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        if cells[0] in ("标记", "门", "---") or set(cells[0]) <= {"-"}:
            continue
        # row may be: | 理解门 | `confirm_understanding`（when…） | 说明 |
        desc = cells[-1] if len(cells) >= 3 else cells[1]
        names = re.findall(r"`(confirm_[a-z0-9_]+|select_[a-z0-9_]+|[a-z][a-z0-9-]*)`", " | ".join(cells))
        for name in names:
            if name.startswith(("confirm_", "select_")) or "-" in name:
                out[name] = desc
        # also allow first cell if it is already a gate id
        key0 = cells[0].strip("`")
        if key0.startswith(("confirm_", "select_")) or key0.startswith("gate:"):
            out[key0] = desc
    return out


def list_skill_dirs(root: Path) -> set[str]:
    sk = root / "skills"
    if not sk.is_dir():
        return set()
    return {p.name for p in sk.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()}


def parse_readme_skill_rows(root: Path) -> list[tuple[str, list[str]]]:
    p = root / "skills" / "README.md"
    if not p.is_file():
        return []
    rows: list[tuple[str, list[str]]] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        left, right = cells[0], cells[1]
        if left in ("步骤", "步骤 / 轨", "别名") or set(left) <= {"-"}:
            continue
        skills = re.findall(r"skills/([a-z0-9-]+)", right)
        if skills:
            rows.append((left, skills))
    return rows


# Explicit high-value maps (README rows are fuzzy; these win for main chains)
EXPLICIT: dict[str, dict[str, list[str]]] = {
    "wf-development": {
        "change/clarify": ["requirements-and-spec", "product-shaping"],
        "change/analyze_input": ["product-doc-analysis", "requirements-and-spec"],
        "change/requirements": ["requirements-and-spec", "cross-layer-consistency"],
        "change/design": ["solution-design", "engineering-quality", "cross-layer-consistency"],
        "change/review-docs": ["design-doc-review", "engineering-quality"],
        "change/plan": ["task-breakdown", "cross-layer-consistency"],
        "change/implement": [
            "implementation-and-selftest",
            "engineering-quality",
            "frontend-implementation",
            "product-doc-analysis",
        ],
        "change/review": ["code-review", "engineering-quality"],
        "change/verify": ["test-design-and-execution"],
        "change/deliver": ["qa-handoff-and-release"],
        "change/release_handoff": ["qa-handoff-and-release"],
        "iterate/plan": ["task-breakdown", "cross-layer-consistency"],
        "iterate/implement": ["implementation-and-selftest", "engineering-quality"],
        "iterate/review": ["code-review", "engineering-quality"],
        "iterate/deliver": ["qa-handoff-and-release"],
        "solo/frame": ["product-shaping"],
        "solo/plan": ["product-shaping", "solution-design", "task-breakdown"],
        "solo/build": ["implementation-and-selftest", "engineering-quality"],
        "solo/test": ["test-design-and-execution"],
        "control/init": ["development-plan", "product-doc-analysis"],
        "control/run": ["development-plan"],
        "control/sync": ["development-plan"],
        "release/acceptance": ["acceptance-and-launch"],
        "release/readiness": ["acceptance-and-launch", "observability-and-instrumentation"],
        "release/deploy": ["acceptance-and-launch"],
        "release/verify": ["acceptance-and-launch"],
        "release/rollback": ["acceptance-and-launch"],
        "release/postrelease": ["acceptance-and-launch", "observability-and-instrumentation"],
        "retro/gather": ["retrospective-and-improvement"],
        "retro/analyze": ["retrospective-and-improvement"],
        "retro/actions": ["retrospective-and-improvement"],
        "intake/parse": ["change-intake", "product-doc-analysis"],
        "defect-fix/fix": ["cross-layer-consistency", "debugging-and-error-recovery"],
        "defect-fix/implement": ["implementation-and-selftest", "debugging-and-error-recovery"],
    },
    "wf-product": {
        "prd/discover": ["customer-needs-discovery", "requirement-discovery-and-prioritization"],
        "prd/benchmark": ["competitive-intelligence-and-learning", "requirement-discovery-and-prioritization"],
        "prd/prioritize": ["requirement-discovery-and-prioritization"],
        "prd/prd": ["prd-writing", "analytics-and-experimentation"],
        "prd/review": ["artifact-review", "review-and-finalize"],
        "plan/goals": ["zero-to-one-product-definition", "requirement-discovery-and-prioritization"],
        "plan/roadmap": ["zero-to-one-product-definition", "requirement-discovery-and-prioritization"],
        "plan/review-plan": ["artifact-review"],
        "prototype/context": ["prototype-and-interaction"],
        "prototype/ia": ["prototype-and-interaction"],
        "prototype/wireframe": ["prototype-and-interaction"],
        "prototype/visual": ["ui-visual-design-system"],
        "prototype/hi-fi": ["ui-visual-design-system"],
        "prototype/review": ["artifact-review", "ui-visual-design-system"],
        "prototype/handoff": ["prototype-and-interaction"],
        "change/intake": ["customer-needs-discovery", "change-management"],
        "change/triage": ["change-management"],
        "change/assess": ["change-management"],
        "change/apply": ["change-management"],
        "change/verify": ["change-management"],
        "change/review": ["artifact-review", "review-and-finalize"],
        "deliver/uat": ["uat-and-retrospective", "analytics-and-experimentation"],
        "deliver/release": ["uat-and-retrospective"],
        "showcase/audience": ["demo-storytelling"],
        "showcase/story": ["demo-storytelling"],
        "showcase/demo": ["demo-storytelling"],
        "showcase/materials": ["presentation-design"],
        "showcase/docs": ["product-docs"],
        "new-product/discover": ["zero-to-one-product-definition", "customer-needs-discovery"],
        "new-product/define": ["zero-to-one-product-definition"],
        "defect/analyze": ["change-management"],
        "defect/apply": ["change-management"],
        "defect/writeback": ["change-management"],
    },
    "wf-testing": {
        "testing/analyze": ["test-basis-analysis", "test-analysis-and-plan"],
        "testing/plan": ["test-analysis-and-plan", "test-data-and-environment"],
        "testing/generate": ["testcase-design", "ai-feature-testing"],
        "testing/review-cases": ["test-artifact-review", "testcase-review"],
        "testing/execute": [
            "test-execution-and-exploration",
            "test-data-and-environment",
            "ai-feature-testing",
        ],
    },
}


def resolve_skills_for_step(
    root: Path,
    pack_key: str,
    wid: str,
    sid: str,
    step: dict,
    skill_dirs: set[str],
    readme_rows: list[tuple[str, list[str]]],
) -> list[str]:
    found: list[str] = []

    def add(name: str) -> None:
        name = name.strip()
        if name and name in skill_dirs and name not in found:
            found.append(name)

    key = f"{wid}/{sid}"
    for s in EXPLICIT.get(pack_key, {}).get(key, []):
        add(s)

    raw = step.get("skills") or []
    if isinstance(raw, str):
        raw = [raw]
    for s in raw:
        add(str(s))

    notes = step.get("notes") or ""
    if isinstance(notes, str):
        for m in re.finditer(r"skills/([a-z0-9-]+)", notes):
            add(m.group(1))

    wf_aliases = {
        "change",
        "iterate",
        "solo",
        "prd",
        "plan",
        "defect",
        "defect-fix",
        "release",
        "testing",
        "prototype",
        "deliver",
        "showcase",
        "new-product",
        "retro",
        "onboard",
        "skill-audit",
        "control",
        "intake",
    }
    matches: list[tuple[int, list[str]]] = []
    for left, skills in readme_rows:
        if not re.search(rf"(?<![a-z0-9-]){re.escape(sid)}(?![a-z0-9-])", left, re.I):
            continue
        left_l = left.lower()
        score = 1
        if wid.lower() in left_l:
            score += 10
        mentioned = [w for w in wf_aliases if w in left_l]
        if mentioned and wid.lower() not in left_l and wid.replace("_", "-") not in mentioned:
            if any(w not in {wid.lower(), wid.replace("_", "-")} for w in mentioned):
                continue
        matches.append((score, skills))
    matches.sort(key=lambda x: -x[0])
    for _, skills in matches[:2]:
        for s in skills:
            add(s)

    # implement/build: keep frontend skill but mark conditional in howto header
    return found


def neutralize_pointers(text: str) -> str:
    """Remove runtime pointer-hopping phrases inside embedded skill text."""
    text = re.sub(r"详见\s*`rules/[^`]+`", "（条款已写入本步骤包）", text)
    text = re.sub(
        r"先读\s*`rules/[^`]+`",
        "先按本包 §3/§5 执行",
        text,
    )
    text = re.sub(
        r"只认\s*`rules/[^`]+`",
        "只认本包硬约束与做法",
        text,
    )
    text = re.sub(
        r"读\s*`frontend-gate\.md`",
        "遵守本包前端硬门（有 UI）",
        text,
    )
    text = re.sub(
        r"`rules/core/clarification\.md`[^。；\n]*",
        "澄清纪律（一次一问、候选答案、未确认不升格）",
        text,
    )
    text = re.sub(
        r"按\s*`skills/[a-z0-9-]+/SKILL\.md`",
        "按本包已嵌入的对应技能节",
        text,
    )
    return text


def skill_body(root: Path, name: str, conditional: str | None = None) -> str:
    p = root / "skills" / name / "SKILL.md"
    header = f"### 技能 `{name}`"
    if conditional:
        header += f"\n\n> **条件加载**：{conditional}"
    if not p.is_file():
        return f"{header}\n\n（未找到 SKILL.md；按本步目标与硬约束执行。）"
    text = p.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2].strip()
    chunks: list[str] = []
    for pat in (
        r"(## 0\. 必做.*?)(?=\n## [1-9]|\Z)",
        r"(## 0\.5 .*?)(?=\n## [1-9]|\Z)",
        r"(## 0\.1 .*?)(?=\n## (?!0)|\Z)",
        r"(## 必做.*?)(?=\n## |\Z)",
        r"(## 反模式.*?)(?=\n## |\Z)",
        r"(## 反合理化.*?)(?=\n## |\Z)",
        r"(## 常见合理化.*?)(?=\n## |\Z)",
    ):
        m = re.search(pat, text, re.S)
        if m:
            chunk = m.group(1).strip()
            if chunk not in chunks:
                chunks.append(chunk)
    if not chunks:
        # Prefer sections with 必做 in title
        for m in re.finditer(r"(## [^\n]*必做[^\n]*\n.*?)(?=\n## |\Z)", text, re.S):
            chunks.append(m.group(1).strip())
            if len(chunks) >= 2:
                break
    if not chunks:
        lines = text.splitlines()
        chunks.append("\n".join(lines[:60]))
    body = neutralize_pointers("\n\n".join(chunks))
    if len(body) > 9000:
        body = body[:9000] + "\n\n…（已截断；完整维护源在 skills/）"
    return f"{header}\n\n{body}"


def hitl_names(step: dict) -> list[str]:
    names: list[str] = []
    h = step.get("hitl")
    if h is None:
        return names
    if isinstance(h, str):
        return [h]
    if isinstance(h, list):
        for item in h:
            if isinstance(item, str):
                names.append(item)
            elif isinstance(item, dict) and item.get("name"):
                names.append(str(item["name"]))
    return names


def _split_path_blob(blob: str) -> list[str]:
    parts = re.split(r"[、,;；|/]+", blob)
    out: list[str] = []
    for p in parts:
        p = p.strip().strip("`\"'")
        p = re.sub(r"[。．.]+$", "", p)
        if p.startswith("rules/") and ("templates/" in p or "closeout" in p):
            out.append(p)
    return out


def extract_template(step: dict, root: Path) -> str | None:
    cands: list[str] = []
    for mr in step.get("must_read") or []:
        s = str(mr).replace("\\", "/")
        if s.startswith("rules/packets/"):
            continue
        cands.extend(_split_path_blob(s))
    notes = step.get("notes") or ""
    if isinstance(notes, str):
        for m in re.finditer(r"(rules/(?:templates|core)/[^\s`\"'，。；]+)", notes):
            cands.extend(_split_path_blob(m.group(1)))
        if "closeout-skeleton" in notes and not cands:
            for rel in (
                "rules/templates/90-handoff/closeout-skeleton.md",
                "rules/templates/closeout-skeleton.md",
            ):
                if (root / rel).is_file():
                    cands.append(rel)
                    break
    seen: list[str] = []
    for c in cands:
        if c not in seen and (root / c).is_file():
            seen.append(c)
    if not seen:
        for c in cands:
            if c not in seen:
                seen.append(c)
    return seen[0] if seen else None


def sanitize_notes_for_yaml(notes: str) -> str:
    """Drop stale file§N anchors that break Test-Template; keep prose intact."""
    if not notes:
        return notes
    # foo.md §1.2 / foo.yaml §0 → foo.md / foo.yaml
    notes = re.sub(
        r"(`?[A-Za-z0-9_./\\-]+\.(?:md|yaml|yml|ps1|py)`?)\s*§[\d]+(?:\.[\d]+)*",
        r"\1",
        notes,
    )
    notes = re.sub(r"[ \t]{2,}", " ", notes)
    return notes.strip()


def notes_to_howto(notes: str) -> str:
    notes = notes.strip()
    if not notes:
        return "按 §2 产出落盘；结果须可验证；有门则先过门。"
    # split into bullets on ；。or numbered cues
    parts = re.split(r"[；;]\s*", notes)
    bullets = []
    for p in parts:
        p = p.strip().strip("。")
        if p:
            bullets.append(f"- {p}。")
    if len(bullets) == 1 and len(notes) > 180:
        bullets = [f"- {notes}"]
    return "### 本步动作清单\n\n" + "\n".join(bullets)


def render_packet(
    root: Path,
    pack_label: str,
    pack_key: str,
    wid: str,
    step: dict,
    gates: dict[str, str],
    skills: list[str],
    template: str | None,
) -> str:
    sid = step["id"]
    name = step.get("name") or sid
    output = step.get("output") or "（见本步产出约定）"
    when = step.get("when")
    notes = step.get("notes") or ""
    if not isinstance(notes, str):
        notes = str(notes)
    notes = notes.strip()

    risk = ""
    if when:
        risk += f"- **条件步** `when={when}`：条件不满足则跳过本步（不打开本包）。\n"
    risk += "- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。\n"

    hard = (
        "- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。\n"
        "- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。\n"
        "- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。\n"
        "- **回执**：`reads=` 必须含本 packet 路径。\n"
    )
    if notes:
        hard += f"\n### 本步专有\n\n- {notes[:900]}\n"

    gate_lines: list[str] = []
    for hn in hitl_names(step):
        desc = gates.get(hn) or "出示确认块后等待用户。"
        gate_lines.append(f"- **HITL `{hn}`**：{desc}")
    gate = step.get("gate")
    if gate:
        gw = step.get("gate_when")
        desc = gates.get(f"gate: {gate}") or gates.get(str(gate)) or "运行对应 verify；未过不得宣称完成。"
        gate_lines.append(
            f"- **GATE `{gate}`"
            + (f" when={gw}" if gw else "")
            + f"**：{desc}"
        )
    if not gate_lines:
        gate_lines.append("- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。")

    howto: list[str] = []
    cond_skills = {
        "frontend-implementation": "仅当本步涉及 UI / 有原型时执行；无 UI 整节标 na。",
        "product-doc-analysis": "仅当本步输入含 PRD/原型/产品文档时执行；否则标 na。",
        "ai-feature-testing": "仅当被测含 LLM/RAG/Agent 时执行；否则标 na。",
    }
    if skills:
        for sk in skills:
            howto.append(skill_body(root, sk, cond_skills.get(sk)))
    else:
        howto.append(notes_to_howto(notes))
    if notes and skills:
        howto.append(f"### 编排备忘\n\n{notes}")

    open_lines = ["- 运行时正文：仅本文件（开局卡已在会话开头读过）。"]
    if template:
        open_lines.append(f"- 填写模板（仅此一个）：`{template}`")
    if gate or (isinstance(notes, str) and ("Claim" in notes or "Invoke-Gate" in notes)):
        open_lines.append(
            "- 验证：`verify/Invoke-Gate.ps1`（完成声称加 `-Claim`）；有 UI 另按包内前端条。"
        )
    if not template and not gate:
        open_lines.append("- 无强制模板：直接写 §2 产出路径产物。")

    rel = f"rules/packets/{wid}/{sid}.md"
    return f"""# 步骤包 · {wid}/{sid}

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：{pack_label}
- **workflow**：`{wid}`
- **step**：`{sid}`（{name}）
- **packet**：`{rel}`
{risk}
## 2. 本步目标

- **目标**：{name}
- **产出**：{output}

## 3. 本步硬约束

{hard}
## 4. 本步门

{chr(10).join(gate_lines)}

## 5. 做法

{chr(10).join(howto)}

## 6. 打开/填写

{chr(10).join(open_lines)}

## 7. 完成信号

- §2 产出已落盘。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 8. 回执字段

```text
route=workflow:{wid} | step={sid} | reads={rel} | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `{rel}`；对不上 = 未遵守读链。
"""


def process_package(root: Path, pack_label: str) -> None:
    gates = load_gates_table(root)
    skill_dirs = list_skill_dirs(root)
    readme_rows = parse_readme_skill_rows(root)
    pack_key = root.name
    wf_dir = root / "workflows"
    for ypath in sorted(wf_dir.glob("*.yaml")):
        raw = ypath.read_text(encoding="utf-8")
        data = yaml.safe_load(raw)
        if not isinstance(data, dict) or "workflow" not in data:
            print(f"skip {ypath.name}")
            continue
        # drop retired runtime index pointer from workflow header
        if isinstance(data.get("workflow"), dict):
            data["workflow"].pop("read_index", None)
        wid = data["workflow"].get("id") or ypath.stem
        steps = data.get("steps") or []
        n = 0
        embedded = 0
        for step in steps:
            if not isinstance(step, dict) or "id" not in step:
                continue
            sid = step["id"]
            if isinstance(step.get("notes"), str):
                step["notes"] = sanitize_notes_for_yaml(step["notes"])
            skills = resolve_skills_for_step(
                root, pack_key, wid, sid, step, skill_dirs, readme_rows
            )
            template = extract_template(step, root)
            if sid == "wrap" and not template:
                for rel in (
                    "rules/templates/90-handoff/closeout-skeleton.md",
                    "rules/templates/closeout-skeleton.md",
                ):
                    if (root / rel).is_file():
                        template = rel
                        break
            packet_rel = f"rules/packets/{wid}/{sid}.md"
            packet_path = root / packet_rel
            packet_path.parent.mkdir(parents=True, exist_ok=True)
            body = render_packet(
                root, pack_label, pack_key, wid, step, gates, skills, template
            )
            # only split joined template backticks if any slipped in
            body = re.sub(
                r"`(rules/templates/[^`]+?[、,][^`]+?)`",
                lambda m: " / ".join(f"`{p}`" for p in _split_path_blob(m.group(1)))
                or m.group(0),
                body,
            )
            packet_path.write_text(body, encoding="utf-8", newline="\n")
            new_mr = [packet_rel]
            if template:
                new_mr.append(template)
            step["must_read"] = new_mr
            step.pop("skills", None)
            n += 1
            if skills:
                embedded += 1
        header = (
            "# 读取：仅当前 step 块。运行时 must_read[0]=rules/packets/<wf>/<step>.md（自包含）。\n"
            "# 禁通读规则目录；方法已嵌入步骤包。维护素材：skills/、rules/core 长文、playbooks/、read-index。\n"
        )
        dumped = yaml.dump(
            data,
            Dumper=_Dumper,
            allow_unicode=True,
            sort_keys=False,
            width=120,
        )
        tmp = ypath.with_suffix(ypath.suffix + ".tmp")
        tmp.write_text(header + dumped, encoding="utf-8", newline="\n")
        tmp.replace(ypath)
        print(f"OK {pack_label}/{wid}: {n} packets ({embedded} with skills)")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: build_step_packets.py <package-root> [label]", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    label = sys.argv[2] if len(sys.argv) > 2 else root.name
    process_package(root, label)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
