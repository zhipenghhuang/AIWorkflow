# 步骤包 · handoff/change_send

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：测试轨
- **workflow**：`handoff`
- **step**：`change_send`（发送变更通知）
- **packet**：`rules/packets/handoff/change_send.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：发送变更通知
- **产出**：{workroot}/handoff/outbound/变更/{CHG-HO-ID}/ + 更新后的测试计划/用例/脚本

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 先按 `workflows/testing.yaml` 的 plan 期中变更完成 CR/影响分析；本步只负责“通知包”。 按 `rules/collaboration/handoff.md` 判 C0/C1/C2/C3；C2/C3 必须先过计划门。 **CHG 包同样先问后发**：`confirm_handoff` 出示拟发摘要，用户确认后才生成 HO 包。 必带：CR、影响矩阵、更新后的计划/用例/脚本/报告、接收方必须做的事/截止、回归范围、生效版本。 受影响角色逐个发（产品/开发）；同一变更一个包可多接收方，但回执逐个登记。 更新 `handoff-ledger.md`、测试计划 //、 `{workroot}/INDEX.md`、activeContext；输出【变更通知已生成】+ 回执截止。 未确认不得发；不得用口头/聊天替代变更包。

## 4. 本步门

- **HITL `confirm_plan`**：版本级首版/换代或范围·准出·缺陷提交策略实质变更 → STOP 一行摘要确认；同会话同载体只一次；专项轻量不设门。版本级须先过：分析表 §2.2/§2.3 无空格 + §2.4 依据覆盖无缺行 + §3.8 四卷 + §3.9 批次表；缺项=计划门不通过
- **HITL `confirm_handoff`**：**凡拟生成任一 HO 或缺陷统一导出必停**：出示类型/接收方/必带摘要/落点（缺陷须写清「本批一份单文件或单 EXPORT 目录」）/阻断/传递方式；用户确认后才落盘；未确认零发包。禁止用「报告门/计划门/批末/平台已交」代替本门。有平台交缺陷 → 本门不因「补导出」置真。未收回执不得称「已接收」；可称「已发送」

## 5. 做法

### 本步动作清单

- 先按 `workflows/testing.yaml` 的 plan 期中变更完成 CR/影响分析。
- 本步只负责“通知包”。 按 `rules/collaboration/handoff.md` 判 C0/C1/C2/C3。
- C2/C3 必须先过计划门。 **CHG 包同样先问后发**：`confirm_handoff` 出示拟发摘要，用户确认后才生成 HO 包。 必带：CR、影响矩阵、更新后的计划/用例/脚本/报告、接收方必须做的事/截止、回归范围、生效版本。 受影响角色逐个发（产品/开发）。
- 同一变更一个包可多接收方，但回执逐个登记。 更新 `handoff-ledger.md`、测试计划 //、 `{workroot}/INDEX.md`、activeContext。
- 输出【变更通知已生成】+ 回执截止。 未确认不得发。
- 不得用口头/聊天替代变更包。

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
