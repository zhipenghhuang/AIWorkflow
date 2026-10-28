# 项目变更与版本记录

> 本文件记录 **AI Workflow** 项目自身的版本与迭代变化；最新在前。  
> 版本格式：`yyyy.MM.dd.N`；当前版本见下表。

## 0. 版本总览

| 包/仓 | 当前版本 | 本次变化 | 说明 |
| --- | --- | --- | --- |
| 产品规范 | `2026.10.28.12` | 更新 | 执行契约/角色契约/门与计划闭环 |
| 开发规范 | `2026.10.28.12` | 更新 | 执行契约/角色契约/门与计划闭环 |
| 测试规范 | `2026.10.28.12` | 更新 | 执行契约/角色契约/门与计划闭环 |
| 母版仓 | `2026.10.28.12` | 更新 | 契约化、CI、正确性与 token 治理 |

> 母版仓版本取三包最高版本，不新增第四套版本号；三包仍可独立升级、独立落地。

## [2026.10.28.12] - 2026-10-28

### Added

- 三包新增 `规则/核心/执行契约.md`：判断模式（execute/analyze/stop）、自主边界、步骤契约（output/verify/on_fail/escalate_to）、计划同步矩阵、时间/Token 纪律、收尾【遵守自检】。
- 三包新增 `规则/协作/角色契约.md`：角色主责/决策权/停止与升级/不做什么；补足 agent YAML 之外的职责边界。
- 步骤新增 `gate_type`（machine/checklist）、`precondition`、`on_fail`、`next` 等契约字段；`validate_workflow.py` 增加空转步、gate_type、next 引用、chain:full 终点警告。
- 根新增 `.github/workflows/validate.yml`、PR 模板、CODEOWNERS、`THIRD_PARTY.md`；三包自检可在 push/PR 自动跑。
- 测试 `writeback-receipt` 门、开发 `confirm_replan`（C2/C3）、`dev_plan_required`/`has_code_change` 条件。

### Changed

- 三包 AGENTS 压缩到 token 预算内（≤5500）；单步读取预算改为 ≤3 个来源；细节下沉到规则/执行契约/角色契约。
- 产品 A 路径与 B 路径统一为可过门：A = `review_status: HUMAN_APPROVED` + `approved_by` + `status: APPROVED`，复跑 prd 至 READY；不再把 A 当 DRAFT。
- UAT verdict 统一为“有条件通过”，兼容“带条件通过”；UAT 与 PRD 的 A-xx/AC-xx 做归一化比较。
- 产品计划/交付/0→1 补 output；onboard.verify、skill-audit、release 补产物/提交步；测试 report→handoff 改为显式短链。
- 测试 `gate_id` 只哈希输入（计划/冒烟/台账），不哈希报告本身；回填回执后复跑保持稳定。
- 开发 release 增加 commit 步；handoff.send 增加 `validate_handoff.py` 校验；defect-fix 门条件改为 `has_code_change`。
- 技能接线：solution-design 补 02F/可观测/AI；测试与产品新技能在步骤中显式加载。
- 计划模板补最小规划集：产品 RICE/WSJF + 缓冲；开发关键路径/外部依赖/里程碑退出/缓冲；测试 9.0 估算与风险 P×I 评分。

### Fixed

- 修复 `validate_workflow.py` 的 next 两遍解析、数字 token、`gate_type` 警告；三包 YAML 校验 0 warning。
- 修复 `Test-Template.ps1` token 正则不支持数字的问题（`c2_or_c3`）。
- 修复产品 Test-Template 被误覆盖的问题（恢复产品版并保留正则修复）。
- 读取索引补执行契约入口；文档治理/工作流不再重复计划同步矩阵。

## [2026.10.28.11] - 2026-10-28

### Added

- 三包 `技能/README.md` 新增「技能质量标准（Skill Anatomy）」：frontmatter 规范、正文结构、反合理化/红旗/验证、≤500 行与渐进披露、修改流程与验收清单。
- 开发轨新增技能：`debugging-and-error-recovery`（复现/定位/缩小/修因/防回归）、`observability-and-instrumentation`（日志/指标/追踪/SLO/告警/成本）、`ai-application-engineering`（LLM/RAG/Agent/评测/护栏/成本/隐私）。
- 产品轨新增技能：`analytics-and-experimentation`（指标树/事件字典/漏斗/留存/A-B/护栏/隐私）。
- 测试轨新增技能：`test-data-and-environment`（环境基线/造数/隔离/清理/PII/依赖）、`ai-feature-testing`（oracle/评测集/非确定性/红队/工具调用）。
- 开发 `threat-modeling` 补强：OWASP ASVS 5.0/WSTG、供应链（SLSA/Scorecard）、AI/LLM 威胁、滥用场景、安全验收与 DoD。
- 开发 `engineering-quality` 补强：AI/LLM 与可访问性/国际化质量行、AI 高风险阻断、常见合理化表。
- 开发 `code-review` 补强：AI 生成代码/供应链/a11y/i18n/合理化表。
- 开发 `acceptance-and-launch` 补强：渐进发布/特性开关/SLO/回滚演练/合理化表。
- 测试 `test-performance-security-compatibility` 补强：OWASP WSTG/LLM、Core Web Vitals（INP）、WCAG 2.2、i18n、混沌/韧性、合理化表。
- 测试 `testcase-design`、`test-execution-and-exploration`、`test-analysis-and-plan` 补强：AI/非确定性用例、a11y/i18n、自动化分层与 CI、flake 治理、证据完整性。
- 产品 `prd-writing` 补强：AI 产品需求、可访问性/国际化、指标/实验、合理化表。
- 其余 9 份技能补齐验证/DoD 节：`api-design`、`retrospective-and-improvement`、`presentation-design`、`product-docs`、`prototype-and-interaction`、`review-and-finalize`、`ui-visual-design-system`、`test-artifact-review`、`test-interface`。
- 三包 `能力/00-能力注册表.md` 新增可选能力：AI 评测/观测/护栏、特性开关、供应链、IaC 扫描、契约测试、a11y、可观测、实验/产品分析、AI 红队、混沌；补充 Agent Skills 规范、SLSA v1.2、OWASP LLM 2025、NIST AI RMF、ISO/IEC 42001、WCAG 2.2、Core Web Vitals、OpenTelemetry 等校准基线。

### Changed

