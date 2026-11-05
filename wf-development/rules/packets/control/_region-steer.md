# 子状态机 · control/steer

> **嵌套闭环**：长链路中的一小段。进入本区读一次；区内仍 **一次只开一个** step packet。

## 定位

- **包轨**：开发
- **父流程**：`rules/packets/control/_chain.md`
- **本区**：`steer` — 总控推进
- **出口**：进入下一子机 `rules/packets/control/_region-close.md`（收尾）

## 区内步骤

| step | 名称 | when | 步骤包 |
| --- | --- | --- | --- |
| `init` | 初始化开发计划 | `—` | `rules/packets/control/init.md` |
| `run` | 按计划执行 | `—` | `rules/packets/control/run.md` |
| `sync` | 同步阶段与证据 | `—` | `rules/packets/control/sync.md` |
| `check` | 阶段门检查 | `—` | `rules/packets/control/check.md` |
| `next` | 下一步建议 | `—` | `rules/packets/control/next.md` |

## 区内纪律

1. 本区是闭环：按表推进；`when` 跳过则不打开该步包。
2. 当前 `packet=` 必须是区内某一步；离开本区前心跳刷新到下一步/下一区。
3. 技能只按**当前步骤包 §6** 打开→执行→回包；不在本区预读全部 skill。
4. 不要为「看全貌」打开其他区的全部步骤包。
