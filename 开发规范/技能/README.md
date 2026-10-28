# 包内专业技能（随包生效 · 无需安装/挂载）

> **定位**：每一步的**专业方法与手艺**（playbook），随本包分发。命中步骤 → 步骤注记直接加载对应 `技能/<name>/SKILL.md` → 按技能标准执行。  
> **目录结构**：`技能/<name>/SKILL.md`（`name` 取 frontmatter）；随包复制、**无需安装**；AGENTS/步注直接按路径读取。宿主支持本地 skills 根时，可把 `技能/` 指向本地 skills 目录（可选，不是前置条件）。  
> **更新**：落地副本可就地改本目录（单包/开源用户无需母版仓）。口令「体检能力」做检查与优化建议（确认后应用）；「通用优化技能/母版技能更新」按通用最优改、不绑具体项目。外部 GitHub skill 仍走 `能力/` +「装配能力」。  
> **格式**：每份技能含 `name` / `description` frontmatter（Agent Skills 兼容）；description 写“做什么 + 何时用 + 中文触发词”；正文为方法/步骤/判定/反模式/验证，单文件目标 ≤500 行（超长拆 `references/`）。质量标准见本文末节。
> **来源**：以下技能是参考 GitHub/企业实践后**改写整合**的中文随包技能，不是把 GitHub 仓库原样搬入；外部 GitHub skill 仍走 `能力/00-能力注册表.md`（可选）。
> **与「能力」的区别**：技能=怎么做（方法/清单/手感，随包生效、必用）；`能力/00-能力注册表.md` 的能力=用哪些外部工具（选装；本机可用即自动使用、不可用走降级）。  
> **与「规则」的区别**：技能给方法；红线/口径/门以 `AGENTS.md` 与 `规则/` 为准（冲突时规则优先）。  
> **整合来源**（方法参考，已改写适配为中文随包版，非逐字复制）：Agent Skills 规范（agentskills.io；frontmatter/渐进披露/≤500 行）、anthropics/skills、addyosmani/agent-skills（MIT；skill anatomy/反合理化/验证门）、obra/superpowers（MIT；系统化调试/计划/评审）、github/spec-kit（MIT）、bmad-code-org/BMAD-METHOD（MIT）、wshobson/agents（MIT）、alibaba/open-code-review（Apache-2.0）、Google Engineering Practices、Google AIP、Microsoft REST API Guidelines、OWASP ASVS 5.0、OWASP WSTG、OWASP Top 10 for LLM 2025、SLSA v1.2、OpenSSF Scorecard、12-Factor、DORA、C4/arc42/ADR、OpenTelemetry（含 GenAI 语义约定）、Diátaxis、Keep a Changelog/SemVer、WCAG 2.2、Core Web Vitals、NIST AI RMF、ISO/IEC 42001（许可以官方为准）。  

## 别名 → 实际路径（旧引用兼容）

| 别名 | 实际路径 |
| --- | --- |
| 00 | `技能/development-plan/SKILL.md` |
| 01 | `技能/requirements-and-spec/SKILL.md` |
| 02 | `技能/solution-design/SKILL.md` |
| 02A | `技能/technology-selection/SKILL.md` |
| 02B | `技能/database-design/SKILL.md` |
| 02C | `技能/api-design/SKILL.md` |
| 02D | `技能/frontend-design/SKILL.md` |
| 02E | `技能/threat-modeling/SKILL.md` |
| 02F | `技能/performance-and-capacity/SKILL.md` |
| quality | `技能/engineering-quality/SKILL.md` |
| 03 | `技能/implementation-and-selftest/SKILL.md` |
| 03A | `技能/frontend-implementation/SKILL.md` |
| 03B | `技能/backend-implementation/SKILL.md` |
| 03C | `技能/design-doc-review/SKILL.md` |
| 04 | `技能/code-review/SKILL.md` |
| 05 | `技能/qa-handoff-and-release/SKILL.md` |
| 06 | `技能/task-breakdown/SKILL.md` |
| 07 | `技能/acceptance-and-launch/SKILL.md` |
| 08 | `技能/retrospective-and-improvement/SKILL.md` |

> 新引用一律用实际路径；编号别名只用于兼容旧文本。

## 步骤 → 技能映射

