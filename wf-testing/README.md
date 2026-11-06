# AI 测试资产体系 — 使用说明

> 供人阅读；**AI 新会话先读** `rules/core/cold-start.md`，口令见 `AGENTS.md`。  
> **template_version**：以 `AGENTS.md` 为准（单点）。

## 1. 是什么

**AI Workflow 包（测试轨）**：主链见 `workflows/testing.yaml`——需求/测试依据分析（需求模型/oracle/追溯）→ **测试计划（唯一编排载体）** → 生成 → **用例评审（独立量规/机器门）** → 按计划执行 → 报告（口令可切入任一步）；内置专业技能（`skills/`：随包生效、按步自动加载，含 `testcase-review`）+ 可选能力层（`capabilities/` 注册表：本机可用即自动使用、不可用降级）。版本级单点：`{workroot}/test-plan.md`（主计划；V1～V4 卷文件从属）、`{workroot}/test-report.md`（计划对照/准出评估/遗留风险）。  
**依据建模**：PRD/迭代方案/原型/接口/代码 diff 先按 `skills/test-basis-analysis/SKILL.md` 建需求模型，落跨轨共用 **`{workroot}/test-analysis.md`（§0 Brief+本期差量表置顶）**/冲突/九类歧义/oracle/TP 追溯；**§2 覆盖单元即验证点**（类型/方法/归属/oracle），§2.1 记点级结论。同轮生成**用户版业务变化说明**（`{workroot}/说明-{主题}-用户版-{yyyyMMdd}.md`；T1+ 用户可见变化必出），供业务用户快速理解，也供 AI 读取完整业务上下文。有产品/开发 Delta 则引用对账。功能/专项双读全表；接口/发布前/探索式至少读 §0。确认门主屏出示 §0 后才写计划/用例；预期无来源不写断言。版本级固定四卷（V1 主链/V2 功能/V3 方法/V4 收口；模板 `test-plan-volume-template.md`），主计划仍是唯一编排入口。  
正式并列轨：功能全量/专项、探索式、接口、发布前、缺陷；**计划驱动模式**按测试计划把各轨串成一条执行链（功能→接口→探索式→非功能→回归→缺陷闭环→报告）。  
**接口域**：独立模板 `rules/templates/20-test-cases/api-test-case-template.md`（契约+对照+用例+脚本清单）+ `validate_api_testcase.py`；禁套功能用例模板。探索式（细节/体验深挖·P4）一场一句章程；T1+ 准出强制（Q14）；随机为旅程办结+去重窗+发现分流（均不替代功能/接口覆盖）。  
口令映射 workflow；条件 `hitl`/`hitl_when`、覆盖三闸、冒烟前置与阻断面、证据红线默认按规则（用户二次明确选择覆盖除外，见 `AGENTS.md` §0 第 5 条）；子代理取档/生命周期按 `rules/collaboration/subagents.md`（决策树详 `multi-agent-output.md` §1.5）；声明 `exec_mode=`（脚本→续跑单模块直跑→同轮≥2 模块子代理→单模块大/高风险拆分；并行补 `pg=`）；分片/核验新开、禁 resume Writer；只读/draft/隔离套可并行≤3，同 MCP 实例需独立会话/路由或独占实例；超时降级直做。  
首次无 `wf-testing onboard: done`（兼容旧 `landing=ok`）时自动按接入清单核验并打标一次；之后直跑。  
**独立实施**：本包可单独落地，不要求开发/产品包同时安装或默认联动；跨包输入是可选的——有则按用户指定路径读入，无则按现有主读/基线执行，最多一句提示，不阻塞、不反复追问。多包同项目时自动探测并共用原件根 `inbound/` 与 `activeContext.md`；不需要额外协作目录或合同文件，本包仍独立执行。  
**成本策略**：**域常青分层库**（功能/接口）+ **变更装填**（suite=`core|module|full`）+ **多轨质量标准**（`rules/special/multi-track-quality.md`：Q11 库≠列车；**Q12 方案细节完整映射**；**Q13 探索常青≠Domain**）。漏测谱系 `rules/special/defect-findings-spectrum.md`；装填速查 `release-train-load.md`。禁日常通读全库。功能 P0 / 接口适用维脚本化；发布前工具测量。**完整覆盖**=验证点/细节映射无空 + P0/GATE/负向/计算类点有结论；**完整执行**=按 suite/depth 装填。探索/随机以可复现发现与缺口衡量，章程按 §0×本项目缺陷簇×谱系**每轮重选**（戳夹分轮，非域库复跑）。禁无分析全仓重生；禁「继续」隐式 generate；禁以「本期不测」整版空库；禁为刷绿砍负向。  
**新版本入口**：计划 §3.7 逐模块/流程标「P0 冒烟/P0 待脚本/迭代功能/接口确定性/一次性/淘汰」；P0 冒烟脚本登记 `{workroot}/smoke-checklist.md`，再按矩阵执行。  
**额外发现**：AI 执行中同时记录用例之外的 UI/布局/显示/文案/冗余标签/console/network/UX 异常，进报告 §5.4；不静默忽略。  
**体验纪律**：验收 UI 减法（冗余文案/标签、删后仍可理解）与 UX/DX/AX 三维；测试资产同样不得净退化；详见 `AGENTS.md` §0.2-11、`rules/templates/20-test-cases/a11y-ux-checklist.md` §2.1。  
**执行引擎**：UI 稳定主链路/E2E 与 API/契约默认 Playwright 脚本；AI 用于设计、探查、失败复核、探索式与报告；性能/安全/兼容/迁移用专项工具，AI 只解读与判定。  
方法参考：ISO/IEC/IEEE 29119-3 测试计划要素、ISTQB 风险驱动/测试金字塔、SBTM 探索式测试；需求分析与澄清参考 fishzjp/qa-skills `requirement-analysis`/`clarify-pattern`、GitHub Spec Kit `clarify`/`analyze`、addyosmani/agent-skills `interview-me`；可选 `qa-skills`/`exploratory-skill` 见 `capabilities/00-contract.md`（未安装按内置技能执行）。  

