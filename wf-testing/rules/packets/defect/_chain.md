# 流程链 · defect

> **父状态机地图（进本 workflow 读一次）**。之后进入当前**子机**（若有）→ **当前步骤包**；禁止通读全链步骤包。

## 定位

- **包轨**：wf-testing
- **workflow**：`defect`（测试缺陷协作）
- **用途**：入口 / 顺序 / 子机划分；**规则正文在 step packet**；**方法质量在 skill（由步骤包 §6 指向）**。

## 入口

- `缺陷协作` → step `classify`
- `查重` → step `classify`
- `提交到平台` → step `classify`
- `回归` → step `classify`
- `指派给我` → step `classify`
- `已解决` → step `classify`
- `复测` → step `classify`
- `缺陷变化巡检` → step `classify`
- `补充澄清` → step `classify`
- `产品判定回流` → step `classify`

## 状态机

本 workflow 步骤较少，无额外子机；按阶段表逐步打开步骤包即可。


## 阶段表（全量索引 · 勿一次读完各包）

| # | step | 名称 | when | 子机 | 步骤包 |
| --- | --- | --- | --- | --- | --- |
| 1 | `classify` | 识别子类 | `—` | — | `rules/packets/defect/classify.md` |
| 2 | `search` | 查重或拉取 | `—` | — | `rules/packets/defect/search.md` |
| 3 | `submit` | 提交或回写 | `defect_submit_required` | — | `rules/packets/defect/submit.md` |
| 4 | `wrap` | 收尾 | `—` | — | `rules/packets/defect/wrap.md` |

## 执行纪律（防丢失 · 不降质）

1. 同时只激活 **一个** step packet；`packet=`/`reads=` 必须指向它。
2. 有子机：进区读 `_region-*` 一次；出区再进下一子机。
3. 步骤包 §6 **必开技能**：打开→执行必做→**回步骤包**；跳过 = 未遵守（质量不降）。
4. `when` 不满足 → 跳过该步（不打开其 packet）。
5. YAML 只编排；不要通读本 YAML 其他 step。
