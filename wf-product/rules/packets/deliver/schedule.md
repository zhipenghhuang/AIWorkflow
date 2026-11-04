# 步骤包 · deliver/schedule

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`deliver`
- **step**：`schedule`（排期与交接）
- **packet**：`rules/packets/deliver/schedule.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：排期与交接
- **产出**：{workroot}/{ver}/40-delivery/交付计划-{ver}.md（模板 rules/templates/40-delivery/delivery-plan-template.md）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 技能：`skills/change-management/SKILL.md`（先读；排期与变更纪律同源）。 拆解（Epic→Story→Task）/估时/依赖/风险 → 交付计划（范围/里程碑/发布窗口）； **不并行写交付计划**；需要估时/依赖素材时只读分模块 scout，结论集中写。 前置：PRD 头部 `status: APPROVED`（未定稿 → 只报缺口并回 `workflows/prd.yaml` review 步，不排期）。 落盘后进入 `review-plan-deliver`（选 A/B）；未过评审方式不得发 PLAN 包。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 技能 `change-management`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「先改 PRD 再说」 | 未分诊/未评估不得改基线；先受理分类再 apply。 |
| 「紧急上线可跳变更单」 | 无单不实施；紧急也要事后留痕与门对齐。 |
| 「实现缺陷当产品缺陷开」 | 须 PRD 原文+现网证据；实现问题退回开发/测试。 |
| 「口头答应客户就算变更」 | 未确认范围/优先级不得入池承诺。 |
### 编排备忘

技能：`skills/change-management/SKILL.md`（先读；排期与变更纪律同源）。 拆解（Epic→Story→Task）/估时/依赖/风险 → 交付计划（范围/里程碑/发布窗口）； **不并行写交付计划**；需要估时/依赖素材时只读分模块 scout，结论集中写。 前置：PRD 头部 `status: APPROVED`（未定稿 → 只报缺口并回 `workflows/prd.yaml` review 步，不排期）。 落盘后进入 `review-plan-deliver`（选 A/B）；未过评审方式不得发 PLAN 包。

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
route=workflow:deliver | step=schedule | reads=rules/packets/deliver/schedule.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/deliver/schedule.md`；对不上 = 未遵守读链。
