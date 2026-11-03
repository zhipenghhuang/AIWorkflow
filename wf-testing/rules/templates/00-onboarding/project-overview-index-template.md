# 项目总览索引模板

> 落盘：`docs/INDEX.md`，用于多包或「保留原有目录 + 旁挂标准树」的项目。
> 单包不另建：`docs/INDEX.md` 就是工作区索引（见 `workspace-index-template.md`）。
> 只做入口与既有目录说明；**不写阶段/门/状态**；不替代各工作区 `INDEX.md`、`docs/materials/INDEX.md`、`inbound/INDEX.md`。

# 项目文档总览 — {{项目}}

> 更新：{{yyyy-MM-dd HH:mm}} ｜ 维护：AI 自动更新

## 1. 工作区索引

> 多包示例；只保留已装包行，未装删除；单包不建本文件。

| 包 | 工作区 | 索引 |
| --- | --- | --- |
| {{wf-product / 产品}} | `docs/product/` | `docs/product/INDEX.md` |
| {{wf-development / 开发}} | `docs/development/` | `docs/development/INDEX.md` |
| {{wf-testing / 测试}} | `docs/testing/` | `docs/testing/INDEX.md` |

## 2. 项目级控制面

| 项 | 路径 |
| --- | --- |
| 权威文档库 | `docs/materials/INDEX.md` |
| 外部原件 | `inbound/INDEX.md` |
| 工作根 | 见环境基线“项目身份”（默认单包 `docs/`、多包 `docs/{owner}/`） |
| 跨包快照 | `activeContext.md` |

## 3. 既有项目目录（未迁移）

> 保留原目录不动，只在此登记用途；迁移或删除须先确认。

| 目录 | 内容 | 处置 |
| --- | --- | --- |
| {{原目录/}} | {{用途}} | 保留 / 逐步吸收 / 待确认 |
