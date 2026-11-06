# 步骤包 · defect/review

> **状态 = 本 step（独立完整）**。全局硬约束见 §3（每步遵守）；本步门/编排/完成见本文；**方法在 §6 skill**（打开→执行→回来）。  
> 与开局卡/他步条文重复 OK；不要跳转拼流程；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-product
- **workflow**：`defect`
- **step**：`review`（重审（条件））
- **packet**：`rules/packets/defect/review.md`
- **角色**：`reviewer-agent`（产品落地文档独立评审（PRD/计划/设计/交付计划/实质变更重审））。用户选 B（AI）时按量规独立复核；只报缺口；结论落评审记录；不替写正文。选 A 时不替代用户放行；本步只做该角色职责；越界交回或升级。
- **上游**：`apply`（取其产出为本步输入；该步被 `when` 跳过时按缺口停/补齐）
- **后续**：`writeback`（进 `writeback` 前的 `when=remark_writeback`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:substantive_change`**：实质变更需重审；满足→真，否则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：进 wf 时读 `_chain` 一次；**中段勿重读**。
- **子状态机**：进「处置回写」区时读 `_region-act` 一次；**中段勿重读**。

## 2. 本步目标

- **目标**：重审（条件）
- **产出**：评审记录（{workroot}/{ver}/10-requirements/评审-{主题}-{yyyyMMdd}.md）

## 3. 本步硬约束

### 全局硬约束（本包已带齐 · 每步都遵守）

- 1. 先判后动；未确认禁写/禁结论；批量不豁免。
- 2. 先查事实；仍不明一次一问（附候选/推荐）。
- 3. 核前提/来源/变量/成本；不迎合；用户有误直接指出。
- 4. 劣解先说依据+主推；用户坚持记 `deviation=`。
- 5. 先权衡；失败 2 次换路径。
- 6. 改前说文件；最小改动；超范围先停。
- 7. 完成只认 `Invoke-Gate.ps1 -Claim -Mode <…>` → `CLAIM: ALLOWED`；原型实走+覆盖矩阵；UAT 未过不发布。
- 8. 收尾六点；只读 2～3 行；主动发现 ≤3。
- 9. 只写现行；删除即移除；不写历史/旧方案。
- 10. 读链：开局卡 → `_chain` → 当前包 → §6 skill → 模板 ≤1；同时只 1 包。
- 11. §6 必开 skill 打开→执行→回包；禁粘贴代替。
- 12. 切步/过门心跳带 `packet=`/`role=`/`task=`；长任务先报进展。
- 13. 用户当轮指令优先；与硬门冲突先说明再二选一。
- 14. 证据先于结论；禁刷绿；密钥零入库。
- **效力**：以上为执行摘要（全文见开局卡 §1）；开局已读则中段不重开全文，**每步仍须逐条遵守**；与开局卡重复不影响。

### 本步操作面（本链本步独立完整）

- **读这些就能干完本步**：本文（全局摘要 + §4 门 + §5 编排）+ §6 表内 skill（一次 1 个闭环）+（若 §7 列出）至多 1 模板。
- **不靠跳转拼流程**：本步所需规则已写在本文；他步/他链可有相同条文，互不依赖。
- **完成声称**：有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **上下文锚**：`packet=`/`reads=` 必须含本 packet；切步前心跳刷新。

### 本步禁止

- 禁止用 read-index / 他步 packet /「详见别处 rules」拼本步流程。
- 禁止跳过 §6 必开技能，或用摘要代替实读。
- 禁止未过 §4 门或未出 §8 信号就宣称完成、推进或写「已通过」。

## 4. 本步门

- **HITL `select_review_mode`**：**STOP 二选一**：A 自行评审通过（HUMAN_APPROVED）｜B AI 独立评审（异人量规+评审记录）。适用 PRD/产品计划/设计交接等（`skills/artifact-review`）；同产物只问一次；点名「AI 评审」=B、「我审/自行通过」=A；未选不得宣称通过/定稿/交开发
- **条件判定 `hitl:landing_doc_review_needed`**：落地文档（PRD P2+、产品计划首版或实质变更、设计评审/设计交接、交付计划、实质变更重审、或用户点名评审）待选评审方式且本会话尚未选定；P0/普通 P1 light 且用户未点名时可假；**P1↑ 默认提示 A / SELF_CHECKED，不强制独立审；P2+ 必问 A/B**；满足→真，否则跳过该门。
- **HITL `confirm_prd`**：评审结论为「通过（可定稿）」且用户点名定稿/进入排期时出示；**出示前**须有【完稿自检摘要】且 `-Mode prd` 非 BLOCKED；定稿前不排期；仅评审不弹门
- **条件判定 `hitl:finalize_requested`**：评审通过且用户点名定稿/进入排期（仅评审不触发）；满足→真，否则跳过该门。
- **GATE `product-review` when=ai_review_chosen**：仅选 B（AI）时运行 `-Mode review`；评审人≠作者；READY 后取 `gate_id`；选 A 不跑本门，须 HUMAN_APPROVED + `approved_by` + 自检摘要 + 复跑 `-Mode prd` 至 READY
- **条件判定 `gate:ai_review_chosen`**：用户已选 B（AI 独立评审）；满足→真，否则跳过该闸（步骤不跳过）。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`artifact-review`、`review-and-finalize` → 见 §6 闭环。

### 本步动作清单

- **单一出处**：通用评审/定稿规则以 本 workflow review 为准。
- 本步只保留产品缺陷平台差异。 条件步：实质变更/方案影响 AC/范围/权限/数据rules/NFR/版本目标才走。
- 纯文字澄清跳过。 **先 STOP【评审方式】**（`skills/artifact-review`）：A 自行通过｜B AI 独立审。
- 未选不得恢复定稿。 **选 A**：【完稿自检摘要】+ 产品视角要点 → HUMAN_APPROVED → `confirm_prd`。
- 不跑 `-Mode review`。
- 须 `-Mode prd` 非 BLOCKED（涉及 PRD 实质变更时）。 **选 B**：先写评审记录再 `-Mode review`。
- 产品视角（是否解决原问题、AC/范围/风险/合规）。
- 技术实现不替开发评。 通过后回写平台并恢复 PRD `APPROVED`。
- 需修回 apply（≤1）。
- 未重审不得标已定稿。

## 6. 技能指向（打开 → 执行 → 回本包）

> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `artifact-review` | **必开** | 进入本步即开（质量不降） | `skills/artifact-review/SKILL.md` | 必做区 → 回本包 |
| `review-and-finalize` | **必开** | 进入本步即开（质量不降） | `skills/review-and-finalize/SKILL.md` | 必做区 → 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 打开/填写

- **本步完整面**：本步骤包（§3 全局摘要 + §4 门 + §5 规则卡/编排）+ §6 必开/条件开 skill（一次 1 个）+ 本步输入。
- **无强制模板**：§5 规则卡已给出输出形状；直接落 §2 产出。
- 验证命令：`verify/Invoke-Gate.ps1`（声称完成加 `-Claim`）。
- 本步不再读 read-index / 他步 packet / 大手册；模板与 skill 只读指定节。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:defect | step=review | agent=reviewer-agent | packet=rules/packets/defect/review.md | reads=rules/packets/defect/review.md[+skill] | skills=artifact-review,review-and-finalize|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/defect/review.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
