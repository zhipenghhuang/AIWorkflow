# 专项索引（功能 / 发布前）

> **用途**：登记功能专项 `S-*` 或发布前专项及其状态（供人工追踪）。  
> **落盘**：  
> - 功能专项：`{workroot}/{ver}/functional/00-专项索引.md`  
> - 发布前：`{workroot}/{ver}/pre-release/00-发布前索引.md`  
> 生成专项资产时增一行；状态变化时更新该行。

## 1. 状态定义（供追踪 · 不阻断执行）

| 状态 | 含义 | 说明 |
| --- | --- | --- |
| 启用 | 资产齐全、当前有效 | 直接执行（`confirm_execution_scope` 仍须确认） |
| 停用 | 暂不执行或已废弃 | 被点名执行时先提醒一次 |
| 草稿 | 生成中/未收口 | 可直接执行；执行即视为收口 |

## 2. 索引表

| ID | 主题 | 状态 | 执行记录/方案路径 | 证据/报告路径 | 备注 |
| --- | --- | --- | --- | --- | --- |
| S-01 | `{主题}` | 草稿/启用/停用 | `{workroot}/{ver}/functional/S-01-{主题}-执行记录.md` | `{workroot}/{ver}/evidence/` |  |
| PERF | 性能 | 草稿/启用/停用 | `{workroot}/{ver}/pre-release/性能-测试方案.md` | `{workroot}/{ver}/pre-release/性能-test-report.md` |  |
| SEC | 安全 | 草稿/启用/停用 | `{workroot}/{ver}/pre-release/安全-测试方案.md` | `{workroot}/{ver}/pre-release/安全-test-report.md` |  |
| COMPAT | 兼容 | 草稿/启用/停用 | `{workroot}/{ver}/pre-release/兼容-测试方案.md` | `{workroot}/{ver}/pre-release/兼容-test-report.md` |  |
