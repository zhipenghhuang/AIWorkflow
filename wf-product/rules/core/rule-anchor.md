# 规则重锚（产品轨）

> **定位**：长会话防丢规则——只重锚**身份 + 当前步骤包**。  
> **硬约束**：`cold-start.md`；**本步规则**：`rules/packets/<wf>/<step>.md`。

## 1. 身份卡

| 项 | 值 |
| --- | --- |
| 包 | 产品规范 |
| 开局卡 | `rules/core/cold-start.md` |
| 流程地图 | `rules/packets/<wf>/_chain.md`（进 wf 一次） |
| 本步规则 | `rules/packets/<wf>/<step>.md` |

## 2. 重锚必读

1. cold-start 扫读 + `activeContext` 进行中 `rule_card`（含 `packet=`）  
2. 当前 YAML step 块  
3. 当前步骤包  

**禁读**：多 packet、通读 skills、read-index 当运行时。

## 3. 心跳

```text
【规则心跳】pkg=产品 | route=workflow:step | packet=rules/packets/<wf>/<step>.md | must=开局卡+步骤包 | forbid=多packet/通读skills | redline=… | rule_card=ok|refresh
```

`packet=` 必填；对不上先 refresh。
