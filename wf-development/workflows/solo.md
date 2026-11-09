# 自包含完整链（产品→开发→测试） · `solo` 状态机

> 全局规则见 `rules/core/global-rules.md`（新会话读一次；同会话不重读全文）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`轻量开发` → `frame`；`自包含开发` → `frame`；`无正式迭代` → `frame`；`小改动` → `frame`；`我有个想法` → `frame`；`想法落地` → `frame`；`小项目` → `frame`；`轻量方案` → `plan`；`只出轻量方案` → `plan`；`轻量测试` → `test`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；全局规则新会话读一次，同会话不重读全文；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `frame` | `implementer` | `new_product_or_unclear_idea` | — | 产品定义卡（{workroot}/10-requirements/产品定义-{主题}-{yyyyMMdd}.md） | `plan` | 停在本步/升级 |
| 2 | `plan` | `implementer` | — | `confirm_spec` | 方案卡（{workroot}/20-design/方案卡-{主题}-{yyyyMMdd}.md） | `build` | 停在本步/升级 |
| 3 | `build` | `implementer` | — | — | 代码/配置改动 + 自测证据 | `test` | 回 plan 修方案卡；范围超出先停下说明 |
| 4 | `test` | `verifier-agent` | — | `gate:completion-gate` | 测试报告（{workroot}/50-verification/测试报告-{主题}-{yyyyMMdd}.md）+ .gate/wf-development/completion.json | `closeout` | 回 build 修复；P0 未过不得进 closeout，修后重跑原用例 + 冒烟 + 影响面 |
| 5 | `closeout` | `implementer` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 默认入口即止；仅按链/继续/按计划执行时向后推进。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `skip=理由`。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/solo.yaml` + 本图 + `rules/packets/solo/`；改本链只重生成该链。
- **轨道**：只接无正式迭代/正式协作（单人或团队，含大改动/高风险）；有正式协作/迭代或需正式发布/QA/交接 → 完整链；大改动/高风险按 `lightweight.md` §2 提高严谨度，不换链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
