# 流程链 · showcase

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：产品
- **workflow**：`showcase`（产品展示与介绍）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 入口

- `准备演示` → step `audience`
- `客户演示` → step `audience`
- `产品介绍` → step `audience`
- `产品汇报` → step `audience`
- `演示彩排` → step `dryrun`
- `一页纸` → step `materials`
- `Deck` → step `materials`
- `用户手册` → step `docs`
- `快速开始` → step `docs`
- `FAQ` → step `docs`
- `发布说明` → step `docs`
- `培训材料` → step `docs`

## 状态机（父）→ 子机

长链路按**子状态机**切开：进某区先读该区 `_region-*`（一次），区内逐步推进；不要把整条父链步骤包一次读完。

| 子机 | 含义 | 地图 |
| --- | --- | --- |
| `story` | 受众故事 | `rules/packets/showcase/_region-story.md` |
| `pack` | 材料发布 | `rules/packets/showcase/_region-pack.md` |
| `close` | 收尾 | `rules/packets/showcase/_region-close.md` |

## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `audience` | 受众与目标 | `—` | `_region-story` | `rules/packets/showcase/audience.md` |
| 2 | `story` | 故事线与流程图 | `—` | `_region-story` | `rules/packets/showcase/story.md` |
| 3 | `demo` | 演示脚本 | `—` | `_region-story` | `rules/packets/showcase/demo.md` |
| 4 | `environment` | Demo 环境与数据 | `—` | `_region-story` | `rules/packets/showcase/environment.md` |
| 5 | `materials` | 展示材料 | `—` | `_region-pack` | `rules/packets/showcase/materials.md` |
| 6 | `docs` | 用户文档 | `docs_requested` | `_region-pack` | `rules/packets/showcase/docs.md` |
| 7 | `dryrun` | 彩排与反馈 | `demo_needs_dryrun` | `_region-pack` | `rules/packets/showcase/dryrun.md` |
| 8 | `publish` | 对外确认 | `materials_for_external` | `_region-pack` | `rules/packets/showcase/publish.md` |
| 9 | `wrap` | 收尾 | `—` | `_region-close` | `rules/packets/showcase/wrap.md` |
| 10 | `commit` | 拟提交 | `—` | `_region-close` | `rules/packets/showcase/commit.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次；出区再进下一子机。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
