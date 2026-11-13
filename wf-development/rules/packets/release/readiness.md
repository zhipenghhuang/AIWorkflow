# 步骤卡 · release/readiness

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`release` / `readiness`（发布就绪检查）
- **packet**：`rules/packets/release/readiness.md`
- **角色**：`delivery-lead`（交付/发布/验收编排）。提测就绪 → UAT/验收 → 发布审批 → 部署 → 冒烟/监控 → 发布记录/复盘；本步只做该角色职责；越界交回或升级。
- **上游**：无（链首）
- **后续**：`acceptance`（进 `acceptance` 前的 `when=has_uat`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。

## 2. 本步目标

- **目标**：发布就绪检查
- **产出**：上线检查单（{workroot}/60-release/）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **GATE `release-readiness`**：**checklist**：按上线检查单逐项核；硬项不过 → NO-GO；test/staging 部署不适用
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`acceptance-and-launch`、`observability-and-instrumentation` → 见 §6 闭环。

- **条件技能**：`qa-handoff-and-release`（有提测/交接物） → 命中则同样走 §6 闭环。

### 本步动作清单

- **先判目标环境（硬前置）**：test/staging/UAT → 不进入本链：按项目档案命令部署并出环境部署记录（`rules/templates/40-delivery/env-deployment-record-template.md`，版本按项目策略），不触发 `confirm_deploy`。
- 只有 prod/生产/正式才继续。
- 无法判断 → 只问一次“目标环境是 test/staging 还是生产？”，不得默认生产。
- 技能见 §6 `qa-handoff-and-release`、§6 `acceptance-and-launch`（先读再核）。
- 读 `{workroot}/development-plan.md`（旧项目可 `{workroot}/00-governance/development-plan.md`；L2+；无则提示缺口，不阻塞单包发布）。
- 收到产品发布决策/UAT 交接包 → 先按 `handoff.receive` 签收并回执。
- 未签收不得把业务验收当已通过。
- 按 `rules/templates/40-delivery/go-live-checklist-template.md` 逐项核：需求/AC、提测单/构建交接（无 QA 项目用自测报告/构建记录替代）、评审、 测试报告/准出、UAT（如适用）、安全/依赖/密钥、配置/迁移、回滚预案、监控/告警/值班、通知、变更审批。
- **硬项**：有代码/配置改动的发布，必须读本轮 `.gate/wf-development/completion.json` 且 `verdict=COMPLETE`、`diff_hash`/提交与当前构建一致。
- 并要求**工作区干净、构建来自已提交或已打 tag 的版本**。
- BLOCKED/旧回执/脏工作区 → NO-GO。
- 纯文档发布写「不适用+依据」。
- **环境边界**：本工作流用于生产/正式发布。
- test/staging 部署不作为 S8，版本按项目版本策略，记录归 S7/`{workroot}/60-release/`。
- 无生产部署形态写「不适用 + 依据」，正式基线按验收/迭代收口。
- 生产发布必须是正式版（无 prerelease）。
- rc/QA 批次不得直接上生产。
- 任一硬项不过 → NO-GO。
- 例外写风险/补偿/批准人。
- 上线检查单一版一档，落 `{workroot}/60-release/`。
- **证据分域**（子代理编排 ）：L3/多系统 → 按检查域只读扇出（需求/测试/安全依赖/配置迁移/回滚监控），各返回 pass/fail＋证据链接 ≤30 行。
- GO/NO-GO 由本步集中判定。
- 小发布直做。
- 输出 `release_ready=GO/NO-GO` 供后续步骤判断。
- 审批记录由 approval 步回填，不在 readiness 阶段伪填“已审批”。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。
> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `acceptance-and-launch` | **必开** | 进入本步即开（质量不降） | `skills/acceptance-and-launch/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `observability-and-instrumentation` | **必开** | 进入本步即开（质量不降） | `skills/observability-and-instrumentation/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `qa-handoff-and-release` | 条件开 | 有提测/交接物 | `skills/qa-handoff-and-release/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（主）**：`rules/templates/40-delivery/go-live-checklist-template.md`；只读本步用到的节，禁止整文件通读。
- **配套模板（按产出需要读；门按结构判分的产物须对齐）**：`rules/templates/40-delivery/env-deployment-record-template.md`。
- **产出前自检**：对照模板必填节逐项填写；缺节、空节、未替换 `{…}` = 不合格（不得标完成）。
- 验证命令：`verify/Invoke-Gate.ps1`（本步非完成 Claim；按 Mode 出回执即可）。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- §2 产出已按模板必填节落地；无空节、无未替换占位符。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:release | step=readiness | agent=delivery-lead | packet=rules/packets/release/readiness.md | global=ok | skills=acceptance-and-launch,observability-and-instrumentation|done|na | claim=ALLOWED|DENIED|na | next=…
```
