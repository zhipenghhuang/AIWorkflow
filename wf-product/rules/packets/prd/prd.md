# 步骤包 · prd/prd

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-product
- **workflow**：`prd`
- **step**：`prd`（PRD 撰写）
- **packet**：`rules/packets/prd/prd.md`
- **角色**：`prd-writer`（PRD 撰写）。按模板落盘完整 PRD；要素齐、可测、无歧义；带缺口不落盘；本步只做该角色职责；越界交回或升级。
- **上游**：`prioritize`（取其产出为本步输入；该步被 `when` 跳过时按缺口停/补齐）
- **后续**：`prototype`（进 `prototype` 前的 `when=has_ui_requirement`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/prd/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/prd/_region-write.md`（撰写交接；进本区一次）。

## 2. 本步目标

- **目标**：PRD 撰写
- **产出**：{workroot}/{ver}/10-requirements/PRD-{主题}.md（模板 rules/templates/10-planning/prd-template.md）

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

- **HITL `confirm_understanding`**：出示【理解复述】（谁/场景/问题/现有替代/代价/目标/范围/非目标/证据/假设）+【推荐方案要点】（主路径/关键rules/异常期望/验收口径/不做）+ 缺口清单；涉及换迭代/相对上版时附**本期差量要点**（增/改/删或「首版全部为增」）。用户须对理解与方案均表态；仅回 OK 未对复述/方案表态不算过；确认后才分诊/入池承诺/写正式 PRD/计划/排期
- **HITL `confirm_scope`**：范围（MVP）/排除项/粗排期/风险 一行摘要；条件门：仅跨版本/高价值/未确认范围时停
- **GATE `product-prd` when=prd_structure_required**：运行 `verify/Invoke-Gate.ps1 -Mode prd -Artifact <当前PRD>`（推荐显式路径）；BLOCKED → 不得进评审/定稿/交开发；DRAFT → 可审不可定稿；回执 `.gate/wf-product/prd.json`。light 缺追溯仅警告。P2+/P1↑/拟定稿或交开发时为真
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`prd-writing`、`analytics-and-experimentation` → 见 §6 闭环。

### 本步动作清单

- skills_required: prd-writing｜skills_optional: analytics-and-experimentation（有指标/埋点/实验才读） 前置：产品计划已确认，或单需求范围已经 `confirm_scope` 批准。
- 两者都无 → 先补一行范围确认（一次），不直接写全量 PRD。 已在需求池/立项书/计划范围内 → 直接写。
- 未定性新输入 → 先走 `workflows/change.yaml` intake，不跳过受理。 **写前先读**：确认的客户需求理解/受理单/需求池/证据。
- 每条 F/R/AC 必须能追溯到来源（访谈/工单/数据/文档/裁决），无来源列 `Q-xx` 待确认，不臆造。
- 未确认的推断标「假设」。 理解门先行：`confirm_understanding` 按 `rules/core/clarification.md` 出示理解复述+方案要点。
- **未双确认不得**落正式 PRD（可出草稿并标待确认）。 P2+ 且开发/测试角色可得时，按 `rules/collaboration/handoff.md` 做需求澄清（Three Amigos）：产品讲问题/AC，开发讲可行性/影响，测试讲可测性/oracle。
- 产出澄清记录（问题/示例/AC/待决，可并入 PRD 的变更记录节或评审记录）并回写 PRD。
- 角色不可得则跳过，不阻塞。 技能：`skills/prd-writing/SKILL.md`（先读再写）+ `skills/analytics-and-experimentation/SKILL.md`（指标/埋点/实验，可选）。
- 自检清单与 `skills/review-and-finalize/SKILL.md` 同源。 要素齐：背景/目标与指标/用户场景/功能清单/流程/状态机/权限矩阵/字段rules/异常边界/非功能/埋点/验收标准/范围排除/依赖风险/里程碑。
- **多需求/版本级**：用 `rules/templates/10-planning/iteration-plan-template.md` 汇总范围、功能覆盖、验收矩阵、执行记录与发布条件。
- PRD 保留单需求明细。验收矩阵先标 `DEV-AC/QA-AC/REL-AC`，不得原样转开发任务。 写不出验收标准 = 需求未定义完。
- 禁臆造用户反馈与数据（引用可回查）。 **级别**：P0/普通 P1 → 轻量模板。
- **P1↑**（权限/资金/隐私/不可逆数据/主数据规则）→ 作者自检按 P2，可用轻量壳但须补权限/rules/异常/AC。
- P2+ → 全量模板。 **作者侧硬纪律**：完稿必须产出【完稿自检摘要】（见 prd-writing ）。
- `gate_when: prd_structure_required` → 跑 `-Mode prd`（`gate: product-prd`）。BLOCKED → 不得进评审/定稿。
- DRAFT → 可审不可定稿。
- 进定稿/交开发前 P2+/P1↑/任何拟 APPROVED 必须再跑至非 BLOCKED。 P0 纯文案且无结构门要求时可跳过 gate。
- 普通 P1 进交开发前仍须非 BLOCKED。 **证据侦察分片**（子代理编排 ）：大 PRD（≥3 来源文档）→ 只读侦察 AC/状态机/权限/NFR/异常边界。
- PRD 正文单写手分节推进，禁并行写。 完稿按评审清单自检，带缺口禁落盘。
- 同路径已有 PRD → 先读并增量更新，禁静默覆盖。

## 6. 技能指向（打开 → 执行 → 回本包）

> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `prd-writing` | **必开** | 进入本步即开（质量不降） | `skills/prd-writing/SKILL.md` | 必做区 → 回本包 |
| `analytics-and-experimentation` | **必开** | 进入本步即开（质量不降） | `skills/analytics-and-experimentation/SKILL.md` | 必做区 → 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/prd/_chain.md`。
- 子状态机（进区一次）：`rules/packets/prd/_region-write.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 验证：`verify/Invoke-Gate.ps1`（完成声称加 `-Claim`）。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:prd | step=prd | agent=prd-writer | packet=rules/packets/prd/prd.md | reads=rules/packets/prd/prd.md[+skill] | skills=prd-writing,analytics-and-experimentation|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/prd/prd.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
