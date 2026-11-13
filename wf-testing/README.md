# AI 测试资产体系 — 使用说明

> 供人阅读；**AI 新会话先读** `AGENTS.md` → `rules/core/cold-start.md` → `rules/core/global-rules.md`（每步重读）。  
> **template_version**：以 `AGENTS.md` 为准（单点）。

## 1. 是什么

**AI Workflow 包（测试轨）**：分析驱动，主链 **分析 → 计划 → 执行 → 报告**。  
- **测试分析** `{workroot}/{ver}/test-analysis.md` 必做：来源盘点、章节回执、依据覆盖、AC/设计点账本、意图台账、覆盖矩阵、方法矩阵、D01–D13 + S6/S7/S11、风险/影响面/核心链路。分析是原文索引；执行三步序在 execute 步骤卡（方案原文 → 结合分析理解 → 现场择优；有互补源则对照；禁只读分析）。
- **环境基线** `env-baseline.md`：环境/账号/接口/样本真值；分析、计划、执行前读命中节，计划 §2.2 写命中节/差异/核验。
- **测试计划** `{workroot}/{ver}/test-plan.md` 是唯一总排：范围、分析引用、影响面/核心链路摘要、类型/轨道、轮次/批次（§3.1 执行形态/并行/隔离，填表口径在计划模板该节）、探索安排、准入准出、缺陷策略、状态/日志。计划不重复分析大表；子代理≠并行，无隔离默认串行。
- **执行记录** `{workroot}/{ver}/functional|api/{NN}-{短名}-执行记录.md`（轨内平铺）：§0 原文对账 + 场景 + 步骤 + 结果 + 证据 + 缺陷，另含每意图终态与原文条目关账。
- **回归锚点** `{workroot}/smoke-checklist.md`：P0 冒烟 + 高价值场景（跨迭代常青）。
- **报告** `{workroot}/{ver}/test-report.md`：按场景/意图/优先级/轨道汇总。

用户说「按测试计划执行」或「继续测试计划」时，按计划执行**全部在范围 P0/P1/P2 意图与轨道**，直到本轮终态；P1/P2 不得用低优先级跳过。

## 2. 目录

| 路径 | 作用 |
| --- | --- |
| `workflows/` | `testing` / `defect` / `handoff` / `onboard` / `materials` / `skill-audit` |
| `agents/` | planner / orchestrator / reviewer / worker / bug / report / onboard |
| `capabilities/` | 包侧契约+参考目录；实例真源 `{workroot}/capabilities/` |
| `skills/` | 依据分析、计划、场景设计、执行、接口、发布前、报告与准出 |
| `rules/gates.md` | 门/`when`/`gate_when` 语义 |
| `rules/workflow.md` | 参考：产物路径/轨道/执行规则（运行时以 `global-rules.md` + 链图 + 步骤卡为准） |
| `rules/tracks/` | `api.md`、`exploratory.md`、`random-flows.md`、`pre-release.md` |
| `rules/templates/` | 分析/计划/执行记录/报告/交接模板；先看 `templates/index.md` |
| `rules/tools/` | 包自检 + 脚本档工具 + 执行记录校验 |
| `verify/` | 覆盖/执行/报告门；运行态写 `.gate/wf-testing/` |

> 实例在项目根：`env-baseline.md`、`activeContext.md`；常青在 **`{workroot}/`**，本期在 **`{workroot}/{ver}/`**。目录 SSOT：`rules/workflow.md` §1.3。  
> **统一落盘**：轨内平铺（单文件不建夹）；功能/接口 `{NN}-{短名}-执行记录.md`；探索/随机 `{主题}-{戳}-…记录.md`；发布前 `{专项}-测试方案.md` + `{专项}-test-report.md`；证据 `{ver}/evidence/`；脚本 `{workroot}/scripts/`。

## 3. 上手

1. 复制 `wf-testing/`（排除 `.draft/`、`.state/`、`.gate/`、`__pycache__`）；包默认不进入项目 git；不跟踪时 `.gitignore` 写 `/wf-testing/`（多包 `/wf/`）与运行态 `.gate/`，不预列未装包、不加注释；在项目根 `AGENTS.md` 补引导语句（样例 `rules/templates/00-onboarding/root-agents-pointer.md`）。
2. 设计文档放入 `inbound/{ver|topic}/` 或 `_common/`；按 `rules/doc-governance.md` 收取/对照。
3. 主流程：**「根据 XX 迭代生成测试计划」→ 计划门确认 →「按测试计划执行」→「测试报告」**。
   - `plan` 内先完成分析（来源/AC/设计点/意图/风险），再写总排；不要求先单独说“分析需求”。
   - `execute` 按计划执行全部在范围 P0/P1/P2 意图与轨道，AI 对照原文/原型/AC + 分析意图/影响面生成场景并写执行记录。
4. 缺陷按计划 §5 提交；有平台→完整交平台、零重复导出；无平台/点名→先问后发、本批统一一份。
5. 交接：内容优先、包按需、先问后发；报告/计划/锚点为默认自洽交付物。

