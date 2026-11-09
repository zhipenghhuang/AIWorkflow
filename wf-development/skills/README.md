# 包内专业技能（随包生效 · 无需安装/挂载）

> **定位**：每一步的**专业方法与手艺**，随本包分发。命中步骤 → 步骤注记直接加载对应 `skills/<name>/SKILL.md` → 按技能标准执行。  
> **目录结构**：`skills/<name>/SKILL.md`（`name` 取 frontmatter）；随包复制、**无需安装**；AGENTS/步注直接按路径读取。宿主支持本地 skills 根时，可把 `skills/` 指向本地 skills 目录（可选，不是前置条件）。  
> **更新**：本包 `skills/` 可就地改。口令「体检能力」做检查与优化建议（确认后应用）；「通用优化技能」按通用最优。外部工具选型写入实例 `{workroot}/capabilities/`（「装配能力」）。  
> **格式**：每份技能含 `name` / `description` frontmatter（Agent Skills 兼容）；description 写“做什么 + 何时用 + 中文触发词”；正文为方法/步骤/判定/反模式/验证，单文件目标 ≤500 行（超长拆 `references/`）。质量标准见本文末节。
> **来源**：以下技能是参考 GitHub/企业实践后**改写整合**的中文随包技能，不是把 GitHub 仓库原样搬入；外部 GitHub skill 仍走 `capabilities/00-contract.md`（可选）。
> **与「能力」的区别**：技能=怎么做（随包必用）；能力选型真源=`{workroot}/capabilities/00-能力清单.md`；包内契约/参考目录非真源。  
> **与「规则」的区别**：技能给方法；红线/口径/门以 `AGENTS.md` 与 `rules/` 为准（冲突时规则优先）。  
> **整合来源**（方法参考，已改写适配为中文随包版，非逐字复制）：Agent Skills 规范（agentskills.io；frontmatter/渐进披露/≤500 行）、anthropics/skills、addyosmani/agent-skills（MIT；skill anatomy/反合理化/验证门）、obra/superpowers（MIT；系统化调试/计划/评审）、github/spec-kit（MIT）、bmad-code-org/BMAD-METHOD（MIT）、wshobson/agents（MIT）、alibaba/open-code-review（Apache-2.0）、Google Engineering Practices、Google AIP、Microsoft REST API Guidelines、OWASP ASVS 5.0、OWASP WSTG、OWASP Top 10 for LLM 2025、SLSA v1.2、OpenSSF Scorecard、12-Factor、DORA、C4/arc42/ADR、OpenTelemetry（含 GenAI 语义约定）、Diátaxis、Keep a Changelog/SemVer、WCAG 2.2、Core Web Vitals、NIST AI RMF、ISO/IEC 42001（许可以官方为准）。  

## 别名 → 实际路径（旧引用兼容）

| 别名 | 实际路径 |
| --- | --- |
| 00 | `skills/development-plan/SKILL.md` |
| 01 | `skills/requirements-and-spec/SKILL.md` |
| 02 | `skills/solution-design/SKILL.md` |
| 02A | `skills/technology-selection/SKILL.md` |
| 02B | `skills/database-design/SKILL.md` |
| 02C | `skills/api-design/SKILL.md` |
| 02D | `skills/frontend-design/SKILL.md` |
| 02E | `skills/threat-modeling/SKILL.md` |
| 02F | `skills/performance-and-capacity/SKILL.md` |
| quality | `skills/engineering-quality/SKILL.md` |
| 03 | `skills/implementation-and-selftest/SKILL.md` |
| 03A | `skills/frontend-implementation/SKILL.md` |
| 03B | `skills/backend-implementation/SKILL.md` |
| 03C | `skills/design-doc-review/SKILL.md` |
| 04 | `skills/code-review/SKILL.md` |
| 05 | `skills/qa-handoff-and-release/SKILL.md` |
| 06 | `skills/task-breakdown/SKILL.md` |
| 07 | `skills/acceptance-and-launch/SKILL.md` |
| 08 | `skills/retrospective-and-improvement/SKILL.md` |

