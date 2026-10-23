# 项目变更与版本记录

> 本文件记录 **AI Workflow** 项目自身的版本与迭代变化；最新在前。  
> 版本格式：`yyyy.MM.dd.N`；当前版本见下表。

## 0. 版本总览

| 包/仓 | 当前版本 | 本次变化 | 说明 |
| --- | --- | --- | --- |
| 产品规范 | `2026.10.23.5` | 更新 | 项目级 CHANGELOG 模板/接入/更新时点 |
| 开发规范 | `2026.10.23.5` | 更新 | CHANGELOG 模板统一；项目级记录 |
| 测试规范 | `2026.10.23.5` | 更新 | 项目级 CHANGELOG 模板/接入/报告更新 |
| 母版仓 | `2026.10.23.5` | 更新 | 取三包最高版本，仅用于记录 |

> 母版仓版本取三包最高版本，不新增第四套版本号；三包仍可独立升级、独立落地。

## [Unreleased]

（无）

## [2026.10.23.5] - 2026-10-23

### Added

- 三包统一 `CHANGELOG模板.md`：项目根 `CHANGELOG.md` 记录本项目版本/迭代、显著变化、迁移与验证；产品/测试包首次具备独立创建能力。
- 产品 `onboard` 创建 `CHANGELOG.md`（无则建、有则保留）；`plan.publish` 记录版本/迭代与链接，`deliver.release` 记录发布/关闭与变化摘要。
- 测试 `onboard` 创建 `CHANGELOG.md`；`testing.report` 记录测试版本/范围/准出/遗留与报告链接。
- 开发沿用既有 `onboard`、`control.wrap`、`iterate.wrap`、`release.record` 更新 `CHANGELOG.md`；模板与产品/测试保持一致。

### Changed

- 根 `CHANGELOG.md` 收敛为项目自身记录：版本总览 + Keep a Changelog 分类 + 迁移/验证；去掉版本记录分工、参考依据等说明性内容。
- 产品/测试 README、模板索引、读取索引同步新模板与更新时点。

### Verification

- 三包 `Test-Template.ps1` / `Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`、`Test-DocHygiene.ps1` 与 `validate_workflow.py` 全部通过。

## [2026.10.23.4] - 2026-10-23

### Removed

- 删除独立多包协作层 `项目协作/`（不保留备份），同时移除三包 `AGENTS.md`、README、模板、onboard 与自检脚本中的相关引用。

### Added

- 三包新增 `规则/澄清.md`：统一「理解回执 → 一次一问 → 更新置信度 → 95% 停止条件 → 复述确认 → 落盘」；明确确认门≠澄清、澄清答复≠执行授权，禁一次多问/自问自答/把假设当结论。
- 开发包新增 `技能/product-doc-analysis/SKILL.md`：PRD/迭代方案/文档/页面原型/截图五遍解析（来源→需求模型→原型→一致性→可开发/可测性），输出带引用、冲突表、GAP、假设与置信度的需求理解包；新增 `change.analyze_input` 步与 `confirm_understanding` 门。
- 测试包新增 `技能/test-basis-analysis/SKILL.md`：依据盘点→十要素需求模型→文档/原型/代码一致性→九类歧义→AC 可测性/oracle→TP 追溯；`testing.analyze` 新增理解门与需求模型输出。
- 产品包新增 `技能/customer-needs-discovery/SKILL.md`：角色地图、证据分层、Mom Test 访谈、问题定义、假设登记、需求复述确认；`change.intake` 新增 `confirm_understanding` 门。
- 开发 `需求基线模板` 增加「0.1 来源与理解」；产品 `受理与处置模板` 增加「2.1 需求理解与澄清」；测试 `工作流.md` 分析短表增加需求模型/oracle/追溯字段。

### Changed

