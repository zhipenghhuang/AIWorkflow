# 步骤包 · defect-fix/gates

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`defect-fix`
- **step**：`gates`（门禁）
- **packet**：`rules/packets/defect-fix/gates.md`
- **条件步** `when=has_code_change`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：门禁
- **产出**：.gate/wf-development/completion.json + 门禁摘要

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 本批无代码/配置改动项 → 跳过（纯文档/纯评估）；有改动运行 `verify/Invoke-Gate.ps1 -Acceptance <缺陷修复卡/任务清单>`，门写 `.gate/wf-development/completion.json`；L1+ 无验收表先补，不得空跑门。 `has_code_change` = 本轮 diff 非空（不含生成物）；与 `implementation_required`（清单已确认）区分，避免纯文档批空跑门。 日志分诊（子代理编排 ）：原始日志落盘，先脚本过滤；仅多文件语义归因才派子代理，返回摘要 ≤30 行。 失败不声称完成；存量失败只对账新增；工具/环境缺失 → BLOCKED。

## 4. 本步门

- **GATE `completion-gate`**：任务开始 `-StartTask`；运行 `verify/Invoke-Gate.ps1 -Acceptance ...`；写 `.gate/wf-development/completion.json`；**前端套装与 capture 只认 `rules/core/frontend-gate.md`**；**写完成前 `-Claim`，只认 `CLAIM: ALLOWED`**；空 diff=`NOT_VERIFIED`、dry-run=`DRY_RUN`、缺项 → `BLOCKED`

## 5. 做法

### 本步动作清单

- 本批无代码/配置改动项 → 跳过（纯文档/纯评估）。
- 有改动运行 `verify/Invoke-Gate.ps1 -Acceptance <缺陷修复卡/任务清单>`，门写 `.gate/wf-development/completion.json`。
- L1+ 无验收表先补，不得空跑门。 `has_code_change` = 本轮 diff 非空（不含生成物）。
- 与 `implementation_required`（清单已确认）区分，避免纯文档批空跑门。 日志分诊（子代理编排 ）：原始日志落盘，先脚本过滤。
- 仅多文件语义归因才派子代理，返回摘要 ≤30 行。 失败不声称完成。
- 存量失败只对账新增。
- 工具/环境缺失 → BLOCKED。

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
route=workflow:defect-fix | step=gates | reads=rules/packets/defect-fix/gates.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/defect-fix/gates.md`；对不上 = 未遵守读链。
