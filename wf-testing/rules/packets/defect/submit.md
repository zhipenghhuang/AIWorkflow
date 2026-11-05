# 步骤包 · defect/submit

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-testing
- **workflow**：`defect`
- **step**：`submit`（提交或回写）
- **packet**：`rules/packets/defect/submit.md`
- **条件步** `when=defect_submit_required`：条件不满足则跳过本步（不打开本包）。
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/defect/_chain.md`（进 workflow 一次）。

## 2. 本步目标

- **目标**：提交或回写
- **产出**：平台单号（或待确认后的统一导出路径）· 备注与状态同轮 · 可复制汇总块（collaboration.md §5.2）

## 3. 本步硬约束

### 开局硬约束（本步可执行摘要）

- 1. **先意图、再动作**（`confirm_task_intent`）：未确认禁生成正式用例/交平台。
- 2. **短读跟随 + 一手源**：`activeContext` + 进行中（`packet=`/`region=`）+ 偏好/洞见/坑 ≤3。
- 3. **依据先建模**：分析表 §0；无 §0 禁正式生成与功能准出。
- 4. **状态机读链 + 技能闭环**：见本包「本步读链与防丢失」。必开 skill 须打开→执行→回步骤包（质量不降）。
- 5. **完成分层**：`-Claim -Mode report|writeback` → 只认 `CLAIM: ALLOWED`。
- 6. **UI 证据 E1**：实点 + 截图/Network；E0 不得单独 pass。
- 7. **能脚本不 AI**；禁刷绿；P0 未过不得整体通过。
- 8. **切步/出子机 → 心跳**，必带 `packet=`。

### 本步读链与防丢失

- **编排**：本文 §5 +（若 §7 列出）一个模板。
- **方法质量**：§6 必开/条件开技能 → **打开→执行→回本包**（同时 1 个 skill）；禁止用粘贴代替实读。
- **禁止**：通读 rules / 多 step packet / 预读本 workflow 全部 skill。
- **完成声称**：有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **上下文锚**：`packet=`/`reads=` 必须含本 packet；切步/出子机前心跳刷新。


## 4. 本步门

- **HITL `confirm_remark`**：拟关/激/解决/标重复/补充澄清/回归写回 → 先列 id+结论+备注全文；确认后执行
- **HITL `confirm_platform`**：有拟入库、须问交平台/新建缺陷单/回写 → STOP（交平台用专用确认句）；**≠** git；否则跳过
- **GATE `writeback-receipt` when=remark_writeback**：运行对应 verify；未过不得宣称完成。

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- remark_writeback＝拟关/激/解决/标重复/补充澄清/回归写回备注。
- 先出 id+备注全文再执行。 platform_submit＝计划 为批末/阶段末/收尾确认且本轮拟新建单时触发。
- 执行批 ID 与计划 对齐。
- 修复批可另立 `B-FIX-xx` 并在计划 登记。
- 细则见 `rules/defects/collaboration.md` /（分流：本地消化/盯办/缺陷。
- 待实现进缺陷清单。
- 测本地消化不开单。
- 外力盯办须实机类型+指派匹配或问用户）。 补充澄清用。
- 回归未通过用。
- 新问题用。
- 非修复处置用。
- 产品判定回流用。
- 写后按 回查。 产品缺陷：提交后直接指派产品负责人，不经开发。
- 产品判定非问题/重复/信息不足 → 指派回测试，按 / 处理。 建单标题：`[V版本?][测试类型]`+正文（已确认迭代版本才加 `[V…]`。
- 类型必加。
- ）。 列表/仅查重展示/仅建单（无状态回写）→ 跳过 remark 门。
- 拟新建单仍按 platform_submit 门。
- 列表子类可跳过本步直 wrap。 回写内容由编排集中生成。
- 子代理只提供事实素材，不写平台、不改状态。 **缺陷通道（）**：`api`/`browser`/「提交禅道|平台」→ **完整交平台即完成**（writeback 回执 + 台账单号）。
- **禁止**同轮导出包、BUG HO、出站实拷详单、一缺陷一目录。 无平台/`export`/点名「缺陷交接包|发给开发|仅导出」→ **先问后发**：出示【拟统一导出】（条数/单文件或单 EXPORT 目录）。
- 确认后本批**只落一份**（见 handoff。
- 禁「拟提交」充数。
- 禁逐条文件夹）。 基线 不全 → 先问补适配直提 vs 统一导出。
- 确认前零落盘。 更新台账/计划平台号。
- 仅导出路径才更新 `handoff-ledger.md`。
- 未回执不得写“开发/产品已接收”。

## 6. 技能指向（打开 → 执行 → 回本包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/defect/_chain.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 验证：`verify/Invoke-Gate.ps1`（完成声称加 `-Claim`）；有 UI 另按 §5 前端硬门。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:defect | step=submit | packet=rules/packets/defect/submit.md | reads=rules/packets/defect/submit.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/defect/submit.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
