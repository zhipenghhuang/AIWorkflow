# 门（开发轨）

> 单一出处：`hitl` / `gate` / `when` 语义与词表。步骤顺序以 `../workflows/*.yaml` 为准；**只认步上 `hitl`/`hitl_when`/`gate_when`**，专规不另造门。
> 读取时机：当前步有门时只读对应行；写/改 YAML 时才读全表。

## 1. 门与 gate

| 标记 | 含义 | 必须行为 |
| --- | --- | --- |
| `hitl:` | 确认门声明 | 标量（单门）或列表（多门；各项 `name` + 可选 `when`）；未写 `when` 视为无条件 |
| `hitl_when:` | 标量门条件 | 条件不满足 → 跳过该门，不算违例 |
| `gate_when:` | 门禁条件 | 条件不满足 → 跳过该 gate（步骤不跳过） |
| `confirm_change` | 变更吸收/影响 | 出示变更类型/影响矩阵/待更新文档/待确认项；实质变更确认后才更新基线 |
| `confirm_task_intent` | 任务开工需求/意图确认（全局硬门） | 任何任务开工前先输出【需求与意图理解】并等用户确认；未确认不得写/执行/对外/下结论；纯只读问答可一句话复述后直接回答。确认后进入 execute，不重复问；范围/AC/目标变化重新确认。细则 `execution-contract.md` §1.0。 |
| `confirm_intent` | 意图理解（择优·防自作主张） | 仅当 `intent_needs_confirm`：出示【意图理解】，确认后才落盘。意图已清 → 跳过本门（可一行回执即做）。细则 `clarification.md` §0。≠ `confirm_understanding`；≠ `confirm_handoff` |
| `confirm_understanding` | 需求理解 | **主屏**：§0【业务与变更简报】+【本期差量表】（增/改/删）+ 待确认单摘要（冲突·GAP·开发择优/置信度）；完整理解包作下钻链接。无 §0/差量表不得过门（L0 迷你 Delta 除外）。确认后才进需求基线/设计/实施/拆单 |
| `confirm_requirements` | 需求基线/范围 | 出示范围/AC/NFR/非目标/未决；未签收不进设计/排期 |
| `select_review_mode` | 落地文档评审方式 | **STOP 二选一**：A 自行评审通过（HUMAN_APPROVED）｜B AI 独立评审（`doc-reviewer`）；同产物只问一次；未选不得进实施。适用需求基线/方案/ADR/前端设计说明等（见 `skills/design-doc-review`） |
| `confirm_spec` | 方案评审 | 出示范围/接口/兼容与回滚/验收；批准后才实施（可在选模式 + 可选 AI 审之后） |
| `confirm_replan` | C2/C3 重基线 | 出示变更等级/影响矩阵/重基线范围（基线/任务/计划/测试）/里程碑与资源影响；确认后才重基线；禁止拆成 C0/C1 绕过 |
| `confirm_plan` | 开发计划/版本范围 | 首次创建或范围·版本·里程碑实质变更；确认后计划状态=已确认 |
| `confirm_backlog` | 迭代清单与节奏 | 出示任务数/RP 覆盖/依赖/风险 + 节奏三选；确认后才实施 |
| `confirm_commit` | 拟提交/推送 | 【拟提交】块（三包统一：文件+`.gitignore`+分支/跟踪+本次动作；本轨扩展：基线/分账/拆分/落点/CI/PR·合并）；**默认仅本地提交**，推送须单独明确并确认；≠收尾第 2 点「待提交摘要」 |
| `confirm_handoff` | 交接包发送 | **凡拟生成任一 HO 包必停**：出示类型/接收方/必带摘要/阻断/传递方式；用户确认后才落盘；未确认零发包。禁止用「定稿门/评审门/发布门已过」代替本门。未收回执不得称「已接收」；可称「已发送」 |
| `confirm_deploy` | 工程部署审批（生产/正式） | 出示版本/窗口/影响面/回滚决策人；并核 **干净工作区 + 已提交或已打 tag + 本轮 `completion.json=COMPLETE`**；未批准不部署，禁止从脏工作区部署；**仅生产/正式环境**，test/staging 部署不触发本门；生产版本必须无 prerelease |
| `confirm_rollback` | 回滚 | 出示触发信号/步骤/数据影响/预计时长；确认后执行 |
| `confirm_acceptance` | UAT/业务验收 | 出示 AC 覆盖/失败项/遗留风险/发布建议；确认后进审批 |
| `confirm_actions` | 复盘行动项 | 出示行动项/负责人/截止/验收；确认后落盘 |
| `confirm_remark` | 回写前备注 | 出示 §6 备注全文 + 状态/指派/resolvedBuild；确认后状态+备注同轮写入；未验证只写「待验证」 |
| `confirm_gitignore` | 入库策略 | 四选一确认资产范围；规范包默认不跟踪，只写已装包一行（多包 `/wf/`），无注释、不预列未装包；其它项只列路径；写档案 §1 并改 `.gitignore` |
| `confirm_docs_migration` | inbound/工作文档归档、搬迁或临时清理 | 出示分类/覆盖对照/拟归档或清理清单与目标；确认后执行 |
| `confirm_iteration_close` | 结束当前迭代/版本并进入下一 | 出示当前迭代标识、未完成项、拟归档摘要、下一迭代标识；确认「结束当前并进入下一」后才按 `rules/doc-governance.md` §7.1 关账；选「并行不关」则只落新资料不归档现行绑定主档。**关闭=停止新范围/冻结版本线，不停止测试**：测试与缺陷修复可继续（走 patch），归档待测试完成；测试未完又要开新迭代，优先「并行不关」 |
| `confirm_skill_changes` | capabilities/技能体检拟变更 | 出示【拟变更清单】（改 `skills/`·`capabilities/`·装配项）；确认后才改本包或给安装步骤；未确认零改动 |
| `select_menu` | 缺陷批末菜单 | 输出总结+【用户选择菜单】，精确执行选项 |
| `gate: completion-gate` | 完成门（开发轨） | 任务开始 `-StartTask`；运行 `verify/Invoke-Gate.ps1 -Acceptance ...`；写 `.gate/wf-development/completion.json`；**前端套装与 capture 只认 `rules/core/frontend-gate.md`**；**写完成前 `-Claim`，只认 `CLAIM: ALLOWED`**；空 diff=`NOT_VERIFIED`、dry-run=`DRY_RUN`、缺项 → `BLOCKED` |
| `gate: dev-plan` | 开发计划检查 | **checklist**：跑 `rules/tools/validate_dev_plan.py`（可用时）+ 阶段表/门/证据/下一步人工核；缺项不过 |
| `gate: materials-validate` | 材料库发布校验 | **checklist**：README/INDEX 齐；所有文件有登记；来源可解析；无草稿/证据/密钥/PII；链接自包含；旧版本状态正确；不通过不称完整。 |
| `gate: release-readiness` | 生产/正式发布就绪 | **checklist**：按上线检查单逐项核；硬项不过 → NO-GO；test/staging 部署不适用 |

