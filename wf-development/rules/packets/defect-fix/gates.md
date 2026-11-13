# 步骤卡 · defect-fix/gates

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`defect-fix` / `gates`（门禁）
- **packet**：`rules/packets/defect-fix/gates.md`
- **角色**：`verifier-agent`（独立验证（开发轨））。只读核验验收清单、diff、证据与完成门结果；返回通过/需修/阻塞；不改代码、不做最终交付判断；本步只做该角色职责；越界交回或升级。
- **前置**：缺陷修复卡/任务清单含本轮 AC 验收表（L1+）；无则先补
- **上游**：`clarify`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`menu`（进 `menu` 前的 `when=implementation_required`）
- **失败去向**：停止本批；不得进入 menu/close，先修复、补证据或报阻塞
- **条件判定 `when:has_code_change`**：本轮代码/配置 diff 非空（不含生成物）；满足→真，否则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/无 UI 时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：门禁
- **产出**：.gate/wf-development/completion.json + 门禁摘要

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **GATE `completion-gate`**：任务开始 `-StartTask`（归档旧任务态）；L2+ `.gate/acceptance.yaml` 的 `task_id` 须与 `.gate/task.json` 一致；运行 `verify/Invoke-Gate.ps1 -Acceptance ...`；写 `.gate/wf-development/completion.json`；**前端套装与 capture 运行时只认当前步骤包内「前端硬门」**（维护真源 本包前端硬门，改后须 `build_step_packets.py` 重生）；**门末自动输出 Claim（只认 `CLAIM: ALLOWED`；`-Claim` 仅复核）**；L1 无定向 test 不跑全仓（`verification.md` §7）；同一检查连续失败 2 次停；空 diff=`NOT_VERIFIED`、dry-run=`DRY_RUN`、缺项 → `BLOCKED`
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 本批无代码/配置改动 → 跳过。
- 有改动默认跑定向 completion（profile `*_scoped` + 受影响前端证据）。
- 升全量条件见 verification §7。
- 门末自动 Claim。
- L1+ 无验收表先补。
- `task_id=BUG-*` 须含原单红证与回归/同类路径。
- 用户明示跳过 Claim → 本步可记 `deviation=skip_claim` 并以本地验证摘要代替 COMPLETE（禁再开全量空转）。
- 日志分诊：原始日志落盘。
- 仅多文件语义归因才派子代理（≤30 行）。

### 前端硬门（本步内嵌 · 有 UI 必遵；无 UI 整节 `na`）

> 本节编号仅指前端门内部；引用写「前端门 §X」。

### 前端门 1. 何时触发

- 新增/改页面、路由、菜单、深链、表单布局、权限可见性、关键空态/错误态。
- 用户指出任一前端缺陷 → 触发同波次**缺陷族全量审计**（不得只修单点）。
- 吸收**补测/完善/体验**类方案开工前，或同批 UI 缺陷 ≥5 → **编码前**先做交互诚实族审计（入口/主 CTA/灰显原因/筛选同构/空态分因/术语；见 DEV-IQ-18），再改代码。

### 前端门 2. 必产物（按 §2.1 分级；该级缺一 = `UNVERIFIED`，不得 Claim 完成）

| # | 产物 | 要求 |
| ---: | --- | --- |
| 1 | `.gate/frontend/parity-matrix.md` | 解码原型后：路由→菜单/标题/区块/列或字段网格/按钮/交互/状态/权限；逐项引用理解包 §10 页面清单/§11 冲突 ID；给 `pass`、`按方案` 或 `na`；**每条路由必须有独立 `###` 区块行（标题含路由），每个变更/新增路由的 `operations` 必须列出原型按钮/操作名并逐项 pass**；出现 `partial/pending/待验收/待补/待验/待确认` 即未完成；`OPEN` 必须带 ID+确认人+下游落点；完成判据须勾选 |
| 2 | `.gate/frontend/route-coverage.json` | 菜单+深链+路由；`result=pass`；每路由桌面+移动截图路径 |
| 3 | 每路由桌面+移动截图 | L2+ **必须**由 `frontend.capture` 生成；含 `evidence.json`（ready+sha256）；骨架/登录页/过短文本 = 失败 |
| 4 | `.gate/frontend/design-qa.md` | 按模板项勾选；结论不得与 evidence 矛盾 |
| 5 | console/network 报告 | 目标：本轮关键路由 error/failed = 0（或登记豁免） |
| 6 | L2+ `.gate/plan-coverage.md` | 方案/需求 → 后端要点 → 前端页/字段 → 截图；含本轮 `task_id`，缺/不一致 = BLOCKED；缺行/未完成行或「未通过/需修」= BLOCKED |
| 7 | 独立评审（`review_required`） | 须核上述产物；只看代码/测试/API 200 不得过 |

> **复用（硬）**：同一任务、同一源码 diff 的 capture 结果可复用；源码变更后只重拍受影响路由；`e2e` 与 `capture` 不得对同一路由重复全量截图。

#### 前端门 2.1. 证据分级（按变更风险裁剪，避免一律重证据）

