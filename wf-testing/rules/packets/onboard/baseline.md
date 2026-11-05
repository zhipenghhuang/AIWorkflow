# 步骤包 · onboard/baseline

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-testing
- **workflow**：`onboard`
- **step**：`baseline`（挂载与基线）
- **packet**：`rules/packets/onboard/baseline.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/onboard/_chain.md`（进 workflow 一次）。

## 2. 本步目标

- **目标**：挂载与基线
- **产出**：env-baseline.md（§1/§2.1/§2.2/§8）· {workroot}/work-log.md（如无）

## 3. 本步硬约束

### 开局硬约束（本步可执行摘要）

- 1. **先意图、再动作**（`confirm_task_intent`）：未确认禁生成正式用例/交平台。
- 2. **短读跟随 + 一手源**：`activeContext` + 进行中（`packet=`/`region=`）+ 偏好/洞见/坑 ≤3。
- 3. **依据先建模**：分析表 §0；无 §0 禁正式生成与功能准出。
- 4. **状态机读链 + 技能闭环**：见本包「本步读链与防丢失」。必开 skill 须打开→执行→回步骤包（质量不降）。
- 5. **完成分层**：`-Claim -Mode report|writeback` → 只认 `CLAIM: ALLOWED`。
- 6. **UI 证据 E1**：实点 + 截图/Network；E0 不得单独 pass。
- 7. **能脚本不 AI**；禁刷绿；P0 未过不得整体通过。
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
route=workflow:onboard | step=baseline | packet=rules/packets/onboard/baseline.md | reads=rules/packets/onboard/baseline.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/onboard/baseline.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
