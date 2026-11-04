# 步骤包 · deliver/review-plan-deliver

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`deliver`
- **step**：`review-plan-deliver`（交付计划评审）
- **packet**：`rules/packets/deliver/review-plan-deliver.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：交付计划评审
- **产出**：评审记录（评审-交付计划-{ver}-{yyyyMMdd}.md）或 HUMAN_APPROVED 声明

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 交付计划将驱动开发/测试窗口：**STOP【评审方式】**（`skills/artifact-review`）A 自行｜B AI。 选 A：出示范围/里程碑/依赖/发布窗自检 → HUMAN_APPROVED。 选 B：核范围与 PRD 一致、里程碑可执行、依赖显式、测试窗口合理；缺口分级；留痕 `评审-交付计划-{ver}-{yyyyMMdd}.md`。 通过后默认交付计划/排期正文；`PLAN` 包仅多文件/签收/仓外/点名时停问建议，确认后走 `workflows/handoff.yaml` send（含 `confirm_handoff`），本步不直接落包。未收回执不得称「已接收」。

## 4. 本步门

- **HITL `select_review_mode`**：**STOP 二选一**：A 自行评审通过（HUMAN_APPROVED）｜B AI 独立评审（异人量规+评审记录）。适用 PRD/产品计划/设计交接等（`skills/artifact-review`）；同产物只问一次；点名「AI 评审」=B、「我审/自行通过」=A；未选不得宣称通过/定稿/交开发

## 5. 做法

### 技能 `artifact-review`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「内容看起来完整，可自行通过」 | 完整≠可判定；缺 AC/证据/范围边界仍须选 A/B 并留痕。 |
| 「作者刚写完，自己审更快」 | 写手自审易盲区；选 B 须异上下文量规，选 A 须 HUMAN_APPROVED。 |
| 「小改不用评审」 | 改基线/AC/范围即实质变更；P0 文案除外仍要声明。 |
| 「先定稿再补问题」 | 定稿门前未 READY 不得恢复；问题清单先于定稿。 |
### 编排备忘

交付计划将驱动开发/测试窗口：**STOP【评审方式】**（`skills/artifact-review`）A 自行｜B AI。 选 A：出示范围/里程碑/依赖/发布窗自检 → HUMAN_APPROVED。 选 B：核范围与 PRD 一致、里程碑可执行、依赖显式、测试窗口合理；缺口分级；留痕 `评审-交付计划-{ver}-{yyyyMMdd}.md`。 通过后默认交付计划/排期正文；`PLAN` 包仅多文件/签收/仓外/点名时停问建议，确认后走 `workflows/handoff.yaml` send（含 `confirm_handoff`），本步不直接落包。未收回执不得称「已接收」。

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
route=workflow:deliver | step=review-plan-deliver | reads=rules/packets/deliver/review-plan-deliver.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/deliver/review-plan-deliver.md`；对不上 = 未遵守读链。
