# 步骤卡 · prd/discover

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`prd` / `discover`（需求洞察与需求池）
- **packet**：`rules/packets/prd/discover.md`
- **角色**：`pm-analyst`（需求洞察与优先级（含受理转入的新需求））。来源分层收集需求 → 入需求池 → 分级排序 → 立项输出范围与风险；不臆造；本步只做该角色职责；越界交回或升级。
- **上游**：无（链首）
- **后续**：`benchmark`（进 `benchmark` 前的 `when=benchmark_or_mode_p`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：需求洞察与需求池
- **产出**：需求池/洞察/竞品分析（{workroot}/requirement-pool.md 或 {workroot}/{ver}/10-requirements/洞察|竞品分析-*.md）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_understanding`**：出示【理解复述】（谁/场景/问题/现有替代/代价/目标/范围/非目标/证据/假设）+【推荐方案要点】（主路径/关键rules/异常期望/验收口径/不做）+ 缺口清单；涉及换迭代/相对上版时附**本期差量要点**（增/改/删或「首版全部为增」）。用户须对理解与方案均表态；仅回 OK 未对复述/方案表态不算过；确认后才分诊/入池承诺/写正式 PRD/计划/排期
- **条件判定 `hitl:understanding_needs_confirm`**：输入为模糊/单点需求、含外部文档或原型、存在实质冲突、方案有取舍、或 P1↑/P2/P3/点名写 PRD/计划/收集需求时需确认**理解+方案要点**；已有**当前任务**理解与方案双确认记录/已确认受理单（含方案要点）、或信息完整的缺陷单/答疑且已能复述且无新方案取舍时假；满足→真，否则跳过该门。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`customer-needs-discovery`、`requirement-discovery-and-prioritization` → 见 §6 闭环。

### 本步动作清单

- 来源分层（用户反馈/客服/数据/销售/竞品/合规）。
- 每条入 `{workroot}/requirement-pool.md`（价值/成本/风险初判 + 状态）。
- **先还原需求**：技能 §6 `customer-needs-discovery`（先读）——区分想要/需要/方案。
- 单个客户/领导/竞品说法标样本与证据等级，不直接当市场结论。
- 按 先查事实。
- 仍不明一次一问（附候选/推荐）。
- 未确认不升格。
- 正式访谈用 `interview-guide-template.md`，综合用 `insight-synthesis-template.md`。
- **未双确认不得**入池承诺/排优先级。
- 未确认推断标「假设」并写验证方式。
- **竞品（模式 S）**：口令「竞品分析/学习竞品」或 0→1/战略定位需要时 → 按 `competitive-intelligence-and-learning` 技能 **模式 S**。
- 落盘 `竞品分析-{主题}-{yyyyMMdd}.md`（模板 `competitor-analysis-template.md`）。
- 产出借/改编/不借表并回绑本产品问题。
- 影响定位/范围须确认。
- 功能差距清单需求 → 转 `benchmark` 步（模式 P），不在本步只交对标矩阵冒充分析。
- **来源扇出**（子代理编排 ）：批量洞察/竞品 ≥4 独立来源 → 按来源只读扇出（返回证据表/去重键 ≤30 行）。
- 主 agent 去重入池。
- 单条反馈直做。
- 引用须可回查（来源+日期），无依据写「待验证」。
- 能力（可选）：docs-mcp 查资料、browser-mcp 查竞品/后台。
- 未装=按主读与用户输入。
- 输入含外部文档/竞品/反馈原件 → 先按 文档治理规则（工作根/原件根/索引/关版整夹） 【入站分析】。
- 确认前不改文件。
- 确认采纳后落 `inbound/{ver|topic}/` 或 `_common/`（或 T7 参考）。
- S1/S2/S3 同批进 `inbound/_archive/`。
- 本包写的 PRD/竞品分析正文落工作区，不进资料。
- 技能见 §6 `requirement-discovery-and-prioritization`（先读再做）。
- 竞品向另按 `competitive-intelligence-and-learning` 技能。

### 本步规则卡：文档治理

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认后将迭代绑定文档迁入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`；主档关闭时快照、主档不移动；「并行不关」只落新资料、不归档现行主档。
- 清理只删已知临时/缓存/未引用失败产物；不确定移 `_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。
> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `customer-needs-discovery` | **必开** | 进入本步即开（质量不降） | `skills/customer-needs-discovery/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `requirement-discovery-and-prioritization` | **必开** | 进入本步即开（质量不降） | `skills/requirement-discovery-and-prioritization/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **模板（产出该类文件时按此填；门按结构判分的产物须对齐）**：`rules/templates/10-planning/requirement-pool-template.md`；`rules/templates/10-planning/interview-guide-template.md`；`rules/templates/10-planning/insight-synthesis-template.md`；`rules/templates/10-planning/competitor-analysis-template.md`。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:prd | step=discover | agent=pm-analyst | packet=rules/packets/prd/discover.md | global=ok | skills=customer-needs-discovery,requirement-discovery-and-prioritization|done|na | claim=ALLOWED|DENIED|na | next=…
```
