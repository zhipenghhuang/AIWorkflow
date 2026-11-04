> **维护素材**：运行时默认不读；方法与硬约束以 `rules/packets/<workflow>/<step>.md` 为准。

# 能力与技能体检（测试轨）

> **读取级别：参考**。仅 `workflows/skill-audit.yaml` 或点名体检时读；业务任务不读。  
> **定位**：盘点**实例能力** + 检查/优化随包技能。  
> **改哪里**：能力 → 只改 `{workroot}/capabilities/`；技能 → 确认后可改本包 `skills/`。点名「通用优化技能」时技能按通用最优（不绑项目）。

## 1. 模式

| 模式 | 触发口令（例） | 对照基准 | 改什么 |
| --- | --- | --- | --- |
| **project** | 体检能力 / 能力优化 / …（且有项目对照物） | `{workroot}/capabilities/`、环境基线索引、T0～T3、轨道、近期门失败/降级、用户目标 | `{workroot}/capabilities/`；本包 `skills/`；基线 §8/§17 仅刷索引 |
| **generic** | 含「通用」「不按项目」「通用最优」；或无填实基线/清单 | 契约+参考目录、技能完整性/映射、生态检索；**禁止**写死环境特例 | 可改包内技能；**不**把某项目选型写进包契约当真源 |

**模式判定**：口令含「通用/不按项目/通用最优」→ generic；否则无填实基线且无 `{workroot}/capabilities/00-能力清单.md` → **强制 generic**；有填实清单或基线 → project。

## 2. 流程

1. **scope** → 2. **inventory** → 3. **discover** → 4. **fit** → 5. **propose** → 6. **apply**（`confirm_skill_changes`）→ 7. **wrap**。

## 2.1 生态检索（discover · 硬）

> 目标：用 skills.sh / `find-skills` 发现可吸收方法或能力候选；**禁止**外部 skill 原样装进母版当第二套 SSOT。

1. **域查询**（按范围选；generic 全量至少各 1 次）：
   - 执行/自动化：`playwright`、`e2e testing`
   - 分析/用例：`qa`、`test case`、`test plan`
   - AI/安全：`ai testing`、`security testing`
   - 元能力：`find skills`
2. **命令**：`npx skills find <query>`；已装 `find-skills` 则先看 [skills.sh](https://skills.sh/) 榜再 CLI。
3. **质量闸**：installs ≥ 1K（generic 可 ≥100 但标「低安装量」）；优先 `currents-dev` / `wshobson` / `fishzjp` / 官方源；多数低安装量 QA 包默认不推荐。
4. **吸收动作**：方法回灌本包 `skills/` 或 `rules/special/script-execution.md`｜能力候选写入 `{workroot}/capabilities/` 或（确认后）`capabilities/reference.md`｜维持。
5. **禁止**：未 HITL `npx skills add` 进母版；禁止用外部用例生成器绕过分析表/oracle/追溯红线。

## 3. 建议卡

```text
ID / 对象（能力名 | skills/<name> | 生态:<owner/repo@skill>）
现象：与基准的差（证据：清单行 / 门失败 / 计划缺口 / 用户目标 / skills.sh installs）
判定：缺装 | 达不到要求 | 过重 | 过时 | 重复 | 映射断裂 | 可吸收方法 | 可维持
动作：装配能力 | 改{workroot}/capabilities/ | 就地改 SKILL.md | 改技能 README 映射 | 回灌参考目录 | 维持+降级可接受
优先级：P0 / P1 / P2
成本：安装 · token · 维护
```

## 4. 可执行动作（确认后）

- **外部能力**：安装/绑定步骤；写入 `{workroot}/capabilities/`（清单/槽位/绑定/装配笔记）；刷基线 §8/§17 索引。可续「装配能力」。  
- **随包技能**：就地改 `skills/<name>/SKILL.md` 与 `skills/README.md`。  
- **包契约/参考目录**：仅当通用缺口且用户确认回灌母版时改 `wf-testing/capabilities/`；默认改实例。  
- 改包后跑 `rules/tools/Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`；改技能后另跑 `rules/tools/check_skills.py <包根> --strict`。

## 5. 纪律

- 未 HITL 零改动。装配=安装向导；本流程=诊断+优化。  
- 能力正文 SSOT=`{workroot}/capabilities/`；他处只索引。  
- generic 禁止环境硬编码；一次会话只体检本包。  
- 生态检索写入报告对应节；无网络/CLI → 记降级，只对照参考目录。
