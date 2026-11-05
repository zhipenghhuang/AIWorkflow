<div align="center">

# AI Workflow

**把产品 · 开发 · 测试，写成 AI 可执行的工作流。**

流程版本化在仓库里：口令即路由，确认门等人拍板，产物落到约定位置。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-2026.11.05.08-0A7EA4.svg)](./CHANGELOG.md)
[![Packages](https://img.shields.io/badge/packages-3-informational.svg)](#三套独立包)
[![Workflow](https://img.shields.io/badge/workflow-YAML-yellow.svg)](#它如何工作)
[![HITL](https://img.shields.io/badge/HITL-confirm%20gates-orange.svg)](#确认门与质量闸)
[![Skills](https://img.shields.io/badge/Agent%20Skills-built--in-success.svg)](#核心能力)
[![Host](https://img.shields.io/badge/host-AGENTS.md-lightgrey.svg)](#快速开始)
[![GitHub](https://img.shields.io/badge/GitHub-AIWorkflow-181717?logo=github)](https://github.com/zhipenghhuang/AIWorkflow)

`YAML` · `Multi-Agent` · `Human-in-the-Loop` · `Agent Skills` · `MCP` · `Playwright`

[快速开始](#快速开始) · [三套包](#三套独立包) · [常用口令](#常用口令) · [FAQ](#faq) · [CHANGELOG](./CHANGELOG.md)

</div>

---

## 这是什么

**AI Workflow** 是一套**规范模板仓库（母版）**：把产品、开发、测试三条协作轨，拆成 AI 可读可执行的包。

每个包包含：流程定义 · 角色契约 · 规则红线 · 内置技能 · 可选能力 · 文档模板。  
复制**一个包**到项目根，挂上薄 `AGENTS.md` 入口——AI 按口令路由到流程，在确认门停下等你拍板，并把产物写到约定位置。

> 本仓用于管理、发布与同步，**不充当业务执行现场**。落地只复制单个包；三包互相独立，也可同项目多包装载并自动探测。

| | |
| --- | --- |
| **是** | 可版本化的工作流 + 角色契约 + HITL 确认门 + 完成门校验 + 文档治理 |
| **不是** | 提示词合集、聊天技巧手册、自研编排引擎 |

---

## 核心能力

| | |
| --- | --- |
| **声明式工作流** | `trigger → steps → agent`；条件步、确认门、质量闸可审查 |
| **多 Agent 协作** | 角色契约按当前步加载；重阶段再读 playbook |
| **人工确认门** | 该停就停：需求 / PRD / 方案 / 清单 / 提交 / 发布 / 回滚 / 验收 |
| **完成只认门** | Agent 只提候选；`verify/` 门读清单 / diff / 证据后才授予完成态 |
| **能力可插拔** | 外部工具已装即用，未装降级；技能随包命中必用 |
| **按风险裁剪** | 产品 P0～P3 · 开发 L0～L3 · 测试 T0～T3 |
| **宿主无关** | 任意支持 `AGENTS.md` 的 AI 编码工具即可 |

```mermaid
flowchart LR
    A["口令 / 文档 / 缺陷"] --> B["包内 AGENTS.md"]
    B --> C["workflows/*.yaml"]
    C --> D["当前步 Agent"]
    D --> E{"HITL 确认门"}
    E -->|确认| F["产物落盘"]
    F --> G["索引 / 归档 / 交接"]
```

<details>
<summary><strong>为什么需要它（痛点对照）</strong></summary>

| 常见痛点 | AI Workflow 的做法 |
| --- | --- |
| 流程靠口口相传，换人、换会话就变样 | 流程写成 `workflows/*.yaml`，步骤 / 条件 / 门 / 产出可审查 |
| AI 一上来就写代码或文档，方向错了才返工 | 需求、PRD、方案、清单、提交、发布设 HITL 确认门，未确认不进入下一步 |
| 跨角色交接靠聊天，接收方不知道要做什么 | 默认自洽主文档；按需 `{HO-ID}` 标准包；**未回执不得称已接收** |
| 每个项目都要重新解释一遍规范 | 整包复制即用；规则与实例分离，换项目只填档案 |
| 外部工具不一定装得齐 | 实例 `capabilities/` 清单：已配即用，未配降级，不阻塞 |
| 产物散落在聊天与桌面 | 文档治理：标准树、索引、归档、根目录白名单 |
| 规范越写越多、互相矛盾 | 单一出处；包自检检查引用、锚点、YAML 与版本单点 |

</details>

---

## 三套独立包

选一条轨即可上手；不必一次装全。数量以各包目录与自检为准。

| 包 | 定位 | 上手 |
| --- | --- | --- |
| **[产品规范](./wf-product/README.md)** | 0→1 与迭代：需求 · 竞品 · PRD · 原型 · UAT · 发布 | [说明](./wf-product/README.md) · [入口](./wf-product/AGENTS.md) |
| **[开发规范](./wf-development/README.md)** | L0～L3：澄清 → 实现 → 验证 → 提测 → 发布；含轻量单人轨 | [说明](./wf-development/README.md) · [入口](./wf-development/AGENTS.md) |
| **[测试规范](./wf-testing/README.md)** | 计划驱动：分析 → 计划 → 生成 → 执行 → 报告 | [说明](./wf-testing/README.md) · [入口](./wf-testing/AGENTS.md) |

<details>
<summary><strong>产品 · 开发 · 测试 · 摘要</strong></summary>

**产品**：只写需求、规则、原型、验收；技术架构 / 栈 / 库 / API / 部署留给开发轨。主链含 `new-product` · `plan` · `prd` · `prototype` · `showcase` · `change` · `defect` · `deliver` · `handoff` · `onboard` · `materials`（另含 `skill-audit`）。产物落在 `docs/product/`（单包 `docs/`）。

**开发**：L0 微改走澄清 → 实现 → 验证 → 提交；L1 加轻量需求卡；L2 全链；L3 再加独立评审、安全 / 回滚演练、发布审批。轻量 `solo`＝一页方案卡 → 确认 → 实施 → 自验 → 完成门。产物落在 `docs/development/`（单包 `docs/`）；根 `CHANGELOG.md`＝产品发版史（用户可见能力 / 破坏性 / 迁移 / 安全）。

**测试**：`docs/testing/test-plan.md` 为版本级编排。主链 `testing` · `defect` · `handoff` · `onboard` · `materials`（另含 `skill-audit`）。R0 冒烟 → R1 正式 → R2+ 回归；稳定主链路优先 Playwright；**能脚本不 AI**。P0 未过不得判整体通过。

**单包优先**：只强制本包工作根（`docs/` 平铺；多包 `docs/{owner}/`）；缺他包不阻塞。根 `CHANGELOG.md` 仅开发维护（无开发包则不建）；产/测写 `work-log.md`（发布决策可含对外摘要供开发落笔）。多包发版软序见开发文档治理。原件根固定 `inbound/`；权威文档库项目级 `docs/materials/`。交接：内容优先、包按需；未回执不得称「已接收」。产品 `confirm_release`＝业务决策；开发 `confirm_deploy`＝工程部署。

</details>

---

## 快速开始

### 环境要求

| 依赖 | 用途 | 必需？ |
| --- | --- | --- |
| 支持 `AGENTS.md` 的 AI 编码工具（Cursor / Claude Code / opencode 等） | 执行宿主 | **必需** |
| PowerShell 5.1+ | 包自检 / 完成门 | 维护与过门时 |
| Python 3 + PyYAML | 完成门、YAML schema、文档校验 | **完成门必需**；缺失=BLOCKED（工作流仍可读/执行，但不能声称完成） |
| Node.js + Playwright | 测试脚本档 | 测试脚本轨可选 |
| 浏览器 MCP | UI 功能 / 探索式执行 | 按需 |
| Git | 提交门与版本管理 | 建议 |

### 1. 获取仓库

```bash
git clone https://github.com/zhipenghhuang/AIWorkflow.git
cd AIWorkflow
```

### 2. 只复制一个包到项目根

```bash
# macOS / Linux（以开发规范为例；排除运行态 / 过程文件 / 缓存）
rsync -a --exclude .draft --exclude .state --exclude .gate --exclude __pycache__ \
  wf-development /path/to/your-project/
```

```powershell
# Windows：排除运行态 / 过程文件 / 缓存
robocopy "wf-development" "E:\path\to\your-project\wf-development" /E /XD .draft .state .gate __pycache__
```

> 业务项目只需要**包 + 自己的文档目录**，不要把整个母版仓复制进去。单包放项目根（如 `wf-development/`）；多包放 `wf/`（如 `wf/wf-development/`）。工作根由项目档案 §1 的 `workroot` 声明；未声明时单包用 `docs/`、多包用 `docs/{owner}/`。产品 / 测试换成对应包名。包默认不进入项目 git：`.gitignore` 只写一行 `/<包目录>/`（多包 `/wf/`），不预列未装包、不加注释。
>
> **母版 / 实例**：母版只维护通用高标准。复制后的包默认不改；发现不匹配时先输出拟改内容 / 原因 / 影响，确认后只改当前实例。项目特例优先改产出文档；通用改进回母版升版本。

### 3. 挂载项目根 `AGENTS.md`

**分层**：包内规范 = 通用规则；项目档案（或产品档案 / 环境基线）= 项目事实；根 `AGENTS.md` = 包挂载 +（可选）落地项目自写的对 AI 额外要求——**母版不规定偏好正文**。

已有则**追加**挂载段，不覆盖原文；没有则新建：

```markdown
# AGENTS.md

本项目工作流：先读 `wf-development/AGENTS.md`（存在时）。
细则以该文件为准；该文件不存在时按普通项目继续，不编造包规。
```

挂载样例见各包 `root-agents-pointer.md`；多包路由模板见 `wf-agents-routing-template.md`。

### 4. 让 AI 接入，然后开跑

对 AI 说：

```text
接入开发规范
```

再例如：

```text
开发计划
```

也可以直接说：`轻量开发` · `写 PRD` · `生成测试计划` · `按方案实施` ……

成功标志：AI 首条输出含 `route=… | step=…`，并开始按包内 workflow 推进（遇确认门会停下等你拍板）。

---

## 常用口令

对 AI 说一句人话即可；命中后按 workflow 执行到产出或下一个确认门。

| 包 | 说一句 | 会发生什么 |
| --- | --- | --- |
| 产品 | 任意自然语言描述需求/反馈 | 五元组入口判定 → 意图类路由 |
| 产品 | `启动新产品：{一句话}` / `产品计划` / `写 PRD` / `画原型` | 0→1 · 计划门 · PRD · 原型 |
| 产品 | `需求变更` / `UAT` / `发布` / `复盘` | 变更 · 验收 · 发布决策 · 复盘 |
| 开发 | 任意自然语言描述问题/需求 | 五元组入口判定 → 意图类路由 |
| 开发 | `轻量开发` / `我有个想法：…` | 方案卡 → 确认 → 实施 → 自验 → 收尾 |
| 开发 | `开发计划` / `按方案实施` / `代码评审` / `提测` | 续跑计划 · 实施 · 评审 · 提测 |
| 开发 | `发布` / `回滚` / `复盘` | 上线检查 · 回滚 · 行动项 |
| 测试 | `生成测试计划` / `按测试计划执行` | 计划门 → 分轨执行 → 报告 |
| 测试 | `测试报告` / `提交缺陷` / `回归验证` | 准出 · 查重提交 · 回归 |
| 三包 | `生成交接包` / `装配能力` / `体检能力` | 交接 / 装工具 / 就地优化技能·能力 |
| 三包 | `导出项目文档` / `生成资料库` / `发资料` | 把 `{workroot}/` 定稿整理进 `docs/materials/{ver}/`，生成可整包发送的完整项目文档集 |

更完整口令表见各包 `AGENTS.md`（产品/开发 §3，测试 §2）。口语未命中时，按各自 `rules/core/routing.md` 做意图判定。

<details>
<summary><strong>多包：意图→包（歧义时先查本表）</strong></summary>

单包装载无需本表。同项目启用 ≥2 个包时，口语可能命中多包——**先定包，再走该包口令/入口判定**；无法唯一则一问 + 推荐。

| 用户信号（同义即可） | 进哪包 | 备注 |
| --- | --- | --- |
| 需求/PRD/原型/UAT/产品计划/立项/竞品 | **产品** | |
| 产品侧缺陷评估、PRD 不符、平台产品单回写 | **产品** | `defect` |
| 改代码/方案实施/提测/代码评审/开发计划 | **开发** | |
| 修 Bug、指派开发、复现红证、产品回复后回流 | **开发** | `defect-fix` |
| 测试计划/用例/按计划执行/准出报告 | **测试** | |
| 交平台缺陷、测试查重、测试回归 | **测试** | `defect` |
| 「发布」= 业务能否上线 / UAT 结论 | **产品** | `confirm_release` |
| 「发布」= 部署/回滚/生产变更 | **开发** | `confirm_deploy` |
| 「发布」= 测试准出/报告能否发 | **测试** | `report` |
| 「下一步/继续」 | **看** `activeContext` 当前包分节与计划 §0 | 无焦点则一问 |
| 「提交/推送/交接包」 | **当前会话正在执行的包** | 未开跑则一问 |
| 无法唯一 | 一问 | 附推荐包与取舍 |

根 `AGENTS.md` 只指向 `wf/AGENTS.md`；「已启用包」在 `wf/AGENTS.md`；一次会话只跑一个包。

</details>

---

## 它如何工作

五步执行模型：

1. **路由** — 多包先定包；新会话读包内开局卡 → `AGENTS.md` 口令表 → 命中 workflow；首条输出 `route=… | step=… | reads=…`；纯解释走 `readonly:analysis`
2. **加载** — 开局卡 → 当前 YAML step 块（门/`must_read`）→ `rules/packets/<workflow>/<step>.md`（本步唯一正文）→ 若包内点名再开一个模板。**同会话中段**：【规则心跳】重锚（`rules/core/rule-anchor.md`），不重读开局卡全文
3. **执行** — 步内方法以步骤包为准；`when` 条件跳过；步上 `hitl` 必须确认；切步/过门须心跳
4. **验证** — `verify/Invoke-Gate.ps1`；只有门能授予 `COMPLETE` / `PASS` / `READY`
5. **落盘** — 写入本包标准目录，更新索引 / 计划 / 项目侧 `activeContext.md`

<details>
<summary><strong>分层落点</strong></summary>

| 层 | 落点 |
| --- | --- |
| Workflow | `workflows/*.yaml` |
| Agent 契约 | `agents/*.yaml` |
| 开局卡 / 门 / 步骤包 / 重锚 | `rules/core/cold-start.md` · `rules/gates.md` · `rules/packets/` · `rules/core/rule-anchor.md` |
| 协作交接 | `rules/collaboration/` + `workflows/handoff.yaml` |
| 专业技能（维护素材；运行时已嵌入步骤包） | `skills/<name>/SKILL.md` |
| 能力层 | 包内契约+参考目录；实例真源 `{工作根}/capabilities/` |
| 验证层 | `verify/`（运行态 → 项目根 `.gate/`） |
| 文档治理 | `rules/doc-governance.md` + `rules/templates/` |
| 工作根 | 项目档案 §1 的 `workroot`；默认单包 `docs/`、多包 `docs/{owner}/` |
| 权威文档库 | 项目级 `docs/materials/{ver}/`（00-overview～07-appendix；README + INDEX） |

执行宿主是任意支持 `AGENTS.md` 自动装载的 AI 编码工具，**不自研编排引擎**。

</details>

---

## 确认门与质量闸

确认门只认 workflow 步骤上的 `hitl`；条件不满足会自动跳过。开跑前按各包 `rules/core/clarification.md`：先分析，再给「我的理解 + 建议 + 需要你拍板（0～1 个）」；总提问 ≤3。

| 包 | 关键确认门 |
| --- | --- |
| 产品 | 立项 · 计划 · 范围 · PRD · 设计 · 原型交接 · 变更 · 交接 · 发布 · 提交 |
| 开发 | 计划 · 需求基线 · 方案 · 任务清单 · 交接 · 部署 · 回滚 · 验收 · 提交 |
| 开发（solo） | 产品定义（按需） · 方案卡 · 提交 |
| 测试 | 计划 · 执行范围 · 交接 · 提交 · 缺陷回写 |

| 闸 | 规则 |
| --- | --- |
| PRD / 方案 / 清单 | 未定稿不排期；未批准不实施；RP / AC / DoR / DoD 覆盖后冻结 |
| 代码门禁 | 失败不声称完成；禁止改断言、跳测试、关告警凑绿 |
| 发布 | 上线检查单 + 审批 + 回滚预案 + 验证 |
| 测试准出 | P0 未过不得整体通过；证据可打开；缺口显式列出 |
| 交接 | 未回执不得称「已接收」；可称「已发送」 |

---

## 仓库结构

```text
AIWorkflow/
├─ wf-product/          # 产品轨母版
├─ wf-development/          # 开发轨母版（含轻量单人轨）
├─ wf-testing/          # 测试轨母版
├─ CHANGELOG.md       # 母版仓产品发版史
├─ THIRD_PARTY.md     # 第三方方法与来源
├─ LICENSE            # MIT
└─ README.md
```

每个包内部结构一致：

```text
{包}/
├─ AGENTS.md             # AI 入口（版本单点）
├─ README.md             # 给人看的上手说明
├─ workflows/*.yaml
├─ agents/*.yaml
├─ skills/<name>/SKILL.md
├─ capabilities/00-contract.md · reference.md
├─ rules/                 # 门 · 读取索引 · 核心/协作/模板/tools …
└─ verify/                 # checks.yaml、完成门；运行态 → .gate/
```

<details>
<summary><strong>文档落点（实例侧）</strong></summary>

各包只强制本包工作根；未装的包不必建对应目录。项目根只保留白名单（档案入口、`activeContext.md`、原始资料根等）。

| 类别 | 落点 |
| --- | --- |
| 开发轨 | `docs/development/`（单包 `docs/`）：`00-governance` · `10-requirements` · `20-design` · `30-architecture/ADR` · `40-tasks` · `50-verification` · `60-release` · `70-ops` · `80-retrospectives`；`capabilities/` · `handoff/` · `_archive/` 不编号 |
| 产品版本目录 | `docs/product/{ver}/`（单包 `docs/{ver}/`）：`10-requirements` · `20-design` · `30-changes` · `40-delivery` · `50-showcase` · `90-retrospectives`；`00-governance/` · `user/` · `capabilities/` 不编号 |
| 测试轨 | `docs/testing/`（单包 `docs/`）：`test-plan.md` · `test-analysis.md` · `test-report.md` · `smoke-checklist.md` · `functional/` · `api/` · `exploratory/` · `random-flows/` · `pre-release/`；`capabilities/` |
| 原件根 | `inbound/` + `INDEX.md`（全量外部输入；不归档/不迁出） |
| 权威文档库 | `docs/materials/{ver}/`（项目级；00-overview～07-appendix；README + INDEX；自包含；不归档） |
| 交接 | `{workroot}/handoff/outbound\|inbound/{category}/` + `handoff-ledger.md`（升包含 `{HO-ID}/`） |
| 索引 | 工作区 `{workroot}/INDEX.md`（单包即 `docs/INDEX.md`）；多包或保留原目录另有总览 `docs/INDEX.md`（不写状态） |
| 编号 | 生命周期域用 `00`～`80`/`10`～`90` 稳定地址，跳号插入不重编；并列/跨切面（`capabilities`/`handoff`/`_archive`、测试轨）不编号；编号不代表阶段/门 |
| 产品发版史 | `CHANGELOG.md`（开发维护；用户可见能力 / 破坏性 / 迁移 / 安全） |

</details>

---

## 设计原则

- **框架固定，局部自主** — 口令映射、步上 `hitl`、输出骨架、证据与红线默认按规则；冲突时先说明风险，用户再次明确后以用户为准。
- **完成只认门** — Agent 不能自证 `COMPLETE` / `PASS` / `READY`。
- **按风险分级** — 低风险少文档，高风险才全链。
- **规则与实例分离** — 通用规范在包内；项目档案与业务产物在实例侧。
- **技能随包，能力跟实例** — 技能给方法；能力选型/绑定在 `{工作根}/capabilities/`，包内仅契约与参考目录。
- **单一出处** — `template_version` 只写在各包 `AGENTS.md`；根 README 不缀版本号为权威源（徽章仅导航提示，真源仍看各包）。
- **文档现行有效** — 只写当前存在的功能与规则。
- **内容优先 · 包按需** — 默认自洽主文档；升包才 `{HO-ID}`。
- **宿主无关** — 包内只写能力名，不写宿主名和本地路径。
- **三维同向 / 做减法** — 兼顾 UX · DX · AX；界面先删无决策价值文案。

---

## 适用场景

**适合**

- 想把 AI 协作从「聊天」变成可复用流程的产品 / 研发 / 测试团队
- 需要人工审批、证据链和文档留痕的项目
- 要在多个项目、多个宿主之间复用同一套规范
- 希望 AI 按变更大小自动裁剪流程

**不适合**

- 只想要一份提示词模板
- 无需流程与留痕的一次性脚本
- 希望 AI 完全自动、不要任何确认门的场景

---

## FAQ

**需要安装编排引擎吗？**  
不需要。执行器就是支持 `AGENTS.md` 的 AI 编码工具；YAML 是给 AI 读的流程定义。

**三个包必须一起装吗？**  
不必。默认单包独立落地；多包联动可选，不因缺他包阻塞。

**没有 Python / Node.js 能跑吗？**  
工作流可以读、可以按步骤执行；但**完成门需要 Python**，缺失会返回 `BLOCKED`，不会降级成“已完成”。Node.js 只在测试脚本轨需要，缺失按降级处理。

**会不会强制写很多文档？**  
不会。开发 L0 不强制文档；L1 轻量；L2/L3 才走完整链。测试按计划装填（suite=core|module|full）。

**支持哪些宿主？**  
任何支持 `AGENTS.md` 入口自动装载与文件读写 / 命令执行 / 对话确认的工具均可。包本身不绑定宿主。

**可以改成我们团队的流程吗？**  
可以。落地后直接改项目里的包副本（推荐「体检能力」确认后再改）。若维护通用母版并多项目同步：优先在母版改，自检后整包同步——同步会覆盖未回灌的实例侧包内改动。

**版本怎么看？**  
只认各包 `AGENTS.md` 的 `template_version`；根 [CHANGELOG.md](./CHANGELOG.md) 记产品发版史，不是版本声明源。

---

<details>
<summary><strong>自检与完成门（维护 / 贡献时）</strong></summary>

改包后或用户点名时运行；业务任务不例行自检。自检为本地/按需，不依赖 CI。执行契约见各包 `rules/core/execution-contract.md`；外部方法来源见 [THIRD_PARTY.md](./THIRD_PARTY.md)。

```powershell
powershell -ExecutionPolicy Bypass -File "wf-product/rules/tools/Test-Template.ps1"
powershell -ExecutionPolicy Bypass -File "wf-development/rules/tools/Test-Template.ps1"
powershell -ExecutionPolicy Bypass -File "wf-testing/rules/tools/Invoke-TestWorkflow.ps1" -Action ValidateTemplateRefs
python wf-product/rules/tools/check_skills.py wf-product --strict
python wf-development/rules/tools/check_skills.py wf-development --strict
python wf-testing/rules/tools/check_skills.py wf-testing --strict
```

完成门示例：

```powershell
powershell -ExecutionPolicy Bypass -File "wf-development/verify/Invoke-Gate.ps1" -ProjectRoot "."
powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Mode report -ProjectRoot "."
powershell -ExecutionPolicy Bypass -File "wf-product/verify/Invoke-Gate.ps1" -Mode prd -ProjectRoot "."
```

单项校验（PRD / 任务清单 / 用例 / 交接包等）见各包 `rules/tools/`。

</details>

---

## 文档导航

| 文档 | 说明 |
| --- | --- |
| [产品规范 README](./wf-product/README.md) · [AGENTS](./wf-product/AGENTS.md) | 产品轨上手与 AI 入口 |
| [开发规范 README](./wf-development/README.md) · [AGENTS](./wf-development/AGENTS.md) | 开发轨上手与 AI 入口 |
| [测试规范 README](./wf-testing/README.md) · [AGENTS](./wf-testing/AGENTS.md) | 测试轨上手与 AI 入口 |
| [CHANGELOG](./CHANGELOG.md) | 母版仓产品发版史 |
| [THIRD_PARTY](./THIRD_PARTY.md) | 第三方方法与来源 |
| [LICENSE](./LICENSE) | MIT |

---

## 反馈与贡献

欢迎通过 [Issues](https://github.com/zhipenghhuang/AIWorkflow/issues) 提出问题或建议。

提交 PR 前请说明：

1. **改动范围**（哪个包 / 哪一层：workflow · agent · 规则 · 技能 · 模板）
2. **验证方式**（跑了哪些自检 / 完成门）
3. 若改了规则或路径，是否同步了读取索引与包 README

<details>
<summary><strong>维护约定</strong></summary>

- 改步骤 → `workflows/`；改角色 → `agents/`；改红线 / 输出 → `rules/`；改方法 → `skills/`；改槽位契约/参考目录 → 包内 `capabilities/`；改项目选型/绑定 → 实例 `{工作根}/capabilities/`
- 落地：「体检能力」技能改包内 `skills/`，能力改实例 `capabilities/`；契约通用改进回母版
- 维护通用母版时：改动先落本仓再同步；实例 `capabilities/` 不在包内，不被包同步覆盖
- 分支：仅维护 `main`

</details>

---

## 维护者

[zhipenghhuang](https://github.com/zhipenghhuang)

## License

本项目采用 [MIT License](./LICENSE)。
