# 迭代交付 · `iterate` 状态机

> 全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`按方案实施` → `precheck`；`按这个方案做` → `precheck`；`按方案做` → `precheck`；`实施这个方案` → `precheck`；`落地迭代方案` → `precheck`；`继续迭代` → `precheck`；`只出任务清单` → `precheck`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `precheck` | `iterate-lead` | — | — | 前置检查结果（需求签收/方案批准/清单/handoff/缺口） | `plan` | 停在本步/升级 |
| 2 | `plan` | `iterate-lead` | — | — | 任务清单 + 冻结的验收清单（{workroot}/40-tasks/任务清单-{ver}.md） | `confirm` | 停在本步/升级 |
| 3 | `confirm` | `iterate-lead` | `implementation_required` | `confirm_backlog` | 已确认清单/节奏 | `implement` | 停在本步/升级 |
| 4 | `implement` | `implementer` | `implementation_required` | — | 代码/配置改动 + 任务状态回写 | `review` | 停在本步/升级 |
| 5 | `review` | `reviewer-agent` | `review_required` | — | 评审结论/缺口 + `.gate/review.md` | `gates` | 回 implement 补前端交付物/方案覆盖矩阵；不得以代码/测试/API 200 代替，不得判通过。 |
| 6 | `gates` | `verifier-agent` | `implementation_required` | `gate:completion-gate` | .gate/wf-development/completion.json + 门禁摘要/文档同步 | `deliver` | 停在本步/升级 |
| 7 | `deliver` | `implementer` | `has_qa_or_deploy_or_requested` | `confirm_intent`、`gate:s6-admission` | 提测单/发布说明/回滚预案 | `retro` | 停在本步/升级 |
| 8 | `retro` | `delivery-lead` | `iteration_done_or_incident` | — | 复盘（{workroot}/80-retrospectives/） | `closeout` | 停在本步/升级 |
| 9 | `closeout` | `iterate-lead` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 默认入口即止；仅按链/继续/按计划执行时向后推进。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `when_eval=假:<依据>`（手工跳过记 `skip=user:<理由>`）。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/iterate.yaml` + 本图 + `rules/packets/iterate/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