- 三包 `AGENTS.md` 的「低风险一次最多问 3 个」改为强制澄清追问环：任何任务先给理解回执，一次只问一个问题，≥95% 且用户明确确认后才产出方案/PRD/用例/代码；L0/T0/P0 也不得跳过（纯机械操作除外）。
- 开发 `change` 增加「产品资料解析与理解确认」步；`requirements/design/implement/review` 增加需求理解包引用、冲突/GAP 继承与需求覆盖核对。
- 测试 `analyze/plan/generate/execute/report` 增加需求模型、oracle 来源、AC/TP 追溯、歧义关闭与报告覆盖；生成前缺模型先补，不直接写用例。
- 产品 `change/prd/new-product/plan` 增加客户需求还原、证据/假设、未确认不排期、PRD 来源可追溯与评审对照。
- 多包改为自动探测：项目根同时存在两个及以上包目录（`产品规范/`、`开发规范/`、`测试规范/`，以各自 `AGENTS.md` 为标志）即启用共享 `项目资料/`、`activeContext.md` 与路由；不再需要 `项目资料/项目协作.md`、额外模板或实例自检。
- 共享资料根 `项目资料/` 改为按需创建，不预建、不强制；单包仍按本包 `资料/` 运行。
- 根 `AGENTS.md` 只做路由：首次接入时按实际包目录补齐已启用包列表，不再写“本会话只启用本包”。
- 三包 `template_version` 更新为 `2026.10.23.4`；根 README 的多包接入、目录结构、FAQ、技能计数（38：产品 12 / 开发 20 / 测试 6）与自检说明同步。

### Migration

- 已接入旧协作层的项目：删除 `项目协作/` 与 `项目资料/项目协作.md` 即可，三包自动接管；不删也不影响（不再读取）。
- 无破坏性工作流变更；现有单包项目的目录与产物不需要迁移。

### Verification

- 三包 `Test-Template.ps1`、测试包 `Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`、三包 `Test-DocHygiene.ps1` 与 `validate_workflow.py` 全部通过；仓库内不再有独立协作层引用（本历史条目除外）。

## [2026.10.23.2] - 2026-10-23

### Added

- 新增 `开发规范/技能/engineering-quality/SKILL.md`：企业级工程质量条、设计/实施启发式、质量属性证据表、12 项评审 rubric。
- 新增 `开发规范/规则/模板/前端设计说明模板.md`：需求/情境 → IA/路由 → 状态矩阵 → 组件/tokens → a11y/性能/兼容/打印 → 交接与验收；含“产品设计输入/保留/优化/偏离”。
- 新增 `开发规范/规则/模板/CHANGELOG模板.md`：项目根长期版本记录骨架（Keep a Changelog + 迁移/验证/文档检查）。
- 新增根 `CHANGELOG.md`：母版仓长期版本与迭代记录首版（回填 2026.10.21～2026.10.23 历史）。
- 新增 `产品规范/规则/模板/开发交接模板.md`：设计意图、必须保留、可优化、未提供、需开发决策、验收对照。
- 产品轨 `prototype-and-interaction` / `ui-visual-design-system` / `prototype.yaml` / `prototype.md` 补设计策略、项目适配、设计系统策略、开发交接边界。
- `开发规范/技能/README.md`、`AGENTS.md`、读取索引、模板索引、workflows、agents 同步挂载新技能/模板。

### Changed

- 重写 `开发规范/技能/frontend-design/SKILL.md`：明确其**按需补充**定位——产品设计完整时直接按方案实现；仅在无原型、原型不完整/仅参考、实现需要补充设计、或需要落地设计系统时使用；已有批准设计不重画。
- `开发规范/技能/frontend-implementation/SKILL.md` 增加“按设计说明实现 + 设计 QA + 设计缺口回写”，禁止绕过 tokens/设计说明。
- `开发规范/技能/solution-design`、`implementation-and-selftest`、`code-review` 统一挂载 `engineering-quality`，避免质量条多处分叉。
- `开发规范/规则/模板/项目档案模板.md` §7.1 增加设计系统/tokens、浏览器矩阵、性能预算、无障碍目标；§9 增加 `CHANGELOG` 与根白名单。
- `开发规范/workflows/` 的 design/implement/review/onboard/control/iterate/release/commit 步同步引用新技能、模板与 CHANGELOG 更新时点。
- 根 `README.md` 更新技能/模板计数、仓库结构、长期记录与归档说明。
- 产品轨 `prototype.yaml` 的 context/visual/handoff 补设计简报、项目适配、设计系统策略与交接边界；`AGENTS.md` 原型纪律增加交接内容要求。

