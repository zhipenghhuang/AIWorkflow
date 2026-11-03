# 路径别名（开发规范）

> 对话/口令中的中文路径 → 规范路径。控制面文件与 handoff 类别只在本表维护；正文引用本表，不重复定义。

## 控制面

| 口令/旧路径 | 规范路径 |
| --- | --- |
| 项目档案 / `project-profile.md` | `project-profile.md` |
| 产品档案 / `product-profile.md` | `product-profile.md` |
| 环境基线 / `env-baseline.md` | `env-baseline.md` |
| 文档索引 / 工作区索引 | `{workroot}/INDEX.md`（单包即 `docs/INDEX.md`） |
| inbound/INDEX.md（原件） | `inbound/INDEX.md` |
| 材料库索引 | `docs/materials/INDEX.md` |
| 工作根 | `{workroot}/` |
| 材料库 | `docs/materials/` |
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

## 旧路径迁移

| 旧 | 新 |
| --- | --- |
| `开发/`（或旧工作根） | `{workroot}/`（单包 `docs/`，多包 `docs/development/`） |
| `开发/文档索引.md` | `{workroot}/INDEX.md` |
| `开发/资料/` | `inbound/`（原件）或 `docs/materials/`（权威文档库） |
| `开发/资料/资料索引.md` | `inbound/INDEX.md` |
| `开发/development-plan.md` | `{workroot}/development-plan.md` |
| `开发/工作日志.md` | `{workroot}/work-log.md` |
| `开发/交接/` | `{workroot}/handoff/` |
| `开发/00-项目治理/` | `{workroot}/00-governance/` |
| `开发/01-需求基线/` | `{workroot}/10-requirements/` |
| `开发/02-方案设计/` | `{workroot}/20-design/` |
| `开发/03-技术设计/` | `{workroot}/30-architecture/` |
| `开发/04-计划与任务/` | `{workroot}/40-tasks/` |
| `开发/05-测试与验收/` | `{workroot}/50-verification/` |
| `开发/06-发布与交付/` | `{workroot}/60-release/` |
| `开发/07-运维与协作/` | `{workroot}/70-ops/` |
| `开发/08-复盘与改进/` | `{workroot}/80-retrospectives/` |
| `docs/`（旧原始资料根） | 先判定：原件 → `inbound/`；旧工作根 → `{workroot}/`；混合 → 停问 |
| `开发规范/` 旧包名 | `wf-development/`（多包 `wf/wf-development/`） |
| `项目档案.md` | `project-profile.md` |
