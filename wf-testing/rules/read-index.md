# 读取索引（测试轨）

> **单一读取入口**：新会话开工先读 `AGENTS.md` **§0 硬节**与本索引当前 step 行；只读“核心必读”，按需再读“命中才读”。**不要通读整本rules / skills / templates**。
> **rule_anchor**：本表**当前行**即方法层锚点（含轨时只读该轨）；切 step 时重读本行（不必重读 AGENTS §0 全文）。step `notes` 的「技能：…」/`skills_required` 与映射冲突时以 YAML 为准。
> **中段重锚**：同会话已路由后按 `rules/core/rule-anchor.md` 心跳；不借心跳通读本索引全表或跨轨。
> **读取预算（目标，非硬上限）**：核心必读 ≤3～4；方法层「命中才读」；总量 ≤8k；复杂步可至 5 并在收尾 `reads=` 说明；大文件只读当前 step 对应节，**workflow 只读当前 step 块（当前 `- name:` 到下一个）**；不得为省预算跳过门/证据。
> **读序（新会话）**：① `AGENTS.md` §0（硬节）→ ② workflow 当前 step 块 → ③ 本索引当前行 → ④ 当前 agent → ⑤ 命中才读的skills / playbook 当前节 → ⑥ 当前产物/证据。**同会话中段**：心跳 → ②③④⑥。**口令表（§2）仅路由未定/首次命中时读**。
> 同一会话文件未变不重读；后续步骤 delta-only。
> **执行契约**：开工判定见 `rules/core/execution-contract.md` §1～§2/§6；心跳见 §7 / `rule-anchor.md`；不占每步常规预算。

## 默认行（所有 step）

- 核心：`AGENTS.md` §0 + 命中 `workflows/{workflow}.yaml` 当前 step 块 + 当前 `agents/{role}.yaml` + 当前产物/证据。
- **布局**：先读项目根 `layout.yaml`，定位本包 `root/workroot/materials_root/handoff_root`；缺失/同 id 双份 → 停问。
- **接入级别**：I0～I3 与 `inbound_structure` 见 `rules/doc-governance.md` §2.5；I0 先档案映射，禁止套标准路径。
- **本责索引**：读 `{workroot}/INDEX.md` 当前入口/材料包；状态以计划 §0 为准，冲突先修计划。
- **跨会话快照 + 项目身份**：开工/续跑先读项目根 `activeContext.md` **总览** + 本包 `### 进行中`；同仓优先档案 §1，否则 `env-baseline.md`「项目身份」+ §1 要点 + §2.1 目录行。无资料或资料不足 → 入口判定 §5（探仓/择要 README → **先回写工作流文档**；可选同步 README）。
- 命中才读：本索引对应行。
- 不读：其它 workflow、全部 agents、全部规则、全部模板；**不跨轨通读**。

> 模板引用若用短名（如“产品计划模板”“测试报告模板”），先按 `rules/templates/index.md` 定位到组；不要猜路径。

## 按 step

