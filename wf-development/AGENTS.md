# AGENTS.md

> **用途**：开发协作 AI 入口。  
> **新会话必读顺序（硬）**：入口已是本文 → ① 开局卡 → ② `activeContext` → ③ `global-rules.md` → ④ `workflows/<id>.md` → ⑤ 当前步骤卡 → ⑥ §6 skill → ⑦ 可选 1 模板；未路由时用 §3 口令表。  
> **每轮协议**：先判新任务/续跑/只读 → 新任务重路由并复述 → 首行锚 `route=…|step=…|packet=…|global=ok`（偏离 `global=dev:…`；只读 `mode=analyze`）→ 结束给收口（六点或 2～3 行）。  
> **首轮硬门**：新任务先给【需求与意图理解】（完整档六段/一行档三行）和版本落点（升 patch/并入批次/na），确认后再改文件；用户明确「直接做/不用确认」或纯只读除外。  
> **已路由中段**：`global-rules` 按 §7 重读分级（新会话/换链/规则变更全文；同链中段按节最小集）；每步读当前步骤卡；心跳（`packet=` + `global=ok`）；禁止同时多 packet；本步流程以当前包为准（独立完整，与他步重复 OK），不跳转拼齐；勿通读 `workflow.md`/协作手册拼流程（参考层按节、按需）。  
> **位置**：`wf-development/`。与项目根 `AGENTS.md` 冲突时以根为准；与用户指令冲突见 §0 第 5 条。  
> **template_version**：`2026.11.10.06`  
> **架构**：`workflows/<id>.md`（状态图）+ 步骤卡（编排/门）+ skills（方法闭环）+ verify。  
>
> **完成口径**：只认 `verify/Invoke-Gate.ps1 -Claim` → `CLAIM: ALLOWED`。前端只认**当前步骤包**内「前端硬门」节（无 UI 标 `na`）。

## 0. 开工

> **硬约束全文**：`rules/core/global-rules.md`。本节只补分级与指针，不重复全局规则正文。

1. **中文**；写现行结论。  
2. **短读**：`activeContext` 总览 + 本包进行中运行状态（workflow/state/packet）+ **偏好/洞见/坑 ≤3 行**（开局卡 §1；写法 `context-memory.md`）；有 `project-profile.md` → §1+§2 表（每新会话一次）。L2+ 有计划才读 `development-plan.md`。  
3. **接入**：`wf-development onboard: done` 则跳过，否则按 onboard-agent 一次判定。  
4. **行为契约**：理解/澄清/检查/择优/冲突按 `rules/core/global-rules.md`（遵守全文；重读见 §7）。  
5. **覆盖优先级**：只认 `rules/core/global-rules.md` §11。  
6. **读取**：分级读链（global-rules §7 主从）；YAML 非规则正文；技能按步骤包 §6 索引（同时 ≤1）。  
7. **契约**：`rules/core/global-rules.md` §1/§4（开工档位【需求与意图理解】+【动作前分析】；只读分析）。  
8. **心跳**：`rules/core/global-rules.md` §8（切步/过门一行锚）。

### 0.0 事实与文档

事实可核实；待确认禁升格；正式资产只写现行。细则 `doc-quality.md`。版本分离见 `versioning.md`。

### 0.1 执行路径

> L0～L3 仅为内部风险标签，不由 AI 选档；**轨道只看正式协作/正式流程，体量/风险不换链**（`lightweight.md` §1～§2）。

| 路径 | 触发 | 完整任务必走 | 可省 |
| --- | --- | --- | --- |
| 文档 | 团队正式迭代内的纯文档/文案/注释 | clarify→implement→verify→closeout | 需求/方案/任务/评审/测试命令（门只核 docs-links/docs-placeholders） |
| 自包含完整链 | 无正式迭代/正式协作（单人或团队，含大改动/高风险）；需正式发布/QA/交接 → 完整链 | `solo`：产品分析→方案→评审→完整开发→评审→测试→完成门 | 无（产品分析/评审/测试不省；正式协作产物有则消费） |
| 标准代码 | 团队正式迭代内的代码/配置变更，单点/≤3 文件/≤1 模块，且不改 API/数据模型/权限 | clarify→implement→verify→closeout | requirements/design/review-docs/plan/review（须记录理由与风险接受人） |
| 完整交付 | 团队正式迭代/正式协作内的 >3 文件 / >1 模块 / 新功能/接口/数据 / 改 API·数据·权限 | clarify→requirements→design?→review-docs→plan→implement→review→verify→deliver→closeout | 仅 `when` 为假的步可跳，收尾 `skip=` |
| 高风险 | 团队正式迭代/正式协作内的权限/资金/迁移/公共 API/破坏性；或需要正式安全/发布审批 | 完整交付 + 独立审 + 安全 + 回滚 + 发布审批 | 无 |
| 缺陷 | 平台缺陷/修复# | `defect-fix` | 无平台→change |

