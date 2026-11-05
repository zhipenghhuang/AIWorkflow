# 流程链 · release

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：开发
- **workflow**：`release`（发布与上线）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 入口

- `发布` → step `readiness`
- `上线` → step `readiness`
- `发版` → step `readiness`
- `生产部署` → step `readiness`
- `正式部署` → step `readiness`
- `回滚` → step `rollback`

## 状态机（父）→ 子机

长链路按**子状态机**切开：进某区先读该区 `_region-*`（一次），区内逐步推进；不要把整条父链步骤包一次读完。

| 子机 | 含义 | 地图 |
| --- | --- | --- |
| `ready` | 就绪与批准 | `rules/packets/release/_region-ready.md` |
| `go` | 部署验证 | `rules/packets/release/_region-go.md` |
| `after` | 事后收尾 | `rules/packets/release/_region-after.md` |

## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `readiness` | 发布就绪检查 | `—` | `_region-ready` | `rules/packets/release/readiness.md` |
| 2 | `acceptance` | 业务验收 | `has_uat` | `_region-ready` | `rules/packets/release/acceptance.md` |
| 3 | `approval` | 工程部署审批 | `release_ready_and_acceptance_passed` | `_region-ready` | `rules/packets/release/approval.md` |
| 4 | `deploy` | 部署 | `release_approved` | `_region-go` | `rules/packets/release/deploy.md` |
| 5 | `verify` | 发布验证 | `has_deployed` | `_region-go` | `rules/packets/release/verify.md` |
| 6 | `rollback` | 回滚 | `release_failed_or_direct_rollback` | `_region-go` | `rules/packets/release/rollback.md` |
| 7 | `postrelease` | 发布后观察 | `has_deployed` | `_region-after` | `rules/packets/release/postrelease.md` |
| 8 | `record` | 发布记录 | `has_deployed` | `_region-after` | `rules/packets/release/record.md` |
| 9 | `retro` | 发布复盘 | `incident_or_major_release` | `_region-after` | `rules/packets/release/retro.md` |
| 10 | `wrap` | 收尾 | `—` | `_region-after` | `rules/packets/release/wrap.md` |
| 11 | `commit` | 拟提交 | `—` | `_region-after` | `rules/packets/release/commit.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次；出区再进下一子机。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
