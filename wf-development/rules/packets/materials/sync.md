# 步骤卡 · materials/sync

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`materials` / `sync`（同步权威文档）
- **packet**：`rules/packets/materials/sync.md`
- **角色**：`delivery-lead`。按本步目标与 §5 动作执行；本步只做该角色职责；越界交回或升级。
- **上游**：`select`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`index`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。

## 2. 本步目标

- **目标**：同步权威文档
- **产出**：docs/materials/{ver}/（00-overview～07-appendix，按需）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。
- **推进**：本流程为 `chain: full`；本步完成后进入下一未跳过步，直至 closeout。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 从 `{workroot}` 选当前定稿，按域**覆盖复制**到 `docs/materials/{ver}/`。
- 从 `inbound/` 选权威正确外部输入， 按域放入同一版本。
- 不按 inputs/deliverables 分栏，来源写 `docs/materials/INDEX.md`。
- 每个 `{ver}/` 自包含。
- 不建外挂 `_common/`。
- 不设 `_archive/`。
- 旧版本目录保留。
- 默认就地覆盖已有文件。
- 仅显式保留历史时写入 `{ver}-r2` 或升 rev，不覆盖旧目录。
- 不直接编辑材料库正文。
- 需要改先改 `{workroot}` 再重新发布（默认仍覆盖同 ver）。
- 多包：只覆盖本包域。
- 他域文件不动。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 模板与证据

- **无强制模板**：§5 编排已给出动作/顺序；直接落 §2 产出。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:materials | step=sync | agent=delivery-lead | packet=rules/packets/materials/sync.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
