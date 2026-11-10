# 步骤卡 · solo/review_docs

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（每步先读并逐条过）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`solo` / `review_docs`（落地文档评审）
- **packet**：`rules/packets/solo/review_docs.md`
- **角色**：`doc-reviewer`（开发落地文档独立评审（实施前 · 与代码 Reviewer 分轨））。按 design-doc-review 量规独立复核需求基线/方案/ADR/前端设计说明等；只报缺口；不替写；不替代 confirm_* 授权与完成门；本步只做该角色职责；越界交回或升级。
- **上游**：`design`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`test_plan`（进 `test_plan` 前的 `when=plan_has_code_change`）
- **失败去向**：回 design 修方案卡/文档；不得带未闭环缺口进 test_plan/build
- **条件判定 `when:do_landing_doc_review`**：L2+ 有新增/变更落地文档或点名文档评审（不依赖是否已选 A/B）；满足→真，否则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：落地文档评审
- **产出**：评审-文档-*.md 或 HUMAN_APPROVED 声明

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：每步读 `rules/core/global-rules.md` 并逐条过；本步未读不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `select_review_mode`**：**STOP 二选一**：A 自行评审通过（HUMAN_APPROVED）｜B AI 独立评审（`doc-reviewer`）；同产物只问一次；未选不得进实施。适用需求基线/方案/ADR/前端设计说明等（见 `skills/design-doc-review`）
- **条件判定 `hitl:need_select_review_mode`**：L2+ 新产出落地文档或点名文档评审，且本会话未选 A/B；满足→真，否则跳过该门。
- **推进**：本步完成后沿父链进入下一未跳过步；口令为单步（只出方案/只出轻量方案/只评审/代码评审/方案评审/只提测/只出清单）或动作清单写明停止/跳转时，以口令/清单为准，即停并输出收尾骨架。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`design-doc-review` → 见 §6 闭环。

### 本步动作清单

- 技能见 §6 `design-doc-review`（只读必做区）。
- STOP 选 A/B。
- 未选不得进 test_plan/build。
- 本步不审 diff（代码走 review）。
- 审方案卡/验收表/用户版说明。
- 缺口回 design。
- 结论落 20-design 或 50-verification（按项目约定）。
- 本步触发以方案卡 §9 do_landing_doc_review 为准。
- L0/L1 小改可 false + 理由。
- L2+/高风险/新功能/落地文档 → true。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → 读必做，并读现场处置/判定/反合理化（技能有这些节时）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `design-doc-review` | **必开** | 进入本步即开（质量不降） | `skills/design-doc-review/SKILL.md` | 只读 L12-L98（硬门槛+方法+反合理化）→ 回本包 |

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
route=workflow:solo | step=review_docs | agent=doc-reviewer | packet=rules/packets/solo/review_docs.md | global=ok | skills=design-doc-review|done|na | claim=ALLOWED|DENIED|na | next=…
```
