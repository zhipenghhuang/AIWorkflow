# 验证（产品轨）

> 目的：让“PRD 定稿/评审通过/UAT 通过/变更关闭/回写完成”有可对账的证据。门读现有 PRD/评审/UAT/受理单，不新增产品文档。
> 读取时机：`prd.review`、`deliver.uat`、`change.apply`、`defect.writeback` 前。维护读 `规则/30-规则治理.md`。

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

P2+ 定稿顺序：`-Mode prd` 结构检查（DRAFT=结构过、未定稿）→ `-Mode review`；READY 后把回执 `gate_id` 回填 PRD/评审记录并置 `APPROVED`，再复跑 `-Mode prd`。轻量 PRD 免独立评审。

## 2. 检查什么

- **PRD**：frontmatter、0～16 节、F/R/A/AC、追溯矩阵、TBD 责任人/期限、来源/假设；P2+ `status=APPROVED` 必须有 `review_status=APPROVED` + `gate_id`。P0/P1 轻量 PRD（`prd_level=light`）只核最小节/验收表/TBD，免独立评审。
- **评审**：reviewer ≠ author；有清单/评分/阻断项；verdict；`gate_id` 由回执回填（不手编）。
- **UAT**：对照 AC/验收标准；有证据；有条件通过有责任人与接受人。
- **变更**：受理单 §6 联动清单每项“已更新/不适用/待补”；待补有责任人/截止。
- **回写**：平台单号、备注、状态、附件回查；声称已回写必须有 noteId/回执/时间。

## 3. 完成状态

| 状态 | 条件 | 报告措辞 |
| --- | --- | --- |
| `READY` | 结构/追溯/评审/UAT/联动/回写检查通过 | 已定稿/评审通过/可发布 |
| `DRAFT` | 结构完整但有非阻断待确认/未定稿 | 草稿/待评审；列待确认 |
| `BLOCKED` | 缺评审/缺证据/关键 TBD 无主/断链/无回执 | 未完成/阻塞/未验证 |

## 4. 成本纪律

- 门只读现有产物，不新增 PRD/评审/UAT 文档。
- 全量 PRD 结构检查用 `validate_prd.py`；轻量 PRD 走 `prd_level=light` 最小校验；语义/独立性/闭合用轻量脚本。
- 不要求每个 PRD 都做全量评分；P0/P1 可轻量，P2+ 才独立评审。
- 人工只判断价值/优先级/设计质量；机器查结构/追溯/证据/回执。
