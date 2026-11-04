# 步骤包 · intake/impact

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`intake`
- **step**：`impact`（影响分析）
- **packet**：`rules/packets/intake/impact.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：影响分析
- **产出**：影响矩阵/待确认项 + C2/C3 重基线清单

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 逐项分析：需求/AC、原型、架构/ADR、DB、API、前端、测试、任务/排期、发布/回滚、 `{workroot}/INDEX.md`。 按 `rules/collaboration/handoff.md` 判 C0～C3；C1+ 需通知受影响角色并发 `CHG` 包；C2/C3 必须 `confirm_replan` → 重基线（需求基线/任务清单/开发计划/测试计划）→ 过 `dev-plan` 检查；禁止拆成 C0/C1 绕过。影响矩阵写入变更记录/吸收报告。 基于 `parse` 理解摘要与冲突/GAP 分析；不得绕开理解摘要凭文件名/标题判断影响；未裁决冲突先列待确认，不静默选一边。 跨版本/高价值且 ≥3 影响域 → 只读分域评估（每域返回受影响/依据/动作 ≤30 行）；影响矩阵与结论集中写，不并行改同一文档。 每项写“受影响/不受影响 + 依据/动作”；禁止沉默。 实质变更（范围/AC/优先级/架构/排期/发布）→ confirm_change：出示变更类型/影响矩阵/待更新文档/待确认项。 需求基线/AC 被替换或新增 → confirm_requirements：出示差异/范围/AC/非目标，确认后冻结；未签收不得改基线。 小澄清（C0/C1 无实质影响）可跳过门，更新后报告。

## 4. 本步门

- **HITL `confirm_change`**：出示变更类型/影响矩阵/待更新文档/待确认项；实质变更确认后才更新基线
- **HITL `confirm_requirements`**：出示范围/AC/NFR/非目标/未决；未签收不进设计/排期
- **HITL `confirm_replan`**：出示变更等级/影响矩阵/重基线范围（基线/任务/计划/测试）/里程碑与资源影响；确认后才重基线；禁止拆成 C0/C1 绕过

## 5. 做法

### 本步动作清单

- 逐项分析：需求/AC、原型、架构/ADR、DB、API、前端、测试、任务/排期、发布/回滚、 `{workroot}/INDEX.md`。 按 `rules/collaboration/handoff.md` 判 C0～C3。
- C1+ 需通知受影响角色并发 `CHG` 包。
- C2/C3 必须 `confirm_replan` → 重基线（需求基线/任务清单/开发计划/测试计划）→ 过 `dev-plan` 检查。
- 禁止拆成 C0/C1 绕过。影响矩阵写入变更记录/吸收报告。 基于 `parse` 理解摘要与冲突/GAP 分析。
- 不得绕开理解摘要凭文件名/标题判断影响。
- 未裁决冲突先列待确认，不静默选一边。 跨版本/高价值且 ≥3 影响域 → 只读分域评估（每域返回受影响/依据/动作 ≤30 行）。
- 影响矩阵与结论集中写，不并行改同一文档。 每项写“受影响/不受影响 + 依据/动作”。
- 禁止沉默。 实质变更（范围/AC/优先级/架构/排期/发布）→ confirm_change：出示变更类型/影响矩阵/待更新文档/待确认项。 需求基线/AC 被替换或新增 → confirm_requirements：出示差异/范围/AC/非目标，确认后冻结。
- 未签收不得改基线。 小澄清（C0/C1 无实质影响）可跳过门，更新后报告。

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
route=workflow:intake | step=impact | reads=rules/packets/intake/impact.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/intake/impact.md`；对不上 = 未遵守读链。
