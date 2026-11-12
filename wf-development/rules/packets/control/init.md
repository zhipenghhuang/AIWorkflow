# 步骤卡 · control/init

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`control` / `init`（初始化开发计划）
- **packet**：`rules/packets/control/init.md`
- **角色**：`iterate-lead`（迭代交付编排）。方案/需求 → 任务清单（含 DoR/DoD）→ 确认节奏 → 编排实施（实施交 implementer）→ 评审/门禁 → 提测 → 总结拟提交；本步只做该角色职责；越界交回或升级。
- **上游**：无（链首）
- **后续**：`run`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：初始化开发计划
- **产出**：开发计划（{workroot}/development-plan.md）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_plan`**：首次创建或范围·版本·里程碑实质变更；确认后计划状态=已确认；未关闭 S 或阻塞实施的 P 未答复时不得确认（`clarification.md` §1.1）
- **条件判定 `hitl:plan_needs_confirm`**：计划/范围/节奏实质变且未确认；满足→真，否则跳过该门。
- **HITL `confirm_iteration_close`**：出示当前迭代标识、未完成项、拟归档摘要、下一迭代标识；确认「结束当前并进入下一」后才按 文档治理规则（工作根/原件根/索引/关版整夹） 关账；选「并行不关」则只落新资料不归档现行绑定主档。**关闭=停止新范围/冻结版本线，不停止测试**：测试与缺陷修复可继续（走 patch），归档待测试完成；测试未完又要开新迭代，优先「并行不关」
- **条件判定 `hitl:iteration_close_needed`**：探测到下一期/换主题/升级且是否关本期不明；满足→真，否则跳过该门。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`development-plan` → 见 §6 闭环。

- **条件技能**：`product-doc-analysis`（输入含 PRD/原型/产品文档）、`product-shaping`（无 PRD/只有想法） → 命中则同样走 §6 闭环。

### 本步动作清单

- 先判换迭代：新方案/新版本到达且当前迭代未关闭 → STOP `confirm_iteration_close`。
- 未决前只做入站/理解/待确认，不得替换 `development-plan.md` 或归档现行绑定文档。
- 本步只建/更新开发计划，不自动执行后续阶段。
- 要推进说「按开发计划执行」。
- 技能见 §6 `development-plan`（先读再做）。
- 模板 `rules/templates/10-planning/development-plan-template.md`。
- 命名：本文档=开发计划（总览/开发轨总控）。
- S3=任务与排期（任务清单/依赖/估算/DoR/DoD/检查点），是计划里的一个阶段。
- 路径：默认 `{workroot}/development-plan.md`。
- 需按治理分区时用 `{workroot}/00-governance/development-plan.md`。
- 旧项目以 `project-profile.md` 声明为准。
- 输入：PRD/原型/AC/接口/仓库/环境（能拿到多少写多少；缺口写 并由用户提供/选择已有资料）。
- 无 PRD/只有想法 → 先按 §6 `product-shaping` 给产品判断（问题/用户/价值/MVP/非目标/成功标准），再填。
- 不强制产品定义卡。
- 输入含 PRD/迭代方案/原型 → 先按 §6 `product-doc-analysis` 产出理解摘要/理解包（来源/目标/范围/F-R-AC/冲突/GAP/置信度）。
- S0 未完成理解确认不得进入 S1/S2。
- 新建：复制模板，填 一页状态（计划状态/当前门/下一动作/需人工）、 输入/外部输入、 阶段表（S0 进行中，其余未开始；每阶段“技能”列必填）、 变更、 执行日志、 归档索引。
- 建 `{workroot}/handoff/handoff-ledger.md`（模板 `rules/templates/90-handoff/handoff-ledger-template.md`）。
- 按模板登记 REQ/DES/PLAN/QA/TEST/FIX/REL 节点。
- 无跨角色交接可不建包，但台账保留。
- L2+ 同时确认 需求台账/变更记录/待决项/决策记录/`inbound/` + `inbound/INDEX.md` 存在。
- 无则按模板补。
- 每阶段按阶段表“技能”列加载技能。
- S2 技术方案按变更面加载 technology-selection/database-design/api-design/frontend-design/threat-modeling/performance-and-capacity，不要求全读。
- 已存在：不覆盖。
- 读现状后转 sync，避免丢失进度。
- L0 微改可写「不适用」。
- L2+ 新项目/新产品默认启用。
- 不强制引用其它包。
- confirm_plan：首次创建/范围·版本·里程碑实质变更时，出示阶段/范围/门/下一步请确认。
- 确认后计划状态=已确认。
- 范围·版本实质变更或换主题（即使不发版）→ 按 文档治理规则（工作根/原件根/索引/关版整夹）。
- 不确定则 `confirm_iteration_close`。
- 确认后先判 T1/T2/T4，再按 关账（T2/T4 保留仍被引用的基础设计/流程图/原型）。
- 关账 materials：**必做**覆盖刷新关闭版 `{prev}/`→superseded，再建 `{next}/` current（默认覆盖最新）。
- 输出首条：route=workflow:control | step=init | stage=S0 | gate=G0 | next_action=补输入/需求分析。

### 本步规则卡：文档治理

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认后将迭代绑定文档迁入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`；主档关闭时快照、主档不移动；「并行不关」只落新资料、不归档现行主档。
- 清理只删已知临时/缓存/未引用失败产物；不确定移 `_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。
> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `development-plan` | **必开** | 进入本步即开（质量不降） | `skills/development-plan/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `product-doc-analysis` | 条件开 | 输入含 PRD/原型/产品文档 | `skills/product-doc-analysis/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `product-shaping` | 条件开 | 无 PRD/只有想法 | `skills/product-shaping/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/10-planning/development-plan-template.md`；只读本步用到的节，禁止整文件通读。
- **参考模板（命中再开，不默认读）**：`rules/templates/90-handoff/handoff-ledger-template.md`。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:control | step=init | agent=iterate-lead | packet=rules/packets/control/init.md | global=ok | skills=development-plan|done|na | claim=ALLOWED|DENIED|na | next=…
```
