# 步骤卡 · new-product/discover

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`new-product` / `discover`（发现与机会评估）
- **packet**：`rules/packets/new-product/discover.md`
- **角色**：`pm-analyst`（需求洞察与优先级（含受理转入的新需求））。来源分层收集需求 → 入需求池 → 分级排序 → 立项输出范围与风险；不臆造；本步只做该角色职责；越界交回或升级。
- **上游**：无（链首）
- **后续**：`go`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：发现与机会评估
- **产出**：{workroot}/{ver}/10-requirements/立项书-{yyyyMMdd}.md

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_understanding`**：出示【理解复述】（谁/场景/问题/现有替代/代价/目标/范围/非目标/证据/假设）+【推荐方案要点】（主路径/关键rules/异常期望/验收口径/不做）+ 缺口清单；涉及换迭代/相对上版时附**本期差量要点**（增/改/删或「首版全部为增」）。用户须对理解与方案均表态；仅回 OK 未对复述/方案表态不算过；确认后才分诊/入池承诺/写正式 PRD/计划/排期
- **条件判定 `hitl:understanding_needs_confirm`**：输入为模糊/单点需求、含外部文档或原型、存在实质冲突、方案有取舍、或 P1↑/P2/P3/点名写 PRD/计划/收集需求时需确认**理解+方案要点**；已有**当前任务**理解与方案双确认记录/已确认受理单（含方案要点）、或信息完整的缺陷单/答疑且已能复述且无新方案取舍时假；满足→真，否则跳过该门。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`zero-to-one-product-definition`、`customer-needs-discovery` → 见 §6 闭环。

### 本步动作清单

- 市场 用户 竞品 问题验证。
- 技能见 §6 `zero-to-one-product-definition` + §6 `customer-needs-discovery`（先读再做）。
- 竞品向另按 `competitive-intelligence-and-learning` 技能 **模式 S**（命中时打开）。
- **先问题后方案再确认**：按 先查事实。
- 仍不明一次一问（附候选/推荐）。
- 未确认不升格。
- **未双确认不得**提 Go 写全量 PRD。
- 产出须含谁/场景/问题/代价/目标/非目标/方案要点/承诺信号。
- 单个客户/竞品/领导说法标样本与证据等级。
- 访谈/综合用 `interview-guide-template.md`/`insight-synthesis-template.md`。
- **竞品（模式 S，0→1 默认）**：有 ≥2 可指认竞品/替代或战略定位需要时，落盘 `竞品分析-{主题}-{yyyyMMdd}.md`（`competitor-analysis-template.md`）。
- 学习决策表 **≥3 条**（借/改编/不借）回写立项书。
- 无公开竞品则写替代方案 +「待补竞品集」。
- 禁只交功能对标矩阵代替选择性学习（对标跟进属迭代 `prd.benchmark`）。
- **来源扇出**（子代理编排 ）：≥4 独立来源 → 按来源只读扇出（市场/用户/竞品/问题），各返回证据表/去重键 ≤30 行。
- 立项书与 Go/Hold/Kill 集中。
- 单来源直做。
- 产出立项书：`{workroot}/{ver}/10-requirements/立项书-{yyyyMMdd}.md`（模板 `rules/templates/10-planning/business-case-template.md`）。
- 引用可回查（来源 + 日期）。
- 禁臆造市场数据与用户反馈。
- 无依据写「待验证」。
- 能力（可选）：browser-mcp 竞品、analytics 数据、docs-mcp 资料。
- 未装 = 降级。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → 读必做，并读现场处置/判定/反合理化（技能有这些节时）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `zero-to-one-product-definition` | **必开** | 进入本步即开（质量不降） | `skills/zero-to-one-product-definition/SKILL.md` | 只读 L11-L18（硬门槛+方法）→ 回本包 |
| `customer-needs-discovery` | **必开** | 进入本步即开（质量不降） | `skills/customer-needs-discovery/SKILL.md` | 只读 L13-L24（硬门槛+方法）→ 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/10-planning/business-case-template.md`；只读本步用到的节，禁止整文件通读。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:new-product | step=discover | agent=pm-analyst | packet=rules/packets/new-product/discover.md | global=ok | skills=zero-to-one-product-definition,customer-needs-discovery|done|na | claim=ALLOWED|DENIED|na | next=…
```
