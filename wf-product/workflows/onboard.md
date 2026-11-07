# 产品规范接入 · `onboard` 状态机

> 全局规则见 `rules/core/global-rules.md`（新会话读一次；同会话不重读全文）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 运行状态为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`接入产品规范` → `mount`；`重新接入` → `migrate`；`生成产品档案` → `profile`；`配置缺陷平台` → `profile`；`生成README` → `profile`；`更新README` → `profile`；`整理README` → `profile`；`装配能力` → `capabilities`；`资料收取` → `materials`；`资料整理` → `materials`；`资料归档` → `materials`；`资料巡检` → `materials`；`文档整理` → `lifecycle`；`文档巡检` → `lifecycle`；`文档清理` → `lifecycle`；`清理临时文件` → `lifecycle`；`清理过程文件` → `lifecycle`；`清理无效文件` → `lifecycle`；`清理失效文件` → `lifecycle`；`清理垃圾文件` → `lifecycle`；`清理临时` → `lifecycle`；`归档失效文档` → `lifecycle`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；全局规则新会话读一次，同会话不重读全文；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `migrate` | `onboard-agent` | — | `confirm_docs_migration` | 迁移清单/更新后的路径 | `mount` | 停在本步/升级 |
| 2 | `mount` | `onboard-agent` | — | — | 项目根 AGENTS.md 包挂载段（已存在则追加，不覆盖） | `profile` | 停在本步/升级 |
| 3 | `profile` | `onboard-agent` | — | — | product-profile.md · activeContext.md · {workroot}/work-log.md（如无）·（模板 rules/templates/） | `materials` | 停在本步/升级 |
| 4 | `materials` | `onboard-agent` | — | `confirm_iteration_close`、`confirm_docs_migration` | 【入站分析】（确认后登记/A0～A2/发布 materials） | `lifecycle` | 停在本步/升级 |
| 5 | `lifecycle` | `onboard-agent` | — | `confirm_docs_migration` | 【文档治理检查】（确认后执行更新/归档/清理） | `gitignore` | 停在本步/升级 |
| 6 | `gitignore` | `onboard-agent` | — | `confirm_gitignore` | .gitignore 更新 + `git check-ignore` 证据 | `capabilities` | 停在本步/升级 |
| 7 | `capabilities` | `onboard-agent` | — | — | {workroot}/capabilities/00-能力清单.md（默认静默；点名装配时另出建议） | `verify` | 停在本步/升级 |
| 8 | `verify` | `onboard-agent` | — | — | {workroot}/00-governance/接入核验-{yyyyMMdd}.md（①～⑥ 逐项 通过/缺口 + 证据） | `closeout` | 停在本步/升级 |
| 9 | `closeout` | `onboard-agent` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 本链为全链入口；按表推进到下一个门/停点。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `skip=理由`。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/onboard.yaml` + 本图 + `rules/packets/onboard/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
