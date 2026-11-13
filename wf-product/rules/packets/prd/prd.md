# 步骤卡 · prd/prd

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`prd` / `prd`（PRD 撰写）
- **packet**：`rules/packets/prd/prd.md`
- **角色**：`prd-writer`（PRD 撰写）。按模板落盘完整 PRD；要素齐、可测、无歧义；带缺口不落盘；本步只做该角色职责；越界交回或升级。
- **上游**：`prioritize`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`prototype`（进 `prototype` 前的 `when=has_ui_requirement`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。

## 2. 本步目标

- **目标**：PRD 撰写
- **产出**：{workroot}/{ver}/10-requirements/PRD-{主题}.md（模板 rules/templates/10-planning/prd-template.md）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
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

- 本步任务：写可评审 PRD。
- 前置：已确认计划或 `confirm_scope`。
- 否则先一行范围确认。
- 未定性新输入 → 先 `change` intake。
- 硬门槛：理解门双确认后才落正式 PRD。
- F/R/AC 可追溯。
- 写不出 AC=未定义完。
- 完稿须【完稿自检摘要】+ `-Mode prd` 非 BLOCKED（P0 纯文案可跳结构门）。
- 级别：P0/普通 P1 轻量。
- P1↑/P2+ 按门槛补齐。
- 方法见 §6 `prd-writing`（可选 analytics）。
- 模板见 §7。
- 澄清/交接索引 先查事实。
- 仍不明一次一问（附候选/推荐）。
- 未确认不升格 `rules/collaboration/handoff.md`。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。
> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `prd-writing` | **必开** | 进入本步即开（质量不降） | `skills/prd-writing/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `analytics-and-experimentation` | 条件开 | 有指标/埋点/实验 | `skills/analytics-and-experimentation/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/10-planning/prd-template.md`；只读本步用到的节，禁止整文件通读。
- 验证命令：`verify/Invoke-Gate.ps1`（完成须 `-Claim` → `CLAIM: ALLOWED`）。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步 Claim 门受 `gate_when: prd_structure_required` 约束：门执行时须 `CLAIM: ALLOWED` 才可写完成态；门被跳过 → 不产门回执，`claim=na` 并写 `when_eval=<假理由>`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:prd | step=prd | agent=prd-writer | packet=rules/packets/prd/prd.md | global=ok | skills=prd-writing|done|na | claim=ALLOWED|DENIED|na | next=…
```
