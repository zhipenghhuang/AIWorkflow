# AGENTS.md

> **用途**：开发协作 AI 入口。新会话读 §0；命中口令 → `workflows/*.yaml` 当前 step → `rules/read-index.md` 当前行 → 当前 `agents/*.yaml`。已路由同会话中段只靠 `rules/core/rule-anchor.md` 心跳，不重读本节全文。
> **位置**：`wf-development/`。与项目根 `AGENTS.md` 冲突时，以项目根为准；与用户指令冲突时见 §0 第 5 条（可覆盖）。
> **template_version**：`2026.11.03.23`（单点：包内版本以本文为准；门面事件同步 doc-facade-sync + 入口/读取链修正）。
> **架构**：Workflow + Agent + rules/gates.md · rules/read-index.md + skills / capabilities + 验证层 + 开发计划控制面；落地文档 `review-docs` + `select_review_mode`（自行｜AI，仅完整档），代码审仍走 `review`。
> **分层**：本包=通用开发规则；`project-profile.md`=项目事实；根 `AGENTS.md`=挂载 + 项目自写额外要求（母版不规定偏好正文）。

## 0. 开工（每任务）

1. **中文**：对话与结论用中文；写现行结论。
2. **activeContext + 项目身份 + 开发计划（硬短读）**：先按 `rules/doc-governance.md` §2.4 定位工作根（项目档案声明优先）；同 id 双份 → 停问。再读 `activeContext.md` **总览（必填）** + `## 开发` 的 `### 进行中`（含 `rule_card`）+ 跨包同步；先按 `进行中` 报备（2～3 句），无则补建本包节。**同轮项目身份（每新会话一次）**：有 `project-profile.md` → 只读 §1 + §2 表；无或资料不足 → `rules/core/routing.md` §5 升级补强并先回写。空壳/占位/命令不可用必须升级。总览须含一句话定位（已接入禁长期「无」）。任务开始/状态变化/阻塞/收尾更新本包进行中（只读分析除外，见执行契约 §1.2）。**三处同拍**：阶段/门/焦点/下一动作语义变化时按 `rules/core/execution-contract.md` §4 规则 7 同步；语义未变可只改进行中。**门面同步**：仅当版本 bump / 迭代关闭 / 发布上线 / 对外可见事实变时按 `rules/core/doc-facade-sync.md`（禁每轮全扫 README）。收尾只改本包分节；多包禁改他包。L2+ 读 `{workroot}/development-plan.md` 报备阶段/门/下一步。
3. **接入状态（一次判定）**：运行时有 `wf-development onboard: done` → 跳过落地检查；无标记 → 按 `agents/onboard-agent.yaml` 判定一次，具备则静默打标，不具备则走 `workflows/onboard.yaml`。`Test-Template.ps1` 只在改包/点名时跑。
4. **独立判断**：不迎合；先查错误前提/逻辑跳跃/信息缺失；数字/结论尽量核实来源；用户有误直接指出；主动提醒忽略的变量、成本与偏差。**方案择优（硬）**：不适配/高风险/明显更差 → 依据+主推（可 1 备选）供确认，禁静默照做。用户按第 5 条二次坚持 → 以用户为准并记 `deviation=`。
5. **冲突与覆盖**：默认按本包规则与红线。用户指令冲突时：①不执行冲突项；②说明风险与替代；③用户再次明确选择 → 以用户为准。收尾 `deviation=` 如实。无冲突：用户明确指令 > 项目根 `AGENTS.md` > 本文 > 当前 agent 契约 > project-profile.md 技术要点（若有）。**拟改与现行代码或 CI 稳定口径冲突 → 先指出再改，禁静默覆盖。** 红线默认可被用户二次明确覆盖。
6. **读取协议**：

| 场景 | 读什么 |
| --- | --- |
| 新会话 / 同会话中段 | 读序、读取预算与只读范围只认 `rules/read-index.md` |
| 路由未定/首条 | 本文 §3 口令表或 `rules/core/routing.md` → 再按上行走已路由；多包歧义先查 `wf/AGENTS.md` **意图→包** |
| 有门/写 YAML | `rules/gates.md` 当前行；不通读全表 |
| verify/收尾 | `verify/README.md` + `rules/core/verification.md` + 检查矩阵 + 验收清单/证据 |
| 交接/变更 | `rules/collaboration/handoff.md` 当前节 + **默认**`handoff-note-template.md`（升包才读交接包说明）+ `handoff-ledger.md`；变更按 C0～C3 |
| 前后端/交付 | `project-profile.md` §7/§8/§9；技能按步读 |
| 维护/查询 | 本文 + `rules/core/maintenance.md` + 点名 |

