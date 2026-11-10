# 步骤卡 · defect/search

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`defect` / `search`（查重或拉取）
- **packet**：`rules/packets/defect/search.md`
- **角色**：`bug-agent`（缺陷平台协作）。查重/提交/回归/回写按专规；备注与状态同轮；读者=开发/产品；本步只做该角色职责；越界交回或升级。
- **上游**：`classify`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`submit`（进 `submit` 前的 `when=defect_submit_required`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：查重或拉取
- **产出**：查重键/拉取快照 + diff 摘要（单号/变化/证据缺口）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：按 `rules/core/global-rules.md` §7 重读并遵守全文；心跳 `global=ok` 表示本步已按 §7 复核；未按 §7 复核不得写 `global=ok`。偏离写 `global=dev:<原因>`。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 提交前查重。
- 回归/巡检拉单读 status/resolution/assignedTo/resolvedBuild/actions/files/lastEditedDate，按 缺陷协作 做快照 diff。
- api 读不全 → browser。
- 仍不全 → 请用户补关键备注/附件，禁只看标题分析。
- 批量查重/快照 diff：达只读扇出阈值则按单扇出，未拆记 deviation。
- 主上下文只收「单号/变化/查重键/证据缺口」≤30 行，判定/复测/回写集中。
- 复测同账号写域禁并行。

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
route=workflow:defect | step=search | agent=bug-agent | packet=rules/packets/defect/search.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
