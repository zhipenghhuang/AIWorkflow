# 门（测试轨）

> 单一出处：主读门、理解门、计划门、执行门、报告门、提交/平台/交接门，以及 `when` / `gate_when` 词表。
> 步骤顺序以 `../workflows/*.yaml` 为准；只认步上 `when` / `hitl` / `hitl_when` / `gate_when`。
> 读取时机：当前步有门时只读对应行；写/改 YAML 时才读全表。

## 1. 门

| 门 | 步上声明 | 动作 |
| --- | --- | --- |
| 开工门 | `confirm_task_intent`（全局，不依赖 step） | 任何任务开工前先给【需求与意图理解】并等确认；纯只读问答可一句话复述后直接答。确认后不重复；范围/目标变化重新确认。 |
| 主读门 | `select_mainread`（when: `mainread_unspecified`） | 主读路径未确认 → STOP 一问；已点名/唯一正式版已在依据清单写明 → 可续，不重问。 |
| 意图门 | `confirm_intent`（when: `intent_needs_confirm`） | 口令无法唯一确定给谁·做什么·形态，或跨角色外发未对齐 → 先对齐；意图已清跳过。 |
| 交接门 | `confirm_handoff`（when: `handoff_send_required`） | 拟生成 HO/统一导出缺陷 → 出示类型/接收方/摘要/落点；确认后落盘；未确认零发包。 |
| 平台门 | `confirm_platform`（when: `platform_ask_required` / `platform_submit`） | 有拟交平台/新建缺陷单 → STOP；新建单出示 `caseId｜标题｜类型｜surface｜结构/厚度｜附件` 清单并抽一单正文（须见设计对照标记+字段级实际）；`validate_defect_steps` 未过禁进确认；回写走备注门；≠ git；无平台动作跳过。 |
| 备注门 | `confirm_remark`（when: `remark_writeback`） | 拟关/激/解决/标重复/补充澄清/回归写回 → 先列 id+结论+备注全文；确认后执行。 |
| 入库门 | `confirm_gitignore`（when: `gitignore_needed`） | 四选一确认资产范围；规范包默认不跟踪，写已装包行与运行态 `.gate/`；接入时一次。 |
| 技能变更门 | `confirm_skill_changes`（when: `skill_changes_pending`） | 出示拟变更清单；确认后才改；未确认零改动。 |
| 材料库闸 | `gate: materials-validate` | README/INDEX 齐；文件有登记；来源可解析；无草稿/证据/密钥/PII；不通过不称完整。 |
| 理解门 | `confirm_understanding`（when: `understanding_needs_confirm`） | **主屏**：分析 §0 摘要、来源盘点计数（含 UI/文案类）、AC/设计点/UI/文案覆盖、关键歧义/冲突、P0 意图与 Oracle；确认后才写计划。 |
| 计划门 | `confirm_plan`（when: `plan_needs_confirm`） | 版本级首版/换代，或范围/准出/缺陷策略实质变更 → STOP 一行摘要：分析计数、P0/P1/P2、N/A、待确认、准出、**批次形态**（如「N 模块·模块子代理·串行/PG-xx」）+ **数据前置**（造数项数/无造数依据）。**待确认只列需用户裁决的范围/准出/接受人**；造数/建号/开通/专项方案编制属执行期自助（`rules/defects/classification.md` §0.4），不得挂待确认。同会话同载体只一次；补丁/单模块、无新增功能面轻量可不设门。 |
| 执行门 | `confirm_execution_scope`（when: `scope_needs_confirm`） | 开跑前一行：计划范围/环境/构建/轮次 → 确认；计划已确认 → 跳过并附【已预授权执行：按计划】。 |
| git 提交门 | `confirm_commit` | 【拟提交·仓库】；默认仅本地提交，推送须点名并单独确认；≠ 收尾摘要；≠ 平台门。 |
| 迁移/资料门 | `confirm_docs_migration`（when: `docs_migration_needed`） | 资料收取/分类/改名/归档、或结构迁移前列清单与目标；确认后执行。 |
| 迭代关闭门 | `confirm_iteration_close`（when: `iteration_close_needed`） | 出示当前迭代、未完成项、拟归档摘要、下一迭代；确认后关账；可「并行不关」。 |
| 覆盖闸 | `gate: coverage-map`（when: `analysis_coverage_required`） | 分析与计划完成后跑 `-Mode coverage`：§2.1 具体 INT 台账+可观测 Oracle；**账本非空且 §1.1 计数被账本行数支撑**；设计点只映射台账，矩阵/细节维 INT 回指台账；来源/章节/依据/覆盖矩阵/方法矩阵/细节维/影响面/核心链路/§4/§5.2/§6 齐；计划 §0 计数/版本准出/准出口径/批次意图范围与分析联动；**§2.2 有造数项时 §3.1 须有数据准备批**；**§2 接口/探索/发布前 纳入=是须有 §3.1 批次**。未 PASS 不得称分析完整/计划可执行/开跑。 |
| 执行批末闸 | `gate: execute-batch`（when: `module_batch_complete`） | 本批意图终态齐后跑 `-Mode execute -Scope "{模块/域}"`：**硬判**环境/分析/计划结构 + 计划状态/联动 + **记录批次 ID ∈ 计划 §3.1 且该批意图跑齐** + 本批记录/证据/阻塞理由/**失败/待实现行失败详情块（含 surface；surface=ui 的失败须截图）**/**§0 分析索引 + 每场景实际/差异（三步序方法在步骤卡/技能）**/**§0 原文/对照与对账计数**/**§1.1 六类（接口 §2.1 适用维）有 SC/N/A+依据；UI/视觉禁弱 N/A（API 主断言/脚本/契约充数）**/INT∈§2.1 台账/**优先级取分析仅作 P0 记账**/**§3 结论回指场景**/意图终态/P0 证伪；原文锚点+可观测 Oracle。实现≠方案的偏差分型与证据在记录「实际/差异」（classification §0.5）。过程不完整 → FAIL/BLOCKED（禁下批）。过程完整且仅产品失败/P0 红 → CONDITIONAL（exit 0，可下批继续找缺陷，须入库）。PASS=本批过程与产品均干净。 |
| 报告闸 | `gate: report-consistency` | 报告正文完成后、宣称准出前跑 `-Mode report`：分析/记录/报告/**全部处置=测意图须有实际场景**/P0/证伪/缺口对账；**计划纳入轨道须有对应记录（功能/接口/探索/发布前）**；§2.2 通过/失败/阻塞/待实现与记录一致；§2.3 细节维计数对分析、原文对账未关>0 不得 PASS；CONDITIONAL 认 §4 接受人行；未 PASS/CONDITIONAL 不得写整体通过。 |
| 回写闸 | `gate: writeback-receipt` | 提交/回写前跑 `-Mode writeback`：有单号/备注/状态/附件回执；新建单另查来源/surface/`结构`/`厚度`（厚度未过→FAIL）；回归写回另查范围卡（构建/范围/冒烟/影响面/未覆盖；未跑须接受人）；只写 `writeback.json`，不覆盖 report。 |

