# 开发规范 — 使用说明

> 供人阅读；**AI 新会话先读** `rules/core/cold-start.md`，口令/分级见 `AGENTS.md`。  
> **template_version**：以 `AGENTS.md` 为准（单点）。

## 1. 是什么

**AI Workflow 包（开发轨）**：声明式 `workflows/*.yaml` + 角色 `agents/*.yaml` + 红线 `rules/` + 内置专业技能（`skills/`：随包生效、按步自动加载）+ 能力契约/参考目录（实例真源 `{workroot}/capabilities/`）+ 文档治理（需求/方案/清单/提测/发布/UAT/复盘统一落位、索引、归档；根 `CHANGELOG.md` 产品发版史 + `{workroot}/work-log.md` 里程碑 + 发布说明按版本）。  
执行宿主（任意支持 AGENTS 的 AI 编码工具，要求见本文「宿主适配」节）按 YAML 步骤执行；步内实现路径交 AI（框架固定 · 局部自主）。  
**产品文档解析**：输入含 PRD/迭代方案/文档/页面原型/截图时，先按 `skills/product-doc-analysis/SKILL.md` 产出需求理解包——**§0【业务与变更简报】+【本期差量表】置顶**（人类快查本期增/改/删），下钻含引用、冲突、GAP、假设与置信度；确认门主屏出示 §0。同轮生成**用户版业务变化说明**（`{workroot}/10-requirements/说明-{主题}-用户版-{yyyyMMdd}.md`；L1+ 用户可见变化必出），供业务用户快速理解，也供 AI 读取完整业务上下文。再按 `rules/core/clarification.md` 先分析、只问意图/范围/验收/风险，技术细节给建议，首轮 0～1 问、总≤3，确认后才进需求基线/方案/实施。
**完整链路**：开发计划（L2+）→ 产品文档解析/需求理解（PRD/迭代方案/原型，可选）→ 开发需求基线/技术差距 → 方案/ADR（前端需要补设计时才另出前端设计说明；产品方案完整则直接实现）→ 任务清单 → 实现/自测 → 评审 → 提测 → 测试报告（可选）→ UAT/验收（已有则引用，无则本包补）→ 工程发布审批 → 部署/verify/回滚 → 发布后观察 → 复盘；按变更分级（L0～L3）裁剪。  
**轻量单人轨**：个人小项目/单一想法默认走 `workflows/solo.yaml`：产品定义（按需）→ 一页方案卡 → 一次方案确认 → 实施 → AI 实测（开发自验）→ 完成门 → 收尾；不再分快/标准/完整档，>3 文件或 >1 模块、权限/资金/数据/迁移/安全等自动升级完整链。轻量=裁文档厚度，**不**降 AC/完成门/自验；拿不准升级。细则见 `rules/core/lightweight.md`。  
**独立落地**：本包可单独使用；不要求安装产品/测试包。缺他包产物时一句缺口并用本包模板补（产品最小硬门槛 + 开发自验），**不因「个人/无 QA」降标**。多包同项目时自动探测并共用原件根 `inbound/` 与 `activeContext.md`；本包仍独立执行自己的 workflow；开发自验 ≠ 版本准出。  
**产品缺陷流转**：开发判定产品缺陷 → 出评估单 → **有平台则以平台回写+指派为主**（不强制再打 BUG 交接包）；无平台/点名交接包 → 先问后发自包含评估包。产品确认后回流开发。三包独立；多包同仓直读不转发。  
**全局纪律**：界面减法、UX/DX/AX 三维同向、开发阶段不背旧数据（`AGENTS.md` §0.3-7/8；细则 `skills/engineering-quality` §1.1～1.2、`skills/frontend-design` §5.1）。

## 2. 目录

