# 读取索引（维护用 · 非运行时必读）

> **维护目录**：运行时读链只认 `cold-start` + `_chain`/`_region`（进 workflow/子区一次）+ 当前步骤包 + 命中 skill；read-index/playbook 仅当前步骤包点名时按节读。  
> 本文不再作为 AI 执行必读；改步骤规则以 packets 为准，可用 `rules/tools/build_step_packets.py` 重生。  
> 下列表格仅供维护者对照历史 MUST/RUN/REF 与口令定位。

## 默认（所有 step）

| MUST | RUN | REF |
| --- | --- | --- |
| cold-start（新会话/切步心跳时）· workflow 当前 step 块 · 当前产物/证据（`agents/<id>.yaml` 仅派工/改角色时） | 心跳（切步/过门） | 他包 AGENTS、他 workflow 全文、全本 skills/模板 |

定位（不计入 MUST）：`doc-governance.md` §2.4；`activeContext` 总览+进行中+**偏好/洞见/坑≤3**；`project-profile.md` §1+§2。

## 按 step

| step | MUST | RUN | REF |
| --- | --- | --- | --- |
| 工作总结口令 | `closeout-skeleton.md` §2 · activeContext 工作总结锚点 | 写锚点区间 | git 日志 |
| 无口令/意图不明 | `routing.md` §0～§6 · profile §1/§7/§8 | 首条 `reason=` | 附录 |
| control.init/run/sync/check/next | control 当前块 · `development-plan` 技能当前节 · 计划现状 | 同步计划状态 | 计划模板；有原型 +product-doc-analysis |
| change.clarify | change 当前块 · `clarification.md` 当前节 | 意图确认回执 | requirements 技能 |
| change.analyze_input | change 当前块 · `product-doc-analysis` · 理解包模板 §0 · 输入文档/原型 | 解码原型（如有）· 差量表 · 用户版说明 | 代码地图 |
| change.requirements | `requirements-and-spec` · 需求基线模板 · 理解包 | 写 AC；跨层命中则矩阵 | PRD 原文 |
| change.design | `solution-design` · 方案模板 | 出方案/ADR；跨层命中则矩阵 | api/db/frontend 子技能当前节 |
| change.plan / iterate.plan | `task-breakdown` · 任务清单模板 · **iq-checklist.md** · `versioning.md` §2.1 | 先确认/继承版本模式（A/B，已固定项目沿用并标注）；拆 SC；校验清单 | `implementation-quality.md` 词典；subagents |
| change.implement / iterate.implement / solo.build | `implementation-and-selftest` §0.5 · 任务卡 SC · **iq-checklist.md**；（有 UI）**frontend-gate.md** | 【实施预检】→ 编码 → 自测指回 SC；（有 UI）矩阵+capture+parity；（有原型）skills=product-doc-analysis+frontend-implementation | IQ 全文、engineering-quality 全文、子技能 |
| change.review-docs | `design-doc-review` · doc-reviewer · 被审文档 | 文档评审结论 | solution-design 节 |
| change.review / iterate.review | `code-review` §4.0 · reviewer · diff；（有 UI）evidence.json / parity | 核对 AC+SC+前端产物；不得只看测试绿 | security-scan |
| change.verify / iterate.gates / solo.test | `verify/README.md` · `checks.yaml` · 验收清单 | `Invoke-Gate` → `-Claim`；（有 UI）`frontend_parity` | verification 长附录、旧截图 |
| change.deliver / iterate.deliver | `qa-handoff-and-release` · 提测模板 · `verification.md` §2.2 | 提测单与债项/DEV-QA-PRODUCT 分流对齐；过 `s6-admission`；有代码则核 completion.json | versioning §3～§7 |
| change.release_handoff / iterate.release_handoff / release.* | 对应 workflow 块 · `qa-handoff`/`acceptance` 当前节 | 按门 HITL | 上线检查单 |
| */wrap · */commit | `closeout-skeleton.md` §0～§1 · `workflow.md` §2（commit 时） | 完整收尾；commit 出示拟提交 | context-memory §4 |
| solo.frame / solo.plan | solo 当前块 · `lightweight.md` 当前节 · 对应技能 | 轻量卡/方案卡 | 全量 PRD |
| iterate.precheck | iterate 当前块 · `iteration-delivery.md` 当前节 | 缺口说明/回 change | playbooks/iterate REF |
| iterate.confirm | iterate 当前块 | confirm_backlog（when） | — |
| iterate.retro | `retrospective-and-improvement` · 复盘模板 | 行动项 | playbooks/iterate REF |
| defect-fix.preflight/pull/triage/gates/menu | defect-fix 当前块 · `fix-collaboration` 节 | 平台/分流动作 | playbooks/defect REF；platform-adapter |
| defect-fix.fix | defect-fix fix 块 · iq-checklist · implementation-and-selftest §0.5 | 红证→根因→修→验；（前端）缺陷族审计 | IQ 词典 |
| defect-fix.close | close 块 · 缺陷文案模板 §6 · verification | 回写全文+证据 | — |
| defect-fix.await_product/assess_*/handoff_product/product_decision/align/clarify | defect playbook 对应节 · fix-collaboration §5 | 产品确认链 | 文案模板 |
| intake.* | intake 块 · `change-intake` ·（有文档）product-doc-analysis | 分流/吸收报告 | doc-governance §3 |
| materials.* | materials 块 · doc-governance §5.2 · materials INDEX | 同步资料库 | — |
| onboard.* | onboard 块 · onboard-agent · doc-governance §2.4+ | 打标/建树 | capabilities |
| skill-audit.* | skill-audit 块 · skill-audit playbook | discover/fit | skills README |
| retro.* | retrospective 技能 · 复盘模板 | 行动项 | — |
| handoff.* | handoff 块 · handoff.md 当前节 · 模板 | 台账/回执 | 升包说明 |

## 读取纪律

- 先读标题/当前节；同一文件只读一次，后续 delta-only。  
- 子代理只读派发路径，不通读全书。  
- 澄清 → `clarification.md`；产品文档/原型 → `product-doc-analysis`（先读「必做」）。  
- 模板短名先查 `rules/templates/index.md`。
