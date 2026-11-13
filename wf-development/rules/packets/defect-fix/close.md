# 步骤卡 · defect-fix/close

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`defect-fix` / `close`（提交推送部署回写）
- **packet**：`rules/packets/defect-fix/close.md`
- **角色**：`defect-fixer`（缺陷修复编排）。平台拉取 → 分类 → 红证修复或产品评估 → 门禁 → 菜单 → 按 YAML hitl 提交/部署/回写 → 发布后验证；本步只做该角色职责；越界交回或升级。
- **前置**：gates 已 COMPLETE，或 skip_claim 且本地验证摘要已落，或本批无代码/配置改动
- **上游**：`menu`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`postrelease`（进 `postrelease` 前的 `when=has_deployed`）
- **失败去向**：门禁未过且未获 skip_claim → 先回 gates/fix；不得提交/部署/回写
- **条件判定 `when:implementation_required`**：非「只出任务清单」且清单已确认；满足→真，否则跳过本步（不打开本包）。

## 2. 本步目标

- **目标**：提交推送部署回写
- **产出**：提交/部署/回写结果

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_commit`**：【拟提交】块（三包统一：文件+`.gitignore`+分支/跟踪+本次动作；本轨扩展：基线/分账/拆分/落点/CI/PR·合并）；**默认仅本地提交**，推送须单独明确并确认；≠收尾第 2 点「待提交摘要」
- **条件判定 `hitl:menu_includes_commit`**：本轮菜单含提交；满足→真，否则跳过该门。
- **HITL `confirm_deploy`**：未批准
- **条件判定 `hitl:menu_includes_deploy`**：本轮菜单含部署；满足→真，否则跳过该门。
- **HITL `confirm_remark`**：出示 §6 备注全文 + 状态/指派/resolvedBuild；确认后状态+备注同轮写入；未验证只写「待验证」
- **条件判定 `hitl:menu_includes_writeback`**：本轮菜单含平台回写；满足→真，否则跳过该门。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 按菜单精确执行。
- hitl 只认本步列表。
- 回写就绪见 fix-collaboration §4.5（含自部署/skip_claim）。
- 含部署须发布说明+回滚+confirm_deploy。
- 未验证不得 resolved。
- 产品缺陷回写按 §5.3/§6.2/§6.3。
- 不强制 FIX 整包。

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
route=workflow:defect-fix | step=close | agent=defect-fixer | packet=rules/packets/defect-fix/close.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
