# 能力与技能体检（开发轨）

> **读取级别：按需**。仅 `skill-audit` 链或点名「体检能力」时读。  
> **改哪里**：能力 → `{workroot}/capabilities/`；技能 → 本包 `skills/`（HITL）。

## 1. 模式

| 模式 | 触发 | 对照 | 改什么 |
| --- | --- | --- | --- |
| **project** | 体检能力等且有项目对照 | `{workroot}/capabilities/`、项目档案索引、栈、近期失败/降级 | 实例能力 + 包内技能 |
| **generic** | 「通用/不按项目/通用最优」或无档案/清单 | 契约+参考目录、技能完整性、生态检索 | 可改技能；禁把项目选型写入包契约当真源 |

判定：含「通用…」→ generic；无填实档案且无 `{workroot}/capabilities/00-能力清单.md` → 强制 generic；否则 project。

## 2. 流程

scope → inventory → **discover** → fit → propose → apply → closeout。

## 2.1 生态检索（discover · 硬）

> 目标：用 skills.sh / `find-skills` 发现可吸收方法或能力候选；**禁止**把外部 skill 原样装进母版当第二套 SSOT。

1. **域查询**（按范围选，generic 全量至少覆盖下列域各 1 次）：
   - 架构/评审/调试：`architecture review`、`code review`、`debugging`
   - 规格/计划：`spec driven`、`planning`
   - 前端：`frontend design`、`react best practices`（档案有前端栈才加深）
   - 安全：`threat modeling`
   - 元能力：`find skills` / `writing skills`
2. **命令**：优先 `npx skills find <query>`；宿主已装 `find-skills` 则按其步骤（先看 [skills.sh](https://skills.sh/) 榜，再 CLI）。
3. **质量闸（推荐才进报告）**：
   - installs ≥ 1K（generic 可放宽到 ≥100 但须标「低安装量」）
   - 优先信誉源：`vercel-labs`、`anthropics`、`obra`、`addyosmani`、`mattpocock`、`openai`、`wshobson`、官方组织仓
   - 仓库过小/无许可说明 → 不推荐
4. **吸收动作（只能选其一写入建议卡）**：
   - **方法回灌**：把可判定步骤/反合理化/DoD 改写进本包 `skills/<name>/SKILL.md`（中文、对齐门与路径）
   - **能力候选**：写入实例 `{workroot}/capabilities/` 或（generic+用户确认）回灌 `capabilities/reference.md`
   - **维持**：已覆盖或冲突编排 → 记「可维持」+理由
5. **禁止**：未 HITL 执行 `npx skills add` 进母版/业务仓；禁止并行第二套口令路由；禁止用外文 skill 覆盖本包中文路径绑定。

## 3. 建议卡

```text
ID / 对象（能力名 | skills/<name> | 生态:<owner/repo@skill>）
现象：与基准的差（证据：清单行 / 门失败 / 用户目标 / skills.sh installs）
判定：缺装 | 达不到要求 | 过重 | 过时 | 重复 | 映射断裂 | 可吸收方法 | 可维持
动作：装配能力 | 改 {workroot}/capabilities/ | 就地改 SKILL.md | 改技能 README 映射 | 回灌参考目录 | 维持+降级可接受
优先级：P0 / P1 / P2
成本：安装 · token · 维护
```

## 4. 确认后

- 能力写入 `{workroot}/capabilities/`；档案 §6 只刷索引。  
- 技能改包内；契约/参考目录仅通用回灌时改。  
- 改包后跑 `rules/tools/Test-Template.ps1`；改技能后另跑 `rules/tools/check_skills.py <包根> --strict`。

## 5. 纪律

未 HITL 零改动；能力 SSOT=`{workroot}/capabilities/`；浏览器可复用 `docs/testing/capabilities/` 指针。  
生态检索证据写入体检报告「生态检索」节；无网络/CLI 不可用 → 记降级并只对照参考目录，不得假装已检索。

