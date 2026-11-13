# 产品展示与介绍 · `showcase` 状态机

> 全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`准备演示` → `audience`；`客户演示` → `audience`；`产品介绍` → `audience`；`产品汇报` → `audience`；`演示彩排` → `dryrun`；`一页纸` → `materials`；`Deck` → `materials`；`用户手册` → `docs`；`快速开始` → `docs`；`FAQ` → `docs`；`发布说明` → `docs`；`培训材料` → `docs`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `audience` | `pm-lead` | — | — | {workroot}/{ver}/50-showcase/展示需求-{受众}-{yyyyMMdd}.md（模板 rules/templates/50-showcase-docs/demo-script-template.md §1） | `story` | 停在本步/升级 |
| 2 | `story` | `pm-lead` | — | `confirm_narrative` | {workroot}/{ver}/50-showcase/故事线-{受众}.md | `demo` | 停在本步/升级 |
| 3 | `demo` | `pm-lead` | — | — | {workroot}/{ver}/50-showcase/演示脚本-{受众}-{yyyyMMdd}.md | `environment` | 停在本步/升级 |
| 4 | `environment` | `pm-lead` | — | — | {workroot}/{ver}/50-showcase/演示检查单-{yyyyMMdd}.md | `materials` | 停在本步/升级 |
| 5 | `materials` | `ux-designer` | — | — | {workroot}/{ver}/50-showcase/一页纸-{产品}.md · {workroot}/{ver}/50-showcase/Deck大纲-{受众}.md（按点名类型产出） | `docs` | 停在本步/升级 |
| 6 | `docs` | `prd-writer` | `docs_requested` | — | {workroot}/user/{按点名类型}-{ver}.md（快速开始/用户手册/FAQ/发布说明/培训材料；未点名默认用户手册） | `dryrun` | 停在本步/升级 |
| 7 | `dryrun` | `pm-lead` | `demo_needs_dryrun` | — | {workroot}/{ver}/50-showcase/反馈记录-{yyyyMMdd}.md | `publish` | 停在本步/升级 |
| 8 | `publish` | `pm-lead` | `materials_for_external` | `confirm_materials` | 对外确认记录（清单 + 数字/截图来源 + 未实现边界 + 批准人） | `closeout` | 停在本步/升级 |
| 9 | `closeout` | `pm-lead` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 默认入口即止；仅按链/继续/按计划执行时向后推进。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `when_eval=假:<依据>`（手工跳过记 `skip=user:<理由>`）。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/showcase.yaml` + 本图 + `rules/packets/showcase/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
