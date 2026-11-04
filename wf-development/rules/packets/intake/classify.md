# 步骤包 · intake/classify

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`intake`
- **step**：`classify`（分类与登记）
- **packet**：`rules/packets/intake/classify.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：分类与登记
- **产出**：DOC/CR/OPEN/DEC 登记

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 分类：PRD/需求/迭代/special/原型/设计/接口/技术/测试/验收/反馈/调研/竞品/会议/数据/原始/其他（细则 `rules/doc-governance.md` ）。 输入为 PRD/迭代方案/需求文档/原型/接口或技术文档 → 先按 `skills/product-doc-analysis/SKILL.md` 产出理解摘要（须含 Brief+本期差量增/改/删 + 来源/目标/范围/F-R-AC/冲突/GAP/置信度），再登记；不得只登记文件名。 登记：`inbound/` 文件给 DOC；变更给 CR；确认项关 OPEN 并写 DEC；原始资料只登记不升级基线。 关联：R/AC/OPEN/CR/T；找不到 → 标 GAP，不硬套。 歧义（新 PRD 还是确认/哪个迭代）→ 一次一问；不猜。 更新 `{workroot}/INDEX.md`/`inbound/INDEX.md`；不直接覆盖正式文档；资料改名/落位/归档按 `rules/doc-governance.md` 确认后执行。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 技能 `product-doc-analysis`

> **条件加载**：仅当本步输入含 PRD/原型/产品文档时执行；否则标 na。

## 0. 必做

1. 列输入清单（路径+版本）；标主读 vs 对照；不能读的标 GAP，禁假装已读。  
2. 有单 HTML 原型 → 先解码模块再枚举页/路由/字段/状态/交互（禁只搜原始 HTML）。  
3. 输出理解包 **§0 Brief + 差量表**（无 §0 不拆单/不实施）。  
4. 冲突列双方原文 → OPEN/待确认；禁静默选边（除非用户声明 SSOT）。  
5. L1+ 用户可见变化 → 同轮用户版业务变化说明。  
6. 回执 `skills=product-doc-analysis`。

## 0.1 禁做

- 用 `activeContext`/旧评审代替原文。  
- 摘要未覆盖就开工 design/plan/implement。

## 0.1 禁做

- 用 `activeContext`/旧评审代替原文。  
- 摘要未覆盖就开工 design/plan/implement。
### 编排备忘

分类：PRD/需求/迭代/special/原型/设计/接口/技术/测试/验收/反馈/调研/竞品/会议/数据/原始/其他（细则 `rules/doc-governance.md` ）。 输入为 PRD/迭代方案/需求文档/原型/接口或技术文档 → 先按 `skills/product-doc-analysis/SKILL.md` 产出理解摘要（须含 Brief+本期差量增/改/删 + 来源/目标/范围/F-R-AC/冲突/GAP/置信度），再登记；不得只登记文件名。 登记：`inbound/` 文件给 DOC；变更给 CR；确认项关 OPEN 并写 DEC；原始资料只登记不升级基线。 关联：R/AC/OPEN/CR/T；找不到 → 标 GAP，不硬套。 歧义（新 PRD 还是确认/哪个迭代）→ 一次一问；不猜。 更新 `{workroot}/INDEX.md`/`inbound/INDEX.md`；不直接覆盖正式文档；资料改名/落位/归档按 `rules/doc-governance.md` 确认后执行。

## 6. 打开/填写

- 运行时正文：仅本文件（开局卡已在会话开头读过）。
- 无强制模板：直接写 §2 产出路径产物。

## 7. 完成信号

- §2 产出已落盘。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 8. 回执字段

```text
route=workflow:intake | step=classify | reads=rules/packets/intake/classify.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/intake/classify.md`；对不上 = 未遵守读链。
