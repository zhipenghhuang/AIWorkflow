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

# --check：只渲染不落盘，用于检测「生成物 vs 源（workflows/*.yaml）」漂移。
CHECK = False
DRIFT: list[str] = []


def emit(path: Path, body: str) -> None:
    """Write generated body atomically; in --check mode only compare and record drift."""
    if CHECK:
        old = path.read_text(encoding="utf-8") if path.is_file() else None
        if old is None:
            DRIFT.append(f"MISSING {path}")
        elif old.replace("\r\n", "\n") != body.replace("\r\n", "\n"):
            DRIFT.append(f"STALE {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(body, encoding="utf-8", newline="\n")
    tmp.replace(path)


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
        "iterate/release_handoff": ["qa-handoff-and-release"],
        "iterate/gates": ["test-design-and-execution"],
        "solo/frame": ["product-shaping", "product-doc-analysis"],
        "solo/product": ["product-shaping", "product-doc-analysis"],
        "solo/design": ["solution-design", "task-breakdown", "engineering-quality"],
        "solo/review_docs": ["design-doc-review"],
        "solo/test_plan": ["test-design-and-execution"],
        "solo/build": ["implementation-and-selftest", "engineering-quality", "frontend-implementation", "product-doc-analysis"],
        "solo/review": ["code-review", "engineering-quality"],
        "solo/test": ["test-design-and-execution"],
        "control/init": ["development-plan", "product-doc-analysis", "product-shaping"],
        "control/run": ["development-plan"],
        "control/sync": ["development-plan"],
        "release/acceptance": ["acceptance-and-launch"],
        "release/readiness": ["acceptance-and-launch", "observability-and-instrumentation", "qa-handoff-and-release"],
        "release/deploy": ["acceptance-and-launch"],
        "release/verify": ["acceptance-and-launch"],
        "release/rollback": ["acceptance-and-launch"],
        "release/postrelease": ["acceptance-and-launch", "observability-and-instrumentation"],
        "retro/gather": ["retrospective-and-improvement"],
        "retro/analyze": ["retrospective-and-improvement"],
        "retro/actions": ["retrospective-and-improvement"],
        "intake/parse": ["change-intake", "product-doc-analysis"],
        "defect-fix/fix": ["debugging-and-error-recovery", "implementation-and-selftest", "cross-layer-consistency"],
        "defect-fix/implement": ["implementation-and-selftest", "debugging-and-error-recovery"],
    },
    "wf-product": {
        "prd/discover": ["customer-needs-discovery", "requirement-discovery-and-prioritization", "competitive-intelligence-and-learning"],
        "prd/benchmark": ["competitive-intelligence-and-learning", "requirement-discovery-and-prioritization"],
        "prd/prioritize": ["requirement-discovery-and-prioritization"],
        "prd/prd": ["prd-writing", "analytics-and-experimentation", "review-and-finalize"],
        "prd/review": ["artifact-review", "review-and-finalize"],
        "plan/goals": ["zero-to-one-product-definition", "requirement-discovery-and-prioritization", "customer-needs-discovery"],
        "plan/roadmap": ["zero-to-one-product-definition", "requirement-discovery-and-prioritization"],
        "plan/review-plan": ["artifact-review"],
        "prototype/context": ["prototype-and-interaction"],
        "prototype/ia": ["prototype-and-interaction"],
        "prototype/wireframe": ["prototype-and-interaction"],
        "prototype/visual": ["ui-visual-design-system"],
        "prototype/hi-fi": ["ui-visual-design-system", "prototype-and-interaction"],
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
        "new-product/discover": ["zero-to-one-product-definition", "customer-needs-discovery", "competitive-intelligence-and-learning"],
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
            "testcase-design",
            "test-execution-and-exploration",
            "test-data-and-environment",
            "test-interface",
            "test-performance-security-compatibility",
            "ai-feature-testing",
        ],
        "testing/report": [
            "test-artifact-review",
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
    explicit = EXPLICIT.get(pack_key, {}).get(key)
    if explicit is not None:
        for s in explicit:
            add(s)
        return found

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

    return found


# 外围参考层 → 短句。core/defects/collaboration 与 skill/模板保留可点开路径。
INLINE_RULES = (
    (
        r"`?rules/core/clarification\.md`?(?:\s*§[\d.]+)?",
        "先查事实；仍不明一次一问（附候选/推荐）；未确认不升格",
    ),
    (
        r"`?rules/doc-governance\.md`?(?:\s*§[\d.]+)?",
        "文档治理规则（工作根/原件根/索引/关版整夹）",
    ),
    (
        r"`?rules/workflow\.md`?(?:\s*§[\d.]+)?",
        "本步编排以当前步骤卡为准；方法见 §6；勿通读手册拼流程",
    ),
    (
        r"`?rules/core/verification\.md`?(?:\s*§[\d.]+)?",
        "完成口径：有 Claim 门才认 CLAIM: ALLOWED；无门则产出落盘+本步门过，claim=na",
    ),
    (
        r"`?rules/core/lightweight\.md`?(?:\s*§[\d.]+)?",
        "按风险裁剪文档厚度；必开技能/HITL 不降",
    ),
    (r"`?rules/core/project-readme\.md`?", "README：只写现行入口/运行/目录"),
    (r"`?rules/core/context-memory\.md`?", "工作记忆：偏好/洞见/坑 ≤3 行"),
    (
        r"`?rules/special/skill-audit\.md`?",
        "技能体检：盘点→适配→拟变更→确认→复检",
    ),
    (r"`?rules/gates\.md`?(?:\s*§[\d.]+)?", "门：见本包 §4"),
)


# Gate ids that require CLAIM: ALLOWED (package-specific). Others → claim=na.
CLAIMABLE_GATES: dict[str, set[str]] = {
    "wf-product": {
        "product-prd",
        "product-review",
        "design-review",
        "uat-evidence",
        "change-closure",
        "writeback",
        "prd",
        "review",
        "uat",
        "change",
    },
    "wf-development": {
        "completion-gate",
        "frontend",
        "s6-admission",
    },
    "wf-testing": {
        "report-consistency",
        "writeback",
        "report",
    },
}


def step_requires_claim(pack_key: str, gate: str | None, notes: str) -> bool:
    if not gate:
        # notes mentioning -Claim with an explicit claimable mode still count
        if re.search(r"-Claim\b", notes or "") and re.search(
            r"Mode\s+(report|writeback|prd|review|design-review|uat|change)",
            notes or "",
            re.I,
        ):
            return True
        return False
    g = str(gate).strip().lower()
    allowed = CLAIMABLE_GATES.get(pack_key, set())
    if g in allowed:
        return True
    # product gates often named product-prd / uat-evidence etc.
    for a in allowed:
        if a in g or g in a:
            return True
    return False


def expand_inline_rules(text: str) -> str:
    """Replace peripheral rule refs with a self-contained sentence (no doc hop)."""
    for pattern, replacement in INLINE_RULES:
        text = re.sub(pattern, replacement, text)
    return text


def rewrite_workflow_refs(text: str, current_wid: str | None = None) -> str:
    """Keep cross-chain targets as `other.step` / `other` 流程; same-chain → 本 workflow."""

    def _wid_of(fname: str) -> str:
        return re.sub(r"\.ya?ml$", "", fname.strip())

    def repl_bt(m: re.Match[str]) -> str:
        wid = _wid_of(m.group(1))
        step = m.group(2)
        if current_wid and wid == current_wid:
            return f"本 workflow{(' ' + step) if step else ''}"
        if step:
            return f"`{wid}.{step}`"
        return f"`{wid}` 流程"

    # `workflows/foo.yaml` [step]
    text = re.sub(
        r"`workflows/([^`]+)`(?:\s+(?:的\s*)?([A-Za-z0-9_-]+))?",
        repl_bt,
        text,
    )
    # bare workflows/foo.yaml [step] (no backticks)
    def repl_bare(m: re.Match[str]) -> str:
        wid = _wid_of(m.group(1) + ".yaml")
        step = m.group(2)
        if current_wid and wid == current_wid:
            return f"本 workflow{(' ' + step) if step else ''}"
        if step:
            return f"`{wid}.{step}`"
        return f"`{wid}` 流程"

    text = re.sub(
        r"(?<![`/\w])workflows/([a-z0-9_-]+)\.ya?ml(?:\s+(?:的\s*)?([A-Za-z0-9_-]+))?",
        repl_bare,
        text,
    )
    return text


def neutralize_pointers(text: str, current_wid: str | None = None) -> str:
    """Inline peripheral rules; keep templates/skills as first-class packet sections."""
    text = expand_inline_rules(text)
    text = re.sub(r"遵守\s*`frontend-gate`", "遵守本包「前端硬门」节（有 UI）", text)
    text = re.sub(r"`?rules/core/frontend-gate\.md`?", "本包前端硬门", text)
    text = re.sub(r"`frontend-gate`", "本包前端硬门", text)
    text = re.sub(r"`?frontend-gate\.md`?", "本包前端硬门", text)
    text = re.sub(
        r"`?rules/core/implementation-quality\.md`?(?:\s*§[\d.]+)?",
        "本包 §5 规则卡",
        text,
    )
    text = re.sub(
        r"\*{0,2}命中则加载\*{0,2}[：:][^\n]*",
        "命中面：按本包 §6 条件开技能闭环（打开→执行→回包）",
        text,
    )
    text = re.sub(r"实施质量门\s*§[\d.]+", "本包 §5 实施预检卡", text)
    text = re.sub(r"按实施质量门[^\n；。]*", "按本包 §5 实施预检卡", text)
    text = re.sub(
        r"`?implementation-quality\.md`?(?:\s*§[\d.]+)?",
        "本包 §5 规则卡",
        text,
    )
    text = re.sub(
        r"已加载\s*product-doc-analysis",
        "已按 §6 闭环执行 product-doc-analysis",
        text,
    )
    text = re.sub(
        r"加载\s*product-doc-analysis",
        "打开 product-doc-analysis 走 §6 闭环",
        text,
    )
    text = re.sub(
        r"`execution-contract\.md`(?:\s*§[\d.]+)?",
        "开局卡分级与动作前分析约定",
        text,
    )
    text = re.sub(r"`contract\.md`", "规则心跳一行格式", text)
    text = re.sub(
        r"`rules/capabilities/instance-discipline\.md`\s*§[\d.]+",
        "实例纪律（按需拉起、结束显式退程）",
        text,
    )
    # Skills → §6（本包技能表）；模板保留真实路径，由 §7 列出。
    text = re.sub(r"`skills/([a-z0-9-]+)/SKILL\.md`", r"§6 `\1`", text)
    text = re.sub(r"`skills/README\.md`", "技能体检：盘点→适配→拟变更→确认→复检", text)
    text = rewrite_workflow_refs(text, current_wid)
    text = re.sub(r"技能[：:]\s*§6", "技能见 §6", text)
    text = re.sub(r"技能[：:]\s+(?!§6)", "技能见 §6：", text)
    text = text.replace("按 本包", "按本包").replace("见 本包", "见本包")
    return text


def _skill_text(root: Path, name: str) -> str:
    p = root / "skills" / name / "SKILL.md"
    if not p.is_file():
        return ""
    text = p.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2].strip()
    return text


