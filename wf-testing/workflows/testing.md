# AI测试流程（分析驱动） · `testing` 状态机

> 全局规则见 `rules/core/global-rules.md`（新会话读一次；同会话不重读全文）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`分析需求` → `plan`；`梳理测试依据` → `plan`；`理解PRD` → `plan`；`理解 PRD` → `plan`；`需求建模` → `plan`；`测试计划` → `plan`；`生成测试计划` → `plan`；`根据迭代生成测试计划` → `plan`；`按迭代生成测试计划` → `plan`；`根据版本生成测试计划` → `plan`；`根据需求生成测试计划` → `plan`；`根据方案生成测试计划` → `plan`；`功能测试计划` → `plan`；`更新计划` → `plan`；`本期变更` → `plan`；`计划变更` → `plan`；`增量变更` → `plan`；`新文档更新测试计划` → `plan`；`按测试计划执行` → `execute`；`按计划执行` → `execute`；`继续测试计划` → `execute`；`执行测试计划` → `execute`；`执行测试` → `execute`；`执行` → `execute`；`跑` → `execute`；`按计划回归` → `execute`；`回归重跑` → `execute`；`重跑` → `execute`；`执行专项` → `execute`；`执行接口测试` → `execute`；`执行探索式测试` → `execute`；`执行随机业务流程` → `execute`；`执行性能测试` → `execute`；`执行安全测试` → `execute`；`执行兼容性测试` → `execute`；`测试报告` → `report`；`出报告` → `report`；`准出评估` → `report`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；全局规则新会话读一次，同会话不重读全文；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `plan` | `test-planner` | — | `select_mainread`、`confirm_understanding`、`confirm_plan`、`confirm_iteration_close`、`confirm_docs_migration`、`gate:coverage-map` | {workroot}/{ver}/test-analysis.md（必做；来源/AC/设计点/意图/风险/覆盖）+ {workroot}/{ver}/test-plan.md（总排） | `execute` | 停在本步/升级 |
| 2 | `execute` | `test-orchestrator` | — | `confirm_execution_scope`、`gate:execute-batch` | 执行记录（场景+步骤+结果+证据）+ 缺陷 + 计划状态 | `report` | 停在本步/升级 |
| 3 | `report` | `report-agent` | — | `gate:report-consistency` | {workroot}/{ver}/test-report.md + 【任务收尾】 | `closeout` | 先修数据/证据或报阻塞；未 PASS/CONDITIONAL 不得进入 closeout |
| 4 | `closeout` | `report-agent` | — | `confirm_platform`、`confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 默认入口即止；仅按链/继续/按计划执行时向后推进。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `skip=理由`。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/testing.yaml` + 本图 + `rules/packets/testing/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
