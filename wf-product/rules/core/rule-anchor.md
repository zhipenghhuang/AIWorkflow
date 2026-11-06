# 规则重锚（产品轨）

> **定位**：长会话防丢规则——只重锚**身份 + 当前步骤包**。  
> **硬约束**：`cold-start.md`；**本步规则**：`rules/packets/<wf>/<step>.md`。

## 1. 身份卡

| 项 | 值 |
| --- | --- |
| 包 | 产品规范 |
| 角色 | 当前 step 的 `agent`（见步骤包 §1「角色」；只做该角色职责） |
| 当前任务 | 取自 `activeContext` 进行中；一句话，不展开 |
| 开局卡 | `rules/core/cold-start.md` |
| 流程地图 | `rules/packets/<wf>/_chain.md`（进 wf 一次） |
| 本步规则 | `rules/packets/<wf>/<step>.md` |

## 2. 重锚必读

1. cold-start 扫读 + `activeContext` 进行中 `rule_card`（含 `packet=`）  
2. 当前步骤包（门、编排、推进、必开技能）。已指向且未改 step 时，核对路径后可不重读全文。  

**禁读**：YAML step 块（非规则正文）、多 packet、通读 skills、read-index/playbook（仅当前步骤包点名时按节读）。

## 3. 心跳

**触发**：每轮首答先判任务类型（新/续/只读）；切 step / 过 hitl·gate → **必做**；长会话每 3～5 轮补一行。

```text
【规则心跳】pkg=产品 | role=<agent> | task=<当前任务一句话> | route=workflow:step | region=<id>|na | packet=rules/packets/<wf>/<step>.md | next=<下一节点>|收尾 | must=开局卡+步骤包 | forbid=多packet/通读skills | redline=… | ext=ok|refresh | rule_card=ok|refresh
```

`packet=` 必填；`role=`/`task=` 缺一即视为身份漂移，先重锚再继续。
