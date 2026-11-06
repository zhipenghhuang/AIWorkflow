# 步骤包 · defect-fix/fix

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-development
- **workflow**：`defect-fix`
- **step**：`fix`（红证与修复）
- **packet**：`rules/packets/defect-fix/fix.md`
- **角色**：`defect-fixer`（缺陷修复编排）。平台拉取 → 分类 → 红证修复或产品评估 → 门禁 → 菜单 → 按 YAML hitl 提交/部署/回写 → 发布后验证；本步只做该角色职责；越界交回或升级。
- **上游**：`align`（取其产出为本步输入；该步被 `when` 跳过时按缺口停/补齐）
- **后续**：`clarify`（进 `clarify` 前的 `when=need_clarification`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件步** `when=implementation_required`：条件不满足则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/defect-fix/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/defect-fix/_region-fix.md`（修复与门禁；进本区一次）。

## 2. 本步目标

- **目标**：红证与修复
- **产出**：修复/方案/验证结果

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

- **本步必开技能（质量不降）**：`debugging-and-error-recovery` → 见 §6 闭环。

- **条件技能**：`cross-layer-consistency`（命中权限/状态/数据基数/多表面） → 命中则同样走 §6 闭环。

### 本步动作清单

- **前置**：本批 triage【分类表】已输出。
- 未出表禁改业务代码（fix-collaboration §4.0）。仅修表中「实现缺陷」行。
- 待产品行不扩写。开跑声明 mode=（同文件集→单写手）。 修前红证。
- 无根因不修。
- 复现与写回按原单口径对齐、引用原单信息（协作。
- 红绿与换路径细则见 AGENTS ）。 **先写缺陷修复卡**（原单口径/SC 差集/同类路径/红证/验证站证据），再改代码。
- 矩阵与判定只认 `implementation-quality.md` ～，不另造表。 **动手前**：先 `verify/Invoke-Gate.ps1 -StartTask -TaskId "BUG-<id>" -ProjectRoot "."`（冻结 `base_commit`。
- 截图须晚于 `started_at`/验收清单）→ 来源完整性检查=0 缺漏（DEV-IQ-16，含相关方案/原型/接口/同类路径）→ 短【实施预检】（DEV-IQ-09。
- **命中须先扩 SC/债项**）。
- 命中重要面同批硬补（DEV-IQ-10）。
- 勾选 `iq-checklist.md`。
- 单元=一条 SC。
- 方法 `skills/implementation-and-selftest/SKILL.md`。 按 `skills/cross-layer-consistency/SKILL.md` 做同类路径扫描：同模型其他写入口、同谓词其他消费方、同权限端点/菜单、同状态其他表面。
- 逐条判「同defects/已正确/不适用」，原单+同类路径各补一条回归。
- 记录根因层/规则缺口。 **DEV-IQ-08**：同根因族 ≥2 → 除回归外须拟改rules/skills/检查项缺口（先拟改+原因+影响，用户确认后改母版或项目适配）。
- 禁止只关单号。 实现缺陷→按 修。
- 产品已认可/修改后认可→按新产品文档/评估单实施（/）。
- 产品改判实现缺陷→按产品说明修，备注引用产品结论。 复杂实施再按 rules/templates/20-design/solution-template.md 展开，文件名 方案-BUG-{id}-{主题}-{yyyyMMdd}.md。
- 简单修复不强制完整方案，但须更新受影响文档/任务清单。 **修复分片**（子代理编排 ）：≥3 单且文件不重叠 → 一组一子代理（worker-agent。
- 默认串行。
- 同文件集合并组）。
- 不达阈值直做。
- 子代理禁 commit/push/改平台，返回 ≤30 行可直填备注的事实素材（rules/defects/fix-collaboration.md ）。 高风险/大改/破坏性缺陷：核验者≠实施者（派 reviewer-agent 独立核验，只给原单＋diff＋红绿命令。
- 核验不替代门禁），并写 `.gate/review.md` 供完成门核对。

### 前端硬门（本步含 UI · 单源）

- **必读**：`rules/core/frontend-gate.md` §1–§5（打开→按本步产出/证据执行→回包）。
- 无 UI → 整节标 `na` + 一句理由；有 UI 不得只看代码/测试/API 200。
- 证据、分级、矩阵、截图/console/network 要求只认该文件，不在本包重复。

## 6. 技能指向（打开 → 执行 → 回本包）

> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `cross-layer-consistency` | 条件开 | 命中权限/状态/数据基数/多表面 | `skills/cross-layer-consistency/SKILL.md` | 必做区 → 回本包 |
| `debugging-and-error-recovery` | **必开** | 进入本步即开（质量不降） | `skills/debugging-and-error-recovery/SKILL.md` | 必做区 → 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/defect-fix/_chain.md`。
- 子状态机（进区一次）：`rules/packets/defect-fix/_region-fix.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 验证：`verify/Invoke-Gate.ps1`（完成声称加 `-Claim`）；有 UI 另按 §5 前端硬门。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:defect-fix | step=fix | agent=defect-fixer | packet=rules/packets/defect-fix/fix.md | reads=rules/packets/defect-fix/fix.md[+skill] | skills=cross-layer-consistency,debugging-and-error-recovery|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/defect-fix/fix.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
