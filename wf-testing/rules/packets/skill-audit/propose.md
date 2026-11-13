# 步骤卡 · skill-audit/propose

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守；重读按 §7 分级）；方法在 §6 指定节（打开→执行→回包）。**未打开本文件=未开跑本步**。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`skill-audit` / `propose`（出具建议）
- **packet**：`rules/packets/skill-audit/propose.md`
- **角色**：`onboard-agent`。按本步目标与 §5 动作执行；本步只做该角色职责；越界交回或升级。
- **上游**：`fit`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`apply`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。

## 2. 本步目标

- **目标**：出具建议
- **产出**：{workroot}/changes/能力技能体检-{yyyyMMdd}.md（工作产物，不进资料区）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：按 `rules/core/global-rules.md` §7 **分级重读并遵守**（中段=最小集，禁每步通读全文）；须先打开本步骤卡；心跳 `global=ok`=已按 §7 复核且步骤卡已实读；未复核不得写 `global=ok`。偏离写 `global=dev:<原因>`。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。
- **推进**：本流程为 `chain: full`；本步完成后进入下一未跳过步，直至 closeout。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 按 `rules/templates/00-onboarding/capability-skill-audit-report-template.md` 与技能体检：盘点→适配→拟变更→确认→复检。
- 含「生态检索」节。
- P0 置顶。
- 能力拟改只针对 `{workroot}/capabilities/`。
- 技能可改本包 `skills/`。
- 未确认不改。
- 可列「下一步：装配能力」。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读技能库找感觉。

## 7. 模板与证据

- **填写模板（主）**：`rules/templates/00-onboarding/capability-skill-audit-report-template.md`；只读本步用到的节，禁止整文件通读。
- **产出前自检**：对照模板必填节逐项填写；缺节、空节、未替换 `{…}` = 不合格（不得标完成）。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- §2 产出已按模板必填节落地；无空节、无未替换占位符。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:skill-audit | step=propose | agent=onboard-agent | packet=rules/packets/skill-audit/propose.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
