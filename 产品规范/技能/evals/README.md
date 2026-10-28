# 技能抽测（产品轨）

> 目的：用 3 条低成本用例验证“技能是否被正确选中、是否产出可判定结果”，不追求全量评测。
> 用法：把 prompt 交给 AI，记录「选中的技能 / 首条输出 / 是否违反 must_not」；每条 ≤1 分钟判断。
> 频率：技能大改后、季度体检时；不阻塞日常业务。

| ID | Prompt | 期望技能 | 必须出现 | 不得出现 |
| --- | --- | --- | --- | --- |
| P-E1 | 客户说“审批流太慢，帮我写 PRD” | `customer-needs-discovery` + `prd-writing` | 先复述问题/角色/场景/证据缺口；范围/AC 未确认前不写全量 PRD | 直接假设审批角色/流程并写完整 PRD |
| P-E2 | “给这 5 个需求排优先级，下周定版本” | `requirement-discovery-and-prioritization` | RICE/WSJF 口径、证据/信心、Won't 清单 | 只按感觉/领导偏好排序 |
| P-E3 | “评审这份 PRD，能交开发吗” | `artifact-review` + `review-and-finalize` | A/B 选择、评分卡/阻断项、未过门写草稿/待评审 | 作者自审自批、无证据称“可交开发” |

判定：3 条中 ≥2 条通过为“可用”；must_not 命中任一为“失败”，需修技能或 description 触发词。
