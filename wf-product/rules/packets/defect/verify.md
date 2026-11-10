# 步骤卡 · defect/verify

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（每步先读并逐条过）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`defect` / `verify`（验证与关闭）
- **packet**：`rules/packets/defect/verify.md`
- **角色**：`pm-lead`（交付编排与变更处置（排期/跟进/受理/变更/缺陷平台/UAT/发布/复盘/展示））。统一受理需求与问题 → 分诊定性 → 影响评估 → 处置确认 → 联动更新 → 验证关闭；平台缺陷可拉取、分析并回写；本步只做该角色职责；越界交回或升级。
- **上游**：`writeback`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`closeout`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:needs_linked_update`**：需联动回写与回执（除纯答疑外均为真）；满足→真，否则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：验证与关闭
- **产出**：验证结果 + 批末总结

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：每步读 `rules/core/global-rules.md` 并逐条过；本步未读不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **GATE `change-closure`**：运行 `verify/Invoke-Gate.ps1 -Mode change`；§6 每项“已更新/不适用/待补”，待补有责任人/截止；未闭合不得关闭
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- **单一出处**：通用联动/关闭规则以 `change.verify` 为准。
- 本步只保留缺陷平台差异。
- 运行 `verify/Invoke-Gate.ps1 -Mode change`（读 `.gate/wf-product/change.json`）。
- 受理单联动清单未闭合、验证结果缺失 → 不得关闭。
- 未 READY → **保持受理单打开，不得进入 closeout 冒充完成**。
- 先补联动/证据或报阻塞。
- 按 先红证/根因。
- 不修表象。
- 回写带证据 + `rules/templates/30-review-change/defect-writeup-template.md`： 产品缺陷 → 受影响 AC/UAT 重验。
- 开发完成新文档实施后验证。
- 未验证不关单。
- 实现缺陷 → 产品侧回执后由开发/测试流程跟踪。
- 产品侧不写「已修复」。
- 非问题/重复/信息不足 → 产品给依据。
- 测试接受后关闭或转需求。
- 未接受转产品复核。
- 下版 → 回池/路线图。
- 不修 → 理由/接受人。
- 退回开发 → 回执，缺陷状态由开发/测试跟踪。
- 验证通过后需再次回写平台（入口 writeback）更新状态/关闭。
- 批末输出【产品缺陷协作总结】。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/30-review-change/defect-writeup-template.md`；只读本步用到的节，禁止整文件通读。
- 验证命令：`verify/Invoke-Gate.ps1`（完成须 `-Claim` → `CLAIM: ALLOWED`）。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步完成 Claim 门：须 `CLAIM: ALLOWED` 后才可写完成态。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:defect | step=verify | agent=pm-lead | packet=rules/packets/defect/verify.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
