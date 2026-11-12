# 步骤卡 · new-product/define

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`new-product` / `define`（产品定义与计划）
- **packet**：`rules/packets/new-product/define.md`
- **角色**：`pm-analyst`（需求洞察与优先级（含受理转入的新需求））。来源分层收集需求 → 入需求池 → 分级排序 → 立项输出范围与风险；不臆造；本步只做该角色职责；越界交回或升级。
- **上游**：`go`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`prd`（进 `prd` 前的 `when=go_decision_go`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:go_decision_go`**：立项结论=Go（Hold/Kill=false）；满足→真，否则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：产品定义与计划
- **产出**：{workroot}/product-plan.md

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_plan`**：首次计划或范围·指标·版本实质变更：目标/路线图/本期范围/**§3.0 Brief+差量表** /里程碑/风险摘要；无差量表（且非明示首版一行）不过门；未确认不进 PRD/排期
- **条件判定 `hitl:plan_needs_confirm`**：首次计划或范围·指标·版本实质变更；满足→真，否则跳过该门。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`zero-to-one-product-definition` → 见 §6 闭环。

### 本步动作清单

- **子链**：按 `plan` 流程 逐步执行（只读子 workflow **当前 step 块**；goals→roadmap→scope→review→publish）。
- **门权威在子链**：`confirm_understanding` `confirm_plan` 评审门以 plan.yaml 步上 hitl 为准。
- 本步不另造门、不重复弹已确认门。
- 落盘 `{workroot}/product-plan.md`。
- 只写总领（做什么 为什么 何时 怎么算成功），需求细节归 PRD。
- 子链 closeout 不执行，统一由本文件末 closeout 收尾。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。
> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `zero-to-one-product-definition` | **必开** | 进入本步即开（质量不降） | `skills/zero-to-one-product-definition/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **无强制模板**：§5 编排已给出动作/顺序；直接落 §2 产出。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:new-product | step=define | agent=pm-analyst | packet=rules/packets/new-product/define.md | global=ok | skills=zero-to-one-product-definition|done|na | claim=ALLOWED|DENIED|na | next=…
```