同一会话文件未变不重读；后续 delta-only；探查限定目录/关键词。**workflow 文件只读当前 step 块（当前 `- name:` 至下一个），不整文件通读。** **规则阅读不是越多越稳**：读全本会稀释当前步约束。不得为省预算跳过门/证据/红线。标 `读取级别：参考` 的大文件只读当前节。宿主整文件注入本文时：中段仍只认心跳 + `rule_card`，禁止每步当全文必读。

7. **执行契约**：判断模式（execute/analyze/stop）、自主边界、步骤契约、计划同步见 `rules/core/execution-contract.md`。规则是下限不是百科全书；产物/路径未列尽按契约 **§1.3** 归类落盘（禁方便堆、禁为补漏加百科）；低价值步骤可合并/省略；输出/门/证据/红线默认不可省（用户按第 5 条选择覆盖除外）；跳过与取舍写收尾【遵守自检】，不静默偏离。只读解释/对比/诊断按 `rules/core/execution-contract.md` §1.2，不强行进入交付链；用户要详细时用分析说明，不受只读简报 2～3 行限制。
8. **规则心跳（硬）**：触发与一行格式只认 `rules/core/rule-anchor.md`；切步 / 过门前后 / 约每 5～8 轮用户消息须输出【规则心跳】并按需 `rule_card=refresh`。心跳≠收尾自检。

### 0.0 事实与文档（硬规则）

- 事实字段须来自配置/命令/权威文档/用户确认；未核实写「待确认」。同一事实单一来源；正式资产只写现行有效（细则 `rules/core/doc-quality.md` §1 第9条）。**待确认/推断禁升格**进档案真值或提测定论（同文件 §1 第 2.1 条）。
- templates / rules / skills 可适配：先拟改/原因/影响，确认后改本包；能靠产出解决的优先改产出。
- **版本标识分离**：产品/测试/构建/部署/文档版本分开；测试只认实际部署版；项目须暴露版本查看方式。矩阵见 `rules/core/versioning.md`。
- **本期范围须可测 / 开关诚实**：提测环境打开本期已实现能力；前后端同开；声明须接线或债项。细则 DEV-IQ-11、`skills/qa-handoff-and-release/SKILL.md`、提测单模板 §3.1。

### 0.1 任务分级（防过度/不足）

| 级别 | 典型 | 必走 | 可跳过 |
| --- | --- | --- | --- |
| L0 微改 | 单文件/文案/配置；无行为/契约/权限/数据变化 | clarify → implement → verify → commit | 10-requirements/20-design/review-docs/plan/review/deliver/release |
| L1 常规 | 多文件、范围收敛、无跨系统契约 | clarify →（轻量卡）→ implement →（代码 review 按风险）→ verify →（有 QA）deliver → commit | 全量 PRD/ADR；有新方案则问 A/B |
| L2 功能/迭代 | 新功能、跨模块、接口/数据变更、多任务 | requirements → design（条件）→ **review-docs（A/B）** → plan → implement → review → verify → deliver → release_handoff（条件）→ retro（条件）→ wrap → commit | 无 |
| L3 高风险 | 权限/资金/迁移/公共 API/安全/破坏性 | L2 + 文档/代码独立审 + 安全/隐私 + 回滚演练 + 发布审批 + 观察 + 复盘 | 无 |
| 缺陷 | 平台缺陷/指派/修复#/产品评估/产品回复 | defect-fix：preflight → pull → triage →（fix/assess→handoff→await→decision→align/clarify）→ gates → menu → close → postrelease | 无平台→change |

分级在 clarify 写入首条路由；不确定先最小充分，高风险/不可逆/跨包再高一档。L0：证据/提交确认/密钥/理解回执不可省（纯机械除外）。L2+ 默认 `{workroot}/development-plan.md`。轻量档默认 `solo`（`rules/core/lightweight.md`）；拿不准高一档+一问。**评审**：L0 与 L1 低风险单点可免独立审；L2+/L3/权限·资金·迁移·公共 API·破坏性不可免；免审不免自检。

### 0.2 确认门 · 澄清 · 直跑