### 1.1 验证点模型（设计完整性层）

- **验证点**=可独立判定“过/不过”的最小承诺；一个验证点可以有多个用例，但**只出一个结论**；一条用例可覆盖多个验证点，每个点分别登记。
- **类型**：正向/负向/不变量/状态/计算/权限/集成/非功能/视觉；负向含“不新增/不改变/不自动/禁止”，必须写可观测反向断言；计算类必须有最小分母集、公式、精度与期望值。
- **方法**：等价/边界/判定/状态/场景/算例/错误推测；P0/GATE/负向/计算类必填。
- **覆盖面矩阵**：分析表 §2.2 按模块×面逐格 `有/N/A+依据`；空格=缺口，不得用“模块简单”跳过。
- **方法×规则矩阵**：分析表 §2.3 按 P0/高风险规则逐方法确认；只测主路径不算完整。
- **归属**：阶段/轨/卷；同一验证点只归一处出结论，他处经过只作前置/造数，不重复计通过。
- **点结论**：登记在 `{workroot}/test-analysis.md` §2/§2.1；用例结论在台账；报告 §4 分列卷结论（V1～V4）、“验证点结论率”和“用例通过率”，三者不得互相替代。
- **版本级固定四卷**：V1 主链 / V2 功能 / V3 方法 / V4 收口；不适用写 `N/A+依据`，不删卷、不改号。主计划仍是唯一编排入口；每卷用 `test-plan-volume-template.md`，共用同一验证点登记表。T0/T1 用轻量计划（同一机制裁剪，不套四卷），不是第二套分卷机制。
- **批次**：计划 §3.9 `B-Vx-xx` 批次表是执行、合并、缺陷提交、子代理、并行的真值；版本级未填=计划门遗漏，先补表；执行期缺表才默认直跑/串行并记 `deviation=no_batch_plan`。模块子代理=一模块一子代理；拆分档=Worker+Reviewer；脚本档=执行器。

