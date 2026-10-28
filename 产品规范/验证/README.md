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
| 平台回写 | `Invoke-Gate.ps1 -Mode writeback -Artifact …` | 单号 + 备注实质 + 状态取值 + 附件回查 |
| 收尾自检 | `python 验证/tools/check_compliance.py --report <收尾文件>` | 【验证回执】+【遵守自检】route/mode/reads |

```powershell
# 推荐始终带 -Artifact，避免多版本 mtime 选错
powershell -ExecutionPolicy Bypass -File "产品规范/验证/Invoke-Gate.ps1" -Mode prd -Artifact "产品/V1/PRD-….md" -ProjectRoot "."
```

作者侧：落盘 →【完稿自检摘要】→ `-Mode prd`（P2+/P1↑/拟定稿必跑；BLOCKED 不得定稿）。选 B：评审记录 → `-Mode review` → 回填 `gate_id`/`review_status: APPROVED` → 复跑 `-Mode prd`。选 A：`review_status: HUMAN_APPROVED` + `approved_by` + `status: APPROVED` → 复跑 `-Mode prd` 至 READY。P1↑ 自检按 P2、可免独立审。回执 `.gate/产品规范/{mode}.json`。

## 2. 检查什么

- **PRD**：frontmatter + TBD；全量另核结构/追溯；**light 不因缺追溯矩阵 BLOCKED**（仅警告）。P2+ APPROVED 须 `review_status`/`gate_id`/`source_of_truth`。
- **评审**：reviewer ≠ author；清单填实；verdict。
- **UAT**：逐条结果+证据；对照 PRD AC；有条件通过须接受人。
- **变更**：§6 联动状态闭合。
- **回写**：单号 + 备注实质内容 + 状态取值 + fileId/无附件；禁仅出现「备注/状态/附件」字样刷绿。

> 独立复制说明：`验证/` 依赖 `规则/tools/validate_prd.py` 做全量 PRD 结构校验；只复制 `验证/` 时请一并复制该脚本，否则全量 PRD 会 BLOCKED（不会假通过）。

## 3. 完成状态

> `READY/DRAFT/BLOCKED` 条件与报告措辞见 `规则/核心/验证规则.md` §2；本文件不重复状态表。回执中文：可定稿/草稿/阻塞；机器仍读 READY/DRAFT/BLOCKED。

## 4. 成本纪律

- 门只读现有产物，不新增 PRD/评审/UAT 文档。
- 全量 PRD 结构检查用 `validate_prd.py`；轻量 PRD 走 `prd_level=light` 最小校验；语义/独立性/闭合用轻量脚本。
- 不要求每个 PRD 都做全量评分；P0/P1 可轻量，P2+ 才独立评审。
- 人工只判断价值/优先级/设计质量；机器查结构/追溯/证据/回执。
