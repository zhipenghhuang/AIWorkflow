# 步骤包 · defect-fix/gates

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-development
- **workflow**：`defect-fix`
- **step**：`gates`（门禁）
- **packet**：`rules/packets/defect-fix/gates.md`
- **角色**：`verifier-agent`（独立验证（开发轨））。只读核验验收清单、diff、证据与完成门结果；返回通过/需修/阻塞；不改代码、不做最终交付判断；本步只做该角色职责；越界交回或升级。
- **前置**：缺陷修复卡/任务清单含本轮 AC 验收表（L1+）；无则先补
- **上游**：`clarify`（取其产出为本步输入；该步被 `when` 跳过时按缺口停/补齐）
- **后续**：`menu`（进 `menu` 前的 `when=implementation_required`）
- **失败去向**：停止本批；不得进入 menu/close，先修复、补证据或报阻塞
- **条件步** `when=has_code_change`：条件不满足则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/defect-fix/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/defect-fix/_region-fix.md`（修复与门禁；进本区一次）。

## 2. 本步目标

- **目标**：门禁
- **产出**：.gate/wf-development/completion.json + 门禁摘要

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

- **GATE `completion-gate`**：任务开始 `-StartTask`；运行 `verify/Invoke-Gate.ps1 -Acceptance ...`；写 `.gate/wf-development/completion.json`；**前端套装与 capture 只认本包硬约束与做法**；**写完成前 `-Claim`，只认 `CLAIM: ALLOWED`**；空 diff=`NOT_VERIFIED`、dry-run=`DRY_RUN`、缺项 → `BLOCKED`
- **推进**：本步完成后沿父链进入下一未跳过步；口令为单步（只出方案/只评审/代码评审/方案评审/只提测/只出清单/轻量方案）或动作清单写明停止/跳转时，以口令/清单为准，即停并输出收尾骨架。

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 本批无代码/配置改动项 → 跳过（纯文档/纯评估）。
- 有改动运行 `verify/Invoke-Gate.ps1 -Acceptance <缺陷修复卡/任务清单>`，门写 `.gate/wf-development/completion.json`。
- L1+ 无验收表先补，不得空跑门。 `has_code_change` = 本轮 diff 非空（不含生成物）。
- 与 `implementation_required`（清单已确认）区分，避免纯文档批空跑门。 日志分诊（子代理编排 ）：原始日志落盘，先脚本过滤。
- 仅多文件语义归因才派子代理，返回摘要 ≤30 行。 失败不声称完成。
- 存量失败只对账新增。
- 工具/环境缺失 → BLOCKED。

### 前端硬门（本步含 UI · 单源）

- **必读**：`rules/core/frontend-gate.md` §1–§5（打开→按本步产出/证据执行→回包）。
- 无 UI → 整节标 `na` + 一句理由；有 UI 不得只看代码/测试/API 200。
- 证据、分级、矩阵、截图/console/network 要求只认该文件，不在本包重复。

## 6. 技能指向（打开 → 执行 → 回本包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/defect-fix/_chain.md`。
- 子状态机（进区一次）：`rules/packets/defect-fix/_region-fix.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 验证：`verify/Invoke-Gate.ps1`（完成声称加 `-Claim`）；有 UI 另按 §5 前端硬门。

## 8. 完成信号

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:defect-fix | step=gates | agent=verifier-agent | packet=rules/packets/defect-fix/gates.md | reads=rules/packets/defect-fix/gates.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/defect-fix/gates.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
