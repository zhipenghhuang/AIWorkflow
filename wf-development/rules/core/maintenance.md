# 维护本包（开发轨）

> 只在改包/自检/维护时读；业务任务不读本节。`AGENTS.md` 只留维护指针。  
> **capabilities/技能体检**（推荐口令「体检能力」）走 `workflows/skill-audit.yaml` + `rules/special/skill-audit.md`（含 **discover** 生态检索：`npx skills find` / find-skills），不替代本节自检。

## 1. 改哪里

- 不变量/路由/读取协议 → `AGENTS.md`
- 步骤顺序/技能挂载 → `workflows/`（step 的 `skills` / `skills_conditional`）；改后跑 `build_step_packets.py`
- 角色契约 → `agents/`
- 红线/输出/门 → `rules/`（门：`rules/gates.md`）
- 澄清协议 → `rules/core/clarification.md`
- 无口令/自然语言入口判定 → `rules/core/routing.md`（改五元组/意图类 A～L/状态修正/置信度时同步；并核 AGENTS 口令表指针；附录仅校验勿当词典）
- 开局卡 → `rules/core/cold-start.md`；前端硬门 → `frontend-gate.md`；实施勾选 → `iq-checklist.md`
- 心跳格式 → `rules/core/global-rules.md` §8（同步 activeContext 运行状态）
- collaboration/handoff/变更分级 → `rules/collaboration/handoff.md`；交接步骤 → `workflows/handoff.yaml`；回执/台账模板 → `rules/templates/`
- 模板 → `rules/templates/`
- 文档质量标准/类型矩阵 → `rules/core/doc-quality.md`
- 工作记忆/偏好/洞见/坑沉淀 → `rules/core/context-memory.md`（读/写/升级/清理单一出处）
- 适配：templates / rules / skills 可按项目实际适配；先拟改/原因/影响，用户确认后改本包并登记；能靠产出文档解决的优先改产出
- 技能 → `skills/`（**可就地改**；通用最优用口令「通用优化技能」）
- 能力契约/参考目录 → 包内 `capabilities/`；实例 → `{workroot}/capabilities/`（`rules/capabilities/instance-discipline.md`）
- capabilities/技能体检流程 → `workflows/skill-audit.yaml` + `rules/special/skill-audit.md`（inventory→discover→fit；方法回灌进 `skills/`，外装进 `{workroot}/capabilities/`）
- 文档树/归档 → `rules/doc-governance.md`
- 门面/对外句同步 → `rules/core/doc-facade-sync.md`（`project-readme.md` 只留读写偏好；改触发矩阵先改前者）
- 子代理编排 → `rules/collaboration/subagents.md`（单一出处），workflow/agent 只留指针
- solo 路径 → `rules/core/lightweight.md`；步骤 → `workflows/solo.yaml`

## 1.1 体检 vs 装配 vs 维护

| 口令 | 用途 |
| --- | --- |
| 装配能力 | 安装并向 `{workroot}/capabilities/` 写入 |
| 体检能力（及同义） | 外部能力改 `{workroot}/capabilities/` + 随包技能可改本包；HITL |
| 通用优化技能 | 同上 workflow，mode=generic（不绑具体项目） |
| 维护/查询 | 改rules/路由/跑自检；技能能力深度分析转体检口令 |

## 2. 自检

```powershell
powershell -ExecutionPolicy Bypass -File "wf-development/rules/tools/Test-Template.ps1"
powershell -ExecutionPolicy Bypass -File "wf-development/rules/tools/Test-DocHygiene.ps1"
python wf-development/rules/tools/check_skills.py wf-development --strict
python wf-development/rules/tools/validate_semantics.py wf-development
python wf-development/rules/tools/validate_tasklist.py <清单路径>
python wf-development/rules/tools/validate_dev_plan.py <开发计划路径>
```

> **`check_skills.py` 必须带包根路径**（上例 `wf-development` 或包内 `.`）；包中文名不是路径，裸跑会 `SKILL_DIR_MISSING`。多包布局把前缀换成 `wf/wf-development`。

自检覆盖：引用可解析 + 章节锚点 + workflows→agents + 步标记词表 + 能力名声明 + 版本单点 + YAML 语法 + 技能（含反模式/反合理化闸）+ 语义（双入口/残句/角色边标识/预算/不可达步）；另跑文档卫生检查（见 `rules/tools/README.md`）。

> 按产物机检（交接包 / 任务清单 / 开发计划）见对应步骤包与 `rules/tools/README.md`；`Test-Template.ps1`已含 YAML schema、步骤包结构与「生成物 ↔ workflows 漂移」检查。

## 3. 质量度量

开发计划 §14（DORA/交付质量）；架构评审评分卡见 `skills/solution-design/SKILL.md` §8（`confirm_spec` 用）。

## 4. 规则撰写标准

新增或保留rules/步骤的标准＝**有用、不冗余（单一出处，其余指针）、不误导、高性价比**；强调集中在不可让项；凡「须确认/询问/固定骨架」处，YAML 步上必须有对应 `hitl`。

## 5. 文档粒度

必读最小、按需加载：被 ≥2 角色/场景引用或按口令分时机点读 → 独立成文；单角色且不足 20 行 → 并入其契约/所属文档；单文件超 200 行且分时段消费再拆；引用不复制。

## 5.1 规则自优化闭环（DEV-IQ-15）

每波收尾、复盘、缺陷族修复后，必须做一次：

1. **现象**：这次暴露的具体错误/返工/缺口。
2. **根因**：是理解、规则、模板、工具、检查项还是执行层。
3. **改层**：优先改能防止复发的单一层——`rules/`、`skills/`、`templates/`、`tools/`、`verify/` 检查项；不要只在代码里补。
4. **前端择优**：同时检查 UI 是否“实用 + 美观 + 与现有系统一致”：导航层级/复用组件/列与区块/密度/层级/间距/响应式/空态/错误态/权限态；原型冲突按方案，布局按原型，视觉按设计系统取优。
5. **验证**：跑 `Test-Template.ps1`、`check_skills.py --strict` 或对应工具；记录改动与版本；同类问题第二次出现而规则未改 = 未收口。

> 规则不是只增不改：发现重复/过时/冲突要合并或替换；维护优先改产出/模板/工具，而不是继续加长必读。

## 6. 宿主无关

本包文本与 YAML 只写能力名（清单见 `capabilities/00-contract.md`）；禁写具体宿主名与宿主本地路径——宿主要求、挂载与配置示例见 README「宿主适配」节。
