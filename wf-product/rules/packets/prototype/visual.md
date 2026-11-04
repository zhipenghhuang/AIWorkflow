# 步骤包 · prototype/visual

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`prototype`
- **step**：`visual`（视觉方向与设计系统）
- **packet**：`rules/packets/prototype/visual.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：视觉方向与设计系统
- **产出**：视觉稿/设计 tokens/标注（{workroot}/{ver}/20-design/）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 技能：`skills/ui-visual-design-system/SKILL.md`。 设计系统策略：复用现有品牌/系统；无则选一套主系统，不混搭；tokens 单一来源。 2～3 个视觉方向（气质/配色/字体/适用场景），写清为什么适合本产品，推荐 1 个并说明理由； 产出 design tokens（颜色/字体/间距/圆角/阴影/组件）。 confirm_design：出示 IA/线框/视觉方向/tokens 请确认；确认后才做高保真。 能力（可选）：design-intelligence / ui-generation / frontend-design；未装 = 按包内技能。

## 4. 本步门

- **HITL `confirm_design`**：IA/线框/2～3 个视觉方向/tokens；确认后才做高保真

## 5. 做法

### 技能 `ui-visual-design-system`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「先做一版再统一 tokens」 | 无方向/tokens 的高保真会返工；先方向再组件。 |
| 「多风格显得丰富」 | 单次交付一个视觉方向；禁止无系统的装饰堆叠。 |
| 「无障碍以后再说」 | 对比度/焦点/语义属现行验收，不债项化逃避。 |
### 编排备忘

技能：`skills/ui-visual-design-system/SKILL.md`。 设计系统策略：复用现有品牌/系统；无则选一套主系统，不混搭；tokens 单一来源。 2～3 个视觉方向（气质/配色/字体/适用场景），写清为什么适合本产品，推荐 1 个并说明理由； 产出 design tokens（颜色/字体/间距/圆角/阴影/组件）。 confirm_design：出示 IA/线框/视觉方向/tokens 请确认；确认后才做高保真。 能力（可选）：design-intelligence / ui-generation / frontend-design；未装 = 按包内技能。

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
route=workflow:prototype | step=visual | reads=rules/packets/prototype/visual.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/prototype/visual.md`；对不上 = 未遵守读链。