| 步骤 | 技能 |
| --- | --- |
| 开发计划 / 进度 / 阶段检查 | `技能/development-plan/SKILL.md` |
| change：review-docs（落地文档评审） | `技能/design-doc-review/SKILL.md`（先选 A/B）+ `engineering-quality` §5 |
| 新文档 / 新变化 / 确认项 / 收件箱 / 变更吸收 | `技能/change-intake/SKILL.md` + `技能/product-doc-analysis/SKILL.md`（PRD/原型/文档） |
| change：clarify / requirements | `技能/requirements-and-spec/SKILL.md` |
| change：analyze_input / intake.parse（PRD/迭代方案/原型/文档解析） | `技能/product-doc-analysis/SKILL.md`（主）+ `技能/requirements-and-spec/SKILL.md`（澄清） |
| change：design / S2 技术方案 | `技能/solution-design/SKILL.md`（主技能）+ `技能/engineering-quality/SKILL.md`（质量条）+ `技能/technology-selection/SKILL.md` / `技能/database-design/SKILL.md` / `技能/api-design/SKILL.md` / `技能/frontend-design/SKILL.md`（按需）/ `技能/threat-modeling/SKILL.md` / `技能/performance-and-capacity/SKILL.md` / `技能/observability-and-instrumentation/SKILL.md` / `技能/ai-application-engineering/SKILL.md`（按变更面加载） |
| change / iterate：plan | `技能/task-breakdown/SKILL.md` |
| change / iterate：implement / verify / S4 编码自测 | `技能/implementation-and-selftest/SKILL.md` + `技能/engineering-quality/SKILL.md` + `技能/frontend-implementation/SKILL.md` / `技能/backend-implementation/SKILL.md`（按端加载） |
| 构建/测试/运行失败、线上异常、偶发问题 | `技能/debugging-and-error-recovery/SKILL.md`（先恢复再根因） |
| 设计/实施/发布涉及生产可诊断性、SLO、日志/指标/追踪/告警 | `技能/observability-and-instrumentation/SKILL.md` |
| 变更含 LLM/RAG/Agent/提示词/模型/工具调用 | `技能/ai-application-engineering/SKILL.md` + `技能/threat-modeling/SKILL.md`（AI 安全） |
| change / iterate：review | `技能/code-review/SKILL.md` + `技能/engineering-quality/SKILL.md` |
| change / iterate：deliver | `技能/qa-handoff-and-release/SKILL.md` |
| release：acceptance / readiness / deploy / verify / rollback / postrelease | `技能/acceptance-and-launch/SKILL.md` + `技能/observability-and-instrumentation/SKILL.md` |
| retro：gather / analyze / actions | `技能/retrospective-and-improvement/SKILL.md` |
| defect-fix 全流程 | `规则/缺陷/缺陷修复协作.md`（本轨专规即技能） |
| iterate 节奏/核验 | `规则/专项/迭代交付.md`（规则，不替代拆单技能） |
| onboard 核验/装配/文档整理 | `agents/onboard-agent.yaml`（核验清单即技能） |

## 开发计划阶段 → 技能（每阶段至少一个）

| 阶段 | 技能 | 何时加载 |
| --- | --- | --- |
| S0 输入检查 | `技能/development-plan/SKILL.md` + `技能/product-doc-analysis/SKILL.md` + `技能/requirements-and-spec/SKILL.md` §2 + `技能/change-intake/SKILL.md` | 核对 PRD/原型/AC/缺口/收件箱 |
| S1 需求分析 | `技能/requirements-and-spec/SKILL.md` + `技能/product-doc-analysis/SKILL.md` | 功能点/AC/状态/权限/异常/影响面 |
| S2 技术方案 | `技能/solution-design/SKILL.md` + `技能/engineering-quality/SKILL.md` + `技能/technology-selection` / `技能/database-design` / `技能/api-design` / `技能/frontend-design` / `技能/threat-modeling` / `技能/performance-and-capacity` / `技能/observability-and-instrumentation` / `技能/ai-application-engineering`（各目录下 SKILL.md；按变更面） | 架构/选型/DB/API/前端/质量/安全/性能/可观测/AI 按变更面 |
| S3 任务与排期 | `技能/task-breakdown/SKILL.md` | 任务清单/依赖/估算/DoR/DoD |
| S4 编码自测 | `技能/implementation-and-selftest/SKILL.md` + `技能/engineering-quality/SKILL.md` + `技能/frontend-implementation/SKILL.md` / `技能/backend-implementation/SKILL.md` + `技能/debugging-and-error-recovery/SKILL.md`（失败时）+ `技能/ai-application-engineering/SKILL.md`（AI 变更） | 前端/后端实现、质量条、调试、单测/自测/文档 |
| S5 评审/CI | `技能/code-review/SKILL.md` + `技能/engineering-quality/SKILL.md` | 代码评审/质量 rubric/安全/供应链/AI 生成代码 |
| S6 提测 | `技能/qa-handoff-and-release/SKILL.md` | 提测单/回归指引/QA 接收 |
| S7 测试/缺陷 | `技能/qa-handoff-and-release/SKILL.md` + `规则/缺陷/缺陷修复协作.md` | 缺陷修复/回归/回写 |
| S8 发布 | `技能/acceptance-and-launch/SKILL.md` + `技能/observability-and-instrumentation/SKILL.md` | 就绪检查/部署/冒烟/回滚/观察/SLO |
| S9 收尾/复盘 | `技能/retrospective-and-improvement/SKILL.md` | 总结/复盘/归档 |

