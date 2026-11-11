# 步骤卡 · testing/plan

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守；重读按 §7 分级）；方法在 §6 指定节（打开→执行→回包）。**未打开本文件=未开跑本步**。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`testing` / `plan`（分析并生成测试计划）
- **packet**：`rules/packets/testing/plan.md`
- **角色**：`test-planner`（测试分析 / 测试计划（总排））。本步只做该角色职责；越界交回或升级。
- **上游**：无（链首）
- **后续**：`execute`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：分析并生成测试计划
- **产出**：{workroot}/{ver}/test-analysis.md（必做；来源/AC/设计点/意图/风险/覆盖）+ {workroot}/{ver}/test-plan.md（总排）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：按 `rules/core/global-rules.md` §7 **分级重读并遵守**（中段=最小集，禁每步通读全文）；须先打开本步骤卡；心跳 `global=ok`=已按 §7 复核且步骤卡已实读；未复核不得写 `global=ok`。偏离写 `global=dev:<原因>`。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `select_mainread`**：主读路径未确认 → STOP 一问；已点名/唯一正式版已在依据清单写明 → 可续，不重问。
- **条件判定 `hitl:mainread_unspecified`**：plan/探索 execute 主读未确认；满足→真，否则跳过该门。
- **HITL `confirm_understanding`**：**主屏**：分析 §0 摘要、来源盘点计数（含 UI/文案类）、AC/设计点/UI/文案覆盖、关键歧义/冲突、P0 意图与 Oracle；确认后才写计划。
- **条件判定 `hitl:understanding_needs_confirm`**：输入含 PRD/方案/原型/接口，存在 2 个以上实质歧义/冲突，T2/T3，或用户要求计划/准出且未确认分析；满足→真，否则跳过该门。
- **HITL `confirm_plan`**：版本级首版/换代，或范围/准出/缺陷策略实质变更 → STOP 一行摘要：分析计数、P0/P1/P2、N/A、待确认、准出、**批次形态**（如「N 模块·模块子代理·串行/PG-xx」）。同会话同载体只一次；补丁/单模块轻量可不设门。
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

### 本步规则卡：先分析，再计划（本步门槛）

- **模板**：分析 + 总排两份都填（见 §7）；轻量仅补丁/单模块且 `版本准出=否`。
- **覆盖先后（硬）**：先按方案原文逐项完整入账（每个应测细节/设计点 → §2.1 INT+Oracle + 矩阵无空格），再写计划总排；**禁止**「先粗计划、细节执行时再补分析」。执行阶段才允许按现场自主打通/择优，不得用执行自主回补分析空账。
- **硬门槛**：① 方案为主参考；至少主读+1 互补源 ② 应测细节/设计点入账；§2.1 INT+Oracle；覆盖面/方法矩阵无未接受空格；计数被行数支撑（门查）③ 分析未确认不写计划；计划未确认不执行；覆盖闸未过不得称可执行 ④ 计划只总排；§0/§3.1 与分析联动 ⑤ §3.1 按模板填 ⑥ P0/P1/P2 均为覆盖义务 ⑦ 准出/轨道纳入见 `multi-track-quality` §0+文首（默认硬纳入；整轨否仅白名单+接受人）。
- **环境**：先读 `env-baseline.md` 命中节；缺基线先接入。
- **预告**：执行三步序见 execute 卡；本步不预生成全量用例≠可浅测。做法见 §6。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → 读必做，并读现场处置/判定/反合理化（技能有这些节时）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `test-basis-analysis` | **必开** | 进入本步即开（质量不降） | `skills/test-basis-analysis/SKILL.md` | 只读 §0–§8（必做+处置/判定/反合理化），按标题定位 → 回本包 |
| `test-analysis-and-plan` | **必开** | 进入本步即开（质量不降） | `skills/test-analysis-and-plan/SKILL.md` | 只读 §0–§7（必做+处置/判定/反合理化），按标题定位 → 回本包 |
| `test-data-and-environment` | **必开** | 进入本步即开（质量不降） | `skills/test-data-and-environment/SKILL.md` | 只读 §1–§7（硬门槛+方法+反合理化），按标题定位 → 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（本步两份都填）**：`rules/templates/10-planning/test-analysis-template.md`；`rules/templates/10-planning/test-plan-template.md`；**按表定位、随填随读**：先读分析模板首行「必填节」索引与 §0–§6；**分析确认后**再读计划模板（避免先看计划污染分析）；表下 `>` 判定口径填该表时再读；禁整文件通读/预读。
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
