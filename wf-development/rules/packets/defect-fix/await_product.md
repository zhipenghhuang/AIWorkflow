# 步骤包 · defect-fix/await_product

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`defect-fix`
- **step**：`await_product`（等待产品处置）
- **packet**：`rules/packets/defect-fix/await_product.md`
- **条件步** `when=product_defect`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：等待产品处置
- **产出**：等待回执（AWAIT_PRODUCT）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- STOP：本步输出后结束，不执行 wrap/后续 step；不改代码、不提交、不部署、不按自己的评估方案实施。 输出【缺陷修复处理总结】的待产品部分（评估单/附件/待决定项）+ 一行 AWAIT_PRODUCT； 同批实现项/澄清项标「待下一批」，不静默丢；不输出提交菜单（未实施，无可提交代码）。 下次用户说「拉取产品回复/产品回复/产品退回/继续缺陷」→ 从 product_decision 进入。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 本步动作清单

- STOP：本步输出后结束，不执行 wrap/后续 step。
- 不改代码、不提交、不部署、不按自己的评估方案实施。 输出【缺陷修复处理总结】的待产品部分（评估单/附件/待决定项）+ 一行 AWAIT_PRODUCT。
- 同批实现项/澄清项标「待下一批」，不静默丢。
- 不输出提交菜单（未实施，无可提交代码）。 下次用户说「拉取产品回复/产品回复/产品退回/继续缺陷」→ 从 product_decision 进入。

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
route=workflow:defect-fix | step=await_product | reads=rules/packets/defect-fix/await_product.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/defect-fix/await_product.md`；对不上 = 未遵守读链。
