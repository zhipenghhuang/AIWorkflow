# 页面原型设计 · `prototype` 状态机

> 全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`画原型` → `context`；`页面原型` → `context`；`原型设计` → `context`；`设计简报` → `context`；`设计策略` → `context`；`线框图` → `wireframe`；`UI设计` → `visual`；`高保真原型` → `hi-fi`；`设计评审` → `review`；`UI走查` → `usability`；`设计走查` → `usability`；`开发交接` → `handoff`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `context` | `ux-designer` | — | — | {workroot}/{ver}/20-design/设计情境-{主题}.md（含设计简报/项目适配/交付等级） | `ia` | 停在本步/升级 |
| 2 | `ia` | `ux-designer` | — | — | {workroot}/{ver}/20-design/IA-{主题}.md | `wireframe` | 停在本步/升级 |
| 3 | `wireframe` | `ux-designer` | — | — | {workroot}/{ver}/20-design/wireframe-{页面}.html 或 原型说明 §线框 | `visual` | 停在本步/升级 |
| 4 | `visual` | `ux-designer` | — | `confirm_design` | 视觉稿/设计 tokens/标注（{workroot}/{ver}/20-design/） | `hi-fi` | 停在本步/升级 |
| 5 | `hi-fi` | `ux-designer` | — | — | {workroot}/{ver}/20-design/prototype/index.html + design-tokens.css | `engineering` | 停在本步/升级 |
| 6 | `engineering` | `ux-designer` | — | — | {workroot}/{ver}/20-design/工程化检查-{主题}.md | `review` | 停在本步/升级 |
| 7 | `review` | `reviewer-agent` | — | `select_review_mode`、`gate:design-review` | {workroot}/{ver}/20-design/设计评审-{主题}.md + prototype-coverage.md | `usability` | 停在本步/升级 |
| 8 | `usability` | `ux-designer` | — | — | {workroot}/{ver}/20-design/可用性走查-{主题}.md | `handoff` | 停在本步/升级 |
| 9 | `handoff` | `ux-designer` | — | `confirm_prototype` | {workroot}/{ver}/20-design/开发交接-{主题}.md | `closeout` | 回 review 补评审/覆盖矩阵/截图；未过不得交开发 |
| 10 | `closeout` | `ux-designer` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 默认入口即止；仅按链/继续/按计划执行时向后推进。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `skip=理由`。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/prototype.yaml` + 本图 + `rules/packets/prototype/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
