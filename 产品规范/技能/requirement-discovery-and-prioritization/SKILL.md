---
name: requirement-discovery-and-prioritization
description: Use when collecting requirements, analyzing users or competitors, prioritizing, or scoping a release. Produce traceable requirement-pool entries and a prioritized MVP scope.
---

# 需求洞察与优先级（技能 · 随包生效）

> 用于：discover / prioritize 步。

## 1. 来源分层（每条都要留证据）

| 来源 | 怎么拿 | 证据要求 |
| --- | --- | --- |
| 用户反馈/客服工单 | 抽样、归类、频次统计 | 渠道+日期+样本量；原文可回查 |
| 数据 | 埋点/报表/漏斗 | 指标名+口径+时间窗 |
| 销售/业务 | 访谈、需求单 | 谁+何时+影响客户数 |
| 竞品 | 官网/试用/公开资料 | 链接+日期（禁凭印象） |
| 合规/外部 | 法规、审计、合同 | 条款/文件+日期 |

## 2. 访谈法（Mom Test 精神）

- 问**过去的行为**与具体案例，不问「你会不会用/你觉得好不好」；
- 一次一问；追问「上次遇到是什么时候、怎么解决的、代价是什么」；
- 记录原话（脱敏），不把推测写成用户结论。

## 3. 问题定义（先问题后方案）

- 谁（角色）／在什么场景／遇到什么问题／现在怎么绕过／代价多大；
- 没有证据的「痛点」→ 标**待验证**，不进版本。

## 4. 优先级方法（按需选一，口径写清）

- **Kano**：基本型/期望型/兴奋型——先保基本型；
- **RICE**：`(触达×影响×信心)/成本`——信心不足先验证；
- **MoSCoW**：Must/Should/Could/Won't——Won't 即范围排除。

拿不准向上一档并说明理由；**不做优先级的需求不排期**。

## 5. 需求池纪律

- 同问题去重合并（不同表达指向主条目）；每条状态唯一（待评估/已立项/已排期/已上线/搁置）；
- 每条有来源、初判（价值/成本/风险）、优先级；搁置写原因；
- 立项输出：MVP 范围 + 排除项 + 粗排期 + 依赖风险（`confirm_scope` 用）。
