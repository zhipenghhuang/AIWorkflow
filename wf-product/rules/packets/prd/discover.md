# 步骤包 · prd/discover

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：产品
- **workflow**：`prd`
- **step**：`discover`（需求洞察与需求池）
- **packet**：`rules/packets/prd/discover.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/prd/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/prd/_region-discover.md`（发现与优先级；进本区一次）。

## 2. 本步目标

- **目标**：需求洞察与需求池
- **产出**：需求池/洞察/竞品分析（{workroot}/requirement-pool.md 或 {workroot}/{ver}/10-requirements/洞察|竞品分析-*.md）

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

- **HITL `confirm_understanding`**：出示【理解复述】（谁/场景/问题/现有替代/代价/目标/范围/非目标/证据/假设）+【推荐方案要点】（主路径/关键rules/异常期望/验收口径/不做）+ 缺口清单；涉及换迭代/相对上版时附**本期差量要点**（增/改/删或「首版全部为增」）。用户须对理解与方案均表态；仅回 OK 未对复述/方案表态不算过；确认后才分诊/入池承诺/写正式 PRD/计划/排期

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`customer-needs-discovery`、`requirement-discovery-and-prioritization` → 见 §6 闭环。

### 本步动作清单

- 来源分层（用户反馈/客服/数据/销售/竞品/合规）。
- 每条入 `{workroot}/requirement-pool.md`（价值/成本/风险初判 + 状态）。
- **先还原需求**：技能 `skills/customer-needs-discovery/SKILL.md`（先读）——区分想要/需要/方案。
- 单个客户/领导/竞品说法标样本与证据等级，不直接当市场结论。 澄清**按 `rules/core/clarification.md` 执行**。
- 正式访谈用 `interview-guide-template.md`，综合用 `insight-synthesis-template.md`。**未双确认不得**入池承诺/排优先级。
- 未确认推断标「假设」并写验证方式。 **竞品（模式 S）**：口令「竞品分析/学习竞品」或 0→1/战略定位需要时 → 技能 `skills/competitive-intelligence-and-learning/SKILL.md` **模式 S**。
- 落盘 `竞品分析-{主题}-{yyyyMMdd}.md`（模板 `competitor-analysis-template.md`）。
- 产出借/改编/不借表并回绑本产品问题。
- 影响定位/范围须确认。功能差距清单需求 → 转 `benchmark` 步（模式 P），不在本步只交对标矩阵冒充分析。 **来源扇出**（子代理编排 ）：批量洞察/竞品 ≥4 独立来源 → 按来源只读扇出（返回证据表/去重键 ≤30 行）。
- 主 agent 去重入池。
- 单条反馈直做。 引用须可回查（来源+日期），无依据写「待验证」。 能力（可选）：docs-mcp 查资料、browser-mcp 查竞品/后台。
- 未装=按主读与用户输入。 输入含外部文档/竞品/反馈原件 → 先按 `rules/doc-governance.md` 【入站分析】。
- 确认前不改文件。确认采纳后落 `inbound/{ver|topic}/` 或 `_common/`（或 T7 参考）。
- S1/S2/S3 同批进 `inbound/_archive/`。
- 本包写的 PRD/竞品分析正文落工作区，不进资料。 技能：`skills/requirement-discovery-and-prioritization/SKILL.md`（先读再做）。
- 竞品向必加 `competitive-intelligence-and-learning`。

## 6. 技能指向（打开 → 执行 → 回本包）

> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  
> 同时只打开 **1** 个 skill；打开期间 `reads=` 可暂加该 skill 路径，闭环结束后以本 packet 为准。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `customer-needs-discovery` | **必开** | 进入本步即开（质量不降） | `skills/customer-needs-discovery/SKILL.md` | 必做区 → 回本包 |
| `requirement-discovery-and-prioritization` | **必开** | 进入本步即开（质量不降） | `skills/requirement-discovery-and-prioritization/SKILL.md` | 必做区 → 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/prd/_chain.md`。
- 子状态机（进区一次）：`rules/packets/prd/_region-discover.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:prd | step=discover | packet=rules/packets/prd/discover.md | reads=rules/packets/prd/discover.md[+skill] | skills=customer-needs-discovery,requirement-discovery-and-prioritization|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/prd/discover.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
