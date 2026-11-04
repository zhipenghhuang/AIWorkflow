# 步骤包 · onboard/control

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`onboard`
- **step**：`control`（开发计划）
- **packet**：`rules/packets/onboard/control.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：开发计划
- **产出**：开发计划（{workroot}/development-plan.md）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- L2+ 新项目/新产品默认建：技能 `skills/development-plan/SKILL.md`；模板 `rules/templates/10-planning/development-plan-template.md`。 填一页状态/输入/阶段表（S0 进行中，其余未开始）/关联链接；已有则不覆盖，读现状后转 control sync。 存量项目（已有版本/迭代/代码）→ 按现状回填当前阶段 Sx 与门，不默认从 S0 重跑；缺口写 。 L0/L1 可写「不适用」或轻量开发卡；不强制引用其它包。 输入缺口写 ，由用户提供/选择已有资料，不阻塞打标。

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

L2+ 新项目/新产品默认建：技能 `skills/development-plan/SKILL.md`；模板 `rules/templates/10-planning/development-plan-template.md`。 填一页状态/输入/阶段表（S0 进行中，其余未开始）/关联链接；已有则不覆盖，读现状后转 control sync。 存量项目（已有版本/迭代/代码）→ 按现状回填当前阶段 Sx 与门，不默认从 S0 重跑；缺口写 。 L0/L1 可写「不适用」或轻量开发卡；不强制引用其它包。 输入缺口写 ，由用户提供/选择已有资料，不阻塞打标。

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
route=workflow:onboard | step=control | reads=rules/packets/onboard/control.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/onboard/control.md`；对不上 = 未遵守读链。
