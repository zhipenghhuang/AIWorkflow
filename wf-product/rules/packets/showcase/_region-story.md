# 子状态机 · showcase/story

> **嵌套闭环**：长链路中的一小段。进入本区读一次；区内仍 **一次只开一个** step packet。

## 定位

- **包轨**：wf-product
- **父流程**：`rules/packets/showcase/_chain.md`
- **本区**：`story` — 受众故事
- **出口**：下一区地图 `rules/packets/showcase/_region-pack.md`（材料发布）。是否进入只按父链「推进」。

## 区内步骤

| step | 名称 | when | 步骤包 |
| --- | --- | --- | --- |
| `audience` | 受众与目标 | `—` | `rules/packets/showcase/audience.md` |
| `story` | 故事线与流程图 | `—` | `rules/packets/showcase/story.md` |
| `demo` | 演示脚本 | `—` | `rules/packets/showcase/demo.md` |
| `environment` | Demo 环境与数据 | `—` | `rules/packets/showcase/environment.md` |

## 区内纪律

1. 默认入口步完成即停，不因本表自动进入下一步。仅按链、继续、按计划执行，或全链入口，才按表走向下一项。`when` 不满足则不打开该步包。
2. 当前 `packet=` 必须是区内某一步；离开本区前心跳刷新到下一步/下一区。
3. 技能只按**当前步骤包 §6** 打开→执行→回包；不在本区预读全部 skill。
4. 不要为「看全貌」打开其他区的全部步骤包。
