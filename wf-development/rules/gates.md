# 门（开发轨）

> 单一出处：`hitl` / `gate` / `when` 语义与词表。步骤顺序以 `../workflows/*.yaml` 为准；**只认步上 `when` / `hitl` / `hitl_when` / `gate_when`**，专规不另造门。
> 读取时机：当前步有门时只读词表对应 token；写/改 YAML 时才读全表。

## 1. 门与 gate

| 标记 | 含义 | 必须行为 |
| --- | --- | --- |
| `hitl:` | 确认门声明 | 标量（单门）或列表（多门；各项 `name` + 可选 `when`）；未写 `when` 视为无条件 |
| `hitl_when:` | 标量门条件 | 条件不满足 → 跳过该门，不算违例 |
| `gate_when:` | 门禁条件 | 条件不满足 → 跳过该 gate（步骤不跳过） |
| `confirm_change` | 变更吸收/影响 | 出示变更类型/影响矩阵/待更新文档/待确认项；实质变更确认后才更新基线 |
| `confirm_task_intent` | 任务开工需求/意图确认（全局硬门） | 任何任务开工前先输出【需求与意图理解】并等用户确认；未确认不得写/执行/对外/下结论；纯只读问答可一句话复述后直接回答。确认后进入 execute，不重复问；范围/AC/目标变化重新确认。**缺陷/批量入口（指派给我、我的待修、修复#N、#N）不豁免本门**；仅用户明说「一次性/直接跑完/中途不停」可免等待（理解仍须先输出）。细则 `global-rules.md` §1。 |
| `confirm_intent` | 意图理解（择优·防自作主张） | 仅当 `intent_needs_confirm`：出示【意图理解】，确认后才落盘。意图已清 → 跳过本门（可一行回执即做）。细则 `clarification.md` §0。≠ `confirm_understanding`；≠ `confirm_handoff` |
| `confirm_understanding` | 需求理解 | **主屏**：§0【业务与变更简报】+【本期差量表】（增/改/删）+ 待确认单摘要（冲突·GAP·开发择优/置信度）；理解摘要/完整理解包按链选择。无 §0/差量表不得过门（L0 迷你 Delta 除外）。确认后才进下一门/实施；是否写需求基线/设计由链决定 |
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
| `gate: completion-gate` | 完成门（开发轨） | 任务开始 `-StartTask`；运行 `verify/Invoke-Gate.ps1 -Acceptance ...`；写 `.gate/wf-development/completion.json`；**前端套装与 capture 运行时只认当前步骤包内「前端硬门」**（维护真源 `rules/core/frontend-gate.md`，改后须 `build_step_packets.py` 重生）；**写完成前 `-Claim`，只认 `CLAIM: ALLOWED`**；空 diff=`NOT_VERIFIED`、dry-run=`DRY_RUN`、缺项 → `BLOCKED` |
| `gate: dev-plan` | 开发计划检查 | **checklist**：跑 `rules/tools/validate_dev_plan.py`（可用时）+ 阶段表/门/证据/下一步人工核；缺项不过 |
| `gate: s6-admission` | S6 提测准入 | **checklist**：按 `verification.md` §2.2 的 `DEV/QA/PRODUCT` 分流表核；`DEV` 未清零、`QA` 未入提测单、`PRODUCT` 未关闭 → 不得标“可提测”；证据=内部分流表+提测单+评审报告。分流表留在内部质量记录，不写入测试提测单。 |
| `gate: materials-validate` | 材料库发布校验 | **checklist**：README/INDEX 齐；所有文件有登记；来源可解析；无草稿/证据/密钥/PII；链接自包含；旧版本状态正确；不通过不称完整。 |
| `gate: release-readiness` | 生产/正式发布就绪 | **checklist**：按上线检查单逐项核；硬项不过 → NO-GO；test/staging 部署不适用 |

> `confirm_task_intent` 是全局开工门（`AGENTS.md` §0 第一问），不依赖 step；其余门仍只认步上声明。

> **`gate_type`（步上字段）**：`machine` = 有脚本回执（读 `.gate/` JSON，verdict 可机器判定）；`checklist` = 按清单/工具核验并留证据，不假装机器可判。未标默认 `checklist`；`gate` 只表示检查点，不等于自动门。新增 gate 必须同时声明 `gate_type` 与证据来源；禁止只写 `gate:` 而无检查方法。

## 2. 步骤条件 `when` 词表

