# 门（产品轨）

> 单一出处：门语义、`when` 词表、门档位。步骤顺序与是否触发以 `../workflows/*.yaml` 为准；**只认步上 `when` / `hitl` / `hitl_when` / `gate_when`**，专规不另造门。
> 读取时机：当前步有门时只读词表对应 token；写/改 YAML 时才读全表。不要每次开工通读。
> 质量审计/评分卡参考见 `special/quality-gate.md`；它不是额外确认门，执行仍只认步上 `hitl`/`hitl_when`/`gate_when`。

## 1. 门语义

| 门 | 含义 | 必须行为 |
| --- | --- | --- |
| `confirm_go` | 新产品立项 | 出示问题/市场/方案/MVP 假设/成本收益/风险/结论（Go/Hold/Kill）；未过不写全量 PRD |
| `confirm_task_intent` | 任务开工需求/意图确认（全局硬门） | 按 `global-rules.md` §1 分级：新开交付/歧义/外发=完整六段等确认；计划内续跑/意图已清=一行回执；纯只读=一句话。未确认（完整档）不得写/执行/对外/下结论。确认后进入 execute，不重复问；范围/AC/目标变化重新确认。≠ `confirm_intent`。 |
| `confirm_intent` | 意图理解（择优·防自作主张） | 仅当 `intent_needs_confirm`：出示【意图理解】，确认后才落盘。意图已清 → 跳过（可一行回执即做）。细则 `clarification.md` §0。≠ `confirm_understanding`；≠ `confirm_handoff` |
| `confirm_understanding` | 需求理解 + 方案要点 | 出示【理解复述】（谁/场景/问题/现有替代/代价/目标/范围/非目标/证据/假设）+【推荐方案要点】（主路径/关键规则/异常期望/验收口径/不做）+ 缺口清单；涉及换迭代/相对上版时附**本期差量要点**（增/改/删或「首版全部为增」）。用户须对理解与方案均表态；仅回 OK 未对复述/方案表态不算过；确认后才分诊/入池承诺/写正式 PRD/计划/排期 |
| `confirm_plan` | 产品计划 | 首次计划或范围·指标·版本实质变更：目标/路线图/本期范围/**§3.0 Brief+差量表** /里程碑/风险摘要；无差量表（且非明示首版一行）不过门；未确认不进 PRD/排期 |
| `confirm_change` | 需求变更/产品缺陷处置/实现缺陷退回 | 出示分诊依据、影响与变更单要点（**含 §2.1 差量表** Now→Proposed）；产品缺陷须有相符证明；无单不实施 |
| `confirm_design` | 设计方向 | IA/线框/2～3 个视觉方向/tokens；确认后才做高保真 |
| `confirm_prototype` | 原型交接 | 原型路径/设计评审结论/交接要点；**评审前必须有 `prototype-coverage.md`（覆盖矩阵硬）+ 浏览器走查证据**；浏览器不可用时记 `browser=unavailable` 并用用户走查证据过门前评审；确认后才交开发 |
| `confirm_narrative` | 展示叙事 | 受众/目标/故事线/演示范围已成形后确认；仅叙事不明或首次对外演示时停 |
| `confirm_materials` | 对外材料 | 一页纸/Deck/user/资料库/整包导出/发布说明；数字/截图/流程与当前项目一致；仅对外发送、承诺或发布前触发 |
| `confirm_scope` | 单需求立项范围 | 范围（MVP）/排除项/粗排期/风险 一行摘要；条件门：仅跨版本/高价值/未确认范围时停 |
| `select_review_mode` | 落地文档评审方式 | **STOP 二选一**：A 自行评审通过（HUMAN_APPROVED）｜B AI 独立评审（异人量规+评审记录）。适用 PRD/产品计划/设计交接等（`skills/artifact-review`）；同产物只问一次；点名「AI 评审」=B、「我审/自行通过」=A；未选不得宣称通过/定稿/交开发 |
| `confirm_prd` | PRD 定稿/实质变更重审 | 评审结论为「通过（可定稿）」且用户点名定稿/进入排期时出示；**出示前**须有【完稿自检摘要】且 `-Mode prd` 非 BLOCKED；定稿前不排期；仅评审不弹门 |
| `confirm_remark` | 缺陷平台回写 | 出示 id+结论+备注全文+附件名+状态/指派变更；备注与状态同轮；平台不支持出 export |
| `confirm_release` | 发布 | 出示 UAT 结论、回滚预案、公告/客服/监控就绪；未过不发布；已发布仅复盘不重复确认 |
| `confirm_commit` | 拟提交 | 【拟提交】块（文件+`.gitignore`+分支/跟踪+本次动作+推送目标）；**默认仅本地提交**，推送须点名并单独确认；禁擅自切主干/force push/开合并 PR；≠收尾第 2 点「待提交摘要」 |
| `confirm_handoff` | 交接包发送 | **凡拟生成任一 HO 包必停**：出示类型/接收方/必带摘要/阻断/传递方式；用户确认后才落盘；未确认零发包。禁止用「定稿门/评审门/发布门已过」代替本门。未收回执不得称「已接收」；可称「已发送」 |
| `confirm_gitignore` | 入库策略 | 四选一确认资产范围；规范包默认不跟踪，`.gitignore` 写已装包行（多包 `/wf/`）与运行态 `.gate/`，无注释、不预列未装包；其它项只列路径；写档案 §1、改 `.gitignore` |
| `confirm_docs_migration` | inbound/工作文档搬迁、归档或临时清理 | 出示分类/覆盖对照/拟归档或清理清单与目标；确认后执行；不擅自删、不覆盖 |
| `confirm_iteration_close` | 结束当前迭代/版本并进入下一 | 出示当前迭代标识、未完成项、拟归档摘要、下一迭代标识；确认后按 `rules/doc-governance.md` §7.1 关账；选「并行不关」则只落新资料。**关闭=停止新范围/冻结版本线，不停止测试与缺陷修复**；测试未完又要开新迭代，优先「并行不关」，归档待测试完成 |
| `confirm_skill_changes` | 能力/技能体检拟变更 | 出示【拟变更清单】（改 `skills/`·`capabilities/`·装配项）；确认后才改本包或给安装步骤；未确认零改动 |
| `gate: product-prd` | PRD 结构门（when: `prd_structure_required`） | 运行 `verify/Invoke-Gate.ps1 -Mode prd -Artifact <当前PRD>`（推荐显式路径）；BLOCKED → 不得进评审/定稿/交开发；DRAFT → 可审不可定稿；回执 `.gate/wf-product/prd.json`。light 缺追溯仅警告。P2+/P1↑/拟定稿或交开发时为真 |
| `gate: product-review` | PRD 评审门禁（when: `ai_review_chosen`） | 仅选 B（AI）时运行 `-Mode review`；评审人≠作者；READY 后取 `gate_id`；选 A 不跑本门，须 HUMAN_APPROVED + `approved_by` + 自检摘要 + 复跑 `-Mode prd` 至 READY |
| `gate: design-review` | 原型设计评审门禁（when: `ai_review_chosen`） | 仅选 B（AI）时运行 `-Mode design-review`；评审人≠作者、结论=通过；同目录必须有 `prototype-coverage.md`（覆盖矩阵硬；浏览器不可用时 `browser=unavailable` + 用户走查证据可过）且结论=通过；未 READY 不得交开发 |
| `gate: uat-evidence` | UAT 门禁 | 运行 `verify/Invoke-Gate.ps1 -Mode uat`；AC 覆盖、证据、有条件通过的责任人/接受人；未 READY 不得写 UAT 通过。无 UAT 要求可写 `verdict: 不适用` + 依据/批准人，门放行但记警告 |
| `gate: change-closure` | 变更/缺陷联动闭合 | 运行 `verify/Invoke-Gate.ps1 -Mode change`；§6 每项“已更新/不适用/待补”，待补有责任人/截止；未闭合不得关闭 |
| `gate: writeback-receipt` | 平台回写门禁 | `Invoke-Gate.ps1 -Mode writeback -Artifact …`；单号+备注实质+状态取值+fileId/无附件；禁标题刷绿；无回执不得声称已回写 |
| `gate: materials-validate` | 材料库发布校验 | **checklist**：README/INDEX 齐；所有文件有登记；来源可解析；无草稿/证据/密钥/PII；链接自包含；旧版本状态正确；不通过不称完整。 |

> `confirm_task_intent` 是全局开工门（`AGENTS.md` 首轮硬门/§0.1），不依赖 step；其余门仍只认步上声明。

> **`gate_type`**：`machine`=有脚本回执（读 `.gate/` JSON）；`checklist`=按清单/工具核验并留证据。未标默认 `checklist`；新增 gate 必须写 `gate_type` + 证据来源，禁止空门。

## 2. `when` 词表

**求值卡（硬）**：外部事实优先；模型自评不确定 → **按触发（真）**；不得用「先问用户」代替 when 求值（路径/档位不确定才先问）。`when` 假 → 跳过整步；`hitl_when` / `hitl[].when` 假 → 只跳过该门；`gate_when` 假 → 只跳过该闸。跳过须写 `skip=` / `when_eval=`。

| token | 为真 | 为假 |
| --- | --- | --- |
| `has_pending_commit` | 有文件变更待提交 | 无待提交文件 |
| `has_uat` | 本轮有 UAT/验收要求（发布门必须核） | 本轮无 UAT/验收要求 |
| `change_requested` | 改动已定稿基线或产品缺陷/问题处置需确认（不含纯新需求入池） | 纯新需求入池/答疑，无基线或缺陷处置变更 |
| `intent_needs_confirm` | 口令/上下文对「给谁·做什么·交付形态」**无法唯一确定**，或跨角色外发handoff/确认文且本任务未对齐，或新开对外交付主题 → 真 | 纯查询/机械、同任务已确认未变、本句已写死意图、已对齐任务内续跑 → 假；**歧义拿不准**按真。细则 `clarification.md` §0 |
| `understanding_needs_confirm` | 输入为模糊/单点需求、含外部文档或原型、存在实质冲突、方案有取舍、或 P1↑/P2/P3/点名写 PRD/计划/收集需求时需确认**理解+方案要点**；已有**当前任务**理解与方案双确认记录/已确认受理单（含方案要点）、或信息完整的缺陷单/答疑且已能复述且无新方案取舍时假 | 当前任务已确认理解与方案要点，或纯查询/机械低风险 |
| `plan_needs_confirm` | 首次计划或范围·指标·版本实质变更 | 同会话已确认且范围/指标/版本未实质变 |
| `new_requirement_or_scope_change` | 新需求/范围变化 | 纯答疑/文案，无新需求或范围变化 |
| `benchmark_or_mode_p` | 口令为竞品对标/功能对标/对标分析/功能差距，或 discover 已分诊为模式 P | 仅洞察/需求池/模式 S，未分诊为模式 P |
| `new_requirement` | 分诊为新需求（不含已定稿基线的需求变更） | 非新需求（变更/答疑/缺陷/重复） |
| `scope_decision_required` | 跨版本/高价值/点名立项，需单需求范围确认 | 未跨版本、非高价值、未点名立项 |
| `scope_unconfirmed` | 无已确认产品计划且无已批准的单需求范围 | 已有已确认产品计划或已批准的单需求范围 |
| `landing_doc_review_needed` | 落地文档（PRD P2+、产品计划首版或实质变更、设计评审/设计交接、交付计划、实质变更重审、或用户点名评审）待选评审方式且本会话尚未选定；P0/普通 P1 light 且用户未点名时可假；**P1↑ 默认 B（AI 独立评审），选 A 须用户明确 + 独立复核；P2+ 必问 A/B** | P0/普通 P1 light 且未点名；或本会话已选定 A/B 且文档未实质变 |
| `ai_review_chosen` | 用户已选 B（AI 独立评审） | 用户选 A 或尚未选择 |
| `prd_structure_required` | 本步为写/改 PRD 且级别为 P2+/P1↑，或用户点名定稿/交开发/拟置 APPROVED，或普通 P1 将交开发；P0 纯文案无结构变更为假 | 非写/改 PRD，或 P0 纯文案且无结构变更 |
| `finalize_requested` | 评审通过且用户点名定稿/进入排期（仅评审不触发） | 仅评审、未点名定稿或进入排期 |
| `has_ui_requirement` | 有页面/界面需求或点名画原型 | 无页面/界面需求且未点名原型 |
| `narrative_needs_confirm` | 受众/目标/演示范围不明或首次对外演示 | 受众/目标/范围已明且非首次对外演示 |
| `materials_for_external` | 材料/文档将对外发送、承诺或发布 | 仅内部留档，不对外发送/承诺/发布 |
| `demo_needs_dryrun` | 准备演示/客户介绍/彩排 | 无演示/客户介绍/彩排 |
| `docs_requested` | 点名用户手册/快速开始/FAQ/发布说明/培训材料 | 未点名用户文档（手册/FAQ/发布说明/培训） |
| `needs_impact_assessment` | 变更/缺陷/新需求需影响评估 | 纯答疑/文案，无需影响评估 |
| `needs_linked_update` | 需联动回写与回执（除纯答疑外均为真） | 纯答疑且无联动项 |
| `decision_required` | 需处置确认（P2+/P3、改已定稿基线、产品缺陷、影响版本/里程碑/KPI；P0/P1 且不改基线=false） | P0/P1 且不改已定稿基线 |
| `change_apply_required` | 处置结论为接受/下期/立即修且确有联动项；或 P0/P1 轻量受理（无 AC/范围变化）确有联动项（无需 `decide`）（拒绝/重复/不修/退回开发/补充信息=false） | 拒绝/重复/不修/退回开发/补充信息 |
| `go_decision_go` | 立项结论=Go（Hold/Kill=false） | 立项结论=Hold/Kill |
| `substantive_change` | 实质变更需重审 | 纯答疑/文案，不改已定稿 AC/范围 |
| `plan_level_change` | 影响版本范围/里程碑/KPI | 不影响版本范围/里程碑/KPI |
| `release_decision_needed` | 未发布或发布内容/窗口变更 | 已发布且仅做复盘 |
| `remark_writeback` | 有拟回写缺陷平台的备注/附件/状态/指派 | 无拟回写缺陷平台的备注/附件/状态/指派 |
| `handoff_send_required` | 拟生成/点名 HO 且未确认类型/接收方/摘要（仅说「要交接包」未确认摘要仍真；不得因它门已过置假） | 用户已确认该摘要未变 |
| `handoff_change_substantive` | 交接包内变更达 C2/C3 或改定稿基线 | 低于该阈值 |
| `prd_ready_for_handoff` | PRD 已 APPROVED 且门 READY，本轮定稿/进排期，台账无同版本 REQ 已发/已收；仅评审不触发 | 未定稿或已发过 |
| `docs_migration_needed` | 有未登记资料、拟改名/搬迁/归档、工作文档清理或旧结构迁移 | 无此类动作或已确认 |
| `skill_changes_pending` | skill-audit 拟改 skills/capabilities 且未确认 | 无拟改或已确认/拒绝 |
| `iteration_close_needed` | 探测到下一期/换主题/升级且是否关本期不明 | 已确认结束或并行不关 |

未写 `when` 视为无条件。`gate_when: ai_review_chosen` 不满足 → 跳过该 gate（步骤可走 A 路径）。同一确认点只问一次；固定骨架不得省略。

**易混**：`new_requirement`（change 分诊新需求入池）≠ `new_requirement_or_scope_change`（prd prioritize）；`substantive_change`（需重审）≠ `plan_level_change`（版本/里程碑/KPI）≠ `handoff_change_substantive`（交接包内 C2/C3 或改定稿基线）。

**P 档推导（按事实，不靠自评）**：P0 纯文案/配置且不改 AC/范围；P1 单点功能或规则、≤1 模块、不改状态/权限/资金/数据主规则；P1↑ 命中权限/资金/隐私/不可逆数据/主数据规则（正文同 P1，自检与结构门按 P2）；P2 新功能/新版本/跨模块，或改已定稿基线，或影响 KPI/里程碑；P3 0→1/新产品/战略。两条都能解释时取高一档；`route` 的 `level=` 须给事实依据（改了哪些 AC、是否触权限或数据、是否改已定稿基线），不得只写档位。档位只决定门与深度，不替代用户判定：本轨 `select_review_mode`/`confirm_*` 仍由用户拍板。

## 3. 门档位（防过度审批）

| 档 | 适用 | 行为 |
| --- | --- | --- |
| autonomous | 只读、低风险、可逆 | 直接做，收尾记录假设 |
| notify | 中风险、可回退 | 展示计划/清单后继续，用户可打断 |
| approve | 高风险/不可逆 | 停：立项、计划、**评审方式选择**、定稿、变更、平台回写、发布、提交、搬迁/归档/清理、交接包发送、技能 / 能力拟变更 |

低风险动作不要升级为 approve；高风险动作不得降为 notify。红线不被“少问/直跑”覆盖。
