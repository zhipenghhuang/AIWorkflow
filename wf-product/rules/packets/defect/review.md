# 步骤卡 · defect/review

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`defect` / `review`（重审（条件））
- **packet**：`rules/packets/defect/review.md`
- **角色**：`reviewer-agent`（产品落地文档独立评审（PRD/计划/设计/交付计划/实质变更重审））。用户选 B（AI）时按量规独立复核；只报缺口；结论落评审记录；不替写正文。选 A 时不替代用户放行；本步只做该角色职责；越界交回或升级。
- **上游**：`apply`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`writeback`（进 `writeback` 前的 `when=remark_writeback`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:substantive_change`**：实质变更需重审；满足→真，否则跳过本步（不打开本包）。

## 2. 本步目标

- **目标**：重审（条件）
- **产出**：评审记录（{workroot}/{ver}/10-requirements/评审-{主题}-{yyyyMMdd}.md）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `select_review_mode`**：**STOP 二选一**：A 自行评审通过（HUMAN_APPROVED）｜B AI 独立评审（异人量规+评审记录）。适用 PRD/产品计划/设计交接等（`skills/artifact-review`）；同产物只问一次；点名「AI 评审」=B、「我审/自行通过」=A；未选不得宣称通过/定稿/交开发
- **条件判定 `hitl:landing_doc_review_needed`**：落地文档（PRD P2+、产品计划首版或实质变更、设计评审/设计交接、交付计划、实质变更重审、或用户点名评审）待选评审方式且本会话尚未选定；P0/普通 P1 light 且用户未点名时可假；**P1↑ 默认 B（AI 独立评审），选 A 须用户明确 + 独立复核；P2+ 必问 A/B**；满足→真，否则跳过该门。
- **HITL `confirm_prd`**：评审结论为「通过（可定稿）」且用户点名定稿/进入排期时出示；**出示前**须有【完稿自检摘要】且 `-Mode prd` 非 BLOCKED；定稿前不排期；仅评审不弹门
- **条件判定 `hitl:finalize_requested`**：评审通过且用户点名定稿/进入排期（仅评审不触发）；满足→真，否则跳过该门。
- **GATE `product-review` when=ai_review_chosen**：仅选 B（AI）时运行 `-Mode review`；评审人≠作者；READY 后取 `gate_id`；选 A 不跑本门，须 HUMAN_APPROVED + `approved_by` + 自检摘要 + 复跑 `-Mode prd` 至 READY
- **条件判定 `gate:ai_review_chosen`**：用户已选 B（AI 独立评审）；满足→真，否则跳过该闸（步骤不跳过）。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`artifact-review`、`review-and-finalize` → 见 §6 闭环。

### 本步动作清单

- **单一出处**：通用评审/定稿规则以 `change.review` 为准。
- 本步只保留产品缺陷平台差异。
- 条件步：实质变更/方案影响 AC/范围/权限/数据规则/NFR/版本目标才走。
- 纯文字澄清跳过。
- **先 STOP【评审方式】**（`skills/artifact-review`）：A 自行通过｜B AI 独立审。
- 未选不得恢复定稿。
- **选 A**：【完稿自检摘要】+ 产品视角要点 → HUMAN_APPROVED → `confirm_prd`。
- 不跑 `-Mode review`。
- 须 `-Mode prd` 非 BLOCKED（涉及 PRD 实质变更时）。
- **选 B**：先写评审记录再 `-Mode review`。
- 产品视角（是否解决原问题、AC/范围/风险/合规）。
- 技术实现不替开发评。
- 通过后回写平台并恢复 PRD `APPROVED`。
- 需修回 apply（≤1）。
- 未重审不得标已定稿。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。
> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `artifact-review` | **必开** | 进入本步即开（质量不降） | `skills/artifact-review/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `review-and-finalize` | **必开** | 进入本步即开（质量不降） | `skills/review-and-finalize/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **无强制模板**：§5 编排已给出动作/顺序；直接落 §2 产出。
- 验证命令：`verify/Invoke-Gate.ps1`（完成须 `-Claim` → `CLAIM: ALLOWED`）。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步 Claim 门受 `gate_when: ai_review_chosen` 约束：门执行时须 `CLAIM: ALLOWED` 才可写完成态；门被跳过 → 不产门回执，`claim=na` 并写 `when_eval=<假理由>`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:defect | step=review | agent=reviewer-agent | packet=rules/packets/defect/review.md | global=ok | skills=artifact-review,review-and-finalize|done|na | claim=ALLOWED|DENIED|na | next=…
```
