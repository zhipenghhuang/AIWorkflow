# 流程链 · onboard

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：wf-development
- **workflow**：`onboard`（开发规范接入）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 隔离边界（改本链不动别链）

- **本链专属**：`rules/packets/onboard/`（本文件、`_region-*`、节点包、`_orch.yaml`）；只重生成本链：`build_step_packets.py <包> <包> --only onboard`。
- **只读共享**：`rules/core/`、`rules/gates.md`、`rules/workflow.md`、`skills/`、`rules/templates/`；改共享层会影响所有链，须跑全包自检。
- **跨链需要时**：重新路由或 handoff；诊断确需只读对方 `_chain.md`，不打开对方节点包，读完回本链。

## 推进

口令只认本包 AGENTS 口令表。本链只排步骤与 `when`，不另列口令。 从已命中的入口步沿阶段表向后；`when` 不满足则跳过且不打开该包。 口令明确只做单步（只出方案/只评审/代码评审/方案评审/只提测/只出清单/轻量方案）时，本步完成即停并输出收尾骨架；其余按表向后。 本步动作清单写明跳过、停止或改走他步时，以清单为准。 全链入口仅：接入/重新接入/基线/装配能力，走到 verify 打标；资料与文档治理只做该步加收尾，不连带其余接入步。

## 状态机

本 workflow 步骤较少，无额外子机；按阶段表与「推进」打开步骤包。


## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `mount` | 复制与挂载确认 | `—` | — | `rules/packets/onboard/mount.md` |
| 2 | `profile` | 档案与规范 | `—` | — | `rules/packets/onboard/profile.md` |
| 3 | `migrate` | 旧项目迁移 | `—` | — | `rules/packets/onboard/migrate.md` |
| 4 | `docs` | 文档树与归档 | `—` | — | `rules/packets/onboard/docs.md` |
| 5 | `materials` | 资料收取与归档 | `—` | — | `rules/packets/onboard/materials.md` |
| 6 | `lifecycle` | 文档治理检查 | `—` | — | `rules/packets/onboard/lifecycle.md` |
| 7 | `control` | 开发计划 | `—` | — | `rules/packets/onboard/control.md` |
| 8 | `gitignore` | 入库策略 | `—` | — | `rules/packets/onboard/gitignore.md` |
| 9 | `capabilities` | 环境与工具检查 | `—` | — | `rules/packets/onboard/capabilities.md` |
| 10 | `verify` | 核验与打标 | `—` | — | `rules/packets/onboard/verify.md` |
| 11 | `wrap` | 收尾 | `—` | — | `rules/packets/onboard/wrap.md` |
| 12 | `commit` | 拟提交 | `—` | — | `rules/packets/onboard/commit.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次。是否进入下一步或下一区，只按上文「推进」。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