## 2. 目录

| 路径 | 作用 |
| --- | --- |
| `workflows/` | `testing` / `defect` / `handoff`（交接包/回执/变更通知） / `onboard` / `materials`（权威文档库）/ `skill-audit`（能力技能体检） |
| `agents/` | analyzer / planner / testcase / **testcase-reviewer** / orchestrator / worker / reviewer（执行核验） / bug / report / onboard |
| `capabilities/` | 包侧契约+参考目录；实例真源在工作根 `{workroot}/capabilities/` |
| `skills/` | 内置专业技能（每步方法/手艺，随包生效、按步自动加载；含 `name/description` frontmatter；`skills/README.md`） |
| `AGENTS.md` | AI 入口（接入 + 口令 → workflow；版本单点） |
| `rules/read-index.md` | **维护用**索引（step→历史 MUST/RUN/REF）；运行时勿读 |
| `rules/gates.md` | 门/`when`/`gate_when` 语义、门档位；含 coverage-map / case-review / report-consistency / writeback-receipt |
| `rules/workflow.md` | 产物路径、覆盖三闸、收尾摘要（只读当前节） |
| `rules/doc-governance.md` | 资料收取/分类/覆盖对照/失效/归档 + 工作文档生命周期/归档/清理 |
| `rules/core/` | `clarification.md`、`routing.md`、`verification.md`、`execution-contract.md`、`doc-quality.md`、`rule-governance.md`、`maintenance.md`、`context-memory.md` |
| `rules/collaboration/` | `handoff.md`、`roles.md`、`subagents.md`（取档/生命周期短口径） |
| `rules/defects/` | `collaboration.md`、`classification.md`、`platform-adapter.md` |
| `rules/special/` | `multi-track-quality.md`、`release-train-load.md`、`defect-findings-spectrum.md`、`multi-agent-output.md`、`script-execution.md` |
| `rules/tracks/` | `api.md`、`exploratory.md`、`random-flows.md`、`pre-release.md`（按口令点读） |
| `rules/playbooks/` | 重阶段步骤卡：生成/执行/缺陷 |
| `rules/templates/` | 按生命周期分 6 组：`00-onboarding` / `10-planning` / `20-test-cases` / `30-execution` / `40-report-review` / `90-handoff`；先看 `rules/templates/index.md` |
| `rules/tools/` | 包自检（`Invoke-TestWorkflow -Action ValidateTemplateRefs`）+ 脚本档工具（`playwright/`、`merge-ledger.mjs`）+ 交接包校验 `validate_handoff.py` + 功能用例校验 `validate_testcase.py` + 接口用例校验 `validate_api_testcase.py` |
| `verify/` | 报告门 `verify/Invoke-Gate.ps1`、检查矩阵、台账/报告/覆盖校验脚本；独立可复制 |

> 实例在项目根：`env-baseline.md`、`activeContext.md`；测试产物统一在 **`{workroot}/`**。目录 SSOT：`rules/workflow.md` §1.3.0。  
> **统一落盘（C）**：`{NN}-{短名}/` 内 `*-功能用例/功能台账` 或 `*-接口用例/接口台账`；探索/随机戳夹自描述；发布前=`{专项}-测试方案/test-report.md`；证据轨级；共享执行器=`{workroot}/scripts/`。SSOT=`rules/workflow.md` §1.3.0。  
> **新鲜度**：准出只认本轮装填；非装填标 `未本轮验证`；报告声明 runId/suite/本轮实测。  
> **归档**：主计划/四卷/报告/CR/交接 → `{workroot}/_archive/`；域主档常青留下；细则 `rules/doc-governance.md` §7。  
> **交接**：内容优先、包按需；出站按需实拷（缺陷有平台→零导出）；入站 `handoff/inbound/{类别}/`。分析表跨轨：`{workroot}/test-analysis.md`。状态唯一入口：计划 §0。

