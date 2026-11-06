# 步骤包 · onboard/docs

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-development
- **workflow**：`onboard`
- **step**：`docs`（文档树与归档）
- **packet**：`rules/packets/onboard/docs.md`
- **角色**：`onboard-agent`（开发包接入）。挂载验收 → 生成档案/规范/activeContext → 文档树/索引/归档 → 确认入库 → 环境与工具检查（默认静默） → 按接入清单核验；本步只做该角色职责；越界交回或升级。
- **上游**：`migrate`（取其产出为本步输入；该步被 `when` 跳过时按缺口停/补齐）
- **后续**：`materials`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/onboard/_chain.md`（进 workflow 一次）。

## 2. 本步目标

- **目标**：文档树与归档
- **产出**：{workroot}/ 标准树 + {workroot}/INDEX.md + inbound/INDEX.md + docs/materials/INDEX.md + 根 CHANGELOG.md + {workroot}/work-log.md

## 3. 本步硬约束

### 开局硬门（3 条；其余见 cold-start §1）

- 1. **每轮先判、再动手**：先判新任务/续跑/只读；新任务或范围变化 → 复述目标/范围/验收并确认；续跑一行确认；只读一句话；首行锚 `route/step/packet` 或 `mode=analyze`；未确认禁写、禁下结论。
- 7. **完成只认门**：`-Claim` → `CLAIM: ALLOWED`；无 ALLOWED 禁写完成/通过/可提测。有 UI → 当前包内前端硬门；无 UI 标 `na`。
- 11. **技能闭环**：§6 必开 skill 打开→执行→回包；禁止粘贴代替。
- 其余硬约束见 `rules/core/cold-start.md` §1（常驻；勿在步内重读全文）。

### 本步读链与防丢失

- **编排**：本文 §5 +（若 §7 列出）一个模板。
- **方法质量**：§6 必开/条件开技能 → **逐个打开→执行→回本包**（一次 1 个）；禁止用粘贴代替实读。
- **禁止**：通读 rules / 多 step packet / 预读本 workflow 全部 skill。
- **完成声称**：有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **上下文锚**：`packet=`/`reads=` 必须含本 packet；切步/出子机前心跳刷新。

### 本步禁止

- 禁止读取本清单外的 rules / skills 正文；需要跳转只按 §6/§7 各一次。
- 禁止跳过 §6 必开技能，或用摘要代替实读。
- 禁止未过 §4 门或未出 §8 信号就宣称完成、推进或写「已通过」。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。
- **推进**：本步完成后沿父链进入下一未跳过步；口令为单步（只出方案/只评审/代码评审/方案评审/只提测/只出清单/轻量方案）或动作清单写明停止/跳转时，以口令/清单为准，即停并输出收尾骨架。

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 按 `rules/doc-governance.md` 定位工作根：默认单包 `docs/`，多包 `docs/development/`。 建工作区：`development-plan.md` `work-log.md` `00-governance/` `10-requirements/` `20-design/` `30-architecture/ADR/` `40-tasks/` `50-verification/` `60-release/` `70-ops/` `80-retrospectives/` `capabilities/` `handoff/` `_archive/`。
- 无内容不建空目录。 建索引：单包 `docs/INDEX.md`（即工作区索引）。
- 多包 `{workroot}/INDEX.md` + 总览 `docs/INDEX.md`（I2 保留既有目录时在总览登记「既有项目目录」）。索引只做导航，不写阶段/门。 另建控制面：`docs/materials/INDEX.md`、`inbound/INDEX.md`、`{workroot}/handoff/handoff-ledger.md`。 可运行 `rules/tools/Initialize-Docs.ps1 -ProjectRoot <项目根> -Mode single|multi -Owner development` 建骨架（只建不删）。 根 `CHANGELOG.md`：有开发规范时为本项目**产品发版史**（开发维护）。
- 无则按 `rules/templates/00-onboarding/changelog-template.md` 建空骨架。
- **禁止**写接入/文档树条目。 `{workroot}/work-log.md`：无则按 `rules/templates/00-onboarding/work-log-template.md` 创建。
- 接入完成可追加一条事件=`接入/治理`。 L2+ 建治理记录：`{workroot}/00-governance/change-log.md`、`open-items.md`、`decisions.md`。
- `{workroot}/10-requirements/requirement-ledger.md`。 原件根 `inbound/` 全索引。
- 新输入先入 `inbound/`。
- 工作区平铺归位 `{workroot}/`。 根白名单：代码/构建、README、`CHANGELOG.md`、`project-profile.md`、`activeContext.md`、`wf-*`/`wf/`、`docs/`、`inbound/`。

本步不嵌入前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回本包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/onboard/_chain.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:onboard | step=docs | agent=onboard-agent | packet=rules/packets/onboard/docs.md | reads=rules/packets/onboard/docs.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/onboard/docs.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
