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
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

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

- **条件技能**：`cross-layer-consistency`（命中权限/状态/数据基数/多表面） → 命中则同样走 §6 闭环。

### 本步动作清单

- **前置**：本批 triage【分类表】已输出。
- 未出表禁改业务代码（fix-collaboration §4.0）。
- 仅修表中「实现缺陷」行。
- 待产品行不扩写。
- 开跑声明 mode=（同文件集→单写手）。
- 修前红证。
- 无根因不修。
- 复现与写回按原单口径对齐、引用原单信息（协作；红绿与换路径细则见 `AGENTS.md`）。
- **先写缺陷修复卡**（原单口径/SC 差集/同类路径/红证/验证站证据），再改代码。
- 矩阵与判定只认 本包 §5 规则卡，不另造表。
- **动手前**：先 `verify/Invoke-Gate.ps1 -StartTask -TaskId "BUG-<id>" -ProjectRoot "."`（冻结 `base_commit`；截图须晚于 `started_at`/验收清单）→ 来源完整性检查=0 缺漏（DEV-IQ-16，含相关方案/原型/接口/同类路径）→ 短【实施预检】（DEV-IQ-09；**命中须先扩 SC/债项**）。
- 命中重要面同批硬补（DEV-IQ-10）。
- 勾选 `iq-checklist.md`。
- 单元=一条 SC。
- 方法 §6 `implementation-and-selftest`。
- 按 §6 `cross-layer-consistency` 做同类路径扫描：同模型其他写入口、同谓词其他消费方、同权限端点/菜单、同状态其他表面。
- 逐条判「同defects/已正确/不适用」，原单+同类路径各补一条回归。
- 记录根因层/规则缺口。
- **DEV-IQ-08**：同根因族 ≥2 → 除回归外须拟改 rules/skills/检查项缺口（先拟改+原因+影响，用户确认后改母版或项目适配）。
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

- 先勾：AC/SC/DoD 差集=0；未进 SC 且无债项 → 不开工。勾选表索引 `rules/core/iq-checklist.md`。
- **DEV-IQ-22（顺序硬）**：方案 → 分析理解 → 实施择优；理解包不抢入口；禁先看分析再找方案；漏读/砍细节 → 停工或 OPEN。**方法**见 §6 `implementation-and-selftest`。
- **预检硬门槛**：写码前命中面须先扩 SC/债项；单元=一条 SC；禁刷绿；最小改动≠裁剪 Then。
- **自测硬门槛**：每条 SC 有验证；未验证显式写；完成前方案盘点+分析合看+择优偏离留痕。有 UI 守本包「前端硬门」。
- 独立评审 → 本链 `review`；不在本步自称已评审。子代理索引 `rules/collaboration/subagents.md`；质量条守本步 §6 已列技能。

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
| 6 | L2+ `.gate/plan-coverage.md` | 方案/需求 → 后端要点 → 前端页/字段 → 截图；缺行/未完成行或「未通过/需修」= BLOCKED |
| 7 | 独立评审（`review_required`） | 须核上述产物；只看代码/测试/API 200 不得过 |

> **复用（硬）**：同一任务、同一源码 diff 的 capture 结果可复用；源码变更后只重拍受影响路由；`e2e` 与 `capture` 不得对同一路由重复全量截图。

#### 前端门 2.1. 证据分级（按变更风险裁剪，避免一律重证据）

开工时在 `.gate/frontend/tier.json` 写 `{"tier":"A|B|C","reason":"…","routes":["/路径"]}`；未写按 **A**。分级决定产物范围，**不变的是**：console/network 无阻断错误、截图晚于本轮源码变更、结论可复核。

| 级别 | 适用 | 必产物 |
| --- | --- | --- |
| **A 关键** | S1/崩溃、权限/资金/数据、路由/菜单/权限可见性、跨模块、响应式或布局大改、新增页面 | §2 全量：parity-matrix（每路由区块）+ route-coverage + 每路由桌面/移动截图 + design-qa + console/network + 独立评审 |
| **B 标准** | 普通交互、状态/校验、空态/错误态、表单字段与布局微调 | **仅受影响路由**：矩阵对应区块行 + route-coverage（受影响路由）+ 桌面/移动截图 + design-qa + console/network |
| **C 轻量** | 纯文案/列名/单位/排序/灰显/颜色等呈现调整，无行为变化 | **受影响路由 1 张桌面截图** + 文案/状态核对表（可并入 design-qa）+ console error=0；不要求移动截图与 parity-matrix |

