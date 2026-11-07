# 新产品 0→1 · `new-product` 状态机

> 全局规则见 `rules/core/global-rules.md`（新会话读一次；同会话不重读全文）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`启动新产品` → `discover`；`新项目` → `discover`；`从0到1` → `discover`；`产品立项` → `discover`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；全局规则新会话读一次，同会话不重读全文；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `discover` | `pm-analyst` | — | `confirm_understanding` | {workroot}/{ver}/10-requirements/立项书-{yyyyMMdd}.md | `go` | 停在本步/升级 |
| 2 | `go` | `pm-analyst` | — | `confirm_go` | 立项决策记录（Go/Hold/Kill + 依据/待verify/责任人，并入立项书） | `define` | 停在本步/升级 |
| 3 | `define` | `pm-analyst` | `go_decision_go` | `confirm_plan` | {workroot}/product-plan.md | `prd` | 停在本步/升级 |
| 4 | `prd` | `prd-writer` | `go_decision_go` | — | PRD + 评审记录/原型（{workroot}/{ver}/10-requirements/、20-design/） | `deliver` | 停在本步/升级 |
| 5 | `deliver` | `pm-lead` | `go_decision_go` | — | 交付计划 + UAT 记录（{workroot}/{ver}/40-delivery/） | `launch` | 停在本步/升级 |
| 6 | `launch` | `pm-lead` | `go_decision_go` | `confirm_release`、`gate:uat-evidence` | 发布决策 + GTM 检查 + 复盘（{workroot}/{ver}/40-delivery/、90-retrospectives/） | `closeout` | 停在本步/升级 |
| 7 | `closeout` | `pm-lead` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 默认入口即止；仅按链/继续/按计划执行时向后推进。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `skip=理由`。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/new-product.yaml` + 本图 + `rules/packets/new-product/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
