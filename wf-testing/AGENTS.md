# AGENTS.md

> **用途**：测试规范 AI 入口。  
> **新会话必读顺序（硬）**：① `rules/core/cold-start.md` → ② 本文 §2 口令表（路由未定/首次）→ ③ workflow 当前 step 块（门/agent/`must_read`）→ ④ `must_read[0]`=`rules/packets/<wf>/<step>.md` → ⑤ 若包内点名则再开**一个**模板。  
> **已路由中段**：心跳 + `rule_card` + 开局卡标签；禁止每步重读本文全文。  
> **位置**：`wf-testing/`。与根冲突以根为准；用户冲突见 §0 第 5 条。  
> **template_version**：`2026.11.04.16`（步骤自包含读包；运行时只认 cold-start + packet；Claim/HITL 不变）。  
> **主链**：分析→计划→生成→用例评审→执行→报告。  
> **完成口径**：只认开局卡 + `-Claim -Mode report|writeback` → `CLAIM: ALLOWED`。

## 0. 开工

> **硬约束全文**：`rules/core/cold-start.md`。本节只补分级与指针。

1. **中文**；写现行结论。  
2. **短读**：`activeContext` 总览 + `## 测试` 进行中 + **偏好/洞见/坑 ≤3 行**（开局卡第 2 条；`context-memory.md`）；身份：档案 §1 或 `env-baseline`（每新会话一次）。  
3. **接入**：`wf-testing onboard: done` 则跳过；生成/执行/缺陷无标记时核验一次。  
4. **择优**：不适配 → 依据+主推；二次坚持 → `deviation=`。  
5. **覆盖**：用户明确指令 > 根 AGENTS > 本文 > agent > 基线。  
6. **读取**：只认开局卡读链 + 当前步骤包；workflow **只读当前 step 块**；`read-index.md`/playbook/`skills/` 为维护素材，默认不打开。  
7. **契约**：`execution-contract.md` §1.0（【需求与意图理解】+【动作前分析】）；开局卡第 1 条已点名，细则不改档位。  
8. **心跳**：`rule-anchor.md`。

### 0.0 事实与文档

事实可核实；待确认禁升格；正式资产只写现行。术语：覆盖单元=验证点；批次=`B-Vx-xx`。

### 0.1 计划门 · 三门 · 澄清

门只认 YAML `hitl*` + `gates.md`（条件门 `hitl_when` 不满足则跳过）。澄清只认 `clarification.md`。依据先建模：分析表 §0 必填。  
**分级**：T0 补丁 / T1 模块 / T2 版本 / T3 高风险（`workflow.md` §1.2）。勿与开发 L* / 产品 P* 混用。

| 对象 | 默认（能脚本不 AI） |
| --- | --- |
| 已脚本化回归 | 脚本档 |
| 规则/用例/台账改写 | 直接编辑 |
| 新稳定 P0 / 确定性接口 | 同轮写脚本；禁 AI 全跑再脚本双耗 |

**依据/E1/准出**：开局卡第 2/6 条；`verification.md` §3.1、`multi-track-quality.md`。**红线**：禁臆造；密钥/PII 不进证据；禁刷绿；P0 未过不得整体通过。**交接**：`handoff.md`。

## 1. 接入

实例在项目根：`env-baseline.md`、`activeContext.md`；工作根必须有 `{workroot}/`；原件根 `inbound/` 固定在项目根（原夹不迁出）。存量全索引，按需复制或 A0～A2 吸收。占位符未换或无基线=未接入。交接 `{workroot}/handoff/outbound|inbound/{category}/` + 台账（`inbound/` 为原件、`handoff/inbound/` 为收件工作副本）。接入 `onboard.yaml` + `onboard-agent.yaml`；标准树与索引按 `rules/doc-governance.md` §2.4 建。

**分级**：T0 补丁/T1 模块/T2 版本/T3 高风险；裁剪见 `rules/workflow.md` §1.2；T0/T1 可轻量，但范围/类型/轨道/执行矩阵/准出/风险必须写清；发布列车/大版本 ≥1 次功能全量。不确定先按最小充分，高风险/不可逆再高一档。**勿把开发 L* / 产品 P* 当测试 T***；计划阶段 P0～P9 ≠ 用例优先级 P0-Smoke ≠ UI 证据 E0/E1 ≠ 资产 Core/Domain/Delta。

