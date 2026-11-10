# 能力契约（包侧 · 非实例真源）

> **定位**：本包 workflow/agent 可引用的**槽位契约**（`tools:` / `tools_allowed:` ⊆ 本表能力名）。  
> **实例真源**：工作根 `{workroot}/capabilities/00-能力清单.md`（选型 / kind / 绑定 / 状态）。正文细节只在 `{workroot}/capabilities/`；环境基线等**仅索引**。  
> **参考**：装配候选见 `capabilities/reference.md`（非真源）。纪律见 `rules/capabilities/instance-discipline.md`。  
> **维护**：新增能力名先登记本表再引用；改后跑 `rules/tools/Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`。

## 1. 槽位契约

| 能力名 | 意图槽 | 用于 | 最低能力面 | 缺失时 | 核心 |
| --- | --- | --- | --- | --- | --- |
| `git` | git | 提交/handoff/回写前版本控制 | — | 停并报告 | 是 |
| `browser-automation` | browser-automation | 功能/探索式轨执行与核验 | navigate · snapshot · network | 功能/探索式不可执行；接口/发布前不默认启用 | 条件 |
| `browser-mcp` | browser-automation | 同上（别名；YAML 兼容） | 同 `browser-automation` | 同左 | 条件 |
| `脚本执行器` | script-runner | 已脚本化回归/冒烟 | 本包 executor | 降级 AI 逐条 | 否 |
| `子代理` | subagent | 模块档/拆分档 | 宿主子代理 | 直跑档 | 否 |
| `defect-platform` | defect-platform | 缺陷提交/回归/回写 | list · get · comment · transition | 确认后本批统一导出（禁逐条目录；禁与平台并行） | 否 |
| `vision-ui` | vision-ui | 视觉/语义复核 | 截图语义判定 | 直跑+截图 | 否 |
| `mobile-automation` | mobile-automation | 移动端点名 | 真机/模拟器自动化 | 报未启用 | 否 |
| `api-client` | api-client | 契约导入/集合回放 | 集合或 HTTP 回放 | 主读+现网 | 否 |
| `api-fuzz` | api-fuzz | OpenAPI 属性/负向 | 契约驱动生成 | AI 现场设计 | 否 |
| `contract-test` | contract-test | 消费方契约 | 契约验证 | 抽样 | 否 |
| `mock-server` | mock-server | 依赖模拟 | mock 注入 | 基线造数 | 否 |
| `perf-test` | perf-test | 性能/容量 | 压测或前端性能测量 | 项目自备 | 否 |
| `sec-scan` | sec-scan | 安全扫描 | SAST/DAST | 负向 smoke | 否 |
| `a11y` | a11y | 可访问性 | a11y 扫描或清单 | 视觉基础条 | 否 |
| `visual-reg` | visual-reg | 截图回归 | 截图断言 | 不启用 | 否 |
| `test-mgmt` | test-mgmt | 用例/执行管理 | 平台同步 | 用例+台账 | 否 |
| `qa-skills` | qa-skills | QA Agent Skills 参考 | 外部 skill | 包内技能 | 否 |
| `playwright-best-practices` | playwright-best-practices | Playwright 稳定性/模式参考 | 外部 Playwright skill | 脚本执行 §6.3 + 执行技能 | 否 |
| `exploratory-skill` | exploratory-skill | SBTM/探索报告 | 外部 skill | 探索式轨规则 | 否 |
| `skill-discovery` | skill-discovery | 生态技能检索 | `npx skills find` / find-skills | 只对照参考目录 | 否 |
| `report-render` | report-render | 执行明细渲染 | 报告引擎 | markdown 台账 | 否 |
| `data-gen` | data-gen | 造数 | 假数据生成 | 基线配方 | 否 |
| `ai-eval` | ai-eval | LLM/RAG 评测 | 评测集跑批 | 手工黄金集 | 否 |
| `ai-redteam` | ai-redteam | AI 红队 | 注入/越狱探测 | 手工红队 | 否 |
| `chaos` | chaos | 故障注入 | 混沌工具 | 人工演练 | 否 |
| `ci` | ci | 构建触发/状态 | CI 读写 | 本机命令 | 否 |

## 2. 缺失提示（硬 · 触达必显）

> **目的**：未装槽位不得用「夹带半句 + 基线写已提示」冒充已知晓。降级可继续跑，但用户必须能看见取舍。

### 2.1 何时出块

| 条件 | 行为 |
| --- | --- |
| 清单 `available` | 静默使用 |
| 未装 / `missing` / `undecided` / 仅 `prompted`（无 accepted） | **每次**命中该槽（开生成 / 开执行门·开跑 / 切发布前专项 / 计划点名该能力）→ 必出独立 **【能力缺失】** 块 |
| 用户明示「接受降级」/「暂不装」 | 清单 → `degraded` + 备注 `accepted=YYYY-MM-DD`；**同会话同槽**免再出全块；**新会话或新战役再触达**出一行短提醒（能力名 + 现行降级 + 「改主意说装配能力」） |
| 用户说「装配能力」 | 走装配流程；装成后 `available`，停提示 |

`prompted` **只记「最近出示过全块」**，**禁止**据此跳过再提示。基线/清单**禁止**写「未安装（已提示）」；未接受写「未安装」，已接受写「未安装（已接受降级）」。

### 2.2 全块版式（不可让）

须**单独成段**（可短表），**禁**塞进门确认尾句、路由行或收尾附注冒充本条：

```
【能力缺失】
- 能力：{名}
- 影响：{本步/本轨做不到的增强面}
- 现行降级：{契约「缺失时」策略，须实写}
- 请选：装配能力 ｜ 接受降级
```

未选也不阻塞已授权的降级执行，但**本回合用户可见回复里必须出现该块**（与门确认可同条消息，块须顶格可见，不得缩成半句）。

### 2.3 触达 × 文案锚点

| 能力 | 触达 | 降级锚点（写入「现行降级」） |
| --- | --- | --- |
| `api-client` / `api-fuzz` | 接口轨生成/执行 | 主读 + 现网 Network；无契约自动导入/属性 fuzz |
| `perf-test` | 发布前·性能 | 项目自备方法（须点名实际手段） |
| `sec-scan` | 发布前·安全 | 负向 smoke（非 SAST/DAST 全扫） |
| `vision-ui` | 执行/探索式 | 直跑 + 截图人工可读 |
| `qa-skills` / `exploratory-skill` | plan / 探索式 | 包内技能 / 探索式轨规则 |
| `browser-automation` / `browser-mcp` | 功能/探索式 | **本轨不可执行**（非降级续跑；须配置或停） |

（其余槽：清单 available 即用；否则按 §1「缺失时」列，上表有名则按 2.1～2.2 出块。）
