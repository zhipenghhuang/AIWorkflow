# 流程链 · solo

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：开发
- **workflow**：`solo`（轻量开发（单人或小项目））
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 入口

- `轻量开发` → step `frame`
- `我有个想法` → step `frame`
- `想法落地` → step `frame`
- `做个` → step `frame`
- `快速做` → step `frame`
- `小项目` → step `frame`
- `轻量方案` → step `plan`
- `只出轻量方案` → step `plan`
- `轻量测试` → step `test`
- `帮我测一下` → step `test`
- `验收一下` → step `test`

## 状态机（父）→ 子机

长链路按**子状态机**切开：进某区先读该区 `_region-*`（一次），区内逐步推进；不要把整条父链步骤包一次读完。

| 子机 | 含义 | 地图 |
| --- | --- | --- |
| `frame` | 定义与方案 | `rules/packets/solo/_region-frame.md` |
| `build` | 建造验证 | `rules/packets/solo/_region-build.md` |
| `close` | 收尾 | `rules/packets/solo/_region-close.md` |

## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `frame` | 产品定义 | `new_product_or_unclear_idea` | `_region-frame` | `rules/packets/solo/frame.md` |
| 2 | `plan` | 一页方案卡 | `—` | `_region-frame` | `rules/packets/solo/plan.md` |
| 3 | `build` | 实施与自测 | `—` | `_region-build` | `rules/packets/solo/build.md` |
| 4 | `test` | 轻量测试 | `—` | `_region-build` | `rules/packets/solo/test.md` |
| 5 | `wrap` | 收尾 | `—` | `_region-close` | `rules/packets/solo/wrap.md` |
| 6 | `commit` | 拟提交 | `—` | `_region-close` | `rules/packets/solo/commit.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次；出区再进下一子机。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
