# AGENTS.md

> **用途**：产品协作 AI 入口。  
> **新会话必读顺序（硬）**：入口已是本文 → ① 开局卡 → ② `activeContext` → ③ `global-rules.md` → ④ `workflows/<id>.md` → ⑤ 当前步骤卡 → ⑥ §6 skill → ⑦ 步骤卡 §7 点名的模板（通常 1 份）；未路由时用 §3 口令表。  
> **每轮协议**：先判新任务/续跑/只读 → 新任务重路由并复述 → 首行锚 `route=…|step=…|packet=…|global=ok`（偏离 `global=dev:…`；只读 `mode=analyze`）→ 结束给收口（六点或 2～3 行）。  
> **已路由中段**：`global-rules` 按 §7 重读分级（新会话/换链/规则变更全文；同链中段按节最小集）；每步读当前步骤卡；心跳（`packet=` + `global=ok`）；禁止同时多 packet；本步流程以当前包为准（独立完整，与他步重复 OK），不跳转拼齐；勿通读 `workflow.md`/协作手册拼流程（参考层按节、按需）。  
> **位置**：`wf-product/`。与根 `AGENTS.md` 冲突以根为准；用户冲突见 §0 第 5 条。  
> **template_version**：`2026.11.11.04`  
> **完成口径**：只认 `verify/Invoke-Gate.ps1 -Claim -Mode <prd|review|design-review|uat|change|writeback>` → `CLAIM: ALLOWED`。

## 0. 开工

> **硬约束全文**：`rules/core/global-rules.md`。本节只补分级与指针。

1. **中文**；写现行结论。  
2. **短读**：`activeContext` 总览 + `## 产品` 进行中（含 workflow/state/packet） + **偏好/洞见/坑 ≤3 行**（开局卡 §1；写法 `context-memory.md`）；有 `product-profile.md`→§1（每新会话一次）。涉计划读 `product-plan.md` §0·§10。  
3. **接入**：`wf-product onboard: done` 则跳过，否则 onboard-agent 一次判定。  
4. **行为契约**：理解/澄清/检查/择优/冲突按 `rules/core/global-rules.md`（遵守全文；重读见 §7）。  
5. **覆盖**：只认 `rules/core/global-rules.md` §11。  
6. **读取**：分级读链（global-rules §7 主从）；YAML 非规则正文；技能按步骤包 §6 索引（同时 ≤1）。  
7. **契约**：`rules/core/global-rules.md` §1/§4（开工档位【需求与意图理解】+【动作前分析】）；理解→方案双确认按域门。  
8. **心跳**：`rules/core/global-rules.md` §8（切步/过门一行锚）。

### 0.1 确认门 · 澄清 · 执行路径

门只认 YAML `hitl*` + `gates.md`；开局门 `confirm_task_intent` 见 `gates.md`（不依赖 step）；开工档位/读链只认 `global-rules.md`；澄清**方法**按需读 `clarification.md`（参考层；理解→方案双确认门仍硬）。

> P0～P3 为内部风险标签，按 `gates.md` §2「P 档推导」的事实判定（不凭感觉），**路径拿不准走全量**；档位不替代用户确认。

| 路径 | 触发 | 完整任务必走 | 可省 |
| --- | --- | --- | --- |
| 轻量受理 | 纯文案/配置，无 AC/范围变化 | intake→triage→就地更新→verify/关闭 | 全量 PRD、独立评审 |
| 标准产品 | AC/范围/状态/权限变化，或计划内小需求 | intake→triage→理解双确认→PRD→评审→交付 | 独立评审（P0/普通 P1 可作者自检；P1↑ 结构门硬、默认可 A/`SELF_CHECKED`；P2+ 必问 A/B）；PRD 可轻量，门不降 |
| 新版本/0→1 | 新产品/新版本/战略 | new-product→plan→PRD→原型→交付→发布 | 无 |
| 高风险 | 权限/资金/数据/合规/不可逆 | 标准产品 + 专项/独立评审/发布门 | 无 |

