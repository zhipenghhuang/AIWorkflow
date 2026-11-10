# 常规代码变更 · `change` 状态机

> 全局规则见 `rules/core/global-rules.md`（每步先读并逐条过）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`常规变更` → `clarify`；`澄清` → `clarify`；`需求澄清` → `clarify`；`提交` → `closeout`；`推送` → `closeout`；`分析PRD` → `analyze_input`；`分析 PRD` → `analyze_input`；`理解需求` → `analyze_input`；`解析原型` → `analyze_input`；`出方案` → `design`；`方案评审` → `review-docs`；`文档评审` → `review-docs`；`设计文档评审` → `review-docs`；`代码评审` → `review`；`提测` → `deliver`；`提测单` → `deliver`；`发布说明` → `deliver`；`回滚预案` → `deliver`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；全局规则每步先读并逐条过；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `clarify` | `implementer` | — | `confirm_iteration_close`、`confirm_docs_migration` | 需求理解包（有外部输入时）+ L1 开发卡（验收/SC）/ L0 轻量回执 | `analyze_input` | 停在本步/升级 |
| 2 | `analyze_input` | `implementer` | `has_product_docs_or_prototypes` | `confirm_understanding` | 需求理解包（{workroot}/10-requirements/理解-{主题}-{yyyyMMdd}.md；§0 Brief+Delta 必填）+ 用户版业务变化说明（L1+ 用户可见变化必出） | `requirements` | 停在本步/升级 |
| 3 | `requirements` | `implementer` | `new_feature_or_scope_change_or_requested` | `confirm_requirements` | 需求基线（{workroot}/10-requirements/） | `design` | 停在本步/升级 |
| 4 | `design` | `implementer` | `new_feature_or_architecture_or_breaking_change_or_high_risk_or_requested` | `confirm_spec` | 方案/ADR（{workroot}/20-design/） | `review-docs` | 停在本步/升级 |
| 5 | `review-docs` | `doc-reviewer` | `do_landing_doc_review` | `select_review_mode`、`confirm_spec` | 评审-文档-*.md 或 HUMAN_APPROVED 声明 | `plan` | 停在本步/升级 |
| 6 | `plan` | `iterate-lead` | `multi_file_or_new_feature_or_requested` | `confirm_backlog` | 任务清单 + 冻结的验收清单（{workroot}/40-tasks/） | `implement` | 停在本步/升级 |
| 7 | `implement` | `implementer` | — | — | 代码/配置改动 | `review` | 回 20-design/review-docs 或 requirements；不得以「先写再补」绕过 |
| 8 | `review` | `reviewer-agent` | `review_required` | — | 评审结论/缺口 + `.gate/review.md` | `verify` | 回 implement 补前端交付物/方案覆盖矩阵；不得以代码/测试/API 200 代替，不得判通过。 |
| 9 | `verify` | `verifier-agent` | `work_changed_or_requested` | `gate:completion-gate` | .gate/wf-development/completion.json + 验证回执 | `deliver` | 停在本步/升级 |
| 10 | `deliver` | `implementer` | `has_qa_or_deploy_or_requested` | `confirm_intent`、`gate:s6-admission` | 提测单/发布说明/回滚预案（{workroot}/60-release/） | `release_handoff` | 停在本步/升级 |
| 11 | `release_handoff` | `delivery-lead` | `has_deploy` | — | 发布就绪包 | `closeout` | 停在本步/升级 |
| 12 | `closeout` | `implementer` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

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
