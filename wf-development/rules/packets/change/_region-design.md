# 子状态机 · change/design

> **嵌套闭环**：长链路中的一小段。进入本区读一次；区内仍 **一次只开一个** step packet。

## 定位

- **包轨**：wf-development
- **父流程**：`rules/packets/change/_chain.md`
- **本区**：`design` — 方案与计划
- **出口**：下一区地图 `rules/packets/change/_region-build.md`（实施与验证）。是否进入只按父链「推进」。

## 区内步骤

| step | 名称 | when | 步骤包 |
| --- | --- | --- | --- |
| `design` | 方案与设计 | `new_feature_or_architecture_or_breaking_change_or_high_risk_or_requested` | `rules/packets/change/design.md` |
| `review-docs` | 落地文档评审 | `landing_doc_review_required` | `rules/packets/change/review-docs.md` |
| `plan` | 任务清单 | `multi_file_or_new_feature_or_requested` | `rules/packets/change/plan.md` |

## 区内纪律

1. 本区按表向后推进；单步口令在本步完成即停；`when` 不满足则不打开该步包。
2. 当前 `packet=` 必须是区内某一步；离开本区前心跳刷新到下一步/下一区。
3. 技能只按**当前步骤包 §6** 打开→执行→回包；不在本区预读全部 skill。
4. 不要为「看全貌」打开其他区的全部步骤包。
