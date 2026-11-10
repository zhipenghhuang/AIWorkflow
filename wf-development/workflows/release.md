# 发布与上线 · `release` 状态机

> 全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`发布` → `readiness`；`上线` → `readiness`；`发版` → `readiness`；`生产部署` → `readiness`；`正式部署` → `readiness`；`回滚` → `rollback`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `readiness` | `delivery-lead` | — | `gate:release-readiness` | 上线检查单（{workroot}/60-release/） | `acceptance` | 停在本步/升级 |
| 2 | `acceptance` | `delivery-lead` | `has_uat` | `confirm_acceptance` | UAT/验收记录（{workroot}/50-verification/） | `approval` | 停在本步/升级 |
| 3 | `approval` | `delivery-lead` | `release_ready_and_acceptance_passed` | `confirm_deploy` | 工程部署审批记录 | `deploy` | 停在本步/升级 |
| 4 | `deploy` | `delivery-lead` | `release_approved` | — | 部署记录 | `verify` | 停止发布，按回滚预案处理；不得隐瞒失败或继续观察 |
| 5 | `verify` | `delivery-lead` | `has_deployed` | — | 发布验证结果/发布记录 | `rollback` | 触发回滚/事故流程；未验证不得称发布成功 |
| 6 | `rollback` | `delivery-lead` | `release_failed_or_direct_rollback` | `confirm_rollback` | 回滚记录 | `postrelease` | 升级事故处理；不重复无效操作，不掩盖数据/业务影响 |
| 7 | `postrelease` | `delivery-lead` | `has_deployed` | — | 发布后verify/观察记录 | `record` | 停在本步/升级 |
| 8 | `record` | `delivery-lead` | `has_deployed` | — | 发布汇报/发布记录（{workroot}/60-release/） | `retro` | 停在本步/升级 |
| 9 | `retro` | `delivery-lead` | `incident_or_major_release` | — | 复盘（{workroot}/80-retrospectives/） | `closeout` | 停在本步/升级 |
| 10 | `closeout` | `delivery-lead` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 默认入口即止；仅按链/继续/按计划执行时向后推进。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `skip=理由`。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/release.yaml` + 本图 + `rules/packets/release/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
