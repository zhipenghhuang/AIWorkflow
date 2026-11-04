# 步骤包 · new-product/launch

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`new-product`
- **step**：`launch`（上市与复盘）
- **packet**：`rules/packets/new-product/launch.md`
- **条件步** `when=go_decision_go`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：上市与复盘
- **产出**：发布决策 + GTM 检查 + 复盘（{workroot}/{ver}/40-delivery/、90-retrospectives/）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 前置：UAT 通过（带条件须已接受）+ GTM 就绪（模板 `rules/templates/40-delivery/gtm-template.md`：定价 / 渠道 / 物料 / 销售客服）+ 发布检查（回滚 / 公告 / 客服 / 监控）。 confirm_release：出示上市要点请确认；**未过 UAT 不发布**。 发布后：指标监控 → 复盘（模板 `rules/templates/60-retro/retro-template.md`）→ 改进项回需求池；更新 `{workroot}/product-plan.md` 。

## 4. 本步门

- **HITL `confirm_release`**：出示 UAT 结论、回滚预案、公告/客服/监控就绪；未过不发布；已发布仅复盘不重复确认
- **GATE `uat-evidence` when=has_uat**：运行 `verify/Invoke-Gate.ps1 -Mode uat`；AC 覆盖、证据、有条件通过的责任人/接受人；未 READY 不得写 UAT 通过。无 UAT 要求可写 `verdict: 不适用` + 依据/批准人，门放行但记警告

## 5. 做法

### 本步动作清单

- 前置：UAT 通过（带条件须已接受）+ GTM 就绪（模板 `rules/templates/40-delivery/gtm-template.md`：定价 / 渠道 / 物料 / 销售客服）+ 发布检查（回滚 / 公告 / 客服 / 监控）。 confirm_release：出示上市要点请确认。
- **未过 UAT 不发布**。 发布后：指标监控 → 复盘（模板 `rules/templates/60-retro/retro-template.md`）→ 改进项回需求池。
- 更新 `{workroot}/product-plan.md` 。

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
route=workflow:new-product | step=launch | reads=rules/packets/new-product/launch.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/new-product/launch.md`；对不上 = 未遵守读链。
