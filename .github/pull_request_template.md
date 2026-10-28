## 改动范围

- 包：产品规范 / 开发规范 / 测试规范 / 母版根
- 层：workflow · agent · 规则 · 技能 · 能力 · 模板 · 验证 · 文档治理
- 关联 issue / 变更单：

## 为什么改

- 问题 / 风险：
- 不改的影响：
- 目标（可验证）：

## 验证

- [ ] `validate_workflow.py <包>`
- [ ] `Test-Template.ps1`（产品/开发）或 `Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`（测试）
- [ ] `Test-DocHygiene.ps1`
- [ ] 相关门 dry-run / fixture（如改门）
- [ ] 改步骤后同步了 `读取索引.md`、`技能/README.md`、包 README、根 README 计数
- [ ] 改规则/门后检查了 `门.md` 词表与 `gate_type`
- [ ] 新增/删除技能后检查了 workflow/agent 引用（无零引用、无悬空）
- [ ] 版本只在三包 `AGENTS.md` 单点更新，并写 `CHANGELOG.md`

## 风险与回滚

- 破坏性变更 / 迁移：
- 回滚方式：
- 需要人工确认的点：

## 自检

- [ ] 没有把项目实例产物/密钥/真实 PII 带入母版
- [ ] 没有新增「只写 gate、无检查方法」的空门
- [ ] 没有把低价值步骤写成必走；跳过条件已写明
