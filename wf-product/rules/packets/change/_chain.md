# 流程链 · change

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：产品
- **workflow**：`change`（需求/问题受理与变更）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 入口

- `需求受理` → step `intake`
- `问题受理` → step `intake`
- `产品缺陷` → step `intake`
- `需求变更` → step `intake`
- `需求答疑` → step `intake`
- `开发不确定` → step `intake`
- `测试发现产品缺陷` → step `intake`

## 状态机（父）→ 子机

长链路按**子状态机**切开：进某区先读该区 `_region-*`（一次），区内逐步推进；不要把整条父链步骤包一次读完。

| 子机 | 含义 | 地图 |
| --- | --- | --- |
| `intake` | 受理评估 | `rules/packets/change/_region-intake.md` |
| `apply` | 落地验证 | `rules/packets/change/_region-apply.md` |
| `close` | 收尾 | `rules/packets/change/_region-close.md` |

## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `intake` | 受理与建档 | `—` | `_region-intake` | `rules/packets/change/intake.md` |
| 2 | `triage` | 分诊与定性 | `—` | `_region-intake` | `rules/packets/change/triage.md` |
| 3 | `new_requirement` | 新需求与优先级（条件） | `new_requirement` | `_region-intake` | `rules/packets/change/new_requirement.md` |
| 4 | `assess` | 影响评估 | `needs_impact_assessment` | `_region-intake` | `rules/packets/change/assess.md` |
| 5 | `decide` | 处置确认 | `decision_required` | `_region-intake` | `rules/packets/change/decide.md` |
| 6 | `apply` | 联动落地 | `change_apply_required` | `_region-apply` | `rules/packets/change/apply.md` |
| 7 | `review` | 重审（条件） | `substantive_change` | `_region-apply` | `rules/packets/change/review.md` |
| 8 | `verify` | 验证与关闭 | `needs_linked_update` | `_region-apply` | `rules/packets/change/verify.md` |
| 9 | `wrap` | 收尾 | `—` | `_region-close` | `rules/packets/change/wrap.md` |
| 10 | `commit` | 拟提交 | `—` | `_region-close` | `rules/packets/change/commit.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次；出区再进下一子机。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
