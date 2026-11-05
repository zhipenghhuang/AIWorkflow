# 步骤包 · intake/scan

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-development
- **workflow**：`intake`
- **step**：`scan`（扫描新输入）
- **packet**：`rules/packets/intake/scan.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/intake/_chain.md`（进 workflow 一次）。

## 2. 本步目标

- **目标**：扫描新输入
- **产出**：新输入候选清单

## 3. 本步硬约束

### 开局硬约束（本步可执行摘要）

- 1. **先意图、再动作**（`confirm_task_intent`）：新开先【需求与意图理解】再确认；未确认禁改代码/外发/下完成结论。
- 2. **短读跟随 + 一手源**：`activeContext` + 进行中（`rule_card`/`packet=`/`region=`）+ 偏好/洞见/坑 ≤3。
- 3. **状态机读链（硬）**：见本包「本步读链与防丢失」。父流程可拆子机；同时只激活**一个**步骤包。
- 4. **技能闭环（质量不降）**：步骤包 §6 标**必开**的 skill 必须打开→按必做执行→**回到步骤包**；禁止把 skill 正文嵌进步骤包替代实读；禁止跳过必开 skill。
- 5. **完成分层**：`verify/Invoke-Gate.ps1 -Claim` → 只认 `CLAIM: ALLOWED`。无 ALLOWED 禁止写「已通过」。
- 6. **前端硬门**：有 UI → 当前步骤包内前端硬门；无 UI 标 `na`。
- 7. **证据先于结论；禁刷绿**；密钥零入库；最小改动；失败同方案 2 次换路径。
- 8. **切步/出子机 → 心跳一行**，必须带 `packet=`（有子机带 `region=`）。

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

- **本步必开技能（质量不降）**：`change-intake` → 见 §6 闭环。

### 本步动作清单

- 技能：`skills/change-intake/SKILL.md`（先读再做）。 输入是交接包（含 `00-交接说明.md` + `01-交接清单.md`）→ 先走 `workflows/handoff.yaml` receive 核对+回执。
- 未签收不进入吸收。 扫描：`inbound/` 未登记/变化文件、`inbound/INDEX.md` 断链、`{workroot}/INDEX.md`、`git status`。
- 不再扫 `_收件箱`。 对照 `{workroot}/INDEX.md` / `需求台账/待决项/开发计划，列出“未登记/未关联”的候选。
- 不读全量历史，不直接改基线。 多个候选 → 列清单让用户选。
- 无新输入 → 报告“无新增”，不空转。 先按 `rules/doc-governance.md` ～（T1～T9 + 索引/复制/A0～A2）。
- **确认前不改文件**。确认后：主副本必留原件根 `inbound/`并索引 → 按需复制 → 按需吸收。
- 未点名可仅索引。放入≠分发他包。 **文档抽取分片**（子代理编排 ）：≥3 份新文档 → 只读扇出（每份返回 DOC/CR/OPEN/DEC 候选＋引用位置＋覆盖关系 ≤30 行）。
- 登记/分类/影响集中。
- 单份直做。

## 6. 技能指向（打开 → 执行 → 回本包）

> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  
> 同时只打开 **1** 个 skill；打开期间 `reads=` 可暂加该 skill 路径，闭环结束后以本 packet 为准。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `change-intake` | **必开** | 进入本步即开（质量不降） | `skills/change-intake/SKILL.md` | 必做区 → 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/intake/_chain.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:intake | step=scan | packet=rules/packets/intake/scan.md | reads=rules/packets/intake/scan.md[+skill] | skills=change-intake|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/intake/scan.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