**不确定**：事实不足或两条路径都能解释 → 先问 1 个关键问题；不得静默降档；用户明确要求从简才可降，并记录 `deviation=`。YAML `when` 不满足可跳过相应步，但须在收尾 `skip=` 记录理由。  
**走链**：路径表是完整任务链/能力边界；单步口令按「入口即止」只做该步；完整任务用「按链/按计划/继续」推进到下一个门/停点。不得无提示断链，也不得越过门自动跑完。

### 0.2 硬红线

**产品特有红线**：回写须 `confirm_remark`；inbound/子代理/体验 UX/DX/AX 不净退化。其余见 `rules/core/global-rules.md`。原型/交接/验证细则随当前步骤包点名再读。

## 1. 接入

实例在项目根：`product-profile.md`（§3 产品规范要点、§7 缺陷平台可选）、`activeContext.md`；产出统一在 `{workroot}/`；权威文档库为 `docs/materials/`。占位符未换=未接入。
工作根必须有 `{workroot}/`。原件根 `inbound/` 固定在项目根；原夹文件不迁出。`keep`/`mix`/`replace` 只管原树结构，仍可索引/复制/吸收。中途存量全索引，按需复制或 A0～A2 吸收。细则 `rules/doc-governance.md` §2。交接：`{workroot}/handoff/outbound|inbound/{category}/` + `handoff-ledger.md`（`inbound/` 为原件、`handoff/inbound/` 为收件工作副本）。口令「接入产品规范、重新接入、生成产品档案」→ `onboard.yaml`；标准树与索引按 `rules/doc-governance.md` §2.4 建。

## 2. 收尾

触发：工作流末步、产品计划全部阶段结束、点名「收尾/总结」。**骨架与硬项以** `rules/templates/90-handoff/closeout-skeleton.md` §1 通用占位为准（专规只填第1点；缺项=未收尾）。按项目事实填 `{…}`，禁照抄他例。收尾/复盘按 `context-memory.md` §4 写「工作记忆」（无则「无」）。提交/回写门按 YAML `hitl` 在骨架后确认；完整【拟提交】在 `closeout` 步只展示一次。

## 3. 口令 → Workflow（命中即停）

> **描述**：表内是常见口令示例（非穷尽），同义表述按五元组路由，不要求逐字匹配；命中优先执行。未命中或任意描述句 → 必读 `rules/core/routing.md`：抽五元组（动作/对象/结果/连续/体量）→ 意图类 A～L → 项目状态修正；首条必写 `reason=`（可附 `intent=`）。不抠固定措辞；路由后按步加载技能，不另造 workflow。

| 优先 | 命中 | workflow | 默认 agent 链 |
| ---: | --- | --- | --- |
| 0 | 工作总结/输出工作总结/今日工作总结/今日总结 | — | 直接按 `rules/templates/90-handoff/closeout-skeleton.md` §2（读/写 `activeContext` 本包工作总结锚点） |
| 1 | 需求/问题/缺陷（未分类；对话/文档/链接/截图） | `change` | pm-lead（默认入口即止；按链/继续至下一门/关单） |
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
| 10 | 需求变更/产品缺陷（对话/文档） | `change` | 默认入口即止；按链/继续至下一门 |
| 11 | 平台产品缺陷拉取/分析 | `defect` | preflight→pull→source→analyze |
| 12 | 平台回写 | `defect` | writeback |
| 13 | UAT/验收 | `deliver` | uat |
| 14 | 发布/上线检查/复盘 | `deliver` | release |
| 15 | 继续/按产品计划执行/下一步 | 按 `{workroot}/product-plan.md` §0 | 对应阶段 |
| 16 | 接入/档案/装配能力/生成README/更新README/整理README | `onboard` | onboard-agent；README 见 `rules/core/project-readme.md` |
| 16.1 | 资料收取/整理 | `onboard` | materials |
| 16.2 | 文档清理/归档巡检 | `onboard` | lifecycle |
| 16.3 | 技能 / 能力体检或优化 | `skill-audit` | scope→…→closeout |
| 16.4 | 导出项目文档/生成资料库/发资料 | `materials` | select→sync→index→closeout |
| 17 | 提交/推送 | 当前 workflow 末步 | 对应角色 |
| 18 | 维护/查询 | 本文 + `rules/core/maintenance.md` | —；清理→16.2；技能→16.3 |
| 19 | 画原型/原型设计 | `prototype` | 按链或点子步（context/wireframe/visual/hi-fi） |
| 20 | 设计评审 → `review`；UI 走查/可用性 → `usability` | `prototype` | review 或 usability（按命中） |
| 21 | 准备演示/产品汇报 | `showcase` | 按链 |
| 22 | 用户手册/FAQ/发布说明/培训 | `showcase` | docs |
| 23 | 一页纸/对外演示材料 | `showcase` | materials |
| 24 | 写交接单/生成交接包 | `handoff` | 默认 compose；升包才 send |
| 25 | 接收/签收交接包 | `handoff` | receive |
| 26 | 交接状态 | —（只读） | 直接读 `{workroot}/handoff/handoff-ledger.md` + `activeContext`；不启动 workflow |
| 27 | 变更通知/同步变更/重规划 | `handoff` | change_* / replan |