# Conditional skills: only open when situation matches; others listed for a step are 必开
CONDITIONAL_SKILLS = {
    "frontend-implementation": "有 UI / 有原型",
    "product-doc-analysis": "输入含 PRD/原型/产品文档",
    "ai-feature-testing": "被测含 LLM/RAG/Agent",
    "cross-layer-consistency": "命中权限/状态/数据基数/多表面",
    "threat-modeling": "安全/威胁面变更",
    "performance-and-capacity": "性能/容量面变更",
    "analytics-and-experimentation": "有指标/埋点/实验",
}

# Per-step conditional skills: only this step treats the skill as 条件开.
STEP_CONDITIONAL_SKILLS: dict[tuple[str, str, str], dict[str, str]] = {
    ("wf-product", "new-product", "discover"): {
        "competitive-intelligence-and-learning": "竞品分析/学习竞品（模式 S）"
    },
    ("wf-product", "plan", "goals"): {
        "customer-needs-discovery": "迭代路径/需求来源不明"
    },
    ("wf-product", "prd", "discover"): {
        "competitive-intelligence-and-learning": "竞品分析/学习竞品（模式 S）"
    },
    ("wf-product", "prd", "prd"): {
        "review-and-finalize": "定稿前自检"
    },
    ("wf-development", "control", "init"): {
        "product-shaping": "无 PRD/只有想法"
    },
    ("wf-development", "release", "readiness"): {
        "qa-handoff-and-release": "有提测/交接物"
    },
    ("wf-development", "solo", "frame"): {
        "product-doc-analysis": "输入含 PRD/原型/产品文档"
    },
}


COMMIT_CARD = """### 本步规则卡：拟提交块（必填 · 字段已在本包）

```text
【拟提交】
- 文件：{本批清单}
- .gitignore 现状：{一句}
- 当前分支：{名}；跟踪远程：{origin/xxx 或无}
- 本次动作：{仅提交（默认） / 提交+推送}；推送目标：{remote+分支 或 不推送}
- 基线：{干净 / 含前序 N 文件（清单与处理） / 含无关文件（排除）}
- 未提交统计：本任务 {n} / 前序 {m} / 无关 {k}
- 建议拆分：{单批 / 按任务拆 N 批}
- 目标落点：{与档案「修复落点分支/命名规则」相符 / 差异}
- 推送前检查：{CI/测试结果；未跑写「未跑」}
- PR/MR：{不开 / 拟开（目标分支）/ 档案要求必须开}
- 合并：{不执行；合并须点名或档案授权}
请确认：1) 是否提交本批；2) 如需推送，请明确「提交+推送」及目标分支。
```

- 默认仅本地提交；推送须单独确认；禁 force push、擅自切主干、擅自开/合并 PR。
- 无文件变更 → 跳过 `confirm_commit` 与提交；不得硬造提交。"""

WRAP_CARD = """### 本步规则卡：六点收尾（缺项=未收尾 · 形状已在本包）

```text
【任务收尾】（测试生成/执行可用【生成收尾】/【执行收尾】）
1. 完成了什么：影响：…
2. 改了哪些文件：文件：…；未提交：…；建议动作：…；待提交摘要：…；git：…；.gitignore：…；文档归档：…
3. 如何验证：结论=…；校验=…；检查=…；未验证/待确认=…
4. 假设与未决项：假设：…；待你确认：…（无则「待你确认：无」）
5. 还存在什么问题或风险：…
6. 当前进度与下一步：当前：…；下一步：…；优先级：…；建议：…；不建议：…；完成标志：…
汇报（可直接复制）：**结论态短名**（…）
【遵守自检】route=… | mode=… | packet=… | skills=… | reads=… | gates=… | confirm=… | sync=… | skip=… | deviation=…
附：运行与沉淀 · 资料补强：… | 工作记忆：… | 运行态：…
```

- 有门回执时跑 `verify/Test-Report.ps1 -Report <收尾文件>`；无门用 `python verify/tools/report_lint.py --format-only --report <收尾文件>`（有该工具时）。
- 同步 plan/INDEX/activeContext（收尾第 2/6 点确认同拍）；完整【拟提交】留待 commit。"""

