# 前端硬门（开发轨 · 单一出处）

> **读取级别：命中即读**。L1+ 且有用户可见 UI 时必读本文；L0 无 UI → 整门 `na`。  
> `AGENTS` / IQ / verification / skill **只留指针**，细则以本文 + `verify/frontend/*` + `verify/tools/frontend_parity.py` 为准。  
> 关联：DEV-IQ-13/14/17/18/19/21（词典见 `implementation-quality.md`）；执行勾选见 `iq-checklist.md`。

## 1. 何时触发

- 新增/改页面、路由、菜单、深链、表单布局、权限可见性、关键空态/错误态。
- 用户指出任一前端缺陷 → 触发同波次**缺陷族全量审计**（不得只修单点）。
- 吸收**补测/完善/体验**类方案开工前，或同批 UI 缺陷 ≥5 → **编码前**先做交互诚实族审计（入口/主 CTA/灰显原因/筛选同构/空态分因/术语；见 DEV-IQ-18），再改代码。

## 2. 必产物（按 §2.1 分级；该级缺一 = `UNVERIFIED`，不得 Claim 完成）

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

### 2.1 证据分级（按变更风险裁剪，避免一律重证据）

开工时在 `.gate/frontend/tier.json` 写 `{"tier":"A|B|C","reason":"…","routes":["/路径"]}`；未写按 **A**。分级决定产物范围，**不变的是**：console/network 无阻断错误、截图晚于本轮源码变更、结论可复核。

| 级别 | 适用 | 必产物 |
| --- | --- | --- |
| **A 关键** | S1/崩溃、权限/资金/数据、路由/菜单/权限可见性、跨模块、响应式或布局大改、新增页面 | §2 全量：parity-matrix（每路由区块）+ route-coverage + 每路由桌面/移动截图 + design-qa + console/network + 独立评审 |
| **B 标准** | 普通交互、状态/校验、空态/错误态、表单字段与布局微调 | **仅受影响路由**：矩阵对应区块行 + route-coverage（受影响路由）+ 桌面/移动截图 + design-qa + console/network |
| **C 轻量** | 纯文案/列名/单位/排序/灰显/颜色等呈现调整，无行为变化 | **受影响路由 1 张桌面截图** + 文案/状态核对表（可并入 design-qa）+ console error=0；不要求移动截图与 parity-matrix |

- **缺陷族审计**：A 级仍须同波次族审计；B/C 级做**同类路径静态扫描**（同模型/同谓词/同状态表面）+ 受影响路由验证，不要求全站矩阵重拍。
- **升级规则**：C 中发现行为/权限/状态变化 → 升 B；B 中触及 A 的条件 → 升 A，并补齐对应产物。
- **机检**：`gate.py` 读取 `tier.json`；C 允许 1 张桌面截图且跳过 parity；A/B 仍按 §2 校验。

## 3. 必命令（RUN）

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

> **采集纪律**：ready 判定用页面标题 + 数据行/关键控件，不用全文包含；布尔属性按 HTML 语义判断（不能只看属性是否存在）；先跑 1 条路由探针，再全量。

## 4. 验收底线（人眼 + 门）

- 业务口径/命名/权限/路由以**方案/PRD**为准；布局/组件/视觉以**原型**为准；按方案偏离须在矩阵标 `按方案`。
- 页面标题、菜单项、按钮/列名与原型**逐字**对照；命名冲突按方案并在矩阵登记，不得静默改名。
- 矩阵最小粒度到**区块/字段/列/操作**；禁止只写「页面已对齐」而无区块行。
- **覆盖度可机检**：`route-coverage.json` 的每条路由必须在矩阵有 `###` 区块行；每个变更/新增路由的 `operations`（原型按钮/操作名）必须逐项出现在该区块并标 `pass`。缺一 = `BLOCKED`。
- **附条件不覆盖前端门**：S5/评审的「附条件」只能用于 OCR、PG、真实样单等非 UI 项；矩阵/截图/console/network 未过只能按 `DEV` 回开发，不得写成 `QA` 条件换取通过。
- **新鲜度**：截图/报告必须晚于本轮源码变更（含未提交工作区）；`base_commit` 相同不足以证明新鲜，源码变更后必须重拍受影响路由。
- **组件复用（硬）**：新增/改页面前先盘点项目既有组件（`ui.js`/设计系统）与至少 1 个相邻页面；日期区间、筛选、弹窗、状态戳等优先复用既有组件与交互；原生控件仅在无既有组件时使用；自造须在 parity-matrix/design-qa 写理由。
- 至少达到原型标准，再谈择优；禁止「能跑就行」的简化单列/自创壳。
- 深链（新建/详情/授权等）必须直达；菜单在约定视口可见或可滚动到达。
- 跨路由返回后，原页面的筛选/分页/展开状态不得被详情页临时条件污染。
- **交互诚实（硬）**：`design-qa` #3/#14/#20 须按条文验收（加载诚实、空态分因、禁用原因+下一步、主 CTA 与阻断一致、筛选展示≡请求）；空勾「状态齐」不算通过。
- **实施纪律（编码时，非事后补勾）**：状态词/KPI 单一映射源跨表面引用；有阻断先不可用再可点；方案点名的明细/下钻/证据入口须可发现（≠仅汇总/JSON）。细则 `iq-checklist.md` + `frontend-implementation` §2。
- 新用受限 Web/平台 API → 目标环境冒烟或 polyfill；console error 阻断本门。
- 接口 200、DOM 文本、class、测试绿 **不能**替代本门。
- 浏览器实例生命周期（默认不预启动、按需拉起、结束显式退程）按 `rules/capabilities/instance-discipline.md` §6。

## 5. 禁做

- 只搜原始 HTML 断言「原型没有该页」（须先解码模块）。
- 手写「通过」但无本轮 `evidence.json` / 哈希对不上。
- MCP 不可用时不做 Playwright/内置浏览器兜底仍标完成。
