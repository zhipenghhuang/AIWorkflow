# 步骤卡 · prototype/review

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`prototype` / `review`（设计评审）
- **packet**：`rules/packets/prototype/review.md`
- **角色**：`reviewer-agent`（产品落地文档独立评审（PRD/计划/设计/交付计划/实质变更重审））。用户选 B（AI）时按量规独立复核；只报缺口；结论落评审记录；不替写正文。选 A 时不替代用户放行；本步只做该角色职责；越界交回或升级。
- **上游**：`engineering`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`usability`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：设计评审
- **产出**：{workroot}/{ver}/20-design/设计评审-{主题}.md + prototype-coverage.md

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `select_review_mode`**：**STOP 二选一**：A 自行评审通过（HUMAN_APPROVED）｜B AI 独立评审（异人量规+评审记录）。适用 PRD/产品计划/设计交接等（`skills/artifact-review`）；同产物只问一次；点名「AI 评审」=B、「我审/自行通过」=A；未选不得宣称通过/定稿/交开发
- **条件判定 `hitl:landing_doc_review_needed`**：落地文档（PRD P2+、产品计划首版或实质变更、设计评审/设计交接、交付计划、实质变更重审、或用户点名评审）待选评审方式且本会话尚未选定；P0/普通 P1 light 且用户未点名时可假；**P1↑ 默认提示 A / SELF_CHECKED，不强制独立审；P2+ 必问 A/B**；满足→真，否则跳过该门。
- **GATE `design-review` when=ai_review_chosen**：仅选 B（AI）时运行 `-Mode design-review`；评审人≠作者、结论=通过；同目录必须有 `prototype-coverage.md`（覆盖矩阵硬；浏览器不可用时 `browser=unavailable` + 用户走查证据可过）且结论=通过；未 READY 不得交开发
- **条件判定 `gate:ai_review_chosen`**：用户已选 B（AI 独立评审）；满足→真，否则跳过该闸（步骤不跳过）。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`artifact-review`、`ui-visual-design-system` → 见 §6 闭环。

### 本步动作清单

- **先选评审方式**（`skills/artifact-review`）：A 自行通过｜B AI 独立审（派 `reviewer-agent` 或异上下文，禁作者自卖自夸）。
- 交开发前必问。
- **原型实走（硬）**：必须用浏览器 MCP（优先）或内置浏览器/Playwright 打开原型，逐页点击 IA/菜单/关键任务/空错权限/移动端，桌面+移动截图。
- 不得只读 HTML/文档或只看截图目录。
- 产出 `prototype-coverage.md`（PRD F/A/AC→页面/路由/状态/交互/字段→原型实现→截图），缺行不得通过。
- 选 A：ux-designer 出示 12 项评分卡自检 → reviewer-agent 核对 → 用户确认 HUMAN_APPROVED（批准人≠作者）。
- 选 B：按 `skills/ui-visual-design-system` 清单 + `rules/templates/20-design/design-review-template.md` 独立审：IA/一致性/状态/交互/文案/响应式/无障碍/视觉。
- 12 项评分卡。
- 阻断/重要/建议。
- 需修回 hi-fi（≤1）。
- 评审员必须核对覆盖矩阵与截图。
- 原型/PRD 是下限。
- 原型有明显缺陷可择优修正，但必须写偏离理由/影响/确认，重大偏离先 `OPEN-*`。
- **评审分片**（≥8 页）：维度扇出。
- 评分卡只算一次。
- 能力 design-review 可选。
- 未装按清单。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → 读必做，并读现场处置/判定/反合理化（技能有这些节时）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `artifact-review` | **必开** | 进入本步即开（质量不降） | `skills/artifact-review/SKILL.md` | 只读 L12-L93（硬门槛+方法+反合理化）→ 回本包 |
| `ui-visual-design-system` | **必开** | 进入本步即开（质量不降） | `skills/ui-visual-design-system/SKILL.md` | 只读 L11-L114（硬门槛+方法+反合理化）→ 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/20-design/design-review-template.md`；只读本步用到的节，禁止整文件通读。
- 验证命令：`verify/Invoke-Gate.ps1`（完成须 `-Claim` → `CLAIM: ALLOWED`）。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步 Claim 门受 `gate_when: ai_review_chosen` 约束：门执行时须 `CLAIM: ALLOWED` 才可写完成态；门被跳过 → 不产门回执，`claim=na` 并写 `when_eval=<假理由>`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:prototype | step=review | agent=reviewer-agent | packet=rules/packets/prototype/review.md | global=ok | skills=artifact-review,ui-visual-design-system|done|na | claim=ALLOWED|DENIED|na | next=…
```
