# 模板索引（产品轨）

> 用途：按 step 找模板，避免“模板存在但没人用”。只读当前 step 需要的一行；不要通读。
> 模板按生命周期分组存放在 `rules/templates/`；下表路径相对 `rules/templates/`。
> **质量门槛**：模板只提供结构；产出必须过 `rules/core/doc-quality.md` 的定位/类型矩阵/评审清单，结构完整≠合格。

## 00-onboarding

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `00-onboarding/workspace-index-template.md` | onboard.profile | `{workroot}/INDEX.md`（工作区导航；单包即 `docs/INDEX.md`） |
| `00-onboarding/project-overview-index-template.md` | onboard.profile（多包 / 保留原目录） | `docs/INDEX.md`（总览；不写状态） |
| `00-onboarding/inbound-index-template.md` | onboard.materials / 文档治理 | `inbound/INDEX.md`（全量原件登记） |
| `00-onboarding/materials-index-template.md` | materials.index | `docs/materials/INDEX.md`（项目级） |
| `00-onboarding/materials-version-readme-template.md` | materials.index | `docs/materials/{ver}/README.md` |
| `00-onboarding/product-profile-template.md` | onboard.profile | 项目根 `product-profile.md`；§3 内联产品规范要点 |
| `00-onboarding/project-readme-template.md` | onboard.profile / 点名生成·更新 README | 按用户偏好择块拼接（非定死大纲）；已有勿整文件覆盖；规则见 `rules/core/project-readme.md` |
| `00-onboarding/active-context-template.md` | onboard / 开工无文件时 | 项目根 `activeContext.md`（含 `### 进行中` 快照）；总览 + 进行中 ≤30 行 |
| `00-onboarding/root-agents-pointer.md` | onboard.mount | 项目根 AGENTS 包挂载样例（偏好正文由项目自写） |
| `00-onboarding/wf-agents-routing-template.md` | onboard.mount（多包） | `wf/AGENTS.md` 路由；只列已装包 |
| `00-onboarding/work-log-template.md` | onboard / deliver.release / plan.publish | `{workroot}/work-log.md`：岗位里程碑（含接入/治理）；禁止改根 CHANGELOG |
| `00-onboarding/capability-skill-audit-report-template.md` | skill-audit.propose | `{workroot}/00-governance/能力技能体检-{yyyyMMdd}.md`（工作产物，不进资料区） |
| `00-onboarding/capabilities/00-capability-inventory.md` | onboard.capabilities | 实例 SSOT 模板：复制到 `{workroot}/capabilities/00-能力清单.md`；绑定按需 `{workroot}/capabilities/绑定/{slot}.md` |

## 10-planning

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `10-planning/product-plan-template.md` | plan.publish | `{workroot}/product-plan.md` 常青主档（含 §3.0 Brief+Delta） |
| `10-planning/iteration-plan-template.md` | plan.publish / prd.prd（多需求版本） | 版本级迭代方案：范围、功能覆盖、验收矩阵、执行记录、发布条件；验收资产 ≠ 开发任务 |
| `10-planning/iteration-change-summary-template.md` | plan.scope / publish（按需） | 默认用计划 §3.0；仅仓外/版本归档/点名才落独立文件为唯一权威 |
| `10-planning/requirement-pool-template.md` | prd.discover / change.new_requirement | `{workroot}/requirement-pool.md`（含证据/方案/确认列） |
| `10-planning/interview-guide-template.md` | prd.discover / new-product.discover | 正式访谈问题单（Mom Test） |
| `10-planning/insight-synthesis-template.md` | prd.discover / new-product.discover | 访谈/工单/数据综合一页纸（含竞品学习摘要） |
| `10-planning/competitor-analysis-template.md` | prd.discover / new-product.discover | 模式 S：选择性学习（借/改编/不借） |
| `10-planning/competitive-benchmark-template.md` | prd.benchmark | 模式 P：功能/能力对标矩阵 → 候选项 |
| `10-planning/business-case-template.md` | new-product.discover / go | 0→1 机会评估（含方案要点/双确认/竞品学习） |
| `10-planning/prd-template.md` | prd.prd（P2/P3） | 全量 PRD；P0/P1 用 `prd-lite-template.md` |
| `10-planning/prd-lite-template.md` | prd.prd（P0/P1） | 单页/≤3 AC；不省 AC/排除/风险 |

