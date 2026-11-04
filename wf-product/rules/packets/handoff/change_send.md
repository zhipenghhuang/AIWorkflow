# 步骤包 · handoff/change_send

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`handoff`
- **step**：`change_send`（发送变更通知）
- **packet**：`rules/packets/handoff/change_send.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：发送变更通知
- **产出**：{workroot}/handoff/outbound/变更/{CHG-HO-ID}/ + 更新后的受影响文档

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 先按 `workflows/change.yaml` 完成受理/影响/处置/变更单；本步只负责“通知包”。 按 判 C0～C3；C2/C3 先过 `confirm_change`/`confirm_plan`。 **CHG 包同样先问后发**：`confirm_handoff` 出示拟发摘要，确认后才生成。 必带：变更单、更新后 PRD/AC/原型、影响矩阵、必做事项/截止、兼容/回滚、生效版本。 多包同仓直读，禁止转发；仓外发文件夹/ZIP。

## 4. 本步门

- **HITL `confirm_change`**：出示分诊依据、影响与变更单要点（**含 §2.1 差量表** Now→Proposed）；产品缺陷须有相符证明；无单不实施
- **HITL `confirm_handoff`**：**凡拟生成任一 HO 包必停**：出示类型/接收方/必带摘要/阻断/传递方式；用户确认后才落盘；未确认零发包。禁止用「定稿门/评审门/发布门已过」代替本门。未收回执不得称「已接收」；可称「已发送」

## 5. 做法

### 本步动作清单

- 先按 `workflows/change.yaml` 完成受理/影响/处置/变更单。
- 本步只负责“通知包”。 按 判 C0～C3。
- C2/C3 先过 `confirm_change`/`confirm_plan`。 **CHG 包同样先问后发**：`confirm_handoff` 出示拟发摘要，确认后才生成。 必带：变更单、更新后 PRD/AC/原型、影响矩阵、必做事项/截止、兼容/回滚、生效版本。 多包同仓直读，禁止转发。
- 仓外发文件夹/ZIP。

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
route=workflow:handoff | step=change_send | reads=rules/packets/handoff/change_send.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/handoff/change_send.md`；对不上 = 未遵守读链。
