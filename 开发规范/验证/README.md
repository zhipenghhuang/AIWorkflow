# 验证（开发轨）

> 目的：把“完成”从 AI 自述变成可复跑的证据。日常只跑一个门；全绿不打断，失败才列阻断项。
> 读取时机：`implement` 收尾前、`verify` 步、`review` 前、`wrap` 前。维护/改规则时读 `规则/核心/规则治理.md`。

## 1. 三条快路径

| 路径 | 适用 | 必跑 | 证据 |
| --- | --- | --- | --- |
| L0 | 单文件/文案/配置，无行为/契约/权限/数据变化 | build + test（定向或全仓）+ 冒烟 | 命令+退出码；空任务窗口 = NOT_VERIFIED |
| L1 | 多文件、普通功能、前端行为变化 | L0 + lint + E2E（前端）+ 前端七项 QA | 桌面+移动截图、console/network |
| L2/L3 | 跨模块、接口/数据、权限/资金/迁移/破坏性 | L1 + 集成/契约/安全/回滚 + 独立评审 | 评审记录、security/rollback |

**定向名实**：仅当 `.gate/project-profile.json` 配了 `lint_scoped`/`test_scoped`/`e2e_scoped`（含 `{files}`）时，门注入本任务变更路径，检查 id=`targeted-*`/`affected-e2e`；**未配则跑全仓命令**，id=`project-*`，不得写「只跑受影响」。
前端最低 L1；纯文案可 L0-light，仍要受影响页截图 + console 无 error。**免审不免自测/证据/门禁**。工具缺失 → `BLOCKED`。

**轻量轨（solo）**：方案卡 §4 验收表即完成门输入；`solo.test` 按 `技能/test-design-and-execution` 出最小充分集并实测，报告落 `05-测试与验收/`。完成门仍按本文件执行；P0 未过不得判通过。

## 2. 一次任务怎么跑

1. **StartTask**：`Invoke-Gate.ps1 -StartTask -TaskId "<任务ID>"` → `.gate/task.json`（`task_id`/`started_at`/`base_commit`）；并清空 `.gate/frontend/` 旧媒体及 `.gate/开发规范/` 下误放的媒体（JSON 回执保留）。门按 **base..工作区** 算变更（中途 commit 不丢窗口）。验收：L1 任务卡 + `-Acceptance`；L2+ `.gate/acceptance.yaml`。命令写 `.gate/project-profile.json`。
2. 实施按验收清单；前端把 `design-qa.md` 拷到 `.gate/frontend/`（L1 七项 / L2+ 十五项）；**截图只写 `.gate/frontend/`**（勿写入 `.gate/开发规范/`）；**截图须晚于 `started_at` 与验收清单 mtime 的较晚者**。
3. 收尾：

```powershell
powershell -ExecutionPolicy Bypass -File "开发规范/验证/Invoke-Gate.ps1" -ProjectRoot "." -Acceptance "开发/04-计划与任务/任务清单-xxx.md"
```

4. 回执 `.gate/开发规范/completion.json`；空任务窗口 → `NOT_VERIFIED`；`--dry-run` → `DRY_RUN`。
5. 先写中文 `【验证回执】` + `【遵守自检】`（route/mode/reads/gates/sync/skip/deviation）；`Test-Report.ps1` 对账（iterate/change/**defect-fix** wrap 均跑）。

**落盘**：`开发规范/验证/` 只读；运行态写项目根 `.gate/开发规范/`（仅 JSON）与 `.gate/frontend/`（截图 + design-qa）。

## 3. 文件

| 文件 | 作用 |
| --- | --- |
| `检查矩阵.yaml` | 人读的策略：变更类型 → 最低检查集 |
| `模板/project-profile.example.json` | 项目命令/前端 URL/视口的可选配置；复制为 `.gate/project-profile.json` |
| `Invoke-Gate.ps1` | 唯一入口；调用 `tools/gate.py` |
| `tools/gate.py` | 变更分级、验收清单解析、检查执行、`completion.json` |
| `验证/Test-Report.ps1` | 报告对账：verdict/禁词/证据 |
| `frontend/验收清单.md` | 只读说明/指针；**实际填写与门读取用 `design-qa.md`**（避免两份同源清单） |
| `frontend/design-qa.md` | 设计 QA 模板；复制到 `.gate/frontend/` 再填；L1 七项、L2+ 十五项 |
| `frontend/playwright.config.template.ts` | Playwright 模板；默认 list+json，不生成 HTML/trace/video；证据落 `.gate/frontend/` |
| `frontend/specs/*.spec.ts` | 主链路/状态/响应式/a11y 模板 |

## 4. 完成状态

> 状态语义、报告措辞与 COMPLETE/PARTIAL/BLOCKED/NOT_VERIFIED/DRY_RUN 条件见 `规则/核心/验证规则.md` §4；本文件不重复，避免两套状态表漂移。

## 5. 成本纪律

- 配了 `*_scoped` → 定向；未配 → 全仓 `project-*`（诚实标 id）。全量回归仍留给发布/L3。
- 截图桌面+移动各 1/页；JPEG/WebP；不默认 HTML/trace/video。
- 门按本轮 `base_commit`+验收重跑；不复用旧回执；早于任务开始的截图 → BLOCKED。
- L1 验收嵌任务卡；L2+ 才落 `acceptance.yaml`。规则只读当前步。
