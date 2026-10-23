# 验证（开发轨）

> 目的：把“完成”从 AI 自述变成可复跑的证据。日常只跑一个门；全绿不打断，失败才列阻断项。
> 读取时机：`implement` 收尾前、`verify` 步、`review` 前、`wrap` 前。维护/改规则时读 `规则/30-规则治理.md`。

## 1. 三条快路径

| 路径 | 适用 | 必跑 | 目标 |
| --- | --- | --- | --- |
| L0 | 单文件/文案/配置，无行为/契约/权限/数据变化 | build/typecheck + 定向测试 + 冒烟；收尾时报告 lint | < 2 分钟 |
| L1 | 多文件、普通功能、前端行为变化 | L0 + lint + 受影响 E2E + 前端状态/截图/console | < 5 分钟 |
| L2/L3 | 跨模块、接口/数据、权限/资金/迁移/破坏性 | L1 + 集成/契约/安全/回滚 + 独立评审 | < 15 分钟起 |

前端行为/布局变化最低 L1；纯文案可 L0-light，但仍要受影响页面截图 + console 无 error。
工具/环境缺失 → `BLOCKED`，不是完成；没有项目命令时用包内最低检查集，不能用“项目没配”跳过。

## 2. 一次任务怎么跑

1. `clarify`/`plan` 产出并确认验收清单（AC + 检查 + 证据）；L1+ 落在任务卡/开发卡或 `验证/.state/acceptance.yaml`（gate 会聚合多任务表；L1+ 无可解析 AC 会 BLOCKED）。项目档案的「质量门禁命令」同步到 `验证/project-profile.json`（gate 不解析 Markdown 档案）。
2. 实施时按验收清单做；前端改动按 `frontend/验收清单.md` 填满 15 项结果/证据并写结论（gate 会核行数、空值、结论），留截图与 console/network 证据。
3. 收尾前运行：

```powershell
powershell -ExecutionPolicy Bypass -File "开发规范/验证/Invoke-Gate.ps1" -ProjectRoot "."
```

4. 门输出 `.gate/completion.json` 与 ≤30 行摘要；`wrap` 只引用该回执。
5. 报告先写 `【验证回执】`，再写完成内容；`验证/Test-Report.ps1` 会检查 verdict 与措辞。

## 3. 文件

| 文件 | 作用 |
| --- | --- |
| `检查矩阵.yaml` | 人读的策略：变更类型 → 最低检查集 |
| `project-profile.example.json` | 项目命令/前端 URL/视口的可选配置；复制为 `project-profile.json` |
| `Invoke-Gate.ps1` | 唯一入口；调用 `tools/gate.py` |
| `tools/gate.py` | 变更分级、验收清单解析、检查执行、`completion.json` |
| `验证/Test-Report.ps1` | 报告对账：verdict/禁词/证据 |
| `frontend/验收清单.md` | 15 项前端验收；截图与设计 QA |
| `frontend/playwright.config.template.ts` | Playwright 模板；截图/trace 落 `.state/frontend/` |
| `frontend/specs/*.spec.ts` | 主链路/状态/响应式/a11y 模板 |

## 4. 完成状态

```text
in_progress → candidate_complete → (gate) → COMPLETE | PARTIAL | BLOCKED
```

- Agent 只能提出 `candidate_complete`；只有门能写 `COMPLETE`。
- `COMPLETE`：验收项全覆盖、必跑检查通过、证据可打开。
- `PARTIAL`：核心通过但有非阻断缺口；报告必须列缺口，禁止写“完成/全部通过”。
- `BLOCKED`：缺环境/缺证据/检查失败/验收未覆盖；报告只能写“未完成/阻塞/未验证”。

## 5. 成本纪律

- 只跑受影响范围；全量回归只留给发布/L3。
- 截图 2～3 张/页；像素 diff 只对关键页/有基线的页面做。
- 门每次按当前 diff/验收清单重跑；不复用旧回执（避免旧 `completion.json` 假绿）。
- 不为每个小改新增文档；验收清单嵌在任务卡/开发卡。
- 规则/技能只读当前步；不通读全本。
