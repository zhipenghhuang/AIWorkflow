# AGENTS.md

> **用途**：产品协作 AI 入口。  
> **新会话必读顺序（硬）**：① `rules/core/cold-start.md` → ② 本文 §3 口令表（路由未定/首次）→ ③ workflow 当前 step 块（门/agent/`must_read`）→ ④ `must_read[0]`=`rules/packets/<wf>/<step>.md` → ⑤ 若包内点名则再开**一个**模板。  
> **已路由中段**：心跳 + `rule_card` + 开局卡标签；禁止每步重读本文全文。  
> **位置**：`wf-product/`。与根 `AGENTS.md` 冲突以根为准；用户冲突见 §0 第 5 条。  
> **template_version**：`2026.11.04.16`（步骤自包含读包；运行时只认 cold-start + packet；Claim/HITL 不变）。  
> **完成口径**：只认开局卡 + `Invoke-Gate.ps1 -Claim -Mode <prd|review|design-review|uat|change|writeback>` → `CLAIM: ALLOWED`。

## 0. 开工

> **硬约束全文**：`rules/core/cold-start.md`。本节只补分级与指针。

1. **中文**；写现行结论。  
2. **短读**：`activeContext` 总览 + `## 产品` 进行中 + **偏好/洞见/坑 ≤3 行**（开局卡第 2 条；`context-memory.md`）；有 `product-profile.md`→§1（每新会话一次）。涉计划读 `product-plan.md` §0·§10。  
3. **接入**：`wf-product onboard: done` 则跳过，否则 onboard-agent 一次判定。  
4. **择优**：不适配 → 依据+主推；二次坚持 → `deviation=`。  
5. **覆盖**：用户明确指令 > 根 AGENTS > 本文 > agent > profile。  
6. **读取**：只认开局卡读链 + 当前步骤包；workflow **只读当前 step 块**；`read-index.md`/playbook/`skills/` 为维护素材，默认不打开。  
7. **契约**：`execution-contract.md` §1.0（【需求与意图理解】+【动作前分析】）+ 理解→方案双确认；开局卡第 1 条已点名，细则不改档位。  
8. **心跳**：`rule-anchor.md`。

### 0.1 确认门 · 澄清 · 任务分级

门只认 YAML `hitl*` + `gates.md`；澄清/`clarification.md`（理解→方案双确认硬）。

| 级别 | 典型 | 必走 | 可跳过 |
| --- | --- | --- | --- |
| P0 | 文案/配置；无 AC 变化 | intake→triage→（联动 apply→verify） | 全量 PRD/独立评审 |
| P1 | 小范围/少 AC，已在计划 | 同上 | 全量 PRD |
| P2 | 跨模块/AC/状态/权限 | 全链 | 无 |
| P3 | 0→1/战略 | new-product+plan+PRD | 无 |

### 0.2 硬红线

1. 禁臆造。 2. AC=条件+动作+观测。 3. 无变更单不实施。 4. 未过设计评审不交开发；UAT 未过不发布。 5. 回写须 `confirm_remark`。 6～8. 见开局卡。 9. inbound/子代理/体验：UX/DX/AX 不净退化。细则 `gates.md` / playbook。  
**原型**：开局卡第 6 条 + `prototype-coverage.md`。**交接**：`handoff.md`。**验证**：`-Claim` + `verify/README.md`。

## 1. 接入

实例在项目根：`product-profile.md`（§3 产品规范要点、§7 缺陷平台可选）、`activeContext.md`；产出统一在 `{workroot}/`；权威文档库为 `docs/materials/`。占位符未换=未接入。
工作根必须有 `{workroot}/`。原件根 `inbound/` 固定在项目根；原夹文件不迁出。`keep`/`mix`/`replace` 只管原树结构，仍可索引/复制/吸收。中途存量全索引，按需复制或 A0～A2 吸收。细则 `rules/doc-governance.md` §2。交接：`{workroot}/handoff/outbound|inbound/{category}/` + `handoff-ledger.md`（`inbound/` 为原件、`handoff/inbound/` 为收件工作副本）。口令「接入产品规范、重新接入、生成产品档案」→ `onboard.yaml`；标准树与索引按 `rules/doc-governance.md` §2.4 建。

## 2. 收尾

触发：工作流末步、产品计划全部阶段结束、点名「收尾/总结」。**骨架与硬项以** `rules/templates/90-handoff/closeout-skeleton.md` §1 通用占位为准（专规只填第1点；缺项=未收尾）。按项目事实填 `{…}`，禁照抄他例。收尾/复盘按 `context-memory.md` §4 写「工作记忆」（无则「无」）。提交/回写门按 YAML `hitl` 在骨架后确认；完整【拟提交】在 commit 只展示一次。

## 3. 口令 → Workflow（命中即停）

