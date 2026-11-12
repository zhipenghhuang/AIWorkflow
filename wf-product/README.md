# 产品规范 — 使用说明

> 供人阅读；**AI 新会话先读** `AGENTS.md` → `rules/core/cold-start.md` → `rules/core/global-rules.md`（global-rules 每步重读）。  
> **template_version**：以 `AGENTS.md` 为准（单点）。

## 1. 是什么

**AI Workflow 包（产品轨）**：声明式 `workflows/*.yaml` + 角色 `agents/*.yaml` + 规则 `rules/` + 内置专业技能（`skills/`：随包生效、按步整卡读取）+ 能力契约/参考目录（实例真源 `{workroot}/capabilities/`）。  
主链：**新产品 0→1**（发现 → 立项 → 产品定义 → PRD → 交付 → 上市 → 复盘）与**迭代**（需求洞察 → 优先级/立项 → PRD → 评审定稿 → 排期 → 跟进/变更 → UAT → 发布 → 复盘）；**产品计划**（`{workroot}/product-plan.md`）为总领单点，**§3.0【业务与变更简报】+本期差量表**为默认权威 Delta（阶段 1 定范围时写入）；独立「迭代变更摘要」仅仓外handoff/版本归档/点名时按需生成。变更单含 §2.1 Now→Proposed（改已定稿基线）。**展示**（`showcase.yaml`）：受众 → 故事线/流程图 → 演示脚本 → Demo 环境 → 材料/用户文档 → 彩排。  
执行宿主（任意支持 AGENTS 的 AI 编码工具，要求见本文「宿主适配」节）按 YAML 步骤执行；步内实现路径交 AI（框架固定 · 局部自主）。  
**需求理解（产品核心职责）**：按 `skills/customer-needs-discovery/SKILL.md` + `rules/core/clarification.md` **多问清需求、完善方案要点、并做理解→方案双确认**；每轮 1 问（或 2～3 互斥选项）；技术细节先给业务向建议请确认；未双确认不得入池承诺/写正式 PRD/定版本；未确认推断标「假设」。  
**竞品与学习**：`skills/competitive-intelligence-and-learning/SKILL.md` 两档——口令「竞品分析」=模式 S（借/改编/不借）；「竞品对标」=模式 P（矩阵→候选项）；0→1 默认 S。  
**体验纪律**：界面减法（删无决策价值文案/标签，删后不清楚改布局）、UX/DX/AX 三维同向；详见 `rules/core/global-rules.md` §12、`skills/ui-visual-design-system/SKILL.md` §1.3～1.4。

## 2. 目录

| 路径 | 作用 |
| --- | --- |
| `workflows/` | `new-product`（0→1）· `plan`（产品计划/路线图）· `prd`（洞察/竞品分析·对标/立项/PRD/评审/需求交接）· `prototype`（设计策略/项目适配/IA/线框/视觉/高保真/评审/交接）· `showcase`（演示/介绍/用户文档）· `change`（受理与变更）· `defect`（缺陷平台）· `deliver`（排期/UAT/发布/复盘）· `handoff`（交接包/接收回执/变更通知/状态）· `onboard` · `materials`（权威文档库）· `skill-audit`（能力技能体检） |
| `agents/` | pm-analyst / prd-writer / pm-lead / reviewer-agent / ux-designer / onboard-agent / verifier-agent / worker-agent |
| `capabilities/` | 包侧契约+参考目录；实例真源在工作根 `{workroot}/capabilities/` |
| `skills/` | 内置专业技能（每步方法/手艺，随包生效、按步整卡读取；`skills/README.md`） |
| `AGENTS.md` | AI 入口（口令→workflow；版本单点） |
| `rules/gates.md` | 门语义、`when` 词表、门档位（autonomous/notify/approve）；含 PRD/评审/设计评审/UAT/变更/回写/材料库等门 |
| `rules/workflow.md` | 参考：阶段护栏/产物路径（运行时以 `global-rules.md` + 链图 + 步骤卡为准） |
| `rules/doc-governance.md` | 资料收取/分类/覆盖对照/失效/归档 + 工作文档生命周期/归档/清理 |
| `rules/core/` | `global-rules.md`、`cold-start.md`、`clarification.md`、`routing.md`、`verification.md`、`rule-governance.md`、`maintenance.md`、`doc-quality.md`、`context-memory.md`（参考层；运行时先读 global-rules） |
| `rules/collaboration/` | `handoff.md`、`subagents.md`、`roles.md` |
| `rules/defects/` | `platform-collaboration.md`、`platform-adapter.md` |
| `rules/special/` | 专项方法：`quality-gate.md`（审计参考）· `skill-audit.md`（能力体检）等 |
| `rules/templates/` | 按生命周期分 8 组：`00-onboarding` / `10-planning` / `20-design` / `30-review-change` / `40-delivery` / `50-showcase-docs` / `60-retro` / `90-handoff`；先看 `rules/templates/index.md` |
| `rules/tools/` | 包自检 `Test-Template.ps1`（YAML 语法/schema + 引用/锚点/流程引用/步标记/能力名/版本单点）+ `validate_workflow.py` + `validate_handoff.py`（交接包完整性） |
| `verify/` | PRD/评审/UAT/变更/回写门 `verify/Invoke-Gate.ps1`、检查矩阵、产物校验脚本；独立可复制 |

