# 流程链 · defect

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：产品
- **workflow**：`defect`（产品缺陷平台协作）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 入口

- `拉取产品缺陷` → step `preflight`
- `我的产品缺陷` → step `preflight`
- `缺陷平台产品缺陷` → step `preflight`
- `禅道产品缺陷` → step `preflight`
- `产品缺陷` → step `preflight`
- `产品缺陷评审` → step `preflight`
- `开发评估单评审` → step `preflight`
- `产品缺陷处置` → step `preflight`
- `产品判定` → step `preflight`
- `产品判定回流` → step `preflight`
- `平台回写` → step `writeback`
- `回写产品缺陷` → step `writeback`
- `粘贴产品缺陷` → step `pull`
- `文档产品缺陷` → step `pull`

## 状态机（父）→ 子机

长链路按**子状态机**切开：进某区先读该区 `_region-*`（一次），区内逐步推进；不要把整条父链步骤包一次读完。

| 子机 | 含义 | 地图 |
| --- | --- | --- |
| `pull` | 拉取分析 | `rules/packets/defect/_region-pull.md` |
| `act` | 处置回写 | `rules/packets/defect/_region-act.md` |
| `close` | 收尾 | `rules/packets/defect/_region-close.md` |

## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `preflight` | 平台配置与可用性 | `—` | `_region-pull` | `rules/packets/defect/preflight.md` |
| 2 | `pull` | 拉取与读取 | `—` | `_region-pull` | `rules/packets/defect/pull.md` |
| 3 | `source` | 来源识别 | `—` | `_region-pull` | `rules/packets/defect/source.md` |
| 4 | `analyze` | 分析 | `—` | `_region-pull` | `rules/packets/defect/analyze.md` |
| 5 | `decide` | 处置确认 | `—` | `_region-pull` | `rules/packets/defect/decide.md` |
| 6 | `apply` | 联动与评审 | `—` | `_region-act` | `rules/packets/defect/apply.md` |
| 7 | `review` | 重审（条件） | `substantive_change` | `_region-act` | `rules/packets/defect/review.md` |
| 8 | `writeback` | 平台回写 | `remark_writeback` | `_region-act` | `rules/packets/defect/writeback.md` |
| 9 | `verify` | 验证与关闭 | `needs_linked_update` | `_region-act` | `rules/packets/defect/verify.md` |
| 10 | `wrap` | 收尾 | `—` | `_region-close` | `rules/packets/defect/wrap.md` |
| 11 | `commit` | 拟提交 | `—` | `_region-close` | `rules/packets/defect/commit.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次；出区再进下一子机。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
