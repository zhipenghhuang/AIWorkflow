# 步骤包 · showcase/materials

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`showcase`
- **step**：`materials`（展示材料）
- **packet**：`rules/packets/showcase/materials.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：展示材料
- **产出**：{workroot}/{ver}/50-showcase/一页纸-{产品}.md · {workroot}/{ver}/50-showcase/Deck大纲-{受众}.md（按点名类型产出）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 一页纸：问题/用户/价值/证据/下一步；Deck：10～12 页，每页一个观点 + 证据 + 图； Mermaid 流程图/业务架构图（不写技术架构）。 **共享事实表 + 分片**（子代理编排 ）：同时产 ≥3 类材料/文档 → 先定事实表（功能/版本/截图/数字/边界），再按类型分片（不同文件）；最后 verifier-agent 一致性核对；单类直做。 技能：`skills/presentation-design/SKILL.md`；能力 doc-suite / presentation 可选。 **项目对齐**：数字/截图/流程/术语与 PRD/原型/构建一致，引用可回查；对外发送/承诺前由 `publish` 步 `confirm_materials` 确认，内部草稿不停。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 技能 `presentation-design`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「多放信息显得专业」 | 对外材料只保留现行结论；堆砌过程/旧方案=噪音。 |
| 「截图可以稍后补」 | 演示材料须与当前 PRD/原型/构建一致；缺证据标待补。 |
| 「品牌色随便挑好看的」 | 有设计系统/品牌规范时先对齐 tokens，不另造视觉语言。 |
### 编排备忘

一页纸：问题/用户/价值/证据/下一步；Deck：10～12 页，每页一个观点 + 证据 + 图； Mermaid 流程图/业务架构图（不写技术架构）。 **共享事实表 + 分片**（子代理编排 ）：同时产 ≥3 类材料/文档 → 先定事实表（功能/版本/截图/数字/边界），再按类型分片（不同文件）；最后 verifier-agent 一致性核对；单类直做。 技能：`skills/presentation-design/SKILL.md`；能力 doc-suite / presentation 可选。 **项目对齐**：数字/截图/流程/术语与 PRD/原型/构建一致，引用可回查；对外发送/承诺前由 `publish` 步 `confirm_materials` 确认，内部草稿不停。

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
route=workflow:showcase | step=materials | reads=rules/packets/showcase/materials.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/showcase/materials.md`；对不上 = 未遵守读链。