## 2. 口令 → Workflow（命中即停）

> **描述**：表内是常见口令示例（非穷尽），同义表述按五元组路由，不要求逐字匹配；命中优先执行。未命中或任意描述句 → 必读 `rules/core/routing.md`：抽五元组（动作/对象/结果/连续/体量）→ 意图类 A～L → 计划状态修正；首条必写 `reason=`（可附 `intent=`）。不抠固定措辞；路由后按步加载技能，不另造 workflow。

| 优先 | 命中 | workflow | 切入 step |
| ---: | --- | --- | --- |
| 0 | 工作总结/输出工作总结/今日工作总结/今日总结 | — | 直接按 `rules/templates/90-handoff/closeout-skeleton.md` §4（读/写 `activeContext` 本包工作总结锚点） |
| 1 | 发布前测试资产/方案（性能·安全·兼容等，同义按入口判定） | `testing`（发布前轨） | generate / execute |
| 2 | 分析需求/测试依据建模 | `testing` | analyze |
| 3 | 测试计划/更新计划/本期变更 | `testing` | plan |
| 4 | 测试报告/准出评估 | `testing` | report |
| 5 | 缺陷协作/提交到平台/缺陷回归 | `defect` | classify（按链至收尾/提交门） |
| 6 | 执行专项 | `testing` | execute |
| 7 | 生成/执行接口测试 | `testing`（接口轨） | generate / execute |
| 8 | 探索式测试（生成/执行） | `testing`（探索式轨） | generate / execute |
| 9 | 随机业务流程（生成/执行·计划外） | `testing`（随机业务流程轨） | generate / execute |
| 10 | 按计划执行/回归重跑 | `testing` | execute（不调度随机业务流程） |
| 10.1 | 当前状态/下一步 | `testing` | status（只读） |
| 11 | 生成用例/测试资产 | `testing` | generate（须分析表；双读原文+表） |
| 12 | 用例/计划/接口资产评审 | `testing` | review-cases 或 plan 内评审 |
| 13 | 接入/环境基线/重新接入/装配能力/生成README/更新README/整理README | `onboard` | baseline / migrate / capabilities；README 见 `rules/core/project-readme.md` |
| 13.3 | 技能 / 能力体检或优化 | `skill-audit` | scope→…→wrap/commit |
| 14 | 维护/查询 | 本文 + `rules/core/maintenance.md` | —；清理→行 17；技能优化→行 13.3 |
| 15 | 脚本编写/脚本执行 | `testing` | generate 或 execute |
| 16 | 资料收取/整理 | `onboard` | materials |
| 16.1 | 导出项目文档/生成资料库/发资料 | `materials` | select→sync→index→wrap→commit |
| 17 | 文档清理/归档巡检 | `onboard` | lifecycle |
| 18 | 写交接单/交接包/接收/变更/重规划 | `handoff` | 默认 compose；升包才 send |
| 19 | 提交/推送 | 当前 workflow 末步或 `handoff` | commit |

