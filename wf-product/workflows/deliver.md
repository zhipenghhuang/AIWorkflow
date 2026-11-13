# 交付与验收 · `deliver` 状态机

> 全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`排期` → `schedule`；`迭代规划` → `schedule`；`交付计划` → `schedule`；`任务拆解` → `schedule`；`交付计划评审` → `review-plan-deliver`；`评审交付计划` → `review-plan-deliver`；`交付跟进` → `followup`；`风险升级` → `followup`；`UAT` → `uat`；`验收` → `uat`；`发布` → `release`；`上线检查` → `release`；`复盘` → `release`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `schedule` | `pm-lead` | — | — | {workroot}/{ver}/40-delivery/交付计划-{ver}.md（模板 rules/templates/40-delivery/delivery-plan-template.md） | `review-plan-deliver` | 回 prd.review 补定稿/评审；未定稿且未获明确豁免不排期 |
| 2 | `review-plan-deliver` | `reviewer-agent` | — | `select_review_mode` | 评审记录（评审-交付计划-{ver}-{yyyyMMdd}.md）或 HUMAN_APPROVED 声明 | `followup` | 停在本步/升级 |
| 3 | `followup` | `pm-lead` | — | — | 产品计划 §7/§8 + 交付计划 §7 状态报告 + 风险/依赖台账 | `uat` | 停在本步/升级 |
| 4 | `uat` | `pm-lead` | `has_uat` | `gate:uat-evidence` | {workroot}/{ver}/40-delivery/UAT-{ver}-{yyyyMMdd}.md（模板 rules/templates/40-delivery/uat-acceptance-template.md） | `release` | 停在本步/升级 |
| 5 | `release` | `pm-lead` | — | `confirm_release`、`gate:uat-evidence` | 发布决策 + 发布记录 + 复盘（{workroot}/{ver}/40-delivery/、90-retrospectives/） | `closeout` | 不发布；回 UAT/审批或报阻塞，不得用“已发布”措辞 |
| 6 | `closeout` | `pm-lead` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 默认入口即止；仅按链/继续/按计划执行时向后推进。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `when_eval=假:<依据>`（手工跳过记 `skip=user:<理由>`）。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/deliver.yaml` + 本图 + `rules/packets/deliver/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
