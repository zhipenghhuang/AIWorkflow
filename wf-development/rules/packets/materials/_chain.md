# 流程链 · materials

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：wf-development
- **workflow**：`materials`（开发权威文档库发布）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 入口

- `导出项目文档` → step `select`
- `生成资料库` → step `select`
- `生成交付资料` → step `select`
- `发资料` → step `select`
- `发项目文档` → step `select`
- `打包项目文档` → step `select`

## 状态机

本 workflow 步骤较少，无额外子机；按阶段表逐步打开步骤包即可。


## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `select` | 选择版本与范围 | `—` | — | `rules/packets/materials/select.md` |
| 2 | `sync` | 同步权威文档 | `—` | — | `rules/packets/materials/sync.md` |
| 3 | `index` | 版本说明、索引与校验 | `—` | — | `rules/packets/materials/index.md` |
| 4 | `wrap` | 收尾 | `—` | — | `rules/packets/materials/wrap.md` |
| 5 | `commit` | 拟提交 | `—` | — | `rules/packets/materials/commit.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次；出区再进下一子机。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
