# tools（轻机检 + 脚本档工具）

> 改工具时才读。AI 默认只按 `AGENTS.md` / workflow 点名调用。

| 脚本 | 点名场景 |
| --- | --- |
| `Invoke-TestWorkflow.ps1` | `-Action ValidateTemplateRefs`（引用/锚点/workflows→agents/步标记/能力名/版本单点/YAML 语法/密钥扫描） |
| `Test-DocHygiene.ps1` | 文档卫生/读取预算：AGENTS 行数、规则超长、孤立模板、读取索引 |
| `validate_workflow.py` | YAML 语法 + workflow/agent 基本 schema + step/agent/entry_points/hitl/when/gate 引用（由自检调用） |
| `playwright/executor.mjs` | 脚本档执行器（**复制到项目** `{workroot}/scripts/`，业务无关勿改逻辑；规则 `rules/special/script-execution.md`，用法同目录 `README.md`；`--mode=api` 支持接口轨无浏览器回放） |
| `playwright/config.template.mjs` | 脚本档适配配置模板（复制为项目 `{workroot}/scripts/case-executor.config.mjs`） |
| `merge-ledger.mjs` | jsonl → 台账机械合并（双格式：功能台账 §1 计数+§2 行；接口台账 判定/计数/空列补摘要；人工已填不覆盖） |
| `Initialize-Docs.ps1` | 初始化文档树/索引骨架（只建不删；`-Mode single / multi -Owner testing`；读/建 `layout.yaml`） | `powershell -File rules/tools/Initialize-Docs.ps1 -ProjectRoot <项目根> -Mode single -Owner testing` |
| `check_secrets.py` | 扫描硬编码口令/Token 字面量（不打印值） |

接入核验由 `agents/onboard-agent.yaml` 接入清单执行，**不**另跑落地脚本（脚本档按需，见接入清单 ⑥）。

```text
wf-testing/rules/tools/Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs
```
