# Active Context — AIWorkflow

> 协作面文件；不进公开面。历史见根 `CHANGELOG.md`。

## 当前焦点

补「AI 代跑提交须写提交信息」硬规则（母版根 `AGENTS.md` + deploy `AGENTS.md` + `scripts/commit.ps1` 注释）。

## 进行中

| 项 | 内容 |
| --- | --- |
| 当前任务 ID | `2026.10.29.2` AI 提交信息硬规则 |
| 状态 | 已改待提交：根 `AGENTS.md` 第 5 条；deploy `AGENTS.md` 同步；`commit.ps1` 注释提示 |
| 最后动作 | 明确：口令「提交/提交推送」时 AI 必须喂有内容的提交信息，禁止回车用 `update 时间戳`；人工双击仍可用默认 |
| 未提交文件 | 以 `git status` 为准（本仓 + 上级 deploy `AGENTS.md`） |
| 下一步口令 | `提交推送`（本仓）；deploy 根 `AGENTS.md` 另用 deploy `commit.bat` |
| 待确认事项 | 无 |

## 运行时

- 路径：`D:\Alearn\code\deploy\AIWorkflow`
- 协作 remote：`origin` → gitee；公开 remote：`github`
- 公开面：`.public/allowlist.txt` + `.public/gitignore`；根 `AGENTS.md` / `activeContext.md` 不入公开面
- 仅本地：`更新项目资产.bat` / `Update-Assets.ps1`（gitignore）
- 不上线：不在 deploy `online.txt`；提交用本目录或 deploy 的 `commit.bat` 均可
