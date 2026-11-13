# AGENTS.md

> **用途**：测试规范 AI 入口。  
> **新会话必读顺序（硬）**：入口已是本文 → ① 开局卡 → ② `activeContext` → ③ `global-rules.md` → ④ `workflows/<id>.md` → ⑤ 当前步骤卡 → ⑥ §6 skill（整卡）→ ⑦ 步骤卡 §7 点名的模板（通常 1 份）；未路由时用 §2 口令表。  
> **每轮协议**：先判新任务/续跑/只读 → 新任务重路由并复述 → **先打开** `activeContext.packet=` 步骤卡（未打开=未开跑本步）→ 首行锚按 `rules/core/cold-start.md` §3 字段（`global=dev:…` 表偏离；只读 `mode=analyze`）→ 结束给收口（六点或 2～3 行）。  
> **已路由中段**：`global-rules` 按 §7 **重读分级**（新会话/换链/规则变更→全文；同链中段→按节最小集，**禁**每步预防性通读）；每步实读当前步骤卡；心跳（`packet=` + `global=ok`）；禁止同时多 packet；本步流程以当前包为准，不跳转拼齐；勿通读 `workflow.md`/协作手册拼流程（参考层按节、按需）。  
> **降本（硬）**：正式证据=断言终态；中间探查进 `.draft`；查重禁同质刷 API；交单只投影禁现网补证。详见 `global-rules` §9、`collaboration` §5/§6.1、`platform-adapter` 查重。  
> **位置**：`wf-testing/`。与根冲突以根为准；与用户指令冲突见 `rules/core/global-rules.md` §11。  
> **template_version**：`2026.11.13.01`  
> **主链**：方案全细节分析 → 计划（数据/造数清单 + 数据准备批）→ **统一造数** → 执行三步序（方案→分析理解→现场择优）→ 报告；分析必做，计划是总排，造数先于功能批一次完成。  
> **完成口径**：只认 `verify/Invoke-Gate.ps1 -Claim -Mode report|writeback` → `CLAIM: ALLOWED`。

## 0. 开工

> **硬约束全文**：`rules/core/global-rules.md`。本节只补分级与指针。

1. **中文**；写现行结论。  
2. **短读**：`activeContext` 总览 + `## 测试` 进行中（含 workflow/state/packet） + **偏好/洞见/坑 ≤3 行**（开局卡 §1；写法 `context-memory.md`）；身份：档案 §1 或 `env-baseline`（每新会话一次）。  
3. **接入**：`wf-testing onboard: done` 则跳过；计划/执行/缺陷无标记时核验一次。  
4. **行为契约**：理解/澄清/检查/择优/冲突按 `rules/core/global-rules.md`（**遵守**；重读分级见 §7，中段禁全文通读充数）。  
5. **覆盖优先级**：只认 `rules/core/global-rules.md` §11。  
6. **读取**：分级读链（global-rules §7 主从）；**本步第一步工具读**须含当前 `packet=` 路径；YAML 非规则正文；技能按步骤包 §6 **整卡读取**（同时 ≤1）。  
7. **契约**：`rules/core/global-rules.md` §1/§4（开工档位【需求与意图理解】+【动作前分析】）。  
8. **心跳**：`rules/core/global-rules.md` §8（切步/过门一行锚；`global=ok`=本步已按 §7 复核且已实读当前步骤卡）。

### 0.0 事实与文档

事实可核实；待确认禁升格；正式资产只写现行。术语：**意图**=可独立判定的测试承诺（`INT-*`）；**场景**=意图的一次具体验证；**执行记录**=场景+步骤+结果+证据+缺陷；**锚点**=P0/高价值回归资产。

### 0.1 门 · 分析 · 计划

步骤门只认 YAML `hitl*` + `gates.md`；开局门 `confirm_task_intent` 见 `gates.md`；开工档位/读链只认 `global-rules.md`；澄清**方法**按需读 `clarification.md`（参考层）。  
**路径**：T0～T3 为内部风险标签，按 `gates.md` §4 的事实判定；补丁/单模块、无新增功能面且不承担版本准出可轻量（命中 T3 面按专项），其余默认完整；路径拿不准按完整。勿与开发 L* / 产品 P* 混用。  
**路由硬门**：无 `{workroot}/{ver}/test-analysis.md` 不得写计划、不得执行；`test-plan.md` 为唯一总排；完成只认 `-Claim -Mode report|writeback` → `CLAIM: ALLOWED`（P0 未过或意图未终态不得整体通过）。缺 `env-baseline` 先接入。  
**读法（硬）**：路由后只读**当前步骤卡 + §6 必开技能（整卡）+ 步骤卡 §7 点名的模板（通常 1 份；分析/计划成对时按 §7 顺序）**；分析/执行/报告硬门槛以本步步骤卡为准，不跳转拼手册。

## 1. 接入

实例在项目根：`env-baseline.md`、`activeContext.md`；工作根必须有 `{workroot}/`；原件根 `inbound/` 固定在项目根。存量全索引，按需复制或 A0～A2 吸收。占位符未换或无基线=未接入。交接 `{workroot}/handoff/outbound|inbound/{category}/` + 台账。接入 `onboard.yaml` + `onboard-agent.yaml`；标准树与索引按 `rules/doc-governance.md` §2.4 建。