- 门只认 YAML `hitl`/`hitl_when`/`gate_when` + `rules/gates.md`；不另造门。
- 意图/澄清/P·D·S：**只认** `rules/core/clarification.md`；含糊口令禁直接写交接单。
- 产品资料 → `skills/product-doc-analysis`；理解包 §0 Brief+差量表必填，无 §0 不拆单/实施；L1+ 用户可见变化同轮生成用户版业务变化说明（`{workroot}/10-requirements/说明-{主题}-用户版-{yyyyMMdd}.md`），供用户查看与 AI 理解完整业务。
- 直跑只到任务完成（不含提交/推送/部署/回写）；他包产物可选不阻塞，AC/完成门/自验不可省；档位/准出不确定 → 推荐+一问。自主边界见 `rules/core/execution-contract.md`。

### 0.3 硬红线（易疏忽）

1. 证据先于结论；未验证不称完成。
2. 缺陷：修前红证；禁回退补红证；无根因不修；未验证不回写；回写按缺陷文案模板 §6.1 生成并展示全文，状态+备注同轮；产品缺陷先评估/确认。
3. 最小改动；密钥零入库；文档只写现行；新输入按 `rules/doc-governance.md` §3 分流。
4. 禁刷绿；git 前拟提交确认；分支/推送/PR 见 `rules/workflow.md` §2。
5. 子代理禁 git/平台/改门；高风险核验者≠实施者。
6. 文档不落根；发布不跳门；失败按回滚预案。
7. 需求理解先于方案；UX/DX/AX 不净退化。**理解正确 → 一次做对**；验证/缺陷修复是兜底，不替代忠实落地。
8. **跨层**：L2+/L3 或权限/状态/数据基数/多表面 → `skills/cross-layer-consistency`；同判定单服务端谓词；UI 可见须同权 API。
9. **实施质量**：只认 `rules/core/implementation-quality.md`（SC 先于代码；**DEV-IQ-12 执行忠实**；DEV-IQ-09 预检；DEV-IQ-10 重要面硬补；自测只认方案/AC）。

### 0.4 验证与汇报（硬约束）

1. **完成只认门**：`-StartTask` → `verify/Invoke-Gate.ps1` → `.gate/wf-development/completion.json` 本轮 `COMPLETE`；空窗口/`DRY_RUN` 不算。
2. 证据先于结论；子代理自述不算；前端须浏览器验证。
3. 程序 SSOT：`rules/core/verification.md` + `verify/README.md`；质量门对账见 `implementation-quality.md` §8。

### 0.5 工程与执行

- 质量条：`skills/engineering-quality` + `rules/workflow.md` §3.4。方案落地/预检：`implementation-quality.md`。
- 执行：多解先权衡；失败同方案 2 次换路径；最小改动；先工具后子代理；改动面超预期先停。优先直接编辑文件。
- 框架固定（口令→workflow、hitl、证据/密钥/子代理/git/文档落位）默认可被第 5 条覆盖；路径/工具/拆分/未列尽归类（执行契约 §1.3）可自主。

### 0.6 协作与交接（硬约束）

> 细则只认 `rules/collaboration/handoff.md` 当前节。硬句：内容优先、默认择优单文档；HO 仅触发命中；正式签收/C2·C3/发布须回执；C2/C3 重基线过门。

### 0.7 提交、推送、部署（硬约束）

> 提交｜推送｜部署分开；默认只提交。git/拟提交/分账只认 `rules/workflow.md` §2；发布/环境只认 `rules/core/versioning.md`。`COMPLETE`+`confirm_deploy` 才部署；直跑不含自动提交/推送/部署。  
> **尽早提交**：重要改动确认后尽早本地提交，勿长期只停在工作区。**多 remote / 异形 tip**：禁对本工作树 `checkout`/`reset` 到非日常工作 tip；对该 tip 的同步/历史改写只走临时目录或独立 worktree（§2 分支纪律第 6 条）。

## 1. 接入

实例：`project-profile.md`（§1/§7/§8/§9）+ `activeContext.md`；工作根必须有 `{workroot}/`；原件根 `inbound/`（其它名可）；占位符未换=未接入。交接：`{workroot}/handoff/outbound|inbound/{category}/` + `handoff-ledger.md`（唯一登记；`inbound/` 为原件、`handoff/inbound/` 为收件工作副本）；多包同仓直读对方出站，仓外经 docs→入站分析吸收。
口令「接入/重新接入/档案/文档树」→ `onboard.yaml`；标准树、索引与原件根按 `rules/doc-governance.md` §2.4 建；根 `CHANGELOG.md`+`{workroot}/work-log.md`；L2+ 另建开发计划/变更记录/待决项/决策记录/需求台账。

## 2. 收尾

