# 步骤包 · defect/source

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`defect`
- **step**：`source`（来源识别）
- **packet**：`rules/packets/defect/source.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：来源识别
- **产出**：来源类型（测试直提/开发评估单/产品复核；逐条标）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 逐条标来源；混批按条处理，不整批套用同一处置模板。 按 `rules/defects/platform-collaboration.md` 判断来源： 备注含「【产品缺陷·开发评估】」或附件名 `缺陷评估-BUG-…` → 开发评估单； 测试提交、类型=产品缺陷、标题/【提交摘要】含“产品缺陷”、备注含相符证明 → 测试直提； 其它 → 产品复核/常规缺陷。 来源决定后续处置与指派：测试直提由产品独立定性；开发评估单由产品复核开发判定与方案。 来源不清 → 读全备注/附件再一次判断，禁只看标题。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 本步动作清单

- 逐条标来源。
- 混批按条处理，不整批套用同一处置模板。 按 `rules/defects/platform-collaboration.md` 判断来源： 备注含「【产品缺陷·开发评估】」或附件名 `缺陷评估-BUG-…` → 开发评估单。
- 测试提交、类型=产品缺陷、标题/【提交摘要】含“产品缺陷”、备注含相符证明 → 测试直提。
- 其它 → 产品复核/常规缺陷。 来源决定后续处置与指派：测试直提由产品独立定性。
- 开发评估单由产品复核开发判定与方案。 来源不清 → 读全备注/附件再一次判断，禁只看标题。

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
route=workflow:defect | step=source | reads=rules/packets/defect/source.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/defect/source.md`；对不上 = 未遵守读链。
