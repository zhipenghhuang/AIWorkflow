# 步骤卡 · onboard/profile

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`onboard` / `profile`（产品档案与上下文）
- **packet**：`rules/packets/onboard/profile.md`
- **角色**：`onboard-agent`（产品包接入）。挂载验收 → 生成产品档案/activeContext → 确认入库 →（可选）能力检查 → 按接入清单核验 → 写入接入标记；本步只做该角色职责；越界交回或升级。
- **上游**：`mount`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`materials`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。

## 2. 本步目标

- **目标**：产品档案与上下文
- **产出**：product-profile.md · activeContext.md · {workroot}/work-log.md（如无）·（模板见 §7）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

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

- **按实填档（硬）**：建档前有界探查（`{workroot}/`、既有 PRD/计划/用户材料若有）。
- 档案第一节须含一句话定位、目标用户、workroot（未声明按约定）、`integration_level`（绿场默认 I3，存量必问）、`inbound_structure`（默认 mix）。
- 第二～四节据实填或「无」/「待确认」。
- `流程偏好` 按计划与 PRD 存量推断（轻量优先/完整优先；用户可改，不额外提问；轻量≠降 AC/门/评审）。
- **禁止**占位符未换就打「wf-product onboard: done」。
- 有根 `README.md` 则按**其实际结构**择要取用。
- 细则见 README：只写现行入口/运行/目录。
- 根 README 按用户偏好选档后写（模板仅素材）。
- 已有不覆盖。
- 点名生成/更新/整理时对照市面高标准给可选补强。
- 缺陷平台可选：问是否启用禅道/Jira/ONES，启用填 provider/baseUrl/凭据来源/提交方式/适配定义， 未启用写「无」。
- 同项目已有开发/测试包配置可复用，不重复存凭据。
- 缺陷平台未配置不阻塞接入。
- `activeContext.md`：无则按 `rules/templates/00-onboarding/active-context-template.md` 建（**总览一句话** + `## 产品` + 跨包同步 + 运行时本包行）。
- 已有则只补/更新总览（若空）、本包分节与本包接入行，禁止整文件覆盖他包内容。
- 总览口径对齐产品档案「一句话定位」。
- `{workroot}/work-log.md`：无则按 `rules/templates/00-onboarding/work-log-template.md` 创建（岗位里程碑侧记；索引可空）。
- 已有则跳过不覆盖。
- 接入完成可追加事件=`接入/治理`。
- **不是**根 `CHANGELOG.md`、也不是产品计划 执行日志。
- 勿把本文件当产品发版史。
- 若仍存在 `{workroot}/CHANGELOG.md` 且尚无 `{workroot}/work-log.md`：列为改名迁移候选（→`work-log.md`），经 `confirm_docs_migration` 确认后执行。
- 未确认不改。
- **禁止**创建/修改/补链项目根 `CHANGELOG.md`（仅开发维护）。
- 无开发包 → 不建根 CHANGELOG。
- 岗位史只用本包工作日志。
- 用户点名要项目发版史 → 建议接入开发包或由其指定写手。
- 本包默认不替建。
- 按 文档治理规则（工作根/原件根/索引/关版整夹） 定位工作根。
- 登记原件根 `inbound/INDEX.md`。
- 权威文档库 `docs/materials/`。
- 建 `docs/materials/INDEX.md` 骨架。
- 外部输入先入 `inbound/`。
- 建索引：单包 `docs/INDEX.md`（含工作区导航）。
- 多包 `{workroot}/INDEX.md` + 总览 `docs/INDEX.md`（I2 在总览登记既有目录）。
- 不写阶段/门。
- 产品档案 增记工作根 `inbound/` 原件根 `docs/materials/` 权威文档库。
- 对外用户文档固定 `{workroot}/user/`，不混入 `inbound/`。

### 本步规则卡：文档治理

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认后将迭代绑定文档迁入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`；主档关闭时快照、主档不移动；「并行不关」只落新资料、不归档现行主档。
- 清理只删已知临时/缓存/未引用失败产物；不确定移 `_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读技能库找感觉。

## 7. 模板与证据

- **填写模板（主）**：`rules/templates/00-onboarding/product-profile-template.md`；只读本步用到的节，禁止整文件通读。
- **配套模板（按产出需要读；门按结构判分的产物须对齐）**：`rules/templates/00-onboarding/active-context-template.md`；`rules/templates/00-onboarding/work-log-template.md`；`rules/templates/00-onboarding/workspace-index-template.md`；`rules/templates/00-onboarding/project-overview-index-template.md`；`rules/templates/00-onboarding/project-readme-template.md`。
- **产出前自检**：对照模板必填节逐项填写；缺节、空节、未替换 `{…}` = 不合格（不得标完成）。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- §2 产出已按模板必填节落地；无空节、无未替换占位符。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:onboard | step=profile | agent=onboard-agent | packet=rules/packets/onboard/profile.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
