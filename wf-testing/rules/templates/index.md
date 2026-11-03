# 模板索引（测试轨）

> 用途：按 step 找模板，避免“模板存在但没人用”。只读当前 step 需要的一行；不要通读。
> 模板按生命周期分组存放在 `rules/templates/`；下表路径相对 `rules/templates/`。
> **质量门槛**：模板只提供结构；产出必须过 `rules/core/doc-quality.md` 的定位/类型矩阵/评审清单，结构完整≠合格。

## 00-onboarding

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `00-onboarding/workspace-index-template.md` | onboard.docs | `{workroot}/INDEX.md`（工作区导航；单包即 `docs/INDEX.md`） |
| `00-onboarding/project-overview-index-template.md` | onboard.docs（多包 / 保留原目录） | `docs/INDEX.md`（总览；不写状态） |
| `00-onboarding/inbound-index-template.md` | onboard.materials / 文档治理 | `inbound/INDEX.md`（全量原件登记） |
| `00-onboarding/materials-index-template.md` | materials.publish | `docs/materials/INDEX.md`（项目级） |
| `00-onboarding/materials-version-readme-template.md` | materials.publish | `docs/materials/{ver}/README.md` |
| `00-onboarding/env-baseline-template.md` | onboard.baseline | 只强制 §1/§2.1/§2.2/§8；其余按需 |
| `00-onboarding/project-readme-template.md` | onboard.baseline / 点名生成·更新 README | 按用户偏好择块拼接（非定死大纲）；已有勿整文件覆盖；规则见 `rules/core/project-readme.md` |
| `00-onboarding/env-baseline-minimal.md` | onboard.baseline | 接入最小集；完整模板按需 |
| `00-onboarding/active-context-template.md` | onboard.context / 开工无文件时 | 项目根 `activeContext.md`（含 `### 进行中` 快照） |
| `00-onboarding/root-agents-pointer.md` | onboard.baseline | 项目根 AGENTS 包挂载样例（偏好正文由项目自写） |
| `00-onboarding/wf-agents-routing-template.md` | onboard.baseline（多包） | `wf/AGENTS.md` 路由；只列已装包 |
| `00-onboarding/work-log-template.md` | onboard / testing.report | `{workroot}/work-log.md`：岗位里程碑（含接入/治理）；禁止改根 CHANGELOG |
| `00-onboarding/capabilities/00-capability-inventory.md` | onboard.capabilities / 接入 | 实例 SSOT 模板：复制到 `{workroot}/capabilities/00-能力清单.md`；绑定按需 `绑定/{slot}.md`（模板 `00-onboarding/capabilities/bindings/browser-automation.md`） |
| `00-onboarding/capability-skill-audit-report-template.md` | skill-audit.propose | `{workroot}/changes/能力技能体检-{yyyyMMdd}.md`（工作产物，不进资料区） |

## 10-planning

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `10-planning/test-plan-lite-template.md` | testing.plan（T0/T1） | 范围/类型/执行矩阵/准出/风险 |
| `10-planning/test-plan-template.md` | testing.plan（版本级） | 完整模板（§0～§18）；小任务用轻量节 |
| `10-planning/test-plan-volume-template.md` | testing.plan（版本级固定四卷） | V1 主链/V2 功能/V3 方法/V4 收口；复用主计划与分析表验证点；不适用写 N/A |
| `10-planning/test-analysis-template.md` | testing.analyze（必出） | 跨轨共用；落 `{workroot}/test-analysis.md`；功能双读全表，接口/发布前至少读 §0 |
| `10-planning/user-facing-change-notes-template.md` | testing.analyze | 用户可读变化说明；AI 业务全景索引；T1+ 用户可见变化必出 |

## 20-test-cases

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `20-test-cases/test-case-template.md` | testing.generate（功能） | 模块总览+结构化详情+评分卡 |
| `20-test-cases/api-test-case-template.md` | testing.generate/execute（接口） | 契约表+覆盖对照+用例详情+脚本清单；机检 `validate_api_testcase.py` |
| `20-test-cases/exploratory-case-template.md` | testing.generate/execute（探索式） | 章程映射+步骤四列+判定面；同戳台账 |
| `20-test-cases/random-flow-case-template.md` | testing.generate/execute（随机业务流程·计划外） | 旅程会话+去重窗+发现分流；不进准出 |
| `20-test-cases/a11y-ux-checklist.md` | testing.report / 走查 | 结果并入报告 §11 |

## 30-execution

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `30-execution/execution-ledger-template.md` | testing.execute | `*-功能台账.md` / `*-接口台账.md`；本轮装填 + 未本轮验证 |
| `30-execution/test-change-record-template.md` | testing.plan（期中变更） | CR + 影响分析 |
| `30-execution/stable-smoke-checklist-template.md` | testing.generate/execute | P0-Smoke 脚本清单 |
| `30-execution/special-index-template.md` | special/发布前索引 | 供人工追踪，不阻断执行 |
| `30-execution/defect-writeup-template.md` | defect.submit / 缺陷回写 | 平台备注/附件/状态/指派文案骨架 |

## 40-report-review

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `40-report-review/test-report-template.md` | testing.report | 计划对照/准出/遗留 |
| `40-report-review/review-record-template.md` | testing.review-cases | 本轮批次/合卷；量规 + 严重度缺口 + 放行/需修 |

## 90-handoff

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `90-handoff/closeout-skeleton.md` | report / wrap / 工作流末步 / 工作总结口令 | 【任务收尾】/【生成收尾】/【执行收尾】/【今日工作总结】；工作总结须围栏外 `范围：from～to` + 读/写 activeContext 本包锚点 |
| `90-handoff/handoff-note-template.md` | **handoff.compose（默认）** | **择优写法**（五问→A/B/C/D）；非填空卷；禁整表套用、禁外印元数据 |
| `90-handoff/handoff-package-brief-template.md` | handoff.send（仅升包） / testing.report | `{workroot}/handoff/outbound/{category}/{HO-ID}/00-交接说明.md` |
| `90-handoff/handoff-checklist-template.md` | handoff.send | `01-交接清单.md`（包内文件/版本/必读） |
| `90-handoff/receipt-template.md` | handoff.receive / 签收 | `04-回执/接收回执.md`（接受/有条件/退回） |
| `90-handoff/handoff-ledger-template.md` | handoff.status / 交接初始化 | `{workroot}/handoff/handoff-ledger.md`（唯一登记） |
| `90-handoff/defect-handoff-detail-template.md` | handoff.send（BUG，无平台/点名） | `02-文档/缺陷详单.md`（十段齐；不依赖平台号） |
