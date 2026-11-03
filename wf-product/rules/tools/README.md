# tools（自检 + 校验）

> 改工具/改包时才读；AI 默认只按 `AGENTS.md`/workflow 点名调用。

| 脚本 | 用途 | 运行 |
| --- | --- | --- |
| `Test-Template.ps1` | 包自检：引用/锚点/workflows→agents/步标记/能力名/版本/YAML/密钥扫描 | `powershell -ExecutionPolicy Bypass -File rules/tools/Test-Template.ps1` |
| `Test-DocHygiene.ps1` | 文档卫生/读取预算：AGENTS 行数、规则超长、孤立模板、读取索引 | `powershell -ExecutionPolicy Bypass -File rules/tools/Test-DocHygiene.ps1` |
| `validate_workflow.py` | YAML 语法 + workflow/agent schema + step/agent/entry/hitl/when/gate/read_ref 引用 | `python rules/tools/validate_workflow.py .` |
| `validate_prd.py` | PRD templates/实例校验 | `python rules/tools/validate_prd.py <PRD.md>` |
| `Initialize-Docs.ps1` | 初始化文档树/索引骨架（只建不删；`-Mode single / multi -Owner product`；按档案 `workroot`，未声明按约定） | `powershell -File rules/tools/Initialize-Docs.ps1 -ProjectRoot <项目根> -Mode single -Owner product` |
| `check_secrets.py` | 扫描硬编码口令/Token 字面量（不打印值） | `python rules/tools/check_secrets.py .` |

- `Test-Template.ps1` 会调用 `validate_workflow.py`（需 Python + PyYAML）；找不到 Python 时显示跳过，不假装通过。
- 改包后跑自检 + 文档卫生；业务任务不例行自检。
