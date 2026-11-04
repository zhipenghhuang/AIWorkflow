# 步骤包 · defect-fix/clarify

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`defect-fix`
- **step**：`clarify`（澄清/非缺陷回写）
- **packet**：`rules/packets/defect-fix/clarify.md`
- **条件步** `when=need_clarification`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：澄清/非缺陷回写
- **产出**：回写结果（【无法确认·待澄清】/重复/设计如此/非defects/外部/已在其它构建修复）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 按 rules/templates/40-delivery/defect-writeup-template.md /： 先按原单口径复现；一次列清缺什么/谁补/截止；给条件式下一步，避免来回踢皮球。 平台备注用中文结论，禁英文处置码、类名、命令、仓库路径；本条是给测试看的。 重复→duplicateBug=主单；设计如此→引用设计原文；外部→给外部证据； 延期/不修复须产品/项目确认，不得开发单方关闭。 不改代码；备注与状态同轮；确认前展示全文。

## 4. 本步门

- **HITL `confirm_remark`**：出示 §6 备注全文 + 状态/指派/resolvedBuild；确认后状态+备注同轮写入；未验证只写「待验证」

## 5. 做法

### 本步动作清单

- 按 rules/templates/40-delivery/defect-writeup-template.md /： 先按原单口径复现。
- 一次列清缺什么/谁补/截止。
- 给条件式下一步，避免来回踢皮球。 平台备注用中文结论，禁英文处置码、类名、命令、仓库路径。
- 本条是给测试看的。 重复→duplicateBug=主单。
- 设计如此→引用设计原文。
- 外部→给外部证据。
- 延期/不修复须产品/项目确认，不得开发单方关闭。 不改代码。
- 备注与状态同轮。
- 确认前展示全文。

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
route=workflow:defect-fix | step=clarify | reads=rules/packets/defect-fix/clarify.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/defect-fix/clarify.md`；对不上 = 未遵守读链。
