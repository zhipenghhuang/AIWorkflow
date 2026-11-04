# 步骤包 · change/decide

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`change`
- **step**：`decide`（处置确认）
- **packet**：`rules/packets/change/decide.md`
- **条件步** `when=decision_required`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：处置确认
- **产出**：处置结论（受理单 §5；改基线时写变更单 §4）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- confirm_change 出示分诊/影响/差量；产品缺陷须相符证明。纯答疑可跳过本门。

## 4. 本步门

- **HITL `confirm_change`**：出示分诊依据、影响与变更单要点（**含 §2.1 差量表** Now→Proposed）；产品缺陷须有相符证明；无单不实施
- **HITL `confirm_plan`**：首次计划或范围·指标·版本实质变更：目标/路线图/本期范围/**§3.0 Brief+差量表** /里程碑/风险摘要；无差量表（且非明示首版一行）不过门；未确认不进 PRD/排期

## 5. 做法

### 本步动作清单

- confirm_change 出示分诊/影响/差量。
- 产品缺陷须相符证明。纯答疑可跳过本门。

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
route=workflow:change | step=decide | reads=rules/packets/change/decide.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/change/decide.md`；对不上 = 未遵守读链。
