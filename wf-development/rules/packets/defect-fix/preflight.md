# 步骤卡 · defect-fix/preflight

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`defect-fix` / `preflight`（平台可用性）
- **packet**：`rules/packets/defect-fix/preflight.md`
- **角色**：`defect-fixer`（缺陷修复编排）。平台拉取 → 分类 → 红证修复或产品评估 → 门禁 → 菜单 → 按 YAML hitl 提交/部署/回写 → 发布后验证；本步只做该角色职责；越界交回或升级。
- **上游**：无（链首）
- **后续**：`pull`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：平台可用性
- **产出**：平台可用性/鉴权结果 + 降级路由（route/reason/next_action）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 读项目档案 provider。
- 若为「无」或未配置： route=workflow:change | reason=no_defect_platform | next_action=按现象走常规变更。
- 终止本 workflow（不执行 next: pull）。
- 禁止向用户索要编号、禁止空转拉平台。
- **勿在本步 `-StartTask`**。
- 有代码修复时在 `fix` 动手前冻结任务窗口。
- **开工门（硬）**：进入本 workflow 先按 `confirm_task_intent` 输出【需求与意图理解】（目标/范围/验收/不做/假设/风险）并等确认。
- 未确认不得进入 pull、不得改测试或业务代码。
- 批量入口（指派给我/我的待修）不豁免。
- 确认后 pull 首条回执须含【清单摘要】，triage 须先出【分类表】再进 fix。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 模板与证据

- **无强制模板**：§5 编排已给出动作/顺序；直接落 §2 产出。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:defect-fix | step=preflight | agent=defect-fixer | packet=rules/packets/defect-fix/preflight.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