> 新引用一律用实际路径；编号别名只用于兼容旧文本。

## 步骤 → 技能映射

| 步骤 | 技能 |
| --- | --- |
| 开发计划 / 进度 / 阶段检查 | `skills/development-plan/SKILL.md` |
| change：review-docs（落地文档评审） | `skills/design-doc-review/SKILL.md`（先选 A/B）+ `engineering-quality` §5 |
| 新文档 / 新变化 / 确认项 / 收件箱 / 变更吸收 | `skills/change-intake/SKILL.md` + `skills/product-doc-analysis/SKILL.md`（PRD/原型/文档） |
| change：clarify / requirements | `skills/requirements-and-spec/SKILL.md` |
| change：analyze_input / intake.parse（PRD/迭代方案/原型/文档解析） | `skills/product-doc-analysis/SKILL.md`（主）+ `skills/requirements-and-spec/SKILL.md`（澄清） |
| change：requirements / design（权限/状态/数据基数/多表面） | `skills/cross-layer-consistency/SKILL.md`（前置）+ `skills/requirements-and-spec/SKILL.md` / `skills/solution-design/SKILL.md` |
| change：design / S2 技术方案 | `skills/solution-design/SKILL.md`（主技能）+ `skills/engineering-quality/SKILL.md`（质量条）+ `skills/technology-selection/SKILL.md` / `skills/database-design/SKILL.md` / `skills/api-design/SKILL.md` / `skills/frontend-design/SKILL.md`（按需）/ `skills/threat-modeling/SKILL.md` / `skills/performance-and-capacity/SKILL.md` / `skills/observability-and-instrumentation/SKILL.md` / `skills/ai-application-engineering/SKILL.md`（按变更面加载） |
| change / iterate：plan | `skills/task-breakdown/SKILL.md` + `skills/cross-layer-consistency/SKILL.md`（矩阵入任务卡） |
| change / iterate：implement / verify / S4 编码自测 | `skills/implementation-and-selftest/SKILL.md`（**§0.5 实施预检强制**）+ `skills/engineering-quality/SKILL.md` + 按端前后端 + `cross-layer-consistency`（命中时）+ 预检命中面再读 threat/perf/observability 当前节 |
| 构建/测试/运行失败、线上异常、偶发问题 | `skills/debugging-and-error-recovery/SKILL.md`（先恢复再根因） |
| 设计/实施/发布涉及生产可诊断性、SLO、日志/指标/追踪/告警 | `skills/observability-and-instrumentation/SKILL.md` |
| 变更含 LLM/RAG/Agent/提示词/模型/工具调用 | `skills/ai-application-engineering/SKILL.md` + `skills/threat-modeling/SKILL.md`（AI 安全） |
| change / iterate：review | `skills/code-review/SKILL.md` + `skills/engineering-quality/SKILL.md` |
| change / iterate：deliver | `skills/qa-handoff-and-release/SKILL.md` |
| solo.frame（轻量档产品定义） | `skills/product-shaping/SKILL.md` |
| solo.plan（一页方案卡） | `skills/product-shaping/SKILL.md` + `skills/solution-design/SKILL.md` + `skills/engineering-quality/SKILL.md` + `skills/task-breakdown/SKILL.md` |
| solo.build（轻量实施） | `skills/implementation-and-selftest/SKILL.md`（§0.5 预检；轻量不降硬补）+ `skills/engineering-quality/SKILL.md` |
| solo.test（轻量测试） | `skills/test-design-and-execution/SKILL.md` |
| release：acceptance / readiness / deploy / verify / rollback / postrelease | `skills/acceptance-and-launch/SKILL.md` + `skills/observability-and-instrumentation/SKILL.md` |
| retro：gather / analyze / actions | `skills/retrospective-and-improvement/SKILL.md` |
| defect-fix 全流程 | `rules/defects/fix-collaboration.md`（本轨专规即技能）+ `skills/cross-layer-consistency/SKILL.md`（根因分层/同类路径/回归） |
| iterate 节奏/核验 | `rules/special/iteration-delivery.md`（规则，不替代拆单技能） |
| onboard 核验/装配/文档整理 | `agents/onboard-agent.yaml`（核验清单即技能） |

