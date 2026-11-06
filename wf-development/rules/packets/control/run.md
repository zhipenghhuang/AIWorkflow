# 步骤包 · control/run

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-development
- **workflow**：`control`
- **step**：`run`（按计划执行）
- **packet**：`rules/packets/control/run.md`
- **角色**：`iterate-lead`（迭代交付编排）。方案/需求 → 任务清单（含 DoR/DoD）→ 确认节奏 → 编排实施（实施交 implementer）→ 评审/门禁 → 提测 → 总结拟提交；本步只做该角色职责；越界交回或升级。
- **上游**：`init`（取其产出为本步输入；该步被 `when` 跳过时按缺口停/补齐）
- **后续**：`sync`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/control/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/control/_region-steer.md`（总控推进；进本区一次）。

## 2. 本步目标

- **目标**：按计划执行
- **产出**：当前阶段执行结果 + 开发计划回写

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

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。
- **推进**：本步完成后沿父链进入下一未跳过步；口令为单步（只出方案/只评审/代码评审/方案评审/只提测/只出清单/轻量方案）或动作清单写明停止/跳转时，以口令/清单为准，即停并输出收尾骨架。

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`development-plan` → 见 §6 闭环。

### 本步动作清单

- 读 `{workroot}/development-plan.md`：确认计划状态、当前阶段、当前门、下一动作、需人工项。 计划状态非「已确认/执行中」→ 先回 init/confirm_plan。
- 有未吸收新输入 → 先走 `workflows/intake.yaml`。 按当前阶段路由：S0/S1 走 `change` analyze_input（有 PRD/原型）/clarify/requirements。
- S2 走 `change` design。
- S3 走 `iterate` plan/confirm。
- S4/S5 走 `change` implement/review/verify 或 `iterate` implement/review/gates。
- S6 走 `change`/`iterate` 的 deliver 步。
- S7 走defects/测试报告（可选输入）。
- S8 走 `release`。
- S9 走 `retro`。执行到下一个 `hitl` 停止，不跳门。 进入/切换任务前检查工作区。
- 有前序未提交 → 输出【基线检查】先提交/隔离/记录例外。
- 未提交默认不得开始下一任务（例外=基线检查选项 C/D 且用户确认）。
- 任务边界 dirty 时先停。 上游包未签收/退回 → 先走 `workflows/handoff.yaml` receive，不进入实施。
- 本阶段发出包未回执 → 只能准备下一步，不得标阶段完成。 多波次：先确认计划选“每波独立评审+过门”或“整迭代只过 S5 全量评审”。
- 不得混用。
- S5 已有波次评审时做集成/AC/证据/抽样复核，不逐行重审。 每步结束回写： 计划状态/当前门/下一动作/健康度。
- 阶段状态/证据/下一步。
- 对应节。
- 执行日志（含 HO/回执）。 缺证据不得标完成。
- 门结论写「通过/不通过/有条件通过 + 批准人/日期/条件」。 开发包独立运行。
- 产品/测试**他包产物**可选，缺则一句缺口并用本包模板补，不因缺他包阻塞。 **不降标**：AC/产品最小判断/完成门/开发自验不可因「单人/无 QA」省略（`rules/core/lightweight.md` ）。 输出首条：route=workflow:control | step=run | stage=… | gate=… | next_action=…。

本步不嵌入前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回本包）

> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `development-plan` | **必开** | 进入本步即开（质量不降） | `skills/development-plan/SKILL.md` | 必做区 → 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/control/_chain.md`。
- 子状态机（进区一次）：`rules/packets/control/_region-steer.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:control | step=run | agent=iterate-lead | packet=rules/packets/control/run.md | reads=rules/packets/control/run.md[+skill] | skills=development-plan|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/control/run.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
