# tools（轻机检 + 脚本档工具）

> 改工具时才读。AI 默认只按 `AGENTS.md` / workflow 点名调用。

| 脚本 | 点名场景 |
| --- | --- |
| `Invoke-TestWorkflow.ps1` | `-Action ValidateTemplateRefs`（引用/锚点/workflows→agents/步标记/能力名/版本单点/YAML 语法/密钥扫描） |
| `Test-DocHygiene.ps1` | 文档卫生/读取预算：AGENTS 行数、规则超长、孤立模板、读取索引 |
| `validate_workflow.py` | YAML 语法 + workflow/agent 基本 schema + step/agent/entry_points/hitl/when/gate 引用（由自检调用） |
| `playwright/executor.mjs` | 脚本档执行器（**复制到项目** `{workroot}/scripts/`，业务无关勿改逻辑；规则 `rules/special/script-execution.md`，用法同目录 `README.md`；`--mode=api` 支持接口轨无浏览器回放） |
| `playwright/config.template.mjs` | 脚本档适配配置模板（复制为项目 `{workroot}/scripts/case-executor.config.mjs`） |
| `validate_testcase.py` | 功能执行记录机检（原文对账/场景表/Oracle/证据/结果） |
| `validate_api_testcase.py` | 接口执行记录机检（原文对账/契约表/场景表/证据/结果） |
| `Initialize-Docs.ps1` | 初始化文档树/索引骨架（只建不删；`-Mode single / multi -Owner testing`；按基线 `workroot`，未声明按约定） | `powershell -File rules/tools/Initialize-Docs.ps1 -ProjectRoot <项目根> -Mode single -Owner testing` |
| `check_secrets.py` | 扫描硬编码口令/Token 字面量（不打印值） |
| `validate_semantics.py` | 语义自检：开局卡结构/global-rules 节/双入口/残句/角色边/预算 | `python rules/tools/validate_semantics.py .` |
| `clean_temp.py` | 临时/脏文件清理（默认 dry-run，只动缓存与过期临时） | `python rules/tools/clean_temp.py --project-root . [--apply]` |

接入核验由 `agents/onboard-agent.yaml` 接入清单执行，**不**另跑落地脚本（脚本档按需，见接入清单 ⑥）。

```text
wf-testing/rules/tools/Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs
```
