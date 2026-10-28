# AGENTS.md

本仓库是 **AI Workflow 母版仓**：维护/发布三包，不是业务执行现场；只复制单个包到项目，不整仓复制。

1. 开工先读 `README.md`（维护约定）和 `activeContext.md`（当前状态/下一步）。
2. 改包后跑三包自检：产品/开发 `规则/tools/Test-Template.ps1`，测试 `规则/tools/Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`，技能 `check_skills.py --strict`。
3. 协作/公开面按 `public-surface.txt` + deploy `surfaces.txt` 的 `split` 规则；`public-surface.txt`、`public.gitignore`、`extras/`、`activeContext.md` 不进公开面。
4. 提交用本目录 `commit.bat` 或 deploy `commit.bat`；默认只提交，推送/公开导出单独确认。
5. 当前任务/版本/未提交状态只看 `activeContext.md`，历史看 `CHANGELOG.md`。
