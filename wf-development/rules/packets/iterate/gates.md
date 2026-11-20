# 步骤卡 · iterate/gates

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`iterate` / `gates`（全量门禁与文档同步）
- **packet**：`rules/packets/iterate/gates.md`
- **角色**：`verifier-agent`（独立验证（开发轨））。只读核验验收清单、diff、证据与完成门结果；返回通过/需修/阻塞；不改代码、不做最终交付判断；本步只做该角色职责；越界交回或升级。
- **上游**：`review`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`deliver`（进 `deliver` 前的 `when=has_qa_or_deploy_or_requested`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:implementation_required`**：非「只出任务清单」且清单已确认；满足→真，否则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/无 UI 时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：全量门禁与文档同步
- **产出**：.gate/wf-development/completion.json + 门禁摘要/文档同步

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_commit`**：【拟提交】块（三包统一：文件+`.gitignore`+分支/跟踪+本次动作；本轨扩展：基线/分账/拆分/落点/CI/PR·合并）；**默认仅本地提交**，推送须单独明确并确认；代码/产物提交在 verify/gates 步确认，推送在 close 步确认，收尾文档在 closeout 确认；≠收尾第 2 点「待提交摘要」
- **条件判定 `hitl:has_pending_commit`**：有文件变更待提交；满足→真，否则跳过该门。
- **GATE `completion-gate`**：**实施前** `-StartTask`（冻结 `base_commit`；归档旧任务态）；L2+ `.gate/acceptance.yaml` 的 `task_id` 须与 `.gate/task.json` 一致；运行 `<包>/verify/Invoke-Gate.ps1 -Acceptance ...`；写 `.gate/wf-development/completion.json`；**前端套装与 capture 运行时只认当前步骤包内「前端硬门」**；**门末自动输出 Claim（只认 `CLAIM: ALLOWED`；`-Claim` 仅复核）**；**回执绑定提交**：StartTask → 实施 → 提交 → 过门；门后只提文档；L1 无定向 test 不跑全仓（`verification.md` §7）；同一检查连续失败 2 次停；空 diff=`NOT_VERIFIED`、dry-run=`DRY_RUN`、缺项 → `BLOCKED`
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`test-design-and-execution` → 见 §6 闭环。

### 本步动作清单

- Invoke-Gate 门末自动 Claim（-Claim 仅复核）。
- 非 COMPLETE 不得 deliver/closeout。
- 同步清单/plan/activeContext。
- 无 QA 时开发自验：AC/SC 全过、证据落盘、前端硬门（无 UI 标 na）。
- 完成门核前端交付物、原型解码、ui-audit 结论与能力可达。
- 缺则 BLOCKED。

### 前端硬门（本步内嵌 · 有 UI 必遵；无 UI 整节 `na`）

> 本节编号仅指前端门内部；引用写「前端门 §X」。

### 前端门 1. 何时触发

- 新增/改页面、路由、菜单、深链、表单布局、权限可见性、关键空态/错误态。
- 用户指出任一前端缺陷 → 触发同波次**缺陷族全量审计**（不得只修单点）。
- 吸收**补测/完善/体验**类方案开工前，或同批 UI 缺陷 ≥5 → **编码前**先做交互诚实族审计（入口/主 CTA/灰显原因/筛选同构/空态分因/术语；见 DEV-IQ-18），再改代码。

### 前端门 2. 必产物（按 §2.1 分级；该级缺一 = `UNVERIFIED`，不得 Claim 完成）

