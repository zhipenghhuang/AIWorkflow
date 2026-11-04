# 规则重锚（开发轨）

> **定位**：长会话防丢规则——只重锚**身份 + 开局卡标签 + 当前步**，**禁止**通读全书 / 全本 `AGENTS.md` / IQ 全文。  
> **单一出处**：心跳格式只认本文；硬约束正文只认 `cold-start.md`。

## 1. 身份卡

| 项 | 值 |
| --- | --- |
| 包 | 开发规范 |
| 开局卡 | `rules/core/cold-start.md` |
| 入口 | 本包 `AGENTS.md`（口令表）；一次会话一个包 workflow |
| 产物根 | `{workroot}/`；档案 `project-profile.md` |

## 2. 重锚必读（按序，够用即停）

1. `cold-start.md`（可扫标题+本步命令表；不必逐字）+ `activeContext` 进行中 `rule_card` + **偏好/洞见/坑 ≤3 行**（无则跳过）  
2. workflow **当前 step 块**  
3. `read-index.md` **当前行**（MUST/RUN/REF）  
4. 当前 agent + 当前产物/证据  

**禁读**：他包；他 workflow 全文；REF 列默认项；整本 skills/模板；通读 `context-memory`（短读热层即可，写法命中再打开）。

## 3. 心跳

**触发**：切 step / 过 hitl·gate 前后 → **必做**；同一步长会话仅在将丢约束时补一行（不必每 5～8 轮机械刷）。

```text
【规则心跳】pkg=开发 | route=workflow:step | level=L0-L3 | role=… | must=开局卡+step块+索引行 | forbid=他包/他workflow全文 | redline=标签1·标签2·标签3 | rule_card=ok|refresh
```

- `redline`：只从 **cold-start** 抽 ≤3 标签（例：`Claim`·`短读记忆`·`frontend-gate`·`先意图后动作`·`skills=`）。  
- 意图未确认 → `intent=pending`，禁实质动作。  
- `rule_card=refresh` → 同轮写回进行中。心跳 ≠ 遵守自检 / 收尾。

## 4. 与 AGENTS 的关系

| 时机 | 读什么 |
| --- | --- |
| 新会话 | **cold-start** → AGENTS §3 口令（若未路由）→ 本文 |
| 已路由中段 | 心跳；不重读 AGENTS 全文 |
| 细则冲突 | frontend-gate / Claim / clarification / 执行契约为 SSOT |