TEST_PLAN_CARD = """### 本步规则卡：先分析，再计划

- 模板：`rules/templates/10-planning/test-analysis-template.md`（分析，必做）＋ `rules/templates/10-planning/test-plan-template.md`（总排）。
- 轻量：`test-plan-lite-template.md`；仅补丁/单模块且 `版本准出=否` 才用。
- 本步内先完成分析落盘，再写计划；分析未确认不得写计划。
- 计划是唯一总排；不重复分析大表；P0/P1/P2 均为覆盖义务。
- 关账：`{workroot}/{ver}/` 整夹迁入 `_archive/{yyyyMMdd}-{ver}/`。"""

LIFECYCLE_CARD = """### 本步规则卡：文档治理扫描

- 分类：长期/固定 → 就地更新；版本/迭代绑定 → 关闭时快照/归档；失效/替代 → 确认后归档；过程/临时（含已完结 .draft/）→ 清理候选。
- 归档前引用检查：被当前计划/用例/脚本/报告引用的输入/数据/冒烟清单保留原位或标「基线」。
- 确认前不改/不移/不删；有候选 → `docs_migration_needed=true`，停门等确认。
- 关账：迭代绑定文档迁入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`；主档关闭时快照、主档不移动；清理只删已知临时/缓存/未引用失败产物。
- 失效资料在 `inbound/INDEX.md` 状态列标记；不确定移 `{workroot}/_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。"""

DOC_GOV_CARD = """### 本步规则卡：文档治理

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认后将迭代绑定文档迁入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`；主档关闭时快照、主档不移动；「并行不关」只落新资料、不归档现行主档。
- 清理只删已知临时/缓存/未引用失败产物；不确定移 `_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。"""

PLAN_CARD = """### 本步规则卡：拆单与 SC

- 先确认范围/AC/非目标；未确认不拆单。
- 每条 AC/Then/异常/权限/数据/跨层抽成 SC；无 SC 不开工（L0 除外）；裁剪写债项。
- 每条 SC 必填可打开的路径+章节/画板/锚点、非空原文、落点、入口类型；`validate_tasklist.py` FAIL → 不得 `confirm_backlog`。
- 任务卡含 DoR/DoD/依赖/并行；并行 >3 或文件重叠 → 拆批。
- 只读不改代码；清单经 `confirm_backlog` 后实施。"""

CONTROL_RUN_CARD = """### 本步规则卡：计划切包（只路由，不实施）

- **本步唯一产出**：目标 `workflow/step` + 同轮更新 `activeContext` 运行状态（含 `packet=`）+ 一行切包锚；然后**立即只打开目标步骤卡**执行。
- **禁在本步**：写/改业务代码、方案正文、任务清单正文、理解包正文、提测单正文；跑前端 capture/parity；宣称阶段完成或 `CLAIM`。
- **选路表（按开发计划 §0 当前阶段）**：
  - S0/S1：有 PRD/原型/方案原文 → `change/analyze_input`；仅口头/缺口 → `change/clarify`；已理解待基线 → `change/requirements`
  - S2 → `change/design`（只要方案则到 design/review-docs 停）
  - S3：无确认清单 → `iterate/plan`；清单待确认 → `iterate/confirm`
  - S4/S5 选链：已有确认任务清单/`iterate` 进行中 → `iterate`（implement→review→gates）；否则 → `change`（implement→review→verify）。拿不准 → 推荐 iterate + 一问
  - S6 → 同链 `deliver`（有清单走 iterate，否则 change）
  - S7：本包只收测试结论/缺陷为**可选输入**并回写计划；有测试包且要跑测 → 提示改用测试包 `testing/execute`（本会话不跨包执行）；无测试包 → 开发自验证据 + 缺口一句
  - S8 → `release` 对应当前子步；S9 → `retro/gather`
- 计划状态非「已确认/执行中」→ 回 `control/init`；有未吸收新输入 → 先 `intake/scan`；上游 HO 未签收/退回 → 先 `handoff/receive`。
- 目标步执行到下一 `hitl`/产出停点即停；回写开发计划证据后，用户说「进度」→ `control/sync`，或再说「按开发计划执行」进下一阶段。
- **不降标**：目标步的必开技能、原文回指、前端硬门、完成门全数生效；本步不代替它们。"""

WORKFLOW_CARD = """### 本步规则卡：变更与提交

- 变更/影响：先判事实与影响面；实质变更走 intake/CR，不静默改基线。
- 提交：默认仅本地提交；推送单独确认；禁 force push/切主干/擅自开 PR。
- 无文件变更 → 不硬造提交。"""

IMPLEMENT_CARD = """### 本步规则卡：实施预检与自测（本步门槛；实施类共用）

- 先勾：AC/SC/DoD 差集=0；未进 SC 且无债项 → 不开工。勾选表索引 `rules/core/iq-checklist.md`。
- **DEV-IQ-22（顺序硬）**：方案 → 分析理解 → 实施择优；理解包不抢入口；禁先看分析再找方案；漏读/砍细节 → 停工或 OPEN。**方法**见 §6 `implementation-and-selftest`。
- **预检硬门槛**：写码前命中面须先扩 SC/债项；单元=一条 SC；禁刷绿；最小改动≠裁剪 Then；验收清单写 `implement_preflight`/`sc_trace`（缺则 Claim BLOCKED）。
- **自测硬门槛**：每条 SC 有验证；未验证显式写；完成前方案盘点+分析合看+择优偏离留痕。有 UI 守本包「前端硬门」。
- 独立评审 → 本链 `review`；不在本步自称已评审。子代理索引 `rules/collaboration/subagents.md`；质量条守本步 §6 已列技能。"""

CLARIFY_CARD = """### 本步规则卡：外部输入与关账

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认后将迭代绑定文档迁入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`；主档关闭时快照、主档不移动；「并行不关」只落新资料、不归档现行主档。
- L1 单点且 `plan` 步不适用 → 进入 `implement` 前落 `{workroot}/40-tasks/开发卡-{主题}-{yyyyMMdd}.md`（模板 `rules/templates/30-planning-tasks/dev-card-lite-template.md`，含验收表/SC 表）；L0 免。
- 交接包先 `handoff.receive`；本步不 `-StartTask`。"""

WRITEBACK_CARD = """### 本步规则卡：平台回写

- 先出【回写拟稿】：单号 + 结论 + 备注全文 + 状态/指派/resolvedBuild + 附件名；用户确认后才写。
- 备注须实质（现象/根因/修复/验证），禁只写「已修复/已处理」；未验证只写「待验证」。
- 平台不支持附件 → 出 export，不假装已回写。"""


def step_card(pack_key: str, wid: str, sid: str) -> str:
    """Step-local rule card: commit/wrap all chains; key steps explicit."""
    if sid == "commit":
        return COMMIT_CARD
    if sid == "wrap":
        return WRAP_CARD
    return STEP_CARDS.get((pack_key, wid, sid), "")


def step_card_append(pack_key: str, wid: str, sid: str) -> str:
    """Append-only card: keep YAML notes as 动作清单, then add short hard gates."""
    return STEP_CARDS_APPEND.get((pack_key, wid, sid), "")


