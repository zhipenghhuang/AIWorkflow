# 步骤卡 · onboard/migrate

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（本会话已读则不重读全文）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`onboard` / `migrate`（旧结构迁移）
- **packet**：`rules/packets/onboard/migrate.md`
- **角色**：`onboard-agent`（产品包接入）。挂载验收 → 生成产品档案/activeContext → 确认入库 →（可选）能力检查 → 按接入清单核验 → 写入接入标记；本步只做该角色职责；越界交回或升级。
- **上游**：无（链首）
- **后续**：`mount`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：旧结构迁移
- **产出**：迁移清单/更新后的路径

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：本会话已读 `rules/core/global-rules.md` 则不重读全文；未读过不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_docs_migration`**：出示分类/覆盖对照/拟归档或清理清单与目标；确认后执行；不擅自删、不覆盖
- **条件判定 `hitl:docs_migration_needed`**：有未登记资料、拟改名/搬迁/归档、工作文档清理或旧结构迁移；满足→真，否则跳过该门。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 「重新接入」= 按现行文档治理规则迁移。
- 先扫描旧结构，按 文档治理（工作根/原件根/索引/关版整夹） 做覆盖对照，列迁移/改名/归档候选，经 `confirm_docs_migration` 确认后执行，不静默丢文件。
- 映射：`{workroot}/输入/`、`inbound/项目文档/{ver}/`、旧扁平前缀文件、`inbound/反馈|调研|竞品|数据/` → `inbound/{ver|topic}/` 或 `_common/`（保持原文件名；类型写索引；**不要**项目文档层、**不要**强制类型前缀扁平）。
- 旧工作区/资料副本先判定：原件进 `inbound/`，定稿进 `docs/materials/`，过程稿进工作区。
- 建立/更新 `{workroot}/INDEX.md`、原件登记 `inbound/INDEX.md`。
- 更新计划、路径引用、activeContext。
- `activeContext` 合并节 `### 洞见 偏好 易踩坑` → 按 工作记忆：偏好/洞见/坑 ≤3 行 拆为 `### 生效中的偏好` + `### 洞见与易踩坑`，逐条补范围/期限/来源并删过期项。
- 不新增空节。
- 冲突/无法判断先问一次，不覆盖。
- 迁移后核对链接，再进入 mount/profile。
- 若存在 `{workroot}/CHANGELOG.md`：列为迁移候选——**用户确认后**改名为 `{workroot}/work-log.md`（内容按工作日志模板整理索引+里程碑条；勿与根 `CHANGELOG.md` 混淆）。
- 未确认不改名。
- 共用原件根 `inbound/`：认根=用户指定优先，否则判定表，不定则问。
- 原夹文件不迁出。
- `keep`/`mix`/`replace` 只管原树。
- 仍可索引/复制/吸收。
- 中途存量全索引，按需复制或 A0～A2。

### 本步规则卡：文档治理

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认后将迭代绑定文档迁入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`；主档关闭时快照、主档不移动；「并行不关」只落新资料、不归档现行主档。
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
