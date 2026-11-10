# 缺陷修复协作 · `defect-fix` 状态机

> 全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`缺陷修复` → `preflight`；`指派给我` → `preflight`；`我的待修` → `preflight`；`修复#` → `preflight`；`#数字` → `preflight`；`拉取产品回复` → `product_decision`；`产品回复` → `product_decision`；`产品退回` → `product_decision`；`继续缺陷` → `product_decision`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `preflight` | `defect-fixer` | — | — | 平台可用性/鉴权结果 + 降级路由（route/reason/next_action） | `pull` | 停在本步/升级 |
| 2 | `pull` | `defect-fixer` | — | — | 清单摘要/分组 | `triage` | 停在本步/升级 |
| 3 | `triage` | `defect-fixer` | — | — | 分类结论（中文结论/依据/下一步） | `assess_product` | 停在本步/升级 |
| 4 | `assess_product` | `defect-fixer` | `product_defect` | — | 产品缺陷评估单（模板 rules/templates/20-design/product-defect-assessment-template.md） | `handoff_product` | 停在本步/升级 |
| 5 | `handoff_product` | `defect-fixer` | `product_defect` | `confirm_remark` | 平台回写结果（备注+附件+指派产品） | `await_product` | 停在本步/升级 |
| 6 | `await_product` | `defect-fixer` | `product_defect` | — | 等待回执（AWAIT_PRODUCT） | `product_decision` | 停在本步/升级 |
| 7 | `product_decision` | `defect-fixer` | `product_decision_received` | — | 产品结论/附件/对齐清单 | `align` | 停在本步/升级 |
| 8 | `align` | `defect-fixer` | `product_decision_requires_alignment` | — | 对齐记录（受影响文档/计划清单） | `fix` | 停在本步/升级 |
| 9 | `fix` | `defect-fixer` | `implementation_required` | — | 修复/方案/验证结果 | `clarify` | 停在本步/升级 |
| 10 | `clarify` | `defect-fixer` | `need_clarification` | `confirm_remark` | 回写结果（【无法确认·待澄清】/重复/设计如此/非defects/外部/已在其它构建修复） | `gates` | 停在本步/升级 |
| 11 | `gates` | `verifier-agent` | `has_code_change` | `gate:completion-gate` | .gate/wf-development/completion.json + 门禁摘要 | `menu` | 停止本批；不得进入 menu/close，先修复、补证据或报阻塞 |
| 12 | `menu` | `defect-fixer` | `implementation_required` | `select_menu` | 【缺陷修复处理总结】+【用户选择菜单】 | `close` | 门禁未过先回 gates/fix；不得输出提交/回写菜单 |
| 13 | `close` | `defect-fixer` | `implementation_required` | `confirm_deploy`、`confirm_remark` | 提交/部署/回写结果 | `postrelease` | 门禁未过先回 gates/fix；不得提交/部署/回写 |
| 14 | `postrelease` | `defect-fixer` | `has_deployed` | — | 发布后verify/发布记录 | `retro` | 停在本步/升级 |
| 15 | `retro` | `defect-fixer` | `recurring_defect_or_incident` | — | 复盘（{workroot}/80-retrospectives/） | `closeout` | 停在本步/升级 |
| 16 | `closeout` | `defect-fixer` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 默认入口即止；仅按链/继续/按计划执行时向后推进。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `skip=理由`。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/defect-fix.yaml` + 本图 + `rules/packets/defect-fix/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
