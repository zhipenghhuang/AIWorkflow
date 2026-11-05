# 验证（测试轨）

> 目的：让“测试通过/准出”有可对账的证据。门读现有测试计划/台账/报告，不新增测试文档。
> 读取时机：`review-cases`、`execute` 批末、`report`、`handoff`/交平台前。维护读 `rules/core/rule-governance.md`。

## 1. 什么时候跑

| 场景 | 命令 | 输出 |
| --- | --- | --- |
| 生成覆盖 | `Invoke-Gate.ps1 -Mode coverage` | 分析表/计划结构 + §3 映射/ID + §4 深度档自检/视觉基础行 |
| 用例评审 | `Invoke-Gate.ps1 -Mode review` | 评审记录结构/独立性/放行结论（`.gate/wf-testing/review.json`） |
| 执行批末（步后门） | `Invoke-Gate.ps1 -Mode execute -Scope "{模块}"` | 分析/计划结构 + **仅 Scope 内**台账/证据/P0；回执含 `scope` |
| 出报告/准出（准出门） | `Invoke-Gate.ps1 -Mode report` | 分析/计划/报告结构 + 各轨现行台账；**只计本轮装填**（排除「未本轮验证」）；忽略 Scope |
| 交平台/回写 | `Invoke-Gate.ps1 -Mode writeback` | 平台回执检查（不覆盖 report） |
| 收尾自检 | `python verify/tools/check_compliance.py --report <收尾文件>` | 回执/自检（route/mode/reads/gates/sync/skip/deviation）+ 六点版式、汇报块、第 2/4/6 点固定子字段、附录；头块禁粘行 |
| 完成口令 | `Invoke-Gate.ps1 -Claim -Mode report` | 读 `.gate/wf-testing/{mode}.json`（缺则 completion）：mode 匹配 + verdict 可放行 + 无阻断 + 计划/分析/报告/台账在回执后未改；输出 `CLAIM: ALLOWED/DENIED` |

```powershell
# 模块批末（Scope 用实际模块目录名，例 16-模块名）
powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Mode execute -Scope "<模块目录名>" -ProjectRoot "."
# 版本准出
powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Mode report -ProjectRoot "."
# 完成/准出表述前（只认 ALLOWED；Claim 按本次结论对应门校验）
powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Claim -Mode report -ProjectRoot "."
```

**完成口径**：`-Claim -Mode report` 只认 report 回执；verdict 非 PASS、有阻断、或计划/分析/报告/台账在回执后又改动 → `CLAIM: DENIED`，只能写“未通过/阻塞/部分完成”。有条件准出须 `CONDITIONAL` + 接受人，否则同样 DENIED。

## 2. 机器门新增项（gate 2.2）

| ID | 模式 | 检查 | 失败处理 |
| --- | --- | --- | --- |
| `analysis-structure` | coverage/execute/report | 分析表 §2 验证点、§2.2 模块×面、§2.3 方法×规则、§2.4 依据覆盖（PRD/方案/原型/接口→验证点）、§3.1 变更影响、§6 设计文档、§7.1 充分性、§7.2 核心链路：表在、无空格、状态无 `缺口/待生成` | FAIL |
| `plan-structure` | coverage/execute/report | 计划 §3.7 有“批次”列；§3.8 V1～V4 齐；§3.9 批次表关键字段齐；同 PG 不得同模块；profile/port/账号默认串行，隔离列声明「独立 server/路由」时，只读可并行（可同账号/写域）；写需无共享写域且账号隔离；≤3（UI 默认 ≤2） | FAIL |
| `case-vp` | coverage/execute/report | 用例 §3 有“验证点”列且逐行非空 | FAIL |
| `case-oracle` | coverage/execute/report | 新格式用例每个 `###` 块含“Oracle 来源” | FAIL |
| `report-structure` | report | 报告 §4 卷结论/点结论/批次与并行表 + §6.1 门槛证据表 | FAIL |
| `*-legacy` | 所有 | 旧格式 analysis/plan/case/report | 默认 `skip`（可运行）；加 `-Strict` 变 FAIL |