**L1 单点**：`plan` 步不适用 → `clarify` 产开发卡（含验收/SC，模板 `rules/templates/30-planning-tasks/dev-card-lite-template.md`）；`implement` 前 SC 差集=0。  
**轨道**：只看正式协作/正式流程；无正式协作的大改动/高风险仍走 `solo` 自包含完整链，按 `lightweight.md` §2 提高产品分析与测试证据，不换链。  
**不确定**：是否正式协作拿不准 → 先问 1 个关键问题；不得静默把自包含链降为只开发；用户明确要求正式流程才转完整链，并记 `deviation=`。YAML `when` 不满足可跳过相应步，但须在收尾 `skip=` 记录理由。  
**所有路径**：首轮理解与确认不可省；「可省」只指后续需求/方案/评审/提测等步骤，不含 clarify。  
**走链**：路径表是完整任务链/能力边界；单步口令按「入口即止」只做该步；完整任务用「按链/按计划/继续」推进到下一个门/停点。不得无提示断链，也不得越过门自动跑完。「按开发计划执行」只做 `control/run` 切包，不把 `control` 沿表推进到 `sync`。

### 0.2 确认门 · 澄清

步骤门只认 YAML `hitl*`；开局门 `confirm_task_intent` 见 `gates.md`（不依赖 step）；开工档位/读链只认 `global-rules.md`；澄清**方法**按需读 `clarification.md`（参考层）。理解包 §0 必填。

### 0.3 硬红线

只认 `rules/core/global-rules.md` + 当前步骤卡硬约束/做法（有 UI 遵守包内「前端硬门」；无 UI 标 na）。失败同方案 2 次换路径。

### 0.4 验证与汇报

完成只认 `-Claim` → `CLAIM: ALLOWED`（`global-rules.md` §9）。细则随当前步骤包 / `verify`，开局不预读。

### 0.5 工程与执行

实施、自验、提交以**当前步骤包** §5/§6 为准；默认只提交。开局不预读 iq / workflow / handoff。

## 1. 接入

实例：`project-profile.md` + `activeContext.md`；工作根 `{workroot}/`；原件根 `inbound/`。口令「接入/档案/文档树」→ `onboard.yaml`。细则 `doc-governance.md` §2.4。

## 2. 收尾

骨架：`rules/templates/90-handoff/closeout-skeleton.md` §1 通用占位（按项目事实填；禁照抄他例；缺项=未收尾）。提交/推送/部署分门确认；默认仅提交。

## 3. 口令 → Workflow（命中即停）

> 表内为常见示例；未命中 → `rules/core/routing.md`。首条须 `route=…|step=…|level=<内部风险标签，按事实推导>|global=ok|reason=…|reads=…|next_action=…`。

| 优先 | 命中 | workflow | 入口 step / 默认 agent |
| ---: | --- | --- | --- |
| 0 | 工作总结/今日总结 | — | `closeout-skeleton.md` §2 |
| 1 | 缺陷修复/指派/修复#；产品回复→`product_decision` | `defect-fix` | defect-fixer |
| 2 | 新文档/变更吸收 | `intake` | scan |
| 3 | 按方案实施/继续迭代 | `iterate` | precheck |
| 4 | 接入/档案/文档树/inbound/README 整理 | `onboard` | 对应 step |
| 4.3 | 技能/能力体检或优化 | `skill-audit` | scope→closeout |
| 4.4 | 导出资料库/发资料 | `materials` | select→… |
| 5 | 提交/推送 | 当前 workflow 末步（`closeout`）或 `change` | 对应角色 |
| 5.1 | 自包含完整链/无正式迭代/轻量开发 | `solo` | frame |
| 5.2 | 轻量方案/只出轻量方案 | `solo` | design |
| 5.3 | 测试/单独实测 | `solo` | test |
| 6 | 常规变更/需求澄清 | `change` | clarify |
| 6.1 | 分析 PRD/方案/原型 | `change` | analyze_input |
| 7 | 出方案/只出方案 | `change` | design |
| 7.1 | 方案/文档评审 | `change` | review-docs |
| 8 | 代码评审 | `change` | review |
| 9 | 提测/发布说明/回滚预案 | `change` | deliver |
| 10 | 发布/上线（生产） | `release` | readiness |
| 11 | 回滚 | `release` | rollback |
| 12 | 复盘 | `retro` | gather |
| 13 | 开发计划/下一步/按计划执行 | `control` | init/sync/next/check/run |
| 14 | 维护/查询 | 本文 + `maintenance.md` | — |
| 15 | 写交接单/交接包/接收/变更/重规划 | `handoff` | compose（默认） |
| 16 | 交接状态 | —（只读） | 直接读 `{workroot}/handoff/handoff-ledger.md` + `activeContext`；不启动 workflow |

