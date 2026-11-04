# 步骤包 · handoff/replan

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`handoff`
- **step**：`replan`（重规划）
- **packet**：`rules/packets/handoff/replan.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：重规划
- **产出**：更新后的开发计划 + 重规划记录

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 按 `rules/collaboration/handoff.md` 触发（需求/方案/依赖/门禁/CI/产能/发布窗口）执行；先冻结当前基线快照，再做影响矩阵。 选一个动作并写理由：保持+加缓冲｜重排｜砍范围/降级 MVP｜拆波次｜重设计｜暂停升级｜重新基线；C2/C3 必须过 `confirm_plan`。 同轮更新开发计划 //////、任务清单、`handoff-ledger.md`、 `{workroot}/INDEX.md`、activeContext；受影响的 `QA/REL/FIX` 包标 `已取代` 并重发。 重规划后重过受影响门（方案/清单/完成门/发布门）；未过门不得把阶段标完成；向产品/测试发 `CHG` 包并收回执。

## 4. 本步门

- **HITL `confirm_plan`**：首次创建或范围·版本·里程碑实质变更；确认后计划状态=已确认

## 5. 做法

### 本步动作清单

- 按 `rules/collaboration/handoff.md` 触发（需求/方案/依赖/门禁/CI/产能/发布窗口）执行。
- 先冻结当前基线快照，再做影响矩阵。 选一个动作并写理由：保持+加缓冲｜重排｜砍范围/降级 MVP｜拆波次｜重设计｜暂停升级｜重新基线。
- C2/C3 必须过 `confirm_plan`。 同轮更新开发计划 //////、任务清单、`handoff-ledger.md`、 `{workroot}/INDEX.md`、activeContext。
- 受影响的 `QA/REL/FIX` 包标 `已取代` 并重发。 重规划后重过受影响门（方案/清单/完成门/发布门）。
- 未过门不得把阶段标完成。
- 向产品/测试发 `CHG` 包并收回执。

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
route=workflow:handoff | step=replan | reads=rules/packets/handoff/replan.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/handoff/replan.md`；对不上 = 未遵守读链。
