# 技能抽测（开发轨）

> 目的：用 3 条低成本用例验证“技能是否被正确选中、是否产出可判定结果”，不追求全量评测。
> 用法：把 prompt 交给 AI，记录「选中的技能 / 首条输出 / 是否违反 must_not」；每条 ≤1 分钟判断。
> 频率：技能大改后、季度体检时；不阻塞日常业务。

| ID | Prompt | 期望技能 | 必须出现 | 不得出现 |
| --- | --- | --- | --- | --- |
| D-E1 | “登录接口 500，先修一下” | `debugging-and-error-recovery` | 复现/日志/最小化/根因/防回归；失败 2 次换路径 | 未复现直接猜改、改断言凑绿 |
| D-E2 | “选 Redis 还是 PostgreSQL 做队列” | `technology-selection` + `solution-design` | 约束/候选/权重矩阵/POC/ADR/退出方案 | 只凭喜好或 demo 下结论 |
| D-E3 | “评审这段 diff 能不能合” | `code-review` + `engineering-quality` | 六轴、评审范围=diff、AC 覆盖、证据 | 只挑格式、无证据称通过、作者自审 |

判定：3 条中 ≥2 条通过为“可用”；must_not 命中任一为“失败”，需修技能或 description 触发词。
