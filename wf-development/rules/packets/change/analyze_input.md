# 步骤卡 · change/analyze_input

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`change` / `analyze_input`（产品资料解析与理解确认）
- **packet**：`rules/packets/change/analyze_input.md`
- **角色**：`implementer`（常规实现）。需求/方案对齐 → 最小改动实现 → 自测/门禁 → 提测文档 → 提交；架构级先方案批准；本步只做该角色职责；越界交回或升级。
- **上游**：`clarify`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`requirements`（进 `requirements` 前的 `when=new_feature_or_scope_change_or_requested`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:has_product_docs_or_prototypes`**：输入含 PRD/迭代方案/需求/原型/截图/接口或技术文档；满足→真，否则跳过本步（不打开本包）。

## 2. 本步目标

- **目标**：产品资料解析与理解确认
- **产出**：需求理解包（{workroot}/10-requirements/理解-{主题}-{yyyyMMdd}.md；§0 Brief+Delta 必填）+ 用户版业务变化说明（L1+ 用户可见变化必出）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_understanding`**：**主屏**：§0【业务与变更简报】+【本期差量表】（增/改/删）+ 待确认单摘要（冲突·GAP·开发择优/置信度）；理解摘要/完整理解包按链选择。无 §0/差量表不得过门（L0 迷你 Delta 除外）。确认后才进下一门/实施；是否写需求基线/设计由链决定
- **条件判定 `hitl:understanding_needs_confirm`**：外部文档/原型、≥2 实质歧义、L2+，或点名方案/排期/估算；满足→真，否则跳过该门。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`product-doc-analysis`、`requirements-and-spec` → 见 §6 闭环。

### 本步动作清单

- 只读输入。
- 多源合看（方案/原型/接口/代码），冲突不静默选边。
- Brief+差量表必填。
- DEV-AC 进开发，QA/REL-AC 转交接。
- confirm_understanding 主屏=理解包 §0（Brief+差量表）+(P/D/S) 用户版+待确认摘要。
- 未确认不进基线/设计/实施。
- 细节只认 §6 `product-doc-analysis` 整卡方法（含用户版说明、P/D/S）。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。
> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `product-doc-analysis` | **必开** | 进入本步即开（质量不降） | `skills/product-doc-analysis/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `requirements-and-spec` | **必开** | 进入本步即开（质量不降） | `skills/requirements-and-spec/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **无强制模板**：§5 编排已给出动作/顺序；直接落 §2 产出。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:change | step=analyze_input | agent=implementer | packet=rules/packets/change/analyze_input.md | global=ok | skills=product-doc-analysis,requirements-and-spec|done|na | claim=ALLOWED|DENIED|na | next=…
```
