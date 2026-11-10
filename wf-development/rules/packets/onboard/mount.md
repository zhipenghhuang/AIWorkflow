# 步骤卡 · onboard/mount

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`onboard` / `mount`（复制与挂载确认）
- **packet**：`rules/packets/onboard/mount.md`
- **角色**：`onboard-agent`（开发包接入）。挂载验收 → 生成档案/规范/activeContext → 文档树/索引/归档 → 确认入库 → 环境与工具检查（默认静默） → 按接入清单核验；本步只做该角色职责；越界交回或升级。
- **上游**：无（链首）
- **后续**：`profile`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。
- **轻量路径**：纯文档/无行为/无 UI/未命中时，可将预检、前端硬门标 `na`（一句理由）；**必开技能与 Claim/HITL 不降**。

## 2. 本步目标

- **目标**：复制与挂载确认
- **产出**：项目根 AGENTS.md 包挂载段（已存在则追加，不覆盖）

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

### 本步动作清单

- 验收：项目根 AGENTS.md 已补入指向本包 AGENTS.md 的引导语句 （样例见 rules/templates/00-onboarding/root-agents-pointer.md；已有则追加、没有则新建）。
- 未补入则按样例写入后再继续。
- 单包只写薄指针。
- 多包只写指向 `wf/AGENTS.md` 的薄指针。
- 多包模式（项目根自动探测到两个及以上包目录）：根 `AGENTS.md` 只写薄指针（先读 `wf/AGENTS.md`）。
- 按 `rules/templates/00-onboarding/wf-agents-routing-template.md` 生成/补齐 `wf/AGENTS.md`，只列已装包。
- 已有则只补行，不覆盖。
- 三包自动探测共享 inbound/上下文。
- **分层**：母版只写入挂载段。
- 不对根写入偏好/喜好正文（落地项目自写）。
- 档案 为项目技术事实摘要，不是偏好容器。

本步无前端硬门。不改界面、不做界面验收 → 不跑 capture / parity。

## 6. 技能指向（打开 → 执行 → 回包）

- 本步无技能指向；按 §5 编排执行。
- 禁止无指向却通读 skills/「找感觉」。

## 7. 模板与证据

- **填写模板（仅此一份）**：`rules/templates/00-onboarding/root-agents-pointer.md`；只读本步用到的节，禁止整文件通读。
- **参考模板（命中再开，不默认读）**：`rules/templates/00-onboarding/wf-agents-routing-template.md`。

## 8. 完成与退出

- §2 产出已落盘；本步无 §6 技能指向。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:onboard | step=mount | agent=onboard-agent | packet=rules/packets/onboard/mount.md | global=ok | skills=na|done|na | claim=ALLOWED|DENIED|na | next=…
```
