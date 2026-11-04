# 步骤包 · onboard/profile

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`onboard`
- **step**：`profile`（产品档案与上下文）
- **packet**：`rules/packets/onboard/profile.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：产品档案与上下文
- **产出**：product-profile.md · activeContext.md · {workroot}/work-log.md（如无）·（模板 rules/templates/）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- **按实填档（硬）**：建档前有界探查（`{workroot}/`、既有 PRD/计划/用户材料若有）。档案第一节须含一句话定位、目标用户、workroot（未声明按约定）、`integration_level`（绿场默认 I3，存量必问）、`inbound_structure`（默认 mix）；第二～四节据实填或「无」/「待确认」； `流程偏好` 按计划与 PRD 存量推断（轻量优先/完整优先；用户可改，不额外提问；轻量≠降 AC/门/评审）。**禁止**占位符未换就打「wf-product onboard: done」。 有根 `README.md` 则按**其实际结构**择要取用；细则见 `rules/core/project-readme.md`。根 README 按用户偏好选档后写（模板仅素材）；已有不覆盖；点名生成/更新/整理时对照市面高标准给可选补强。 缺陷平台可选：问是否启用禅道/Jira/ONES，启用填 provider/baseUrl/凭据来源/提交方式/适配定义， 未启用写「无」；同项目已有开发/测试包配置可复用，不重复存凭据。缺陷平台未配置不阻塞接入。 `activeContext.md`：无则按 `rules/templates/00-onboarding/active-context-template.md` 建（**总览一句话** + `## 产品` + 跨包同步 + 运行时本包行）；已有则只补/更新总览（若空）、本包分节与本包接入行，禁止整文件覆盖他包内容。总览口径对齐产品档案「一句话定位」。 `{workroot}/work-log.md`：无则按 `rules/templates/00-onboarding/work-log-template.md` 创建（岗位里程碑侧记；索引可空）。已有则跳过不覆盖。接入完成可追加事件=`接入/治理`。 **不是**根 `CHANGELOG.md`、也不是产品计划 执行日志；勿把本文件当产品发版史。 若仍存在 `{workroot}/CHANGELOG.md` 且尚无 `{workroot}/wo

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

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
route=workflow:onboard | step=profile | reads=rules/packets/onboard/profile.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/onboard/profile.md`；对不上 = 未遵守读链。