- 三包 48 份技能 `description` 均具备中文触发词（其中 34 份本次补加），提升中文口令下的技能选择准确率。
- 产品 `prd`、开发 `change`、测试 `testing` 的步骤注记挂载新技能，确保命中步骤可加载。
- 测试 `Invoke-TestWorkflow.ps1` 自检白名单补充 `02-文档/`，消除交接包模板路径误报。
- 根 `README.md` 计数同步：工作流 产品 11 / 开发 10 / 测试 5（合计 26），技能 产品 14 / 开发 24 / 测试 10（合计 48）。
- 三包实例适配边界：实例默认不改；AI 发现不匹配先输出拟改内容/原因/影响，用户确认后可本地适配模板/技能/规则，留痕且不影响母版；母版整包更新前备份/比对。
- 三包版本对齐 `2026.10.28.11`。

## [2026.10.28.10] - 2026-10-28

### Added

- 三包 `AGENTS.md` §0.0 与 `文档质量标准.md` §0.1：母版只维护通用高标准；实例规范目录只读；模板是骨架、标准是底线；按项目实际裁剪，不逐条机械填写；不匹配优先改产出文档；适配建议回母版需用户确认。
- `README.md`、`Update-Assets.ps1`、三包 `维护.md` 增加母版/实例边界说明。

### Changed

- 冲突优先级改为“先修母版模板并升版本 → 自检 → 整包分发”，禁止实例各自改模板。
- 三包版本对齐 `2026.10.28.10`。

## [2026.10.28.9] - 2026-10-28

### Added

- 三包新增 `规则/核心/文档质量标准.md`：通用硬门槛、按文档位置的类型矩阵、交付前评审清单、参考基线（ISO/IEC/IEEE 29148、29119-3、ISTQB、MADR、Keep a Changelog/SemVer、Google SRE、GitHub Docs、Diátaxis、WCAG 2.2、OpenAPI 3.1）。
- 三包 `AGENTS.md` §0.0 增加“所有文档过质量标准”；模板索引、维护入口增加指针。
- 质量标准补充冲突优先级：AGENTS/红线 > 质量标准 > 模板结构；模板冲突先修模板，不按旧模板产出。

### Changed

- 三包 `收尾骨架`「今日工作总结」：删除「待确认 N 项，见最近任务收尾第 4 点」；改为与收尾「汇报」同口径的确定性结论说明体，禁止待确认表与待确认指针。只读/状态简报分级未改。
- 三包版本对齐 `2026.10.28.9`。

## [2026.10.28.8] - 2026-10-28

### Added

- 三包 `AGENTS.md` §0.0「事实字段不臆填（硬规则）」：环境 URL/端口/IP、构建/提交、账号、日期、接收人、数据量、测试结果、缺陷号、发布窗口、审批/准出结论等，必须来自实际配置/命令/文档/用户确认；未确认写「待确认」并停下问。
- 开发：提测单、发布说明、交接包说明模板增加事实字段校验；测试环境必须用户/测试确认，禁止开发默认/示例值。
- 测试：测试计划、测试报告模板增加事实字段校验；执行数据/结果/缺陷/准出必须来自台账/证据。
- 产品：PRD、UAT 模板增加事实字段校验；客户事实/指标/日期无来源写「假设/待验证」。

### Changed

- 文档语言：禁止辩解式/对比式/冗余括注（如解释“不是某个环境/端口”）和未经确认的“应该/可能”结论。
- 三包版本对齐 `2026.10.28.8`。

## [2026.10.28.6] - 2026-10-28

### Added

- 测试：`Invoke-Gate.ps1 -Mode execute -Scope`；缺 Scope 且无法推断 → BLOCKED；report 仍全仓。
- 开发：`-StartTask` 写入 `base_commit`；门按 base..工作区计 diff；profile `*_scoped`+`{files}` 真正定向。
- 产品：回执 `artifact_via`；未传 `-Artifact` 仅警告不拦。

### Changed

- 测试：execute 的 coverage/p0 对 Scope 外 soft；禁无 Scope 全仓 FAIL 当本批结论。
- 产品：light PRD 缺追溯 → warning；writeback 须备注实质/状态取值/附件回查。
- 开发：未配定向时检查 id=`project-*`；截图新鲜度对照 `started_at`；defect-fix wrap 跑 `Test-Report.ps1`。

### Fixed

- 开发：中途 commit 导致空 diff → `NOT_VERIFIED` 的假阴性（任务窗口丢失）。
- 三包文档：去掉「定向/拒绝旧截图」与实现不符的表述。

## [2026.10.28.5] - 2026-10-28

### Added

- 开发规范 `AGENTS.md` §0.7：本地提交/推送/部署三件事分离；默认仅提交，推送单独确认，部署只走 `release`。
- 提交节奏硬触发：任务开始前基线检查、任务完成/切换前提交检查、每日/会话结束提交提醒、>20 文件或 >500 行阈值、发布前干净工作区。
- `规则/工作流.md` §2.1：提交节奏、基线检查、`【提交提醒】`、`【拟提交】` 增加基线/本任务-前序-无关统计/建议拆分/CI。

### Changed

- `规则/门.md`：`confirm_commit` 默认仅本地提交，推送须单独确认；`confirm_deploy` 增加干净工作区、已提交/tag、`completion=COMPLETE` 硬项。
- `workflows/iterate.yaml`、`change.yaml`、`control.yaml`、`release.yaml`：补齐任务边界/脏工作区停下、提交提醒、推送单独确认、部署前干净构建。
- `规则/模板/90-交接与收尾/收尾骨架.md`：第 2 点增加未提交统计与建议动作；`wrap` 有未提交时输出【提交提醒】。

## [2026.10.27.14] - 2026-10-27

### Changed

- 三包 `规则/文档治理.md` §7：**换迭代 = 关当前版进入下一版**；与正式发版同一套分类/归档/清理标准，仅跳过发版对外项（根 CHANGELOG/发布说明/准出等）。
- 新门 `confirm_iteration_close` / `iteration_close_needed`：不确定是否结束当前迭代（如仍在提测/缺陷回归）→ 先问确认；确认后执行 §7.1；选「并行不关」只落新资料。
- 废除原 §8.1「轻量卫生」表述；入站/换代工作流与 AGENTS 对齐 §7；相关步挂载双门（迭代关闭 + 文档迁移）。

## [2026.10.27.13] - 2026-10-27

### Added

