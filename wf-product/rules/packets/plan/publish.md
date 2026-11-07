# 步骤卡 · plan/publish

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（本会话已读则不重读全文）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`plan` / `publish`（落盘与索引）
- **packet**：`rules/packets/plan/publish.md`
- **角色**：`pm-lead`（交付编排与变更处置（排期/跟进/受理/变更/缺陷平台/UAT/发布/复盘/展示））。统一受理需求与问题 → 分诊定性 → 影响评估 → 处置确认 → 联动更新 → 验证关闭；平台缺陷可拉取、分析并回写；本步只做该角色职责；越界交回或升级。
- **上游**：`review-plan`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`next`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：落盘与索引
- **产出**：{workroot}/product-plan.md（模板 rules/templates/10-planning/product-plan-template.md）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：本会话已读 `rules/core/global-rules.md` 则不重读全文；未读过不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_iteration_close`**：出示当前迭代标识、未完成项、拟归档摘要、下一迭代标识；确认后按 文档治理（工作根/原件根/索引/关版整夹） 关账；选「并行不关」则只落新资料。**关闭=停止新范围/冻结版本线，不停止测试与缺陷修复**；测试未完又要开新迭代，优先「并行不关」，归档待测试完成
- **条件判定 `hitl:iteration_close_needed`**：探测到下一期/换主题/升级且是否关本期不明；满足→真，否则跳过该门。
- **HITL `confirm_docs_migration`**：出示分类/覆盖对照/拟归档或清理清单与目标；确认后执行；不擅自删、不覆盖
- **条件判定 `hitl:docs_migration_needed`**：有未登记资料、拟改名/搬迁/归档、工作文档清理或旧结构迁移；满足→真，否则跳过该门。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 须已完成 review-plan 选模式（或本轮跳过条件满足）。
- 核对 Brief+差量表已落盘（或独立迭代变更摘要已互指）。
- 总控表状态回写（阶段 产物 门 状态 下一动作）。
- 版本索引挂 PRD 迭代方案（多需求版本）/ 评审 受理/变更 交付计划 UAT GTM 原型 复盘 迭代变更摘要（若独立文件）。
- 多需求/多功能版本：在版本目录落 `迭代方案-{ver}.md`（模板 `rules/templates/10-planning/iteration-plan-template.md`），汇总范围、功能覆盖、验收矩阵、执行记录与发布条件。
- 单需求可只用 PRD，不强制另立。
- 更新 `{workroot}/work-log.md`（仅本文件）：索引表新增一行 + 一条里程碑条目，事件类型=`计划确认`（结论/产出/遗留；关联产品计划路径）。
- 无文件则先按工作日志模板创建再写。
- **不是**根 `CHANGELOG.md`、也不是产品计划 执行日志（细粒度过程仍只写 ）。
- **禁止**创建/修改/补链项目根 `CHANGELOG.md`。
- 无开发包则不建根。
- **主档不移动**：`{workroot}/product-plan.md` 常青。
- 季度结束复制当期执行到 `{workroot}/_archive/{yyyy-Qn}/产品计划-{yyyy-Qn}.md`，主档保留历史索引并重置当前季度。
- 版本/结项把当期目录整体移入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`（点名执行）。
- 先判 T1/T2/T4，T2/T4 增量迭代保留仍被引用的 PRD/原型基线，不整夹归档。
- 版本/结项归档时按 文档治理（工作根/原件根/索引/关版整夹） 扫描。
- 先判 T1/T2/T4，T2/T4 保留仍被引用的 PRD/原型基线。
- 失效资料进 `inbound/_archive/{ver}/` + 归档清单。
- 部分/增量/参考不动。
- 未确认不移动。
- 同步按 文档治理（工作根/原件根/索引/关版整夹） （仅本步关版本/结项时，非日常收尾）：长期主档就地更新、版本绑定目录关闭时归档、已完结临时/失败/重复列清理候选。
- 确认后执行。
- **换代/新版本主题（即使不结项发版）** → 按。
- 不确定则 `confirm_iteration_close`。
- 确认后先判 T1/T2/T4，再按 关账（T2/T4 保留仍被引用的 PRD/原型基线；跳过仅发版项）。
- 建/更新 `{workroot}/handoff/handoff-ledger.md`（模板 `rules/templates/90-handoff/handoff-ledger-template.md`）。
- 按模板登记计划/PRD/设计/变更/UAT/发布节点。
- 变更分级与重规划触发写入计划执行日志/变更记录。
- 稳定真值（愿景/用户/北极星/指标口径）留在主档与 `product-profile.md`，不随季度归档。

### 本步规则卡：文档治理

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认后将迭代绑定文档迁入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`；主档关闭时快照、主档不移动；「并行不关」只落新资料、不归档现行主档。
- 清理只删已知临时/缓存/未引用失败产物；不确定移 `_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/10-planning/product-plan-template.md`；只读本步用到的节，禁止整文件通读。
- **参考模板（命中再开，不默认读）**：`rules/templates/10-planning/iteration-plan-template.md`；`rules/templates/90-handoff/handoff-ledger-template.md`。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:plan | step=publish | agent=pm-lead | packet=rules/packets/plan/publish.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
