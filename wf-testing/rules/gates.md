# 门（测试轨）

> 单一出处：计划门、门1～3、迁移/资料门、`when`/`gate_when` 词表。步骤顺序以 `../workflows/*.yaml` 为准；**只认步上 `when` / `hitl` / `hitl_when` / `gate_when`**，专规不另造门。
> 读取时机：当前步有门时只读词表对应行；写/改 YAML 时才读全表。

## 1. 门

| 门 | 步上声明 | 动作 |
| --- | --- | --- |
| 门1 | `select_mainread`（when: `mainread_unspecified` 等，见 §2） | 主读路径未确认 → STOP 一问；已选定或唯一正式版已在 §0/理解门写明待确认 → 可续；不得重问 |
| 任务开工门 | `confirm_task_intent`（全局，不依赖 step） | 任何任务开工前先输出【需求与意图理解】并等用户确认；未确认不得写/执行/对外/下结论；纯只读问答可一句话复述后直接回答。确认后进入 execute，不重复问；范围/AC/目标变化重新确认。细则 `execution-contract.md` §1.0。 |
| 意图门 | `confirm_intent`（when: `intent_needs_confirm`） | 仅歧义/外发未对齐/新开交付时出示【意图理解】并停等；意图已清跳过（可一行回执即做）。细则 `clarification.md` §0。≠ 理解门；≠ 交接门 |
| 理解门 | `confirm_understanding`（when: `understanding_needs_confirm`） | **主屏**：测试分析表 §0【业务与变更简报】+【本期差量表】+ 冲突/九类歧义/GAP 计数与 oracle 要点；无 §0 不过门（T0 迷你差量除外）。确认后才写计划/用例/断言 |
| 计划门 | `confirm_plan`（when: `plan_needs_confirm`） | 版本级首版/换代或范围·准出·缺陷提交策略实质变更 → STOP 一行摘要确认；同会话同载体只一次；专项轻量不设门。版本级须先过：分析表 §2.2/§2.3 无空格 + §2.4 依据覆盖无缺行 + §3.8 四卷 + §3.9 批次表；缺项=计划门不通过 |
| 门2 | `confirm_execution_scope`（when: `scope_needs_confirm`） | 开跑前一行：主读/计划范围/环境 → 确认；同会话同载体只一次；计划驱动已确认 → 跳过并附【已预授权执行：按计划】 |
| 门3 | `confirm_platform`（when: `standalone_generate_with_pending` / `platform_ask_required` / `platform_submit`） | 有拟入库、须问交平台/新建缺陷单 → STOP（交平台用专用确认句）；**回写走备注门**；**≠** git；否则跳过 |
| git提交 | `confirm_commit` | 【拟提交·仓库】（见 `workflow.md` §4.1；≡ 产品/开发 `confirm_commit`）；**默认仅本地提交**，推送须点名并单独确认；≠收尾第 2 点「待提交摘要」；≠门3 |
| 迁移/资料门 | `confirm_docs_migration`（when: `docs_migration_needed`） | 资料收取/分类/改名/归档、或旧结构迁移前列清单与目标；确认后执行 |
| 备注门 | `confirm_remark`（when: `remark_writeback`） | 拟关/激/解决/标重复/补充澄清/回归写回 → 先列 id+结论+备注全文；确认后执行 |
| 入库门 | `confirm_gitignore` | 四选一确认资产范围；规范包默认不跟踪，只写已装包一行（多包 `/wf/`），无注释、不预列未装包；其它项只列路径；写基线入库节；接入时一次 |
| 技能变更门 | `confirm_skill_changes`（when: `skill_changes_pending`） | 出示【拟变更清单】（改 `skills/`·`capabilities/`·装配项）；确认后才改本包或给安装步骤；未确认零改动 |
| 迭代关闭门 | `confirm_iteration_close`（when: `iteration_close_needed`） | 出示当前迭代标识、未完成项、拟归档摘要、下一迭代标识；确认后按 `rules/doc-governance.md` §7.1 关账；选「并行不关」则只落新资料。**关闭=停止新范围/冻结版本线，不停止测试与缺陷修复**；测试未完又要开新迭代，优先「并行不关」，归档待测试完成 |
| 交接门 | `confirm_handoff`（when: `handoff_send_required`） | **凡拟生成任一 HO 或缺陷统一导出必停**：出示类型/接收方/必带摘要/落点（缺陷须写清「本批一份单文件或单 EXPORT 目录」）/阻断/传递方式；用户确认后才落盘；未确认零发包。禁止用「报告门/计划门/批末/平台已交」代替本门。有平台交缺陷 → 本门不因「补导出」置真。未收回执不得称「已接收」；可称「已发送」 |
| 覆盖闸 | `gate: coverage-map`（when: `functional_coverage_required`） | 功能全量/专项新生成/补生成：运行 `verify/Invoke-Gate.ps1 -Mode coverage`；§3 映射无空行且 ID 真实；§4 须含深度档自检与视觉基础行；分析表 §2.2/§2.3 无空格、§2.4 依据覆盖无缺行；不适用于其它轨 |
| 用例评审闸 | `gate: case-review`（when: `case_review_required`） | 功能全量/专项 T1+ **且用户选 B**（或点名机检）：运行 `verify/Invoke-Gate.ps1 -Mode review`；选 A 不跑本闸（仍须 HUMAN_APPROVED 记录）。只认 `{workroot}/reviews/` 现行（优先 INDEX）；结论可解析、独立性声明、阻断未清不得放行；回执 `.gate/wf-testing/review.json`；未 PASS 不得写「放行执行/评审通过」 |
| 评审方式门 | `select_review_mode`（when: `landing_doc_review_needed`） | **STOP 二选一**：A 自行｜B AI（testcase-reviewer）；可附自定义焦点。适用面见 `landing_doc_review_needed`（计划/分析表/功能/接口/发布前/探索式）。同产物只问一次；未选不得宣称评审通过/计划可驱动/进 P2 |
| 评审确认门 | `confirm_review`（when: `review_needs_confirm`） | 结论=需修后放行、有条件放行须接受人、或与计划 P2 入口冲突 → STOP；已放行且无未接受重要项 → 跳过 |
| 执行批末闸 | `gate: execute-batch`（when: `module_batch_complete`） | **每批一次**（不是阶段末一次合成）：本批终态齐后 `Invoke-Gate.ps1 -Mode execute -Scope "{模块}"`；只对 Scope 内台账；回执含 `scope`；禁无 Scope 全仓当本批结论。批次合并按计划 §3.9：文件在、逐条落盘、计数一致、结果合法、证据可打开；未过不得开下一批 |
| 报告闸 | `gate: report-consistency` | 报告正文完成后、宣称准出前运行 `verify/Invoke-Gate.ps1 -Mode report`；**全仓**对账；未 PASS/CONDITIONAL 不得写整体通过；回执 `.gate/wf-testing/report.json` |
| 回写闸 | `gate: writeback-receipt`（when: `remark_writeback`） | 交平台/回写前运行 `verify/Invoke-Gate.ps1 -Mode writeback`；无回执/备注状态不同轮/附件未回查 → BLOCKED；只写 `writeback.json`，不覆盖 report |
| `gate: materials-validate` | 材料库发布校验 | **checklist**：README/INDEX 齐；所有文件有登记；来源可解析；无草稿/证据/密钥/PII；链接自包含；旧版本状态正确；不通过不称完整。 |
| 回写模式 | `verify/Invoke-Gate.ps1 -Mode writeback` | 同上（gate 与命令的单一出处）；未过不得声称已回写 |

