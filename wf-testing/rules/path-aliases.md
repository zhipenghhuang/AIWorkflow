# 路径别名（测试规范）

> 对话/口令中的中文路径 → 规范路径。控制面文件与 handoff 类别只在本表维护；正文引用本表。

## 控制面

| 口令/路径 | 规范路径 |
| --- | --- |
| 项目档案 / `project-profile.md` | `project-profile.md` |
| 产品档案 / `product-profile.md` | `product-profile.md` |
| 环境基线 / `env-baseline.md` | `env-baseline.md` |
| 文档索引 / 工作区索引 | `{workroot}/INDEX.md`（单包即 `docs/INDEX.md`） |
| inbound/INDEX.md | `inbound/INDEX.md` |
| 材料库索引 | `docs/materials/INDEX.md` |
| 工作根 | `{workroot}/` |
| 材料库 | `docs/materials/` |
| 测试分析 | `{workroot}/{ver}/test-analysis.md` |
| 测试计划 / 总排 | `{workroot}/{ver}/test-plan.md` |
| 执行记录 | `{workroot}/{ver}/functional|api/{NN}-{短名}-执行记录.md` |
| 探索记录 | `{workroot}/{ver}/exploratory/{主题}-{戳}-探索记录.md` |
| 随机记录 / 覆盖账本 / 体验建议 | `{workroot}/{ver}/random-flows/{主题}-{戳}-随机记录.md`；账本 `{workroot}/{ver}/random-flows/_覆盖账本.md`；建议 `{workroot}/{ver}/random-flows/_体验建议.md` |
| 发布前专项 | `{workroot}/{ver}/pre-release/{专项}-…` |
| 证据 | `{workroot}/{ver}/evidence/` |
| 回归锚点 / 冒烟清单 | `{workroot}/smoke-checklist.md` |
| 主业务旅程清单（随机） | `{workroot}/journey-map.md` |
| 测试报告 | `{workroot}/{ver}/test-report.md` |
| 当前迭代夹 | `{workroot}/{ver}/` |
| handoff-ledger.md | `{workroot}/handoff/handoff-ledger.md` |

## 交接类别

| 中文/口令 | category id |
| --- | --- |
| 需求 | `requirements` |
| 设计 | `design` |
| 计划 | `plan` |
| 提测 | `qa` |
| 报告 | `report` |
| 缺陷 | `bug` |
| 回归/修复 | `fix` |
| 澄清 | `clarification` |
| 发布 | `release` |
| 验收 | `uat` |
| 变更 | `change` |
| 复盘 | `retro` |
| 确认/决策 | `decision` |
| 待分拣 | `unsorted` |
