# AGENTS.md

> **用途**：开发协作 AI 入口。  
> **新会话必读顺序（硬）**：① 开局卡 → ② 口令表（未路由）→ ③ `_chain`（进 wf）→ ④ `_region-*`（进长链子区）→ ⑤ 步骤包 → ⑥ §6 **必开** skill 闭环（打开→执行→回包）→ ⑦ 可选 1 模板。  
> **已路由中段**：心跳（必带 `packet=`）+ `rule_card`；**禁止**每步重读本文全文、禁止同时多 packet。  
> **位置**：`wf-development/`。与项目根 `AGENTS.md` 冲突时以根为准；与用户指令冲突见 §0 第 5 条。  
> **template_version**：`2026.11.05.04`（状态机分区；技能打开→执行→回包；质量不降）。  
> **架构**：`_chain`/`_region`（路径）+ 步骤包（编排/门）+ skills（方法闭环）+ verify。  
>
> **完成口径**：只认开局卡第 5 条 + `verify/Invoke-Gate.ps1 -Claim` → `CLAIM: ALLOWED`。前端只认**当前步骤包**内「前端硬门」节（无 UI 标 `na`）。

## 0. 开工

> **硬约束全文**：`rules/core/cold-start.md`。本节只补分级与指针，不重复开局卡正文。

1. **中文**；写现行结论。  
2. **短读**：`activeContext` 总览 + 本包进行中（含 `rule_card`）+ **偏好/洞见/坑 ≤3 行**（开局卡第 2 条；写法 `context-memory.md`）；有 `project-profile.md` → §1+§2 表（每新会话一次）。L2+ 有计划才读 `development-plan.md`。  
3. **接入**：`wf-development onboard: done` 则跳过，否则按 onboard-agent 一次判定。  
4. **独立判断 / 择优**：不适配 → 依据+主推；用户二次坚持 → `deviation=`。  
5. **覆盖优先级**：用户明确指令 > 根 AGENTS > 本文 > agent > profile。  
6. **读取**：分级读链（开局卡 §4）；YAML 非规则正文；技能按步骤包 §6 索引（同时 ≤1）。  
7. **契约**：`execution-contract.md` §1.0（【需求与意图理解】+【动作前分析】；只读分析）；开局卡第 1 条已点名，细则不改档位。  
8. **心跳**：`rule-anchor.md`（切步/过门必做）。

### 0.0 事实与文档

事实可核实；待确认禁升格；正式资产只写现行。细则 `doc-quality.md`。版本分离见 `versioning.md`。

### 0.1 任务分级

| 级别 | 典型 | 必走 | 可跳过 |
| --- | --- | --- | --- |
| L0 | 单文件/文案/配置；无行为契约变化 | clarify→implement→verify→commit | requirements/design/review-docs/plan/review/deliver |
| L1 | 多文件、范围收敛 | clarify→（轻量卡）→implement→（按风险 review）→verify→（有QA）deliver→commit | 全量 PRD/ADR |
| L2 | 新功能/跨模块/接口数据 | requirements→design?→**review-docs**→plan→implement→review→verify→deliver→… | 无 |
| L3 | 权限/资金/迁移/公共API/破坏性 | L2 + 独立审 + 安全 + 回滚 + 发布审批 | 无 |
| 缺陷 | 平台缺陷/修复# | `defect-fix` 链 | 无平台→change |

### 0.2 确认门 · 澄清

门只认 YAML `hitl*` + `gates.md`；澄清只认 `clarification.md`。理解包 §0 必填。

### 0.3 硬红线

只认开局卡八条 + 当前步骤包硬约束/做法（有 UI 遵守包内「前端硬门」；无 UI 标 na）。失败同方案 2 次换路径。

### 0.4 验证与汇报

完成只认 `-Claim` → `CLAIM: ALLOWED`。SSOT：`verification.md` + `verify/README.md`。

### 0.5 工程与执行

