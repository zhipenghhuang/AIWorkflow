# 步骤卡 · materials/select

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`materials` / `select`（选择版本与范围）
- **packet**：`rules/packets/materials/select.md`
- **角色**：`pm-lead`。按本步目标与 §5 动作执行；本步只做该角色职责；越界交回或升级。
- **上游**：无（链首）
- **后续**：`sync`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。

## 2. 本步目标

- **目标**：选择版本与范围
- **产出**：【材料库发布范围】版本/受众/域/包含/排除

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_materials`**：一页纸/Deck/user/资料库/整包导出/发布说明；数字/截图/流程与当前项目一致；仅对外发送、承诺或发布前触发
- **条件判定 `hitl:materials_for_external`**：材料/文档将对外发送、承诺或发布；满足→真，否则跳过该门。
- **推进**：本流程为 `chain: full`；本步完成后进入下一未跳过步，直至 closeout。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 先按 文档治理规则（工作根/原件根/索引/关版整夹） 定位工作根，再读 `{workroot}/INDEX.md`、`{workroot}` 当前定稿与 `docs/materials/INDEX.md`。
- 版本取项目/迭代版本。
- 缺则问一次，不硬造。
- 默认只收定稿、正确、完整、可独立阅读的文档。
- 草稿/过程/证据/密钥/PII/未授权第三方文档不进库。
- 域默认：`01-requirements` `02-design` `06-release`（业务决策）。
- **发布模式默认 overwrite-latest**：未明确「保留历史/不覆盖/升 rev/另存快照/签收锁定」→ 不询问、直接覆盖目标 `{ver}/`。
- 换迭代关账触发时：先覆盖刷新关闭版 `{prev}/`，再处理 `{next}/`（文档治理关账）。
- 对外发送/承诺前走 `confirm_materials`（仅内部入库不触发）。

### 本步规则卡：文档治理

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认后将迭代绑定文档迁入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`；主档关闭时快照、主档不移动；「并行不关」只落新资料、不归档现行主档。
- 清理只删已知临时/缓存/未引用失败产物；不确定移 `_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。

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
route=workflow:materials | step=select | agent=pm-lead | packet=rules/packets/materials/select.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
