# 步骤包 · solo/test

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-development
- **workflow**：`solo`
- **step**：`test`（轻量测试）
- **packet**：`rules/packets/solo/test.md`
- **角色**：`verifier-agent`（独立验证（开发轨））。只读核验验收清单、diff、证据与完成门结果；返回通过/需修/阻塞；不改代码、不做最终交付判断；本步只做该角色职责；越界交回或升级。
- **上游**：`build`（取其产出为本步输入；该步被 `when` 跳过时按缺口停/补齐）
- **后续**：`wrap`
- **失败去向**：回 build 修复；P0 未过不得进 wrap，修后重跑原用例 + 冒烟 + 影响面
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/solo/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/solo/_region-build.md`（建造验证；进本区一次）。

## 2. 本步目标

- **目标**：轻量测试
- **产出**：轻量测试报告（{workroot}/50-verification/测试报告-{主题}-{yyyyMMdd}.md）+ .gate/wf-development/completion.json

## 3. 本步硬约束

### 开局硬门（3 条；其余见 cold-start §1）

- 1. **每轮先判、再动手**：先判新任务/续跑/只读；新任务或范围变化 → 复述目标/范围/验收并确认；续跑一行确认；只读一句话；首行锚 `route/step/packet` 或 `mode=analyze`；未确认禁写、禁下结论。
- 7. **完成只认门**：`-Claim` → `CLAIM: ALLOWED`；无 ALLOWED 禁写完成/通过/可提测。有 UI → 当前包内前端硬门；无 UI 标 `na`。
- 11. **技能闭环**：§6 必开 skill 打开→执行→回包；禁止粘贴代替。
- 其余硬约束见 `rules/core/cold-start.md` §1（常驻；勿在步内重读全文）。

### 本步读链与防丢失

- **编排**：本文 §5 +（若 §7 列出）一个模板。
- **方法质量**：§6 必开/条件开技能 → **逐个打开→执行→回本包**（一次 1 个）；禁止用粘贴代替实读。
- **禁止**：通读 rules / 多 step packet / 预读本 workflow 全部 skill。
- **完成声称**：有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **上下文锚**：`packet=`/`reads=` 必须含本 packet；切步/出子机前心跳刷新。

### 本步禁止

- 禁止读取本清单外的 rules / skills 正文；需要跳转只按 §6/§7 各一次。
- 禁止跳过 §6 必开技能，或用摘要代替实读。
- 禁止未过 §4 门或未出 §8 信号就宣称完成、推进或写「已通过」。

## 4. 本步门

- **GATE `completion-gate` when=solo_gate_required**：任务开始 `-StartTask`；运行 `verify/Invoke-Gate.ps1 -Acceptance ...`；写 `.gate/wf-development/completion.json`；**前端套装与 capture 只认本包硬约束与做法**；**写完成前 `-Claim`，只认 `CLAIM: ALLOWED`**；空 diff=`NOT_VERIFIED`、dry-run=`DRY_RUN`、缺项 → `BLOCKED`
- **推进**：本步完成后沿父链进入下一未跳过步；口令为单步（只出方案/只评审/代码评审/方案评审/只提测/只出清单/轻量方案）或动作清单写明停止/跳转时，以口令/清单为准，即停并输出收尾骨架。

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`test-design-and-execution` → 见 §6 闭环。

### 本步动作清单

- 技能：`skills/test-design-and-execution/SKILL.md`（先读再做）。
- 模板 `rules/templates/40-delivery/lite-test-report-template.md`。
- 口径 `lightweight.md`。
- 门禁见 `verify/README.md`。 **开发自验**（非准出）：按方案卡测试点 + **AC 走查**。
- 覆盖集（按风险完整，不是只跑一条）=主路径 + 1 边界 + 1 异常 + 权限/数据域（适用时）+ 受影响回归。
- 前端看状态/视口/console/network/截图。
- 后端看响应/错误码/日志。
- 数据变更看迁移前后与回滚路径。 先 UI 后 Network。
- 不猜未见 API。
- 失败留证。
- 同一失败修复后跑「原用例 + 冒烟 + 影响面」，2 次无效换路径/升级。 失败分类：产品/实现/环境/数据/测试问题。
- 产品范围问题停下问用户，不按现网实现改预期。 写报告：范围/环境/AC 走查/测试点/结果/证据/defects/缺口/verdict（开发自验）。
- P0 未过 = FAIL。
- 禁写「已准出」。 运行 `verify/Invoke-Gate.ps1 -ProjectRoot "." -Acceptance "<方案卡路径>"`。
- 读 `.gate/wf-development/completion.json`。
- 非 COMPLETE 不得进 wrap 报完成。 无方案卡/验收表（单独测试入口）：仍按 `lightweight.md` 出完整证据块（范围/检查/结果/证据/缺口），不跑 completion-gate。
- wrap 写 `verification=not_applicable`。 纯文档/无代码改动：只核链接/占位/事实，不跑 completion-gate。
- wrap 写 `verification=not_applicable` + 依据。

### 前端硬门（本步含 UI · 单源）

- **必读**：`rules/core/frontend-gate.md` §1–§5（打开→按本步产出/证据执行→回包）。
- 无 UI → 整节标 `na` + 一句理由；有 UI 不得只看代码/测试/API 200。
- 证据、分级、矩阵、截图/console/network 要求只认该文件，不在本包重复。

## 6. 技能指向（打开 → 执行 → 回本包）

> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `test-design-and-execution` | **必开** | 进入本步即开（质量不降） | `skills/test-design-and-execution/SKILL.md` | 必做区 → 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/solo/_chain.md`。
- 子状态机（进区一次）：`rules/packets/solo/_region-build.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 验证：`verify/Invoke-Gate.ps1`（完成声称加 `-Claim`）；有 UI 另按 §5 前端硬门。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:solo | step=test | agent=verifier-agent | packet=rules/packets/solo/test.md | reads=rules/packets/solo/test.md[+skill] | skills=test-design-and-execution|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/solo/test.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
