# 步骤卡 · change/clarify

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`change` / `clarify`（对齐与澄清）
- **packet**：`rules/packets/change/clarify.md`
- **角色**：`implementer`（常规实现）。需求/方案对齐 → 最小改动实现 → 自测/门禁 → 提测文档 → 提交；架构级先方案批准；本步只做该角色职责；越界交回或升级。
- **上游**：无（链首）
- **后续**：`analyze_input`（进 `analyze_input` 前的 `when=has_product_docs_or_prototypes`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。

## 2. 本步目标

- **目标**：对齐与澄清
- **产出**：需求理解包（有外部输入时）+ L1 开发卡（验收/SC）/ L0 轻量回执

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_iteration_close`**：出示当前迭代标识、未完成项、拟归档摘要、下一迭代标识；确认「结束当前并进入下一」后才按 文档治理规则（工作根/原件根/索引/关版整夹） 关账；选「并行不关」则只落新资料不归档现行绑定主档。**关闭=停止新范围/冻结版本线，不停止测试**：测试与缺陷修复可继续（走 patch），归档待测试完成；测试未完又要开新迭代，优先「并行不关」
- **条件判定 `hitl:iteration_close_needed`**：探测到下一期/换主题/升级且是否关本期不明；满足→真，否则跳过该门。
- **HITL `confirm_docs_migration`**：出示分类/覆盖对照/拟归档或清理清单与目标；确认后执行
- **条件判定 `hitl:docs_migration_needed`**：将搬迁/归档/清理且清单未确认；满足→真，否则跳过该门。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`requirements-and-spec`、`product-shaping` → 见 §6 闭环。

### 本步规则卡：外部输入与关账

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认后将迭代绑定文档迁入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`；主档关闭时快照、主档不移动；「并行不关」只落新资料、不归档现行主档。
- L1 单点且 `plan` 步不适用 → 进入 `implement` 前落 `{workroot}/40-tasks/开发卡-{主题}-{yyyyMMdd}.md`（模板 `rules/templates/30-planning-tasks/dev-card-lite-template.md`，含验收表/SC 表）；L0 免。
- 交接包先 `handoff.receive`；本步不 `-StartTask`。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。
> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `requirements-and-spec` | **必开** | 进入本步即开（质量不降） | `skills/requirements-and-spec/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `product-shaping` | **必开** | 进入本步即开（质量不降） | `skills/product-shaping/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **模板**：L1 单点且 `plan` 步不适用 → 用 `rules/templates/30-planning-tasks/dev-card-lite-template.md`；L0 免；其它无强制模板。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:change | step=clarify | agent=implementer | packet=rules/packets/change/clarify.md | global=ok | skills=requirements-and-spec,product-shaping|done|na | claim=ALLOWED|DENIED|na | next=…
```
