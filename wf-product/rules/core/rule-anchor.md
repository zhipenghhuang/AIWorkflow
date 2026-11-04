# 规则重锚（产品轨）

> **定位**：只重锚身份 + **开局卡标签** + 当前步；禁止通读全书。  
> **硬约束正文**：`rules/core/cold-start.md`。心跳格式只认本文。

## 1. 身份卡

| 项 | 值 |
| --- | --- |
| 包 | 产品规范 |
| 开局卡 | `rules/core/cold-start.md` |
| 入口 | 本包 `AGENTS.md`（口令表）；一次会话一个包 workflow |
| 产物根 | `{workroot}/`；档案 `product-profile.md` |

## 2. 重锚必读（按序）

1. `cold-start.md` + `activeContext` 进行中 `rule_card` + **偏好/洞见/坑 ≤3 行**（无则跳过）  
2. workflow **当前 step 块**  
3. `read-index.md` **当前行**  
4. 当前 agent + 产物/证据  

**禁读**：他包；他 workflow 全文；整本 skills/模板；通读 `context-memory`（短读热层即可）。

## 3. 心跳

**触发**：切 step / 过 hitl·gate → 必做；同一步不必机械连刷。

```text
【规则心跳】pkg=产品 | route=workflow:step | role=… | must=开局卡+step块+索引行 | forbid=他包/他workflow全文 | redline=标签1·标签2·标签3 | rule_card=ok|refresh
```

- `redline` 只从 **cold-start** 抽 ≤3 标签（例：`Claim`·`短读记忆`·`双确认`·`原型矩阵`·`先意图后动作`）。  
- `intent=pending` 时禁实质动作。心跳 ≠ 遵守自检 / 收尾。

## 4. 与 AGENTS

| 时机 | 读什么 |
| --- | --- |
| 新会话 | **cold-start** → AGENTS §3 口令（未路由）→ 本文 |
| 已路由中段 | 心跳；不重读 AGENTS 全文 |
