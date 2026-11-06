# 步骤包 · prototype/visual

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-product
- **workflow**：`prototype`
- **step**：`visual`（视觉方向与设计系统）
- **packet**：`rules/packets/prototype/visual.md`
- **角色**：`ux-designer`（产品设计（信息架构/线框/视觉/高保真原型/评审/handoff/展示材料））。没有专职设计师时，由产品经理戴“设计帽子”，产出可用、可评审、可交付开发的高保真原型；本步只做该角色职责；越界交回或升级。
- **上游**：`wireframe`（取其产出为本步输入；该步被 `when` 跳过时按缺口停/补齐）
- **后续**：`hi-fi`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/prototype/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/prototype/_region-visual.md`（视觉与评审；进本区一次）。

## 2. 本步目标

- **目标**：视觉方向与设计系统
- **产出**：视觉稿/设计 tokens/标注（{workroot}/{ver}/20-design/）

## 3. 本步硬约束

### 开局硬门（3 条；其余见 cold-start §1）

- 1. **每轮先判、再动手**：先判新任务/续跑/只读；新任务或范围变化 → 复述目标/范围/验收并确认；续跑一行确认；只读一句话；首行锚 `route/step/packet` 或 `mode=analyze`；未确认禁写、禁下结论。
- 7. **完成只认门**：`-Claim` → `CLAIM: ALLOWED`；无 ALLOWED 禁写完成/通过/可提测。原型实走 + 覆盖矩阵；UAT 未过不发布。
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

- **HITL `confirm_design`**：IA/线框/2～3 个视觉方向/tokens；确认后才做高保真
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`ui-visual-design-system` → 见 §6 闭环。

### 本步动作清单

- 技能：`skills/ui-visual-design-system/SKILL.md`。 设计系统策略：复用现有品牌/系统。
- 无则选一套主系统，不混搭。
- tokens 单一来源。 2～3 个视觉方向（气质/配色/字体/适用场景），写清为什么适合本产品，推荐 1 个并说明理由。
- 产出 design tokens（颜色/字体/间距/圆角/阴影/组件）。 confirm_design：出示 IA/线框/视觉方向/tokens 请确认。
- 确认后才做高保真。 能力（可选）：design-intelligence ui-generation frontend-design。
- 未装 = 按包内技能。

## 6. 技能指向（打开 → 执行 → 回本包）

> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `ui-visual-design-system` | **必开** | 进入本步即开（质量不降） | `skills/ui-visual-design-system/SKILL.md` | 必做区 → 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/prototype/_chain.md`。
- 子状态机（进区一次）：`rules/packets/prototype/_region-visual.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:prototype | step=visual | agent=ux-designer | packet=rules/packets/prototype/visual.md | reads=rules/packets/prototype/visual.md[+skill] | skills=ui-visual-design-system|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/prototype/visual.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
