# 步骤包 · plan/scope

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`plan`
- **step**：`scope`（本期范围与里程碑）
- **packet**：`rules/packets/plan/scope.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：本期范围与里程碑
- **产出**：产品计划工作稿 §3 范围/§4 里程碑（确认后同轮并入主档）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 本期做 / 不做（MVP）、产能约束、里程碑（设计 / 开发 / 提测 / UAT / 发布）、依赖与风险。 ** Brief+本期差量表必填**（默认权威写在计划本节；增/改/删；首版可「全部为增」）。 **独立迭代变更摘要**：默认不建；仅仓外handoff/版本单独归档/用户点名时才落 `迭代变更摘要-{ver}.md` 为唯一权威， 只写「见该路径」（模板 `rules/templates/10-planning/iteration-change-summary-template.md`）。禁止双份完整表。 confirm_plan：出示目标 / 路线图 / 本期范围 / ** 差量表摘要** / 里程碑 / 风险请确认；首次计划或范围·指标·版本实质变更必停； 同周期同版本只确认一次（「继续」沿用）。 **确认后必须同轮落盘**：把确认稿并入 `{workroot}/product-plan.md`（/含/），不要等 wrap；会话中断时以已落盘稿为准。 **计划未确认不进入 PRD / 排期**（见 `rules/workflow.md` 第 1 节）。 **无产品计划第 3.0 节 Brief+差量表（权威在独立摘要时须可打开）不得交开发当本期范围已清**。

## 4. 本步门

- **HITL `confirm_plan`**：首次计划或范围·指标·版本实质变更：目标/路线图/本期范围/**§3.0 Brief+差量表** /里程碑/风险摘要；无差量表（且非明示首版一行）不过门；未确认不进 PRD/排期

## 5. 做法

### 本步动作清单

- 本期做 / 不做（MVP）、产能约束、里程碑（设计 / 开发 / 提测 / UAT / 发布）、依赖与风险。 ** Brief+本期差量表必填**（默认权威写在计划本节。
- 增/改/删。
- 首版可「全部为增」）。 **独立迭代变更摘要**：默认不建。
- 仅仓外handoff/版本单独归档/用户点名时才落 `迭代变更摘要-{ver}.md` 为唯一权威， 只写「见该路径」（模板 `rules/templates/10-planning/iteration-change-summary-template.md`）。禁止双份完整表。 confirm_plan：出示目标 / 路线图 / 本期范围 / ** 差量表摘要** / 里程碑 / 风险请确认。
- 首次计划或范围·指标·版本实质变更必停。
- 同周期同版本只确认一次（「继续」沿用）。 **确认后必须同轮落盘**：把确认稿并入 `{workroot}/product-plan.md`（/含/），不要等 wrap。
- 会话中断时以已落盘稿为准。 **计划未确认不进入 PRD / 排期**（见 `rules/workflow.md` 第 1 节）。 **无产品计划第 3.0 节 Brief+差量表（权威在独立摘要时须可打开）不得交开发当本期范围已清**。

## 6. 打开/填写

- 运行时正文：仅本文件（开局卡已在会话开头读过）。
- 无强制模板：直接写 §2 产出路径产物。

## 7. 完成信号

- §2 产出已落盘。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 8. 回执字段

```text
route=workflow:plan | step=scope | reads=rules/packets/plan/scope.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/plan/scope.md`；对不上 = 未遵守读链。
