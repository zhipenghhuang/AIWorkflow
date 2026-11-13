# 步骤卡 · handoff/change_receive

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`handoff` / `change_receive`（接收变更并适配）
- **packet**：`rules/packets/handoff/change_receive.md`
- **角色**：`pm-lead`。按本步目标与 §5 动作执行；本步只做该角色职责；越界交回或升级。
- **上游**：`change_send`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`replan`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。

## 2. 本步目标

- **目标**：接收变更并适配
- **产出**：变更影响分析 + 产品计划/文档调整 + 回执

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_change`**：出示分诊依据、影响与变更单要点（**含 §2.1 差量表** Now→Proposed）；产品缺陷须有相符证明；无单不实施
- **条件判定 `hitl:handoff_change_substantive`**：交接包内变更达 C2/C3 或改定稿基线；满足→真，否则跳过该门。
- **HITL `confirm_plan`**：首次计划或范围·指标·版本实质变更：目标/路线图/本期范围/**§3.0 Brief+差量表** /里程碑/风险摘要；无差量表（且非明示首版一行）不过门；未确认不进 PRD/排期
- **条件判定 `hitl:plan_level_change`**：影响版本范围/里程碑/KPI；满足→真，否则跳过该门。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 读变更包 00/01/02。
- 按 `rules/collaboration/handoff.md` 判级别。
- 核对变更单、影响矩阵、生效版本、回滚/兼容。
- 先做影响分析：PRD/AC、原型、范围/优先级、里程碑、UAT/发布、需求池、通知对象。
- C0 → 就地更新并书面答复。
- C1 → 更新受影响文档/计划，回执。
- C2/C3 → 重基线并过门，必要时反向发 `CHG`。
- 更新 `handoff-ledger.md`、产品计划、 `{workroot}/INDEX.md`、activeContext。
- 填写回执。
- 与现有 PRD/计划冲突 → 列冲突，不静默选一边。
- 未裁决前不进入实施/排期。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读技能库找感觉。

## 7. 模板与证据

- **无强制模板**：§5 编排已给出动作/顺序；直接落 §2 产出。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:handoff | step=change_receive | agent=pm-lead | packet=rules/packets/handoff/change_receive.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
