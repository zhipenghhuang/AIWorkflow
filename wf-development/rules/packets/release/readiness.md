# 步骤包 · release/readiness

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-development
- **workflow**：`release`
- **step**：`readiness`（发布就绪检查）
- **packet**：`rules/packets/release/readiness.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/release/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/release/_region-ready.md`（就绪与批准；进本区一次）。

## 2. 本步目标

- **目标**：发布就绪检查
- **产出**：上线检查单（{workroot}/60-release/）

## 3. 本步硬约束

### 开局硬约束（本步可执行摘要）

- 1. **先意图、再动作**（`confirm_task_intent`）：新开先【需求与意图理解】再确认；未确认禁改代码/外发/下完成结论。
- 2. **短读跟随 + 一手源**：`activeContext` + 进行中（`rule_card`/`packet=`/`region=`）+ 偏好/洞见/坑 ≤3。
- 3. **状态机读链（硬）**：见本包「本步读链与防丢失」。父流程可拆子机；同时只激活**一个**步骤包。
- 4. **技能闭环（质量不降）**：步骤包 §6 标**必开**的 skill 必须打开→按必做执行→**回到步骤包**；禁止把 skill 正文嵌进步骤包替代实读；禁止跳过必开 skill。
- 5. **完成分层**：`verify/Invoke-Gate.ps1 -Claim` → 只认 `CLAIM: ALLOWED`。无 ALLOWED 禁止写「已通过」。
- 6. **前端硬门**：有 UI → 当前步骤包内前端硬门；无 UI 标 `na`。
- 7. **证据先于结论；禁刷绿**；密钥零入库；最小改动；失败同方案 2 次换路径。
- 8. **切步/出子机 → 心跳一行**，必须带 `packet=`（有子机带 `region=`）。

### 本步读链与防丢失

- **编排**：本文 §5 +（若 §7 列出）一个模板。
- **方法质量**：§6 必开/条件开技能 → **打开→执行→回本包**（同时 1 个 skill）；禁止用粘贴代替实读。
- **禁止**：通读 rules / 多 step packet / 预读本 workflow 全部 skill。
- **完成声称**：有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **上下文锚**：`packet=`/`reads=` 必须含本 packet；切步/出子机前心跳刷新。


## 4. 本步门

- **GATE `release-readiness`**：**checklist**：按上线检查单逐项核；硬项不过 → NO-GO；test/staging 部署不适用

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`acceptance-and-launch`、`observability-and-instrumentation` → 见 §6 闭环。

### 本步动作清单

- **先判目标环境（硬前置）**：test/staging/UAT → 立即停止本工作流，按 S7 环境部署（版本按项目策略），不触发 `confirm_deploy`。
- 只有 prod/生产/正式才继续。无法判断 → 只问一次“目标环境是 test/staging 还是生产？”，不得默认生产。 技能：`skills/qa-handoff-and-release/SKILL.md`、`skills/acceptance-and-launch/SKILL.md`（先读再核）。 读 `{workroot}/development-plan.md`（旧项目可 `{workroot}/00-governance/development-plan.md`。
- L2+。
- 无则提示缺口，不阻塞单包发布）。 收到产品发布决策/UAT 交接包 → 先按 `workflows/handoff.yaml` receive 签收并回执。
- 未签收不得把业务验收当已通过。 按 `rules/templates/40-delivery/go-live-checklist-template.md` 逐项核：需求/AC、提测单/构建交接（无 QA 项目用自测报告/构建记录替代）、评审、 测试报告/准出、UAT（如适用）、安全/依赖/密钥、配置/迁移、回滚预案、监控/告警/值班、通知、变更审批。 **硬项**：有代码/配置改动的发布，必须读本轮 `.gate/wf-development/completion.json` 且 `verdict=COMPLETE`、`diff_hash`/提交与当前构建一致。
- 并要求**工作区干净、构建来自已提交或已打 tag 的版本**。
- BLOCKED/旧回执/脏工作区 → NO-GO。纯文档发布写「不适用+依据」。 **环境边界**：本工作流用于生产/正式发布。
- test/staging 部署不作为 S8，版本按项目版本策略，记录归 S7/`{workroot}/60-release/`。
- 无生产部署形态写「不适用 + 依据」，正式基线按验收/迭代收口。生产发布必须是正式版（无 prerelease）。
- rc/QA 批次不得直接上生产。 任一硬项不过 → NO-GO。
- 例外写风险/补偿/批准人。上线检查单一版一档，落 `{workroot}/60-release/`。 **证据分域**（子代理编排 ）：L3/多系统 → 按检查域只读扇出（需求/测试/安全依赖/配置迁移/回滚监控），各返回 pass/fail＋证据链接 ≤30 行。
- GO/NO-GO 由本步集中判定。
- 小发布直做。 输出 `release_ready=GO/NO-GO` 供后续步骤判断。
- 审批记录由 approval 步回填，不在 readiness 阶段伪填“已审批”。

## 6. 技能指向（打开 → 执行 → 回本包）

> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  
> 同时只打开 **1** 个 skill；打开期间 `reads=` 可暂加该 skill 路径，闭环结束后以本 packet 为准。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `acceptance-and-launch` | **必开** | 进入本步即开（质量不降） | `skills/acceptance-and-launch/SKILL.md` | 必做区 → 回本包 |
| `observability-and-instrumentation` | **必开** | 进入本步即开（质量不降） | `skills/observability-and-instrumentation/SKILL.md` | 必做区 → 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/release/_chain.md`。
- 子状态机（进区一次）：`rules/packets/release/_region-ready.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 验证：`verify/Invoke-Gate.ps1`（完成声称加 `-Claim`）；有 UI 另按 §5 前端硬门。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:release | step=readiness | packet=rules/packets/release/readiness.md | reads=rules/packets/release/readiness.md[+skill] | skills=acceptance-and-launch,observability-and-instrumentation|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/release/readiness.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
