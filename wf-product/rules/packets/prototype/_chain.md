# 流程链 · prototype

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：产品
- **workflow**：`prototype`（页面原型设计）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 入口

- `画原型` → step `context`
- `页面原型` → step `context`
- `原型设计` → step `context`
- `设计简报` → step `context`
- `设计策略` → step `context`
- `线框图` → step `wireframe`
- `UI设计` → step `visual`
- `高保真原型` → step `hi-fi`
- `设计评审` → step `review`
- `UI走查` → step `usability`
- `设计走查` → step `usability`
- `开发交接` → step `handoff`

## 状态机（父）→ 子机

长链路按**子状态机**切开：进某区先读该区 `_region-*`（一次），区内逐步推进；不要把整条父链步骤包一次读完。

| 子机 | 含义 | 地图 |
| --- | --- | --- |
| `shape` | 结构与线框 | `rules/packets/prototype/_region-shape.md` |
| `visual` | 视觉与评审 | `rules/packets/prototype/_region-visual.md` |
| `hand` | 交接收尾 | `rules/packets/prototype/_region-hand.md` |

## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `context` | 项目情境与参考基准 | `—` | `_region-shape` | `rules/packets/prototype/context.md` |
| 2 | `ia` | 信息架构与页面清单 | `—` | `_region-shape` | `rules/packets/prototype/ia.md` |
| 3 | `wireframe` | 低保真线框 | `—` | `_region-shape` | `rules/packets/prototype/wireframe.md` |
| 4 | `visual` | 视觉方向与设计系统 | `—` | `_region-visual` | `rules/packets/prototype/visual.md` |
| 5 | `hi-fi` | 高保真可点击原型 | `—` | `_region-visual` | `rules/packets/prototype/hi-fi.md` |
| 6 | `engineering` | 工程化与可访问性 | `—` | `_region-shape` | `rules/packets/prototype/engineering.md` |
| 7 | `review` | 设计评审 | `—` | `_region-visual` | `rules/packets/prototype/review.md` |
| 8 | `usability` | 可用性走查 | `—` | `_region-visual` | `rules/packets/prototype/usability.md` |
| 9 | `handoff` | 开发交接 | `—` | `_region-hand` | `rules/packets/prototype/handoff.md` |
| 10 | `wrap` | 收尾 | `—` | `_region-hand` | `rules/packets/prototype/wrap.md` |
| 11 | `commit` | 拟提交 | `—` | `_region-hand` | `rules/packets/prototype/commit.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次；出区再进下一子机。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
