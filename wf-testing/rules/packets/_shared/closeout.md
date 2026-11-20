# 收尾与提交 · 共享终端（测试）

> **全局规则**：开始本步前读 `rules/core/global-rules.md`；首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。
> 适用：本包所有 workflow 的 `closeout` 终端状态。状态真值=`activeContext.md` 本包运行状态；本步完成后置 `done`。
> 本文件是唯一收尾步；各链不再单独生成 closeout 步骤包。

## 1. 进入条件

- 本链最后一个 domain 步骤的产出已落盘；`report-consistency` 已 PASS/CONDITIONAL（或明确不适用）；完成表述另须 `-Claim` → `CLAIM: ALLOWED`。
- 没有未闭环阻塞；有则先写 `blocked`。
- 缺陷提交/平台回写若是本链 domain 动作，已完成或明确不适用；本步只做最终提交确认。

## 2. 收尾六点（标题与子字段以 `rules/templates/90-handoff/closeout-skeleton.md` §1 为准）

1. 完成了什么：短段 +「影响：」。
2. 改了哪些文件：文件：/未提交：/建议动作：/待提交摘要：/git：/.gitignore：/文档归档：。
3. 如何验证：命令/结果/门回执；未验证项写「未验证：」。
4. 假设与未决项（待你确认）：假设：/待你确认：/默认（不回复即执行）：/回复：/可转发产品：；有决策项按 事项/选项/建议/影响默认 四行。
5. 还存在什么问题或风险：风险、阻塞、责任人、恢复条件。
6. 当前进度与下一步：当前：；下一步：1）…（执行：/产出：/完成标志：）+ 优先级：/建议：/不建议：。

> 另写「附：运行与沉淀」：资料补强：/工作记忆：/运行态：。只写现行结论；缺项=未收尾。【遵守自检】字段只认 `rules/core/execution-contract.md` §6。
> 发出前自检：头块分行（【任务收尾】【验证回执】【遵守自检】）→ 汇报独立 → 六点齐 → 附齐 → `python <包>/verify/tools/check_compliance.py --report <收尾文件>`。

## 3. 状态与同步

- `activeContext.md` 本包运行状态：`workflow/state=closeout/status=done|blocked|cancelled`、`packet: `rules/packets/_shared/closeout.md``、`gate=<回执或 na>`、`next=`。
- 本轮若改被测版本或焦点：同轮改 `activeContext` 命中句（禁只改进行中表）。本包不写根 CHANGELOG。
- 阶段/门/焦点变化才更新 `{workroot}/{ver}/test-plan.md` §0/§6；仅新增/改名/归档文件才更新 `{workroot}/INDEX.md`。
- 有对外门面变化时在收尾第 6 点说明一句。

## 4. 缺陷提交门（`confirm_platform`）

- 本链有拟交平台/统一导出的缺陷时：出示拟提交表（`caseId｜标题｜类型｜surface｜十段｜附件`）并抽一单正文，确认后执行；未确认不得交平台。
- 无拟提交缺陷或已有平台回写 → 跳过本门。

## 5. 提交门（`confirm_commit`）

有变更：出示【拟提交·仓库】块（文件 / `.gitignore` 现状 / 分支与跟踪 / 仅提交或提交推送 / 推送目标），确认后执行；默认仅本地提交，推送须点名。
无变更：跳过本门，不得硬造提交。

## 6. 终端判定

- `done`：产出落盘、门已过或无门、无未闭环阻断。
- `blocked`：有阻断；写卡点、已尝试、恢复条件。
- `cancelled`：用户确认取消；写原因与未完成项。
- P0 未过或任一 `处置=测` 意图未终态 → 只能 `blocked`，不得写整体通过。

## 7. 回执

```text
route=workflow:<id> | step=closeout | packet=rules/packets/_shared/closeout.md | reads=rules/core/global-rules.md | global=ok | claim=ALLOWED|DENIED|na | status=done|blocked|cancelled | next=…
```
