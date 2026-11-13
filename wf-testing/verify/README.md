# 验证（测试轨）

> 目的：让“分析完整/执行通过/准出”有可对账的证据。门读现有分析/计划/执行记录/报告，不新增测试文档。
> 读取时机：计划门（coverage）、执行批末（execute）、报告（report）、交平台（writeback）、材料库发布（materials）。

## 1. 什么时候跑

| 场景 | 命令 | 输出 |
| --- | --- | --- |
| 分析与计划 | `Invoke-Gate.ps1 -Mode coverage` | 分析结构/来源/章节/依据/意图/AC 账本/覆盖矩阵/方法矩阵/细节维/影响面/核心链路 + 计划结构 |
| 执行批末 | `Invoke-Gate.ps1 -Mode execute -Scope "{模块/域}"` | 分析/计划结构硬判 + Scope 内记录/证据/INT∈§2.1/终态/证伪；过程完整且仅产品红 → CONDITIONAL |
| 报告/准出 | `Invoke-Gate.ps1 -Mode report` | 分析/计划/记录/报告一致；全部 P0/P1/P2 意图终态；场景/意图计数；缺口 |
| 交平台/回写 | `Invoke-Gate.ps1 -Mode writeback` | 平台回执（单号/备注/状态/附件）；回归写回另查范围卡（构建/范围/冒烟/影响面/未覆盖） |
| 材料库发布 | `Invoke-Gate.ps1 -Mode materials -Version "{ver}"` | README/INDEX 齐、文件全登记、无草稿/证据、无密钥、链接自包含；来源与旧版本状态人工核 |
| 完成口令 | `Invoke-Gate.ps1 -Claim -Mode report` | 读 `.gate/wf-testing/report.json`；输出 `CLAIM: ALLOWED/DENIED` |

```powershell
powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Mode coverage -ProjectRoot "."
powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Mode execute -Scope "<模块目录名>" -ProjectRoot "."
powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Mode report -ProjectRoot "."
powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Mode materials -Version "{ver}" -ProjectRoot "."
powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Claim -Mode report -ProjectRoot "."
```

**完成口径**：`-Claim -Mode report` 只认 report 回执；verdict 非 PASS/CONDITIONAL、有阻断、或分析/计划/执行记录/报告在回执后又改动 → `CLAIM: DENIED`。`-Mode report` 的 PASS/CONDITIONAL 均可进入 closeout（CONDITIONAL 须报告 §4 有非空接受人）；是否可写“完成/准出”仍只看 `-Claim`。

## 2. 机器门检查

| ID | 模式 | 检查 | 失败处理 |
| --- | --- | --- | --- |
| `analysis-structure` | coverage/execute/report | `test-analysis.md`：来源盘点、章节回执、依据覆盖、**§2.1 意图台账**、§2.1.1 设计点账本、覆盖/方法矩阵、细节维、影响面、核心链路、风险、§6；**账本不得为空表**；§1.1 的已映射/总数须被 §1.2/§1.3/§2.1.1 实际行数支撑；§2.2/§2.3/§2.4 的 INT 须∈台账；§4 缺口表、§5.2 变更追溯、§6 11 项齐全 | FAIL（三模式同硬） |
| `env-baseline` | coverage/execute/report | `env-baseline.md` 存在且含项目身份/§1 登录/§4 或 §2.2 账号/§8 浏览器结构；缺失或空壳 → 不跑 | FAIL |
| `plan-structure` | coverage/execute/report | `test-plan.md`：范围/引用分析/env-baseline/影响面摘要/轨道/轮次/批次/探索/准入准出；§0 须有 计划状态/版本准出/准出口径/风险档/分析计数；suite/depth 有效且 core 仅补丁；迭代正式轨硬纳入（整轨否仅 §0 白名单+接受人，拒软理由）；T1+ 章程数；§4.3 S6/S7/S11 | FAIL（三模式同硬） |
| `plan-analysis-link` | coverage/execute/report | 计划 §0 计数=分析 §2.1；lite 不得 `版本准出=是`；版本准出/准出口径不冲突；发版须 full+full；完整版本计划须有 P0（§4 可豁免）；§3.1 批次意图范围覆盖全部 `处置=测`（写「全部」视为覆盖）；T1+ 功能细节维不得全否 | FAIL |
| `plan-state` | execute/report | §0 计划状态 ∈ 已确认/执行中/待关闭 | FAIL |
| `batch-coverage` | execute | 记录 §0 批次 ID 在计划 §3.1；该批意图范围已被场景覆盖（写「全部」的批只校验批次存在） | FAIL |
| `execution-record` | execute/report | 场景表非空；每场景有 INT/优先级/场景/实际/差异；**§0 有分析索引（`test-analysis.md` 命中节）**；**`原文/依据` = 原文对应段（有互补源则对照；分析不作互补源）**；§0「原文 / 对照」+ 原文对账 `可验收单元 N` 且 `已覆盖+补录 ≥ N`、未关0/接受人；功能 §1.1 六类各有 SC 或 N/A+依据（UI/视觉禁「API 主断言/脚本/契约」充 N/A）；接口 §2.1 适用维有 SC 或不适用+依据；优先级与 §2.1 一致（仅 P0 记账，测试依据仍原文）；功能步骤 3～7；失败/待实现有缺陷号或拟提交处置；通过须可观测 Oracle；§3 意图结论表有场景 ID 且回指 §1 | FAIL |
| `evidence-exists` | execute/report | 失败/阻塞/待实现证据可打开；P0 通过有证据 | FAIL |
| `intent-analysis-link` | execute/report | 执行 INT 须在 **§2.1 台账**（设计点不能冒充）；分析只作索引，**不作 Oracle 来源、不作互补源** | FAIL |
| `p0-status` | execute/report | P0 场景/意图失败 → execute 在过程完整时可为 CONDITIONAL（可下批）；report 不得 PASS；P0 以分析 §2.1 优先级为准 | execute: CONDITIONAL；report: 不得 PASS |
| `p0-falsify` | execute/report | P0 仅正向通过 → FAIL（须证伪/负向场景或 N/A+接受） | FAIL |
| `intent-coverage` | report | 每个 `处置=测` 台账意图有**实际场景**（§3 声明不算）；无测项台账 → FAIL | FAIL；execute 仅批内 |
| `intent-scenes` | report | 每个 `处置=测` 意图在场景表出现；只有 §3 结论无场景 → FAIL | FAIL |
| `intent-conclusion` | execute/report | 每个意图有终态（通过/失败/阻塞/待实现/N/A）；P1/P2 未测同样失败 | FAIL |
| `p0-missing` | report | 分析中 P0 意图无场景执行 | FAIL；execute 仅批内 |
| `track-records` | report | 计划纳入轨道有**实质**记录（Q18）：功能→`functional/`；接口→非空 `api/*执行记录`（契约+场景；禁空壳）；探索→非空 `*探索记录`（章程+风险点/会话；已跑数≤实质记录数）；发布前→非空方案+`*test-report` | FAIL |
| `report-structure` | report | 报告 §0～§5、§2.1/§2.2 计数、§2.3 覆盖与收口、§4 缺口；§2.2 通过/失败/阻塞/待实现与执行记录一致；细节维 x/16 对分析适用数；原文对账未关>0 不得 PASS；suite/depth 对计划；结论唯一 | FAIL |
| `report-verdict` | report | 准出可解析；与 P0/意图终态/失败一致；发版 PASS 须 full/full | FAIL |
| `conditional-acceptor` | report | CONDITIONAL 须 §4 缺口表非空接受人（须用户确认口径，Q19；门检结构非空） | FAIL |
| `writeback-receipt` | writeback | 单号/备注/状态/附件/回执；回归写回须构建/范围/冒烟/影响面/未覆盖（未跑须接受人） | FAIL |

