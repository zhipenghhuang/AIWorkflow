# 包内专业技能（随包生效 · 无需安装/挂载）

> **定位**：每一步的**专业方法与手艺**（playbook），随本包分发。命中步骤 → 步骤注记直接加载对应 `技能/<name>/SKILL.md` → 按技能标准执行。  
> **目录结构**：`技能/<name>/SKILL.md`（`name` 取 frontmatter）；随包复制、**无需安装**；AGENTS/步注直接按路径读取。宿主支持本地 skills 根时，可把 `技能/` 指向本地 skills 目录（可选，不是前置条件）。  
> **更新**：可就地改本目录。口令「体检能力」检查/优化（确认后应用）；「通用优化技能」按通用最优。外部 skill 走 `能力/` +「装配能力」。  
> **格式**：每份技能含 `name` / `description` frontmatter（Agent Skills 兼容），description 写“做什么 + 何时用 + 中文触发词”；正文为方法/步骤/判定/反模式/验证，单文件目标 ≤500 行（超长拆 `references/`）。质量标准见本文末节。
> **来源**：以下技能是参考 GitHub/企业实践后**改写整合**的中文随包技能，不是把 GitHub 仓库原样搬入；外部 GitHub skill 走 `能力/00-能力注册表.md`（可选）。
> **与「能力」的区别**：技能=怎么做（方法/清单/手感，随包生效、必用）；`能力/00-能力注册表.md` 的能力=用哪些外部工具（选装；本机可用即自动使用、不可用走降级）。  
> **与「规则」的区别**：技能给方法；红线/门以 `AGENTS.md` 与 `规则/` 为准（冲突时规则优先）。  
> **整合来源**（方法参考，已改写适配为中文随包版）：Agent Skills 规范（agentskills.io；frontmatter/渐进披露/≤500 行）、anthropics/skills、addyosmani/agent-skills（MIT；skill anatomy/反合理化/验证门）、deanpeters/Product-Manager-Skills、shinpr/prd-reviewer（异上下文 PRD 审）、headout pm-os l1-reviewer（问题/反范围/场景/可测 AC）、NIST AI RMF / Generative AI Profile、ISO/IEC 42001、EU AI Act（按适用）、OWASP Top 10 for LLM 2025、ETIS 评审（AI 产物人责）、Stage-Gate / Lean Startup / Working Backwards、The Mom Test / JTBD / Continuous Discovery / BABOK、WCAG 2.2、Core Web Vitals、Google SRE（SLI/SLO）、主流设计系统（许可以官方为准）。  

## 编号别名 → 实际路径（旧引用兼容）

| 别名 | 实际路径 |
| --- | --- |
| 00 | `技能/zero-to-one-product-definition/SKILL.md` |
| 01 | `技能/requirement-discovery-and-prioritization/SKILL.md` |
| 02 | `技能/prd-writing/SKILL.md` |
| 03 | `技能/review-and-finalize/SKILL.md` |
| 04 | `技能/change-management/SKILL.md` |
| 05 | `技能/uat-and-retrospective/SKILL.md` |
| 06 | `技能/prototype-and-interaction/SKILL.md` |
| 07 | `技能/ui-visual-design-system/SKILL.md` |
| 08 | `技能/demo-storytelling/SKILL.md` |
| 09 | `技能/presentation-design/SKILL.md` |
| 10 | `技能/product-docs/SKILL.md` |

> 新引用一律用实际路径；编号别名只用于兼容旧文本。  
> **无编号别名**（勿强加 00–10）：`customer-needs-discovery`、`competitive-intelligence-and-learning`、`analytics-and-experimentation`、`artifact-review` 等后增技能，只按目录名引用。

## 步骤 → 技能映射

