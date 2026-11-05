# 流程链 · new-product

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：产品
- **workflow**：`new-product`（新产品 0→1）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 入口

- `启动新产品` → step `discover`
- `新项目` → step `discover`
- `从0到1` → step `discover`
- `产品立项` → step `discover`

## 状态机（父）→ 子机

长链路按**子状态机**切开：进某区先读该区 `_region-*`（一次），区内逐步推进；不要把整条父链步骤包一次读完。

| 子机 | 含义 | 地图 |
| --- | --- | --- |
| `define` | 发现定义 | `rules/packets/new-product/_region-define.md` |
| `build` | PRD交付 | `rules/packets/new-product/_region-build.md` |
| `close` | 收尾 | `rules/packets/new-product/_region-close.md` |

## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `discover` | 发现与机会评估 | `—` | `_region-define` | `rules/packets/new-product/discover.md` |
| 2 | `go` | 立项评审 | `—` | `_region-define` | `rules/packets/new-product/go.md` |
| 3 | `define` | 产品定义与计划 | `go_decision_go` | `_region-define` | `rules/packets/new-product/define.md` |
| 4 | `prd` | 需求定义（PRD） | `go_decision_go` | `_region-build` | `rules/packets/new-product/prd.md` |
| 5 | `deliver` | 交付与验收 | `go_decision_go` | `_region-build` | `rules/packets/new-product/deliver.md` |
| 6 | `launch` | 上市与复盘 | `go_decision_go` | `_region-build` | `rules/packets/new-product/launch.md` |
| 7 | `wrap` | 收尾 | `—` | `_region-close` | `rules/packets/new-product/wrap.md` |
| 8 | `commit` | 拟提交 | `—` | `_region-close` | `rules/packets/new-product/commit.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次；出区再进下一子机。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
