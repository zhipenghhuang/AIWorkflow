# 步骤包 · onboard/gitignore

> **状态 = 本 step**。本文管编排与完成口径；**方法质量在 §6 指向的 skill**（打开→执行→回来）。  
> 不要把 skill 正文嵌进本文；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-development
- **workflow**：`onboard`
- **step**：`gitignore`（入库策略）
- **packet**：`rules/packets/onboard/gitignore.md`
- **轻量档**：L0/P0/T0 且本步无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：`rules/packets/onboard/_chain.md`（进 workflow 一次）。

## 2. 本步目标

- **目标**：入库策略
- **产出**：.gitignore 更新 + `git check-ignore` 证据

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

- **HITL `confirm_gitignore`**：四选一确认资产范围；规范包默认不跟踪，只写已装包一行（多包 `/wf/`），无注释、不预列未装包；其它项只列路径；写档案 §1 并改 `.gitignore`

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 四选一：①只忽略运行态/缓存。
- ②忽略产物+证据。
- ③忽略产物+证据+资料（保留模板）。
- ④自定义。 默认②。
- 写档案 、改 .gitignore。
- 密钥/凭据/本地日志不入库。
- `{workroot}/INDEX.md` 与正式文档按选择入库。 规范包默认不跟踪：只写已装包一行（如 `/wf-development/`），多包写 `/wf/`。
- 不预列未装包、不加注释。
- 其它项只列路径。

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
route=workflow:onboard | step=gitignore | packet=rules/packets/onboard/gitignore.md | reads=rules/packets/onboard/gitignore.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/onboard/gitignore.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
