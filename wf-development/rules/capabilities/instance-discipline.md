# 实例能力纪律（开发）

> **读取级别：参考**。装配 / 体检 / 首次触达外部工具时读；业务顺跑只读 `{workroot}/capabilities/00-能力清单.md` 相关行。

## 1. 单一出处

- **真源**：`{workroot}/capabilities/`（清单必有；`槽位/` · `绑定/` · `装配/` 按需）。
- **禁双写**：`project-profile.md` 等**不得**维护完整选型/绑定正文；只索引 `{workroot}/capabilities/00-能力清单.md`。
- **包侧**：`capabilities/00-contract.md` + `capabilities/reference.md`。实例选型不写回包内。

## 2. 渐进读

清单 →（按需）`槽位/` →（按需）`绑定/`。无清单时首次命中或「装配能力」再建。

## 3. kind 与纪律

同测试包语义：`mcp`｜`skill-cli`｜`builtin`｜`none`。禁静默换 `impl`。浏览器冒烟若复用测试实例，清单写 `复用=docs/testing/capabilities/…`，不复制绑定正文。

## 4. 口令

装配 → 写 `{workroot}/capabilities/`；体检能力部分只改实例 `{workroot}/capabilities/`，技能改包内 `skills/`。

## 5. 安全

无密钥入库；配置入口只记宿主用户级路径类型。
