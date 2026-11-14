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


def resolve_skills_for_step(
    root: Path,
    step: dict,
    skill_dirs: set[str],
) -> list[str]:
    raw = step.get("skills")
    if raw is None:
        return []
    if isinstance(raw, str):
        raw = [raw]
    found: list[str] = []
    for item in raw:
        name = str(item).strip()
        if name and name in skill_dirs and name not in found:
            found.append(name)
    return found


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
    text = re.sub(r"`skills/README\.md`", "技能体检（盘点→适配→拟变更→确认→复检）", text)
    text = rewrite_workflow_refs(text, current_wid)
    text = re.sub(r"技能[：:]\s*§6", "技能见 §6", text)
    text = re.sub(r"技能[：:]\s+(?!§6)", "技能见 §6：", text)
    text = text.replace("按 本包", "按本包").replace("见 本包", "见本包")
    text = text.replace("按 技能体检", "按技能体检").replace("与 技能体检", "与技能体检")
    return text


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
        "轻量：可裁剪文档厚度；升级触发与无QA自验见步骤卡；必开技能/HITL不降",
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
    text = re.sub(r"`skills/README\.md`", "技能体检（盘点→适配→拟变更→确认→复检）", text)
    text = rewrite_workflow_refs(text, current_wid)
    text = re.sub(r"技能[：:]\s*§6", "技能见 §6", text)
    text = re.sub(r"技能[：:]\s+(?!§6)", "技能见 §6：", text)
    text = text.replace("按 本包", "按本包").replace("见 本包", "见本包")
    text = text.replace("按 技能体检", "按技能体检").replace("与 技能体检", "与技能体检")
    return text


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

TEST_PLAN_CARD = """### 本步规则卡：先分析，再计划（本步门槛）

- **模板**：分析 + 总排两份都填（见 §7）；轻量仅补丁/单模块、无新增功能面且 `版本准出=否`。
- **覆盖先后（硬）**：先按方案原文逐项完整入账（每个应测细节/设计点 → §2.1 INT+Oracle + 矩阵无空格），再写计划总排；**禁止**「先粗计划、细节执行时再补分析」。执行阶段才允许按现场自主打通/择优，不得用执行自主回补分析空账。
- **硬门槛**：① 方案为主参考；至少主读+1 互补源 ② 应测细节/设计点入账；§2.1 INT+**字段级** Oracle（禁主题句充数，见分析模板 / `testcase-design` §3.1）；覆盖面/方法矩阵无未接受空格；计数被行数支撑（门查）③ 分析未确认不写计划；计划未确认不执行；覆盖闸未过不得称可执行 ④ 计划只总排；§0/§3.1 与分析联动 ⑤ §3.1 按模板填 ⑥ P0/P1/P2 均为覆盖义务 ⑦ 准出/轨道纳入见 `multi-track-quality` §0+文首（默认硬纳入；整轨否仅白名单+接受人）。
- **环境**：先读 `env-baseline.md` 命中节；缺基线先接入。
- **只读核验（可做）**：为落 §2.2/§1.4 事实可登录、GET 接口/页面结构/构建版本；**禁业务写**；回执进 `.draft`，证据与断言以执行期为准；未实测到具体值写「待确认」。
- **造数先行（硬）**：分析定稿后再定造数——§2.2 造数行落到字段级成功信号/幂等前缀/清理，§3.1 设**数据准备批**（执行形态含「造数」）一次造齐可复用数据，出 `{ver}/functional/00-数据准备-造数台账.md`；后续批按台账消费、缺则补造回写，不逐场景重造。造数/建号/开通/专项方案编制属执行期自助（`defects/classification.md` §0.4），不列计划门待确认；无需造数写「无需造数+依据」。
- **预告**：执行三步序见 execute 卡；本步不预生成全量用例≠可浅测。做法见 §6。"""

