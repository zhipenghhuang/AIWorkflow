# 步骤卡 · defect/submit

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守；重读按 §7 分级）；方法在 §6 指定节（打开→执行→回包）。**未打开本文件=未开跑本步**。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`defect` / `submit`（提交或回写）
- **packet**：`rules/packets/defect/submit.md`
- **角色**：`bug-agent`（缺陷平台协作）。查重/提交/回归/回写按专规；备注与状态同轮；读者=开发/产品；本步只做该角色职责；越界交回或升级。
- **上游**：`search`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`closeout`
- **失败去向**：不提交/不回写；补证据、补探查或问用户；不得为交平台改标失败
- **条件判定 `when:defect_submit_required`**：子类为提交/修改/回归写回/补充澄清/产品回流/新建单；满足→真，否则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：提交或回写
- **产出**：平台单号（或待确认后的统一导出路径）· 备注与状态同轮 · 可复制汇总块（collaboration.md §5.2）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：按 `rules/core/global-rules.md` §7 **分级重读并遵守**（中段=最小集，禁每步通读全文）；须先打开本步骤卡；心跳 `global=ok`=已按 §7 复核且步骤卡已实读；未复核不得写 `global=ok`。偏离写 `global=dev:<原因>`。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_remark`**：拟关/激/解决/标重复/补充澄清/回归写回 → 先列 id+结论+备注全文；确认后执行。
- **条件判定 `hitl:remark_writeback`**：拟关/激/解决/标重复/补充澄清/回归写回；满足→真，否则跳过该门。
- **HITL `confirm_platform`**：有拟交平台/新建缺陷单 → STOP；回写走备注门；≠ git；无平台动作跳过。
- **条件判定 `hitl:platform_submit`**：拟新建缺陷单/交平台（含：发现即提交预授权｜批末/阶段末/收尾确认｜用户口令提交到平台；见 collaboration §6.1）；满足→真，否则跳过该门。
- **GATE `writeback-receipt` when=remark_writeback**：按本包门表该门的检查方法核验并留证据；未过不得宣称完成。
- **条件判定 `gate:remark_writeback`**：拟关/激/解决/标重复/补充澄清/回归写回；满足→真，否则跳过该闸（步骤不跳过）。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- remark_writeback＝拟关/激/解决/标重复/补充澄清/回归写回备注。
- 先出 id+备注全文再执行。
- platform_submit＝拟新建单且命中 collaboration §6.1（发现即提交｜批末/阶段末/收尾确认｜用户口令提交到平台）。
- 执行批 ID 与计划对齐。
- 修复批可另立 `B-FIX-xx` 并在计划登记。
- 细则见 `rules/defects/collaboration.md`。
- **交前复判（硬）**：§5.1 Q15 + §6.0。
- 投影交单禁现网补证。
- 回执优先 functional/*回执*。
- 产品缺陷直提产品。
- 建单标题 `[V?][类型]+正文`。
- 列表/仅查重/仅建单（无状态回写）→ 跳过 remark 门。
- 拟新建仍走 platform_submit。
- **缺陷通道**完整交平台即完成（writeback 回执+台账单号）。
- 禁同轮导出包。
- 未回执不得写“已接收”。

### 本步规则卡：投影交单与回执

- **platform_submit**：发现即提交（计划预授权）｜批末/阶段末/收尾确认｜用户口令提交到平台（`collaboration` §6.1）。
- **投影（硬）**：steps=执行失败详情投影；禁交单窗现网补截图/主键/文案；缺则回 execute 补采。
- **回执**：优先 `functional/*回执*.md`（或 `api/`）；evidence 旁放须文件名含回执/回写；过 writeback 门。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 模板与证据

- **无强制模板**：§5 编排已给出动作/顺序；直接落 §2 产出。
- 验证命令：`verify/Invoke-Gate.ps1`（完成须 `-Claim` → `CLAIM: ALLOWED`）。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步 Claim 门受 `gate_when: remark_writeback` 约束：门执行时须 `CLAIM: ALLOWED` 才可写完成态；门被跳过 → 不产门回执，`claim=na` 并写 `when_eval=<假理由>`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:defect | step=submit | agent=bug-agent | packet=rules/packets/defect/submit.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
