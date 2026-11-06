# 子状态机 · prd/write

> **嵌套闭环**：长链路中的一小段。进入本区读一次；区内仍 **一次只开一个** step packet。

## 定位

- **包轨**：wf-product
- **父流程**：`rules/packets/prd/_chain.md`
- **本区**：`write` — 撰写交接
- **出口**：下一区地图 `rules/packets/prd/_region-close.md`（收尾）。是否进入只按父链「推进」。

## 区内步骤

| step | 名称 | when | 步骤包 |
| --- | --- | --- | --- |
| `prd` | PRD 撰写 | `—` | `rules/packets/prd/prd.md` |
| `prototype` | 页面原型（条件） | `has_ui_requirement` | `rules/packets/prd/prototype.md` |
| `review` | PRD 评审与定稿 | `—` | `rules/packets/prd/review.md` |
| `handoff` | 需求交接包 | `prd_ready_for_handoff` | `rules/packets/prd/handoff.md` |

## 区内纪律

1. 默认入口步完成即停，不因本表自动进入下一步。仅按链、继续、按计划执行，或全链入口，才按表走向下一项。`when` 不满足则不打开该步包。
2. 当前 `packet=` 必须是区内某一步；离开本区前心跳刷新到下一步/下一区。
3. 技能只按**当前步骤包 §6** 打开→执行→回包；不在本区预读全部 skill。
4. 不要为「看全貌」打开其他区的全部步骤包。
