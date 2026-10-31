# 包内专业技能（随包生效 · 无需安装/挂载）

> **定位**：每一步的**专业方法与手艺**（playbook），随本包分发。命中步骤 → 步骤注记直接加载对应 `技能/<name>/SKILL.md` → 按技能标准执行。  
> **目录结构**：`技能/<name>/SKILL.md`（`name` 取 frontmatter）；随包复制、**无需安装**；AGENTS/步注直接按路径读取。宿主支持本地 skills 根时，可把 `技能/` 指向本地 skills 目录（可选，不是前置条件）。  
> **更新**：可就地改本目录。口令「体检能力」检查/优化（确认后应用）；「通用优化技能」按通用最优。外部工具/skill 选型写入实例 `测试/能力/`（「装配能力」）；包内 `能力/` 仅契约与参考目录。  
> **格式**：每份技能含 `name` / `description` frontmatter（Agent Skills 兼容），description 写“做什么 + 何时用 + 中文触发词”；正文为方法/步骤/判定/反模式/验证，单文件目标 ≤500 行（超长拆 `references/`）。质量标准见本文末节。
> **来源**：以下技能是参考 GitHub/企业实践后**改写整合**的中文随包技能，不是把 GitHub 仓库原样搬入；外部 GitHub skill 走 `能力/00-能力契约.md`（可选）。
> **与「规则」的区别**：技能给方法；红线/口径/门以 `AGENTS.md` 与 `规则/` 为准（冲突时规则优先）。  
> **整合来源**（方法参考，已改写适配为中文随包版，非逐字复制）：Agent Skills 规范（agentskills.io；frontmatter/渐进披露/≤500 行）、anthropics/skills、addyosmani/agent-skills（MIT；skill anatomy/反合理化/验证门）、obra/superpowers（MIT；系统化调试/验证）、fishzjp/qa-skills（MIT；需求模型/九类歧义/证据分级）、saleem-daqa/qa-test-case-generation（MIT）、JohnWayneeee/casely-qa-skill（MIT）、gneder/qa-test-plan-skill（MIT）、petrkindlmann/qa-skills（MIT）、fugazi/test-automation-skills-agents（ISTQB 静态测试清单）、GitHub Spec Kit（MIT；clarify/analyze）、ISTQB CTFL / ISO/IEC/IEEE 29119-3、OWASP WSTG / ASVS 5.0 / Top 10 for LLM 2025、WCAG 2.2、Core Web Vitals、OpenTelemetry、NIST AI RMF、schemathesis 等工具社区经验。

## 步骤 → 技能映射

| 步骤 / 轨 | 技能 |
| --- | --- |
| analyze（需求/测试依据建模） | `技能/test-basis-analysis/SKILL.md`（需求模型/冲突/九类歧义/oracle/TP 追溯） |
| analyze / plan | `技能/test-analysis-and-plan/SKILL.md`（企业级计划/类型选择/执行编排/自动化分层）+ `技能/test-data-and-environment/SKILL.md`（环境/数据/账号/依赖） |
| generate（功能/专项） | `技能/testcase-design/SKILL.md`（+ AI 功能附加：`技能/ai-feature-testing/SKILL.md`） |
| review-cases / 计划评审（落地产物） | `技能/test-artifact-review/SKILL.md`（范围总览 + 计划/分析量规 + 选 B【自主分析】）+ `技能/testcase-review/SKILL.md`（用例细轴 A1–A6/S1–S6） |
| execute（功能/探索式/计划驱动） | `技能/test-execution-and-exploration/SKILL.md`（计划编排/回归/探索）+ `技能/test-data-and-environment/SKILL.md`（数据/环境/隔离）+ `技能/ai-feature-testing/SKILL.md`（AI 非确定性执行） |
| 接口轨 | `技能/test-interface/SKILL.md`（脚本优先 + 契约/复用；+ `规则/轨契约/接口.md`） |
| 发布前轨 | `技能/test-performance-security-compatibility/SKILL.md`（基础/标准/高风险级 + 工具矩阵/LLM 安全/韧性；+ `规则/轨契约/发布前.md`） |
| AI/LLM/RAG/Agent 功能 | `技能/ai-feature-testing/SKILL.md`（oracle/评测集/重复阈值/红队）+ `技能/test-performance-security-compatibility/SKILL.md`（安全） |
| report | `规则/模板/40-报告与评审/测试报告模板.md` + `规则/工作流.md` §4（即技能） |
| defect | `规则/缺陷/缺陷协作.md`（即技能） |
| 脚本档 | `规则/专项/脚本执行.md`（即技能） |
| onboard | `agents/onboard-agent.yaml`（核验清单即技能） |

