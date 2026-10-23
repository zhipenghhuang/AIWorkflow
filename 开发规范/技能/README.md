# 包内专业技能（随包生效 · 无需安装/挂载）

> **定位**：每一步的**专业方法与手艺**（playbook），随本包分发。命中步骤 → 步骤注记直接加载对应 `技能/<name>/SKILL.md` → 按技能标准执行。  
> **目录结构**：`技能/<name>/SKILL.md`（`name` 取 frontmatter）；随包复制、**无需安装**；AGENTS/步注直接按路径读取。宿主支持本地 skills 根时，可把 `技能/` 指向本地 skills 目录（可选，不是前置条件）。  
> **格式**：每份技能含 `name` / `description` frontmatter（Agent Skills 兼容），正文为方法/步骤/自检/反模式；描述中的触发条件用于 AI 选择技能。  
> **来源**：以下技能是参考 GitHub/企业实践后**改写整合**的中文随包技能，不是把 GitHub 仓库原样搬入；外部 GitHub skill 仍走 `能力/00-能力注册表.md`（可选）。  
> **与「能力」的区别**：技能=怎么做（方法/清单/手感，随包生效、必用）；`能力/00-能力注册表.md` 的能力=用哪些外部工具（选装；本机可用即自动使用、不可用走降级）。  
> **与「规则」的区别**：技能给方法；红线/口径/门以 `AGENTS.md` 与 `规则/` 为准（冲突时规则优先）。  
> **整合来源**（方法参考，已改写适配为中文随包版，非逐字复制）：github/spec-kit（MIT；spec/plan/tasks/converge、clarify/analyze 歧义与一致性）、addyosmani/agent-skills（MIT；interview-me、planning-and-task-breakdown、definition-of-done、code-review）、obra/superpowers（MIT；writing-plans/executing-plans/TDD）、bmad-code-org/BMAD-METHOD（MIT；按规模裁剪/durable context）、fishzjp/qa-skills（MIT；requirement-analysis 需求模型）、wshobson/agents（MIT）、alibaba/open-code-review（Apache-2.0）、Google Engineering Practices（code review / small CLs）、Google AIP、Microsoft REST API Guidelines、OWASP ASVS 5.0、12-Factor App、DORA 五项指标、C4/arc42/ADR、Diátaxis、Keep a Changelog/SemVer/Conventional Commits、WCAG 2.2、Vercel Web Interface Guidelines、anthropics/skills `frontend-design`、nextlevelbuilder/ui-ux-pro-max-skill、Ant Design/Carbon/Polaris/Primer/Atlassian/GOV.UK/Material 3/Fluent 2 等企业设计系统（许可与版本以官方仓库为准）。  

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
| 新文档 / 新变化 / 确认项 / 收件箱 / 变更吸收 | `技能/change-intake/SKILL.md` + `技能/product-doc-analysis/SKILL.md`（PRD/原型/文档） |
| change：clarify / requirements | `技能/requirements-and-spec/SKILL.md` |
| change：analyze_input / intake.parse（PRD/迭代方案/原型/文档解析） | `技能/product-doc-analysis/SKILL.md`（主）+ `技能/requirements-and-spec/SKILL.md`（澄清） |
| change：design / S2 技术方案 | `技能/solution-design/SKILL.md`（主技能）+ `技能/engineering-quality/SKILL.md`（质量条）+ `技能/technology-selection/SKILL.md` / `技能/database-design/SKILL.md` / `技能/api-design/SKILL.md` / `技能/frontend-design/SKILL.md`（按需）/ `技能/threat-modeling/SKILL.md` / `技能/performance-and-capacity/SKILL.md`（按变更面加载） |
| change / iterate：plan | `技能/task-breakdown/SKILL.md` |
| change / iterate：implement / verify / S4 编码自测 | `技能/implementation-and-selftest/SKILL.md` + `技能/engineering-quality/SKILL.md` + `技能/frontend-implementation/SKILL.md` / `技能/backend-implementation/SKILL.md`（按端加载） |
| change / iterate：review | `技能/code-review/SKILL.md` + `技能/engineering-quality/SKILL.md` |
| change / iterate：deliver | `技能/qa-handoff-and-release/SKILL.md` |
| release：acceptance / readiness / deploy / verify / rollback / postrelease | `技能/acceptance-and-launch/SKILL.md` |
| retro：gather / analyze / actions | `技能/retrospective-and-improvement/SKILL.md` |
| defect-fix 全流程 | `规则/缺陷修复协作.md`（本轨专规即技能） |
| iterate 节奏/核验 | `规则/迭代交付.md`（规则，不替代拆单技能） |
| onboard 核验/装配/文档整理 | `agents/onboard-agent.yaml`（核验清单即技能） |

## 开发计划阶段 → 技能（每阶段至少一个）

| 阶段 | 技能 | 何时加载 |
| --- | --- | --- |
| S0 输入检查 | `技能/development-plan/SKILL.md` + `技能/product-doc-analysis/SKILL.md` + `技能/requirements-and-spec/SKILL.md` §2 + `技能/change-intake/SKILL.md` | 核对 PRD/原型/AC/缺口/收件箱 |
| S1 需求分析 | `技能/requirements-and-spec/SKILL.md` + `技能/product-doc-analysis/SKILL.md` | 功能点/AC/状态/权限/异常/影响面 |
| S2 技术方案 | `技能/solution-design/SKILL.md` + `技能/engineering-quality/SKILL.md` + `技能/technology-selection` / `技能/database-design` / `技能/api-design` / `技能/frontend-design` / `技能/threat-modeling` / `技能/performance-and-capacity`（各目录下 SKILL.md） | 架构/选型/DB/API/前端/质量/安全/性能按变更面 |
| S3 任务与排期 | `技能/task-breakdown/SKILL.md` | 任务清单/依赖/估算/DoR/DoD |
| S4 编码自测 | `技能/implementation-and-selftest/SKILL.md` + `技能/engineering-quality/SKILL.md` + `技能/frontend-implementation/SKILL.md` / `技能/backend-implementation/SKILL.md` | 前端/后端实现、质量条、单测/自测/文档 |
| S5 评审/CI | `技能/code-review/SKILL.md` + `技能/engineering-quality/SKILL.md` | 代码评审/质量 rubric/安全/CI |
| S6 提测 | `技能/qa-handoff-and-release/SKILL.md` | 提测单/回归指引/QA 接收 |
| S7 测试/缺陷 | `技能/qa-handoff-and-release/SKILL.md` + `规则/缺陷修复协作.md` | 缺陷修复/回归/回写 |
| S8 发布 | `技能/acceptance-and-launch/SKILL.md` | 就绪检查/部署/冒烟/回滚/观察 |
| S9 收尾/复盘 | `技能/retrospective-and-improvement/SKILL.md` | 总结/复盘/归档 |

**维护**：改技能 → 改本目录（母版改，随包分发）；技能只写方法，**禁**另立红线/门（SSOT 在 `AGENTS.md`/`规则/`）。  
**新增技能**：加 frontmatter（`name` + `description`，description 写清“何时用”），在本表挂到具体步骤，并在对应 workflow 的 `notes` 写「技能：…（先读再执行）」。跨阶段支撑技能（如 `engineering-quality`）必须同时挂到 S2/S4/S5 与 design/implement/review 步。
