# 步骤包 · onboard/baseline

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：测试轨
- **workflow**：`onboard`
- **step**：`baseline`（挂载与基线）
- **packet**：`rules/packets/onboard/baseline.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：挂载与基线
- **产出**：env-baseline.md（§1/§2.1/§2.2/§8）· {workroot}/work-log.md（如无）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 挂载：按 `rules/templates/00-onboarding/root-agents-pointer.md` 补入薄指针（追加不覆盖）；单包指向本包，多包指向 `wf/AGENTS.md`；不写包装载说明。 **按实填档（硬）**：建档前有界探查（预览地址/`{workroot}/`/既有计划若有）。「项目身份」写 workroot（未声明按约定）、`integration_level`（绿场默认 I3，存量必问）、`inbound_structure`（默认 mix）、`流程偏好`（按计划与级别推断；用户可改，不额外提问）；基线登录/设计输入/入库/浏览器能力索引节据实填；**禁止**占位符未换就打「wf-testing onboard: done」。 有根 `README.md` 则按**其实际结构**择要取用；细则见 `rules/core/project-readme.md`。根 README 按用户偏好选档后写（模板仅素材）；已有不覆盖；点名生成/更新/整理时对照市面高标准给可选补强。 按 `rules/doc-governance.md` 定位工作根；登记原件根 `inbound/INDEX.md`；权威文档库 `docs/materials/`。 建索引：单包 `docs/INDEX.md`（含工作区导航）；多包 `{workroot}/INDEX.md` + 总览 `docs/INDEX.md`（I2 在总览登记既有目录）；不写阶段/门。 多包模式：根 `AGENTS.md` 只写薄指针（先读 `wf/AGENTS.md`）；按 `rules/templates/00-onboarding/wf-agents-routing-template.md` 生成/补齐 `wf/AGENTS.md`，只列已装包；已有则只补行，不覆盖。 接入级别：绿场默认 I3；存量/杂乱必问；I0 只写现场树+映射，I2 新写只进标准树；确认 `inbound_structure`（默认 mix）；写 `env-baseline.md` 的 workroot / `i

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 本步动作清单

- 挂载：按 `rules/templates/00-onboarding/root-agents-pointer.md` 补入薄指针（追加不覆盖）。
- 单包指向本包，多包指向 `wf/AGENTS.md`。
- 不写包装载说明。 **按实填档（硬）**：建档前有界探查（预览地址/`{workroot}/`/既有计划若有）。「项目身份」写 workroot（未声明按约定）、`integration_level`（绿场默认 I3，存量必问）、`inbound_structure`（默认 mix）、`流程偏好`（按计划与级别推断。
- 用户可改，不额外提问）。
- 基线登录/设计输入/入库/浏览器能力索引节据实填。
- **禁止**占位符未换就打「wf-testing onboard: done」。 有根 `README.md` 则按**其实际结构**择要取用。
- 细则见 `rules/core/project-readme.md`。根 README 按用户偏好选档后写（模板仅素材）。
- 已有不覆盖。
- 点名生成/更新/整理时对照市面高标准给可选补强。 按 `rules/doc-governance.md` 定位工作根。
- 登记原件根 `inbound/INDEX.md`。
- 权威文档库 `docs/materials/`。 建索引：单包 `docs/INDEX.md`（含工作区导航）。
- 多包 `{workroot}/INDEX.md` + 总览 `docs/INDEX.md`（I2 在总览登记既有目录）。
- 不写阶段/门。 多包模式：根 `AGENTS.md` 只写薄指针（先读 `wf/AGENTS.md`）。
- 按 `rules/templates/00-onboarding/wf-agents-routing-template.md` 生成/补齐 `wf/AGENTS.md`，只列已装包。
- 已有则只补行，不覆盖。 接入级别：绿场默认 I3。
- 存量/杂乱必问。
- I0 只写现场树+映射，I2 新写只进标准树。
- 确认 `inbound_structure`（默认 mix）。
- 写 `env-baseline.md` 的 workroot / `integration_level` / `inbound_structure`。 建本包资料副本区骨架（可先空）。
- 禁 `项目文档/`。 `{workroot}/work-log.md`：无则按模板创建。
- 已有跳过。接入完成可追加事件=`接入/治理`。若有 `{workroot}/CHANGELOG.md` 且无工作日志 → 改名候选（确认后执行）。 **禁止**创建/修改/补链根 `CHANGELOG.md`（仅开发维护）。无开发包 → 不建根。
- 岗位史只用本包工作日志。 `env-baseline.md`：先填「项目身份」。
- 记原件根 `inbound/` + 本包副本根。
- 资料模式默认 mix（keep 仍可复制/吸收）。 存量全索引。
- 按需复制/A0～A2 吸收。 **禁**类型前缀扁平。
- **禁**再建 `项目文档/`。不建 `{workroot}/计划执行看板.md`。

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
route=workflow:onboard | step=baseline | reads=rules/packets/onboard/baseline.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/onboard/baseline.md`；对不上 = 未遵守读链。
