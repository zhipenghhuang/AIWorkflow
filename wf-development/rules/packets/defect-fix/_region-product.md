# 子状态机 · defect-fix/product

> **嵌套闭环**：长链路中的一小段。进入本区读一次；区内仍 **一次只开一个** step packet。

## 定位

- **包轨**：wf-development
- **父流程**：`rules/packets/defect-fix/_chain.md`
- **本区**：`product` — 产品协作闭环
- **出口**：下一区地图 `rules/packets/defect-fix/_region-fix.md`（修复与门禁）。是否进入只按父链「推进」。

## 区内步骤

| step | 名称 | when | 步骤包 |
| --- | --- | --- | --- |
| `assess_product` | 产品缺陷评估 | `product_defect` | `rules/packets/defect-fix/assess_product.md` |
| `handoff_product` | 评估单提交产品 | `product_defect` | `rules/packets/defect-fix/handoff_product.md` |
| `await_product` | 等待产品处置 | `product_defect` | `rules/packets/defect-fix/await_product.md` |
| `product_decision` | 产品处置读取 | `product_decision_received` | `rules/packets/defect-fix/product_decision.md` |
| `align` | 文档对齐 | `product_decision_requires_alignment` | `rules/packets/defect-fix/align.md` |

## 区内纪律

1. 本区按表向后推进；单步口令在本步完成即停；`when` 不满足则不打开该步包。
2. 当前 `packet=` 必须是区内某一步；离开本区前心跳刷新到下一步/下一区。
3. 技能只按**当前步骤包 §6** 打开→执行→回包；不在本区预读全部 skill。
4. 不要为「看全貌」打开其他区的全部步骤包。
