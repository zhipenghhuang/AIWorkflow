# 规则/tools 脚本说明

| 脚本 | 用途 | 运行 |
| --- | --- | --- |
| `Test-Template.ps1` | 包自检：引用/锚点/workflows→agents/步标记/能力名/版本/YAML 语法/开发计划模板 schema | `powershell -ExecutionPolicy Bypass -File 规则/tools/Test-Template.ps1` |
| `Test-DocHygiene.ps1` | 文档卫生/读取预算：AGENTS 行数、规则超长、孤立模板、读取索引 | `powershell -ExecutionPolicy Bypass -File 规则/tools/Test-DocHygiene.ps1` |
| `validate_workflow.py` | YAML 语法 + workflow/agent 基本 schema + step/agent/entry_points/hitl/when/gate 引用 | `python 规则/tools/validate_workflow.py .` |
| `validate_tasklist.py` | 任务清单模板/实例校验：章节/列/ID/状态/依赖/任务卡字段/RP 覆盖 | `python 规则/tools/validate_tasklist.py <清单路径>` |
| `validate_dev_plan.py` | 开发计划校验：阶段/门/状态/下一步/关键节/链接 | `python 规则/tools/validate_dev_plan.py <开发计划路径>` |
| `Initialize-Docs.ps1` | 初始化文档树/索引骨架（只建不删；默认 `开发/`；`-DocsRoot` 兼容旧仓如 `docs/`，非第三套概念；搬迁仍需确认） | `powershell -File 规则/tools/Initialize-Docs.ps1 -ProjectRoot <项目根> -DocsRoot 开发` |

- `Test-Template.ps1` 会调用 `validate_workflow.py`（需要 Python + PyYAML）；找不到 Python 时显示“跳过”，不假装通过。  
- 改包后跑自检；任务清单写完先跑 `validate_tasklist.py`，开发计划写完先跑 `validate_dev_plan.py` 再确认。  
- 脚本只读，不改文件；路径以包根/清单实际路径为准。