| 路径 | 作用 |
| --- | --- |
| `workflows/` | 流程定义：`solo`（轻量单人轨）/ `intake`（变更吸收）/ `change` / `defect-fix` / `iterate` / `handoff`（交接包/回执/变更通知）/ `onboard` / `release` / `retro` / `control`（开发计划）/ `materials`（权威文档库）/ `skill-audit`（能力技能体检） |
| `agents/` | 角色契约：implementer / defect-fixer / iterate-lead / reviewer-agent / **doc-reviewer** / **verifier-agent** / onboard-agent / delivery-lead / worker-agent |
| `capabilities/` | 包侧契约+参考目录；实例真源在工作根 `{workroot}/capabilities/` |
| `skills/` | 内置专业技能（结构 `skills/<name>/SKILL.md`；编号→路径映射见 `skills/README.md`） |
| `AGENTS.md` | AI 入口（口令 → workflow；分级；接入标记；版本单点） |
| `rules/core/cold-start.md` | **开局卡**（常驻硬约束 SSOT） |
| `rules/core/frontend-gate.md` | 前端硬门（有 UI 必读） |
| `rules/core/iq-checklist.md` | 实施质量勾选（implement 先勾） |
| `rules/read-index.md` | **维护用**索引（step→历史 MUST/RUN/REF）；运行时勿读 |
| `rules/gates.md` | 门/gate/`when` 语义、门档位；含 `completion-gate` |
| `rules/workflow.md` | 护栏、提交门、文档落位摘要（只读当前节） |
| `rules/doc-governance.md` | 资料收取/分类/覆盖对照/失效/归档 + 工作文档生命周期/归档/清理 + 根 CHANGELOG / 工作日志 / 发布说明 |
| `rules/core/` | `cold-start.md`、`frontend-gate.md`、`iq-checklist.md`、`execution-contract.md`、`clarification.md`、`routing.md`、`verification.md`、`implementation-quality.md`（词典）、`rule-anchor.md` 等 |
| `rules/collaboration/` | `handoff.md`、`roles.md`、`subagents.md` |
| `rules/defects/` | `fix-collaboration.md`、`platform-adapter.md` |
| `rules/special/` | `iteration-delivery.md`（迭代/任务清单/DoR/DoD 参考） |
| `rules/playbooks/` | 重阶段步骤卡：迭代/缺陷/发布 |
| `rules/templates/` | 按生命周期分 7 组：`00-onboarding` / `10-planning` / `20-design` / `30-planning-tasks` / `40-delivery` / `60-retro` / `90-handoff`；先看 `rules/templates/index.md` |
| `rules/tools/` | 包自检 `Test-Template.ps1`、YAML 校验、任务清单校验、文档树初始化 `Initialize-Docs.ps1`、交接包校验 `validate_handoff.py` |
| `verify/` | 完成门 `verify/Invoke-Gate.ps1`、检查矩阵、前端 20 项清单/路由覆盖校验/Playwright 模板、报告 `verify/Test-Report.ps1`（包内只读）；运行态落项目根 `.gate/` |

实例在项目根：`project-profile.md`、`activeContext.md`（含 `### 进行中` 快照）、根 `CHANGELOG.md`、`{workroot}/`。跨角色交接：**内容优先、包按需**——提测默认自洽提测单并实拷 `handoff/outbound/提测/`；HO 仅多文件/签收/仓外/同发发版/点名时先问后发到 `handoff/outbound/{category}/{HO-ID}/`。入站 `handoff/inbound/`。有平台已交不强制 BUG/FIX 整包。多包同仓直读对方出站。

### 2.1 文档分层（按需读）

| 层 | 位置 | 读法 |
| --- | --- | --- |
| 入口 | `AGENTS.md` | 新会话读 **§0 硬节**；中段按 `rules/core/rule-anchor.md` 心跳；口令表仅路由未定/首次命中时读；禁止通读 §0～§3 全文 |
| 多包定包 | `wf/AGENTS.md` **意图→包** | 歧义口令先定包再路由 |
| 路由 | `workflows/*.yaml` | 只读命中 workflow 的当前 step |
| 运行时读链 | `cold-start`（开局）→ `_chain`/`_region`（进链一次）→ **当前步骤包**（含全局摘要，独立完整）→ §6 skill | 全局每步遵守；本步不跳转拼流程；他步可重复同文 |
| 参考手册 | `rules/workflow.md`、`rules/defects/fix-collaboration.md`、`rules/collaboration/handoff.md`（标 `读取级别：参考`） | 只读当前 step/阶段节，禁止通读 |
| 技能 | `skills/<name>/SKILL.md` | 命中步才读；不命中不读 |
| 模板 | `rules/templates/index.md` → 当前组 | 只读当前要填的一份 |
| 验证 | `verify/` | 收尾/过门时读；运行态写 `.gate/wf-development/` |

