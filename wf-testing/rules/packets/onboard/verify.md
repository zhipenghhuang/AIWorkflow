# 步骤包 · onboard/verify

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：测试轨
- **workflow**：`onboard`
- **step**：`verify`（核验与打标）
- **packet**：`rules/packets/onboard/verify.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：核验与打标
- **产出**：{workroot}/changes/接入核验-{yyyyMMdd}.md（①～⑦ 逐项 通过/缺口 + 证据）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 按 onboard-agent 接入清单核验（①～⑦，含写「wf-testing onboard: done」；若有旧 landing=ok 删除并改写），逐项给「通过/缺口 + 证据路径」，不得只写“已核验”。 跑 `rules/tools/Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`；BLOCKED 不得打标。 有挂起原口令则 resume；此后业务任务见标记直跑。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 本步动作清单

- 按 onboard-agent 接入清单核验（①～⑦，含写「wf-testing onboard: done」。
- 若有旧 landing=ok 删除并改写），逐项给「通过/缺口 + 证据路径」，不得只写“已核验”。 跑 `rules/tools/Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`。
- BLOCKED 不得打标。 有挂起原口令则 resume。
- 此后业务任务见标记直跑。

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
route=workflow:onboard | step=verify | reads=rules/packets/onboard/verify.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/onboard/verify.md`；对不上 = 未遵守读链。
