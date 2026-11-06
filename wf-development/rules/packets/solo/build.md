# 步骤包 · solo/build

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-development
- **workflow**：`solo`
- **step**：`build`（实施与自测）
- **packet**：`rules/packets/solo/build.md`
- **角色**：`implementer`（常规实现）。需求/方案对齐 → 最小改动实现 → 自测/门禁 → 提测文档 → 提交；架构级先方案批准；本步只做该角色职责；越界交回或升级。
- **前置**：plan 已确认；方案卡验收表已冻结；范围/AC 未确认不得写代码
- **上游**：`plan`（取其产出为本步输入；该步被 `when` 跳过时按缺口停/补齐）
- **后续**：`test`
- **失败去向**：回 plan 修方案卡；范围超出先停下说明
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/solo/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/solo/_region-build.md`（建造验证；进本区一次）。

## 2. 本步目标

- **目标**：实施与自测
- **产出**：代码/配置改动 + 自测证据

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

- **本步必开技能（质量不降）**：`implementation-and-selftest`、`engineering-quality` → 见 §6 闭环。

### 本步动作清单

- **动手前硬门**：勾选 `iq-checklist.md`。
- 有行为变化须 DEV-IQ-09【实施预检】且**命中面先扩 SC/债项**（未扩表=预检无效，禁改码）。
- 有方案条款时 SC 差集=0（DEV-IQ-12）。
- 命中重要面 → DEV-IQ-10 同批硬补（轻量不降硬补）。方法 `implementation-and-selftest`。
- 细则 `implementation-quality.md`/§4.3。 技能：`implementation-and-selftest`（先读再改）+ `engineering-quality`。
- 预检命中面再读对应技能当前节。
- 失败时 + `debugging-and-error-recovery`。 动手前写本轮任务标记：`verify/Invoke-Gate.ps1 -StartTask -TaskId "<任务ID>" -ProjectRoot "."`（仅本步。
- frame/plan 不计窗口）。 按方案卡验收表+预检扩出的 SC 实施。
- **可验证单元=一条 SC**（自证后再下一条。
- 页面能开≠单元完成）。
- 前端按 `verify/frontend/acceptance.md` 留状态/视口/console/network 截图。 可测逻辑补测。
- 密钥零入库。
- 外部输入校验。
- 破坏性变更先停。
- 改动面超出方案卡 → 停下说明，不擅自扩范围。 需独立评审/多波次/跨模块 → 升级 `change`/`iterate`。
- 本步不冒充已评审。 实施完更新方案卡「执行记录」与任务状态，准备 test。

### 前端硬门（本步含 UI · 单源）

- **必读**：`rules/core/frontend-gate.md` §1–§5（打开→按本步产出/证据执行→回包）。
- 无 UI → 整节标 `na` + 一句理由；有 UI 不得只看代码/测试/API 200。
- 证据、分级、矩阵、截图/console/network 要求只认该文件，不在本包重复。

## 6. 技能指向（打开 → 执行 → 回本包）

> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `implementation-and-selftest` | **必开** | 进入本步即开（质量不降） | `skills/implementation-and-selftest/SKILL.md` | 必做区 → 回本包 |
| `engineering-quality` | **必开** | 进入本步即开（质量不降） | `skills/engineering-quality/SKILL.md` | 必做区 → 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/solo/_chain.md`。
- 子状态机（进区一次）：`rules/packets/solo/_region-build.md`。
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
route=workflow:solo | step=build | agent=implementer | packet=rules/packets/solo/build.md | reads=rules/packets/solo/build.md[+skill] | skills=implementation-and-selftest,engineering-quality|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/solo/build.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
