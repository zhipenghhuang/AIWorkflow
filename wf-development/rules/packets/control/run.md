# 步骤包 · control/run

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`control`
- **step**：`run`（按计划执行）
- **packet**：`rules/packets/control/run.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：按计划执行
- **产出**：当前阶段执行结果 + 开发计划回写

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 读 `{workroot}/development-plan.md` //：确认计划状态、当前阶段、当前门、下一动作、需人工项。 计划状态非「已确认/执行中」→ 先回 init/confirm_plan；有未吸收新输入 → 先走 `workflows/intake.yaml`。 按当前阶段路由：S0/S1 走 `change` analyze_input（有 PRD/原型）/clarify/requirements；S2 走 `change` design；S3 走 `iterate` plan/confirm； S4/S5 走 `change` implement/review/verify 或 `iterate` implement/review/gates；S6 走 `change`/`iterate` 的 deliver 步； S7 走defects/测试报告（可选输入）；S8 走 `release`；S9 走 `retro`。执行到下一个 `hitl` 停止，不跳门。 进入/切换任务前检查工作区；有前序未提交 → 输出【基线检查】先提交/隔离/记录例外；未提交默认不得开始下一任务（例外=基线检查选项 C/D 且用户确认）；任务边界 dirty 时先停。 上游包未签收/退回 → 先走 `workflows/handoff.yaml` receive，不进入实施；本阶段发出包未回执 → 只能准备下一步，不得标阶段完成。 多波次：先确认计划选“每波独立评审+过门”或“整迭代只过 S5 全量评审”；不得混用；S5 已有波次评审时做集成/AC/证据/抽样复核，不逐行重审。 每步结束回写： 计划状态/当前门/下一动作/健康度； 阶段状态/证据/下一步；// 对应节； 执行日志（含 HO/回执）。 缺证据不得标完成；门结论写「通过/不通过/有条件通过 + 批准人/日期/条件」。 开发包独立运行；产品/测试**他包产物**可选，缺则一句缺口并用本包模板补，不因缺他包阻塞。 **不降标**：AC/产品最小判断/完成门/开发自验不可因「单人/无 QA」省略（`rules/core

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 技能 `development-plan`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「计划可以后补」 | L2+ 无计划则阶段/门/下一动作失真；先建再跑。 |
| 「阶段表技能列可空」 | 每阶段至少挂一个技能；空列=加载失败。 |
| 「状态只改 activeContext」 | 计划 §0 / 索引 / 进行中三处同拍。 |
### 编排备忘

读 `{workroot}/development-plan.md` //：确认计划状态、当前阶段、当前门、下一动作、需人工项。 计划状态非「已确认/执行中」→ 先回 init/confirm_plan；有未吸收新输入 → 先走 `workflows/intake.yaml`。 按当前阶段路由：S0/S1 走 `change` analyze_input（有 PRD/原型）/clarify/requirements；S2 走 `change` design；S3 走 `iterate` plan/confirm； S4/S5 走 `change` implement/review/verify 或 `iterate` implement/review/gates；S6 走 `change`/`iterate` 的 deliver 步； S7 走defects/测试报告（可选输入）；S8 走 `release`；S9 走 `retro`。执行到下一个 `hitl` 停止，不跳门。 进入/切换任务前检查工作区；有前序未提交 → 输出【基线检查】先提交/隔离/记录例外；未提交默认不得开始下一任务（例外=基线检查选项 C/D 且用户确认）；任务边界 dirty 时先停。 上游包未签收/退回 → 先走 `workflows/handoff.yaml` receive，不进入实施；本阶段发出包未回执 → 只能准备下一步，不得标阶段完成。 多波次：先确认计划选“每波独立评审+过门”或“整迭代只过 S5 全量评审”；不得混用；S5 已有波次评审时做集成/AC/证据/抽样复核，不逐行重审。 每步结束回写： 计划状态/当前门/下一动作/健康度； 阶段状态/证据/下一步；// 对应节； 执行日志（含 HO/回执）。 缺证据不得标完成；门结论写「通过/不通过/有条件通过 + 批准人/日期/条件」。 开发包独立运行；产品/测试**他包产物**可选，缺则一句缺口并用本包模板补，不因缺他包阻塞。 **不降标**：AC/产品最小判断/完成门/开发自验不可因「单人/无 QA」省略（`rules/core/lightweight.md` ）。 输出首条：route=workflow:control | step=run | stage=… | gate=… | next_action=…

## 6. 打开/填写

- 运行时正文：仅本文件（开局卡已在会话开头读过）。
- 无强制模板：直接写 §2 产出路径产物。

## 7. 完成信号

- §2 产出已落盘。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 8. 回执字段

```text
route=workflow:control | step=run | reads=rules/packets/control/run.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/control/run.md`；对不上 = 未遵守读链。
