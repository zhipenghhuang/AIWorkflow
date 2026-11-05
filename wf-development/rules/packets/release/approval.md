# 步骤包 · release/approval

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-development
- **workflow**：`release`
- **step**：`approval`（工程部署审批）
- **packet**：`rules/packets/release/approval.md`
- **条件步** `when=release_ready_and_acceptance_passed`：条件不满足则跳过本步（不打开本包）。
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/release/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/release/_region-ready.md`（就绪与批准；进本区一次）。

## 2. 本步目标

- **目标**：工程部署审批
- **产出**：工程部署审批记录

## 3. 本步硬约束

### 开局硬约束（本步可执行摘要）

- 1. **先意图、再动作**（`confirm_task_intent`）：新开先【需求与意图理解】再确认；未确认禁改代码/外发/下完成结论。
- 2. **短读跟随 + 一手源**：`activeContext` + 进行中（`rule_card`/`packet=`/`region=`）+ 偏好/洞见/坑 ≤3。
- 3. **状态机读链（硬）**：见本包「本步读链与防丢失」。父流程可拆子机；同时只激活**一个**步骤包。
- 4. **技能闭环（质量不降）**：步骤包 §6 标**必开**的 skill 必须打开→按必做执行→**回到步骤包**；禁止把 skill 正文嵌进步骤包替代实读；禁止跳过必开 skill。
- 5. **完成分层**：`verify/Invoke-Gate.ps1 -Claim` → 只认 `CLAIM: ALLOWED`。无 ALLOWED 禁止写「已通过」。
- 6. **前端硬门**：有 UI → 当前步骤包内前端硬门；无 UI 标 `na`。
- 7. **证据先于结论；禁刷绿**；密钥零入库；最小改动；失败同方案 2 次换路径。
- 8. **切步/出子机 → 心跳一行**，必须带 `packet=`（有子机带 `region=`）。

### 本步读链与防丢失

- **编排**：本文 §5 +（若 §7 列出）一个模板。
- **方法质量**：§6 必开/条件开技能 → **打开→执行→回本包**（同时 1 个 skill）；禁止用粘贴代替实读。
- **禁止**：通读 rules / 多 step packet / 预读本 workflow 全部 skill。
- **完成声称**：有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **上下文锚**：`packet=`/`reads=` 必须含本 packet；切步/出子机前心跳刷新。


## 4. 本步门

- **HITL `confirm_deploy`**：出示版本/窗口/影响面/回滚决策人；并核 **干净工作区 + 已提交或已打 tag + 本轮 `completion.json=COMPLETE`**；未批准不部署，禁止从脏工作区部署；**仅生产/正式环境**，test/staging 部署不触发本门；生产版本必须无 prerelease

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 工程 go/no-go：基于上线检查单 + UAT/验收 + 测试报告 + 风险/回滚。
- 出示版本/窗口/影响面/回滚决策人。
- 并核**干净工作区 + 已提交或已打 tag + completion=COMPLETE**。 **目标必须是生产/正式环境**。
- test/staging 部署不触发本门，版本按项目策略。生产版本必须是正式版（无 prerelease）。
- rc/QA 批次直接上生产 → NO-GO。 若项目已有业务发布决策（其它流程/产品包/用户确认）且 UAT 已过 → 本步只确认工程就绪，不重复业务决策。
- 没有 → 本门覆盖业务+工程范围。 未批准不得部署。
- 禁止从脏工作区/未提交代码部署。
- 有条件批准须列明条件与监控措施。
- 发布内容/窗口/回滚变更 → 重新确认。输出 `release_approved=true/false` 供 deploy 判断。

## 6. 技能指向（打开 → 执行 → 回本包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/release/_chain.md`。
- 子状态机（进区一次）：`rules/packets/release/_region-ready.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:release | step=approval | packet=rules/packets/release/approval.md | reads=rules/packets/release/approval.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/release/approval.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
