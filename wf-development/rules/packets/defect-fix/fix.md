# 步骤卡 · defect-fix/fix

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`defect-fix` / `fix`（红证与修复）
- **packet**：`rules/packets/defect-fix/fix.md`
- **角色**：`defect-fixer`（缺陷修复编排）。平台拉取 → 分类 → 红证修复或产品评估 → 门禁 → 菜单 → 按 YAML hitl 提交/部署/回写 → 发布后验证；本步只做该角色职责；越界交回或升级。
- **上游**：`align`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`clarify`（进 `clarify` 前的 `when=need_clarification`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:implementation_required`**：非「只出任务清单」且清单已确认；满足→真，否则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/无 UI 时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：红证与修复
- **产出**：修复/方案/验证结果

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`debugging-and-error-recovery`、`implementation-and-selftest` → 见 §6 闭环。

- **条件技能**：`cross-layer-consistency`（命中权限/状态/数据基数/多表面）、`frontend-implementation`（有 UI / 有原型）、`backend-implementation`（后端/接口/数据访问/任务/集成/迁移） → 命中则同样走 §6 闭环。

### 本步动作清单

- **前置**：本批 triage【分类表】已输出。
- 未出表禁改业务代码（fix-collaboration §4.0）。
- 仅修表中「实现缺陷」行。
- 待产品行不扩写。
- 修中发现原预期相对现行过时/冲突→停改回 triage（§4.0#8）。
- 按现行修，禁改回旧口径。
- 开跑声明 mode=（同文件集→单写手）。
- 修前红证。
- 无根因不修。
- 复现与写回按原单口径对齐、引用原单信息（红绿/换路径/回归/验证站轻验见 fix-collaboration §4.5 与 §6 `debugging-and-error-recovery`）。
- 修后：本地硬验。
- 测环境依赖且已部署验证站→相关模块轻验（原入口+同模块≤2）。
- 完整复测归测试。
- **先写缺陷修复卡**（原单口径/SC 差集/同类路径/红证/验证站证据），再改代码。
- 矩阵与判定只认 本包 §5 规则卡（矩阵见 `rules/core/implementation-quality.md` 当前节），不另造表。
- L1+ 验收表用 `verify/templates/acceptance.yaml`（task_id: BUG-<id>）或任务清单 AC 表。
- 须含原单复现/红证与回归/同类路径。
- **动手前**：先 `<包>/verify/Invoke-Gate.ps1 -StartTask -TaskId "BUG-<id>" -ProjectRoot "."`（冻结 `base_commit`；截图须晚于 `started_at`/验收清单）→ 来源完整性检查=0 缺漏（DEV-IQ-16，含相关方案/原型/接口/同类路径）→ 短【实施预检】（DEV-IQ-09；**命中须先扩 SC/债项**）。
- 命中重要面同批硬补（DEV-IQ-10）。
- 勾选 `iq-checklist.md`。
- 单元=一条 SC。
- 方法 §6 `implementation-and-selftest`。
- 按 §6 `cross-layer-consistency` 做同类路径扫描：同模型其他写入口、同谓词其他消费方、同权限端点/菜单、同状态其他表面。
- 逐条判「同defects/已正确/不适用」，原单+同类路径各补一条回归。
- 记录根因层/规则缺口。
- **DEV-IQ-08**：同根因族 ≥2 → 除回归外须拟改 规则/技能/检查项缺口（先拟改+原因+影响，用户确认后改母版或项目适配）。
- 禁止只关单号。
- 实现缺陷→按缺陷修复协作修。
- 产品已认可/修改后认可→按新产品文档/评估单实施。
- 产品改判实现缺陷→按产品说明修，备注引用产品结论。
- 复杂实施再按 `rules/templates/20-design/solution-template.md` 展开，文件名 `方案-BUG-{id}-{主题}-{yyyyMMdd}.md`。
- 简单修复不强制完整方案，但须更新受影响文档/任务清单。
- L1+ UI 命中前端硬门 A 级、L2+ / 高风险/大改/破坏性：核验者≠实施者（派 `reviewer-agent` 独立核验或走 `code-review` 技能；只给原单＋diff＋红绿命令；核验不替代门禁），并写 `.gate/review.md` 供完成门核对。
- **修复分片**（子代理编排）：≥3 单且文件不重叠 → 一组一子代理（worker-agent；文件不相交可并行≤3；同文件/同根因合并组；「同为实现缺陷」alone 不够）。
- 达阈值未分片→deviation=subagent_skipped:<理由>。
- 不达阈值直做。
- 子代理禁 commit/push/改平台，返回 ≤30 行可直填备注的事实素材（`rules/defects/fix-collaboration.md`）。

### 本步规则卡：实施预检与自测（本步门槛；实施类共用）

- **先 StartTask（硬）**：动手前 `<包>/verify/Invoke-Gate.ps1 -StartTask -TaskId "<本轮任务ID>" -ProjectRoot "."`（冻结 `base_commit`）；`-TaskId` 用方案/验收清单同一 id（L2+ 与 `.gate/acceptance.yaml` 一致），勿另起新 id；提交在 StartTask 之后；门后只提文档。
- 先勾：AC/SC/DoD 差集=0；未进 SC 且无债项 → 不开工。勾选表索引 `rules/core/iq-checklist.md`。
- **一次完善（主）**：本期范围内方案条款同批落地；验证/评审是兜底，不把「以后补/挂债过门」当默认路径。
- **DEV-IQ-22（顺序硬）**：方案 → 分析/技术方案理解 → 实施择优；理解包不抢入口；禁先看分析再找方案；漏读/砍细节 → 停工或 OPEN。
- **预检硬门槛**：写码前命中面须先扩 SC/债项；单元=一条 SC；禁刷绿；最小改动≠裁剪 Then；P0 禁告警/拒单挂债冒充闭合（DEV-IQ-05）；验收清单写 `implement_preflight`/`sc_trace`，命中 `shared_globs` 另写 `impact_map`（缺则 Claim BLOCKED）。
- **矩阵/词表**：命中权限/状态/数据基数/多表面或需判定时，按需打开 `rules/core/implementation-quality.md` 当前节；本卡只列门槛，不重复矩阵。
- **自测硬门槛**：每条 SC 有验证（含负面/边界）；断言指回方案；未验证显式写；完成前方案盘点+分析合看+择优偏离留痕。有 UI 守本包「前端硬门」。
- 独立评审 → 本链 `review`；不在本步自称已评审；`self_review` 不作过门证据（DEV-VER-06）。子代理开跑先写一行 `mode=工具|直做|单写手|分片|拆分 | reason=…`（频率与隔离见 `rules/collaboration/subagents.md`；达阈值按净收益取档，净收益为正却直做记 `deviation=subagent_skipped:<理由>`）；质量条守本步 §6 已列技能。
- **项目说明（单包/无产品包）**：实现完成前把受影响当前行为/规则/边界并入 `{workroot}/project-guide.md`；多包读产品包同文件；不追加版本节；历史留方案/CR。

### 前端硬门（本步内嵌 · 有 UI 必遵；无 UI 整节 `na`）

> 本节编号仅指前端门内部；引用写「前端门 §X」。

### 前端门 1. 何时触发

- 新增/改页面、路由、菜单、深链、表单布局、权限可见性、关键空态/错误态。
- 用户指出任一前端缺陷 → 触发同波次**缺陷族全量审计**（不得只修单点）。
- 吸收**补测/完善/体验**类方案开工前，或同批 UI 缺陷 ≥5 → **编码前**先做交互诚实族审计（入口/主 CTA/灰显原因/筛选同构/空态分因/术语；见 DEV-IQ-18），再改代码。

### 前端门 2. 必产物（按 §2.1 分级；该级缺一 = `UNVERIFIED`，不得 Claim 完成）

| # | 产物 | 要求 |
| ---: | --- | --- |
| 1 | `.gate/frontend/parity-matrix.md` | 解码原型后：路由→菜单/标题/区块/列或字段网格/按钮/弹窗（标题+按钮+关闭）/文案/字段标签/交互/状态/权限；逐项引用理解包 §10 页面清单/§11 冲突 ID（完整链）；solo 链改引方案卡 §0.1/§1；给 `pass`、`按方案` 或 `na`；**每条路由必须有独立 `###` 区块行（标题含路由），每个变更/新增路由的 `operations` 必须列出原型按钮/操作名并逐项 pass**；出现 `partial/pending/待验收/待补/待验/待确认` 即未完成；`OPEN` 必须带 ID+确认人+下游落点；完成判据须勾选。SPA 原型按 §3-1b 解码；矩阵只引解码结果。**无原型**：按方案＋设计系统＋同模块基线页写设计基线（规格/状态矩阵），矩阵对照。 |
| 2 | `.gate/frontend/route-coverage.json` | 菜单+深链+路由；`result=pass`；每路由桌面+移动截图路径 |
| 3 | 每路由桌面+移动截图 | L2+ **必须**由 `frontend.capture` 生成；含 `evidence.json`（ready+sha256）；骨架/登录页/过短文本 = 失败 |
| 4 | `.gate/frontend/design-qa.md` | 按模板项勾选；结论不得与 evidence 矛盾 |
| 5 | console/network 报告 | 目标：本轮关键路由 error/failed = 0（或登记豁免） |
| 6 | L2+ `.gate/plan-coverage.md` | 方案/需求 → 后端要点 → 前端页/字段 → 截图；含本轮 `task_id`，缺/不一致 = BLOCKED；缺行/未完成行或「未通过/需修」= BLOCKED。**能力可达行（硬）**：写端点→页面入口/动作/证据；无入口标 `non-ui` 并确认；只写接口可调=BLOCKED。 |
| 7 | 独立评审（`review_required`） | 评审前必须按 §2.5 打开当前迭代原型（解码产物），逐路由核对矩阵/截图/操作；未见原型、矩阵缺路由或操作、截图与原型不符 = `DENIED`。只看代码/测试/API 200 不得过 |
| 8 | `.gate/frontend/ui-audit.md` | 独立 `ui-auditor`（≠实施者）逐路由页面/控件（按钮/弹窗/文案/字段）/操作/状态/跨页一致性/后端可达实操；每条路由有 `###` 区块，`operations` 与 parity-matrix/route-coverage 对账；原型缺陷（照搬/择优）与真实数据（稀疏/空/大数）必填；结论=通过；含待验/未点通/缺口 = 未完成 |

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

