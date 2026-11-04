# 步骤包 · handoff/receive

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：测试轨
- **workflow**：`handoff`
- **step**：`receive`（接收与签收）
- **packet**：`rules/packets/handoff/receive.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：接收与签收
- **产出**：入站分析/吸收 + 接收回执（按需）+ 测试计划/文档更新 + 台账状态

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- **硬**：打开→分析→吸收→同步；`inbound/` 为原件、`handoff/inbound/` 为收件工作副本。 多包同仓直读对方出站；仓外主副本原件根 `inbound/` + 工作副本 `{workroot}/handoff/inbound/{类别}/`。 按类型更新计划/分析表/准入；正式签收才回执。更新台账、计划 /、索引、activeContext。

## 4. 本步门

- **HITL `confirm_understanding`**：**主屏**：测试分析表 §0【业务与变更简报】+【本期差量表】+ 冲突/九类歧义/GAP 计数与 oracle 要点；无 §0 不过门（T0 迷你差量除外）。确认后才写计划/用例/断言
- **HITL `confirm_plan`**：版本级首版/换代或范围·准出·缺陷提交策略实质变更 → STOP 一行摘要确认；同会话同载体只一次；专项轻量不设门。版本级须先过：分析表 §2.2/§2.3 无空格 + §2.4 依据覆盖无缺行 + §3.8 四卷 + §3.9 批次表；缺项=计划门不通过

## 5. 做法

### 本步动作清单

- **硬**：打开→分析→吸收→同步。
- `inbound/` 为原件、`handoff/inbound/` 为收件工作副本。 多包同仓直读对方出站。
- 仓外主副本原件根 `inbound/` + 工作副本 `{workroot}/handoff/inbound/{类别}/`。 按类型更新计划/分析表/准入。
- 正式签收才回执。更新台账、计划 /、索引、activeContext。

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
route=workflow:handoff | step=receive | reads=rules/packets/handoff/receive.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/handoff/receive.md`；对不上 = 未遵守读链。
