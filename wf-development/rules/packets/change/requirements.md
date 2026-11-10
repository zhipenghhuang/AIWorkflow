# 步骤卡 · change/requirements

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（每步先读并逐条过）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`change` / `requirements`（需求基线）
- **packet**：`rules/packets/change/requirements.md`
- **角色**：`implementer`（常规实现）。需求/方案对齐 → 最小改动实现 → 自测/门禁 → 提测文档 → 提交；架构级先方案批准；本步只做该角色职责；越界交回或升级。
- **上游**：`analyze_input`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`design`（进 `design` 前的 `when=new_feature_or_architecture_or_breaking_change_or_high_risk_or_requested`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:new_feature_or_scope_change_or_requested`**：新功能/范围变化，或点名做 requirements；满足→真，否则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：需求基线
- **产出**：需求基线（{workroot}/10-requirements/）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：每步读 `rules/core/global-rules.md` 并逐条过；本步未读不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_requirements`**：出示范围/AC/NFR/非目标/未决；未签收不进设计/排期
- **条件判定 `hitl:requirements_need_confirm`**：需求基线实质变且未确认；满足→真，否则跳过该门。
- **推进**：本步完成后沿父链进入下一未跳过步；口令为单步（只出方案/只出轻量方案/只评审/代码评审/方案评审/只提测/只出清单）或动作清单写明停止/跳转时，以口令/清单为准，即停并输出收尾骨架。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`requirements-and-spec` → 见 §6 闭环。

- **条件技能**：`cross-layer-consistency`（命中权限/状态/数据基数/多表面） → 命中则同样走 §6 闭环。

### 本步动作清单

- 以理解包为输入、引用不重写。
- 基线每条 AC 带原文来源（文件+章节/画板），供实施/验证回指原文。
- 只收 DEV-AC。
- GAP/冲突必须继承。
- 未签收不得进设计/排期。
- L2+ 跳过 design 时基线仍须经 review-docs。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → 读必做，并读现场处置/判定/反合理化（技能有这些节时）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `requirements-and-spec` | **必开** | 进入本步即开（质量不降） | `skills/requirements-and-spec/SKILL.md` | 只读 L10-L83（硬门槛+方法+反合理化）→ 回本包 |
| `cross-layer-consistency` | 条件开 | 命中权限/状态/数据基数/多表面 | `skills/cross-layer-consistency/SKILL.md` | 只读 L12-L127（硬门槛+方法+反合理化）→ 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/10-planning/requirement-baseline-template.md`；只读本步用到的节，禁止整文件通读。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:change | step=requirements | agent=implementer | packet=rules/packets/change/requirements.md | global=ok | skills=requirements-and-spec,cross-layer-consistency|done|na | claim=ALLOWED|DENIED|na | next=…
```