**求值卡（硬）**：外部事实优先；模型自评不确定 → **按触发（真）**；不得用「先问用户」代替 when 求值（路径/档位不确定才先问，见 AGENTS §0.1）。`when` 假 → 跳过整步及其 hitl；`hitl_when` / `hitl[].when` 假 → 只跳过该门；`gate_when` 假 → 只跳过该闸。跳过须写 `skip=` / `when_eval=`。

| token | 为真 | 为假 |
| --- | --- | --- |
| `c2_or_c3` | 本轮变更分级 C2（范围/里程碑/资源）或 C3（战略/架构/合规/破坏性） | 未达 C2 |
| `has_code_change` | 本轮代码/配置 diff 非空（不含生成物） | 纯文档/无 diff |
| `plan_has_code_change` | 方案卡改动面含代码/配置/页面/接口（非纯文档） | 纯文档/文案/注释 |
| `dev_plan_required` | L2+ 或已有 `development-plan.md` | L0/L1 且无计划 |
| `release_failed_or_direct_rollback` | 入口=回滚，或部署/发布验证失败触发回滚 | 正常发布路径 |
| `new_feature_or_scope_change_or_requested` | 新功能/范围变化，或点名做 requirements | 无新功能/范围且未点名 |
| `new_feature_or_architecture_or_breaking_change_or_high_risk_or_requested` | 新功能/架构/破坏性/高风险，或点名做 design | 未命中且未点名 |
| `multi_file_or_new_feature_or_requested` | 多文件或新功能，或点名做 plan | 单点且未点名 |
| `has_qa_or_deploy_or_requested` | 本轮有提测/QA/部署交付，或点名 deliver | 无交付且未点名 |
| `has_deployed` | 本轮部署步骤已成功执行 | 尚未成功部署 |
| `has_uat` | 本轮有 UAT/业务验收要求 | 无 UAT 要求 |
| `release_ready_and_acceptance_passed` | 上线检查单 GO，且 UAT 通过或不需要 | 未 GO 或验收未过 |
| `release_approved` | `confirm_deploy` 已批准 | 未批准 |
| `iteration_done_or_incident` | 迭代收尾或事故复盘入口 | 否 |
| `recurring_defect_or_incident` | 复发缺陷或事故需复盘 | 否 |
| `incident_or_major_release` | 事故或重大发版需复盘 | 否 |
| `docs_migration_needed` | 将搬迁/归档/清理且清单未确认 | 已确认或无搬迁 |
| `requirements_need_confirm` | 需求基线实质变且未确认 | 已确认或无实质变 |
| `new_product_or_unclear_idea` | 自包含链：方向不清/新产品（正式协作/迭代 → 完整链） | 小改/需求已清 |
| `solo_gate_required` | 自包含链：有方案卡/验收表且已 StartTask | 单独测试/纯文档 |
| `intent_needs_confirm` | 给谁·做什么·形态无法唯一确定，或跨角色外发未对齐，或新开对外交付 | 查询/机械/同任务已确认/意图写死/任务内续跑；**歧义拿不准**按真 |
| `understanding_needs_confirm` | 外部文档/原型、≥2 实质歧义、L2+，或点名方案/排期/估算 | 当前任务已理解确认；纯查询/机械低风险 |
| `solo_understanding_needs_confirm` | 自包含链：输入含文档/原型/多源，或大改动/高风险 | 一句话/无文档小改 |
| `has_product_docs_or_prototypes` | 输入含 PRD/迭代方案/需求/原型/截图/接口或技术文档 | 无此类输入 |
| `change_is_substantive` | 改已定稿 AC/范围/对外承诺（未达 C2 也可真） | 纯答疑/文案/无基线改动 |
| `backlog_approval_required` | L2+，或清单/范围/节奏实质变化 | L1 小批只通知 |
| `plan_needs_confirm` | 计划/范围/节奏实质变且未确认 | 已确认未变 |
| `has_pending_commit` | 有文件变更待提交 | 无待提交 |
| `work_changed_or_requested` | 本轮有代码/配置/文档改动，或点名验证 | 只读不动 |
| `implementation_required` | 非「只出任务清单」且清单已确认 | 只出清单或未确认 |
| `need_select_review_mode` | L2+ 新产出落地文档或点名文档评审，且本会话未选 A/B | L0 无新文档；已选 A/B |
| `do_landing_doc_review` | L2+ 有新增/变更落地文档或点名文档评审（不依赖是否已选 A/B） | L0/无新文档 |
| `design_needs_spec_approval` | L1 有新方案/ADR/前端设计且未进 review-docs | L0；或 L2+ 由 review-docs 接管 |
| `review_required` | 有实施且（L2+/L3，或高风险/大改/破坏性，或 **L2+ 新功能**，或 **L1+ 用户可见 UI 命中前端硬门 A 级**，或点名） | L0 单文件，或确实低风险 L1 单点且未命中前端硬门 A 级（免审须记理由；免审不免自测） |
| `product_defect` | triage 判定为产品缺陷 | 工程缺陷或其他 |
| `product_decision_received` | 已收到产品处置结论 | 仍在等产品 |
| `product_decision_requires_alignment` | 产品结论需再对齐范围/方案 | 结论可直接实施或关闭 |
| `need_clarification` | 缺陷信息不足须澄清 | 可实施 |
| `menu_includes_commit` | 本轮菜单含提交 | 不含 |
| `menu_includes_writeback` | 本轮菜单含平台回写 | 不含 |
| `menu_includes_deploy` | 本轮菜单含部署 | 不含 |
| `not_awaiting_product` | 非 await_product / 非 AWAIT_PRODUCT 输出 | 正在等产品 |
| `handoff_send_required` | 拟生成/点名 HO 且未确认类型/接收方/摘要 | 已确认该摘要未变 |
| `handoff_change_substantive` | 交接包内达 C2/C3 或改定稿基线 | 低于该阈值 |
| `skill_changes_pending` | skill-audit 拟改未确认 | 无拟改或已确认/拒绝 |
| `iteration_close_needed` | 探测到下一期/换主题/升级且是否关本期不明 | 已确认结束或并行不关 |

