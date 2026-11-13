# 复盘与改进 · `retro` 状态机

> 全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`复盘` → `gather`；`事故复盘` → `gather`；`迭代复盘` → `gather`；`版本复盘` → `gather`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `gather` | `delivery-lead` | — | — | 时间线/影响/证据/指标 | `analyze` | 停在本步/升级 |
| 2 | `analyze` | `delivery-lead` | — | — | 直接原因/根本原因/贡献因素 | `actions` | 停在本步/升级 |
| 3 | `actions` | `delivery-lead` | — | `confirm_actions` | 行动项（负责人/截止/验收） | `record` | 停在本步/升级 |
| 4 | `record` | `delivery-lead` | — | — | 复盘文档（{workroot}/80-retrospectives/） | `closeout` | 停在本步/升级 |
| 5 | `closeout` | `delivery-lead` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 默认入口即止；仅按链/继续/按计划执行时向后推进。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `when_eval=假:<依据>`（手工跳过记 `skip=user:<理由>`）。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/retro.yaml` + 本图 + `rules/packets/retro/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
