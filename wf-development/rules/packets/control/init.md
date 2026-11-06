# 步骤包 · control/init

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-development
- **workflow**：`control`
- **step**：`init`（初始化开发计划）
- **packet**：`rules/packets/control/init.md`
- **角色**：`iterate-lead`（迭代交付编排）。方案/需求 → 任务清单（含 DoR/DoD）→ 确认节奏 → 编排实施（实施交 implementer）→ 评审/门禁 → 提测 → 总结拟提交；本步只做该角色职责；越界交回或升级。
- **上游**：无（链首）
- **后续**：`run`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/control/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/control/_region-steer.md`（总控推进；进本区一次）。

## 2. 本步目标

- **目标**：初始化开发计划
- **产出**：开发计划（{workroot}/development-plan.md）

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

- **HITL `confirm_plan`**：首次创建或范围·版本·里程碑实质变更；确认后计划状态=已确认
- **HITL `confirm_iteration_close`**：出示当前迭代标识、未完成项、拟归档摘要、下一迭代标识；确认「结束当前并进入下一」后才按 `rules/doc-governance.md` §7.1 关账；选「并行不关」则只落新资料不归档现行绑定主档。**关闭=停止新范围/冻结版本线，不停止测试**：测试与缺陷修复可继续（走 patch），归档待测试完成；测试未完又要开新迭代，优先「并行不关」
- **推进**：本步完成后沿父链进入下一未跳过步；口令为单步（只出方案/只评审/代码评审/方案评审/只提测/只出清单/轻量方案）或动作清单写明停止/跳转时，以口令/清单为准，即停并输出收尾骨架。

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`development-plan` → 见 §6 闭环。

- **条件技能**：`product-doc-analysis`（输入含 PRD/原型/产品文档） → 命中则同样走 §6 闭环。

### 本步动作清单

- 本步只建/更新开发计划，不自动执行后续阶段。
- 要推进说「按开发计划执行」。 技能：`skills/development-plan/SKILL.md`（先读再做）。
- 模板 `rules/templates/10-planning/development-plan-template.md`。 命名：本文档=开发计划（总览/开发轨总控）。
- S3=任务与排期（任务清单/依赖/估算/DoR/DoD/检查点），是计划里的一个阶段。 路径：默认 `{workroot}/development-plan.md`。
- 需按治理分区时用 `{workroot}/00-governance/development-plan.md`。
- 旧项目以 `project-profile.md` 声明为准。 输入：PRD/原型/AC/接口/仓库/环境（能拿到多少写多少。
- 缺口写 并由用户提供/选择已有资料）。 无 PRD/只有想法 → 先按 `skills/product-shaping/SKILL.md` 给产品判断（问题/用户/价值/MVP/非目标/成功标准），再填。
- 不强制产品定义卡。 输入含 PRD/迭代方案/原型 → 先按 `skills/product-doc-analysis/SKILL.md` 产出理解摘要/理解包（来源/目标/范围/F-R-AC/冲突/GAP/置信度）。
- S0 未完成理解确认不得进入 S1/S2。 新建：复制模板，填 一页状态（计划状态/当前门/下一动作/需人工）、 输入/外部输入、 阶段表（S0 进行中，其余未开始。
- 每阶段“技能”列必填）、 变更、 执行日志、 归档索引。 建 `{workroot}/handoff/handoff-ledger.md`（模板 `rules/templates/90-handoff/handoff-ledger-template.md`）。
- 按模板登记 REQ/DES/PLAN/QA/TEST/FIX/REL 节点。
- 无跨角色交接可不建包，但台账保留。 L2+ 同时确认 需求台账/变更记录/待决项/决策记录/`inbound/` + `inbound/INDEX.md` 存在。
- 无则按模板补。 每阶段按阶段表“技能”列加载技能。
- S2 技术方案按变更面加载 02A/02B/02C/02D/02E/02F，不要求全读。 已存在：不覆盖。
- 读现状后转 sync，避免丢失进度。 L0 微改可写「不适用」。
- L2+ 新项目/新产品默认启用。
- 不强制引用其它包。 confirm_plan：首次创建/范围·版本·里程碑实质变更时，出示阶段/范围/门/下一步请确认。
- 确认后计划状态=已确认。 范围·版本实质变更或换主题（即使不发版）→ 按 `rules/doc-governance.md`。
- 不确定则 `confirm_iteration_close`。
- 确认后先判 T1/T2/T4，再按 关账（T2/T4 保留仍被引用的基础设计/流程图/原型）。 关账 materials：**必做**覆盖刷新关闭版 `{prev}/`→superseded，再建 `{next}/` current（默认覆盖最新）。 输出首条：route=workflow:control | step=init | stage=S0 | gate=G0 | next_action=补输入/需求分析。

本步不嵌入前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回本包）

> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `development-plan` | **必开** | 进入本步即开（质量不降） | `skills/development-plan/SKILL.md` | 必做区 → 回本包 |
| `product-doc-analysis` | 条件开 | 输入含 PRD/原型/产品文档 | `skills/product-doc-analysis/SKILL.md` | 必做区 → 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/control/_chain.md`。
- 子状态机（进区一次）：`rules/packets/control/_region-steer.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:control | step=init | agent=iterate-lead | packet=rules/packets/control/init.md | reads=rules/packets/control/init.md[+skill] | skills=development-plan,product-doc-analysis|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/control/init.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
