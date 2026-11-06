# 维护本包（测试轨）

> 只在改包/自检/维护时读；业务任务不读本节。`AGENTS.md` 只留维护指针。  
> **capabilities/技能体检**走 `workflows/skill-audit.yaml` + `rules/playbooks/skill-audit.md`（含 **discover** 生态检索：`npx skills find` / find-skills）。

## 1. 改哪里

- 不变量/路由/读取协议 → `AGENTS.md`
- 无口令/自然语言入口判定 → `rules/core/routing.md`（改五元组/意图类 A～L/状态修正/置信度时同步；并核 AGENTS §2 指针与读取索引「无口令」行；附录仅校验勿当词典）
- 开局卡 → `rules/core/cold-start.md`
- 规则心跳/重锚 → `rules/core/rule-anchor.md`（同步 cold-start、执行契约、activeContext `rule_card`）
- 步骤 → `workflows/`（含 `skill-audit.yaml`）
- 角色 → `agents/`
- 红线/输出/门 → `rules/`（门：`rules/gates.md`）
- 澄清协议 → `rules/core/clarification.md`
- collaboration/handoff/变更分级 → `rules/collaboration/handoff.md`；交接步骤 → `workflows/handoff.yaml`；回执/台账模板 → `rules/templates/`
- 子代理取档/生命周期 → `rules/collaboration/subagents.md`；批流/准确度/MCP/计划驱动详版 → `rules/special/multi-agent-output.md`
- 轨边界 → `rules/tracks/`
- 模板 → `rules/templates/`
- 文档质量标准/类型矩阵 → `rules/core/doc-quality.md`
- 工作记忆/偏好/洞见/坑沉淀 → `rules/core/context-memory.md`（读/写/升级/清理单一出处）
- 适配：templates / rules / skills 可按项目实际适配；AI 先出拟改/原因/影响，用户确认后改本包并登记；能靠产出文档解决的优先改产出
- 技能 → `skills/`（**可就地改**；通用最优：「通用优化技能」）
- 能力契约/参考目录 → 包内 `capabilities/`；实例选型/绑定 → `{workroot}/capabilities/`（纪律 `rules/capabilities/instance-discipline.md`）
- capabilities/技能体检 → `workflows/skill-audit.yaml` + `rules/playbooks/skill-audit.md`（inventory→discover→fit；方法回灌进 `skills/`，外装进 `{workroot}/capabilities/`）
- 计划编排 → 测试计划模板 + `rules/workflow.md` §3.6 + `rules/special/multi-agent-output.md` §4（三处同步）
- 门面/对外句同步 → `rules/core/doc-facade-sync.md`（`project-readme.md` 只留读写偏好）
- 读取索引 → `rules/read-index.md`（改 step/reads 后同步）

## 1.1 体检 vs 装配 vs 维护

| 口令 | 用途 |
| --- | --- |
| 装配能力 | 安装并向 `{workroot}/capabilities/` 写入选型/绑定 |
| 体检能力（及同义） | 外部能力（改实例）+ 随包技能（可改包内）；HITL |
| 通用优化技能 / 通用最优技能 | 同上，mode=generic |
| 维护/查询 | 改rules/自检；深度技能能力分析转体检口令 |

## 2. 自检

```powershell
powershell -ExecutionPolicy Bypass -File "wf-testing/rules/tools/Invoke-TestWorkflow.ps1" -Action ValidateTemplateRefs
powershell -ExecutionPolicy Bypass -File "wf-testing/rules/tools/Test-DocHygiene.ps1"
python wf-testing/rules/tools/check_skills.py wf-testing --strict
python wf-testing/rules/tools/validate_semantics.py wf-testing
python wf-testing/rules/tools/validate_testcase.py <模块用例.md>
python wf-testing/rules/tools/validate_api_testcase.py <接口域用例.md>
```

> **`check_skills.py` 必须带包根路径**（上例 `wf-testing` 或包内 `.`）；包中文名不是路径，裸跑会 `SKILL_DIR_MISSING`。多包布局把前缀换成 `wf/wf-testing`。

自检覆盖：引用/锚点/workflows→agents/步标记/能力名/版本单点/YAML/技能（含反模式/反合理化闸）/语义（双入口/残句/角色边标识/预算/不可达步）；另跑文档卫生检查（见 `rules/tools/README.md`）。功能/接口用例机检见上两行。

> 按产物机检（交接包 / PRD / 任务清单 / 用例 / 接口用例 / 开发计划）见对应步骤包与 `rules/tools/README.md`；`Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`已含 YAML schema、步骤包结构与「生成物 ↔ workflows/_orch 漂移」检查。

## 3. 无障碍/UX

`rules/templates/20-test-cases/a11y-ux-checklist.md`；结果并入测试报告 §11。

## 4. 重排维护

改口令表/门表/清单编号后，检索全包「行 N」「优先 N」「§x.y」等编号引用并同步（自检不查编号引用）。

## 5. 规则撰写标准

新增或保留rules/步骤的标准＝**有用、不冗余（单一出处，其余指针）、不误导、高性价比**；默认可完成的动作不写；强调集中在不可让项；凡阻塞式确认门处，YAML 步上必须有对应 `hitl`；澄清类一问不入 hitl。

## 6. 文档粒度

常驻最小、按需加载：被 ≥2 角色/场景引用或按口令分时机点读 → 独立成文；单角色且不足 20 行 → 并入其契约/所属文档；单文件超 200 行且分时段消费再拆；引用不复制。

## 7. 宿主无关

本包文本与 YAML 只写能力名（⊆ `capabilities/00-contract.md`）；选型/绑定只写 `{workroot}/capabilities/`；基线 §8/§17 仅索引；§13 平台配置仍在基线；宿主要求见 README「宿主适配」。