## 3. 检查什么

- **分析**：§2.1 台账完整（具体 INT+可观测 Oracle）；来源/章节/依据/AC 账本非空，且 §1.1 计数被实际账本行数支撑；每个 AC/F/R/N 映射台账或 N/A+接受人；覆盖矩阵/方法矩阵/细节维/影响面/核心链路无未接受空格且 INT 回指台账；风险逐类有结论。**目标=完整覆盖方案可验收单元，正确检出缺陷。**
- **计划**：范围/轨道/轮次/批次/探索/准入准出可执行；引用分析与 env-baseline；§0 计数/版本准出/准出口径/批次意图范围与 §2.1 联动；suite/depth 已声明且 core 仅补丁；覆盖闸 PASS 后才称可执行。
- **执行**：过程（分析/计划/链接/证据/终态/证伪）不过 → FAIL 禁下批；`未执行`/`未本轮验证` 仍在 → FAIL（批未关）；过程完整且仅产品红 → CONDITIONAL 可下批继续找缺陷（须入库）。**三步序方法**：方案原文 → 结合分析理解 → 现场择优（有互补源则对照）；门检要求 §0 有分析索引、每场景有实际/差异；优先级以分析 §2.1 为准；§3 意图结论须有场景 ID；P0 须证伪；功能记录 3～7 步且可复核。
- **报告**：台账处置=测有实际场景且全终态；§2.2 通过/失败/阻塞/待实现与记录一致；P0 全过且有证伪；细节维 x/16 对分析适用数；计划纳入轨道有对应记录；CONDITIONAL 认 §4 接受人；非 PASS/CONDITIONAL 禁用“全部通过/可发布”。
- **回写**：单号/备注/状态/附件回执；`writeback` 不覆盖 report。回执优先 `{ver}/写回回执.md`（本轮覆盖）；亦认存量 `functional|api|evidence` 下含 `回执`/`回写` 的 md（排除 `_archive`/`.draft` 与按日散落）；多份时优先固定名。回归写回另核范围卡：构建/范围（默认|扩大）/冒烟/影响面/未覆盖；未跑或未覆盖须有接受人。

## 4. 成本纪律

- 步后门 `execute -Scope` 只对 Scope 内记录；报告门全仓本轮。
- 失败/阻塞证据必看；通过不要求每条截图；不每补丁全量回归。
- 门默认全严格；`-Strict` 为兼容开关，不存在放宽模式。

## 5. 门自测

```powershell
python wf-testing/verify/tools/selftest_gate.py
```

正例（coverage/execute/report PASS）+ 反例：来源计数大于账本行、矩阵写假 INT、lite 声明版本准出、幽灵意图（§3 无场景）、P0 改写、P0 记不适用、无 P0、计划草稿态、批次 ID 不匹配、软性发布前 N/A、软性接口 N/A、空壳探索记录等（以脚本内用例为准）。改 `test_gate.py` 后必须跑；输出 `SELFTEST OK (n/n)` 且 n 与脚本用例数一致才可提交。
