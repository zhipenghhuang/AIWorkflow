# 迭代交付

> **真值分层**：步骤/门 = `workflows/iterate.yaml`；主流程/分级 = `skills/development-plan/SKILL.md`；本文 = **口令 / DoR / DoD / 输出骨架**（不另写第二套步骤表）。角色见 `agents/iterate-lead.yaml`。  
> 确认门只认步上 `hitl`（标量用 `hitl_when`）。  
> 拆单方法：`skills/task-breakdown/SKILL.md`；模板：`rules/templates/30-planning-tasks/task-list-template.md`；发布/验收：`skills/acceptance-and-launch/SKILL.md`；复盘：`skills/retrospective-and-improvement/SKILL.md`。

## 1. 口令

| 形态 | 范围 |
| --- | --- |
| 按方案实施 {路径} / 落地迭代方案 {名} | 清单→实施→验证→文档→总结→（含部署）发布交接 |
| …只出任务清单 | 仅清单（`iterate.yaml` precheck→plan→closeout；跳过 confirm/实施/门禁/deliver；清单文件有变更时按 closeout 的 `confirm_commit`） |
| 继续迭代 {版本/主题} | 读清单续跑；清单与节奏未变则跳过 `confirm_backlog` |
| 迭代复盘 / 版本复盘 | 转 `workflows/retro.yaml` |

路径歧义 → 一问。无 `#` 的「落地…优化方案」且无「迭代」字样 → 一问缺陷或迭代。

## 2. 前置（DoR / DoD）

- 档案关键项已填；需求基线/方案已确认（L2+；无则先补，不凭聊天记忆）。
- L2+ 《开发计划》已建/已读；无则按 `skills/development-plan/SKILL.md` 创建或提示缺口（不强制引用其它包）。
- 任务清单未建 → 先按 `skills/task-breakdown/SKILL.md` 拆；旧清单未完成 → 先问是否续跑/替换，**禁覆盖**。
- **DoR**：需求/AC 明确、依赖就绪、环境/数据可用、方案/接口已确认、任务可独立验证。
- **DoD**：AC 满足、测试通过、评审通过（如触发）、三维影响已说明、文档同步、证据留存、可回滚；项目级 DoD 见档案 §8。

## 3. 主流程指针

顺序与确认门以 `workflows/iterate.yaml` 为准；分级方法见 `skills/development-plan/SKILL.md`。本文不复述步骤表。

## 4. 任务清单

位置：`{workroot}/40-tasks/任务清单-{ver}.md`；模板 `rules/templates/30-planning-tasks/task-list-template.md`。  
字段：ID/阶段/任务/要求点（RP）/优先级/风险/依赖/并行/负责人/预估/状态；任务卡含 AC、精确文件/接口、三维影响、测试先行、验证命令、回滚/开关、DoD、状态记录。  
规则：

- 每任务尽量**可独立验收**；有依赖标先后（供端先于消费端）；L 任务必须拆。  
- 每个 RP 至少一个任务；每个任务至少一个 RP；RP 可核对且全覆盖才开工。  
- 完成当场回写状态/验证摘要/提交号；阻塞/中断记原因；RP 未覆盖不得标完成。  
- 状态：未开始/进行中/阻塞/待验收/完成/取消；“实现完”≠“完成”，需验收/DoD。  
- 确认后冻结；新增/删除/拆分/调序 → 记任务清单 §6 变更记录；**禁覆盖未完成任务清单**。

## 5. 输出骨架

排版：`- ` 列表、子项两格缩进，整块可复制。

```text
【迭代交付总结】{时间} | {版本/主题} | 任务{N}：完成{A}/未完成{B} | 要求点{M}：已实现{C}/偏离{D}

# {任务号} {标题}
结论：{一句}
要求点：{RP}
修改文件：{模块/类名}
验证：{命令+结果}
提交状态：{待提交|不提交|已提交 hash}
文档同步：{路径或「无」}
发布交接：{提测单/发布说明/上线检查单路径，或「无」}
现场状态：{…}
确认后按指令执行。
```

```text
【{项目名称} 迭代交付汇报】{日期} | {版本/主题} | {N} 项
- #{任务号} {标题}
  - 交付内容：{一句}
  - 验证：{业务语言}；提交 {hash}
  - 发布：{未发布/已发布版本/回滚}
```

提交信息与粒度见 `rules/workflow.md` §2；文档落位/归档见 rules/workflow.md §5。  
本节的【迭代交付总结】置入【任务收尾】「完成了什么」短段，并单列「影响：」；「汇报：」须用 `rules/templates/90-handoff/closeout-skeleton.md` §1 **结论说明体**（导语加粗、正文一段）。若需对外粘贴【迭代交付汇报】清单，可附于第 1 点但不得替代「汇报」段、不得在汇报下另起工程子 bullet；第 2～6 点按收尾骨架 §2。

## 6. 复盘与改进

- 迭代完成、发布回滚、事故、重复缺陷 → `retro` 工作流（`skills/retrospective-and-improvement/SKILL.md`；模板 `retro-template.md`）。  
- 轻量复盘至少：做得好/待改进/行动项（负责人+截止+验收）。  
- 行动项进任务清单或 `{workroot}/80-retrospectives/改进项.md`；下次复盘先对账。