> **描述**：表内是常见口令示例（非穷尽），同义表述按五元组路由，不要求逐字匹配；命中优先执行。未命中或任意描述句 → 必读 `rules/core/routing.md`：抽五元组（动作/对象/结果/连续/体量）→ 意图类 A～L → 项目状态修正；首条必写 `reason=`（可附 `intent=`）。不抠固定措辞；路由后按步加载技能，不另造 workflow。

| 优先 | 命中 | workflow | 默认 agent 链 |
| ---: | --- | --- | --- |
| 0 | 工作总结/输出工作总结/今日工作总结/今日总结 | — | 直接按 `rules/templates/90-handoff/closeout-skeleton.md` §3（读/写 `activeContext` 本包工作总结锚点） |
| 1 | 需求/问题/缺陷（未分类；对话/文档/链接/截图） | `change` | pm-lead（按分级条件链至下一门/关单） |
| 2 | 启动新产品 / 新项目/从0到1/产品立项 | `new-product` | pm-analyst（discover→go→define，按链执行到下一个门） |
| 3 | 产品计划/产品规划/路线图/版本规划 | `plan` | pm-analyst→pm-lead（goals→roadmap→scope→review-plan→publish，按链执行到下一个门） |
| 4 | 收集需求/需求洞察/需求池 | `prd` | discover |
| 4.1 | 分析客户需求/访谈澄清 | `prd` | discover（先理解后入池） |
| 4.2 | 竞品分析/对标 | `prd` | discover 或 benchmark（按入口判定） |
| 5 | 单需求立项/排优先级 | `prd` | prioritize |
| 6 | 写 PRD | `prd` | prd（须已确认范围） |
| 7 | PRD 评审/定稿 | `prd` | review |
| 8 | 排期/交付计划 | `deliver` | schedule→review-plan-deliver |
| 9 | 需求答疑/跟进 | `change` | intake→triage |
| 10 | 需求变更/产品缺陷（对话/文档） | `change` | 按链至下一门 |
| 11 | 平台产品缺陷拉取/分析 | `defect` | preflight→pull→source→analyze |
| 12 | 平台回写 | `defect` | writeback |
| 13 | UAT/验收 | `deliver` | uat |
| 14 | 发布/上线检查/复盘 | `deliver` | release |
| 15 | 继续/按产品计划执行/下一步 | 按 `{workroot}/product-plan.md` §0 | 对应阶段 |
| 16 | 接入/档案/装配能力/生成README/更新README/整理README | `onboard` | onboard-agent；README 见 `rules/core/project-readme.md` |
| 16.1 | 资料收取/整理 | `onboard` | materials |
| 16.2 | 文档清理/归档巡检 | `onboard` | lifecycle |
| 16.3 | 技能 / 能力体检或优化 | `skill-audit` | scope→…→wrap/commit |
| 16.4 | 导出项目文档/生成资料库/发资料 | `materials` | select→sync→index→wrap→commit |
| 17 | 提交/推送 | 当前 workflow 末步 | 对应角色 |
| 18 | 维护/查询 | 本文 + `rules/core/maintenance.md` | —；清理→16.2；技能→16.3 |
| 19 | 画原型/原型设计 | `prototype` | 按链或点子步（context/wireframe/visual/hi-fi） |
| 20 | 设计评审 → `review`；UI 走查/可用性 → `usability` | `prototype` | review 或 usability（按命中） |
| 21 | 准备演示/产品汇报 | `showcase` | 按链 |
| 22 | 用户手册/FAQ/发布说明/培训 | `showcase` | docs |
| 23 | 一页纸/对外演示材料 | `showcase` | materials |
| 24 | 写交接单/生成交接包 | `handoff` | 默认 compose；升包才 send |
| 25 | 接收/签收交接包 | `handoff` | receive |
| 26 | 交接状态 | `handoff` | status |
| 27 | 变更通知/同步变更/重规划 | `handoff` | change_* / replan |

