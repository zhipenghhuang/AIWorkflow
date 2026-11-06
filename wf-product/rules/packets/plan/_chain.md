# 流程链 · plan

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：wf-product
- **workflow**：`plan`（产品计划）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 隔离边界（改本链不动别链）

- **本链专属**：`rules/packets/plan/`（本文件、`_region-*`、节点包、`_orch.yaml`）；只重生成本链：`build_step_packets.py <包> <包> --only plan`。
- **只读共享**：`rules/core/`、`rules/gates.md`、`rules/workflow.md`、`skills/`、`rules/templates/`；改共享层会影响所有链，须跑全包自检。
- **跨链需要时**：重新路由或 handoff；诊断确需只读对方 `_chain.md`，不打开对方节点包，读完回本链。

## 推进

口令只认本包 AGENTS 口令表。本链只排步骤与 `when`，不另列口令。 默认：入口步的产出与本步门完成后即停，并输出收尾骨架；不打开后续步骤包。 向后走，仅当口令是按链、继续、按计划执行，或本流程处于全链入口。

## 状态机（父）→ 子机

长链路按**子状态机**切开：进某区先读该区 `_region-*`（一次）。区内是否进入下一步只按上文「推进」；不要把整条父链步骤包一次读完。

| 子机 | 含义 | 地图 |
| --- | --- | --- |
| `shape` | 目标范围 | `rules/packets/plan/_region-shape.md` |
| `publish` | 发布下一步 | `rules/packets/plan/_region-publish.md` |
| `close` | 收尾 | `rules/packets/plan/_region-close.md` |

## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `goals` | 目标与指标 | `—` | `_region-shape` | `rules/packets/plan/goals.md` |
| 2 | `roadmap` | 路线图与优先级 | `—` | `_region-shape` | `rules/packets/plan/roadmap.md` |
| 3 | `scope` | 本期范围与里程碑 | `—` | `_region-shape` | `rules/packets/plan/scope.md` |
| 4 | `review-plan` | 计划文档评审 | `—` | `_region-shape` | `rules/packets/plan/review-plan.md` |
| 5 | `publish` | 落盘与索引 | `—` | `_region-publish` | `rules/packets/plan/publish.md` |
| 6 | `next` | 计划续跑 | `—` | `_region-publish` | `rules/packets/plan/next.md` |
| 7 | `wrap` | 收尾 | `—` | `_region-close` | `rules/packets/plan/wrap.md` |
| 8 | `commit` | 拟提交 | `—` | `_region-close` | `rules/packets/plan/commit.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次。是否进入下一步或下一区，只按上文「推进」。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