| 步骤 | 技能 |
| --- | --- |
| plan：goals / roadmap | `技能/zero-to-one-product-definition/SKILL.md`（0→1）+ `技能/requirement-discovery-and-prioritization/SKILL.md`（迭代）+ `技能/customer-needs-discovery/SKILL.md`（目标依据）+ `技能/analytics-and-experimentation/SKILL.md`（指标树） |
| new-product：discover / go / define | `技能/zero-to-one-product-definition/SKILL.md` + `技能/customer-needs-discovery/SKILL.md` + `技能/competitive-intelligence-and-learning/SKILL.md`（模式 S） |
| prd：discover | `技能/customer-needs-discovery/SKILL.md` + `技能/requirement-discovery-and-prioritization/SKILL.md`；竞品分析口令加 `competitive-intelligence-and-learning`（S） |
| prd：benchmark | `技能/competitive-intelligence-and-learning/SKILL.md`（模式 P）+ `技能/requirement-discovery-and-prioritization/SKILL.md` |
| prd：prioritize | `技能/requirement-discovery-and-prioritization/SKILL.md` + 按需 `customer-needs-discovery` |
| prd：prd（撰写） | `技能/prd-writing/SKILL.md`（§9 完稿自检摘要 + P1↑；与 `03` 同源）+ `技能/analytics-and-experimentation/SKILL.md`（指标/埋点/实验） |
| prd：review（评审定稿） | `技能/artifact-review/SKILL.md`（先选 A/B）+ `技能/review-and-finalize/SKILL.md`（选 B 量规） |
| plan：review-plan | `技能/artifact-review/SKILL.md` |
| prototype：review | `技能/artifact-review/SKILL.md` + `技能/ui-visual-design-system/SKILL.md` |
| deliver：review-plan-deliver | `技能/artifact-review/SKILL.md` |
| change/defect：review（实质变更重审） | `技能/artifact-review/SKILL.md`（先选 A/B）+ `技能/review-and-finalize/SKILL.md`（选 B） |
| change：intake / triage / assess / apply / verify（需求/问题/产品缺陷/变更） | `技能/customer-needs-discovery/SKILL.md`（intake）+ `技能/change-management/SKILL.md` |
| defect：pull / analyze / apply / writeback（平台缺陷协作） | `技能/change-management/SKILL.md` + `规则/缺陷/缺陷平台协作.md` |
| prototype：context / ia / wireframe / engineering / review / usability / handoff | `技能/prototype-and-interaction/SKILL.md`（设计策略/项目适配/交接边界）；context 竞品借鉴按需 + `competitive-intelligence-and-learning` §5 |
| prototype：visual / hi-fi | `技能/ui-visual-design-system/SKILL.md`（设计系统策略/设计方向/tokens） |
| deliver：schedule / followup（变更转 change） | `技能/change-management/SKILL.md` |
| deliver：uat / release（含复盘） | `技能/uat-and-retrospective/SKILL.md` + `技能/analytics-and-experimentation/SKILL.md`（发布度量/实验） |
| showcase：audience / story / demo / dryrun | `技能/demo-storytelling/SKILL.md` |
| showcase：materials | `技能/presentation-design/SKILL.md` |
| showcase：docs | `技能/product-docs/SKILL.md` |
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
| 反模式 / 反合理化 | 常见错法或偷懒借口 + 纠正 | **必有其一**（不强制两者齐） |
| 红旗 | 可观察的违规信号 | ≥3 条 |
| 验证/DoD | 证据与退出条件 | 每条可复核 |

**3. 写作纪律**

- **流程而非知识**：写“先做什么、怎么判定、产出什么”，不写百科。
- **具体**：能写字段/阈值/模板节就不写“检查一下”；引用本包真实路径，不造文件。
- **单一出处**：红线/门/评分卡只引用，不复制；跨技能用名称引用。
- **渐进披露**：主文件目标 ≤500 行、≤4500 tokens；**超长才拆** `references/`。
- **宿主/模型中立**：不写死某宿主工具名、模型版本或私有调用方式；写能力与目标。
- **只写现行**：不记录历史过程/旧方案。业务项目禁止改项目根 CHANGELOG；过程/接入进本包工作日志。母版仓包能力变化由母版维护会话记母版根 CHANGELOG（通常开发落笔）。
- **中文优先**：方法与判定用中文；保留必要英文术语与代码/命令。

**4. 修改流程**

1. 改 `技能/<name>/SKILL.md`；同步本 README 映射与相关 workflow `notes`。
2. 跑 `规则/tools/Test-Template.ps1`；改引用/映射后跑 `规则/tools/Test-DocHygiene.ps1`。
3. 更新包 `AGENTS.md` `template_version`；业务项目不写项目根 CHANGELOG；母版仓可见包能力变化才记母版根 CHANGELOG；不单独给技能设版本号。
4. 新增技能必须在本表挂到具体步骤；跨阶段技能挂到所有适用阶段。

**5. 验收清单**

- [ ] name 与目录一致；description 含 what/when/中文触发。
- [ ] 有适用/不适用、流程、判定、反模式或反合理化、验证。
- [ ] 无红线/门复制；引用路径存在；无宿主/模型硬编码。
- [ ] ≤500 行；超长已拆 references；映射已更新。
- [ ] 自检通过；版本/CHANGELOG 已同步。
