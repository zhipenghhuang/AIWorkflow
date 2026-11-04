# 步骤包 · release/approval

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`release`
- **step**：`approval`（工程部署审批）
- **packet**：`rules/packets/release/approval.md`
- **条件步** `when=release_ready_and_acceptance_passed`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：工程部署审批
- **产出**：工程部署审批记录

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 工程 go/no-go：基于上线检查单 + UAT/验收 + 测试报告 + 风险/回滚；出示版本/窗口/影响面/回滚决策人；并核**干净工作区 + 已提交或已打 tag + completion=COMPLETE**。 **目标必须是生产/正式环境**；test/staging 部署不触发本门，版本按项目策略。生产版本必须是正式版（无 prerelease）；rc/QA 批次直接上生产 → NO-GO。 若项目已有业务发布决策（其它流程/产品包/用户确认）且 UAT 已过 → 本步只确认工程就绪，不重复业务决策；没有 → 本门覆盖业务+工程范围。 未批准不得部署；禁止从脏工作区/未提交代码部署；有条件批准须列明条件与监控措施；发布内容/窗口/回滚变更 → 重新确认。输出 `release_approved=true/false` 供 deploy 判断。

## 4. 本步门

- **HITL `confirm_deploy`**：出示版本/窗口/影响面/回滚决策人；并核 **干净工作区 + 已提交或已打 tag + 本轮 `completion.json=COMPLETE`**；未批准不部署，禁止从脏工作区部署；**仅生产/正式环境**，test/staging 部署不触发本门；生产版本必须无 prerelease

## 5. 做法

### 本步动作清单

- 工程 go/no-go：基于上线检查单 + UAT/验收 + 测试报告 + 风险/回滚。
- 出示版本/窗口/影响面/回滚决策人。
- 并核**干净工作区 + 已提交或已打 tag + completion=COMPLETE**。 **目标必须是生产/正式环境**。
- test/staging 部署不触发本门，版本按项目策略。生产版本必须是正式版（无 prerelease）。
- rc/QA 批次直接上生产 → NO-GO。 若项目已有业务发布决策（其它流程/产品包/用户确认）且 UAT 已过 → 本步只确认工程就绪，不重复业务决策。
- 没有 → 本门覆盖业务+工程范围。 未批准不得部署。
- 禁止从脏工作区/未提交代码部署。
- 有条件批准须列明条件与监控措施。
- 发布内容/窗口/回滚变更 → 重新确认。输出 `release_approved=true/false` 供 deploy 判断。

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
route=workflow:release | step=approval | reads=rules/packets/release/approval.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/release/approval.md`；对不上 = 未遵守读链。
