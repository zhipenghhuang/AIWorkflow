# 步骤包 · onboard/profile

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：产品
- **workflow**：`onboard`
- **step**：`profile`（产品档案与上下文）
- **packet**：`rules/packets/onboard/profile.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/onboard/_chain.md`（进 workflow 一次）。

## 2. 本步目标

- **目标**：产品档案与上下文
- **产出**：product-profile.md · activeContext.md · {workroot}/work-log.md（如无）·（模板 rules/templates/）

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

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- **按实填档（硬）**：建档前有界探查（`{workroot}/`、既有 PRD/计划/用户材料若有）。档案第一节须含一句话定位、目标用户、workroot（未声明按约定）、`integration_level`（绿场默认 I3，存量必问）、`inbound_structure`（默认 mix）。
- 第二～四节据实填或「无」/「待确认」。
- `流程偏好` 按计划与 PRD 存量推断（轻量优先/完整优先。
- 用户可改，不额外提问。
- 轻量≠降 AC/门/评审）。**禁止**占位符未换就打「wf-product onboard: done」。 有根 `README.md` 则按**其实际结构**择要取用。
- 细则见 `rules/core/project-readme.md`。根 README 按用户偏好选档后写（模板仅素材）。
- 已有不覆盖。
- 点名生成/更新/整理时对照市面高标准给可选补强。 缺陷平台可选：问是否启用禅道/Jira/ONES，启用填 provider/baseUrl/凭据来源/提交方式/适配定义， 未启用写「无」。
- 同项目已有开发/测试包配置可复用，不重复存凭据。缺陷平台未配置不阻塞接入。 `activeContext.md`：无则按 `rules/templates/00-onboarding/active-context-template.md` 建（**总览一句话** + `## 产品` + 跨包同步 + 运行时本包行）。
- 已有则只补/更新总览（若空）、本包分节与本包接入行，禁止整文件覆盖他包内容。总览口径对齐产品档案「一句话定位」。 `{workroot}/work-log.md`：无则按 `rules/templates/00-onboarding/work-log-template.md` 创建（岗位里程碑侧记。
- 索引可空）。已有则跳过不覆盖。接入完成可追加事件=`接入/治理`。 **不是**根 `CHANGELOG.md`、也不是产品计划 执行日志。
- 勿把本文件当产品发版史。 若仍存在 `{workroot}/CHANGELOG.md` 且尚无 `{workroot}/work-log.md`：列为改名迁移候选（→`work-log.md`），经 `confirm_docs_migration` 确认后执行。
- 未确认不改。 **禁止**创建/修改/补链项目根 `CHANGELOG.md`（仅开发维护）。无开发包 → 不建根 CHANGELOG。
- 岗位史只用本包工作日志。用户点名要项目发版史 → 建议接入开发包或由其指定写手。
- 本包默认不替建。 按 `rules/doc-governance.md` 定位工作根。
- 登记原件根 `inbound/INDEX.md`。
- 权威文档库 `docs/materials/`。 建 `docs/materials/INDEX.md` 骨架。
- 外部输入先入 `inbound/`。 建索引：单包 `docs/INDEX.md`（含工作区导航）。
- 多包 `{workroot}/INDEX.md` + 总览 `docs/INDEX.md`（I2 在总览登记既有目录）。
- 不写阶段/门。 产品档案 增记工作根 / `inbound/` 原件根 / `docs/materials/` 权威文档库。 对外用户文档固定 `{workroot}/user/`，不混入 `inbound/`。

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
route=workflow:onboard | step=profile | packet=rules/packets/onboard/profile.md | reads=rules/packets/onboard/profile.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/onboard/profile.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
