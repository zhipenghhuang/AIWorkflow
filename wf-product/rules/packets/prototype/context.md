# 步骤包 · prototype/context

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：产品
- **workflow**：`prototype`
- **step**：`context`（项目情境与参考基准）
- **packet**：`rules/packets/prototype/context.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/prototype/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/prototype/_region-shape.md`（结构与线框；进本区一次）。

## 2. 本步目标

- **目标**：项目情境与参考基准
- **产出**：{workroot}/{ver}/20-design/设计情境-{主题}.md（含设计简报/项目适配/交付等级）

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

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`prototype-and-interaction` → 见 §6 闭环。

### 本步动作清单

- 读 PRD/产品计划/UAT/现有系统截图/品牌/约束。
- 写清用户/任务/环境/设备/数据量/权限/术语/合规。 PRD 缺失 → 一句话说明缺口，按用户输入/产品档案继续，不阻塞。
- 禁把猜测写成 PRD 结论。 设计策略/项目适配：产品定位、与现有系统的关系、要借什么/不借什么、明确不做什么。
- 差异化只在产品定位需要时写。 2～3 个竞品/同类系统/设计规范参考（链接+日期）。
- 优先引用已有 `竞品分析`/`竞品对标` 的借·改编行。
- 无则本步补参考并写借/不借。 关键任务：补 1 张主用户旅程（步骤/情绪/痛点/机会）或写「单页工具不适用」。
- 设计原则 3～5 条。
- 交付等级=概念/线框/高保真/可交接。 覆盖目标：PRD F/A/AC → 页面/路由/状态。
- 未读主读/情境资料不得开画。 技能：`skills/prototype-and-interaction/SKILL.md`。
- 竞品借鉴命中时加 `competitive-intelligence-and-learning`。
- 能力 design-intelligence/browser-mcp 可选。

## 6. 技能指向（打开 → 执行 → 回本包）

> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  
> 同时只打开 **1** 个 skill；打开期间 `reads=` 可暂加该 skill 路径，闭环结束后以本 packet 为准。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `prototype-and-interaction` | **必开** | 进入本步即开（质量不降） | `skills/prototype-and-interaction/SKILL.md` | 必做区 → 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/prototype/_chain.md`。
- 子状态机（进区一次）：`rules/packets/prototype/_region-shape.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:prototype | step=context | packet=rules/packets/prototype/context.md | reads=rules/packets/prototype/context.md[+skill] | skills=prototype-and-interaction|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/prototype/context.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
