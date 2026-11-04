# 步骤包 · control/check

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`control`
- **step**：`check`（阶段门检查）
- **packet**：`rules/packets/control/check.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：阶段门检查
- **产出**：阶段门检查结论/缺口

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 技能：`skills/development-plan/SKILL.md` ；只读检查，不改代码。 可运行 `python rules/tools/validate_dev_plan.py <开发计划路径>`（可用时）；核验：阶段表与当前阶段一致；每阶段“技能”列已填；本阶段输入/产出/证据齐；下一阶段输入具备；风险/变更已更新；L2+ 开发计划存在。 交接核验：本阶段应发/应收的 HO 是否有回执；`handoff-ledger.md` 与计划 / 是否一致；阻断下游的包是否已升级；未回执不得判阶段完成。 多波次（若计划含 W1/W2/波次）：计划总控表（当前阶段/门）带当前波次；门结论有 G{n}-W{k}；S2～S5 禁因某波次已过就整行「完成」且输入/证据波次不得陈旧（见 `skills/development-plan/SKILL.md` ）。 缺口按「阶段/门/缺什么/影响/建议」列出；不替代机器门禁与测试结论。 不过门 → 回到对应阶段补；不得把「计划写了」当「已执行」。

## 4. 本步门

- **GATE `dev-plan` when=dev_plan_required**：**checklist**：跑 `rules/tools/validate_dev_plan.py`（可用时）+ 阶段表/门/证据/下一步人工核；缺项不过

## 5. 做法

### 技能 `development-plan`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「计划可以后补」 | L2+ 无计划则阶段/门/下一动作失真；先建再跑。 |
| 「阶段表技能列可空」 | 每阶段至少挂一个技能；空列=加载失败。 |
| 「状态只改 activeContext」 | 计划 §0 / 索引 / 进行中三处同拍。 |
### 编排备忘

技能：`skills/development-plan/SKILL.md` ；只读检查，不改代码。 可运行 `python rules/tools/validate_dev_plan.py <开发计划路径>`（可用时）；核验：阶段表与当前阶段一致；每阶段“技能”列已填；本阶段输入/产出/证据齐；下一阶段输入具备；风险/变更已更新；L2+ 开发计划存在。 交接核验：本阶段应发/应收的 HO 是否有回执；`handoff-ledger.md` 与计划 / 是否一致；阻断下游的包是否已升级；未回执不得判阶段完成。 多波次（若计划含 W1/W2/波次）：计划总控表（当前阶段/门）带当前波次；门结论有 G{n}-W{k}；S2～S5 禁因某波次已过就整行「完成」且输入/证据波次不得陈旧（见 `skills/development-plan/SKILL.md` ）。 缺口按「阶段/门/缺什么/影响/建议」列出；不替代机器门禁与测试结论。 不过门 → 回到对应阶段补；不得把「计划写了」当「已执行」。

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
route=workflow:control | step=check | reads=rules/packets/control/check.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/control/check.md`；对不上 = 未遵守读链。
