# 步骤包 · onboard/profile

> **状态 = 本 step（独立完整）**。全局硬约束见 §3（每步遵守）；本步门/编排/完成见本文；**方法在 §6 skill**（打开→执行→回来）。  
> 与开局卡/他步条文重复 OK；不要跳转拼流程；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-product
- **workflow**：`onboard`
- **step**：`profile`（产品档案与上下文）
- **packet**：`rules/packets/onboard/profile.md`
- **角色**：`onboard-agent`（产品包接入）。挂载验收 → 生成产品档案/activeContext → 确认入库 →（可选）能力检查 → 按接入清单核验 → 写入接入标记；本步只做该角色职责；越界交回或升级。
- **上游**：`mount`（取其产出为本步输入；该步被 `when` 跳过时按缺口停/补齐）
- **后续**：`materials`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：进 wf 时读 `_chain` 一次；**中段勿重读**。

## 2. 本步目标

- **目标**：产品档案与上下文
- **产出**：product-profile.md · activeContext.md · {workroot}/work-log.md（如无）·（模板 rules/templates/）

## 3. 本步硬约束

### 全局硬约束（本包已带齐 · 每步都遵守）

- 1. 先判后动；未确认禁写/禁结论；批量不豁免。
- 2. 先查事实；仍不明一次一问（附候选/推荐）。
- 3. 核前提/来源/变量/成本；不迎合；用户有误直接指出。
- 4. 劣解先说依据+主推；用户坚持记 `deviation=`。
- 5. 先权衡；失败 2 次换路径。
- 6. 改前说文件；最小改动；超范围先停。
- 7. 完成只认 `Invoke-Gate.ps1 -Claim -Mode <…>` → `CLAIM: ALLOWED`；原型实走+覆盖矩阵；UAT 未过不发布。
- 8. 收尾六点；只读 2～3 行；主动发现 ≤3。
- 9. 只写现行；删除即移除；不写历史/旧方案。
- 10. 读链：开局卡 → `_chain` → 当前包 → §6 skill → 模板 ≤1；同时只 1 包。
- 11. §6 必开 skill 打开→执行→回包；禁粘贴代替。
- 12. 切步/过门心跳带 `packet=`/`role=`/`task=`；长任务先报进展。
- 13. 用户当轮指令优先；与硬门冲突先说明再二选一。
- 14. 证据先于结论；禁刷绿；密钥零入库。
- **效力**：以上为执行摘要（全文见开局卡 §1）；开局已读则中段不重开全文，**每步仍须逐条遵守**；与开局卡重复不影响。

### 本步操作面（本链本步独立完整）

- **读这些就能干完本步**：本文（全局摘要 + §4 门 + §5 编排）+ §6 表内 skill（一次 1 个闭环）+（若 §7 列出）至多 1 模板。
- **不靠跳转拼流程**：本步所需规则已写在本文；他步/他链可有相同条文，互不依赖。
- **完成声称**：有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **上下文锚**：`packet=`/`reads=` 必须含本 packet；切步前心跳刷新。

### 本步禁止

- 禁止用 read-index / 他步 packet /「详见别处 rules」拼本步流程。
- 禁止跳过 §6 必开技能，或用摘要代替实读。
- 禁止未过 §4 门或未出 §8 信号就宣称完成、推进或写「已通过」。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- **按实填档（硬）**：建档前有界探查（`{workroot}/`、既有 PRD/计划/用户材料若有）。档案第一节须含一句话定位、目标用户、workroot（未声明按约定）、`integration_level`（绿场默认 I3，存量必问）、`inbound_structure`（默认 mix）。
- 第二～四节据实填或「无」/「待确认」。
- `流程偏好` 按计划与 PRD 存量推断（轻量优先/完整优先。
- 用户可改，不额外提问。
- 轻量≠降 AC/门/评审）。**禁止**占位符未换就打「wf-product onboard: done」。 有根 `README.md` 则按**其实际结构**择要取用。
- 细则见 README：只写现行入口/运行/目录。根 README 按用户偏好选档后写（模板仅素材）。
- 已有不覆盖。
- 点名生成/更新/整理时对照市面高标准给可选补强。 缺陷平台可选：问是否启用禅道/Jira/ONES，启用填 provider/baseUrl/凭据来源/提交方式/适配定义， 未启用写「无」。
- 同项目已有开发/测试包配置可复用，不重复存凭据。缺陷平台未配置不阻塞接入。 `activeContext.md`：无则按 `rules/templates/00-onboarding/active-context-template.md` 建（**总览一句话** + `## 产品` + 跨包同步 + 运行时本包行）。
- 已有则只补/更新总览（若空）、本包分节与本包接入行，禁止整文件覆盖他包内容。总览口径对齐产品档案「一句话定位」。 `{workroot}/work-log.md`：无则按 `rules/templates/00-onboarding/work-log-template.md` 创建（岗位里程碑侧记。
- 索引可空）。已有则跳过不覆盖。接入完成可追加事件=`接入/治理`。 **不是**根 `CHANGELOG.md`、也不是产品计划 执行日志。
- 勿把本文件当产品发版史。 若仍存在 `{workroot}/CHANGELOG.md` 且尚无 `{workroot}/work-log.md`：列为改名迁移候选（→`work-log.md`），经 `confirm_docs_migration` 确认后执行。
- 未确认不改。 **禁止**创建/修改/补链项目根 `CHANGELOG.md`（仅开发维护）。无开发包 → 不建根 CHANGELOG。
- 岗位史只用本包工作日志。用户点名要项目发版史 → 建议接入开发包或由其指定写手。
- 本包默认不替建。 按 本包 §5 文档治理规则 定位工作根。
- 登记原件根 `inbound/INDEX.md`。
- 权威文档库 `docs/materials/`。 建 `docs/materials/INDEX.md` 骨架。
- 外部输入先入 `inbound/`。 建索引：单包 `docs/INDEX.md`（含工作区导航）。
- 多包 `{workroot}/INDEX.md` + 总览 `docs/INDEX.md`（I2 在总览登记既有目录）。
- 不写阶段/门。 产品档案 增记工作根 `inbound/` 原件根 `docs/materials/` 权威文档库。 对外用户文档固定 `{workroot}/user/`，不混入 `inbound/`。

### 本步规则卡：文档治理

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认结束当前迭代后，主计划/四卷/报告/CR/交接落 `{workroot}/_archive/`；「并行不关」只落新资料，不归档现行主档。
- 清理只删已知临时/缓存/未引用失败产物；不确定移 `_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。

## 6. 技能指向（打开 → 执行 → 回本包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 打开/填写

- **本步完整面**：本步骤包（§3 全局摘要 + §4 门 + §5 规则卡/编排）+ §6 必开/条件开 skill（一次 1 个）+ 本步输入。
- **填写模板（仅此一份）**：`rules/templates/00-onboarding/active-context-template.md`；`rules/templates/00-onboarding/work-log-template.md`；只读本步用到的节，禁止整文件通读。
- 本步不再读 read-index / 他步 packet / 大手册；模板与 skill 只读指定节。

## 8. 完成信号

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:onboard | step=profile | agent=onboard-agent | packet=rules/packets/onboard/profile.md | reads=rules/packets/onboard/profile.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/onboard/profile.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
