# 读取索引（维护用 · 非运行时必读）

> **维护目录**：运行时读链只认 `cold-start` + 当前 YAML step + `rules/packets/<wf>/<step>.md`（+ 可选一个模板）。  
> 本文不再作为 AI 执行必读；改步骤规则以 packets 为准，可用 `rules/tools/build_step_packets.py` 重生。  
> 下列表格仅供维护者对照历史 MUST/RUN/REF 与口令定位。

## 默认行（所有 step）

- **核心必读（≤4 来源）**：`cold-start.md`（新会话/心跳）· 命中 workflow 当前 step 块 · 当前 agent · 当前产物/证据。
- **定位（不计入必读）**：工作根、接入级别、索引口径只认 `rules/doc-governance.md` §2.4/§2.5；入口/材料包看 `{workroot}/INDEX.md`；跨会话快照看项目根 `activeContext.md` 总览 + 本包 `### 进行中` + **偏好/洞见/坑≤3**（开局卡第 2 条；写法 `context-memory.md`）；项目身份见 `product-profile.md` §1（`AGENTS.md` §0 已列）。
- **命中才读**：本索引对应行「可选」列；方法层 skills / playbook / 模板按 step 命中再读。
- 不读：其它 workflow、全部 agents、全部模板、全本规则。

> 模板引用若用短名（如“产品计划模板”“UAT验收模板”），先按 `rules/templates/index.md` 定位到组；不要猜路径。  
> **技能绑定**：优先认 workflow 当前 step 的 `skills:` / `must_read:`；与 `skills/README.md` 映射一致时以 YAML 为准。

## 按 step

> 行内 `workflow.step` 为定位项；`/` 分隔并列项（可跨 workflow）；`workflow.*` = 该 workflow 全部 step；`commit` / `wrap` 为全局行，适用各 workflow 的对应末步。

