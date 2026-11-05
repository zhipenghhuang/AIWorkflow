# 流程链 · control

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：wf-development
- **workflow**：`control`（开发计划）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 入口

- `开发计划` → step `init`
- `项目计划` → step `init`
- `排期` → step `init`
- `生成计划` → step `init`
- `根据文档出计划` → step `init`
- `按开发计划执行` → step `run`
- `继续开发计划` → step `run`
- `进度` → step `sync`
- `当前阶段` → step `sync`
- `当前状态` → step `sync`
- `下一步` → step `next`
- `阶段检查` → step `check`

## 状态机（父）→ 子机

长链路按**子状态机**切开：进某区先读该区 `_region-*`（一次），区内逐步推进；不要把整条父链步骤包一次读完。

| 子机 | 含义 | 地图 |
| --- | --- | --- |
| `steer` | 总控推进 | `rules/packets/control/_region-steer.md` |
| `close` | 收尾 | `rules/packets/control/_region-close.md` |

## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `init` | 初始化开发计划 | `—` | `_region-steer` | `rules/packets/control/init.md` |
| 2 | `run` | 按计划执行 | `—` | `_region-steer` | `rules/packets/control/run.md` |
| 3 | `sync` | 同步阶段与证据 | `—` | `_region-steer` | `rules/packets/control/sync.md` |
| 4 | `check` | 阶段门检查 | `—` | `_region-steer` | `rules/packets/control/check.md` |
| 5 | `next` | 下一步建议 | `—` | `_region-steer` | `rules/packets/control/next.md` |
| 6 | `wrap` | 收尾 | `—` | `_region-close` | `rules/packets/control/wrap.md` |
| 7 | `commit` | 拟提交 | `—` | `_region-close` | `rules/packets/control/commit.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次；出区再进下一子机。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
