# 步骤包 · control/next

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`control`
- **step**：`next`（下一步建议）
- **packet**：`rules/packets/control/next.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：下一步建议
- **产出**：当前阶段/下一步 3 件事/建议入口

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 本步只读建议，不执行阶段；要执行说「按开发计划执行」。 先确认 `inbound/`、`{workroot}/INDEX.md` 无未吸收输入；有 → 建议先 `workflows/intake.yaml`/`materials`。 读 `handoff-ledger.md`：待回执/退回/有条件接收会阻塞哪些阶段，列入“需要用户决策”最前；下一步给对应 handoff.receive/send 入口。 基于开发计划给出：当前阶段、已过门、下一步 3 件事（动作+产出+截止）、建议 workflow/step。 需要用户决策的列最前；缺口不阻塞时给降级路径。 不擅自启用其它包；需要跨包资料时只提示可选输入。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 本步动作清单

- 本步只读建议，不执行阶段。
- 要执行说「按开发计划执行」。 先确认 `inbound/`、`{workroot}/INDEX.md` 无未吸收输入。
- 有 → 建议先 `workflows/intake.yaml`/`materials`。 读 `handoff-ledger.md`：待回执/退回/有条件接收会阻塞哪些阶段，列入“需要用户决策”最前。
- 下一步给对应 handoff.receive/send 入口。 基于开发计划给出：当前阶段、已过门、下一步 3 件事（动作+产出+截止）、建议 workflow/step。 需要用户决策的列最前。
- 缺口不阻塞时给降级路径。 不擅自启用其它包。
- 需要跨包资料时只提示可选输入。

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
route=workflow:control | step=next | reads=rules/packets/control/next.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/control/next.md`；对不上 = 未遵守读链。
