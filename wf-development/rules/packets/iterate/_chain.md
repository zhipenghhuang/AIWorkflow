# 流程链 · iterate

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：wf-development
- **workflow**：`iterate`（迭代交付）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 隔离边界（改本链不动别链）

- **本链专属**：`rules/packets/iterate/`（本文件、`_region-*`、节点包、`_orch.yaml`）；只重生成本链：`build_step_packets.py <包> <包> --only iterate`。
- **只读共享**：`rules/core/`、`rules/gates.md`、`rules/workflow.md`、`skills/`、`rules/templates/`；改共享层会影响所有链，须跑全包自检。
- **跨链需要时**：重新路由或 handoff；诊断确需只读对方 `_chain.md`，不打开对方节点包，读完回本链。

## 推进

口令只认本包 AGENTS 口令表。本链只排步骤与 `when`，不另列口令。 从已命中的入口步沿阶段表向后；`when` 不满足则跳过且不打开该包。 口令明确只做单步（只出方案/只评审/代码评审/方案评审/只提测/只出清单/轻量方案）时，本步完成即停并输出收尾骨架；其余按表向后。 本步动作清单写明跳过、停止或改走他步时，以清单为准。

## 状态机（父）→ 子机

长链路按**子状态机**切开：进某区先读该区 `_region-*`（一次）。区内按表向后；不要把整条父链步骤包一次读完。

| 子机 | 含义 | 地图 |
| --- | --- | --- |
| `plan` | 计划确认 | `rules/packets/iterate/_region-plan.md` |
| `build` | 实施验证 | `rules/packets/iterate/_region-build.md` |
| `ship` | 交付收尾 | `rules/packets/iterate/_region-ship.md` |

## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `precheck` | 前置检查 | `—` | `_region-plan` | `rules/packets/iterate/precheck.md` |
| 2 | `plan` | 读方案与拆清单 | `—` | `_region-plan` | `rules/packets/iterate/plan.md` |
| 3 | `confirm` | 确认清单与节奏 | `implementation_required` | `_region-plan` | `rules/packets/iterate/confirm.md` |
| 4 | `implement` | 实施与定向自验 | `implementation_required` | `_region-build` | `rules/packets/iterate/implement.md` |
| 5 | `review` | 代码评审 | `review_required` | `_region-build` | `rules/packets/iterate/review.md` |
| 6 | `gates` | 全量门禁与文档同步 | `implementation_required` | `_region-build` | `rules/packets/iterate/gates.md` |
| 7 | `deliver` | 提测与发布文档 | `has_qa_or_deploy_or_requested` | `_region-ship` | `rules/packets/iterate/deliver.md` |
| 8 | `release_handoff` | 发布交接 | `has_deploy` | `_region-ship` | `rules/packets/iterate/release_handoff.md` |
| 9 | `retro` | 迭代复盘 | `iteration_done_or_incident` | `_region-ship` | `rules/packets/iterate/retro.md` |
| 10 | `wrap` | 收尾 | `—` | `_region-ship` | `rules/packets/iterate/wrap.md` |
| 11 | `commit` | 拟提交 | `—` | `_region-ship` | `rules/packets/iterate/commit.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次。是否进入下一步或下一区，只按上文「推进」。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
