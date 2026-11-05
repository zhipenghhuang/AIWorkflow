# 子状态机 · new-product/define

> **嵌套闭环**：长链路中的一小段。进入本区读一次；区内仍 **一次只开一个** step packet。

## 定位

- **包轨**：产品
- **父流程**：`rules/packets/new-product/_chain.md`
- **本区**：`define` — 发现定义
- **出口**：进入下一子机 `rules/packets/new-product/_region-build.md`（PRD交付）

## 区内步骤

| step | 名称 | when | 步骤包 |
| --- | --- | --- | --- |
| `discover` | 发现与机会评估 | `—` | `rules/packets/new-product/discover.md` |
| `go` | 立项评审 | `—` | `rules/packets/new-product/go.md` |
| `define` | 产品定义与计划 | `go_decision_go` | `rules/packets/new-product/define.md` |

## 区内纪律

1. 本区是闭环：按表推进；`when` 跳过则不打开该步包。
2. 当前 `packet=` 必须是区内某一步；离开本区前心跳刷新到下一步/下一区。
3. 技能只按**当前步骤包 §6** 打开→执行→回包；不在本区预读全部 skill。
4. 不要为「看全貌」打开其他区的全部步骤包。