> `confirm_task_intent` 是全局开工门（`AGENTS.md` §0 第一问），不依赖 step；其余门仍只认步上声明。

> **`gate_type`**：`machine`=有脚本回执（读 `.gate/` JSON）；`checklist`=按清单/工具核验并留证据。未标默认 `checklist`；新增 gate 必须写 `gate_type` + 证据来源，禁止空门。  
> **gate 2.2**：`test_gate.py` 对新格式硬检 `analysis-structure`（含 §2.4 依据覆盖）/`plan-structure`/`case-vp`/`case-oracle`/`report-structure`；旧格式默认 `skip`，加 `-Strict` 变 FAIL。

**依据覆盖前置（硬）**：`coverage-map` 前须满足 `rules/core/verification.md` §3.1.1；缺行=P0 阻断。

## 2. `when` / `gate_when` 词表

**求值卡（硬）**：外部事实优先；模型自评不确定 → **按触发（真）**；不得用「先问用户」代替 when 求值（路径/档位不确定才先问，见 AGENTS）。`when` 假 → 跳过整步；`hitl_when` / `hitl[].when` 假 → 只跳过该门；`gate_when` 假 → 只跳过该闸、步骤继续。跳过须在收尾写 `skip=` / `when_eval=`。

| token | 为真 | 为假 |
| --- | --- | --- |
| `mainread_unspecified` | analyze/plan/generate/探索 execute 主读路径未确认 | 已选定，或唯一正式版已在 §0/理解门写明待确认 |
| `mainread_unspecified_for_generate` | 同 `mainread_unspecified`，仅挂在 generate 步 | 同左假；与上词同语义，优先用本步声明的那个 |
| `exploratory_mainread_missing` | 探索式 execute 且主读/章程路径未确认 | 已确认或非探索轨 |
| `intent_needs_confirm` | 口令无法唯一确定给谁·做什么·形态，或跨角色外发未对齐，或新开对外交付 | 查询/机械/已确认回归/同任务已确认/意图已写死/任务内续跑；拿不准按真 |
| `understanding_needs_confirm` | 见下「展开」 | 见下「展开」 |
| `plan_needs_confirm` | 版本级首版/换代，或范围·准出·缺陷策略实质变更 | 同会话已确认且未实质变；专项轻量不设门 |
| `scope_needs_confirm` | 见下「展开」 | 见下「展开」 |
| `standalone_generate_with_pending` | 独立生成且有拟入库/待交平台确认 | 同会话续 execute |
| `platform_ask_required` | 本轮有拟交平台/新建缺陷单待确认（**不含回写**；回写只认 `remark_writeback`） | 与 git 无关；无平台动作 |
| `has_pending_commit` | 有文件变更待提交（git；≠门3） | 无待提交变更 |
| `remark_writeback` | 拟关/激/解决/标重复/补充澄清/回归写回 | 无写回动作 |
| `platform_submit` | 拟新建缺陷单/交平台 | 无新建/交平台 |
| `defect_submit_required` | 子类为提交/修改/回归写回/补充澄清/产品回流/新建单 | 列表/仅查重展示/只读巡检/无需回写 |
| `docs_migration_needed` | 本步将搬迁/归档/清理 inbound 或工作文档且尚未确认清单 | 已确认本轮迁移清单后置假；无搬迁 |
| `handoff_send_required` | 拟生成/点名 HO，或拟落盘缺陷统一导出且尚未确认类型/接收方/摘要/落点 | 用户已确认该摘要未变；本轮缺陷走 api/browser 且未点名导出 |
| `landing_doc_review_needed` | 见下「展开」 | 见下「展开」 |
| `review_needs_confirm` | 见下「展开」 | 见下「展开」 |
| `skill_changes_pending` | skill-audit 出具拟改且用户未确认 | 无拟变更或已确认/拒绝 |
| `iteration_close_needed` | 探测到下一期/换主题/版本升级且是否关本期不明确 | 已确认结束或明确并行不关 |