> `confirm_task_intent` 是全局开工门（`AGENTS.md` §0 第一问），不依赖 step；其余门仍只认步上声明。

> **`gate_type`（步上字段）**：`machine` = 有脚本回执（读 `.gate/` JSON，verdict 可机器判定）；`checklist` = 按清单/工具核验并留证据，不假装机器可判。未标默认 `checklist`；`gate` 只表示检查点，不等于自动门。新增 gate 必须同时声明 `gate_type` 与证据来源；禁止只写 `gate:` 而无检查方法。

## 2. 步骤条件 `when` 词表

`c2_or_c3`（本轮变更分级为 C2 范围/里程碑/资源或 C3 战略/架构/合规/破坏性 → 真）｜`has_code_change`（本轮代码/配置 diff 非空，不含生成物 → 真）｜`dev_plan_required`（L2+ 或 `{workroot}/development-plan.md` 已存在 → 真；L0/L1 且无计划 → 假）｜`release_failed_or_direct_rollback`（入口=回滚 或 发布失败/触发回滚条件）｜`new_feature_or_scope_change_or_requested`｜`new_feature_or_architecture_or_breaking_change_or_high_risk_or_requested`｜`multi_file_or_new_feature_or_requested`｜`has_qa_or_deploy_or_requested`｜`has_deploy`｜`has_uat`｜`release_failed`｜`release_ready`｜`release_ready_and_acceptance_passed`｜`release_approved`｜`has_deployed`｜`iteration_done_or_incident`｜`recurring_defect_or_incident`｜`incident_or_major_release`｜`docs_migration_needed`｜`requirements_need_confirm`｜`new_product_or_unclear_idea`（轻量档输入是新想法/新产品/方向不清 → 真）｜`solo_gate_required`（轻量档本轮有方案卡/验收表且已 StartTask → 真；单独测试/纯文档 → 假）｜`intent_needs_confirm`｜`understanding_needs_confirm`｜`has_product_docs_or_prototypes`｜`change_is_substantive`｜`backlog_approval_required`｜`plan_needs_confirm`｜`has_pending_commit`｜`code_changed_or_requested`｜`implementation_required`｜`landing_doc_review_needed`（L2+ 新产出需求基线/方案/ADR/前端设计说明，或点名文档评审，且本会话尚未选定 A/B；L0 无新文档=false）｜`landing_doc_review_required`（L2+ 有新增/变更需求基线、方案、ADR、前端设计说明，或用户点名文档评审；不依赖是否已选 A/B；L0/无新文档=false。用于 review-docs 步自身的 when；模式选择仍用 landing_doc_review_needed）｜`design_needs_spec_approval`（L1 有新方案/ADR/前端设计且未进入 review-docs → 真；L0 或 L2+ 由 review-docs 接管 → 假）｜`review_required`（有实施且 L2+/L3、高风险/大改/破坏性/新功能/点名代码评审 → 真；L0 单文件或确实低风险的 L1 单点 → 假；免审须在计划/验收记录理由与风险接受人，免审不免自测；多波次必须先选“每波审”或“只 S5 全量审”，不得混用）｜`product_defect`｜`product_decision_received`｜`product_decision_requires_alignment`｜`need_clarification`｜`menu_includes_commit`｜`menu_includes_writeback`｜`menu_includes_deploy`｜`not_awaiting_product`（本轮 await_product 或 product_decision 输出 AWAIT_PRODUCT 时为假，否则为真）｜`handoff_send_required`（拟生成或用户点名生成任一 HO 交接包（常用类型为示例，含 OTHER/项目扩展）且本包本会话尚未得到用户对**本次拟发包的类型/接收方/摘要**的确认 → 真；用户已看到【拟发包】并明确确认该摘要未变 → 假；仅说「要/生成/交接包/确认发包」但未确认具体摘要 → 真。**不得**因其它门已过而置假）｜`handoff_change_substantive`（交接包内变更达到 C2/C3 或改动已定稿基线）｜`skill_changes_pending`（`skill-audit` 出具拟改 skills / capabilities表/装配项且用户尚未确认；无拟变更或已确认/拒绝后为假）｜`iteration_close_needed`（探测到下一期方案/换主题/版本升级，且当前迭代是否结束不明确，或用户未明确「关这期/下一期」；已确认结束或明确并行不关后为假）。

