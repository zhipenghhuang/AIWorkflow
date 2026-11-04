# 步骤包 · solo/test

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`solo`
- **step**：`test`（轻量测试）
- **packet**：`rules/packets/solo/test.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：轻量测试
- **产出**：轻量测试报告（{workroot}/50-verification/测试报告-{主题}-{yyyyMMdd}.md）+ .gate/wf-development/completion.json

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 技能：`skills/test-design-and-execution/SKILL.md`（先读再做）；模板 `rules/templates/40-delivery/lite-test-report-template.md`；口径 `lightweight.md` ；门禁见 `verify/README.md`。 **开发自验**（非准出）：按方案卡测试点 + **AC 走查**；最小充分集=主路径 + 1 边界 + 1 异常 + 权限/数据域（适用时）+ 受影响回归；前端看状态/视口/console/network/截图；后端看响应/错误码/日志；数据变更看迁移前后与回滚路径。 先 UI 后 Network；不猜未见 API；失败留证；同一失败修复后跑「原用例 + 冒烟 + 影响面」，2 次无效换路径/升级。 失败分类：产品/实现/环境/数据/测试问题；产品范围问题停下问用户，不按现网实现改预期。 写报告：范围/环境/AC 走查/测试点/结果/证据/defects/缺口/verdict（开发自验）；P0 未过 = FAIL；禁写「已准出」。 运行 `verify/Invoke-Gate.ps1 -ProjectRoot "." -Acceptance "<方案卡路径>"`；读 `.gate/wf-development/completion.json`；非 COMPLETE 不得进 wrap 报完成。 无方案卡/验收表（如单独「轻量测试」入口）：只做诊断测试并出报告，不跑 completion-gate；wrap 写 `verification=not_applicable`。 纯文档/无代码改动：只核链接/占位/事实，不跑 completion-gate；wrap 写 `verification=not_applicable` + 依据。

## 4. 本步门

- **GATE `completion-gate` when=solo_gate_required**：任务开始 `-StartTask`；运行 `verify/Invoke-Gate.ps1 -Acceptance ...`；写 `.gate/wf-development/completion.json`；**前端套装与 capture 只认 `rules/core/frontend-gate.md`**；**写完成前 `-Claim`，只认 `CLAIM: ALLOWED`**；空 diff=`NOT_VERIFIED`、dry-run=`DRY_RUN`、缺项 → `BLOCKED`

## 5. 做法

### 技能 `test-design-and-execution`

# 轻量测试设计与执行（技能 · 随包生效）

> 用于：`solo.test`；`change.verify` / `iterate.gates` 在无 QA、且触及用户路径/业务rules/接口行为时**必用**（见 `lightweight.md` §4.1）。
> 目标：用**最小充分集**做**开发自验**——回答「这次改动能不能用」，不是堆用例数量，也不是版本准出。
> 边界：不替代完整测试包的测试计划/用例库/覆盖三闸/准出门；结论用语写「开发自验 / 可交付」，禁写「已准出」。
> 口径：`rules/core/lightweight.md` §4～§4.1；门禁与证据见 `verify/README.md`；P0 未过不得判整体通过。
> 不确定「是否要正式测 / 是否够自验」→ 推荐路径 + 一问确认，不静默跳过用户路径。

## 0. AC 走查（硬）

对照方案卡/需求基线/任务卡验收表：每条 AC → 通过 / 失败 / 未测+理由；未走查不得写 PASS。走查可与测试点表合并，但 AC ID 必须可对账。

## 1. 先建测试卡（5～10 行）

在方案卡的「测试策略」或测试报告开头写清：

| 项 | 内容 |
| --- | --- |
| 变更点 | 改了什么（文件/接口/页面/规则） |
| 影响面 | 直接受影响 + 邻接（谁调用、谁展示、谁依赖） |
| 风险 | 主链路阻断 / 数据 / 权限 / 资金 / 兼容 / 性能 / 安全 |
| P0 | 不过就不能交付的 1～5 条 |
| P1 | 重要但可带缺口交付的 |
| 测试类型 | 功能 / 边界 / 权限 / 异常 / 回归 / 兼容 / 探索式（按风险选） |
| 环境/数据 | 构建、URL、账号、测试数据、清理方式 |
| 不测 | 明确不测项 + 理由 + 接受人 |

**P0 判定**

- 主业务链走不通、数据错/丢、越权、资金错、核心页面打不开 → P0。
- 拿不准向上一档；P0 不因「实现简单」降级。

## 2. 设计最小充分集

按顺序展开，不跳：

1. **主路径**：用户从入口到结果的完整故事，至少 1 条成功。
2. **rules/状态**：合法状态迁移抽样；有状态对象至少 1 条非法跃迁。
3. **边界**：数字/长度/时间/金额/分页取 `min-1 / min / max / max+1` 的代表值。
4. **权限/数据域**：跨角色/租户至少 1 条；文档未声明时做角色冒烟，不假装已覆盖。
5. **异常/失败**：空值、重复提交、网络失败、超时、脏数据、依赖不可用。
6. **写操作**：失败或写后回查 + 清理（可并入主条）。
7. **UI/体验**：布局、遮挡、截断、空态/加载/错误提示、按钮状态、文案减法；截图同帧检查。
8. **回归**：原失败用例 + 冒烟子集 + 影响面组；稳定主链路优先脚本。

**技法速用**

- 等价类：有效/无效各取代表，不穷举同类。
- 边界值：数字、长度、时间、金额、分页都适用。
- 判定表：条件组合互斥时一格一用例。
- 状态迁移：状态 × 事件矩阵；每个非法跃迁一条负向。
- 场景法：入口 → 动作 → 观测点；主路径 + 分支变体。
- 错误推测：按历史defects/常见漏测补，不替代前五类。

**最小覆盖（与变更类型匹配）**

| 变更 | 至少覆盖 |
| --- | --- |
| 纯文案/样式 | 受影响页面 + console 无 error |
| 前端行为 | 主路径 + 1 边界 + 1 异常 + 受影响回归 |
### 编排备忘

技能：`skills/test-design-and-execution/SKILL.md`（先读再做）；模板 `rules/templates/40-delivery/lite-test-report-template.md`；口径 `lightweight.md` ；门禁见 `verify/README.md`。 **开发自验**（非准出）：按方案卡测试点 + **AC 走查**；最小充分集=主路径 + 1 边界 + 1 异常 + 权限/数据域（适用时）+ 受影响回归；前端看状态/视口/console/network/截图；后端看响应/错误码/日志；数据变更看迁移前后与回滚路径。 先 UI 后 Network；不猜未见 API；失败留证；同一失败修复后跑「原用例 + 冒烟 + 影响面」，2 次无效换路径/升级。 失败分类：产品/实现/环境/数据/测试问题；产品范围问题停下问用户，不按现网实现改预期。 写报告：范围/环境/AC 走查/测试点/结果/证据/defects/缺口/verdict（开发自验）；P0 未过 = FAIL；禁写「已准出」。 运行 `verify/Invoke-Gate.ps1 -ProjectRoot "." -Acceptance "<方案卡路径>"`；读 `.gate/wf-development/completion.json`；非 COMPLETE 不得进 wrap 报完成。 无方案卡/验收表（如单独「轻量测试」入口）：只做诊断测试并出报告，不跑 completion-gate；wrap 写 `verification=not_applicable`。 纯文档/无代码改动：只核链接/占位/事实，不跑 completion-gate；wrap 写 `verification=not_applicable` + 依据。

## 6. 打开/填写

- 运行时正文：仅本文件（开局卡已在会话开头读过）。
- 验证：`verify/Invoke-Gate.ps1`（完成声称加 `-Claim`）；有 UI 另按包内前端条。

## 7. 完成信号

- §2 产出已落盘。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 8. 回执字段

```text
route=workflow:solo | step=test | reads=rules/packets/solo/test.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/solo/test.md`；对不上 = 未遵守读链。
