# 步骤包 · intake/absorb

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`intake`
- **step**：`absorb`（局部更新）
- **packet**：`rules/packets/intake/absorb.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：局部更新
- **产出**：已更新文档/台账/任务 · 【迭代关账/归档候选】（如有）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 只改受影响章节；保留稳定 ID；正式产物直接替换旧结论（不留“已作废/旧方案”说明），变更前后与原因只记 CR/变更记录。 更新：需求台账/PRD、迭代计划/任务清单、方案/ADR、DB/API/前端、测试/发布文档（按影响）。 更新：`开发计划` （计划状态/当前门/下一动作）、（受影响阶段/范围）、/、 执行日志；`{workroot}/INDEX.md`、`activeContext`。 更新 `handoff-ledger.md`：受影响交接包标 `已取代/需重发`；C1+ **建议**发 `CHG`（先问后发）；未正式签收场景不以缺回执阻塞日常吸收完成判定。 不新建重复文档；同一主题就地更新；不同工作先问用户。 本步只准备，不实施代码；实施走 change/iterate。 **换迭代/关版本（强制）**：新迭代文档已采纳或换主题/换代 → 按 `rules/doc-governance.md` ；不确定当前是否结束 → STOP `confirm_iteration_close`；确认后先判 T1/T2/T4，再按 关账（T2/T4 保留仍被引用的基础设计/流程图/原型；分析分类/归档/清理/修链；跳过仅发版项）。用户说并行不关 → 只落新资料。

## 4. 本步门

- **HITL `confirm_iteration_close`**：出示当前迭代标识、未完成项、拟归档摘要、下一迭代标识；确认「结束当前并进入下一」后才按 `rules/doc-governance.md` §7.1 关账；选「并行不关」则只落新资料不归档现行绑定主档。**关闭=停止新范围/冻结版本线，不停止测试**：测试与缺陷修复可继续（走 patch），归档待测试完成；测试未完又要开新迭代，优先「并行不关」
- **HITL `confirm_docs_migration`**：出示分类/覆盖对照/拟归档或清理清单与目标；确认后执行

## 5. 做法

### 本步动作清单

- 只改受影响章节。
- 保留稳定 ID。
- 正式产物直接替换旧结论（不留“已作废/旧方案”说明），变更前后与原因只记 CR/变更记录。 更新：需求台账/PRD、迭代计划/任务清单、方案/ADR、DB/API/前端、测试/发布文档（按影响）。 更新：`开发计划` （计划状态/当前门/下一动作）、（受影响阶段/范围）、/、 执行日志。
- `{workroot}/INDEX.md`、`activeContext`。 更新 `handoff-ledger.md`：受影响交接包标 `已取代/需重发`。
- C1+ **建议**发 `CHG`（先问后发）。
- 未正式签收场景不以缺回执阻塞日常吸收完成判定。 不新建重复文档。
- 同一主题就地更新。
- 不同工作先问用户。 本步只准备，不实施代码。
- 实施走 change/iterate。 **换迭代/关版本（强制）**：新迭代文档已采纳或换主题/换代 → 按 `rules/doc-governance.md`。
- 不确定当前是否结束 → STOP `confirm_iteration_close`。
- 确认后先判 T1/T2/T4，再按 关账（T2/T4 保留仍被引用的基础设计/流程图/原型。
- 分析分类/归档/清理/修链。
- 跳过仅发版项）。用户说并行不关 → 只落新资料。

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
route=workflow:intake | step=absorb | reads=rules/packets/intake/absorb.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/intake/absorb.md`；对不上 = 未遵守读链。
