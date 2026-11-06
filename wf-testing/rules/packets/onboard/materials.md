# 步骤包 · onboard/materials

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-testing
- **workflow**：`onboard`
- **step**：`materials`（资料收取与归档）
- **packet**：`rules/packets/onboard/materials.md`
- **角色**：`onboard-agent`（测试包接入）。挂载 → 基线关键节 → activeContext → 入库确认 → 环境与工具检查（默认静默） → 按接入清单核验；本步只做该角色职责；越界交回或升级。
- **上游**：`baseline`（取其产出为本步输入；该步被 `when` 跳过时按缺口停/补齐）
- **后续**：`lifecycle`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/onboard/_chain.md`（进 workflow 一次）。

## 2. 本步目标

- **目标**：资料收取与归档
- **产出**：【入站分析】（确认后登记/A0～A2/发布 materials）

## 3. 本步硬约束

### 开局硬门（3 条；其余见 cold-start §1）

- 1. **每轮先判、再动手**：先判新任务/续跑/只读；新任务或范围变化 → 复述目标/范围/验收并确认；续跑一行确认；只读一句话；首行锚 `route/step/packet` 或 `mode=analyze`；未确认禁写、禁下结论。
- 7. **完成只认门**：`-Claim` → `CLAIM: ALLOWED`；无 ALLOWED 禁写完成/通过/可提测。P0 未过不得整体通过；UI 证据 E1 实点+截图/Network。
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

- **HITL `confirm_iteration_close`**：出示当前迭代标识、未完成项、拟归档摘要、下一迭代标识；确认后按 `rules/doc-governance.md` §7.1 关账；选「并行不关」则只落新资料。**关闭=停止新范围/冻结版本线，不停止测试与缺陷修复**；测试未完又要开新迭代，优先「并行不关」，归档待测试完成
- **HITL `confirm_docs_migration`**：资料收取/分类/改名/归档、或旧结构迁移前列清单与目标；确认后执行
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 按 `rules/doc-governance.md` ～ 执行：扫描本包资料根 + 原件根 `inbound/`（环境基线。
- keep/mix）+ 项目根（replace/用户投放）的未登记/变化文件 → 按版本/主题归属分类 → 与同主题旧文件做覆盖对照 （全量替代/全量覆盖/部分覆盖/增量补充/仅新增/重复/冲突）→ 输出【资料收取与归档候选】。
- **此时不改索引、不改名、不移动、不标记失效**。 有未登记/变化文件、拟改名/搬迁/归档候选 → `docs_migration_needed=true`，停在本门等确认。
- 无候选才继续。 按 `rules/doc-governance.md` ～。
- 确认前不改文件。确认后：索引必做 → 按需复制 → 按需 A0～A2 吸收。
- 失效只动包内副本。存量未点名的保持仅索引。对话/根散落须先留主副本于原件根 `inbound/`。 部分覆盖/增量补充/参考/待确认 → 保留原文件，不归档。
- 冲突/无法判断 → 停下问一次。归档前做引用检查：被当前计划/用例/脚本/报告引用的设计输入、测试数据、稳定冒烟清单保留原位或标“基线”，不标失效。 无候选 → 报「无未登记/失效候选」，不改文件。 **换迭代/关版本（强制）**：确认采纳新迭代/换主题后按 `rules/doc-governance.md`。
- 不确定则 `confirm_iteration_close`。
- 确认后先按 判 T1/T2/T4，再按 关账（跳过仅发版项）。
- T2/T4 保留仍被引用的设计输入/测试数据/稳定冒烟清单/脚本，只归档被替代的用例轮次/报告/CR。不依赖关报告。 关账 materials：**必做**覆盖刷新关闭版 `{prev}/`→superseded，再建 `{next}/` current（默认 overwrite-latest）。

## 6. 技能指向（打开 → 执行 → 回本包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/onboard/_chain.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:onboard | step=materials | agent=onboard-agent | packet=rules/packets/onboard/materials.md | reads=rules/packets/onboard/materials.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/onboard/materials.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
