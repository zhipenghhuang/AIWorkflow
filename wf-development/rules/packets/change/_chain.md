# 流程链 · change

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：开发
- **workflow**：`change`（常规代码变更）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 入口

- `常规变更` → step `clarify`
- `澄清` → step `clarify`
- `需求澄清` → step `clarify`
- `提交` → step `commit`
- `推送` → step `commit`
- `分析PRD` → step `analyze_input`
- `分析 PRD` → step `analyze_input`
- `理解需求` → step `analyze_input`
- `解析原型` → step `analyze_input`
- `出方案` → step `design`
- `方案评审` → step `review-docs`
- `文档评审` → step `review-docs`
- `设计文档评审` → step `review-docs`
- `代码评审` → step `review`
- `提测` → step `deliver`
- `提测单` → step `deliver`
- `发布说明` → step `deliver`
- `回滚预案` → step `deliver`

## 状态机（父）→ 子机

长链路按**子状态机**切开：进某区先读该区 `_region-*`（一次），区内逐步推进；不要把整条父链步骤包一次读完。

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
| 9 | `verify` | 自验与完成门 | `code_changed_or_requested` | `_region-build` | `rules/packets/change/verify.md` |
| 10 | `deliver` | 提测与发布文档 | `has_qa_or_deploy_or_requested` | `_region-ship` | `rules/packets/change/deliver.md` |
| 11 | `release_handoff` | 发布交接 | `has_deploy` | `_region-ship` | `rules/packets/change/release_handoff.md` |
| 12 | `wrap` | 收尾 | `—` | `_region-ship` | `rules/packets/change/wrap.md` |
| 13 | `commit` | 拟提交 | `—` | `_region-ship` | `rules/packets/change/commit.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次；出区再进下一子机。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
