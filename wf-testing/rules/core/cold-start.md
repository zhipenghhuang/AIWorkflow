# 开局卡（测试轨）

> **读取级别：常驻**。新会话先读本文，再按需读口令表。中段心跳带 `packet=`（有子机带 `region=`）。

## 1. 八条硬约束

1. **先意图、再动作**（`confirm_task_intent`）：未确认禁生成正式用例/交平台。
2. **短读跟随 + 一手源**：`activeContext` + 进行中（`packet=`/`region=`）+ 偏好/洞见/坑 ≤3。
3. **依据先建模**：分析表 §0；无 §0 禁正式生成与功能准出。
4. **状态机读链 + 技能闭环**：见 §4。必开 skill 须打开→执行→回步骤包（质量不降）。
5. **完成分层**：`-Claim -Mode report|writeback` → 只认 `CLAIM: ALLOWED`。
6. **UI 证据 E1**：实点 + 截图/Network；E0 不得单独 pass。
7. **能脚本不 AI**；禁刷绿；P0 未过不得整体通过。
8. **切步/出子机 → 心跳**，必带 `packet=`。

## 2. 本步命令

| 场景 | RUN |
| --- | --- |
| 进 wf | `_chain.md` 一次 → 子机（若有）→ 步骤包 |
| 执行 step | 步骤包 → §6 技能闭环 → 回包 |
| 准出 | `-Claim -Mode report` |

## 3. 禁做

- 跳过必开 skill；把 skill 嵌进步骤包；通读全链步骤包。

## 4. 状态机读链

```text
_chain →（_region-*）→ 步骤包 → skill 闭环（必开/条件开）→ 可选 1 模板
```

## 5. 回执

`route=… | step=… | region=…|na | packet=… | skills=…|done|na | claim=… | next=…`