## 2. 口令 → Workflow（命中即停）

> **描述**：表内是常见口令示例（非穷尽），同义表述按五元组路由，不要求逐字匹配；命中优先执行。未命中或任意描述句 → 必读 `rules/core/routing.md`：抽五元组 → 意图类 A～I → 计划状态修正；首条必写 `reason=`。不抠固定措辞；路由后按步加载技能，不另造 workflow。

| 优先 | 命中 | workflow | 切入 step |
| ---: | --- | --- | --- |
| 0 | 工作总结/输出工作总结/今日工作总结/今日总结 | — | 直接按 `rules/templates/90-handoff/closeout-skeleton.md` §2 |
| 1 | **根据迭代/版本/需求/方案生成测试计划**；根据迭代生成测试计划；生成测试计划；测试计划；更新计划；本期变更 | `testing` | plan（本步内完成分析 + 计划） |
| 2 | 按测试计划执行；按计划执行；继续测试计划；按计划重跑 | `testing` | execute |
| 3 | 测试报告；准出评估 | `testing` | report |
| 4 | 执行专项；执行接口测试；执行探索式；执行随机业务流程；执行发布前；执行性能/安全/兼容 | `testing` | execute（按 track 契约） |
| 5 | 分析需求；梳理测试依据；理解 PRD（用户明确只做分析） | `testing` | plan（分析部分；仍产出分析文件） |
| 6 | 缺陷协作/提交到平台/缺陷回归 | `defect` | classify（按链至收尾/提交门） |
| 7 | 当前状态/下一步 | —（只读） | 直接读 `activeContext` + `test-plan.md` §0；不启动 workflow |
| 8 | 接入/环境基线/重新接入/装配能力/生成README/更新README/整理README | `onboard` | baseline / migrate / capabilities |
| 9 | 技能/能力体检或优化 | `skill-audit` | scope→…→closeout |
| 10 | 维护/查询 | 本文 + `rules/core/maintenance.md` | — |
| 11 | 资料收取/整理 | `onboard` | materials |
| 12 | 文档清理/归档巡检 | `onboard` | lifecycle |
| 13 | 写交接单/交接包/接收/变更/重规划 | `handoff` | 默认 compose；升包才 send |
| 14 | 提交/推送 | 当前 workflow 末步（`closeout`）或 `handoff` | 对应角色 |
| 15 | 交接状态 | —（只读） | 直接读 `{workroot}/handoff/handoff-ledger.md` + `activeContext`；不启动 workflow |
| 16 | 导出项目文档/生成资料库/发资料 | `materials` | select→sync→index→closeout |

**入口即止**：单步入口做到产出即止（不含提交/推送/部署/回写），仍按 `closeout-skeleton.md` 输出；标「按链」到链末停点；「按计划执行」走 execute→report；`report` 门后追加提交/交平台确认；`onboard` / `materials` / `skill-audit` 的 `chain: full` 例外（跑到链末停点）。  
**路由消歧**：裸「回归」先确认 `defect` 单回归还是 `testing.execute` 重跑；确认后走「按计划回归 / 回归重跑 / 重跑」或 `defect`，勿把裸「回归」直接当 execute。**发资料 vs 交接**：「发资料/导出」指整库或资料包（`materials`）；把某份文档交给具体角色（确认/知会/提测）走 `handoff.compose`。  
**主链**：`plan → execute → report`（`plan` 默认 `next: execute`）。  
**版本级单点**：`test-plan.md` / `test-report.md`；补丁可用 `plan_tier=lite`（不承担版本准出）。  
**路径**：本期产物在 `{workroot}/{ver}/`；执行记录 `functional|api/{NN}-{短名}-执行记录.md`（平铺，细则 §3）。  
**无口令**：口语未命中 → `rules/core/routing.md`。  
首条按 `rules/core/cold-start.md` §3 回执字段，并补 `level=<按事实推导>`、`reason=`、`reads=`、`next_action=`；`mode=execute/analyze/stop` 按判断模式给；无标记预检加 `preflight=onboard`；有主读加 `input=`。只读可 `route=readonly:analysis | step=explain | mode=analyze | …`；字段名不得改别名（如 `role=`）。

## 3. 实例路径

根留 `env-baseline.md`、`activeContext.md` 与原件根 `inbound/`；常青在 `{workroot}/`；**本期**分析/计划/执行/报告在 `{workroot}/{ver}/`；权威文档库为 `docs/materials/`。禁止在项目根堆测试产物。
- 分析 / 计划 / 报告：`{ver}/test-analysis.md` · `test-plan.md` · `test-report.md`。
- 执行：`{ver}/functional|api/{NN}-{短名}-执行记录.md`（平铺）；探索/随机：`{ver}/exploratory|random-flows/{主题}-{戳}-…记录.md`；发布前：`{ver}/pre-release/{专项}-…`。
- 缺陷写回回执：`{ver}/写回回执.md`（本轮覆盖；细则 `collaboration`）。
- 锚点：`{workroot}/smoke-checklist.md`；证据：`{ver}/evidence/`；脚本：`{workroot}/scripts/`。

