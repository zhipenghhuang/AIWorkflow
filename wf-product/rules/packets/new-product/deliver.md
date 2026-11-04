# 步骤包 · new-product/deliver

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`new-product`
- **step**：`deliver`（交付与验收）
- **packet**：`rules/packets/new-product/deliver.md`
- **条件步** `when=go_decision_go`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：交付与验收
- **产出**：交付计划 + UAT 记录（{workroot}/{ver}/40-delivery/）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- **子链**：按 `workflows/deliver.yaml` 的 schedule / followup / uat 逐步执行（只读当前 step 块）；需求/问题/产品缺陷 → `workflows/change.yaml` 受理与处置。 **门权威在子链**：UAT/评审门以 deliver.yaml（及 change）hitl 为准；本步不重复跑门。 UAT 按 PRD 验收标准逐条对照（结果 + 证据）；产品缺陷 vs 实现缺陷要有依据。 技能：`skills/change-management/SKILL.md` / `skills/uat-and-retrospective/SKILL.md`。

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
### 技能 `uat-and-retrospective`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「差不多能用就可以上」 | UAT 未过不发布；有条件通过须遗留+责任人+接受人。 |
| 「复盘可以以后补」 | 重大发布/回滚/事故须同轮或约定窗口内复盘。 |
| 「没有埋点就跳过指标」 | 无成功指标不发布；无埋点写不适用+原因。 |
### 编排备忘

**子链**：按 `workflows/deliver.yaml` 的 schedule / followup / uat 逐步执行（只读当前 step 块）；需求/问题/产品缺陷 → `workflows/change.yaml` 受理与处置。 **门权威在子链**：UAT/评审门以 deliver.yaml（及 change）hitl 为准；本步不重复跑门。 UAT 按 PRD 验收标准逐条对照（结果 + 证据）；产品缺陷 vs 实现缺陷要有依据。 技能：`skills/change-management/SKILL.md` / `skills/uat-and-retrospective/SKILL.md`。

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
route=workflow:new-product | step=deliver | reads=rules/packets/new-product/deliver.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/new-product/deliver.md`；对不上 = 未遵守读链。
