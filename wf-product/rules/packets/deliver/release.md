# 步骤包 · deliver/release

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：产品
- **workflow**：`deliver`
- **step**：`release`（发布与复盘）
- **packet**：`rules/packets/deliver/release.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/deliver/_chain.md`（进 workflow 一次）。
- **子状态机**：`rules/packets/deliver/_region-ship.md`（验收发布；进本区一次）。

## 2. 本步目标

- **目标**：发布与复盘
- **产出**：发布决策 + 发布记录 + 复盘（{workroot}/{ver}/40-delivery/、90-retrospectives/）

## 3. 本步硬约束

### 开局硬约束（本步可执行摘要）

- 1. **先意图、再动作**（`confirm_task_intent`）：未确认禁写正式 PRD/外发/定范围。
- 2. **短读跟随 + 一手源**：`activeContext` + 进行中（`packet=`/`region=`）+ 偏好/洞见/坑 ≤3。
- 3. **理解→方案双确认未完成 → 不得入池/写正式 PRD/定版本范围**。
- 4. **状态机读链 + 技能闭环**：见本包「本步读链与防丢失」。必开 skill 须打开→执行→回步骤包（质量不降）。
- 5. **完成分层**：`-Claim -Mode <…>` → 只认 `CLAIM: ALLOWED`。
- 6. **原型硬门**：实走 + 覆盖矩阵；缺行不得过。
- 7. **禁臆造**；AC 可观测；变更无单不实施；UAT 未过不发布。
- 8. **切步/出子机 → 心跳**，必带 `packet=`。

### 本步读链与防丢失

- **编排**：本文 §5 +（若 §7 列出）一个模板。
- **方法质量**：§6 必开/条件开技能 → **打开→执行→回本包**（同时 1 个 skill）；禁止用粘贴代替实读。
- **禁止**：通读 rules / 多 step packet / 预读本 workflow 全部 skill。
- **完成声称**：有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **上下文锚**：`packet=`/`reads=` 必须含本 packet；切步/出子机前心跳刷新。


## 4. 本步门

- **HITL `confirm_release`**：出示 UAT 结论、回滚预案、公告/客服/监控就绪；未过不发布；已发布仅复盘不重复确认
- **GATE `uat-evidence` when=has_uat**：运行 `verify/Invoke-Gate.ps1 -Mode uat`；AC 覆盖、证据、有条件通过的责任人/接受人；未 READY 不得写 UAT 通过。无 UAT 要求可写 `verdict: 不适用` + 依据/批准人，门放行但记警告

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`uat-and-retrospective` → 见 §6 闭环。

### 本步动作清单

- 技能：`skills/uat-and-retrospective/SKILL.md`（先读再核）。 前置：UAT 通过（带条件须已接受）。
- 发布就绪：回滚预案/公告/客服话术/监控指标（并入 UAT 记录「发布前置」节）。 直接入口「发布」时：`has_uat=true` → 必须先运行 `verify/Invoke-Gate.ps1 -Mode uat`（读 `.gate/wf-product/uat.json`），未 READY 不得进入 confirm_release。
- 无 UAT 要求 → 写「不适用+依据」，门条件不满足则跳过，不得伪造回执。 发布前可派 verifier-agent 只读核对发布就绪证据（UAT/回滚/公告/监控），返回缺口 ≤30 行。
- 发布决策仍由本步做。 confirm_release：出示发布要点（版本/时间窗/回滚/通知范围）请确认。
- **未过 UAT 不发布**。
- 已发布且仅做复盘 → 条件不满足，跳过本门。本门是业务发布决策。
- **如启用开发轨**，工程部署由其 `release` 执行（`confirm_deploy`），不重复审批。
- 未启用则由用户安排，本包不执行部署。 发布决策后默认交发布决策正文。
- `REL` 包按需先问后发。收到开发发布结果 → 有包则 receive。 发布后：数据监控（指标/埋点）→ 复盘（模板 `rules/templates/60-retro/retro-template.md`，落 `{workroot}/{ver}/90-retrospectives/复盘-{ver}.md`：目标 vs 实际/根因/改进项→回需求池）。
- 如启用开发轨，研发复盘可由其补充，产品复盘合并引用。
- 未启用则本包独立复盘。 更新 `{workroot}/work-log.md`（仅本文件）：按场景追加里程碑——有发布决策写事件=`发布决策`（结论宜含本版对外变化摘要 1～5 条产品语言或链到发布说明，供开发写根 CHANGELOG）。
- 有 UAT 结论写=`UAT 结论`。
- 有复盘写=`复盘`。无文件则按模板建。 **不是**根 `CHANGELOG.md`、也不是计划 执行日志。本门=`confirm_release` 业务决策。
- 根发版史由开发在工程发版时写（有开发包时）。 **禁止**创建/修改/补链项目根 `CHANGELOG.md`。
- 无开发包则不建根。 版本关闭/结项：按 `rules/doc-governance.md`。
- 先判 T1/T2/T4，T2/T4 保留仍被引用的 PRD/原型基线，不整夹归档。
- 失效资料 → `inbound/_archive/` + 清单。
- 部分/增量/参考不归档。
- 未确认不移动。 同步按 `rules/doc-governance.md` ～（仅本步关版本/结项时，非日常收尾）：先判 T1/T2/T4，T2/T4 保留仍被引用的 PRD/原型基线。
- 长期主档就地更新、版本绑定目录归档、已完结临时/失败/重复列清理候选。
- 确认后执行。

## 6. 技能指向（打开 → 执行 → 回本包）

> **技能闭环（硬）**：打开 → 只读必做区并执行 → **回到本步骤包**继续门/产出/完成信号。  
> 同时只打开 **1** 个 skill；打开期间 `reads=` 可暂加该 skill 路径，闭环结束后以本 packet 为准。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `uat-and-retrospective` | **必开** | 进入本步即开（质量不降） | `skills/uat-and-retrospective/SKILL.md` | 必做区 → 回本包 |

- 必开未打开 / 未按必做执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/deliver/_chain.md`。
- 子状态机（进区一次）：`rules/packets/deliver/_region-ship.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 验证：`verify/Invoke-Gate.ps1`（完成声称加 `-Claim`）；有 UI 另按 §5 前端硬门。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:deliver | step=release | packet=rules/packets/deliver/release.md | reads=rules/packets/deliver/release.md[+skill] | skills=uat-and-retrospective|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/deliver/release.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
