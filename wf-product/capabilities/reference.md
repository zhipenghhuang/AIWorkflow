# 能力参考目录（非实例真源）

> **定位**：装配/体检时的**候选举例**。**不**代替 `{workroot}/capabilities/00-能力清单.md`。契约见 `00-contract.md`。

## 1. 候选实现

| 能力名 | 主选 | 备选 |
| --- | --- | --- |
| `git` | 宿主内置 git | — |
| `子代理` | 宿主子代理 | — |
| `defect-platform` | 本包内置 zentao 适配 | Jira MCP；ONES/TAPD 按适配 |
| `docs-mcp` | upstash/context7（MIT） | — |
| `browser-automation` / `browser-mcp` | chrome-devtools-mcp | playwright-mcp；skill-cli（ego-lite 等） |
| `spec-clarify` | addyosmani/agent-skills interview-me | deanpeters/Product-Manager-Skills |
| `pm-skills` | deanpeters/Product-Manager-Skills | bmad-code-org/bmad-method@bmad-agent-pm；chituai/prd-writer |
| `clarify-grill` | mattpocock/skills@grill-me | mattpocock/skills@grill-with-docs |
| `prototype-skill` | mattpocock/skills@prototype | — |
| `handoff-skill` | mattpocock/skills@handoff | — |
| `skill-discovery` | vercel-labs/skills@find-skills | — |
| `design-diagram` | tt-a1i/archify（MIT） | mermaid |
| `design-intelligence` | nextlevelbuilder/ui-ux-pro-max-skill | — |
| `ui-generation` | superdesigndev/superdesign-skill | — |
| `frontend-design` | anthropics/skills frontend-design | — |
| `design-review` | vercel-labs/agent-skills web-design-guidelines | — |
| `design-tokens` | arvindrk/extract-design-system | — |
| `prototype` | GLips/Figma-Context-MCP | grab/cursor-talk-to-figma-mcp |
| `doc-suite` | anthropics/skills 文档技能集 | Markdown |
| `presentation` | zarazhangrui/frontend-slides | addsumtech/slides_maker |
| `demo-video` | noamdorr/saas-product-demo-video | vincentsch/explainroo |
| `gtm` | AIDevGTM/gtm-cofounder | LiChang1125/B2B_Sales_Agent_Skill |
| `issue-tracker` | 禅道适配；Jira MCP | export |
| `analytics` | 项目 SQL/BI | — |
| `experimentation` | growthbook/growthbook | Unleash；Statsig |
| `product-analytics` | PostHog/posthog | 项目 BI |

## 2. 生态索引

- 技能安装器：vercel-labs/skills（`npx skills find` / find-skills）；标准：agentskills.io、anthropics/skills、addyosmani/agent-skills、mattpocock/skills。
- PM：deanpeters/Product-Manager-Skills；BMAD PM 仅作方法参考；设计底座：包内原型技能 + `prototype-scaffold.html`。
- 吸收纪律：体检 discover 后方法回灌 `skills/` 或装配本表能力；禁止外装 skill 覆盖口令→workflow。
- 实例写入：`{workroot}/capabilities/`；宿主安装见 README「宿主适配」。
