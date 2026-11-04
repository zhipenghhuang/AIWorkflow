> **维护素材**：运行时默认不读；方法与硬约束以 `rules/packets/<workflow>/<step>.md` 为准。

# 能力与技能体检（产品轨）

> **读取级别：参考**。仅 skill-audit 或点名体检时读。  
> **改哪里**：能力 → `{workroot}/capabilities/`；技能 → 本包 `skills/`（HITL）。

## 1. 模式

| 模式 | 触发 | 对照 | 改什么 |
| --- | --- | --- | --- |
| **project** | 体检能力等且有对照 | `{workroot}/capabilities/`、产品档案索引、阶段、近期降级 | 实例能力 + 包内技能 |
| **generic** | 「通用…」或无档案/清单 | 契约+参考目录、技能完整性、生态检索 | 可改技能；禁项目选型写入包契约当真源 |

判定：含「通用/不按项目/通用最优」→ generic；无填实档案且无 `{workroot}/capabilities/00-能力清单.md` → 强制 generic；否则 project。

## 2. 流程

scope → inventory → **discover** → fit → propose → apply → wrap。

## 2.1 生态检索（discover · 硬）

> 目标：用 skills.sh / `find-skills` 发现可吸收方法或能力候选；**禁止**外部 skill 原样装进母版当第二套 SSOT。

1. **域查询**（按范围选；generic 全量至少各 1 次）：
   - {workroot}/PRD：`product manager`、`prd`、`product discovery`
   - 澄清/原型：`grill`、`prototype`、`handoff`
   - 设计：`frontend design`、`web design guidelines`、`ui ux`
   - 元能力：`find skills`、`writing skills`
2. **命令**：`npx skills find <query>`；已装 `find-skills` 则先看 [skills.sh](https://skills.sh/) 榜再 CLI。
3. **质量闸**：installs ≥ 1K（generic 可 ≥100 但标「低安装量」）；优先 `vercel-labs` / `anthropics` / `mattpocock` / `bmad-code-org` / 官方源。
4. **吸收动作**：方法回灌本包 `skills/`｜能力候选写入 `{workroot}/capabilities/` 或（确认后）`capabilities/reference.md`｜维持。
5. **禁止**：未 HITL `npx skills add` 进母版；禁止并行第二套产品编排覆盖口令→workflow。

## 3. 建议卡

```text
ID / 对象（能力名 | skills/<name> | 生态:<owner/repo@skill>）
现象：与基准的差（证据：清单行 / 门失败 / 用户目标 / skills.sh installs）
判定：缺装 | 达不到要求 | 过重 | 过时 | 重复 | 映射断裂 | 可吸收方法 | 可维持
动作：装配能力 | 改{workroot}/capabilities/ | 就地改 SKILL.md | 改技能 README 映射 | 回灌参考目录 | 维持+降级可接受
优先级：P0 / P1 / P2
成本：安装 · token · 维护
```

## 4. 确认后

- 能力写入 `{workroot}/capabilities/`；档案 §6 只刷索引。  
- 技能改包内；契约/参考目录仅通用回灌时改。  
- 改包后跑 `rules/tools/Test-Template.ps1`；改技能后另跑 `rules/tools/check_skills.py <包根> --strict`。

## 5. 纪律

未 HITL 零改动；能力 SSOT=`{workroot}/capabilities/`；浏览器可复用 `docs/testing/capabilities/` 指针。  
生态检索写入报告对应节；无网络/CLI → 记降级，只对照参考目录。
