# 能力契约（包侧 · 非实例真源）

> **定位**：本包 workflow/agent 可引用的**槽位契约**（`tools:` / `tools_allowed:` ⊆ 本表能力名）。  
> **实例真源**：工作根 `{workroot}/capabilities/00-能力清单.md`。正文细节只在 `{workroot}/capabilities/`；产品档案等**仅索引**。  
> **参考**：`capabilities/reference.md`（非真源）。纪律见 `rules/capabilities/instance-discipline.md`。  
> **维护**：新增能力名先登记本表再引用；改后跑 `rules/tools/Test-Template.ps1`。设计类外部能力全部可选。

## 1. 槽位契约

| 能力名 | 意图槽 | 用于 | 最低能力面 | 缺失时 | 核心 |
| --- | --- | --- | --- | --- | --- |
| `git` | git | 文档提交/推送 | — | 停并报告 | 是 |
| `子代理` | subagent | 分片/侦察/核验 | 宿主子代理 | 单上下文 | 否 |
| `defect-platform` | defect-platform | 产品缺陷协作 | 平台读写或 export | export | 否 |
| `docs-mcp` | docs-mcp | 查inbound/文档 | 文档检索 | 主读+用户输入 | 否 |
| `browser-automation` | browser-automation | 竞品/后台/反馈页 | navigate · snapshot | 用户提供资料 | 否 |
| `browser-mcp` | browser-automation | 同上（别名） | 同左 | 同左 | 否 |
| `spec-clarify` | spec-clarify | 客户访谈/澄清 | 访谈方法 | 包内澄清+技能 | 否 |
| `pm-skills` | pm-skills | PM 方法库 | 外部 PM skills | 包内技能 | 否 |
| `clarify-grill` | clarify-grill | 深挖澄清问法 | 外部 grill skill | 包内澄清+customer-needs | 否 |
| `prototype-skill` | prototype-skill | 原型边界方法增强 | 外部原型 skill | 包内 prototype-and-interaction | 否 |
| `handoff-skill` | handoff-skill | 交接手艺增强 | 外部 handoff skill | 包内交接规则 | 否 |
| `skill-discovery` | skill-discovery | 生态技能检索 | `npx skills find` / find-skills | 只对照参考目录 | 否 |
| `design-diagram` | design-diagram | 流程/状态/IA 图 | 绘图 | 文字描述 | 否 |
| `design-intelligence` | design-intelligence | 视觉方向/设计系统 | 设计 skill | 包内 UI 技能 | 否 |
| `ui-generation` | ui-generation | 高保真生成 | 生成 CLI/skill | 包内原型技能+脚手架 | 否 |
| `frontend-design` | frontend-design | 视觉方向 | 设计 skill | 包内 UI 技能 | 否 |
| `design-review` | design-review | 无障碍/UX 审查 | 审查工具 | 包内清单 | 否 |
| `design-tokens` | design-tokens | 提取 tokens | 提取工具 | 手工定 tokens | 否 |
| `prototype` | prototype | 原型读取/走查 | 设计工具 MCP | 截图/链接描述 | 否 |
| `doc-suite` | doc-suite | 文档导出 | docx/pptx 等 | Markdown | 否 |
| `presentation` | presentation | 演示稿增强 | 幻灯/HTML 工具 | 包内 presentation-design | 否 |
| `demo-video` | demo-video | 演示视频 | 视频 skill | 现场+截图 | 否 |
| `gtm` | gtm | GTM/销售赋能 | GTM skill | 包内 GTM 模板 | 否 |
| `issue-tracker` | issue-tracker | 需求池同步 | 平台同步 | 本地 Markdown | 否 |
| `analytics` | analytics | 数据口径核对 | SQL/BI | 用户数据摘要 | 否 |
| `experimentation` | experimentation | A/B/灰度 | 实验平台 | 手工+BI | 否 |
| `product-analytics` | product-analytics | 事件/漏斗 | 分析平台 | 事件字典+SQL | 否 |

## 2. 缺失提示（触达可见 · 分档）

> 降级可续跑，但不得静默。status / 接受降级见 `rules/capabilities/instance-discipline.md`。`git` 核心缺失 → 停并报告（不用本块替代）。

### 2.1 何时出块

| 条件 | 行为 |
| --- | --- |
| 清单 `available` | 静默使用 |
| **硬触达**未装 / `missing` / `undecided` / 仅 `prompted`（无 `accepted`） | 本战役**首次**命中该槽 → 必出【能力缺失】全块；同战役再触达一行短提醒 |
| **软触达**未装 | 不出全块；本步因缺能力致产出缩水/定稿风险 ↑ → 收尾「适度建议」至多 1 条 |
| 「接受降级」/「暂不装」 | `degraded` + `accepted=YYYY-MM-DD`；同会话免全块；新会话/新战役短提醒 |
| 「装配能力」 | 装成后 `available`，停提示 |

**硬触达**：`defect-platform`（defect / 回写）；本步确需页面取证时的 `browser-automation` / `browser-mcp`；本步确需平台同步时的 `issue-tracker`。  
**软触达**：其余可选增强（如 `pm-skills`、`design-*`、`doc-suite`、`presentation`、`demo-video`、`gtm` 等）。

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
| `defect-platform` | defect / 回写 | 粘贴/导出；无平台读写 |
| `browser-automation` / `browser-mcp` | 竞品/后台/反馈页取证 | 用户提供链接/截图 |
| `issue-tracker` | 需求池同步 | 本地 Markdown |
