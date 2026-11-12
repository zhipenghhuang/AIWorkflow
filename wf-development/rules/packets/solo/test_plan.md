# 步骤卡 · solo/test_plan

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`solo` / `test_plan`（测试分析与计划）
- **packet**：`rules/packets/solo/test_plan.md`
- **角色**：`test-planner`（测试分析与计划（开发自包含链））。按方案卡写测试分析与计划；不写代码、不执行测试、不判版本准出；本步只做该角色职责；越界交回或升级。
- **上游**：`review_docs`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`build`
- **失败去向**：回 design 修方案卡；AC/范围不清先停下说明
- **条件判定 `when:plan_has_code_change`**：方案卡改动面含代码/配置/页面/接口（非纯文档）；满足→真，否则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：测试分析与计划
- **产出**：测试分析与计划（{workroot}/50-verification/测试分析与计划-{主题}-{yyyyMMdd}.md）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`test-design-and-execution` → 见 §6 闭环。

### 本步动作清单

- 技能见 §6 `test-design-and-execution`（测试卡/设计）。
- 模板 `rules/templates/40-delivery/solo-test-plan-template.md`。
- 输入：方案卡 §0/§1/§4（理解/产品行为/AC）。
- 只做测试分析与计划，不改代码。
- 产出：来源/AC 账本、影响面/核心链路、覆盖矩阵、P0/P1/P2、环境/数据、不测、回归锚点。
- 纯文档 `plan_has_code_change=false` 跳过。
- 代码/配置必产。
- 测试报告只写执行结果，不重复本计划。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。
> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `test-design-and-execution` | **必开** | 进入本步即开（质量不降） | `skills/test-design-and-execution/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/40-delivery/solo-test-plan-template.md`；只读本步用到的节，禁止整文件通读。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:solo | step=test_plan | agent=test-planner | packet=rules/packets/solo/test_plan.md | global=ok | skills=test-design-and-execution|done|na | claim=ALLOWED|DENIED|na | next=…
```
