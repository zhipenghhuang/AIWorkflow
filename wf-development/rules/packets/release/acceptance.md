# 步骤卡 · release/acceptance

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`release` / `acceptance`（业务验收）
- **packet**：`rules/packets/release/acceptance.md`
- **角色**：`delivery-lead`（交付/发布/验收编排）。提测就绪 → UAT/验收 → 发布审批 → 部署 → 冒烟/监控 → 发布记录/复盘；本步只做该角色职责；越界交回或升级。
- **上游**：`readiness`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`approval`（进 `approval` 前的 `when=release_ready_and_acceptance_passed`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:has_uat`**：本轮有 UAT/业务验收要求；满足→真，否则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：业务验收
- **产出**：UAT/验收记录（{workroot}/50-verification/）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_acceptance`**：出示 AC 覆盖/失败项/遗留风险/发布建议；确认后进审批
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`acceptance-and-launch` → 见 §6 闭环。

### 本步动作清单

- 条件步：有业务验收/产品签收要求才走。
- 技能见 §6 `acceptance-and-launch`。
- 模板 `rules/templates/40-delivery/uat-acceptance-template.md`。
- 可选输入：项目已有 UAT/验收资料（任意路径/来源，含产品包/测试报告/用户提供）→ 直接引用/对照，不重复验收。
- 没有 → 本步产 UAT（不要求安装其它包）。
- 对照需求基线/PRD AC + 测试报告 + 提测单。
- 结论=通过/有条件/不通过。
- 失败/遗留不瞒报。
- confirm_acceptance：出示 AC 覆盖/失败项/遗留风险/发布建议，确认后进入审批。
- 未签收不得审批（用户豁免须记录）。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。
> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `acceptance-and-launch` | **必开** | 进入本步即开（质量不降） | `skills/acceptance-and-launch/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/40-delivery/uat-acceptance-template.md`；只读本步用到的节，禁止整文件通读。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:release | step=acceptance | agent=delivery-lead | packet=rules/packets/release/acceptance.md | global=ok | skills=acceptance-and-launch|done|na | claim=ALLOWED|DENIED|na | next=…
```
