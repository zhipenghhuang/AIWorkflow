# 步骤卡 · solo/design

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`solo` / `design`（方案与验收）
- **packet**：`rules/packets/solo/design.md`
- **角色**：`implementer`（常规实现）。需求/方案对齐 → 最小改动实现 → 自测/门禁 → 提测文档 → 提交；架构级先方案批准；本步只做该角色职责；越界交回或升级。
- **前置**：product 已完成；方案卡 §0/§1 已冻结；产品/AC 未确认不得写技术方案
- **上游**：`product`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`review_docs`（进 `review_docs` 前的 `when=do_landing_doc_review`）
- **失败去向**：回 product 修产品分析；范围/AC 不清先停下说明

## 2. 本步目标

- **目标**：方案与验收
- **产出**：方案卡（方案/验收部分：§2/§3/§4/§6/§9）（{workroot}/20-design/方案卡-{主题}-{yyyyMMdd}.md）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_spec`**：出示范围/接口/兼容与回滚/验收；批准后才实施（可在选模式 + 可选 AI 审之后）
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`solution-design`、`task-breakdown`、`engineering-quality` → 见 §6 闭环。

- **条件技能**：`threat-modeling`（命中鉴权/权限/敏感数据/上传/回调/公共 API/资金/AI）、`performance-and-capacity`（命中列表/批量/导出/循环查库/无界集合/统计/首屏/高并发） → 命中则同样走 §6 闭环。

### 本步动作清单

- 技能见 §6 `solution-design` + §6 `task-breakdown`（任务拆分）+ §6 `engineering-quality`。
- 模板 `rules/templates/30-planning-tasks/solution-card-template.md`。
- 本步只写方案卡方案/验收部分（§2/§3/§4/§6/§9），不写产品分析/测试计划，不改代码。
- 必填：改动面/接口/数据/兼容/回滚、任务（文件/AC）、方案卡 §3.1 的 SC 表（方案条款/来源/落点/入口类型/证据；无行为变化写「不适用」）、验收表（ID/验收标准/检查/证据）、风险/假设/待确认。
- 验收表必须可被 `verify/Invoke-Gate.ps1` 读取。
- 每条 AC 有检查与证据。
- 自检：AC 可观测。
- 每个任务有文件与验证。
- 不把「应该/正常」写成验收。
- 需要正式发布/QA/UAT/交接 → 转完整链。
- 代码/文档评审在本链按条件执行。
- 技术上的接口/迁移/安全 → 在本链补方案与测试证据，不因体量换链。
- confirm_spec：出示「做什么/为什么/不做什么/怎么做/怎么验/风险」。
- 确认后进 review_docs（条件）→ test_plan（代码/配置）或 build（纯文档）。
- 「只出轻量方案」→ 本步后直接 closeout，跳过 review_docs/test_plan/build/review/test。
- 测试分析与计划由 test_plan 步产出。
- 本步不写测试计划/执行结果。
- 在方案卡 §9 写 review_required（true/false + 理由；L1+ UI 命中前端硬门 A 级/L2+/高风险/新功能 → true）和 do_landing_doc_review（true/false + 理由；L2+/高风险/新功能/落地文档 → true）。
- §9 过程证据填理解包/方案/评审记录/安全/回滚（gate 读取；可指本卡；未产生写不适用）。
- 更新 `{workroot}/INDEX.md`/`activeContext.md`（有变化时）。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。
> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `solution-design` | **必开** | 进入本步即开（质量不降） | `skills/solution-design/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `task-breakdown` | **必开** | 进入本步即开（质量不降） | `skills/task-breakdown/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `engineering-quality` | **必开** | 进入本步即开（质量不降） | `skills/engineering-quality/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `threat-modeling` | 条件开 | 命中鉴权/权限/敏感数据/上传/回调/公共 API/资金/AI | `skills/threat-modeling/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `performance-and-capacity` | 条件开 | 命中列表/批量/导出/循环查库/无界集合/统计/首屏/高并发 | `skills/performance-and-capacity/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（主）**：`rules/templates/30-planning-tasks/solution-card-template.md`；只读本步用到的节，禁止整文件通读。
- **产出前自检**：对照模板必填节逐项填写；缺节、空节、未替换 `{…}` = 不合格（不得标完成）。
- 验证命令：`verify/Invoke-Gate.ps1`（本步非完成 Claim；按 Mode 出回执即可）。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- §2 产出已按模板必填节落地；无空节、无未替换占位符。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:solo | step=design | agent=implementer | packet=rules/packets/solo/design.md | global=ok | skills=solution-design,task-breakdown,engineering-quality|done|na | claim=ALLOWED|DENIED|na | next=…
```