> 本门是「实施三段式」（本包 §5 规则卡（矩阵见 `rules/core/implementation-quality.md` 当前节））在前端的落地：先准备对照计划 → 按计划一次实施 → 自验+独立复核+门。

> **一次做完口径**：UI 交付以「一次实施即完整正确」为目标；发现任何维度不符回开发补齐，不以“下轮再改/记债项”收尾（前端缺口不得债项化）。

**A. 规格与清单（先于编码）**
- **先计划后编码**：写码前必须按 `ui-audit-template.md` §0 产出对照计划（页面×面板×布局×交互/弹窗/文案/字段×状态×权限×后端契约），后端契约未冻结的页面不得先写前端；缺计划 = 未开工。
- **原型单源**：当前迭代原型路径/版本只认 `project-profile.md` 的 `prototype=`（配 `prototype_version=`）；缺声明/文件不存在/与迭代不符 = `BLOCKED`。解析顺序 `project-profile.md` → 理解包 §10 → `inbound/INDEX.md`；禁止在入口或通用规则硬编码实例路径。
- **以源码为规格**：规格以解码后的 HTML 结构 / CSS **浏览器计算值** / JS 行为（handler、文案原文、存储语义、按钮与状态）为准，截图只作外观参考；逐项对照须引用源码位置（函数名/行号）。
- **控件/内容全量清单（硬）**：逐路由枚举原型中每个可见面——页面/区块/表格列/字段/筛选/按钮/链接/行操作/弹窗（标题+按钮+关闭）/提示与文案/状态/空态/权限。每项写「原型源码（函数/行号）→ 实际渲染（同视口 DOM/computed/截图）→ 我方实现（文件:行）→ 结果（pass/按方案/择优）」；只列主路径或只写「查看/导出」等大类 = 未开工。
- **解码产物最低要求**：`.gate/prototype/` 至少含 `prototype.json`（`modules`/`routes` 非空），或等价的结构清单（模块/路由/面板，文件名按项目实际）；只有截图/空清单 = `BLOCKED`；矩阵只引解码结果，不得由实现反抄操作名。
- **无原型例外**：仅当 `frontend.requirePrototype=false` 且写明理由，改用设计基线；仍须逐路由截图与矩阵。

