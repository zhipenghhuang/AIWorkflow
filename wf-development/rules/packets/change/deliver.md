# 步骤包 · change/deliver

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`change`
- **step**：`deliver`（提测与发布文档）
- **packet**：`rules/packets/change/deliver.md`
- **条件步** `when=has_qa_or_deploy_or_requested`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：提测与发布文档
- **产出**：提测单/发布说明/回滚预案（{workroot}/60-release/）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 自洽提测单真源 60-release/，同轮拷 handoff/outbound；未 COMPLETE 不得标可提测。 跳过本步≠跳过自验。附加 HO 包另走 handoff。

## 4. 本步门

- **HITL `confirm_intent`**：仅当 `intent_needs_confirm`：出示【意图理解】，确认后才落盘。意图已清 → 跳过本门（可一行回执即做）。细则 `clarification.md` §0。≠ `confirm_understanding`；≠ `confirm_handoff`

## 5. 做法

### 技能 `qa-handoff-and-release`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「提测单可以口头说」 | 影响面/AC/环境/已知问题须落盘；无单 QA 可拒收。 |
| 「自测绿=可发布」 | 发布门与完成门分开；无证据不得称可上线。 |
| 「回滚预案以后写」 | 高风险/生产发布缺回滚=阻断。 |
### 编排备忘

自洽提测单真源 60-release/，同轮拷 handoff/outbound；未 COMPLETE 不得标可提测。 跳过本步≠跳过自验。附加 HO 包另走 handoff。

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
route=workflow:change | step=deliver | reads=rules/packets/change/deliver.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/change/deliver.md`；对不上 = 未遵守读链。