**入口即止**：除 `workflow.chain: full`/表中标「按链」/「继续/按计划执行」外，从入口 step 执行到产出完成即停（不含提交/推送/部署/回写）；不自动进入后续 step 或门。`onboard` 仅「接入/重新接入/生成档案/装配能力」入口走 `chain: full` 到 `verify` 打标；「资料/文档治理」入口只执行该步 + 收尾，不连带跑接入核验。单步入口结束仍按 `rules/templates/90-handoff/closeout-skeleton.md` 输出。中段以当前链图「推进」与步骤卡 §4 为准，口径与本段相同。
**路由消歧**：裸「产品缺陷」未带平台/单号/对话限定时先问或按 `change` 受理；明确平台/单号 → `defect`。**发资料 vs 交接**：「发资料/导出」指整库或资料包（`materials`）；把某份文档交给具体角色（确认/知会/提测）走 `handoff.compose`。
**单条 vs 批量**：单条需求/问题/缺陷→`change`；平台缺陷→`defect`；批量洞察/需求池盘点→`prd` discover；**竞品分析/学习竞品**→`prd` discover（模式 S）；**竞品对标/功能差距**→`prd` benchmark（模式 P）；0→1→`new-product`（含模式 S）。分不清先 `change` 受理再分诊。
**需求理解前置**：`收集需求`/`立项`/`写 PRD`/`产品计划` 前必须先完成客户需求**理解复述 + 方案要点**双确认（门硬；方法按需读 `rules/core/clarification.md`）；换迭代/定本期范围须在计划 **§3.0** 落 Brief+本期差量表（默认唯一权威；独立迭代变更摘要仅仓外handoff/版本归档/点名时用，且与 §3.0 互指禁双份）；缺口未齐须继续问用户；`写 PRD` 还要求范围已确认；未确认推断标「假设」。
**无口令**：口语未命中上表 → `rules/core/routing.md`（通用意图类，非口令同义词表）。
首条按 `rules/core/cold-start.md` §3 回执字段，并补 `level=<按事实推导>`、`reason=`、`reads=<实际读取来源>`、`next_action=`；`mode=execute/analyze/stop` 按判断模式给；有输入加 `input=<路径>`；`change` 加 `type=<初判>`；`defect` 加 `scope=<范围>`。纯只读分析可写 `route=readonly:analysis | step=explain | mode=analyze | reason=… | next_action=…`；字段名不得改别名（如 `role=`）。

## 4. 维护

