# 子状态机 · defect/pull

> **嵌套闭环**：长链路中的一小段。进入本区读一次；区内仍 **一次只开一个** step packet。

## 定位

- **包轨**：产品
- **父流程**：`rules/packets/defect/_chain.md`
- **本区**：`pull` — 拉取分析
- **出口**：进入下一子机 `rules/packets/defect/_region-act.md`（处置回写）

## 区内步骤

| step | 名称 | when | 步骤包 |
| --- | --- | --- | --- |
| `preflight` | 平台配置与可用性 | `—` | `rules/packets/defect/preflight.md` |
| `pull` | 拉取与读取 | `—` | `rules/packets/defect/pull.md` |
| `source` | 来源识别 | `—` | `rules/packets/defect/source.md` |
| `analyze` | 分析 | `—` | `rules/packets/defect/analyze.md` |
| `decide` | 处置确认 | `—` | `rules/packets/defect/decide.md` |

## 区内纪律

1. 本区是闭环：按表推进；`when` 跳过则不打开该步包。
2. 当前 `packet=` 必须是区内某一步；离开本区前心跳刷新到下一步/下一区。
3. 技能只按**当前步骤包 §6** 打开→执行→回包；不在本区预读全部 skill。
4. 不要为「看全貌」打开其他区的全部步骤包。