| step | 必读（核心 + 命中才读） | 可选 | 预算 |
| --- | --- | --- | ---: |
| 工作总结口令（无 workflow） | `rules/templates/90-handoff/closeout-skeleton.md` §3（含围栏外 `范围：from～to`）+ 项目根 `activeContext.md` 本包「工作总结锚点」 | 产品计划/工作日志（仅区间内） | 6k |
| 无口令/意图不明 | `rules/core/routing.md` §0～§6（五元组/意图类/状态/首条/资料不足升级）+ product-profile.md相关节 | 附录校验、产品计划 §0、需求池 | 5k |
| plan.goals / roadmap / scope / publish / next | `workflows/plan.yaml` 当前 step 块 + 产品计划模板（含 §3.0）+ `rules/core/clarification.md` §1～§5 + 技能（迭代=`requirement-discovery-and-prioritization` / 0→1=`zero-to-one-product-definition`）；`next` 以计划 §0 为主 | 迭代变更摘要模板、需求池/上期复盘/客户需求简报、`analytics-and-experimentation`、`work-log-template.md`、`doc-quality.md` §2 计划行 | 8k |
| new-product.discover / go | `workflows/new-product.yaml` 当前 step 块 + `rules/core/clarification.md` §1～§5 + 技能 `zero-to-one-product-definition` + 立项书模板 | `customer-needs-discovery`、`competitive-intelligence-and-learning`（模式 S）、竞品分析模板、访谈指南/洞察综合、竞品/市场资料 | 8k |
| new-product.define / prd / deliver / launch | 子链 `plan`/`prd`/`deliver` **当前 step 块**（门在子 yaml hitl）；本步 notes；PRD 模板（小改轻量节） | 计划/原型/UAT；子链 wrap/commit 不跑 | 8k |
| prd.discover | `workflows/prd.yaml` discover 块 + `rules/core/clarification.md` §1～§5 + `customer-needs-discovery` + `requirement-discovery-and-prioritization` + 需求池；竞品分析口令加 `competitive-intelligence-and-learning`（S）+ 竞品分析模板 | 访谈指南/洞察综合、文档治理 §3、竞品资料 | 8k |
| prd.benchmark | `workflows/prd.yaml` benchmark 块 + `competitive-intelligence-and-learning`（模式 P）+ 竞品对标模板 + 需求池 | `requirement-discovery-and-prioritization`、browser 资料 | 8k |
| prd.prioritize | `workflows/prd.yaml` prioritize 块 + `rules/core/clarification.md` §1～§5 + `requirement-discovery-and-prioritization` + 需求池 | 竞品分析/对标产物、洞察综合 | 8k |
| prd.prd | `workflows/prd.yaml` prd 步 + PRD 模板（P2/P3）或 `prd-lite-template.md`（P0/P1）+ 技能 `prd-writing` + 需求理解/受理单（有则） | 需求池、计划 §3/§7、资料、`analytics-and-experimentation`（有指标/埋点）、`doc-quality.md` §2 PRD 行 | 8k |
| prd.prototype | 同 `prototype.*` 当前 step（子链切入）；`workflows/prd.yaml` prototype 步 notes | 设计情境/原型产物 | 8k |
| prd.review | 技能 `artifact-review` + 评审记录模板 + 当前 PRD + `verify/README.md` | `review-and-finalize`（选 B）、需求理解、计划 §3、需求池 | 8k |
| plan.review-plan | 技能 `artifact-review` + 产品计划原文 | 计划模板 §目标/范围 | 6k |
| prototype.review | 技能 `artifact-review` + `prototype-coverage.md`（产物，含真实浏览器走查证据）+ 设计评审模板 + `verify/README.md`（design-review 机器门） | 原型/交接、`ui-visual-design-system` | 8k |
| prd.handoff | `workflows/prd.yaml` handoff + `rules/collaboration/handoff.md` §3/§4 + 交接包说明/清单模板 + PRD/评审/原型 | handoff-ledger.md、产品计划 §12 | 8k |
| change.intake / triage | `workflows/change.yaml` 当前步 + `clarification.md`（intake）+ 受理模板 + 技能 `change-management` 必做 | `customer-needs-discovery`（intake）、playbook/change REF、文档治理 §3 | 8k |
| change.new_requirement | change 当前步 + 技能 `requirement-discovery-and-prioritization` 必做 + 需求池 | `customer-needs-discovery`、立项书、playbook REF | 8k |
| change.assess / decide | change 当前步 + `change-management` 必做 + 受理模板 §4/§5 | 变更单模板、gates 对应行、playbook REF | 8k |
| change.apply / review | change 当前步 + `change-management`/`artifact-review` 必做 | 受理 §6、评审模板、`verify/README.md`、playbook REF | 8k |
| change.verify | change verify 步 + `verify/README.md` + 受理 §7 | handoff-ledger、UAT 证据、playbook REF | 8k |
| change.wrap / commit | `closeout-skeleton.md` §0～§1；（commit）workflow.md §3 REF | context-memory §4 | 6k |
| defect.preflight / pull / source / analyze | `workflows/defect.yaml` 当前步 + `rules/playbooks/defect.md` 对应行 + `rules/defects/platform-collaboration.md` 当前节 | 受理模板、product-profile.md §7、能力契约 | 8k |
| defect.decide / apply / review | `workflows/defect.yaml` 当前步 + playbook 对应行 + 缺陷平台协作当前节 | 变更单/处置/评审模板 | 8k |
| defect.writeback / verify | `workflows/defect.yaml` 当前步 + playbook 对应行 + `rules/templates/30-review-change/defect-writeup-template.md`（回写）+ `verify/README.md`（writeback） | 平台适配定义、UAT/回归证据 | 8k |
| prototype.context / ia / wireframe / visual / hi-fi / engineering / review / usability / handoff | `workflows/prototype.yaml` 当前 step 块 + `rules/playbooks/prototype.md` + 技能当前节；context 优先读已有竞品分析/对标 | 原型脚手架、设计评审/交接模板、`competitive-intelligence-and-learning` §5 | 8k |
| deliver.schedule | `workflows/deliver.yaml` schedule + 交付计划模板 | 产品计划 §4 | 6k |
| deliver.review-plan-deliver | 技能 `artifact-review` + 交付计划原文 | PLAN 交接规则 | 6k |
| deliver.followup / uat / release | `workflows/deliver.yaml` 当前 step 块 + `rules/playbooks/release.md` + 技能当前节 + `verify/README.md`（uat） | UAT/复盘模板、`analytics-and-experimentation`（发布度量）、`work-log-template.md` | 8k |
| handoff.compose | `workflows/handoff.yaml` compose 块 + 协作 §3.0～§3.0.1 + `handoff-note-template.md` + 台账 | 专模（PRD/开发交接等） | 6k |
| handoff.status / send / receive / change_send / change_receive / replan | `workflows/handoff.yaml` 当前 step 块 + 协作当前节；**send** 另加交接包说明/清单 + 台账/计划 | 接收回执模板、文档治理 §3、变更单 | 8k |
| showcase.audience / story / demo / environment / materials / docs / dryrun / publish | `workflows/showcase.yaml` 当前 step 块 + 技能 `demo-storytelling` / `product-docs` / `presentation-design` + 展示模板 | product-profile.md/计划/PRD/原型 | 8k |
| onboard.* | `workflows/onboard.yaml` 当前 step 块 + `agents/onboard-agent.yaml` + `rules/doc-governance.md` 当前节（§2.4 起） | `rules/templates/00-onboarding/capabilities/`/`rules/capabilities/instance-discipline.md`、`work-log-template.md` | 8k |
| skill-audit.* | `workflows/skill-audit.yaml` 当前 step 块 + `agents/onboard-agent.yaml` + `rules/playbooks/skill-audit.md` 当前节（discover 必读 §2.1） | `{workroot}/capabilities/00-能力清单.md`、包内契约/参考目录、`skills/README.md`、`capability-skill-audit-report-template.md`；按范围抽查 SKILL；discover 时 skills.sh / `npx skills find` | 8k |
| commit | `closeout-skeleton.md` §0/§1（通用占位）+ `workflow.md` §3；有门产物读 `.gate/wf-product/{mode}.json` | git 状态 | 5k |
| wrap | `closeout-skeleton.md` §0/§1 + `context-memory.md` §4；有门产物读 gate JSON；无门写自检结论 | 产品计划 §0/§7/§10、activeContext | 5k |
| materials.* | `workflows/materials.yaml` 当前 step 块 + `rules/doc-governance.md` §5.2 + `docs/materials/INDEX.md` + `{workroot}` 当前定稿 | 版本 README/域目录/来源 | 6k |

## 读取纪律

- 先读标题/目录/当前节；不要从第一行读到最后一行。
- 同一文件只读一次；后续步骤用 delta-only。
- 需要跨文件综合时，先列“要回答的问题”，再定向 grep/读节；不要用“通读”代替定位。
- 子代理只读派发路径与节选，不读整本rules/档案/历史。
- 任何澄清/追问 → `rules/core/clarification.md`；客户需求发现 → `skills/customer-needs-discovery/SKILL.md`；竞品分析/对标/学习模仿 → `skills/competitive-intelligence-and-learning/SKILL.md`；不另造提问格式。
