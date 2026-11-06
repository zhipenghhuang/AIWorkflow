# 步骤包 · onboard/migrate

> **状态 = 本 step（独立完整）**。全局硬约束见 §3（每步遵守）；本步门/编排/完成见本文；**方法在 §6 skill**（打开→执行→回来）。  
> 与开局卡/他步条文重复 OK；不要跳转拼流程；不要跳过必开 skill。

## 1. 元信息

- **包轨**：wf-testing
- **workflow**：`onboard`
- **step**：`migrate`（旧结构迁移）
- **packet**：`rules/packets/onboard/migrate.md`
- **角色**：`onboard-agent`（测试包接入）。挂载 → 基线关键节 → activeContext → 入库确认 → 环境与工具检查（默认静默） → 按接入清单核验；本步只做该角色职责；越界交回或升级。
- **上游**：无（链首）
- **后续**：`baseline`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/未命中时，可将预检标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。
- **父状态机**：进 wf 时读 `_chain` 一次；**中段勿重读**。

## 2. 本步目标

- **目标**：旧结构迁移
- **产出**：迁移清单/更新后的路径

## 3. 本步硬约束

### 全局硬约束（本包已带齐 · 每步都遵守）

- 1. 先判后动；未确认禁写/禁结论；批量不豁免。
- 2. 先查事实；仍不明一次一问（附候选/推荐）。
- 3. 核前提/来源/变量/成本；不迎合；用户有误直接指出。
- 4. 劣解先说依据+主推；用户坚持记 `deviation=`。
- 5. 先权衡；失败 2 次换路径。
- 6. 改前说文件；最小改动；超范围先停。
- 7. 完成只认 `-Claim -Mode report|writeback` → `CLAIM: ALLOWED`；P0 未过不得整体通过；UI 证据 E1 实点+截图/Network。
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

- **HITL `confirm_docs_migration`**：资料收取/分类/改名/归档、或旧结构迁移前列清单与目标；确认后执行
- **条件判定 `hitl:docs_migration_needed`**：本步将搬迁/归档/清理 inbound 或工作文档且尚未确认清单；满足→真，否则跳过该门。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步工作规则（编排）

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 「重新接入」先扫描旧结构，列出迁移清单与目标，经 `confirm_docs_migration` 确认后执行，不静默丢文件。
- 不重复问同一迁移。 建齐本包按需副本树。
- 旧包内 `inbound/项目文档/{ver}/` → `inbound/{ver}/`。原件根 `inbound/`文件**不迁入**包内。
- 认根按文档治理。`keep`/`mix`/`replace` 只管原树，仍可索引/复制/吸收。 错位归档纠正：根 `{workroot}/_archive/` 内各轨资产 → 各自轨 `_archive/`。
- 散落失效资料 → `inbound/INDEX.md 状态`。
- 列清单确认后执行。 `docs/materials/{ver}/05-testing/test-data/` 保持。
- `{workroot}/测试用例/`+`{workroot}/执行台账/` → `{workroot}/functional/{NN}-{短名}/*-功能用例.md`+`*-功能台账.md`。
- 接口同理 `*-接口用例/台账`。
- 旧平铺下次迁入。
- `{workroot}/测试脚本/` → `{workroot}/scripts/`。
- `{workroot}/变更记录/` → `{workroot}/changes/`。
- `{workroot}/pre-release/{专项}/` 保持，性能/安全/兼容各自独立。
- `{workroot}/计划执行看板.md` → 合并进 `{workroot}/test-plan.md` 后删除。 资料迁移前先按 本包 §5 文档治理规则 做覆盖对照，输出迁移/改名/归档候选。
- 确认后执行，不静默丢文件。 若存在 `{workroot}/CHANGELOG.md`：列为迁移候选——**用户确认后**改名为 `{workroot}/work-log.md`（内容按工作日志模板整理索引+里程碑条。
- 勿与根 `CHANGELOG.md` 混淆）。
- 未确认不改名。 更新 `env-baseline.md`、测试计划/报告、`inbound/INDEX.md`、`docs/materials/INDEX.md`、activeContext。
- `activeContext` 合并节 `### 洞见 偏好 易踩坑` → 按 工作记忆：偏好/洞见/坑 ≤3 行 拆为 `### 生效中的偏好` + `### 洞见与易踩坑`，逐条补范围/期限/来源并删过期项。
- 不新增空节。旧路径不改则注明兼容，不强迁。 文件冲突/无法判断归属/三项混在一个方案 → 停下问一次，不擅自覆盖。 迁移后核对链接与引用，再进入 baseline/context。

### 本步规则卡：文档治理

- 外部输入先入站：落 `inbound/{ver|topic}/` 或 `_common/`；登记 `inbound/INDEX.md`；确认后才改名/归档；不把原件迁出 inbound。
- 迭代关账：确认结束当前迭代后，主计划/四卷/报告/CR/交接落 `{workroot}/_archive/`；「并行不关」只落新资料，不归档现行主档。
- 清理只删已知临时/缓存/未引用失败产物；不确定移 `_archive/_pending-cleanup/{yyyyMMdd}/` 并写清单。

## 6. 技能指向（打开 → 执行 → 回本包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 打开/填写

- **本步完整面**：本步骤包（§3 全局摘要 + §4 门 + §5 规则卡/编排）+ §6 必开/条件开 skill（一次 1 个）+ 本步输入。
- **无强制模板**：§5 规则卡已给出输出形状；直接落 §2 产出。
- 本步不再读 read-index / 他步 packet / 大手册；模板与 skill 只读指定节。

## 8. 完成信号

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 9. 回执字段

```text
route=workflow:onboard | step=migrate | agent=onboard-agent | packet=rules/packets/onboard/migrate.md | reads=rules/packets/onboard/migrate.md[+skill] | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```

`packet=` 必须含 `rules/packets/onboard/migrate.md`；必开 skill 须在本步内完成闭环。对不上 = 规则上下文已断或质量未达标。
