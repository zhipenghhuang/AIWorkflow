# 步骤包 · prd/prioritize

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`prd`
- **step**：`prioritize`（优先级与立项）
- **packet**：`rules/packets/prd/prioritize.md`
- **条件步** `when=new_requirement_or_scope_change`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：优先级与立项
- **产出**：需求池优先级/立项建议（{workroot}/requirement-pool.md §优先级）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 条件步：跨版本/高价值需求或点名「立项」才走；小需求直接进 PRD（不设门）。 方法按需：RICE / Kano / MoSCoW；产出：优先级 + 版本范围（MVP）+ 排除项 + 粗排期 + 依赖风险。 依据=确认的客户需求+证据+成本/风险；**模式 S 借鉴项**须已回绑问题；**模式 P 候选项**进版本须本步或计划范围确认，不得因「竞品有」自动 Must。 不把领导偏好、单个客户直接当优先级；未确认/未验证需求不排期；取舍给建议，不替用户决定。 技能：`skills/requirement-discovery-and-prioritization/SKILL.md`（先读再做）。 confirm_scope：出示范围/目标/粗排期请确认，批准后才进 PRD；仅跨版本/高价值/点名立项链时停。

## 4. 本步门

- **HITL `confirm_scope`**：范围（MVP）/排除项/粗排期/风险 一行摘要；条件门：仅跨版本/高价值/未确认范围时停

## 5. 做法

### 技能 `requirement-discovery-and-prioritization`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「先排进版本再澄清」 | 理解→方案双确认未过不得入池承诺。 |
| 「客户喊得响=优先级高」 | 用价值/风险/成本矩阵；嗓门不是 RICE。 |
| 「范围可以边做边定」 | 无边界=无 AC；未定义完禁评审通过。 |
| 「竞品有的我们都要」 | 对标是输入不是清单照搬；写非目标。 |
### 编排备忘

条件步：跨版本/高价值需求或点名「立项」才走；小需求直接进 PRD（不设门）。 方法按需：RICE / Kano / MoSCoW；产出：优先级 + 版本范围（MVP）+ 排除项 + 粗排期 + 依赖风险。 依据=确认的客户需求+证据+成本/风险；**模式 S 借鉴项**须已回绑问题；**模式 P 候选项**进版本须本步或计划范围确认，不得因「竞品有」自动 Must。 不把领导偏好、单个客户直接当优先级；未确认/未验证需求不排期；取舍给建议，不替用户决定。 技能：`skills/requirement-discovery-and-prioritization/SKILL.md`（先读再做）。 confirm_scope：出示范围/目标/粗排期请确认，批准后才进 PRD；仅跨版本/高价值/点名立项链时停。

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
route=workflow:prd | step=prioritize | reads=rules/packets/prd/prioritize.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/prd/prioritize.md`；对不上 = 未遵守读链。
