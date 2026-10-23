# Playbook · 发布与上线（就绪 → 验收 → 审批 → 部署 → 验证/回滚 → 观察）

> 只读本卡 + 当前步 YAML；按需读 `acceptance-and-launch` / `qa-handoff-and-release` 技能。
> 当前步：`release.readiness / acceptance / approval / deploy / verify / rollback / postrelease / record / retro`。

## 1. 读什么

| 步 | 必读 | 可选/按需 |
| --- | --- | --- |
| readiness | `release.yaml` + 上线检查单模板 + 技能 `qa-handoff-and-release` | 开发计划/提测单 |
| acceptance | 技能 `acceptance-and-launch` + UAT 模板 | 测试报告/需求基线 |
| approval | 门表 `confirm_deploy` + 上线检查单 | 风险/回滚决策人 |
| deploy | 项目档案 §8 发布方式/命令 + 发布说明 | 配置/数据快照 |
| verify | 发布说明「线上验证要点」+ 基线 | 监控/日志面板 |
| rollback | 发布说明回滚步骤 + 门表 `confirm_rollback` | 数据影响/时长 |
| postrelease | 发布记录模板 + 监控/告警 | 观察期指标 |
| record | 发布说明/发布记录模板 | 文档索引、根 `CHANGELOG.md` |
| retro | 复盘模板 + 技能 `retrospective-and-improvement` | 上次行动项 |

## 2. 流程卡

1. **readiness**：按上线检查单逐项核：需求/AC、提测/构建、评审、测试/准出、UAT、安全/依赖/密钥、配置/迁移、回滚、监控/告警/值班、通知、变更审批。任一硬项不过 → NO-GO；例外写风险/补偿/批准人。输出 `release_ready=GO/NO-GO`。
2. **acceptance**（条件）：有业务验收才走；对照需求/PRD AC + 测试报告 + 提测单；结论=通过/有条件/不通过；`confirm_acceptance` 后进审批；未签收不得审批。
3. **approval**：基于检查单 + UAT + 测试 + 风险/回滚；出示版本/窗口/影响面/回滚决策人；`confirm_deploy` 后部署；有条件批准列条件与监控；发布内容/窗口变更重新确认。若业务发布决策已由产品/用户完成，本门只确认工程侧。
4. **deploy**：按档案发布方式/命令；部署前记录版本/构建/配置/数据快照/健康基线；按发布说明逐步执行；失败即停，按回滚预案；部署后先主链路冒烟，再关键回归，不先全量。
5. **verify**：按发布说明「线上验证要点」逐条核；对照发布前基线看错误率/延迟/吞吐/业务指标；异常分级可观察/需修复/需回滚；触发回滚立即转 rollback。
6. **rollback**（条件）：部署失败/验证失败/触发回滚条件才走；`confirm_rollback` 后执行；回滚后复跑冒烟/关键回归；记录时间线/影响/证据；不掩盖失败。
7. **postrelease**：观察日志/指标/告警/关键业务；结论=成功/带风险成功/回滚；遗留进 `06-复盘与改进/`。
8. **record**：汇总版本/构建、内容、步骤、验证、观察、遗留、回滚；更新发布说明/发布记录/根 `CHANGELOG.md`/索引/activeContext/开发计划。
9. **retro**（条件）：事故/回滚/重大发布才走；行动项有负责人/截止/验收。

## 3. 红线

- 未过上线检查/审批不得部署；验证失败按预案回滚，不恋战。
- 禁把测试环境证据当生产证据；禁对外发布未经确认的话术。
- 部署失败即停；未验证不写「已修复/已发布成功」。
- 密钥零入库；发布记录不夹带敏感信息。

## 4. 输出

上线检查单/审批记录/部署记录/发布验证/发布记录/复盘。收尾按 `规则/模板/收尾骨架.md`。
