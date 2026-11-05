# 子状态机 · change/intake

> **嵌套闭环**：长链路中的一小段。进入本区读一次；区内仍 **一次只开一个** step packet。

## 定位

- **包轨**：产品
- **父流程**：`rules/packets/change/_chain.md`
- **本区**：`intake` — 受理评估
- **出口**：进入下一子机 `rules/packets/change/_region-apply.md`（落地验证）

## 区内步骤

| step | 名称 | when | 步骤包 |
| --- | --- | --- | --- |
| `intake` | 受理与建档 | `—` | `rules/packets/change/intake.md` |
| `triage` | 分诊与定性 | `—` | `rules/packets/change/triage.md` |
| `new_requirement` | 新需求与优先级（条件） | `new_requirement` | `rules/packets/change/new_requirement.md` |
| `assess` | 影响评估 | `needs_impact_assessment` | `rules/packets/change/assess.md` |
| `decide` | 处置确认 | `decision_required` | `rules/packets/change/decide.md` |

## 区内纪律

1. 本区是闭环：按表推进；`when` 跳过则不打开该步包。
2. 当前 `packet=` 必须是区内某一步；离开本区前心跳刷新到下一步/下一区。
3. 技能只按**当前步骤包 §6** 打开→执行→回包；不在本区预读全部 skill。
4. 不要为「看全貌」打开其他区的全部步骤包。
