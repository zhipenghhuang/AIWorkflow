# 模板索引（测试轨）

> 用途：按 step 找模板；只读当前 step 需要的一行，不要通读。
> 模板按生命周期分组存放在 `rules/templates/`；下表路径相对 `rules/templates/`。

## 00-onboarding

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `00-onboarding/workspace-index-template.md` | onboard.context | `{workroot}/INDEX.md`（工作区导航） |
| `00-onboarding/project-overview-index-template.md` | onboard.context（多包） | `docs/INDEX.md`（总览） |
| `00-onboarding/inbound-index-template.md` | onboard.materials | `inbound/INDEX.md` |
| `00-onboarding/materials-index-template.md` | materials.index | `docs/materials/INDEX.md` |
| `00-onboarding/materials-version-readme-template.md` | materials.index | `docs/materials/{ver}/README.md` |
| `00-onboarding/env-baseline-template.md` | onboard.baseline | 环境/账号/数据基线 |
| `00-onboarding/env-baseline-minimal.md` | onboard.baseline | 接入最小集 |
| `00-onboarding/project-readme-template.md` | onboard.baseline / README | 项目 README |
| `00-onboarding/active-context-template.md` | onboard.context | `activeContext.md` |
| `00-onboarding/root-agents-pointer.md` | onboard.baseline | 根 AGENTS 挂载样例 |
| `00-onboarding/wf-agents-routing-template.md` | onboard.baseline（多包） | `wf/AGENTS.md` 路由 |
| `00-onboarding/work-log-template.md` | onboard / report | `{workroot}/work-log.md` |
| `00-onboarding/capabilities/00-capability-inventory.md` | onboard.capabilities | 能力清单模板 |
| `00-onboarding/capability-skill-audit-report-template.md` | skill-audit.propose | 体检报告 |

## 10-planning

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `10-planning/test-analysis-template.md` | testing.plan（必做） | 来源/章节/依据/AC 设计点/意图/覆盖矩阵/方法矩阵/D01–D13+S6/S7/S11/风险/影响面/核心链路；落 `{workroot}/{ver}/test-analysis.md` |
| `10-planning/test-plan-template.md` | testing.plan（总排） | 范围/引用分析/影响面/核心链路摘要/轨道/轮次/批次/探索/准入准出；落 `{workroot}/{ver}/test-plan.md` |
| `10-planning/test-plan-lite-template.md` | testing.plan（补丁/单模块） | 轻量总排；分析仍必做 |
| `10-planning/user-facing-change-notes-template.md` | testing.plan / 用户点名 | 用户可读变化说明；按需 |

## 20-test-cases

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `20-test-cases/test-case-template.md` | testing.execute（功能） | 执行记录：场景+步骤+Oracle+结果+证据+缺陷 |
| `20-test-cases/api-test-case-template.md` | testing.execute（接口） | 接口执行记录：契约清单+适用维+请求+判定+证据 |
| `20-test-cases/exploratory-case-template.md` | testing.execute（探索式） | 一场一句+会话记录 |
| `20-test-cases/random-flow-case-template.md` | testing.execute（随机·计划外） | 旅程会话+去重窗+分流 |
| `20-test-cases/a11y-ux-checklist.md` | testing.execute / report（按需） | 无障碍/UX 检查 |

## 30-execution

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `30-execution/test-change-record-template.md` | testing.plan（期中变更） | CR + 影响分析 |
| `30-execution/stable-smoke-checklist-template.md` | testing.execute / report | P0 冒烟 + 高价值锚点 |
| `30-execution/special-index-template.md` | special/发布前索引 | 人工追踪 |
| `30-execution/defect-writeup-template.md` | defect.submit / 回写 | 平台备注/附件/状态/指派 |

## 40-report-review

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `40-report-review/test-report-template.md` | testing.report | 结论/意图覆盖/缺陷/缺口/发布建议 |

## 90-handoff

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `90-handoff/closeout-skeleton.md` | report / closeout / 末步 | 【任务收尾】/【执行收尾】/工作总结 |
| `90-handoff/handoff-note-template.md` | handoff.compose | 交接说明 |
| `90-handoff/handoff-package-brief-template.md` | handoff.send | 升包说明 |
| `90-handoff/handoff-checklist-template.md` | handoff.send | 包内清单 |
| `90-handoff/receipt-template.md` | handoff.receive | 接收回执 |
| `90-handoff/handoff-ledger-template.md` | 交接初始化 / 状态只读 | 交接台账 |
| `90-handoff/defect-handoff-detail-template.md` | handoff.send（BUG） | 缺陷详单 |
