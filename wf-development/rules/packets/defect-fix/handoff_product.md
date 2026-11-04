# 步骤包 · defect-fix/handoff_product

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`defect-fix`
- **step**：`handoff_product`（评估单提交产品）
- **packet**：`rules/packets/defect-fix/handoff_product.md`
- **条件步** `when=product_defect`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：评估单提交产品
- **产出**：平台回写结果（备注+附件+指派产品）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 按 rules/templates/40-delivery/defect-writeup-template.md 出备注全文；上传评估单附件并回查挂载； **双通道**：本步已交/回写平台（评估附件+指派产品）→ **不**再强制 `BUG` 整包。无平台/点名「缺陷交接包」→ **先问后发**，确认后 `handoff.send` 自包含评估详单。未回执不得写“产品已接收”。 指派产品经理；状态按档案映射置「待产品确认/待评审」；resolution 不填。 确认前展示备注全文+附件名+状态/指派变更；备注与状态同轮。 提交后停，不进入 fix；输出 AWAIT_PRODUCT。

## 4. 本步门

- **HITL `confirm_remark`**：出示 §6 备注全文 + 状态/指派/resolvedBuild；确认后状态+备注同轮写入；未验证只写「待验证」

## 5. 做法

### 本步动作清单

- 按 rules/templates/40-delivery/defect-writeup-template.md 出备注全文。
- 上传评估单附件并回查挂载。
- **双通道**：本步已交/回写平台（评估附件+指派产品）→ **不**再强制 `BUG` 整包。无平台/点名「缺陷交接包」→ **先问后发**，确认后 `handoff.send` 自包含评估详单。未回执不得写“产品已接收”。 指派产品经理。
- 状态按档案映射置「待产品确认/待评审」。
- resolution 不填。 确认前展示备注全文+附件名+状态/指派变更。
- 备注与状态同轮。 提交后停，不进入 fix。
- 输出 AWAIT_PRODUCT。

## 6. 打开/填写

- 运行时正文：仅本文件（开局卡已在会话开头读过）。
- 无强制模板：直接写 §2 产出路径产物。

## 7. 完成信号

- §2 产出已落盘。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 8. 回执字段

```text
route=workflow:defect-fix | step=handoff_product | reads=rules/packets/defect-fix/handoff_product.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/defect-fix/handoff_product.md`；对不上 = 未遵守读链。
