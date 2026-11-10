# 步骤卡 · handoff/compose

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（每步先读并逐条过）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`handoff` / `compose`（写交接单文档）
- **packet**：`rules/packets/handoff/compose.md`
- **角色**：`pm-lead`。按本步目标与 §5 动作执行；本步只做该角色职责；越界交回或升级。
- **上游**：无（链首）
- **后续**：`send`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：写交接单文档
- **产出**：自洽交接单文档（默认非 HO；落 outbound/{category}/；同轮记 handoff-ledger.md）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：每步读 `rules/core/global-rules.md` 并逐条过；本步未读不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_intent`**：仅当 `intent_needs_confirm`：出示【意图理解】，确认后才落盘。意图已清 → 跳过（可一行回执即做）。细则 `clarification.md` §0。≠ `confirm_understanding`；≠ `confirm_handoff`
- **条件判定 `hitl:intent_needs_confirm`**：口令/上下文对「给谁·做什么·交付形态」**无法唯一确定**，或跨角色外发handoff/确认文且本任务未对齐，或新开对外交付主题；满足→真，否则跳过该门。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- **默认入口**。
- 读 内容优先、包按需。
- 未回执不得称已接收 与 `handoff-note-template.md`（择优，非填空卷）。
- **意图择优**：先判 `intent_needs_confirm`（澄清方法见 clarification）。
- 真 → 完整【意图理解】停等再落盘。
- 假 → 一行【意图】回执后直写。
- 禁止含糊「交接」直接成文。
- 五问→形态 A/B/C 或专模。
- 禁止整表粘贴。
- 确认类优先 B 一页纸。
- 专模真源写版本目录，同轮实拷 `{workroot}/handoff/outbound/{category}/`。
- 无专模直接写出站类。
- 不建 HO。
- 禁外印元数据。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/90-handoff/handoff-note-template.md`；只读本步用到的节，禁止整文件通读。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:handoff | step=compose | agent=pm-lead | packet=rules/packets/handoff/compose.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