改不变量/路由/读取协议 → 本文；改无口令路由 → `rules/core/routing.md`；改心跳 → `rules/core/global-rules.md` §8；改步骤 → `workflows/`；改角色 → `agents/`；改门/红线/输出 → `rules/`；改澄清 → `rules/core/clarification.md`；改协作/交接/变更分级 → `rules/collaboration/handoff.md` + `workflows/handoff.yaml`；改模板 → `rules/templates/`；改技能 → `skills/`；改能力 → `capabilities/`；改文档树/归档 → `rules/doc-governance.md`；改门面同步 → `rules/core/doc-facade-sync.md`（及 `project-readme.md` 指针）；改步骤读包 → `rules/packets/`（改后跑 `build_step_packets.py`）+ `Validate-StepPackets.ps1`。自检见 `rules/core/maintenance.md` §2。

## 5. 多包（自动探测）

`wf/`（含 ≥2 个 `wf-*`）=多包；项目根单个 `wf-*` =单包；同 id 双份/半迁停问。
- **口令表节号**：本包与开发 §3；测试 §2（勿跨包按节号直译）。
- **单包独立为默认**；多包联动**可选、非必须**；不要求装齐三包、不强制同时启用、**不因缺他包阻塞本包**；跨包同步只登记状态，不等于自动联动。**联动=交付物字段+同仓直读，≠共安装、≠自动跑对方、≠强制引用他包路径。**
- **实例面（硬）**：实例根 `AGENTS`/README/档案/`activeContext`/`.gitignore` 只写**已装包**；不描述包的用途/装载/升级。规范包**默认不跟踪**：`.gitignore` 只写一行 `/<已装包>/`（多包 `/wf/`）；不预列未装包、不加注释。用户明确要求跟踪时才跟踪。
- 共用原件根 `inbound/`（项目根固定；无则 onboard 建）、根 `activeContext.md`（总览 → 已启用包分节 → 跨包同步 → 运行时；单包只建本包节）。
- 各包只改本分节、与本包相关的跨包同步一行、本包接入行；禁止整文件覆盖或改他包分节。
- 一次会话只执行一个包 workflow；跨包默认交自洽交付物或同仓直读对方 `handoff/outbound/`；**仅升包时**用 `handoff/outbound/{category}/{HO-ID}/`；不复制正文、不自动执行对方 workflow。
- **歧义定包**：先查 `wf/AGENTS.md` **意图→包**；无该文件时用下表；无法唯一则一问。多包应 onboard 生成 `wf/AGENTS.md`。
- **无 `wf/AGENTS.md` 兜底**（有则以该文件为准）：产品缺陷评估/平台产品单→产品；修代码/开发缺陷流→开发；交平台/测试回归→测试；发布=业务上线/UAT→产品；发布=部署/回滚→开发；发布=准出报告→测试；下一步/继续→`activeContext` 当前包分节（无焦点一问）；提交/推送/交接→当前会话已绑定包（未开跑一问）。
- 单包不启用以上规则，仍用同分节骨架（仅本包节）。

## 6. 技能与能力（按步加载）

- **角色边界**：谁负责/能定什么/何时停/向谁升级见 `rules/collaboration/roles.md`；出现职责冲突先查此表，不靠聊天记忆。
- **技能（必用）**：`skills/<name>/SKILL.md`，随包复制、命中步必用；方法见 `skills/README.md`。体检能力确认后可就地改本包 skills / capabilities。
- **技能质量**：新增/大改按 `skills/README.md` 末节；description 含中文触发词；≤500 行；须有反模式/反合理化；改后 `check_skills.py --strict`。
- **能力（可选 · 实例 SSOT）**：真源 `{workroot}/capabilities/00-能力清单.md`；包内 `capabilities/00-contract.md`+`capabilities/reference.md` 非真源。纪律 `rules/capabilities/instance-discipline.md`。「装配能力」写实例；「体检能力」含 **discover**（`npx skills find` / find-skills）→ 方法回灌或能力候选，禁外装并行编排。
- **适度建议（业务会话）**：仅当有证据表明现行 skills / capabilities 达不到本任务要求、与清单/档案明显不符、或持续降级损害定稿/准出时，在收尾待确认表附 **至多 1 条**（对象+现象+「说体检能力」）；禁推销清单、禁未确认改 skills / capabilities。同会话同类只提一次。