- （已被 .14 取代）原 §8.1 迭代切入卫生：换代时同会话卫生扫描；现并入 §7 关账。
- 挂载：开发 `intake.absorb` / `materials` / `change` / `control`；产品 `materials` / `change` / `plan.publish`；测试 `materials` / `testing.plan` 期中变更。

## [2026.10.27.12] - 2026-10-27

### Changed

- skill-audit：无填实项目档案/产品档案/环境基线 → **强制 generic**（母版无项目不再空跑 project）；口令增「能力优化/技能优化/优化能力…」「母版能力优化」。
- onboard lifecycle：增「清理无效/失效/垃圾文件、文档清理、归档失效文档」等同义入口；「维护/查询」含清理→lifecycle、含能力优化→skill-audit。

## [2026.10.27.11] - 2026-10-27

### Added

- 三包 `workflows/skill-audit.yaml` + `规则/playbooks/skill-audit.md` + 体检报告模板：口令「体检能力」等；默认项目适配，含「通用/母版」→ generic。
- 门 `confirm_skill_changes` / `skill_changes_pending`；确认后可就地改本包 `技能/`·`能力/`（单包/开源无需母版仓）。
- 业务会话「适度建议」：有证据达不到要求时收尾至多 1 条指向「体检能力」。

### Changed

- 「装配能力」仍只做安装向导；深度诊断走 skill-audit。根 README FAQ/维护约定改为：落地可就地改包；母版同步会覆盖未回灌改动。

## [2026.10.27.10] - 2026-10-27

### Changed

- 测试：工作流 §2.1.0 增加「疑似体验/布局不合理」——截图时顺带看一眼，**有见则记额外发现**，默认不 fail、不做设计评审；探索式侧重补一句展开后邻接布局。

## [2026.10.27.9] - 2026-10-27

### Added

- 测试：`技能/testcase-design` §2.2 **深度档**（P0/状态/边界/权限/写操作/视觉最低厚度）；完整≠条数，禁场景 1:1 冒充覆盖。
- 测试：工作流 §2.1.0 **视觉落地**——生成登记视觉基础；浏览器 MCP **截图同帧检六项**（布局/遮挡/截断/空态加载错误/按钮态/文案减法）。
- 测试：覆盖闸机器核用例 §4「深度档自检」「视觉基础」存在性（`test_gate.py` Mode coverage）。

### Changed

- 三闸②=映射 + 深度档；计划模板 §3.5 改为 P0 强制面勾选（详版在技能，不重复清单）。
- generate/execute playbook、testcase-agent/worker/orchestrator、评审技能、门/验证/报告模板、testing.yaml 同步指针；AGENTS `template_version`→`2026.10.27.9`。

## [2026.10.27.8] - 2026-10-27

### Added

- 三包 `AGENTS.md` 增加「模板是下限不是上限」与「不确定且影响范围/验收/风险 → 停下问 1 个关键问题」，明确 AI 可在步内方法/顺序/工具/拆分/措辞上自主择优；输出骨架、门、证据、红线仍不可省。
- 产品 UAT 门支持 `verdict: 不适用`（仅无 UAT 要求；须写依据 + 批准人/接受人），解决内部变更「不适用」与门 BLOCKED 的矛盾。
- 开发 `code-review` 技能补充 `.gate/review.md` 评审记录字段；前端实现补充表单/焦点/图片/深链/危险操作等高收益 UI 检查。

### Changed

- 阅读协议从「硬上限」改为「预算目标（非硬上限）」：常规 ≤5 来源/≤8k tokens，确需更多只读当前节并说明；workflow 只读当前 step 块，不整文件通读。
- 冲突优先级改为「安全/合规/硬红线 > 用户明确指令 > 项目根 AGENTS > 本文」；澄清 3 问上限对阻塞/安全/合规/高风险问题不适用。
- 开发 `change` 顺序改为 `release_handoff → wrap → commit`，`iterate` 改为 `release_handoff → retro → wrap → commit`；`retro/intake/control` 增加独立 commit 门，避免 wrap 更新漏提交。
- 产品 `new-product` 移除与子流程重复的计划/PRD/UAT 门；产品原型/展示口令按入口分档，避免「线框图/彩排」误跑全链。
- 测试 `AGENTS.md` 压缩至读取预算内；测试/产品条令中的 `AGENTS §5 六段`、`§0.3-4` 等错误引用改为收尾骨架/实际节；测试包同期含 `2026.10.27.9/.10` 深度档/视觉落地（见上节），本批审计的测试项已并入。
- 开发资料口径统一：新资料优先落 `资料/{版本或主题}/` 或 `_通用/`，无法判断时可临时落根并标「待分类」，确认后同批归位；消除「文件 → 资料根」与「禁止平铺」的冲突。

### Fixed

- 开发完成门评审结论解析：`未通过/不通过/部分通过/需修` 不再被 `通过` 子串误放行；要求 reviewer/implementer 字段且不得同人。
- 测试报告门结论解析：`未通过/部分通过` 不再被 `通过` 子串误判为 PASS；评审复核节增加 `未通过/不通过/未复核` 负向判断。
- 根 README 移除过期版本/数量徽章与「先完整阅读 AGENTS」误导；三包 README/结构计数、`§0.2-11～12`/`§0.3-10～12` 等错误引用校正。
- 修正 `测试规范/规则/专项/多Agent与输出.md` 合并行与失效 `§0.3-4` 引用；修正 `agents/testcase-reviewer.yaml` 裸 `Invoke-Gate.ps1` 引用。

## [Unreleased]

### Added

- 三包补强全局体验规则：界面减法（删冗余标语/说明/副标题/次要标签；删后不清楚重设计布局，不加回说明）；UX/DX/AX 三维同向，任一不得净退化。
- 开发规范新增「开发阶段不背旧数据」：`项目档案` 标记 `项目阶段=开发` 时直接改结构/删旧数据/重建夹具，用新数据测试；禁旧数据兼容分支/双写/回填；上线/真实数据/外部契约例外。
- 开发 `项目档案` 增加 `项目阶段` 与数据/夹具重建命令；前端设计 QA、方案/设计模板、代码评审、工程质量条同步。

### Changed

- 开发代码评审由五轴扩为六轴（新增体验三维）；开发阶段旧数据兼容检查纳入评审。
- 产品/测试技能与模板补充文案减法、三维体验检查项。

### Removed

- 无。

