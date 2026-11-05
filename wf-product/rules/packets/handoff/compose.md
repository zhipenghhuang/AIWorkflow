# 步骤包 · handoff/compose

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：产品
- **workflow**：`handoff`
- **step**：`compose`（写交接单文档）
- **packet**：`rules/packets/handoff/compose.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/handoff/_chain.md`（进 workflow 一次）。

## 2. 本步目标

- **目标**：写交接单文档
- **产出**：自洽交接单文档（默认非 HO；落 outbound/{category}/）

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

- **HITL `confirm_intent`**：仅当 `intent_needs_confirm`：出示【意图理解】，确认后才落盘。意图已清 → 跳过（可一行回执即做）。细则 `clarification.md` §0。≠ `confirm_understanding`；≠ `confirm_handoff`

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- **默认入口**。读协作 ～ 与 `handoff-note-template.md`（择优，非填空卷）。 **意图择优**：先判 `intent_needs_confirm`（澄清 ）。真 → 完整【意图理解】停等再落盘。
- 假 → 一行【意图】回执后直写。禁止含糊「交接」直接成文。 五问→形态 A/B/C 或专模。
- 禁止整表粘贴。确认类优先 B 一页纸。 专模真源写版本目录，同轮实拷 `{workroot}/handoff/outbound/{category}/`。
- 无专模直接写出站类。不建 HO。
- 禁外印元数据。

## 6. 技能指向（打开 → 执行 → 回本包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/handoff/_chain.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:handoff | step=compose | packet=rules/packets/handoff/compose.md | reads=rules/packets/handoff/compose.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/handoff/compose.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
