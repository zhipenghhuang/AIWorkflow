# 步骤卡 · deliver/uat

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`deliver` / `uat`（UAT 验收）
- **packet**：`rules/packets/deliver/uat.md`
- **角色**：`pm-lead`（交付编排与变更处置（排期/跟进/受理/变更/缺陷平台/UAT/发布/复盘/展示））。统一受理需求与问题 → 分诊定性 → 影响评估 → 处置确认 → 联动更新 → 验证关闭；平台缺陷可拉取、分析并回写；本步只做该角色职责；越界交回或升级。
- **上游**：`followup`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`release`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:has_uat`**：本轮有 UAT/验收要求（发布门必须核）；满足→真，否则跳过本步（不打开本包）。

## 2. 本步目标

- **目标**：UAT 验收
- **产出**：{workroot}/{ver}/40-delivery/UAT-{ver}-{yyyyMMdd}.md（模板 rules/templates/40-delivery/uat-acceptance-template.md）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **GATE `uat-evidence`**：运行 `verify/Invoke-Gate.ps1 -Mode uat`；AC 覆盖、证据、有条件通过的责任人/接受人；未 READY 不得写 UAT 通过。无 UAT 要求可写 `verdict: 不适用` + 依据/批准人，门放行但记警告
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`uat-and-retrospective` → 见 §6 闭环。

- **条件技能**：`analytics-and-experimentation`（有指标/埋点/实验） → 命中则同样走 §6 闭环。

### 本步动作清单

- 技能见 §6 `uat-and-retrospective`。
- 按 PRD 验收标准**逐条对照**（结果+证据）。
- 运行 `verify/Invoke-Gate.ps1 -Mode uat`。
- 未 READY 不得写“UAT 通过/可发布”。
- **分模块核验**（子代理编排 ）：≥3 模块 → 按模块只读扇出（AC 结果+证据+缺口 ≤30 行）。
- UAT 结论集中。
- 单模块直做。
- 可选输入：若项目已有测试报告/提测单/其它验收资料（任意路径/来源）则读。
- 无则用现有inbound/用户输入，不阻塞。
- 测试报告是证据，不替代 UAT 结论。
- 收到测试报告/准出 → 有包则 `handoff.receive`，无包则读报告正文。
- UAT 通过后默认交 UAT 记录。
- `UAT` 包按需先问后发。
- 判定产品缺陷 vs 实现缺陷（依据：PRD 原文/设计对照）。
- 结论：通过/不通过/有条件通过（有条件通过须列遗留、责任人与接受人）。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。
> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `uat-and-retrospective` | **必开** | 进入本步即开（质量不降） | `skills/uat-and-retrospective/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `analytics-and-experimentation` | 条件开 | 有指标/埋点/实验 | `skills/analytics-and-experimentation/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（主）**：`rules/templates/40-delivery/uat-acceptance-template.md`；只读本步用到的节，禁止整文件通读。
- **产出前自检**：对照模板必填节逐项填写；缺节、空节、未替换 `{…}` = 不合格（不得标完成）。
- 验证命令：`verify/Invoke-Gate.ps1`（完成须 `-Claim` → `CLAIM: ALLOWED`）。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- §2 产出已按模板必填节落地；无空节、无未替换占位符。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步完成 Claim 门：须 `CLAIM: ALLOWED` 后才可写完成态。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:deliver | step=uat | agent=pm-lead | packet=rules/packets/deliver/uat.md | global=ok | skills=uat-and-retrospective|done|na | claim=ALLOWED|DENIED|na | next=…
```
