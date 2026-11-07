# 步骤卡 · prd/prototype

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（本会话已读则不重读全文）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`prd` / `prototype`（页面原型（条件））
- **packet**：`rules/packets/prd/prototype.md`
- **角色**：`ux-designer`（产品设计（信息架构/线框/视觉/高保真原型/评审/handoff/展示材料））。没有专职设计师时，由产品经理戴“设计帽子”，产出可用、可评审、可交付开发的高保真原型；本步只做该角色职责；越界交回或升级。
- **上游**：`prd`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`review`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:has_ui_requirement`**：有页面/界面需求或点名画原型；满足→真，否则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：页面原型（条件）
- **产出**：{workroot}/{ver}/20-design/原型-{主题}.html + 原型说明/交接要点（条件）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：本会话已读 `rules/core/global-rules.md` 则不重读全文；未读过不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`prototype-and-interaction`、`ui-visual-design-system` → 见 §6 闭环。

### 本步动作清单

- 条件步：有界面/页面需求或用户点名「画原型」才走。
- 纯后端/接口跳过。
- 按 `prototype` 流程 执行（情境 → IA → 线框 → 视觉 → 高保真 → 工程化 → 评审 → 可用性 → 交接）。
- 只执行所列步骤，不执行 prototype.closeout（由本链统一收尾）。
- 原型完成后回 PRD 评审。
- PRD 追溯矩阵「原型/页面」列回填。
- 技能见 §6 `prototype-and-interaction`、§6 `ui-visual-design-system`。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → 读必做，并读现场处置/判定/反合理化（技能有这些节时）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `prototype-and-interaction` | **必开** | 进入本步即开（质量不降） | `skills/prototype-and-interaction/SKILL.md` | 只读 L11-L22（硬门槛+方法）→ 回本包 |
| `ui-visual-design-system` | **必开** | 进入本步即开（质量不降） | `skills/ui-visual-design-system/SKILL.md` | 只读 L11-L114（硬门槛+方法+反合理化）→ 回本包 |

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
route=workflow:prd | step=prototype | agent=ux-designer | packet=rules/packets/prd/prototype.md | global=ok | skills=prototype-and-interaction,ui-visual-design-system|done|na | claim=ALLOWED|DENIED|na | next=…
```
