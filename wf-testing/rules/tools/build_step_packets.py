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

# --check：只渲染不落盘，用于检测「生成物 vs 源（workflows/*.yaml + _orch.yaml）」漂移。
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


# 外部规则 → 自足短句。只替换「外围规则」；核心步骤规则由 STEP_CARDS 内联。
INLINE_RULES = (
    (
        r"`?rules/core/clarification\.md`?(?:\s*§[\d.]+)?",
        "澄清：先查事实；仍不明一次一问（附候选/推荐）；未确认不升格",
    ),
    (
        r"`?(?:rules/core/)?iq-checklist\.md`?",
        "实施预检：先勾 AC/SC/DoD；未进 SC 且无债项不开工；命中面先扩 SC",
    ),
    (
        r"(?:子代理按\s*)?`?rules/collaboration/subagents\.md`?(?:\s*§[\d.]+)?",
        "子代理：只读派发摘录与本批节；同一文件不重读；写域隔离；主代理核产物",
    ),
    (
        r"`?rules/collaboration/handoff\.md`?(?:\s*§[\d.]+)?",
        "交接：内容优先、包按需；未回执不得称已接收",
    ),
    (
        r"`?rules/doc-governance\.md`?(?:\s*§[\d.]+)?",
        "本包 §5 文档治理规则",
    ),
    (
        r"`?rules/workflow\.md`?(?:\s*§[\d.]+)?",
        "提交：默认仅本地提交；推送单独确认；禁 force push/切主干",
    ),
    (
        r"`?rules/core/verification\.md`?(?:\s*§[\d.]+)?",
        "完成：只认 CLAIM: ALLOWED；状态 COMPLETE/PARTIAL/BLOCKED/NOT_VERIFIED",
    ),
    (
        r"`?rules/core/lightweight\.md`?(?:\s*§[\d.]+)?",
        "轻量：纯文档可裁剪；必开技能/Claim/HITL 不降",
    ),
    (r"`?rules/core/project-readme\.md`?", "README：只写现行入口/运行/目录"),
    (r"`?rules/core/context-memory\.md`?", "工作记忆：偏好/洞见/坑 ≤3 行"),
    (
        r"`?rules/playbooks/skill-audit\.md`?",
        "技能体检：盘点→适配→拟变更→确认→复检",
    ),
    (
        r"`?rules/defects/[^`\s]+\.md`?(?:\s*§[\d.]+)?",
        "缺陷：先红证/根因；不修表象；回写带证据",
    ),
    (r"`?rules/gates\.md`?(?:\s*§[\d.]+)?", "门：见本包 §4"),
    (r"`?rules/read-index\.md`?", "禁止 read-index"),
)


def expand_inline_rules(text: str) -> str:
    """Replace peripheral rule refs with a self-contained sentence (no doc hop)."""
    for pattern, replacement in INLINE_RULES:
        text = re.sub(pattern, replacement, text)
    return text