## 2. `when` / `gate_when` 词表

**求值卡（硬）**：外部事实优先；模型自评不确定 → 按触发（真）；不得用「先问用户」代替 when 求值。`when` 假 → 跳过整步；`hitl_when` / `hitl[].when` 假 → 只跳过该门；`gate_when` 假 → 只跳过该闸、步骤继续。跳过须在收尾写 `skip=` / `when_eval=`。

| token | 为真 | 为假 |
| --- | --- | --- |
| `mainread_unspecified` | plan/探索 execute 主读未确认 | 已选定/唯一正式版已写明 |
| `understanding_needs_confirm` | 输入含 PRD/方案/原型/接口，存在 2 个以上实质歧义/冲突，T2/T3，或用户要求计划/准出且未确认分析 | 同一范围分析已确认；纯查询/机械低风险；T0 范围已钉 |
| `plan_needs_confirm` | 版本级首版/换代，或范围/准出/缺陷策略实质变化 | 同会话已确认且未实质变；补丁/单模块、无新增功能面轻量 |
| `scope_needs_confirm` | 非计划驱动、计划 §0 非已确认/执行中/待关闭，或范围/环境实质变化 | 计划驱动且 §0 已确认/执行中/待关闭 |
| `analysis_coverage_required` | 本轮创建/更新分析或计划 | 纯只读/无分析/计划变更 |
| `module_batch_complete` | 本批计划内意图已执行完、执行记录终态齐（无未执行）、失败/阻塞有证据；P0 失败须有缺陷/解释（非「零红灯才推进」） | 未跑完/记录未齐/证据缺 |
| `platform_ask_required` | 本轮有拟交平台/新建缺陷单待确认（不含回写） | 无平台动作 |
| `platform_submit` | 拟新建缺陷单/交平台（含：发现即提交预授权｜批末/阶段末/收尾确认｜用户口令提交到平台；见 collaboration §6.1） | 无新建/交平台 |
| `has_pending_commit` | 有文件变更待提交（git；≠平台门） | 无待提交 |
| `docs_migration_needed` | 本步将搬迁/归档/清理 inbound 或工作文档且未确认清单 | 已确认/无搬迁 |
| `iteration_close_needed` | 探测到下一期/换主题/版本升级且是否关本期不明确 | 已确认结束或明确并行不关 |
| `intent_needs_confirm` | 口令无法唯一确定给谁·做什么·形态，或跨角色外发未对齐，或新开对外交付 | 查询/机械/已确认回归/同任务已确认/意图已写死 |
| `handoff_send_required` | 拟生成/点名 HO，或拟落盘缺陷统一导出且未确认 | 用户已确认该摘要未变；本轮未点名导出 |
| `defect_submit_required` | 子类为提交/修改/回归写回/补充澄清/产品回流/新建单 | 列表/仅查重展示/只读巡检/无需回写 |
| `skill_changes_pending` | skill-audit 出具拟改且用户未确认 | 无拟变更或已确认/拒绝 |
| `gitignore_needed` | 接入/首次入库且资产范围未确认 | 已确认/无需入库 |
| `remark_writeback` | 拟关/激/解决/标重复/补充澄清/回归写回 | 无写回动作 |

