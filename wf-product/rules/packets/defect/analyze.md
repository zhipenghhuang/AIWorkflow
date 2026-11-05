# 步骤包 · defect/analyze

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：产品
- **workflow**：`defect`
- **step**：`analyze`（分析）
- **packet**：`rules/packets/defect/analyze.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/defect/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/defect/_region-pull.md`（拉取分析；进本区一次）。

## 2. 本步目标

- **目标**：分析
- **产出**：逐条分析结论（受理单 §3/§4）

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

- **本步必开技能（质量不降）**：`change-management` → 见 §6 闭环。

### 本步动作清单

- 按 `skills/change-management/SKILL.md` / 与 `rules/defects/platform-collaboration.md` ： 先分来源。
- 测试直提 → 产品独立定性。
- 开发评估单 → 复核开发判定与方案选项，不重做技术设计。 对照 PRD/设计判产品缺陷 vs 实现缺陷。
- 产品缺陷须有相符证明。 开发评估单读全文并核实现核对。
- 缺核对 → 退回开发补齐。
- 是否解决原问题、影响哪些 AC/范围/数据/合规/回归/回滚。
- 技术架构/实现细节不替开发评审。
- 结论五选一： 认可方案/修改后认可/不认可方案/判定实现defects/判定非问题。 测试无资料默认实现缺陷正确。
- 需求缺口由产品终审，不责备测试默认。 体验类不挡主路径 → 转 change，不硬开产品缺陷。 测试直提结论五选一：产品缺陷/实现defects/非问题/重复/信息不足。 批量时以侦察回执为输入。
- **五选一/处置建议/相符证明集中**，不采信子代理终态。 给出处置建议：立即修/下版/不修/退回开发/补充信息。

## 6. 技能指向（打开 → 执行 → 回本包）

> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  
> 同时只打开 **1** 个 skill；打开期间 `reads=` 可暂加该 skill 路径，闭环结束后以本 packet 为准。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `change-management` | **必开** | 进入本步即开（质量不降） | `skills/change-management/SKILL.md` | 必做区 → 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/defect/_chain.md`。
- 子状态机（进区一次）：`rules/packets/defect/_region-pull.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:defect | step=analyze | packet=rules/packets/defect/analyze.md | reads=rules/packets/defect/analyze.md[+skill] | skills=change-management|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/defect/analyze.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