## [2026.10.27.7] - 2026-10-27

### Added

- 产品作者侧闭环：【完稿自检摘要】必落盘；`gate: product-prd`（`prd_structure_required`）；PRODUCT-VER-09/10。
- **P1↑（elevated）**：权限/资金/隐私/不可逆数据/主数据 → 自检与结构门按 P2，可免独立审。

### Changed

- P2+/P1↑/拟定稿：A/B 均须 `-Mode prd` 非 BLOCKED 才可定稿/交开发（不再“建议跑”）。
- `prd-writing` §9、`prd.yaml`、门/验证规则/收尾骨架/AGENTS §0.4 同步。

### Removed

- 无。

## [2026.10.27.6] - 2026-10-27

### Added

- 测试：`技能/test-artifact-review`——计划/分析短表/功能/接口/探索/发布前统一 A/B；选 B 强制【自主分析】+ 自定义焦点。
- 计划步接入 `select_review_mode`；`review-cases` 扩为多轨资产评审。

### Changed

- 纠正「测试只硬闸功能用例」过窄；机检仍仅功能轨选 B。
- `testcase-reviewer` / `工作流.md` §2.5 / 门词表 / AGENTS 路由同步。

### Removed

- 无。

## [2026.10.27.5] - 2026-10-27

### Added

- **三包统一**落地文档门 `select_review_mode`：产出后 STOP 二选一——A 自行评审通过（HUMAN_APPROVED）｜B AI 独立评审；未选不得宣称通过/定稿/实施/进 P2。
- 产品：`技能/artifact-review`；PRD/产品计划/设计评审/**交付计划**/实质变更重审接入选择门；选 B 才跑 `-Mode review`。
- 开发：`技能/design-doc-review` + `agents/doc-reviewer.yaml` + 步 `review-docs`（方案/基线/ADR/前端设计说明）；与代码 `review` 分轨。
- 测试：用例评审步先问 A/B；选 B 才 `case-review` 机检。

### Changed

- 产品/开发/测试 `规则/门.md`、AGENTS、相关 workflows 同步；方案评审口令改挂 `review-docs`；change/defect 重审与 deliver 排期同步 A/B。
- 整合 shinpr/prd-reviewer、headout l1-reviewer、NIST/ETIS、IEEE 1028/ISO 20246、既有 QA skills 方法。

### Removed

- 无。

## [2026.10.27.4] - 2026-10-27

### Added

- 测试规范主链新增独立步 `review-cases`（用例评审）；角色 `agents/testcase-reviewer.yaml`；技能 `技能/testcase-review`（A1–A6/S1–S6 企业量规，整合 ISTQB CTFL 静态测试、ISO 29119-3、fishzjp/qa-skills、casely、saleem-daqa、petrkindlmann/qa-skills、fugazi ISTQB static-testing 等方法）。
- 机器门 `Invoke-Gate.ps1 -Mode review` / `gate: case-review`；`confirm_review` HITL；评审记录模板升级为量规+严重度表；验证规则 TEST-VER-09。

### Changed

- 测试主链：analyze→plan→generate→**review-cases**→execute→report；口令「用例评审」改挂 `review-cases`（不再挂 generate）；T1+ 功能进 P2 前须评审放行；生成写手不得自审自放行。
- 测试 `testcase-agent`、playbooks/generate、门词表、读取索引、计划模板 P2 入口、能力注册表 `qa-skills` 同步。

### Removed

- 无（旧「口令横切挂 generate」语义由独立步取代，口令仍可用）。

## [2026.10.27.3] - 2026-10-27

### Added

- 三包收尾骨架新增“表达与编号”规则：汇报层可保留技术/编号代号，但首次出现必须带中文描述；明细层禁止裸编号。
- 第 4 点改为“假设与未决项（待你确认）”唯一入口：需拍板表 + 默认项 + 回复格式；第 1 点不再写待确认指针。
- 三包验证回执改为中文结论（通过/部分通过/阻塞/未验证；产品：可定稿/草稿/阻塞；测试：可准出/有条件准出/不准出/阻塞），机器代号放括号。
- 第 6 点扩展为“当前 / 下一步 / 建议与理由 / 完成标志”。

### Changed

- 三包 AGENTS：收尾改为“中文回执 → 第1点纯执行汇报 → 第4点待确认表 → 第6点进度与下一步”；修正产品/测试待确认落盘路径。
- 产品/测试 workflows：wrap/report 步统一指向第 4 点；修正“待确认放六点后”的顺序矛盾；测试 `execute` 的 `when` 词表统一为已声明的 `exploratory_mainread_missing`。
- 开发 `report_lint.py`：支持中文回执解析；检查第 4 点待确认表；允许“部分完成/阶段完成/文档阶段完成/部分验证/有条件通过”等限定措辞。
- 开发/产品/测试 `规则/核心/验证规则.md`、`验证/README.md`：补中文回执与机器状态映射。
- 版本单点：产品/开发 `2026.10.27.3`；测试 `2026.10.27.4`（并行“主链强制用例评审 + 企业量规门”）；母版取最高 `2026.10.27.4`。

### Removed

- 收尾骨架第 1 点前的独立 `【待你确认】` 块（改为第 4 点内）。

## [2026.10.27.2] - 2026-10-27

### Added

- 三包收尾骨架新增 `【待你确认】` 决策块：`ID/事项/选项/建议/分析/不决定默认`；无则写「无」；第 1 点前必须出现。
- 澄清规则新增「不确定项分流」：阻塞项即时问（0～1 个），非阻塞项登记后收尾集中输出，禁止散问。
- 开发 `验证/tools/report_lint.py` 检查 `【任务收尾】` 是否含 `【待你确认】` 块。

### Changed

- 三包 AGENTS：先写验证回执 → 再写 `【待你确认】` → 再写六点；第 4 点只引用块，不重复列表。
- 产品/测试 workflows 的 wrap/report 步骤显式要求 `【待你确认】` 块；产品 intake/测试 analyze 指向澄清 §2.1。
- 三包收尾骨架：决策表最多 5 项需拍板；每项必须有互斥选项、建议、影响/默认；`[阻塞]` 只标不决定就无法继续的项。
- 读取索引 wrap/commit 指向收尾骨架 `§0.5/§2`（测试轨 `§0/§2`）。
- 版本单点三包统一 `2026.10.27.2`。

### Removed

- 无。

## [2026.10.26.5] - 2026-10-26