```text
方案/迭代 → 分析（来源/意图/风险/覆盖） → 计划（总排） → 执行（边生成边记录） → 报告/准出
```

示例口令：

```text
根据 V2.7 迭代生成测试计划，主读 inbound/V2.7.0/…
（计划门确认：范围/分析计数/P0/P1/P2/N/A/准出）
按测试计划执行
测试报告
```

**新版本迭代执行 6 步**：

1. 读方案/提测影响面/变更点；打开 `{ver}/test-analysis.md` 与 `{ver}/test-plan.md`、根 `smoke-checklist.md`。
2. 计划按 `multi-track-quality` **§0** 硬纳入正式轨（整轨否仅白名单+接受人）；§3：R0 → R1 功能/接口/探索/发布前 → R2 回归。
3. 执行：开跑直接打开原文，按原文目录/可验收单元逐项对照；逐场景对照原文对应段（有互补源则对照；分析只作索引）；P0 至少一条证伪场景；按意图/影响面/方法矩阵生成场景；脚本优先；边执行边写执行记录与原文对账；UI 探针 ≠ 接口轨；**失败/待实现行当场按执行模板 §2/§3 失败卡写满（含 `surface`/技术附记），批末门检；交单只逐槽位搬运**。
4. 缺陷即回归：原单 + 冒烟子集 + 影响面 + 锚点。
5. 探索式与发布前按计划闭环硬映射；小改用发布前基础级，不整轨取消。
6. 报告声明 suite/depth/发布前风险级 + 意图结论 + 缺口；对照 `multi-track-quality` 准出。

**期中变更（不新开计划）**：给 AI 新变化/新文档 → `{workroot}/{ver}/changes/CR-*.md` 影响分析 → 更新分析/计划/执行记录 → P0 冒烟 + 变更意图 + 影响面 → 报告/验收。A 澄清/B 同范围增量不重开计划门；C 实质变更回计划门；D 缺陷走缺陷轨。

## 4. 自检

```text
wf-testing/rules/tools/Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs
wf-testing/verify/Invoke-Gate.ps1 -Mode coverage -ProjectRoot "." -Strict
wf-testing/verify/Invoke-Gate.ps1 -Mode report -ProjectRoot "." -Strict
python wf-testing/verify/tools/selftest_gate.py
```

自检时机：改包后、用户点名；接入核验由 onboarding 接入清单执行。自检含 YAML 语法/schema、引用、锚点、步骤包、技能质量、生成漂移；门自测含正例+反例（计数/假 INT/lite 版本/幽灵意图/P0 改写/P0 记不适用/无 P0/计划草稿/批次 ID 不匹配/失败详情/交单回执）。

## 5. 宿主适配

本包不写死任何宿主；换宿主改实例侧（`{workroot}/capabilities/` + 基线索引），包零改动。

- **最低能力**：入口自动装载、文件读写、shell、对话式确认门；浏览器自动化按需（功能/探索式）；子代理可选（多模块执行/大文档分片；无 Task 降级直跑）。
- **入口挂载**：AGENTS.md 系按 `root-agents-pointer.md`；CLAUDE.md 系可用 @ 引用本包 AGENTS。
- **MCP/Skill 配置**：只写宿主本地/用户级配置；实例选型与绑定写 `{workroot}/capabilities/`。
- **能力（可选）**：槽位见 `capabilities/00-contract.md`；真源 `{workroot}/capabilities/00-能力清单.md`；缺失按契约降级；未接受降级每次触达出【能力缺失】块（契约 §2）。纪律 `rules/capabilities/instance-discipline.md`。
- **体检能力**：口令「体检能力」→ `skill-audit`；能力改实例，技能可改本包 `skills/`。业务收尾可附至多 1 条能力/技能建议（有判据）。

## 6. 质量与成本

- **完整覆盖 / 完整执行 / 准出**：只认 `rules/special/multi-track-quality.md` **§0** + 文首 + §3。
- **优先级** = P0/P1/P2 都是覆盖义务，不是免测开关。
- **影响面** = 直接/邻接/上游/下游/共享数据/事件/回归；迭代不能只测改动模块。
- **探索** = T1+ 高风险面有结论；有面对须覆盖；场次按风险面/预算；风险面 ≥4（少则事实说明+接受人）；T0/补丁可 N/A+用户确认（Q19）。
- **T3 默认** = suite≥`module`、接口 depth≥`standard`、发布前≥标准级；降档写事实依据+用户确认；计划 §0 须写档位依据。
- **方法** = 质量特性（ISO 25010 八类）+ 方法矩阵（常用列 + 其他方法）；P0/关键至少两种方法或写单方法依据；按风险选，不要求全用。
- **关账** = 认正文（Q18）；**接受人** = 用户当轮确认，禁 AI 自填顶替必做（Q19）。
- **脚本优先**：确定性/P0/接口/稳定主链路优先脚本。
- **不做**：全量用例库维护、预生成逐步骤用例、逐用例多轮检查、全库日常重跑。