开工时在 `.gate/frontend/tier.json` 写 `{"tier":"A|B|C","reason":"…","routes":["/路径"]}`；未写按 **A**。分级决定产物范围，**不变的是**：console/network 无阻断错误、截图/报告晚于本轮源码变更、结论可复核。`tier.json` 与 console/network/playwright 结果须晚于本轮任务开始；旧 `tier.json` 不读（按 A 校验），旧报告 BLOCKED。

| 级别 | 适用 | 必产物 |
| --- | --- | --- |
| **A 关键** | S1/崩溃、权限/资金/数据、路由/菜单/权限可见性、跨模块、响应式或布局大改、新增页面 | §2 全量：parity-matrix（每路由区块）+ route-coverage + 每路由桌面/移动截图 + design-qa + console/network + 独立评审 |
| **B 标准** | 普通交互、状态/校验、空态/错误态、表单字段与布局微调 | **仅受影响路由**：矩阵对应区块行 + route-coverage（受影响路由）+ 桌面/移动截图 + design-qa + console/network |
| **C 轻量** | 纯文案/列名/单位/排序/灰显/颜色等呈现调整，无行为变化 | **受影响路由 1 张桌面截图** + 文案/状态核对表（可并入 design-qa）+ console error=0；不要求移动截图与 parity-matrix |

- **缺陷族审计**：A 级仍须同波次族审计；B/C 级做**同类路径静态扫描**（同模型/同谓词/同状态表面）+ 受影响路由验证，不要求全站矩阵重拍。
- **升级规则**：C 中发现行为/权限/状态变化 → 升 B；B 中触及 A 的条件 → 升 A，并补齐对应产物。
- **机检**：`gate.py` 读取 `tier.json`（旧文件不读，按 A）；C 允许 1 张桌面截图且跳过 parity；A/B 仍按 §2 校验。

### 前端门 3. 必命令（RUN）

```text
# 1) 原型解码（单 HTML + base64/importmap 时）
python <包>/rules/tools/extract_prototype_modules.py <原型.html> .gate/prototype

# 2) 实现后由门禁或显式调用 capture（项目配置 frontend.capture）
# 产出 evidence.json + 桌面/移动图；ready!=true 不得过

# 3) 机检（L2+ 另加 --require-generated；项目 profile 打开 requireMatrixRoutes 时加 --require-matrix-routes）
python <包>/verify/tools/frontend_parity.py --evidence-dir .gate/frontend --require-matrix-routes

# 4) 完成口令：门末自动输出 CLAIM；仅复核时执行（本步无 completion-gate 则跳过）
powershell -File <包>/verify/Invoke-Gate.ps1 -Claim -ProjectRoot .
```

> **采集纪律**：ready 判定用页面标题 + 数据行/关键控件，不用全文包含；布尔属性按 HTML 语义判断（不能只看属性是否存在）；先跑 1 条路由探针，再全量。

### 前端门 4. 验收底线（人眼 + 门）

- 业务口径/命名/权限/路由以**方案/PRD**为准；布局/组件/视觉以**原型**为准；按方案偏离须在矩阵标 `按方案`。
- 页面标题、菜单项、按钮/列名与原型**逐字**对照；命名冲突按方案并在矩阵登记，不得静默改名。
- 矩阵最小粒度到**区块/字段/列/操作**；禁止只写「页面已对齐」而无区块行。
- **覆盖度可机检**：`route-coverage.json` 的每条路由必须在矩阵有 `###` 区块行；每个变更/新增路由的 `operations`（原型按钮/操作名）必须逐项出现在该区块并标 `pass`。缺一 = `BLOCKED`。
- **附条件不覆盖前端门**：S5/评审的「附条件」只能用于 OCR、PG、真实样单等非 UI 项；矩阵/截图/console/network 未过只能按 `DEV` 回开发，不得写成 `QA` 条件换取通过。
- **新鲜度**：截图/报告必须晚于本轮源码变更（含未提交工作区）；`base_commit` 相同不足以证明新鲜，源码变更后必须重拍受影响路由。
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
- 浏览器实例生命周期（默认不预启动、按需拉起、结束显式退程）按 实例纪律（按需拉起、结束显式退程）。

### 前端门 5. 禁做

- 只搜原始 HTML 断言「原型没有该页」（须先解码模块）。
- 手写「通过」但无本轮 `evidence.json` / 哈希对不上。
- MCP 不可用时不做 Playwright/内置浏览器兜底仍标完成。
- 对带状态的共享模块只 bump 部分引用的 `?v=`/hash（易双例：确认挂死、权限态分裂）。

> L0 无 UI：整节标 `na` + 一句理由，勿机械跑 capture。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读技能库找感觉。

## 7. 模板与证据

- **无强制模板**：§5 编排已给出动作/顺序；直接落 §2 产出。
- 验证命令：`verify/Invoke-Gate.ps1`（门末自动给 `CLAIM: ALLOWED`；`-Claim` 仅复核）；有 UI 遵 §5 前端硬门（已内嵌）。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步完成 Claim 门：须 `CLAIM: ALLOWED` 后才可写完成态。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:defect-fix | step=gates | agent=verifier-agent | packet=rules/packets/defect-fix/gates.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
