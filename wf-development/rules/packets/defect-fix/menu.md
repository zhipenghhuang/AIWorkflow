# 步骤包 · defect-fix/menu

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`defect-fix`
- **step**：`menu`（总结菜单）
- **packet**：`rules/packets/defect-fix/menu.md`
- **条件步** `when=implementation_required`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：总结菜单
- **产出**：【缺陷修复处理总结】+【用户选择菜单】

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 预授权（一次性/直接跑完）：声明默认界并直接执行（见 AGENTS ）；默认只到本步输出 （修复＋门禁＋总结菜单）待选择，仅含后续且范围不明时一问， 禁静默连跑提交/推送/部署/回写；含后续由范围确认覆盖。总结与菜单必须同轮输出。 产品缺陷项须列评估单/产品结论/对齐状态。

## 4. 本步门

- **HITL `select_menu`**：输出总结+【用户选择菜单】，精确执行选项

## 5. 做法

### 本步动作清单

- 预授权（一次性/直接跑完）：声明默认界并直接执行（见 AGENTS ）。
- 默认只到本步输出 （修复＋门禁＋总结菜单）待选择，仅含后续且范围不明时一问， 禁静默连跑提交/推送/部署/回写。
- 含后续由范围确认覆盖。总结与菜单必须同轮输出。 产品缺陷项须列评估单/产品结论/对齐状态。

## 6. 打开/填写

- 运行时正文：仅本文件（开局卡已在会话开头读过）。
- 无强制模板：直接写 §2 产出路径产物。

## 7. 完成信号

- §2 产出已落盘。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 8. 回执字段

```text
route=workflow:defect-fix | step=menu | reads=rules/packets/defect-fix/menu.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/defect-fix/menu.md`；对不上 = 未遵守读链。