## 4. git

有 `.git` 时：完整任务收尾检查仓库状态与 `.gitignore`；结论只写入【任务收尾】第 2 点（字段：`待提交摘要` / `git` / `.gitignore`）；禁止收尾外另造 git 块；仓库完整清单仅【拟提交·仓库】一次（门=`confirm_commit`；≠ 平台门 `confirm_platform`）。无 `.git` 时第 2 点写「无仓库」。
提交/推送前：出示【拟提交·仓库】→ `confirm_commit` 确认后执行；禁擅自切主干、force push、开/合并 PR（除非点名）。重要改动确认后尽早提交。多 remote / 异形 tip 时禁对本工作树 `checkout`/`reset` 到非日常 tip；同步/历史改写只在临时目录或独立 worktree。

## 5. 收尾

触发：工作流末步、计划全部阶段结束、点名「收尾/总结」。**骨架与硬项以** `closeout-skeleton.md` §1 通用占位为准（执行用【执行收尾】；专规只填第1点；缺项=未收尾）。按项目事实填 `{…}`，禁照抄他例。收尾/复盘按 `context-memory.md` §4 写「工作记忆」（无则「无」）。浏览器退程见多Agent §2.2。`confirm_platform` 与【拟提交·仓库】在骨架后按 `hitl` 分门确认。

## 6. 维护

改不变量/路由/读取协议 → 本文；改无口令路由 → `rules/core/routing.md`；改心跳 → `rules/core/global-rules.md` §8；改步骤/技能挂载 → `workflows/*.yaml`（step 的 `skills` / `skills_conditional`；改后跑 `build_step_packets.py`）；改角色 → `agents/`；改红线/门 → `rules/`；改澄清 → `rules/core/clarification.md`；改协作/交接 → `rules/collaboration/handoff.md` + `workflows/handoff.yaml`；改子代理派工/生命周期 → `rules/collaboration/subagents.md`；改计划 §3.1 填表 → 计划模板该节；改轨边界 → `rules/tracks/`；改多轨准出 → `rules/special/multi-track-quality.md`；改 templates / skills / capabilities → 对应目录；改计划编排轮次/准出 → 计划模板 + `rules/workflow.md` §3.6（详版执行按节读 `multi-agent-output.md` §4）；改步骤读包 → `rules/packets/`（改后跑 `build_step_packets.py`）+ `Validate-StepPackets.ps1`；改门 → `verify/tools/test_gate.py` + `verify/tools/selftest_gate.py`。自检见 `rules/core/maintenance.md` §2。

## 7. 多包（自动探测）

`wf/`（含 ≥2 个 `wf-*`）=多包；项目根单个 `wf-*` =单包；同 id 双份/半迁停问。
- **口令表节号**：本包 §2；产品/开发 §3。
- **单包独立为默认**；多包联动可选、非必须；缺他包不阻塞本包。
- **联动=交付物字段 + 同仓直读**；无提测单时本包自填影响面。
- **实例面（硬）**：实例根 `AGENTS`/README/档案/`activeContext`/`.gitignore` 只写已装包；规范包默认不跟踪：`.gitignore` 只写一行 `/<已装包>/`（多包 `/wf/`）；不预列未装包、不加注释。
- 共用原件根 `inbound/`、根 `activeContext.md`；各包只改本分节。一次会话只执行一个包 workflow；跨包默认交自洽交付物或同仓直读；仅升包时用 `handoff/outbound/{category}/{HO-ID}/`。
- **歧义定包**：先查 `wf/AGENTS.md` **意图→包**；无该文件时用兜底：产品缺陷评估/平台产品单→产品；修代码/开发缺陷流→开发；交平台/测试回归→测试；发布=业务上线/UAT→产品；发布=部署/回滚→开发；发布=准出报告→测试；下一步/继续→`activeContext` 当前包分节（无焦点一问）；提交/推送/交接→当前会话已绑定包（未开跑一问）。无法唯一则一问。多包应 onboard 生成 `wf/AGENTS.md`。

## 8. 技能与能力（按步加载）

- **角色边界**：见 `rules/collaboration/roles.md`；出现职责冲突先查此表。
- **技能（必用）**：`skills/<name>/SKILL.md`，随包复制、命中步必用；方法见 `skills/README.md`。
- **技能质量**：新增/大改按 `skills/README.md` 末节；description 含中文触发词；≤500 行；须有反模式/反合理化；改后 `check_skills.py --strict`。
- **能力（可选 · 实例 SSOT）**：真源 `{workroot}/capabilities/00-能力清单.md`（常青）；包内 `capabilities/00-contract.md` 只定义槽位。清单 available 即用，否则按契约降级；未接受降级每次触达出【能力缺失】块。能力不替代技能。「装配能力」写实例；「接受降级」写 `degraded`+`accepted=`；「体检能力」含 discover，禁外装绕过分析/oracle。
- **适度建议**：仅当有证据表明技能/能力达不到要求时，收尾附至多 1 条；禁推销、禁未确认改 skills/capabilities。能力缺失全块不受限制。
