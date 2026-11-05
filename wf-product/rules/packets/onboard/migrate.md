# 步骤包 · onboard/migrate

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：产品
- **workflow**：`onboard`
- **step**：`migrate`（旧结构迁移）
- **packet**：`rules/packets/onboard/migrate.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/onboard/_chain.md`（进 workflow 一次）。

## 2. 本步目标

- **目标**：旧结构迁移
- **产出**：迁移清单/更新后的路径

## 3. 本步硬约束

### 开局硬约束（本步可执行摘要）

- 1. **先意图、再动作**（`confirm_task_intent`）：未确认禁写正式 PRD/外发/定范围。
- 2. **短读跟随 + 一手源**：`activeContext` + 进行中（`packet=`/`region=`）+ 偏好/洞见/坑 ≤3。
- 3. **理解→方案双确认未完成 → 不得入池/写正式 PRD/定版本范围**。
- 4. **状态机读链 + 技能闭环**：见本包「本步读链与防丢失」。必开 skill 须打开→执行→回步骤包（质量不降）。
- 5. **完成分层**：`-Claim -Mode <…>` → 只认 `CLAIM: ALLOWED`。
- 6. **原型硬门**：实走 + 覆盖矩阵；缺行不得过。
- 7. **禁臆造**；AC 可观测；变更无单不实施；UAT 未过不发布。
- 8. **切步/出子机 → 心跳**，必带 `packet=`。

### 本步读链与防丢失

- **编排**：本文 §5 +（若 §7 列出）一个模板。
- **方法质量**：§6 必开/条件开技能 → **打开→执行→回本包**（同时 1 个 skill）；禁止用粘贴代替实读。
- **禁止**：通读 rules / 多 step packet / 预读本 workflow 全部 skill。
- **完成声称**：有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **上下文锚**：`packet=`/`reads=` 必须含本 packet；切步/出子机前心跳刷新。


## 4. 本步门

- **HITL `confirm_docs_migration`**：出示分类/覆盖对照/拟归档或清理清单与目标；确认后执行；不擅自删、不覆盖

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

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

## 6. 技能指向（打开 → 执行 → 回本包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/onboard/_chain.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:onboard | step=migrate | packet=rules/packets/onboard/migrate.md | reads=rules/packets/onboard/migrate.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/onboard/migrate.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
