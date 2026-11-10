# 步骤卡 · testing/report

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`testing` / `report`（输出报告）
- **packet**：`rules/packets/testing/report.md`
- **角色**：`report-agent`（收尾与报告（计划 vs 实际））。本步只做该角色职责；越界交回或升级。
- **上游**：`execute`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`closeout`
- **失败去向**：先修数据/证据或报阻塞；未 PASS/CONDITIONAL 不得进入 closeout
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：输出报告
- **产出**：{workroot}/{ver}/test-report.md + 【任务收尾】

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：按 `rules/core/global-rules.md` §7 重读并遵守全文；心跳 `global=ok` 表示本步已按 §7 复核；未按 §7 复核不得写 `global=ok`。偏离写 `global=dev:<原因>`。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **GATE `report-consistency`**：运行对应 verify；未过不得宣称完成。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。 报告门通过后只追加一次提交或交平台确认，不回到 execute。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 本步任务：出准出报告。
- 结论唯一（PASS/CONDITIONAL/FAIL/BLOCKED）。
- 失败与阻塞并存优先 FAIL（用例态见 `rules/defects/classification.md`）。
- 硬门槛：P0 全过。
- 全部处置=测意图有终态。
- 报告计数与执行记录一致。
- 对账/细节维可回指（无 ID 不算收口）。
- 原文对账未关>0 不得 PASS。
- 先正文再 `-Mode report`。
- 模板见 §7。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/40-report-review/test-report-template.md`；只读本步用到的节，禁止整文件通读。
- 验证命令：`verify/Invoke-Gate.ps1`（完成须 `-Claim` → `CLAIM: ALLOWED`）。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步完成 Claim 门：须 `CLAIM: ALLOWED` 后才可写完成态。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:testing | step=report | agent=report-agent | packet=rules/packets/testing/report.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
