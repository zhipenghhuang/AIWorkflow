# 步骤包 · defect-fix/product_decision

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`defect-fix`
- **step**：`product_decision`（产品处置读取）
- **packet**：`rules/packets/defect-fix/product_decision.md`
- **条件步** `when=product_decision_received`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：产品处置读取
- **产出**：产品结论/附件/对齐清单

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 入口直达（拉取产品回复/产品回复/产品退回/继续缺陷）视为本步条件成立； 未读产品回复/附件前不得进 fix；平台仍无产品回复/仍指派产品 → 输出 AWAIT_PRODUCT，不重复 handoff。 按 rules/defects/fix-collaboration.md / 读全单：状态/解决码/指派人/全部备注/附件/新产品文档/关联需求。 归类：认可方案/修改后认可/判定实现defects/判定非问题/要求补充信息。 仅“回派”无备注/附件说明 → 视为未确认，输出 AWAIT_PRODUCT 请产品补结论。 认可或修改后认可或改判实现 → implementation_required + product_decision_requires_alignment； 要求补充/非问题 → need_clarification； 非问题按产品要求退回测试/关闭，不自行改代码。 读不全（solutionChannel=manual）→ 请用户补关键附件/备注，禁只看标题或只读一句备注。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 本步动作清单

- 入口直达（拉取产品回复/产品回复/产品退回/继续缺陷）视为本步条件成立。
- 未读产品回复/附件前不得进 fix。
- 平台仍无产品回复/仍指派产品 → 输出 AWAIT_PRODUCT，不重复 handoff。 按 rules/defects/fix-collaboration.md / 读全单：状态/解决码/指派人/全部备注/附件/新产品文档/关联需求。 归类：认可方案/修改后认可/判定实现defects/判定非问题/要求补充信息。 仅“回派”无备注/附件说明 → 视为未确认，输出 AWAIT_PRODUCT 请产品补结论。 认可或修改后认可或改判实现 → implementation_required + product_decision_requires_alignment。
- 要求补充/非问题 → need_clarification。
- 非问题按产品要求退回测试/关闭，不自行改代码。 读不全（solutionChannel=manual）→ 请用户补关键附件/备注，禁只看标题或只读一句备注。

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
route=workflow:defect-fix | step=product_decision | reads=rules/packets/defect-fix/product_decision.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/defect-fix/product_decision.md`；对不上 = 未遵守读链。
