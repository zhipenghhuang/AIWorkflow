# 步骤卡 · materials/index

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守；重读按 §7 分级）；方法在 §6 指定节（打开→执行→回包）。**未打开本文件=未开跑本步**。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`materials` / `index`（版本说明、索引与校验）
- **packet**：`rules/packets/materials/index.md`
- **角色**：`test-orchestrator`。按本步目标与 §5 动作执行；本步只做该角色职责；越界交回或升级。
- **上游**：`sync`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`closeout`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。

## 2. 本步目标

- **目标**：版本说明、索引与校验
- **产出**：docs/materials/{ver}/README.md + docs/materials/INDEX.md + 【材料库校验】通过/待补

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：按 `rules/core/global-rules.md` §7 **分级重读并遵守**（中段=最小集，禁每步通读全文）；须先打开本步骤卡；心跳 `global=ok`=已按 §7 复核且步骤卡已实读；未复核不得写 `global=ok`。偏离写 `global=dev:<原因>`。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **GATE `materials-validate`**：按本包门表该门的检查方法核验并留证据；未过不得宣称完成。
- **推进**：本流程为 `chain: full`；本步完成后进入下一未跳过步，直至 closeout。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- README 写版本、范围、包含/不包含、阅读顺序、来源、缺失/待补、本次是否覆盖刷新。
- INDEX 登记所有文件：版本/域/文档/来源（IN-xxxx、docs/... 或 generated）/状态/更新时间。
- 刷新 `last_published_at`。
- 状态只写 `current superseded`。
- 默认覆盖同 ver。
- 仅显式保留历史时升 `rev` 或 `{ver}-r2`。
- **门（materials-validate）**：README/INDEX 齐。
- 所有文件有登记。
- 来源可解析。
- 无草稿/证据/密钥/PII。
- 链接自包含，只发 `{ver}/` 不缺文件。
- 测试数据默认不外发。
- 旧版本状态正确。
- 待补项列明，不把“已生成”说成“已完整”。
- 多包：README/INDEX 由开发包（无则产品包）刷新。
- 本包只提交 `05-testing` 与索引行，不重建他域。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读技能库找感觉。

## 7. 模板与证据

- **填写模板（主）**：`rules/templates/00-onboarding/materials-index-template.md`；只读本步用到的节，禁止整文件通读。
- **配套模板（按产出需要读；门按结构判分的产物须对齐）**：`rules/templates/00-onboarding/materials-version-readme-template.md`。
- **产出前自检**：对照模板必填节逐项填写；缺节、空节、未替换 `{…}` = 不合格（不得标完成）。
- 验证命令：`verify/Invoke-Gate.ps1`（本步非完成 Claim；按 Mode 出回执即可）。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- §2 产出已按模板必填节落地；无空节、无未替换占位符。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:materials | step=index | agent=test-orchestrator | packet=rules/packets/materials/index.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
