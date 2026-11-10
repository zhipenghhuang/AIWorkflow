# 步骤卡 · defect-fix/close

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（每步先读并逐条过）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`defect-fix` / `close`（提交推送部署回写）
- **packet**：`rules/packets/defect-fix/close.md`
- **角色**：`defect-fixer`（缺陷修复编排）。平台拉取 → 分类 → 红证修复或产品评估 → 门禁 → 菜单 → 按 YAML hitl 提交/部署/回写 → 发布后验证；本步只做该角色职责；越界交回或升级。
- **前置**：gates 已 COMPLETE，或本批无代码/配置改动
- **上游**：`menu`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`postrelease`（进 `postrelease` 前的 `when=has_deployed`）
- **失败去向**：门禁未过先回 gates/fix；不得提交/部署/回写
- **条件判定 `when:implementation_required`**：非「只出任务清单」且清单已确认；满足→真，否则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：提交推送部署回写
- **产出**：提交/部署/回写结果

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：每步读 `rules/core/global-rules.md` 并逐条过；本步未读不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- **HITL `confirm_deploy`**：未批准
- **条件判定 `hitl:menu_includes_deploy`**：本轮菜单含部署；满足→真，否则跳过该门。
- **HITL `confirm_remark`**：出示 §6 备注全文 + 状态/指派/resolvedBuild；确认后状态+备注同轮写入；未验证只写「待验证」
- **条件判定 `hitl:menu_includes_writeback`**：本轮菜单含平台回写；满足→真，否则跳过该门。
- **推进**：本步完成后沿父链进入下一未跳过步；口令为单步（只出方案/只出轻量方案/只评审/代码评审/方案评审/只提测/只出清单）或动作清单写明停止/跳转时，以口令/清单为准，即停并输出收尾骨架。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 按菜单精确执行（组合=并集、重复步骤只执行一次）。
- 确认门以本步 hitl 列表为准（专规不另造门）： 含提交/推送 → confirm_commit（【拟提交】块）。
- 含部署 → 先过就绪检查并产出/更新发布说明+回滚预案+上线检查单 （rules/templates/40-delivery/release-notes-template.md、rules/templates/40-delivery/go-live-checklist-template.md，落 {workroot}/60-release/），再 confirm_deploy（版本/窗口/影响面/回滚决策人）。
- 未批准不部署。
- 含回写 → confirm_remark（ 备注全文）。
- **回写就绪四条件**：①本地复测通过且部署冒烟通过（不崩、可回归）。
- ②按 生成备注并带提交 hash/版本。
- ③展示全文+状态/指派/resolvedBuild。
- ④状态+备注同轮写入。
- 任一未满足只写「待验证」，不得 resolved。
- 可与菜单同轮展示拟提交清单+备注全文+部署要点，用户一次确认后连续执行 （预授权已含本步时，展示照常、免重复等待，见 AGENTS ）。
- 部署失败即停、不继续回写。
- 部署后先冒烟再回写。
- 未验证不得写成“已修复”。
- 产品缺陷回写按，点名产品文档/评估单/对齐记录。
- 修复/回归完成且已写回平台 → **不**强制 `FIX` 整包。
- 无平台/点名 → **先问后发** 自包含 FIX 包。
- 未回执不得写“测试已回归/产品已验收”。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/40-delivery/release-notes-template.md`；只读本步用到的节，禁止整文件通读。
- **参考模板（命中再开，不默认读）**：`rules/templates/40-delivery/go-live-checklist-template.md`。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:defect-fix | step=close | agent=defect-fixer | packet=rules/packets/defect-fix/close.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
