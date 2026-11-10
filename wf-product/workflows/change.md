# 需求/问题受理与变更 · `change` 状态机

> 全局规则见 `rules/core/global-rules.md`（每步先读并逐条过）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`需求受理` → `intake`；`问题受理` → `intake`；`产品缺陷` → `intake`；`需求变更` → `intake`；`需求答疑` → `intake`；`开发不确定` → `intake`；`测试发现产品缺陷` → `intake`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；全局规则每步先读并逐条过；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `intake` | `pm-lead` | — | `confirm_understanding`、`confirm_iteration_close`、`confirm_docs_migration` | {workroot}/{ver}/30-changes/受理-{主题}-{yyyyMMdd}.md | `triage` | 停在本步/升级 |
| 2 | `triage` | `pm-lead` | — | — | 分诊结论（写入受理单 §3） | `new_requirement` | 停在本步/升级 |
| 3 | `new_requirement` | `pm-analyst` | `new_requirement` | `confirm_scope` | {workroot}/requirement-pool.md 更新 + 范围结论 | `assess` | 停在本步/升级 |
| 4 | `assess` | `pm-lead` | `needs_impact_assessment` | — | 影响评估（受理单 §4；改基线时同步变更单 §3） | `decide` | 停在本步/升级 |
| 5 | `decide` | `pm-lead` | `decision_required` | `confirm_change`、`confirm_plan` | 处置结论（受理单 §5；改基线时写变更单 §4） | `apply` | 停在本步/升级 |
| 6 | `apply` | `pm-lead` | `change_apply_required` | — | 更新后的 PRD/AC/原型/计划等 + 受理单 §6 | `review` | 回 decide/受理单；拒绝/重复/实现缺陷/补充信息不得更新基线 |
| 7 | `review` | `reviewer-agent` | `substantive_change` | `select_review_mode`、`confirm_prd`、`gate:product-review` | 评审记录（{workroot}/{ver}/10-requirements/评审-{主题}-{yyyyMMdd}.md） | `verify` | 停在本步/升级 |
| 8 | `verify` | `pm-lead` | `needs_linked_update` | `gate:change-closure` | 验证结果（受理单 §7 / UAT / 变更单 §5） | `closeout` | 停在本步/升级 |
| 9 | `closeout` | `pm-lead` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 默认入口即止；仅按链/继续/按计划执行时向后推进。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `skip=理由`。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/change.yaml` + 本图 + `rules/packets/change/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
