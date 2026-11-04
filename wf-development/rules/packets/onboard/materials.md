# 步骤包 · onboard/materials

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`onboard`
- **step**：`materials`（资料收取与归档）
- **packet**：`rules/packets/onboard/materials.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：资料收取与归档
- **产出**：【入站分析】（确认后登记 / A0～A2 吸收 / 定稿发布 materials）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 扫描 `inbound/` + 项目根散落；按 `rules/doc-governance.md` ～ 分类与覆盖对照，输出【入站分析】；确认前不改索引、不改名、不移动、不归档。 确认后同批：`inbound/INDEX.md` 登记 → 按需 A0～A2 吸收到 `{workroot}/` → 定稿发布 `docs/materials/`。 外部输入主副本只在 `inbound/`；materials 只放定稿、正确、完整、可发送内容。 冲突/无法判断 → 停问；S1/S2/S3 只归档工作区旧稿；`inbound/` 不归档。 换代/关版本按 ；关账时**必做**覆盖刷新关闭版 materials→superseded 再开新版；旧目录保留，不设 `_archive`；日常发布默认 overwrite-latest。

## 4. 本步门

- **HITL `confirm_iteration_close`**：出示当前迭代标识、未完成项、拟归档摘要、下一迭代标识；确认「结束当前并进入下一」后才按 `rules/doc-governance.md` §7.1 关账；选「并行不关」则只落新资料不归档现行绑定主档。**关闭=停止新范围/冻结版本线，不停止测试**：测试与缺陷修复可继续（走 patch），归档待测试完成；测试未完又要开新迭代，优先「并行不关」
- **HITL `confirm_docs_migration`**：出示分类/覆盖对照/拟归档或清理清单与目标；确认后执行

## 5. 做法

### 本步动作清单

- 扫描 `inbound/` + 项目根散落。
- 按 `rules/doc-governance.md` ～ 分类与覆盖对照，输出【入站分析】。
- 确认前不改索引、不改名、不移动、不归档。 确认后同批：`inbound/INDEX.md` 登记 → 按需 A0～A2 吸收到 `{workroot}/` → 定稿发布 `docs/materials/`。 外部输入主副本只在 `inbound/`。
- materials 只放定稿、正确、完整、可发送内容。 冲突/无法判断 → 停问。
- S1/S2/S3 只归档工作区旧稿。
- `inbound/` 不归档。 换代/关版本按。
- 关账时**必做**覆盖刷新关闭版 materials→superseded 再开新版。
- 旧目录保留，不设 `_archive`。
- 日常发布默认 overwrite-latest。

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
