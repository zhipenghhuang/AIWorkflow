# 步骤卡 · deliver/release

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（本会话已读则不重读全文）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`deliver` / `release`（发布与复盘）
- **packet**：`rules/packets/deliver/release.md`
- **角色**：`pm-lead`（交付编排与变更处置（排期/跟进/受理/变更/缺陷平台/UAT/发布/复盘/展示））。统一受理需求与问题 → 分诊定性 → 影响评估 → 处置确认 → 联动更新 → 验证关闭；平台缺陷可拉取、分析并回写；本步只做该角色职责；越界交回或升级。
- **上游**：`uat`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`closeout`
- **失败去向**：不发布；回 UAT/审批或报阻塞，不得用“已发布”措辞
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：发布与复盘
- **产出**：发布决策 + 发布记录 + 复盘（{workroot}/{ver}/40-delivery/、90-retrospectives/）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：本会话已读 `rules/core/global-rules.md` 则不重读全文；未读过不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_release`**：出示 UAT 结论、回滚预案、公告/客服/监控就绪；未过不发布；已发布仅复盘不重复确认
- **条件判定 `hitl:release_decision_needed`**：未发布或发布内容/窗口变更；满足→真，否则跳过该门。
- **GATE `uat-evidence` when=has_uat**：运行 `verify/Invoke-Gate.ps1 -Mode uat`；AC 覆盖、证据、有条件通过的责任人/接受人；未 READY 不得写 UAT 通过。无 UAT 要求可写 `verdict: 不适用` + 依据/批准人，门放行但记警告
- **条件判定 `gate:has_uat`**：本轮有 UAT/验收要求（发布门必须核）；满足→真，否则跳过该闸（步骤不跳过）。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`uat-and-retrospective` → 见 §6 闭环。

### 本步动作清单

- 技能见 §6 `uat-and-retrospective`（先读再核）。
- 前置：UAT 通过（带条件须已接受）。
- 发布就绪：回滚预案/公告/客服话术/监控指标（并入 UAT 记录「发布前置」节）。
- 直接入口「发布」时：`has_uat=true` → 必须先运行 `verify/Invoke-Gate.ps1 -Mode uat`（读 `.gate/wf-product/uat.json`），未 READY 不得进入 confirm_release。
- 无 UAT 要求 → 写「不适用+依据」，门条件不满足则跳过，不得伪造回执。
- 发布前可派 verifier-agent 只读核对发布就绪证据（UAT/回滚/公告/监控），返回缺口 ≤30 行。
- 发布决策仍由本步做。
- confirm_release：出示发布要点（版本/时间窗/回滚/通知范围）请确认。
- **未过 UAT 不发布**。
- 已发布且仅做复盘 → 条件不满足，跳过本门。
- 本门是业务发布决策。
- **如启用开发轨**，工程部署由其 `release` 执行（`confirm_deploy`），不重复审批。
- 未启用则由用户安排，本包不执行部署。
- 发布决策后默认交发布决策正文。
- `REL` 包按需先问后发。
- 收到开发发布结果 → 有包则 receive。
- 发布后：数据监控（指标/埋点）→ 复盘（模板 `rules/templates/60-retro/retro-template.md`，落 `{workroot}/{ver}/90-retrospectives/复盘-{ver}.md`：目标 vs 实际/根因/改进项→回需求池）。
- 如启用开发轨，研发复盘可由其补充，产品复盘合并引用。
- 未启用则本包独立复盘。
- 更新 `{workroot}/work-log.md`（仅本文件）：按场景追加里程碑——有发布决策写事件=`发布决策`（结论宜含本版对外变化摘要 1～5 条产品语言或链到发布说明，供开发写根 CHANGELOG）。
- 有 UAT 结论写=`UAT 结论`。
- 有复盘写=`复盘`。
- 无文件则按模板建。
- **不是**根 `CHANGELOG.md`、也不是计划 执行日志。
- 本门=`confirm_release` 业务决策。
- 根发版史由开发在工程发版时写（有开发包时）。
- **禁止**创建/修改/补链项目根 `CHANGELOG.md`。
- 无开发包则不建根。
- 版本关闭/结项：按 文档治理（工作根/原件根/索引/关版整夹）。
- 先判 T1/T2/T4，T2/T4 保留仍被引用的 PRD/原型基线，不整夹归档。
- 失效资料 → `inbound/_archive/` + 清单。
- 部分/增量/参考不归档。
- 未确认不移动。
- 同步按 文档治理（工作根/原件根/索引/关版整夹） （仅本步关版本/结项时，非日常收尾）：先判 T1/T2/T4，T2/T4 保留仍被引用的 PRD/原型基线。
- 长期主档就地更新、版本绑定目录归档、已完结临时/失败/重复列清理候选。
- 确认后执行。

### 本步规则卡：文档治理

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认后将迭代绑定文档迁入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`；主档关闭时快照、主档不移动；「并行不关」只落新资料、不归档现行主档。
- 清理只删已知临时/缓存/未引用失败产物；不确定移 `_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → 读必做，并读现场处置/判定/反合理化（技能有这些节时）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `uat-and-retrospective` | **必开** | 进入本步即开（质量不降） | `skills/uat-and-retrospective/SKILL.md` | 只读 L10-L59（硬门槛+方法+反合理化）→ 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/60-retro/retro-template.md`；只读本步用到的节，禁止整文件通读。
- 验证命令：`verify/Invoke-Gate.ps1`（完成须 `-Claim` → `CLAIM: ALLOWED`）。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步完成 Claim 门：须 `CLAIM: ALLOWED` 后才可写完成态。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:deliver | step=release | agent=pm-lead | packet=rules/packets/deliver/release.md | global=ok | skills=uat-and-retrospective|done|na | claim=ALLOWED|DENIED|na | next=…
```
