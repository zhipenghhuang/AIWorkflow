# 读取索引（开发轨）

> **单一读取入口**：只读本表当前 step 行的「必读」列，按需再读「可选」；**不要通读整本 rules / skills / templates**。
> **rule_anchor**：本表**当前行**即方法层锚点；切 step 时重读本行（不必重读 AGENTS §0 全文）。step `notes` 的「技能：…」/`skills_required` 与映射冲突时以 YAML 为准。
> **中段重锚**：同会话已路由后按 `rules/core/rule-anchor.md` 心跳；不借心跳通读本索引全表。
> **读取预算（目标，非硬上限）**：核心 ≤3～4 个来源（命中才读）+ ≤8k tokens；复杂可至 5；大文件只读当前 step 对应节，**workflow 只读当前 step 块（当前 `- name:` 到下一个）**；确需更多时只读当前节并在收尾说明，不得为省预算跳过门/证据。
> **语义核心**：新会话可含 `AGENTS.md` §0；中段默认 = workflow 当前 step 块 + 当前 agent + 当前产物/证据；skills / playbook/模板 = **命中才读**。
> **读序（新会话）**：① `AGENTS.md` §0（硬节）→ ② workflow 当前 step 块 → ③ 本索引当前行 → ④ 当前 agent → ⑤ 当前skills / playbook 当前节 → ⑥ 当前产物/证据。**同会话中段**：心跳 → ②③④⑥。**口令表仅路由未定/首次命中时读**。
> 同一会话文件未变不重读；后续步骤 delta-only。
> **执行契约**：开工判定见 `rules/core/execution-contract.md` §1～§2/§6；心跳见 §7 / `rule-anchor.md`；不占每步常规预算。

## 默认行（所有 step）

- **核心必读（≤4 来源）**：`AGENTS.md` §0 · 命中 `workflows/{workflow}.yaml` 当前 step 块 · 当前 `agents/{role}.yaml` · 当前产物/证据（顺序见上方「读序」）。
- **定位（不计入必读）**：工作根、接入级别、索引口径只认 `rules/doc-governance.md` §2.4/§2.5；入口/材料包看 `{workroot}/INDEX.md`；跨会话快照看项目根 `activeContext.md` 总览 + 本包 `### 进行中`；项目身份见 `project-profile.md` §1 + §2 表（`AGENTS.md` §0 已列）。
- **命中才读**：本索引对应行「可选」列；方法层 skills / playbook / 模板按 step 命中再读。
- 不读：其它 workflow、全部 agents、全部模板、全本规则。

> 模板引用若用短名（如“产品计划模板”“测试报告模板”），先按 `rules/templates/index.md` 定位到组；不要猜路径。

## 按 step

> 行内 `workflow.step` 为定位项；`/` 分隔并列项（可跨 workflow）；`workflow.*` = 该 workflow 全部 step。

