# 步骤包 · defect/apply

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`defect`
- **step**：`apply`（联动与评审）
- **packet**：`rules/packets/defect/apply.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：联动与评审
- **产出**：受理单 §6 + 变更单/最新 PRD/AC/计划/UAT + 缺陷处置单 + 附件清单

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- **仅在 decide 确认后执行**；纯拉取/只读分析止于 analyze，不落处置单。 **产品缺陷才更新 PRD/AC/计划/UAT**；实现defects/非问题/重复/信息不足只产缺陷处置单与回执，不进入 PRD/AC 更新。 即使无需联动，也至少落缺陷处置单/受理单回执；不适用项写原因。 按 `workflows/change.yaml` 的 apply 规则更新 PRD/AC/原型/交付计划/产品计划/需求池/UAT/发布检查； 已有受理单（pull 建档）就地更新，不重复建档；同一缺陷多轮处理只留一份现行受理单。 产品缺陷确认 → 产出 `{workroot}/{ver}/30-changes/缺陷处置-{BUG-ID}-{主题}-{yyyyMMdd}.md` （模板 `rules/templates/30-review-change/product-defect-disposition-template.md`），写清判定、依据、新口径、对开发要求、验收标准、指派对象。 实现defects/非问题/重复/信息不足也产出缺陷处置单（说明+下一步+指派），不要求 PRD 变更。 实质变更 → 走 review 步（产品视角：是否解决原问题/AC 影响/范围/风险；不评价技术实现细节）。 生成回写附件：缺陷处置单/受理单/变更单/评审意见/PRD 变更摘要（按需）；不修改代码或技术方案。 **缺陷双通道**：本步已回写平台 → **不**再强制 `BUG` 整包。无平台/`export`/用户点名「缺陷交接包」→ **先问后发**，确认后 `handoff.send` 自包含处置详单。平台附件与包内口径同源，禁重复造口径。 联动审计（子代理编排 ）：≥4 份受影响文档 → 单写手完成后派 verifier-agent 只读核验（受理单 ＋改动产物），返回未更新/旧口径/待补 ≤30 行。 三包独立：产品文档落本包目录，附件上传平台；不引用开发/测试包内部路径。 平台附件/开发评估单/新产品文档：先按 `rules/doc-governance.md` 【入站

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 技能 `change-management`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「先改 PRD 再说」 | 未分诊/未评估不得改基线；先受理分类再 apply。 |
| 「紧急上线可跳变更单」 | 无单不实施；紧急也要事后留痕与门对齐。 |
| 「实现缺陷当产品缺陷开」 | 须 PRD 原文+现网证据；实现问题退回开发/测试。 |
| 「口头答应客户就算变更」 | 未确认范围/优先级不得入池承诺。 |
### 编排备忘

**仅在 decide 确认后执行**；纯拉取/只读分析止于 analyze，不落处置单。 **产品缺陷才更新 PRD/AC/计划/UAT**；实现defects/非问题/重复/信息不足只产缺陷处置单与回执，不进入 PRD/AC 更新。 即使无需联动，也至少落缺陷处置单/受理单回执；不适用项写原因。 按 `workflows/change.yaml` 的 apply 规则更新 PRD/AC/原型/交付计划/产品计划/需求池/UAT/发布检查； 已有受理单（pull 建档）就地更新，不重复建档；同一缺陷多轮处理只留一份现行受理单。 产品缺陷确认 → 产出 `{workroot}/{ver}/30-changes/缺陷处置-{BUG-ID}-{主题}-{yyyyMMdd}.md` （模板 `rules/templates/30-review-change/product-defect-disposition-template.md`），写清判定、依据、新口径、对开发要求、验收标准、指派对象。 实现defects/非问题/重复/信息不足也产出缺陷处置单（说明+下一步+指派），不要求 PRD 变更。 实质变更 → 走 review 步（产品视角：是否解决原问题/AC 影响/范围/风险；不评价技术实现细节）。 生成回写附件：缺陷处置单/受理单/变更单/评审意见/PRD 变更摘要（按需）；不修改代码或技术方案。 **缺陷双通道**：本步已回写平台 → **不**再强制 `BUG` 整包。无平台/`export`/用户点名「缺陷交接包」→ **先问后发**，确认后 `handoff.send` 自包含处置详单。平台附件与包内口径同源，禁重复造口径。 联动审计（子代理编排 ）：≥4 份受影响文档 → 单写手完成后派 verifier-agent 只读核验（受理单 ＋改动产物），返回未更新/旧口径/待补 ≤30 行。 三包独立：产品文档落本包目录，附件上传平台；不引用开发/测试包内部路径。 平台附件/开发评估单/新产品文档：先按 `rules/doc-governance.md` 【入站分析】（多为 T6）；确认后落 `inbound/{ver|topic}/`，同步处置结论到工作区；S1/S2/S3 同批进 `inbound/_archive/`。

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
route=workflow:defect | step=apply | reads=rules/packets/defect/apply.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/defect/apply.md`；对不上 = 未遵守读链。