| step | 核心必读 | 命中才读 | 预算 |
| --- | --- | --- | ---: |
| 工作总结口令（无 workflow） | `rules/templates/90-交接与收尾/收尾骨架.md` §4（含围栏外 `范围：from～to`）+ 项目根 `activeContext.md` 本包「工作总结锚点」 | 测试计划/台账/工作日志（仅区间内） | 6k |
| 无口令/意图不明 | `rules/core/routing.md` §0～§4 + §6 + env-baseline.md要点 + 计划 §0（有则） | 附录校验、台账/报告摘要 | 5k |
| testing.status | `workflows/testing.yaml` 当前 step 块（status）+ `{workroot}/test-plan.md` §0/§9/§16 | activeContext | 4k |
| testing.analyze | `workflows/testing.yaml` 当前 step 块（analyze）+ `skills/test-basis-analysis` + `测试分析表模板.md`（§0 Brief+Delta 必填）+ **用户版业务变化说明模板** | `workflow.md` §2.1.0；`clarification.md` 本步相关节；主读/产品或开发 Delta/上版失败摘要；`test-data-and-environment`；`ai-feature-testing`（主读含 AI/LLM 时） | 8k |
| testing.plan（轻量） | `rules/playbooks/generate.md` + `测试计划-轻量模板.md` + **测试分析表** | `skills/test-analysis-and-plan`；`test-data-and-environment`；上版报告/稳定冒烟；`ai-feature-testing` | 8k |
| testing.plan（版本级） | `测试计划模板.md` **§0 + 本轮待填节**（禁整文件通读）+ `rules/playbooks/generate.md` + **测试分析表** + **用户版说明（如有）** | `skills/test-analysis-and-plan`；AC→TP 追溯（表内）；模板其它节按需；输入清点；文档治理 §3（有新文档时）；`test-data-and-environment`；`ai-feature-testing` | 8k |
| testing.generate（功能） | `rules/playbooks/generate.md` + `workflow.md` §2.1.0 + **`测试用例模板.md`** + 多轨质量 §2.1 + 计划 §3.2/§3.7 + **测试分析表** + **用户版说明（如有）** + **命中域现行用例** | `skills/testcase-design`；脚本执行 §1/§2；`ai-feature-testing` | 8k |
| testing.generate（接口） | `generate.md` + **`tracks/api.md`** + **`接口测试用例模板.md`** + 多轨质量 §2.2 + 分析表 §0 + **命中接口域现行资产** | `skills/test-interface`；脚本执行 §2；`validate_api_testcase.py` | 8k |
| testing.generate（探索式） | `generate.md` + **`tracks/exploratory.md`** + **`探索式用例模板.md`** + 多轨质量 §2.4 + 分析表 §0 | 计划 §12；`test-execution-and-exploration` §4 | 8k |
| testing.generate（随机业务流程） | `generate.md` + **`tracks/random-flows.md`** + **`随机业务流程用例模板.md`** | `_覆盖账本` 最近 N 轮；有则基线菜单地图/`00-稳定冒烟清单`（办结候选）；禁计划/主读/分析表当编排或判定 | 8k |
| testing.generate（发布前） | `generate.md` + **`tracks/pre-release.md`** + `多轨质量标准` §2.3 + 计划发布前节/硬映射 | 专项技能（性能/安全/兼容）；工具 README；分析表 §0 | 8k |
| testing.coverage | `verify/README.md` + `rules/core/verification.md` + 功能用例 §3/§4 + 计划 §3.2/§3.7 | 工作流 §2.1.0；`testcase-design` §2.2 | 4k |
| testing.review-cases | `workflow.md` §2.5 + `skills/test-artifact-review` + `skills/testcase-review` + 评审记录模板 + 被审产物 | coverage 回执、计划 §3.2/§9.2、`ai-feature-testing` | 8k |
| testing.plan（评审） | 技能 `test-artifact-review` + 计划量规 + 计划原文 | 测试分析表、§0/§2/§3/§5/§9 | 6k |
| testing.execute（功能/专项） | `rules/playbooks/execute.md` + `workflow.md` §3.0/§3.1 + 计划 §0/§3.7/§9 + 装填域用例/台账 | 测试分析表（oracle）；开跑前核评审放行；`多Agent` 当前节；`test-data-and-environment`；`ai-feature-testing` | 8k |
| testing.execute（脚本档） | `rules/playbooks/execute.md` + `rules/special/script-execution.md` §3/§4 + executor README | `多Agent` §3 | 8k |
| testing.execute（接口） | `rules/playbooks/execute.md` + `rules/tracks/api.md` + `接口测试用例模板`（当前域）+ `多轨质量标准` §2.2 + 技能 `test-interface` | 脚本执行 §3 | 8k |
| testing.execute（探索式） | `rules/playbooks/execute.md` + `rules/tracks/exploratory.md` + `多轨质量标准` §2.4 + **本轮探索式用例**（四列步骤） | `多Agent` §1.1/§2.1；`test-execution-and-exploration` §4 | 8k |
| testing.execute（随机业务流程） | `rules/playbooks/execute.md` + `rules/tracks/random-flows.md` + **本轮随机用例** | `多Agent` §1.1/§2.1；`test-execution-and-exploration` §4.1；账本窗；禁计划/主读当编排或判定 | 8k |
| testing.execute（发布前） | `rules/playbooks/execute.md` + `rules/tracks/pre-release.md` + `多轨质量标准` §2.3 + 专项技能 | 工具 README、`ai-feature-testing` | 8k |
| testing.execute（批末） | `verify/README.md` + `verification.md` + 本模块台账；`Invoke-Gate.ps1 -Mode execute -Scope …` | 计划 §9/§10 | 6k |
| testing.report | `verify/README.md` + `rules/core/verification.md` + `多轨质量标准` §3 + `workflow.md` §4 + 测试报告模板 + 计划 §5/§9/§10 | 收尾骨架 §0/§0.5/§2；台账/证据；`工作日志模板.md`；`ai-feature-testing` | 8k |
| testing.handoff | `verify/README.md`（writeback）+ 收尾骨架 §0/§0.5/§2 + 拟提交/交平台清单 | git 状态、回写回执 | 6k |
| handoff.compose | `workflows/handoff.yaml` compose 块 + 协作 §3.0～§3.0.1 + `通用交接单文档模板.md` + 台账 | 专模（报告/计划等） | 6k |
| handoff.*（status/send/receive/change_*/replan） | `workflows/handoff.yaml` 当前 step 块 + 协作当前节；**send** 另加交接包说明/清单 + 台账/计划 | 接收回执模板、测试报告/变更模板 | 8k |
| defect.* | `workflows/defect.yaml` 当前 step 块 + `rules/playbooks/defect.md` + `rules/defects/collaboration.md` 当前节（提交含 §6.0） | 平台适配 §0+能力（平台时）；缺陷文案（提交/回写时）；缺陷分类含 §0（分流/判类型）；基线缺陷节 | 8k |
| onboard.* | `workflows/onboard.yaml` 当前 step 块 + `agents/onboard-agent.yaml` + `rules/doc-governance.md` | env-baseline.md模板、`rules/templates/00-接入与基线/capabilities/`、`rules/capabilities/instance-discipline.md`、`工作日志模板.md` | 8k |
| skill-audit.* | `workflows/skill-audit.yaml` 当前 step 块 + `agents/onboard-agent.yaml` + `rules/playbooks/skill-audit.md` 当前节（discover 必读 §2.1） | `{workroot}/capabilities/00-能力清单.md`、包内契约/参考目录、`skills/README.md`、体检报告模板；按范围抽查 SKILL；discover 时 skills.sh / `npx skills find` | 8k |

| materials.publish | `workflows/materials.yaml` 当前 step 块 + `rules/doc-governance.md` §5.2 + `docs/materials/INDEX.md` + `{workroot}` 当前定稿 | 版本 README/域目录/来源 | 6k |

## 读取纪律

- 先读标题/目录/当前节；不要从第一行读到最后一行。
- 同一文件只读一次；后续步骤用 delta-only。
- 需要跨文件综合时，先列“要回答的问题”，再定向 grep/读节；不要用“通读”代替定位。
- 子代理只读派发路径与节选，不读整本rules/档案/历史；Reviewer 只收 jsonl+证据+预期。
- 规则阅读不是“越多越稳”：读错轨/读全本会稀释当前步约束；只读当前 step 卡。
- 任何澄清/追问 → `rules/core/clarification.md`；不另造提问格式。
