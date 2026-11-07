# 步骤卡 · onboard/docs

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（本会话已读则不重读全文）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`onboard` / `docs`（文档树与归档）
- **packet**：`rules/packets/onboard/docs.md`
- **角色**：`onboard-agent`（开发包接入）。挂载验收 → 生成档案/规范/activeContext → 文档树/索引/归档 → 确认入库 → 环境与工具检查（默认静默） → 按接入清单核验；本步只做该角色职责；越界交回或升级。
- **上游**：`migrate`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`materials`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：文档树与归档
- **产出**：{workroot}/ 标准树 + {workroot}/INDEX.md + inbound/INDEX.md + docs/materials/INDEX.md + 根 CHANGELOG.md + {workroot}/work-log.md

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：本会话已读 `rules/core/global-rules.md` 则不重读全文；未读过不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。
- **推进**：本步完成后沿父链进入下一未跳过步；口令为单步（只出方案/只评审/代码评审/方案评审/只提测/只出清单/轻量方案）或动作清单写明停止/跳转时，以口令/清单为准，即停并输出收尾骨架。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 按 文档治理（工作根/原件根/索引/关版整夹） 定位工作根：默认单包 `docs/`，多包 `docs/development/`。
- 建工作区：`development-plan.md` `work-log.md` `00-governance/` `10-requirements/` `20-design/` `30-architecture/ADR/` `40-tasks/` `50-verification/` `60-release/` `70-ops/` `80-retrospectives/` `capabilities/` `handoff/` `_archive/`。
- 无内容不建空目录。
- 建索引：单包 `docs/INDEX.md`（即工作区索引）。
- 多包 `{workroot}/INDEX.md` + 总览 `docs/INDEX.md`（I2 保留既有目录时在总览登记「既有项目目录」）。
- 索引只做导航，不写阶段/门。
- 另建控制面：`docs/materials/INDEX.md`、`inbound/INDEX.md`、`{workroot}/handoff/handoff-ledger.md`。
- 可运行 `rules/tools/Initialize-Docs.ps1 -ProjectRoot <项目根> -Mode single|multi -Owner development` 建骨架（只建不删）。
- 根 `CHANGELOG.md`：有开发规范时为本项目**产品发版史**（开发维护）。
- 无则按 `rules/templates/00-onboarding/changelog-template.md` 建空骨架。
- **禁止**写接入/文档树条目。
- `{workroot}/work-log.md`：无则按 `rules/templates/00-onboarding/work-log-template.md` 创建。
- 接入完成可追加一条事件=`接入/治理`。
- L2+ 建治理记录：`{workroot}/00-governance/change-log.md`、`open-items.md`、`decisions.md`。
- `{workroot}/10-requirements/requirement-ledger.md`。
- 原件根 `inbound/` 全索引。
- 新输入先入 `inbound/`。
- 工作区平铺归位 `{workroot}/`。
- 根白名单：代码/构建、README、`CHANGELOG.md`、`project-profile.md`、`activeContext.md`、`wf-*`/`wf/`、`docs/`、`inbound/`。

### 本步规则卡：文档治理

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认后将迭代绑定文档迁入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`；主档关闭时快照、主档不移动；「并行不关」只落新资料、不归档现行主档。
- 清理只删已知临时/缓存/未引用失败产物；不确定移 `_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/00-onboarding/changelog-template.md`；只读本步用到的节，禁止整文件通读。
- **参考模板（命中再开，不默认读）**：`rules/templates/00-onboarding/work-log-template.md`。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:onboard | step=docs | agent=onboard-agent | packet=rules/packets/onboard/docs.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