TEST_EXECUTE_CARD = """### 本步规则卡：计划驱动执行编排（本步门槛）

- **取档真值**：先读计划 §3.1；缺行按决策树补；隔离不成立 → 串行并记 `plan_batch_conflict`。取档详法见 §6 执行技能。
- **开跑声明（不可省）**：`exec_mode=脚本|直跑|模块子代理|拆分` + `pg=PG-xx|na`；**须与计划 §3.1 一致**（不一致 → 改计划或记 `deviation=`+reason；禁表写子代理、实跑直跑长期并存）；声明须对话可见（`global-rules` §8）。
- **子代理硬门槛**：模块/拆分档走 Task；一模块一新开；Reviewer fresh；返回 ≤30 行；不过门、不 git、不交平台、不改他模块。
- **质量锁**：同一意图禁并行；共享写域串行；不采信口头完成；禁为通过率删负向/边界/证伪（`multi-track-quality` Q9）。
- **Oracle 锁（硬）**：P0 通过须 `testcase-design` §3/§3.1——字段级 Oracle、同义多表/多载体对账、§3 命中专用负向独立落点或 N/A+依据；主题句不得单独支撑通过；失败原因须用户可读。
- **阻塞锁（硬）**：缺数据/账号/入口临时不通 → 先自助造数/换样/换角/换入口（有界）；**未穷尽禁止落阻塞**；摘要须卡点+已尝试+恢复条件。终态表见 `classification.md` §0.4。
- **基线锁（硬）**：开跑读命中节；造数/换样前查基线造数·样本节；本批打通的**新可复用** API/配方/样本/冲突 → **同轮**按基线「同步规则」回写；批末自检有则补齐、无则禁改。细则 SSOT：基线同步节 + §6 `test-data-and-environment`。
- **先造数后执行（硬）**：首跑先过计划数据准备批，核对造数台账（对象/ID/成功信号/幂等/清理）；后续批按台账消费，缺项或数据漂移先补造再断言；**专用负向无配方不得标通过**；台账未齐不得宣告功能批完成。
- **证据终态制（硬）**：`evidence/` 只留断言终态（通常每 SC 1～2 叶）；中间探查/重试进 `.draft/`（`global-rules` §9）。UI 失败**当场**钉断言截图；禁留到交平台再补。
- **失败卡（硬）**：失败/待实现行当场按 `test-case-template` §2 / `api-test-case-template` §3 失败卡写满（六要素：对象/全码、环境、操作≥3步、观测≥2条、证据、业务后果 + `surface=ui|api|ui+api`）；有 UI 面的**失败**须 UI 路径+截图（待实现可非截图，须缺失证据）；纯 API 才可请求链；本批门核六要素，缺项/缺 surface/UI 失败无截图 → FAIL，补采后再关批；交平台逐槽位搬运并回读比对。
- **三步序 + 偏差择优（硬）**：顺序与禁则见动作清单；**方法**见 §6 `test-execution-and-exploration`；分型专文 `rules/defects/classification.md` §0.5。
- **同域锁（硬）**：结果/写操作页落通过前做同域自洽探针（方法 §6 执行技能 5.2，含列表/徽标/KPI↔详情）；同屏冲突/读写分裂/旁路假可过 → 禁选型通过（`classification.md` §0.5）。S7/S11 收口门槛见 `multi-track-quality` §2.4.1。"""

LIFECYCLE_CARD = """### 本步规则卡：文档治理扫描

- 分类：长期/固定 → 就地更新；版本/迭代绑定 → 关闭时快照/归档；失效/替代 → 确认后归档；过程/临时（含已完结 .draft/）→ 清理候选。
- 归档前引用检查：被当前计划/用例/脚本/报告引用的输入/数据/冒烟清单保留原位或标「基线」。
- 确认前不改/不移/不删；有候选 → `docs_migration_needed=true`，停门等确认。
- 关账：`{workroot}/{ver}/` 整夹迁入 `_archive/{yyyyMMdd}-{ver}/`；清理只删已知临时/缓存/未引用失败产物。
- 失效资料在 `inbound/INDEX.md` 状态列标记；不确定移 `{workroot}/_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。"""

