# 步骤包 · handoff/send

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-development
- **workflow**：`handoff`
- **step**：`send`（生成交接包）
- **packet**：`rules/packets/handoff/send.md`
- **角色**：`iterate-lead`（迭代交付编排）。方案/需求 → 任务清单（含 DoR/DoD）→ 确认节奏 → 编排实施（实施交 implementer）→ 评审/门禁 → 提测 → 总结拟提交；本步只做该角色职责；越界交回或升级。
- **上游**：`compose`（取其产出为本步输入；该步被 `when` 跳过时按缺口停/补齐）
- **后续**：`receive`
- **失败去向**：缺 00/01/快照/占位符/链接断 → 不发送；补后重跑校验
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/handoff/_chain.md`（进 workflow 一次）。

## 2. 本步目标

- **目标**：生成交接包
- **产出**：{workroot}/handoff/outbound/{category}/{HO-ID}/ + 【交接包已生成】

## 3. 本步硬约束

### 开局硬门（3 条；其余见 cold-start §1）

- 1. **每轮先判、再动手**：先判新任务/续跑/只读；新任务或范围变化 → 复述目标/范围/验收并确认；续跑一行确认；只读一句话；首行锚 `route/step/packet` 或 `mode=analyze`；未确认禁写、禁下结论。
- 7. **完成只认门**：`-Claim` → `CLAIM: ALLOWED`；无 ALLOWED 禁写完成/通过/可提测。有 UI → 当前包内前端硬门；无 UI 标 `na`。
- 11. **技能闭环**：§6 必开 skill 打开→执行→回包；禁止粘贴代替。
- 其余硬约束见 `rules/core/cold-start.md` §1（常驻；勿在步内重读全文）。

### 本步读链与防丢失

- **编排**：本文 §5 +（若 §7 列出）一个模板。
- **方法质量**：§6 必开/条件开技能 → **逐个打开→执行→回本包**（一次 1 个）；禁止用粘贴代替实读。
- **禁止**：通读 rules / 多 step packet / 预读本 workflow 全部 skill。
- **完成声称**：有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **上下文锚**：`packet=`/`reads=` 必须含本 packet；切步/出子机前心跳刷新。

### 本步禁止

- 禁止读取本清单外的 rules / skills 正文；需要跳转只按 §6/§7 各一次。
- 禁止跳过 §6 必开技能，或用摘要代替实读。
- 禁止未过 §4 门或未出 §8 信号就宣称完成、推进或写「已通过」。

## 4. 本步门

- **HITL `confirm_handoff`**：**凡拟生成任一 HO 包必停**：出示类型/接收方/必带摘要/阻断/传递方式；用户确认后才落盘；未确认零发包。禁止用「定稿门/评审门/发布门已过」代替本门。未收回执不得称「已接收」；可称「已发送」
- **推进**：本步完成后沿父链进入下一未跳过步；口令为单步（只出方案/只评审/代码评审/方案评审/只提测/只出清单/轻量方案）或动作清单写明停止/跳转时，以口令/清单为准，即停并输出收尾骨架。

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- **仅升包**。先读 包触发与 类别。
- 未命中 → 改走 `compose`，不得生 HO。 **先问后发**：`confirm_handoff` 出示【拟发包】。
- 用户确认「要包」后才写盘到 `handoff/outbound/{category}/{HO-ID}/`。
- 未确认零发包。 确认后：完整包 `00/01/02/03/04`。
- 刷新出站散文件实拷。
- 跑 `validate_handoff.py` → 台账已发送。 回执默认仍可选。
- 仅正式签收/C2·C3/发布要求填写。 传递：多包同仓直读出站路径。
- 仓外文件夹或 ZIP。输出【交接包已生成】。

本步不嵌入前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回本包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/handoff/_chain.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:handoff | step=send | agent=iterate-lead | packet=rules/packets/handoff/send.md | reads=rules/packets/handoff/send.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/handoff/send.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
