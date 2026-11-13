# 步骤卡 · new-product/go

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`new-product` / `go`（立项评审）
- **packet**：`rules/packets/new-product/go.md`
- **角色**：`pm-analyst`（需求洞察与优先级（含受理转入的新需求））。来源分层收集需求 → 入需求池 → 分级排序 → 立项输出范围与风险；不臆造；本步只做该角色职责；越界交回或升级。
- **上游**：`discover`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`define`（进 `define` 前的 `when=go_decision_go`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。

## 2. 本步目标

- **目标**：立项评审
- **产出**：立项决策记录（Go/Hold/Kill + 依据/待verify/责任人，并入立项书）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_go`**：出示问题/市场/方案/MVP 假设/成本收益/风险/结论（Go/Hold/Kill）；未过不写全量 PRD
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`zero-to-one-product-definition`、`customer-needs-discovery`、`competitive-intelligence-and-learning` → 见 §6 闭环。

### 本步动作清单

- 出示问题 用户 市场 竞品 方案与 MVP 假设 成本收益 风险 结论（Go Hold Kill）请确认。
- 批准（Go）才进入产品定义。
- Hold 列待验证项与责任人。
- Kill 记录原因并归档。
- Hold/Kill 后直接 `closeout`/归档。
- `define/prd/deliver/launch` 的 `when: go_decision_go` 会自动跳过，不得继续写 PRD/排期/问发布。
- **未过立项不写全量 PRD**（本步编排以当前步骤卡为准；方法见 §6；勿通读手册拼流程 ）。

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
| `zero-to-one-product-definition` | **必开** | 进入本步即开（质量不降） | `skills/zero-to-one-product-definition/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `customer-needs-discovery` | **必开** | 进入本步即开（质量不降） | `skills/customer-needs-discovery/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `competitive-intelligence-and-learning` | **必开** | 进入本步即开（质量不降） | `skills/competitive-intelligence-and-learning/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **无强制模板**：§5 规则卡已给出输出形状；直接落 §2 产出。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:new-product | step=go | agent=pm-analyst | packet=rules/packets/new-product/go.md | global=ok | skills=zero-to-one-product-definition,customer-needs-discovery,competitive-intelligence-and-learning|done|na | claim=ALLOWED|DENIED|na | next=…
```
