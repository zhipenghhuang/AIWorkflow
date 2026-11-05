# 步骤包 · defect/writeback

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：产品
- **workflow**：`defect`
- **step**：`writeback`（平台回写）
- **packet**：`rules/packets/defect/writeback.md`
- **条件步** `when=remark_writeback`：条件不满足则跳过本步（不打开本包）。
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/defect/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/defect/_region-act.md`（处置回写；进本区一次）。

## 2. 本步目标

- **目标**：平台回写
- **产出**：平台回写结果（备注/附件/状态/指派）

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

- **HITL `confirm_remark`**：出示 id+结论+备注全文+附件名+状态/指派变更；备注与状态同轮；平台不支持出 export
- **GATE `writeback-receipt`**：`Invoke-Gate.ps1 -Mode writeback -Artifact …`；单号+备注实质+状态取值+fileId/无附件；禁标题刷绿；无回执不得声称已回写

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`change-management` → 见 §6 闭环。

### 本步动作清单

- 按 `rules/templates/30-review-change/defect-writeup-template.md` /：回写前出示 id、来源、结论、备注全文、附件名、 状态/指派变更、目标版本。
- 确认后执行。 运行 `verify/Invoke-Gate.ps1 -Mode writeback`。
- 无回执/备注状态不同轮/附件未回查 → 不得声称已回写。 未配置平台/无权限 → 先回 preflight。
- 无既有分析/结论 → 回 pull/analyze，不凭空回写。
- 只改字段未分析 → 先补分析。 备注与状态同轮。
- 备注写分诊依据/处置结论/影响 AC/目标版本/下一步/需要谁做什么。
- 回写内容由编排集中生成。
- 子代理只提供事实素材，不写平台、不改状态。 禁密钥/绝对路径/用例路径。 附件上传后回查挂载。
- 失败重试≤1，禁删缺陷。平台不支持/无权限 → 出 export 包，标「待回写」。 指派：产品缺陷/实现缺陷→开发。
- 非问题/重复/信息不足按来源→测试或开发。
- 补充信息/信息不足→提交人/测试/开发（按来源）。目标版本/截止写清。 回写后更新受理单 /。

## 6. 技能指向（打开 → 执行 → 回本包）

> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  
> 同时只打开 **1** 个 skill；打开期间 `reads=` 可暂加该 skill 路径，闭环结束后以本 packet 为准。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `change-management` | **必开** | 进入本步即开（质量不降） | `skills/change-management/SKILL.md` | 必做区 → 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

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
route=workflow:defect | step=writeback | packet=rules/packets/defect/writeback.md | reads=rules/packets/defect/writeback.md[+skill] | skills=change-management|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/defect/writeback.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
