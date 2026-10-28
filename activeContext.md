# Active Context — AIWorkflow

> 协作面文件；不进公开面。历史见根 `CHANGELOG.md`。

## 当前焦点

三包入口判定通用化（`2026.10.28.20`）：五元组→意图类 A～K，适配任意描述句，非固定口令词典。迁入 deploy 为 `split`；公开清单见 `public-surface.txt`。

## 进行中

| 项 | 内容 |
| --- | --- |
| 当前任务 ID | `2026.10.28.20` 三包入口判定通用化 |
| 状态 | 进行中：三包 `.20` 已改，未提交；截至 2026-10-28 21:52 |
| 最后动作 | 更新三包入口判定、README、维护与读取索引；重写本 `activeContext` 当前焦点；新增根 `AGENTS.md` |
| 未提交文件 | 39 个（21 改 / 14 删 / 4 新增）；关键：根 `AGENTS.md`、三包 `AGENTS.md`、根 `README.md`、`CHANGELOG.md`、`activeContext.md`、`public-surface.txt`、新增 `extras/工作交接.md`、新增产品/测试 `规则/核心/入口判定.md`、删除 `extras/work-handoff/` |
| 下一步口令 | `自检`（跑三包脚本）→ `收尾` → `提交`；推送/公开导出单独确认 |
| 待确认事项 | 是否提交并推送 `.20`；是否同步 9 个实例到 `.20`；公开面是否随本次发布 |

## 运行时

- 路径：`D:\Alearn\code\deploy\AIWorkflow`
- 协作 remote：`origin` → gitee；公开 remote：`github`
- 仅本地：`更新项目资产.bat` / `Update-Assets.ps1`（gitignore）
- 不上线：不在 deploy `online.txt`；提交用本目录或 deploy 的 `commit.bat` 均可
