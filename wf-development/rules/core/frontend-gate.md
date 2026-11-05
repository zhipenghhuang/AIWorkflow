# 前端硬门（开发轨 · 单一出处）

> **读取级别：命中即读**。L1+ 且有用户可见 UI 时必读本文；L0 无 UI → 整门 `na`。  
> `AGENTS` / IQ / verification / skill **只留指针**，细则以本文 + `verify/frontend/*` + `verify/tools/frontend_parity.py` 为准。  
> 关联：DEV-IQ-13/14/17/18/19/21（词典见 `implementation-quality.md`）；执行勾选见 `iq-checklist.md`。

## 1. 何时触发

- 新增/改页面、路由、菜单、深链、表单布局、权限可见性、关键空态/错误态。
- 用户指出任一前端缺陷 → 触发同波次**缺陷族全量审计**（不得只修单点）。

## 2. 必产物（缺一 = `UNVERIFIED`，不得 Claim 完成）

| # | 产物 | 要求 |
| ---: | --- | --- |
| 1 | `.gate/frontend/parity-matrix.md` | 解码原型后：路由→菜单/标题/区块/列或字段网格/按钮/交互/状态/权限；逐项引用理解包 §10 页面清单/§11 冲突 ID；给 `pass`、`按方案` 或 `na`；**每条路由必须有独立 `###` 区块行（标题含路由），每个变更/新增路由的 `operations` 必须列出原型按钮/操作名并逐项 pass**；出现 `partial/pending/待验收/待补/待验/待确认` 即未完成；`OPEN` 必须带 ID+确认人+下游落点；完成判据须勾选 |
| 2 | `.gate/frontend/route-coverage.json` | 菜单+深链+路由；`result=pass`；每路由桌面+移动截图路径 |
| 3 | 每路由桌面+移动截图 | L2+ **必须**由 `frontend.capture` 生成；含 `evidence.json`（ready+sha256）；骨架/登录页/过短文本 = 失败 |
| 4 | `.gate/frontend/design-qa.md` | 按模板项勾选；结论不得与 evidence 矛盾 |
| 5 | console/network 报告 | 目标：本轮关键路由 error/failed = 0（或登记豁免） |
| 6 | L2+ `.gate/plan-coverage.md` | 方案/需求 → 后端要点 → 前端页/字段 → 截图；缺行或「需修」= BLOCKED |
| 7 | 独立评审（`review_required`） | 须核上述产物；只看代码/测试/API 200 不得过 |

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

## 4. 验收底线（人眼 + 门）

- 业务口径/命名/权限/路由以**方案/PRD**为准；布局/组件/视觉以**原型**为准；按方案偏离须在矩阵标 `按方案`。
- 页面标题、菜单项、按钮/列名与原型**逐字**对照；命名冲突按方案并在矩阵登记，不得静默改名。
- 矩阵最小粒度到**区块/字段/列/操作**；禁止只写「页面已对齐」而无区块行。
- **覆盖度可机检**：`route-coverage.json` 的每条路由必须在矩阵有 `###` 区块行；每个变更/新增路由的 `operations`（原型按钮/操作名）必须逐项出现在该区块并标 `pass`。缺一 = `BLOCKED`。
- **附条件不覆盖前端门**：S5/评审的「附条件」只能用于 OCR、PG、真实样单等非 UI 项；矩阵/截图/console/network 未过只能按 `DEV` 回开发，不得写成 `QA` 条件换取通过。
- **新鲜度**：截图/报告必须晚于本轮源码变更（含未提交工作区）；`base_commit` 相同不足以证明新鲜，源码变更后必须重拍受影响路由。
- 至少达到原型标准，再谈择优；禁止「能跑就行」的简化单列/自创壳。
- 深链（新建/详情/授权等）必须直达；菜单在约定视口可见或可滚动到达。
- 跨路由返回后，原页面的筛选/分页/展开状态不得被详情页临时条件污染。
- 接口 200、DOM 文本、class、测试绿 **不能**替代本门。
- 浏览器实例生命周期（默认不预启动、按需拉起、结束显式退程）按 `rules/capabilities/instance-discipline.md` §6。

## 5. 禁做

- 只搜原始 HTML 断言「原型没有该页」（须先解码模块）。
- 手写「通过」但无本轮 `evidence.json` / 哈希对不上。
- MCP 不可用时不做 Playwright/内置浏览器兜底仍标完成。
