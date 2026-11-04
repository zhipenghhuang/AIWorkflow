# 步骤包 · handoff/change_receive

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`handoff`
- **step**：`change_receive`（接收变更并适配）
- **packet**：`rules/packets/handoff/change_receive.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：接收变更并适配
- **产出**：变更影响分析 + 开发计划/文档调整 + 回执

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 读变更包 00/01/02；按 判级别；核对变更单、影响矩阵、生效版本、回滚/兼容。 先做影响分析：需求/AC、原型/设计、架构/DB/API/前端、任务/排期、测试/发布、依赖。 更新需求基线/方案/ADR/任务清单/开发计划；C0 就地更新并答复；C1 更新并回执；C2/C3 重基线并过门，必要时反向发 `CHG`。 更新 `handoff-ledger.md`、开发计划 //////、 `{workroot}/INDEX.md`、activeContext；填写回执。 与现有方案/代码冲突 → 列冲突，不静默选一边；未裁决前不实施。

## 4. 本步门

- **HITL `confirm_change`**：出示变更类型/影响矩阵/待更新文档/待确认项；实质变更确认后才更新基线
- **HITL `confirm_plan`**：首次创建或范围·版本·里程碑实质变更；确认后计划状态=已确认

## 5. 做法

### 本步动作清单

- 读变更包 00/01/02。
- 按 判级别。
- 核对变更单、影响矩阵、生效版本、回滚/兼容。 先做影响分析：需求/AC、原型/设计、架构/DB/API/前端、任务/排期、测试/发布、依赖。 更新需求基线/方案/ADR/任务清单/开发计划。
- C0 就地更新并答复。
- C1 更新并回执。
- C2/C3 重基线并过门，必要时反向发 `CHG`。 更新 `handoff-ledger.md`、开发计划 //////、 `{workroot}/INDEX.md`、activeContext。
- 填写回执。 与现有方案/代码冲突 → 列冲突，不静默选一边。
- 未裁决前不实施。

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
route=workflow:handoff | step=change_receive | reads=rules/packets/handoff/change_receive.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/handoff/change_receive.md`；对不上 = 未遵守读链。