| # | 产物 | 要求 |
| ---: | --- | --- |
| 1 | `.gate/frontend/parity-matrix.md` | 解码原型后：路由→菜单/标题/区块/列或字段网格/按钮/交互/状态/权限；逐项引用理解包 §10 页面清单/§11 冲突 ID（完整链）；solo 链改引方案卡 §0.1/§1；给 `pass`、`按方案` 或 `na`；**每条路由必须有独立 `###` 区块行（标题含路由），每个变更/新增路由的 `operations` 必须列出原型按钮/操作名并逐项 pass**；出现 `partial/pending/待验收/待补/待验/待确认` 即未完成；`OPEN` 必须带 ID+确认人+下游落点；完成判据须勾选。SPA 原型按 §3-1b 解码；矩阵只引解码结果。**无原型**：按方案＋设计系统＋同模块基线页写设计基线（规格/状态矩阵），矩阵对照。 |
| 2 | `.gate/frontend/route-coverage.json` | 菜单+深链+路由；`result=pass`；每路由桌面+移动截图路径 |
| 3 | 每路由桌面+移动截图 | L2+ **必须**由 `frontend.capture` 生成；含 `evidence.json`（ready+sha256）；骨架/登录页/过短文本 = 失败 |
| 4 | `.gate/frontend/design-qa.md` | 按模板项勾选；结论不得与 evidence 矛盾 |
| 5 | console/network 报告 | 目标：本轮关键路由 error/failed = 0（或登记豁免） |
| 6 | L2+ `.gate/plan-coverage.md` | 方案/需求 → 后端要点 → 前端页/字段 → 截图；含本轮 `task_id`，缺/不一致 = BLOCKED；缺行/未完成行或「未通过/需修」= BLOCKED。**能力可达行（硬）**：写端点→页面入口/动作/证据；无入口标 `non-ui` 并确认；只写接口可调=BLOCKED。 |
| 7 | 独立评审（`review_required`） | 评审前必须按 §2.5 打开当前迭代原型（解码产物），逐路由核对矩阵/截图/操作；未见原型、矩阵缺路由或操作、截图与原型不符 = `DENIED`。只看代码/测试/API 200 不得过 |
| 8 | `.gate/frontend/ui-audit.md` | 独立 `ui-auditor`（≠实施者）逐路由页面/操作/状态/跨页一致性/后端可达实操；每条路由有 `###` 区块，`operations` 与 parity-matrix/route-coverage 对账；原型缺陷（照搬/择优）与真实数据（稀疏/空/大数）必填；结论=通过；含待验/未点通/缺口 = 未完成 |

> **复用（硬）**：同一任务、同一源码 diff 的 capture 结果可复用；源码变更后只重拍受影响路由；`e2e` 与 `capture` 不得对同一路由重复全量截图。
>
> **降级**：capture 降级记 `degraded`，不得完成；评审/完成门前补。

#### 前端门 2.1. 证据分级（按变更风险裁剪，避免一律重证据）

开工时在 `.gate/frontend/tier.json` 写 `{"tier":"A|B|C","reason":"…","routes":["/路径"]}`；**未写 = 未开工**：实施步骤开工前必须落盘（缺则 `BLOCKED`，禁先写代码后补）。分级只裁剪证据量，不裁剪质量底（逐字对照、截图新鲜度、console 0 始终生效）；拿不准按 **A**。分级决定产物范围，**不变的是**：console/network 无阻断错误、截图/报告晚于本轮源码变更、结论可复核。`tier.json` 与 console/network/playwright 结果须晚于本轮任务开始；旧 `tier.json` 不读（按 A 校验），旧报告 BLOCKED。

| 级别 | 适用 | 必产物 |
| --- | --- | --- |
| **A 关键** | 崩溃、权限/资金/数据、路由/菜单/权限可见性、跨模块、响应式或布局大改、新增页面 | §2 全量：parity-matrix（每路由区块）+ route-coverage + 每路由桌面/移动截图 + design-qa + console/network + **ui-audit** + 独立评审 |
| **B 标准** | 普通交互、状态/校验、空态/错误态、表单字段与布局微调 | **仅受影响路由**：矩阵对应区块行 + route-coverage（受影响路由）+ 桌面/移动截图 + design-qa + console/network + **ui-audit（受影响路由）** |
| **C 轻量** | 纯文案/列名/单位/排序/灰显/颜色等呈现调整，无行为变化 | **受影响路由 1 张桌面截图** + 文案/状态核对表（可并入 design-qa）+ console error=0；**免独立 ui-audit**、不要求移动截图与 parity-matrix |

