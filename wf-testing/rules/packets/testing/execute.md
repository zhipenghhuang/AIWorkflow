# 步骤卡 · testing/execute

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（本会话已读则不重读全文）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`testing` / `execute`（按计划执行）
- **packet**：`rules/packets/testing/execute.md`
- **角色**：`test-orchestrator`（计划驱动执行编排（功能/接口/探索/发布前/回归））。按 {workroot}/{ver}/test-plan.md §3 轮次/§4 准出执行全部在范围意图与轨道；生成场景、记录结果、管理证据/缺陷/回归；本步只做该角色职责；越界交回或升级。
- **前置**：分析表与测试计划已确认；按计划执行全部在范围意图
- **上游**：`plan`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`report`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：按计划执行
- **产出**：执行记录（场景+步骤+结果+证据）+ 缺陷 + 计划状态

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：本会话已读 `rules/core/global-rules.md` 则不重读全文；未读过不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_execution_scope`**：开跑前一行：计划范围/环境/构建/轮次 → 确认；计划已确认 → 跳过并附【已预授权执行：按计划】。
- **条件判定 `hitl:scope_needs_confirm`**：非计划驱动、计划 §0 非已确认/执行中/待关闭，或范围/环境实质变化；满足→真，否则跳过该门。
- **GATE `execute-batch` when=module_batch_complete**：运行对应 verify；未过不得宣称完成。
- **条件判定 `gate:module_batch_complete`**：本批计划内意图已执行完、执行记录终态齐（无未执行）、失败/阻塞有证据、P0 不外溢；满足→真，否则跳过该闸（步骤不跳过）。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`testcase-design`、`test-execution-and-exploration`、`test-data-and-environment` → 见 §6 闭环。

- **条件技能**：`test-interface`（计划含接口轨/执行接口批）、`test-performance-security-compatibility`（计划含发布前/性能/安全/兼容）、`ai-feature-testing`（被测含 LLM/RAG/Agent） → 命中则同样走 §6 闭环。

### 本步动作清单

- 按计划执行全部在范围 P0/P1/P2 意图：功能/接口/探索/发布前/回归按计划轮次与批次推进。
- 开跑前读 `env-baseline.md` 命中节。
- 取档以计划 §3.1 为真值，缺行按决策树补并记偏差，开跑声明 `exec_mode=`+`pg=`。
- 开跑先按原文目录/可验收单元对账分析 §1.1/§1.2/§2.1.1，漏来源/漏章、漏 AC/字段规则/入口先补分析再执行。
- 对账写功能/接口执行记录 §0「原文对账」行（探索/发布前在本轨记录信息写同义对账；可验收单元 N/已覆盖 n/本轮补录 n/未关 0+接受人）。
- 多源对照硬门槛：逐场景打开原文对应段并另读≥1互补源，分析只作索引，禁只读分析（做法按 §6 执行技能闭环）。
- 边执行边写执行记录（场景+原文/依据+步骤+数据+Oracle+结果+证据+缺陷+意图结论）。
- 步骤写清位置/数据/预期，供人复核。
- 不把步骤当预写脚本逐条点。
- 全部 `处置=测` 意图到终态，P1/P2 不得用低优先级跳过。
- 失败/待实现留证并进缺陷。
- 阻塞留证，需外力进盯办（勿把阻塞当缺陷凑交）。
- P0 意图至少一条证伪场景（负向/状态/权限/幂等/恢复按适用），只有正向通过不得记 P0 完整。
- T1+ 功能收口前 S6/S7/S11 有落点。
- 批末按计划 §3.1 批次/意图范围核对本轮记录，缺意图补测或写缺口+接受人，未关不得合并，并更新计划 §0/§6 与执行记录结论。

### 本步规则卡：计划驱动执行编排

- **取档真值**：先读计划 §3.1；缺行按决策树补（脚本→点名→接口单 Agent→无 Task 直跑→继续单模块直跑→≥2 模块子代理→大单拆分）；隔离不成立 → 串行并记 `plan_batch_conflict`。详档仅在 §6 执行技能闭环按需打开。
- **开跑声明（不可省）**：`exec_mode=脚本|直跑|模块子代理|拆分` + `pg=PG-xx|na`；对照决策树一句。
- **子代理**：模块/拆分档走 Task；一模块一新开；拆分档 Reviewer 须 fresh（禁 resume Worker）；返回 ≤30 行；不过门、不 git、不交平台、不改他模块。
- **质量锁**：同一意图禁并行；共享写域串行；质量优先于并行；不采信口头完成。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → 读必做，并读现场处置/判定/反合理化（技能有这些节时）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `testcase-design` | **必开** | 进入本步即开（质量不降） | `skills/testcase-design/SKILL.md` | 只读 L13-L125（硬门槛+方法+反合理化）→ 回本包 |
| `test-execution-and-exploration` | **必开** | 进入本步即开（质量不降） | `skills/test-execution-and-exploration/SKILL.md` | 只读 L14-L118（必做+处置/判定/反合理化）→ 回本包 |
| `test-data-and-environment` | **必开** | 进入本步即开（质量不降） | `skills/test-data-and-environment/SKILL.md` | 只读 L13-L77（硬门槛+方法+反合理化）→ 回本包 |
| `test-interface` | 条件开 | 计划含接口轨/执行接口批 | `skills/test-interface/SKILL.md` | 只读 L11-L62（必做+处置/判定/反合理化）→ 回本包 |
| `test-performance-security-compatibility` | 条件开 | 计划含发布前/性能/安全/兼容 | `skills/test-performance-security-compatibility/SKILL.md` | 只读 L11-L69（硬门槛+方法+反合理化）→ 回本包 |
| `ai-feature-testing` | 条件开 | 被测含 LLM/RAG/Agent | `skills/ai-feature-testing/SKILL.md` | 只读 L13-L93（硬门槛+方法+反合理化）→ 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/20-test-cases/test-case-template.md`；只读本步用到的节，禁止整文件通读。
- 验证命令：`verify/Invoke-Gate.ps1`（本步非完成 Claim；按 Mode 出回执即可）。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:testing | step=execute | agent=test-orchestrator | packet=rules/packets/testing/execute.md | global=ok | skills=testcase-design,test-execution-and-exploration,test-data-and-environment,test-interface,test-performance-security-compatibility,ai-feature-testing|done|na | claim=ALLOWED|DENIED|na | next=…
```