**入口即止**：单步入口只执行该步到产出完成即止，并仍按 `rules/templates/90-handoff/closeout-skeleton.md` 输出；表中标「按链」的从入口执行到链末停点；“按计划执行”走全链；`testing.report` 例外——报告门后按 `next` 追加一次提交/交平台确认，不重跑执行；`workflow.chain: full`（如 onboard）例外，但仅「接入/基线/重新接入」入口走全链到 verify/打标；「资料/文档治理」入口只执行该步 + 收尾。
**计划驱动主链**：生成测试计划→**计划/分析 A/B 评审**→计划门确认→生成用例→**多轨资产评审（放行）**→按计划执行→报告/准出。
**版本级单点**：`{workroot}/test-plan.md`、`{workroot}/test-report.md`；全量首跑必经；缺则轻量补；发布列车/大版本 ≥1 次功能全量；补丁=P0 冒烟+影响面+已脚本化回归。
**执行三态**：「继续」=续跑未完成；「回归/重跑」=重测既有用例（结果就地覆盖、只留最新）；缺陷平台单回归→行 5。
**需求理解前置**：`生成用例/资产`、`测试计划`、接口/发布前定范围前必须已有 **测试分析表**（`{workroot}/test-analysis.md`；模板 `rules/templates/10-planning/test-analysis-template.md`）；无表 → 先 analyze。功能/专项 **双读原文+全表**；接口/发布前/探索式 **至少读 §0**。**按计划执行**：计划 §0 已确认且表路径可打开 → 不阻断；表缺失仅告警并建议补建，勿强制赶回 analyze。
**用例评审前置**：功能全量/专项 T1+ 在进 P2/正式执行前必须经 `review-cases` 放行（选 B → 机器门 PASS/CONDITIONAL；选 A → HUMAN_APPROVED + 评审记录）；默认按本轮装填批次成卷（同轨同主读可合卷，跨轨不合卷）；生成写手不得自审自放行；T0 可 SELF_CHECKED 并声明。方法：`skills/testcase-review/SKILL.md` + `工作流` §2.5。
**无口令**：口语未命中上表 → `rules/core/routing.md`（通用意图类，非口令同义词表）。
首条：`route=workflow:<id> | step=<id> | role=<agent> | mode=execute/analyze/stop | reason=… | reads=<读取索引行> | next_action=…`；仅无标记预检时加 `preflight=onboard`；有主读/输入时加 `input=<路径>`。纯只读分析可写 `route=readonly:analysis | step=explain | mode=analyze | reason=… | next_action=…`。

## 3. 实例路径

根留 `env-baseline.md`、`activeContext.md` 与原件根 `inbound/`；测试产物统一 `{workroot}/`；权威文档库为 `docs/materials/`。inbound/分轨归档/计划/报告/CR/交接落点见 `rules/workflow.md` §1.3。禁止在项目根堆测试产物。

## 4. git

有 `.git` 时：完整任务收尾检查仓库状态与 `.gitignore`；结论只写入【任务收尾】第 2 点（字段：`待提交摘要` / `git` / `.gitignore`）；拟改 ignore 列入第 4 点表，确认后再改；禁止收尾外另造 git 块；仓库完整清单仅【拟提交·仓库】一次（门=`confirm_commit`，≡他包同名；≠第 2 点摘要，≠门3 `confirm_platform`）。无 `.git` 时第 2 点写「无仓库」。
提交/推送前：出示【拟提交·仓库】→ `confirm_commit` 确认后执行；禁擅自切主干、force push、开/合并 PR（除非点名）。重要改动确认后尽早提交。多 remote / 异形 tip 时禁对本工作树 `checkout`/`reset` 到非日常 tip；对该 tip 的同步/历史改写只走临时目录（见 `rules/workflow.md` §4.1）。

## 5. 收尾

触发：工作流末步、计划全部阶段结束、点名「收尾/总结」。**骨架与硬项以** `rules/templates/90-handoff/closeout-skeleton.md` §1 通用占位为准（生成/执行用【生成收尾】/【执行收尾】；专规只填第1点；缺项=未收尾）。按项目事实填 `{…}`，禁照抄他例。收尾/复盘按 `context-memory.md` §4 写「工作记忆」（无则「无」）。浏览器退程见多Agent §2.2。门3（`confirm_platform`）与【拟提交·仓库】在骨架后按 `hitl` 分门确认。

## 6. 维护

改不变量/路由/读取协议 → 本文；改无口令路由 → `rules/core/routing.md`；改心跳/重锚 → `rules/core/rule-anchor.md`；改步骤 → `workflows/`；改角色 → `agents/`；改红线/门 → `rules/`；改澄清 → `rules/core/clarification.md`；改协作/交接/变更分级 → `rules/collaboration/handoff.md` + `workflows/handoff.yaml`；改轨边界 → `rules/tracks/`；改多轨准出/depth/硬映射 → `rules/special/multi-track-quality.md`（再同步tracks/工作流/验证规则）；改 templates / skills / capabilities → 对应目录；改计划编排 → 测试计划模板 + `workflow.md` §3.6 + `rules/special/multi-agent-output.md` §4（三处同步）；改门面同步 → `rules/core/doc-facade-sync.md`（及 `project-readme.md` 指针）；改步骤读包 → `rules/packets/`（改后跑 `build_step_packets.py`）+ `Validate-StepPackets.ps1`。自检见 `rules/core/maintenance.md` §2。

