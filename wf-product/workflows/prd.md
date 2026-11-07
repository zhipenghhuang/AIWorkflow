# 需求与 PRD · `prd` 状态机

> 全局规则见 `rules/core/global-rules.md`（新会话读一次；同会话不重读全文）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`收集需求` → `discover`；`需求洞察` → `discover`；`竞品分析` → `discover`；`学习竞品` → `discover`；`需求池` → `discover`；`分析客户需求` → `discover`；`需求调研` → `discover`；`客户访谈` → `discover`；`需求澄清` → `discover`；`竞品对标` → `benchmark`；`功能对标` → `benchmark`；`对标分析` → `benchmark`；`功能差距` → `benchmark`；`立项` → `prioritize`；`单需求立项` → `prioritize`；`排优先级` → `prioritize`；`写PRD` → `prd`；`写 PRD` → `prd`；`出PRD` → `prd`；`补PRD` → `prd`；`PRD评审` → `review`；`PRD 评审` → `review`；`定稿` → `review`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；全局规则新会话读一次，同会话不重读全文；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `discover` | `pm-analyst` | — | `confirm_understanding` | 需求池/洞察/竞品分析（{workroot}/requirement-pool.md 或 {workroot}/{ver}/10-requirements/洞察/竞品分析-*.md） | `benchmark` | 停在本步/升级 |
| 2 | `benchmark` | `pm-analyst` | `benchmark_or_mode_p` | `confirm_scope` | 竞品对标矩阵 + 需求池候选项（{workroot}/{ver}/10-requirements/竞品对标-*.md + {workroot}/requirement-pool.md） | `prioritize` | 停在本步/升级 |
| 3 | `prioritize` | `pm-analyst` | `new_requirement_or_scope_change` | `confirm_scope` | 需求池优先级/立项建议（{workroot}/requirement-pool.md §优先级） | `prd` | 停在本步/升级 |
| 4 | `prd` | `prd-writer` | — | `confirm_understanding`、`confirm_scope`、`gate:product-prd` | {workroot}/{ver}/10-requirements/PRD-{主题}.md（模板 rules/templates/10-planning/prd-template.md） | `prototype` | 停在本步/升级 |
| 5 | `prototype` | `ux-designer` | `has_ui_requirement` | — | {workroot}/{ver}/20-design/原型-{主题}.html + 原型说明/交接要点（条件） | `review` | 停在本步/升级 |
| 6 | `review` | `reviewer-agent` | — | `select_review_mode`、`confirm_prd`、`gate:product-review` | 评审记录或 HUMAN_APPROVED 声明 | `handoff` | 停在本步/升级 |
| 7 | `handoff` | `pm-lead` | `prd_ready_for_handoff` | — | {workroot}/handoff/outbound/需求/ 自洽 PRD 实拷 + handoff-ledger.md；升 REQ 包时走 handoff.send | `closeout` | 停在本步/升级 |
| 8 | `closeout` | `prd-writer` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 默认入口即止；仅按链/继续/按计划执行时向后推进。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `skip=理由`。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/prd.yaml` + 本图 + `rules/packets/prd/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
