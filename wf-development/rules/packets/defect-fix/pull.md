# 步骤包 · defect-fix/pull

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-development
- **workflow**：`defect-fix`
- **step**：`pull`（拉取与归组）
- **packet**：`rules/packets/defect-fix/pull.md`
- **角色**：`defect-fixer`（缺陷修复编排）。平台拉取 → 分类 → 红证修复或产品评估 → 门禁 → 菜单 → 按 YAML hitl 提交/部署/回写 → 发布后验证；本步只做该角色职责；越界交回或升级。
- **上游**：`preflight`（取其产出为本步输入；该步被 `when` 跳过时按缺口停/补齐）
- **后续**：`triage`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/defect-fix/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/defect-fix/_region-intake.md`（接入与分类；进本区一次）。

## 2. 本步目标

- **目标**：拉取与归组
- **产出**：清单摘要/分组

## 3. 本步硬约束

### 开局硬门（3 条；其余见 cold-start §1）

- 1. **每轮先判、再动手**：先判新任务/续跑/只读；新任务或范围变化 → 复述目标/范围/验收并确认；续跑一行确认；只读一句话；首行锚 `route/step/packet` 或 `mode=analyze`；未确认禁写、禁下结论。
- 7. **完成只认门**：`-Claim` → `CLAIM: ALLOWED`；无 ALLOWED 禁写完成/通过/可提测。有 UI → 当前包内前端硬门；无 UI 标 `na`。
- 11. **技能闭环**：§6 必开 skill 打开→执行→回包；禁止粘贴代替。
- 其余硬约束见 `rules/core/cold-start.md` §1（常驻；勿在步内重读全文）。

### 本步读链与防丢失

- **编排**：本文 §5 +（若 §7 列出）一个模板。
- **方法质量**：§6 必开/条件开技能 → **逐个打开→执行→回本包**（一次 1 个）；禁止用粘贴代替实读。
- **禁止**：通读 rules / 多 step packet / 预读本 workflow 全部 skill。
- **完成声称**：有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **上下文锚**：`packet=`/`reads=` 必须含本 packet；切步/出子机前心跳刷新。

### 本步禁止

- 禁止读取本清单外的 rules / skills 正文；需要跳转只按 §6/§7 各一次。
- 禁止跳过 §6 必开技能，或用摘要代替实读。
- 禁止未过 §4 门或未出 §8 信号就宣称完成、推进或写「已通过」。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。
- **推进**：本步完成后沿父链进入下一未跳过步；口令为单步（只出方案/只评审/代码评审/方案评审/只提测/只出清单/轻量方案）或动作清单写明停止/跳转时，以口令/清单为准，即停并输出收尾骨架。

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 首条回执含 mode=（缺陷批加严，见 subagents）。拉取后读全单：提交信息（标题/steps/数据/环境/附件）＋历史备注/讨论＋产品评估/回复附件。
- **批量侦察**（子代理编排 ）：≥5 单且读单成本高（多备注/附件/评估单）或合计 ≥20k token → 逐单只读扇出（一单/小批一子代理），返回「分类候选/证据缺口/查重键/产品评估要点」≤30 行。
- 编排集中读回执并读关键单原文。
- 不可用→deviation=subagent_skipped:unavailable，仍进 triage 出分类表。 同号重复修复预检。
- 归组后进入 triage（未 triage 禁改码）。 历史预检跳过项：产品缺陷待产品确认 → 跳过标注「待产品」。
- 已修复未再激活 → 跳过标注「已处理」。
- 无法确认被激活 → 重新分类处置。
- 产品已回复/已退回 → 直接进 product_decision。

本步不嵌入前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回本包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/defect-fix/_chain.md`。
- 子状态机（进区一次）：`rules/packets/defect-fix/_region-intake.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:defect-fix | step=pull | agent=defect-fixer | packet=rules/packets/defect-fix/pull.md | reads=rules/packets/defect-fix/pull.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/defect-fix/pull.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
