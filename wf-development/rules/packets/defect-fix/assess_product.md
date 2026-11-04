# 步骤包 · defect-fix/assess_product

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`defect-fix`
- **step**：`assess_product`（产品缺陷评估）
- **packet**：`rules/packets/defect-fix/assess_product.md`
- **条件步** `when=product_defect`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：产品缺陷评估
- **产出**：产品缺陷评估单（模板 rules/templates/20-design/product-defect-assessment-template.md）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 按 rules/defects/fix-collaboration.md ： 写评估单前必做实现核对（代码路径与/或接口契约·响应），结论写入评估单「实现核对」；未核对不得出单。 写 缺陷评估-{BUG-ID}-{主题}-{yyyyMMdd}.md，落 {workroot}/00-governance/缺陷评估/； 只写实现核对摘要/判定依据/问题影响/方案选项 A/B/C/推荐/影响面/待产品确认； 不写可编码实现细节、不拆开发任务、不排开发排期；不得与正常迭代方案 方案-{主题}-… 混用。 没有相符证明且不属于需求缺口变体 → 不判产品缺陷：按实现缺陷或 need_clarification 处理。 无平台/export/文档输入 → 评估单经 change/handoff 交付，口径与平台备注同源。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 本步动作清单

- 按 rules/defects/fix-collaboration.md ： 写评估单前必做实现核对（代码路径与/或接口契约·响应），结论写入评估单「实现核对」。
- 未核对不得出单。 写 缺陷评估-{BUG-ID}-{主题}-{yyyyMMdd}.md，落 {workroot}/00-governance/缺陷评估/。
- 只写实现核对摘要/判定依据/问题影响/方案选项 A/B/C/推荐/影响面/待产品确认。
- 不写可编码实现细节、不拆开发任务、不排开发排期。
- 不得与正常迭代方案 方案-{主题}-… 混用。 没有相符证明且不属于需求缺口变体 → 不判产品缺陷：按实现缺陷或 need_clarification 处理。 无平台/export/文档输入 → 评估单经 change/handoff 交付，口径与平台备注同源。

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
route=workflow:defect-fix | step=assess_product | reads=rules/packets/defect-fix/assess_product.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/defect-fix/assess_product.md`；对不上 = 未遵守读链。
