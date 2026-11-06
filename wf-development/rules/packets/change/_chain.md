# 流程链 · change

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：wf-development
- **workflow**：`change`（常规代码变更）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 隔离边界（改本链不动别链）

- **本链专属**：`rules/packets/change/`（本文件、`_region-*`、节点包、`_orch.yaml`）；只重生成本链：`build_step_packets.py <包> <包> --only change`。
- **只读共享**：`rules/core/`、`rules/gates.md`、`rules/workflow.md`、`skills/`、`rules/templates/`；改共享层会影响所有链，须跑全包自检。
- **跨链需要时**：重新路由或 handoff；诊断确需只读对方 `_chain.md`，不打开对方节点包，读完回本链。

## 推进

口令只认本包 AGENTS 口令表。本链只排步骤与 `when`，不另列口令。 从已命中的入口步沿阶段表向后；`when` 不满足则跳过且不打开该包。 口令明确只做单步（只出方案/只评审/代码评审/方案评审/只提测/只出清单/轻量方案）时，本步完成即停并输出收尾骨架；其余按表向后。 本步动作清单写明跳过、停止或改走他步时，以清单为准。

## 状态机（父）→ 子机

长链路按**子状态机**切开：进某区先读该区 `_region-*`（一次）。区内按表向后；不要把整条父链步骤包一次读完。

| 子机 | 含义 | 地图 |
| --- | --- | --- |
| `align` | 对齐与基线 | `rules/packets/change/_region-align.md` |
| `design` | 方案与计划 | `rules/packets/change/_region-design.md` |
| `build` | 实施与验证 | `rules/packets/change/_region-build.md` |
| `ship` | 交付收尾 | `rules/packets/change/_region-ship.md` |

## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `clarify` | 对齐与澄清 | `—` | `_region-align` | `rules/packets/change/clarify.md` |
| 2 | `analyze_input` | 产品资料解析与理解确认 | `has_product_docs_or_prototypes` | `_region-align` | `rules/packets/change/analyze_input.md` |
| 3 | `requirements` | 需求基线 | `new_feature_or_scope_change_or_requested` | `_region-align` | `rules/packets/change/requirements.md` |
| 4 | `design` | 方案与设计 | `new_feature_or_architecture_or_breaking_change_or_high_risk_or_requested` | `_region-design` | `rules/packets/change/design.md` |
| 5 | `review-docs` | 落地文档评审 | `landing_doc_review_required` | `_region-design` | `rules/packets/change/review-docs.md` |
| 6 | `plan` | 任务清单 | `multi_file_or_new_feature_or_requested` | `_region-design` | `rules/packets/change/plan.md` |
| 7 | `implement` | 实施 | `—` | `_region-build` | `rules/packets/change/implement.md` |
| 8 | `review` | 代码评审 | `review_required` | `_region-build` | `rules/packets/change/review.md` |
| 9 | `verify` | 自验与完成门 | `work_changed_or_requested` | `_region-build` | `rules/packets/change/verify.md` |
| 10 | `deliver` | 提测与发布文档 | `has_qa_or_deploy_or_requested` | `_region-ship` | `rules/packets/change/deliver.md` |
| 11 | `release_handoff` | 发布交接 | `has_deploy` | `_region-ship` | `rules/packets/change/release_handoff.md` |
| 12 | `wrap` | 收尾 | `—` | `_region-ship` | `rules/packets/change/wrap.md` |
| 13 | `commit` | 拟提交 | `—` | `_region-ship` | `rules/packets/change/commit.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次。是否进入下一步或下一区，只按上文「推进」。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
