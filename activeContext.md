# Active Context — AIWorkflow

> 协作面文件；不进公开面。历史见根 `CHANGELOG.md`。

## 当前焦点

`.23` 工作区：三包 `activeContext` 新增 `### 进行中` 跨会话快照 + 文档质量标准「当前有效状态（硬）」；公开面已迁 `.public/`。未提交。

## 进行中

| 项 | 内容 |
| --- | --- |
| 当前任务 ID | `2026.10.28.23` 工作区收尾（含 activeContext 进行中快照） |
| 状态 | 进行中：三包 `.23` 已改，三包自检通过，未提交；截至 2026-10-28 22:22 |
| 最后动作 | 三包 activeContext 模板新增 `### 进行中`，同步 AGENTS/执行契约/收尾骨架/读取索引/模板索引/文档治理；明确单包独立为默认、多包联动可选、跨包同步仅多包填写；三包文档质量标准新增「当前有效状态（硬）」；修复 `§1.9` 引用；根 AGENTS 公开面说明改 `.public/allowlist.txt`；三包自检通过 |
| 未提交文件 | 47 个（45 改 / 2 新增）；关键：三包 activeContext 模板、AGENTS、执行契约、收尾骨架、读取索引、模板索引、文档治理、规则治理；根 AGENTS/CHANGELOG/activeContext、`.public/allowlist.txt`；开发规范版本策略两份新增；提交前以 `git status` 为准 |
| 下一步口令 | `收尾` → `提交`；推送/公开导出单独确认（三包自检已跑） |
| 待确认事项 | 是否提交并推送 `.23`；是否同步实例到 `.23`；公开面是否随本次发布 |

## 运行时

- 路径：`D:\Alearn\code\deploy\AIWorkflow`
- 协作 remote：`origin` → gitee；公开 remote：`github`
- 公开面：`.public/allowlist.txt` + `.public/gitignore`；根 `AGENTS.md` / `activeContext.md` 不入公开面
- 仅本地：`更新项目资产.bat` / `Update-Assets.ps1`（gitignore）
- 不上线：不在 deploy `online.txt`；提交用本目录或 deploy 的 `commit.bat` 均可
