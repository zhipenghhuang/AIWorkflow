# 步骤包 · onboard/capabilities

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：测试轨
- **workflow**：`onboard`
- **step**：`capabilities`（环境与工具检查）
- **packet**：`rules/packets/onboard/capabilities.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：环境与工具检查
- **产出**：{workroot}/capabilities/00-能力清单.md（默认静默；点名装配时另出建议）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 若无 `{workroot}/capabilities/`：自 `rules/templates/00-onboarding/capabilities/` 复制骨架（不覆盖已有清单正文）。 默认静默：不输出全量工具清单、不冒烟；可用性以清单为准，首次使用按契约降级。 仅当用户点名「装配能力」时：对照契约+参考目录+现清单盘点，确认后写入 `{workroot}/capabilities/`（及按需绑定/装配笔记）；刷基线 / 索引；安装指引见 README「宿主适配」。 例外：已配置且明显不可用、会影响预期的事项，一句话说明。禁强推、禁把选型写回包内契约。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 本步动作清单

- 若无 `{workroot}/capabilities/`：自 `rules/templates/00-onboarding/capabilities/` 复制骨架（不覆盖已有清单正文）。 默认静默：不输出全量工具清单、不冒烟。
- 可用性以清单为准，首次使用按契约降级。 仅当用户点名「装配能力」时：对照契约+参考目录+现清单盘点，确认后写入 `{workroot}/capabilities/`（及按需绑定/装配笔记）。
- 刷基线 / 索引。
- 安装指引见 README「宿主适配」。 例外：已配置且明显不可用、会影响预期的事项，一句话说明。禁强推、禁把选型写回包内契约。

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
route=workflow:onboard | step=capabilities | reads=rules/packets/onboard/capabilities.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/onboard/capabilities.md`；对不上 = 未遵守读链。