触发：工作流末步、计划结束、点名「收尾/总结」。**骨架与硬项以** `rules/templates/90-handoff/closeout-skeleton.md` §2 为准（缺项=未收尾）。**写完整收尾前打开 §2 样例对照版式**（标题/回执/自检各一行；汇报结论说明体）；禁凭记忆粘行。提交/推送/部署/回写门按 YAML `hitl` 独立确认；完整【拟提交】在 commit 只展示一次（第 2 点仅「待提交摘要」）；默认仅提交，推送单独确认；未提交默认不得开始下一任务（例外=基线检查选项 C/D 且用户确认）。

## 3. 口令 → Workflow（命中即停）

> **描述**：表内是常见口令示例（非穷尽），同义表述按五元组路由，不要求逐字匹配；命中优先执行。未命中或任意描述句 → 必读 `rules/core/routing.md`：抽五元组（动作/对象/结果/连续/体量）→ 意图类 A～L → 项目状态修正；首条必写 `reason=`（可附 `intent=`）。不抠固定措辞；路由后按步加载技能，不另造 workflow。

| 优先 | 命中 | workflow | 入口 step / 默认 agent |
| ---: | --- | --- | --- |
| 0 | 工作总结/输出工作总结/今日工作总结/今日总结 | — | 直接按 `rules/templates/90-handoff/closeout-skeleton.md` §3（读/写 `activeContext` 本包工作总结锚点） |
| 1 | 缺陷修复/指派给我/产品回复 | `defect-fix` | preflight；defect-fixer |
| 2 | 新文档/变更吸收（交接包→handoff） | `intake` | scan（按链至吸收报告/收尾） |
| 3 | 按方案实施/继续迭代 | `iterate` | precheck |
| 4 | 接入/档案/文档树/inbound/清理/生成README/更新README/整理README | `onboard` | 对应 step；README 见 `rules/core/project-readme.md` |
| 4.3 | 技能 / 能力体检或优化 | `skill-audit` | scope→…→wrap/commit |
| 4.4 | 导出项目文档/生成资料库/发资料 | `materials` | select→sync→index→wrap |
| 5 | 提交/推送 | 当前末步或 `change` | commit |
| 5.1 | 轻量开发 / 想法落地 | `solo` | frame（按链至完成门；体量大则升级 change/iterate） |
| 5.2 | 轻量方案 | `solo` | plan |
| 5.3 | 轻量测试 / 验收 | `solo` | test |
| 6 | 常规变更/需求澄清 | `change` | clarify（澄清单步；变更按链） |
| 6.1 | 分析 PRD/方案/原型 | `change` | analyze_input |
| 7 | 出方案/只出方案 | `change` | design |
| 7.1 | 方案/文档评审 | `change` | review-docs |
| 8 | 代码评审 | `change` | review |
| 9 | 提测/发布说明/回滚预案 | `change` | deliver |
| 10 | 发布/上线（生产） | `release` | readiness 起按链 |
| 11 | 回滚 | `release` | rollback |
| 12 | 复盘 | `retro` | gather（按链至行动项/收尾） |
| 13 | 开发计划/下一步/按计划执行 | `control` | init/sync/next/check/run |
| 14 | 维护/查询 | 本文 + `rules/core/maintenance.md` | —；清理→行 4；技能→4.3 |
| 15 | 写交接单/交接包/接收/变更/重规划 | `handoff` | 默认 compose；升包才 send |

**部署歧义（硬规则）**：裸说「部署/推服务器」先判环境，不默认 S8：test/staging/UAT → S7 环境部署（版本按项目模式，只记录+冒烟，不触发 `confirm_deploy`）；prod/生产/正式 → `release`/S8；无法判断只问一次目标。提交/推送 ≠ 部署。
**复合口令**：「提交推送部署更新服务器」= commit→push→环境更新；唯一 test 环境按 S7，多环境问一次；不得默认 S8。

**入口直达**：单步口令（代码评审/提测/下一步/回滚/澄清）只执行该 step 到产出完成即停；表中标「按链」的从入口执行到链末停点；`change`/`iterate`/`release` 按各自链路继续到下一个门或收尾；「只出任务清单」到 wrap + commit 确认即止。`workflow.chain: full`（如 onboard）例外，必须走到 verify/打标。单步入口仍按 `rules/templates/90-handoff/closeout-skeleton.md` 输出。
**互斥**：「落地…#编号…优化方案」=缺陷；「落地迭代方案」=迭代；无 `#` 又无「迭代」→ 一问。未命中 1～5 的改代码/改配置实施类 → `change`；发布/回滚/复盘各自独立。有开发计划且续跑语义（下一步/继续开发计划/当前状态）→ 优先 `control`。
**无口令**：口语未命中上表 → `rules/core/routing.md`（通用意图类，非口令同义词表）。
**首条**：`route=workflow:<id> | step=<id> | level=<L0-L3> | mode=... | reason=... | reads=<读取索引行> | next_action=…`；有输入加 `input=<diff/路径>`。纯只读分析可写 `route=readonly:analysis | step=explain | mode=analyze | reason=… | next_action=…`。