### Changed

- 三包根 `activeContext.md` 统一为分节骨架：总览 → 已启用包分节（产品/开发/测试）→ 跨包同步 → 运行时；单包只建本包节，多包只补本包节，禁止整文件覆盖。
- 接入免检标记统一为 `产品|开发|测试规范接入：已完成`；测试废除现行写入 `landing=ok`（读时兼容旧标记，写入时改写）。
- onboard/AGENTS：明确只改本分节与本包运行时行；与工作日志/根 CHANGELOG 边界写在模板导语。

## [2026.10.26.4] - 2026-10-26

### Added

- 三包统一 `工作日志.md`（模板：岗位里程碑侧记，索引 + 事件条；人类可查）；落点 `产品/` · `开发/` · `测试/`。
- 开发发版仍写根 `CHANGELOG.md`（给人看）+ `发布说明-{版本}.md`（单版叙事）+ `开发/工作日志.md`（本轨里程碑）。

### Changed

- 取消产品/测试包内 `CHANGELOG.md` 模板与写入；旧文件接入时改名迁移为 `工作日志.md`（须确认）。
- 产品/测试/开发**禁止**向根 `CHANGELOG.md` 补岗位内容；根仅开发维护项目发版史。
- 文档治理明确三分法：根 CHANGELOG ≠ 工作日志 ≠ 计划执行日志 ≠ 发布说明。

### Removed

- 产品/测试 `CHANGELOG模板.md`（改由 `工作日志模板.md` 承接）。

## [2026.10.26.3] - 2026-10-26

### Added

- 多包 `项目资料/` 明确为共享收件箱语义：≥2 包按需创建、只放外部主副本、放入≠自动分发；当前包扫描→确认→登记索引→只吸收进本包；其它包日后引用、不自动跑。
- 文档治理「互引（可选）」：有对等目录可读 `产品/…` `开发/…` `测试/…` 或交接路径；缺对等包一句缺口，从不强制安装。

### Changed

- CHANGELOG 方案 D 写清：根 `CHANGELOG.md`（开发发布真值）+ `产品/CHANGELOG.md` + `测试/CHANGELOG.md`；年归档各自 `_归档/changelog/`；产品/测试不建根 CHANGELOG。
- 收取落点提示：多包 → `项目资料/`；单包 → 本包 `资料/`（intake / change / testing / change-intake）。
- 根 README「单包/多包/交接」：工作根硬编码、CHANGELOG D、共享收件箱吸收、交接同仓可读不转发 / 跨仓文件夹·ZIP、回执可选。
- 交接便携口径：始终生成包；同仓就地读；跨仓外送；回执可选但未回执不得称已交接；三包 README / `prd.yaml` 去掉「整包复制给」旧措辞。
- 开发轨工作文档根统一为 `开发/`（取消可配置文档根占位）；工作文档根默认 `产品/` · `开发/` · `测试/`；已有 docs/ 等用 keep/mix/replace 兼容，映射记档案。`Initialize-Docs.ps1 -DocsRoot` 仅兼容旧仓，非第三套概念。
- 文档分层与读取预算：常驻规则 ≤3k、AGENTS ≤5.5k、参考手册 ≤10k、技能 ≤4.5k、单步读取 ≤8k；参考手册统一标 `读取级别：参考`，只读当前 step 节。
- 去重与排布：开发 `工作流.md` 删除标准目录树（指向 `文档治理.md`）；测试 `工作流.md` 删除速查表（指向 workflow/多Agent/脚本执行）；删除 `资料治理.md`/`文档生命周期.md` 兼容指针；`缺陷文案模板.md` 移入 `规则/模板/{组}/`。
- 测试 `AGENTS.md` 压缩常驻集：T0～T3 移到 `工作流.md` §1.2，交接硬约束改为指针；README 增加“文档分层（按需读）”。
- `Test-DocHygiene` 区分常驻/参考/模板/技能预算；三包当前 0 warning。
- 去重：`验证/README.md` 状态表改为指向 `规则/核心/验证规则.md`；读取索引写入固定读序与单步 8k 硬上限；`缺陷文案模板.md` 进模板索引。
- 目录结构（2026-10-24）：三包 `规则/` 收敛为四个常驻入口（`读取索引/门/工作流/文档治理`）+ `核心/协作/缺陷/专项` + `playbooks/模板/tools`；模板按 `00～90` 生命周期分组（产品 36 / 开发 31 / 测试 23），索引迁至 `规则/模板/模板索引.md`；产品版本目录改为 `01-需求与定义`～`06-复盘`；开发缺陷评估移至 `00-项目治理/缺陷评估/`；测试新增功能测试模块规模阈值。
- 自检同步：`Test-DocHygiene` / `Test-Template` / `Invoke-TestWorkflow` 改为递归扫描与新路径；三包自检全绿（产品 677/185，开发 1027/238，测试 749/260）。

## [2026.10.24.3] - 2026-10-24

### Added

- 三包新增 `规则/协作与交接.md`：角色/RACI、协作节奏（Three Amigos/提测/准出/发布/复盘）、发出/接收交接矩阵、交接包规范、回执/退回/超时、C0～C3 变更分级、重规划触发、文档同步矩阵、计划回写。
- 三包新增 `workflows/handoff.yaml`：`status`（待回执/超时/阻断）、`send`（生成交接包）、`receive`（核对+回执+更新计划）、`change_send`（变更通知）、`change_receive`（影响分析+适配）、`replan`（重基线+通知）、`wrap/commit`。
- 三包新增交接模板：`交接包说明模板.md`、`交接清单模板.md`、`接收回执模板.md`、`交接台账模板.md`；新增 `validate_handoff.py`（必带文件/元数据/清单路径/包 ID 校验）。
- 计划模板补全：产品计划新增 §3.2 协作接口、§12 交接台账摘要、§13 计划自适应；开发计划新增 §2.3 协作接口、§9.1 变更分级/重规划、§15 追溯扩展；测试计划新增 §17 协作交接、§18 计划自适应；测试报告新增 §12 交接与回执。
- 交接包目录：`产品/交接/{HO-ID}/`、`{文档事实源目录}/交接/{HO-ID}/`、`测试/交接/{HO-ID}/`；收到的包落各自 `资料/交接/{HO-ID}/`（只读）；台账 `交接台账.md` 为唯一登记。

### Changed

