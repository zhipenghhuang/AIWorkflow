# 验证（测试轨）

> 目的：让“分析完整/执行通过/准出”有可对账的证据。门读现有分析/计划/执行记录/报告，不新增测试文档。
> 读取时机：计划门（coverage）、执行批末（execute）、报告（report）、交平台（writeback）。

## 1. 什么时候跑

| 场景 | 命令 | 输出 |
| --- | --- | --- |
| 分析与计划 | `Invoke-Gate.ps1 -Mode coverage` | 分析结构/来源/章节/依据/意图/AC 账本/覆盖矩阵/方法矩阵/细节维/影响面/核心链路 + 计划结构 |
| 执行批末 | `Invoke-Gate.ps1 -Mode execute -Scope "{模块/域}"` | 分析/计划结构硬判 + Scope 内记录/证据/INT∈§2.1/终态/证伪；过程完整且仅产品红 → CONDITIONAL |
| 报告/准出 | `Invoke-Gate.ps1 -Mode report` | 分析/计划/记录/报告一致；全部 P0/P1/P2 意图终态；场景/意图计数；缺口 |
| 交平台/回写 | `Invoke-Gate.ps1 -Mode writeback` | 平台回执（单号/备注/状态/附件） |
| 完成口令 | `Invoke-Gate.ps1 -Claim -Mode report` | 读 `.gate/wf-testing/report.json`；输出 `CLAIM: ALLOWED/DENIED` |

```powershell
powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Mode coverage -ProjectRoot "."
powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Mode execute -Scope "<模块目录名>" -ProjectRoot "."
powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Mode report -ProjectRoot "."
powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Claim -Mode report -ProjectRoot "."
```

**完成口径**：`-Claim -Mode report` 只认 report 回执；verdict 非 PASS/CONDITIONAL、有阻断、或分析/计划/执行记录/报告在回执后又改动 → `CLAIM: DENIED`。`-Mode report` 的 PASS/CONDITIONAL 均可进入 closeout（CONDITIONAL 须报告 §4 有非空接受人）；是否可写“完成/准出”仍只看 `-Claim`。

## 2. 机器门检查

| ID | 模式 | 检查 | 失败处理 |
| --- | --- | --- | --- |
| `analysis-structure` | coverage/execute/report | `test-analysis.md`：来源盘点、章节回执、依据覆盖、**§2.1 意图台账**（具体 INT-*-* + 来源/意图/可观测 Oracle/P/处置；禁簇名行；P0 不设 N/A）、§2.1.1 设计点（意图列只映射台账；处置=测须有处置=测的 INT）、覆盖/方法矩阵/细节维/影响面/核心链路/风险；章节/依据/设计点 INT 须∈台账 | FAIL（三模式同硬） |
| `env-baseline` | coverage/execute/report | `env-baseline.md` 存在且含项目身份/§1 登录/§4 账号/§8 浏览器结构；缺失或空壳 → 不跑 | FAIL |
| `plan-structure` | coverage/execute/report | `test-plan.md`：范围/引用分析/env-baseline/影响面摘要/轨道/轮次/批次/探索/准入准出/suite/depth/环境核验；§3.1 扇出按**同并行组**计；完整计划轨道/轮次非空、§4.3 S6/S7/S11 有着落 | FAIL（三模式同硬） |
| `execution-record` | execute/report | 场景表非空；每场景有 INT；原文/依据可回指锚点；功能记录有「步骤」列（执行行 2～7 短步，缺步骤/单动作 FAIL）；失败/待实现有缺陷号或拟提交处置；通过须可观测 Oracle（禁「通过/正常」）；结果合法 | FAIL |
| `evidence-exists` | execute/report | 失败/阻塞/待实现证据可打开；P0 通过有证据 | FAIL |
| `intent-analysis-link` | execute/report | 执行 INT 须在 **§2.1 台账**（设计点不能冒充）；通过场景与分析来源/Oracle 有对账交集 | FAIL |
| `p0-status` | execute/report | P0 场景/意图失败 → execute 在过程完整时可为 CONDITIONAL（可下批）；report 不得 PASS | execute: CONDITIONAL；report: 不得 PASS |
| `p0-falsify` | execute/report | P0 仅正向通过 → FAIL（须证伪/负向场景或 N/A+接受） | FAIL |
| `intent-coverage` | report | 每个 `处置=测` 台账意图出现在执行记录；无测项台账 → FAIL（禁设计点冒充覆盖） | FAIL；execute 仅批内 |
| `intent-conclusion` | execute/report | 每个意图有终态（通过/失败/阻塞/待实现/N/A）；P1/P2 未测同样失败 | FAIL |
| `p0-missing` | report | 分析中 P0 意图未出现在执行记录 | FAIL；execute 仅批内 |
| `report-structure` | report | 报告 §0～§5、§2.1/§2.2 计数、§2.3 覆盖与收口、§4 缺口；结论唯一 | FAIL |
| `report-verdict` | report | 准出可解析；与 P0/意图终态/失败一致 | FAIL |
| `conditional-acceptor` | report | CONDITIONAL 须 §4 缺口表非空接受人 | FAIL |
| `writeback-receipt` | writeback | 单号/备注/状态/附件/回执 | FAIL |

## 3. 检查什么

- **分析**：§2.1 台账完整（具体 INT+可观测 Oracle）；来源/章节/依据无缺口；每个 AC/F/R/N 映射台账或 N/A+接受人；覆盖矩阵/方法矩阵/细节维/影响面/核心链路无未接受空格；风险逐类有结论。**目标=完整覆盖方案可验收单元，正确检出缺陷。**
- **计划**：范围/轨道/轮次/批次/探索/准入准出可执行；引用分析与 env-baseline；suite/depth 已声明；覆盖闸 PASS 后才称可执行。
- **执行**：过程（分析/计划/链接/证据/终态/证伪）不过 → FAIL 禁下批；`未执行`/`未本轮验证` 仍在 → FAIL（批未关）；过程完整且仅产品红 → CONDITIONAL 可下批继续找缺陷（须入库）。双读原文+互补源；P0 须证伪；功能记录步骤须可复核。
- **报告**：台账处置=测全终态；P0 全过且有证伪；CONDITIONAL 认 §4 接受人；非 PASS/CONDITIONAL 禁用“全部通过/可发布”。
- **回写**：单号/备注/状态/附件回执；`writeback` 不覆盖 report。

## 4. 成本纪律

- 步后门 `execute -Scope` 只对 Scope 内记录；报告门全仓本轮。
- 失败/阻塞证据必看；通过不要求每条截图；不每补丁全量回归。