STEP_CARDS: dict[tuple[str, str, str], str] = {
    ("wf-testing", "testing", "plan"): TEST_PLAN_CARD,
    ("wf-testing", "onboard", "lifecycle"): LIFECYCLE_CARD,
    ("wf-development", "change", "plan"): PLAN_CARD,
    ("wf-development", "iterate", "plan"): PLAN_CARD,
    ("wf-development", "change", "implement"): IMPLEMENT_CARD,
    ("wf-development", "iterate", "implement"): IMPLEMENT_CARD,
    ("wf-development", "solo", "build"): IMPLEMENT_CARD,
    ("wf-development", "control", "run"): CONTROL_RUN_CARD,
    ("wf-development", "change", "clarify"): CLARIFY_CARD,
    ("wf-product", "change", "apply"): WRITEBACK_CARD,
    ("wf-product", "defect", "apply"): WRITEBACK_CARD,
    ("wf-product", "defect", "writeback"): WRITEBACK_CARD,
}

# defect-fix/fix：保留 YAML 分片/mode 动作清单，再追加实施预检卡（勿用 STEP_CARDS 整段替换）。
STEP_CARDS_APPEND: dict[tuple[str, str, str], str] = {
    ("wf-development", "defect-fix", "fix"): IMPLEMENT_CARD,
}

TEMPLATE_OVERRIDES: dict[tuple[str, str, str], str] = {
    ("wf-testing", "testing", "plan"): "rules/templates/10-planning/test-plan-template.md",
    ("wf-testing", "testing", "analyze"): "rules/templates/10-planning/test-analysis-template.md",
    ("wf-testing", "testing", "report"): "rules/templates/40-report-review/test-report-template.md",
    ("wf-testing", "testing", "review-cases"): "rules/templates/40-report-review/review-record-template.md",
    ("wf-testing", "handoff", "compose"): "rules/templates/90-handoff/handoff-note-template.md",
    ("wf-testing", "onboard", "baseline"): "rules/templates/00-onboarding/env-baseline-template.md",
    ("wf-development", "change", "requirements"): "rules/templates/10-planning/requirement-baseline-template.md",
    ("wf-development", "change", "design"): "rules/templates/20-design/solution-template.md",
    ("wf-development", "change", "plan"): "rules/templates/30-planning-tasks/task-list-template.md",
    ("wf-development", "change", "deliver"): "rules/templates/40-delivery/qa-handoff-template.md",
    ("wf-development", "iterate", "plan"): "rules/templates/30-planning-tasks/task-list-template.md",
    ("wf-development", "release", "readiness"): "rules/templates/40-delivery/go-live-checklist-template.md",
    ("wf-development", "release", "record"): "rules/templates/40-delivery/release-record-template.md",
    ("wf-development", "solo", "product"): "rules/templates/30-planning-tasks/solution-card-template.md",
    ("wf-development", "solo", "design"): "rules/templates/30-planning-tasks/solution-card-template.md",
    ("wf-product", "prd", "benchmark"): "rules/templates/10-planning/competitive-benchmark-template.md",
    ("wf-product", "deliver", "uat"): "rules/templates/40-delivery/uat-acceptance-template.md",
    ("wf-product", "deliver", "schedule"): "rules/templates/40-delivery/delivery-plan-template.md",
    ("wf-product", "handoff", "compose"): "rules/templates/90-handoff/handoff-note-template.md",
}


def load_when_table(root: Path) -> dict[str, str]:
    """Parse gates.md when tables/paragraphs into token→true-condition."""
    p = root / "rules" / "gates.md"
    out: dict[str, str] = {}
    if not p.is_file():
        return out
    text = p.read_text(encoding="utf-8")
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        token = cells[0].strip("` ")
        if not re.fullmatch(r"[a-z][a-z0-9_]+", token):
            continue
        true = cells[1].strip()
        if not true or set(true) <= {"-"} or "见下" in true:
            continue
        out.setdefault(token, true)
    for m in re.finditer(r"^`?([a-z][a-z0-9_]+)`?[：:]\s*(.+)$", text, re.M):
        token = m.group(1)
        definition = m.group(2).strip()
        if not definition:
            continue
        previous = out.get(token, "")
        if not previous or "见下" in previous or len(definition) > len(previous):
            out[token] = definition
    return out


def when_line(token: str, when_map: dict[str, str], kind: str, action: str) -> str:
    true = when_map.get(token)
    if true:
        true = re.sub(r"[。；;]\s*$", "", true)
        true = re.sub(r"\s*→\s*(真|假)[。；;]?$", "", true)
        return f"- **条件判定 `{kind}:{token}`**：{true}；满足→真，否则{action}。"
    return f"- **条件判定 `{kind}:{token}`**：词表未定义 → 按触发（真），不得跳过。"


def hitl_pairs(step: dict) -> list[tuple[str, str]]:
    raw = step.get("hitl")
    pairs: list[tuple[str, str]] = []
    default_when = str(step.get("hitl_when") or "")
    if isinstance(raw, str):
        pairs.append((raw, default_when))
    elif isinstance(raw, list):
        for item in raw:
            if isinstance(item, str):
                pairs.append((item, default_when))
            elif isinstance(item, dict) and item.get("name"):
                pairs.append((str(item["name"]), str(item.get("when") or default_when)))
    return [(n, w) for n, w in pairs if n]


def build_work_rules(
    root: Path,
    skills: list[str],
    notes: str,
    wid: str,
    sid: str,
    card: str = "",
    extra_card: str = "",
    step_conditional: dict[str, str] | None = None,
) -> str:
    """Step orchestration rules only — do NOT paste skill bodies (quality lives in skills)."""
    step_conditional = step_conditional or {}
    parts: list[str] = []
    parts.append(
        "> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。\n"
        "> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，"
        "**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。\n"
    )
    if skills:
        must = [s for s in skills if s not in CONDITIONAL_SKILLS and s not in step_conditional]
        cond = [s for s in skills if s in CONDITIONAL_SKILLS or s in step_conditional]
        if must:
            parts.append(
                "- **本步必开技能（质量不降）**："
                + "、".join(f"`{s}`" for s in must)
                + " → 见 §6 闭环。\n"
            )
        if cond:
            parts.append(
                "- **条件技能**："
                + "、".join(
                    f"`{s}`（{step_conditional.get(s) or CONDITIONAL_SKILLS[s]}）"
                    for s in cond
                )
                + " → 命中则同样走 §6 闭环。\n"
            )
    if card:
        parts.append(card)
        parts.append("")
    elif notes.strip():
        parts.append(notes_to_howto(notes, wid))
        parts.append("")
    else:
        parts.append(notes_to_howto("", wid))
        parts.append("")
    if extra_card:
        parts.append(extra_card)
        parts.append("")
    if needs_frontend_gate(root, wid, sid):
        embedded = frontend_gate_embed(root)
        if embedded:
            parts.append(embedded)
        else:
            parts.append(
                "### 前端硬门（本步含 UI）\n\n"
                "- 有 UI：按本包前端硬门执行；无 UI → 整节 `na` + 一句理由。\n"
                "- 不得只看代码/测试/API 200 代替界面证据。"
            )
    elif (root / "rules" / "core" / "frontend-gate.md").is_file():
        parts.append(
            "本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。"
        )
    return "\n".join(parts).strip()


_QUALITY_H = re.compile(r"^##\s+.*(?:现场处置|判定|反合理化|合理化与反驳)")


def _section_end(lines: list[str], start_idx: int) -> int:
    for j in range(start_idx + 1, len(lines)):
        if re.match(r"^##\s", lines[j]):
            return j - 1
    return len(lines) - 1


