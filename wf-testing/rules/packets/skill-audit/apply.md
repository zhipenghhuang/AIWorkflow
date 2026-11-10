# 步骤卡 · skill-audit/apply

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（每步必读并逐条过）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`skill-audit` / `apply`（确认并应用）
- **packet**：`rules/packets/skill-audit/apply.md`
- **角色**：`onboard-agent`。按本步目标与 §5 动作执行；本步只做该角色职责；越界交回或升级。
- **上游**：`propose`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`closeout`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：确认并应用
- **产出**：已应用变更清单 + ValidateTemplateRefs / check_skills 自检结果

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：每步读 `rules/core/global-rules.md` 并逐条过（切步/过门/续跑都重读）；心跳 `global=ok` 表示本步已读；未读不得写 `global=ok`。偏离写 `global=dev:<原因>`。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_skill_changes`**：出示拟变更清单；确认后才改；未确认零改动。
- **条件判定 `hitl:skill_changes_pending`**：skill-audit 出具拟改且用户未确认；满足→真，否则跳过该门。
- **推进**：本流程为 `chain: full`；本步完成后进入下一未跳过步，直至 closeout。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 有拟改项 → skill_changes_pending=true，出示【拟变更清单】确认后按 技能体检：盘点→适配→拟变更→确认→复检 执行。
- 否则跳过。
- 改包后**必须**跑 `rules/tools/Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`。
- 改技能另跑 `check_skills.py --strict`。
- 失败不得声称完成。
- 结果写入体检报告。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 模板与证据

- **无强制模板**：§5 编排已给出动作/顺序；直接落 §2 产出。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:skill-audit | step=apply | agent=onboard-agent | packet=rules/packets/skill-audit/apply.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
