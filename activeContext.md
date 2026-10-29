# Active Context — AIWorkflow

> 协作面文件；不进公开面。历史见根 `CHANGELOG.md`。

## 当前焦点

开发规范跨层一致性规则/技能优化（2026.10.29.12）。

## 进行中

| 项 | 内容 |
| --- | --- |
| 当前任务 ID | MAINT-20261029-CROSS-LAYER |
| 状态 | 已完成分析/母版改动；待用户确认是否提交/推送 |
| 最后动作 | 新增 `技能/cross-layer-consistency`；四维矩阵挂到需求/方案/任务/实现/评审/测试/缺陷；自检通过 |
| 未提交文件 | `CHANGELOG.md`、`开发规范/AGENTS.md`、`开发规范/规则/读取索引.md`、`开发规范/验证/检查矩阵.yaml`；其余改动已被自动提交 `6faf992` |
| 下一步口令 | 确认提交/推送，或先审阅拟提交清单 |
| 待确认事项 | 是否把本批母版改动提交并推送 |

## 运行时

- 路径：`D:\Alearn\code\deploy\AIWorkflow`
- 协作 remote：`origin` → gitee；公开 remote：`github`
- 公开面：`.public/allowlist.txt` + `.public/gitignore`；根 `AGENTS.md` / `activeContext.md` 不入公开面
- 仅本地：`更新项目资产.bat` / `Update-Assets.ps1`（gitignore）
- 不上线：不在 deploy `online.txt`；提交用本目录或 deploy 的 `commit.bat` 均可