def skill_section_range(root: Path, name: str) -> tuple[int, int, str] | None:
    """Line window: 必做 plus 现场处置/判定/反合理化 when those headings exist.

    Line numbers are a generated window, not a reason to drop those sections.
    """
    p = root / "skills" / name / "SKILL.md"
    if not p.is_file():
        return None
    lines = p.read_text(encoding="utf-8").splitlines()
    start = None
    label = ""
    for i, line in enumerate(lines):
        if re.match(r"^##\s*0(?:\.\d+)?\s*[.、]?\s*必做", line) or re.match(
            r"^##\s*必做", line
        ):
            start = i
            label = "必做"
            break
    if start is None:
        for i, line in enumerate(lines):
            if re.match(r"^##\s*0(?:[.、\s]|$)", line) or re.match(
                r"^##\s*1(?:[.、\s])", line
            ):
                start = i
                label = "硬门槛+方法"
                break
    if start is None:
        return None
    end = _section_end(lines, start)
    if label != "必做":
        for j in range(start + 1, len(lines)):
            if re.match(r"^##\s*(?:参考|附录|变更记录|Changelog)\b", lines[j], re.I):
                end = j - 1
                break
    last_q = None
    for j in range(start + 1, len(lines)):
        if _QUALITY_H.match(lines[j]):
            last_q = j
    if last_q is not None:
        qend = _section_end(lines, last_q)
        if qend > end:
            end = qend
            label = (
                "必做+处置/判定/反合理化"
                if label == "必做"
                else "硬门槛+方法+反合理化"
            )
    while end > start and not lines[end].strip():
        end -= 1
    return start + 1, end + 1, label




