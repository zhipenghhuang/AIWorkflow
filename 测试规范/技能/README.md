# 包内专业技能（随包生效 · 无需安装/挂载）

> **定位**：每一步的**专业方法与手艺**（playbook），随本包分发。命中步骤 → 步骤注记直接加载对应 `技能/<name>/SKILL.md` → 按技能标准执行。  
> **目录结构**：`技能/<name>/SKILL.md`（`name` 取 frontmatter）；随包复制、**无需安装**；AGENTS/步注直接按路径读取。宿主支持本地 skills 根时，可把 `技能/` 指向本地 skills 目录（可选，不是前置条件）。  
> **格式**：每份技能含 `name` / `description` frontmatter（Agent Skills 兼容），描述中的触发条件用于 AI 选择技能。  
> **来源**：以下技能是参考 GitHub/企业实践后**改写整合**的中文随包技能，不是把 GitHub 仓库原样搬入；外部 GitHub skill 走 `能力/00-能力注册表.md`（可选）。  
> **与「规则」的区别**：技能给方法；红线/口径/门以 `AGENTS.md` 与 `规则/` 为准（冲突时规则优先）。  
> **整合来源**（方法参考，已改写适配为中文随包版，非逐字复制）：fishzjp/qa-skills（MIT；requirement-analysis / clarify-pattern / test-strategy 的需求模型、九类歧义、证据分级）、JohnWayneeee/casely-qa-skill（MIT；规格洞/TestRail-ready）、gneder/qa-test-plan-skill（MIT；需求→计划/Gherkin）、GitHub Spec Kit（MIT；clarify/analyze 歧义与一致性）、addyosmani/agent-skills（MIT；interview-me）、社区 QA 技能库、ISTQB 系实践、wshobson/agents（MIT）测试/安全技能、schemathesis 等工具社区经验。

## 步骤 → 技能映射

| 步骤 / 轨 | 技能 |
| --- | --- |
| analyze（需求/测试依据建模） | `技能/test-basis-analysis/SKILL.md`（需求模型/冲突/九类歧义/oracle/TP 追溯） |
| analyze / plan | `技能/test-analysis-and-plan/SKILL.md`（企业级计划/类型选择/执行编排） |
| generate（功能/专项） | `技能/testcase-design/SKILL.md` |
| execute（功能/探索式/计划驱动） | `技能/test-execution-and-exploration/SKILL.md`（计划编排/回归/探索） |
| 接口轨 | `技能/test-interface/SKILL.md`（脚本优先 + 契约/复用；+ `规则/轨契约/接口.md`） |
| 发布前轨 | `技能/test-performance-security-compatibility/SKILL.md`（基础/标准/高风险级 + 工具矩阵；+ `规则/轨契约/发布前.md`） |
| report | `规则/模板/测试报告模板.md` + `规则/工作流.md` §4（即技能） |
| defect | `规则/缺陷协作.md`（即技能） |
| 脚本档 | `规则/脚本执行.md`（即技能） |
| onboard | `agents/onboard-agent.yaml`（核验清单即技能） |

**维护**：改技能 → 改本目录（母版改，随包分发）；技能只写方法，**禁**另立红线/门（SSOT 在 `AGENTS.md`/`规则/`）。
