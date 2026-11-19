---
name: test-doc-review
description: Use when reviewing testing landing documents (test-analysis + test-plan suite) before execution. Ask human vs AI review mode first; apply test-doc rubric when AI review is chosen. 中文触发：测试计划评审、测试分析评审、分析计划独立评审、A/B 评审。
---

# 测试落地文档评审（技能 · 随包生效）

> 用于：`{ver}/test-analysis.md` + `{ver}/test-plan.md` 成套（将约束执行与准出）。  
> **不替代**覆盖闸 `-Mode coverage`、执行批闸、报告闸；**不替代**执行拆分档 Worker→Reviewer 证据复核。  
> 门：`select_review_mode` → A 自行通过｜B AI 独立评审 → 可执行授权仍认 `confirm_plan`。

## 1. 必须先停问

分析+计划落盘、宣称可执行前，**STOP**：

```text
【评审方式】产物={test-analysis + test-plan 路径}｜级别={T0～T3}
请二选一：
A. 自行评审通过 — 你过目后放行；AI 只附结构自检摘要；review_status=HUMAN_APPROVED
B. AI 独立评审 — 另起评审身份按量规审；产出 {workroot}/{ver}/评审-测试计划-{yyyyMMdd}.md
（回复 A 或 B；不得未问自选）
```

- 点名「测试计划评审 / AI 评审」→ B；「我审/自行通过」→ A。  
- lite/T0 无新增功能面 → 本门可跳过（记 `when_eval`）。  
- 版本级首版/换代或范围·准出·缺陷策略实质变更 → **必问**。

## 2. 强制适用

| 产物 | 强制选模式 |
| --- | --- |
| 版本级 test-analysis + test-plan（首版/换代/实质变更） | 是 |
| 点名「测试计划评审/分析评审」 | 是 |
| lite/T0 无新增功能面 | 否（确认门按 `plan_needs_confirm`） |

选 B 时主动找：可独立证伪未分列、弱 Oracle、覆盖空格、为通过率折叠、准出口径空洞、轨道纳入无批次。

## 3. 量规（成套）

| 轴 | PASS | FAIL |
| --- | --- | --- |
| 来源可追溯 | 主读+互补源；章节可回指 | 无主读或不可打开 |
| INT 可证伪 | 具体 INT + 字段级 Oracle；可独立证伪已分列 | 主题句充数；映射当合并 |
| 覆盖闭合 | 覆盖/方法矩阵无未接受空格；计数被行数支撑 | 只写汇总无账本 |
| 计划可执行 | §0 计数/准出/批次与分析联动；造数项有数据准备批 | 空批次或造数悬空 |
| 轨道诚实 | 纳入=是有批次；探索行有主责/同路径 SC/不可固化理由 | 轨道空壳或功能面伪装探索 |
| 发现优先 | 深度与负向服务于找缺陷 | 为通过率删负向/折叠 INT |

## 4. A / B 路径

| | A 自行 | B AI |
| --- | --- | --- |
| 执行 | 自检摘要 + 用户放行 | 独立上下文；评审者 ≠ 作者；禁改正文 |
| 留痕 | HUMAN_APPROVED + 确认人/时间 | `评审-测试计划-*.md` + 量规缺口表 |
| 需修 | 回 plan 修订 | 回 plan → 重审 ≤1 |
| 之后 | 仍走 `confirm_plan`（可执行授权） | 同左；AI 通过 ≠ 自动开跑 |

## 5. 边界

| | test-doc-review | coverage-map | 执行 Reviewer |
| --- | --- | --- | --- |
| 对象 | 分析+计划内容质量 | 结构/计数/矩阵机检 | 执行证据链 |
| 时机 | 开跑前 | plan 步末 | 拆分档批末 |

## 6. DoD / 自检

- [ ] 已 STOP 选 A/B（或 when 假已记 `when_eval`）
- [ ] 量规轴无阻断缺口；需修已回 plan 且重审 ≤1
- [ ] 留痕齐（HUMAN_APPROVED 或 `评审-测试计划-*.md`）
- [ ] 未把覆盖闸 PASS / 作者自评写成独立评审通过
- [ ] 之后仍走 `confirm_plan` 才可执行

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「覆盖闸过了就能跑」 | 结构齐 ≠ 内容独立评审；版本级须 A/B。 |
| 「确认过计划就行」 | `confirm_plan` 是执行授权；方式选择在前。 |
| 「少写几条 INT 好看」 | 发现问题优先；可独立证伪须分列。 |
| 「作者自审算独立」 | B 路径评审者 ≠ 作者；禁收自评锚定。 |
