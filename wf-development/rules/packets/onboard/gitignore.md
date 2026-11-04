# 步骤包 · onboard/gitignore

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：开发轨
- **workflow**：`onboard`
- **step**：`gitignore`（入库策略）
- **packet**：`rules/packets/onboard/gitignore.md`
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：入库策略
- **产出**：.gitignore 更新 + `git check-ignore` 证据

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- 四选一：①只忽略运行态/缓存；②忽略产物+证据；③忽略产物+证据+资料（保留模板）；④自定义。 默认②；写档案 、改 .gitignore；密钥/凭据/本地日志不入库；`{workroot}/INDEX.md` 与正式文档按选择入库。 规范包默认不跟踪：只写已装包一行（如 `/wf-development/`），多包写 `/wf/`；不预列未装包、不加注释；其它项只列路径。

## 4. 本步门

- **HITL `confirm_gitignore`**：四选一确认资产范围；规范包默认不跟踪，只写已装包一行（多包 `/wf/`），无注释、不预列未装包；其它项只列路径；写档案 §1 并改 `.gitignore`

## 5. 做法

### 本步动作清单

- 四选一：①只忽略运行态/缓存。
- ②忽略产物+证据。
- ③忽略产物+证据+资料（保留模板）。
- ④自定义。 默认②。
- 写档案 、改 .gitignore。
- 密钥/凭据/本地日志不入库。
- `{workroot}/INDEX.md` 与正式文档按选择入库。 规范包默认不跟踪：只写已装包一行（如 `/wf-development/`），多包写 `/wf/`。
- 不预列未装包、不加注释。
- 其它项只列路径。

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
route=workflow:onboard | step=gitignore | reads=rules/packets/onboard/gitignore.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/onboard/gitignore.md`；对不上 = 未遵守读链。
