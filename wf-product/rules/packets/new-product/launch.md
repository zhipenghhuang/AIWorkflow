# 步骤卡 · new-product/launch

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（本会话已读则不重读全文）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`new-product` / `launch`（上市与复盘）
- **packet**：`rules/packets/new-product/launch.md`
- **角色**：`pm-lead`（交付编排与变更处置（排期/跟进/受理/变更/缺陷平台/UAT/发布/复盘/展示））。统一受理需求与问题 → 分诊定性 → 影响评估 → 处置确认 → 联动更新 → 验证关闭；平台缺陷可拉取、分析并回写；本步只做该角色职责；越界交回或升级。
- **上游**：`deliver`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`closeout`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:go_decision_go`**：立项结论=Go（Hold/Kill=false）；满足→真，否则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：上市与复盘
- **产出**：发布决策 + GTM 检查 + 复盘（{workroot}/{ver}/40-delivery/、90-retrospectives/）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：本会话已读 `rules/core/global-rules.md` 则不重读全文；未读过不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_release`**：出示 UAT 结论、回滚预案、公告/客服/监控就绪；未过不发布；已发布仅复盘不重复确认
- **GATE `uat-evidence` when=has_uat**：运行 `verify/Invoke-Gate.ps1 -Mode uat`；AC 覆盖、证据、有条件通过的责任人/接受人；未 READY 不得写 UAT 通过。无 UAT 要求可写 `verdict: 不适用` + 依据/批准人，门放行但记警告
- **条件判定 `gate:has_uat`**：本轮有 UAT/验收要求（发布门必须核）；满足→真，否则跳过该闸（步骤不跳过）。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 前置：UAT 通过（带条件须已接受）+ GTM 就绪（模板 `rules/templates/40-delivery/gtm-template.md`：定价 渠道 物料 销售客服）+ 发布检查（回滚 公告 客服 监控）。
- confirm_release：出示上市要点请确认。
- **未过 UAT 不发布**。
- 发布后：指标监控 → 复盘（模板 `rules/templates/60-retro/retro-template.md`）→ 改进项回需求池。
- 更新 `{workroot}/product-plan.md`。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/40-delivery/gtm-template.md`；只读本步用到的节，禁止整文件通读。
- **参考模板（命中再开，不默认读）**：`rules/templates/60-retro/retro-template.md`。
- 验证命令：`verify/Invoke-Gate.ps1`（完成须 `-Claim` → `CLAIM: ALLOWED`）。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步完成 Claim 门：须 `CLAIM: ALLOWED` 后才可写完成态。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:new-product | step=launch | agent=pm-lead | packet=rules/packets/new-product/launch.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
