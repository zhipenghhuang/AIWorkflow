# 步骤卡 · testing/execute

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守；重读按 §7 分级）；方法在 §6 指定节（打开→执行→回包）。**未打开本文件=未开跑本步**。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`testing` / `execute`（按计划执行）
- **packet**：`rules/packets/testing/execute.md`
- **角色**：`test-orchestrator`（计划驱动执行编排（功能/接口/探索/发布前/回归））。按 {workroot}/{ver}/test-plan.md §3 轮次/§4 准出执行全部在范围意图与轨道；生成场景、记录结果、管理证据/缺陷/回归；本步只做该角色职责；越界交回或升级。
- **前置**：分析表与测试计划已确认；按计划执行全部在范围意图
- **上游**：`plan`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`report`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。

## 2. 本步目标

- **目标**：按计划执行
- **产出**：执行记录（场景+步骤+结果+证据）+ 缺陷 + 计划状态

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：按 `rules/core/global-rules.md` §7 **分级重读并遵守**（中段=最小集，禁每步通读全文）；须先打开本步骤卡；心跳 `global=ok`=已按 §7 复核且步骤卡已实读；未复核不得写 `global=ok`。偏离写 `global=dev:<原因>`。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_execution_scope`**：开跑前一行：计划范围/环境/构建/轮次 → 确认；计划已确认 → 跳过并附【已预授权执行：按计划】。
- **条件判定 `hitl:scope_needs_confirm`**：非计划驱动、计划 §0 非已确认/执行中/待关闭，或范围/环境实质变化；满足→真，否则跳过该门。
- **GATE `execute-batch` when=module_batch_complete**：按本包门表该门的检查方法核验并留证据；未过不得宣称完成。
- **条件判定 `gate:module_batch_complete`**：本批计划内意图已执行完、执行记录终态齐（无未执行）、失败/阻塞有证据；P0 失败须有缺陷/解释（非「零红灯才推进」）；满足→真，否则跳过该闸（步骤不跳过）。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`testcase-design`、`test-execution-and-exploration`、`test-data-and-environment` → 见 §6 闭环。

- **条件技能**：`test-interface`（计划含接口轨/执行接口批）、`test-performance-security-compatibility`（计划含发布前/性能/安全/兼容）、`ai-feature-testing`（被测含 LLM/RAG/Agent） → 命中则同样走 §6 闭环。

### 本步动作清单

- 本步任务：按计划执行全部在范围 P0/P1/P2 意图与轨道（功能/接口/探索/发布前/回归）。开跑前读 `env-baseline.md` 命中节；取档以计划 §3.1 为真值；开跑声明 `exec_mode=`+`pg=`。**硬门槛**：
  - ① 执行记录原文对账齐（可验收单元 N；未关 0，缺口仅用户确认 Q19）；§0 有分析索引，每场景有实际/差异。
  - ② 功能六类有面对须 SC（无面对才 N/A+事实句）；**UI 面**：原文/分析命中页面·路由·控件·布局·导出 → §1.1「UI/视觉」须 ≥1 条 E1（浏览器实点+截图/Network），禁以「API 主断言/脚本/契约摘录」整类 N/A（无页面面才事实句 N/A，或当轮用户确认）。
  - ③ 全部 `处置=测` 意图终态；P0 须证伪；深度按 Q17 + testcase-design §3/§3.1（字段级 Oracle、专用负向、交叉对账）；禁浅打勾、禁删负向（Q9）；主题句 Oracle 不得单独支撑 P0 通过。
  - ④ INT 须在分析 §2.1 台账；意图结论回指场景表。
  - ⑤ 计划含接口轨须非空 `api/` 契约记录+场景表+§2.1 维表+depth（Q18）；成功契约字段级；`validate_api_testcase` 无 ERROR；禁探活通过率关账；发布前须先建方案+硬映射；探索已跑须非空记录。
  - ⑥ 缺数据/账号/入口先自助造数/换样/换角（有界），未穷尽禁阻塞；阻塞摘要须卡点+已尝试+恢复条件；专用负向无配方不得标通过。
  - ⑦ 批末跑 execute 闸并更新计划状态；失败/待实现留证进缺陷，真阻塞进盯办；对人进度落点（开跑可见/批末关账/外力·拟提交）见 global-rules §8。

### 本步规则卡：计划驱动执行编排（本步门槛）

- **取档真值**：先读计划 §3.1；缺行按决策树补；隔离不成立 → 串行并记 `plan_batch_conflict`。取档详法见 §6 执行技能。
- **开跑声明（不可省）**：`exec_mode=脚本|直跑|模块子代理|拆分` + `pg=PG-xx|na`；**须与计划 §3.1 一致**（不一致 → 改计划或记 `deviation=`+reason；禁表写子代理、实跑直跑长期并存）；声明须对话可见（`global-rules` §8）。
- **子代理硬门槛**：模块/拆分档走 Task；一模块一新开；Reviewer fresh；返回 ≤30 行；不过门、不 git、不交平台、不改他模块。
- **质量锁**：同一意图禁并行；共享写域串行；不采信口头完成；禁为通过率删负向/边界/证伪（`multi-track-quality` Q9）。
- **Oracle 锁（硬）**：P0 通过须 `testcase-design` §3/§3.1——字段级 Oracle、同义多表/多载体对账、§3 命中专用负向独立落点或 N/A+依据；主题句不得单独支撑通过；失败原因须用户可读。
- **阻塞锁（硬）**：缺数据/账号/入口临时不通 → 先自助造数/换样/换角/换入口（有界）；**未穷尽禁止落阻塞**；摘要须卡点+已尝试+恢复条件。终态表见 `classification.md` §0.4。
- **基线锁（硬）**：开跑读命中节；造数/换样前查基线造数·样本节；本批打通的**新可复用** API/配方/样本/冲突 → **同轮**按基线「同步规则」回写；批末自检有则补齐、无则禁改。细则 SSOT：基线同步节 + §6 `test-data-and-environment`。
- **先造数后执行（硬）**：首跑先过计划数据准备批，核对造数台账（对象/ID/成功信号/幂等/清理）；后续批按台账消费，缺项或数据漂移先补造再断言；**专用负向无配方不得标通过**；台账未齐不得宣告功能批完成。
- **证据终态制（硬）**：`evidence/` 只留断言终态（通常每 SC 1～2 叶）；中间探查/重试进 `.draft/`（`global-rules` §9）。UI 失败**当场**钉断言截图；禁留到交平台再补。
- **失败详情成稿（硬）**：失败/待实现行当场按 `test-case-template` §2 / `api-test-case-template` §3 槽位写满（问题标题…技术附记 + `surface=ui|api|ui+api`）；有 UI 面的**失败**须 UI 路径+截图（待实现可非截图，须缺失证据）；纯 API 才可请求链；本批门核失败详情，缺块/缺 surface/UI 失败无截图 → FAIL，补采后再关批。
- **三步序 + 偏差择优（硬）**：顺序与禁则见动作清单；**方法**见 §6 `test-execution-and-exploration`；分型专文 `rules/defects/classification.md` §0.5。
- **同域锁（硬）**：结果/写操作页落通过前做同域自洽探针（方法 §6 执行技能 5.2，含列表/徽标/KPI↔详情）；同屏冲突/读写分裂/旁路假可过 → 禁选型通过（`classification.md` §0.5）。S7/S11 收口门槛见 `multi-track-quality` §2.4.1。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。
> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `testcase-design` | **必开** | 进入本步即开（质量不降） | `skills/testcase-design/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `test-execution-and-exploration` | **必开** | 进入本步即开（质量不降） | `skills/test-execution-and-exploration/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `test-data-and-environment` | **必开** | 进入本步即开（质量不降） | `skills/test-data-and-environment/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `test-interface` | 条件开 | 计划含接口轨/执行接口批 | `skills/test-interface/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `test-performance-security-compatibility` | 条件开 | 计划含发布前/性能/安全/兼容 | `skills/test-performance-security-compatibility/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `ai-feature-testing` | 条件开 | 被测含 LLM/RAG/Agent | `skills/ai-feature-testing/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（按轨）**：功能/探索 → `rules/templates/20-test-cases/test-case-template.md`；接口 → `rules/templates/20-test-cases/api-test-case-template.md`；发布前 → 本轨专项方案/报告。只读本轨用到的节，禁整文件通读；禁混用模板。
- 验证命令：`verify/Invoke-Gate.ps1`（本步非完成 Claim；按 Mode 出回执即可）。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:testing | step=execute | agent=test-orchestrator | packet=rules/packets/testing/execute.md | global=ok | skills=testcase-design,test-execution-and-exploration,test-data-and-environment|done|na | claim=ALLOWED|DENIED|na | next=…
```