> 读取预算（目标，非硬上限）：核心 ≤3～4 个来源（命中才读）+ ≤8k tokens；复杂可至 5；先读当前 step、当前 agent、当前技能节、当前产物，再按需补规则节。规则不是越多越稳，读全本会稀释当前 step 约束。

## 3. 上手（快速开始）

1. 复制 `wf-development/` 到项目根下一层；**排除** `.draft/`、`.state/`、`.gate/`、`__pycache__/`（运行态/过程文件/缓存，不是规范）。推荐 `git archive` 或 `robocopy /XD .draft .state .gate __pycache__`。包默认不进入项目 git；不跟踪时 `.gitignore` 只写一行 `/wf-development/`（多包 `/wf/`），不预列未装包、不加注释。
2. 挂载：按 `rules/templates/00-onboarding/root-agents-pointer.md` 把引导语句补入项目根 `AGENTS.md`（追加不覆盖；母版不写偏好正文，由落地项目自写）。  
3. 对 AI 说「接入开发规范」→ `workflows/onboard.yaml`：建档 → 文档树/索引/归档 → 根 `CHANGELOG.md` + `{workroot}/work-log.md` → 入库策略 → 打标。  
3.1 **个人小项目/想法**：直接说「我有个想法：…」或「轻量开发」→ `solo`：按需产品定义 → 一页方案卡 → 你确认 → 实施 → AI 实测 → 收尾；L2+ 自动升级完整链。纯文档小改走 `change` L0；代码/配置小改走 `change` L1 或 `solo`。  
3.2 **不用口令**：任意自然语言描述即可；AI 按 `rules/core/routing.md` 抽五元组→意图类→状态修正，不抠固定措辞；首条 `route`/`reason`。轻量/完整由项目状态决定；判断错可一句纠正。  
4. 之后任务**不再**例行落地自检，直接路由执行。  
5. 新文档/变化/确认项：直接把文件发给 AI，或说「这是新一期方案/这个未决项定了/新增需求…」→ `workflows/intake.yaml`：收件→分类→覆盖对照→影响分析→局部更新→变更吸收报告；你只确认实质变更与资料归档。整理现有资料说「资料收取 / 资料整理 / 资料归档 / 资料巡检」；检查工作文档/临时文件说「文档巡检 / 清理临时文件」。  
6. 新项目/新产品：说「开发计划」→ `workflows/control.yaml` init，按 `rules/templates/10-planning/development-plan-template.md` 建 `{workroot}/development-plan.md`（新项目建议 `{workroot}/development-plan.md`；旧项目可保留 `{workroot}/00-governance/development-plan.md`）；首次计划经 `confirm_plan` 后从 S0 输入检查开始按阶段/门执行。S3 叫「任务与排期」，不要与开发计划混称。  
6.1 日常推进：说 **「按开发计划执行 / 下一步 / 当前状态」** → `control` 的 run/next；读计划 §0，按当前阶段路由到 change/iterate/release/retro，执行到下一个门停止；每步回写计划与执行日志。  
7. 新功能/迭代：说「按方案实施」或「只出任务清单」→ 任务清单按 `rules/templates/30-planning-tasks/task-list-template.md` 落 `{workroot}/40-tasks/`；确认后实施。  
8. 发布：说「发布/上线」→ `workflows/release.yaml`；发布前必须过上线检查单与审批。测试/预发部署不算 S8（A 模式 `rc.N`；B 模式 `0.3.x` QA 批次）；版本口径见 `rules/core/versioning.md`。  
9. 复盘：说「复盘/事故复盘」→ `workflows/retro.yaml`。
10. 交接：**内容优先、包按需**。提测默认只交提测单；说「生成交接包…」或命中多文件/签收/仓外/同发发版时先问再 send。接收走 receive。多包同仓直读。

