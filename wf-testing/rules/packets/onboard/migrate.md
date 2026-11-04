# 步骤包 · onboard/migrate

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：测试轨
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

- 「重新接入」先扫描旧结构，列出迁移清单与目标，经 `confirm_docs_migration` 确认后执行，不静默丢文件；不重复问同一迁移。 建齐本包按需副本树；旧包内 `inbound/项目文档/{ver}/` → `inbound/{ver}/`。原件根 `inbound/`文件**不迁入**包内；认根按文档治理 。`keep`/`mix`/`replace` 只管原树，仍可索引/复制/吸收。 错位归档纠正：根 `{workroot}/_archive/` 内各轨资产 → 各自轨 `_archive/`；散落失效资料 → `inbound/INDEX.md 状态`；列清单确认后执行。 `docs/materials/{ver}/05-testing/test-data/` 保持；`{workroot}/测试用例/`+`{workroot}/执行台账/` → `{workroot}/functional/{NN}-{短名}/*-功能用例.md`+`*-功能台账.md`；接口同理 `*-接口用例/台账`；旧平铺下次迁入； `{workroot}/测试脚本/` → `{workroot}/scripts/`；`{workroot}/变更记录/` → `{workroot}/changes/`；`{workroot}/pre-release/{专项}/` 保持，性能/安全/兼容各自独立； `{workroot}/计划执行看板.md` → 合并进 `{workroot}/test-plan.md` / 后删除。 资料迁移前先按 `rules/doc-governance.md` 做覆盖对照，输出迁移/改名/归档候选；确认后执行，不静默丢文件。 若存在 `{workroot}/CHANGELOG.md`：列为迁移候选——**用户确认后**改名为 `{workroot}/work-log.md`（内容按工作日志模板整理索引+里程碑条；勿与根 `CHANGELOG.md` 混淆）；未确认不改名。 更新 `env-baseline.md` 、测试计划/报告、`inbound/IN

## 4. 本步门

- **HITL `confirm_docs_migration`**：资料收取/分类/改名/归档、或旧结构迁移前列清单与目标；确认后执行

## 5. 做法

### 本步动作清单

- 「重新接入」先扫描旧结构，列出迁移清单与目标，经 `confirm_docs_migration` 确认后执行，不静默丢文件。
- 不重复问同一迁移。 建齐本包按需副本树。
- 旧包内 `inbound/项目文档/{ver}/` → `inbound/{ver}/`。原件根 `inbound/`文件**不迁入**包内。
- 认根按文档治理 。`keep`/`mix`/`replace` 只管原树，仍可索引/复制/吸收。 错位归档纠正：根 `{workroot}/_archive/` 内各轨资产 → 各自轨 `_archive/`。
- 散落失效资料 → `inbound/INDEX.md 状态`。
- 列清单确认后执行。 `docs/materials/{ver}/05-testing/test-data/` 保持。
- `{workroot}/测试用例/`+`{workroot}/执行台账/` → `{workroot}/functional/{NN}-{短名}/*-功能用例.md`+`*-功能台账.md`。
- 接口同理 `*-接口用例/台账`。
- 旧平铺下次迁入。
- `{workroot}/测试脚本/` → `{workroot}/scripts/`。
- `{workroot}/变更记录/` → `{workroot}/changes/`。
- `{workroot}/pre-release/{专项}/` 保持，性能/安全/兼容各自独立。
- `{workroot}/计划执行看板.md` → 合并进 `{workroot}/test-plan.md` / 后删除。 资料迁移前先按 `rules/doc-governance.md` 做覆盖对照，输出迁移/改名/归档候选。
- 确认后执行，不静默丢文件。 若存在 `{workroot}/CHANGELOG.md`：列为迁移候选——**用户确认后**改名为 `{workroot}/work-log.md`（内容按工作日志模板整理索引+里程碑条。
- 勿与根 `CHANGELOG.md` 混淆）。
- 未确认不改名。 更新 `env-baseline.md` 、测试计划/报告、`inbound/INDEX.md`、`docs/materials/INDEX.md`、activeContext。
- `activeContext` 合并节 `### 洞见 / 偏好 / 易踩坑` → 按 `rules/core/context-memory.md` 拆为 `### 生效中的偏好` + `### 洞见与易踩坑`，逐条补范围/期限/来源并删过期项。
- 不新增空节。旧路径不改则注明兼容，不强迁。 文件冲突/无法判断归属/三项混在一个方案 → 停下问一次，不擅自覆盖。 迁移后核对链接与引用，再进入 baseline/context。

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
