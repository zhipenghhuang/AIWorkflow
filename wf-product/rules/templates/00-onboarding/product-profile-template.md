# {产品名} 产品档案

> 实例文件（随仓库入库）。凭据只写来源，不写原文。

## 1. 产品档案

| 项 | 填写 |
| --- | --- |
| 产品名称 | `{{产品名称}}` |
| 一句话定位 | `{{为谁解决什么问题}}` |
| 目标用户 | `{{核心用户/角色}}` |
| 成功指标 | `{{北极星指标 + 1～2 个辅助指标}}` |
| 版本/迭代节奏 | `{{双周/月/其它}}` |
| 流程偏好 | `{{轻量优先 / 完整优先；默认按计划与 PRD 存量推断}}`（影响入口；轻量≠降 AC/门/评审，见 `rules/core/routing.md` §3） |
| 负责人（我） | `{{姓名/账号}}` |
| 产品要点载体 | 本档案 §3（项目事实摘要）；对 AI 的额外要求由项目根 `AGENTS.md` 自写 |
| 文档分类 | `{workroot}/`：`product-plan.md`、`requirement-pool.md`、`work-log.md`、`00-governance/`、`user/`、`{ver}/10-requirements`、`{ver}/20-design`、`{ver}/30-changes`、`{ver}/40-delivery`、`{ver}/50-showcase`、`{ver}/90-retrospectives`、`handoff/`、`capabilities/`、`_archive/`；项目级权威文档库 `docs/materials/`（细则 `rules/doc-governance.md`） |
| workroot | 默认为 docs/；非标准时写实际路径 |
| integration_level | `{{I0 / I1 / I2 / I3；默认 I3}}` |
| inbound_structure | `{{keep / mix / replace；默认 mix}}` |
| 原件根 | `inbound/` + `INDEX.md`；`keep/mix/replace` 只整理原件结构；不迁出、不删除、不归档 |
| 权威文档库 | `docs/materials/`（项目级；定稿/完整/可发送；每版自包含；不设 `_archive`；旧版本保留） |
| 交接 | `{workroot}/handoff/outbound/{category}/` + `{workroot}/handoff/inbound/{category}/` + `handoff-ledger.md`；`inbound/` 为原件 |
| 资产入库范围 | `{{实例 / 模板 / 实例+模板 / 全不加入}}` |

## 2. 用户与场景

### 2.1 用户画像

| 角色 | 谁 | 核心诉求 | 使用频次 |
| --- | --- | --- | --- |
| `{{角色}}` | `{{…}}` | `{{…}}` | `{{高/中/低}}` |

### 2.2 核心场景（主链路）

1. `{{场景}}`：`{{触发 → 操作 → 结果}}`

### 2.3 术语与口径

| 术语 | 定义/口径 | 来源 |
| --- | --- | --- |
| `{{…}}` | `{{…}}` | `{{PRD/业务确认}}` |

## 3. 产品要点（事实摘要 · 内联）

> **定位**：本产品原则/范围/合规/体验的**事实摘要**，不是对 AI 的偏好指令；长期偏好与特殊要求由落地项目自写于根 `AGENTS.md`，短期/计划内偏好按 `rules/core/context-memory.md` 记入 `activeContext`。已有外部规范文档 → 写引用指针，要点仍汇总本节。

- 产品原则：`{{…}}`
- 范围边界：`{{做什么 / 不做什么}}`
- 合规与隐私：`{{…}}`
- 体验规范：`{{…}}`

## 4. 优先级与交付约定

- 优先级方法：`{{RICE / Kano / MoSCoW}}`；评分口径：`{{…}}`
- 版本节奏 / 发布窗口：`{{…}}`
- 变更规则：需求/问题/产品缺陷先走 `change` 受理单；改动已定稿基线才产生变更单；无变更单不实施；模板 `rules/templates/30-review-change/intake-disposition-template.md`、`rules/templates/30-review-change/change-request-template.md`
- UAT：按 PRD 验收标准逐条；发布门 `confirm_release`

## 5. 同步规则

1. **任务开始**：按 `AGENTS.md` §0 硬短读本档案 **§1**（名称/一句话定位/目标用户/流程偏好；场景任务再加 §2.2 标题行）；§1/§3 命中且足以支撑本任务 → 免重复询问。细节节按任务命中再读，禁止每任务通读全文。
2. **资料不足升级**：§1 空壳/占位/冲突/缺关键事实 → 入口判定 §5（README + 有界探查）→ 同轮回写本档案命中节与 `activeContext` 总览；收尾【资料补强】提示后续受益。
3. **收尾回写**：新决策/口径/边界、本轮核实的身份字段 → 就地更新；只写现行有效（**覆盖终态**，不追加过程句）；接入/迁移/归档事件进工作日志或归档清单，不进档案格；推断标「假设/待验证」。
4. **与实现冲突**：以代码/现网为准，先更新档案再动手。对外版本/迭代名或产品定位句已变却档案仍写旧「当前」→ 同轮改正（细节见 `doc-facade-sync.md` §2.1；未命中事件不扫）。
5. 档案变更**不**触发包自检。
6. **可用工具**：状态变化时更新 `{workroot}/capabilities/00-能力清单.md`，并刷新 §6 索引。
7. **缺陷平台（§7）**：provider/端点/凭据来源/提交方式变化 → 就地更新；不重复存凭据。

## 6. 可用工具（索引 · 按需）

> **SSOT**：`{workroot}/capabilities/00-能力清单.md`（接入时自模板 `rules/templates/00-onboarding/capabilities/` 创建）。本节只索引；契约/候选见 `wf-product/capabilities/`。未配置 = 降级，不阻塞。

| 项 | 值 |
| --- | --- |
| 能力清单 | `{workroot}/capabilities/00-能力清单.md` |
| 摘要（可选） | `{以清单为准}` |

## 7. 缺陷协作平台（按需 · 可选）

> 未启用写「无」。若同项目已有开发/测试包配置，优先复用 `project-profile.md` §3/§4 或测试包环境基线 §13 的 provider/端点/凭据来源；本节只记产品侧差异，不重复存凭据。

| 项 | 填写 |
| --- | --- |
| provider | `{{zentao / jira / ones / 无}}` |
| baseUrl | `{{平台地址}}` |
| 凭据来源 | `{{环境变量/本地配置路径（不入库）}}` |
| 默认产品/项目 | `{{ID + 显示名}}` |
| 当前产品账号/指派对象 | `{{账号/姓名}}` |
| 提交/回写方式 | `{{api（默认）/ browser / export}}` |
| 备注格式 | `{{html / markdown / text；默认 html=zentao}}` |
| 适配定义 | 最小契约：认证 / 列表·查重 / 详情 / 备注 / 状态变更（语义→平台取值）/ 指派 / 附件上传·回查 / 用户查询；`内置 zentao` 仅禅道；其它 provider 禁套禅道路径 |
| solutionChannel | `{{auto / manual；默认 manual}}` |
| 附件能力 | `{{支持 / 不支持 / 待适配}}` |
| 浏览器绑定 | `{{复用 docs/testing/capabilities/… ｜ {workroot}/capabilities/绑定/… ｜ 无}}` |
| 状态/指派映射 | `{{平台状态 ↔ 产品处置：待确认/待开发处理中/已确认/下版/关闭}}` |
