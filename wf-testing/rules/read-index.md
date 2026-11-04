# 读取索引（维护用 · 非运行时必读）

> **维护目录**：运行时读链只认 `cold-start` + 当前 YAML step + `rules/packets/<wf>/<step>.md`（+ 可选一个模板）。  
> 本文不再作为 AI 执行必读；改步骤规则以 packets 为准，可用 `rules/tools/build_step_packets.py` 重生。  
> 下列表格仅供维护者对照历史 MUST/RUN/REF 与口令定位。

## 默认行（所有 step）

- **核心必读（≤4 来源）**：`cold-start.md`（新会话/心跳）· 命中 workflow 当前 step 块 · 当前 agent · 当前产物/证据。
- **定位（不计入必读）**：工作根、接入级别、索引口径只认 `rules/doc-governance.md` §2.4/§2.5；入口/材料包看 `{workroot}/INDEX.md`；跨会话快照看项目根 `activeContext.md` 总览 + 本包 `### 进行中` + **偏好/洞见/坑≤3**（开局卡第 2 条；写法 `context-memory.md`）；项目身份见 `env-baseline.md`（`AGENTS.md` §0 已列）。
- **命中才读**：本索引对应行；方法层 skills / playbook / 模板按 step 命中再读。
- 不读：其它 workflow、全部 agents、全部规则、全部模板；**不跨轨通读**。

> 模板引用若用短名（如“产品计划模板”“测试报告模板”），先按 `rules/templates/index.md` 定位到组；不要猜路径。

## 按 step

> 行内 `workflow.step` 为定位项；`/` 分隔并列项（可跨 workflow）；`workflow.*` = 该 workflow 全部 step。

