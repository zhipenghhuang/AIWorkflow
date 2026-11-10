# 步骤卡 · change/deliver

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（每步先读并逐条过）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`change` / `deliver`（提测与发布文档）
- **packet**：`rules/packets/change/deliver.md`
- **角色**：`implementer`（常规实现）。需求/方案对齐 → 最小改动实现 → 自测/门禁 → 提测文档 → 提交；架构级先方案批准；本步只做该角色职责；越界交回或升级。
- **上游**：`verify`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`release_handoff`（进 `release_handoff` 前的 `when=has_deploy`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:has_qa_or_deploy_or_requested`**：本轮有提测/QA/部署交付，或点名 deliver；满足→真，否则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：提测与发布文档
- **产出**：提测单/发布说明/回滚预案（{workroot}/60-release/）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：每步读 `rules/core/global-rules.md` 并逐条过；本步未读不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_intent`**：仅当 `intent_needs_confirm`：出示【意图理解】，确认后才落盘。意图已清 → 跳过本门（可一行回执即做）。细则 `clarification.md` §0。≠ `confirm_understanding`；≠ `confirm_handoff`
- **条件判定 `hitl:intent_needs_confirm`**：给谁·做什么·形态无法唯一确定，或跨角色外发未对齐，或新开对外交付；满足→真，否则跳过该门。
- **GATE `s6-admission`**：**checklist**：按 `verification.md` §2.2 的 `DEV/QA/PRODUCT` 分流表核；`DEV` 未清零、`QA` 未入提测单、`PRODUCT` 未关闭 → 不得标“可提测”；证据=内部分流表+提测单+评审报告。分流表留在内部质量记录，不写入测试提测单。
- **推进**：本步完成后沿父链进入下一未跳过步；口令为单步（只出方案/只出轻量方案/只评审/代码评审/方案评审/只提测/只出清单）或动作清单写明停止/跳转时，以口令/清单为准，即停并输出收尾骨架。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`qa-handoff-and-release` → 见 §6 闭环。

### 本步动作清单

- 自洽提测单真源 60-release，同轮拷 handoff/outbound。
- 未 COMPLETE 不得标可提测。
- 跳过本步≠跳过自验。
- 附加 HO 包另走 handoff。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → 读必做，并读现场处置/判定/反合理化（技能有这些节时）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `qa-handoff-and-release` | **必开** | 进入本步即开（质量不降） | `skills/qa-handoff-and-release/SKILL.md` | 只读 L10-L152（硬门槛+方法+反合理化）→ 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/40-delivery/qa-handoff-template.md`；只读本步用到的节，禁止整文件通读。
- 验证命令：`verify/Invoke-Gate.ps1`（完成须 `-Claim` → `CLAIM: ALLOWED`）。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步完成 Claim 门：须 `CLAIM: ALLOWED` 后才可写完成态。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:change | step=deliver | agent=implementer | packet=rules/packets/change/deliver.md | global=ok | skills=qa-handoff-and-release|done|na | claim=ALLOWED|DENIED|na | next=…
```
