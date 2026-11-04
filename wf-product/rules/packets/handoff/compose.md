# 步骤包 · handoff/compose

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`handoff`
- **step**：`compose`（写交接单文档）
- **packet**：`rules/packets/handoff/compose.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：写交接单文档
- **产出**：自洽交接单文档（默认非 HO；落 outbound/{category}/）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- **默认入口**。读协作 ～ 与 `handoff-note-template.md`（择优，非填空卷）。 **意图择优**：先判 `intent_needs_confirm`（澄清 ）。真 → 完整【意图理解】停等再落盘；假 → 一行【意图】回执后直写。禁止含糊「交接」直接成文。 五问→形态 A/B/C 或专模；禁止整表粘贴。确认类优先 B 一页纸。 专模真源写版本目录，同轮实拷 `{workroot}/handoff/outbound/{category}/`；无专模直接写出站类。不建 HO；禁外印元数据。

## 4. 本步门

- **HITL `confirm_intent`**：仅当 `intent_needs_confirm`：出示【意图理解】，确认后才落盘。意图已清 → 跳过（可一行回执即做）。细则 `clarification.md` §0。≠ `confirm_understanding`；≠ `confirm_handoff`

## 5. 做法

### 本步动作清单

- **默认入口**。读协作 ～ 与 `handoff-note-template.md`（择优，非填空卷）。 **意图择优**：先判 `intent_needs_confirm`（澄清 ）。真 → 完整【意图理解】停等再落盘。
- 假 → 一行【意图】回执后直写。禁止含糊「交接」直接成文。 五问→形态 A/B/C 或专模。
- 禁止整表粘贴。确认类优先 B 一页纸。 专模真源写版本目录，同轮实拷 `{workroot}/handoff/outbound/{category}/`。
- 无专模直接写出站类。不建 HO。
- 禁外印元数据。

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
route=workflow:handoff | step=compose | reads=rules/packets/handoff/compose.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/handoff/compose.md`；对不上 = 未遵守读链。