同一会话同一确认点只问一次；inbound/迁移/清理清单确认后本轮不再重复。条件不满足 → 跳过该步（及其 hitl）；不确定按触发处理。`release_failed` = 部署失败或发布验证失败/触发回滚条件；`release_ready` = 上线检查单结论 GO；`release_ready_and_acceptance_passed` = 上线检查单 GO 且 UAT/验收通过或不需要；`release_approved` = `confirm_deploy` 已批准；`implementation_required` = 非「只出任务清单」且清单已确认；`backlog_approval_required` = L2+，或清单/范围/节奏实质变化；L1 小批只通知不审批。`has_product_docs_or_prototypes` = 输入含外部 PRD/迭代方案/需求文档/页面原型/截图/接口或技术文档；`understanding_needs_confirm` = 有外部文档/原型、存在 2 个以上实质歧义或冲突、L2+，或用户要求方案/排期/估算；已有**当前任务**理解确认记录则假，纯信息查询/机械低风险操作不触发。`intent_needs_confirm` = 口令/上下文对「给谁·做什么·交付形态」**无法唯一确定**，或跨角色外发handoff/确认文且本任务未对齐过该意图，或新开对外交付主题 → 真；纯查询/机械低风险、同任务意图已确认未变、本句已写死意图、或已对齐任务内的实施续跑（含改代码）→ 假。拿不准按真。细则 `clarification.md` §0。

**评审模式**：`review_required` 在 clarify/plan 判定并写入计划/任务清单；**不单独设 hitl**——用户确认计划/清单后，AI 自动执行 review（或记录免审），不再逐次问“要不要评审”。评审记录的范围必须覆盖本轮完成门 diff；范围小于 diff → 该门不得判 `COMPLETE`。

**波次评审**：计划选定“每波独立评审+过门”后，每波实施完成 → 该波 diff 独立评审 → 结论通过 → 才开下一波；未通过不得把下一波标完成。最终 S5 只做集成/AC/证据/抽样复核，不得替代波次评审。

**前端评审前置（硬）**：进入 `change.review` / `iterate.review` 前，前端变更必须有 `.gate/frontend/parity-matrix.md` + `route-coverage.json` + `design-qa.md` + 每路由桌面/移动截图 + console/network；缺一 → `on_fail` 回 implement 补，不得以代码/测试/API 200 代替。评审员还须抽全部一级/二级菜单、关键深链与关键业务页（按 `project-profile.md` 声明）。

**方案覆盖前置（硬）**：L2+ 进入评审前必须有 `.gate/plan-coverage.md`；后端/功能行覆盖接口/字段/状态/权限/错误码/迁移→实现/测试，前端行覆盖页面/路由/字段/交互→截图；缺行或结论“需修/阻塞” → 回 implement，不得判通过。原型/方案是下限：至少达到原型标准；原型有明显缺陷时可择优修正，但必须在矩阵写偏离理由与确认。

## 3. 门档位（防过度审批）

| 档 | 适用 | 行为 |
| --- | --- | --- |
| autonomous | 只读、L0 微改、可逆 | 直接做，收尾记录假设；仅保留证据/提交/密钥红线 |
| notify | L1 常规、清单/节奏未实质变化 | 展示清单/计划后继续，用户可打断 |
| approve | L2+ 范围/方案/清单实质变化、L3、部署/回滚/回写/提交、skills / capabilities拟变更 | 停：需求基线、**评审方式选择**、方案、清单/节奏、部署、回滚、回写、提交、交接包发送、技能变更 |

低风险动作不要升级为 approve；高风险动作不得降为 notify。红线不被“少问/直跑”覆盖。

**轻量档**：快档只 `confirm_spec` + `confirm_commit`；产品定义不单独设门，方向不清在方案卡里列选项一次性确认；`completion-gate` 仍必须过（见 `rules/core/lightweight.md` §5）。
