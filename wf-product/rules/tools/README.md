# tools（自检 + 校验）

> 改工具/改包时才读；AI 默认只按 `AGENTS.md`/workflow 点名调用。

| 脚本 | 用途 | 运行 |
| --- | --- | --- |
| `Test-Template.ps1` | 包自检：引用/锚点/workflows→agents/步标记/能力名/版本/YAML/密钥扫描 | `powershell -ExecutionPolicy Bypass -File rules/tools/Test-Template.ps1` |
| `Test-DocHygiene.ps1` | 文档卫生/整文件预算：AGENTS、开局卡、global-rules；模板索引；结构/临时文件 | `powershell -ExecutionPolicy Bypass -File rules/tools/Test-DocHygiene.ps1` |
| `validate_workflow.py` | YAML 语法 + workflow/agent schema + step/agent/entry/hitl/when/gate/read_ref 引用 | `python rules/tools/validate_workflow.py .` |
| `build_step_packets.py` | 由 `workflows/*.yaml` 生成链图/步骤卡；`--check` 只检漂移、不落盘 | `python rules/tools/build_step_packets.py . [--check]` |
| `validate_step_packets.py` | 步骤卡 9 节结构/技能存在/整卡读取/生成漂移（`Validate-StepPackets.ps1` 入口） | `powershell -File rules/tools/Validate-StepPackets.ps1 -PackageRoot .` |
| `check_skills.py` | 技能质量：frontmatter/≤500 行/反模式/README 映射 | `python rules/tools/check_skills.py . --strict` |
| `validate_prd.py` | PRD templates/实例校验 | `python rules/tools/validate_prd.py <PRD.md>` |
| `Initialize-Docs.ps1` | 初始化文档树/索引骨架（只建不删；`-Mode single / multi -Owner product`；按档案 `workroot`，未声明按约定） | `powershell -File rules/tools/Initialize-Docs.ps1 -ProjectRoot <项目根> -Mode single -Owner product` |
| `check_secrets.py` | 扫描硬编码口令/Token 字面量（不打印值） | `python rules/tools/check_secrets.py .` |
| `validate_semantics.py` | 语义自检：开局卡结构/global-rules 节/双入口/残句/角色边/预算 | `python rules/tools/validate_semantics.py .` |
| `clean_temp.py` | 临时/缓存/过期日志清理（默认 dry-run；`--reset-frontend` 先归档；archive 用保留窗口显式清理） | `python rules/tools/clean_temp.py --project-root . [--apply] [--reset-frontend] [--gate-archive-keep N] [--gate-archive-days D]` |

- `Test-Template.ps1` 会调用 `validate_workflow.py`（需 Python + PyYAML）；找不到 Python 时显示跳过，不假装通过。
- 改包后跑自检 + 文档卫生；业务任务不例行自检。
