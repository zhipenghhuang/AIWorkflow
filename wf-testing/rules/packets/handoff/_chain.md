# 流程链 · handoff

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：wf-testing
- **workflow**：`handoff`（协作交接）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 隔离边界（改本链不动别链）

- **本链专属**：`rules/packets/handoff/`（本文件、`_region-*`、节点包、`_orch.yaml`）；只重生成本链：`build_step_packets.py <包> <包> --only handoff`。
- **只读共享**：`rules/core/`、`rules/gates.md`、`rules/workflow.md`、`skills/`、`rules/templates/`；改共享层会影响所有链，须跑全包自检。
- **跨链需要时**：重新路由或 handoff；诊断确需只读对方 `_chain.md`，不打开对方节点包，读完回本链。

## 推进

口令只认本包 AGENTS 口令表。本链只排步骤与 `when`，不另列口令。 默认：入口步的产出与本步门完成后即停，并输出收尾骨架；不打开后续步骤包。 向后走，仅当口令是按链、继续、按计划执行，或本流程处于全链入口。

## 状态机

本 workflow 无额外子机。是否进入下一步只按「推进」。


## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `status` | 交接状态 | `—` | — | `rules/packets/handoff/status.md` |
| 2 | `compose` | 写交接单文档 | `—` | — | `rules/packets/handoff/compose.md` |
| 3 | `send` | 生成交接包 | `—` | — | `rules/packets/handoff/send.md` |
| 4 | `receive` | 接收与签收 | `—` | — | `rules/packets/handoff/receive.md` |
| 5 | `change_send` | 发送变更通知 | `—` | — | `rules/packets/handoff/change_send.md` |
| 6 | `change_receive` | 接收变更并适配 | `—` | — | `rules/packets/handoff/change_receive.md` |
| 7 | `replan` | 重规划 | `—` | — | `rules/packets/handoff/replan.md` |
| 8 | `wrap` | 收尾 | `—` | — | `rules/packets/handoff/wrap.md` |
| 9 | `commit` | 拟提交 | `—` | — | `rules/packets/handoff/commit.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次。是否进入下一步或下一区，只按上文「推进」。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