- 产品 `prd` 增加 `prd.handoff`（PRD 定稿→REQ 包），`prototype.handoff`（→DES 包），`deliver`/`change`/`defect` 增加 PLAN/UAT/REL/CHG/BUG 包；开发 `control`/`change`/`iterate`/`intake`/`defect-fix`/`release`/`retro` 增加接收/发送/回执/变更适配；测试 `testing`/`defect` 增加提测签收、报告包、缺陷包、变更包。
- 三包 `AGENTS.md` 新增协作与交接硬约束（包/回执/三选一/C0～C3/计划同轮回写）；`规则/门.md` 新增 `confirm_handoff` 与 `handoff_send_required`/`handoff_change_substantive` 条件；`规则/读取索引.md`、`模板索引.md`、`文档治理.md`、`工作流.md`、README 同步。
- `已发送 ≠ 已交接`：未收回执只能报“待回执/已发送”，不得写“已交接/已接收”，不得把提测、UAT、发布、变更实施标为完成。
- 单包仍独立：接收方未装包时按普通文档阅读并按回执模板回复；不要求额外协作目录或合同文件。

### Verification

- 三包 `Test-Template.ps1` / `Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs` 全部通过（产品 664 引用/186 锚点；开发 1006/238；测试 737/257）。
- `Test-DocHygiene.ps1`：0 error；仅保留既有规则/AGENTS token 预算与孤立模板警告。
- `validate_handoff.py` 用临时夹具验证：完整包 `HANDOFF_VALIDATION_OK`。

## [2026.10.24.2] - 2026-10-24

### Fixed

- 开发门：运行态改为 `.gate/开发规范/`；删除包内 `.state`/`project-profile.json` 回退；任务开始 `-StartTask` 校验 `task_id`；空 diff=`NOT_VERIFIED`、dry-run=`DRY_RUN`；验收证据必须存在；L2+ 核 `process.review`，L3 核 `security`/`rollback`；Git 中文路径与 BOM 修复；`report_lint` 允许“未完成/未通过/未修复”。
- 产品门：UAT 解析 §2 表并对照 PRD AC；评审必须有唯一清单结果/结论；`release` 与 `new-product.deliver` 增加 UAT 门；`onboard` 标 `chain: full` 并去掉 activeContext 预填标记；P0/P1 补 `decide`；PRD 状态机改为有状态才要求；`source_of_truth`/追溯行/gate_id 一致性校验；BOM 修复。
- 测试门：台账增加 `用例优先级`/`缺陷优先级` 列，P0 判定不再失效；报告门对账计划/稳定冒烟清单的 P0 缺失；新增 `-Mode coverage`；`writeback` 只写 `writeback.json`，不覆盖 report；覆盖解析只读用例文档、排除证据目录；报告回执与 verdict 校验；配置模板去掉项目硬编码。
- 自检：实例路径（`.gate/`、交接实例文件等）不参与包内引用检查；`Test-DocHygiene` 增加规则/AGENTS/技能 token 预算警告；Python 自检统一 `-B`；复制说明排除 `.state/.gate/__pycache__`。
- 保留并兼容工作区 handoff 功能；本次只修其自检引用/能力声明，不改其流程语义。

### Verification

- 三包 `Test-Template.ps1` / `Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs` 全部通过。
- 临时夹具：开发空 diff→NOT_VERIFIED、dry-run→DRY_RUN、旧 `.state` 不读取、缺证据→BLOCKED、L2 缺评审→BLOCKED；产品 UAT 缺 AC→BLOCKED、完整 AC→READY；测试计划有 P0/台账缺失→FAIL、P0 失败→FAIL、writeback 不覆盖 report。

## [2026.10.23.7] - 2026-10-23

### Fixed

- 产品门：P0/P1 轻量 PRD 不再被全量 PRD 结构校验误判；新增 `prd_level: light` 最小结构校验与 `SELF_CHECKED` 免独立评审。P2+ 定稿改为“结构门→评审门→回填 `gate_id`→复跑结构门”，`gate_id` 由门回执生成，不再手编。
- 产品门：占位符检测覆盖 `{主题}` 等模板占位（排除代码块/Mermaid），避免 APPROVED 文档带占位符；迁移步补 `confirm_docs_migration`。
- 开发门：聚合任务清单内多张验收表；发现验收清单为空/不可解析时 L1+ 非纯文档变更直接 BLOCKED；前端 `design-qa.md` 必须填满 15 项结果/证据且结论非“不通过”；占位符检测排除代码示例，避免误伤 API 文档。
- 开发流程：`review` 不再提前读取尚未生成的完成门回执；`iterate.review` 用 `review_required` 精确触发；`defect-fix` 等待产品回复时不再误走 `wrap`。
- 测试门：排除 `_归档`/`.draft`/`资料` 台账；报告 `准出评估` 必须唯一且与 P0/未执行/计数一致；未执行>0 不得 PASS；功能测试资产必须有设计点覆盖映射；证据路径按多级祖先解析；`writeback` 只核回执，不强制计划/台账。
- 开发门不再提供无实现的 `report`/`writeback` 模式（报告对账仍由 `Test-Report.ps1` 负责）；三包门回执新增 `gate_id`，读回执前核对 `package`/`mode`，避免多包互相覆盖。

### Verification

- 三包 `Test-Template.ps1` / `Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`、`Test-DocHygiene.ps1` 全部通过。
- 临时夹具验证：轻量 PRD → READY；多任务验收表 → 2/2；空验收清单 → BLOCKED；前端 QA 15 项未填 → BLOCKED；测试未执行 + 报告写通过 → FAIL；归档台账不参与计数；证据全路径可解析；`writeback` 无计划/台账可 PASS；产品/开发门回执被跨包误读 → 报告 lint 失败。

## [2026.10.23.6] - 2026-10-23

### Added

- 三包新增 `验证/` 轻量验证层：`README.md`、`检查矩阵.yaml`、`Invoke-Gate.ps1`、机器门脚本；每包独立、无共享运行时依赖。
- 开发包：完成门 `completion-gate`（`verify`/`gates`），读验收清单/diff/证据，写 `.gate/completion.json`；前端检查矩阵、15 项验收清单、Playwright/axe 模板、报告 `Test-Report.ps1`。
- 测试包：报告门 `report-consistency`，读计划/台账/报告，检查计数一致、P0、证据、覆盖缺口、回写回执。
- 产品包：PRD/评审/UAT/变更/回写门，检查结构/追溯/TBD/独立评审/联动闭合/平台回执。
- 三包新增 `规则/20-验证.md`、`规则/30-规则治理.md`；收尾/报告模板增加【验证回执】；PRD/评审/UAT 模板增加 `review_status`/`verdict`/`gate_id`。

