# 子状态机 · change/align

> **嵌套闭环**：长链路中的一小段。进入本区读一次；区内仍 **一次只开一个** step packet。

## 定位

- **包轨**：wf-development
- **父流程**：`rules/packets/change/_chain.md`
- **本区**：`align` — 对齐与基线
- **出口**：进入下一子机 `rules/packets/change/_region-design.md`（方案与计划）

## 区内步骤

| step | 名称 | when | 步骤包 |
| --- | --- | --- | --- |
| `clarify` | 对齐与澄清 | `—` | `rules/packets/change/clarify.md` |
| `analyze_input` | 产品资料解析与理解确认 | `has_product_docs_or_prototypes` | `rules/packets/change/analyze_input.md` |
| `requirements` | 需求基线 | `new_feature_or_scope_change_or_requested` | `rules/packets/change/requirements.md` |

## 区内纪律

1. 本区是闭环：按表推进；`when` 跳过则不打开该步包。
2. 当前 `packet=` 必须是区内某一步；离开本区前心跳刷新到下一步/下一区。
3. 技能只按**当前步骤包 §6** 打开→执行→回包；不在本区预读全部 skill。
4. 不要为「看全貌」打开其他区的全部步骤包。
