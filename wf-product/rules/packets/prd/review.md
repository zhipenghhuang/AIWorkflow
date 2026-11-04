# 步骤包 · prd/review

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`prd`
- **step**：`review`（PRD 评审与定稿）
- **packet**：`rules/packets/prd/review.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：PRD 评审与定稿
- **产出**：评审记录或 HUMAN_APPROVED 声明

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 入口=「PRD评审」→ `finalize_requested=false`（只评审）；入口=「定稿」或用户明确要进入排期 → true。 **先选评审方式**（`skills/artifact-review`）：STOP 出示【评审方式】A 自行评审通过｜B AI 独立评审；未选不得宣称通过/定稿。P0/P1 light 可提示默认 A；P2+ 必问。 **选 A**：出示【完稿自检摘要】+ 四硬门要点 → 用户确认 → `HUMAN_APPROVED`；**跳过**独立 reviewer 与 `-Mode review`；**仍必须** `-Mode prd` 非 BLOCKED（P2+/P1↑/拟定稿）；用户对放行负责。 **选 B**：技能 `skills/review-and-finalize/SKILL.md` + `skills/artifact-review`；独立复核（完整/可测/无歧义/范围/依赖/风险/验收/埋点/追溯/无臆造）；对照客户需求理解防偷换问题/扩大范围/假设当事实。 **B 路径门禁**：先写评审记录再跑 `-Mode review`（`gate_when: ai_review_chosen`）；READY 后回填 `gate_id`、`review_status=AI_REVIEWED`/`APPROVED`；再复跑 `-Mode prd`。未 READY 不得写“评审通过/定稿”。 **定稿前结构门（A/B 均适用）**：`confirm_prd` 前 `-Mode prd` 不得为 BLOCKED；无【完稿自检摘要】不得定稿。 **评审分片**（子代理编排 ）：大 PRD → 维度扇出；评分卡只算一次。 产出：`评审-{主题}-{yyyyMMdd}.md`（B）或 HUMAN_APPROVED 声明（A）+【评审结论】+【完稿自检摘要】。 结论=需修 → 回 prd 修订（同回合≤1），不弹定稿门；通过且要定稿/排期 → `confirm_prd`；仅评审 → 收尾不弹定稿门。 批准后回写 PRD 头部 `status: APP

## 4. 本步门

- **HITL `select_review_mode`**：**STOP 二选一**：A 自行评审通过（HUMAN_APPROVED）｜B AI 独立评审（异人量规+评审记录）。适用 PRD/产品计划/设计交接等（`skills/artifact-review`）；同产物只问一次；点名「AI 评审」=B、「我审/自行通过」=A；未选不得宣称通过/定稿/交开发
- **HITL `confirm_prd`**：评审结论为「通过（可定稿）」且用户点名定稿/进入排期时出示；**出示前**须有【完稿自检摘要】且 `-Mode prd` 非 BLOCKED；定稿前不排期；仅评审不弹门
- **GATE `product-review` when=ai_review_chosen**：仅选 B（AI）时运行 `-Mode review`；评审人≠作者；READY 后取 `gate_id`；选 A 不跑本门，须 HUMAN_APPROVED + `approved_by` + 自检摘要 + 复跑 `-Mode prd` 至 READY

## 5. 做法

### 技能 `artifact-review`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「内容看起来完整，可自行通过」 | 完整≠可判定；缺 AC/证据/范围边界仍须选 A/B 并留痕。 |
| 「作者刚写完，自己审更快」 | 写手自审易盲区；选 B 须异上下文量规，选 A 须 HUMAN_APPROVED。 |
| 「小改不用评审」 | 改基线/AC/范围即实质变更；P0 文案除外仍要声明。 |
| 「先定稿再补问题」 | 定稿门前未 READY 不得恢复；问题清单先于定稿。 |
### 技能 `review-and-finalize`

## 常见合理化与反驳

| 合理化 | 现实 |
| --- | --- |
| 「量规太严，先放行」 | READY 条件未齐不得定稿；有条件通过须列遗留。 |
| 「小问题口头说说就行」 | 评审记录先于改稿；未写记录不得称已审。 |
| 「用户说好看就过」 | 可测 AC/范围/风险仍要过量规，不替代体验偏好。 |
### 编排备忘

入口=「PRD评审」→ `finalize_requested=false`（只评审）；入口=「定稿」或用户明确要进入排期 → true。 **先选评审方式**（`skills/artifact-review`）：STOP 出示【评审方式】A 自行评审通过｜B AI 独立评审；未选不得宣称通过/定稿。P0/P1 light 可提示默认 A；P2+ 必问。 **选 A**：出示【完稿自检摘要】+ 四硬门要点 → 用户确认 → `HUMAN_APPROVED`；**跳过**独立 reviewer 与 `-Mode review`；**仍必须** `-Mode prd` 非 BLOCKED（P2+/P1↑/拟定稿）；用户对放行负责。 **选 B**：技能 `skills/review-and-finalize/SKILL.md` + `skills/artifact-review`；独立复核（完整/可测/无歧义/范围/依赖/风险/验收/埋点/追溯/无臆造）；对照客户需求理解防偷换问题/扩大范围/假设当事实。 **B 路径门禁**：先写评审记录再跑 `-Mode review`（`gate_when: ai_review_chosen`）；READY 后回填 `gate_id`、`review_status=AI_REVIEWED`/`APPROVED`；再复跑 `-Mode prd`。未 READY 不得写“评审通过/定稿”。 **定稿前结构门（A/B 均适用）**：`confirm_prd` 前 `-Mode prd` 不得为 BLOCKED；无【完稿自检摘要】不得定稿。 **评审分片**（子代理编排 ）：大 PRD → 维度扇出；评分卡只算一次。 产出：`评审-{主题}-{yyyyMMdd}.md`（B）或 HUMAN_APPROVED 声明（A）+【评审结论】+【完稿自检摘要】。 结论=需修 → 回 prd 修订（同回合≤1），不弹定稿门；通过且要定稿/排期 → `confirm_prd`；仅评审 → 收尾不弹定稿门。 批准后回写 PRD 头部 `status: APPROVED`、`source_of_truth: true`、`updated`；更新产品计划 。**未定稿不排期**。

## 6. 打开/填写

- 运行时正文：仅本文件（开局卡已在会话开头读过）。
- 验证：`verify/Invoke-Gate.ps1`（完成声称加 `-Claim`）；有 UI 另按包内前端条。

## 7. 完成信号

- §2 产出已落盘。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 8. 回执字段

```text
route=workflow:prd | step=review | reads=rules/packets/prd/review.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/prd/review.md`；对不上 = 未遵守读链。
