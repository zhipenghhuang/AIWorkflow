# 子状态机 · iterate/plan

> **嵌套闭环**：长链路中的一小段。进入本区读一次；区内仍 **一次只开一个** step packet。

## 定位

- **包轨**：wf-development
- **父流程**：`rules/packets/iterate/_chain.md`
- **本区**：`plan` — 计划确认
- **出口**：下一区地图 `rules/packets/iterate/_region-build.md`（实施验证）。是否进入只按父链「推进」。

## 区内步骤

| step | 名称 | when | 步骤包 |
| --- | --- | --- | --- |
| `precheck` | 前置检查 | `—` | `rules/packets/iterate/precheck.md` |
| `plan` | 读方案与拆清单 | `—` | `rules/packets/iterate/plan.md` |
| `confirm` | 确认清单与节奏 | `implementation_required` | `rules/packets/iterate/confirm.md` |

## 区内纪律

1. 本区按表向后推进；单步口令在本步完成即停；`when` 不满足则不打开该步包。
2. 当前 `packet=` 必须是区内某一步；离开本区前心跳刷新到下一步/下一区。
3. 技能只按**当前步骤包 §6** 打开→执行→回包；不在本区预读全部 skill。
4. 不要为「看全貌」打开其他区的全部步骤包。
