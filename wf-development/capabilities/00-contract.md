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

## 2. 缺失提示（触达可见 · 分档）

> 降级可续跑，但不得静默。status / 接受降级见 `rules/capabilities/instance-discipline.md`。`git` 核心缺失 → 停并报告（不用本块替代）。

### 2.1 何时出块

| 条件 | 行为 |
| --- | --- |
| 清单 `available` | 静默使用 |
| **硬触达**未装 / `missing` / `undecided` / 仅 `prompted`（无 `accepted`） | 本战役**首次**命中该槽 → 必出【能力缺失】全块；同战役再触达一行短提醒 |
| **软触达**未装 | 不出全块；本步因缺能力致 AC/门证据/提测或发布就绪风险 ↑ → 收尾「适度建议」至多 1 条 |
| 「接受降级」/「暂不装」 | `degraded` + `accepted=YYYY-MM-DD`；同会话免全块；新会话/新战役短提醒 |
| 「装配能力」 | 装成后 `available`，停提示 |

**硬触达**：`defect-platform`（缺陷拉取/回写）；`security-scan`（review / release 且命中安全面或发版就绪）；本步确需页面验证时的 `browser-automation` / `browser-mcp`。  
**软触达**：其余可选增强（如 `planning-and-task-breakdown`、`design-*`、`code-review`、`unit-test-gen`、`mutation-gate`、`release-automation` 等）。

### 2.2 全块版式

须单独成段；禁塞进路由行或收尾附注冒充：

```
【能力缺失】
- 能力：{名}
- 影响：{本步做不到的增强面}
- 现行降级：{§1「缺失时」，须实写}
- 请选：装配能力 ｜ 接受降级
```

未选也不阻塞已授权的降级执行，但本回合可见回复须出现该块。

### 2.3 硬触达锚点

| 能力 | 触达 | 降级锚点 |
| --- | --- | --- |
| `defect-platform` | defect-fix / 回写 | provider=无 → 降级 change / 导出 |
| `security-scan` | review / release（安全面或发版） | 人工清单；非自动 SAST |
| `browser-automation` / `browser-mcp` | UAT / 冒烟 / 页面验证 | 手工清单 + 证据 |
