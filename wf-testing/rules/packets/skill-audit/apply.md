# 步骤包 · skill-audit/apply

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：测试轨
- **workflow**：`skill-audit`
- **step**：`apply`（确认并应用）
- **packet**：`rules/packets/skill-audit/apply.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：确认并应用
- **产出**：已应用变更清单 + ValidateTemplateRefs / check_skills 自检结果

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 有拟改项 → skill_changes_pending=true，出示【拟变更清单】确认后按 playbook 执行；否则跳过。 改包后**必须**跑 `rules/tools/Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`；改技能另跑 `check_skills.py --strict`；失败不得声称完成；结果写入体检报告。

## 4. 本步门

- **HITL `confirm_skill_changes`**：出示【拟变更清单】（改 `skills/`·`capabilities/`·装配项）；确认后才改本包或给安装步骤；未确认零改动

## 5. 做法

### 本步动作清单

- 有拟改项 → skill_changes_pending=true，出示【拟变更清单】确认后按 playbook 执行。
- 否则跳过。 改包后**必须**跑 `rules/tools/Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`。
- 改技能另跑 `check_skills.py --strict`。
- 失败不得声称完成。
- 结果写入体检报告。

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
route=workflow:skill-audit | step=apply | reads=rules/packets/skill-audit/apply.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/skill-audit/apply.md`；对不上 = 未遵守读链。
