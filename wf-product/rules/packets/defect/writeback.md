# 步骤包 · defect/writeback

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`defect`
- **step**：`writeback`（平台回写）
- **packet**：`rules/packets/defect/writeback.md`
- **条件步** `when=remark_writeback`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：平台回写
- **产出**：平台回写结果（备注/附件/状态/指派）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 按 `rules/templates/30-review-change/defect-writeup-template.md` /：回写前出示 id、来源、结论、备注全文、附件名、 状态/指派变更、目标版本；确认后执行。 运行 `verify/Invoke-Gate.ps1 -Mode writeback`；无回执/备注状态不同轮/附件未回查 → 不得声称已回写。 未配置平台/无权限 → 先回 preflight；无既有分析/结论 → 回 pull/analyze，不凭空回写； 只改字段未分析 → 先补分析。 备注与状态同轮；备注写分诊依据/处置结论/影响 AC/目标版本/下一步/需要谁做什么； 回写内容由编排集中生成；子代理只提供事实素材，不写平台、不改状态。 禁密钥/绝对路径/用例路径。 附件上传后回查挂载；失败重试≤1，禁删缺陷。平台不支持/无权限 → 出 export 包，标「待回写」。 指派：产品缺陷/实现缺陷→开发；非问题/重复/信息不足按来源→测试或开发； 补充信息/信息不足→提交人/测试/开发（按来源）。目标版本/截止写清。 回写后更新受理单 /。

## 4. 本步门

- **HITL `confirm_remark`**：出示 id+结论+备注全文+附件名+状态/指派变更；备注与状态同轮；平台不支持出 export
- **GATE `writeback-receipt`**：`Invoke-Gate.ps1 -Mode writeback -Artifact …`；单号+备注实质+状态取值+fileId/无附件；禁标题刷绿；无回执不得声称已回写

## 5. 做法

### 技能 `change-management`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「先改 PRD 再说」 | 未分诊/未评估不得改基线；先受理分类再 apply。 |
| 「紧急上线可跳变更单」 | 无单不实施；紧急也要事后留痕与门对齐。 |
| 「实现缺陷当产品缺陷开」 | 须 PRD 原文+现网证据；实现问题退回开发/测试。 |
| 「口头答应客户就算变更」 | 未确认范围/优先级不得入池承诺。 |
### 编排备忘

按 `rules/templates/30-review-change/defect-writeup-template.md` /：回写前出示 id、来源、结论、备注全文、附件名、 状态/指派变更、目标版本；确认后执行。 运行 `verify/Invoke-Gate.ps1 -Mode writeback`；无回执/备注状态不同轮/附件未回查 → 不得声称已回写。 未配置平台/无权限 → 先回 preflight；无既有分析/结论 → 回 pull/analyze，不凭空回写； 只改字段未分析 → 先补分析。 备注与状态同轮；备注写分诊依据/处置结论/影响 AC/目标版本/下一步/需要谁做什么； 回写内容由编排集中生成；子代理只提供事实素材，不写平台、不改状态。 禁密钥/绝对路径/用例路径。 附件上传后回查挂载；失败重试≤1，禁删缺陷。平台不支持/无权限 → 出 export 包，标「待回写」。 指派：产品缺陷/实现缺陷→开发；非问题/重复/信息不足按来源→测试或开发； 补充信息/信息不足→提交人/测试/开发（按来源）。目标版本/截止写清。 回写后更新受理单 /。

## 6. 打开/填写

- 运行时正文：仅本文件（开局卡已在会话开头读过）。
- 验证：`verify/Invoke-Gate.ps1`（完成声称加 `-Claim`）；有 UI 另按包内前端条。

## 7. 完成信号

- §2 产出已落盘。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 8. 回执字段

```text
route=workflow:defect | step=writeback | reads=rules/packets/defect/writeback.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/defect/writeback.md`；对不上 = 未遵守读链。