**B. 基线对齐（原样优先）**
- 按 A 清单逐项做到 `pass/na`；布局/文案/数值以原型计算值为准（基础声明被原型自身媒体/重皮肤层覆盖时，注明并以计算值为准）。
- **偏离登记**：只允许 `按方案`（方案/PRD 优先）或 `择优：<收益>`；无标签的容器/横幅/空白/改名/删字段 = 未完成；原型缺陷逐条 `照搬`/`择优`。
- **整页单一 owner**：同页所有面板与布局由同一实施者整体对照；分片只按页面切，不按面板切。

**C. 吸收与择优（B 全 pass/na 之后）**
- **吸收**：先列原型/设计系统中保留的好做法（信息层级、密度、分组、组件复用），不得另起页面壳或第二套 tokens；新增组件/容器须在偏离登记写理由。
- **择优**：按真实场景逐项分析（稀疏/空/大数、移动端、a11y、操作路径、错误恢复）；每项写 before/after（截图或坐标/间距实测）+ 收益；**择优后协调/实用/美观任一维度不得劣于原型**。
- **同视口并排对照（硬）**：桌面与移动各一组，原型与实现同视口并排；逐段量区块间距/空带/密度（px），差异要么归零、要么标 `择优`；出现无原型依据的空白带/横幅/大白卡且未登记 = 未完成。
- **维度唯一出处**：逐维对照只认 `ui-audit-template.md` 的 20 维（缺维或结论非 pass/na = `BLOCKED`）；本文件不另列维度。