- **缺陷族审计**：A 级仍须同波次族审计；B/C 级做**同类路径静态扫描**（同模型/同谓词/同状态表面）+ 受影响路由验证，不要求全站矩阵重拍。
- **升级规则**：C 中发现行为/权限/状态变化 → 升 B；B 中触及 A 的条件 → 升 A，并补齐对应产物。
- **机检**：`gate.py` 读取 `tier.json`（旧文件不读，按 A）；C 允许 1 张桌面截图且跳过 parity；A/B 仍按 §2 校验，另以 `--require-audit` 校验 `ui-audit`（缺/待验/未点通 = BLOCKED）。

#### 前端门 2.5. 原型对齐与实施出口（硬）

**A. 规格来源（先于编码）**
- **原型单源**：当前迭代原型路径/版本只认 `project-profile.md` 的 `prototype=`（配 `prototype_version=`）；缺声明/文件不存在/与迭代不符 = `BLOCKED`。解析顺序 `project-profile.md` → 理解包 §10 → `inbound/INDEX.md`；禁止在入口或通用规则硬编码实例路径。
- **以源码为规格**：规格以解码后的 HTML 结构 / CSS 数值 / JS 行为（handler、文案原文、存储语义、按钮与状态）为准，截图只作外观参考；逐项对照须引用源码位置（函数名/行号）。原型可运行/可解码时默认移植，不凭描述重写。
- **解码产物最低要求**：`.gate/prototype/` 至少含 `prototype.json`（`modules`/`routes` 非空），或等价的结构清单（模块/路由/面板，文件名按项目实际）；只有截图/空清单 = `BLOCKED`；矩阵只引解码结果，不得由实现反抄操作名。
- **无原型例外**：仅当 `frontend.requirePrototype=false` 且写明理由，改用设计基线；仍须逐路由截图与矩阵。

**B. 对照粒度（三个必须）**
- **逐面板结构**：每面板一行写「原型渲染函数 + 结构类型（列表/横条/环/表/卡/事件）+ 行列 + 数字单位 + 空态文案 + 点击目标」（模板：`ui-audit-template.md` §2.2 / `frontend-prototype-parity-template.md` §3.1）；结构类型不一致 = `BLOCKED`。
- **逐交互行为**：每个按钮/链接/行操作/排序/复选/下拉/输入/图表点/图例/关闭确认一行写「原型 handler → 行为 → 我方实现 → 实际结果」；行为不一致（弹窗内容、导出范围、筛选生效、状态保持、反馈）= `BLOCKED`。
- **整页单一 owner**：同页所有面板由同一实施者整体对照；分片只按页面切，不按面板切。
- **原样优先、择优留痕**：布局/文案以原型为准；偏离标 `按方案` 或 `择优：<收益>`，不得降低密度/可读性/操作路径。原型缺陷（稀疏布局失真、空态缺失、示例日期写死、死交互）须显式列出并逐条决定 `照搬` 或 `择优`；发现缺陷仍照抄 = 未完成。

**C. 自检与复核（完成前）**
- **图文自检 + 真实数据**：实施者与评审者必须用图像读截图逐面板/逐交互核对，并用稀疏 / 空 / 大数三种真实数据形态各验一次；只看 ready/console/哈希/接口 200 = 未验证。
- **独立视觉复核**：矩阵与 `ui-audit.md` 的 `pass` 不得实现者自评，须非实现者看图复核确认。
- **实施出口机检（git 钩子强制）**：UI 改动提交/标完成前必须跑 §3-3 机检并写 `.gate/frontend/gate.json`；缺/`ok=false`/早于暂存文件即阻断。绕过仅 `--no-verify` 或 `DSH_GATE_BYPASS=1`（写 `.gate/precommit-bypass.log`，评审必查）。

**D. 顺序**
- 先按原型与方案对齐（结构 + 行为）→ 再择优优化（稀疏/空态/移动端/a11y），每处偏离在矩阵留理由。

### 前端门 3. 必命令（RUN）

