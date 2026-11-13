# 步骤卡 · change/design

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`change` / `design`（方案与设计）
- **packet**：`rules/packets/change/design.md`
- **角色**：`implementer`（常规实现）。需求/方案对齐 → 最小改动实现 → 自测/门禁 → 提测文档 → 提交；架构级先方案批准；本步只做该角色职责；越界交回或升级。
- **上游**：`requirements`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`review-docs`（进 `review-docs` 前的 `when=do_landing_doc_review`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:new_feature_or_architecture_or_breaking_change_or_high_risk_or_requested`**：新功能/架构/破坏性/高风险，或点名做 design；满足→真，否则跳过本步（不打开本包）。

## 2. 本步目标

- **目标**：方案与设计
- **产出**：方案/ADR（{workroot}/20-design/）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_spec`**：出示范围/接口/兼容与回滚/验收；批准后才实施（可在选模式 + 可选 AI 审之后）
- **条件判定 `hitl:design_needs_spec_approval`**：L1 有新方案/ADR/前端设计且未进 review-docs；满足→真，否则跳过该门。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`solution-design`、`engineering-quality` → 见 §6 闭环。

- **条件技能**：`cross-layer-consistency`（命中权限/状态/数据基数/多表面）、`threat-modeling`（命中鉴权/权限/敏感数据/上传/回调/公共 API/资金/AI）、`performance-and-capacity`（命中列表/批量/导出/循环查库/无界集合/统计/首屏/高并发） → 命中则同样走 §6 闭环。

### 本步动作清单

- L0 可跳过。
- L1 本步 confirm_spec。
- L2+ 落盘后进 review-docs。
- 子域技能（api/db/frontend/threat/…）按变更面读对应技能当前节。
- 前端补设计说明模板。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。
> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `solution-design` | **必开** | 进入本步即开（质量不降） | `skills/solution-design/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `engineering-quality` | **必开** | 进入本步即开（质量不降） | `skills/engineering-quality/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `cross-layer-consistency` | 条件开 | 命中权限/状态/数据基数/多表面 | `skills/cross-layer-consistency/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `threat-modeling` | 条件开 | 命中鉴权/权限/敏感数据/上传/回调/公共 API/资金/AI | `skills/threat-modeling/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `performance-and-capacity` | 条件开 | 命中列表/批量/导出/循环查库/无界集合/统计/首屏/高并发 | `skills/performance-and-capacity/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（主）**：`rules/templates/20-design/solution-template.md`；只读本步用到的节，禁止整文件通读。
- **配套模板（按产出需要读；门按结构判分的产物须对齐）**：`rules/templates/20-design/frontend-design-spec-template.md`；`rules/templates/20-design/frontend-prototype-parity-template.md`；`rules/templates/20-design/adr-template.md`。
- **产出前自检**：对照模板必填节逐项填写；缺节、空节、未替换 `{…}` = 不合格（不得标完成）。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- §2 产出已按模板必填节落地；无空节、无未替换占位符。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:change | step=design | agent=implementer | packet=rules/packets/change/design.md | global=ok | skills=solution-design,engineering-quality|done|na | claim=ALLOWED|DENIED|na | next=…
```