### Changed

- 澄清停止条件从“≥95% 置信度”改为“需求理解包 + 缺口清单无实质缺口（或剩余缺口被接受为假设）+ 用户确认”；95% 仅作参考，不作为停止条件。
- 澄清流程改为“先分析后提问”：技术/方案细节由 AI 查规则、技能、代码、文档后给建议；只问影响意图/范围/验收/风险的问题；首轮 0～1 问、总≤3；确认后执行。
- 开发 `change.verify` / `iterate.gates` 改为 `verifier-agent` 独立验证；`project-gates` 保留，新增 `completion-gate`。
- 开发 `AGENTS.md`、产品/测试 `AGENTS.md` 增加验证/汇报硬约束；读取索引增加验证行。
- 文档/模板引用同步；`.gitignore` 忽略 `.gate/` 与 `验证/.state/`。

### Verification

- 三包 `Test-Template.ps1` / `Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`、`Test-DocHygiene.ps1`、`validate_workflow.py` 全部通过。
- 新增门已用临时夹具验证：开发 docs-only → COMPLETE；无命令代码 → BLOCKED；测试台账/报告一致 → PASS；P0 失败 → FAIL；产品独立评审 → READY；自评 → BLOCKED；PRD 模板占位符 → BLOCKED；报告假完成措辞 → REPORT_LINT_FAIL。

## [2026.10.23.5] - 2026-10-23

### Added

- 三包统一 `CHANGELOG模板.md`：项目根 `CHANGELOG.md` 记录本项目版本/迭代、显著变化、迁移与验证；产品/测试包首次具备独立创建能力。
- 产品 `onboard` 创建 `CHANGELOG.md`（无则建、有则保留）；`plan.publish` 记录版本/迭代与链接，`deliver.release` 记录发布/关闭与变化摘要。
- 测试 `onboard` 创建 `CHANGELOG.md`；`testing.report` 记录测试版本/范围/准出/遗留与报告链接。
- 开发沿用既有 `onboard`、`control.wrap`、`iterate.wrap`、`release.record` 更新 `CHANGELOG.md`；模板与产品/测试保持一致。

### Changed

- 根 `CHANGELOG.md` 收敛为项目自身记录：版本总览 + Keep a Changelog 分类 + 迁移/验证；去掉版本记录分工、参考依据等说明性内容。
- 产品/测试 README、模板索引、读取索引同步新模板与更新时点。

### Verification

- 三包 `Test-Template.ps1` / `Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`、`Test-DocHygiene.ps1` 与 `validate_workflow.py` 全部通过。

## [2026.10.23.4] - 2026-10-23

### Removed

- 删除独立多包协作层 `项目协作/`（不保留备份），同时移除三包 `AGENTS.md`、README、模板、onboard 与自检脚本中的相关引用。

### Added

- 三包新增 `规则/澄清.md`：统一「理解回执 → 一次一问 → 更新置信度 → 95% 停止条件 → 复述确认 → 落盘」；明确确认门≠澄清、澄清答复≠执行授权，禁一次多问/自问自答/把假设当结论。
- 开发包新增 `技能/product-doc-analysis/SKILL.md`：PRD/迭代方案/文档/页面原型/截图五遍解析（来源→需求模型→原型→一致性→可开发/可测性），输出带引用、冲突表、GAP、假设与置信度的需求理解包；新增 `change.analyze_input` 步与 `confirm_understanding` 门。
- 测试包新增 `技能/test-basis-analysis/SKILL.md`：依据盘点→十要素需求模型→文档/原型/代码一致性→九类歧义→AC 可测性/oracle→TP 追溯；`testing.analyze` 新增理解门与需求模型输出。
- 产品包新增 `技能/customer-needs-discovery/SKILL.md`：角色地图、证据分层、Mom Test 访谈、问题定义、假设登记、需求复述确认；`change.intake` 新增 `confirm_understanding` 门。
- 开发 `需求基线模板` 增加「0.1 来源与理解」；产品 `受理与处置模板` 增加「2.1 需求理解与澄清」；测试 `工作流.md` 分析短表增加需求模型/oracle/追溯字段。

### Changed

- 三包 `AGENTS.md` 的「低风险一次最多问 3 个」改为强制澄清追问环：任何任务先给理解回执，一次只问一个问题，≥95% 且用户明确确认后才产出方案/PRD/用例/代码；L0/T0/P0 也不得跳过（纯机械操作除外）。
- 开发 `change` 增加「产品资料解析与理解确认」步；`requirements/design/implement/review` 增加需求理解包引用、冲突/GAP 继承与需求覆盖核对。
- 测试 `analyze/plan/generate/execute/report` 增加需求模型、oracle 来源、AC/TP 追溯、歧义关闭与报告覆盖；生成前缺模型先补，不直接写用例。
- 产品 `change/prd/new-product/plan` 增加客户需求还原、证据/假设、未确认不排期、PRD 来源可追溯与评审对照。
- 多包改为自动探测：项目根同时存在两个及以上包目录（`产品规范/`、`开发规范/`、`测试规范/`，以各自 `AGENTS.md` 为标志）即启用共享 `项目资料/`、`activeContext.md` 与路由；不再需要 `项目资料/项目协作.md`、额外模板或实例自检。
- 共享资料根 `项目资料/` 改为按需创建，不预建、不强制；单包仍按本包 `资料/` 运行。
- 根 `AGENTS.md` 只做路由：首次接入时按实际包目录补齐已启用包列表，不再写“本会话只启用本包”。
- 三包 `template_version` 更新为 `2026.10.23.4`；根 README 的多包接入、目录结构、FAQ、技能计数（38：产品 12 / 开发 20 / 测试 6）与自检说明同步。

### Migration

- 已接入旧协作层的项目：删除 `项目协作/` 与 `项目资料/项目协作.md` 即可，三包自动接管；不删也不影响（不再读取）。
- 无破坏性工作流变更；现有单包项目的目录与产物不需要迁移。

### Verification

- 三包 `Test-Template.ps1`、测试包 `Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`、三包 `Test-DocHygiene.ps1` 与 `validate_workflow.py` 全部通过；仓库内不再有独立协作层引用（本历史条目除外）。