**维护**：改技能 → 改本目录（母版改，随包分发）；技能只写方法，**禁**另立红线/门（SSOT 在 `AGENTS.md`/`规则/`）。  
**新增技能**：加 frontmatter（`name` + `description`，description 写清“何时用”），在本表挂到具体步骤，并在对应 workflow 的 `notes` 写「技能：…（先读再执行）」。跨阶段支撑技能（如 `engineering-quality`）必须同时挂到 S2/S4/S5 与 design/implement/review 步。

## 技能质量标准（Skill Anatomy）

> 依据 Agent Skills 规范与 addyosmani/agent-skills 的 skill anatomy，结合本包“规则/技能分离”约束。新增或大改技能按此验收。

**1. Frontmatter（必填）**

- `name`：小写字母/数字/连字符，与目录名一致；≤64 字符。
- `description`：≤1024 字符；写清“做什么 + 何时用 + 中文触发词”；不写步骤摘要（避免模型只读摘要不读正文）。
- 可选 `license` / `compatibility` / `metadata` / `allowed-tools` 按宿主需要；不写宿主/模型私有字段。

**2. 正文结构（推荐顺序）**

| 节 | 作用 | 最低要求 |
| --- | --- | --- |
| 定位/适用 | 何时用、何时不用、与相邻技能边界 | 正/负触发各 ≥1 |
| 流程 | 可执行步骤，按顺序/分支 | 每步有动作与产出 |
| 判定 | 阈值、评分卡、分类表 | 可判定，不写“适当/尽量” |
| 反合理化 | 常见偷懒借口 + 事实反驳 | 3～7 条，针对本技能 |
| 红旗 | 可观察的违规信号 | ≥3 条 |
| 验证/DoD | 证据与退出条件 | 每条可复核 |

**3. 写作纪律**

- **流程而非知识**：写“先做什么、怎么判定、产出什么”，不写百科。
- **具体**：能写命令/字段/阈值就不写“检查一下”；引用本包真实路径，不造文件。
- **单一出处**：红线/门/评分卡只引用，不复制；跨技能用名称引用。
- **渐进披露**：主文件目标 ≤500 行、≤4500 tokens；超长拆 `references/`，引用一层深。
- **宿主/模型中立**：不写死某宿主工具名、模型版本或私有调用方式；写能力与目标。
- **只写现行**：不记录历史过程/旧方案；版本变化进 CHANGELOG。
- **中文优先**：方法与判定用中文；保留必要英文术语与代码/命令。

**4. 修改流程**

1. 改 `技能/<name>/SKILL.md`；同步本 README 映射与相关 workflow `notes`。
2. 跑 `规则/tools/Test-Template.ps1`；改引用/映射后跑 `规则/tools/Test-DocHygiene.ps1`。
3. 更新包 `AGENTS.md` `template_version` + 根 `CHANGELOG.md`；不单独给技能设版本号。
4. 新增技能必须在本表挂到具体步骤；跨阶段技能挂到所有适用阶段。

**5. 验收清单**

- [ ] name 与目录一致；description 含 what/when/中文触发。
- [ ] 有适用/不适用、流程、判定、反合理化、红旗、验证。
- [ ] 无红线/门复制；引用路径存在；无宿主/模型硬编码。
- [ ] ≤500 行；超长已拆 references；映射已更新。
- [ ] 自检通过；版本/CHANGELOG 已同步。