**D. 自检与出口（完成前）**
- **图文自检 + 真实数据**：实施者与评审者必须用图像读截图逐面板/逐交互核对，并用稀疏 / 空 / 大数三种真实数据形态各验一次；只看 ready/console/哈希/接口 200 = 未验证。
- **独立视觉复核**：矩阵与 `ui-audit.md` 的 `pass` 不得实现者自评，须非实现者看图复核确认；复核须抽核同视口并排对照与区块间距。
- **实施出口机检（git 钩子强制）**：UI 改动提交/标完成前必须跑 §3-3 机检并写 `.gate/frontend/gate.json`；缺/`ok=false`/早于暂存文件即阻断。绕过仅 `--no-verify` 或 `DSH_GATE_BYPASS=1`（写 `.gate/precommit-bypass.log`，评审必查）。

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
- **基线→择优（硬）**：先按 §2.5 A/B 做到全 pass/na，再按 C 吸收/择优；必须附同视口并排对照与区块间距/空带实测，**择优后协调/实用/美观任一维度不得劣于原型**；禁止「能跑就行」的简化单列/自创壳。
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
| `debugging-and-error-recovery` | **必开** | 进入本步即开（质量不降） | `skills/debugging-and-error-recovery/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `implementation-and-selftest` | **必开** | 进入本步即开（质量不降） | `skills/implementation-and-selftest/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `cross-layer-consistency` | 条件开 | 命中权限/状态/数据基数/多表面 | `skills/cross-layer-consistency/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `frontend-implementation` | 条件开 | 有 UI / 有原型 | `skills/frontend-implementation/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `backend-implementation` | 条件开 | 后端/接口/数据访问/任务/集成/迁移 | `skills/backend-implementation/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（主）**：`rules/templates/20-design/solution-template.md`；只读本步用到的节，禁止整文件通读。
- **配套模板（按产出需要读；门按结构判分的产物须对齐）**：`rules/templates/10-planning/project-guide-template.md`。
- **产出前自检**：对照模板必填节逐项填写；缺节、空节、未替换 `{…}` = 不合格（不得标完成）。
- 验证命令：`<包>/verify/Invoke-Gate.ps1`（本步非完成 Claim；machine 门按 Mode 出回执，checklist 门按 §4 清单留证、不跑）；有 UI 遵 §5 前端硬门（已内嵌）。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- §2 产出已按模板必填节落地；无空节、无未替换占位符。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:defect-fix | step=fix | agent=defect-fixer | packet=rules/packets/defect-fix/fix.md | global=ok | skills=debugging-and-error-recovery=done|na,implementation-and-selftest=done|na | claim=ALLOWED|DENIED|na | next=…
```
