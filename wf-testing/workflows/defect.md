# 测试缺陷协作 · `defect` 状态机

> 全局规则见 `rules/core/global-rules.md`（遵守；重读按 §7 分级：新会话/换链全文，中段最小集，禁预防性通读）。每步先**实读**当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 为续跑指针；已有测试计划时阶段语义以计划 §0 为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`缺陷协作` → `classify`；`查重` → `classify`；`提交到平台` → `classify`；`指派给我` → `classify`；`已解决` → `classify`；`复测` → `classify`；`缺陷变化巡检` → `classify`；`补充澄清` → `classify`；`产品判定回流` → `classify`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `classify` | `bug-agent` | — | — | 子类判定（回归/提交/修改/查重/列表/巡检/澄清/产品回流 + 依据） | `search` | 停在本步/升级 |
| 2 | `search` | `bug-agent` | — | — | 查重键/拉取快照 + diff 摘要（单号/变化/证据缺口） | `submit` | 停在本步/升级 |
| 3 | `submit` | `bug-agent` | `defect_submit_required` | `confirm_remark`、`confirm_platform`、`gate:writeback-receipt` | 平台单号（或待确认后的统一导出路径）· 备注与状态同轮 · 可复制汇总块（collaboration.md §5.2） | `closeout` | 不提交/不回写；补证据、补探查或问用户；不得为交平台改标失败 |
| 4 | `closeout` | `report-agent` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 默认入口即止；仅按链/继续/按计划执行时向后推进。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `when_eval=假:<依据>`（手工跳过记 `skip=user:<理由>`）。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/defect.yaml` + 本图 + `rules/packets/defect/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
