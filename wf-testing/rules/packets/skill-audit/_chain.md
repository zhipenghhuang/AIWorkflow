# 流程链 · skill-audit

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：wf-testing
- **workflow**：`skill-audit`（能力与技能体检）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 隔离边界（改本链不动别链）

- **本链专属**：`rules/packets/skill-audit/`（本文件、`_region-*`、节点包、`_orch.yaml`）；只重生成本链：`build_step_packets.py <包> <包> --only skill-audit`。
- **只读共享**：`rules/core/`、`rules/gates.md`、`rules/workflow.md`、`skills/`、`rules/templates/`；改共享层会影响所有链，须跑全包自检。
- **跨链需要时**：重新路由或 handoff；诊断确需只读对方 `_chain.md`，不打开对方节点包，读完回本链。

## 推进

口令只认本包 AGENTS 口令表。本链只排步骤与 `when`，不另列口令。 默认：入口步的产出与本步门完成后即停，并输出收尾骨架；不打开后续步骤包。 向后走，仅当口令是按链、继续、按计划执行，或本流程处于全链入口。 因此本流程不走默认即停：从入口步沿阶段表走到链末；`when` 不满足则跳过且不打开该包。

## 状态机

本 workflow 无额外子机。是否进入下一步只按「推进」。


## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `scope` | 定范围与模式 | `—` | — | `rules/packets/skill-audit/scope.md` |
| 2 | `inventory` | 盘点 | `—` | — | `rules/packets/skill-audit/inventory.md` |
| 3 | `discover` | 生态检索 | `—` | — | `rules/packets/skill-audit/discover.md` |
| 4 | `fit` | 适配分析 | `—` | — | `rules/packets/skill-audit/fit.md` |
| 5 | `propose` | 出具建议 | `—` | — | `rules/packets/skill-audit/propose.md` |
| 6 | `apply` | 确认并应用 | `—` | — | `rules/packets/skill-audit/apply.md` |
| 7 | `wrap` | 收尾 | `—` | — | `rules/packets/skill-audit/wrap.md` |
| 8 | `commit` | 拟提交 | `—` | — | `rules/packets/skill-audit/commit.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次。是否进入下一步或下一区，只按上文「推进」。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
