# 步骤包 · defect/verify

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：产品
- **workflow**：`defect`
- **step**：`verify`（验证与关闭）
- **packet**：`rules/packets/defect/verify.md`
- **条件步** `when=needs_linked_update`：条件不满足则跳过本步（不打开本包）。
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/defect/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/defect/_region-act.md`（处置回写；进本区一次）。

## 2. 本步目标

- **目标**：验证与关闭
- **产出**：验证结果 + 批末总结

## 3. 本步硬约束

### 开局硬约束（本步可执行摘要）

- 1. **先意图、再动作**（`confirm_task_intent`）：未确认禁写正式 PRD/外发/定范围。
- 2. **短读跟随 + 一手源**：`activeContext` + 进行中（`packet=`/`region=`）+ 偏好/洞见/坑 ≤3。
- 3. **理解→方案双确认未完成 → 不得入池/写正式 PRD/定版本范围**。
- 4. **状态机读链 + 技能闭环**：见本包「本步读链与防丢失」。必开 skill 须打开→执行→回步骤包（质量不降）。
- 5. **完成分层**：`-Claim -Mode <…>` → 只认 `CLAIM: ALLOWED`。
- 6. **原型硬门**：实走 + 覆盖矩阵；缺行不得过。
- 7. **禁臆造**；AC 可观测；变更无单不实施；UAT 未过不发布。
- 8. **切步/出子机 → 心跳**，必带 `packet=`。

### 本步读链与防丢失

- **编排**：本文 §5 +（若 §7 列出）一个模板。
- **方法质量**：§6 必开/条件开技能 → **打开→执行→回本包**（同时 1 个 skill）；禁止用粘贴代替实读。
- **禁止**：通读 rules / 多 step packet / 预读本 workflow 全部 skill。
- **完成声称**：有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **上下文锚**：`packet=`/`reads=` 必须含本 packet；切步/出子机前心跳刷新。


## 4. 本步门

- **GATE `change-closure`**：运行 `verify/Invoke-Gate.ps1 -Mode change`；§6 每项“已更新/不适用/待补”，待补有责任人/截止；未闭合不得关闭

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- **单一出处**：通用联动/关闭规则以 `workflows/change.yaml` verify 为准。
- 本步只保留缺陷平台差异。 运行 `verify/Invoke-Gate.ps1 -Mode change`（读 `.gate/wf-product/change.json`）。
- 受理单联动清单未闭合、验证结果缺失 → 不得关闭。 未 READY → **保持受理单打开，不得进入 wrap/commit 冒充完成**。
- 先补联动/证据或报阻塞。 按 `rules/defects/platform-collaboration.md` + `rules/templates/30-review-change/defect-writeup-template.md` ： 产品缺陷 → 受影响 AC/UAT 重验。
- 开发完成新文档实施后验证。
- 未验证不关单。 实现缺陷 → 产品侧回执后由开发/测试流程跟踪。
- 产品侧不写「已修复」。 非问题/重复/信息不足 → 产品给依据。
- 测试接受后关闭或转需求。
- 未接受转产品复核。 下版 → 回池/路线图。
- 不修 → 理由/接受人。
- 退回开发 → 回执，缺陷状态由开发/测试跟踪。 验证通过后需再次回写平台（入口 writeback）更新状态/关闭。
- 批末输出【产品缺陷协作总结】。

## 6. 技能指向（打开 → 执行 → 回本包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/defect/_chain.md`。
- 子状态机（进区一次）：`rules/packets/defect/_region-act.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 验证：`verify/Invoke-Gate.ps1`（完成声称加 `-Claim`）；有 UI 另按 §5 前端硬门。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:defect | step=verify | packet=rules/packets/defect/verify.md | reads=rules/packets/defect/verify.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/defect/verify.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
