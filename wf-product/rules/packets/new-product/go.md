# 步骤包 · new-product/go

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：产品
- **workflow**：`new-product`
- **step**：`go`（立项评审）
- **packet**：`rules/packets/new-product/go.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/new-product/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/new-product/_region-define.md`（发现定义；进本区一次）。

## 2. 本步目标

- **目标**：立项评审
- **产出**：立项决策记录（Go/Hold/Kill + 依据/待verify/责任人，并入立项书）

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

- **HITL `confirm_go`**：出示问题/市场/方案/MVP 假设/成本收益/风险/结论（Go/Hold/Kill）；未过不写全量 PRD

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`zero-to-one-product-definition`、`customer-needs-discovery`、`competitive-intelligence-and-learning` → 见 §6 闭环。

### 本步动作清单

- 出示问题 / 用户 / 市场 / 竞品 / 方案与 MVP 假设 / 成本收益 / 风险 / 结论（Go / Hold / Kill）请确认。 批准（Go）才进入产品定义。
- Hold 列待验证项与责任人。
- Kill 记录原因并归档。 Hold/Kill 后直接 `wrap`/归档。
- `define/prd/deliver/launch` 的 `when: go_decision_go` 会自动跳过，不得继续写 PRD/排期/问发布。 **未过立项不写全量 PRD**（`rules/workflow.md` ）。

## 6. 技能指向（打开 → 执行 → 回本包）

> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  
> 同时只打开 **1** 个 skill；打开期间 `reads=` 可暂加该 skill 路径，闭环结束后以本 packet 为准。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `zero-to-one-product-definition` | **必开** | 进入本步即开（质量不降） | `skills/zero-to-one-product-definition/SKILL.md` | 必做区 → 回本包 |
| `customer-needs-discovery` | **必开** | 进入本步即开（质量不降） | `skills/customer-needs-discovery/SKILL.md` | 必做区 → 回本包 |
| `competitive-intelligence-and-learning` | **必开** | 进入本步即开（质量不降） | `skills/competitive-intelligence-and-learning/SKILL.md` | 必做区 → 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/new-product/_chain.md`。
- 子状态机（进区一次）：`rules/packets/new-product/_region-define.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:new-product | step=go | packet=rules/packets/new-product/go.md | reads=rules/packets/new-product/go.md[+skill] | skills=zero-to-one-product-definition,customer-needs-discovery,competitive-intelligence-and-learning|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/new-product/go.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
