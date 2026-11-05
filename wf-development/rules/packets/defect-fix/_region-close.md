# 子状态机 · defect-fix/close

> **嵌套闭环**：长链路中的一小段。进入本区读一次；区内仍 **一次只开一个** step packet。

## 定位

- **包轨**：开发
- **父流程**：`rules/packets/defect-fix/_chain.md`
- **本区**：`close` — 关闭与收尾
- **出口**：本 workflow 收尾或出口 step（wrap/commit）

## 区内步骤

| step | 名称 | when | 步骤包 |
| --- | --- | --- | --- |
| `close` | 提交推送部署回写 | `implementation_required` | `rules/packets/defect-fix/close.md` |
| `postrelease` | 发布后验证 | `has_deployed` | `rules/packets/defect-fix/postrelease.md` |
| `retro` | 复盘 | `recurring_defect_or_incident` | `rules/packets/defect-fix/retro.md` |
| `wrap` | 收尾 | `not_awaiting_product` | `rules/packets/defect-fix/wrap.md` |

## 区内纪律

1. 本区是闭环：按表推进；`when` 跳过则不打开该步包。
2. 当前 `packet=` 必须是区内某一步；离开本区前心跳刷新到下一步/下一区。
3. 技能只按**当前步骤包 §6** 打开→执行→回包；不在本区预读全部 skill。
4. 不要为「看全貌」打开其他区的全部步骤包。
