# 步骤卡 · iterate/precheck

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（每步先读并逐条过）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`iterate` / `precheck`（前置检查）
- **packet**：`rules/packets/iterate/precheck.md`
- **角色**：`iterate-lead`（迭代交付编排）。方案/需求 → 任务清单（含 DoR/DoD）→ 确认节奏 → 编排实施（实施交 implementer）→ 评审/门禁 → 提测 → 总结拟提交；本步只做该角色职责；越界交回或升级。
- **上游**：无（链首）
- **后续**：`plan`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：前置检查
- **产出**：前置检查结果（需求签收/方案批准/清单/handoff/缺口）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：每步读 `rules/core/global-rules.md` 并逐条过；本步未读不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。
- **推进**：本步完成后沿父链进入下一未跳过步；口令为单步（只出方案/只出轻量方案/只评审/代码评审/方案评审/只提测/只出清单）或动作清单写明停止/跳转时，以口令/清单为准，即停并输出收尾骨架。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 缺理解包/未签收方案 → 回 change.analyze_input 或 requirements/design/review-docs。
- 交接包先 receive。
- 禁本步 -StartTask。
- 并行/关账见 iteration-delivery + 文档治理规则（工作根/原件根/索引/关版整夹）。

### 本步规则卡：文档治理

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认后将迭代绑定文档迁入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`；主档关闭时快照、主档不移动；「并行不关」只落新资料、不归档现行主档。
- 清理只删已知临时/缓存/未引用失败产物；不确定移 `_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 模板与证据

- **无强制模板**：§5 规则卡已给出输出形状；直接落 §2 产出。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:iterate | step=precheck | agent=iterate-lead | packet=rules/packets/iterate/precheck.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