```text
# 1) 原型解码（单 HTML + base64/importmap 时）
python <包>/rules/tools/extract_prototype_modules.py <原型.html> .gate/prototype

# 1b) SPA 原型：浏览器按 hash 路由提取结构/截图 → .gate/prototype/。

# 2) 实现后由门禁或显式调用 capture（项目配置 frontend.capture）
# 产出 evidence.json + 桌面/移动图；ready!=true 不得过

# 3) 机检（实施出口 / 评审 / 完成门同一命令；L2+ 必带 --require-generated）
python <包>/verify/tools/frontend_parity.py --evidence-dir .gate/frontend \
  --require-prototype --require-tier --require-generated --require-matrix-routes \
  --require-audit --write .gate/frontend/gate.json

# 3a) 审计前 parity 自检可去掉 --require-audit；进入 ui-audit/评审/提交/完成门前必须带。
#     ui-audit 步：独立 ui-auditor 按模板填 .gate/frontend/ui-audit.md 后跑上面命令。

# 3b) 首次接入：安装提交前钩子（之后 git commit 自动校验 gate.json / ui-audit / plan-coverage）
powershell -File <包>/verify/Install-GitHooks.ps1 -ProjectRoot .

# 4) 完成口令：门末自动输出 CLAIM；仅复核时执行（本步无 completion-gate 则跳过）
powershell -File <包>/verify/Invoke-Gate.ps1 -Claim -ProjectRoot .
```

> **采集纪律**：ready 判定用页面标题 + 数据行/关键控件，不用全文包含；布尔属性按 HTML 语义判断（不能只看属性是否存在）；先跑 1 条路由探针，再全量。

### 前端门 4. 验收底线（人眼 + 门）

- 业务口径/命名/权限/路由以**方案/PRD**为准；布局/组件/视觉有原型以原型为准、无原型以**设计基线**为准；按方案偏离须在矩阵标 `按方案`。
- 页面标题、菜单项、按钮/列名与原型**逐字**对照；命名冲突按方案并在矩阵登记，不得静默改名。
- 矩阵最小粒度到**区块/字段/列/操作**；禁止只写「页面已对齐」而无区块行。
- **覆盖度可机检**：`route-coverage.json` 的每条路由必须在矩阵有 `###` 区块行；每个变更/新增路由的 `operations` 必须逐项出现在该区块并标 `pass`。缺一 = `BLOCKED`。
- `operations` 逐项点通（入口→点击→结果/权限/错误）；静态图不算。
- 写接口须有页面入口或已确认 `non-ui`；接口替代页面=未完成。
- **审计底线（硬）**：A/B 每个可见操作实际点通；跨页术语/状态词/KPI/组件/密度/主操作/日期筛选一致；写端点有页面入口或 `non-ui`；缺一 = 未完成。审计不替代测试/准出。
- **真实数据（硬）**：稀疏/空/大数三形态各验一次；只满数据截图 = 未验证；原型满数据 mock 不能作为通过依据。
- **审计未过不得进 review/提交/Claim**；缺口回 implement 修并回归；UI 缺口不得债项化。
- 正式入口禁用固定样例（demo 关）；缺数据显示空态。
- **附条件不覆盖前端门**：评审/完成门的「附条件」只能用于 OCR、PG、真实样单等非 UI 项；矩阵/截图/console/network 未过只能按 `DEV` 回开发，不得写成 `QA` 条件换取通过。
- **债项口径**：矩阵/审计中的「待产品/后续优化」等偏离必须落 `.gate/acceptance.yaml` 的 `debts`（id/owner/decision）；`blocking` 债项未关闭 = `BLOCKED`，不得带债 Claim；无 ID 的口头债项视为未登记。
- **新鲜度**：截图/报告必须晚于本轮源码变更（含未提交工作区）；`base_commit` 相同不足以证明新鲜。**顺序**：代码/测试/脚本定稿→重拍→回写→提交→过门；改脚本/测试同重拍。
- **组件复用（硬）**：新增/改页面前先盘点项目既有组件（`ui.js`/设计系统）与至少 1 个相邻页面；日期区间、筛选、弹窗、状态戳等优先复用既有组件与交互；原生控件仅在无既有组件时使用；自造须在 parity-matrix/design-qa 写理由。
- **共享模块单例（硬 · DEV-IQ-19）**：带模块级可变状态的共享 JS（store、确认/弹窗 Promise、会话权限等）须单一入口；禁止多 chunk 各写不同 `./xxx.js?v=`。改文件或 bump 戳 → 改入口真源并核对引用；有项目 token 自检须跑过。确认后无请求/偶发丢权限 → 先查是否双例加载。
- 至少达到原型标准，再谈择优：协调（设计系统/同类页一致，无第二套 tokens）、实用（密度与操作路径不劣于同类页）、美观（层级/留白/对齐/对比度）——按 `design-qa` #7/#8/#9/#18 验收（对比度另见 #13）；禁止「能跑就行」的简化单列/自创壳。
- 深链（新建/详情/授权等）必须直达；菜单在约定视口可见或可滚动到达。
- **导航唯一**：侧栏/菜单无同对象重复项，同一页面组件只注册一次；兼容旧路径命中主入口且未新增可见项。
- 跨路由返回后，原页面的筛选/分页/展开状态不得被详情页临时条件污染。
- **交互诚实（硬）**：`design-qa` #3/#14/#20 须按条文验收（加载诚实、空态分因、禁用原因+下一步、主 CTA 与阻断一致、筛选展示≡请求）；空勾「状态齐」不算通过。
- **实施纪律（编码时，非事后补勾）**：状态词/KPI 单一映射源跨表面引用；有阻断先不可用再可点；方案点名的明细/下钻/证据入口须可发现（≠仅汇总/JSON）。细则 `iq-checklist.md` + `frontend-implementation` §2。
- 新用受限 Web/平台 API → 目标环境冒烟或 polyfill；console error 阻断本门。
- 接口 200、DOM 文本、class、测试绿 **不能**替代本门。
- 浏览器实例生命周期：按当前 agent 已挂载选用，优先绑定、表内空闲套可借；按需拉起、结束退程；细则 实例纪律（按需拉起、结束显式退程）。

