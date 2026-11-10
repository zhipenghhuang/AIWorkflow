# rules/ 目录地图（产品规范）

> 维护用；业务执行不读本文。运行时读链见 `core/global-rules.md` §7。

## 0. 正式层级

- **运行时**：`AGENTS.md` → `core/cold-start.md` → `activeContext.md`（状态）→ `core/global-rules.md`（每步读）→ `workflows/<id>.md` → `packets/<id>/<step>.md` → `skills/`/`templates/` 指定节。
- **规则字典**：`gates.md` · `doc-governance.md` · `collaboration/` · `defects/`（按需查，不每步通读）。
- **参考层**：`workflow.md` · `core/` 的 `execution-contract`/`clarification`/`verification`/`doc-quality`/`rule-governance`/`doc-facade-sync`。
- **每步全局规则**：读 `core/global-rules.md` 并逐条过；首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。步骤卡只留指针，不复制正文。

## 1. 分层

| 路径 | 作用 | 改动影响面 |
| --- | --- | --- |
| `core/` | 运行时：`global-rules.md` + `cold-start.md`；其余为参考层（澄清/验证/质量/规则治理/门面/版本） | 全包所有链 |
| `gates.md` | 确认门与 `when` 条件词表 | 全包所有链 |
| `workflows/<id>.md` | 生成的一页链图（运行时读一次） | 该链 |
| `workflow.md` | 参考：阶段护栏、git/提交/交付、文档落位（运行时以 global-rules + 链图 + 步骤卡为准） | 全包所有链 |
| `packets/<wf>/` | **某条链专属**：步骤卡；终端共享 `rules/packets/_shared/closeout.md` | 仅该链 |
| `templates/` | 模板库（按步引用，见 `templates/index.md`） | 引用它的链 |
| `tools/` | 生成器与自检 | 维护 |
| `capabilities/` `collaboration/` `defects/` `special/` | 按需参考，不预读 | 引用它的链 |
| `doc-governance.md` `path-aliases.md` | 文档治理 / 路径别名 | 点名时 |

## 2. 三类改动

1. **只改一条链**：改 `workflows/<wf>.yaml`（及步骤卡需要时）→ 只重生成该链：
   `python rules/tools/build_step_packets.py <包> --only <wf>`
   其它链的 packet 不变。
2. **改共享规则**：`core/global-rules.md`、`gates.md`、技能/模板 → 跑全包自检（`Test-Template.ps1` + `validate_workflow.py` + `validate_semantics.py` + `check_skills.py --strict`）。
3. **改技能/模板**：查 `skills/README.md`、`templates/index.md` 的引用面；被链引用越多，影响越大。

## 3. 共享库（链路按需引用）

- **全局规则**：`core/global-rules.md`（每步读；步骤卡只留指针；改全局规则无需重生步骤卡）。
- 技能库：`skills/README.md`（步骤 → 技能映射；步骤包 §6 只列必开/条件开，AI 按 §6 选择，不全库通读）。
- 模板库：`templates/index.md`（按 step 找模板；每步至多 1 个）。
- 能力库：`{workroot}/capabilities/00-能力清单.md`（实例真源；包内只有契约与候选）。

## 4. 不允许

- 节点包引用其它链的 `rules/packets/<other>/`（跨链走路由或 handoff；诊断只读对方链图，不读节点包）。
- 手改生成物（链图、步骤卡）：下次生成会覆盖。