实施勾选 `iq-checklist.md`；词典 `implementation-quality.md`。git/部署：`workflow.md` §2；`versioning.md`。默认只提交。交接：`handoff.md`。

## 1. 接入

实例：`project-profile.md` + `activeContext.md`；工作根 `{workroot}/`；原件根 `inbound/`。口令「接入/档案/文档树」→ `onboard.yaml`。细则 `doc-governance.md` §2.4。

## 2. 收尾

骨架：`rules/templates/90-handoff/closeout-skeleton.md` §1 通用占位（按项目事实填；禁照抄他例；缺项=未收尾）。提交/推送/部署分门确认；默认仅提交。

## 3. 口令 → Workflow（命中即停）

> 表内为常见示例；未命中 → `rules/core/routing.md`。首条须 `route=…|step=…|level=…|reason=…|reads=…|next_action=…`。

| 优先 | 命中 | workflow | 入口 step / 默认 agent |
| ---: | --- | --- | --- |
| 0 | 工作总结/今日总结 | — | `closeout-skeleton.md` §1 |
| 1 | 缺陷修复/指派/修复#；产品回复→`product_decision` | `defect-fix` | defect-fixer |
| 2 | 新文档/变更吸收 | `intake` | scan |
| 3 | 按方案实施/继续迭代 | `iterate` | precheck |
| 4 | 接入/档案/文档树/inbound/README 整理 | `onboard` | 对应 step |
| 4.3 | 技能/能力体检或优化 | `skill-audit` | scope→wrap/commit |
| 4.4 | 导出资料库/发资料 | `materials` | select→… |
| 5 | 提交/推送 | 当前末步或 `change` | commit |
| 5.1 | 轻量开发/想法落地 | `solo` | frame |
| 5.2 | 轻量方案 | `solo` | plan |
| 5.3 | 轻量测试/验收 | `solo` | test |
| 6 | 常规变更/需求澄清 | `change` | clarify |
| 6.1 | 分析 PRD/方案/原型 | `change` | analyze_input |
| 7 | 出方案/只出方案 | `change` | design |
| 7.1 | 方案/文档评审 | `change` | review-docs |
| 8 | 代码评审 | `change` | review |
| 9 | 提测/发布说明/回滚预案 | `change` | deliver |
| 10 | 发布/上线（生产） | `release` | readiness |
| 11 | 回滚 | `release` | rollback |
| 12 | 复盘 | `retro` | gather |
| 13 | 开发计划/下一步/按计划执行 | `control` | init/sync/next/check/run |
| 14 | 维护/查询 | 本文 + `maintenance.md` | — |
| 15 | 写交接单/交接包/接收/变更/重规划 | `handoff` | compose（默认） |

**部署**：裸「部署」先判环境；test/staging≠S8；prod→`release`。提交/推送≠部署。  
**续跑有计划**：「下一步/继续开发计划」优先 `control`。

## 4. 维护

改开局卡 → `rules/core/cold-start.md`；改前端硬门真源 → `frontend-gate.md` 后须 `build_step_packets.py` 重生包；改不变量/口令 → 本文；改步骤 → `workflows/` + `rules/packets/`（改后跑 `build_step_packets.py`）；改心跳 → `rule-anchor.md`；自检 → `maintenance.md` §2 + `Validate-StepPackets.ps1`。

## 5. 文档治理（摘要）

工作根/原件根/换迭代：`doc-governance.md`。根 `CHANGELOG.md`=产品发版史；`{workroot}/work-log.md`=岗位里程碑。

## 6. 技能与能力

命中步必读 `skills/<name>/SKILL.md`（先读「必做」区）。能力实例 SSOT=`{workroot}/capabilities/00-能力清单.md`。

## 7. 多包

单包独立为默认；缺他包不阻塞。一次会话只跑一个包 workflow。歧义定包查 `wf/AGENTS.md` 意图→包。