DOC_GOV_CARD = """### 本步规则卡：文档治理

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认后将 `{workroot}/{ver}/` **整夹**迁入 `_archive/{yyyyMMdd}-{ver}/`；常青仅 smoke/scripts/capabilities/handoff 台账；「并行不关」只落新资料、不归档现行主档。
- 清理只删已知临时/缓存/未引用失败产物；不确定移 `_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。"""

PLAN_CARD = """### 本步规则卡：拆单与 SC

- 先确认范围/AC/非目标；未确认不拆单。
- 每条 AC/Then/异常/权限/数据/跨层抽成 SC；无 SC 不开工（L0 除外）；裁剪写债项。
- 任务卡含 DoR/DoD/依赖/并行；并行 >3 或文件重叠 → 拆批。
- 只读不改代码；清单经 `confirm_backlog` 后实施。"""

WORKFLOW_CARD = """### 本步规则卡：变更与提交

- 变更/影响：先判事实与影响面；实质变更走 intake/CR，不静默改基线。
- 提交：默认仅本地提交；推送单独确认；禁 force push/切主干/擅自开 PR。
- 无文件变更 → 不硬造提交。"""

IMPLEMENT_CARD = """### 本步规则卡：实施预检与自测（本步门槛；实施类共用）

- 先勾：AC/SC/DoD 差集=0；未进 SC 且无债项 → 不开工。勾选表索引 `rules/core/iq-checklist.md`。
- **DEV-IQ-22（顺序硬）**：方案 → 分析理解 → 实施择优；理解包不抢入口；禁先看分析再找方案；漏读/砍细节 → 停工或 OPEN。**方法**见 §6 `implementation-and-selftest`。
- **预检硬门槛**：写码前命中面须先扩 SC/债项；单元=一条 SC；禁刷绿；最小改动≠裁剪 Then。
- **自测硬门槛**：每条 SC 有验证；未验证显式写；完成前方案盘点+分析合看+择优偏离留痕。有 UI 守本包「前端硬门」。
- 独立评审 → 本链 `review`；不在本步自称已评审。子代理索引 `rules/collaboration/subagents.md`；质量条守本步 §6 已列技能。"""

CLARIFY_CARD = """### 本步规则卡：外部输入与关账

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认后 `{workroot}/{ver}/` 整夹归档；「并行不关」只落新资料、不归档现行主档。
- 交接包先 `handoff.receive`；本步不 `-StartTask`。"""

WRITEBACK_CARD = """### 本步规则卡：平台回写

- 先出【回写拟稿】：单号 + 结论 + 备注全文 + 状态/指派/resolvedBuild + 附件名；用户确认后才写。
- 备注须实质（现象/根因/修复/验证），禁只写「已修复/已处理」；未验证只写「待验证」。
- 平台不支持附件 → 出 export，不假装已回写。"""

DEFECT_SEARCH_CARD = """### 本步规则卡：查重节流

- **义务**：提交前必查重；范围含未关闭/已解决/已关闭。
- **节流（硬）**：先拉一份近期列表 → 本地按标题/模块/现象过滤 → 必要时至多 1～2 次高信号 search；**禁止** 8+ 同质关键词连环 search。
- 产出一份 dedup 快照；主上下文候选判定 ≤30 行（见 `collaboration` §5.0.0、`platform-adapter`）。"""