> 新项目建议 `-Strict`：`powershell -File wf-testing/verify/Invoke-Gate.ps1 -Mode report -ProjectRoot "." -Strict`。旧实例先按旧格式运行；迁移后再开 `-Strict`。

## 3. 检查什么

- **计划**：`{workroot}/test-plan.md` 存在；§0 状态、§5 准出、§9.2 编排、§11 缺陷策略、§12 探索章程可读；版本级 §3.8 四卷/§3.9 批次表可读且与 §3.7/§9.2/§11.2 对齐；§3.7/§9.2 与 `smoke-checklist.md` 的 P0 用例必须进台账且为本轮终态。
- **台账**：路径宜为 `{轨}/{NN}-{短名}/*-功能台账.md` 或 `*-接口台账.md`（兼容旧名）；§1.1 本轮装填与 §2 非「未本轮验证」行一致；`未本轮验证` 不计通过率；P0 不得为未本轮验证。
- **P0**：P0-Smoke / P0-HighRisk 未通过、未执行、未本轮验证或计划有但台账缺失时，报告不得写 PASS/整体通过。
- **结果自检**：落账前四问（断言面/证据/状态语义/写操作 Network）；批末抽 2～3 条 P0/失败/阻塞对照页面/证据/Network（人工核，`checks.yaml` manual）。
- **报告**：§4 数字与台账**本轮装填**一致；须声明 suite/depth/本轮构建；§1 准出评估唯一且与 P0/本轮未执行/缺口一致；§4 卷结论（V1～V4）/点结论率/用例通过率分列；§3.9 批次/并行/合并未过/偏差可见；回执与门一致。§5 硬项见checks.yaml。
- **覆盖**：功能全量/专项 §3 映射无空行且映射到真实用例 ID，含验证点列；§4 含「深度档自检」「视觉基础」行（缺则 FAIL）；报告/coverage 模式功能资产必须有映射；P0 点有用例或“不适用+依据”；本批命中域对应分析表 §2.2/§2.3 行无空格、§2.4 依据覆盖无缺行；§3.1 变更影响/§6 设计文档/§7.1 充分性/§7.2 核心链路无缺口（人工核，`checks.yaml` manual）。语义是否达标见评审量规，门不臆造深度分数。
- **依据覆盖硬核**：见 `rules/core/verification.md` §3.1（缺行=P0 阻断；E1/E0；报告/评审只认本轮证据）。
- **用例评审**：存在现行 `评审-*.md`（合卷/计划）或 `*-评审-*.md`（单域 C 命名）；可解析结论（放行执行/有条件放行/需修后放行）；含独立性与量规/严重度痕迹；放行时不得残留未消化阻断；有条件放行须有接受人；语义量规由 AI 按技能执行，机器只核结构与放行态。批次数见 `工作流` §2.5。
- **回写**：交平台时存在回执（单号/备注/状态/附件）；`writeback` 只写 `.gate/wf-testing/writeback.json`，不要求计划/台账，不覆盖 report。
- **口径**：只统计当前台账本轮行，`_archive`/`.draft`/`资料`/`证据`/`未本轮验证` 不参与准出对账。

## 4. 完成状态

> `PASS/CONDITIONAL/FAIL/BLOCKED` 条件与报告措辞见 `rules/core/verification.md` §2；本文件不重复状态表。回执中文：可准出/有条件准出/不准出/阻塞；机器仍读 PASS/CONDITIONAL/FAIL/BLOCKED。

## 5. 成本纪律

- **步后窄 / 准出本轮**：域批末 = `execute -Scope`；宣称准出 = `report`（本轮装填口径）。二者不可混用。
- execute 上 `coverage-map` / `p0-missing` 为 soft（矩阵 optional），不单独拉垮本批；report 仍硬。
- 门只读现有计划/台账/报告，不新增文档；证据失败/阻塞必看。
- 迭代准出 suite≥module；发版/完整项目=full；补丁=core+窄影响面且报告标明补丁口径；报告须声明 suite + 本轮构建。
