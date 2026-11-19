# 收尾与提交 · 共享终端（开发）

> **全局规则**：开始本步前读 `rules/core/global-rules.md`；首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。
> 适用：本包所有 workflow 的 `closeout` 终端状态。状态真值=`activeContext.md` 本包运行状态；本步完成后置 `done`。
> 本文件是唯一收尾步；各链不再单独生成 closeout 步骤包。

## 1. 进入条件

- 本链最后一个 domain 步骤的产出已落盘；`completion-gate`/`s6-admission`/`release-readiness` 等门已 `ALLOWED` 或明确不适用。
- 没有未闭环阻塞；有则先写 `blocked`。
- 需要提交时，`.gitignore`、待提交文件、分支/跟踪已核对。

## 2. 收尾六点（标题与子字段以 `rules/templates/90-handoff/closeout-skeleton.md` §1 为准）

1. 完成了什么：短段 +「影响：」。
2. 改了哪些文件：文件：/未提交：/建议动作：/待提交摘要：/git：/.gitignore：/文档归档：。
3. 如何验证：命令/结果/门回执；未验证项写「未验证：」。
4. 假设与未决项（待你确认）：假设：/待你确认：/默认（不回复即执行）：/回复：/可转发产品：；有决策项按 事项/选项/建议/影响默认 四行。
5. 还存在什么问题或风险：风险、阻塞、责任人、恢复条件。
6. 当前进度与下一步：当前：；下一步：1）…（执行：/产出：/完成标志：）+ 优先级：/建议：/不建议：。

> 另写「附：运行与沉淀」：资料补强：/工作记忆：/运行态：。只写现行结论；缺项=未收尾。【遵守自检】字段只认 `rules/core/execution-contract.md` §6。
> 发出前自检：头块分行（【任务收尾】【验证回执】【遵守自检】）→ 汇报独立 → 六点齐 → 附齐 → `python verify/tools/check_compliance.py --report <收尾文件>`。
> 有完成门：引用本轮 `CLAIM: ALLOWED`（门末已给）；无 ALLOWED 不得写完成；不重复跑全量。

## 3. 状态与同步

- `activeContext.md` 本包运行状态：`workflow/state=closeout/status=done|blocked|cancelled`、`packet: `rules/packets/_shared/closeout.md``、`gate=<回执或 na>`、`next=`。
- 本轮若改产品版本 SSOT：同轮改 `activeContext` 版本/焦点命中句；有计划则 §0 现行版本/焦点命中句一并改；有用户可见条目 → 根 `CHANGELOG` 对应版块（无则 `na`）；并按 `doc-facade-sync.md` 打开 README（及文首已有的现行版本句）对账，未打开不得 `冷层:ok`。跳过 Claim / 用户自提交不豁免。
- 阶段/门/焦点变化才更新 `{workroot}/development-plan.md` §0/§10；仅新增/改名/归档文件才更新 `{workroot}/INDEX.md`（文首现行版本句随 SSOT 变除外，见 `global-rules` §8）。
- 有对外门面变化时在收尾第 6 点说明一句。

## 4. 提交门（`confirm_commit`）

有变更：出示【拟提交·收尾文档】块（文件 / `.gitignore` 现状 / 分支与跟踪 / 仅提交或提交推送 / 推送目标），确认后执行；默认仅本地提交，推送须点名。
顺序：代码/产物已在前序 verify/gates 步的 `confirm_commit` 确认并提交；本门只确认收尾文档/索引；门后不再改代码/证据。门后改代码/证据 → 重跑门（回执绑定提交）。
无变更：跳过本门，不得硬造提交。未过完成门不得用本门提交代码/产物。
部署/回写/发布有独立门，不在本步重跑。

## 5. 终端判定

- `done`：产出落盘、门已过或无门、无未闭环阻断。
- `blocked`：有阻断；写卡点、已尝试、恢复条件。
- `cancelled`：用户确认取消；写原因与未完成项。
- 未过门或仍有未闭环阻断 → 只能 `blocked`，不得写完成/通过。

## 6. 回执

```text
route=workflow:<id> | step=closeout | packet=rules/packets/_shared/closeout.md | reads=rules/core/global-rules.md | global=ok | claim=ALLOWED|DENIED|na | status=done|blocked|cancelled | next=…
```