- **缺陷族审计**：A 级仍须同波次族审计；B/C 级做**同类路径静态扫描**（同模型/同谓词/同状态表面）+ 受影响路由验证，不要求全站矩阵重拍。
- **升级规则**：C 中发现行为/权限/状态变化 → 升 B；B 中触及 A 的条件 → 升 A，并补齐对应产物。
- **机检**：`gate.py` 读取 `tier.json`；C 允许 1 张桌面截图且跳过 parity；A/B 仍按 §2 校验。

### 前端门 3. 必命令（RUN）

```text
# 1) 原型解码（单 HTML + base64/importmap 时）
python <包>/rules/tools/extract_prototype_modules.py <原型.html> .gate/prototype

# 2) 实现后由门禁或显式调用 capture（项目配置 frontend.capture）
# 产出 evidence.json + 桌面/移动图；ready!=true 不得过

# 3) 机检（L2+ 另加 --require-generated；项目 profile 打开 requireMatrixRoutes 时加 --require-matrix-routes）
python <包>/verify/tools/frontend_parity.py --evidence-dir .gate/frontend --require-matrix-routes

# 4) 完成口令
powershell -File <包>/verify/Invoke-Gate.ps1 -Claim -ProjectRoot .
```

### 前端门 4. 验收底线（人眼 + 门）

- 业务口径/命名/权限/路由以**方案/PRD**为准；布局/组件/视觉以**原型**为准；按方案偏离须在矩阵标 `按方案`。
- 页面标题、菜单项、按钮/列名与原型**逐字**对照；命名冲突按方案并在矩阵登记，不得静默改名。
- 矩阵最小粒度到**区块/字段/列/操作**；禁止只写「页面已对齐」而无区块行。
- **覆盖度可机检**：`route-coverage.json` 的每条路由必须在矩阵有 `###` 区块行；每个变更/新增路由的 `operations`（原型按钮/操作名）必须逐项出现在该区块并标 `pass`。缺一 = `BLOCKED`。
- **附条件不覆盖前端门**：S5/评审的「附条件」只能用于 OCR、PG、真实样单等非 UI 项；矩阵/截图/console/network 未过只能按 `DEV` 回开发，不得写成 `QA` 条件换取通过。
- **新鲜度**：截图/报告必须晚于本轮源码变更（含未提交工作区）；`base_commit` 相同不足以证明新鲜，源码变更后必须重拍受影响路由。
- 至少达到原型标准，再谈择优；禁止「能跑就行」的简化单列/自创壳。
- 深链（新建/详情/授权等）必须直达；菜单在约定视口可见或可滚动到达。
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

> L0 无 UI：整节标 `na` + 一句理由，勿机械跑 capture。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → 读必做，并读现场处置/判定/反合理化（技能有这些节时）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `debugging-and-error-recovery` | **必开** | 进入本步即开（质量不降） | `skills/debugging-and-error-recovery/SKILL.md` | 只读 L12-L90（硬门槛+方法+反合理化）→ 回本包 |
| `implementation-and-selftest` | **必开** | 进入本步即开（质量不降） | `skills/implementation-and-selftest/SKILL.md` | 只读 L13-L133（必做+处置/判定/反合理化）→ 回本包 |
| `cross-layer-consistency` | 条件开 | 命中权限/状态/数据基数/多表面 | `skills/cross-layer-consistency/SKILL.md` | 只读 L12-L127（硬门槛+方法+反合理化）→ 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/20-design/solution-template.md`；只读本步用到的节，禁止整文件通读。
- 验证命令：`verify/Invoke-Gate.ps1`（本步非完成 Claim；按 Mode 出回执即可）；有 UI 遵 §5 前端硬门（已内嵌）。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:defect-fix | step=fix | agent=defect-fixer | packet=rules/packets/defect-fix/fix.md | global=ok | skills=debugging-and-error-recovery,implementation-and-selftest,cross-layer-consistency|done|na | claim=ALLOWED|DENIED|na | next=…
```
