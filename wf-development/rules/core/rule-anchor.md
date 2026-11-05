# 规则重锚（开发轨）

> **定位**：长会话防丢规则——只重锚**身份 + 当前步骤包**，禁止通读全书。  
> **硬约束正文**：`cold-start.md`；**本步规则正文**：当前 `rules/packets/<wf>/<step>.md`。

## 1. 身份卡

| 项 | 值 |
| --- | --- |
| 包 | 开发规范 |
| 开局卡 | `rules/core/cold-start.md` |
| 入口 | 本包 `AGENTS.md`（口令表） |
| 流程地图 | `rules/packets/<wf>/_chain.md`（进 wf 一次） |
| 本步规则 | `rules/packets/<wf>/<step>.md` |

## 2. 重锚必读（按序，够用即停）

1. cold-start 标题扫读 + `activeContext` 进行中 `rule_card`（必须含 `packet=`）  
2. workflow **当前 step 块**（门/must_read）  
3. **当前步骤包**（若 `rule_card` 已指向且未改 step，可确认路径后不重读全文）  

**禁读**：他包；他 workflow 全文；一次多个 skill；read-index/playbook 当运行时。

## 3. 心跳

**触发**：切 step / 过 hitl·gate → **必做**；将丢约束时补一行。

```text
【规则心跳】pkg=开发 | route=workflow:step | region=<id>|na | packet=rules/packets/<wf>/<step>.md | must=步骤包+必开skill闭环 | forbid=跳过必开skill/多packet | redline=… | rule_card=ok|refresh
```

- `packet=` **必填**；有子机时写 `region=`。  
- 必开 skill 未闭环不得标完成。  
- 意图未确认 → `intent=pending`。

## 4. 与 AGENTS

| 时机 | 读什么 |
| --- | --- |
| 新会话 | cold-start → 口令表（未路由）→ 本文格式 |
| 已路由中段 | 心跳 + 当前步骤包；不重读 AGENTS 全文 |
