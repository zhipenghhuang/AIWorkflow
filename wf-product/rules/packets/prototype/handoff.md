# 步骤卡 · prototype/handoff

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`prototype` / `handoff`（开发交接）
- **packet**：`rules/packets/prototype/handoff.md`
- **角色**：`ux-designer`（产品设计（信息架构/线框/视觉/高保真原型/评审/handoff/展示材料））。没有专职设计师时，由产品经理戴“设计帽子”，产出可用、可评审、可交付开发的高保真原型；本步只做该角色职责；越界交回或升级。
- **前置**：prototype.review 已通过；选 B 时 design-review 已 READY；或有用户明确豁免与依据
- **上游**：`usability`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`closeout`
- **失败去向**：回 review 补评审/覆盖矩阵/截图；未过不得交开发

## 2. 本步目标

- **目标**：开发交接
- **产出**：{workroot}/{ver}/20-design/开发交接-{主题}.md

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_prototype`**：原型路径/设计评审结论/交接要点；**评审前必须有 `prototype-coverage.md`（覆盖矩阵硬）+ 浏览器走查证据**；浏览器不可用时记 `browser=unavailable` 并用用户走查证据过门前评审；确认后才交开发
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`prototype-and-interaction` → 见 §6 闭环。

### 本步动作清单

- 按 `rules/templates/20-design/dev-handoff-template.md` 产 `开发交接-{主题}.md`：组件/状态/交互/动效/tokens/响应式/无障碍证据/验收对照。
- 覆盖矩阵与版本元数据。
- 评审通过后默认交付自洽开发交接文档（真源版本目录 + 实拷 `handoff/outbound/设计/`）。
- `DES` 包仅多文件/签收/仓外/点名时停问建议，确认后走 `handoff` 流程 的 `send`（落 `handoff/outbound/设计/{HO-ID}/`）。
- **不得在本步直接写 HO 包**。
- 必须写清设计意图、必须保留、可优化、未提供、需开发决策。
- 开发补充/差异化设计不得静默改主流程。
- 回链 PRD 追溯矩阵「原型/页面」列。
- 标注“原型≠生产代码”。
- confirm_prototype：出示原型路径/设计评审与可用性结论/交接要点请确认。
- 确认后交开发。
- PRD 追溯矩阵「原型/页面」列回填。
- 拟提交按 本步编排以当前步骤卡为准。
- 方法见 §6。
- 勿通读手册拼流程。

### 本步规则卡：变更与提交

- 变更/影响：先判事实与影响面；实质变更走 intake/CR，不静默改基线。
- 提交：默认仅本地提交；推送单独确认；禁 force push/切主干/擅自开 PR。
- 无文件变更 → 不硬造提交。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。
> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `prototype-and-interaction` | **必开** | 进入本步即开（质量不降） | `skills/prototype-and-interaction/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（主）**：`rules/templates/20-design/dev-handoff-template.md`；只读本步用到的节，禁止整文件通读。
- **配套模板（按产出需要读；门按结构判分的产物须对齐）**：`rules/templates/90-handoff/handoff-package-brief-template.md`。
- **产出前自检**：对照模板必填节逐项填写；缺节、空节、未替换 `{…}` = 不合格（不得标完成）。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- §2 产出已按模板必填节落地；无空节、无未替换占位符。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:prototype | step=handoff | agent=ux-designer | packet=rules/packets/prototype/handoff.md | global=ok | skills=prototype-and-interaction|done|na | claim=ALLOWED|DENIED|na | next=…
```
