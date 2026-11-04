# 步骤包 · intake/parse

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`intake`
- **step**：`parse`（解析与理解）
- **packet**：`rules/packets/intake/parse.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：解析与理解
- **产出**：资料理解摘要（Brief+本期差量 + 来源/目标/范围/F-R-AC/冲突/GAP/置信度）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 技能：`skills/product-doc-analysis/SKILL.md`（先读再做）；只读解析，不直接改基线。 输入含 PRD/迭代方案/需求文档/原型/接口/技术文档 → 产出理解摘要（含 Brief+增/改/删差量）；每条结论标 `[原文]`/`[推断]`/`[假设]`/`[待确认]`/`[GAP]` 并引用章节/页码/页面/组件。 重点：本期差量、目标与非目标、角色/场景、F/R/AC、状态机、权限、字段口径、异常/NFR、原型、文档间/原型/代码冲突、缺口与假设。 原型只作 UI/交互依据，不反推后端规则；冲突列双方原文，待用户裁决。 一次一问至无实质缺口（`rules/core/clarification.md`）；未确认不得进入 impact/absorb。 confirm_understanding：出示 Brief+差量表 + 来源/目标/范围/非目标/F-R-AC/冲突/GAP/置信度；用户明确确认后才继续；已确认内容不重复问。 理解摘要登记到 `{workroot}/INDEX.md`/`inbound/INDEX.md`；实质吸收可落理解包 ；不新建重复文档、不改基线正文。

## 4. 本步门

- **HITL `confirm_understanding`**：**主屏**：§0【业务与变更简报】+【本期差量表】（增/改/删）+ 待确认单摘要（冲突·GAP·开发择优/置信度）；完整理解包作下钻链接。无 §0/差量表不得过门（L0 迷你 Delta 除外）。确认后才进需求基线/设计/实施/拆单

## 5. 做法

### 技能 `change-intake`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「先塞进待办再看」 | 先分流/分级/影响面，再入受理；禁止未读资料开写。 |
| 「交接包放一下就算接收」 | 入站须分析吸收；未回执不得称已接收。 |
| 「小补充不用记变更」 | 改基线/AC 必须留痕；否则后续无法追溯。 |
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
### 技能 `requirements-and-spec`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「先写方案细节再补 AC」 | AC/边界不清不开设计；理解包缺口先问。 |
| 「推断当确认」 | 未确认标假设；不得当已定事实进任务。 |
| 「QA-AC 也算开发范围」 | 只认 DEV-AC；QA/REL 转交接，不写进开发任务。 |
### 编排备忘

技能：`skills/product-doc-analysis/SKILL.md`（先读再做）；只读解析，不直接改基线。 输入含 PRD/迭代方案/需求文档/原型/接口/技术文档 → 产出理解摘要（含 Brief+增/改/删差量）；每条结论标 `[原文]`/`[推断]`/`[假设]`/`[待确认]`/`[GAP]` 并引用章节/页码/页面/组件。 重点：本期差量、目标与非目标、角色/场景、F/R/AC、状态机、权限、字段口径、异常/NFR、原型、文档间/原型/代码冲突、缺口与假设。 原型只作 UI/交互依据，不反推后端规则；冲突列双方原文，待用户裁决。 一次一问至无实质缺口（`rules/core/clarification.md`）；未确认不得进入 impact/absorb。 confirm_understanding：出示 Brief+差量表 + 来源/目标/范围/非目标/F-R-AC/冲突/GAP/置信度；用户明确确认后才继续；已确认内容不重复问。 理解摘要登记到 `{workroot}/INDEX.md`/`inbound/INDEX.md`；实质吸收可落理解包 ；不新建重复文档、不改基线正文。

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
route=workflow:intake | step=parse | reads=rules/packets/intake/parse.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/intake/parse.md`；对不上 = 未遵守读链。