### 前端门 5. 禁做

- 只搜原始 HTML 断言「原型没有该页」（须先解码模块）。
- 手写「通过」但无本轮 `evidence.json` / 哈希对不上。
- 写 UI 缺口债项化/以接口替代换过门。
- 固定样例/演示数据填充正式入口。
- MCP 不可用不做浏览器兜底仍标完成。
- 对带状态的共享模块只 bump 部分引用的 `?v=`/hash（易双例：确认挂死、权限态分裂）。
- 未跑 §2.5 实施出口机检就提交或标完成；`tier.json` 缺失先写代码后补。
- 未做 `ui-audit`、用实施者自评/矩阵/截图代替独立审计；只审改动页、未点通操作、未核对后端可达就判通过。
- 把原型路径/版本等实例数据写进入口 `AGENTS` 或通用规则（应落 `project-profile.md`）。
- 原型未对照、矩阵无 `###` 路由区块、或截图与原型不符时以「测试绿/接口 200」判通过。

> L0 无 UI：整节标 `na` + 一句理由，勿机械跑 capture。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。
> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `test-design-and-execution` | **必开** | 进入本步即开（质量不降） | `skills/test-design-and-execution/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **模板（产出该类文件时按此填；门按结构判分的产物须对齐）**：`rules/templates/40-delivery/lite-test-report-template.md`。
- **产出前自检**：对照模板必填节逐项填写；缺节、空节、未替换 `{…}` = 不合格（不得标完成）。
- 验证命令：`<包>/verify/Invoke-Gate.ps1`（门末自动给 `CLAIM: ALLOWED`；`-Claim` 仅复核）；有 UI 遵 §5 前端硬门（已内嵌）。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- §2 产出已按模板必填节落地；无空节、无未替换占位符。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步完成 Claim 门：须 `CLAIM: ALLOWED` 后才可写完成态。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:iterate | step=gates | agent=verifier-agent | packet=rules/packets/iterate/gates.md | global=ok | skills=test-design-and-execution=done|na | claim=ALLOWED|DENIED|na | next=…
```
