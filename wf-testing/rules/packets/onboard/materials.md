# 步骤包 · onboard/materials

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：测试轨
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

- 按 `rules/doc-governance.md` ～ 执行：扫描本包资料根 + 原件根 `inbound/`（环境基线 ；keep/mix）+ 项目根（replace/用户投放）的未登记/变化文件 → 按版本/主题归属分类 → 与同主题旧文件做覆盖对照 （全量替代/全量覆盖/部分覆盖/增量补充/仅新增/重复/冲突）→ 输出【资料收取与归档候选】；**此时不改索引、不改名、不移动、不标记失效**。 有未登记/变化文件、拟改名/搬迁/归档候选 → `docs_migration_needed=true`，停在本门等确认；无候选才继续。 按 `rules/doc-governance.md` ～；确认前不改文件。确认后：索引必做 → 按需复制 → 按需 A0～A2 吸收；失效只动包内副本。存量未点名的保持仅索引。对话/根散落须先留主副本于原件根 `inbound/`。 部分覆盖/增量补充/参考/待确认 → 保留原文件，不归档；冲突/无法判断 → 停下问一次。归档前做引用检查：被当前计划/用例/脚本/报告引用的设计输入、测试数据、稳定冒烟清单保留原位或标“基线”，不标失效。 无候选 → 报「无未登记/失效候选」，不改文件。 **换迭代/关版本（强制）**：确认采纳新迭代/换主题后按 `rules/doc-governance.md` ；不确定则 `confirm_iteration_close`；确认后先按 判 T1/T2/T4，再按 关账（跳过仅发版项）；T2/T4 保留仍被引用的设计输入/测试数据/稳定冒烟清单/脚本，只归档被替代的用例轮次/报告/CR。不依赖关报告。 关账 materials：**必做**覆盖刷新关闭版 `{prev}/`→superseded，再建 `{next}/` current（默认 overwrite-latest）。

## 4. 本步门

- **HITL `confirm_iteration_close`**：出示当前迭代标识、未完成项、拟归档摘要、下一迭代标识；确认后按 `rules/doc-governance.md` §7.1 关账；选「并行不关」则只落新资料。**关闭=停止新范围/冻结版本线，不停止测试与缺陷修复**；测试未完又要开新迭代，优先「并行不关」，归档待测试完成
- **HITL `confirm_docs_migration`**：资料收取/分类/改名/归档、或旧结构迁移前列清单与目标；确认后执行

## 5. 做法

### 本步动作清单

- 按 `rules/doc-governance.md` ～ 执行：扫描本包资料根 + 原件根 `inbound/`（环境基线。
- keep/mix）+ 项目根（replace/用户投放）的未登记/变化文件 → 按版本/主题归属分类 → 与同主题旧文件做覆盖对照 （全量替代/全量覆盖/部分覆盖/增量补充/仅新增/重复/冲突）→ 输出【资料收取与归档候选】。
- **此时不改索引、不改名、不移动、不标记失效**。 有未登记/变化文件、拟改名/搬迁/归档候选 → `docs_migration_needed=true`，停在本门等确认。
- 无候选才继续。 按 `rules/doc-governance.md` ～。
- 确认前不改文件。确认后：索引必做 → 按需复制 → 按需 A0～A2 吸收。
- 失效只动包内副本。存量未点名的保持仅索引。对话/根散落须先留主副本于原件根 `inbound/`。 部分覆盖/增量补充/参考/待确认 → 保留原文件，不归档。
- 冲突/无法判断 → 停下问一次。归档前做引用检查：被当前计划/用例/脚本/报告引用的设计输入、测试数据、稳定冒烟清单保留原位或标“基线”，不标失效。 无候选 → 报「无未登记/失效候选」，不改文件。 **换迭代/关版本（强制）**：确认采纳新迭代/换主题后按 `rules/doc-governance.md`。
- 不确定则 `confirm_iteration_close`。
- 确认后先按 判 T1/T2/T4，再按 关账（跳过仅发版项）。
- T2/T4 保留仍被引用的设计输入/测试数据/稳定冒烟清单/脚本，只归档被替代的用例轮次/报告/CR。不依赖关报告。 关账 materials：**必做**覆盖刷新关闭版 `{prev}/`→superseded，再建 `{next}/` current（默认 overwrite-latest）。

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
