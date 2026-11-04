# 步骤包 · prd/handoff

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`prd`
- **step**：`handoff`（需求交接包）
- **packet**：`rules/packets/prd/handoff.md`
- **条件步** `when=prd_ready_for_handoff`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：需求交接包
- **产出**：{workroot}/handoff/outbound/需求/ 自洽 PRD 实拷 + handoff-ledger.md；升 REQ 包时走 handoff.send

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- PRD 已 APPROVED 且 PRD 门 READY 后执行；本步只决定「交自洽 PRD 还是打 REQ 包」，**不得在本步直接写 `{HO-ID}/`**。 **最优默认**：定稿后交付**自洽 PRD**（实施可读：全量 AC/范围/非目标/边界/NFR/待决写进 PRD）；**不**默认打 REQ 包。 **REQ 包按需**：多文件（原型源等）/正式签收/仓外 ZIP/点名 → 停问建议；确认后走 `workflows/handoff.yaml` 的 `send`（含 `confirm_handoff`），不另造模板。未命中不机械每问。 仅评审未定稿 → 跳过。未回执不得写“开发/测试已接收”。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 本步动作清单

- PRD 已 APPROVED 且 PRD 门 READY 后执行。
- 本步只决定「交自洽 PRD 还是打 REQ 包」，**不得在本步直接写 `{HO-ID}/`**。 **最优默认**：定稿后交付**自洽 PRD**（实施可读：全量 AC/范围/非目标/边界/NFR/待决写进 PRD）。
- **不**默认打 REQ 包。 **REQ 包按需**：多文件（原型源等）/正式签收/仓外 ZIP/点名 → 停问建议。
- 确认后走 `workflows/handoff.yaml` 的 `send`（含 `confirm_handoff`），不另造模板。未命中不机械每问。 仅评审未定稿 → 跳过。未回执不得写“开发/测试已接收”。

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
route=workflow:prd | step=handoff | reads=rules/packets/prd/handoff.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/prd/handoff.md`；对不上 = 未遵守读链。
