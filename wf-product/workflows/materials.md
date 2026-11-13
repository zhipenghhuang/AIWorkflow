# 产品权威文档库发布 · `materials` 状态机

> 全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`导出项目文档` → `select`；`生成资料库` → `select`；`生成交付资料` → `select`；`发资料` → `select`；`发项目文档` → `select`；`打包项目文档` → `select`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `select` | `pm-lead` | — | `confirm_materials` | 【材料库发布范围】版本/受众/域/包含/排除 | `sync` | 停在本步/升级 |
| 2 | `sync` | `pm-lead` | — | — | docs/materials/{ver}/（00-overview～07-appendix，按需） | `index` | 停在本步/升级 |
| 3 | `index` | `pm-lead` | — | `gate:materials-validate` | docs/materials/{ver}/README.md + docs/materials/INDEX.md + 【材料库校验】通过/待补 | `closeout` | 停在本步/升级 |
| 4 | `closeout` | `pm-lead` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 本链为全链入口；按表推进到下一个门/停点。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `when_eval=假:<依据>`（手工跳过记 `skip=user:<理由>`）。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/materials.yaml` + 本图 + `rules/packets/materials/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
