# rules/ 目录地图（开发规范）

> 维护用；业务执行不读本文。运行时读链见 `core/cold-start.md` §4。

## 1. 分层

| 路径 | 作用 | 改动影响面 |
| --- | --- | --- |
| `core/` | 全局常驻与通用规则：开局卡、心跳、执行契约、澄清、文档治理、质量、验证、版本 | 全包所有链 |
| `gates.md` | 确认门与 `when` 条件词表 | 全包所有链 |
| `workflow.md` | 阶段护栏、git/提交/交付、文档落位 | 全包所有链 |
| `packets/<wf>/` | **某条链专属**：`_chain`、`_region-*`、节点包、`_orch.yaml` | 仅该链 |
| `templates/` | 模板库（按步引用，见 `templates/index.md`） | 引用它的链 |
| `tools/` | 生成器与自检 | 维护 |
| `capabilities/` `collaboration/` `defects/` `playbooks/` `special/` | 按需参考，不常驻 | 引用它的链 |
| `doc-governance.md` `path-aliases.md` | 文档治理 / 路径别名 | 点名时 |
| `read-index.md` | 维护索引（非运行时） | 改规则对照用 |

## 2. 三类改动

1. **只改一条链**：改 `packets/<wf>/_orch.yaml` 或 `workflows/<wf>.yaml` → 只重生成该链：
   `python rules/tools/build_step_packets.py <包> <包> --only <wf>`
   其它链的 packet 不变。
2. **改共享规则**：`core/`、`gates.md`、`workflow.md` → 跑全包自检（`Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs` + `validate_workflow.py` + `validate_semantics.py` + `check_skills.py --strict`）。
3. **改技能/模板**：查 `skills/README.md`、`templates/index.md` 的引用面；被链引用越多，影响越大。

## 3. 共享库（链路按需引用）

- **全局规则**：`core/cold-start.md` §1（直接加编号条目；开工/切包读一次，改后重生步骤包）。
- 技能库：`skills/README.md`（步骤 → 技能映射；步骤包 §6 只列必开/条件开，AI 按 §6 选择，不全库通读）。
- 模板库：`templates/index.md`（按 step 找模板；每步至多 1 个）。
- 能力库：`{workroot}/capabilities/00-能力清单.md`（实例真源；包内只有契约与候选）。

## 4. 不允许

- 节点包引用其它链的 `rules/packets/<other>/`（跨链走路由或 handoff；诊断确需只读对方 `_chain.md`，不读节点包）。
- 手改生成物（`_chain.md`、`_region-*.md`、节点包）：下次生成会覆盖。