> 实例在项目根：`product-profile.md`（含 §3 产品规范要点——固定内联）、`activeContext.md`（含 `### 进行中` 快照）；产出统一在 **`{workroot}/`**；权威文档库为项目级 `docs/materials/`。  
> **三层**：`inbound/` 原件；`{workroot}/` 工作区（计划/需求池/版本目录/user/handoff/capabilities/过程）；`docs/materials/` 定稿、完整、可发送的权威文档库。  
> **交接**：内容优先、包按需；默认交自洽主文档并实拷 `{workroot}/handoff/outbound/{category}/`；HO 仅多文件/正式签收/仓外/点名时先问后发到 `handoff/outbound/{category}/{HO-ID}/`。入站 `handoff/inbound/`。多包同仓直读对方出站，禁无意义转发。  
> **可选联动（不强制）**：本包可独立落地，不要求安装开发/测试包；PRD/立项书/产品计划可作为其输入；工程部署由开发轨执行（如启用），未启用由用户安排。多包同项目共用 `inbound/` 与 `activeContext.md`，本包仍独立执行。  
> **边界**：产品负责需求、规则、原型、验收；技术架构、技术栈、数据库/API/部署归开发轨（如启用）或由用户安排。  

### 2.1 文档分层（按需读）

| 层 | 位置 | 读法 |
| --- | --- | --- |
| 入口 | `AGENTS.md` | **§0 开工（新会话一次）+ `global-rules`（每步）**；中段按 `rules/core/global-rules.md` §8 心跳；口令表仅路由未定/首次命中时读；禁止通读 §0～§3 全文 |
| 多包定包 | `wf/AGENTS.md` **意图→包** | 歧义口令先定包再路由 |
| 路由 | `workflows/*.yaml` | 只读命中 workflow 的当前 step |
| 运行时读链 | `cold-start` → `activeContext` → `global-rules`（每步）→ `workflows/<id>.md` 链图（进链一次）→ **当前步骤卡** → §6 skill | 全局每步遵守；本步不跳转拼流程；他步可重复同文 |
| 参考手册 | `rules/workflow.md`、`rules/collaboration/handoff.md`（标 `读取级别：参考`） | 只读当前 step/阶段节，禁止通读 |
| 技能 | `skills/<name>/SKILL.md` | 命中步才读；不命中不读 |
| 模板 | `rules/templates/index.md` → 当前组 | 只读当前要填的一份 |
| 验证 | `verify/` | 收尾/过门时读；运行态写 `.gate/wf-product/` |

> 读取预算（目标，非硬上限）：核心必读 ≤3～4（`AGENTS.md` 当前相关节 + 当前步骤卡 + 当前 agent/当前关键产物）；方法层按命中才读；单步读取 = 当前步骤包 + §6 技能整卡（另加每步 `global-rules`）；普通步 ≤12k，复杂步可至 22k（超出在 `reads=` 说明）；按节读的规则手册不设整文件上限；复杂步可至 5 并在收尾 `reads=` 说明；不得为省预算跳过门/证据/红线。预算约束技能长度与拆分，不把技能截断成行窗；技能确实过长时拆 `references/`，不靠少读降本。

### 2.2 版本目录（新产品默认）

```text
{workroot}/{ver}/
├─ 10-requirements/     立项书、洞察、PRD、评审记录
├─ 20-design/           设计情境、IA、线框、高保真、tokens、工程化检查、设计评审、可用性、开发交接
├─ 30-changes/          受理、变更单、产品缺陷处置
├─ 40-delivery/         交付计划、UAT、GTM
├─ 50-showcase/         展示需求、故事线、演示脚本、一页纸、Deck、检查单、反馈
└─ 90-retrospectives/   复盘
```

按需建目录，**无内容不建空目录**。旧项目保留原路径，在 `product-profile.md` 记录实际路径；说「重新接入」时再迁移。

## 3. 上手（快速开始）