**入口即止**：除 `workflow.chain: full`/表中标「按链」/「继续/按计划执行」外，从入口 step 执行到产出完成即停；不自动进入后续 step 或门。`onboard` 仅「接入/重新接入/生成档案/装配能力」入口走 `chain: full` 到 `verify` 打标；「资料/文档治理」入口只执行该步 + 收尾，不连带跑接入核验。单步入口结束仍按 `rules/templates/90-handoff/closeout-skeleton.md` 输出。
**单条 vs 批量**：单条需求/问题/缺陷→`change`；平台缺陷→`defect`；批量洞察/需求池盘点→`prd` discover；**竞品分析/学习竞品**→`prd` discover（模式 S）；**竞品对标/功能差距**→`prd` benchmark（模式 P）；0→1→`new-product`（含模式 S）。分不清先 `change` 受理再分诊。
**需求理解前置**：`收集需求`/`立项`/`写 PRD`/`产品计划` 前必须先完成客户需求**理解复述 + 方案要点**双确认（`rules/core/clarification.md`）；换迭代/定本期范围须在计划 **§3.0** 落 Brief+本期差量表（默认唯一权威；独立迭代变更摘要仅仓外handoff/版本归档/点名时用，且与 §3.0 互指禁双份）；缺口未齐须继续问用户；`写 PRD` 还要求范围已确认；未确认推断标「假设」。
**无口令**：口语未命中上表 → `rules/core/routing.md`（通用意图类，非口令同义词表）。
首条：`route=workflow:<id> | step=<id> | role=<agent> | mode=execute/analyze/stop | reason=… | reads=<读取索引行> | next_action=…`；有输入加 `input=<路径>`；`change` 加 `type=<初判>`；`defect` 加 `scope=<范围>`。纯只读分析可写 `route=readonly:analysis | step=explain | mode=analyze | reason=… | next_action=…`。

## 4. 维护

改不变量/路由/读取协议 → 本文；改无口令路由 → `rules/core/routing.md`；改心跳/重锚 → `rules/core/rule-anchor.md`；改步骤 → `workflows/`；改角色 → `agents/`；改门/红线/输出 → `rules/`；改澄清 → `rules/core/clarification.md`；改协作/交接/变更分级 → `rules/collaboration/handoff.md` + `workflows/handoff.yaml`；改模板 → `rules/templates/`；改技能 → `skills/`；改能力 → `capabilities/`；改文档树/归档 → `rules/doc-governance.md`；改门面同步 → `rules/core/doc-facade-sync.md`（及 `project-readme.md` 指针）；改步骤读包 → `rules/packets/`（改后跑 `build_step_packets.py`）+ `Validate-StepPackets.ps1`。自检见 `rules/core/maintenance.md` §2。

## 5. 多包（自动探测）

`wf/`（含 ≥2 个 `wf-*`）=多包；项目根单个 `wf-*` =单包；同 id 双份/半迁停问。
- **口令表节号**：本包与开发 §3；测试 §2（勿跨包按节号直译）。
- **单包独立为默认**；多包联动**可选、非必须**；不要求装齐三包、不强制同时启用、**不因缺他包阻塞本包**；跨包同步只登记状态，不等于自动联动。**联动=交付物字段+同仓直读，≠共安装、≠自动跑对方、≠强制引用他包路径。**
- **实例面（硬）**：实例根 `AGENTS`/README/档案/`activeContext`/`.gitignore` 只写**已装包**；不描述包的用途/装载/升级。规范包**默认不跟踪**：`.gitignore` 只写一行 `/<已装包>/`（多包 `/wf/`）；不预列未装包、不加注释。用户明确要求跟踪时才跟踪。
- 共用原件根 `inbound/`（项目根固定；无则 onboard 建）、根 `activeContext.md`（总览 → 已启用包分节 → 跨包同步 → 运行时；单包只建本包节）。
- 各包只改本分节、与本包相关的跨包同步一行、本包接入行；禁止整文件覆盖或改他包分节。
- 一次会话只执行一个包 workflow；跨包默认交自洽交付物或同仓直读对方 `handoff/outbound/`；**仅升包时**用 `handoff/outbound/{category}/{HO-ID}/`；不复制正文、不自动执行对方 workflow。
- **歧义定包**：缺陷/发布/下一步等先查 `wf/AGENTS.md` **意图→包**；无法唯一则一问。
- 单包不启用以上规则，仍用同分节骨架（仅本包节）。

## 6. 技能与能力（按步加载）

- **角色边界**：谁负责/能定什么/何时停/向谁升级见 `rules/collaboration/roles.md`；出现职责冲突先查此表，不靠聊天记忆。
- **技能（必用）**：`skills/<name>/SKILL.md`，随包复制、命中步必用；方法见 `skills/README.md`。体检能力确认后可就地改本包 skills / capabilities。
- **技能质量**：新增/大改按 `skills/README.md` 末节；description 含中文触发词；≤500 行；须有反模式/反合理化；改后 `check_skills.py --strict`。
- **能力（可选 · 实例 SSOT）**：真源 `{workroot}/capabilities/00-能力清单.md`；包内 `capabilities/00-contract.md`+`capabilities/reference.md` 非真源。纪律 `rules/capabilities/instance-discipline.md`。「装配能力」写实例；「体检能力」含 **discover**（`npx skills find` / find-skills）→ 方法回灌或能力候选，禁外装并行编排。
- **适度建议（业务会话）**：仅当有证据表明现行 skills / capabilities 达不到本任务要求、与清单/档案明显不符、或持续降级损害定稿/准出时，在收尾待确认表附 **至多 1 条**（对象+现象+「说体检能力」）；禁推销清单、禁未确认改 skills / capabilities。同会话同类只提一次。
