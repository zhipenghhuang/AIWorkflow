# 步骤卡 · defect-fix/product_decision

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`defect-fix` / `product_decision`（产品处置读取）
- **packet**：`rules/packets/defect-fix/product_decision.md`
- **角色**：`defect-fixer`（缺陷修复编排）。平台拉取 → 分类 → 红证修复或产品评估 → 门禁 → 菜单 → 按 YAML hitl 提交/部署/回写 → 发布后验证；本步只做该角色职责；越界交回或升级。
- **上游**：`await_product`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`align`（进 `align` 前的 `when=product_decision_requires_alignment`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:product_decision_received`**：已收到产品处置结论；满足→真，否则跳过本步（不打开本包）。

## 2. 本步目标

- **目标**：产品处置读取
- **产出**：产品结论/附件/对齐清单

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 入口直达（拉取产品回复/产品回复/产品退回/继续缺陷）视为本步条件成立。
- 未读产品回复/附件前不得进 fix。
- 平台仍无产品回复/仍指派产品 → 输出 AWAIT_PRODUCT，不重复 handoff。
- 按 rules/defects/fix-collaboration.md 读全单：状态/解决码/指派人/全部备注/附件/新产品文档/关联需求。
- 归类：认可方案/修改后认可/判定实现缺陷/判定非问题/要求补充信息。
- 仅“回派”无备注/附件说明 → 视为未确认，输出 AWAIT_PRODUCT 请产品补结论。
- 认可或修改后认可或改判实现 → implementation_required + product_decision_requires_alignment。
- 要求补充/非问题 → need_clarification。
- 非问题按产品要求退回测试/关闭，不自行改代码。
- 读不全（solutionChannel=manual）→ 请用户补关键附件/备注，禁只看标题或只读一句备注。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读技能库找感觉。

## 7. 模板与证据

- **无强制模板**：§5 编排已给出动作/顺序；直接落 §2 产出。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:defect-fix | step=product_decision | agent=defect-fixer | packet=rules/packets/defect-fix/product_decision.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