### 迁移与兼容

- 无破坏性工作流变更；现有项目无需搬迁文件。
- 下游项目下次接入/版本关闭时：按模板创建根 `CHANGELOG.md`；已有文档按现有归档规则保持正确。
- 产品交接：下次原型交付使用 `开发交接模板.md`；已有原型可在下一次交接补“必须保留/可优化/未提供”。
- 新技能为增量挂载；未安装任何外部设计/工程工具时，全部按包内技能降级执行。

### 验证

- 该版本改动相关自检通过（开发引用 808 处/锚点 170 处；产品 468 处/117 处；测试 582 处/217 处）；三包 `Test-DocHygiene.ps1` 0 warning；`validate_workflow.py` 输出 `YAML_VALIDATION_OK`。后续澄清追问环接入后的全量结果见 `2026.10.23.4`。

## [2026.10.23.1] - 2026-10-23

### Added

- 三包新增 `规则/读取索引.md`、`规则/门.md`、`规则/playbooks/`、`规则/文档治理.md`、`规则/模板/收尾骨架.md`、`规则/模板索引.md`。
- 新增 `Test-DocHygiene.ps1`（文档卫生/读取预算检查）。
- 拆分产品/开发/测试缺陷协作模板，以及测试计划、环境基线、PRD、开发卡轻量模板。
- 模板索引与读取索引建立，减少“模板存在但没人用/读取放大”。

### Changed

- 三包 `AGENTS.md` 瘦身：产品 195→109 行、开发 267→120 行、测试 224→129 行；输出骨架、门、维护、多包细节下沉。
- 读取预算与按步加载成为默认；重阶段改用 playbook；`hitl`/`gate`/`when` 语义收敛到 `规则/门.md`。
- 三包自检与文档卫生全绿；版本统一 `2026.10.23.1`。

### Fixed

- 修复冲突门与入口不一致；统一收尾输出与「今日工作总结」。

### 迁移与兼容

- 包内结构调整；下游按整包同步，不手工搬规则。
- 旧 `资料治理.md`/`文档生命周期.md` 仅保留指针，实际规则以 `文档治理.md` 为准。

### 验证

- `Test-Template.ps1`、`Test-DocHygiene.ps1`、`validate_workflow.py` 通过。

## [2026.10.22.5] - 2026-10-22

### Changed

- 三包收尾统一为「结论说明体」，新增「今日工作总结」列表输出；`wrap` 与 `commit` 的拟提交展示去重。

### Docs

- `activeContext.md` 记录当前焦点与下一步；历史移入 `_归档/context/`。

## [2026.10.21.4] - 2026-10-22

> 版本号按 10-21 迭代命名，提交日期为 10-22。

### Changed

- 产品轨：条件确认门与收尾闭环强化，减少无效停门。
- 开发轨：入口直达与少问原则；单步入口只执行当前步。
- 测试轨：单步入口与阻塞判定强化。

### 验证

- 三包分别提交：`a07ee3a`（产品）、`7c3a5b6`（开发）、`7f54724`（测试）。

## [2026.10.21] - 2026-10-21

### Added

- 初始化仓库：`产品规范/`、`开发规范/`、`测试规范/` 三套独立包。
- 初始规模：20 条工作流、24 份角色契约、34 个内置技能、70 份模板/脚手架。
- 根 `README.md`、`.gitignore`、`.gitattributes`、LICENSE 与仓库维护脚本。

### Notes

- 初始提交：`cc4e10a`（仓库配置）、`8b51d9a`（产品）、`7f1ab83`（开发）、`c6b8d30`（测试）、`105a14f`（README）。

## 历史归档

| 年份 | 文件 | 说明 |
| --- | --- | --- |
| 2026 | 本文件 | 当前历史较短，暂不拆分；超过约 500 行或跨年时按头部规则归档 |
