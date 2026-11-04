# 步骤包 · iterate/confirm

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`iterate`
- **step**：`confirm`（确认清单与节奏）
- **packet**：`rules/packets/iterate/confirm.md`
- **条件步** `when=implementation_required`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：确认清单与节奏
- **产出**：已确认清单/节奏

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 清单未变可跳过 hitl；L1 notify、L2+ 实质变化 approve。确认后冻结；变更记清单 。

## 4. 本步门

- **HITL `confirm_backlog`**：出示任务数/RP 覆盖/依赖/风险 + 节奏三选；确认后才实施

## 5. 做法

### 本步动作清单

- 清单未变可跳过 hitl。
- L1 notify、L2+ 实质变化 approve。确认后冻结。
- 变更记清单 。

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
route=workflow:iterate | step=confirm | reads=rules/packets/iterate/confirm.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/iterate/confirm.md`；对不上 = 未遵守读链。
