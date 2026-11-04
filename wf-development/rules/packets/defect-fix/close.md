# 步骤包 · defect-fix/close

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`defect-fix`
- **step**：`close`（提交推送部署回写）
- **packet**：`rules/packets/defect-fix/close.md`
- **条件步** `when=implementation_required`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：提交推送部署回写
- **产出**：提交/部署/回写结果

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 按菜单精确执行（组合=并集、重复步骤只执行一次）；确认门以本步 hitl 列表为准（专规不另造门）： 含提交/推送 → confirm_commit（【拟提交】块）；含部署 → 先过就绪检查并产出/更新发布说明+回滚预案+上线检查单 （rules/templates/40-delivery/release-notes-template.md、rules/templates/40-delivery/go-live-checklist-template.md，落 {workroot}/60-release/），再 confirm_deploy（版本/窗口/影响面/回滚决策人）； 未批准不部署；含回写 → confirm_remark（ 备注全文）。 **回写就绪四条件**：①部署后冒烟/原单复核通过；②按 生成备注并带提交 hash/版本；③展示全文+状态/指派/resolvedBuild；④状态+备注同轮写入。任一未满足只写「待验证」，不得 resolved。 可与菜单同轮展示拟提交清单+备注全文+部署要点，用户一次确认后连续执行 （预授权已含本步时，展示照常、免重复等待，见 AGENTS ）。 部署失败即停、不继续回写；部署后先冒烟再回写；未验证不得写成“已修复”。 产品缺陷回写按 /，点名产品文档/评估单/对齐记录。 修复/回归完成且已写回平台 → **不**强制 `FIX` 整包；无平台/点名 → **先问后发** 自包含 FIX 包。未回执不得写“测试已回归/产品已验收”。

## 4. 本步门

- **HITL `confirm_commit`**：【拟提交】块（三包统一：文件+`.gitignore`+分支/跟踪+本次动作；本轨扩展：基线/分账/拆分/落点/CI/PR·合并）；**默认仅本地提交**，推送须单独明确并确认；≠收尾第 2 点「待提交摘要」
- **HITL `confirm_deploy`**：出示版本/窗口/影响面/回滚决策人；并核 **干净工作区 + 已提交或已打 tag + 本轮 `completion.json=COMPLETE`**；未批准不部署，禁止从脏工作区部署；**仅生产/正式环境**，test/staging 部署不触发本门；生产版本必须无 prerelease
- **HITL `confirm_remark`**：出示 §6 备注全文 + 状态/指派/resolvedBuild；确认后状态+备注同轮写入；未验证只写「待验证」

## 5. 做法

### 本步动作清单

- 按菜单精确执行（组合=并集、重复步骤只执行一次）。
- 确认门以本步 hitl 列表为准（专规不另造门）： 含提交/推送 → confirm_commit（【拟提交】块）。
- 含部署 → 先过就绪检查并产出/更新发布说明+回滚预案+上线检查单 （rules/templates/40-delivery/release-notes-template.md、rules/templates/40-delivery/go-live-checklist-template.md，落 {workroot}/60-release/），再 confirm_deploy（版本/窗口/影响面/回滚决策人）。
- 未批准不部署。
- 含回写 → confirm_remark（ 备注全文）。 **回写就绪四条件**：①部署后冒烟/原单复核通过。
- ②按 生成备注并带提交 hash/版本。
- ③展示全文+状态/指派/resolvedBuild。
- ④状态+备注同轮写入。任一未满足只写「待验证」，不得 resolved。 可与菜单同轮展示拟提交清单+备注全文+部署要点，用户一次确认后连续执行 （预授权已含本步时，展示照常、免重复等待，见 AGENTS ）。 部署失败即停、不继续回写。
- 部署后先冒烟再回写。
- 未验证不得写成“已修复”。 产品缺陷回写按 /，点名产品文档/评估单/对齐记录。 修复/回归完成且已写回平台 → **不**强制 `FIX` 整包。
- 无平台/点名 → **先问后发** 自包含 FIX 包。未回执不得写“测试已回归/产品已验收”。

## 6. 打开/填写

- 运行时正文：仅本文件（开局卡已在会话开头读过）。
- 无强制模板：直接写 §2 产出路径产物。

## 7. 完成信号

- §2 产出已落盘。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 8. 回执字段

```text
route=workflow:defect-fix | step=close | reads=rules/packets/defect-fix/close.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/defect-fix/close.md`；对不上 = 未遵守读链。
