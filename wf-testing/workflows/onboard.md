# 测试规范接入 · `onboard` 状态机

> 全局规则见 `rules/core/global-rules.md`（遵守；重读按 §7 分级：新会话/换链全文，中段最小集，禁预防性通读）。每步先**实读**当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 为续跑指针；已有测试计划时阶段语义以计划 §0 为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`接入` → `baseline`；`重新接入` → `migrate`；`生成环境基线` → `baseline`；`装配能力` → `capabilities`；`生成README` → `baseline`；`更新README` → `baseline`；`整理README` → `baseline`；`资料收取` → `materials`；`资料整理` → `materials`；`资料归档` → `materials`；`资料巡检` → `materials`；`文档整理` → `lifecycle`；`文档巡检` → `lifecycle`；`文档清理` → `lifecycle`；`清理临时文件` → `lifecycle`；`清理过程文件` → `lifecycle`；`清理无效文件` → `lifecycle`；`清理失效文件` → `lifecycle`；`清理垃圾文件` → `lifecycle`；`清理临时` → `lifecycle`；`归档失效文档` → `lifecycle`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `migrate` | `onboard-agent` | — | `confirm_docs_migration` | 迁移清单/更新后的路径 | `baseline` | 停在本步/升级 |
| 2 | `baseline` | `onboard-agent` | — | — | env-baseline.md（§1/§2.1/§2.2/§8）· {workroot}/work-log.md（如无） | `materials` | 停在本步/升级 |
| 3 | `materials` | `onboard-agent` | — | `confirm_iteration_close`、`confirm_docs_migration` | 【入站分析】（确认后登记/A0～A2/发布 materials） | `lifecycle` | 停在本步/升级 |
| 4 | `lifecycle` | `onboard-agent` | — | `confirm_docs_migration` | 【文档治理检查】（确认后执行更新/归档/清理） | `context` | 停在本步/升级 |
| 5 | `context` | `onboard-agent` | — | — | activeContext.md | `gitignore` | 停在本步/升级 |
| 6 | `gitignore` | `onboard-agent` | — | `confirm_gitignore` | .gitignore 更新 + `git check-ignore` 证据 | `capabilities` | 停在本步/升级 |
| 7 | `capabilities` | `onboard-agent` | — | — | {workroot}/capabilities/00-能力清单.md（默认静默；点名装配时另出建议） | `verify` | 停在本步/升级 |
| 8 | `verify` | `onboard-agent` | — | — | {workroot}/_archive/接入核验-{yyyyMMdd}.md 或工作日志一行（①～⑦ 逐项 通过/缺口 + 证据） | `closeout` | 停在本步/升级 |
| 9 | `closeout` | `onboard-agent` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 本链按入口分级：接入/重新接入/基线/生成档案/装配能力入口推进到 `verify` 打标；资料收取/文档治理/清理入口只做该步 + 收尾，不连带其余接入步。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `when_eval=假:<依据>`（手工跳过记 `skip=user:<理由>`）。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/onboard.yaml` + 本图 + `rules/packets/onboard/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
