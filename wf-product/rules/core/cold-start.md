# 开局卡（产品轨）

> **读取级别：常驻**。新会话 / 切包 / 接管 **先读本文**，再按需读 `AGENTS.md` 口令表与当前 step。  
> 中段心跳 `redline` 只从本文抽 ≤3 标签。  
> **冲突**：用户本轮明确指令 > 根 AGENTS > 开局卡/包规则；与门/红线冲突先说明再等选择。

## 1. 八条硬约束

1. **先意图、再动作**（门名 `confirm_task_intent`；档位只认 `execution-contract.md` §1.0，本卡不改门）：新开先输出【需求与意图理解】再等确认；续跑一行；只读一句话。未确认 → 禁写正式 PRD/外发/定范围。实质动作前【动作前分析】：写/门/外发/提交六字段；只读免；续跑/可逆小改可合并一行；**禁先做后补，禁无增量重复长文**。
2. **短读跟随 + 一手源**：开工读 `activeContext` 总览 + 产品进行中 + **偏好/洞见/坑 ≤3**（无则当无；`context-memory.md`）。一手源：客户材料/访谈/现行 PRD/原型 > 热层二手结论。
3. **理解→方案双确认未完成 → 不得入池/写正式 PRD/定版本范围**（门禁档位不变）。
4. **当前步只读步骤包**：workflow **当前 step 块**（门/agent/`must_read`）+ `must_read[0]` = `rules/packets/<wf>/<step>.md`（本步唯一正文）+（若包内 §6 列出）**一个模板**。禁通读 rules / read-index / playbook / 未嵌入的 skill。
5. **完成分层**：中途完成/准出 → `Invoke-Gate.ps1 -Claim -Mode <prd|review|design-review|uat|change|writeback>` → 只认 `CLAIM: ALLOWED`。**wrap/收尾** 另写【遵守自检】一行（无计划 `triad=na`；未触门面 `facade=na`）+ 工作记忆五问（有/无）。心跳 ≠ 遵守自检。
6. **原型硬门**：评审须真实打开原型逐页点 + 覆盖矩阵 `{workroot}/{ver}/20-design/prototype-coverage.md`；缺行不得过。浏览器不可用 → `browser=unavailable`，矩阵仍硬。
7. **禁臆造**；AC 须条件+动作+观测；变更无单不实施；UAT 未过不发布；不适配先依据+主推。
8. **切步/过门 → 规则心跳一行**（`rule-anchor.md`）；同一步不必每轮刷心跳。

## 2. 本步命令

| 场景 | RUN |
| --- | --- |
| 任何任务开工 | 短读记忆 →【需求与意图理解】（或续跑一行）→ 确认后再动手 |
| 原型评审 | 打开本步 packet → 浏览器实走 + 截图 + 填 coverage 矩阵 |
| design-review 交开发前 | `Invoke-Gate.ps1 -Mode design-review` → `-Claim -Mode design-review` |
| PRD/UAT/变更闭合 | 对应 `-Mode` 门禁 → `-Claim` |
| wrap / 收尾 | 打开 wrap packet + `closeout-skeleton` →【遵守自检】 |
| 回写 | `-Claim -Mode writeback` + `confirm_remark` |

## 3. 禁做

- 未确认项当已确认进 PRD/计划；跳过短读却按习惯定范围。
- 只读 HTML/文档代替原型实走（除非用户走查证据且已标降级）。
- Claim DENIED 仍写准出；回执后改产物不重跑门。
- 把指针当已读；通读 `rules/` 或再去打开 skill/read-index。

## 4. 读链（唯一路径 · 禁通读）

```text
① cold-start（本文）
② AGENTS 口令表（仅未路由时）
③ YAML 当前 step 块（门 / agent / must_read）
④ must_read[0] = rules/packets/<wf>/<step>.md（本步正文唯一）
⑤ 若本步要填模板：再开包内写明的那一个模板路径
⑥ Claim / closeout 按包内「完成/收尾」节
```

| 要找 | 打开 |
| --- | --- |
| 硬约束 | 本文 + **当前步骤包 §3** |
| 本步做什么 | **当前步骤包**（唯一正文） |
| 门语义 | 步骤包 §4；维护写 YAML 时才读 `gates.md` |
| 怎么做 | 步骤包 §5（已嵌入技能必做） |
| 完成了没 | `verify` Claim / 包内 §7 |

禁止：通读 `rules/`、通读 `AGENTS` 过程百科、用 README/read-index/playbook 当运行时规则。

## 5. 回执最小字段

```text
route=… | step=… | intent=confirmed|pending|readonly | skills=embedded | reads=rules/packets/… | claim=ALLOWED|DENIED|na | memory=read|na | next=…
```

`reads=` 必须含本步 packet 路径（+ 若打开的模板）；对不上 = 未遵守读链。
