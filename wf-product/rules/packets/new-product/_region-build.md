# 子状态机 · new-product/build

> **嵌套闭环**：长链路中的一小段。进入本区读一次；区内仍 **一次只开一个** step packet。

## 定位

- **包轨**：wf-product
- **父流程**：`rules/packets/new-product/_chain.md`
- **本区**：`build` — PRD交付
- **出口**：下一区地图 `rules/packets/new-product/_region-close.md`（收尾）。是否进入只按父链「推进」。

## 区内步骤

| step | 名称 | when | 步骤包 |
| --- | --- | --- | --- |
| `prd` | 需求定义（PRD） | `go_decision_go` | `rules/packets/new-product/prd.md` |
| `deliver` | 交付与验收 | `go_decision_go` | `rules/packets/new-product/deliver.md` |
| `launch` | 上市与复盘 | `go_decision_go` | `rules/packets/new-product/launch.md` |

## 区内纪律

1. 默认入口步完成即停，不因本表自动进入下一步。仅按链、继续、按计划执行，或全链入口，才按表走向下一项。`when` 不满足则不打开该步包。
2. 当前 `packet=` 必须是区内某一步；离开本区前心跳刷新到下一步/下一区。
3. 技能只按**当前步骤包 §6** 打开→执行→回包；不在本区预读全部 skill。
4. 不要为「看全貌」打开其他区的全部步骤包。