`gate_when` 声明子集：`analysis_coverage_required`｜`module_batch_complete`。

**`analysis_coverage_required` 展开**：本轮 `test-analysis.md` 或 `test-plan.md` 新建/更新 → 真；纯只读、无分析/计划变更 → 假。覆盖闸检查分析来源/意图/风险/AC 设计点与计划结构。

**`module_batch_complete` 展开**：本批意图均有终态；失败/阻塞/待实现有证据或明确原因；执行记录与计划 §0/§6 已同步；分析/计划已能过结构闸（§2.1 台账完整，INT 可链）。不是「整个模块/全仓跑完」。产品 P0 失败在过程完整时可 CONDITIONAL 下批；分析残缺/链接断/证据缺 → 不得推进。

## 3. 门档位（防过度审批）

| 档 | 适用 | 行为 |
| --- | --- | --- |
| autonomous | 只读、列表/巡检、已脚本化回归、低风险执行 | 直接做，收尾记录变化/假设 |
| notify | 同范围执行、A/B 类变更 | 展示范围/计划/环境后继续，用户可打断 |
| approve | 计划实质变更、首次执行未确认范围、平台建单/回写、提交、资料搬迁/清理、交接包发送、skills/capabilities 拟变更 | 停：计划门、执行门、平台门、备注门、迁移门、交接门、技能变更门 |

## 4. T 档推导（按事实）

- **T0**：补丁/单模块、不承担版本准出、无新增功能面。
- **T1**：单模块新增/变更，且本轮单独出准出结论。
- **T2**：版本级/多模块/发布列车。
- **T3**：权限/资金/不可逆/合规，或需跨版本回归。

两条都能解释时取高一档；`route` 的 `level=` 给事实依据。档位只决定门与深度，不替代用户判定。