def neutralize_pointers(text: str) -> str:
    """Inline peripheral rules; keep templates/skills as first-class packet sections."""
    text = expand_inline_rules(text)
    text = re.sub(r"遵守\s*`frontend-gate`", "遵守本包「前端硬门」节（有 UI）", text)
    text = re.sub(r"`?rules/core/frontend-gate\.md`?", "本包前端硬门", text)
    text = re.sub(r"`frontend-gate`", "本包前端硬门", text)
    text = re.sub(r"`?frontend-gate\.md`?", "本包前端硬门", text)
    text = re.sub(
        r"`?rules/core/implementation-quality\.md`?(?:\s*§[\d.]+)?",
        "本包 §5 实施预检卡",
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
        "本包 §5 实施预检卡",
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
    text = re.sub(r"`rule-anchor\.md`", "规则心跳一行格式", text)
    text = re.sub(
        r"`rules/capabilities/instance-discipline\.md`\s*§[\d.]+",
        "实例纪律（按需拉起、结束显式退程）",
        text,
    )
    # Skills → §6（本包技能表）；模板保留真实路径，由 §7 列出。
    text = re.sub(r"`skills/([a-z0-9-]+)/SKILL\.md`", r"§6 `\1`", text)
    text = re.sub(r"`skills/README\.md`", "技能体检：盘点→适配→拟变更→确认→复检", text)
    text = re.sub(r"`workflows/[^`]+`", "本 workflow", text)
    text = re.sub(r"技能[：:]\s*§6", "技能见 §6", text)
    text = re.sub(r"技能[：:]\s+(?!§6)", "技能见 §6：", text)
    return text


def is_thin_notes(notes: str) -> bool:
    n = (notes or "").strip()
    return (not n) or n.startswith("只读 must_read")


def load_orch(root: Path, wid: str) -> dict[str, str]:
    p = root / f"rules/packets/{wid}/_orch.yaml"
    if not p.is_file():
        return {}
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    steps = data.get("steps") if isinstance(data, dict) else None
    if not isinstance(steps, dict):
        return {}
    out: dict[str, str] = {}
    for k, v in steps.items():
        if isinstance(v, str) and v.strip() and not is_thin_notes(v):
            out[str(k)] = v.strip()
    return out


def save_orch(root: Path, wid: str, steps: dict[str, str]) -> None:
    path = root / f"rules/packets/{wid}/_orch.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "workflow": wid,
        "purpose": "编排笔记缓存：生成步骤包 §5 的真源；YAML notes 保持薄指针。勿手改 packet 后丢此文件。",
        "steps": {k: steps[k] for k in sorted(steps.keys())},
    }
    dumped = yaml.dump(
        payload,
        Dumper=_Dumper,
        allow_unicode=True,
        sort_keys=False,
        width=120,
    )
    header = (
        f"# orch · {wid} — packet rebuild source (not runtime must_read)\n"
        "# YAML step.notes may be thin; rich orchestration lives here.\n"
    )
    emit(path, header + dumped)


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
【遵守自检】route=… | mode=… | packet=… | skills=… | reads=… | gates=… | confirm=… | sync=…（triad=…；facade=…） | skip=… | deviation=…
附：运行与沉淀 · 资料补强：… | 工作记忆：… | 运行态：…
```

- 有门回执时跑 `verify/Test-Report.ps1 -Report <收尾文件>`；无门用 `python verify/tools/report_lint.py --format-only --report <收尾文件>`（有该工具时）。
- 同步 plan/INDEX/activeContext（triad）；完整【拟提交】留待 commit。"""

TEST_PLAN_CARD = """### 本步规则卡：计划模板与必填节

- 模板（完整路径）：`rules/templates/10-planning/test-plan-template.md`；只读 §0 + 本轮待填节（§3.7 执行矩阵 / §3.8 四卷 / §3.9 批次表 / §5 准出 / §9 编排），**不要整文件通读**。
- 轻量路径：`rules/templates/10-planning/test-plan-lite-template.md` §3/§8；仅补丁/单模块且不承担版本准出才用。
- 前置：先有测试分析表；无表 → 先 analyze，不写计划。
- 版本级：四卷 V1～V4 + 批次表；计划门核分析表 §2.2/§2.3/§2.4 无空格、§3.8 四卷、§3.9 批次表。
- 模板按路径选，不按 T 标签；不适用写 N/A + 依据。
- 迭代关账：确认结束当前迭代后，主计划/四卷/报告/CR/交接落 `{workroot}/_archive/`；「并行不关」只落新资料。"""

LIFECYCLE_CARD = """### 本步规则卡：文档治理扫描

- 分类：长期/固定 → 就地更新；版本/迭代绑定 → 关闭时快照/归档；失效/替代 → 确认后归档；过程/临时（含已完结 .draft/）→ 清理候选。
- 归档前引用检查：被当前计划/用例/脚本/报告引用的输入/数据/冒烟清单保留原位或标「基线」。
- 确认前不改/不移/不删；有候选 → `docs_migration_needed=true`，停门等确认。
- 关账：主计划/四卷/报告/CR/交接落 `{workroot}/_archive/`；清理只删已知临时/缓存/未引用失败产物。
- 失效资料在 `inbound/INDEX.md` 状态列标记；不确定移 `{workroot}/_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。"""

DOC_GOV_CARD = """### 本步规则卡：文档治理

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认结束当前迭代后，主计划/四卷/报告/CR/交接落 `{workroot}/_archive/`；「并行不关」只落新资料，不归档现行主档。
- 清理只删已知临时/缓存/未引用失败产物；不确定移 `_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。"""

IMPLEMENT_CARD = """### 本步规则卡：实施预检与自测

- 先勾：AC/SC/DoD 差集=0；未进 SC 且无债项 → 不开工。
- 实施预检（写代码前）：权限/状态/数据基数/多表面/失败路径/交互诚实/运行时 API 逐面判定；命中 → 先扩 SC/债项，再改码。有 UI 且含禁用/灰显/空列表/加载/筛选/主按钮 → 交互诚实默认命中；多表面同一状态/KPI → 跨层默认命中。
- 单元=一条 SC；先红后绿；禁改断言/跳测试/关告警刷绿；最小改动≠裁剪 Then。
- 自测：每条 SC 至少一条验证；边界/错误/权限/重复/并发按命中补；未验证显式写「未验证」。
- 子代理：只读派发摘录与本批节；同一文件不重读；写域隔离；主代理核产物，不采信自述。"""

CLARIFY_CARD = """### 本步规则卡：外部输入与关账

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认结束当前迭代后，主计划/四卷/报告/CR/交接落 `{workroot}/_archive/`；「并行不关」只落新资料，不归档现行主档。
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


STEP_CARDS: dict[tuple[str, str, str], str] = {
    ("wf-testing", "testing", "plan"): TEST_PLAN_CARD,
    ("wf-testing", "onboard", "lifecycle"): LIFECYCLE_CARD,
    ("wf-development", "change", "implement"): IMPLEMENT_CARD,
    ("wf-development", "iterate", "implement"): IMPLEMENT_CARD,
    ("wf-development", "solo", "build"): IMPLEMENT_CARD,
    ("wf-development", "change", "clarify"): CLARIFY_CARD,
    ("wf-product", "change", "apply"): WRITEBACK_CARD,
    ("wf-product", "defect", "apply"): WRITEBACK_CARD,
    ("wf-product", "defect", "writeback"): WRITEBACK_CARD,
}

TEMPLATE_OVERRIDES: dict[tuple[str, str, str], str] = {
    ("wf-testing", "testing", "plan"): "rules/templates/10-planning/test-plan-template.md",
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


# Nested state-machine regions for long workflows (id, title, step_ids)
REGIONS: dict[str, dict[str, list[tuple[str, str, list[str]]]]] = {
    "wf-development": {
        "change": [
            ("align", "对齐与基线", ["clarify", "analyze_input", "requirements"]),
            ("design", "方案与计划", ["design", "review-docs", "plan"]),
            ("build", "实施与验证", ["implement", "review", "verify"]),
            ("ship", "交付收尾", ["deliver", "release_handoff", "wrap", "commit"]),
        ],
        "defect-fix": [
            ("intake", "接入与分类", ["preflight", "pull", "triage"]),
            (
                "product",
                "产品协作闭环",
                [
                    "assess_product",
                    "handoff_product",
                    "await_product",
                    "product_decision",
                    "align",
                ],
            ),
            ("fix", "修复与门禁", ["clarify", "fix", "gates", "menu"]),
            ("close", "关闭与收尾", ["close", "postrelease", "retro", "wrap"]),
        ],
        "iterate": [
            ("plan", "计划确认", ["precheck", "plan", "confirm"]),
            ("build", "实施验证", ["implement", "review", "gates"]),
            ("ship", "交付收尾", ["deliver", "release_handoff", "retro", "wrap", "commit"]),
        ],
        "release": [
            ("ready", "就绪与批准", ["acceptance", "readiness", "approval"]),
            ("go", "部署验证", ["deploy", "verify", "rollback"]),
            ("after", "事后收尾", ["postrelease", "record", "retro", "wrap", "commit"]),
        ],
        "control": [
            ("steer", "总控推进", ["init", "run", "sync", "check", "next"]),
            ("close", "收尾", ["wrap", "commit"]),
        ],
        "solo": [
            ("frame", "定义与方案", ["frame", "plan"]),
            ("build", "建造验证", ["build", "test"]),
            ("close", "收尾", ["wrap", "commit"]),
        ],
    },
    "wf-product": {
        "prd": [
            ("discover", "发现与优先级", ["discover", "benchmark", "prioritize"]),
            ("write", "撰写交接", ["prd", "prototype", "review", "handoff"]),
            ("close", "收尾", ["wrap", "commit"]),
        ],
        "prototype": [
            ("shape", "结构与线框", ["context", "ia", "wireframe", "engineering"]),
            ("visual", "视觉与评审", ["visual", "hi-fi", "review", "usability"]),
            ("hand", "交接收尾", ["handoff", "wrap", "commit"]),
        ],
        "change": [
            (
                "intake",
                "受理评估",
                ["intake", "triage", "new_requirement", "assess", "decide"],
            ),
            ("apply", "落地验证", ["apply", "review", "verify"]),
            ("close", "收尾", ["wrap", "commit"]),
        ],
        "defect": [
            (
                "pull",
                "拉取分析",
                ["preflight", "pull", "source", "analyze", "decide"],
            ),
            ("act", "处置回写", ["apply", "review", "writeback", "verify"]),
            ("close", "收尾", ["wrap", "commit"]),
        ],
        "plan": [
            ("shape", "目标范围", ["goals", "roadmap", "scope", "review-plan"]),
            ("publish", "发布下一步", ["publish", "next"]),
            ("close", "收尾", ["wrap", "commit"]),
        ],
        "new-product": [
            ("define", "发现定义", ["discover", "go", "define"]),
            ("build", "PRD交付", ["prd", "deliver", "launch"]),
            ("close", "收尾", ["wrap", "commit"]),
        ],
        "deliver": [
            ("prep", "排期跟进", ["schedule", "review-plan-deliver", "followup"]),
            ("ship", "验收发布", ["uat", "release"]),
            ("close", "收尾", ["wrap", "commit"]),
        ],
        "showcase": [
            ("story", "受众故事", ["audience", "story", "demo", "environment"]),
            ("pack", "材料发布", ["materials", "docs", "dryrun", "publish"]),
            ("close", "收尾", ["wrap", "commit"]),
        ],
    },
    "wf-testing": {
        "testing": [
            ("prep", "分析计划", ["status", "analyze", "plan", "generate", "review-cases"]),
            ("run", "执行报告", ["execute", "report"]),
            ("close", "交接收尾", ["handoff"]),
        ],
    },
}


def build_work_rules(
    root: Path,
    skills: list[str],
    notes: str,
    wid: str,
    sid: str,
    card: str = "",
    extra_card: str = "",
) -> str:
    """Step orchestration rules only — do NOT paste skill bodies (quality lives in skills)."""
    parts: list[str] = []
    parts.append(
        "> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。\n"
        "> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，"
        "**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。\n"
    )
    if skills:
        must = [s for s in skills if s not in CONDITIONAL_SKILLS]
        cond = [s for s in skills if s in CONDITIONAL_SKILLS]
        if must:
            parts.append(
                "- **本步必开技能（质量不降）**："
                + "、".join(f"`{s}`" for s in must)
                + " → 见 §6 闭环。\n"
            )
        if cond:
            parts.append(
                "- **条件技能**："
                + "、".join(f"`{s}`（{CONDITIONAL_SKILLS[s]}）" for s in cond)
                + " → 命中则同样走 §6 闭环。\n"
            )
    if card:
        parts.append(card)
        parts.append("")
    elif notes.strip():
        parts.append(notes_to_howto(notes))
        parts.append("")
    else:
        parts.append(notes_to_howto(""))
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


def build_skill_index(skills: list[str], notes: str) -> str:
    if not skills:
        return (
            "- 本步无技能指向；按 §5 编排执行。\n"
            "- 禁止无指向却通读 skills/「找感觉」。"
        )
    lines = [
        "> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  ",
        "> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。",
        "",
        "| 技能 | 级别 | 何时 | 路径 | 打开后 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for sk in skills:
        if sk in CONDITIONAL_SKILLS:
            level = "条件开"
            when = CONDITIONAL_SKILLS[sk]
        else:
            level = "**必开**"
            when = "进入本步即开（质量不降）"
        lines.append(
            f"| `{sk}` | {level} | {when} | `skills/{sk}/SKILL.md` | 必做区 → 回本包 |"
        )
    lines.append("")
    lines.append("- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。")
    lines.append("- 条件未命中 → 该行 `na` + 一句理由。")
    lines.append("- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。")
    return "\n".join(lines)


def regions_for(pack_key: str, wid: str) -> list[tuple[str, str, list[str]]]:
    return REGIONS.get(pack_key, {}).get(wid, [])


def region_of_step(
    pack_key: str, wid: str, sid: str
) -> tuple[str, str] | None:
    for rid, title, sids in regions_for(pack_key, wid):
        if sid in sids:
            return rid, title
    return None


def render_region_packet(
    pack_label: str,
    pack_key: str,
    wid: str,
    rid: str,
    title: str,
    step_ids: list[str],
    steps_by_id: dict[str, dict],
    next_region: tuple[str, str] | None,
) -> str:
    rows = [
        "| step | 名称 | when | 步骤包 |",
        "| --- | --- | --- | --- |",
    ]
    for sid in step_ids:
        st = steps_by_id.get(sid) or {}
        name = st.get("name") or sid
        when = st.get("when") or "—"
        rows.append(
            f"| `{sid}` | {name} | `{when}` | `rules/packets/{wid}/{sid}.md` |"
        )
    nxt = (
        f"下一区地图 `rules/packets/{wid}/_region-{next_region[0]}.md`（{next_region[1]}）。是否进入只按父链「推进」。"
        if next_region
        else "链末为 wrap/commit。是否进入只按父链「推进」。"
    )
    return f"""# 子状态机 · {wid}/{rid}

> **嵌套闭环**：长链路中的一小段。进入本区读一次；区内仍 **一次只开一个** step packet。

## 定位

- **包轨**：{pack_label}
- **父流程**：`rules/packets/{wid}/_chain.md`
- **本区**：`{rid}` — {title}
- **出口**：{nxt}

## 区内步骤

{chr(10).join(rows)}

## 区内纪律

1. {region_advance_line(pack_key)}
2. 当前 `packet=` 必须是区内某一步；离开本区前心跳刷新到下一步/下一区。
3. 技能只按**当前步骤包 §6** 打开→执行→回包；不在本区预读全部 skill。
4. 不要为「看全貌」打开其他区的全部步骤包。
"""


def render_chain_packet(
    pack_label: str,
    pack_key: str,
    wid: str,
    wf_name: str,
    steps: list[dict],
    chain_full: bool,
) -> str:
    rows = [
        "| # | step | 名称 | when | 子机 | 步骤包 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for i, step in enumerate(steps, 1):
        if not isinstance(step, dict) or "id" not in step:
            continue
        sid = step["id"]
        name = step.get("name") or sid
        when = step.get("when") or "—"
        reg = region_of_step(pack_key, wid, sid)
        reg_s = f"`_region-{reg[0]}`" if reg else "—"
        rows.append(
            f"| {i} | `{sid}` | {name} | `{when}` | {reg_s} | `rules/packets/{wid}/{sid}.md` |"
        )
    regions = regions_for(pack_key, wid)
    if regions:
        reg_lines = [
            "| 子机 | 含义 | 地图 |",
            "| --- | --- | --- |",
        ]
        for rid, title, _ in regions:
            reg_lines.append(
                f"| `{rid}` | {title} | `rules/packets/{wid}/_region-{rid}.md` |"
            )
        if pack_key == "wf-development":
            zone_how = "区内按表向后；不要把整条父链步骤包一次读完。"
        else:
            zone_how = "区内是否进入下一步只按上文「推进」；不要把整条父链步骤包一次读完。"
        region_block = (
            "## 状态机（父）→ 子机\n\n"
            "长链路按**子状态机**切开：进某区先读该区 `_region-*`（一次）。"
            + zone_how
            + "\n\n"
            + "\n".join(reg_lines)
        )
    else:
        if pack_key == "wf-development":
            short = "本 workflow 步骤较少，无额外子机；按阶段表与「推进」打开步骤包。\n"
        else:
            short = "本 workflow 无额外子机。是否进入下一步只按「推进」。\n"
        region_block = "## 状态机\n\n" + short

    return f"""# 流程链 · {wid}

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：{pack_label}
- **workflow**：`{wid}`（{wf_name}）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 隔离边界（改本链不动别链）

- **本链专属**：`rules/packets/{wid}/`（本文件、`_region-*`、节点包、`_orch.yaml`）；只重生成本链：`build_step_packets.py <包> <包> --only {wid}`。
- **只读共享**：`rules/core/`、`rules/gates.md`、`rules/workflow.md`、`skills/`、`rules/templates/`；改共享层会影响所有链，须跑全包自检。
- **跨链需要时**：重新路由或 handoff；诊断确需只读对方 `_chain.md`，不打开对方节点包，读完回本链。

## 推进

{advance_prose(pack_key, wid, chain_full)}

{region_block}

## 阶段表（全量索引 · 勿一次读完各包）

{chr(10).join(rows)}

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次。是否进入下一步或下一区，只按上文「推进」。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
"""


# 每步独立完整：把 cold-start §1 硬约束全文摘要写入步骤包（跨步重复 OK；勿靠跳转拼齐）。
INLINE_HARD_RULES = tuple(str(i) for i in range(1, 15))


def cold_start_digest(root: Path) -> str:
    """Embed cold-start §1 into each step packet (duplication across steps is intentional)."""
    p = root / "rules" / "core" / "cold-start.md"
    if not p.is_file():
        return "- （开局卡缺失：先意图确认；完成只认 CLAIM: ALLOWED；禁通读全书。）"
    text = p.read_text(encoding="utf-8")
    # Prefer the short invariants (§1.1) for packets; full text stays in §1 (session start).
    m = re.search(r"## 1\.1[^\n]*\n(.*?)(?=\n## |\Z)", text, re.S)
    if not m:
        m = re.search(r"## 1\. 硬约束\n(.*?)(?=\n## |\Z)", text, re.S)
    block = m.group(1).strip() if m else ""
    lines = []
    for line in block.splitlines():
        line = line.strip()
        rm = re.match(r"^(\d+)\.\s*(.+)$", line)
        if rm and rm.group(1) in INLINE_HARD_RULES:
            body = rm.group(2)
            if len(body) > 220:
                body = body[:220] + "…"
            lines.append(f"- {rm.group(1)}. {body}")
    if not lines:
        return "- 先意图确认；本步只读步骤包；完成只认 CLAIM: ALLOWED；证据先于结论。"
    text = neutralize_pointers("\n".join(lines))
    text = text.replace("见 §4", "见本包「本步操作面」")
    text = text.replace("（`rule-anchor.md`）", "（心跳格式）")
    # Inside a step packet, 「本文」易被当成步骤包；读链主语改回开局卡。
    text = re.sub(r"(\*\*读链\*\*：)本文 →", r"\1开局卡 →", text)
    return (
        text
        + "\n- **效力**：以上为执行摘要（全文见开局卡 §1）；开局已读则中段不重开全文，**每步仍须逐条遵守**；与开局卡重复不影响。"
    )


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
    body = neutralize_pointers("\n\n".join(parts))
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
            "口令明确只做单步（只出方案/只评审/代码评审/方案评审/只提测/只出清单/轻量方案）时，本步完成即停并输出收尾骨架；其余按表向后。",
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
    if pack_key == "wf-development":
        return (
            "- **推进**：本步完成后沿父链进入下一未跳过步；"
            "口令为单步（只出方案/只评审/代码评审/方案评审/只提测/只出清单/轻量方案）或动作清单写明停止/跳转时，"
            "以口令/清单为准，即停并输出收尾骨架。"
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


def notes_to_howto(notes: str) -> str:
    notes = neutralize_pointers(notes.strip())
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
        role_txt = f"（{role}）" if role else ""
        goal_txt = f"{role_goal.rstrip('。；')}；" if role_goal else ""
        identity += f"- **角色**：`{agent_id}`{role_txt}。{goal_txt}本步只做该角色职责；越界交回或升级。\n"
    precondition = step.get("precondition")
    if isinstance(precondition, str) and precondition.strip():
        identity += f"- **前置**：{precondition.strip()}\n"
    identity += (
        f"- **上游**：`{prev_id}`（取其产出为本步输入；该步被 `when` 跳过时按缺口停/补齐）\n"
        if prev_id else "- **上游**：无（链首）\n"
    )
    if terminal:
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
    risk += f"- **父状态机**：进 wf 时读 `_chain` 一次；**中段勿重读**。\n"
    reg = region_of_step(pack_key, wid, sid)
    if reg:
        risk += (
            f"- **子状态机**：进「{reg[1]}」区时读 `_region-{reg[0]}` 一次；**中段勿重读**。\n"
        )

    hard = (
        "### 全局硬约束（本包已带齐 · 每步都遵守）\n\n"
        + cold_start_digest(root)
        + "\n\n### 本步操作面（本链本步独立完整）\n\n"
        "- **读这些就能干完本步**：本文（全局摘要 + §4 门 + §5 编排）+ §6 表内 skill（一次 1 个闭环）"
        "+（若 §7 列出）至多 1 模板。\n"
        "- **不靠跳转拼流程**：本步所需规则已写在本文；他步/他链可有相同条文，互不依赖。\n"
        "- **完成声称**：有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。\n"
        "- **上下文锚**：`packet=`/`reads=` 必须含本 packet；切步前心跳刷新。\n"
        "\n### 本步禁止\n\n"
        "- 禁止用 read-index / 他步 packet /「详见别处 rules」拼本步流程。\n"
        "- 禁止跳过 §6 必开技能，或用摘要代替实读。\n"
        "- 禁止未过 §4 门或未出 §8 信号就宣称完成、推进或写「已通过」。"
    )

    gate_lines: list[str] = []
    for hn, hw in hitl_pairs(step):
        desc = neutralize_pointers(gates.get(hn) or "出示确认块后等待用户。")
        gate_lines.append(f"- **HITL `{hn}`**：{desc}")
        if hw:
            gate_lines.append(when_line(str(hw), when_map, "hitl", "跳过该门"))
    gate = step.get("gate")
    if gate:
        gw = step.get("gate_when")
        desc = gates.get(f"gate: {gate}") or gates.get(str(gate)) or "运行对应 verify；未过不得宣称完成。"
        desc = neutralize_pointers(desc)
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
    extra_card = ""
    if not card and (
        "doc-governance" in notes
        or any("doc-governance" in (gates.get(hn) or "") for hn, _ in hitl_pairs(step))
    ):
        extra_card = DOC_GOV_CARD
    work = build_work_rules(
        root, skills, notes, wid, sid, card=card, extra_card=extra_card
    )
    skill_idx = build_skill_index(skills, notes)

    open_lines = [
        "- **本步完整面**：本步骤包（§3 全局摘要 + §4 门 + §5 规则卡/编排）"
        "+ §6 必开/条件开 skill（一次 1 个）+ 本步输入。",
    ]
    uniq_tpl = list(dict.fromkeys(t for t in templates if t))
    if uniq_tpl:
        open_lines.append(
            "- **填写模板（仅此一份）**：`" + "`；`".join(uniq_tpl)
            + "`；只读本步用到的节，禁止整文件通读。"
        )
    else:
        open_lines.append(
            "- **无强制模板**：§5 规则卡已给出输出形状；直接落 §2 产出。"
        )
    if gate or ("Claim" in notes or "Invoke-Gate" in notes):
        verify_line = "- 验证命令：`verify/Invoke-Gate.ps1`（声称完成加 `-Claim`）"
        if needs_frontend_gate(root, wid, sid):
            verify_line += "；有 UI 遵 §5 前端硬门（已内嵌）"
        open_lines.append(verify_line + "。")
    open_lines.append("- 本步不再读 read-index / 他步 packet / 大手册；模板与 skill 只读指定节。")

    rel = f"rules/packets/{wid}/{sid}.md"
    skill_names = ",".join(skills) if skills else "na"
    done_line = (
        "- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。"
        if skills
        else "- §2 产出已落盘；本步无 §6 技能指向。"
    )
    return f"""# 步骤包 · {wid}/{sid}

> **状态 = 本 step（独立完整）**。全局硬约束见 §3（每步遵守）；本步门/编排/完成见本文；**方法在 §6 skill**（打开→执行→回来）。  
> 与开局卡/他步条文重复 OK；不要跳转拼流程；不要跳过必开 skill。

## 1. 元信息

- **包轨**：{pack_label}
- **workflow**：`{wid}`
- **step**：`{sid}`（{name}）
- **packet**：`{rel}`
{identity}{risk}
## 2. 本步目标

- **目标**：{name}
- **产出**：{output}

## 3. 本步硬约束

{hard}

## 4. 本步门

{chr(10).join(gate_lines)}

## 5. 本步工作规则（编排）

{work}

## 6. 技能指向（打开 → 执行 → 回本包）

{skill_idx}

## 7. 打开/填写

{chr(10).join(open_lines)}

## 8. 完成信号

{done_line}
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:{wid} | step={sid} | agent={agent_id or "na"} | packet={rel} | reads={rel}[+skill] | skills={skill_names}|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `{rel}`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
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
        orch_cache = load_orch(root, wid)
        orch_out: dict[str, str] = {}
        # Parent state machine + nested region machines
        chain_path = root / f"rules/packets/{wid}/_chain.md"
        chain_path.parent.mkdir(parents=True, exist_ok=True)
        wf_meta = data.get("workflow") if isinstance(data.get("workflow"), dict) else {}
        chain_full = str((wf_meta or {}).get("chain") or "") == "full"
        chain_body = render_chain_packet(
            pack_label, pack_key, wid, wf_name, steps, chain_full
        )
        tmp_c = chain_path
        emit(tmp_c, chain_body)

        steps_by_id = {
            s["id"]: s for s in steps if isinstance(s, dict) and "id" in s
        }
        regs = regions_for(pack_key, wid)
        # only keep step ids that exist in this workflow
        regs = [
            (rid, title, [s for s in sids if s in steps_by_id])
            for rid, title, sids in regs
        ]
        regs = [(rid, title, sids) for rid, title, sids in regs if sids]
        for i, (rid, title, sids) in enumerate(regs):
            nxt = None
            if i + 1 < len(regs):
                nxt = (regs[i + 1][0], regs[i + 1][1])
            rpath = root / f"rules/packets/{wid}/_region-{rid}.md"
            rbody = render_region_packet(
                pack_label, pack_key, wid, rid, title, sids, steps_by_id, nxt
            )
            emit(rpath, rbody)

        n = 0
        indexed = 0
        for step in steps:
            if not isinstance(step, dict) or "id" not in step:
                continue
            sid = step["id"]
            full_notes = step.get("notes") or ""
            if not isinstance(full_notes, str):
                full_notes = str(full_notes)
            # Prefer rich YAML notes; if already thinned, revive from _orch cache.
            if is_thin_notes(full_notes) and sid in orch_cache:
                full_notes = orch_cache[sid]
            full_notes = sanitize_notes_for_yaml(full_notes)
            if full_notes and not is_thin_notes(full_notes):
                orch_out[sid] = full_notes
            # Resolve skills from rich notes (_orch / pre-thin), never from thin YAML stub.
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
            templates = list(
                dict.fromkeys(
                    ([template] if template else [])
                    + re.findall(r"rules/templates/[^\s`，。；]+?\.md", full_notes)
                )
            )
            packet_rel = f"rules/packets/{wid}/{sid}.md"
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
                template,
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
            for t in templates:
                if t not in new_mr:
                    new_mr.append(t)
            step["must_read"] = new_mr
            step.pop("skills", None)
            # YAML stays thin orchestration — rich notes persist in _orch.yaml
            step["notes"] = (
                f"只读 must_read 步骤包（+流程链 `_chain` 进 workflow 时一次）。"
                f"本字段非规则正文；编排笔记见 packets/{wid}/_orch.yaml。"
            )
            n += 1
            if skills:
                indexed += 1
        if orch_out:
            # Keep prior orch entries for deleted/renamed steps only if still useful —
            # prefer current workflow steps as sole source.
            save_orch(root, wid, orch_out)
        header = (
            f"# 编排：只读当前 step。进 wf → packets/{wid}/_chain.md；进子机 → _region-*；执行 → 步骤包。\n"
            f"# 步骤包 §6 必开技能：打开→执行→回包（质量不降）。禁把 skill 正文嵌进步骤包。\n"
            f"# 富编排笔记：packets/{wid}/_orch.yaml（重建用）。禁通读本 YAML 其他 step。\n"
        )
        print_msg_extra = f", regions={len(regs)}" if regs else ""
        dumped = yaml.dump(
            data,
            Dumper=_Dumper,
            allow_unicode=True,
            sort_keys=False,
            width=120,
        )
        emit(ypath, header + dumped)
        print(
            f"OK {pack_label}/{wid}: {n} packets + _chain{print_msg_extra} ({indexed} skill-linked)"
        )


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
            print(f"PACKETS_STALE: {len(DRIFT)} 处生成物与 workflows/_orch 源不一致")
            for d in DRIFT[:40]:
                print("  " + d)
            print("修：python rules/tools/build_step_packets.py <包根> 后重跑自检。")
            return 1
        print("PACKETS_UP_TO_DATE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
