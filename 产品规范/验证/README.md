# 验证（产品轨）

> 目的：让“PRD 定稿/评审通过/UAT 通过/变更关闭/回写完成”有可对账的证据。门读现有 PRD/评审/UAT/受理单，不新增产品文档。
> 读取时机：`prd.review`、`deliver.uat`、`change.apply`、`defect.writeback` 前。维护读 `规则/核心/规则治理.md`。

## 1. 什么时候跑

| 场景 | 命令 | 输出 |
| --- | --- | --- |
| PRD 定稿 | `Invoke-Gate.ps1 -Mode prd` | 结构/AC/追溯/TBD/定稿状态 |
| PRD 评审 | `Invoke-Gate.ps1 -Mode review` | 独立评审/评分/阻断项 |
| UAT | `Invoke-Gate.ps1 -Mode uat` | AC 覆盖/证据/遗留接受人 |
| 变更关闭 | `Invoke-Gate.ps1 -Mode change` | 联动清单闭合 |
| 平台回写 | `Invoke-Gate.ps1 -Mode writeback` | 单号/备注/状态/附件回执 |

```powershell
powershell -ExecutionPolicy Bypass -File "产品规范/验证/Invoke-Gate.ps1" -Mode prd -ProjectRoot "."
```

作者侧：落盘 →【完稿自检摘要】→ `-Mode prd`（P2+/P1↑/拟定稿必跑；BLOCKED 不得定稿）。选 B：评审记录 → `-Mode review` → 回填 `gate_id`/APPROVED → 复跑 `-Mode prd`。选 A：HUMAN_APPROVED + 结构非 BLOCKED。P1↑ 自检按 P2、可免独立审。回执 `.gate/产品规范/{mode}.json`。

## 2. 检查什么

- **PRD**：frontmatter、0～16 节、F/R/A/AC、追溯矩阵至少 1 行有效 F/R/A/AC、TBD 责任人/期限、来源/假设；P2+ `status=APPROVED` 必须有 `review_status=APPROVED` + `gate_id` + `source_of_truth=true`，且 PRD 与评审记录 `gate_id` 一致。P0/P1 轻量 PRD（`prd_level=light`）只核最小节/验收表/TBD，免独立评审。
- **评审**：reviewer ≠ author；清单必须选择“全部通过”或逐条例外（不能保留模板双选项）；有结论/评分/阻断项；verdict。
- **UAT**：解析 §2 逐条验收表；每条有结果+证据；有 PRD 时逐条对照 PRD §13 AC，缺 AC = BLOCKED；有条件通过必须有责任人/接受人。无 UAT 要求可写 `verdict: 不适用` + 依据 + 批准人/接受人，门放行并记警告；不得用不适用绕过真实用户验收。
- **变更**：受理单 §6 联动清单每项“已更新/不适用/待补”；待补有责任人/截止。
- **回写**：平台单号、备注、状态、附件回查；声称已回写必须有 noteId/回执/时间。

> 独立复制说明：`验证/` 依赖 `规则/tools/validate_prd.py` 做全量 PRD 结构校验；只复制 `验证/` 时请一并复制该脚本，否则全量 PRD 会 BLOCKED（不会假通过）。

## 3. 完成状态

> `READY/DRAFT/BLOCKED` 条件与报告措辞见 `规则/核心/验证规则.md` §2；本文件不重复状态表。回执中文：可定稿/草稿/阻塞；机器仍读 READY/DRAFT/BLOCKED。

## 4. 成本纪律

- 门只读现有产物，不新增 PRD/评审/UAT 文档。
- 全量 PRD 结构检查用 `validate_prd.py`；轻量 PRD 走 `prd_level=light` 最小校验；语义/独立性/闭合用轻量脚本。
- 不要求每个 PRD 都做全量评分；P0/P1 可轻量，P2+ 才独立评审。
- 人工只判断价值/优先级/设计质量；机器查结构/追溯/证据/回执。
