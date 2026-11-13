# 步骤卡 · prd/benchmark

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`prd` / `benchmark`（竞品对标与差距候选项）
- **packet**：`rules/packets/prd/benchmark.md`
- **角色**：`pm-analyst`（需求洞察与优先级（含受理转入的新需求））。来源分层收集需求 → 入需求池 → 分级排序 → 立项输出范围与风险；不臆造；本步只做该角色职责；越界交回或升级。
- **上游**：`discover`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`prioritize`（进 `prioritize` 前的 `when=new_requirement_or_scope_change`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:benchmark_or_mode_p`**：口令为竞品对标/功能对标/对标分析/功能差距，或 discover 已分诊为模式 P；满足→真，否则跳过本步（不打开本包）。

## 2. 本步目标

- **目标**：竞品对标与差距候选项
- **产出**：竞品对标矩阵 + 需求池候选项（{workroot}/{ver}/10-requirements/竞品对标-*.md + {workroot}/requirement-pool.md）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_scope`**：范围（MVP）/排除项/粗排期/风险 一行摘要；条件门：仅跨版本/高价值/未确认范围时停
- **条件判定 `hitl:scope_decision_required`**：跨版本/高价值/点名立项，需单需求范围确认；满足→真，否则跳过该门。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`competitive-intelligence-and-learning`、`requirement-discovery-and-prioritization` → 见 §6 闭环。

### 本步动作清单

- 入口=「竞品对标/功能对标/对标分析/功能差距」或 discover 分诊为模式 P。
- 技能见 §6 `competitive-intelligence-and-learning` **模式 P**（先读）+ `requirement-discovery-and-prioritization`（入池字段）。
- 落盘模板 `competitive-benchmark-template.md`。
- 对标矩阵含本产品列与 ≥2 竞品。
- 差距项入需求池**候选项**（来源=`竞品对标`+链接+日期）。
- 可无完整客户访谈，但**禁止**自动已立项/已排期。
- ≥4 竞品/来源按子代理编排只读扇出。
- 判断与入池去重集中。
- 用户要「按对标进本期」→ `confirm_scope`（Top N + 成本粗估）。
- 仅沉淀候选项不承诺版本 → 可跳过门。
- 发现定位级问题 → 建议补做模式 S（`discover`/竞品分析），不在本步终裁差异化。
- 能力：browser-mcp 可选。
- 未装=用户提供链接/截图。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。
> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `competitive-intelligence-and-learning` | **必开** | 进入本步即开（质量不降） | `skills/competitive-intelligence-and-learning/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `requirement-discovery-and-prioritization` | **必开** | 进入本步即开（质量不降） | `skills/requirement-discovery-and-prioritization/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（主）**：`rules/templates/10-planning/competitive-benchmark-template.md`；只读本步用到的节，禁止整文件通读。
- **产出前自检**：对照模板必填节逐项填写；缺节、空节、未替换 `{…}` = 不合格（不得标完成）。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- §2 产出已按模板必填节落地；无空节、无未替换占位符。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:prd | step=benchmark | agent=pm-analyst | packet=rules/packets/prd/benchmark.md | global=ok | skills=competitive-intelligence-and-learning,requirement-discovery-and-prioritization|done|na | claim=ALLOWED|DENIED|na | next=…
```
