# 能力契约（包侧 · 非实例真源）

> **定位**：本包 workflow/agent 可引用的**槽位契约**（`tools:` / `tools_allowed:` ⊆ 本表能力名）。  
> **实例真源**：工作根 `{workroot}/capabilities/00-能力清单.md`。正文细节只在 `{workroot}/capabilities/`；项目档案等**仅索引**。  
> **参考**：`capabilities/reference.md`（非真源）。纪律见 `rules/capabilities/instance-discipline.md`。  
> **维护**：新增能力名先登记本表再引用；改后跑 `rules/tools/Test-Template.ps1`。包内 `skills/` 覆盖方法；外部能力只增强工具。

## 1. 槽位契约

| 能力名 | 意图槽 | 用于 | 最低能力面 | 缺失时 | 核心 |
| --- | --- | --- | --- | --- | --- |
| `git` | git | 提交/推送 | — | 停并报告 | 是 |
| `defect-platform` | defect-platform | 缺陷拉取/回写 | list · get · comment · transition 或 export | provider=无→降级 change | 否 |
| `子代理` | subagent | 分片/侦察/独立核验 | 宿主子代理 | 本会话直做 | 否 |
| `spec-clarify` | spec-clarify | 需求澄清 | 访谈/澄清方法 | 包内澄清+技能 | 否 |
| `planning-and-task-breakdown` | planning | 任务拆解 | 拆单方法 | 包内 task-breakdown | 否 |
| `docs-mcp` | docs-mcp | 查库/框架文档 | 文档检索 | 代码+实测 | 否 |
| `repo-mcp` | repo-forge | PR/MR/流水线 | forge API | 手动看页 | 否 |
| `issue-tracker` | issue-tracker | 任务/缺陷同步 | 同步读写 | 本地清单 | 否 |
| `ci` | ci | 构建/门禁 | CI 状态 | 本地命令 | 否 |
| `design-diagram` | design-diagram | 方案可视化 | 绘图 | 纯文本 | 否 |
| `design-intelligence` | design-intelligence | 设计方向参考 | 设计 skill | 包内 frontend-design | 否 |
| `design-review` | design-review | UI 审查 | 审查清单/工具 | 包内评分卡 | 否 |
| `code-review` | code-review | diff 评审增强 | 评审工具 | reviewer-agent | 否 |
| `architecture-skill` | architecture-skill | 架构演进/模块边界方法 | 外部架构 skill | 包内 solution-design | 否 |
| `debugging-skill` | debugging-skill | 系统化调试增强 | 外部调试 skill | 包内 debugging-and-error-recovery | 否 |
| `verification-skill` | verification-skill | 完成前验证纪律 | 外部验证 skill | 包内 implementation §4.0 | 否 |
| `threat-model-skill` | threat-model-skill | 威胁建模方法增强 | 外部威胁模型 skill | 包内 threat-modeling | 否 |
| `frontend-perf-skill` | frontend-perf-skill | 前端性能实践 | 外部前端 perf skill | 包内 frontend-implementation | 否 |
| `skill-discovery` | skill-discovery | 生态技能检索 | `npx skills find` / find-skills | 只对照参考目录 | 否 |
| `security-scan` | security-scan | SAST/密钥/依赖 | 扫描器 | 人工清单 | 否 |
| `sbom` | sbom | SBOM | 生成 SBOM | 锁文件+人工 | 否 |
| `unit-test-gen` | unit-test-gen | 单测生成 | 生成/覆盖 | 手写+门禁 | 否 |
| `mutation-gate` | mutation-gate | 变异测试信号 | 变异工具 | 不启用 | 否 |
| `browser-automation` | browser-automation | UAT/冒烟/页面验证 | navigate · snapshot | 手工清单+证据 | 否 |
| `browser-mcp` | browser-automation | 同上（别名） | 同左 | 同左 | 否 |
| `release-automation` | release-automation | 发版联动 | 发版自动化 | 模板手写 | 否 |
| `ai-eval` | ai-eval | LLM 评测 | 评测跑批 | 手工黄金集 | 否 |
| `ai-observability` | ai-observability | 模型/提示观测 | 观测后端 | 结构化日志 | 否 |
| `prompt-guard` | prompt-guard | 输入输出护栏 | 护栏引擎 | 规则+人工 | 否 |
| `feature-flag` | feature-flag | 灰度/开关 | 开关平台 | 配置开关 | 否 |
| `supply-chain` | supply-chain | 依赖/供应链 | 更新/评分 | 锁文件+人工 | 否 |
| `iac-scan` | iac-scan | IaC/容器扫描 | IaC 扫描 | 人工清单 | 否 |
| `contract-test` | contract-test | 消费方契约 | 契约验证 | 文档+用例 | 否 |
| `a11y` | a11y | 可访问性 | a11y 工具 | 人工 WCAG | 否 |
| `observability` | observability | 日志指标追踪 | OTel 等 | 基础日志指标 | 否 |

## 2. 首缺提示（写入实例清单）

| 能力 | 触达 | 提示示例 |
| --- | --- | --- |
| `planning-and-task-breakdown` | plan | 未装外部拆单，已按包内技能；需要装说「装配能力」 |
| `design-diagram` | design | 未装 design-diagram，已按纯文本；需要装说「装配能力」 |
| `design-intelligence` | design | 未装 design-intelligence，已按包内 frontend-design；需要装说「装配能力」 |
| `design-review` | review | 未装 design-review，已按评分卡；需要装说「装配能力」 |
| `code-review` | review | 未装 code-review，已用独立核验；需要装说「装配能力」 |
| `security-scan` | review/release | 未装 security-scan，已按人工清单；需要装说「装配能力」 |
| `browser-automation` / `browser-mcp` | release | 未配置浏览器自动化，已按手工清单；需要装说「装配能力」 |
| `unit-test-gen` | implement（逻辑结构面命中或 L2+ 核心模块） | 未装 unit-test-gen，已按手写+门禁；需要装说「装配能力」 |
| `mutation-gate` | implement（逻辑结构面命中且需加强信号） | 未装 mutation-gate，不以变异为门；需要装说「装配能力」 |
| `release-automation` | 发版 | 未装 release-automation，已按模板；需要装说「装配能力」 |