### 2.1 实例目录分类（禁止根目录堆测试产物）

| 位置 | 放什么 | 禁止 |
| --- | --- | --- |
| 项目根 | `env-baseline.md`、`activeContext.md`、原件根 `inbound/` | 测试计划/报告/用例/台账/脚本/证据 |
| `{workroot}/` | `test-plan.md`、`test-analysis.md`、`test-report.md`、`smoke-checklist.md`、`work-log.md` | 长期堆临时；关账搬走仍有效域主档；散落评审记录 |
| `{workroot}/reviews/` | `INDEX.md` + 现行 `*-评审-*.md`；被替代进 `_archive/` | 域夹/轨根/工作根散落；只增不删 |
| `{workroot}/functional/` | 功能域：`{NN}-{短名}/` + `*-功能用例.md` + `*-功能台账.md` + `scripts/`；`evidence/`；`00-专项索引.md` | 光秃用例；接口资产；评审记录 |
| `{workroot}/api/` | 接口域：`{NN}-{短名}/` + `*-接口用例.md` + `*-接口台账.md` + `scripts/`；`evidence/` | 与功能混淆命名；评审记录 |
| `{workroot}/exploratory/` | `{主题}-{戳}/` + `*-探索用例.md` + `*-探索台账.md`；`evidence/`（方法常青·戳夹分轮） | 功能全量冒充；把戳夹当 Domain 常青库 |
| `{workroot}/random-flows/` | `_覆盖账本` + `{主题}-{戳}/` + `*-随机用例.md` + `*-随机台账.md`；`evidence/` | 计划内轨道混用 |
| `{workroot}/pre-release/` | `performance/`、`security/`、`compatibility/`、`migration/`；方案/报告/证据/脚本 | 光秃方案/报告；多专项混一案 |
| `{workroot}/changes/` | `CR-{yyyyMMdd-HHmm}-{slug}.md` | 整期方案 |
| `{workroot}/scripts/` | 共享 executor / config | 业务域脚本（放域夹） |
| `{workroot}/handoff/` | `outbound|inbound/{category}/` + `handoff-ledger.md` | 把材料库当收件箱 |
| `{workroot}/_archive/` | 主计划/四卷/报告/CR/交接快照 + `_pending-cleanup/` | 仍有效域主档 |
| `docs/materials/` | 项目级权威文档库；测试写 `05-testing` | 草稿/证据/密钥/PII |

> 规则：项目根保留 `env-baseline.md`、`activeContext.md` 与原件根 `inbound/`；所有测试产物都在 `{workroot}/` 下；权威文档库是项目级 `docs/materials/`。  
> 设计输入原件在 `inbound/`；定稿副本/完整项目文档进 `docs/materials/{ver}/`。入站 T1～T9；A0～A2 吸收；细则见 `rules/doc-governance.md`。  
> 无法判断归属 → `待确认` + 一次一问，不先移动。


### 2.2 文档分层（按需读）

| 层 | 位置 | 读法 |
| --- | --- | --- |
| 入口 | `AGENTS.md` | 新会话读 **§0 硬节**；中段按 `rules/core/rule-anchor.md` 心跳；口令表（§2）仅路由未定/首次命中时读；禁止通读全文 |
| 多包定包 | `wf/AGENTS.md` **意图→包** | 歧义口令先定包再路由 |
| 路由 | `workflows/*.yaml` | 只读命中 workflow 的当前 step |
| 运行时读链 | `cold-start`（开局）→ `_chain`/`_region`（进链一次）→ **当前步骤包**（含全局摘要，独立完整）→ §6 skill | 全局每步遵守；本步不跳转拼流程；他步可重复同文 |
| 参考手册 | `rules/workflow.md`、`rules/collaboration/subagents.md`、`rules/special/multi-agent-output.md`、`rules/defects/collaboration.md`、`rules/special/script-execution.md`、`rules/collaboration/handoff.md`（标 `读取级别：参考`） | 只读当前 step/阶段节，禁止通读 |
| 技能 | `skills/<name>/SKILL.md` | 命中步才读；不命中不读 |
| 模板 | `rules/templates/index.md` → 当前组 | 只读当前要填的一份 |
| 验证 | `verify/` | 收批/报告/回写时读；运行态写 `.gate/wf-testing/` |

