# 验证（测试轨）

> 目的：让“测试通过/准出”有可对账的证据。门读现有测试计划/台账/报告，不新增测试文档。
> 读取时机：`review-cases`、`execute` 批末、`report`、`handoff`/交平台前。维护读 `规则/核心/规则治理.md`。

## 1. 什么时候跑

| 场景 | 命令 | 输出 |
| --- | --- | --- |
| 生成覆盖 | `Invoke-Gate.ps1 -Mode coverage` | §3 映射/ID + §4 深度档自检/视觉基础行 |
| 用例评审 | `Invoke-Gate.ps1 -Mode review` | 评审记录结构/独立性/放行结论（`.gate/测试规范/review.json`） |
| 执行批末（步后门） | `Invoke-Gate.ps1 -Mode execute -Scope "{模块}"` | **仅 Scope 内**台账/证据/P0；回执含 `scope` |
| 出报告/准出（准出门） | `Invoke-Gate.ps1 -Mode report` | 扫各轨现行台账；**只计本轮装填**（排除「未本轮验证」）；忽略 Scope |
| 交平台/回写 | `Invoke-Gate.ps1 -Mode writeback` | 平台回执检查（不覆盖 report） |
| 收尾自检 | `python 验证/tools/check_compliance.py --report <收尾文件>` | 【验证回执】+【遵守自检】route/mode/reads |

```powershell
# 模块批末（例 M16）
powershell -ExecutionPolicy Bypass -File "测试规范/验证/Invoke-Gate.ps1" -Mode execute -Scope "功能测试/ASN" -ProjectRoot "."
# 版本准出
powershell -ExecutionPolicy Bypass -File "测试规范/验证/Invoke-Gate.ps1" -Mode report -ProjectRoot "."
```

## 2. 检查什么

- **计划**：`测试/测试计划.md` 存在；§0 状态、§5 准出、§9.2 编排、§11 缺陷策略、§12 探索章程可读；§3.7/§9.2 与 `00-稳定冒烟清单` 的 P0 用例必须进台账且为本轮终态。
- **台账**：路径宜为 `{轨}/{NN}-{短名}/*-功能台账.md` 或 `*-接口台账.md`（兼容旧名）；§1.1 本轮装填与 §2 非「未本轮验证」行一致；`未本轮验证` 不计通过率；P0 不得为未本轮验证。
- **P0**：P0-Smoke / P0-HighRisk 未通过、未执行、未本轮验证或计划有但台账缺失时，报告不得写 PASS/整体通过。
- **报告**：§4 数字与台账**本轮装填**一致；须声明 suite/depth/本轮构建；§1 准出评估唯一且与 P0/本轮未执行/缺口一致；回执与门一致。§5 硬项见检查矩阵。
- **覆盖**：功能全量/专项 §3 映射无空行且映射到真实用例 ID；§4 含「深度档自检」「视觉基础」行（缺则 FAIL）；报告/coverage 模式功能资产必须有映射；P0 点有用例或“不适用+依据”。语义是否达标见评审量规，门不臆造深度分数。
- **用例评审**：存在现行 `评审-*.md`（合卷/计划）或 `*-评审-*.md`（单域 C 命名）；可解析结论（放行执行/有条件放行/需修后放行）；含独立性与量规/严重度痕迹；放行时不得残留未消化阻断；有条件放行须有接受人；语义量规由 AI 按技能执行，机器只核结构与放行态。批次数见 `工作流` §2.5。
- **回写**：交平台时存在回执（单号/备注/状态/附件）；`writeback` 只写 `.gate/测试规范/writeback.json`，不要求计划/台账，不覆盖 report。
- **口径**：只统计当前台账本轮行，`_归档`/`.draft`/`资料`/`证据`/`未本轮验证` 不参与准出对账。

## 3. 完成状态

> `PASS/CONDITIONAL/FAIL/BLOCKED` 条件与报告措辞见 `规则/核心/验证规则.md` §2；本文件不重复状态表。回执中文：可准出/有条件准出/不准出/阻塞；机器仍读 PASS/CONDITIONAL/FAIL/BLOCKED。

## 4. 成本纪律

- **步后窄 / 准出本轮**：域批末 = `execute -Scope`；宣称准出 = `report`（本轮装填口径）。二者不可混用。
- execute 上 `coverage-map` / `p0-missing` 为 soft（矩阵 optional），不单独拉垮本批；report 仍硬。
- 门只读现有计划/台账/报告，不新增文档；证据失败/阻塞必看。
- 迭代准出 suite≥module；发版/完整项目=full；补丁=core+窄影响面且报告标明补丁口径；报告须声明 suite + 本轮构建。
