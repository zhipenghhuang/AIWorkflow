# 规则重锚（开发轨）

> **定位**：长会话防丢规则——只重锚**身份 + 当前步骤包**，禁止通读全书。  
> **硬约束正文**：`cold-start.md`；**本步规则正文**：当前 `rules/packets/<wf>/<step>.md`。

## 1. 身份卡

| 项 | 值 |
| --- | --- |
| 包 | 开发规范 |
| 角色 | 当前 step 的 `agent`（见步骤包 §1「角色」；只做该角色职责） |
| 当前任务 | 取自 `activeContext` 进行中；一句话，不展开 |
| 开局卡 | `rules/core/cold-start.md` |
| 入口 | 本包 `AGENTS.md`（口令表） |
| 流程地图 | `rules/packets/<wf>/_chain.md`（进 wf 一次） |
| 本步规则 | `rules/packets/<wf>/<step>.md` |

## 2. 重锚必读（按序，够用即停）

1. cold-start 标题扫读 + `activeContext` 进行中 `rule_card`（必须含 `packet=`）  
2. **当前步骤包**（门、编排、推进、必开技能）。`rule_card` 已指向且未改 step 时，核对路径后可不重读全文。  

**禁读**：他包；他 workflow；YAML step 块（非规则正文）；一次多个 skill；read-index/playbook（仅当前步骤包点名时按节读）。

## 3. 心跳

**触发**：每轮首答先判任务类型（新/续/只读）；切 step / 过 hitl·gate → **必做**；长会话每 3～5 轮或上下文变长时补一行。**单回合长任务**（同一回复内连续执行、无中间轮次）在进入新子机、或连续 >20 分钟无用户可见输出时，先发一行可见进展再继续。

```text
【规则心跳】pkg=开发 | role=<agent> | task=<当前任务一句话> | route=workflow:step | region=<id>|na | packet=rules/packets/<wf>/<step>.md | next=<下一节点>|收尾 | must=步骤包+必开skill闭环 | forbid=多packet/跳技能 | redline=… | ext=ok|refresh | rule_card=ok|refresh
```

- `packet=` **必填**；`role=`/`task=` 缺一即视为身份漂移，先重锚再继续。  
- 有子机时写 `region=`。  
- 必开 skill 未闭环不得标完成。  
- 意图未确认 → `intent=pending`。

## 4. 与 AGENTS

| 时机 | 读什么 |
| --- | --- |
| 新会话 | cold-start → 口令表（未路由）→ 本文格式 |
| 已路由中段 | 心跳 + 当前步骤包；不重读 AGENTS 全文 |