> 读取预算（目标，非硬上限）：核心必读 ≤3～4（AGENTS 当前节 + 当前 step YAML 块 + 当前 agent/当前关键产物）；方法层按读取索引「命中才读」；总量目标 ≤8k，含 1 个必开技能的步骤实测可至 ~10k（技能正文是最大项），超出在收尾 `reads=` 说明，不为凑预算跳过必开技能/门/证据；不得为省预算跳过门/证据/红线。规则不是越多越稳，读全本会稀释当前 step 约束。

## 3. 上手（快速开始）

1. 复制 `wf-testing/`（排除 `.draft/`、`.state/`、`.gate/`、`__pycache__/`）；包默认不进入项目 git，不跟踪时 `.gitignore` 只写一行 `/wf-testing/`（多包 `/wf/`），不预列未装包、不加注释；在项目根 `AGENTS.md` 补入引导语句（样例见 `rules/templates/00-onboarding/root-agents-pointer.md`）
2. 设计文档放入设计输入目录（默认 `inbound/{ver|topic}/` 或 `_common/`；新文件先按 `rules/doc-governance.md` 收取/对照）  
3. 主流程：「生成测试计划」→ 计划门确认 →「生成测试资产」→「用例评审」放行 →「按测试计划执行」→ 报告/准出；日常用「当前状态 / 下一步」只读计划 §0；也可用「生成测试资产」/「执行××专题」单轨切入  
3.1 **不用口令**：任意自然语言描述要测什么/怎么测/跑测/准出即可；AI 按 `rules/core/routing.md` 抽五元组→意图类→计划状态修正，不抠固定措辞；首条 `route`/`reason`。有计划优先按 §0 续跑；未建模不得直接写用例；判断错可一句纠正。  
4. 缺陷按计划 §11 提交；有平台→**完整交平台即完成、零导出**；无平台/`export`/点名→**先问后发、本批统一一份**（禁逐条文件夹；§3.1.1）。
5. 交接：**内容优先、包按需、先问后发**。默认交报告/计划/平台缺陷；说「生成交接包…」或命中多文件/签收/仓外时才问并发包。接收类口令走 `receive`。

```text
方案文档 → 分析 → 计划 → 资产 → 执行 → 报告/准出
→（可选，经你确认）交接包 TEST/PLAN/BUG/… 
```

示例口令：

```text
生成测试计划，主读 inbound/V2.7.0/IBIPS_V2.7.0_….md
（计划门确认：范围/类型/轨道/缺陷策略/探索章程/准出）
按测试计划执行

资料收取 inbound/V2.0/…
（AI 输出入站分析 T1～T9 + 覆盖对照 + 归档候选；确认后同批落位/归档）

文档巡检
（AI 输出工作文档更新/归档 + 临时文件清理候选；确认后执行）
```

**新版本迭代执行 6 步**：

