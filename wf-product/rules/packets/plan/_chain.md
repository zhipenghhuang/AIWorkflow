# 流程链 · plan

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：产品
- **workflow**：`plan`（产品计划）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 入口

- `产品计划` → step `goals`
- `产品规划` → step `goals`
- `路线图` → step `roadmap`
- `Roadmap` → step `roadmap`
- `版本规划` → step `roadmap`
- `下季度做什么` → step `roadmap`
- `下个月做什么` → step `roadmap`
- `排优先级（版本级）` → step `roadmap`
- `计划评审` → step `review-plan`
- `计划文档评审` → step `review-plan`
- `按产品计划执行` → step `next`
- `继续` → step `next`
- `下一步` → step `next`
- `当前状态` → step `next`

## 状态机（父）→ 子机

长链路按**子状态机**切开：进某区先读该区 `_region-*`（一次），区内逐步推进；不要把整条父链步骤包一次读完。

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
2. 有子机：进区读 `_region-*` 一次；出区再进下一子机。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