`gate_when` 声明子集：`functional_coverage_required`｜`case_review_required`｜`module_batch_complete`｜`remark_writeback`。不满足 → 跳过对应 gate，步骤不跳过。

`functional_coverage_required`：功能全量/专项新生成，或本轮新增/变更功能用例 → 真；纯接口/发布前/探索式、仅回归重跑 → 假（按各轨覆盖门）。

`module_batch_complete`：本批计划内步骤已执行完、本批台账终态齐（无「未执行」）、证据可打开，且达到 `rules/templates/10-planning/test-plan-template.md` §3.9 的批次合并条件；不是「整个模块/全仓跑完」。判定以当前 `execute` 批与台账 Scope 为准。

`landing_doc_review_needed`：下列任一待审且本会话该产物尚未选定 A/B → 真：**计划**（T1+ 首版/换代/范围·准出·缺陷策略实质变；**T0/普通 T1 轻量且用户未点名 → 假**）、**测试分析表**（T2/T3 或歧义≥2）、**功能/专项用例**（T1+）、**接口资产**（T1+ 生成或计划驱动/进准出）、**发布前**（T2+ 或发版准出/计划已列）、**探索式**（计划 §12 纳入且 T2+，或报告引用进准出）。用户点名「自行通过/我审」→ A 后置假；「AI 评审」→ B 后置假；T0 可 SELF_CHECKED。

