---
name: test-interface
description: Use for API and contract testing. Prefer script-first execution, contract coverage, negative/authorization checks, and reusable regression assets over repeated AI UI clicking.
---

# 接口测试（技能 · 随包生效）

> 产物/维度/脚本默认以 `规则/轨契约/接口.md` 为准；本技能=找 bug 的手感与提效方式。

## 1. 契约阅读法

- 从 OpenAPI/设计文档/Network 提取：必填、类型与格式、枚举、范围、长度、默认值、错误码表。
- 每个「未声明」都是风险点：声明下一步动作（试/问/标不适用）。
- 记录契约版本；breaking change（删字段/改类型/改语义/新必填）单独标记。

## 2. 脚本优先（默认）

- 确定性接口用例 → **同轮产出脚本**（`executor --mode=api`），回归 0 token。
- AI 只做：契约探查、语义/业务规则判定、脚本生成/维护、失败复核；**不逐步点击 UI 替代接口调用**。
- 脚本放 `测试/接口测试/脚本/`；`tags: ['interface','smoke'|'regression']`；`suites` 固定；**P0 接口冒烟**登记 `测试/00-稳定冒烟清单.md`，其余按 tags 选型。

## 3. 接口缺陷谱系（照单排查）

参数校验缺口（非法/空/停用引用）｜越权与 IDOR（换主体访问）｜幂等缺失（重放）｜终态重入｜超长与 Emoji 截断/乱码｜分页边界与排序注入｜错误码语义错（假成功 / 200 空壳）｜浮点与精度｜时区｜大字段与响应膨胀｜HTTP 方法与内容类型误用。

## 4. 三层写法

正常契约（成功码 + 关键字段断言）→ 异常输入（4xx 且无脏写）→ 对抗（越权/重放/注入）。  
判定三要素：状态码 + 业务信号 + 关键字段值——**仅 2xx 不得记通过**。

## 5. 隔离与数据

- 无 token/越权条用隔离上下文；写条**写后回查**（列表/详情）。
- 造数走 `api`（快、可核对）；UI 仅保留主路径。
- 清数/幂等用 `runStamp`/业务前缀；不污染后续用例。

## 6. 工具（选装 · 未装降级）

- `api-client`：OpenAPI/Postman/Apifox 导入，契约初稿 → 实测校正。
- `api-fuzz`（schemathesis）：生成负向候选 → **人工对照判定**，禁自动判过。
- `contract-test`（Pact/Specmatic）：消费方契约；breaking change 阻断。
- `mock-server`：依赖未交付/异常注入；mock 结论不得冒充真实链路。
- 接口脚本默认走 `executor --mode=api`；CI 可按 `--tag=interface`/`--suite=…` 复跑。

## 7. 资产复用

- 按模块/契约版本维护脚本；新版本只更新受影响 endpoint；旧轮留档仅用户确认/版本关闭 → `测试/接口测试/_归档/{yyyyMMdd}-{版本或批次}/`，**禁**整包装进根 `测试/_归档/`。
- 失败先区分：产品缺陷 / 契约漂移 / 脚本漂移 / 环境数据；脚本漂移修脚本，契约漂移更新用例与脚本。
