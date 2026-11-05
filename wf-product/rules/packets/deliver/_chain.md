# 流程链 · deliver

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：产品
- **workflow**：`deliver`（交付与验收）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 入口

- `排期` → step `schedule`
- `迭代规划` → step `schedule`
- `交付计划` → step `schedule`
- `任务拆解` → step `schedule`
- `交付计划评审` → step `review-plan-deliver`
- `评审交付计划` → step `review-plan-deliver`
- `交付跟进` → step `followup`
- `风险升级` → step `followup`
- `UAT` → step `uat`
- `验收` → step `uat`
- `发布` → step `release`
- `上线检查` → step `release`
- `复盘` → step `release`

## 状态机（父）→ 子机

长链路按**子状态机**切开：进某区先读该区 `_region-*`（一次），区内逐步推进；不要把整条父链步骤包一次读完。

| 子机 | 含义 | 地图 |
| --- | --- | --- |
| `prep` | 排期跟进 | `rules/packets/deliver/_region-prep.md` |
| `ship` | 验收发布 | `rules/packets/deliver/_region-ship.md` |
| `close` | 收尾 | `rules/packets/deliver/_region-close.md` |

## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `schedule` | 排期与交接 | `—` | `_region-prep` | `rules/packets/deliver/schedule.md` |
| 2 | `review-plan-deliver` | 交付计划评审 | `—` | `_region-prep` | `rules/packets/deliver/review-plan-deliver.md` |
| 3 | `followup` | 交付跟进 | `—` | `_region-prep` | `rules/packets/deliver/followup.md` |
| 4 | `uat` | UAT 验收 | `has_uat` | `_region-ship` | `rules/packets/deliver/uat.md` |
| 5 | `release` | 发布与复盘 | `—` | `_region-ship` | `rules/packets/deliver/release.md` |
| 6 | `wrap` | 收尾 | `—` | `_region-close` | `rules/packets/deliver/wrap.md` |
| 7 | `commit` | 拟提交 | `—` | `_region-close` | `rules/packets/deliver/commit.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次；出区再进下一子机。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