`case_review_required`：功能全量/专项且 T1/T2/T3 **且用户选 B**，或点名机检 → 真；选 A、T0 → 假（仍须 HUMAN_APPROVED）。接口/发布前/探索式：机器门可不跑，但 **A/B 或 HUMAN_APPROVED 评审记录不可省**（见多轨质量标准 §4）。

`review_needs_confirm`：评审结论为需修后放行、有条件放行（重要遗留需接受人）、或计划 §9.2 P2 要求评审通过但记录未放行时为真；结论=放行执行且无未接受重要项时为假。

`scope_needs_confirm`：非计划驱动、计划状态非「已确认/执行中/待关闭」或范围/环境实质变化时为真；计划驱动且 §0 为已确认/执行中/待关闭时为假。期中变更 A/B 并入后保持已确认→假；C 变更中→真（计划门）。

`understanding_needs_confirm`：输入含 PRD/迭代方案/原型/接口或技术文档、存在 2 个以上实质歧义/冲突、T2/T3，或用户要求计划/用例/准出时真；已有**本轮当前范围**确认的需求理解包/测试分析表或纯信息查询/机械低风险操作时假。**T0 且范围已钉**（补丁范围/环境/准出口径本轮已写死或计划 §0 已确认）→ **默认假**。**计划驱动 execute**：`{workroot}/test-plan.md` §0 为已确认/执行中/待关闭，且本轮范围测试分析表可打开（或计划声明不适用+依据）→ **假**（不重复理解门；门2 仍按 `scope_needs_confirm`）。缺理解包却要**宣称功能准出** → **仍真**。

同一会话同一确认点只问一次；inbound/迁移/清理清单确认后本轮不再重复（`docs_migration_needed` 置假）。

**T 档推导（按事实，不靠自评）**：T0 补丁/单模块且不承担版本准出、无新增功能面；T1 单模块新增或变更，且本轮单独出准出结论；T2 版本级/多模块/发布列车；T3 高风险（权限/资金/不可逆/合规）或需跨版本回归。两条都能解释时取高一档；`route` 的 `level=` 须给事实依据（模块数、是否承担版本准出、是否新增功能面），不得只写档位。档位只决定门与深度（`case_review_required`/`landing_doc_review_needed` 等），不替代用户判定。

## 3. 门档位（防过度审批）

| 档 | 适用 | 行为 |
| --- | --- | --- |
| autonomous | 只读、列表/巡检、已脚本化回归 | 直接做，收尾记录变化/假设 |
| notify | 同范围生成/执行、A/B 期中变更 | 展示范围/计划/环境后继续，用户可打断 |
| approve | 计划实质变更、首次执行未确认范围、**评审方式选择**、用例需修/有条件放行确认、平台建单/回写、提交、资料搬迁/清理、交接包发送、**skills / capabilities拟变更** | 停：计划门、门2/门3、评审方式门、评审确认门、备注门、迁移门、交接门、技能变更门 |

低风险动作不要升级为 approve；高风险动作不得降为 notify。红线不被“少问/直跑”覆盖。
