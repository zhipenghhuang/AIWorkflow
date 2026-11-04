# 步骤包 · materials/sync

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`materials`
- **step**：`sync`（同步权威文档）
- **packet**：`rules/packets/materials/sync.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：同步权威文档
- **产出**：docs/materials/{ver}/（00-overview～07-appendix，按需）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 从 `{workroot}` 选当前定稿，按域**覆盖复制**到 `docs/materials/{ver}/`；从 `inbound/` 选权威正确外部输入， 按域放入同一版本；不按 inputs/deliverables 分栏，来源写 `docs/materials/INDEX.md`。 每个 `{ver}/` 自包含；不建外挂 `_common/`；不设 `_archive/`；旧版本目录保留。 默认就地覆盖已有文件；仅显式保留历史时写入 `{ver}-r2` 或升 rev，不覆盖旧目录。 不直接编辑材料库正文；需要改先改 `{workroot}` 再重新发布（默认仍覆盖同 ver）。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 本步动作清单

- 从 `{workroot}` 选当前定稿，按域**覆盖复制**到 `docs/materials/{ver}/`。
- 从 `inbound/` 选权威正确外部输入， 按域放入同一版本。
- 不按 inputs/deliverables 分栏，来源写 `docs/materials/INDEX.md`。 每个 `{ver}/` 自包含。
- 不建外挂 `_common/`。
- 不设 `_archive/`。
- 旧版本目录保留。 默认就地覆盖已有文件。
- 仅显式保留历史时写入 `{ver}-r2` 或升 rev，不覆盖旧目录。 不直接编辑材料库正文。
- 需要改先改 `{workroot}` 再重新发布（默认仍覆盖同 ver）。

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
route=workflow:materials | step=sync | reads=rules/packets/materials/sync.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/materials/sync.md`；对不上 = 未遵守读链。
