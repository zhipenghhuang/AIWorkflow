# 步骤卡 · handoff/send

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`handoff` / `send`（生成交接包）
- **packet**：`rules/packets/handoff/send.md`
- **角色**：`iterate-lead`。按本步目标与 §5 动作执行；本步只做该角色职责；越界交回或升级。
- **上游**：`compose`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`receive`
- **失败去向**：缺 00/01/快照/占位符/链接断 → 不发送；补后重跑校验

## 2. 本步目标

- **目标**：生成交接包
- **产出**：{workroot}/handoff/outbound/{category}/{HO-ID}/ + 【交接包已生成】

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_handoff`**：**凡拟生成任一 HO 包必停**：出示类型/接收方/必带摘要/阻断/传递方式；用户确认后才落盘；未确认零发包。禁止用「定稿门/评审门/发布门已过」代替本门。未收回执不得称「已接收」；可称「已发送」
- **条件判定 `hitl:handoff_send_required`**：拟生成/点名 HO 且未确认类型/接收方/摘要；满足→真，否则跳过该门。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- **仅升包**。
- 先读 包触发与 类别。
- 未命中 → 改走 `compose`，不得生 HO。
- **先问后发**：`confirm_handoff` 出示【拟发包】。
- 用户确认「要包」后才写盘到 `handoff/outbound/{category}/{HO-ID}/`。
- 未确认零发包。
- 确认后：完整包 `00/01/02/03/04`。
- 刷新出站散文件实拷。
- 跑 `validate_handoff.py` → 台账已发送。
- 回执默认仍可选。
- 仅正式签收/C2·C3/发布要求填写。
- 传递：多包同仓直读出站路径。
- 仓外文件夹或 ZIP。
- 输出【交接包已生成】。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读技能库找感觉。

## 7. 模板与证据

- **填写模板（主）**：`rules/templates/90-handoff/handoff-package-brief-template.md`；只读本步用到的节，禁止整文件通读。
- **配套模板（按产出需要读；门按结构判分的产物须对齐）**：`rules/templates/90-handoff/handoff-checklist-template.md`。
- **产出前自检**：对照模板必填节逐项填写；缺节、空节、未替换 `{…}` = 不合格（不得标完成）。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- §2 产出已按模板必填节落地；无空节、无未替换占位符。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:handoff | step=send | agent=iterate-lead | packet=rules/packets/handoff/send.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
