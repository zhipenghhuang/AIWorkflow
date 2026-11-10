# 步骤卡 · onboard/migrate

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`onboard` / `migrate`（旧结构迁移）
- **packet**：`rules/packets/onboard/migrate.md`
- **角色**：`onboard-agent`（测试包接入）。挂载 → 基线关键节 → activeContext → 入库确认 → 环境与工具检查（默认静默） → 按接入清单核验；本步只做该角色职责；越界交回或升级。
- **上游**：无（链首）
- **后续**：`baseline`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：旧结构迁移
- **产出**：迁移清单/更新后的路径

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：按 `rules/core/global-rules.md` §7 重读并遵守全文；心跳 `global=ok` 表示本步已按 §7 复核；未按 §7 复核不得写 `global=ok`。偏离写 `global=dev:<原因>`。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_docs_migration`**：资料收取/分类/改名/归档、或结构迁移前列清单与目标；确认后执行。
- **条件判定 `hitl:docs_migration_needed`**：本步将搬迁/归档/清理 inbound 或工作文档且未确认清单；满足→真，否则跳过该门。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 「重新接入」先扫描旧结构，列出迁移清单与目标，经 `confirm_docs_migration` 确认后执行，不静默丢文件。
- 不重复问同一迁移。
- 建齐本包按需副本树。
- 旧包内 `inbound/项目文档/{ver}/` → `inbound/{ver}/`。
- 原件根 `inbound/`文件**不迁入**包内。
- 认根按文档治理。
- `keep`/`mix`/`replace` 只管原树，仍可索引/复制/吸收。
- 错位归档纠正：根 `{workroot}/_archive/` 内各轨资产 → 各自轨 `_archive/`。
- 散落失效资料 → `inbound/INDEX.md 状态`。
- 列清单确认后执行。
- `docs/materials/{ver}/05-testing/test-data/` 保持。
- `{workroot}/测试用例/`+`{workroot}/执行台账/` → `{workroot}/{ver}/functional/{NN}-{短名}-执行记录.md`（平铺；旧用例/台账合并进执行记录）。
- 接口同理。
- `{workroot}/测试脚本/` → `{workroot}/scripts/`。
- `{workroot}/变更记录/` → `{workroot}/{ver}/changes/`。
- 旧 `pre-release/{专项}/` 子夹 → `{ver}/pre-release/{专项}-测试方案.md` 等平铺。
- `{workroot}/计划执行看板.md` → 合并进 `{workroot}/{ver}/test-plan.md` 后删除。
- 资料迁移前先按 文档治理规则（工作根/原件根/索引/关版整夹） 做覆盖对照，输出迁移/改名/归档候选。
- 确认后执行，不静默丢文件。
- 若存在 `{workroot}/CHANGELOG.md`：列为迁移候选——**用户确认后**改名为 `{workroot}/work-log.md`（内容按工作日志模板整理索引+里程碑条；勿与根 `CHANGELOG.md` 混淆）。
- 未确认不改名。
- 更新 `env-baseline.md`、测试计划/报告、`inbound/INDEX.md`、`docs/materials/INDEX.md`、activeContext。
- `activeContext` 合并节 `### 洞见 偏好 易踩坑` → 按 工作记忆：偏好/洞见/坑 ≤3 行 拆为 `### 生效中的偏好` + `### 洞见与易踩坑`，逐条补范围/期限/来源并删过期项。
- 不新增空节。
- 旧路径不改则注明兼容，不强迁。
- 文件冲突/无法判断归属/三项混在一个方案 → 停下问一次，不擅自覆盖。
- 迁移后核对链接与引用，再进入 baseline/context。

### 本步规则卡：文档治理

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认后将 `{workroot}/{ver}/` **整夹**迁入 `_archive/{yyyyMMdd}-{ver}/`；常青仅 smoke/scripts/capabilities/handoff 台账；「并行不关」只落新资料、不归档现行主档。
- 清理只删已知临时/缓存/未引用失败产物；不确定移 `_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 模板与证据

- **无强制模板**：§5 规则卡已给出输出形状；直接落 §2 产出。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:onboard | step=migrate | agent=onboard-agent | packet=rules/packets/onboard/migrate.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
