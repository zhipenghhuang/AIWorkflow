# Playbook · 交付与发布（排期 → 跟进 → UAT → 发布 → 复盘）

> 只读本卡 + 当前步 YAML；UAT/复盘技能按步读。
> 当前步：`deliver.schedule / followup / uat / release`。

## 1. 读什么

| 步 | 必读 | 可选/按需 |
| --- | --- | --- |
| schedule | `deliver.yaml` + `技能/change-management/SKILL.md`（排期纪律）+ 交付计划模板 | PRD `status: APPROVED` |
| followup | 交付计划 + 受理模板 | 变更单 |
| uat | `技能/uat-and-retrospective/SKILL.md` + UAT 模板 | 测试报告/提测单（可选） |
| release | UAT 记录 + 复盘模板 + 门表 `confirm_release` | GTM/发布检查 |

## 2. 流程卡

1. **schedule**：前置 PRD APPROVED；拆 Epic→Story→Task → 交付计划。默认交计划正文；`PLAN` 包按需先问后发。
2. **followup**：跟进进度/风险/依赖；答疑书面留痕；新需求/变更/缺陷/不确定 → 转 `change.yaml`，不直接改 PRD/排期。收到开发/测试交接包先 `handoff.receive` 核对+回执。
3. **uat**：按 PRD 验收对照；有 TEST 包则签收，否则读测试报告；默认交 UAT 记录；`UAT` 包按需。
4. **release**：`confirm_release`；默认交发布决策；`REL` 包按需；有开发发布包则 receive。
5. **复盘**：改进项回需求池；`RETRO` 包按需。

## 3. 红线

- 未定稿不排期；未过 UAT 不发布；带条件通过必须列遗留/责任人/接受人。
- 发布必须定义成功指标与埋点；无指标写「不适用+原因」。
- 不执行部署；不替开发做工程审批。
- 版本关闭归档/清理先确认；证据/当前计划/源文件永不自动删除。

## 4. 输出

交付计划 / UAT 记录 / 发布检查 / 复盘 / 回归需求池。收尾按 `规则/模板/90-交接与收尾/收尾骨架.md`。
