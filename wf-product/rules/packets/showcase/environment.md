# 步骤包 · showcase/environment

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`showcase`
- **step**：`environment`（Demo 环境与数据）
- **packet**：`rules/packets/showcase/environment.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：Demo 环境与数据
- **产出**：{workroot}/{ver}/50-showcase/演示检查单-{yyyyMMdd}.md

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 构建/原型版本、账号角色、seed/重置、网络、设备、录屏兜底、权限与隐私； `rules/templates/50-showcase-docs/demo-checklist-template.md` 逐项过；能力（可选）browser-mcp 走查，未装=手工检查。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 本步动作清单

- 构建/原型版本、账号角色、seed/重置、网络、设备、录屏兜底、权限与隐私。
- `rules/templates/50-showcase-docs/demo-checklist-template.md` 逐项过。
- 能力（可选）browser-mcp 走查，未装=手工检查。

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
route=workflow:showcase | step=environment | reads=rules/packets/showcase/environment.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/showcase/environment.md`；对不上 = 未遵守读链。
