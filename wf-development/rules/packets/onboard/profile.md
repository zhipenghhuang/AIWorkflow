# 步骤包 · onboard/profile

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`onboard`
- **step**：`profile`（档案与规范）
- **packet**：`rules/packets/onboard/profile.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：档案与规范
- **产出**：project-profile.md（含 §7 技术要点事实摘要 / §8 交付治理 / §9 文档归档）· activeContext.md

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- **按实填档（硬）**：建档前有界探查仓库实情（依赖/目录/入口/构建与测试命令）；有根 `README.md` 则按**其实际结构**择要取用（不规定章节，见 `rules/core/project-readme.md`）。按 rules/templates/00-onboarding/project-profile-template.md 建档； 一句话定位、workroot（未声明按约定）、`integration_level`（绿场默认 I3，存量必问）、`inbound_structure`（默认 mix）、 代码地图/门禁、/ 据实填或「无」/「待确认」；**禁止**占位符未换就打「wf-development onboard: done」。 **根 README**：按用户偏好选档后写（见 `rules/core/project-readme.md`）；模板仅素材；已有不覆盖；点名生成/更新/整理时对照市面高标准给可选补强。 按 `rules/templates/00-onboarding/version-policy-template.md` 产 `{workroot}/60-release/versioning.md`（版本格式/升级/环境/tag/审批；不确定写「待确认」）。 记工作根、`inbound/` 原件根、`docs/materials/` 权威文档库。 推断并填写 `协作模式`/`流程偏好`：单包+无计划/测试/产品/交接 → 单人/轻量优先；多包或已有计划/QA/交接 → 团队/完整优先；用户可改，不额外提问。轻量优先=入口偏好，不降 AC/完成门/开发自验（`lightweight.md` ）。 `activeContext.md`：无则按 `rules/templates/00-onboarding/active-context-template.md` 建（**总览一句话** + `## 开发` + 跨包同步 + 运行时本包行）；已有则只补/更新总览（若空）、本包分节与本包接入行，禁止整文件覆盖他包内容。总览口径对齐项目档案「一句

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 本步动作清单

- **按实填档（硬）**：建档前有界探查仓库实情（依赖/目录/入口/构建与测试命令）。
- 有根 `README.md` 则按**其实际结构**择要取用（不规定章节，见 `rules/core/project-readme.md`）。按 rules/templates/00-onboarding/project-profile-template.md 建档。
- 一句话定位、workroot（未声明按约定）、`integration_level`（绿场默认 I3，存量必问）、`inbound_structure`（默认 mix）、 代码地图/门禁、/ 据实填或「无」/「待确认」。
- **禁止**占位符未换就打「wf-development onboard: done」。 **根 README**：按用户偏好选档后写（见 `rules/core/project-readme.md`）。
- 模板仅素材。
- 已有不覆盖。
- 点名生成/更新/整理时对照市面高标准给可选补强。 按 `rules/templates/00-onboarding/version-policy-template.md` 产 `{workroot}/60-release/versioning.md`（版本格式/升级/环境/tag/审批。
- 不确定写「待确认」）。 记工作根、`inbound/` 原件根、`docs/materials/` 权威文档库。 推断并填写 `协作模式`/`流程偏好`：单包+无计划/测试/产品/交接 → 单人/轻量优先。
- 多包或已有计划/QA/交接 → 团队/完整优先。
- 用户可改，不额外提问。轻量优先=入口偏好，不降 AC/完成门/开发自验（`lightweight.md` ）。 `activeContext.md`：无则按 `rules/templates/00-onboarding/active-context-template.md` 建（**总览一句话** + `## 开发` + 跨包同步 + 运行时本包行）。
- 已有则只补/更新总览（若空）、本包分节与本包接入行，禁止整文件覆盖他包内容。总览口径对齐项目档案「一句话定位」。 认根：用户指定优先。
- 否则按 `rules/doc-governance.md`。
- 不确定问用户。登记后默认 `mix`。
- 可改 keep/replace。工作根按 定位（档案声明优先，否则单包 `docs/`、多包 `docs/development/`）。 技术要点少 → 内联档案 事实摘要（勿为几行另建目录）。
- 无对应栈写「不适用」。 旧结构迁移（一次性）：检测到 `项目规范/` 目录 → 一问：并入 事实摘要并删除目录（默认建议）。 产出后进入 docs 步建立文档树/索引。

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
