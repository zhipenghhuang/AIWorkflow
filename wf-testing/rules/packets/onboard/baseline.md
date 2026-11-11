# 步骤卡 · onboard/baseline

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守；重读按 §7 分级）；方法在 §6 指定节（打开→执行→回包）。**未打开本文件=未开跑本步**。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`onboard` / `baseline`（挂载与基线）
- **packet**：`rules/packets/onboard/baseline.md`
- **角色**：`onboard-agent`（测试包接入）。挂载 → 基线关键节 → activeContext → 入库确认 → 环境与工具检查（默认静默） → 按接入清单核验；本步只做该角色职责；越界交回或升级。
- **上游**：`migrate`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`materials`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：挂载与基线
- **产出**：env-baseline.md（§1/§2.1/§2.2/§8）· {workroot}/work-log.md（如无）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：按 `rules/core/global-rules.md` §7 **分级重读并遵守**（中段=最小集，禁每步通读全文）；须先打开本步骤卡；心跳 `global=ok`=已按 §7 复核且步骤卡已实读；未复核不得写 `global=ok`。偏离写 `global=dev:<原因>`。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 挂载：按 `rules/templates/00-onboarding/root-agents-pointer.md` 补入薄指针（追加不覆盖）。
- 单包指向本包，多包指向 `wf/AGENTS.md`。
- 不写包装载说明。
- **按实填档（硬）**：建档前有界探查（预览地址/`{workroot}/`/既有计划若有）。
- 「项目身份」写 workroot（未声明按约定）、`integration_level`（绿场默认 I3，存量必问）、`inbound_structure`（默认 mix）、`流程偏好`（按计划与级别推断；用户可改，不额外提问）。
- 基线登录/设计输入/入库/浏览器能力索引节据实填。
- **禁止**占位符未换就打「wf-testing onboard: done」。
- 有根 `README.md` 则按**其实际结构**择要取用。
- 细则见 README：只写现行入口/运行/目录。
- 根 README 按用户偏好选档后写（模板仅素材）。
- 已有不覆盖。
- 点名生成/更新/整理时对照市面高标准给可选补强。
- 按 文档治理规则（工作根/原件根/索引/关版整夹） 定位工作根。
- 登记原件根 `inbound/INDEX.md`。
- 权威文档库 `docs/materials/`。
- 建索引：单包 `docs/INDEX.md`（含工作区导航）。
- 多包 `{workroot}/INDEX.md` + 总览 `docs/INDEX.md`（I2 在总览登记既有目录）。
- 不写阶段/门。
- 多包模式：根 `AGENTS.md` 只写薄指针（先读 `wf/AGENTS.md`）。
- 按 `rules/templates/00-onboarding/wf-agents-routing-template.md` 生成/补齐 `wf/AGENTS.md`，只列已装包。
- 已有则只补行，不覆盖。
- 接入级别：绿场默认 I3。
- 存量/杂乱必问。
- I0 只写现场树+映射，I2 新写只进标准树。
- 确认 `inbound_structure`（默认 mix）。
- 写 `env-baseline.md` 的 workroot `integration_level` `inbound_structure`。
- 建本包资料副本区骨架（可先空）。
- 禁 `项目文档/`。
- `{workroot}/work-log.md`：无则按模板创建。
- 已有跳过。
- 接入完成可追加事件=`接入/治理`。
- 若有 `{workroot}/CHANGELOG.md` 且无工作日志 → 改名候选（确认后执行）。
- **禁止**创建/修改/补链根 `CHANGELOG.md`（仅开发维护）。
- 无开发包 → 不建根。
- 岗位史只用本包工作日志。
- `env-baseline.md`：先填「项目身份」。
- 记原件根 `inbound/` + 本包副本根。
- 资料模式默认 mix（keep 仍可复制/吸收）。
- 存量全索引。
- 按需复制/A0～A2 吸收。
- **禁**类型前缀扁平。
- **禁**再建 `项目文档/`。
- 不建 `{workroot}/计划执行看板.md`。

### 本步规则卡：文档治理

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认后将 `{workroot}/{ver}/` **整夹**迁入 `_archive/{yyyyMMdd}-{ver}/`；常青仅 smoke/scripts/capabilities/handoff 台账；「并行不关」只落新资料、不归档现行主档。
- 清理只删已知临时/缓存/未引用失败产物；不确定移 `_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/00-onboarding/env-baseline-template.md`；只读本步用到的节，禁止整文件通读。
- **参考模板（命中再开，不默认读）**：`rules/templates/00-onboarding/root-agents-pointer.md`；`rules/templates/00-onboarding/wf-agents-routing-template.md`。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:onboard | step=baseline | agent=onboard-agent | packet=rules/packets/onboard/baseline.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
