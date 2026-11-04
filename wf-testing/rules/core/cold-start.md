# 开局卡（测试轨）

> **读取级别：常驻**。新会话 / 切包 / 接管 **先读本文**，再按需读 `AGENTS.md` 口令表与当前 step。  
> 中段心跳 `redline` 只从本文抽 ≤3 标签。  
> **冲突**：用户本轮明确指令 > 根 AGENTS > 开局卡/包规则；与门/红线冲突先说明再等选择。

## 1. 八条硬约束

1. **先意图、再动作**（门名 `confirm_task_intent`；档位只认 `execution-contract.md` §1.0，本卡不改门）：新开先输出【需求与意图理解】再等确认；续跑/脚本回归一行；只读一句话。未确认 → 禁生成正式用例/交平台。实质动作前【动作前分析】：写/门/外发/提交六字段；只读免；续跑可合并一行；**禁先做后补，禁无增量重复长文**。
2. **短读跟随 + 一手源**：开工读 `activeContext` 总览 + 测试进行中 + **偏好/洞见/坑 ≤3**（无则当无；`context-memory.md`）。一手源：PRD/方案/原型/接口 > 旧报告/热层；覆盖矩阵缺行不得生成或评审通过。
3. **依据先建模**：分析表 §0 Brief+差量；无 §0 禁正式生成与功能准出。
4. **当前步只读步骤包**：workflow **当前 step 块**（门/agent/`must_read`）+ `must_read[0]` = `rules/packets/<wf>/<step>.md`（本步唯一正文）+（若包内 §6 列出）**一个模板**。禁通读 rules / read-index / playbook / 未嵌入的 skill。
5. **完成分层**：中途通过/准出 → `Invoke-Gate.ps1 -Claim -Mode report`（已回写 → `-Mode writeback`）→ 只认 `CLAIM: ALLOWED`。**wrap/收尾** 另写【遵守自检】一行（无计划 `triad=na`；未触门面 `facade=na`）+ 工作记忆五问（有/无）。心跳 ≠ 遵守自检。
6. **UI 证据 E1**：点名页面须浏览器 MCP 或 Playwright 实点 + 桌面/移动截图 + Network；E0 不得单独判 pass。有开发包 `evidence.json` 时优先核对其哈希，不另造截图标准。
7. **能脚本不 AI**（决策表见 `AGENTS` §0.3）；禁刷绿；P0 未过不得整体通过；密钥/PII 不进证据；不适配先依据+主推。
8. **切步/过门 → 规则心跳一行**（`rule-anchor.md`）；同一步不必每轮刷心跳。

## 2. 本步命令

| 场景 | RUN |
| --- | --- |
| 任何任务开工 | 短读记忆 →【需求与意图理解】（或续跑一行）→ 确认后再动手 |
| 分析/计划 | 打开本步 packet → 填 PRD/方案/原型/接口 → 验证点覆盖表 |
| 生成 | 打开本步 packet → 命中域增量（保 caseId）；冷启动无域才首生 |
| 执行（UI） | 打开本步 packet → E1 实点 + 截图/Network；引用本轮证据 |
| 报告/准出 | `Invoke-Gate -Mode report` → `-Claim -Mode report` |
| wrap / 收尾 | 打开 wrap packet + `closeout-skeleton` →【遵守自检】 |
| 回写 | `-Claim -Mode writeback` |

## 3. 禁做

- 用用例数/通过率代替覆盖矩阵与本轮证据；跳过短读却按习惯改准出口径。
- 浏览器不可用仍对 UI 点名项标 pass。
- Claim DENIED 仍写准出；未装填当本轮已跑。
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
