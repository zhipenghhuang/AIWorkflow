# 步骤卡 · defect-fix/align

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（本会话已读则不重读全文）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`defect-fix` / `align`（文档对齐）
- **packet**：`rules/packets/defect-fix/align.md`
- **角色**：`defect-fixer`（缺陷修复编排）。平台拉取 → 分类 → 红证修复或产品评估 → 门禁 → 菜单 → 按 YAML hitl 提交/部署/回写 → 发布后验证；本步只做该角色职责；越界交回或升级。
- **上游**：`product_decision`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`fix`（进 `fix` 前的 `when=implementation_required`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:product_decision_requires_alignment`**：产品结论需再对齐范围/方案；满足→真，否则跳过本步（不打开本包）。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：文档对齐
- **产出**：对齐记录（受影响文档/计划清单）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：本会话已读 `rules/core/global-rules.md` 则不重读全文；未读过不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。
- **推进**：本步完成后沿父链进入下一未跳过步；口令为单步（只出方案/只评审/代码评审/方案评审/只提测/只出清单/轻量方案）或动作清单写明停止/跳转时，以口令/清单为准，即停并输出收尾骨架。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 仅产品回复且需实施（认可/修改后认可/改判实现）时执行。
- 非问题/补充信息跳过，转 clarify。
- 按 缺陷：先红证/根因。
- 不修表象。
- 回写带证据： ≥3 份新产品文档 → 只读抽取扇出（每份返回变更点/AC/影响面候选 ≤30 行）。
- 对齐结论由本步集中写，不并行改同一文档。
- 产品新文档按 文档治理（工作根/原件根/索引/关版整夹） （T6）：确认后原件落 `inbound/{ver|topic}/`，登记索引。
- S1/S2/S3 同批进 `inbound/_archive/`。
- 结论同步工作区。
- 构成需求/范围/AC/接口/数据实质变更 → 按 `intake` 流程 与 变更/提交（本步门 + 共享 closeout） 做影响分析/CR。
- 逐项对照评估单/原方案，列一致/差异/新增/删除。
- 更新 {workroot}/10-requirements/需求台账、{workroot}/20-design/方案-…/ADR/接口/DB、{workroot}/40-tasks/任务清单、 {workroot}/50-verification/UAT、{workroot}/60-release/提测单/发布说明/回滚、开发计划、 项目档案（新入口/命令/规范变化）、{workroot}/00-governance/变更记录（CR）、`{workroot}/INDEX.md`、`activeContext`。
- 不适用写原因。
- 未对齐不得 fix。

### 本步规则卡：文档治理

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认后将迭代绑定文档迁入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`；主档关闭时快照、主档不移动；「并行不关」只落新资料、不归档现行主档。
- 清理只删已知临时/缓存/未引用失败产物；不确定移 `_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。

### 本步规则卡：变更与提交

- 变更/影响：先判事实与影响面；实质变更走 intake/CR，不静默改基线。
- 提交：默认仅本地提交；推送单独确认；禁 force push/切主干/擅自开 PR。
- 无文件变更 → 不硬造提交。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 模板与证据

- **无强制模板**：§5 规则卡已给出输出形状；直接落 §2 产出。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:defect-fix | step=align | agent=defect-fixer | packet=rules/packets/defect-fix/align.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
