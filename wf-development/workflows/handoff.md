# 协作交接 · `handoff` 状态机

> 全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`写交接单` → `compose`；`生成交接包` → `send`；`接收交接包` → `receive`；`变更通知` → `change_send`；`同步变更` → `change_receive`；`重规划` → `replan`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `compose` | `iterate-lead` | — | `confirm_intent` | 自洽交接单文档（默认非 HO；落 outbound/{category}/；同轮记 handoff-ledger.md） | `send` | 停在本步/升级 |
| 2 | `send` | `iterate-lead` | — | `confirm_handoff` | {workroot}/handoff/outbound/{category}/{HO-ID}/ + 【交接包已生成】 | `receive` | 缺 00/01/快照/占位符/链接断 → 不发送；补后重跑校验 |
| 3 | `receive` | `iterate-lead` | — | `confirm_change`、`confirm_plan` | 入站分析/吸收 + 接收回执（按需）+ 开发计划/文档更新 + 台账状态 | `change_send` | 停在本步/升级 |
| 4 | `change_send` | `iterate-lead` | — | `confirm_change`、`confirm_handoff` | {workroot}/handoff/outbound/变更/{CHG-HO-ID}/ + 更新后的受影响文档 | `change_receive` | 停在本步/升级 |
| 5 | `change_receive` | `iterate-lead` | — | `confirm_change`、`confirm_plan` | 变更影响分析 + 开发计划/文档调整 + 回执 | `replan` | 停在本步/升级 |
| 6 | `replan` | `iterate-lead` | — | `confirm_plan` | 更新后的开发计划 + 重规划记录 | `closeout` | 停在本步/升级 |
| 7 | `closeout` | `implementer` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 默认入口即止；仅按链/继续/按计划执行时向后推进。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `when_eval=假:<依据>`（手工跳过记 `skip=user:<理由>`）。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/handoff.yaml` + 本图 + `rules/packets/handoff/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
