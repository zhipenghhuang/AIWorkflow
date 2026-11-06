# 子状态机 · iterate/build

> **嵌套闭环**：长链路中的一小段。进入本区读一次；区内仍 **一次只开一个** step packet。

## 定位

- **包轨**：wf-development
- **父流程**：`rules/packets/iterate/_chain.md`
- **本区**：`build` — 实施验证
- **出口**：下一区地图 `rules/packets/iterate/_region-ship.md`（交付收尾）。是否进入只按父链「推进」。

## 区内步骤

| step | 名称 | when | 步骤包 |
| --- | --- | --- | --- |
| `implement` | 实施与定向自验 | `implementation_required` | `rules/packets/iterate/implement.md` |
| `review` | 代码评审 | `review_required` | `rules/packets/iterate/review.md` |
| `gates` | 全量门禁与文档同步 | `implementation_required` | `rules/packets/iterate/gates.md` |

## 区内纪律

1. 本区按表向后推进；单步口令在本步完成即停；`when` 不满足则不打开该步包。
2. 当前 `packet=` 必须是区内某一步；离开本区前心跳刷新到下一步/下一区。
3. 技能只按**当前步骤包 §6** 打开→执行→回包；不在本区预读全部 skill。
4. 不要为「看全貌」打开其他区的全部步骤包。
