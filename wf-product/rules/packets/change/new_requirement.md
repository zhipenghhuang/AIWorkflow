# 步骤卡 · change/new_requirement

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`change` / `new_requirement`（新需求与优先级（条件））
- **packet**：`rules/packets/change/new_requirement.md`
- **角色**：`pm-analyst`（需求洞察与优先级（含受理转入的新需求））。来源分层收集需求 → 入需求池 → 分级排序 → 立项输出范围与风险；不臆造；本步只做该角色职责；越界交回或升级。
- **上游**：`triage`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`assess`（进 `assess` 前的 `when=needs_impact_assessment`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:new_requirement`**：分诊为新需求（不含已定稿基线的需求变更）；满足→真，否则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：新需求与优先级（条件）
- **产出**：{workroot}/requirement-pool.md 更新 + 范围结论

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_scope`**：范围（MVP）/排除项/粗排期/风险 一行摘要；条件门：仅跨版本/高价值/未确认范围时停
- **条件判定 `hitl:scope_decision_required`**：跨版本/高价值/点名立项，需单需求范围确认；满足→真，否则跳过该门。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 仅新需求。
- 入池须证据。
- confirm_scope 后进 assess/路线图。
- 细节只认技能必做。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 模板与证据

- **无强制模板**：§5 编排已给出动作/顺序；直接落 §2 产出。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:change | step=new_requirement | agent=pm-analyst | packet=rules/packets/change/new_requirement.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
