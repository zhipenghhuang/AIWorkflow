---
name: presentation-design
description: Use when creating a one-pager, pitch deck outline, or demo visuals. Structures the narrative, uses Mermaid diagrams and clear visual hierarchy, aligns with the project, and avoids generic AI-looking slides.
---

# 展示材料设计（技能 · 随包生效）

> 用于：`showcase` 的 materials 步。  
> 目标：**一页一个观点；图服务于结论；与项目真实情况一致。**

## 1. 一页纸（One-pager）

| 区块 | 内容 |
| --- | --- |
| 一句话 | 为谁解决什么问题，凭什么 |
| 问题/代价 | 现状 + 证据（来源/日期） |
| 方案 | 关键能力（3～4 个） |
| 价值 | 指标/收益/案例 |
| 证据 | 数据/客户/试点/测试 |
| 下一步 | 决策/试用/联系 |

- 一页只讲一个主张；数字有来源；不堆功能。

## 2. Deck 大纲（10～12 页）

1. 封面（受众/日期/版本）
2. 背景与目标
3. 问题与代价（证据）
4. 方案总览（Mermaid 流程图）
5. 关键场景 1（演示/截图）
6. 关键场景 2
7. 差异化/竞品（来源+日期）
8. 价值/ROI/案例
9. 实施/集成/风险（业务视角）
10. 路线图/下一步
11. 结论与请求（决策/试用）
12. 附录（数据来源/术语）

- 每页：标题=结论；正文 ≤3 点；图/表优先；避免大段文字。
- 流程图用 Mermaid：`flowchart LR` 表达用户任务/价值流；技术架构图归开发，不放进产品 Deck（除非受众是技术评审且由开发提供）。

## 3. 视觉规范

- 一套主色 + 中性色；字号阶 ≤4 级；间距统一。
- 图表：先结论后图；坐标轴/单位/来源清楚。
- 截图：当前构建、脱敏、标注关键点；不拉伸/不模糊。
- 避免 AI 味：紫蓝渐变、无意义玻璃拟态、图标堆砌、每页大标题。

## 4. 项目对齐

- 每个数字/截图/流程能回指 PRD/原型/构建/UAT；
- 术语与产品一致；未实现能力标“后续”；
- 对外版本与 GTM/发布说明一致；
- 真实客户信息脱敏；演示数据标注“示例”。

## 5. 可访问性

- 对比度 ≥4.5:1；字号 ≥18pt（投影）；不只用颜色传达状态；
- 图表有文字结论；视频/动效有静态兜底。

## 6. 可选工具（不强制）

- `anthropics/skills` doc-suite（docx/pptx/pdf）
- `zarazhangrui/frontend-slides`（HTML 演示稿，MIT）
- `addsumtech/slides_maker`（可编辑 PPTX，MIT）

包内模板优先；工具只增强，不改变内容标准。