DEFECT_SUBMIT_CARD = """### 本步规则卡：逐槽位搬运与回执

- **先定 surface**：`ui|api|ui+api`（读者看到的面）；有菜单/页面/控件→ui，纯接口→api；入口指纹（ui|network|contract）只说明入口怎么找到，≠surface。
- **十段清单（缺段禁交）**：【提交摘要】【环境】【测试数据/业务主键】【问题】【复现】【实际】【预期】【接口判定】【设计对照】【技术附记】；首段含 `问题标题：`+`一句话影响：`+`最小复现：`；末段=`【技术附记】`。
- **platform_submit**：发现即提交（计划预授权）｜批末/阶段末/收尾确认｜用户口令提交到平台（`collaboration` §6.1）；确认门出示清单+一单正文；`validate_defect_steps` 0 ERROR 后才进确认/POST。
- **搬运（硬）**：steps=执行记录失败卡按文案模板 §5.0.1a **逐槽位复制**；禁概括/改写/合并/凭记忆重写；`surface=ui`/`ui+api` 的【复现】必须是 UI 导航，API 只进第8/10块；`surface=api` 才可请求链；禁自拟精简十段、禁交单窗现网补截图/主键/文案、禁重开页面补拍。
- **回读（硬）**：POST 后回读 steps，与搬运稿做十段块级比对；缺段/末段【技术附记】缺失/明显截断 → 判失败，重试或标失败，禁只凭 HTTP 成功写「已交单」。
- **平台自洽（硬）**：建单/挂靠补证/澄清备注均须可跟做构造+观测自洽；截图/响应**上传并回查**或正文写 `字段=值`；禁测仓 `evidence/…`、本机路径、未上传叶名充证据（`collaboration` 平台自洽 + 文案模板 §5.0.3#16/#17）。
- **附件门（硬）**：`surface=ui`/`ui+api` → ≥1 钉点截图已挂本单；`surface=api` → 响应文件已挂**或**正文关键片段齐；回查 `files` 后再写回执（禁「有 json 叶=已交证」）。
- **写入自检（硬 · 新建/正式交平台）**：十段齐 + §5.0.1b 厚度 + `surface` 一致；**POST/PUT 前** `python rules/tools/validate_defect_steps.py <steps>` 须 0 ERROR（结构+厚度；缺项按 ERROR 回补）；HTML/文本版式按适配「写入前自检」；建单 body 带 `assignedTo`（禁建后再 assign+comment 刷首条备注）。
- **入口门（硬）**：搬运前核执行详情含 `入口指纹=`；写接口单须有回查字段=值（Q22）；细则 `collaboration` §5.0.1c / `classification` §0.4。
- **台账**：`{ver}/缺陷台账.md`（§0 本轮写回每轮覆盖；§1 版本台账累计）；新建单写 `来源=记录投影|现网补采`、`surface=`、`结构=齐|缺`、`厚度=过|未过`（厚度未过禁标交单成功）；回归写回附范围卡（构建/回归范围/冒烟/影响面/未覆盖；未跑/未覆盖写接受人，槽位见 `collaboration` §7.0）；过 writeback 门。"""


def step_card(pack_key: str, wid: str, sid: str) -> str:
    """Step-local rule card that replaces YAML notes (commit/wrap/plan-style)."""
    if sid == "commit":
        return COMMIT_CARD
    if sid == "wrap":
        return WRAP_CARD
    return STEP_CARDS.get((pack_key, wid, sid), "")


def step_card_append(pack_key: str, wid: str, sid: str) -> str:
    """Extra hard gates appended after notes (does not drop action list)."""
    return STEP_CARDS_APPEND.get((pack_key, wid, sid), "")


STEP_CARDS: dict[tuple[str, str, str], str] = {
    ("wf-testing", "testing", "plan"): TEST_PLAN_CARD,
    ("wf-testing", "onboard", "lifecycle"): LIFECYCLE_CARD,
    ("wf-development", "change", "plan"): PLAN_CARD,
    ("wf-development", "iterate", "plan"): PLAN_CARD,
    ("wf-development", "change", "implement"): IMPLEMENT_CARD,
    ("wf-development", "iterate", "implement"): IMPLEMENT_CARD,
    ("wf-development", "solo", "build"): IMPLEMENT_CARD,
    ("wf-development", "defect-fix", "fix"): IMPLEMENT_CARD,
    ("wf-development", "change", "clarify"): CLARIFY_CARD,
    ("wf-product", "change", "apply"): WRITEBACK_CARD,
    ("wf-product", "defect", "apply"): WRITEBACK_CARD,
    ("wf-product", "defect", "writeback"): WRITEBACK_CARD,
}