| step | 必读 | 可选 | 预算 |
| --- | --- | ---: | ---: |
| 工作总结口令（无 workflow） | `rules/templates/90-handoff/closeout-skeleton.md` §3（含围栏外 `范围：from～to`）+ 项目根 `activeContext.md` 本包「工作总结锚点」 | git 日志/工作日志/本轮任务收尾（仅区间内） | 6k |
| 无口令/意图不明 | `rules/core/routing.md` §0～§6（五元组/意图类/状态/首条/资料不足升级）+ project-profile.md §1/§7/§8 | 附录校验、开发计划、 `{workroot}/INDEX.md` | 5k |
| control.init / run / sync / check / next | `workflows/control.yaml` 当前 step 块 + 技能 `development-plan` 当前节 + 开发计划现状；有 PRD/原型时 + 技能 `product-doc-analysis`；版本/发布阶段 + `rules/core/versioning.md` §4～§5 | 开发计划模板、根 `changelog-template.md`、`work-log-template.md`、validate_dev_plan | 8k |
| change.clarify | `workflows/change.yaml` 当前 step 块 + `rules/core/clarification.md` §1/§1.1～§5 + 技能 `requirements-and-spec` §1 + project-profile.md §2/§8 | 代码地图 | 7k |
| change.analyze_input | `workflows/change.yaml` 当前 step 块 + `rules/core/clarification.md` §1.1/§2～§5 + 技能 `product-doc-analysis` + 需求理解包模板 §0 + **用户版业务变化说明模板** + 输入文档/原型 + 需求台账；有产品 Delta 则引用 | 代码地图、项目计划、产品迭代变更摘要 | 8k |
| change.requirements | 技能 `requirements-and-spec` + 需求基线模板 + 需求台账 + 需求理解包 + **用户版说明（如有）**；`cross-layer-consistency`（命中权限/状态/数据基数/多表面时） | PRD/需求文档（可选输入） | 8k |
| change.design | 技能 `solution-design` + 方案模板；`engineering-quality`（命中风险/质量条时）+ `cross-layer-consistency`（命中时）+ ADR（有架构决策时）；子技能按变更面命中再读 | `frontend-design-spec-template.md`；命中面再读 `api-design` / `database-design` / `frontend-implementation` / `threat-modeling` / 性能/可观测/AI 子技能 | 8k |
| change.plan / iterate.plan | 技能 `task-breakdown` + 任务清单模板（L1 可 `dev-card-lite-template.md`）；**用户版说明（如有）**；`rules/core/implementation-quality.md`（SC/债项/**DEV-IQ-12 抽全**/矩阵门）+ `cross-layer-consistency`（四维矩阵，命中时）+ `rules/playbooks/iterate.md`（iterate 时）；标记 `[P]` 时 + `rules/collaboration/subagents.md` §2/§5 | 代码地图 scout | 8k |
| change.implement / iterate.implement | 技能 `implementation-and-selftest`（含 §0.5 预检）+ 任务清单 + project-profile.md §2/§7；`rules/core/implementation-quality.md` **§3～§4（DEV-IQ-09/10/12；有开关时 +DEV-IQ-11）** + `engineering-quality`；`cross-layer-consistency`（命中时）；失败时 + `debugging-and-error-recovery`；AI 变更 + `ai-application-engineering`；**分片/拆分时 + `rules/collaboration/subagents.md` §1/§3/§6/§7** | 预检命中面再读 threat/perf/observability 当前节；前后端子技能、`前端设计说明` | 8k |
| change.review-docs | 技能 `design-doc-review` + doc-reviewer + 被审方案/基线/ADR；`engineering-quality` §5（命中评审轴时） | solution-design 当前节 | 8k |
| change.review / iterate.review | 技能 `code-review`（含 §4.0 AC+SC / 原文抽核）+ reviewer-agent + diff；先判 `review_required`；评审范围=门禁 diff；`engineering-quality` §5 / `cross-layer-consistency`（命中时）；**独立核验/维度扇出时 + `rules/collaboration/subagents.md` §7/§8** | 任务卡 SC、理解包§0（L2+ 有则）、security-scan、design-review | 8k |
| change.verify / iterate.gates | `verify/README.md` + `rules/core/verification.md` + `verify/checks.yaml` + 验收清单/diff/证据；取重或有行为时 + `rules/core/implementation-quality.md` §8（含 implement_preflight） | `.gate/wf-development/completion.json`、日志摘要 | 6k |
| change.deliver / iterate.deliver | 技能 `qa-handoff-and-release` + 提测/发布模板；`rules/core/implementation-quality.md` §6～§7（债项/基线再验；有开关时 +DEV-IQ-11）+ `rules/core/versioning.md` §3～§7；有代码改动时 + 本轮 `.gate/wf-development/completion.json` | 发布说明/回滚预案 | 8k |
| change.release_handoff / iterate.release_handoff | `workflows/change.yaml` 或 `iterate.yaml` 当前 step 块 + 技能 `qa-handoff-and-release` / `acceptance-and-launch` 当前节 + `rules/core/versioning.md` §5～§7 | 提测/发布/上线检查单 | 8k |
| change.wrap / control.wrap / intake.wrap / handoff.wrap / release.wrap / retro.wrap / defect-fix.wrap | `rules/templates/90-handoff/closeout-skeleton.md` §0/§0.5/§2（中文回执、遵守自检）；命中版本 bump/关迭代/发版/对外事实变时 + `rules/core/doc-facade-sync.md` | {workroot}/INDEX.md / activeContext/根 `CHANGELOG.md`/`{workroot}/work-log.md` | 6k |
| handoff.compose | `workflows/handoff.yaml` compose 块 + 协作 §3.0～§3.0.1 + `handoff-note-template.md` + 台账 | 专模（提测单等） | 6k |
| handoff.status / send / receive / change_send / change_receive / replan | `workflows/handoff.yaml` 当前 step 块 + 协作当前节；**send** 另加交接包说明/清单模板 + 台账/计划 | 接收回执模板、提测/发布模板 | 8k |
| change.commit / iterate.commit / control.commit / intake.commit / retro.commit / handoff.commit / release.commit / iterate.wrap | `rules/templates/90-handoff/closeout-skeleton.md` §0/§0.5/§2（中文回执、第4点待确认） + `rules/workflow.md` §2；有门回执时 + 本轮 `.gate/wf-development/completion.json` | git 状态、`{workroot}/INDEX.md` / 根 `CHANGELOG.md`/`{workroot}/work-log.md` | 6k |
| solo.frame | `workflows/solo.yaml` 当前 step 块 + `rules/core/lightweight.md` §0～§3.1 + 技能 `product-shaping` + 产品定义卡模板 + project-profile.md §2/§8 | 需求/PRD（可选） | 6k |
| solo.plan | `workflows/solo.yaml` 当前 step 块 + `rules/core/lightweight.md` §0/§2～§5 + 技能 `product-shaping`/`solution-design`/`task-breakdown` + 方案卡模板；`engineering-quality`（命中风险/质量条时读当前节） | 需求基线/方案templates/代码地图 | 7k |
| solo.build | 技能 `implementation-and-selftest`（§0.5 预检）+ `engineering-quality` + 方案卡 + project-profile.md §2/§7；`implementation-quality.md` §3～§4（有行为时，含 DEV-IQ-12）；失败时 + `debugging-and-error-recovery` | 预检命中面技能当前节；前后端子技能、前端设计说明 | 8k |
| solo.test | `workflows/solo.yaml` 当前 step 块 + `rules/core/lightweight.md` §4 + 技能 `test-design-and-execution` + `verify/README.md` + `verify/checks.yaml` + 方案卡/验收清单 | 轻量测试报告模板、本轮 `.gate/wf-development/completion.json` | 7k |
| solo.wrap / solo.commit | `rules/templates/90-handoff/closeout-skeleton.md` §0/§0.5/§2 + `rules/workflow.md` §2；有门回执时 + 本轮 `.gate/wf-development/completion.json` | {workroot}/INDEX.md / activeContext/根 `CHANGELOG.md`/`{workroot}/work-log.md` | 6k |
| iterate.precheck / confirm / release_handoff / retro | `workflows/iterate.yaml` 当前 step 块 + `rules/playbooks/iterate.md` 当前节 | 开发计划/复盘模板 | 8k |
| defect-fix.preflight / pull / triage / gates / menu | `workflows/defect-fix.yaml` 当前 step 块 + `rules/playbooks/defect.md` 当前行 + `rules/defects/fix-collaboration.md` 当前节 | 平台时→`platform-adapter.md`；gates→`verify/README.md`；产品缺陷→评估模板 | 8k |
| defect-fix.fix | `workflows/defect-fix.yaml` fix 块 + `rules/defects/fix-collaboration.md` §4.4/§4.5 + `rules/core/implementation-quality.md` §3～§4（DEV-IQ-09/10/12；有代码时）+ `skills/implementation-and-selftest` §0.5 | 跨层命中→`cross-layer-consistency` §5；复杂实施→方案模板；失败→`debugging-and-error-recovery` | 8k |
| defect-fix.close | `workflows/defect-fix.yaml` close 块 + `rules/defects/fix-collaboration.md` §4.5/§6 + `rules/templates/40-delivery/defect-writeup-template.md` §6.0/§6.1/§6.9/§6.10 + `rules/core/verification.md` §3～§4 + 部署/冒烟/复核证据 | 平台时→`platform-adapter.md`；发布说明/回滚/上线检查单 | 8k |
| defect-fix.postrelease | `workflows/defect-fix.yaml` postrelease 块 + 发布说明/发布记录模板 | 监控/日志、复盘模板 | 6k |
| defect-fix.await_product / assess_product / handoff_product / product_decision / align / clarify | `rules/playbooks/defect.md` 对应节 + `rules/defects/fix-collaboration.md` §5 当前节 | 写回时→缺陷文案模板 §6；产品新文档/附件 | 8k |
| defect-fix.retro | 同 `retro.gather…`；`workflows/defect-fix.yaml` retro 步 notes | 本轮缺陷事实材料 | 6k |
| release.readiness / acceptance / approval / deploy / verify / rollback / postrelease / record / retro | `workflows/release.yaml` 当前 step 块 + `rules/playbooks/release.md` + 技能 `acceptance-and-launch` 当前节 + `observability-and-instrumentation`（SLO/告警）+ `rules/core/versioning.md` §5～§7；record/wrap 命中时 + `rules/core/doc-facade-sync.md`；`retro` 同复盘技能当前节 | 上线检查单/发布记录/复盘模板 | 8k |
| retro.gather / analyze / actions / record | 技能 `retrospective-and-improvement` + 复盘模板 + 事实材料 | 上次行动项 | 8k |
| onboard.* | `workflows/onboard.yaml` 当前 step 块 + `agents/onboard-agent.yaml` + `rules/doc-governance.md` 当前节（§2.4 起）+ `rules/core/versioning.md` §1～§2 | `rules/templates/00-onboarding/capabilities/`/`rules/capabilities/instance-discipline.md`/根 `changelog-template.md`/`work-log-template.md`/`version-policy-template.md` | 8k |
| skill-audit.* | `workflows/skill-audit.yaml` 当前 step 块 + `agents/onboard-agent.yaml` + `rules/playbooks/skill-audit.md` 当前节（discover 必读 §2.1） | `{workroot}/capabilities/00-能力清单.md`、包内契约/参考目录、`skills/README.md`、`capability-skill-audit-report-template.md`；按范围抽查 SKILL；discover 时 skills.sh / `npx skills find` | 8k |
| intake.scan / classify / parse / impact / absorb / report | `workflows/intake.yaml` 当前 step 块 + 技能 `change-intake` + `skills/product-doc-analysis`（有 PRD/原型/文档时）+ 需求台账/变更记录 | 文档治理 §3～§4 入站意图+同批归档 | 8k |
| materials.* | `workflows/materials.yaml` 当前 step 块 + `rules/doc-governance.md` §5.2 + `docs/materials/INDEX.md` + `{workroot}` 当前定稿 | 版本 README/域目录/来源 | 6k |

## 读取纪律

- 先读标题/目录/当前节；不要从第一行读到最后一行。
- 同一文件只读一次；后续步骤用 delta-only。
- 需要跨文件综合时，先列“要回答的问题”，再定向 grep/读节；不要用“通读”代替定位。
- 子代理只读派发路径与节选，不读整本rules/档案/历史。
- 任何澄清/追问 → `rules/core/clarification.md`（不确定项先 §1.1 标 P/D/S）；产品文档/原型解析 → `skills/product-doc-analysis/SKILL.md`；不另造提问格式。