| step | 核心必读 | 命中才读 | 预算 |
| --- | --- | --- | ---: |
| 工作总结口令（无 workflow） | `rules/templates/90-handoff/closeout-skeleton.md` §4（含围栏外 `范围：from～to`）+ 项目根 `activeContext.md` 本包「工作总结锚点」 | 测试计划/台账/工作日志（仅区间内） | 6k |
| 无口令/意图不明 | `rules/core/routing.md` §0～§6（含 §5 资料不足升级）+ env-baseline.md要点 + 计划 §0（有则） | 附录校验、台账/报告摘要 | 5k |
| testing.status | `workflows/testing.yaml` 当前 step 块（status）+ `{workroot}/test-plan.md` §0/§3.8/§3.9/§9/§16 | activeContext | 4k |
| testing.analyze | `workflows/testing.yaml` analyze 块 + `skills/test-basis-analysis` + `test-analysis-template.md`（§0 Brief+Delta）+ 当前主读/分析表产物 | 用户版说明模板；`workflow.md` §2.1.0；`clarification.md` 本步节；产品或开发 Delta/上版失败摘要；`test-data-and-environment`；`ai-feature-testing`（AI/LLM 时） | 8k |
| testing.plan（轻量） | `rules/playbooks/generate.md` + `test-plan-lite-template.md` + **测试分析表** | `skills/test-analysis-and-plan`；`test-data-and-environment`；上版报告/稳定冒烟；`ai-feature-testing` | 8k |
| testing.plan（版本级） | `test-plan-template.md` **§0 + 本轮待填节**（禁整文件通读）+ `rules/playbooks/generate.md` + **测试分析表** + **用户版说明（如有）** | `test-plan-volume-template.md`（四卷）；`多Agent` §1.1/§1.5（批次/执行形态）；`skills/test-analysis-and-plan`；AC→TP 追溯（表内）；模板其它节按需；输入清点；文档治理 §3（有新文档时）；`test-data-and-environment`；`ai-feature-testing` | 8k |
| testing.generate（功能） | `rules/playbooks/generate.md` + **`test-case-template.md`** + 技能 `testcase-design` + 命中域现行用例/分析表产物 | `workflow.md` §2.1.0；多轨质量 §2.1；计划 §3.2/§3.7；分析表 §2.2～§2.4/§3.1/§6/§7.2；用户版说明；脚本执行 §1/§2；`ai-feature-testing` | 8k |
| testing.generate（接口） | `generate.md` + **`tracks/api.md`** + **`api-test-case-template.md`** + **技能 `test-interface`** + 多轨质量 §2.2 + 分析表 §0 + **命中接口域现行资产** | 脚本执行 §2；`validate_api_testcase.py`；`ai-feature-testing`（AI 接口时） | 8k |
| testing.generate（探索式） | `generate.md` + **`tracks/exploratory.md`** + **`exploratory-case-template.md`** + 多轨质量 §2.4 + 分析表 §0 | 计划 §12；`test-execution-and-exploration` §4 | 8k |
| testing.generate（随机业务流程） | `generate.md` + **`tracks/random-flows.md`** + **`random-flow-case-template.md`** | `_覆盖账本` 最近 N 轮；有则基线菜单地图/`smoke-checklist.md`（办结候选）；禁计划/主读/分析表当编排或判定 | 8k |
| testing.generate（发布前） | `generate.md` + **`tracks/pre-release.md`** + `多轨质量标准` §2.3 + 计划发布前节/硬映射 | 专项技能（性能/安全/兼容）；工具 README；分析表 §0 | 8k |
| coverage 闸（generate 后/execute 前） | `verify/README.md` + `rules/core/verification.md` + 功能用例 §3/§4 + 计划 §3.2/§3.7 + 分析表 §2.2/§2.3/§2.4/§3.1/§6/§7.1/§7.2 | 工作流 §2.1.0；`testcase-design` §2.2 | 6k |
| testing.review-cases | `workflow.md` §2.5 + `skills/test-artifact-review` + `skills/testcase-review` + 评审记录模板 + 被审产物 | coverage 回执、计划 §3.2/§9.2、`ai-feature-testing` | 8k |
| testing.plan（评审） | 技能 `test-artifact-review` + 计划量规 + 计划原文 | 测试分析表、§0/§2/§3/§5/§9、§2.2/§2.3/§2.4、§3.8/§3.9 | 8k |
| testing.execute（功能/专项） | `rules/playbooks/execute.md` + `workflow.md` §3.0/§3.1 + **技能 `test-execution-and-exploration`** + 计划 §0/§3.7/§3.9/§9（T0/T1 用 lite §3/§8）+ 装填域用例/台账 | 写完整【执行收尾】时→`closeout-skeleton.md` §1；测试分析表（oracle）；开跑前核评审放行；`多Agent` 当前节（批次真值 §4.1）；`test-data-and-environment`；`ai-feature-testing` | 8k |
| testing.execute（脚本档） | `rules/playbooks/execute.md` + `rules/special/script-execution.md` §3/§4 + executor README | 写完整【执行收尾】时→骨架 §1；`多Agent` §3 | 8k |
| testing.execute（接口） | `rules/playbooks/execute.md` + `rules/tracks/api.md` + `api-test-case-template.md`（当前域）+ `多轨质量标准` §2.2 + 技能 `test-interface` | 写完整【执行收尾】时→骨架 §1；脚本执行 §3 | 8k |
| testing.execute（探索式） | `rules/playbooks/execute.md` + `rules/tracks/exploratory.md` + `多轨质量标准` §2.4 + **本轮探索式用例**（四列步骤） | 写完整【执行收尾】时→骨架 §1；`多Agent` §1.1/§2.1；`test-execution-and-exploration` §4 | 8k |
| testing.execute（随机业务流程） | `rules/playbooks/execute.md` + `rules/tracks/random-flows.md` + **本轮随机用例** | 写完整【执行收尾】时→骨架 §1；`多Agent` §1.1/§2.1；`test-execution-and-exploration` §4.1；账本窗；禁计划/主读当编排或判定 | 8k |
| testing.execute（发布前） | `rules/playbooks/execute.md` + `rules/tracks/pre-release.md` + `多轨质量标准` §2.3 + 专项技能 | 写完整【执行收尾】时→骨架 §1；工具 README、`ai-feature-testing` | 8k |
| testing.execute（批末） | `verify/README.md` + `verification.md` + 本模块台账 + `closeout-skeleton.md` §1；`Invoke-Gate.ps1 -Mode execute -Scope …` | 计划 §3.9 批次合并/§9/§10 | 6k |
| testing.report | `verify/README.md` + `rules/core/verification.md` + 测试报告模板 + 计划/台账本轮产物 | `多轨质量标准` §3；`workflow.md` §5；计划 §5/§9/§10/§3.9；收尾骨架 §2/§0；`context-memory.md` §4；批次/并行统计；`work-log-template.md`；`ai-feature-testing` | 8k |
| testing.handoff | `verify/README.md`（writeback）+ `closeout-skeleton.md` §1 + `context-memory.md` §4 + 拟提交/交平台清单 | 骨架 §0；git 状态、回写回执 | 6k |
| commit（handoff/defect wrap） | `rules/templates/90-handoff/closeout-skeleton.md` §0/§0.5/§2 + `rules/workflow.md` §4.1 + git 状态；有门回执时 + `.gate/wf-testing/report.json` | 拟提交·仓库/回写回执 | 5k |
| handoff.compose | `workflows/handoff.yaml` compose 块 + 协作 §3.0～§3.0.1 + `handoff-note-template.md` + 台账 | 专模（报告/计划等） | 6k |
| handoff.*（status/send/receive/change_*/replan） | `workflows/handoff.yaml` 当前 step 块 + 协作当前节；**send** 另加交接包说明/清单 + 台账/计划 | 接收回执模板、测试报告/变更模板 | 8k |
| defect.* | `workflows/defect.yaml` 当前 step 块 + `rules/playbooks/defect.md` + `rules/defects/collaboration.md` 当前节（提交含 §6.0） | 平台适配 §0+能力（平台时）；缺陷文案（提交/回写时）；缺陷分类 §0/§0.4（分流/到不了防混）；基线缺陷节 | 8k |
| onboard.* | `workflows/onboard.yaml` 当前 step 块 + `agents/onboard-agent.yaml` + `rules/doc-governance.md` 当前节（§2.4 起） | `env-baseline-template.md`、`rules/templates/00-onboarding/capabilities/`、`rules/capabilities/instance-discipline.md`、`work-log-template.md` | 8k |
| skill-audit.* | `workflows/skill-audit.yaml` 当前 step 块 + `agents/onboard-agent.yaml` + `rules/playbooks/skill-audit.md` 当前节（discover 必读 §2.1） | `{workroot}/capabilities/00-能力清单.md`、包内契约/参考目录、`skills/README.md`、体检报告模板；按范围抽查 SKILL；discover 时 skills.sh / `npx skills find` | 8k |
| materials.* | `workflows/materials.yaml` 当前 step 块 + `rules/doc-governance.md` §5.2 + `docs/materials/INDEX.md` + `{workroot}` 当前定稿 | 版本 README/域目录/来源 | 6k |

## 读取纪律

- 先读标题/目录/当前节；不要从第一行读到最后一行。
- 同一文件只读一次；后续步骤用 delta-only。
- 需要跨文件综合时，先列“要回答的问题”，再定向 grep/读节；不要用“通读”代替定位。
- 子代理只读派发路径与节选，不读整本rules/档案/历史；Reviewer 只收 jsonl+证据+预期。
- 规则阅读不是“越多越稳”：读错轨/读全本会稀释当前步约束；只读当前 step 卡。
- 任何澄清/追问 → `rules/core/clarification.md`；不另造提问格式。
