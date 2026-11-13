# 步骤卡 · defect-fix/assess_product

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`defect-fix` / `assess_product`（产品缺陷评估）
- **packet**：`rules/packets/defect-fix/assess_product.md`
- **角色**：`defect-fixer`（缺陷修复编排）。平台拉取 → 分类 → 红证修复或产品评估 → 门禁 → 菜单 → 按 YAML hitl 提交/部署/回写 → 发布后验证；本步只做该角色职责；越界交回或升级。
- **上游**：`triage`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`handoff_product`（进 `handoff_product` 前的 `when=product_defect`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:product_defect`**：triage 判定为产品缺陷；满足→真，否则跳过本步（不打开本包）。

## 2. 本步目标

- **目标**：产品缺陷评估
- **产出**：产品缺陷评估单（模板 rules/templates/20-design/product-defect-assessment-template.md）

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

- 按 rules/defects/fix-collaboration.md： 写评估单前必做实现核对（代码路径与/或接口契约·响应），结论写入评估单「实现核对」。
- 未核对不得出单。
- 写 缺陷评估-{BUG-ID}-{主题}-{yyyyMMdd}.md，落 {workroot}/00-governance/缺陷评估。
- 只客观写实现核对摘要/判定依据/问题影响/方案选项 A/B/C/推荐/影响面/待产品确认。
- 不写可编码实现细节、不拆开发任务、不排开发排期。
- 不写期望回复/时限威胁/超期升级/评估单版本过程史。
- 不得与正常迭代方案 方案-{主题}-… 混用。
- 口径存疑但实现路径清晰时，改出评审版修复方案（fix-collaboration §5.1 档位，落 20-design/BUG优化修复方案/），与评估单二选一、不重复出。
- 没有相符证明且不属于需求缺口变体 → 不判产品缺陷：按实现缺陷或 need_clarification 处理。
- 无平台/export/文档输入 → 评估单经 change/handoff 交付，口径与平台备注同源。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读技能库找感觉。

## 7. 模板与证据

- **填写模板（主）**：`rules/templates/20-design/product-defect-assessment-template.md`；只读本步用到的节，禁止整文件通读。
- **产出前自检**：对照模板必填节逐项填写；缺节、空节、未替换 `{…}` = 不合格（不得标完成）。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- §2 产出已按模板必填节落地；无空节、无未替换占位符。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:defect-fix | step=assess_product | agent=defect-fixer | packet=rules/packets/defect-fix/assess_product.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
