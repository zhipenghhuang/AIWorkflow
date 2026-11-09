# 验证（测试轨）

> 目的：让“分析完整/执行通过/准出”有可对账的证据。门读现有分析/计划/执行记录/报告，不新增测试文档。
> 读取时机：计划门（coverage）、执行批末（execute）、报告（report）、交平台（writeback）。

## 1. 什么时候跑

| 场景 | 命令 | 输出 |
| --- | --- | --- |
| 分析与计划 | `Invoke-Gate.ps1 -Mode coverage` | 分析结构/来源/章节/依据/意图/AC 账本/覆盖矩阵/方法矩阵/细节维/影响面/核心链路 + 计划结构 |
| 执行批末 | `Invoke-Gate.ps1 -Mode execute -Scope "{模块/域}"` | 仅 Scope 内执行记录/证据/P0/意图终态 |
| 报告/准出 | `Invoke-Gate.ps1 -Mode report` | 分析/计划/记录/报告一致；全部 P0/P1/P2 意图终态；场景/意图计数；缺口 |
| 交平台/回写 | `Invoke-Gate.ps1 -Mode writeback` | 平台回执（单号/备注/状态/附件） |
| 完成口令 | `Invoke-Gate.ps1 -Claim -Mode report` | 读 `.gate/wf-testing/report.json`；输出 `CLAIM: ALLOWED/DENIED` |

```powershell
powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Mode coverage -ProjectRoot "."
powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Mode execute -Scope "<模块目录名>" -ProjectRoot "."
powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Mode report -ProjectRoot "."
powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Claim -Mode report -ProjectRoot "."
```

**完成口径**：`-Claim -Mode report` 只认 report 回执；verdict 非 PASS/CONDITIONAL、有阻断、或分析/计划/执行记录/报告在回执后又改动 → `CLAIM: DENIED`。

## 2. 机器门检查

| ID | 模式 | 检查 | 失败处理 |
| --- | --- | --- | --- |
| `analysis-structure` | coverage/execute/report | `test-analysis.md`：来源盘点（总数=已映射+N/A+缺口）、章节回执、依据覆盖、意图台账（INT/来源/意图/Oracle/P0/P1/P2/处置/接受人；非空）、AC/设计点账本、覆盖矩阵/方法矩阵/细节维/影响面/核心链路、风险清单/扫描；章节/依据/AC 的 INT 引用须存在 | FAIL |
| `env-baseline` | coverage/execute/report | `env-baseline.md` 存在且含项目身份/§1 登录/§4 账号/§8 浏览器结构；缺失或空壳 → 不跑 | FAIL |
| `plan-structure` | coverage/execute/report | `test-plan.md`：范围/引用分析/env-baseline/影响面摘要/轨道/轮次/批次/探索/准入准出/suite/depth/环境核验；完整计划轨道/轮次非空、§4.3 S6/S7/S11 有着落；轻量计划 §3 含轮次/准入/准出 | FAIL |
| `execution-record` | execute/report | `*执行记录.md` 场景表（SC/INT/原文依据/优先级/场景/结果/证据；非空、每场景有 INT）+ 意图结论表 + env-baseline；结果合法 | FAIL |
| `evidence-exists` | execute/report | 失败/阻塞/待实现证据可打开；P0 通过有证据 | FAIL |
| `p0-status` | execute/report | P0 场景/意图失败/阻塞/待实现/未执行 → 不得 PASS | FAIL |
| `intent-coverage` | report | 分析中每个 `处置=测` 意图出现在执行记录 | FAIL；execute 仅批内 |
| `intent-conclusion` | execute/report | 每个意图有终态（通过/失败/阻塞/待实现/N/A）；P1/P2 未测同样失败 | FAIL |
| `p0-missing` | report | 分析中 P0 意图未出现在执行记录 | FAIL；execute 仅批内 |
| `report-structure` | report | 报告 §0～§5、§2.1 场景统计（非空）、§2.2 意图结论（非空）、§2.3 覆盖与收口（原文对账/AC/细节维/影响面/核心链路/S6/S7/S11）、§4 缺口；结论唯一 | FAIL |
| `report-verdict` | report | 准出评估/verdict 可解析；PASS 与全部意图终态、失败/未执行、P0/缺口一致；CONDITIONAL 有接受人 | FAIL |
| `writeback-receipt` | writeback | 单号/备注/状态/附件/回执 | FAIL |

## 3. 检查什么

- **分析**：来源盘点/章节/依据无缺口；每个 AC/F/R/N 有意图或 N/A+接受人；AC/设计点账本无未解释缺口；覆盖矩阵/方法矩阵/细节维 D01–D13+S6/S7/S11/影响面/核心链路无未接受空格；P0 有 Oracle/不可接受失败；风险逐类有结论。
- **计划**：范围/轨道/轮次/批次/探索/准入准出/缺陷策略可执行；引用分析路径与 env-baseline；影响面/核心链路摘要齐；suite/depth 已声明；环境/构建/账号/数据/核验不空。
- **执行记录**：场景表非空；每场景有意图/**原文依据**；结果合法；每个意图有终态；失败/阻塞/待实现有证据或原因；P0 通过有证据；env-baseline 命中。开跑原文对账行与来源关账由 execute 步骤卡/模板约束，报告 §2.3 复核。
- **报告**：§2.1 场景计数、§2.2 意图计数与执行记录一致；全部 P0/P1/P2 意图终态；P0 全过或有书面接受；S6/S7/S11/探索有落点；缺口显式列接受人；声明 runId/构建/suite/depth；非 PASS/CONDITIONAL 禁用“全部通过/可发布”。
- **回写**：单号/备注/状态/附件回执；`writeback` 不覆盖 report。

## 4. 成本纪律

- 步后门 `execute -Scope` 只对 Scope 内记录；报告门全仓本轮。
- 失败/阻塞证据必看；通过不要求每条截图；不每补丁全量回归。
