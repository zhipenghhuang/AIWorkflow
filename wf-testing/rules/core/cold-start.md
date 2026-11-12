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

- 读 `activeContext` 运行状态里的 `packet=`，**先用工具打开该步骤卡**，再从该步继续；不从头重跑。
- 未打开 `packet=` → 不得写 `global=ok`、不得宣称已按本步包执行。
- packet 丢失用 `workflows/<id>.md` 状态表定位；仍不明 → 停下问用户。
- 同链中段：`global-rules` 按 §7 最小集复核，禁预防性通读全文/大手册。
- 状态/心跳/计划同步细则见 `rules/core/global-rules.md` §8。

## 3. 回执（字段单一出处）

```text
route=workflow:<id> | step=<id> | agent=<agent> | packet=<本步步骤卡路径> | global=ok|dev:<原因> | skills=<name=done|na,…> | claim=ALLOWED|DENIED|na | next=<...>
```

- **字段名固定**，不得自造别名（如 `role=`、`workflow=`）；`route/step/packet/global` 必填，`agent/skills/claim/next` 按需。
- **首条锚**（每轮第一行）可加 `level=<按事实推导> | reason=<意图类+信号+轨道依据> | reads=<实际读取来源> | next_action=`；只读写 `route=readonly:analysis | step=explain | mode=analyze`。
- `packet=` 必须是本步已打开的步骤卡相对路径；`global=ok` = 已按 §7 复核且步骤卡已实读。
- 跳过步骤/门记 `skip=<理由>`；`when` 求值后跳过记 `when_eval=假:<依据>`。收尾【遵守自检】另按本包收尾骨架。
