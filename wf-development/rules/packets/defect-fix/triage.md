# 步骤包 · defect-fix/triage

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-development
- **workflow**：`defect-fix`
- **step**：`triage`（分类与处置）
- **packet**：`rules/packets/defect-fix/triage.md`
- **角色**：`defect-fixer`（缺陷修复编排）。平台拉取 → 分类 → 红证修复或产品评估 → 门禁 → 菜单 → 按 YAML hitl 提交/部署/回写 → 发布后验证；本步只做该角色职责；越界交回或升级。
- **上游**：`pull`（取其产出为本步输入；该步被 `when` 跳过时按缺口停/补齐）
- **后续**：`assess_product`（进 `assess_product` 前的 `when=product_defect`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/defect-fix/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/defect-fix/_region-intake.md`（接入与分类；进本区一次）。

## 2. 本步目标

- **目标**：分类与处置
- **产出**：分类结论（中文结论/依据/下一步）

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

- **条件技能**：`cross-layer-consistency`（命中权限/状态/数据基数/多表面） → 命中则同样走 §6 闭环。

### 本步动作清单

- **§4.0 门禁**：本步必产出【分类表】（≥2 单逐行：单号|处置|依据一句|下一步）。
- 未出表禁进 fix/禁改业务代码。
- 禁「多为实现缺陷」代替逐单。子代理不可用→mode=直做|单写手 + deviation=…，仍须出表。 按 rules/defects/fix-collaboration.md 分类： 实现缺陷→implementation_required。
- 产品缺陷/需求缺口/设计口径不明→product_defect。
- 信息不足/无法复现/环境数据不一致/预期不明/重复/设计如此/非defects/外部/已在其它构建修复→need_clarification。
- 延期/不修复须产品/项目确认，不得开发单方关闭。 产品缺陷不得先写完整技术方案，只写评估单。
- 口径存疑但实现路径清晰 → 出评审版修复方案（solution-template 裁剪，落 20-design/BUG优化修复方案/），评估单与评审版方案二选一，不重复出。 混批含产品缺陷+实现缺陷：两轨并行——实现项照常 fix（可先提交），产品项出评估单/评审版方案并 AWAIT_PRODUCT。
- 仅当实现项依赖产品结论时该实现项等待，不整批阻塞。 pull 已标「待产品」→ 直接输出 AWAIT_PRODUCT，不重新评估/不重复 handoff。 分类结论须引用原单 steps/数据/环境/设计依据，禁只看标题。
- 批量时以侦察回执为输入，**分类/五选一/处置集中**，不采信子代理终态。 拟标 product_defect 前须完成实现核对（相关代码路径与/或接口行为），只凭页面观感不得判产品缺陷。 测试无设计文档默认实现缺陷属正确。
- 开发改判需求缺口须写明并交产品终审，不与测试争默认。 不挡主路径且无合规/资金/数据风险的体验类 → 不硬推 product_defect。
- 点名要改走产品 change/需求池。 每条实现缺陷同时记「根因层（需求/设计/数据模型/实现/测试/契约/文档）+ 同类路径候选（同模型写入口/同谓词消费方/同权限端点/同状态表面）+ 规则缺口」。
- 按 `skills/cross-layer-consistency/SKILL.md` 取矩阵，不只修表面现象。 内部处置码只用于路由，不写进平台备注。

本步不嵌入前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回本包）

> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `cross-layer-consistency` | 条件开 | 命中权限/状态/数据基数/多表面 | `skills/cross-layer-consistency/SKILL.md` | 必做区 → 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/defect-fix/_chain.md`。
- 子状态机（进区一次）：`rules/packets/defect-fix/_region-intake.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:defect-fix | step=triage | agent=defect-fixer | packet=rules/packets/defect-fix/triage.md | reads=rules/packets/defect-fix/triage.md[+skill] | skills=cross-layer-consistency|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/defect-fix/triage.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
