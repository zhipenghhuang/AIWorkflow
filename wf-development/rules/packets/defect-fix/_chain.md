# 流程链 · defect-fix

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：wf-development
- **workflow**：`defect-fix`（缺陷修复协作）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 隔离边界（改本链不动别链）

- **本链专属**：`rules/packets/defect-fix/`（本文件、`_region-*`、节点包、`_orch.yaml`）；只重生成本链：`build_step_packets.py <包> <包> --only defect-fix`。
- **只读共享**：`rules/core/`、`rules/gates.md`、`rules/workflow.md`、`skills/`、`rules/templates/`；改共享层会影响所有链，须跑全包自检。
- **跨链需要时**：重新路由或 handoff；诊断确需只读对方 `_chain.md`，不打开对方节点包，读完回本链。

## 推进

口令只认本包 AGENTS 口令表。本链只排步骤与 `when`，不另列口令。 从已命中的入口步沿阶段表向后；`when` 不满足则跳过且不打开该包。 口令明确只做单步（只出方案/只评审/代码评审/方案评审/只提测/只出清单/轻量方案）时，本步完成即停并输出收尾骨架；其余按表向后。 本步动作清单写明跳过、停止或改走他步时，以清单为准。

## 状态机（父）→ 子机

长链路按**子状态机**切开：进某区先读该区 `_region-*`（一次）。区内按表向后；不要把整条父链步骤包一次读完。

| 子机 | 含义 | 地图 |
| --- | --- | --- |
| `intake` | 接入与分类 | `rules/packets/defect-fix/_region-intake.md` |
| `product` | 产品协作闭环 | `rules/packets/defect-fix/_region-product.md` |
| `fix` | 修复与门禁 | `rules/packets/defect-fix/_region-fix.md` |
| `close` | 关闭与收尾 | `rules/packets/defect-fix/_region-close.md` |

## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `preflight` | 平台可用性 | `—` | `_region-intake` | `rules/packets/defect-fix/preflight.md` |
| 2 | `pull` | 拉取与归组 | `—` | `_region-intake` | `rules/packets/defect-fix/pull.md` |
| 3 | `triage` | 分类与处置 | `—` | `_region-intake` | `rules/packets/defect-fix/triage.md` |
| 4 | `assess_product` | 产品缺陷评估 | `product_defect` | `_region-product` | `rules/packets/defect-fix/assess_product.md` |
| 5 | `handoff_product` | 评估单提交产品 | `product_defect` | `_region-product` | `rules/packets/defect-fix/handoff_product.md` |
| 6 | `await_product` | 等待产品处置 | `product_defect` | `_region-product` | `rules/packets/defect-fix/await_product.md` |
| 7 | `product_decision` | 产品处置读取 | `product_decision_received` | `_region-product` | `rules/packets/defect-fix/product_decision.md` |
| 8 | `align` | 文档对齐 | `product_decision_requires_alignment` | `_region-product` | `rules/packets/defect-fix/align.md` |
| 9 | `fix` | 红证与修复 | `implementation_required` | `_region-fix` | `rules/packets/defect-fix/fix.md` |
| 10 | `clarify` | 澄清/非缺陷回写 | `need_clarification` | `_region-fix` | `rules/packets/defect-fix/clarify.md` |
| 11 | `gates` | 门禁 | `has_code_change` | `_region-fix` | `rules/packets/defect-fix/gates.md` |
| 12 | `menu` | 总结菜单 | `implementation_required` | `_region-fix` | `rules/packets/defect-fix/menu.md` |
| 13 | `close` | 提交推送部署回写 | `implementation_required` | `_region-close` | `rules/packets/defect-fix/close.md` |
| 14 | `postrelease` | 发布后验证 | `has_deployed` | `_region-close` | `rules/packets/defect-fix/postrelease.md` |
| 15 | `retro` | 复盘 | `recurring_defect_or_incident` | `_region-close` | `rules/packets/defect-fix/retro.md` |
| 16 | `wrap` | 收尾 | `not_awaiting_product` | `_region-close` | `rules/packets/defect-fix/wrap.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次。是否进入下一步或下一区，只按上文「推进」。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
