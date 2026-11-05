# 流程链 · onboard

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：产品
- **workflow**：`onboard`（产品规范接入）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 入口

- `接入产品规范` → step `mount`
- `重新接入` → step `migrate`
- `生成产品档案` → step `profile`
- `配置缺陷平台` → step `profile`
- `生成README` → step `profile`
- `更新README` → step `profile`
- `整理README` → step `profile`
- `装配能力` → step `capabilities`
- `资料收取` → step `materials`
- `资料整理` → step `materials`
- `资料归档` → step `materials`
- `资料巡检` → step `materials`
- `文档整理` → step `lifecycle`
- `文档巡检` → step `lifecycle`
- `文档清理` → step `lifecycle`
- `清理临时文件` → step `lifecycle`
- `清理过程文件` → step `lifecycle`
- `清理无效文件` → step `lifecycle`
- `清理失效文件` → step `lifecycle`
- `清理垃圾文件` → step `lifecycle`

## 状态机

本 workflow 步骤较少，无额外子机；按阶段表逐步打开步骤包即可。


## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `migrate` | 旧结构迁移 | `—` | — | `rules/packets/onboard/migrate.md` |
| 2 | `mount` | 复制与挂载确认 | `—` | — | `rules/packets/onboard/mount.md` |
| 3 | `profile` | 产品档案与上下文 | `—` | — | `rules/packets/onboard/profile.md` |
| 4 | `materials` | 资料收取与归档 | `—` | — | `rules/packets/onboard/materials.md` |
| 5 | `lifecycle` | 文档治理检查 | `—` | — | `rules/packets/onboard/lifecycle.md` |
| 6 | `gitignore` | 入库策略 | `—` | — | `rules/packets/onboard/gitignore.md` |
| 7 | `capabilities` | 环境与工具检查（可选） | `—` | — | `rules/packets/onboard/capabilities.md` |
| 8 | `verify` | 核验与打标 | `—` | — | `rules/packets/onboard/verify.md` |
| 9 | `wrap` | 收尾 | `—` | — | `rules/packets/onboard/wrap.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次；出区再进下一子机。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
