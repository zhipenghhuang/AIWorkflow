# 流程链 · prd

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：产品
- **workflow**：`prd`（需求与 PRD）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 入口

- `收集需求` → step `discover`
- `需求洞察` → step `discover`
- `竞品分析` → step `discover`
- `学习竞品` → step `discover`
- `需求池` → step `discover`
- `分析客户需求` → step `discover`
- `需求调研` → step `discover`
- `客户访谈` → step `discover`
- `需求澄清` → step `discover`
- `竞品对标` → step `benchmark`
- `功能对标` → step `benchmark`
- `对标分析` → step `benchmark`
- `功能差距` → step `benchmark`
- `立项` → step `prioritize`
- `单需求立项` → step `prioritize`
- `排优先级` → step `prioritize`
- `写PRD` → step `prd`
- `写 PRD` → step `prd`
- `出PRD` → step `prd`
- `补PRD` → step `prd`

## 状态机（父）→ 子机

长链路按**子状态机**切开：进某区先读该区 `_region-*`（一次），区内逐步推进；不要把整条父链步骤包一次读完。

| 子机 | 含义 | 地图 |
| --- | --- | --- |
| `discover` | 发现与优先级 | `rules/packets/prd/_region-discover.md` |
| `write` | 撰写交接 | `rules/packets/prd/_region-write.md` |
| `close` | 收尾 | `rules/packets/prd/_region-close.md` |

## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `discover` | 需求洞察与需求池 | `—` | `_region-discover` | `rules/packets/prd/discover.md` |
| 2 | `benchmark` | 竞品对标与差距候选项 | `—` | `_region-discover` | `rules/packets/prd/benchmark.md` |
| 3 | `prioritize` | 优先级与立项 | `new_requirement_or_scope_change` | `_region-discover` | `rules/packets/prd/prioritize.md` |
| 4 | `prd` | PRD 撰写 | `—` | `_region-write` | `rules/packets/prd/prd.md` |
| 5 | `prototype` | 页面原型（条件） | `has_ui_requirement` | `_region-write` | `rules/packets/prd/prototype.md` |
| 6 | `review` | PRD 评审与定稿 | `—` | `_region-write` | `rules/packets/prd/review.md` |
| 7 | `handoff` | 需求交接包 | `prd_ready_for_handoff` | `_region-write` | `rules/packets/prd/handoff.md` |
| 8 | `wrap` | 收尾 | `—` | `_region-close` | `rules/packets/prd/wrap.md` |
| 9 | `commit` | 拟提交 | `—` | `_region-close` | `rules/packets/prd/commit.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次；出区再进下一子机。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
