# 产品缺陷平台协作 · `defect` 状态机

> 全局规则见 `rules/core/global-rules.md`（新会话读一次；同会话不重读全文）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`拉取产品缺陷` → `preflight`；`我的产品缺陷` → `preflight`；`缺陷平台产品缺陷` → `preflight`；`禅道产品缺陷` → `preflight`；`产品缺陷评审` → `preflight`；`开发评估单评审` → `preflight`；`产品缺陷处置` → `preflight`；`产品判定` → `preflight`；`产品判定回流` → `preflight`；`平台回写` → `writeback`；`回写产品缺陷` → `writeback`；`粘贴产品缺陷` → `pull`；`文档产品缺陷` → `pull`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；全局规则新会话读一次，同会话不重读全文；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `preflight` | `pm-lead` | — | — | 平台可用性/降级说明 | `pull` | 停在本步/升级 |
| 2 | `pull` | `pm-lead` | — | — | 缺陷清单摘要 + 每条受理单/读取记录 | `source` | 停在本步/升级 |
| 3 | `source` | `pm-lead` | — | — | 来源类型（测试直提/开发评估单/产品复核；逐条标） | `analyze` | 停在本步/升级 |
| 4 | `analyze` | `pm-lead` | — | — | 逐条分析结论（受理单 §3/§4） | `decide` | 停在本步/升级 |
| 5 | `decide` | `pm-lead` | — | `confirm_change`、`confirm_plan` | 处置决策（受理单 §5 / 变更单 §4 / 缺陷处置单） | `apply` | 停在本步/升级 |
| 6 | `apply` | `pm-lead` | — | — | 受理单 §6 + 变更单/最新 PRD/AC/计划/UAT + 缺陷处置单 + 附件清单 | `review` | 回 decide；非产品缺陷只产处置单，不改 PRD/AC/计划 |
| 7 | `review` | `reviewer-agent` | `substantive_change` | `select_review_mode`、`confirm_prd`、`gate:product-review` | 评审记录（{workroot}/{ver}/10-requirements/评审-{主题}-{yyyyMMdd}.md） | `writeback` | 停在本步/升级 |
| 8 | `writeback` | `pm-lead` | `remark_writeback` | `confirm_remark`、`gate:writeback-receipt` | 平台回写结果（备注/附件/状态/指派） | `verify` | 停在本步/升级 |
| 9 | `verify` | `pm-lead` | `needs_linked_update` | `gate:change-closure` | 验证结果 + 批末总结 | `closeout` | 停在本步/升级 |
| 10 | `closeout` | `pm-lead` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 默认入口即止；仅按链/继续/按计划执行时向后推进。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `skip=理由`。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/defect.yaml` + 本图 + `rules/packets/defect/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
