# 步骤包 · defect/apply

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：产品
- **workflow**：`defect`
- **step**：`apply`（联动与评审）
- **packet**：`rules/packets/defect/apply.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/defect/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/defect/_region-act.md`（处置回写；进本区一次）。

## 2. 本步目标

- **目标**：联动与评审
- **产出**：受理单 §6 + 变更单/最新 PRD/AC/计划/UAT + 缺陷处置单 + 附件清单

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

- **仅在 decide 确认后执行**。
- 纯拉取/只读分析止于 analyze，不落处置单。 **产品缺陷才更新 PRD/AC/计划/UAT**。
- 实现defects/非问题/重复/信息不足只产缺陷处置单与回执，不进入 PRD/AC 更新。 即使无需联动，也至少落缺陷处置单/受理单回执。
- 不适用项写原因。 按 `workflows/change.yaml` 的 apply 规则更新 PRD/AC/原型/交付计划/产品计划/需求池/UAT/发布检查。
- 已有受理单（pull 建档）就地更新，不重复建档。
- 同一缺陷多轮处理只留一份现行受理单。 产品缺陷确认 → 产出 `{workroot}/{ver}/30-changes/缺陷处置-{BUG-ID}-{主题}-{yyyyMMdd}.md` （模板 `rules/templates/30-review-change/product-defect-disposition-template.md`），写清判定、依据、新口径、对开发要求、验收标准、指派对象。 实现defects/非问题/重复/信息不足也产出缺陷处置单（说明+下一步+指派），不要求 PRD 变更。 实质变更 → 走 review 步（产品视角：是否解决原问题/AC 影响/范围/风险。
- 不评价技术实现细节）。 生成回写附件：缺陷处置单/受理单/变更单/评审意见/PRD 变更摘要（按需）。
- 不修改代码或技术方案。 **缺陷双通道**：本步已回写平台 → **不**再强制 `BUG` 整包。无平台/`export`/用户点名「缺陷交接包」→ **先问后发**，确认后 `handoff.send` 自包含处置详单。平台附件与包内口径同源，禁重复造口径。 联动审计（子代理编排 ）：≥4 份受影响文档 → 单写手完成后派 verifier-agent 只读核验（受理单 ＋改动产物），返回未更新/旧口径/待补 ≤30 行。 三包独立：产品文档落本包目录，附件上传平台。
- 不引用开发/测试包内部路径。 平台附件/开发评估单/新产品文档：先按 `rules/doc-governance.md` 【入站分析】（多为 T6）。
- 确认后落 `inbound/{ver|topic}/`，同步处置结论到工作区。
- S1/S2/S3 同批进 `inbound/_archive/`。

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
- 子状态机（进区一次）：`rules/packets/defect/_region-act.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:defect | step=apply | packet=rules/packets/defect/apply.md | reads=rules/packets/defect/apply.md[+skill] | skills=change-management|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/defect/apply.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