def build_skill_index(
    root: Path,
    skills: list[str],
    notes: str,
    step_conditional: dict[str, str] | None = None,
) -> str:
    step_conditional = step_conditional or {}
    if not skills:
        return (
            "- 本步无技能指向；按 §5 编排执行。\n"
            "- 禁止无指向却通读 skills/「找感觉」。"
        )
    lines = [
        "> **技能闭环（硬）**：打开 → 读必做，并读现场处置/判定/反合理化（技能有这些节时）→ **回到本步骤包**继续门/产出/完成信号。  ",
        "> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。",
        "",
        "| 技能 | 级别 | 何时 | 路径 | 打开后 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for sk in skills:
        if sk in step_conditional:
            level = "条件开"
            when = step_conditional[sk]
        elif sk in CONDITIONAL_SKILLS:
            level = "条件开"
            when = CONDITIONAL_SKILLS[sk]
        else:
            level = "**必开**"
            when = "进入本步即开（质量不降）"
        rng = skill_section_range(root, sk)
        opened = "必做区 → 回本包"
        if rng:
            opened = f"只读 L{rng[0]}-L{rng[1]}（{rng[2]}）→ 回本包"
        lines.append(
            f"| `{sk}` | {level} | {when} | `skills/{sk}/SKILL.md` | {opened} |"
        )
    lines.append("")
    lines.append("- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。")
    lines.append("- 条件未命中 → 该行 `na` + 一句理由。")
    lines.append("- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。")
    return "\n".join(lines)


def render_chain_packet(
    pack_label: str,
    pack_key: str,
    wid: str,
    wf_name: str,
    steps: list[dict],
    chain_full: bool,
    wf_meta: dict | None = None,
    entry_points: dict | None = None,
) -> str:
    wf_meta = wf_meta or {}
    entry_points = entry_points or {}
    ids = [s["id"] for s in steps if isinstance(s, dict) and "id" in s]
    rows = [
        "| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for i, step in enumerate([s for s in steps if isinstance(s, dict) and "id" in s], 1):
        sid = step["id"]
        idx = ids.index(sid)
        if wid == "control" and sid == "run":
            nxt = "目标步骤卡"
        else:
            nxt = step.get("next") or (ids[idx + 1] if idx + 1 < len(ids) else "—")
        gates = [hn for hn, _ in hitl_pairs(step)]
        if step.get("gate"):
            gates.append(f"gate:{step['gate']}")
        gate_s = "、".join(f"`{g}`" for g in gates) if gates else "—"
        when_s = f"`{step['when']}`" if step.get("when") else "—"
        rows.append(
            f"| {i} | `{sid}` | `{step.get('agent') or '—'}` | {when_s} | {gate_s} | "
            f"{str(step.get('output') or '—').replace('|', '/')} | `{nxt}` | "
            f"{'停在本步/升级' if not step.get('on_fail') else str(step['on_fail']).replace('|', '/')} |"
        )
    entries = "；".join(f"`{k}` → `{v}`" for k, v in entry_points.items()) or "按 AGENTS 口令表"
    terminal = wf_meta.get("terminal") or "closeout"
    if wid == "control":
        full_note = (
            "`run` 只切包，不沿本表进入 `sync`。"
            "「按开发计划执行」关闭本包并只打开目标步骤卡；「进度」才进 `sync`。"
            "其它入口仍入口即止。"
        )
        cross_line = (
            "`control/run` 切包 = 关闭本包后只打开目标步骤卡（一次仍只一张卡）。"
            "其余跨链走重新路由或 handoff；诊断可读对方状态图。"
        )
    else:
        full_note = (
            "本链为全链入口；按表推进到下一个门/停点。"
            if chain_full
            else "默认入口即止；仅按链/继续/按计划执行时向后推进。"
        )
        cross_line = "跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。"
    track_line = (
        "- **轨道**：只接无正式迭代/正式协作（单人或团队，含大改动/高风险）；有正式协作/迭代或需正式发布/QA/交接 → 完整链；大改动/高风险按 `lightweight.md` §2 提高严谨度，不换链。\n"
        if wid == "solo" else ""
    )
    return f"""# {wf_name} · `{wid}` 状态机

> 全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：{entries}
- **终端**：`{terminal}`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；本图进链读一次；每步先读当前 packet。

## 2. 状态表

{chr(10).join(rows)}

## 3. 推进

- {full_note}
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `skip=理由`。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/{wid}.yaml` + 本图 + `rules/packets/{wid}/`；改本链只重生成该链。
{track_line}- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- {cross_line}

## 5. 终端

- 所有 domain 状态结束后进入 `{terminal}`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
"""



def frontend_gate_embed(root: Path) -> str | None:
    p = root / "rules" / "core" / "frontend-gate.md"
    if not p.is_file():
        return None
    text = p.read_text(encoding="utf-8")
    parts: list[str] = []
    # Titles may carry suffixes like 「（缺一=…）」/「（RUN）」— match by prefix.
    for title in ("## 1. 何时触发", "## 2. 必产物", "## 3. 必命令", "## 4. 验收底线", "## 5. 禁做"):
        m = re.search(
            rf"({re.escape(title)}[^\n]*\n.*?)(?=\n## |\Z)",
            text,
            re.S,
        )
        if m:
            parts.append(m.group(1).strip())
    if len(parts) < 5:
        # Fail loud in build log; incomplete embed is worse than missing.
        print(
            f"WARN frontend-gate embed incomplete: got {len(parts)}/5 sections from {p}",
            file=sys.stderr,
        )
    if not parts:
        return None
    body = neutralize_pointers("\n\n".join(parts), None)
    # 内嵌节不能与步骤包自己的 §1～§9 抢编号：降级并加“前端门”前缀。
    body = re.sub(
        r"^(#{2,3})\s+([0-9]+(?:\.[0-9]+)*)\.?\s*(.*)$",
        lambda m: ("###" if m.group(1) == "##" else "####")
        + f" 前端门 {m.group(2)}. {m.group(3)}",
        body,
        flags=re.M,
    )
    return (
        "### 前端硬门（本步内嵌 · 有 UI 必遵；无 UI 整节 `na`）\n\n"
        + "> 本节编号仅指前端门内部；引用写「前端门 §X」。\n\n"
        + body
        + "\n\n> L0 无 UI：整节标 `na` + 一句理由，勿机械跑 capture。"
    )


# 只有真正改界面或验收界面的步才嵌入全文。关键词（原型/页面）会把整门挂进写文档的步。
UI_GATE_STEPS = {
    ("change", "implement"),
    ("change", "review"),
    ("change", "verify"),
    ("iterate", "implement"),
    ("iterate", "review"),
    ("iterate", "gates"),
    ("solo", "build"),
    ("solo", "test"),
    ("defect-fix", "fix"),
    ("defect-fix", "gates"),
    ("release", "verify"),
}


def needs_frontend_gate(root: Path, wid: str, sid: str) -> bool:
    if not (root / "rules" / "core" / "frontend-gate.md").is_file():
        return False
    return (wid, sid) in UI_GATE_STEPS


def region_advance_line(pack_key: str) -> str:
    if pack_key == "wf-development":
        return "本区按表向后推进；单步口令在本步完成即停；`when` 不满足则不打开该步包。"
    return (
        "默认入口步完成即停，不因本表自动进入下一步。"
        "仅按链、继续、按计划执行，或全链入口，才按表走向下一项。"
        "`when` 不满足则不打开该步包。"
    )


def advance_prose(pack_key: str, wid: str, chain_full: bool) -> str:
    """Runtime stop/go. Matches each package AGENTS; no new stop rule beyond AGENTS."""
    route = "口令只认本包 AGENTS 口令表。本链只排步骤与 `when`，不另列口令。"
    if pack_key == "wf-development":
        parts = [
            route,
            "从已命中的入口步沿阶段表向后；`when` 不满足则跳过且不打开该包。",
            "口令明确只做单步（只出方案/只出轻量方案/只评审/代码评审/方案评审/只提测/只出清单）时，本步完成即停并输出收尾骨架；其余按表向后。",
            "本步动作清单写明跳过、停止或改走他步时，以清单为准。",
        ]
        if chain_full and wid == "onboard":
            parts.append(
                "全链入口仅：接入/重新接入/基线/装配能力，走到 verify 打标；"
                "资料与文档治理只做该步加收尾，不连带其余接入步。"
            )
        elif chain_full:
            parts.append(
                "因此本流程不走默认即停：从入口步沿阶段表走到链末；`when` 不满足则跳过且不打开该包。"
            )
        return " ".join(parts)
    parts = [
        route,
        "默认：入口步的产出与本步门完成后即停，并输出收尾骨架；不打开后续步骤包。",
        "向后走，仅当口令是按链、继续、按计划执行，或本流程处于全链入口。",
    ]
    if chain_full and wid == "onboard":
        if pack_key == "wf-testing":
            parts.append(
                "全链入口仅：接入、重新接入、基线、装配能力，走到 verify 打标。"
                "资料与文档治理只做该步加收尾，不连带其余接入步。"
            )
        else:
            parts.append(
                "全链入口仅：接入、重新接入、生成档案、装配能力，走到 verify 打标。"
                "资料与文档治理只做该步加收尾，不连带其余接入步。"
            )
    elif chain_full:
        parts.append(
            "因此本流程不走默认即停：从入口步沿阶段表走到链末；`when` 不满足则跳过且不打开该包。"
        )
    if pack_key == "wf-testing" and wid == "testing":
        parts.append("report：报告门通过后只追加一次提交或交平台确认，不回到 execute。")
    return " ".join(parts)


def packet_advance(pack_key: str, wid: str, sid: str) -> str:
    if pack_key == "wf-development" and wid == "control" and sid == "run":
        return (
            "- **推进**：本步只完成切包；**不**沿 control 自动进入 `sync`。"
            "同轮更新 `activeContext` 后关闭本包，只打开目标步骤卡；"
            "目标步到下一 `hitl`/产出停点即停；之后用户说「进度」→ `sync`，或再说「按开发计划执行」进下一阶段。"
        )
    if wid in ("materials", "skill-audit"):
        return (
            "- **推进**：本流程为 `chain: full`；本步完成后进入下一未跳过步，直至 closeout。"
        )
    extra = ""
    if pack_key == "wf-testing" and wid == "testing" and sid == "report":
        extra = " 报告门通过后只追加一次提交或交平台确认，不回到 execute。"
    return (
        "- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。"
        "仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。"
        + extra
    )


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
    """Drop stale file§N anchors and repair residue left by earlier passes."""
    if not notes:
        return notes
    # foo.md §1.2 / foo.yaml §0 → foo.md / foo.yaml
    notes = re.sub(
        r"(`?[A-Za-z0-9_./\\-]+\.(?:md|yaml|yml|ps1|py)`?)\s*§[\d]+(?:\.[\d]+)*",
        r"\1",
        notes,
    )
    # residue after anchor removal: "test-plan //" / "计划 //////、"
    notes = re.sub(r"(?<=[\u4e00-\u9fffA-Za-z0-9_`])\s*/{2,}(?=[\s，。；、]|$)", "", notes)
    notes = re.sub(r"(?<=[\u4e00-\u9fffA-Za-z0-9_`])\s*/(?=[\s，。；、]|$)", "", notes)
    # dangling arrow left by deleted section name
    notes = notes.replace("→。", "→ 停并说明缺口。")
    notes = re.sub(r"→\s*([；，])", r"→ 停并说明缺口\1", notes)
    notes = re.sub(r"\s+([、，。；：])", r"\1", notes)
    notes = re.sub(r"[ \t]{2,}", " ", notes)
    return notes.strip()


def load_agent_meta(root: Path, agent_id: str | None) -> tuple[str, str]:
    """Return (role, goal-one-line) from agents/<id>.yaml for packet identity."""
    if not agent_id:
        return ("", "")
    path = root / "agents" / f"{agent_id}.yaml"
    if not path.is_file():
        return ("", "")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return ("", "")
    if not isinstance(data, dict):
        return ("", "")
    role = str(data.get("role") or "").strip()
    goal = str(data.get("goal") or "").strip()
    if len(goal) > 80:
        cut = max(goal.rfind("；", 0, 80), goal.rfind("。", 0, 80), goal.rfind("→", 0, 80))
        goal = goal[: cut + 1].rstrip("→；。 ") if cut >= 30 else ""
    return (role, goal)


def step_edges(steps: list, step: dict) -> dict:
    """Resolve upstream / downstream / failure edge for the current step."""
    ids = [s["id"] for s in steps if isinstance(s, dict) and "id" in s]
    sid = step.get("id")
    if sid not in ids:
        return {}
    i = ids.index(sid)
    prev_id = ids[i - 1] if i > 0 else None
    explicit = step.get("next")
    next_id = explicit if isinstance(explicit, str) and explicit else (
        ids[i + 1] if i + 1 < len(ids) else None
    )
    nxt = next((s for s in steps if isinstance(s, dict) and s.get("id") == next_id), {})
    return {
        "prev": prev_id,
        "next": next_id,
        "next_when": nxt.get("when"),
        "terminal": not next_id,
        "on_fail": step.get("on_fail"),
    }


def notes_to_howto(notes: str, current_wid: str | None = None) -> str:
    notes = neutralize_pointers(notes.strip(), current_wid)
    if not notes:
        return "按 §2 产出落盘；结果须可验证；有门则先过门。"
    # Split on 。；; outside （）/() and backticks so paren lists stay intact.
    parts: list[str] = []
    buf: list[str] = []
    depth = 0
    in_bt = False
    for c in notes:
        if c == "`":
            in_bt = not in_bt
            buf.append(c)
            continue
        if not in_bt and c in "（(":
            depth += 1
            buf.append(c)
            continue
        if not in_bt and c in "）)":
            depth = max(0, depth - 1)
            buf.append(c)
            continue
        if not in_bt and depth == 0 and c in "。；;":
            chunk = "".join(buf).strip().strip("。")
            if chunk:
                parts.append(chunk)
            buf = []
            continue
        buf.append(c)
    tail = "".join(buf).strip().strip("。")
    if tail:
        parts.append(tail)
    bullets = [f"- {p}。" for p in parts if p]
    if len(bullets) <= 1 and len(notes) > 180:
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
    full_notes: str,
    edges: dict | None = None,
    agent_meta: tuple[str, str] = ("", ""),
    when_map: dict[str, str] | None = None,
    templates: list[str] | None = None,
) -> str:
    sid = step["id"]
    when_map = when_map or {}
    templates = templates or ([template] if template else [])
    name = step.get("name") or sid
    output = step.get("output") or "（见本步产出约定）"
    when = step.get("when")
    notes = full_notes.strip() if isinstance(full_notes, str) else str(full_notes or "")
    agent_id = str(step.get("agent") or "")
    role, role_goal = agent_meta
    edges = edges or {}
    prev_id = edges.get("prev")
    next_id = edges.get("next")
    next_when = edges.get("next_when")
    on_fail = edges.get("on_fail")
    terminal = bool(edges.get("terminal"))

    identity = ""
    if agent_id:
        # materials/handoff/skill-audit 复用主轨 agent：不粘贴主轨 role/goal
        if wid in ("materials", "handoff", "skill-audit"):
            role_txt = ""
            goal_txt = "按本步目标与 §5 动作执行；"
        else:
            role_txt = f"（{role}）" if role else ""
            goal_txt = f"{role_goal.rstrip('。；')}；" if role_goal else ""
        identity += f"- **角色**：`{agent_id}`{role_txt}。{goal_txt}本步只做该角色职责；越界交回或升级。\n"
    precondition = step.get("precondition")
    if isinstance(precondition, str) and precondition.strip():
        identity += f"- **前置**：{precondition.strip()}\n"
    identity += (
        f"- **上游**：`{prev_id}`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）\n"
        if prev_id else "- **上游**：无（链首）\n"
    )
    if pack_key == "wf-development" and wid == "control" and sid == "run":
        identity += "- **后续**：目标步骤卡（不自动打开 `sync`；「进度」才回 `sync`）\n"
    elif terminal:
        identity += "- **后续**：链末出口（完成本步即收尾，不再打开节点）\n"
    else:
        cond = f"（进 `{next_id}` 前的 `when={next_when}`）" if next_when else ""
        identity += f"- **后续**：`{next_id}`{cond}\n"
    identity += (
        f"- **失败去向**：{on_fail}\n" if on_fail
        else "- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。\n"
    )

    risk = ""
    if when:
        risk += when_line(str(when), when_map, "when", "跳过本步（不打开本包）") + "\n"
    if (root / "rules" / "core" / "frontend-gate.md").is_file():
        risk += (
            "- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；"
            "**必开技能与 Claim/HITL 不降**。\n"
        )
    else:
        risk += (
            "- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；"
            "**必开技能与 Claim/HITL 不降**。\n"
        )

    if pack_key == "wf-development" and wid == "control" and sid == "run":
        boundary = (
            "- 选路完成前只读本包 + §6 技能。\n"
            "- 选路后同轮关闭本包，只打开目标步骤卡；目标卡的技能、门、原文回指取代本包。\n"
            "- 禁止把目标卡规则抄进本包，禁止在本包内实施。"
        )
    else:
        boundary = (
            "- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。\n"
            "- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。\n"
            "- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。"
        )
    hard = (
        "> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。\n"
        "\n### 本步边界\n\n"
        f"{boundary}"
    )

    gate_lines: list[str] = []
    for hn, hw in hitl_pairs(step):
        desc = neutralize_pointers(gates.get(hn) or "出示确认块后等待用户。", wid)
        gate_lines.append(f"- **HITL `{hn}`**：{desc}")
        if hw:
            gate_lines.append(when_line(str(hw), when_map, "hitl", "跳过该门"))
    gate = step.get("gate")
    if gate:
        gw = step.get("gate_when")
        desc = gates.get(f"gate: {gate}") or gates.get(str(gate)) or "运行对应 verify；未过不得宣称完成。"
        desc = neutralize_pointers(desc, wid)
        gate_lines.append(
            f"- **GATE `{gate}`"
            + (f" when={gw}" if gw else "")
            + f"**：{desc}"
        )
        if gw:
            gate_lines.append(when_line(str(gw), when_map, "gate", "跳过该闸（步骤不跳过）"))
    if not gate_lines:
        gate_lines.append("- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。")
    gate_lines.append(packet_advance(pack_key, wid, sid))

    card = step_card(pack_key, wid, sid)
    gate_text = " ".join(gates.get(hn) or "" for hn, _ in hitl_pairs(step))
    extras: list[str] = []
    if not card:
        if "doc-governance" in notes or "doc-governance" in gate_text:
            extras.append(DOC_GOV_CARD)
        if "workflow.md" in notes or "workflow.md" in gate_text:
            extras.append(WORKFLOW_CARD)
        if "implementation-quality" in notes and not any("实施预检" in e for e in extras):
            extras.append(IMPLEMENT_CARD)
    extra_card = "\n\n".join(extras)
    if pack_key == "wf-development" and wid == "solo" and sid == "build":
        extra_card = (
            extra_card
            + "\n\n### 测试输入\n- 读本轮 `测试分析与计划-{主题}-{yyyyMMdd}.md`；按 P0/P1/P2 与覆盖矩阵实施/自测。"
        ).strip()
    step_conditional = STEP_CONDITIONAL_SKILLS.get((pack_key, wid, sid), {})
    work = build_work_rules(
        root,
        skills,
        notes,
        wid,
        sid,
        card=card,
        extra_card=extra_card,
        step_conditional=step_conditional,
    )
    skill_idx = build_skill_index(root, skills, notes, step_conditional)

    open_lines: list[str] = []
    uniq_tpl = list(dict.fromkeys(t for t in templates if t))
    primary_tpl = template if template in uniq_tpl else (uniq_tpl[0] if uniq_tpl else None)
    others = [t for t in uniq_tpl if t != primary_tpl]
    if primary_tpl:
        open_lines.append(
            f"- **填写模板（仅此一份）**：`{primary_tpl}`；只读本步用到的节，禁止整文件通读。"
        )
    if others:
        open_lines.append(
            "- **参考模板（命中再开，不默认读）**：`" + "`；`".join(others) + "`。"
        )
    if not uniq_tpl:
        if (pack_key, wid, sid) == ("wf-development", "change", "clarify"):
            open_lines.append(
                "- **模板**：L1 单点且 `plan` 步不适用 → 用 `rules/templates/30-planning-tasks/dev-card-lite-template.md`；L0 免；其它无强制模板。"
            )
        elif card or extra_card:
            open_lines.append(
                "- **无强制模板**：§5 规则卡已给出输出形状；直接落 §2 产出。"
            )
        else:
            open_lines.append(
                "- **无强制模板**：§5 编排已给出动作/顺序；直接落 §2 产出。"
            )
    if gate or ("Claim" in notes or "Invoke-Gate" in notes):
        _need_claim = step_requires_claim(pack_key, gate if isinstance(gate, str) else None, notes)
        verify_line = (
            "- 验证命令：`verify/Invoke-Gate.ps1`（完成须 `-Claim` → `CLAIM: ALLOWED`）"
            if _need_claim
            else "- 验证命令：`verify/Invoke-Gate.ps1`（本步非完成 Claim；按 Mode 出回执即可）"
        )
        if needs_frontend_gate(root, wid, sid):
            verify_line += "；有 UI 遵 §5 前端硬门（已内嵌）"
        open_lines.append(verify_line + "。")

    rel = f"rules/packets/{wid}/{sid}.md"
    skill_names = ",".join(skills) if skills else "na"
    done_line = (
        "- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。"
        if skills
        else "- §2 产出已落盘；本步无 §6 技能指向。"
    )
    requires_claim = step_requires_claim(pack_key, gate if isinstance(gate, str) else None, notes)
    claim_line = (
        "- 本步完成 Claim 门：须 `CLAIM: ALLOWED` 后才可写完成态。"
        if requires_claim
        else "- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。"
    )
    banner = (
        "选路前只读本包；选路后关闭本包，只打开目标步骤卡。"
        if pack_key == "wf-development" and wid == "control" and sid == "run"
        else "不读他步 packet / 大手册。"
    )
    return f"""# 步骤卡 · {wid}/{sid}

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。{banner}

## 1. 元信息

- **workflow / step**：`{wid}` / `{sid}`（{name}）
- **packet**：`{rel}`
{identity}{risk}
## 2. 本步目标

- **目标**：{name}
- **产出**：{output}

## 3. 本步硬约束（全局规则 + 本步边界）

{hard}

## 4. 本步门

{chr(10).join(gate_lines)}

## 5. 本步动作

{work}

## 6. 技能指向（打开 → 执行 → 回包）

{skill_idx}

## 7. 模板与证据

{chr(10).join(open_lines) if open_lines else "- 无强制模板；按 §2 产出直接落盘。"}

## 8. 完成与退出

{done_line}
- 本步 hitl 已确认，或 when 条件跳过。
{claim_line}
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:{wid} | step={sid} | agent={agent_id or "na"} | packet={rel} | global=ok | skills={skill_names}|done|na | claim=ALLOWED|DENIED|na | next=…
```
"""


def process_package(root: Path, pack_label: str, only: set[str] | None = None) -> None:
    gates = load_gates_table(root)
    when_map = load_when_table(root)
    skill_dirs = list_skill_dirs(root)
    readme_rows = parse_readme_skill_rows(root)
    pack_key = root.name
    wf_dir = root / "workflows"
    for ypath in sorted(wf_dir.glob("*.yaml")):
        if only and ypath.stem not in only:
            continue
        raw = ypath.read_text(encoding="utf-8")
        data = yaml.safe_load(raw)
        if not isinstance(data, dict) or "workflow" not in data:
            print(f"skip {ypath.name}")
            continue
        if isinstance(data.get("workflow"), dict):
            data["workflow"].pop("read_index", None)
        wid = data["workflow"].get("id") or ypath.stem
        wf_name = data["workflow"].get("name") or wid
        steps = data.get("steps") or []
        # Parent state machine + nested region machines
        chain_path = root / f"workflows/{wid}.md"
        chain_path.parent.mkdir(parents=True, exist_ok=True)
        wf_meta = data.get("workflow") if isinstance(data.get("workflow"), dict) else {}
        chain_full = str((wf_meta or {}).get("chain") or "") == "full"
        chain_body = render_chain_packet(
            pack_label, pack_key, wid, wf_name, steps, chain_full,
            wf_meta=wf_meta, entry_points=data.get("entry_points") or {},
        )
        tmp_c = chain_path
        emit(tmp_c, chain_body)

        steps_by_id = {
            s["id"]: s for s in steps if isinstance(s, dict) and "id" in s
        }
        n = 0
        indexed = 0
        for step in steps:
            if not isinstance(step, dict) or "id" not in step:
                continue
            sid = step["id"]
            full_notes = step.get("notes") or ""
            if not isinstance(full_notes, str):
                full_notes = str(full_notes)
            full_notes = sanitize_notes_for_yaml(full_notes)
            # Resolve skills from rich YAML notes.
            step_for_skills = dict(step)
            step_for_skills["notes"] = full_notes
            skills = resolve_skills_for_step(
                root, pack_key, wid, sid, step_for_skills, skill_dirs, readme_rows
            )
            # template from full notes before thinning yaml
            step_for_tpl = dict(step)
            step_for_tpl["notes"] = full_notes
            template = TEMPLATE_OVERRIDES.get((pack_key, wid, sid)) or extract_template(
                step_for_tpl, root
            )
            # commit/wrap 的正文已由 §5 规则卡内联；不再把 8KB/29KB 模板作为必读跳转。
            if sid in ("commit", "wrap"):
                template = None
                templates: list[str] = []
            else:
                templates = list(
                    dict.fromkeys(
                        ([template] if template else [])
                        + re.findall(r"rules/templates/[^\s`，。；]+?\.md", full_notes)
                    )
                )
            # Primary template: §2 output path wins; else explicit/notes first.
            out_tpl = re.findall(
                r"rules/templates/[^\s`，。；]+?\.md", str(step.get("output") or "")
            )
            primary = (
                out_tpl[0]
                if out_tpl
                else (template if template in templates else (templates[0] if templates else None))
            )
            if primary and primary not in templates:
                templates.insert(0, primary)
            packet_rel = f"rules/packets/{wid}/{sid}.md"
            if sid == "closeout":
                step["must_read"] = ["rules/packets/_shared/closeout.md"]
                step["notes"] = "收尾与提交；共享终端；状态=done。"
                n += 1
                continue
            packet_path = root / packet_rel
            packet_path.parent.mkdir(parents=True, exist_ok=True)
            body = render_packet(
                root,
                pack_label,
                pack_key,
                wid,
                step,
                gates,
                skills,
                primary,
                full_notes,
                edges=step_edges(steps, step),
                agent_meta=load_agent_meta(root, step.get("agent")),
                when_map=when_map,
                templates=templates,
            )
            body = re.sub(
                r"`(rules/templates/[^`]+?[、,][^`]+?)`",
                lambda m: " / ".join(f"`{p}`" for p in _split_path_blob(m.group(1)))
                or m.group(0),
                body,
            )
            emit(packet_path, body)
            new_mr = [packet_rel]
            if primary and primary not in new_mr:
                new_mr.append(primary)
            step["must_read"] = new_mr
            step.pop("skills", None)
            # YAML carries the rich note; no separate cache.
            step["notes"] = full_notes if full_notes else "按本步目标与产出执行。"
            n += 1
            if skills:
                indexed += 1
        header = (
            f"# 编排：进 wf → workflows/{wid}.md；执行 → 当前 step 步骤包；终端 → _shared/closeout.md。\n"
            f"# 步骤卡 §6 必开技能：打开→执行→回包。禁把 skill 正文嵌进步骤卡。\n"
            f"# 本 YAML 只定义状态/门/产出；不用于运行时通读。\n"
        )
        dumped = yaml.dump(
            data,
            Dumper=_Dumper,
            allow_unicode=True,
            sort_keys=False,
            width=120,
        )
        emit(ypath, header + dumped)
        print(f"OK {pack_label}/{wid}: {n} steps, {indexed} skill-linked, terminal=closeout")


def main() -> int:
    global CHECK
    if len(sys.argv) < 2:
        print("Usage: build_step_packets.py <package-root> [label] [--only wf1,wf2] [--check]", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    label = root.name
    only: set[str] | None = None
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--check":
            CHECK = True
        elif arg == "--only" and i + 1 < len(args):
            only = {x.strip() for x in args[i + 1].split(",") if x.strip()}
            i += 2
            continue
        elif arg.startswith("--only="):
            only = {x.strip() for x in arg.split("=", 1)[1].split(",") if x.strip()}
        elif not arg.startswith("--"):
            label = arg
        i += 1
    process_package(root, label, only)
    if CHECK:
        if DRIFT:
            print(f"PACKETS_STALE: {len(DRIFT)} 处生成物与 workflows 源不一致")
            for d in DRIFT[:40]:
                print("  " + d)
            print("修：python rules/tools/build_step_packets.py <包根> 后重跑自检。")
            return 1
        print("PACKETS_UP_TO_DATE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