落地通常只装本包。多包歧义定包见`wf/AGENTS.md` **意图→包**；若同项目装多个包，三包自动探测并共享inbound/上下文，不需要额外协作目录；一次会话只执行一个包的 workflow。长会话中段按 `rules/core/rule-anchor.md` 心跳，不重读 AGENTS §0 全文。

## 4. 自检

```text
wf-development/rules/tools/Test-Template.ps1
wf-development/rules/tools/Test-DocHygiene.ps1
wf-development/verify/Invoke-Gate.ps1 -ProjectRoot "."
```

自检内容：引用可解析、章节锚点、workflows→agents、步标记词表、能力名声明、版本单点、**YAML 语法/基本 schema、开发计划模板 schema**；文档卫生检查 AGENTS 行数、规则超长、孤立模板、读取索引/工作流挂载。  
自检时机：改包后、用户点名；接入核验由 onboarding 接入清单执行。  
任务清单/开发计划可单独校验：

```text
python wf-development/rules/tools/validate_tasklist.py <任务清单路径>
python wf-development/rules/tools/validate_dev_plan.py <开发计划路径>
```

## 5. 宿主适配（宿主无关）

本包不写死任何宿主（Cursor / opencode / Claude Code 等均可）；换宿主只改实例侧（`project-profile.md`），包零改动。

- **最低能力**：入口自动装载（AGENTS.md 或等价）、文件读写、shell、对话式确认门（hitl）；子代理（按 `rules/collaboration/subagents.md`：达阈值分片/文件不相交可并行≤3/超时降级）、MCP（如缺陷平台）按需。  
- **入口挂载**：AGENTS.md 系宿主按 `rules/templates/00-onboarding/root-agents-pointer.md` 挂载；CLAUDE.md 系可用 @ 引用指向本包 AGENTS.md。  
- **MCP 配置落点**：只写宿主本地/用户级配置（如 Cursor：`%USERPROFILE%\.cursor\mcp.json`；路径以宿主官方文档为准）；禁项目内配置作规范入口。  
- **能力（可选）**：槽位见 `capabilities/00-contract.md`；候选见 `capabilities/reference.md`；**真源** `{workroot}/capabilities/00-能力清单.md`。清单 available 即用，否则降级；档案 §6 仅索引；点名「装配能力」写入实例。纪律：`rules/capabilities/instance-discipline.md`。  
- **体检能力**：口令「体检能力」等 → `skill-audit`：能力改 `{workroot}/capabilities/`，技能可改本包 `skills/`。  
- **技能格式**：`skills/*.md` 含 `name/description` frontmatter，兼容 Agent Skills 发现机制；随包加载不依赖安装。

## 6. 文档与归档

- **三层**：`inbound/` 原件；`{workroot}/` 工作区；`docs/materials/` 项目权威文档库。工作根读项目档案 §1 `workroot`；未声明按单包 `docs/`、多包 `docs/development/`。
- **工作区**：`development-plan.md`、`work-log.md`、`00-governance/`（变更/待决/决策/缺陷评估）、`10-requirements/`、`20-design/`、`30-architecture/ADR/`、`40-tasks/`、`50-verification/`、`60-release/`、`70-ops/`、`80-retrospectives/`、`capabilities/`、`handoff/`、`_archive/`；按需建，无内容不建空目录。  
- **权威文档库**：项目级 `docs/materials/`；每版 `{ver}/` 自包含，域 `00-overview`～`07-appendix`；`README.md` + `INDEX.md`；不设 `_archive`，旧版本保留；正文从工作区发布，不直接改。  
- **原件**：`inbound/INDEX.md` 全量登记；`keep/mix/replace` 只整理原件结构；不迁出、不删除、不归档。  
- **版本记录**：根 `CHANGELOG.md`＝仅开发维护的产品发版史（用户可见能力/破坏性/迁移·兼容/安全；禁过程项）；`{workroot}/work-log.md`＝岗位里程碑；发布说明一版一档。  
- 细则与命名/根目录白名单见 `rules/workflow.md` §5、`rules/doc-governance.md`。
