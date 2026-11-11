# 轨契约 · 接口（正式轨）

> 口令「生成/执行接口测试」时默读本文。  
> **计划驱动**：按 `{workroot}/{ver}/test-plan.md` §2 轨道/§3 轮次/§4 准出；本契约定接口执行细节，计划定范围/顺序/门禁。  
> **执行口径**：不预写全量接口用例；按契约清单 + 意图，执行时生成场景并写执行记录；确定性场景同轮脚本。

## 边界

| 项 | 约定 |
| --- | --- |
| 正式产物 | `{workroot}/{ver}/api/{NN}-{短名}-执行记录.md`（平铺；见 `rules/workflow.md` §1.3.0）；脚本 `{workroot}/scripts/`；P0 接口冒烟登记根 `smoke-checklist.md` |
| 过程 | `{workroot}/{ver}/api/.draft/` |
| 模板 | `rules/templates/20-test-cases/api-test-case-template.md`（执行记录；禁套功能模板） |
| 机检 | 落盘后 `rules/tools/validate_api_testcase.py <域文件>`；ERROR 未清不得称接口资产完成 |
| 执行形态 | **脚本优先**：确定性接口默认 executor --mode=api；AI 单 Agent 只做契约探查、语义判定、失败复核、脚本维护 |
| depth | `core`=补丁（P0维）；`standard`=迭代默认（命中接口适用维可执行+脚本）；`full`=发版（范围内全部必测接口×适用维） |
| 依据 | 主读/OpenAPI/Network + 分析 §2 接口意图；计划 §2 轨道；禁猜未见 path/字段；契约漂移须更新记录/脚本 |

## 产物与落盘

| 产物 | 路径 | 最低字段 |
| --- | --- | --- |
| 接口执行记录 | `{workroot}/{ver}/api/{NN}-{短名}-执行记录.md` | §0 记录信息 / §1 契约清单 / §2 场景与结果 / §3 失败详情 / §4 结论 |
| 契约清单 | 记录 §1 | EP｜方法+path｜关键参数/头｜成功码+关键字段｜来源 |
| 场景表 | 记录 §2 | SC｜优先级｜维度｜请求｜参数/头｜预期｜实际/差异｜结果｜证据｜缺陷｜EP｜INT/AC｜原文/契约 |
| 脚本 | `{workroot}/scripts/` | caseId｜api 动作｜断言｜tags/suites｜契约版本 |
| 锚点 | `{workroot}/smoke-checklist.md` | P0 接口冒烟 + P0锚点 |

## 适用维度（按接口语义；不要求全维矩阵）

成功契约｜无 token/失效｜越权/IDOR｜参数边界｜超长/Emoji｜非法状态/假成功｜幂等/并发｜不存在资源｜分页边界｜排序/注入｜错误 METHOD/Content-Type。

- 每个必测 EP 的适用维至少一个场景；「不适用」仅当该维对该 EP 无语义（事实句）；禁有适用维空写不适用。空缺=缺口。
- depth 未选中的维可标“本轮 depth 未装”，不得写“通过”进准出。

## 判定与执行纪律

- **判定三要素**：HTTP 状态码 + 业务码/业务信号 + 关键字段值；仅 2xx 不得记通过。
- 写条**写后回查**；假成功/200 空壳=失败。
- 无 token/越权用隔离上下文；失败摘要含方法+path+关键参数+码/消息（无密钥）；复核后仍失败才落终态。
- 错误语义对齐：预期业务阻断时实际须同类门禁/阻断码；入口错配/指纹过期/参数门禁错类不算“符合预期”。
- 中断续跑：以本轮记录内已有终态为准，从首个未完成条继续；已判定条不重跑（点名重测除外）。
- 开跑新鲜度：按计划 §3 轮次/意图；未进本轮→未执行/未本轮验证；depth 未选中的维不得保留“通过”。

## 脚本优先

- 执行器：`{workroot}/scripts/executor.mjs --mode=api --draftDir={workroot}/{ver}/api/.draft --evidenceDir={workroot}/{ver}/evidence`；脚本放 `{workroot}/scripts/`。
- 登录钩子 `config.apiLogin`；动作限 `api`（expectStatus/expectMessage/expectFields/save）与 `note`；无 token/越权用隔离上下文。
- 资产：按域/契约维护记录+脚本；跨版本只更新受影响 EP；旧轮 `_archive/`；P0 接口冒烟进 `smoke-checklist.md`。
- 契约漂移：breaking change 必须新增/更新场景与脚本；禁因换代重写全套；半残合并≥2 次 → 有界重生该域。
- 落账：AI 按 jsonl 汇总到执行记录；失败升级按 `script-execution` §3（有界复核）。

## 能力（可选）

| 能力名 | 用途 | 降级 |
| --- | --- | --- |
| api-client | OpenAPI/Postman/Apifox 导入 | 主读 + 现网 Network |
| api-fuzz | 负向候选 | AI 按维度现场设计；候选人工复核 |
| contract-test | 消费方契约 | 成功契约抽样 |
| mock-server | 依赖未交付/异常注入 | 基线造数 |

- api-fuzz 产物只作候选；禁自动判通过/直接落账；mock 结论不得冒充真实链路。

## 红线

- path/方法/关键字段以实测或主读原文为准；冲突标明以何为准。
- 写口真值：成功写口须同动作 Network/主读+实测成功；405/404 否定后禁把未验证邻口写成唯一真值。
- 生成必用 `api-test-case-template.md`；禁功能模板顶替；落盘跑 `validate_api_testcase.py`。
- 用例/场景 ID 用 `{前缀}-{NN}`；覆盖对照禁空；判定三要素；脚本默认。
- 域记录/脚本跨版本保留；只更新受影响 EP；`_archive/` 仅下线/重生快照。
- 与功能 UI 结论分轨；接口绿不冒充页面通论。
- **功能记录内嵌 API 探针 ≠ 接口轨完成**：迭代默认纳入接口轨（`multi-track-quality` §0）；纳入=是时须有 `{ver}/api/` 非空执行记录 + §1 契约清单 + 适用维落点 + 声明 depth≥`standard`（补丁才可 core）；未齐不得称接口覆盖完成/准出引用接口绿。
- **关账认正文（Q18）**：每域 `api/{NN}-…-执行记录.md` 非空且含 §1 契约清单 + §2 场景表；脚本/jsonl/探针 **不得** 顶替记录。计划范围点名的契约域 **必须有** 实质记录；仅当核实无该域契约面时写 N/A+事实句+**用户确认**（Q19），禁有面不测。
- 需要浏览器仅当契约依赖页面触发请求；否则 HTTP/客户端按契约测。
