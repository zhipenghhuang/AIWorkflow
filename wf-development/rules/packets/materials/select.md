# 步骤包 · materials/select

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`materials`
- **step**：`select`（选择版本与范围）
- **packet**：`rules/packets/materials/select.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：选择版本与范围
- **产出**：【材料库发布范围】版本/受众/域/包含/排除

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 先按 `rules/doc-governance.md` 定位工作根，再读 `{workroot}/INDEX.md`、`{workroot}` 当前定稿与 `docs/materials/INDEX.md`。 版本取项目/迭代版本；缺则问一次，不硬造。默认只收定稿、正确、完整、可独立阅读的文档； 草稿/过程/证据/密钥/PII/未授权第三方文档不进库。03-technical / 04-implementation / 06-release（工程发布）。 **发布模式默认 overwrite-latest**：未明确「保留历史/不覆盖/升 rev/另存快照/签收锁定」→ 不询问、直接覆盖目标 `{ver}/`。 换迭代关账触发时：先覆盖刷新关闭版 `{prev}/`，再处理 `{next}/`（见 `doc-governance.md` ）。 外发前按现有 `confirm_handoff` / `confirm_intent` 确认，不新造门。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 本步动作清单

- 先按 `rules/doc-governance.md` 定位工作根，再读 `{workroot}/INDEX.md`、`{workroot}` 当前定稿与 `docs/materials/INDEX.md`。 版本取项目/迭代版本。
- 缺则问一次，不硬造。默认只收定稿、正确、完整、可独立阅读的文档。
- 草稿/过程/证据/密钥/PII/未授权第三方文档不进库。03-technical / 04-implementation / 06-release（工程发布）。 **发布模式默认 overwrite-latest**：未明确「保留历史/不覆盖/升 rev/另存快照/签收锁定」→ 不询问、直接覆盖目标 `{ver}/`。 换迭代关账触发时：先覆盖刷新关闭版 `{prev}/`，再处理 `{next}/`（见 `doc-governance.md` ）。 外发前按现有 `confirm_handoff` / `confirm_intent` 确认，不新造门。

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
route=workflow:materials | step=select | reads=rules/packets/materials/select.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/materials/select.md`；对不上 = 未遵守读链。
