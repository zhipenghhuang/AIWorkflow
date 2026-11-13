# packets/（链路运行时表面）

## 结构

```text
<workflow>/
  <step>.md           # 步骤卡（当前唯一激活）
_shared/
  closeout.md         # 所有链共享的收尾/提交终端
```

链图不在这里：在 `workflows/<id>.md`（进链读一次）。

> **硬**：AI 开跑本步前必须用工具打开对应 `<step>.md`；未打开本文件 = 未开跑本步；不得凭记忆/`global=ok` 冒充。

## 步骤卡固定内容

| 节 | 内容 |
| --- | --- |
| §1 元信息 | 链/step、角色、上游/后续、失败去向 |
| §2 目标与产出 | 本步做什么、落到哪 |
| §3 硬约束 | 全局规则指针（每步必读 `rules/core/global-rules.md` + `global=ok`）+ 本步边界 |
| §4 门 | hitl / gate / 推进与停点 |
| §5 动作 | 编排、动作清单、前端硬门（有 UI 的步） |
| §6 技能 | 必开 / 条件开；打开→执行→回包 |
| §7 模板与证据 | 至多 1 个主模板 + 按需参考 |
| §8 完成与退出 | 可验证的完成判定、失败去向 |
| §9 回执 | `route/step/agent/packet/skills/claim/next` |

## 链路隔离

- 本目录 `<workflow>/` 只服务该链；改它不影响其它链。
- 只重生成一条链：`build_step_packets.py <包> --only <wf>`。
- 共享层（`rules/core/global-rules.md`、`gates.md`、`skills/`、`templates/`）改动影响所有链。

## 维护

- 生成物（`workflows/<id>.md`、`<step>.md`）不要手改；改 `workflows/*.yaml` 的 notes / gate / skills 后重生成。
- 改共享层或全量重生成后跑：`Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs` + `validate_workflow.py` + `validate_step_packets.py` + `validate_semantics.py` + `check_skills.py --strict`。
