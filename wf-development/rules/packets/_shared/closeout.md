# 收尾与提交 · 共享终端（开发）

> **全局规则**：开始本步前读 `rules/core/global-rules.md`；首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。
> 适用：本包所有 workflow 的 `closeout` 终端状态。状态真值=`activeContext.md` 本包运行状态；本步完成后置 `done`。
> 本文件是唯一收尾步；各链不再单独生成 closeout 步骤包。

## 1. 进入条件

- 本链最后一个 domain 步骤的产出已落盘；`completion-gate`/`s6-admission`/`release-readiness` 等门已 `ALLOWED` 或明确不适用。
- 没有未闭环阻塞；有则先写 `blocked`。
- 需要提交时，`.gitignore`、待提交文件、分支/跟踪已核对。

## 2. 收尾六点（按 `rules/templates/90-handoff/closeout-skeleton.md` §1）

1. **完成了什么**：短段 +「影响：」。
2. **改了哪些文件**：文件清单；未提交项；待提交摘要；git；`.gitignore`。
3. **验证与证据**：命令/结果/门回执；未验证项显式写出。
4. **假设**：本轮依赖的假设及影响。
5. **风险 / 阻塞**：风险、阻塞、责任人、恢复条件。
6. **下一步**：建议动作或下一个门。

> 只写现行结论，不写历史修改过程；缺项=未收尾。
> 有完成门：引用本轮 `CLAIM: ALLOWED`（门末已给）；无 ALLOWED 不得写完成；不重复跑全量。

## 3. 状态与同步

- `activeContext.md` 本包运行状态：`workflow/state=closeout/status=done|blocked|cancelled`、`packet: `rules/packets/_shared/closeout.md``、`gate=<回执或 na>`、`next=`。
- 本轮若改产品版本 SSOT：同轮改 `activeContext` 版本/焦点命中句；有计划则 §0 现行版本/焦点命中句一并改；有用户可见条目 → 根 `CHANGELOG` 对应版块（无则 `na`）；并按 `doc-facade-sync.md` 打开 README（及文首已有的现行版本句）对账，未打开不得 `冷层:ok`。跳过 Claim / 用户自提交不豁免。
- 阶段/门/焦点变化才更新 `{workroot}/development-plan.md` §0/§10；仅新增/改名/归档文件才更新 `{workroot}/INDEX.md`（文首现行版本句随 SSOT 变除外，见 `global-rules` §8）。
- 不再单独写 `triad=`/`facade=` 字段；有对外门面变化时在收尾第 6 点说明一句。

## 4. 提交门（`confirm_commit`）

有变更：出示【拟提交】块（文件 / `.gitignore` 现状 / 分支与跟踪 / 仅提交或提交推送 / 推送目标），确认后执行；默认仅本地提交，推送须点名。
无变更：跳过本门，不得硬造提交。
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
