# 步骤包 · defect-fix/align

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`defect-fix`
- **step**：`align`（文档对齐）
- **packet**：`rules/packets/defect-fix/align.md`
- **条件步** `when=product_decision_requires_alignment`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：文档对齐
- **产出**：对齐记录（受影响文档/计划清单）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 仅产品回复且需实施（认可/修改后认可/改判实现）时执行；非问题/补充信息跳过，转 clarify。 按 rules/defects/fix-collaboration.md ： ≥3 份新产品文档 → 只读抽取扇出（每份返回变更点/AC/影响面候选 ≤30 行）；对齐结论由本步集中写，不并行改同一文档。 产品新文档按 `rules/doc-governance.md` （T6）：确认后原件落 `inbound/{ver|topic}/`，登记索引；S1/S2/S3 同批进 `inbound/_archive/`；结论同步工作区。 构成需求/范围/AC/接口/数据实质变更 → 按 workflows/intake.yaml 与 rules/workflow.md 做影响分析/CR； 逐项对照评估单/原方案，列一致/差异/新增/删除； 更新 {workroot}/10-requirements/需求台账、{workroot}/20-design/方案-…/ADR/接口/DB、{workroot}/40-tasks/任务清单、 {workroot}/50-verification/UAT、{workroot}/60-release/提测单/发布说明/回滚、开发计划 //、 项目档案 //（新入口/命令/规范变化）、{workroot}/00-governance/变更记录（CR）、`{workroot}/INDEX.md`、`activeContext`； 不适用写原因；未对齐不得 fix。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 本步动作清单

- 仅产品回复且需实施（认可/修改后认可/改判实现）时执行。
- 非问题/补充信息跳过，转 clarify。 按 rules/defects/fix-collaboration.md ： ≥3 份新产品文档 → 只读抽取扇出（每份返回变更点/AC/影响面候选 ≤30 行）。
- 对齐结论由本步集中写，不并行改同一文档。 产品新文档按 `rules/doc-governance.md` （T6）：确认后原件落 `inbound/{ver|topic}/`，登记索引。
- S1/S2/S3 同批进 `inbound/_archive/`。
- 结论同步工作区。 构成需求/范围/AC/接口/数据实质变更 → 按 workflows/intake.yaml 与 rules/workflow.md 做影响分析/CR。
- 逐项对照评估单/原方案，列一致/差异/新增/删除。
- 更新 {workroot}/10-requirements/需求台账、{workroot}/20-design/方案-…/ADR/接口/DB、{workroot}/40-tasks/任务清单、 {workroot}/50-verification/UAT、{workroot}/60-release/提测单/发布说明/回滚、开发计划 //、 项目档案 //（新入口/命令/规范变化）、{workroot}/00-governance/变更记录（CR）、`{workroot}/INDEX.md`、`activeContext`。
- 不适用写原因。
- 未对齐不得 fix。

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
route=workflow:defect-fix | step=align | reads=rules/packets/defect-fix/align.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/defect-fix/align.md`；对不上 = 未遵守读链。