## 自包含完整链（solo）

> 用于无正式迭代/正式协作：产品分析 → 方案 → 完整开发 → 测试；不是只开发，也不依赖产品/测试包。大改动/高风险不换链，按 `rules/core/lightweight.md` §2 提高产品分析与测试证据；正式协作/迭代 → 完整链。

| 步骤 | 技能 | 说明 |
| --- | --- | --- |
| frame | `product-shaping` | 方向不清/新产品时走；小改跳过 |
| plan | `product-shaping` + `product-doc-analysis`（输入含文档/原型）+ `solution-design` + `engineering-quality` + `task-breakdown` | 产品分析/方案/任务/验收/测试策略 |
| build | `implementation-and-selftest`（§0.5 预检）+ `engineering-quality` | 预检→硬补→完整开发；失败时加 `debugging-and-error-recovery` |
| test | `test-design-and-execution` | 设计→执行→报告；按风险完整；大改动/高风险全节 + 独立 verifier；P0 未过 = FAIL |

## 开发计划阶段 → 技能（每阶段至少一个）

| 阶段 | 技能 | 何时加载 |
| --- | --- | --- |
| S0 输入检查 | `skills/development-plan/SKILL.md` + `skills/product-doc-analysis/SKILL.md` + `skills/requirements-and-spec/SKILL.md` §2 + `skills/change-intake/SKILL.md` | 核对 PRD/原型/AC/缺口/收件箱 |
| S1 需求分析 | `skills/requirements-and-spec/SKILL.md` + `skills/product-doc-analysis/SKILL.md` + `skills/cross-layer-consistency/SKILL.md`（命中时） | 功能点/AC/状态/权限/异常/影响面/四维覆盖矩阵 |
| S2 技术方案 | `skills/solution-design/SKILL.md` + `skills/engineering-quality/SKILL.md` + `skills/technology-selection` / `skills/database-design` / `skills/api-design` / `skills/frontend-design` / `skills/threat-modeling` / `skills/performance-and-capacity` / `skills/observability-and-instrumentation` / `skills/ai-application-engineering`（各目录下 SKILL.md；按变更面）+ `skills/cross-layer-consistency/SKILL.md`（单一谓词/权限/状态/数据基数） | 架构/选型/DB/API/前端/质量/安全/性能/可观测/AI 按变更面 |
| S3 任务与排期 | `skills/task-breakdown/SKILL.md` + `skills/cross-layer-consistency/SKILL.md`（矩阵入任务卡） | 任务清单/依赖/估算/DoR/DoD/覆盖矩阵 |
| S4 编码自测 | `implementation-and-selftest`（§0.5 预检）+ `engineering-quality` + 按端前后端 + `debugging-and-error-recovery`（失败时）+ `ai-application-engineering`（AI 变更）+ `cross-layer-consistency`（命中时）+ 预检命中面子技能当前节 | 预检→硬补→实现、质量条、调试、单测/自测/文档 |
| S5 评审/CI | `skills/code-review/SKILL.md` + `skills/engineering-quality/SKILL.md` + `skills/cross-layer-consistency/SKILL.md`（跨层一致性） | 代码评审/质量 rubric/安全/供应链/AI 生成代码 |
| S6 提测 | `skills/qa-handoff-and-release/SKILL.md` | 提测单/回归指引/QA 接收 |
| S7 测试/缺陷 | `skills/qa-handoff-and-release/SKILL.md` + `rules/defects/fix-collaboration.md` | 缺陷修复/回归/回写 |
| S8 发布 | `skills/acceptance-and-launch/SKILL.md` + `skills/observability-and-instrumentation/SKILL.md` | 就绪检查/部署/冒烟/回滚/观察/SLO |
| S9 收尾/复盘 | `skills/retrospective-and-improvement/SKILL.md` | 总结/复盘/归档 |

