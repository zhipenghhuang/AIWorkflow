# 步骤包 · intake/scan

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`intake`
- **step**：`scan`（扫描新输入）
- **packet**：`rules/packets/intake/scan.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：扫描新输入
- **产出**：新输入候选清单

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 技能：`skills/change-intake/SKILL.md`（先读再做）。 输入是交接包（含 `00-交接说明.md` + `01-交接清单.md`）→ 先走 `workflows/handoff.yaml` receive 核对+回执；未签收不进入吸收。 扫描：`inbound/` 未登记/变化文件、`inbound/INDEX.md` 断链、`{workroot}/INDEX.md`、`git status`；不再扫 `_收件箱`。 对照 `{workroot}/INDEX.md` / `需求台账/待决项/开发计划，列出“未登记/未关联”的候选；不读全量历史，不直接改基线。 多个候选 → 列清单让用户选；无新输入 → 报告“无新增”，不空转。 先按 `rules/doc-governance.md` ～（T1～T9 + 索引/复制/A0～A2）；**确认前不改文件**。确认后：主副本必留原件根 `inbound/`并索引 → 按需复制 → 按需吸收；未点名可仅索引。放入≠分发他包。 **文档抽取分片**（子代理编排 ）：≥3 份新文档 → 只读扇出（每份返回 DOC/CR/OPEN/DEC 候选＋引用位置＋覆盖关系 ≤30 行）；登记/分类/影响集中；单份直做。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 技能 `change-intake`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「先塞进待办再看」 | 先分流/分级/影响面，再入受理；禁止未读资料开写。 |
| 「交接包放一下就算接收」 | 入站须分析吸收；未回执不得称已接收。 |
| 「小补充不用记变更」 | 改基线/AC 必须留痕；否则后续无法追溯。 |
### 编排备忘

技能：`skills/change-intake/SKILL.md`（先读再做）。 输入是交接包（含 `00-交接说明.md` + `01-交接清单.md`）→ 先走 `workflows/handoff.yaml` receive 核对+回执；未签收不进入吸收。 扫描：`inbound/` 未登记/变化文件、`inbound/INDEX.md` 断链、`{workroot}/INDEX.md`、`git status`；不再扫 `_收件箱`。 对照 `{workroot}/INDEX.md` / `需求台账/待决项/开发计划，列出“未登记/未关联”的候选；不读全量历史，不直接改基线。 多个候选 → 列清单让用户选；无新输入 → 报告“无新增”，不空转。 先按 `rules/doc-governance.md` ～（T1～T9 + 索引/复制/A0～A2）；**确认前不改文件**。确认后：主副本必留原件根 `inbound/`并索引 → 按需复制 → 按需吸收；未点名可仅索引。放入≠分发他包。 **文档抽取分片**（子代理编排 ）：≥3 份新文档 → 只读扇出（每份返回 DOC/CR/OPEN/DEC 候选＋引用位置＋覆盖关系 ≤30 行）；登记/分类/影响集中；单份直做。

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
route=workflow:intake | step=scan | reads=rules/packets/intake/scan.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/intake/scan.md`；对不上 = 未遵守读链。
