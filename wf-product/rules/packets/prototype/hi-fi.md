# 步骤包 · prototype/hi-fi

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：产品
- **workflow**：`prototype`
- **step**：`hi-fi`（高保真可点击原型）
- **packet**：`rules/packets/prototype/hi-fi.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/prototype/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/prototype/_region-visual.md`（视觉与评审；进本区一次）。

## 2. 本步目标

- **目标**：高保真可点击原型
- **产出**：{workroot}/{ver}/20-design/prototype/index.html + design-tokens.css

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

- **本步必开技能（质量不降）**：`ui-visual-design-system` → 见 §6 闭环。

### 本步动作清单

- 静态 HTML/CSS（可少量 JS），浏览器直接打开。
- 覆盖核心流程、状态、响应式、无障碍基础。 数据模型/seed/重置。
- 导航/历史/返回/未保存提醒。
- 每页状态矩阵逐项落地。
- 单据类 A4 打印/导出。 原型/PRD 版本元数据（页面 title/meta 或说明文件）。 不做生产级后端。
- 无设计师时以“清晰、一致、可用”为准，不冒充品牌级视觉。 **分页构建**（子代理编排 ）：≥8 页 → 中心先定 IA/tokens/组件/页面契约。
- 一页或一小批一子代理，只写 `原型/pages/{page}.html`。
- pages 不相交可并行≤3。
- **禁止并行写 `prototype/index.html`**。
- 超时降级直做。
- 编排组装 index。
- verifier 一致性/无障碍。
- <8 页单 agent。
- 声明 `mode=`。 技能：`skills/prototype-and-interaction/SKILL.md`、`skills/ui-visual-design-system/SKILL.md`。
- 能力 ui-generation 可选增强，未装不影响。

## 6. 技能指向（打开 → 执行 → 回本包）

> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  
> 同时只打开 **1** 个 skill；打开期间 `reads=` 可暂加该 skill 路径，闭环结束后以本 packet 为准。

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
route=workflow:prototype | step=hi-fi | packet=rules/packets/prototype/hi-fi.md | reads=rules/packets/prototype/hi-fi.md[+skill] | skills=ui-visual-design-system|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/prototype/hi-fi.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
