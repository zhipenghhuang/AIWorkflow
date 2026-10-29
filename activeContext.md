# Active Context — AIWorkflow

> 协作面文件；不进公开面。历史见根 `CHANGELOG.md`。

## 当前焦点

测试规范 2026.10.29.18：准出门槛（迭代≥module / 发版=full）+ 冲突清扫完成。

## 进行中

| 项 | 内容 |
| --- | --- |
| 当前任务 ID | MAINT-20261029-TEST-EVERGREEN |
| 状态 | 完善加固已落地；自检 OK |
| 最后动作 | 准出门槛强化；清 README/多Agent/报告/onboard/agents 旧冲突；版本 2026.10.29.18 |
| 未提交文件 | 见 `git status` |
| 下一步口令 | 确认是否提交/推送 |
| 待确认事项 | 是否提交/推送；IBIPS 另案迁移 |

## 运行时

- 路径：`D:\Alearn\code\deploy\AIWorkflow`
- 协作 remote：`origin` → gitee；公开 remote：`github`
- 公开面：`.public/allowlist.txt` + `.public/gitignore`；根 `AGENTS.md` / `activeContext.md` 不入公开面
- 仅本地：`更新项目资产.bat` / `Update-Assets.ps1`（gitignore）
- 不上线：不在 deploy `online.txt`；提交用本目录或 deploy 的 `commit.bat` 均可
