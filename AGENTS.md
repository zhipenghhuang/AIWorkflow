# AGENTS.md

本仓库是 **AI Workflow 母版仓**：维护/发布三包，不是业务执行现场；只复制单个包到项目，不整仓复制。

1. 开工先读 `README.md`（维护约定）和 `activeContext.md`（当前状态/下一步）。
2. 改包后跑三包自检：产品/开发 `规则/tools/Test-Template.ps1`，测试 `规则/tools/Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`，技能 `check_skills.py --strict`。
3. 协作/公开面按 `.public/allowlist.txt` + deploy `surfaces.txt` 的 `split` 规则；根 `AGENTS.md`、`activeContext.md`、`.public/`、`extras/` 不进公开面。
4. 提交用本目录 `commit.bat` / `scripts/commit.ps1` 或 deploy `commit.bat`；默认只提交，推送/公开导出单独确认。
5. **AI 代跑提交（硬）**：用户口令「提交 / 提交推送」时，必须先根据 `activeContext` / diff 写出有内容的提交信息（主题或版本 + 简述，可一行），再喂给 `commit.ps1` 的「提交信息」提示；**禁止**回车接受默认 `update yyyy-MM-dd HH:mm`。人工双击 bat 仍可用默认时间戳。
6. 当前任务/版本/未提交状态只看 `activeContext.md`，历史看 `CHANGELOG.md`。
