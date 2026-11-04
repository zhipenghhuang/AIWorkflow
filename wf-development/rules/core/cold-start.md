# 开局卡（开发轨）

> **读取级别：常驻**。新会话 / 切包 / 接管任务 **先读本文（≤60 行）**，再按需读 `AGENTS.md` 口令表与当前 step。  
> **中段**：心跳 `redline` 只从本文抽 ≤3 标签；禁止借心跳通读 `AGENTS`/`implementation-quality` 全文。  
> **冲突**：用户本轮明确指令 > 根 AGENTS > 开局卡/包规则；与门/红线冲突须先说明再等选择（不静默覆盖）。

## 1. 八条硬约束

1. **先意图、再动作**（门名 `confirm_task_intent`；档位只认 `execution-contract.md` §1.0，本卡不改门）：新开先输出【需求与意图理解】再等确认；续跑一行回执；只读一句话。未确认 → 禁改代码/外发/下完成结论。实质动作前【动作前分析】：**写/门/外发/提交** 六字段；只读免；计划内续跑/可逆小改可合并一行；**禁先做后补，禁无增量重复长文**。
2. **短读跟随 + 一手源**：开工读 `activeContext` 总览 + 本包进行中（含 `rule_card`）+ **偏好/洞见/坑 ≤3 行**（无则当无；写法只认 `context-memory.md`）。一手源：方案/PRD/原型（有 UI 须解码）> 热层/旧评审/旧截图；续跑先「继承基线核对」。
3. **当前步只读步骤包**：workflow **当前 step 块**（只取门/agent/`must_read`）+ `must_read[0]` = `rules/packets/<wf>/<step>.md`（本步唯一正文）+（若包内 §6 列出）**一个模板**。禁通读他 workflow / 全本 rules / read-index / playbook / 未嵌入的 skill。
4. **方法在包内**：步骤包已嵌入本步必做；回执 `skills=embedded`（或包内列出的名称）。有原型的 implement → 包内必含原型解码 + 前端实施条款。
5. **完成分层**：中途声称完成 → 只认 `Invoke-Gate.ps1 -Claim` → `CLAIM: ALLOWED`（原样粘贴）；`DENIED` 只能写未完成/阻塞。**wrap/收尾** 另写【遵守自检】一行（`triad`/`facade` 按契约：无计划=`triad=na`，未触门面=`facade=na`）+ 工作记忆五问（有记 1 行 / 无写无）。心跳 ≠ 遵守自检。无 ALLOWED **禁止**把热层/计划写成「已通过」。
6. **前端硬门**：有 UI 的 L1+ → 步骤包硬约束中的前端条（产物套装 + capture/`evidence.json`）；手写矩阵/骨架图/API 200 ≠ 页面完成。
7. **证据先于结论；禁刷绿**；密钥零入库；最小改动；失败同方案 2 次换路径；不适配先依据+主推（`deviation=` 仅用户二次坚持后）。
8. **切步/过门 →【规则心跳】一行**（`rule-anchor.md`）；同一步长会话不必每轮刷心跳。

## 2. 本步命令（按档选，最多 4 条）

| 场景 | RUN |
| --- | --- |
| 任何任务开工 | 短读记忆 →【需求与意图理解】（或续跑一行）→ 确认后再动手 |
| 有原型的分析/设计/计划 | 打开本步 packet → 按包内做法解码原型 → 覆盖/差异矩阵 |
| implement / solo.build（有行为） | 打开本步 packet →【实施预检】→ 按 SC 编码 → 自测指回 SC |
| implement（有 UI） | 按包内前端硬门：矩阵 → 实现 → `frontend.capture` → parity |
| verify / 声称完成前 | `verify/Invoke-Gate.ps1` → `-Claim`；前端另跑 `verify/tools/frontend_parity.py` |
| wrap / 收尾 | 打开 wrap packet + `closeout-skeleton` →【遵守自检】 |
| 用户报一个前端缺陷 | 先全量菜单/深链/路由审计（缺陷族），禁止只修单点 |

## 3. 禁做（短）

- 用「测试绿 / DOM 有字 / 旧截图」代替本轮浏览器证据；跳过短读却「按习惯做」。
- 自造一级导航/页面壳/详情布局（矩阵未写明则禁止）。
- 门禁 `BLOCKED`/`DENIED` 后仍写通过，或回执过期后不重跑门。
- 为省预算跳过门、证据、红线；把指针当已读；通读 `rules/` 或再去打开 skill/read-index。

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
| 门语义 | 步骤包 §4（已摘入）；维护写 YAML 时才读 `gates.md` |
| 怎么做 | 步骤包 §5（已嵌入技能必做） |
| 完成了没 | `verify` Claim / 包内 §7 |

禁止：通读 `rules/`、通读 `AGENTS` 过程百科、用 README/read-index/playbook 当运行时规则。

## 5. 回执最小字段

```text
route=… | step=… | intent=confirmed|pending|readonly | skills=embedded | reads=rules/packets/… | claim=ALLOWED|DENIED|na | memory=read|na | next=…
```

`reads=` 必须含本步 packet 路径（+ 若打开的模板）；对不上 = 未遵守读链。