**维护**：改技能 → 改本目录（确认后就地改）；技能只写方法，**禁**另立红线/门（SSOT 在 `AGENTS.md`/`规则/`）。

## 技能质量标准（Skill Anatomy）

> 依据 Agent Skills 规范与 addyosmani/agent-skills 的 skill anatomy，结合本包“规则/技能分离”约束。新增或大改技能按此验收。

**1. Frontmatter（必填）**

- `name`：小写字母/数字/连字符，与目录名一致；≤64 字符。
- `description`：≤1024 字符；写清“做什么 + 何时用 + 中文触发词”；不写步骤摘要。
- 可选 `license` / `compatibility` / `metadata` / `allowed-tools` 按宿主需要；不写宿主/模型私有字段。

**2. 正文结构（推荐顺序）**

| 节 | 作用 | 最低要求 |
| --- | --- | --- |
| 定位/适用 | 何时用、何时不用、与相邻技能边界 | 正/负触发各 ≥1 |
| 流程 | 可执行步骤，按顺序/分支 | 每步有动作与产出 |
| 判定 | 阈值、评分卡、分类表 | 可判定，不写“适当/尽量” |
| 反模式 / 反合理化 | 常见错法或偷懒借口 + 纠正 | **必有其一**：反模式表 **或** 反合理化 3～7 条（不强制两者齐） |
| 红旗 | 可观察的违规信号 | 推荐 ≥3；与判定/DoD 重叠时可并入判定节 |
| 验证/DoD | 证据与退出条件 | 每条可复核 |

**3. 写作纪律**

- **流程而非知识**：写“先做什么、怎么判定、产出什么”，不写百科。
- **具体**：能写字段/阈值/命令就不写“检查一下”；引用本包真实路径，不造文件。
- **单一出处**：红线/门/评分卡只引用，不复制；跨技能用名称引用。
- **渐进披露**：主文件目标 ≤500 行、≤4500 tokens；**超长才拆** `references/`（≤500 行且节清晰则不必硬拆）。
- **宿主/模型中立**：不写死某宿主工具名、模型版本或私有调用方式；写能力与目标。
- **只写现行**：不记录历史过程/旧方案。业务项目禁止改项目根 CHANGELOG；过程/接入进本包工作日志。母版仓包能力变化由母版维护会话记母版根 CHANGELOG。
- **中文优先**：方法与判定用中文；保留必要英文术语与代码/命令。

**4. 修改流程**

1. 改 `技能/<name>/SKILL.md`；同步本 README 映射与相关 workflow `notes`。
2. 跑 `规则/tools/Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`；改引用/映射后跑 `规则/tools/Test-DocHygiene.ps1`。
3. 更新包 `AGENTS.md` `template_version`；业务项目不写项目根 CHANGELOG；母版仓可见包能力变化才记母版根 CHANGELOG；不单独给技能设版本号。
4. 新增技能必须在本表挂到具体步骤；跨阶段技能挂到所有适用阶段。

**5. 验收清单**

- [ ] name 与目录一致；description 含 what/when/中文触发。
- [ ] 有适用/不适用、流程、判定、反模式或反合理化、验证（红旗可并入判定）。
- [ ] 无红线/门复制；引用路径存在；无宿主/模型硬编码。
- [ ] ≤500 行；超长才拆 references；映射已更新。
- [ ] 自检通过；版本/CHANGELOG 已同步。
