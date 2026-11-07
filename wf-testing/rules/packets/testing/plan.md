# 步骤卡 · testing/plan

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（本会话已读则不重读全文）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`testing` / `plan`（分析并生成测试计划）
- **packet**：`rules/packets/testing/plan.md`
- **角色**：`test-planner`（测试分析 / 测试计划（总排））。先完整分析主读（来源/AC/设计点/意图/风险/Oracle），再产出可执行的 {workroot}/{ver}/test-plan.md；本步只做该角色职责；越界交回或升级。
- **上游**：无（链首）
- **后续**：`execute`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：分析并生成测试计划
- **产出**：{workroot}/{ver}/test-analysis.md（必做；来源/AC/设计点/意图/风险/覆盖）+ {workroot}/{ver}/test-plan.md（总排）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：本会话已读 `rules/core/global-rules.md` 则不重读全文；未读过不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `select_mainread`**：主读路径未确认 → STOP 一问；已点名/唯一正式版已在依据清单写明 → 可续，不重问。
- **条件判定 `hitl:mainread_unspecified`**：plan/探索 execute 主读未确认；满足→真，否则跳过该门。
- **HITL `confirm_understanding`**：**主屏**：分析 §0 摘要、来源盘点计数、AC/设计点覆盖、关键歧义/冲突、P0 意图与 Oracle；确认后才写计划。
- **条件判定 `hitl:understanding_needs_confirm`**：输入含 PRD/方案/原型/接口，存在 2 个以上实质歧义/冲突，T2/T3，或用户要求计划/准出且未确认分析；满足→真，否则跳过该门。
- **HITL `confirm_plan`**：版本级首版/换代，或范围/准出/缺陷策略实质变更 → STOP 一行摘要：分析计数、P0/P1/P2、N/A、待确认、准出。同会话同载体只一次；补丁/单模块轻量可不设门。
- **条件判定 `hitl:plan_needs_confirm`**：版本级首版/换代，或范围/准出/缺陷策略实质变化；满足→真，否则跳过该门。
- **HITL `confirm_iteration_close`**：出示当前迭代、未完成项、拟归档摘要、下一迭代；确认后关账；可「并行不关」。
- **条件判定 `hitl:iteration_close_needed`**：探测到下一期/换主题/版本升级且是否关本期不明确；满足→真，否则跳过该门。
- **HITL `confirm_docs_migration`**：资料收取/分类/改名/归档、或结构迁移前列清单与目标；确认后执行。
- **条件判定 `hitl:docs_migration_needed`**：本步将搬迁/归档/清理 inbound 或工作文档且未确认清单；满足→真，否则跳过该门。
- **GATE `coverage-map` when=analysis_coverage_required**：运行对应 verify；未过不得宣称完成。
- **条件判定 `gate:analysis_coverage_required`**：本轮创建/更新分析或计划；满足→真，否则跳过该闸（步骤不跳过）。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`test-basis-analysis`、`test-analysis-and-plan`、`test-data-and-environment` → 见 §6 闭环。

### 本步规则卡：先分析，再计划

- 模板（本步两份都填）：`rules/templates/10-planning/test-analysis-template.md`（分析，必做）＋ `rules/templates/10-planning/test-plan-template.md`（总排）。
- **分析多源**：写分析时至少读主读 + 1 个互补源（原型/接口/代码/现网/历史缺陷）；不能只看单一文档。
- **分析必做**：来源盘点/章节回执/依据覆盖/AC 设计点账本；每条有意图或 N/A+依据+接受人；每个 AC/设计点有落点；覆盖矩阵（模块×13 面）、方法矩阵、D01–D13 + S6/S7/S11、风险、影响面（直接/邻接/上游/下游/共享数据/事件/回归）、核心链路无未接受空格。
- **环境基线**：先读 `env-baseline.md` 命中节；计划 §2.2 写命中节/差异/核验，不复制整本；缺基线先接入。
- **执行双读预告**：分析是原文索引，不替代；后续执行须打开原文对应段并另读 ≥1 互补源，禁只读分析。
- **优先级**：P0 门禁/阻断必须全过；P1 核心必须执行并出结论；P2 常规必须执行并出结论或 N/A+依据+接受人。P0/P1/P2 都是覆盖义务，不是免测开关。
- **计划只做总排**：范围、分析引用/计数、影响面/核心链路摘要、类型/轨道、轮次/批次、探索、准入准出、缺陷策略、状态/日志；不重复分析大表。
- **命令入口**：用户说「根据 XX 迭代生成测试计划」时，本步内完成分析 + 计划；不要求再单独说「分析需求」。
- **计划门**：主屏展示分析关键结论 + 计划摘要；分析未确认不写计划，计划未确认不执行。
- 执行时按计划展开全部在范围 P0/P1/P2 意图；场景在执行时生成并写执行记录，不预生成全量用例。
- 方法质量按 §6 必开技能闭环；本卡写门槛，技能写做法。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → 读必做，并读现场处置/判定/反合理化（技能有这些节时）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `test-basis-analysis` | **必开** | 进入本步即开（质量不降） | `skills/test-basis-analysis/SKILL.md` | 只读 L12-L122（必做+处置/判定/反合理化）→ 回本包 |
| `test-analysis-and-plan` | **必开** | 进入本步即开（质量不降） | `skills/test-analysis-and-plan/SKILL.md` | 只读 L11-L92（必做+处置/判定/反合理化）→ 回本包 |
| `test-data-and-environment` | **必开** | 进入本步即开（质量不降） | `skills/test-data-and-environment/SKILL.md` | 只读 L13-L77（硬门槛+方法+反合理化）→ 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（本步两份都填）**：`rules/templates/10-planning/test-analysis-template.md`；`rules/templates/10-planning/test-plan-template.md`；各只读本步用到的节，禁止整文件通读；分析模板先于计划模板。
- 验证命令：`verify/Invoke-Gate.ps1`（本步非完成 Claim；按 Mode 出回执即可）。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:testing | step=plan | agent=test-planner | packet=rules/packets/testing/plan.md | global=ok | skills=test-basis-analysis,test-analysis-and-plan,test-data-and-environment|done|na | claim=ALLOWED|DENIED|na | next=…
```
