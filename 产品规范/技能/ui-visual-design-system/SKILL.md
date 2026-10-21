---
name: ui-visual-design-system
description: Use when choosing a visual direction, defining design tokens, or reviewing UI consistency, accessibility, and responsiveness. Provides a self-contained design system, project-fit criteria, and review scorecard that works without external design skills.
---

# UI 视觉与设计系统（技能 · 随包生效）

> 用于：`prototype` 的 visual / review 步。  
> 目标：无设计师时也能出一致、清晰、贴合项目、可用的界面；不追求品牌级高定。

## 1. 项目适配（先定方向）

- 用户/场景/环境：B 端后台（信息密度/效率）｜C 端（亲和/引导）｜数据产品（对比/图表）｜移动作业（触控/弱网/拍照）｜单据打印（A4/核对）。
- 品牌/现有系统：主色、字体、圆角、密度、术语；能复用则复用，不另造一套。
- 2～3 个视觉方向，按“适配度/实用性/美观/实现成本”选 1 个，说明理由。
- 避免「AI 味」：紫蓝渐变、无意义玻璃拟态、过多圆角/阴影、图标堆砌、每页大标题。

## 2. Design tokens（先定后画）

- 颜色：主色 / 辅色 / 中性 / 语义（success / warning / danger / info）；每色 1～2 变体。
- 字体：1 个主字体 + 字号阶（12 / 14 / 16 / 20 / 24 / 32）；行高 1.4～1.6。
- 间距：4 / 8 基准（4 / 8 / 12 / 16 / 24 / 32 / 48）。
- 圆角 / 边框 / 阴影：各 2～3 档，统一使用。
- 落 `design-tokens.css` CSS 变量；禁止页面里散落硬编码。

## 3. 布局与层级

- 栅格 / 最大宽度 / 留白；一屏一个主任务；标题 / 正文 / 辅助三级。
- 密度：B 端可紧凑，C 端留白；不要同时高密度 + 大圆角。
- 对齐：左对齐为主；数字右对齐；表格列宽稳定；表单标签位置统一。

## 4. 组件清单

按钮（主/次/危险/禁用/loading）、输入/选择/日期、表格（排序/筛选/分页/空态）、卡片、标签、Tabs、弹窗、Toast、面包屑、步骤条、空态、错误页。

- 每个组件定义：尺寸 / 状态 / 文案 / 交互 / tokens。
- 组件状态：default / hover / focus / active / disabled / loading / error。
- 同类页面复用同一组件；不因页面不同改交互。

## 5. 设计评审清单（12 项评分卡）

| # | 维度 | 0～2 分 | 阻断 |
| ---: | --- | --- | --- |
| 1 | 项目情境贴合 | 用户/任务/环境/约束 | 是 |
| 2 | 覆盖完整（PRD F/A） | 页面/路由/状态 | 是 |
| 3 | IA/导航 | 主任务可达、无死路 | 是 |
| 4 | 交互/反馈 | 校验/确认/撤销/loading | 是 |
| 5 | 状态完整 | 空/加载/失败/成功/禁用/无权限/边界 | 是 |
| 6 | 数据真实 | seed/关系/边界/重置 | 重要 |
| 7 | 响应式/手机 | 主任务可完成 | 是 |
| 8 | 无障碍 | 对比度/焦点/键盘/label/alt | 是 |
| 9 | 视觉/设计系统 | tokens/组件/层级/密度 | 重要 |
| 10 | 打印/导出 | 单据 A4/门槛（如适用） | 是 |
| 11 | 可用性 | 关键任务走查/启发式 | 重要 |
| 12 | 版本/交接 | 原型/PRD 版本、组件/状态/交互 | 重要 |

> 阻断项必须 2 分；总分 ≥20/24 且无阻断才可交接。

## 6. 交付

- tokens 文件 + 组件说明 + 页面路径/截图 + 无障碍证据；问题分级（阻断/重要/建议）。
- 原型 ≠ 生产代码；开发按项目框架实现，不直接上线原型。

## 7. 参考（可选，不随包）

WCAG 2.2 AA、Material / Apple HIG、Vercel Web Interface Guidelines、Refactoring UI、Nielsen 10；需要时查，不强制安装。
