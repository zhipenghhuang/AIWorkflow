# 步骤包 · plan/publish

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：产品
- **workflow**：`plan`
- **step**：`publish`（落盘与索引）
- **packet**：`rules/packets/plan/publish.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/plan/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/plan/_region-publish.md`（发布下一步；进本区一次）。

## 2. 本步目标

- **目标**：落盘与索引
- **产出**：{workroot}/product-plan.md（模板 rules/templates/10-planning/product-plan-template.md）

## 3. 本步硬约束

### 开局硬约束（本步可执行摘要）

- 1. **先意图、再动作**（`confirm_task_intent`）：未确认禁写正式 PRD/外发/定范围。
- 2. **短读跟随 + 一手源**：`activeContext` + 进行中（`packet=`/`region=`）+ 偏好/洞见/坑 ≤3。
- 3. **理解→方案双确认未完成 → 不得入池/写正式 PRD/定版本范围**。
- 4. **状态机读链 + 技能闭环**：见本包「本步读链与防丢失」。必开 skill 须打开→执行→回步骤包（质量不降）。
- 5. **完成分层**：`-Claim -Mode <…>` → 只认 `CLAIM: ALLOWED`。
- 6. **原型硬门**：实走 + 覆盖矩阵；缺行不得过。
- 7. **禁臆造**；AC 可观测；变更无单不实施；UAT 未过不发布。
- 8. **切步/出子机 → 心跳**，必带 `packet=`。

### 本步读链与防丢失

- **编排**：本文 §5 +（若 §7 列出）一个模板。
- **方法质量**：§6 必开/条件开技能 → **打开→执行→回本包**（同时 1 个 skill）；禁止用粘贴代替实读。
- **禁止**：通读 rules / 多 step packet / 预读本 workflow 全部 skill。
- **完成声称**：有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **上下文锚**：`packet=`/`reads=` 必须含本 packet；切步/出子机前心跳刷新。


## 4. 本步门

- **HITL `confirm_iteration_close`**：出示当前迭代标识、未完成项、拟归档摘要、下一迭代标识；确认后按 `rules/doc-governance.md` §7.1 关账；选「并行不关」则只落新资料。**关闭=停止新范围/冻结版本线，不停止测试与缺陷修复**；测试未完又要开新迭代，优先「并行不关」，归档待测试完成
- **HITL `confirm_docs_migration`**：出示分类/覆盖对照/拟归档或清理清单与目标；确认后执行；不擅自删、不覆盖

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 须已完成 review-plan 选模式（或本轮跳过条件满足）。核对 Brief+差量表已落盘（或独立迭代变更摘要已互指）。总控表状态回写（阶段 / 产物 / 门 / 状态 / 下一动作）。
- 版本索引挂 PRD / 迭代方案（多需求版本）/ 评审 / 受理/变更 / 交付计划 / UAT / GTM / 原型 / 复盘 / 迭代变更摘要（若独立文件）。 多需求/多功能版本：在版本目录落 `迭代方案-{ver}.md`（模板 `rules/templates/10-planning/iteration-plan-template.md`），汇总范围、功能覆盖、验收矩阵、执行记录与发布条件。
- 单需求可只用 PRD，不强制另立。 更新 `{workroot}/work-log.md`（仅本文件）：索引表新增一行 + 一条里程碑条目，事件类型=`计划确认`（结论/产出/遗留。
- 关联产品计划路径）。
- 无文件则先按工作日志模板创建再写。 **不是**根 `CHANGELOG.md`、也不是产品计划 执行日志（细粒度过程仍只写 ）。 **禁止**创建/修改/补链项目根 `CHANGELOG.md`。
- 无开发包则不建根。 **主档不移动**：`{workroot}/product-plan.md` 常青。
- 季度结束复制当期执行到 `{workroot}/_archive/{yyyy-Qn}/产品计划-{yyyy-Qn}.md`，主档保留历史索引并重置当前季度。
- 版本/结项把当期目录整体移入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`（点名执行）。
- 先判 T1/T2/T4，T2/T4 增量迭代保留仍被引用的 PRD/原型基线，不整夹归档。 版本/结项归档时按 `rules/doc-governance.md` 扫描。
- 先判 T1/T2/T4，T2/T4 保留仍被引用的 PRD/原型基线。
- 失效资料进 `inbound/_archive/{ver}/` + 归档清单。
- 部分/增量/参考不动。
- 未确认不移动。 同步按 `rules/doc-governance.md` ～（仅本步关版本/结项时，非日常收尾）：长期主档就地更新、版本绑定目录关闭时归档、已完结临时/失败/重复列清理候选。
- 确认后执行。 **换代/新版本主题（即使不结项发版）** → 按。
- 不确定则 `confirm_iteration_close`。
- 确认后先判 T1/T2/T4，再按 关账（T2/T4 保留仍被引用的 PRD/原型基线。
- 跳过仅发版项）。 建/更新 `{workroot}/handoff/handoff-ledger.md`（模板 `rules/templates/90-handoff/handoff-ledger-template.md`）。
- 按模板登记计划/PRD/设计/变更/UAT/发布节点。
- 变更分级与重规划触发写入计划执行日志/变更记录。 稳定真值（愿景/用户/北极星/指标口径）留在主档与 `product-profile.md`，不随季度归档。

## 6. 技能指向（打开 → 执行 → 回本包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/plan/_chain.md`。
- 子状态机（进区一次）：`rules/packets/plan/_region-publish.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:plan | step=publish | packet=rules/packets/plan/publish.md | reads=rules/packets/plan/publish.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/plan/publish.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
