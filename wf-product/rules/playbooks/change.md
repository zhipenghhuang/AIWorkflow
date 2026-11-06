> **维护素材**：运行时默认不读；方法与硬约束以 `rules/packets/<workflow>/<step>.md` 为准。

# Playbook · 需求/问题受理与变更（含 P0～P3 分级）

> 只读本卡 + 当前步 YAML；细节按指针读，**不要通读 `workflow.md` 全本**。
> 当前步：`change.intake / triage / new_requirement / assess / decide / apply / review / verify`。

## 1. 执行路径（先判，决定走多深；不选级别）

| 路径 | 触发 | 必走 | 可省 | 产物 |
| --- | --- | --- | --- | --- |
| 轻量受理 | 纯文案/配置，无 AC/范围变化 | intake→triage→apply→verify | 全量 PRD/独立评审/计划门 | 受理单/变更记录 |
| 标准产品 | AC/范围/状态/权限变化，或计划内小需求 | intake→triage→理解双确认→PRD→评审→apply→verify | 独立评审（P1 普通可作者自检；P1↑/P2+ 不可省）；PRD 可轻量，门不降 | PRD/变更单/评审/UAT |
| 新版本/0→1 | 新产品/新版本/战略 | `new-product` + `plan` + PRD + 原型/交付 | 无 | 全量 |
| 高风险 | 权限/资金/数据/合规/不可逆 | 标准产品 + 专项/独立评审/发布门 | 无 | 全量 + 专项 |

不选级别；不确定按全量；AC/范围变化不得用 P0/P1 绕过；高风险/不可逆/跨包再高一档。

## 2. 读什么

| 步 | 必读 | 可选/按需 |
| --- | --- | --- |
| intake | `change.yaml` + `skills/change-management/SKILL.md` §1 + 受理模板 | 文档治理 §3（新资料） |
| triage | 技能 §2 | 缺陷平台协作 §2.2（平台来源） |
| new_requirement | 技能 §4 + 需求池 | 产品计划 §2 |
| assess | 技能 §3 + 受理模板 §4 | 变更单模板（已定稿基线） |
| decide | 技能 §4 + 门表 `confirm_change`/`confirm_plan` | 变更单模板 |
| apply | 技能 §5 + 受理模板 §6 | PRD/原型/UAT/GTM |
| review | `reviewer-agent` + `skills/review-and-finalize/SKILL.md` | 评审模板 |
| verify | 受理模板 §7 | 回归/UAT 证据 |

## 3. 流程卡

1. **intake**：对话/文档/缺陷单/测试报告均可；澄清**按 `rules/core/clarification.md` 执行**（技能 `customer-needs-discovery`）；**未双确认不得**分诊。抽取提出人/来源/日期、原文、期望、关联 PRD/AC、版本/环境/证据、时间要求。未知标「待确认/假设」。去重合并，生成 RQ/CR/BUG 编号。新资料按文档治理 §3 输出候选，确认后才落位。
2. **triage**：判定树分类（新需求/变更/答疑/产品缺陷/实现defects/技术不确定/重复/无效）。产品缺陷必须有 PRD/设计原文 + 现网/测试证据 + 相符证明；无依据按实现defects/待确认。结论写受理单，不在此实施。
3. **new_requirement**（条件）：入需求池 R-xx，价值/成本/风险/优先级/版本/状态；仅跨版本/高价值/点名立项才 `confirm_scope`，小需求直接进 PRD/变更。
4. **assess**（条件）：评需求/AC、成本/排期、技术/测试风险、数据/合规/权限、回滚、依赖；列受影响产物。按 `rules/collaboration/handoff.md` §6 判 C0～C3；改动已定稿基线 → 必须产生变更单。跨角色影响 → 准备 `CHG` 交接包（影响矩阵/更新文档/截止）。
5. **decide**：出示分诊依据/影响/处置选项/变更单要点；`confirm_change` 后才实施；影响版本范围/里程碑/KPI 叠加 `confirm_plan`。纯答疑可跳过。
6. **apply**：按受理单 §6 逐项更新；变更单与受理单互链。默认交变更单正文；`CHG` 包按需先问后发。
7. **review**（条件）：实质变更（范围/AC/状态机/权限/数据rules/NFR/版本目标）才重审；只报缺口；通过才恢复 `APPROVED`。
8. **verify**：影响 AC/UAT/发布 → 受影响项重验；未 UAT/未发布 → 测试/回归/冒烟证据；未验证不关闭。退回开发 → 回执后关闭受理单，不写「已修复」。关单与回执：正式签收/C2·C3/发布相关 → 须回执；仅通知/同仓直读/用户代收 → 台账「已发送」+用户确认即可关闭。未回执不得称「已接收/已交接完成」。

## 4. 红线

- 无变更单不实施变更；口头变更先落单。
- 未完成客户需求理解确认不得写 PRD/排期；客户说法不等于需求，单个客户/竞品/领导偏好不得直接当市场结论。
- 产品缺陷无相符证明不得判；实现缺陷不改 PRD。
- 联动清单未闭合不得关闭；未验证不得关闭。
- 纯文案/配置可轻量；AC/范围变化不得用 P0/P1 绕过全量 PRD，证据、回执、联动清单不可省。

## 5. 输出

受理单 + 变更单（如适用）+ 最新 PRD/AC/计划/UAT + 开发/测试回执 + 联动清单。收尾按 `rules/templates/90-handoff/closeout-skeleton.md`。
