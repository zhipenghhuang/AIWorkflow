# 步骤卡 · solo/review

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`solo` / `review`（代码评审）
- **packet**：`rules/packets/solo/review.md`
- **角色**：`reviewer-agent`（代码评审/独立核验）。RP/AC/SC↔改动文件↔验证输出对账；只报正确性/需求覆盖/安全/性能/范围/体验三维缺口；核验不替代机器门禁；本步只做该角色职责；越界交回或升级。
- **前置**：有 UI → .gate/frontend/parity-matrix.md/route-coverage.json/design-qa.md 存在且非空；高风险 → .gate/plan-coverage.md（如已生成）；非前端/低档 → 无
- **上游**：`build`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`test`
- **失败去向**：回 build 补前端交付物/方案覆盖；不得以代码/测试/API 200 代替，不得判通过
- **条件判定 `when:review_required`**：有实施且（L2+/L3，或高风险/大改/破坏性，或 **L2+ 新功能**，或 **L1+ 用户可见 UI 命中前端硬门 A 级**，或点名）；满足→真，否则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：代码评审
- **产出**：评审结论/缺口 + .gate/review.md

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

- **本步必开技能（质量不降）**：`code-review`、`engineering-quality` → 见 §6 闭环。

### 本步动作清单

- 技能见 §6 `code-review` + §6 `engineering-quality`。
- 核验者≠实施者。
- 覆盖本轮 diff+AC/SC。
- 写 .gate/review.md。
- 评审记录路径回写方案卡 §9 过程证据。
- 有 UI 核 parity 产物。
- 免审须记理由。
- 免审不免自测。
- 方法只认 code-review。
- 本步触发以方案卡 §9 review_required 为准。
- L0/L1 小改且未命中 A 级可 false + 理由。
- L1+ UI 命中前端硬门 A 级/L2+/高风险/新功能/点名 → true。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → 读必做，并读现场处置/判定/反合理化（技能有这些节时）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `code-review` | **必开** | 进入本步即开（质量不降） | `skills/code-review/SKILL.md` | 只读 L11-L95（硬门槛+方法+反合理化）→ 回本包 |
| `engineering-quality` | **必开** | 进入本步即开（质量不降） | `skills/engineering-quality/SKILL.md` | 只读 L13-L65（硬门槛+方法）→ 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **无强制模板**：§5 编排已给出动作/顺序；直接落 §2 产出。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:solo | step=review | agent=reviewer-agent | packet=rules/packets/solo/review.md | global=ok | skills=code-review,engineering-quality|done|na | claim=ALLOWED|DENIED|na | next=…
```
