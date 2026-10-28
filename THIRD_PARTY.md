# 第三方方法与来源

> 本仓的技能与规则是**参考公开实践后改写适配的中文版本**，不是对上游仓库的原样搬运。
> 引用仅用于方法对齐；具体许可、版本与条款以各项目官方仓库/标准原文为准。
> 新增外部方法时：在本文件登记「来源 / 版本或 commit / 许可 / 用在哪 / 是否改写」，并在技能 README 的整合来源中同步。

## 1. 工程与 Agent 工作流

| 来源 | 许可 | 本仓用法 |
| --- | --- | --- |
| [github/spec-kit](https://github.com/github/spec-kit) | MIT | specify/plan/tasks/analyze/converge 的思路；`development-plan`、`product-doc-analysis`、`test-basis-analysis` |
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | MIT | 按规模裁剪、端到端交付；L0～L3 / T0～T3 / P0～P3 分级 |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | MIT | skill anatomy、反合理化、Definition of Done；技能质量标准 |
| [obra/superpowers](https://github.com/obra/superpowers) | MIT | 系统化调试、计划执行、评审/验证；`debugging-and-error-recovery`、`development-plan` |
| [anthropics/skills](https://github.com/anthropics/skills) | Apache-2.0（部分 source-available） | frontend-design、doc-suite 等方法参考；能力注册表可选 |
| [wshobson/agents](https://github.com/wshobson/agents) | MIT | 多宿主插件/技能组织方式参考 |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | MIT | Web Interface Guidelines / UI 审查 |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | MIT | 设计系统/风格/配色参考 |
| [superdesigndev/superdesign-skill](https://github.com/superdesigndev/superdesign-skill) | 见上游 | 设计生成参考（可选能力） |

## 2. 工程规范与安全

| 来源 | 许可/性质 | 本仓用法 |
| --- | --- | --- |
| Google Engineering Practices | 公开文档 | 小 CL、评审、CI 节奏 |
| Google AIP / Microsoft REST API Guidelines | 公开文档 | API 设计原则 |
| OWASP ASVS 5.0 / WSTG / Top 10 for LLM 2025 | 官方许可 | 安全设计、测试、威胁建模 |
| SLSA v1.2 / OpenSSF Scorecard | 公开规范 | 供应链与构建可信 |
| 12-Factor / DORA / Google SRE | 公开方法 | 工程基线、发布、SLO、复盘 |
| C4 / arc42 / ADR | 公开方法 | 架构表达与决策记录 |
| OpenTelemetry（含 GenAI 语义约定） | Apache-2.0 | 可观测性与 AI 观测 |
| Keep a Changelog / SemVer | 公开规范 | 版本记录 |

## 3. 产品与测试

| 来源 | 许可/性质 | 本仓用法 |
| --- | --- | --- |
| SVPG / Lean Startup / Working Backwards / Continuous Discovery | 公开方法 | 机会评估、发现、PRD/Go-Hold-Kill |
| The Mom Test / JTBD / BABOK | 公开方法 | 客户访谈、需求分析 |
| RICE / WSJF / Kano / MoSCoW | 公开方法 | 优先级 |
| ISO/IEC/IEEE 29119-3 / 29148 | 标准（不复制原文） | 测试计划要素、需求追溯 |
| ISTQB CTFL / 风险驱动测试 | 公开知识体系 | 测试分级、风险、估算 |
| SBTM（Session-Based Test Management） | 公开方法 | 探索式测试 |
| Playwright best practices | Apache-2.0 | 脚本档、trace、flake 治理 |
| WCAG 2.2 / Core Web Vitals | W3C / Google | 可访问性、性能 |
| NIST AI RMF / ISO/IEC 42001 / EU AI Act | 公开框架/法规（按适用） | AI 治理与风险 |

## 4. 维护约定

- 上游方法只作参考；**不逐字复制**受版权保护的标准正文。
- 每次新增/替换来源：更新本文件 + 对应 `技能/README.md` 的「整合来源」。
- 不把外部仓库整包塞进三包；需要安装的走 `能力/00-能力注册表.md` 的「装配能力」。
- 许可不明或条款冲突的来源，不进入母版；改为链接引用。
