# 步骤包 · materials/index

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-testing
- **workflow**：`materials`
- **step**：`index`（版本说明、索引与校验）
- **packet**：`rules/packets/materials/index.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/materials/_chain.md`（进 workflow 一次）。

## 2. 本步目标

- **目标**：版本说明、索引与校验
- **产出**：docs/materials/{ver}/README.md + docs/materials/INDEX.md + 【材料库校验】通过/待补

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

- **GATE `materials-validate`**：**checklist**：README/INDEX 齐；所有文件有登记；来源可解析；无草稿/证据/密钥/PII；链接自包含；旧版本状态正确；不通过不称完整。

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

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

## 6. 技能指向（打开 → 执行 → 回本包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 打开/填写

- 本步正文：本步骤包（编排/门/完成）。
- 父状态机（进 wf 一次）：`rules/packets/materials/_chain.md`。
- 技能：按 §6 **必开/条件开** 闭环（打开→执行→回本包），质量不降。
- 验证：`verify/Invoke-Gate.ps1`（完成声称加 `-Claim`）；有 UI 另按 §5 前端硬门。

## 8. 完成信号

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:materials | step=index | packet=rules/packets/materials/index.md | reads=rules/packets/materials/index.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/materials/index.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
