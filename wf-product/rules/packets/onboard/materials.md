# 步骤包 · onboard/materials

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`onboard`
- **step**：`materials`（资料收取与归档）
- **packet**：`rules/packets/onboard/materials.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：资料收取与归档
- **产出**：【入站分析】（确认后登记/A0～A2/发布 materials）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 按 `rules/doc-governance.md` ～：入站意图分析（T1～T9）+ 覆盖对照 → 输出【入站分析】；确认前不改文件。 有候选 → `docs_migration_needed=true`，停本门；无候选继续。 确认后：原件留/落入原件根 `inbound/`并**全量可查索引** → 仅对确认需要的文件复制进 `inbound/` → 按 A0～A2 吸收 → 失效只动包内副本/工作区旧稿。存量默认仅索引，不强制全复制。对话/根散落须先留主副本于原件根 `inbound/`。 部分覆盖/增量/参考保留；冲突停下问。无候选 → 报「无未登记/失效候选」。归档前做引用检查：被当前产品计划/PRD/原型/交付/UAT 引用的文档保留原位或标“基线”，不标失效。 **换迭代/关版本（强制）**：确认采纳新迭代/换主题后按 `rules/doc-governance.md` ；不确定则 `confirm_iteration_close`；确认后先按 判 T1/T2/T4，再按 关账（跳过仅发版项）；T2/T4 保留仍被引用的 PRD/原型基线，只归档被替代增量与旧稿。不依赖发版。 关账 materials：**必做**覆盖刷新关闭版 `{prev}/`→superseded，再建 `{next}/` current（默认 overwrite-latest）。

## 4. 本步门

- **HITL `confirm_iteration_close`**：出示当前迭代标识、未完成项、拟归档摘要、下一迭代标识；确认后按 `rules/doc-governance.md` §7.1 关账；选「并行不关」则只落新资料。**关闭=停止新范围/冻结版本线，不停止测试与缺陷修复**；测试未完又要开新迭代，优先「并行不关」，归档待测试完成
- **HITL `confirm_docs_migration`**：出示分类/覆盖对照/拟归档或清理清单与目标；确认后执行；不擅自删、不覆盖

## 5. 做法

### 本步动作清单

- 按 `rules/doc-governance.md` ～：入站意图分析（T1～T9）+ 覆盖对照 → 输出【入站分析】。
- 确认前不改文件。 有候选 → `docs_migration_needed=true`，停本门。
- 无候选继续。 确认后：原件留/落入原件根 `inbound/`并**全量可查索引** → 仅对确认需要的文件复制进 `inbound/` → 按 A0～A2 吸收 → 失效只动包内副本/工作区旧稿。存量默认仅索引，不强制全复制。对话/根散落须先留主副本于原件根 `inbound/`。 部分覆盖/增量/参考保留。
- 冲突停下问。无候选 → 报「无未登记/失效候选」。归档前做引用检查：被当前产品计划/PRD/原型/交付/UAT 引用的文档保留原位或标“基线”，不标失效。 **换迭代/关版本（强制）**：确认采纳新迭代/换主题后按 `rules/doc-governance.md`。
- 不确定则 `confirm_iteration_close`。
- 确认后先按 判 T1/T2/T4，再按 关账（跳过仅发版项）。
- T2/T4 保留仍被引用的 PRD/原型基线，只归档被替代增量与旧稿。不依赖发版。 关账 materials：**必做**覆盖刷新关闭版 `{prev}/`→superseded，再建 `{next}/` current（默认 overwrite-latest）。

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
route=workflow:onboard | step=materials | reads=rules/packets/onboard/materials.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/onboard/materials.md`；对不上 = 未遵守读链。
