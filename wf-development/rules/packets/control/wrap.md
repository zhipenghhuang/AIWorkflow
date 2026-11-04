# 步骤包 · control/wrap

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`control`
- **step**：`wrap`（收尾）
- **packet**：`rules/packets/control/wrap.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：收尾
- **产出**：【任务收尾】（计划/进度/下一步明细置第 1 点，六段压缩）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 对照 `rules/templates/90-handoff/closeout-skeleton.md` 输出六段压缩；第1点含当前阶段/门/下一步 只读查询不写计划；有实质进展时更新开发计划 /、 `{workroot}/INDEX.md` 与 activeContext（现状三处同拍；`sync=` 含 `triad=`）；更新 `handoff-ledger.md` 摘要与待回执/退回项。 版本/迭代关闭：追加 `{workroot}/work-log.md` 里程碑（索引+条目；结论/产出/遗留）；**仅**用户可见版本关闭/发版时更新根 `CHANGELOG.md`（产品语言：用户可见capabilities/破坏性/迁移·兼容/安全；禁接入/文档治理/过程项）——工作日志≠根 CHANGELOG≠开发计划执行日志。 按 `rules/doc-governance.md` ～ 扫描 `inbound/`，输出【资料收取与归档候选】；只归档用户确认的 `失效` 项，部分覆盖/增量/参考不动；未确认不移动。 同步按 `rules/doc-governance.md` ～（仅本步关版本/结项时，非日常收尾）：先判 T1/T2/T4，T2/T4 保留仍被引用的基础设计/流程图/原型；长期基线就地更新、版本绑定的增量方案/任务清单/UAT/提测单归档、已完结临时/失败/重复列清理候选；确认后执行。 未提交默认不得开始下一任务（例外=基线检查选项 C/D 且用户确认）。 本步先出骨架与拟提交清单；完整【拟提交】在下一步 commit 只展示一次。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 本步动作清单

- 对照 `rules/templates/90-handoff/closeout-skeleton.md` 输出六段压缩。
- 第1点含当前阶段/门/下一步 只读查询不写计划。
- 有实质进展时更新开发计划 /、 `{workroot}/INDEX.md` 与 activeContext（现状三处同拍。
- `sync=` 含 `triad=`）。
- 更新 `handoff-ledger.md` 摘要与待回执/退回项。 版本/迭代关闭：追加 `{workroot}/work-log.md` 里程碑（索引+条目。
- 结论/产出/遗留）。
- **仅**用户可见版本关闭/发版时更新根 `CHANGELOG.md`（产品语言：用户可见capabilities/破坏性/迁移·兼容/安全。
- 禁接入/文档治理/过程项）——工作日志≠根 CHANGELOG≠开发计划执行日志。 按 `rules/doc-governance.md` ～ 扫描 `inbound/`，输出【资料收取与归档候选】。
- 只归档用户确认的 `失效` 项，部分覆盖/增量/参考不动。
- 未确认不移动。 同步按 `rules/doc-governance.md` ～（仅本步关版本/结项时，非日常收尾）：先判 T1/T2/T4，T2/T4 保留仍被引用的基础设计/流程图/原型。
- 长期基线就地更新、版本绑定的增量方案/任务清单/UAT/提测单归档、已完结临时/失败/重复列清理候选。
- 确认后执行。 未提交默认不得开始下一任务（例外=基线检查选项 C/D 且用户确认）。 本步先出骨架与拟提交清单。
- 完整【拟提交】在下一步 commit 只展示一次。

## 6. 打开/填写

- 运行时正文：仅本文件（开局卡已在会话开头读过）。
- 填写模板（仅此一个）：`rules/templates/90-handoff/closeout-skeleton.md`

## 7. 完成信号

- §2 产出已落盘。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 8. 回执字段

```text
route=workflow:control | step=wrap | reads=rules/packets/control/wrap.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/control/wrap.md`；对不上 = 未遵守读链。
