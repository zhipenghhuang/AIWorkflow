# 步骤包 · materials/index

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`materials`
- **step**：`index`（版本说明、索引与校验）
- **packet**：`rules/packets/materials/index.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：版本说明、索引与校验
- **产出**：docs/materials/{ver}/README.md + docs/materials/INDEX.md + 【材料库校验】通过/待补

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- README 写版本、范围、包含/不包含、阅读顺序、来源、缺失/待补、本次是否覆盖刷新。 INDEX 登记所有文件：版本/域/文档/来源（IN-xxxx、docs/... 或 generated）/状态/更新时间；刷新 `last_published_at`。 状态只写 `current / superseded`；默认覆盖同 ver；仅显式保留历史时升 `rev` 或 `{ver}-r2`。 **门（materials-validate）**：README/INDEX 齐；所有文件有登记；来源可解析；无草稿/证据/密钥/PII； 链接自包含，只发 `{ver}/` 不缺文件；测试数据默认不外发；旧版本状态正确。 待补项列明，不把“已生成”说成“已完整”。

## 4. 本步门

- **GATE `materials-validate`**：**checklist**：README/INDEX 齐；所有文件有登记；来源可解析；无草稿/证据/密钥/PII；链接自包含；旧版本状态正确；不通过不称完整。

## 5. 做法

### 本步动作清单

- README 写版本、范围、包含/不包含、阅读顺序、来源、缺失/待补、本次是否覆盖刷新。 INDEX 登记所有文件：版本/域/文档/来源（IN-xxxx、docs/... 或 generated）/状态/更新时间。
- 刷新 `last_published_at`。 状态只写 `current / superseded`。
- 默认覆盖同 ver。
- 仅显式保留历史时升 `rev` 或 `{ver}-r2`。 **门（materials-validate）**：README/INDEX 齐。
- 所有文件有登记。
- 来源可解析。
- 无草稿/证据/密钥/PII。
- 链接自包含，只发 `{ver}/` 不缺文件。
- 测试数据默认不外发。
- 旧版本状态正确。 待补项列明，不把“已生成”说成“已完整”。

## 6. 打开/填写

- 运行时正文：仅本文件（开局卡已在会话开头读过）。
- 验证：`verify/Invoke-Gate.ps1`（完成声称加 `-Claim`）；有 UI 另按包内前端条。

## 7. 完成信号

- §2 产出已落盘。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 8. 回执字段

```text
route=workflow:materials | step=index | reads=rules/packets/materials/index.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/materials/index.md`；对不上 = 未遵守读链。
