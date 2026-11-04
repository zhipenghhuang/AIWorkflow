# 步骤包 · defect-fix/retro

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`defect-fix`
- **step**：`retro`（复盘）
- **packet**：`rules/packets/defect-fix/retro.md`
- **条件步** `when=recurring_defect_or_incident`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：复盘
- **产出**：复盘（{workroot}/80-retrospectives/）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 条件步：重复defects/事故/回滚才走；技能 skills/retrospective-and-improvement/SKILL.md，模板 rules/templates/60-retro/retro-template.md。 行动项必须有负责人/截止/验收；进任务清单或 {workroot}/80-retrospectives/改进项.md。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 技能 `retrospective-and-improvement`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「没出事就不用复盘」 | 重大发布/回滚/事故必复盘；改进项须可执行负责。 |
| 「复盘写成流水账」 | 要根因+动作+验收；禁只抒情。 |
| 「改进以后再说」 | 无主人和日期的动作=未立项。 |
### 编排备忘

条件步：重复defects/事故/回滚才走；技能 skills/retrospective-and-improvement/SKILL.md，模板 rules/templates/60-retro/retro-template.md。 行动项必须有负责人/截止/验收；进任务清单或 {workroot}/80-retrospectives/改进项.md。

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
route=workflow:defect-fix | step=retro | reads=rules/packets/defect-fix/retro.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/defect-fix/retro.md`；对不上 = 未遵守读链。
