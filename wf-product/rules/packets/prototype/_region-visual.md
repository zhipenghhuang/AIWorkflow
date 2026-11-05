# 子状态机 · prototype/visual

> **嵌套闭环**：长链路中的一小段。进入本区读一次；区内仍 **一次只开一个** step packet。

## 定位

- **包轨**：产品
- **父流程**：`rules/packets/prototype/_chain.md`
- **本区**：`visual` — 视觉与评审
- **出口**：进入下一子机 `rules/packets/prototype/_region-hand.md`（交接收尾）

## 区内步骤

| step | 名称 | when | 步骤包 |
| --- | --- | --- | --- |
| `visual` | 视觉方向与设计系统 | `—` | `rules/packets/prototype/visual.md` |
| `hi-fi` | 高保真可点击原型 | `—` | `rules/packets/prototype/hi-fi.md` |
| `review` | 设计评审 | `—` | `rules/packets/prototype/review.md` |
| `usability` | 可用性走查 | `—` | `rules/packets/prototype/usability.md` |

## 区内纪律

1. 本区是闭环：按表推进；`when` 跳过则不打开该步包。
2. 当前 `packet=` 必须是区内某一步；离开本区前心跳刷新到下一步/下一区。
3. 技能只按**当前步骤包 §6** 打开→执行→回包；不在本区预读全部 skill。
4. 不要为「看全貌」打开其他区的全部步骤包。
