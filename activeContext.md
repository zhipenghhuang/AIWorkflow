# Active Context — AIWorkflow

> 协作面文件；不进公开面。历史见根 `CHANGELOG.md`。

## 当前焦点

`.29.1` 工作区：三包文档治理补强（版本目录平铺、迭代关账前置 T1/T2/T4、归档前引用检查）；三包 `AGENTS.md`/`onboard.yaml` 同步；三包自检与技能检查通过。未提交。

## 进行中

| 项 | 内容 |
| --- | --- |
| 当前任务 ID | `2026.10.29.1` 三包文档治理补强 |
| 状态 | 完成待提交：三包 `.29.1` 已改，三包自检/技能检查通过；截至 2026-10-29 |
| 最后动作 | 三包 `规则/文档治理.md` 增补版本目录平铺与历史原件归档；§3/§7.1 增补关账前置（T1 才归档旧基线，T2/T4 保留仍被引用的基础设计/PRD 基线/测试数据）；`workflows/onboard.yaml` materials/lifecycle 同步；三包 `AGENTS.md` 摘要同步；版本对齐 `.29.1` |
| 未提交文件 | 40 个（含 `.23` 遗留的测试规范改动 + 本次 19 个文件）；以 `git status` 为准 |
| 下一步口令 | `收尾` → `提交`；推送/公开导出单独确认（三包自检已跑） |
| 待确认事项 | 是否提交 `.29.1`；是否同步实例到 `.29.1`；公开面是否随本次发布 |

## 运行时

- 路径：`D:\Alearn\code\deploy\AIWorkflow`
- 协作 remote：`origin` → gitee；公开 remote：`github`
- 公开面：`.public/allowlist.txt` + `.public/gitignore`；根 `AGENTS.md` / `activeContext.md` 不入公开面
- 仅本地：`更新项目资产.bat` / `Update-Assets.ps1`（gitignore）
- 不上线：不在 deploy `online.txt`；提交用本目录或 deploy 的 `commit.bat` 均可
