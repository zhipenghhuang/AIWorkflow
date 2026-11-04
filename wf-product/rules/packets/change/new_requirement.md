# 步骤包 · change/new_requirement

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`change`
- **step**：`new_requirement`（新需求与优先级（条件））
- **packet**：`rules/packets/change/new_requirement.md`
- **条件步** `when=new_requirement`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：新需求与优先级（条件）
- **产出**：{workroot}/requirement-pool.md 更新 + 范围结论

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 仅新需求；入池须证据；confirm_scope 后进 assess/路线图。细节只认技能必做。

## 4. 本步门

- **HITL `confirm_scope`**：范围（MVP）/排除项/粗排期/风险 一行摘要；条件门：仅跨版本/高价值/未确认范围时停

## 5. 做法

### 本步动作清单

- 仅新需求。
- 入池须证据。
- confirm_scope 后进 assess/路线图。细节只认技能必做。

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
route=workflow:change | step=new_requirement | reads=rules/packets/change/new_requirement.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/change/new_requirement.md`；对不上 = 未遵守读链。
