# 步骤卡 · release/approval

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`release` / `approval`（工程部署审批）
- **packet**：`rules/packets/release/approval.md`
- **角色**：`delivery-lead`（交付/发布/验收编排）。提测就绪 → UAT/验收 → 发布审批 → 部署 → 冒烟/监控 → 发布记录/复盘；本步只做该角色职责；越界交回或升级。
- **上游**：`acceptance`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`deploy`（进 `deploy` 前的 `when=release_approved`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:release_ready_and_acceptance_passed`**：上线检查单 GO，且 UAT 通过或不需要；满足→真，否则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：工程部署审批
- **产出**：工程部署审批记录

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_deploy`**：未批准
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 工程 go/no-go：基于上线检查单 + UAT/验收 + 测试报告 + 风险/回滚。
- 出示版本/窗口/影响面/回滚决策人。
- 并核**干净工作区 + 已提交或已打 tag + completion=COMPLETE**。
- **目标必须是生产/正式环境**。
- test/staging 部署不触发本门，版本按项目策略。
- 生产版本必须是正式版（无 prerelease）。
- rc/QA 批次直接上生产 → NO-GO。
- 若项目已有业务发布决策（其它流程/产品包/用户确认）且 UAT 已过 → 本步只确认工程就绪，不重复业务决策。
- 没有 → 本门覆盖业务+工程范围。
- 未批准不得部署。
- 禁止从脏工作区/未提交代码部署。
- 有条件批准须列明条件与监控措施。
- 发布内容/窗口/回滚变更 → 重新确认。
- 输出 `release_approved=true/false` 供 deploy 判断。

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
route=workflow:release | step=approval | agent=delivery-lead | packet=rules/packets/release/approval.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
