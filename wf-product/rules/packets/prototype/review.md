# 步骤包 · prototype/review

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：产品
- **workflow**：`prototype`
- **step**：`review`（设计评审）
- **packet**：`rules/packets/prototype/review.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/prototype/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/prototype/_region-visual.md`（视觉与评审；进本区一次）。

## 2. 本步目标

- **目标**：设计评审
- **产出**：{workroot}/{ver}/20-design/设计评审-{主题}.md + prototype-coverage.md

## 3. 本步硬约束

### 开局硬约束（本步可执行摘要）

- 1. **先意图、再动作**（`confirm_task_intent`）：未确认禁写正式 PRD/外发/定范围。
- 2. **短读跟随 + 一手源**：`activeContext` + 进行中（`packet=`/`region=`）+ 偏好/洞见/坑 ≤3。
- 3. **理解→方案双确认未完成 → 不得入池/写正式 PRD/定版本范围**。
- 4. **状态机读链 + 技能闭环**：见本包「本步读链与防丢失」。必开 skill 须打开→执行→回步骤包（质量不降）。
- 5. **完成分层**：`-Claim -Mode <…>` → 只认 `CLAIM: ALLOWED`。
- 6. **原型硬门**：实走 + 覆盖矩阵；缺行不得过。
- 7. **禁臆造**；AC 可观测；变更无单不实施；UAT 未过不发布。
- 8. **切步/出子机 → 心跳**，必带 `packet=`。

### 本步读链与防丢失

- **编排**：本文 §5 +（若 §7 列出）一个模板。
- **方法质量**：§6 必开/条件开技能 → **打开→执行→回本包**（同时 1 个 skill）；禁止用粘贴代替实读。
- **禁止**：通读 rules / 多 step packet / 预读本 workflow 全部 skill。
- **完成声称**：有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **上下文锚**：`packet=`/`reads=` 必须含本 packet；切步/出子机前心跳刷新。


## 4. 本步门

- **HITL `select_review_mode`**：**STOP 二选一**：A 自行评审通过（HUMAN_APPROVED）｜B AI 独立评审（异人量规+评审记录）。适用 PRD/产品计划/设计交接等（`skills/artifact-review`）；同产物只问一次；点名「AI 评审」=B、「我审/自行通过」=A；未选不得宣称通过/定稿/交开发
- **GATE `design-review` when=ai_review_chosen**：仅选 B（AI）时运行 `-Mode design-review`；评审人≠作者、结论=通过；同目录必须有 `prototype-coverage.md`（覆盖矩阵硬；浏览器不可用时 `browser=unavailable` + 用户走查证据可过）且结论=通过；未 READY 不得交开发

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`artifact-review`、`ui-visual-design-system` → 见 §6 闭环。

### 本步动作清单

- **先选评审方式**（`skills/artifact-review`）：A 自行通过｜B AI 独立审（派 `reviewer-agent` 或异上下文，禁作者自卖自夸）。交开发前必问。 **原型实走（硬）**：必须用浏览器 MCP（优先）或内置浏览器/Playwright 打开原型，逐页点击 IA/菜单/关键任务/空错权限/移动端，桌面+移动截图。
- 不得只读 HTML/文档或只看截图目录。产出 `prototype-coverage.md`（PRD F/A/AC→页面/路由/状态/交互/字段→原型实现→截图），缺行不得通过。 选 A：ux-designer 出示 12 项评分卡自检 → reviewer-agent 核对 → 用户确认 HUMAN_APPROVED（批准人≠作者）。 选 B：按 `skills/ui-visual-design-system` 清单 + `rules/templates/20-design/design-review-template.md` 独立审：IA/一致性/状态/交互/文案/响应式/无障碍/视觉。
- 12 项评分卡。
- 阻断/重要/建议。
- 需修回 hi-fi（≤1）。评审员必须核对覆盖矩阵与截图。 原型/PRD 是下限。
- 原型有明显缺陷可择优修正，但必须写偏离理由/影响/确认，重大偏离先 `OPEN-*`。 **评审分片**（≥8 页）：维度扇出。
- 评分卡只算一次。能力 design-review 可选。
- 未装按清单。

## 6. 技能指向（打开 → 执行 → 回本包）

> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  
> 同时只打开 **1** 个 skill；打开期间 `reads=` 可暂加该 skill 路径，闭环结束后以本 packet 为准。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `artifact-review` | **必开** | 进入本步即开（质量不降） | `skills/artifact-review/SKILL.md` | 必做区 → 回本包 |
| `ui-visual-design-system` | **必开** | 进入本步即开（质量不降） | `skills/ui-visual-design-system/SKILL.md` | 必做区 → 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/prototype/_chain.md`。
- 子状态机（进区一次）：`rules/packets/prototype/_region-visual.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 验证：`verify/Invoke-Gate.ps1`（完成声称加 `-Claim`）；有 UI 另按 §5 前端硬门。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:prototype | step=review | packet=rules/packets/prototype/review.md | reads=rules/packets/prototype/review.md[+skill] | skills=artifact-review,ui-visual-design-system|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/prototype/review.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
