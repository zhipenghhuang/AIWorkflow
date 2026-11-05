# packets/（状态机式运行时表面）

## 结构

```text
<workflow>/
  _chain.md           # 父状态机（进 wf 读一次）
  _region-<id>.md     # 子状态机（长链分区；进区读一次）
  <step>.md           # 步骤状态（当前唯一激活）
```

## 技能

- **不**把 skill 正文写入步骤包。
- 步骤包 §6 **指向** skill：`打开 → 执行必做 → 回到步骤包`。
- 标**必开**的必须执行（质量不降）；条件开未命中则 `na`。

## 维护

改分区/技能映射后跑：`rules/tools/build_step_packets.py <包根>`。
