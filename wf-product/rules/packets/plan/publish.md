# 步骤包 · plan/publish

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`plan`
- **step**：`publish`（落盘与索引）
- **packet**：`rules/packets/plan/publish.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：落盘与索引
- **产出**：{workroot}/product-plan.md（模板 rules/templates/10-planning/product-plan-template.md）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 须已完成 review-plan 选模式（或本轮跳过条件满足）。核对 Brief+差量表已落盘（或独立迭代变更摘要已互指）。总控表状态回写（阶段 / 产物 / 门 / 状态 / 下一动作）；版本索引挂 PRD / 迭代方案（多需求版本）/ 评审 / 受理/变更 / 交付计划 / UAT / GTM / 原型 / 复盘 / 迭代变更摘要（若独立文件）。 多需求/多功能版本：在版本目录落 `迭代方案-{ver}.md`（模板 `rules/templates/10-planning/iteration-plan-template.md`），汇总范围、功能覆盖、验收矩阵、执行记录与发布条件；单需求可只用 PRD，不强制另立。 更新 `{workroot}/work-log.md`（仅本文件）：索引表新增一行 + 一条里程碑条目，事件类型=`计划确认`（结论/产出/遗留；关联产品计划路径）；无文件则先按工作日志模板创建再写。 **不是**根 `CHANGELOG.md`、也不是产品计划 执行日志（细粒度过程仍只写 ）。 **禁止**创建/修改/补链项目根 `CHANGELOG.md`；无开发包则不建根。 **主档不移动**：`{workroot}/product-plan.md` 常青；季度结束复制当期执行到 `{workroot}/_archive/{yyyy-Qn}/产品计划-{yyyy-Qn}.md`，主档保留历史索引并重置当前季度； 版本/结项把当期目录整体移入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`（点名执行）；先判 T1/T2/T4，T2/T4 增量迭代保留仍被引用的 PRD/原型基线，不整夹归档。 版本/结项归档时按 `rules/doc-governance.md` 扫描；先判 T1/T2/T4，T2/T4 保留仍被引用的 PRD/原型基线；失效资料进 `inbound/_archive/{ver}/` + 归档清单；部分/增量/参考不动；未确认不移动。 同步按 `rules/doc-governance.md` ～（仅本

## 4. 本步门

- **HITL `confirm_iteration_close`**：出示当前迭代标识、未完成项、拟归档摘要、下一迭代标识；确认后按 `rules/doc-governance.md` §7.1 关账；选「并行不关」则只落新资料。**关闭=停止新范围/冻结版本线，不停止测试与缺陷修复**；测试未完又要开新迭代，优先「并行不关」，归档待测试完成
- **HITL `confirm_docs_migration`**：出示分类/覆盖对照/拟归档或清理清单与目标；确认后执行；不擅自删、不覆盖

## 5. 做法

### 本步动作清单

- 须已完成 review-plan 选模式（或本轮跳过条件满足）。核对 Brief+差量表已落盘（或独立迭代变更摘要已互指）。总控表状态回写（阶段 / 产物 / 门 / 状态 / 下一动作）。
- 版本索引挂 PRD / 迭代方案（多需求版本）/ 评审 / 受理/变更 / 交付计划 / UAT / GTM / 原型 / 复盘 / 迭代变更摘要（若独立文件）。 多需求/多功能版本：在版本目录落 `迭代方案-{ver}.md`（模板 `rules/templates/10-planning/iteration-plan-template.md`），汇总范围、功能覆盖、验收矩阵、执行记录与发布条件。
- 单需求可只用 PRD，不强制另立。 更新 `{workroot}/work-log.md`（仅本文件）：索引表新增一行 + 一条里程碑条目，事件类型=`计划确认`（结论/产出/遗留。
- 关联产品计划路径）。
- 无文件则先按工作日志模板创建再写。 **不是**根 `CHANGELOG.md`、也不是产品计划 执行日志（细粒度过程仍只写 ）。 **禁止**创建/修改/补链项目根 `CHANGELOG.md`。
- 无开发包则不建根。 **主档不移动**：`{workroot}/product-plan.md` 常青。
- 季度结束复制当期执行到 `{workroot}/_archive/{yyyy-Qn}/产品计划-{yyyy-Qn}.md`，主档保留历史索引并重置当前季度。
- 版本/结项把当期目录整体移入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`（点名执行）。
- 先判 T1/T2/T4，T2/T4 增量迭代保留仍被引用的 PRD/原型基线，不整夹归档。 版本/结项归档时按 `rules/doc-governance.md` 扫描。
- 先判 T1/T2/T4，T2/T4 保留仍被引用的 PRD/原型基线。
- 失效资料进 `inbound/_archive/{ver}/` + 归档清单。
- 部分/增量/参考不动。
- 未确认不移动。 同步按 `rules/doc-governance.md` ～（仅本步关版本/结项时，非日常收尾）：长期主档就地更新、版本绑定目录关闭时归档、已完结临时/失败/重复列清理候选。
- 确认后执行。 **换代/新版本主题（即使不结项发版）** → 按。
- 不确定则 `confirm_iteration_close`。
- 确认后先判 T1/T2/T4，再按 关账（T2/T4 保留仍被引用的 PRD/原型基线。
- 跳过仅发版项）。 建/更新 `{workroot}/handoff/handoff-ledger.md`（模板 `rules/templates/90-handoff/handoff-ledger-template.md`）。
- 按模板登记计划/PRD/设计/变更/UAT/发布节点。
- 变更分级与重规划触发写入计划执行日志/变更记录。 稳定真值（愿景/用户/北极星/指标口径）留在主档与 `product-profile.md`，不随季度归档。

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
route=workflow:plan | step=publish | reads=rules/packets/plan/publish.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/plan/publish.md`；对不上 = 未遵守读链。
