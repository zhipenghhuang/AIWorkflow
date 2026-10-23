# Playbook · 迭代交付（清单 → 实施 → 评审/门禁 → 提测 → 收尾）

> 只读本卡 + 当前步 YAML；`迭代交付.md` 只作参考，不要求全读。
> 当前步：`iterate.precheck / plan / confirm / implement / review / gates / deliver / wrap / release_handoff / retro`。

## 1. 读什么

| 步 | 必读 | 可选/按需 |
| --- | --- | --- |
| precheck | `iterate.yaml` + 需求基线/方案/开发计划现状 | 项目档案 §8 |
| plan | `技能/task-breakdown/SKILL.md` + 任务清单模板（L1 可用 `开发卡-轻量模板.md`） | 代码地图 scout（大仓） |
| confirm | 门表 `confirm_backlog`（仅需 approve 时） | 清单 §6 |
| implement | `技能/implementation-and-selftest/SKILL.md` + `技能/engineering-quality/SKILL.md` | 子代理编排 §2、`前端设计说明模板.md` |
| review | `技能/code-review/SKILL.md` + `技能/engineering-quality/SKILL.md` §5 + reviewer-agent | security-scan |
| gates | `验证/Invoke-Gate.ps1` + `验证/检查矩阵.yaml` | `.gate/completion.json`、日志摘要 |
| deliver | `技能/qa-handoff-and-release/SKILL.md` + 提测/发布模板 | 回滚预案 |
| wrap | `规则/模板/收尾骨架.md` | 文档治理、根 `CHANGELOG.md` |
| release_handoff | 发布就绪包 + `release.yaml` | 上线检查单 |
| retro | `技能/retrospective-and-improvement/SKILL.md` + 复盘模板 | 上次行动项对账 |

## 2. 分级与确认

- **L0 微改**：单文件、无契约/数据/权限/安全影响 → clarify→implement→verify→commit；不建清单。
- **L1 常规**：多文件但范围收敛、无跨系统契约 → 轻量清单；**清单/节奏未实质变化时 default=notify**：展示任务数/RP 覆盖/依赖/风险后继续，不强制 `confirm_backlog`。
- **L2 功能/迭代**：新功能/跨模块/接口/数据/多任务 → 全链；清单新建/范围/节奏变化 → `confirm_backlog` approve。
- **L3 高风险**：权限/资金/数据迁移/公共 API/安全合规/破坏性 → L2 + 独立评审 + 安全/隐私 + 回滚演练 + 发布审批 + 观察 + 复盘。
- 不确定按高一档；低风险不要升级为 approve。

## 3. 流程卡

1. **precheck**：读需求基线/方案/开发计划/清单现状；确认需求已签收、方案已批准（L2+）；输入含 PRD/迭代方案/原型但无理解包 → 先回 `change.analyze_input`；缺失 → 一句话说明，转 `change` 的 requirements/design 补确认。
2. **plan**：只读，不改代码；输入=已确认需求/方案 + 代码地图 + 项目档案 §8；大仓/≥5 文件可派只读 scout（返回文件/函数/调用方/测试/风险 ≤30 行）；拆完自检 RP 覆盖/AC/精确文件/依赖无环/并行冲突/L 已拆/检查点。
3. **confirm**：仅 L2+ 或范围/节奏实质变化时 approve；L1 默认 notify；「继续迭代」清单未变 → 跳过。
4. **implement**：按清单执行；完成当场回写状态/验证摘要/提交号；≥3 个可独立任务且文件集不相交才分片；默认串行；子代理不改清单/计划。
5. **review**：仅多文件/新功能/高风险/大改/点名时执行；L0 单文件跳过；核验者≠实施者；只报正确性/需求覆盖/安全/性能/范围缺口。
6. **gates**：按档案最小充分集；失败不声称完成；存量失败只对账新增；文档与实现同变更。
7. **deliver**：有 QA/部署才走；提测单/发布说明/回滚预案落 `05-发布与交付/`；先产文档再提交；无 QA 也要留自测证据。
8. **wrap**：更新清单/索引/activeContext/开发计划；有变更才 `confirm_commit`；【拟提交】只展示一次；提交后回填 hash。
9. **release_handoff**：含部署 → 转 `release.yaml`；本步不直接部署。
10. **retro**：迭代完成/事故/重大发布才走；小迭代 3～5 条；行动项有负责人/截止/验收；下次复盘先对账。

## 4. 红线

- 未完成任务清单禁止覆盖；不同工作先问；偏离暂停澄清。
- 未验证/未覆盖不得标完成；「实现完」≠「完成」。
- 高风险/大改核验者≠实施者；核验不替代门禁。
- 子代理不 git/不平台/不改清单/不改确认门；返回 ≤30 行。

## 5. 输出

任务清单/代码/验证证据/提测单/发布说明/复盘/收尾。收尾按 `规则/模板/收尾骨架.md`。
