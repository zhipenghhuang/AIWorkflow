# 开局卡（测试轨）

> **冲突**：覆盖顺序只认 `rules/core/global-rules.md` §11；与门/红线冲突先说明风险，再等用户选择。
> **读取级别：常驻**（新会话读一次）；`global-rules` 按 §7 重读，中段只重锚运行状态，不重读本卡。
> **入口**：宿主已打开本包 `AGENTS.md`；本卡不再回指 AGENTS。口令未定再回 AGENTS 口令表 / `routing.md`。

## 1. 新会话顺序（按序一次）

1. `activeContext.md`：总览 + 本包运行状态（workflow/state/packet）+ **偏好/洞见/坑 ≤3 行**（无则当无；写法 `context-memory.md`）。
2. `rules/core/global-rules.md`：按 §7 重读（开局全文）；未按 §7 复核不得写 `global=ok`。
3. 有 `env-baseline.md` → 身份/§1/§4/§8/§13/§16 命中节；涉计划再读 `{workroot}/{ver}/test-plan.md` §0/§6。
4. 未接入 → `onboard`；已接入（`wf-testing onboard: done`）→ 命中 workflow 后读 `workflows/<id>.md`（一次）→ 当前步骤卡。

## 2. 续跑

- 读 `activeContext` 运行状态里的 `packet=`，从该步继续；不从头重跑。
- packet 丢失用 `workflows/<id>.md` 状态表定位；仍不明 → 停下问用户。
- 状态/心跳/计划同步细则见 `rules/core/global-rules.md` §8。

## 3. 回执

```text
route=workflow:<id> | step=<id> | packet=<path> | global=ok | skills=<...|na> | claim=ALLOWED|DENIED|na | next=<...>
```