同一会话同一确认点只问一次；inbound/迁移/清理清单确认后本轮不再重复。

**L 档推导（按事实，不靠自评）**：L0 纯文档/文案/注释；L1 代码/配置且 ≤3 文件、≤1 模块、无接口/数据/权限变化；L2 新功能/接口/数据，或 >3 文件，或 >1 模块；L3 权限/资金/迁移/公共 API/破坏性。`route` 的 `level=` 必须给事实依据（文件数/模块数/是否改接口或数据）；两条路径都能解释时取高一档。

**评审模式**：`review_required` 在 clarify/plan 判定并写入计划/任务清单；**不单独设 hitl**——用户确认计划/清单后，AI 自动执行 review（或记录免审），不再逐次问“要不要评审”。评审记录的范围必须覆盖本轮完成门 diff；范围小于 diff → 该门不得判 `COMPLETE`。

**波次评审**：计划选定“每波独立评审+过门”后，每波实施完成 → 该波 diff 独立评审 → 结论通过 → 才开下一波；未通过不得把下一波标完成。最终 S5 只做集成/AC/证据/抽样复核，不得替代波次评审。

**前端评审前置（硬）**：进入 `change.review` / `iterate.review` 前，按当前步骤包内「前端硬门」核验；缺项、`partial/pending` 或未生成证据 → `on_fail` 回 implement，不得以代码/测试/API 200 代替。评审员还须抽全部一级/二级菜单、关键深链与关键业务页（按档案声明）。

**方案覆盖前置（硬）**：L2+ 进入评审前必须有 `.gate/plan-coverage.md`；后端/功能行覆盖接口/字段/状态/权限/错误码/迁移→实现/测试，前端行覆盖页面/路由/字段/交互→截图；缺行、存在未完成行，或结论为“未通过/不通过/需修/阻塞” → 回 implement，不得判通过。原型/方案是下限：至少达到原型标准；原型有明显缺陷时可择优修正，但必须在矩阵写偏离理由与确认。

## 3. 门档位（防过度审批）

| 档 | 适用 | 行为 |
| --- | --- | --- |
| autonomous | 只读、L0 微改、可逆 | 直接做，收尾记录假设；仅保留证据/提交/密钥红线 |
| notify | L1 常规、清单/节奏未实质变化 | 展示清单/计划后继续，用户可打断 |
| approve | L2+ 范围/方案/清单实质变化、L3、部署/回滚/回写/提交、skills / capabilities拟变更 | 停：需求基线、**评审方式选择**、方案、清单/节奏、部署、回滚、回写、提交、交接包发送、技能变更 |

低风险动作不要升级为 approve；高风险动作不得降为 notify。红线不被“少问/直跑”覆盖。

**自包含链（solo）**：只 `confirm_spec` + `completion-gate` + `confirm_commit`；产品定义不单独设门，方向不清在方案卡里列选项一次性确认（见 `rules/core/lightweight.md` §5）。
