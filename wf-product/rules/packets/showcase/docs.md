# 步骤卡 · showcase/docs

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`showcase` / `docs`（用户文档）
- **packet**：`rules/packets/showcase/docs.md`
- **角色**：`prd-writer`（PRD 撰写）。按模板落盘完整 PRD；要素齐、可测、无歧义；带缺口不落盘；本步只做该角色职责；越界交回或升级。
- **上游**：`materials`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`dryrun`（进 `dryrun` 前的 `when=demo_needs_dryrun`）
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **条件判定 `when:docs_requested`**：点名用户手册/快速开始/FAQ/发布说明/培训材料；满足→真，否则跳过本步（不打开本包）。

## 2. 本步目标

- **目标**：用户文档
- **产出**：{workroot}/user/{按点名类型}-{ver}.md（快速开始/用户手册/FAQ/发布说明/培训材料；未点名默认用户手册）

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

- **本步必开技能（质量不降）**：`product-docs` → 见 §6 闭环。

### 本步动作清单

- 点名用户手册/快速开始/FAQ/发布说明/培训材料 → `docs_requested=true`。
- 技能见 §6 `product-docs`。
- 模板 `rules/templates/50-showcase-docs/user-manual-quickstart-template.md`、`rules/templates/50-showcase-docs/release-notes-template.md`。
- 只产被点名的文档类型，不一次生成四类。
- 按任务组织：5 分钟快速开始 → 常用任务 → FAQ/故障 → 版本说明。
- 截图/步骤与当前构建一致。
- 同时产 ≥3 类文档 → 共享事实表 + 按类型分片（不同文件，单写手/类）。
- verifier-agent 核对数字/版本/截图/边界。
- 不并行写同一文档。
- 不写未发布功能。
- 客户版发布说明面向用户，不写内部实现与内部路径。
- 对外前由 `publish` 步确认。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。
> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `product-docs` | **必开** | 进入本步即开（质量不降） | `skills/product-docs/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/50-showcase-docs/user-manual-quickstart-template.md`；只读本步用到的节，禁止整文件通读。
- **参考模板（命中再开，不默认读）**：`rules/templates/50-showcase-docs/release-notes-template.md`。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:showcase | step=docs | agent=prd-writer | packet=rules/packets/showcase/docs.md | global=ok | skills=product-docs|done|na | claim=ALLOWED|DENIED|na | next=…
```
