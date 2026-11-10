# 步骤卡 · prd/prd

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（每步先读并逐条过）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`prd` / `prd`（PRD 撰写）
- **packet**：`rules/packets/prd/prd.md`
- **角色**：`prd-writer`（PRD 撰写）。按模板落盘完整 PRD；要素齐、可测、无歧义；带缺口不落盘；本步只做该角色职责；越界交回或升级。
- **上游**：`prioritize`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`prototype`（进 `prototype` 前的 `when=has_ui_requirement`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：PRD 撰写
- **产出**：{workroot}/{ver}/10-requirements/PRD-{主题}.md（模板 rules/templates/10-planning/prd-template.md）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：每步读 `rules/core/global-rules.md` 并逐条过；本步未读不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_understanding`**：出示【理解复述】（谁/场景/问题/现有替代/代价/目标/范围/非目标/证据/假设）+【推荐方案要点】（主路径/关键rules/异常期望/验收口径/不做）+ 缺口清单；涉及换迭代/相对上版时附**本期差量要点**（增/改/删或「首版全部为增」）。用户须对理解与方案均表态；仅回 OK 未对复述/方案表态不算过；确认后才分诊/入池承诺/写正式 PRD/计划/排期
- **条件判定 `hitl:understanding_needs_confirm`**：输入为模糊/单点需求、含外部文档或原型、存在实质冲突、方案有取舍、或 P1↑/P2/P3/点名写 PRD/计划/收集需求时需确认**理解+方案要点**；已有**当前任务**理解与方案双确认记录/已确认受理单（含方案要点）、或信息完整的缺陷单/答疑且已能复述且无新方案取舍时假；满足→真，否则跳过该门。
- **HITL `confirm_scope`**：范围（MVP）/排除项/粗排期/风险 一行摘要；条件门：仅跨版本/高价值/未确认范围时停
- **条件判定 `hitl:scope_unconfirmed`**：无已确认产品计划且无已批准的单需求范围；满足→真，否则跳过该门。
- **GATE `product-prd` when=prd_structure_required**：运行 `verify/Invoke-Gate.ps1 -Mode prd -Artifact <当前PRD>`（推荐显式路径）；BLOCKED → 不得进评审/定稿/交开发；DRAFT → 可审不可定稿；回执 `.gate/wf-product/prd.json`。light 缺追溯仅警告。P2+/P1↑/拟定稿或交开发时为真
- **条件判定 `gate:prd_structure_required`**：本步为写/改 PRD 且级别为 P2+/P1↑，或用户点名定稿/交开发/拟置 APPROVED，或普通 P1 将交开发；P0 纯文案无结构变更为假；满足→真，否则跳过该闸（步骤不跳过）。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`prd-writing` → 见 §6 闭环。

- **条件技能**：`analytics-and-experimentation`（有指标/埋点/实验） → 命中则同样走 §6 闭环。

### 本步动作清单

- skills_required: prd-writing｜skills_optional: analytics-and-experimentation（有指标/埋点/实验才读） 前置：产品计划已确认，或单需求范围已经 `confirm_scope` 批准。
- 两者都无 → 先补一行范围确认（一次），不直接写全量 PRD。
- 已在需求池/立项书/计划范围内 → 直接写。
- 未定性新输入 → 先走 `change.intake`，不跳过受理。
- **写前先读**：确认的客户需求理解/受理单/需求池/证据。
- 每条 F/R/AC 必须能追溯到来源（访谈/工单/数据/文档/裁决），无来源列 `Q-xx` 待确认，不臆造。
- 未确认的推断标「假设」。
- 理解门先行：`confirm_understanding` 按 先查事实。
- 仍不明一次一问（附候选/推荐）。
- 未确认不升格 出示理解复述+方案要点。
- **未双确认不得**落正式 PRD（可出草稿并标待确认）。
- P2+ 且开发/测试角色可得时，按 内容优先、包按需。
- 未回执不得称已接收 做需求澄清（Three Amigos）：产品讲问题/AC，开发讲可行性/影响，测试讲可测性/oracle。
- 产出澄清记录（问题/示例/AC/待决，可并入 PRD 的变更记录节或评审记录）并回写 PRD。
- 角色不可得则跳过，不阻塞。
- 技能见 §6 `prd-writing`（先读再写）+ §6 `analytics-and-experimentation`（指标/埋点/实验，可选）。
- 定稿自检清单与 `review-and-finalize` 技能同源（评审步技能，本步不强制打开）。
- 要素齐：背景/目标与指标/用户场景/功能清单/流程/状态机/权限矩阵/字段rules/异常边界/非功能/埋点/验收标准/范围排除/依赖风险/里程碑。
- **多需求/版本级**：用 `rules/templates/10-planning/iteration-plan-template.md` 汇总范围、功能覆盖、验收矩阵、执行记录与发布条件。
- PRD 保留单需求明细。
- 验收矩阵先标 `DEV-AC/QA-AC/REL-AC`，不得原样转开发任务。
- 写不出验收标准 = 需求未定义完。
- 禁臆造用户反馈与数据（引用可回查）。
- **级别**：P0/普通 P1 → 轻量模板。
- **P1↑**（权限/资金/隐私/不可逆数据/主数据规则）→ 作者自检按 P2，可用轻量壳但须补权限/rules/异常/AC。
- P2+ → 全量模板。
- **作者侧硬纪律**：完稿必须产出【完稿自检摘要】（见 prd-writing ）。
- `gate_when: prd_structure_required` → 跑 `-Mode prd`（`gate: product-prd`）。
- BLOCKED → 不得进评审/定稿。
- DRAFT → 可审不可定稿。
- 进定稿/交开发前 P2+/P1↑/任何拟 APPROVED 必须再跑至非 BLOCKED。
- P0 纯文案且无结构门要求时可跳过 gate。
- 普通 P1 进交开发前仍须非 BLOCKED。
- **证据侦察分片**（子代理编排 ）：大 PRD（≥3 来源文档）→ 只读侦察 AC/状态机/权限/NFR/异常边界。
- PRD 正文单写手分节推进，禁并行写。
- 完稿按评审清单自检，带缺口禁落盘。
- 同路径已有 PRD → 先读并增量更新，禁静默覆盖。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → 读必做，并读现场处置/判定/反合理化（技能有这些节时）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `prd-writing` | **必开** | 进入本步即开（质量不降） | `skills/prd-writing/SKILL.md` | 只读 L11-L135（硬门槛+方法+反合理化）→ 回本包 |
| `analytics-and-experimentation` | 条件开 | 有指标/埋点/实验 | `skills/analytics-and-experimentation/SKILL.md` | 只读 L13-L78（硬门槛+方法+反合理化）→ 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/10-planning/prd-template.md`；只读本步用到的节，禁止整文件通读。
- **参考模板（命中再开，不默认读）**：`rules/templates/10-planning/iteration-plan-template.md`。
- 验证命令：`verify/Invoke-Gate.ps1`（完成须 `-Claim` → `CLAIM: ALLOWED`）。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步完成 Claim 门：须 `CLAIM: ALLOWED` 后才可写完成态。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:prd | step=prd | agent=prd-writer | packet=rules/packets/prd/prd.md | global=ok | skills=prd-writing,analytics-and-experimentation|done|na | claim=ALLOWED|DENIED|na | next=…
```
