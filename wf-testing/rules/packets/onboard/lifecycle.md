# 步骤包 · onboard/lifecycle

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-testing
- **workflow**：`onboard`
- **step**：`lifecycle`（文档治理检查）
- **packet**：`rules/packets/onboard/lifecycle.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/onboard/_chain.md`（进 workflow 一次）。

## 2. 本步目标

- **目标**：文档治理检查
- **产出**：【文档治理检查】（确认后执行更新/归档/清理）

## 3. 本步硬约束

### 开局硬约束（本步可执行摘要）

- 1. **先意图、再动作**（`confirm_task_intent`）：未确认禁生成正式用例/交平台。
- 2. **短读跟随 + 一手源**：`activeContext` + 进行中（`packet=`/`region=`）+ 偏好/洞见/坑 ≤3。
- 3. **依据先建模**：分析表 §0；无 §0 禁正式生成与功能准出。
- 4. **状态机读链 + 技能闭环**：见本包「本步读链与防丢失」。必开 skill 须打开→执行→回步骤包（质量不降）。
- 5. **完成分层**：`-Claim -Mode report|writeback` → 只认 `CLAIM: ALLOWED`。
- 6. **UI 证据 E1**：实点 + 截图/Network；E0 不得单独 pass。
- 7. **能脚本不 AI**；禁刷绿；P0 未过不得整体通过。
- 8. **切步/出子机 → 心跳**，必带 `packet=`。

### 本步读链与防丢失

- **编排**：本文 §5 +（若 §7 列出）一个模板。
- **方法质量**：§6 必开/条件开技能 → **打开→执行→回本包**（同时 1 个 skill）；禁止用粘贴代替实读。
- **禁止**：通读 rules / 多 step packet / 预读本 workflow 全部 skill。
- **完成声称**：有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **上下文锚**：`packet=`/`reads=` 必须含本 packet；切步/出子机前心跳刷新。


## 4. 本步门

- **HITL `confirm_docs_migration`**：资料收取/分类/改名/归档、或旧结构迁移前列清单与目标；确认后执行

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 按 `rules/doc-governance.md` ～、 与 `rules/workflow.md` 扫描（本步=点名清理/巡检入口）： ① 分类：长期/固定、版本/迭代绑定、失效/替代、过程/临时。
- ② 判定：长期就地更新。
- 版本绑定关闭时快照/归档。
- 部分覆盖保留。
- 失效确认后归档。
- **已完结**临时/失败/重复（含已完结 `.draft/`）列清理候选。
- ②.1 归档前做引用检查：被当前计划/用例/脚本/报告引用的设计输入、测试数据、稳定冒烟清单保留原位或标“基线”，不标失效。 ③ 输出【文档治理检查】：保留/更新/归档/清理/待确认。
- **确认前不改/不移/不删**。 有候选 → `docs_migration_needed=true`，停在本门等确认。
- 无候选 → 报「无生命周期候选」，不改文件。 关账按 `rules/doc-governance.md` ：主计划/四卷/报告/CR/交接落 `{workroot}/_archive/`。
- **功能/接口域主档常青留下**。
- 轨内 `_archive/` 仅下线域/重生快照/旧探索轮。
- 失效资料落 `inbound/INDEX.md 状态`。 清理只删已知临时/缓存/未引用失败产物与过期运行态（`.gate/wf-testing/` 非 JSON 媒体、`.gate/logs`）。
- 进行中 draft、现行证据（含仍被报告引用的失败实拍）、当前计划/报告、源文件、用户文件、密钥永不自动删除。
- 不确定移 `{workroot}/_archive/_pending-cleanup/{yyyyMMdd}/` 并写清理清单。

## 6. 技能指向（打开 → 执行 → 回本包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/onboard/_chain.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:onboard | step=lifecycle | packet=rules/packets/onboard/lifecycle.md | reads=rules/packets/onboard/lifecycle.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/onboard/lifecycle.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
