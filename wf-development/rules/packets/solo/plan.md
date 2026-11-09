# 步骤卡 · solo/plan

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（本会话已读则不重读全文）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`solo` / `plan`（产品分析与方案）
- **packet**：`rules/packets/solo/plan.md`
- **角色**：`implementer`（常规实现）。需求/方案对齐 → 最小改动实现 → 自测/门禁 → 提测文档 → 提交；架构级先方案批准；本步只做该角色职责；越界交回或升级。
- **上游**：`frame`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`build`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：产品分析与方案
- **产出**：方案卡（{workroot}/20-design/方案卡-{主题}-{yyyyMMdd}.md）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：本会话已读 `rules/core/global-rules.md` 则不重读全文；未读过不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_spec`**：出示范围/接口/兼容与回滚/验收；批准后才实施（可在选模式 + 可选 AI 审之后）
- **推进**：本步完成后沿父链进入下一未跳过步；口令为单步（只出方案/只评审/代码评审/方案评审/只提测/只出清单/轻量方案）或动作清单写明停止/跳转时，以口令/清单为准，即停并输出收尾骨架。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`product-shaping`、`solution-design`、`task-breakdown`、`engineering-quality` → 见 §6 闭环。

- **条件技能**：`product-doc-analysis`（输入含 PRD/原型/产品文档） → 命中则同样走 §6 闭环。

### 本步动作清单

- 技能见 §6 `product-shaping`（产品分析）+ §6 `solution-design` 当前节 + §6 `engineering-quality` + §6 `task-breakdown`（任务拆分）。
- 模板 `rules/templates/30-planning-tasks/solution-card-template.md`。
- 本步只读/写方案卡，不改代码。
- 把「产品行为 + 技术方案 + 任务 + 验收 + 测试策略 + 风险」压到一页。
- 输入含文档/原型/截图/接口文档 → 先按 §6 `product-doc-analysis` 的 §0 Brief+差量表相关节（大改动/高风险全节）产出理解摘要，并入方案卡 §0/§1。
- 一句话输入用产品五字段+假设，不另起理解包。
- 方案卡 §0 必填「输入与理解」（原文/一句话 + 影响面 + 未确认项）。
- 大改动/高风险：§0/§1 全节 + 影响面/替代/非目标/AC 追溯/风险。
- 有文档/原型 → `product-doc-analysis`。
- 必填：范围/非目标、主流程与状态/权限/异常、改动面/接口/数据/兼容/回滚、任务（文件/AC）、验收表（ID/验收标准/检查/证据）、测试点（P0/P1/类型）、风险/假设/待确认。
- 验收表必须可被 `verify/Invoke-Gate.ps1` 读取。
- 每条 AC 有检查与证据（路径或命令）。
- 自检：AC 可观测。
- 每个任务有文件与验证。
- P0 测试点齐。
- 不把「应该/正常」写成验收。
- 需要正式评审/发布/QA/UAT/交接 → 转完整链。
- 技术上的接口/迁移/安全 → 在本链补方案与测试证据，不因体量换链。
- confirm_spec：出示「做什么/为什么/不做什么/怎么做/怎么验/风险」。
- 用户确认后进 build。
- 「只出轻量方案」→ 本步后直接 closeout，跳过 build/test。
- 更新 `{workroot}/INDEX.md`/`activeContext.md`（有变化时）。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → 读必做，并读现场处置/判定/反合理化（技能有这些节时）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `product-shaping` | **必开** | 进入本步即开（质量不降） | `skills/product-shaping/SKILL.md` | 只读 L13-L125（硬门槛+方法+反合理化）→ 回本包 |
| `product-doc-analysis` | 条件开 | 输入含 PRD/原型/产品文档 | `skills/product-doc-analysis/SKILL.md` | 只读 L12-L19（必做）→ 回本包 |
| `solution-design` | **必开** | 进入本步即开（质量不降） | `skills/solution-design/SKILL.md` | 只读 L13-L112（硬门槛+方法+反合理化）→ 回本包 |
| `task-breakdown` | **必开** | 进入本步即开（质量不降） | `skills/task-breakdown/SKILL.md` | 只读 L12-L107（硬门槛+方法+反合理化）→ 回本包 |
| `engineering-quality` | **必开** | 进入本步即开（质量不降） | `skills/engineering-quality/SKILL.md` | 只读 L13-L65（硬门槛+方法）→ 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/30-planning-tasks/solution-card-template.md`；只读本步用到的节，禁止整文件通读。
- 验证命令：`verify/Invoke-Gate.ps1`（本步非完成 Claim；按 Mode 出回执即可）。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:solo | step=plan | agent=implementer | packet=rules/packets/solo/plan.md | global=ok | skills=product-shaping,product-doc-analysis,solution-design,task-breakdown,engineering-quality|done|na | claim=ALLOWED|DENIED|na | next=…
```