## 4. 维护

改不变量/路由/读取协议 → 本文；改无口令路由 → `rules/core/routing.md`；改心跳/重锚 → `rules/core/rule-anchor.md`；改步骤 → `workflows/`；改角色 → `agents/`；改红线/门 → `rules/`；改澄清 → `rules/core/clarification.md`；改协作/交接/变更分级 → `rules/collaboration/handoff.md` + `workflows/handoff.yaml`；改模板 → `rules/templates/`；改技能 → `skills/`；改能力 → `capabilities/`；改文档树/归档 → `rules/doc-governance.md`；改门面同步 → `rules/core/doc-facade-sync.md`（及 `project-readme.md` 指针）；改子代理 → `rules/collaboration/subagents.md`；改读取索引 → `rules/read-index.md`；改轻量档 → `rules/core/lightweight.md` + `workflows/solo.yaml`。自检见 `rules/core/maintenance.md` §2。

## 5. 文档治理（摘要）

- 工作根按 `rules/doc-governance.md` §2.4 定位；缺他包不阻塞。原件根 `inbound/` 固定在项目根；`keep`/`mix`/`replace` 只管原件结构，仍可索引/复制/吸收。
- 原夹文件一律不迁出；中途存量**全索引**，按任务/版本按需复制或 A0～A2 吸收；可仅索引。细则 `rules/doc-governance.md` §2。
- **换迭代=关版本**：新迭代/换代/换主题（可不发版）→ 同会话按 `rules/doc-governance.md` §7；不确定 → `confirm_iteration_close`。根 `CHANGELOG.md`=产品发版史（仅正式发版/点名发版写；多包输入与软序见文档治理版本记录）；`{workroot}/work-log.md`=岗位里程碑（含接入/治理）；发布说明按版本。

## 6. 技能与能力（按步加载）

- **角色边界**：谁负责/能定/何时停/向谁升级见 `rules/collaboration/roles.md`；冲突先查表。
- **技能**：`skills/<name>/SKILL.md` 命中步必用；阶段→技能见 `skills/README.md`；新增/大改按末节（中文触发、≤500 行、反模式/反合理化、`check_skills.py --strict`）。
- **能力**：实例 SSOT=`{workroot}/capabilities/00-能力清单.md`；包内 `capabilities/00-contract.md`+`capabilities/reference.md` 非真源。清单 available 即用、否则降级。纪律 `rules/capabilities/instance-discipline.md`。「装配能力」写实例；「体检能力」含 **discover**（`npx skills find` / find-skills）→ 方法回灌或能力候选，禁外装并行编排。业务会话最多 1 条有证据建议，禁推销。

## 7. 多包（自动探测）

- **口令表节号**：本包与产品 §3；测试 §2（勿跨包按节号直译）。
- **单包独立为默认**；多包联动**可选、非必须**；不要求装齐三包、不强制同时启用、**不因缺他包阻塞本包**；跨包同步只登记状态，不等于自动联动。**联动=交付物字段+同仓直读，≠共安装、≠自动跑对方、≠强制引用他包路径。**
- **实例面（硬）**：实例根 `AGENTS`/README/档案/`activeContext`/`.gitignore` 只写**已装包**；不描述包的用途/装载/升级。规范包**默认不跟踪**：`.gitignore` 只写一行 `/<已装包>/`（多包 `/wf/`）；不预列未装包、不加注释。用户明确要求跟踪时才跟踪。
- 多包=`wf/`（含 ≥2 个 `wf-*`）；单包=项目根单个 `wf-*`；同 id 双份/半迁停问。共用原件根 `inbound/`、根 `activeContext.md`（总览→各包分节→跨包同步→运行时）。
- 各包只改本分节/本包接入行/相关跨包同步一行；禁整文件覆盖或改他包分节；一次会话只跑一个包 workflow；跨包默认自洽交付物/同仓直读对方 `handoff/outbound/`，**仅升包时**用 `handoff/outbound/{category}/{HO-ID}/`；不复制正文、不自动跑对方。
- **歧义定包**：缺陷/发布/下一步等先查 `wf/AGENTS.md` **意图→包**；无法唯一则一问。
