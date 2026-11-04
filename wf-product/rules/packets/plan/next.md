# 步骤包 · plan/next

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`plan`
- **step**：`next`（计划续跑）
- **packet**：`rules/packets/plan/next.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：计划续跑
- **产出**：当前阶段/门/下一动作

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 仅由「下一步/当前状态/继续」入口触发；正常「产品计划」链到 publish 止，不执行本步。 只读 `{workroot}/product-plan.md` ///：报备当前阶段、当前门、下一动作、需人工项； 「按产品计划执行」= 按 路由到 plan / prd / deliver / change 对应 step，执行到下一个 `hitl` 停止； 「下一步」只报动作与入口，不执行；「当前状态」只读，不重写计划。 有未吸收的新文档/变化 → 先走 `workflows/change.yaml` intake，不直接改 PRD/计划。 有未回执/退回/阻断的交接包 → 先走 `workflows/handoff.yaml` status/receive，不直接推进阶段。 产品包独立运行；开发/测试包为可选输入/输出，缺则不阻塞。 执行后回写 状态/下一动作、 执行日志；门结论/变更写 。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 本步动作清单

- 仅由「下一步/当前状态/继续」入口触发。
- 正常「产品计划」链到 publish 止，不执行本步。 只读 `{workroot}/product-plan.md` ///：报备当前阶段、当前门、下一动作、需人工项。
- 「按产品计划执行」= 按 路由到 plan / prd / deliver / change 对应 step，执行到下一个 `hitl` 停止。
- 「下一步」只报动作与入口，不执行。
- 「当前状态」只读，不重写计划。 有未吸收的新文档/变化 → 先走 `workflows/change.yaml` intake，不直接改 PRD/计划。 有未回执/退回/阻断的交接包 → 先走 `workflows/handoff.yaml` status/receive，不直接推进阶段。 产品包独立运行。
- 开发/测试包为可选输入/输出，缺则不阻塞。 执行后回写 状态/下一动作、 执行日志。
- 门结论/变更写 。

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
route=workflow:plan | step=next | reads=rules/packets/plan/next.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/plan/next.md`；对不上 = 未遵守读链。
