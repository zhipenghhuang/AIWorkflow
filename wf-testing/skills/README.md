# 包内专业技能（随包生效 · 无需安装/挂载）

> **定位**：每一步的专业方法与手艺，随本包分发。命中步骤 → 步骤包 §6 打开并**整卡读取**对应 `skills/<name>/SKILL.md` → 按技能标准执行。  
> **目录结构**：`skills/<name>/SKILL.md`；随包复制、无需安装。  
> **更新**：可就地改本目录。口令「体检能力」检查/优化（确认后应用）；「通用优化技能」按通用最优。外部工具选型写入实例 `{workroot}/capabilities/`（「装配能力」）。  
> **格式**：每份技能含 `name` / `description` frontmatter；description 写“做什么 + 何时用 + 中文触发词”；正文为方法/步骤/判定/反模式/验证，单文件目标 ≤500 行。质量标准见本文末节。  
> **与「能力」的区别**：技能=怎么做（随包必用）；能力选型真源=`{workroot}/capabilities/00-能力清单.md`；包内契约/参考目录非真源。  
> **与规则的区别**：技能给方法；红线/口径/门以 `AGENTS.md` 与 `rules/` 为准（冲突时规则优先）。

## 步骤 → 技能映射

| 步骤 / 轨 | 技能 |
| --- | --- |
| plan（分析必做 + 计划总排） | `skills/test-basis-analysis/SKILL.md`（来源/AC/设计点/意图/风险/Oracle） + `skills/test-analysis-and-plan/SKILL.md`（范围/轨道/轮次/准入准出） + `skills/test-data-and-environment/SKILL.md` |
| execute（功能/接口/探索/发布前/回归） | `skills/testcase-design/SKILL.md`（场景/深度/步骤） + `skills/test-execution-and-exploration/SKILL.md`（执行/记录/证据/回归） + `skills/test-data-and-environment/SKILL.md` + `skills/ai-feature-testing/SKILL.md`（AI 功能时） |
| 接口轨 | `skills/test-interface/SKILL.md`（契约/适用维/脚本/执行记录；+ `rules/tracks/api.md`） |
| 发布前轨 | `skills/test-performance-security-compatibility/SKILL.md`（风险级/指标/工具/韧性；+ `rules/tracks/pre-release.md`） |
| AI/LLM/RAG/Agent 功能 | `skills/ai-feature-testing/SKILL.md`（Oracle/评测集/重复阈值/红队） + `skills/test-performance-security-compatibility/SKILL.md`（安全） |
| report | `skills/test-report/SKILL.md`（结论判定/对账/缺口）+ `rules/templates/40-report-review/test-report-template.md` |
| defect | `rules/defects/collaboration.md` |
| 脚本档 | `rules/special/script-execution.md` |
| onboard | `agents/onboard-agent.yaml`（核验清单即技能） |

**维护**：改技能 → 改本目录；技能只写方法，禁另立红线/门（SSOT 在 `AGENTS.md`/`rules/`）。

## 技能质量标准（Skill Anatomy）

> 依据 Agent Skills 规范与 addyosmani/agent-skills 的 skill anatomy，结合本包“规则/技能分离”约束。

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
| 反模式 / 反合理化 | 常见错法或偷懒借口 + 纠正 | **必有其一**；`check_skills.py` 硬闸 |
| 红旗 | 可观察的违规信号 | 推荐 ≥3 |
| verify/DoD | 证据与退出条件 | 每条可复核 |

**3. 写作纪律**

- **流程而非知识**：写“先做什么、怎么判定、产出什么”。
- **具体**：能写字段/阈值/命令就不写“检查一下”；引用本包真实路径。
- **单一出处**：红线/门/评分卡只引用，不复制。
- **渐进披露**：主文件建议 ≤500 行；步骤卡 §6 默认**整卡读取**；确实过长的附录/命令/样例才拆 `references/`，由正文点名再开。
- **宿主/模型中立**：不写死某宿主工具名、模型版本或私有调用方式。
- **只写现行**：不记录历史过程/旧方案。

**4. 修改流程**

1. 改 `skills/<name>/SKILL.md`；同步本 README 映射与相关 workflow `notes`。
2. 跑 `rules/tools/Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`；改引用后跑 `Test-DocHygiene.ps1`；必跑 `check_skills.py <包根> --strict`。
3. 更新包 `AGENTS.md` `template_version`。
4. 新增技能必须挂到具体步骤。
5. **生态吸收**：经 `skill-audit` discover（`npx skills find` / find-skills）确认后，只**方法回灌**本目录或登记 `{workroot}/capabilities/`；禁止外部 skill 原样并行第二套编排。

**6. 验收清单**

- [ ] name 与目录一致；description 含 what/when/中文触发。
- [ ] 有适用/不适用、流程、判定、反模式或反合理化、验证。
- [ ] 无红线/门复制；引用路径存在。
- [ ] ≤500 行；映射已更新。
- [ ] `check_skills.py --strict` 通过。
