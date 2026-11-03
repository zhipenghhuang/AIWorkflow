# 路径别名（产品规范）

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
| `产品/`（或旧工作根） | `{workroot}/`（单包 `docs/`，多包 `docs/product/`） |
| `产品/文档索引.md` | `{workroot}/INDEX.md` |
| `产品/资料/` | `inbound/`（原件）或 `docs/materials/`（权威文档库） |
| `产品/资料/资料索引.md` | `inbound/INDEX.md` |
| `产品/product-plan.md` | `{workroot}/product-plan.md` |
| `产品/工作日志.md` | `{workroot}/work-log.md` |
| `产品/交接/` | `{workroot}/handoff/` |
| `产品/01-需求与定义/` | `{workroot}/{ver}/10-requirements/` |
| `产品/02-原型与设计/` | `{workroot}/{ver}/20-design/` |
| `产品/03-变更与缺陷/` | `{workroot}/{ver}/30-changes/` |
| `产品/04-交付与验收/` | `{workroot}/{ver}/40-delivery/` |
| `产品/05-展示与材料/` | `{workroot}/{ver}/50-showcase/` |
| `产品/06-复盘/` | `{workroot}/{ver}/90-retrospectives/` |
| `docs/`（旧原始资料根） | 先判定：原件 → `inbound/`；旧工作根 → `{workroot}/`；混合 → 停问 |
| `产品档案.md` | `product-profile.md` |
