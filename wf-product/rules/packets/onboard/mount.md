# 步骤包 · onboard/mount

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`onboard`
- **step**：`mount`（复制与挂载确认）
- **packet**：`rules/packets/onboard/mount.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：复制与挂载确认
- **产出**：项目根 AGENTS.md 包挂载段（已存在则追加，不覆盖）

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 验收：项目根 AGENTS.md 已补入指向本包 AGENTS.md 的引导语句 （样例见 `rules/templates/00-onboarding/root-agents-pointer.md`；已有则追加、没有则新建）； 未补入则按样例写入后再继续。单包只写薄指针；多包只写指向 `wf/AGENTS.md` 的薄指针。 多包模式（项目根自动探测到两个及以上包目录）：根 `AGENTS.md` 只写薄指针（先读 `wf/AGENTS.md`）；按 `rules/templates/00-onboarding/wf-agents-routing-template.md` 生成/补齐 `wf/AGENTS.md`，只列已装包；已有则只补行，不覆盖；三包自动探测共享 inbound/上下文。 **分层**：母版只写入挂载段；不对根写入偏好/喜好正文（落地项目自写）。档案 为产品事实摘要，不是偏好容器。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。

## 5. 做法

### 本步动作清单

- 验收：项目根 AGENTS.md 已补入指向本包 AGENTS.md 的引导语句 （样例见 `rules/templates/00-onboarding/root-agents-pointer.md`。
- 已有则追加、没有则新建）。
- 未补入则按样例写入后再继续。单包只写薄指针。
- 多包只写指向 `wf/AGENTS.md` 的薄指针。 多包模式（项目根自动探测到两个及以上包目录）：根 `AGENTS.md` 只写薄指针（先读 `wf/AGENTS.md`）。
- 按 `rules/templates/00-onboarding/wf-agents-routing-template.md` 生成/补齐 `wf/AGENTS.md`，只列已装包。
- 已有则只补行，不覆盖。
- 三包自动探测共享 inbound/上下文。 **分层**：母版只写入挂载段。
- 不对根写入偏好/喜好正文（落地项目自写）。档案 为产品事实摘要，不是偏好容器。

## 6. 打开/填写

- 运行时正文：仅本文件（开局卡已在会话开头读过）。
- 无强制模板：直接写 §2 产出路径产物。

## 7. 完成信号

- §2 产出已落盘。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 8. 回执字段

```text
route=workflow:onboard | step=mount | reads=rules/packets/onboard/mount.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/onboard/mount.md`；对不上 = 未遵守读链。