1. 复制 `wf-product/` 到项目根下一层；排除 `.draft/`、`.state/`、`.gate/`、`__pycache__/`（运行态/过程文件/缓存，不是规范）；包默认不进入项目 git，不跟踪时 `.gitignore` 只写一行 `/wf-product/`（多包 `/wf/`），不预列未装包、不加注释
2. 挂载：按 `rules/templates/00-onboarding/root-agents-pointer.md` 把引导语句补入项目根 `AGENTS.md`（追加不覆盖；母版不写偏好正文，由落地项目自写）  
3. 对 AI 说「接入产品规范」→ 生成 `product-profile.md` 与 `activeContext.md`、确认入库策略、打标  
4. 之后直接说口令：「收集需求」「竞品分析」「竞品对标」「产品计划」「写 PRD」「设计简报」「画原型」「PRD 评审」「排期」「需求变更」「UAT」「发布」「准备演示」「用户手册」「发布说明」「复盘」「资料收取」「资料整理」「资料归档」「文档巡检」「清理临时文件」  
4.1 **不用口令**：任意自然语言描述需求/反馈/规划即可；AI 按 `rules/core/routing.md` 抽五元组→意图类→状态修正，不抠固定措辞；首条 `route`/`reason`。单条默认受理、批量走洞察、空白新品走 0→1；判断错可一句纠正。  
5. 也可以直接把需求/问题/缺陷发来（对话或文档）：AI 走 `change` 受理 → 分诊 → 处置 → 联动更新，最后给出受理单、变更单（如适用）、最新 PRD/计划/UAT 与开发/测试回执。  
6. 已配置禅道/Jira/ONES：说「拉取我的产品缺陷」→ 读详情/备注/附件 → 分析 → 回写备注/附件/状态/指派；未配置则粘贴/导出，不阻塞。

**三条主链**：

- **新产品（0→1）**：`启动新产品：{一句话}` → 立项书 → 确认 Go → 产品计划 → PRD → 画原型 → 交付 → 上市 → 复盘
- **迭代**：`产品计划` → `写 PRD` → `画原型` → `PRD 评审` → `排期` → `变更` → `UAT` → `发布` → `复盘`
- **展示/文档**：`准备演示：{受众/场景}` → 故事线/流程图 → 演示脚本 → Demo 检查单 → 材料 → 用户文档 → 彩排

有 `{workroot}/product-plan.md` 后，说 **「继续 / 按产品计划执行 / 下一步 / 当前状态」**：按 §0 总控表从当前阶段续跑；`下一步` 只报动作，`按产品计划执行` 执行到下一个门。

落地通常只装本包。多包歧义定包见`wf/AGENTS.md` **意图→包**；若同项目装多个包，三包自动探测并共享inbound/上下文，不需要额外协作目录；一次会话只执行一个包的 workflow。长会话中段按 `rules/core/global-rules.md` §8 心跳，不重读 AGENTS §0 全文。

## 4. 自检

```text
wf-product/rules/tools/Test-Template.ps1
```

含 YAML 语法/schema（PyYAML；未装 python 时该项跳过并提示）。PRD 另跑 `python rules/tools/validate_prd.py <PRD.md>`（元数据/16 节/Mermaid/ID/追溯/技术边界）。自检时机：改包后、用户点名；接入核验由 onboarding 接入清单执行。

## 5. 宿主适配（宿主无关）

本包不写死任何宿主（Cursor / opencode / Claude Code 等均可）；换宿主只改实例侧（`product-profile.md`），包零改动。

- **最低能力**：入口自动装载（AGENTS.md 或等价）、文件读写、shell、对话式确认门（hitl）；子代理（按 `rules/collaboration/subagents.md`：达阈值分片/适当并行≤3/超时降级）、MCP 按需。  
- **入口挂载**：AGENTS.md 系宿主按 `rules/templates/00-onboarding/root-agents-pointer.md` 挂载；CLAUDE.md 系可用 @ 引用指向本包 AGENTS.md。
- **能力（可选）**：槽位见 `capabilities/00-contract.md`；候选见 `capabilities/reference.md`；**真源** `{workroot}/capabilities/00-能力清单.md`。清单 available 即用，否则降级；档案 §6 仅索引；点名「装配能力」写入实例。纪律：`rules/capabilities/instance-discipline.md`。  
- **体检能力**：口令「体检能力」等 → `skill-audit`：能力改 `{workroot}/capabilities/`，技能可改本包 `skills/`。
- **MCP 配置落点**：只写宿主本地/用户级配置（路径以宿主官方文档为准）；禁项目内配置作规范入口。  
- **缺陷平台（可选）**：禅道/Jira/ONES 的 MCP/API 配置只写宿主本地/用户级配置；`product-profile.md` §7 只记 provider/凭据来源/适配定义；未配置走粘贴/export，不阻塞。
