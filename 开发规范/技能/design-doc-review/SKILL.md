---
name: design-doc-review
description: Use when reviewing development landing documents (requirements baseline, solution design, ADR, frontend design notes, task plan). Ask human vs AI review mode first; apply enterprise design-doc rubric when AI review is chosen. 中文触发：设计文档评审、需求基线、技术方案、ADR、前端设计说明、任务计划、A/B 评审。
---

# 开发落地文档评审（技能 · 随包生效）

> 用于：需求基线 / 技术方案 / ADR / 前端设计说明 /（可选）任务清单与开发计划中**将直接指导编码实施**的产物。  
> **不替代**代码评审（`code-review` / `reviewer-agent` 的 diff 步）。  
> 门：`select_review_mode` → A 自行通过｜B AI 独立评审 → 实施前授权仍认 `confirm_*`。

## 1. 必须先停问

落地设计类文档落盘、进入 implement 前，**STOP**：

```text
【评审方式】产物={方案/基线/ADR/前端设计说明路径}｜级别={L0～L3}
请二选一：
A. 自行评审通过 — 你过目后放行；AI 只附结构/评分卡自检摘要；review_status=HUMAN_APPROVED
B. AI 独立评审 — 另起文档评审身份按量规审；产出 开发/.../评审-文档-{主题}-{时间}.md
（回复 A 或 B；不得未问自选）
```

- 用户点名「方案评审」且要 AI → B；「我看过了/自行通过」→ A。  
- L0 微改无新方案文档 → 本门跳过。  
- L2+ 有新方案/基线/破坏性 ADR → **必问**。

## 2. 强制适用

> **是否合理**：基线/方案/ADR/前端说明决定「做什么、怎么做」——强制 A/B；任务清单偏执行拆解，默认 A 即可，避免每页都停问。选 B 时主动找范围漂移/不可验证/回滚空洞。

| 产物 | 强制选模式 |
| --- | --- |
| 需求基线（新功能/范围变） | 是（可与 `confirm_requirements` 同轮：先选模式再签收） |
| 技术方案（architecture/契约/高风险） | 是 |
| ADR（架构/破坏性） | 随方案 |
| 前端设计说明（补 UI 设计时） | 随方案一并向用户出示 |
| 任务清单 L2+ | 可选（默认 A + `confirm_backlog`）；点名 AI 则 B |
| 开发计划实质变更 | 可选结构核验走 `gate: dev-plan`；内容审可选 B |

## 3. 量规（IEEE 1028 / ISO 20246 技术评审取向）

### 单文档轴

| ID | 轴 | PASS | FAIL |
| --- | --- | --- | --- |
| D1 | 范围对齐 | 逐条响应 RP/F/R/AC；不擅自扩 | 静默加需求 |
| D2 | 可实施 | 接口/数据/权限/失败路径写清 | 「稍后细化」挡主路径 |
| D3 | 可验证 | 每条设计决策有验收/检查点 | 无法对照 AC |
| D4 | 兼容回滚 | 迁移/兼容/回滚或「不适用+理由」 | 破坏性无回滚 |
| D5 | 安全隐私 | 鉴权/输入/敏感数据有说 | L3 面缺失 |
| D6 | 观测与测试 | 日志/指标/测试策略 | 无观测无测略 |
| D7 | 一致性 | 与基线/ADR/前端说明无矛盾 | 三处口径冲突 |
| D8 | 三维体验 | UX/DX/AX 无净退化；开发阶段不背旧数据 | 为兼容堆双写（开发阶段） |

### 套件

- ADR 与方案结论一致；前端说明与原型/PRD 状态矩阵对齐。  
- engineering-quality 评分卡：阻断项满分；≥20/24。

## 4. A / B 路径

| | A 自行 | B AI |
| --- | --- | --- |
| 执行 | 出示自检摘要 + 等用户「通过」 | 独立上下文审 → 严重度缺口表 |
| 留痕 | HUMAN_APPROVED + 确认人/时间 | `评审-文档-*.md` + 量规表 |
| 需修 | 用户指出 → 回 design/requirements | 回作者修订 → 重审 ≤1 |
| 之后 | 仍走原 `confirm_spec`/`confirm_requirements`（若尚未签收） | 同左；AI 通过 ≠ 自动实施 |

## 5. 与代码评审边界

| | design-doc-review | code-review |
| --- | --- | --- |
| 时机 | 实施前 | 实施后 |
| 对象 | 方案/基线/ADR/设计说明 | diff + 证据 |
| 产物 | 评审-文档-*.md | `.gate/review.md` |

## 6. GitHub / 行业方法（内化）

| 来源 | 吸收 |
| --- | --- |
| IEEE 1028 / ISO/IEC 20246 | 技术评审找缺陷；角色分离 |
| arXiv LLM design-doc review | 结构完备 + 一致性 + 可追溯自动辅助 |
| Google Eng Practices / 小 CL | 设计先于大改；评审可扫描 |
| NIST AI RMF | AI 生成设计须人责；B 路径 AI 不终裁实施权 |
| engineering-quality / solution-design | 本包质量条与方案结构 |

可选能力：`code-review`/`design-review` 不替代本文档审；未装不阻塞。
