# 步骤卡 · control/run

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（每步先读并逐条过）；方法在 §6 指定节（打开→执行→回包）。选路前只读本包；选路后关闭本包，只打开目标步骤卡。

## 1. 元信息

- **workflow / step**：`control` / `run`（按计划执行）
- **packet**：`rules/packets/control/run.md`
- **角色**：`iterate-lead`（迭代交付编排）。方案/需求 → 任务清单（含 DoR/DoD）→ 确认节奏 → 编排实施（实施交 implementer）→ 评审/门禁 → 提测 → 总结拟提交；本步只做该角色职责；越界交回或升级。
- **上游**：`init`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：目标步骤卡（不自动打开 `sync`；「进度」才回 `sync`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：按计划执行
- **产出**：切包声明（目标 workflow/step/packet）+ activeContext 运行状态更新；实施/方案/任务正文只在目标步骤卡产出

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：每步读 `rules/core/global-rules.md` 并逐条过；本步未读不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 选路完成前只读本包 + §6 技能。
- 选路后同轮关闭本包，只打开目标步骤卡；目标卡的技能、门、原文回指取代本包。
- 禁止把目标卡规则抄进本包，禁止在本包内实施。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。
- **推进**：本步只完成切包；**不**沿 control 自动进入 `sync`。同轮更新 `activeContext` 后关闭本包，只打开目标步骤卡；目标步到下一 `hitl`/产出停点即停；之后用户说「进度」→ `sync`，或再说「按开发计划执行」进下一阶段。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`development-plan` → 见 §6 闭环。

### 本步规则卡：计划切包（只路由，不实施）

- **本步唯一产出**：目标 `workflow/step` + 同轮更新 `activeContext` 运行状态（含 `packet=`）+ 一行切包锚；然后**立即只打开目标步骤卡**执行。
- **禁在本步**：写/改业务代码、方案正文、任务清单正文、理解包正文、提测单正文；跑前端 capture/parity；宣称阶段完成或 `CLAIM`。
- **选路表（按开发计划 §0 当前阶段）**：
  - S0/S1：有 PRD/原型/方案原文 → `change/analyze_input`；仅口头/缺口 → `change/clarify`；已理解待基线 → `change/requirements`
  - S2 → `change/design`（只要方案则到 design/review-docs 停）
  - S3：无确认清单 → `iterate/plan`；清单待确认 → `iterate/confirm`
  - S4/S5 选链：已有确认任务清单/`iterate` 进行中 → `iterate`（implement→review→gates）；否则 → `change`（implement→review→verify）。拿不准 → 推荐 iterate + 一问
  - S6 → 同链 `deliver`（有清单走 iterate，否则 change）
  - S7：本包只收测试结论/缺陷为**可选输入**并回写计划；有测试包且要跑测 → 提示改用测试包 `testing/execute`（本会话不跨包执行）；无测试包 → 开发自验证据 + 缺口一句
  - S8 → `release` 对应当前子步；S9 → `retro/gather`
- 计划状态非「已确认/执行中」→ 回 `control/init`；有未吸收新输入 → 先 `intake/scan`；上游 HO 未签收/退回 → 先 `handoff/receive`。
- 目标步执行到下一 `hitl`/产出停点即停；回写开发计划证据后，用户说「进度」→ `control/sync`，或再说「按开发计划执行」进下一阶段。
- **不降标**：目标步的必开技能、原文回指、前端硬门、完成门全数生效；本步不代替它们。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → 读必做，并读现场处置/判定/反合理化（技能有这些节时）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `development-plan` | **必开** | 进入本步即开（质量不降） | `skills/development-plan/SKILL.md` | 只读 L14-L159（硬门槛+方法+反合理化）→ 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
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
route=workflow:control | step=run | agent=iterate-lead | packet=rules/packets/control/run.md | global=ok | skills=development-plan|done|na | claim=ALLOWED|DENIED|na | next=…
```
