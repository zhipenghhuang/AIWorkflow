# 流程链 · testing

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：wf-testing
- **workflow**：`testing`（AI测试流程）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 入口

- `分析需求` → step `analyze`
- `理解PRD` → step `analyze`
- `理解 PRD` → step `analyze`
- `梳理测试依据` → step `analyze`
- `需求建模` → step `analyze`
- `测试计划` → step `plan`
- `生成测试计划` → step `plan`
- `功能测试计划` → step `plan`
- `更新计划` → step `plan`
- `本期变更` → step `plan`
- `计划变更` → step `plan`
- `增量变更` → step `plan`
- `新文档更新测试计划` → step `plan`
- `按测试计划执行` → step `execute`
- `按计划执行` → step `execute`
- `执行测试计划` → step `execute`
- `继续测试计划` → step `execute`
- `回归` → step `execute`
- `重跑` → step `execute`
- `脚本执行` → step `execute`

## 状态机（父）→ 子机

长链路按**子状态机**切开：进某区先读该区 `_region-*`（一次），区内逐步推进；不要把整条父链步骤包一次读完。

| 子机 | 含义 | 地图 |
| --- | --- | --- |
| `prep` | 分析计划 | `rules/packets/testing/_region-prep.md` |
| `run` | 执行报告 | `rules/packets/testing/_region-run.md` |
| `close` | 交接收尾 | `rules/packets/testing/_region-close.md` |

## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `status` | 当前状态与下一步 | `—` | `_region-prep` | `rules/packets/testing/status.md` |
| 2 | `analyze` | 分析需求 | `—` | `_region-prep` | `rules/packets/testing/analyze.md` |
| 3 | `plan` | 测试计划 | `—` | `_region-prep` | `rules/packets/testing/plan.md` |
| 4 | `generate` | 生成用例 | `—` | `_region-prep` | `rules/packets/testing/generate.md` |
| 5 | `review-cases` | 用例与多轨资产评审 | `—` | `_region-prep` | `rules/packets/testing/review-cases.md` |
| 6 | `execute` | 执行测试 | `—` | `_region-run` | `rules/packets/testing/execute.md` |
| 7 | `report` | 输出报告 | `—` | `_region-run` | `rules/packets/testing/report.md` |
| 8 | `handoff` | 收尾与提交确认 | `—` | `_region-close` | `rules/packets/testing/handoff.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次；出区再进下一子机。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
