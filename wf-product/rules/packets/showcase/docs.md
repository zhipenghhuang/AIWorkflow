# 步骤包 · showcase/docs

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`showcase`
- **step**：`docs`（用户文档）
- **packet**：`rules/packets/showcase/docs.md`
- **条件步** `when=docs_requested`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：用户文档
- **产出**：{workroot}/user/{按点名类型}-{ver}.md（快速开始/用户手册/FAQ/发布说明/培训材料；未点名默认用户手册）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 点名用户手册/快速开始/FAQ/发布说明/培训材料 → `docs_requested=true`。 技能：`skills/product-docs/SKILL.md`；模板 `rules/templates/50-showcase-docs/user-manual-quickstart-template.md`、`rules/templates/50-showcase-docs/release-notes-template.md`。 只产被点名的文档类型，不一次生成四类；按任务组织：5 分钟快速开始 → 常用任务 → FAQ/故障 → 版本说明；截图/步骤与当前构建一致； 同时产 ≥3 类文档 → 共享事实表 + 按类型分片（不同文件，单写手/类）；verifier-agent 核对数字/版本/截图/边界；不并行写同一文档。 不写未发布功能；客户版发布说明面向用户，不写内部实现与内部路径；对外前由 `publish` 步确认。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 技能 `product-docs`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「手册可以写计划中功能」 | 只写现行已发布能力；未上线标「未提供」或删除。 |
| 「FAQ 先猜用户会问」 | 无来源标待验证；禁止臆造政策/限制。 |
| 「和 PRD 不一致先发再改」 | 对外文档与 PRD/发布说明冲突=阻断。 |
### 编排备忘

点名用户手册/快速开始/FAQ/发布说明/培训材料 → `docs_requested=true`。 技能：`skills/product-docs/SKILL.md`；模板 `rules/templates/50-showcase-docs/user-manual-quickstart-template.md`、`rules/templates/50-showcase-docs/release-notes-template.md`。 只产被点名的文档类型，不一次生成四类；按任务组织：5 分钟快速开始 → 常用任务 → FAQ/故障 → 版本说明；截图/步骤与当前构建一致； 同时产 ≥3 类文档 → 共享事实表 + 按类型分片（不同文件，单写手/类）；verifier-agent 核对数字/版本/截图/边界；不并行写同一文档。 不写未发布功能；客户版发布说明面向用户，不写内部实现与内部路径；对外前由 `publish` 步确认。

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
route=workflow:showcase | step=docs | reads=rules/packets/showcase/docs.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/showcase/docs.md`；对不上 = 未遵守读链。
