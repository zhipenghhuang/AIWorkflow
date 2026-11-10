# 变更吸收 · `intake` 状态机

> 全局规则见 `rules/core/global-rules.md`（每步先读并逐条过）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`新文档` → `scan`；`新变化` → `scan`；`确认项` → `scan`；`收件箱` → `scan`；`变更吸收` → `scan`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；全局规则每步先读并逐条过；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `scan` | `iterate-lead` | — | — | 新输入候选清单 | `classify` | 停在本步/升级 |
| 2 | `classify` | `iterate-lead` | — | — | DOC/CR/OPEN/DEC 登记 | `parse` | 停在本步/升级 |
| 3 | `parse` | `iterate-lead` | — | `confirm_understanding` | 资料理解摘要（Brief+本期差量 + 来源/目标/范围/F-R-AC/冲突/GAP/置信度） | `impact` | 停在本步/升级 |
| 4 | `impact` | `iterate-lead` | — | `confirm_change`、`confirm_requirements`、`confirm_replan` | 影响矩阵/待确认项 + C2/C3 重基线清单 | `absorb` | 停在本步/升级 |
| 5 | `absorb` | `iterate-lead` | — | `confirm_iteration_close`、`confirm_docs_migration` | 已更新文档/台账/任务 · 【迭代关账/归档候选】（如有） | `report` | 停在本步/升级 |
| 6 | `report` | `iterate-lead` | — | — | 【变更吸收报告】 | `closeout` | 停在本步/升级 |
| 7 | `closeout` | `iterate-lead` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 默认入口即止；仅按链/继续/按计划执行时向后推进。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `skip=理由`。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/intake.yaml` + 本图 + `rules/packets/intake/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