## 7. 多包（自动探测）

`wf/`（含 ≥2 个 `wf-*`）=多包；项目根单个 `wf-*` =单包；同 id 双份/半迁停问。
- **口令表节号**：本包 §2；产品/开发 §3（勿跨包按节号直译）。
- **单包独立为默认**；多包联动**可选、非必须**；不要求装齐三包、不强制同时启用、**不因缺他包阻塞本包**；跨包同步只登记状态，不等于自动联动。
- **联动=交付物字段 + 同仓直读**（提测单影响面/AC/CHG 等）→ 测试侧映射为装填；**≠** 共安装、**≠** 自动跑对方 workflow、**≠** 要求对方会写 Core/suite、**≠** 强制引用他包路径；无提测单时本包自填命中域。
- **实例面（硬）**：实例根 `AGENTS`/README/档案/`activeContext`/`.gitignore` 只写**已装包**；不描述包的用途/装载/升级。规范包**默认不跟踪**：`.gitignore` 只写一行 `/<已装包>/`（多包 `/wf/`）；不预列未装包、不加注释。用户明确要求跟踪时才跟踪。
- 共用原件根 `inbound/`（项目根固定；无则 onboard 建）、根 `activeContext.md`（总览 → 已启用包分节 → 跨包同步 → 运行时；单包只建本包节）。
- 各包只改本分节、与本包相关的跨包同步一行、本包接入行；禁止整文件覆盖或改他包分节。
- 一次会话只执行一个包 workflow；跨包默认交自洽交付物或同仓直读对方 `handoff/outbound/`；**仅升包时**用 `handoff/outbound/{category}/{HO-ID}/`；不复制正文、不自动执行对方 workflow。
- **歧义定包**：缺陷/发布/下一步等先查 `wf/AGENTS.md` **意图→包**；无法唯一则一问。
- 单包不启用以上规则，仍用同分节骨架（仅本包节）；无提测单时测试自填命中域，不阻塞。

## 8. 技能与能力（按步加载）

- **角色边界**：谁负责/能定什么/何时停/向谁升级见 `rules/collaboration/roles.md`；出现职责冲突先查此表，不靠聊天记忆。
- **技能（必用）**：`skills/<name>/SKILL.md`，随包复制、命中步必用；方法见 `skills/README.md`。本包副本可在「体检能力」确认后就地改技能。
- **技能质量**：新增/大改按 `skills/README.md` 末节；description 含中文触发词；≤500 行；须有反模式/反合理化；改后 `check_skills.py --strict`。
- **能力（可选 · 实例 SSOT）**：真源 `{workroot}/capabilities/00-能力清单.md`（详情/绑定按需同目录）；包内 `capabilities/00-contract.md` 只定义槽位，`capabilities/reference.md` 为候选举例。清单 available 即用，否则按契约降级；**未接受降级的缺失槽每次触达须出独立【能力缺失】块**（契约 §2；`prompted` 不抑制再提示；禁基线「已提示」冒充已知晓）。能力不替代技能。纪律 `rules/capabilities/instance-discipline.md`。「装配能力」=写入实例清单/绑定；「接受降级」=清单 `degraded`+`accepted=`；「体检能力」含 **discover**（`npx skills find` / find-skills）→ 方法回灌或能力候选，禁外装绕过分析表/oracle，见 `workflows/skill-audit.yaml`。
- **适度建议（业务会话）**：仅当有证据表明现行 skills / capabilities 达不到本任务要求、与清单/计划明显不符、或持续降级损害准出时，在收尾待确认表附 **至多 1 条**（对象+现象+「说体检能力」）；禁推销清单、禁未确认改 skills / capabilities。同会话同类只提一次。**能力缺失全块**不受本条「至多 1 条 / 同会话一次」限制（契约 §2 优先）。
