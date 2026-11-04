# 步骤包 · testing/review-cases

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：测试轨
- **workflow**：`testing`
- **step**：`review-cases`（用例与多轨资产评审）
- **packet**：`rules/packets/testing/review-cases.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：用例与多轨资产评审
- **产出**：评审记录（单域或合卷路径见 templates）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- STOP 选 A/B；不重生成。功能选 B 跑 -Mode review。方法只认 testcase-review / artifact-review 必做。

## 4. 本步门

- **HITL `select_review_mode`**：**STOP 二选一**：A 自行｜B AI（testcase-reviewer）；可附自定义焦点。适用面见 `landing_doc_review_needed`（计划/分析表/功能/接口/发布前/探索式）。同产物只问一次；未选不得宣称评审通过/计划可驱动/进 P2
- **HITL `confirm_review`**：结论=需修后放行、有条件放行须接受人、或与计划 P2 入口冲突 → STOP；已放行且无未接受重要项 → 跳过
- **GATE `case-review` when=case_review_required**：运行对应 verify；未过不得宣称完成。

## 5. 做法

### 技能 `test-artifact-review`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「生成完直接执行」 | T1+ 须评审放行；写手不得自审自放行。 |
| 「计划很长就等于充分」 | 用量规看范围/oracle/追溯/准出，不看篇幅。 |
| 「有条件通过先跑着」 | CONDITIONAL 须列条件；未接受不得当 PASS。 |
### 技能 `testcase-review`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「条数多就是覆盖好」 | 看追溯/深度/负面/数据链路，不看条数。 |
| 「生成模型写的应该对」 | 无来源断言=缺陷；抽查 A1–A6/S1–S6。 |
| 「评审太慢，先执行」 | 放行前执行污染准出；T0 才可 SELF_CHECKED 并声明。 |
### 编排备忘

STOP 选 A/B；不重生成。功能选 B 跑 -Mode review。方法只认 testcase-review / artifact-review 必做。

## 6. 打开/填写

- 运行时正文：仅本文件（开局卡已在会话开头读过）。
- 验证：`verify/Invoke-Gate.ps1`（完成声称加 `-Claim`）；有 UI 另按包内前端条。

## 7. 完成信号

- §2 产出已落盘。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 8. 回执字段

```text
route=workflow:testing | step=review-cases | reads=rules/packets/testing/review-cases.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/testing/review-cases.md`；对不上 = 未遵守读链。
