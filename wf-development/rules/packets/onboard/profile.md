# 步骤卡 · onboard/profile

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`onboard` / `profile`（档案与规范）
- **packet**：`rules/packets/onboard/profile.md`
- **角色**：`onboard-agent`（开发包接入）。挂载验收 → 生成档案/规范/activeContext → 文档树/索引/归档 → 确认入库 → 环境与工具检查（默认静默） → 按接入清单核验；本步只做该角色职责；越界交回或升级。
- **上游**：`mount`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`migrate`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：档案与规范
- **产出**：project-profile.md（含 §7 技术要点事实摘要 / §8 交付治理 / §9 文档归档）· activeContext.md

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

- **按实填档（硬）**：建档前有界探查仓库实情（依赖/目录/入口/构建与测试命令）。
- 有根 `README.md` 则按**其实际结构**择要取用（不规定章节，见 README：只写现行入口/运行/目录）。
- 按 rules/templates/00-onboarding/project-profile-template.md 建档。
- 一句话定位、workroot（未声明按约定）、`integration_level`（绿场默认 I3，存量必问）、`inbound_structure`（默认 mix）、 代码地图/门禁、/ 据实填或「无」/「待确认」。
- **禁止**占位符未换就打「wf-development onboard: done」。
- **根 README**：按用户偏好选档后写（见 README：只写现行入口/运行/目录）。
- 模板仅素材。
- 已有不覆盖。
- 点名生成/更新/整理时对照市面高标准给可选补强。
- 按 `rules/templates/00-onboarding/version-policy-template.md` 产 `{workroot}/60-release/versioning.md`（版本格式/升级/环境/tag/审批；不确定写「待确认」）。
- 记工作根、`inbound/` 原件根、`docs/materials/` 权威文档库。
- 按实际参与角色填 `协作模式`（无事实写「待确认」）。
- `流程偏好` 仅作提示，不覆盖正式协作/正式流程判定。
- 不因单包/无产物推断为单人。
- 轨道不由此字段决定。
- 自包含不降 AC/完成门/开发自验（`lightweight.md` ）。
- `activeContext.md`：无则按 `rules/templates/00-onboarding/active-context-template.md` 建（**总览一句话** + `## 开发` + 跨包同步 + 运行时本包行）。
- 已有则只补/更新总览（若空）、本包分节与本包接入行，禁止整文件覆盖他包内容。
- 总览口径对齐项目档案「一句话定位」。
- 认根：用户指定优先。
- 否则按 文档治理规则（工作根/原件根/索引/关版整夹）。
- 不确定问用户。
- 登记后默认 `mix`。
- 可改 keep/replace。
- 工作根按 定位（档案声明优先，否则单包 `docs/`、多包 `docs/development/`）。
- 技术要点少 → 内联档案 事实摘要（勿为几行另建目录）。
- 无对应栈写「不适用」。
- 旧结构迁移（一次性）：检测到 `项目规范/` 目录 → 一问：并入 事实摘要并删除目录（默认建议）。
- 产出后进入 docs 步建立文档树/索引。

### 本步规则卡：文档治理

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认后将迭代绑定文档迁入 `{workroot}/_archive/{yyyyMMdd}-{ver}/`；主档关闭时快照、主档不移动；「并行不关」只落新资料、不归档现行主档。
- 清理只删已知临时/缓存/未引用失败产物；不确定移 `_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/00-onboarding/project-profile-template.md`；只读本步用到的节，禁止整文件通读。
- **参考模板（命中再开，不默认读）**：`rules/templates/00-onboarding/version-policy-template.md`；`rules/templates/00-onboarding/active-context-template.md`。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:onboard | step=profile | agent=onboard-agent | packet=rules/packets/onboard/profile.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
