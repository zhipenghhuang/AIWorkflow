# 步骤包 · onboard/migrate

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`onboard`
- **step**：`migrate`（旧结构迁移）
- **packet**：`rules/packets/onboard/migrate.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：旧结构迁移
- **产出**：迁移清单/更新后的路径

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 「重新接入」= 按现行文档治理规则迁移；先扫描旧结构，按 `rules/doc-governance.md` 做覆盖对照，列迁移/改名/归档候选，经 `confirm_docs_migration` 确认后执行，不静默丢文件。 映射：`{workroot}/输入/`、`inbound/项目文档/{ver}/`、旧扁平前缀文件、`inbound/反馈|调研|竞品|数据/` → `inbound/{ver|topic}/` 或 `_common/`（保持原文件名；类型写索引；**不要**项目文档层、**不要**强制类型前缀扁平）； 旧工作区/资料副本先判定：原件进 `inbound/`，定稿进 `docs/materials/`，过程稿进工作区；建立/更新 `{workroot}/INDEX.md`、原件登记 `inbound/INDEX.md`；更新计划 、路径引用、activeContext；`activeContext` 合并节 `### 洞见 / 偏好 / 易踩坑` → 按 `rules/core/context-memory.md` 拆为 `### 生效中的偏好` + `### 洞见与易踩坑`，逐条补范围/期限/来源并删过期项；不新增空节。 冲突/无法判断先问一次，不覆盖；迁移后核对链接，再进入 mount/profile。 若存在 `{workroot}/CHANGELOG.md`：列为迁移候选——**用户确认后**改名为 `{workroot}/work-log.md`（内容按工作日志模板整理索引+里程碑条；勿与根 `CHANGELOG.md` 混淆）；未确认不改名。 共用原件根 `inbound/`：认根=用户指定优先，否则判定表，不定则问。原夹文件不迁出。`keep`/`mix`/`replace` 只管原树；仍可索引/复制/吸收。中途存量全索引，按需复制或 A0～A2。

## 4. 本步门

- **HITL `confirm_docs_migration`**：出示分类/覆盖对照/拟归档或清理清单与目标；确认后执行；不擅自删、不覆盖

## 5. 做法

### 本步动作清单

- 「重新接入」= 按现行文档治理规则迁移。
- 先扫描旧结构，按 `rules/doc-governance.md` 做覆盖对照，列迁移/改名/归档候选，经 `confirm_docs_migration` 确认后执行，不静默丢文件。 映射：`{workroot}/输入/`、`inbound/项目文档/{ver}/`、旧扁平前缀文件、`inbound/反馈|调研|竞品|数据/` → `inbound/{ver|topic}/` 或 `_common/`（保持原文件名。
- 类型写索引。
- **不要**项目文档层、**不要**强制类型前缀扁平）。
- 旧工作区/资料副本先判定：原件进 `inbound/`，定稿进 `docs/materials/`，过程稿进工作区。
- 建立/更新 `{workroot}/INDEX.md`、原件登记 `inbound/INDEX.md`。
- 更新计划 、路径引用、activeContext。
- `activeContext` 合并节 `### 洞见 / 偏好 / 易踩坑` → 按 `rules/core/context-memory.md` 拆为 `### 生效中的偏好` + `### 洞见与易踩坑`，逐条补范围/期限/来源并删过期项。
- 不新增空节。 冲突/无法判断先问一次，不覆盖。
- 迁移后核对链接，再进入 mount/profile。 若存在 `{workroot}/CHANGELOG.md`：列为迁移候选——**用户确认后**改名为 `{workroot}/work-log.md`（内容按工作日志模板整理索引+里程碑条。
- 勿与根 `CHANGELOG.md` 混淆）。
- 未确认不改名。 共用原件根 `inbound/`：认根=用户指定优先，否则判定表，不定则问。原夹文件不迁出。`keep`/`mix`/`replace` 只管原树。
- 仍可索引/复制/吸收。中途存量全索引，按需复制或 A0～A2。

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
route=workflow:onboard | step=migrate | reads=rules/packets/onboard/migrate.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/onboard/migrate.md`；对不上 = 未遵守读链。
