# 技能抽测（测试轨）

> 目的：用 3 条低成本用例验证“技能是否被正确选中、是否产出可判定结果”，不追求全量评测。
> 用法：把 prompt 交给 AI，记录「选中的技能 / 首条输出 / 是否违反 must_not」；每条 ≤1 分钟判断。
> 频率：技能大改后、季度体检时；不阻塞日常业务。

| ID | Prompt | 期望技能 | 必须出现 | 不得出现 |
| --- | --- | --- | --- | --- |
| T-E1 | “根据这份 PRD 生成功能用例” | `test-basis-analysis` + `testcase-design` | 需求模型/歧义/GAP/oracle；再设计用例与覆盖映射 | 直接写用例、按现网反推预期 |
| T-E2 | “执行这个模块，尽量跑完” | `test-execution-and-exploration` | 计划/批次/证据/blocked 四问；失败实拍 | 无证据判通过、blocked 当通过 |
| T-E3 | “出测试报告，能准出吗” | `test-execution-and-exploration` + 报告规则 | 跑 `-Mode report`、台账/报告对账、P0/S1S2/探索硬项 | 未跑门写“整体通过/可发布” |

判定：3 条中 ≥2 条通过为“可用”；must_not 命中任一为“失败”，需修技能或 description 触发词。
