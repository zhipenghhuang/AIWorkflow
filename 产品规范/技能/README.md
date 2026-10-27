# 包内专业技能（随包生效 · 无需安装/挂载）

> **定位**：每一步的**专业方法与手艺**（playbook），随本包分发。命中步骤 → 步骤注记直接加载对应 `技能/<name>/SKILL.md` → 按技能标准执行。  
> **目录结构**：`技能/<name>/SKILL.md`（`name` 取 frontmatter）；随包复制、**无需安装**；AGENTS/步注直接按路径读取。宿主支持本地 skills 根时，可把 `技能/` 指向本地 skills 目录（可选，不是前置条件）。  
> **格式**：每份技能含 `name` / `description` frontmatter（Agent Skills 兼容），描述中的触发条件用于 AI 选择技能。  
> **来源**：以下技能是参考 GitHub/企业实践后**改写整合**的中文随包技能，不是把 GitHub 仓库原样搬入；外部 GitHub skill 走 `能力/00-能力注册表.md`（可选）。  
> **与「能力」的区别**：技能=怎么做（方法/清单/手感，随包生效、必用）；`能力/00-能力注册表.md` 的能力=用哪些外部工具（选装；本机可用即自动使用、不可用走降级）。  
> **与「规则」的区别**：技能给方法；红线/门以 `AGENTS.md` 与 `规则/` 为准（冲突时规则优先）。  
> **整合来源**（方法参考，已改写适配为中文随包版）：deanpeters/Product-Manager-Skills、shinpr/prd-reviewer（异上下文 PRD 审）、headout pm-os l1-reviewer（问题/反范围/场景/可测 AC）、NIST AI RMF / ETIS 评审（AI 产物人责）、addyosmani/agent-skills、fishzjp/qa-skills、chituai/prd-writer；0→1 参考 Stage-Gate / Lean Startup / Working Backwards；客户发现参考 The Mom Test / JTBD / Continuous Discovery / BABOK；视觉参考 WCAG 2.2 与主流设计系统。  

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

## 步骤 → 技能映射

| 步骤 | 技能 |
| --- | --- |
| plan：goals / roadmap | `技能/zero-to-one-product-definition/SKILL.md`（0→1）+ `技能/requirement-discovery-and-prioritization/SKILL.md`（迭代）+ `技能/customer-needs-discovery/SKILL.md`（目标依据） |
| new-product：discover / go / define | `技能/zero-to-one-product-definition/SKILL.md` + `技能/customer-needs-discovery/SKILL.md` |
| prd：discover / prioritize | `技能/customer-needs-discovery/SKILL.md` + `技能/requirement-discovery-and-prioritization/SKILL.md` |
| prd：prd（撰写） | `技能/prd-writing/SKILL.md`（§9 完稿自检摘要 + P1↑；与 `03` 同源） |
| prd：review（评审定稿） | `技能/artifact-review/SKILL.md`（先选 A/B）+ `技能/review-and-finalize/SKILL.md`（选 B 量规） |
| plan：review-plan | `技能/artifact-review/SKILL.md` |
| prototype：review | `技能/artifact-review/SKILL.md` + `技能/ui-visual-design-system/SKILL.md` |
| deliver：review-plan-deliver | `技能/artifact-review/SKILL.md` |
| change/defect：review（实质变更重审） | `技能/artifact-review/SKILL.md`（先选 A/B）+ `技能/review-and-finalize/SKILL.md`（选 B） |
| change：intake / triage / assess / apply / verify（需求/问题/产品缺陷/变更） | `技能/customer-needs-discovery/SKILL.md`（intake）+ `技能/change-management/SKILL.md` |
| defect：pull / analyze / apply / writeback（平台缺陷协作） | `技能/change-management/SKILL.md` + `规则/缺陷/缺陷平台协作.md` |
| prototype：context / ia / wireframe / engineering / review / usability / handoff | `技能/prototype-and-interaction/SKILL.md`（设计策略/项目适配/交接边界） |
| prototype：visual / hi-fi | `技能/ui-visual-design-system/SKILL.md`（设计系统策略/设计方向/tokens） |
| deliver：schedule / followup（变更转 change） | `技能/change-management/SKILL.md` |
| deliver：uat / release（含复盘） | `技能/uat-and-retrospective/SKILL.md` |
| showcase：audience / story / demo / dryrun | `技能/demo-storytelling/SKILL.md` |
| showcase：materials | `技能/presentation-design/SKILL.md` |
| showcase：docs | `技能/product-docs/SKILL.md` |
| onboard | `agents/onboard-agent.yaml`（核验清单即技能） |

**维护**：改技能 → 改本目录（母版改，随包分发）；技能只写方法，**禁**另立红线/门（SSOT 在 `AGENTS.md`/`规则/`）。
