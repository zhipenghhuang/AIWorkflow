# 步骤包 · materials/sync

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：开发
- **workflow**：`materials`
- **step**：`sync`（同步权威文档）
- **packet**：`rules/packets/materials/sync.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/materials/_chain.md`（进 workflow 一次）。

## 2. 本步目标

- **目标**：同步权威文档
- **产出**：docs/materials/{ver}/（00-overview～07-appendix，按需）

## 3. 本步硬约束

### 开局硬约束（本步可执行摘要）

- 1. **先意图、再动作**（`confirm_task_intent`）：新开先【需求与意图理解】再确认；未确认禁改代码/外发/下完成结论。
- 2. **短读跟随 + 一手源**：`activeContext` + 进行中（`rule_card`/`packet=`/`region=`）+ 偏好/洞见/坑 ≤3。
- 3. **状态机读链（硬）**：见本包「本步读链与防丢失」。父流程可拆子机；同时只激活**一个**步骤包。
- 4. **技能闭环（质量不降）**：步骤包 §6 标**必开**的 skill 必须打开→按必做执行→**回到步骤包**；禁止把 skill 正文嵌进步骤包替代实读；禁止跳过必开 skill。
- 5. **完成分层**：`verify/Invoke-Gate.ps1 -Claim` → 只认 `CLAIM: ALLOWED`。无 ALLOWED 禁止写「已通过」。
- 6. **前端硬门**：有 UI → 当前步骤包内前端硬门；无 UI 标 `na`。
- 7. **证据先于结论；禁刷绿**；密钥零入库；最小改动；失败同方案 2 次换路径。
- 8. **切步/出子机 → 心跳一行**，必须带 `packet=`（有子机带 `region=`）。

### 本步读链与防丢失

- **编排**：本文 §5 +（若 §7 列出）一个模板。
- **方法质量**：§6 必开/条件开技能 → **打开→执行→回本包**（同时 1 个 skill）；禁止用粘贴代替实读。
- **禁止**：通读 rules / 多 step packet / 预读本 workflow 全部 skill。
- **完成声称**：有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **上下文锚**：`packet=`/`reads=` 必须含本 packet；切步/出子机前心跳刷新。


## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 从 `{workroot}` 选当前定稿，按域**覆盖复制**到 `docs/materials/{ver}/`。
- 从 `inbound/` 选权威正确外部输入， 按域放入同一版本。
- 不按 inputs/deliverables 分栏，来源写 `docs/materials/INDEX.md`。 每个 `{ver}/` 自包含。
- 不建外挂 `_common/`。
- 不设 `_archive/`。
- 旧版本目录保留。 默认就地覆盖已有文件。
- 仅显式保留历史时写入 `{ver}-r2` 或升 rev，不覆盖旧目录。 不直接编辑材料库正文。
- 需要改先改 `{workroot}` 再重新发布（默认仍覆盖同 ver）。

## 6. 技能指向（打开 → 执行 → 回本包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/materials/_chain.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 无强制模板：直接写 §2 产出路径产物。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:materials | step=sync | packet=rules/packets/materials/sync.md | reads=rules/packets/materials/sync.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/materials/sync.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