**维护**：改技能 → 改本目录（用户确认后就地改）；技能只写方法，**禁**另立红线/门（SSOT 在 `AGENTS.md`/`rules/`）。  
**新增技能**：加 frontmatter（`name` + `description`，description 写清“何时用”），在本表挂到具体步骤，并在对应 workflow 的 `notes` 写「技能：…（先读再执行）」。跨阶段支撑技能（如 `engineering-quality`）必须同时挂到 S2/S4/S5 与 20-design/implement/review 步。

## 技能质量标准（Skill Anatomy）

> 依据 Agent Skills 规范与 addyosmani/agent-skills 的 skill anatomy，结合本包“rules/技能分离”约束。新增或大改技能按此验收。

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
| 反模式 / 反合理化 | 常见错法或偷懒借口 + 纠正 | **必有其一**（可用「反模式」「反合理化」「合理化与反驳」「常见合理化」）；`check_skills.py` 硬闸 |
| 红旗 | 可观察的违规信号 | ≥3 条 |
| verify/DoD | 证据与退出条件 | 每条可复核 |

**3. 写作纪律**

- **流程而非知识**：写“先做什么、怎么判定、产出什么”，不写百科。
- **具体**：能写命令/字段/阈值就不写“检查一下”；引用本包真实路径，不造文件。
- **单一出处**：红线/门/评分卡只引用，不复制；跨技能用名称引用。
- **渐进披露**：主文件目标 ≤500 行、≤4500 tokens；**超长才拆** `references/`。
- **宿主/模型中立**：不写死某宿主工具名、模型版本或私有调用方式；写能力与目标。
- **只写现行**：不记录历史过程/旧方案。母版仓维护：用户可见包能力进母版根 CHANGELOG（产品语言）；过程/接入进工作日志。业务项目：项目发版史仅开发发版时写项目根 CHANGELOG。
- **中文优先**：方法与判定用中文；保留必要英文术语与代码/命令。

**4. 修改流程**

1. 改 `skills/<name>/SKILL.md`；同步本 README 映射与相关 workflow `notes`。
2. 跑 `rules/tools/Test-Template.ps1`；改引用/映射后跑 `rules/tools/Test-DocHygiene.ps1`；必跑 `rules/tools/check_skills.py <包根> --strict`。
3. 更新包 `AGENTS.md` `template_version`；仅母版仓且有用户可见包能力变化时才更新母版根 `CHANGELOG.md`；业务项目不因改技能写项目根 CHANGELOG；不单独给技能设版本号。
4. 新增技能必须在本表挂到具体步骤；跨阶段技能挂到所有适用阶段。
5. **收敛**：长期无 step/`skills_required` 挂载、与相邻技能高度重复 → 并入 `references/` 或合并技能；经「体检capabilities/通用优化技能」确认后再删目录，禁止静默删技能。
6. **生态吸收**：经 `skill-audit` discover（`npx skills find` / find-skills）确认后，只**方法回灌**本目录或登记 `{workroot}/capabilities/`；禁止外部 skill 原样并行第二套编排。

**5. 验收清单**

- [ ] name 与目录一致；description 含 what/when/中文触发。
- [ ] 有适用/不适用、流程、判定、反模式或反合理化、验证。
- [ ] 无红线/门复制；引用路径存在；无宿主/模型硬编码。
- [ ] ≤500 行；超长已拆 references；映射已更新。
- [ ] `check_skills.py --strict` 通过；版本/CHANGELOG 已同步。
