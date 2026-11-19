# 步骤卡 · materials/index

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`materials` / `index`（版本说明、索引与校验）
- **packet**：`rules/packets/materials/index.md`
- **角色**：`delivery-lead`。按本步目标与 §5 动作执行；本步只做该角色职责；越界交回或升级。
- **上游**：`sync`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`closeout`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。

## 2. 本步目标

- **目标**：版本说明、索引与校验
- **产出**：docs/materials/{ver}/README.md + docs/materials/INDEX.md + 【材料库校验】通过/待补

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **GATE `materials-validate`**：**checklist**：README/INDEX 齐；文件均登记；来源可解析；无草稿/证据/密钥/PII；**链接自包含**（正文无未改写的工作区/`inbound/` 路径）；缺失三分类分列；完整包须 `00-overview` 含现行入口（`project-guide` 或等价）+ 阅读顺序（有冲突须效力说明）；`本包未完成` 为空；旧版本状态正确；不过不称完整。
- **推进**：本流程为 `chain: full`；本步完成后进入下一未跳过步，直至 closeout。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- README 写版本、范围、包含/不包含、阅读顺序、来源、缺失三类（产品缺口｜故意不收录｜本包未完成）、本次是否覆盖刷新。
- INDEX 登记所有文件：版本/域/文档/来源（IN-xxxx、docs/... 或 generated）/状态/更新时间。
- 刷新 `last_published_at`。
- 状态只写 `current`/`superseded`。
- 默认覆盖同 ver。
- 仅显式保留历史时升 `rev`/`{ver}-r2`。
- **门（materials-validate）**：README/INDEX 齐。
- 全文件已登记。
- 来源可解析。
- 无草稿/证据/密钥/PII。
- 链接自包含。
- 完整包 overview 硬项齐（`project-guide` 或等价 + 阅读顺序；有冲突须效力说明）。
- `本包未完成` 为空。
- 旧版状态正确。
- 有「本包未完成」或链接未改写 → 不过门、不称完整。
- 测试数据默认不外发。
- 多包：README/INDEX 由本包统一刷新。
- 只改本域与索引行。
- `06-release/` 业务文件不动。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读技能库找感觉。

## 7. 模板与证据

- **模板（产出该类文件时按此填；门按结构判分的产物须对齐）**：`rules/templates/00-onboarding/materials-index-template.md`；`rules/templates/00-onboarding/materials-version-readme-template.md`。
- **产出前自检**：对照模板必填节逐项填写；缺节、空节、未替换 `{…}` = 不合格（不得标完成）。
- 验证命令：`verify/Invoke-Gate.ps1`（本步非完成 Claim；machine 门按 Mode 出回执，checklist 门按 §4 清单留证、不跑）。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- §2 产出已按模板必填节落地；无空节、无未替换占位符。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:materials | step=index | agent=delivery-lead | packet=rules/packets/materials/index.md | global=ok | skills=na | claim=ALLOWED|DENIED|na | next=…
```
