# 模板索引（开发轨）

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
| `00-onboarding/project-profile-template.md` | onboard.profile | 项目根 `project-profile.md` |
| `00-onboarding/project-readme-template.md` | onboard.profile / 点名生成·更新 README | 按用户偏好择块拼接（非定死大纲）；已有勿整文件覆盖；规则见 `rules/core/project-readme.md` |
| `00-onboarding/version-policy-template.md` | onboard.profile / control.init | 项目级版本口径一页（版本格式/升级/环境/tag/审批） |
| `00-onboarding/active-context-template.md` | onboard / 开工无文件时 | 项目根 `activeContext.md`（含 `### 进行中` 快照） |
| `00-onboarding/root-agents-pointer.md` | onboard.mount | 项目根 AGENTS 包挂载样例（偏好正文由项目自写） |
| `00-onboarding/wf-agents-routing-template.md` | onboard.mount（多包） | `wf/AGENTS.md` 路由；只列已装包 |
| `00-onboarding/changelog-template.md` | onboard.docs / control.wrap / release.record | 项目根 `CHANGELOG.md`：产品发版史（用户可见capabilities/破坏性/迁移/安全；开发维护） |
| `00-onboarding/work-log-template.md` | onboard.docs / control.wrap / release.record | `{workroot}/work-log.md`：岗位里程碑（含接入/治理）；不写进根 CHANGELOG |
| `00-onboarding/capability-skill-audit-report-template.md` | skill-audit.propose | `{workroot}/00-governance/能力技能体检-{yyyyMMdd}.md`（工作产物，不进资料区） |
| `00-onboarding/capabilities/00-capability-inventory.md` | onboard.capabilities | 实例 SSOT 模板：复制到 `{workroot}/capabilities/00-能力清单.md`；绑定按需 `{workroot}/capabilities/绑定/{slot}.md` |

## 10-planning

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `10-planning/development-plan-template.md` | control.init / onboard.control | L2+ 开发计划 |
| `10-planning/requirement-ledger-template.md` | onboard.docs / change.requirements | {workroot}/10-requirements/ |
| `10-planning/requirement-understanding-template.md` | change.analyze_input / intake.parse | §0 Brief+Delta 门面 + 下钻理解包 |
| `10-planning/user-facing-change-notes-template.md` | change.analyze_input | 用户可读变化说明；AI 业务全景索引；L1+ 用户可见变化必出 |
| `10-planning/requirement-baseline-template.md` | change.requirements | 需求/AC/NFR/非目标 |
| `10-planning/product-definition-card-template.md` | solo.frame | 一页产品定义：问题/用户/价值/MVP/非目标/成功标准/风险 |
| `10-planning/change-record-template.md` | {workroot}/00-governance/ | CR 留痕 |
| `10-planning/open-items-template.md` | {workroot}/00-governance/ | OPEN 跟踪 |
| `10-planning/decision-record-template.md` | {workroot}/00-governance/ | DEC 留痕 |
| `10-planning/change-absorption-report-template.md` | intake.report | 输入/影响/更新/待确认 |

## 20-design

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `20-design/solution-template.md` | change.design | 方案/接口/兼容/回滚 |
| `20-design/frontend-design-spec-template.md` | change.design（前端变更） | 页面/状态/tokens/a11y/性能/交接 |
| `20-design/frontend-prototype-parity-template.md` | change.design / implement（前端） | 原型对齐矩阵：路由/导航/复用组件/区块/状态；冲突与 OPEN 清单 |
| `20-design/adr-template.md` | change.design | 架构决策 |
| `20-design/product-defect-assessment-template.md` | defect-fix.assess_product | 只写评估，不写技术方案 |

## 30-planning-tasks

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `30-planning-tasks/task-list-template.md` | change.plan / iterate.plan | RP/AC/DoR/DoD |
| `30-planning-tasks/solution-card-template.md` | solo.plan | 一页方案卡：产品行为/技术/任务/验收/测试/风险 |
| `30-planning-tasks/dev-card-lite-template.md` | change.clarify / iterate.plan（L1） | 目标/AC/改动面/verify/回滚；L0 不用 |

## 40-delivery

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `40-delivery/qa-handoff-template.md` | change.deliver / iterate.deliver | **受众=测试转测**；环境就绪/开关当前值/可执行入口；禁 commit |
| `40-delivery/env-deployment-record-template.md` | S7 测试/预发/UAT 环境更新 | 非生产发布；版本保持 rc；部署/verify/回滚 |
| `40-delivery/release-notes-template.md` | change.deliver / release.record | **受众=工程部署**（非客户版）；审批/窗口/灰度/监控/回滚 |
| `40-delivery/go-live-checklist-template.md` | release.readiness | 硬项/NO-GO |
| `40-delivery/release-record-template.md` | release.record | 实际步骤/verify/观察 |
| `40-delivery/uat-acceptance-template.md` | release.acceptance | 逐条 AC |
| `40-delivery/lite-test-report-template.md` | solo.test | 轻量测试：范围/测试点/结果/证据/defects/缺口/verdict |
| `40-delivery/defect-writeup-template.md` | defect-fix.close / 缺陷处置 | 平台备注/附件/状态/指派文案骨架；**close 必读 §6.0/§6.1/§6.9/§6.10** |

## 60-retro

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `60-retro/retro-template.md` | release.retro / retro.record | 事实/根因/行动项 |

## 90-handoff

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `90-handoff/closeout-skeleton.md` | wrap / 工作流末步 / 工作总结口令 | 【任务收尾】/【今日工作总结】固定骨架；工作总结须围栏外 `范围：from～to` + 读/写 activeContext 本包锚点 |
| `90-handoff/handoff-note-template.md` | **handoff.compose（默认）** | **择优写法**（五问→A/B/C/D）；非填空卷；禁整表套用、禁外印元数据 |
| `90-handoff/handoff-package-brief-template.md` | handoff.send（仅升包） | `{workroot}/handoff/outbound/{category}/{HO-ID}/00-交接说明.md` |
| `90-handoff/handoff-checklist-template.md` | handoff.send | `01-交接清单.md`（包内文件/版本/必读） |
| `90-handoff/receipt-template.md` | handoff.receive / 正式签收时 | `04-回执/接收回执.md`（默认不强制填写） |
| `90-handoff/handoff-ledger-template.md` | handoff.status / 交接初始化 | `{workroot}/handoff/handoff-ledger.md`（唯一登记；含单文档发出） |
