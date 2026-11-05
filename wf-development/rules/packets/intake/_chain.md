# 流程链 · intake

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：wf-development
- **workflow**：`intake`（变更吸收）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 入口

- `新文档` → step `scan`
- `新变化` → step `scan`
- `变更` → step `scan`
- `确认项` → step `scan`
- `收件箱` → step `scan`
- `变更吸收` → step `scan`

## 状态机

本 workflow 步骤较少，无额外子机；按阶段表逐步打开步骤包即可。


## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `scan` | 扫描新输入 | `—` | — | `rules/packets/intake/scan.md` |
| 2 | `classify` | 分类与登记 | `—` | — | `rules/packets/intake/classify.md` |
| 3 | `parse` | 解析与理解 | `—` | — | `rules/packets/intake/parse.md` |
| 4 | `impact` | 影响分析 | `—` | — | `rules/packets/intake/impact.md` |
| 5 | `absorb` | 局部更新 | `—` | — | `rules/packets/intake/absorb.md` |
| 6 | `report` | 吸收报告 | `—` | — | `rules/packets/intake/report.md` |
| 7 | `wrap` | 收尾 | `—` | — | `rules/packets/intake/wrap.md` |
| 8 | `commit` | 拟提交 | `—` | — | `rules/packets/intake/commit.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次；出区再进下一子机。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
