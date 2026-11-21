# 迭代上下文模板（iteration-context.yaml）

> 用途：**本期**输入与范围的单一出处。每期一份，随本期 PRD/方案/原型/计划生成；**不要**把本期原型/交互路径写进项目档案。
> 落点：`{workroot}/00-governance/iteration-context.yaml`（当前迭代；关版时随计划归档）。
> 读取：`design`/`plan` 产出；`implement`/`ui-audit`/`review`/门按本文件解析“本期有没有原型/基线/交互/哪些波次”。缺本文件且 A/B UI = G4.0 不过。
> 原则：稳定事实（技术栈、设计系统、命令）在 `project-profile.md`；本期事实在本文。`prototype: none` 是合法值，不是异常。

## 1. 填写骨架（复制为 YAML）

```yaml
schema: 1
iteration: "{迭代/版本}"
risk: "L0|L1|L2|L3"
updated_at: "{yyyy-MM-dd}"

inputs:
  prd: "{路径|none}"
  solution: "{路径|none}"
  contract: "{路径#版本|none}"
  prototype: "{路径|none}"          # none = 本期无原型
  prototype_version: "{版本|na}"
  prototype_sha256: "{哈希|na}"     # 有原型时填；换版必须重解码/重对照
  design_spec: "{路径|none}"        # 前端设计说明（无原型时的基线来源之一）
  interaction_spec: "{路径|none}"   # 交互规格 yaml（有交互时必填）

frontend:
  scope: ["/path"]                  # 本期涉及页面/路由；[] = 无 UI
  baseline: "prototype|design_spec|existing_page|prd|none"
  interactions: "required|none"     # required = 有交互控件，必须有 interaction_spec

backend:
  scope: ["module/api"]             # 本期涉及后端模块/接口；[] = 无后端

waves:                              # 单波次也写 W1；多波次逐项
  - id: "W1"
    scope: ["{范围}"]

domains:                            # 13 域适用性；S4.0 定，S4.4 闭合；名称与 plan-coverage §6 一致
  功能与契约: {apply: true, depth: "full"}
  状态与幂等: {apply: true, depth: "full"}
  权限与数据域: {apply: true, depth: "full"}
  边界与异常: {apply: true, depth: "standard"}
  输入面与负向: {apply: true, depth: "standard"}
  并发与一致性: {apply: false, reason: "无并发写/无共享状态"}
  性能与容量: {apply: true, depth: "standard"}
  安全与合规: {apply: true, depth: "standard"}
  可观测与运维: {apply: false, reason: "无新异步任务/无运行时服务"}
  兼容与响应式: {apply: true, depth: "standard"}
  可访问性与文案: {apply: true, depth: "standard"}
  集成与多表面: {apply: true, depth: "standard"}
  数据与迁移/回滚: {apply: false, reason: "本期无 schema/数据迁移"}
```

## 2. 解析规则（门按此顺序）

1. 当前任务/方案/理解包 §1 的来源清单（最具体，带版本）；
2. 本文件 `inputs`；
3. 开发计划 §2 输入表；
4. 仍无 → `frontend.scope` 为空则 `na`；有 UI 但无 `prototype`/`design_spec`/`existing_page`/`prd` 基线 = G4.0 不过。

- `prototype: none` + `baseline: design_spec|existing_page|prd`：合法；矩阵/审计写 `baseline=`，不得因“无原型”跳过对齐。
- **图片/Figma/无法解码的原型**：`prototype` 填参考图路径，`baseline: design_spec`（另写规格）；`baseline: prototype` 只用于可解码 HTML/SPA（要过 `.gate/prototype` 解码）。
- `baseline: prototype` 但原型不存在/哈希不符 = G4.0 不过；换版后矩阵/flow 用例失效，必须重跑。
- `frontend.scope: []` = 无 UI：S4.2 与前端门整节 `na`；不要求原型/截图/ui-audit。
- `frontend.interactions: required` 但 `interaction_spec: none` = G4.2 不过；`none` 仅用于无交互控件的静态页，审计 §4 写 `无交互流` + 理由。
- `domains` 的键固定 13 个；`apply: false` 必须写 `reason`；高风险域（function/state_idempotency/permission/input_negative/concurrency/security/integration/migration_rollback）L2+ 不得仅以 `reason` 跳过，须 user 接受或改范围。
- 每期只维护这一份；换迭代新建/更新，不把上期路径留在 `project-profile.md`。

## 3. 最小示例（无原型、有 UI、无后端）

```yaml
schema: 1
iteration: "V1.4"
risk: "L1"
inputs:
  prd: "inbound/V1.4/需求.md"
  solution: "docs/development/20-design/方案-用户列表-20261121.md"
  contract: "none"
  prototype: "none"
  prototype_version: "na"
  prototype_sha256: "na"
  design_spec: "docs/development/20-design/前端设计说明-用户列表-20261121.md"
  interaction_spec: "docs/development/20-design/交互规格-用户列表-20261121.yaml"
frontend:
  scope: ["/users"]
  baseline: "design_spec"
  interactions: "required"
backend:
  scope: []
waves:
  - id: "W1"
    scope: ["用户列表"]
domains:
  功能与契约: {apply: true, depth: "standard"}
  状态与幂等: {apply: true, depth: "standard"}
  权限与数据域: {apply: true, depth: "standard"}
  边界与异常: {apply: true, depth: "standard"}
  输入面与负向: {apply: true, depth: "standard"}
  并发与一致性: {apply: false, reason: "列表只读，无并发写"}
  性能与容量: {apply: true, depth: "standard"}
  安全与合规: {apply: true, depth: "standard"}
  可观测与运维: {apply: false, reason: "无新异步任务"}
  兼容与响应式: {apply: true, depth: "standard"}
  可访问性与文案: {apply: true, depth: "standard"}
  集成与多表面: {apply: true, depth: "standard"}
  数据与迁移/回滚: {apply: false, reason: "无数据迁移"}
```