## 20-design

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `20-design/design-review-template.md` | prototype.review | 12 项评分卡 |
| `20-design/prototype-coverage.md` | prototype.review / prd.prototype | PRD F/A/AC → 页面/路由/状态/交互/字段 → 截图证据矩阵 |
| `20-design/prototype-spec-template.md` | prototype.context / wireframe | 小项目可合并单文件 |
| `20-design/dev-handoff-template.md` | prototype.handoff | 设计意图/必须保留/可优化/未提供/验收对照 |
| `20-design/prototype-engineering-checklist-template.md` | prototype.engineering | 路由/状态/响应式/a11y/打印 |
| `20-design/usability-review-template.md` | prototype.usability | 3～5 关键任务/Nielsen 10 |
| `20-design/prototype-scaffold.html` | prototype.wireframe / hi-fi | 离线、无依赖起步 |

## 30-review-change

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `30-review-change/review-record-template.md` | prd.review / change.review | 独立评审记录 |
| `30-review-change/intake-disposition-template.md` | change.intake / defect.pull | 受理单/分诊/影响/联动/验证 |
| `30-review-change/change-request-template.md` | change.assess / decide | 改动已定稿基线时（含 §2.1 Now→Proposed 差量表） |
| `30-review-change/product-defect-disposition-template.md` | defect.apply | 产品缺陷处置单 |
| `30-review-change/defect-writeup-template.md` | defect.writeback / 缺陷处置 | 平台备注/附件/状态/指派文案骨架 |

## 40-delivery

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `40-delivery/delivery-plan-template.md` | deliver.schedule | 范围/里程碑/发布窗口 |
| `40-delivery/uat-acceptance-template.md` | deliver.uat | **业务签收 SSOT**；逐条 AC 对照（≠ 开发工程侧 UAT） |
| `40-delivery/gtm-template.md` | new-product.launch / deliver.release | 定价/渠道/物料/客服 |

## 50-showcase-docs

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `50-showcase-docs/demo-script-template.md` | showcase.audience / story / demo | 展示需求/故事线/脚本 |
| `50-showcase-docs/demo-checklist-template.md` | showcase.environment | 构建/账号/seed/网络/兜底 |
| `50-showcase-docs/one-pager-deck-outline-template.md` | showcase.materials | 一页纸/Deck 大纲 |
| `50-showcase-docs/user-manual-quickstart-template.md` | showcase.docs | 用户文档 |
| `50-showcase-docs/release-notes-template.md` | showcase.docs / deliver.release | **客户版**发布说明（≠ 开发工程/部署发布说明） |
| `50-showcase-docs/feedback-log-template.md` | showcase.dryrun | 彩排反馈/异议/需求 |

## 60-retro

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `60-retro/retro-template.md` | deliver.release | 目标 vs 实际/根因/行动项 |

## 90-handoff

| 模板 | 用于 step | 说明 |
| --- | --- | --- |
| `90-handoff/closeout-skeleton.md` | wrap / 工作流末步 / 工作总结口令 | 【任务收尾】/【今日工作总结】固定骨架；工作总结须围栏外 `范围：from～to` + 读/写 activeContext 本包锚点 |
| `90-handoff/handoff-note-template.md` | **handoff.compose（默认）** | **择优写法**（五问→A/B/C/D）；非填空卷；禁整表套用、禁外印元数据 |
| `90-handoff/handoff-package-brief-template.md` | handoff.send（仅升包） / prd.handoff / prototype.handoff | `{workroot}/handoff/outbound/{category}/{HO-ID}/00-交接说明.md` |
| `90-handoff/handoff-checklist-template.md` | handoff.send | `01-交接清单.md`（包内文件/版本/必读） |
| `90-handoff/receipt-template.md` | handoff.receive / 签收 | `04-回执/接收回执.md`（接受/有条件/退回） |
| `90-handoff/handoff-ledger-template.md` | handoff.status / 交接初始化 | `{workroot}/handoff/handoff-ledger.md`（唯一登记） |