## [2026.10.23.2] - 2026-10-23

### Added

- 新增 `开发规范/技能/engineering-quality/SKILL.md`：企业级工程质量条、设计/实施启发式、质量属性证据表、12 项评审 rubric。
- 新增 `开发规范/规则/模板/前端设计说明模板.md`：需求/情境 → IA/路由 → 状态矩阵 → 组件/tokens → a11y/性能/兼容/打印 → 交接与验收；含“产品设计输入/保留/优化/偏离”。
- 新增 `开发规范/规则/模板/CHANGELOG模板.md`：项目根长期版本记录骨架（Keep a Changelog + 迁移/验证/文档检查）。
- 新增根 `CHANGELOG.md`：母版仓长期版本与迭代记录首版（回填 2026.10.21～2026.10.23 历史）。
- 新增 `产品规范/规则/模板/开发交接模板.md`：设计意图、必须保留、可优化、未提供、需开发决策、验收对照。
- 产品轨 `prototype-and-interaction` / `ui-visual-design-system` / `prototype.yaml` / `prototype.md` 补设计策略、项目适配、设计系统策略、开发交接边界。
- `开发规范/技能/README.md`、`AGENTS.md`、读取索引、模板索引、workflows、agents 同步挂载新技能/模板。

### Changed

- 重写 `开发规范/技能/frontend-design/SKILL.md`：明确其**按需补充**定位——产品设计完整时直接按方案实现；仅在无原型、原型不完整/仅参考、实现需要补充设计、或需要落地设计系统时使用；已有批准设计不重画。
- `开发规范/技能/frontend-implementation/SKILL.md` 增加“按设计说明实现 + 设计 QA + 设计缺口回写”，禁止绕过 tokens/设计说明。
- `开发规范/技能/solution-design`、`implementation-and-selftest`、`code-review` 统一挂载 `engineering-quality`，避免质量条多处分叉。
- `开发规范/规则/模板/项目档案模板.md` §7.1 增加设计系统/tokens、浏览器矩阵、性能预算、无障碍目标；§9 增加 `CHANGELOG` 与根白名单。
- `开发规范/workflows/` 的 design/implement/review/onboard/control/iterate/release/commit 步同步引用新技能、模板与 CHANGELOG 更新时点。
- 根 `README.md` 更新技能/模板计数、仓库结构、长期记录与归档说明。
- 产品轨 `prototype.yaml` 的 context/visual/handoff 补设计简报、项目适配、设计系统策略与交接边界；`AGENTS.md` 原型纪律增加交接内容要求。

### 迁移与兼容

- 无破坏性工作流变更；现有项目无需搬迁文件。
- 下游项目下次接入/版本关闭时：按模板创建根 `CHANGELOG.md`；已有文档按现有归档规则保持正确。
- 产品交接：下次原型交付使用 `开发交接模板.md`；已有原型可在下一次交接补“必须保留/可优化/未提供”。
- 新技能为增量挂载；未安装任何外部设计/工程工具时，全部按包内技能降级执行。

### 验证

- 该版本改动相关自检通过（开发引用 808 处/锚点 170 处；产品 468 处/117 处；测试 582 处/217 处）；三包 `Test-DocHygiene.ps1` 0 warning；`validate_workflow.py` 输出 `YAML_VALIDATION_OK`。后续澄清追问环接入后的全量结果见 `2026.10.23.4`。

## [2026.10.23.1] - 2026-10-23

### Added

- 三包新增 `规则/读取索引.md`、`规则/门.md`、`规则/playbooks/`、`规则/文档治理.md`、`规则/模板/收尾骨架.md`、`规则/模板索引.md`。
- 新增 `Test-DocHygiene.ps1`（文档卫生/读取预算检查）。
- 拆分产品/开发/测试缺陷协作模板，以及测试计划、环境基线、PRD、开发卡轻量模板。
- 模板索引与读取索引建立，减少“模板存在但没人用/读取放大”。

### Changed

- 三包 `AGENTS.md` 瘦身：产品 195→109 行、开发 267→120 行、测试 224→129 行；输出骨架、门、维护、多包细节下沉。
- 读取预算与按步加载成为默认；重阶段改用 playbook；`hitl`/`gate`/`when` 语义收敛到 `规则/门.md`。
- 三包自检与文档卫生全绿；版本统一 `2026.10.23.1`。

### Fixed

- 修复冲突门与入口不一致；统一收尾输出与「今日工作总结」。

### 迁移与兼容

- 包内结构调整；下游按整包同步，不手工搬规则。
- 旧 `资料治理.md`/`文档生命周期.md` 仅保留指针，实际规则以 `文档治理.md` 为准。

### 验证

- `Test-Template.ps1`、`Test-DocHygiene.ps1`、`validate_workflow.py` 通过。

## [2026.10.22.5] - 2026-10-22

### Changed

- 三包收尾统一为「结论说明体」，新增「今日工作总结」列表输出；`wrap` 与 `commit` 的拟提交展示去重。

### Docs

- `activeContext.md` 记录当前焦点与下一步；历史移入 `_归档/context/`。

## [2026.10.21.4] - 2026-10-22

> 版本号按 10-21 迭代命名，提交日期为 10-22。

### Changed

- 产品轨：条件确认门与收尾闭环强化，减少无效停门。
- 开发轨：入口直达与少问原则；单步入口只执行当前步。
- 测试轨：单步入口与阻塞判定强化。

### 验证

- 三包分别提交：`a07ee3a`（产品）、`7c3a5b6`（开发）、`7f54724`（测试）。

## [2026.10.21] - 2026-10-21

### Added

- 初始化仓库：`产品规范/`、`开发规范/`、`测试规范/` 三套独立包。
- 初始规模：20 条工作流、24 份角色契约、34 个内置技能、70 份模板/脚手架。
- 根 `README.md`、`.gitignore`、`.gitattributes`、LICENSE 与仓库维护脚本。

### Notes

- 初始提交：`cc4e10a`（仓库配置）、`8b51d9a`（产品）、`7f1ab83`（开发）、`c6b8d30`（测试）、`105a14f`（README）。

## 历史归档

| 年份 | 文件 | 说明 |
| --- | --- | --- |
| 2026 | 本文件 | 当前历史较短，暂不拆分；超过约 500 行或跨年时按头部规则归档 |
