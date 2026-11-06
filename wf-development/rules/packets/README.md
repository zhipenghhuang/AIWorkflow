# packets/（链路运行时表面）

## 结构

```text
<workflow>/
  _chain.md           # 父状态机（进 wf 读一次；含隔离边界）
  _region-<id>.md     # 子状态机（长链分区；进区读一次）
  _orch.yaml          # 富编排真源（生成 §5；不是运行时必读）
  <step>.md           # 步骤包（当前唯一激活）
```

## 步骤包固定内容

| 节 | 内容 |
| --- | --- |
| §1 元信息 | 包/链/step、**角色**、**前置**、**上游**、**后续**、**失败去向**、轻量路径 |
| §2 目标与产出 | 本步做什么、落到哪 |
| §3 硬约束 | 开局硬约束摘要（14 条）+ 读链 + **本步禁止** |
| §4 门 | hitl / gate / 推进与停点 |
| §5 工作规则 | 编排、动作清单、前端硬门（有 UI 的步） |
| §6 技能指向 | 必开 / 条件开；打开→执行→回包 |
| §7 打开/填写 | 本步要读的文件与模板（至多 1 个） |
| §8 完成信号 | 可验证的完成判定 |
| §9 回执 | `route/step/agent/packet/reads/skills/claim/next` |

## 技能

- **不**把 skill 正文写入步骤包。
- §6 **指向** skill：`打开 → 执行必做 → 回到步骤包`；标**必开**必须执行，条件开未命中标 `na`。
- 技能库目录见 `skills/README.md`，模板库见 `rules/templates/index.md`。

## 链路隔离

- 本目录 `<workflow>/` 只服务该链；改它不影响其它链。
- 只重生成一条链：`build_step_packets.py <包> <包> --only <wf>`。
- 共享层（`rules/core/`、`gates.md`、`workflow.md`、`skills/`、`templates/`）改动影响所有链。

## 维护

- 生成物（`_chain`、`_region`、`<step>.md`）不要手改；改 `_orch.yaml` / `workflows/*.yaml` / `core/` 后重生成。
- 改了共享层或全量重生成后，跑：`Test-Template.ps1` + `validate_workflow.py` + `validate_step_packets.py` + `validate_semantics.py` + `check_skills.py --strict`。
