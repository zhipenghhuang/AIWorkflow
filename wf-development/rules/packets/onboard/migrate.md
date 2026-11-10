# 步骤卡 · onboard/migrate

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（每步先读并逐条过）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`onboard` / `migrate`（旧项目迁移）
- **packet**：`rules/packets/onboard/migrate.md`
- **角色**：`onboard-agent`（开发包接入）。挂载验收 → 生成档案/规范/activeContext → 文档树/索引/归档 → 确认入库 → 环境与工具检查（默认静默） → 按接入清单核验；本步只做该角色职责；越界交回或升级。
- **上游**：`profile`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`docs`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：旧项目迁移
- **产出**：迁移清单/更新后的路径

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：每步读 `rules/core/global-rules.md` 并逐条过；本步未读不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_docs_migration`**：出示分类/覆盖对照/拟归档或清理清单与目标；确认后执行
- **条件判定 `hitl:docs_migration_needed`**：将搬迁/归档/清理且清单未确认；满足→真，否则跳过该门。
- **推进**：本步完成后沿父链进入下一未跳过步；口令为单步（只出方案/只出轻量方案/只评审/代码评审/方案评审/只提测/只出清单）或动作清单写明停止/跳转时，以口令/清单为准，即停并输出收尾骨架。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 「重新接入」先扫描旧结构，按 文档治理规则（工作根/原件根/索引/关版整夹） 做覆盖对照，列迁移/改名/归档候选，经 `confirm_docs_migration` 确认后执行，不静默丢文件。
- docs 步不再重复确认。
- **工作根**按 文档治理规则（工作根/原件根/索引/关版整夹） 定位。
- **原件根 `inbound/`** 只登记/整理，主副本不迁入 `{workroot}/`。
- `keep`/`mix`/`replace` 只管原件结构（仍无 `_archive/`）。
- 均允许索引/复制/吸收。
- 原件禁止迁入 `{workroot}/`。
- 旧 `inbound/项目文档/{ver}/`、`inbound/原始素材/`、旧扁平前缀 → `inbound/{ver|topic}/` 或 `inbound/_common/`。
- 旧工作区 `inbound/` 副本先判定，不直接当原件。
- 材料库只收定稿。
- 更新 `project-profile.md`、`{workroot}/INDEX.md`、`inbound/INDEX.md`、`docs/materials/INDEX.md`、开发计划链接、activeContext。
- `activeContext` 合并节 `### 洞见 偏好 易踩坑` → 按 工作记忆：偏好/洞见/坑 ≤3 行 拆为 `### 生效中的偏好` + `### 洞见与易踩坑`，逐条补范围/期限/来源并删过期项。
- 不新增空节。
- 冲突/无法判断先问一次，不覆盖。
- 迁移后核对链接，再进入 docs/control 步。

### 本步规则卡：文档治理

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认后将迭代绑定文档迁入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`；主档关闭时快照、主档不移动；「并行不关」只落新资料、不归档现行主档。
- 清理只删已知临时/缓存/未引用失败产物；不确定移 `_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

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