**部署**：裸「部署」先判环境；test/staging≠S8；prod→`release`。提交/推送≠部署。  
**缺陷批入口不豁免开工门**：「指派给我」「我的待修」「修复#N」「#N」走 `defect-fix`，但须先输出【需求与意图理解】并等确认；未确认不得拉单后直接改码。仅「一次性/直接跑完/中途不停」可免等待（理解照常先输出）。  
**续跑有计划**：「下一步/继续开发计划」优先 `control`。  
**单步口令即停**：口令明确只做单步（只出方案/只出轻量方案/只评审/代码评审/方案评审/只提测/只出清单）时，执行到该步产出完成即停（不含提交/推送/部署/回写）并按收尾骨架输出；其余按链图「推进」继续。「按开发计划执行」只切到目标步骤卡，不沿 `control` 表继续。`onboard` 全链仅接入/重新接入/基线/装配能力入口；资料/文档治理只做该步+收尾。  
**路由消歧**：裸「提交」按当前 workflow 末步；只有交接包内的提交才走 `handoff`。裸「方案/出方案」走 `change.design`；点名「轻量」才走 `solo.design`。**发资料 vs 交接**：「发资料/导出」指整库或资料包（`materials`）；把某份文档交给具体角色（确认/知会/提测）走 `handoff.compose`。

## 4. 维护

改开局卡 → `rules/core/cold-start.md`；改前端硬门真源 → `frontend-gate.md` 后须 `build_step_packets.py` 重生包；改不变量/口令 → 本文；改步骤 → `workflows/` + `rules/packets/`（改后跑 `build_step_packets.py`）；改心跳 → `rules/core/global-rules.md` §8；自检 → `maintenance.md` §2 + `Validate-StepPackets.ps1`。

## 5. 文档治理（摘要）

工作根/原件根/换迭代：`doc-governance.md`。根 `CHANGELOG.md`=产品发版史；`{workroot}/work-log.md`=岗位里程碑。

## 6. 技能与能力

命中步必读 `skills/<name>/SKILL.md`（先读「必做」区）。能力实例 SSOT=`{workroot}/capabilities/00-能力清单.md`。

## 7. 多包

单包独立为默认；缺他包不阻塞。一次会话只跑一个包 workflow。歧义定包先查 `wf/AGENTS.md` 意图→包；无该文件时用兜底：产品缺陷评估/平台产品单→产品；修代码/开发缺陷流→开发；交平台/测试回归→测试；发布=业务上线/UAT→产品；发布=部署/回滚→开发；发布=准出报告→测试；下一步/继续→`activeContext` 当前包分节（无焦点一问）；提交/推送/交接→当前会话已绑定包（未开跑一问）。无法唯一则一问。多包应 onboard 生成 `wf/AGENTS.md`。

### 7.1 单包自带产品/测试切片（无独立角色或自包含完整链）

> **正式协作/迭代**（产品/测试按迭代/版本正式介入）走完整链，以对方职责为准；**无正式迭代/正式协作**（单人或团队，含大改动/高风险）走 `solo` 自包含完整链，产品分析与测试由开发自代行；大改动/高风险按 `lightweight.md` §2 提高严谨度。
> **触发**：无独立产品/测试角色、未装对应包，或无正式迭代/正式协作时启用；有独立角色且已按迭代/版本正式介入本轮交付 → 不走本节。
> **口径**：不拥有测试计划库/版本准出；不得写「已准出」。轨道与严谨度见 `rules/core/lightweight.md` §1～§2。

开发包单独落地时，产品与测试的最小职责由开发自代行，**内容全部在本包内**：

- **产品**：需求/范围/AC/影响面/非目标/风险；输入含文档/原型 → `product-doc-analysis`；方向不清列选项+推荐；不是只开发。用本包 `requirements-and-spec` / `product-shaping` / `acceptance-and-launch`。
- **测试**：分析/计划（`solo.test_plan`）→ 执行 → 报告；AC 走查/P0/P1/P2/覆盖/证据/缺口；大改动/高风险全节 + 独立 verifier；用本包 `test-design-and-execution` / `implementation-and-selftest`。不代写版本级测试计划/准出结论。
- **评审**：`solo.review_docs`（条件）审方案卡/验收表/用户版；`solo.review`（条件）审 diff/AC/SC/前端产物；L1+ UI 命中前端硬门 A 级/L2+/高风险/新功能 → true；L0/L1 小改且未命中 A 级可 false + 理由；不冒充已评审。
- **链路**：产品分析 → 方案 → 评审 → 完整开发 → 评审 → 测试 → 收尾；产物按 `10-requirements`/`20-design`/`40-tasks`/`50-verification`/`60-release` 落位。
- **有独立产品/测试且已按迭代/版本正式介入本轮交付时**：以对方职责为准，开发只做本地自测 + 部署冒烟；无正式迭代仍按本节由开发补产品分析与测试。

