# 能力与技能体检 · `skill-audit` 状态机

> 全局规则见 `rules/core/global-rules.md`（每步必读并逐条过；切步/过门/续跑都重读）。每步先读当前步骤卡；进本 workflow 读一次；当前状态以 `activeContext` 为续跑指针；已有测试计划时阶段语义以计划 §0 为准。**只读当前 packet**，不通读全链。

## 1. 入口与终止

- **入口**：`体检能力` → `scope`；`能力技能体检` → `scope`；`检查技能能力` → `scope`；`能力优化` → `scope`；`技能优化` → `scope`；`优化能力` → `scope`；`优化技能` → `scope`；`优化技能能力` → `scope`；`更新能力建议` → `scope`；`更新技能` → `scope`；`维护技能能力` → `scope`；`通用优化技能` → `scope`；`通用最优技能` → `scope`
- **终端**：`closeout`（共享 `rules/packets/_shared/closeout.md`）
- **读链**：按 `rules/core/global-rules.md` §7；全局规则每步读并逐条过；本图进链读一次；每步先读当前 packet。

## 2. 状态表

| # | state | 角色 | when | 门 | 产出 | 下一步 | 失败/跳过 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `scope` | `onboard-agent` | — | — | 体检范围卡（模式 project/generic、范围、依据） | `inventory` | 停在本步/升级 |
| 2 | `inventory` | `onboard-agent` | — | — | 库存摘要（capabilities/skills/映射/缺口，含证据） | `discover` | 停在本步/升级 |
| 3 | `discover` | `onboard-agent` | — | — | 生态检索表（query / 候选 / installs / 吸收动作 / 证据） | `fit` | 停在本步/升级 |
| 4 | `fit` | `onboard-agent` | — | — | 适配分析表（够用/缺口/过重/冲突/重复/映射断裂/可吸收方法 + 证据） | `propose` | 停在本步/升级 |
| 5 | `propose` | `onboard-agent` | — | — | {workroot}/changes/能力技能体检-{yyyyMMdd}.md（工作产物，不进资料区） | `apply` | 停在本步/升级 |
| 6 | `apply` | `onboard-agent` | — | `confirm_skill_changes` | 已应用变更清单 + ValidateTemplateRefs / check_skills 自检结果 | `closeout` | 停在本步/升级 |
| 7 | `closeout` | `onboard-agent` | — | `confirm_commit` | 任务收尾 + 拟提交确认 | `—` | 停在本步/升级 |

## 3. 推进

- 本链为全链入口；按表推进到下一个门/停点。
- `when` 不满足 → 跳过该状态（不打开其 packet），收尾记 `skip=理由`。
- 切步/过门：更新 `activeContext` 运行状态 + 一行锚；不重读本图。
- 续跑：读运行状态里的 `packet=`，从该步继续；packet 丢失用本表定位。
- 失败：按状态表“失败/跳过”回退或停下；不静默跳过。

## 4. 边界

- **本链专属**：`workflows/skill-audit.yaml` + 本图 + `rules/packets/skill-audit/`；改本链只重生成该链。
- **共享**：`rules/core/`、`rules/gates.md`、`skills/`、`rules/templates/`；改共享层跑全包自检。
- 跨链：重新路由或 handoff；诊断可读对方状态图，不打开对方 packet。

## 5. 终端

- 所有 domain 状态结束后进入 `closeout`；`done / blocked / cancelled` 三选一，未过门不得 `done`。
