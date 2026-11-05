# 开局卡（开发轨）

> **读取级别：常驻**。新会话 / 切包 / 接管任务 **先读本文（≤60 行）**，再按需读 `AGENTS.md` 口令表。  
> **中段**：心跳重锚身份 + 当前步骤包（及所在子机）；禁止通读全书。  
> **冲突**：用户本轮明确指令 > 根 AGENTS > 开局卡/包规则；与门/红线冲突须先说明再等选择。

## 1. 八条硬约束

1. **先意图、再动作**（`confirm_task_intent`）：新开先【需求与意图理解】再确认；未确认禁改代码/外发/下完成结论。
2. **短读跟随 + 一手源**：`activeContext` + 进行中（`rule_card`/`packet=`/`region=`）+ 偏好/洞见/坑 ≤3。
3. **状态机读链（硬）**：见 §4。父流程可拆子机；同时只激活**一个**步骤包。
4. **技能闭环（质量不降）**：步骤包 §6 标**必开**的 skill 必须打开→按必做执行→**回到步骤包**；禁止把 skill 正文嵌进步骤包替代实读；禁止跳过必开 skill。
5. **完成分层**：`verify/Invoke-Gate.ps1 -Claim` → 只认 `CLAIM: ALLOWED`。无 ALLOWED 禁止写「已通过」。
6. **前端硬门**：有 UI → 当前步骤包内前端硬门；无 UI 标 `na`。
7. **证据先于结论；禁刷绿**；密钥零入库；最小改动；失败同方案 2 次换路径。
8. **切步/出子机 → 心跳一行**，必须带 `packet=`（有子机带 `region=`）。

## 2. 本步命令

| 场景 | RUN |
| --- | --- |
| 进 workflow | 读 `_chain.md` 一次 → 落到入口 step / 子机 |
| 进长链子区 | 读 `_region-*.md` 一次 → 区内逐步 |
| 执行 step | 开该步骤包 → §6 必开 skill 闭环 → 回包完成门/产出 |
| 声称完成 | `verify/Invoke-Gate.ps1 -Claim` |
| 轻量 L0 | 预检/前端可 `na`+理由；**必开 skill 与 Claim 不降** |

## 3. 禁做

- 通读整条 workflow 的全部步骤包 / 一次开多个 skill。
- 跳过必开 skill，或把 SKILL 粘贴进步骤包冒充已执行。
- 切步后仍用旧 `packet=`；Claim DENIED 仍写通过。

## 4. 状态机读链（防稀释 · 不降质）

```text
父状态机  rules/packets/<wf>/_chain.md          ← 进 wf 一次
 └─ 子状态机 rules/packets/<wf>/_region-<id>.md ← 进该区一次（长链才有）
      └─ 步骤包   rules/packets/<wf>/<step>.md  ← 当前唯一激活
           └─ 技能闭环 skills/<name>/SKILL.md   ← §6 必开/条件开：打开→执行→回步骤包
                └─ 模板（可选，至多 1）
```

| 层级 | 管什么 | 不管什么 |
| --- | --- | --- |
| `_chain` / `_region` | 路径、入口、区内步骤表 | 方法细节 |
| 步骤包 | 门、产出、完成、编排 | 不粘贴 skill 全文 |
| skill | 专业方法/必做（质量） | 不改门名/Claim |

## 5. 回执

```text
route=… | step=… | region=…|na | packet=rules/packets/… | reads=… | skills=name|done|na | claim=… | next=…
```

`packet=` 丢失或必开 skill 未闭环 = 先重锚/补做，再继续。