1. 读方案/提测影响面/变更点；打开 **Core 冒烟清单 + 命中域现行用例**（禁通读全库；禁跳过命中域）。
2. 计划 §3.7 装填：命中域 + **邻接影响面（宁多勿漏）**；迭代 suite=module；发版/完整项目=full。
3. 生成：命中域增量保 caseId（无域才首生）；映射/用例宁多勿漏；覆盖三闸过关 → 评审。
4. 执行：core 冒烟全绿 → 装填域（module/full）；接口 depth≥standard（迭代）/full（发版）；发布前硬映射按风险级。
5. 缺陷即回归；探索式/发布前按计划穿插并闭环目标/映射。
6. 报告声明 suite+depth+风险级；**对照多轨质量标准 §3 才可准出**；更新 Core 与 §3.7。

**期中变更（不新开计划）**：给 AI 新变化/新文档，或产品在平台确认并给新说明/附件 → `{workroot}/changes/CR-*.md` 影响分析 → 按 CR §5 更新 inbound/计划/用例/脚本/报告/索引 → P0 冒烟 + 变更用例 + 影响面 → 报告/验收。A 澄清/B 同范围增量不重开计划门；C 实质变更回计划门；D 缺陷走缺陷轨；产品确认带新 AC → D+B/D+C。**执行时机默认等计划模块/阶段位；提前仅限 P0/高风险、阻塞后续、独立且数据/入口就绪、有专门含变更构建；P0 冒烟可在构建/阶段边界先跑；执行前核构建含变更；产品确认新 AC 按新 AC 回归。**  

计划驱动执行覆盖本包可执行轨道；单元/静态、UAT、灰度/生产验证由对应团队执行或协调，计划登记责任人与证据，不冒充已测。  


## 4. 自检

```text
wf-testing/rules/tools/Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs
wf-testing/verify/Invoke-Gate.ps1 -Mode coverage -ProjectRoot "." -Strict
wf-testing/verify/Invoke-Gate.ps1 -Mode report -ProjectRoot "." -Strict
```

自检时机：改包后、用户点名；接入核验由 onboarding 接入清单执行。自检含 YAML 语法/schema（`rules/tools/validate_workflow.py`，需 Python + PyYAML）。  
**gate 2.2**：新格式硬检 `analysis-structure`/`plan-structure`/`case-vp`/`report-structure`；旧实例默认 `skip`，迁移后加 `-Strict` 变 FAIL。  
可选输入：见 §1「独立实施」；有则按用户指定路径读入，无则按现有资料执行，最多一句提示，不阻塞；回写由用户点名。

## 5. 宿主适配（宿主无关）

本包不写死任何宿主（Cursor / opencode / Claude Code 等均可）；换宿主改实例侧（`{workroot}/capabilities/` + 基线索引），包零改动。

- **最低能力**：入口自动装载（AGENTS.md 或等价）、文件读写、shell、对话式确认门（hitl）；浏览器自动化按需（功能/探索式轨必需）、子代理（分片/核验，按 `rules/collaboration/subagents.md` 取档与 §0 生命周期）。  
- **入口挂载**：AGENTS.md 系宿主按 `rules/templates/00-onboarding/root-agents-pointer.md` 挂载；CLAUDE.md 系可用 @ 引用指向本包 AGENTS.md。
- **MCP/Skill 配置落点**：只写宿主本地/用户级配置（如 Cursor：`%USERPROFILE%\.cursor\mcp.json`）；实例选型与绑定写 `{workroot}/capabilities/`（基线 §8/§17 仅索引）；禁项目内 mcp 作规范入口。
- **能力（可选）**：槽位见包内 `capabilities/00-contract.md`；候选见 `capabilities/reference.md`；**真源** `{workroot}/capabilities/00-能力清单.md`（kind=`mcp`｜`skill-cli`｜`builtin`）。清单 available 即用，否则按契约降级；**缺失触达须独立【能力缺失】块**（每次触达直至「接受降级」或装成；`prompted` 仅审计不抑制）。点名「装配能力」/「接受降级」后写实例。纪律：`rules/capabilities/instance-discipline.md`。  
- **体检能力**：口令「体检能力」等 → `skill-audit`：能力改 `{workroot}/capabilities/`，技能可改本包 `skills/`。
