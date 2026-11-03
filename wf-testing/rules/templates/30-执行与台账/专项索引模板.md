# 专项索引（功能 / 发布前）

> **用途**：登记功能专项 `S-*` 或发布前专项及其状态（供人工追踪）。  
> **落盘**：  
> - 功能专项：`{workroot}/functional/00-专项索引.md`（可与台账侧同名索引互链，以本文件为登记真值）  
> - 发布前：`{workroot}/pre-release/00-发布前索引.md`  
> 生成专项资产时增一行；状态变化时更新该行，勿删历史行（可改备注）。

## 1. 状态定义（供追踪 · 不阻断执行）

| 状态 | 含义 | 说明 |
| --- | --- | --- |
| 启用 | 资产齐全、当前有效 | 直接执行（门2 仍须确认） |
| 停用 | 暂不执行或已废弃 | 被点名执行时先提醒一次 |
| 草稿 | 生成中/未收口 | 可直接执行；执行即视为收口 |

## 2. 索引表

| ID | 主题 | 状态 | 用例/方案路径 | 台账/报告路径 | 备注 |
| --- | --- | --- | --- | --- | --- |
| S-01 | `{主题}` | 草稿/启用/停用 | `{workroot}/functional/S-01-{主题}/S-01-{主题}-功能用例.md` | `{workroot}/functional/S-01-{主题}/S-01-{主题}-功能台账.md` |  |
| PERF | 性能 | 草稿/启用/停用 | `{workroot}/pre-release/performance/性能-测试方案.md` | `{workroot}/pre-release/performance/性能-test-report.md` |  |
| SEC | 安全 | 草稿/启用/停用 | `{workroot}/pre-release/security/安全-测试方案.md` | `{workroot}/pre-release/security/安全-test-report.md` |  |
| COMPAT | 兼容 | 草稿/启用/停用 | `{workroot}/pre-release/compatibility/兼容-测试方案.md` | `{workroot}/pre-release/compatibility/兼容-test-report.md` |  |
