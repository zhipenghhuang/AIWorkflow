# 步骤包 · handoff/change_send

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-testing
- **workflow**：`handoff`
- **step**：`change_send`（发送变更通知）
- **packet**：`rules/packets/handoff/change_send.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/handoff/_chain.md`（进 workflow 一次）。

## 2. 本步目标

- **目标**：发送变更通知
- **产出**：{workroot}/handoff/outbound/变更/{CHG-HO-ID}/ + 更新后的测试计划/用例/脚本

## 3. 本步硬约束

### 开局硬约束（本步可执行摘要）

- 1. **先意图、再动作**（`confirm_task_intent`）：未确认禁生成正式用例/交平台。
- 2. **短读跟随 + 一手源**：`activeContext` + 进行中（`packet=`/`region=`）+ 偏好/洞见/坑 ≤3。
- 3. **依据先建模**：分析表 §0；无 §0 禁正式生成与功能准出。
- 4. **状态机读链 + 技能闭环**：见本包「本步读链与防丢失」。必开 skill 须打开→执行→回步骤包（质量不降）。
- 5. **完成分层**：`-Claim -Mode report|writeback` → 只认 `CLAIM: ALLOWED`。
- 6. **UI 证据 E1**：实点 + 截图/Network；E0 不得单独 pass。
- 7. **能脚本不 AI**；禁刷绿；P0 未过不得整体通过。
- 8. **切步/出子机 → 心跳**，必带 `packet=`。

### 本步读链与防丢失

- **编排**：本文 §5 +（若 §7 列出）一个模板。
- **方法质量**：§6 必开/条件开技能 → **打开→执行→回本包**（同时 1 个 skill）；禁止用粘贴代替实读。
- **禁止**：通读 rules / 多 step packet / 预读本 workflow 全部 skill。
- **完成声称**：有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **上下文锚**：`packet=`/`reads=` 必须含本 packet；切步/出子机前心跳刷新。


## 4. 本步门

- **HITL `confirm_plan`**：版本级首版/换代或范围·准出·缺陷提交策略实质变更 → STOP 一行摘要确认；同会话同载体只一次；专项轻量不设门。版本级须先过：分析表 §2.2/§2.3 无空格 + §2.4 依据覆盖无缺行 + §3.8 四卷 + §3.9 批次表；缺项=计划门不通过
- **HITL `confirm_handoff`**：**凡拟生成任一 HO 或缺陷统一导出必停**：出示类型/接收方/必带摘要/落点（缺陷须写清「本批一份单文件或单 EXPORT 目录」）/阻断/传递方式；用户确认后才落盘；未确认零发包。禁止用「报告门/计划门/批末/平台已交」代替本门。有平台交缺陷 → 本门不因「补导出」置真。未收回执不得称「已接收」；可称「已发送」

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 先按 `workflows/testing.yaml` 的 plan 期中变更完成 CR/影响分析。
- 本步只负责“通知包”。 按 `rules/collaboration/handoff.md` 判 C0/C1/C2/C3。
- C2/C3 必须先过计划门。 **CHG 包同样先问后发**：`confirm_handoff` 出示拟发摘要，用户确认后才生成 HO 包。 必带：CR、影响矩阵、更新后的计划/用例/脚本/报告、接收方必须做的事/截止、回归范围、生效版本。 受影响角色逐个发（产品/开发）。
- 同一变更一个包可多接收方，但回执逐个登记。 更新 `handoff-ledger.md`、测试计划 //、 `{workroot}/INDEX.md`、activeContext。
- 输出【变更通知已生成】+ 回执截止。 未确认不得发。
- 不得用口头/聊天替代变更包。

## 6. 技能指向（打开 → 执行 → 回本包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/handoff/_chain.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:handoff | step=change_send | packet=rules/packets/handoff/change_send.md | reads=rules/packets/handoff/change_send.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/handoff/change_send.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