# Append-only cards: keep YAML notes as 动作清单, then add short hard gates.
STEP_CARDS_APPEND: dict[tuple[str, str, str], str] = {
    ("wf-testing", "testing", "execute"): TEST_EXECUTE_CARD,
    ("wf-testing", "defect", "search"): DEFECT_SEARCH_CARD,
    ("wf-testing", "defect", "submit"): DEFECT_SUBMIT_CARD,
}

# testing.plan：分析+计划双模板（primary=分析；dual_fill 依赖 templates≥2）
PLAN_DUAL_TEMPLATES = (
    "rules/templates/10-planning/test-analysis-template.md",
    "rules/templates/10-planning/test-plan-template.md",
)

TEMPLATE_OVERRIDES: dict[tuple[str, str, str], str] = {
    ("wf-product", "onboard", "profile"): "rules/templates/00-onboarding/product-profile-template.md",
    ("wf-development", "onboard", "docs"): "rules/templates/00-onboarding/workspace-index-template.md",
    ("wf-development", "change", "analyze_input"): "rules/templates/10-planning/requirement-understanding-template.md",
    ("wf-development", "handoff", "compose"): "rules/templates/90-handoff/handoff-note-template.md",
    ("wf-development", "handoff", "send"): "rules/templates/90-handoff/handoff-package-brief-template.md",
    ("wf-development", "defect-fix", "close"): "rules/templates/40-delivery/defect-writeup-template.md",
    ("wf-development", "iterate", "deliver"): "rules/templates/40-delivery/qa-handoff-template.md",
    ("wf-testing", "handoff", "send"): "rules/templates/90-handoff/handoff-package-brief-template.md",
    ("wf-product", "change", "intake"): "rules/templates/30-review-change/intake-disposition-template.md",
    ("wf-product", "prototype", "wireframe"): "rules/templates/20-design/prototype-spec-template.md",
    ("wf-product", "new-product", "prd"): "rules/templates/10-planning/prd-template.md",
    ("wf-testing", "testing", "plan"): PLAN_DUAL_TEMPLATES[0],
    ("wf-testing", "testing", "execute"): "rules/templates/20-test-cases/test-case-template.md",
    ("wf-testing", "testing", "report"): "rules/templates/40-report-review/test-report-template.md",
    ("wf-testing", "defect", "submit"): "rules/templates/30-execution/defect-writeup-template.md",
    ("wf-testing", "handoff", "compose"): "rules/templates/90-handoff/handoff-note-template.md",
    ("wf-testing", "onboard", "baseline"): "rules/templates/00-onboarding/env-baseline-template.md",
    ("wf-development", "change", "requirements"): "rules/templates/10-planning/requirement-baseline-template.md",
    ("wf-development", "change", "design"): "rules/templates/20-design/solution-template.md",
    ("wf-development", "change", "plan"): "rules/templates/30-planning-tasks/task-list-template.md",
    ("wf-development", "change", "deliver"): "rules/templates/40-delivery/qa-handoff-template.md",
    ("wf-development", "iterate", "plan"): "rules/templates/30-planning-tasks/task-list-template.md",
    ("wf-development", "release", "readiness"): "rules/templates/40-delivery/go-live-checklist-template.md",
    ("wf-development", "release", "record"): "rules/templates/40-delivery/release-record-template.md",
    ("wf-development", "solo", "plan"): "rules/templates/30-planning-tasks/solution-card-template.md",
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
    append_card: str = "",
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
    if skills or step_conditional:
        must = list(skills)
        cond = [s for s in step_conditional if s not in skills]
        if must:
            parts.append(
                "- **本步必开技能（质量不降）**："
                + "、".join(f"`{s}`" for s in must)
                + " → 见 §6 闭环。\n"
            )
        if cond:
            parts.append(
                "- **条件技能**："
                + "、".join(f"`{s}`（{step_conditional[s]}）" for s in cond)
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
    if append_card:
        parts.append(append_card)
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


def build_skill_index(
    root: Path,
    skills: list[str],
    notes: str,
    step_conditional: dict[str, str] | None = None,
) -> str:
    step_conditional = step_conditional or {}
    if not skills and not step_conditional:
        return (
            "- 本步无技能指向；按 §5 编排执行。\n"
            "- 禁止无指向却通读技能库找感觉。"
        )
    lines = [
        "> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  ",
        "> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。",
        "> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。",
        "",
        "| 技能 | 级别 | 何时 | 路径 | 打开后 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for sk in skills:
        if sk in step_conditional:
            level = "条件开"
            when = step_conditional[sk]
        else:
            level = "**必开**"
            when = "进入本步即开（质量不降）"
        opened = "整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包"
        lines.append(
            f"| `{sk}` | {level} | {when} | `skills/{sk}/SKILL.md` | {opened} |"
        )
    for sk, when in step_conditional.items():
        if sk in skills:
            continue
        lines.append(
            f"| `{sk}` | 条件开 | {when} | `skills/{sk}/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |"
        )
    lines.append("")
    lines.append("- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。")
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
    full_note = (
        "本链按入口分级：接入/重新接入/基线/生成档案/装配能力入口推进到 `verify` 打标；"
        "资料收取/文档治理/清理入口只做该步 + 收尾，不连带其余接入步。"
    ) if (chain_full and wid == "onboard") else (
        "本链为全链入口；按表推进到下一个门/停点。" if chain_full
        else "默认入口即止；仅按链/继续/按计划执行时向后推进。"
    )
    return f"""# {wf_name} · `{wid}` 状态机

> 全局规则见 `rules/core/global-rules.md`（遵守；重读按 §7 分级：新会话/换链全文，中段最小集，禁预防性通读）。每步先**实读**当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 为续跑指针；已有测试计划时阶段语义以计划 §0 为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：{entries}
- **终端**：`{terminal}`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；本图进链读一次；每步先读当前 packet。

## 2. 状态表

{chr(10).join(rows)}

## 3. 推进

- {full_note}
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `when_eval=假:<依据>`（手工跳过记 `skip=user:<理由>`）。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/{wid}.yaml` + 本图 + `rules/packets/{wid}/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

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


def load_template_index(root: Path) -> dict[tuple[str, str], list[str]]:
    """templates/index.md「用于 step」→ (workflow, step) → template paths.

    Keeps the index and the step cards in sync: a template assigned to a step
    must be discoverable from that step's §7, otherwise the gate can demand a
    structure the card never points at.
    """
    p = root / "rules" / "templates" / "index.md"
    out: dict[tuple[str, str], list[str]] = {}
    if not p.is_file():
        return out
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        tpl = cells[0].strip("` ")
        if not tpl.endswith(".md") and not tpl.endswith(".html"):
            continue
        rel = f"rules/templates/{tpl}"
        if not (root / rel).is_file():
            continue
        for wid, sid in re.findall(r"\b([a-z][a-z0-9-]*)\.([a-z][a-z0-9_-]*)\b", cells[1]):
            out.setdefault((wid, sid), []).append(rel)
    return out


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
    explicit_prev = step.get("prev")
    prev_id = explicit_prev if isinstance(explicit_prev, str) and explicit_prev else (ids[i - 1] if i > 0 else None)
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
    # Numbered clauses: keep one item per ①…⑩ so gates stay addressable and readable.
    markers = "①②③④⑤⑥⑦⑧⑨⑩"
    positions = [i for i, ch in enumerate(notes) if ch in markers]
    if len(positions) >= 2:
        lead = notes[: positions[0]].strip().strip("：:；;。 ")
        numbered: list[str] = []
        if lead:
            numbered.append(f"- {lead}：")
        for k, pos in enumerate(positions):
            nxt = positions[k + 1] if k + 1 < len(positions) else len(notes)
            seg = notes[pos:nxt].strip().strip("；;。 ")
            if seg:
                numbered.append(("  - " if lead else "- ") + f"{seg}。")
        return "### 本步动作清单\n\n" + "\n".join(numbered)
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
    ref_only: bool = False,
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
    if needs_frontend_gate(root, wid, sid):
        risk += (
            "- **轻量路径**：纯文档/无行为/无 UI 时，可将预检、前端硬门标 `na`（一句理由）；"
            "**必开技能与 Claim/HITL 不降**。\n"
        )

    hard = (
        "> **全局规则**：按 `rules/core/global-rules.md` §7 **分级重读并遵守**（中段=最小集，禁每步通读全文）；须先打开本步骤卡；心跳 `global=ok`=已按 §7 复核且步骤卡已实读；未复核不得写 `global=ok`。偏离写 `global=dev:<原因>`。\n"
        "\n### 本步边界\n\n"
        "- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。\n"
        "- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。\n"
        "- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。"
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
        desc = gates.get(f"gate: {gate}") or gates.get(str(gate)) or "按本包门表该门的检查方法核验并留证据；未过不得宣称完成。"
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
    append_card = step_card_append(pack_key, wid, sid)
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
    step_conditional = step.get("skills_conditional") or {}
    work = build_work_rules(
        root,
        skills,
        notes,
        wid,
        sid,
        card=card,
        append_card=append_card,
        extra_card=extra_card,
        step_conditional=step_conditional,
    )
    skill_idx = build_skill_index(root, skills, notes, step_conditional)

    open_lines: list[str] = []
    uniq_tpl = list(dict.fromkeys(t for t in templates if t))
    primary_tpl = template if template in uniq_tpl else (uniq_tpl[0] if uniq_tpl else None)
    others = [t for t in uniq_tpl if t != primary_tpl]
    dual_fill = (
        pack_key == "wf-testing"
        and wid == "testing"
        and sid == "plan"
        and len(uniq_tpl) >= 2
    )
    if dual_fill:
        open_lines.append(
            "- **填写模板（本步两份都填）**：`"
            + "`；`".join(uniq_tpl)
            + "`；**按表定位、随填随读**：先读分析模板首行「必填节」索引与 §0–§6；"
            "**分析确认后**再读计划模板（避免先看计划污染分析）；表下 `>` 判定口径填该表时再读；禁整文件通读/预读。"
        )
        open_lines.append(
            "- **轻量档**（`plan_tier=lite`，仅补丁/单模块、无新增功能面且 `版本准出=否`）：计划改用 "
            "`rules/templates/10-planning/test-plan-lite-template.md`；分析仍用上表分析模板。"
        )
    elif primary_tpl:
        if pack_key == "wf-testing" and wid == "defect" and sid == "submit":
            open_lines.append(
                f"- **正式交平台/新建单（硬）**：必开 `{primary_tpl}` — 缺陷通道只读 **§5.0.1～§5.0.1b**"
                "（需要粘贴骨架再开 §5.0.2）；盯办通道改读 **§5.0.3b**。只读点名节，**禁**整文件通读、**禁**跳过本条自拟 steps。"
            )
            open_lines.append(
                "- **仅状态回写备注**（无关/激/解决等）：用同模板 **§8** 对应骨架；不强制十段。"
            )
        elif pack_key == "wf-testing" and wid == "testing" and sid == "execute":
            open_lines.append(
                f"- **填写模板（按轨）**：功能/探索 → `{primary_tpl}`；接口 → "
                "`rules/templates/20-test-cases/api-test-case-template.md`；发布前 → 本轨专项方案/报告。"
                "只读本轨用到的节，禁整文件通读；禁混用模板。"
            )
        else:
            open_lines.append(
                f"- **填写模板（主）**：`{primary_tpl}`；只读本步用到的节，禁止整文件通读。"
            )
        if others:
            open_lines.append(
                "- **配套模板（按产出需要读；门按结构判分的产物须对齐）**：`" + "`；`".join(others) + "`。"
            )
    elif uniq_tpl:
        open_lines.append(
            "- **模板（产出该类文件时按此填；门按结构判分的产物须对齐）**：`"
            + "`；`".join(uniq_tpl)
            + "`。"
        )
    if not uniq_tpl:
        if card or extra_card:
            open_lines.append(
                "- **无强制模板**：§5 规则卡已给出输出形状；直接落 §2 产出。"
            )
        else:
            open_lines.append(
                "- **无强制模板**：§5 编排已给出动作/顺序；直接落 §2 产出。"
            )
    if uniq_tpl:
        open_lines.append(
            "- **产出前自检**：对照模板必填节逐项填写；缺节、空节、未替换 `{…}` = 不合格（不得标完成）。"
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
    gate_when = str(step.get("gate_when") or "")
    if requires_claim and gate_when:
        claim_line = (
            f"- 本步 Claim 门受 `gate_when: {gate_when}` 约束："
            "门执行时须 `CLAIM: ALLOWED` 才可写完成态；门被跳过 → 不产门回执，"
            "`claim=na` 并写 `when_eval=<假理由>`。"
        )
    elif requires_claim:
        claim_line = "- 本步完成 Claim 门：须 `CLAIM: ALLOWED` 后才可写完成态。"
    else:
        claim_line = "- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。"
    tpl_done = "- §2 产出已按模板必填节落地；无空节、无未替换占位符。\n" if uniq_tpl else ""
    return f"""# 步骤卡 · {wid}/{sid}

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守；重读按 §7 分级）；方法在 §6 指定节（打开→执行→回包）。**未打开本文件=未开跑本步**。不读他步 packet / 大手册。

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
{tpl_done}- 本步 hitl 已确认，或 when 条件跳过。
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
    tpl_index = load_template_index(root)
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
            skills = resolve_skills_for_step(root, step_for_skills, skill_dirs)
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
            # 模板索引 = 单一出处：本步在 index 里挂过的模板都要在 §7 可见；
            # 已有主模板时补为配套模板，避免“门按结构判分、卡里看不到模板”。
            ref_only = False
            idx_tpls = tpl_index.get((wid, sid), [])
            for t in idx_tpls:
                if t not in templates:
                    templates.append(t)
            if templates and not primary:
                ref_only = True
            if pack_key == "wf-testing" and wid == "testing" and sid == "plan":
                for t in PLAN_DUAL_TEMPLATES:
                    if t not in templates:
                        templates.append(t)
                primary = PLAN_DUAL_TEMPLATES[0]
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
                ref_only=ref_only,
            )
            body = re.sub(
                r"`(rules/templates/[^`]+?[、,][^`]+?)`",
                lambda m: " / ".join(f"`{p}`" for p in _split_path_blob(m.group(1)))
                or m.group(0),
                body,
            )
            emit(packet_path, body)
            new_mr = [packet_rel]
            if pack_key == "wf-testing" and wid == "testing" and sid == "plan":
                for t in PLAN_DUAL_TEMPLATES:
                    if t and t not in new_mr:
                        new_mr.append(t)
            elif primary and primary not in new_mr:
                new_mr.append(primary)
            step["must_read"] = new_mr
            # YAML carries the rich note; no separate cache.
            step["notes"] = full_notes if full_notes else "按本步目标与产出执行。"
            n += 1
            if skills:
                indexed += 1
        header = (
            f"# 编排：进 wf → workflows/{wid}.md；执行 → 当前 step 步骤包；终端 → _shared/closeout.md。\n"
            f"# 步骤卡 §6 必开技能：整卡读取→执行→回包。禁把 skill 正文嵌进步骤卡。\n"
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
