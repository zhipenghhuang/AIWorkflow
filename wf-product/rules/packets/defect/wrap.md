# 步骤包 · defect/wrap

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`defect`
- **step**：`wrap`（收尾）
- **packet**：`rules/packets/defect/wrap.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：收尾
- **产出**：【任务收尾】（产品缺陷协作总结置第 1 点）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 对照 `rules/templates/90-handoff/closeout-skeleton.md` 输出【任务收尾】（须含【遵守自检】）；第1点含【产品缺陷协作总结】与本轮真实单号 更新产品计划 //、activeContext、 `{workroot}/INDEX.md`；现状三处同拍（执行契约 规则 7）；`sync=` 含 `triad=aligned|deferred:<原因>`；语义已变禁只改 activeContext。未verify/待回写项明示。 本步先出骨架与拟提交清单，提交门在下一步。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 本步动作清单

- 对照 `rules/templates/90-handoff/closeout-skeleton.md` 输出【任务收尾】（须含【遵守自检】）。
- 第1点含【产品缺陷协作总结】与本轮真实单号 更新产品计划 //、activeContext、 `{workroot}/INDEX.md`。
- 现状三处同拍（执行契约 规则 7）。
- `sync=` 含 `triad=aligned|deferred:<原因>`。
- 语义已变禁只改 activeContext。未verify/待回写项明示。 本步先出骨架与拟提交清单，提交门在下一步。

## 6. 打开/填写

- 运行时正文：仅本文件（开局卡已在会话开头读过）。
- 填写模板（仅此一个）：`rules/templates/90-handoff/closeout-skeleton.md`

## 7. 完成信号

- §2 产出已落盘。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 8. 回执字段

```text
route=workflow:defect | step=wrap | reads=rules/packets/defect/wrap.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/defect/wrap.md`；对不上 = 未遵守读链。
