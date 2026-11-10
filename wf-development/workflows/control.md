# 开发计划 · `control` 状态机

> 全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`开发计划` → `init`；`项目计划` → `init`；`排期` → `init`；`生成计划` → `init`；`根据文档出计划` → `init`；`按开发计划执行` → `run`；`继续开发计划` → `run`；`进度` → `sync`；`当前阶段` → `sync`；`当前状态` → `sync`；`下一步` → `next`；`阶段检查` → `check`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `init` | `iterate-lead` | — | `confirm_plan`、`confirm_iteration_close` | 开发计划（{workroot}/development-plan.md） | `run` | 停在本步/升级 |
| 2 | `run` | `iterate-lead` | — | — | 切包声明（目标 workflow/step/packet）+ activeContext 运行状态更新；实施/方案/任务正文只在目标步骤卡产出 | `目标步骤卡` | 停在本步/升级 |
| 3 | `sync` | `iterate-lead` | — | — | 更新后的开发计划 | `check` | 停在本步/升级 |
| 4 | `check` | `reviewer-agent` | — | `gate:dev-plan` | 阶段门检查结论/缺口 | `next` | 停在本步/升级 |
| 5 | `next` | `iterate-lead` | — | — | 当前阶段/下一步 3 件事/建议入口 | `closeout` | 停在本步/升级 |
| 6 | `closeout` | `iterate-lead` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- `run` 只切包，不沿本表进入 `sync`。「按开发计划执行」关闭本包并只打开目标步骤卡；「进度」才进 `sync`。其它入口仍入口即止。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `skip=理由`。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/control.yaml` + 本图 + `rules/packets/control/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- `control/run` 切包 = 关闭本包后只打开目标步骤卡（一次仍只一张卡）。其余跨链走重新路由或 handoff；诊断可读对方状态图。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
