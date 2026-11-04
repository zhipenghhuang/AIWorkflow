# 步骤包 · onboard/lifecycle

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`onboard`
- **step**：`lifecycle`（文档治理检查）
- **packet**：`rules/packets/onboard/lifecycle.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：文档治理检查
- **产出**：【文档治理检查】（确认后执行更新/归档/清理）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 按 `rules/doc-governance.md` ～、 扫描工作文档与过程文件（本步=点名清理/巡检入口）： ① 分类：长期/固定、版本/迭代绑定、失效/替代、过程/临时； ② 判定：长期基线/项目档案就地更新；版本绑定方案/任务清单/UAT/提测单关闭时归档；部分覆盖保留；失效确认后归档；**已完结**临时/失败/重复列清理候选；用户可见版本关闭时根 `CHANGELOG.md` 同步发版史；里程碑关闭另在 `{workroot}/work-log.md` 记一条； ②.1 归档前做引用检查：被当前计划/技术设计/测试验收引用的方案、基础设计、流程图保留原位或标“基线”，不标失效。 ③ 输出【文档治理检查】：保留/更新/归档/清理/待确认；**确认前不改/不移/不删**。 有候选 → `docs_migration_needed=true`，停在本门等确认；无候选 → 报「无生命周期候选」，不改文件。 清理只删已知临时/缓存/未引用失败产物与过期运行态（`.gate/frontend` 旧截图、`.gate/wf-development/` 非 JSON 媒体、`.gate/logs`）；进行中 draft、现行证据、当前计划/方案/任务清单、源文件、用户文件、密钥、根 `CHANGELOG.md`、`{workroot}/work-log.md` 永不自动删除；不确定移 `{workroot}/_archive/_pending-cleanup/{yyyyMMdd}/` 并写清理清单。

## 4. 本步门

- **HITL `confirm_docs_migration`**：出示分类/覆盖对照/拟归档或清理清单与目标；确认后执行

## 5. 做法

### 本步动作清单

- 按 `rules/doc-governance.md` ～、 扫描工作文档与过程文件（本步=点名清理/巡检入口）： ① 分类：长期/固定、版本/迭代绑定、失效/替代、过程/临时。
- ② 判定：长期基线/项目档案就地更新。
- 版本绑定方案/任务清单/UAT/提测单关闭时归档。
- 部分覆盖保留。
- 失效确认后归档。
- **已完结**临时/失败/重复列清理候选。
- 用户可见版本关闭时根 `CHANGELOG.md` 同步发版史。
- 里程碑关闭另在 `{workroot}/work-log.md` 记一条。
- ②.1 归档前做引用检查：被当前计划/技术设计/测试验收引用的方案、基础设计、流程图保留原位或标“基线”，不标失效。 ③ 输出【文档治理检查】：保留/更新/归档/清理/待确认。
- **确认前不改/不移/不删**。 有候选 → `docs_migration_needed=true`，停在本门等确认。
- 无候选 → 报「无生命周期候选」，不改文件。 清理只删已知临时/缓存/未引用失败产物与过期运行态（`.gate/frontend` 旧截图、`.gate/wf-development/` 非 JSON 媒体、`.gate/logs`）。
- 进行中 draft、现行证据、当前计划/方案/任务清单、源文件、用户文件、密钥、根 `CHANGELOG.md`、`{workroot}/work-log.md` 永不自动删除。
- 不确定移 `{workroot}/_archive/_pending-cleanup/{yyyyMMdd}/` 并写清理清单。

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
route=workflow:onboard | step=lifecycle | reads=rules/packets/onboard/lifecycle.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/onboard/lifecycle.md`；对不上 = 未遵守读链。
