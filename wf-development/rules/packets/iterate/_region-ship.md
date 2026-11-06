# 子状态机 · iterate/ship

> **嵌套闭环**：长链路中的一小段。进入本区读一次；区内仍 **一次只开一个** step packet。

## 定位

- **包轨**：wf-development
- **父流程**：`rules/packets/iterate/_chain.md`
- **本区**：`ship` — 交付收尾
- **出口**：链末为 wrap/commit。是否进入只按父链「推进」。

## 区内步骤

| step | 名称 | when | 步骤包 |
| --- | --- | --- | --- |
| `deliver` | 提测与发布文档 | `has_qa_or_deploy_or_requested` | `rules/packets/iterate/deliver.md` |
| `release_handoff` | 发布交接 | `has_deploy` | `rules/packets/iterate/release_handoff.md` |
| `retro` | 迭代复盘 | `iteration_done_or_incident` | `rules/packets/iterate/retro.md` |
| `wrap` | 收尾 | `—` | `rules/packets/iterate/wrap.md` |
| `commit` | 拟提交 | `—` | `rules/packets/iterate/commit.md` |

## 区内纪律

1. 本区按表向后推进；单步口令在本步完成即停；`when` 不满足则不打开该步包。
2. 当前 `packet=` 必须是区内某一步；离开本区前心跳刷新到下一步/下一区。
3. 技能只按**当前步骤包 §6** 打开→执行→回包；不在本区预读全部 skill。
4. 不要为「看全貌」打开其他区的全部步骤包。
