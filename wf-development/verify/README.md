# 验证（开发轨）

> 目的：把“完成”从 AI 自述变成可复跑的证据。日常只跑一个门；全绿不打断，失败才列阻断项。
> 读取时机：`implement` 收尾前、`verify` 步、`review` 前、`wrap` 前。维护/改规则时读 `rules/core/rule-governance.md`。

## 1. 三条快路径

| 路径 | 适用 | 必跑 | 证据 |
| --- | --- | --- | --- |
| L0 | 单文件/文案/配置，无行为/契约/权限/数据变化 | build + test（定向或全仓）+ 冒烟 | 命令+退出码；空任务窗口 = NOT_VERIFIED |
| L1 | 多文件、普通功能、前端行为变化 | L0 + lint + E2E（前端）+ 前端七项 QA | 桌面+移动截图、console/network |
| L2/L3 | 跨模块、接口/数据、权限/资金/迁移/破坏性 | L1 + 集成/契约/安全/回滚 + 独立评审 | 评审记录、security/rollback |

**定向名实**：仅当 `.gate/project-profile.json` 配了 `lint_scoped`/`test_scoped`/`e2e_scoped`（含 `{files}`）时，门注入本任务变更路径，检查 id=`targeted-*`/`affected-e2e`；**未配则跑全仓命令**，id=`project-*`，不得写「只跑受影响」。
前端最低 L1；纯文案可 L0-light，仍要受影响页截图 + console 无 error。**免审不免自测/证据/门禁**。工具缺失 → `BLOCKED`。

**轻量轨（solo）**：方案卡 §4 验收表即完成门输入；`solo.test` 按 `skills/test-design-and-execution` 出最小充分集并实测，报告落 `{workroot}/50-verification/`。完成门仍按本文件执行；P0 未过不得判通过。

**任务清单 `[P]` 机检**：`python wf-development/rules/tools/validate_tasklist.py <任务清单.md>`；文件重叠/相互依赖/并行>3 → FAIL，不 confirm、不派工。完成门加 `-Tasklist <任务清单.md>` 可在准出前再硬拦一次。  


## 2. 一次任务怎么跑

1. **StartTask**：`Invoke-Gate.ps1 -StartTask -TaskId "<任务ID>"` → `.gate/task.json`（`task_id`/`started_at`/`base_commit`）；并清空 `.gate/frontend/` 旧媒体及 `.gate/wf-development/` 下误放的媒体（JSON 回执保留）。门按 **base..工作区** 算变更（中途 commit 不丢窗口）。验收：L1 任务卡 + `-Acceptance`；L2+ `.gate/acceptance.yaml`。命令写 `.gate/project-profile.json`。
2. 实施按验收清单；前端把 `design-qa.md` 拷到 `.gate/frontend/`（L1 七项 / L2+ 十五项）；**截图只写 `.gate/frontend/`**（勿写入 `.gate/wf-development/`）；**截图须晚于 `started_at` 与验收清单 mtime 的较晚者**。
3. 收尾：

```powershell
powershell -ExecutionPolicy Bypass -File "wf-development/verify/Invoke-Gate.ps1" -ProjectRoot "." -Acceptance "{workroot}/40-tasks/任务清单-xxx.md" -Tasklist "{workroot}/40-tasks/任务清单-xxx.md"
```

4. 回执 `.gate/wf-development/completion.json`；空任务窗口 → `NOT_VERIFIED`；`--dry-run` → `DRY_RUN`。
5. 先写中文 `【验证回执】` + `【遵守自检】`（route/mode/reads/gates/sync/skip/deviation）；`Test-Report.ps1` 对账（iterate/change/**defect-fix** wrap 均跑）；可选 `python verify/tools/check_compliance.py --report <收尾文件>`。

**落盘**：`wf-development/verify/` 只读；运行态写项目根 `.gate/wf-development/`（仅 JSON）与 `.gate/frontend/`（截图 + design-qa）。

## 3. 文件

| 文件 | 作用 |
| --- | --- |
| `checks.yaml` | 人读的策略：变更类型 → 最低检查集 |
| `templates/project-profile.example.json` | 项目命令/前端 URL/视口的可选配置；复制为 `.gate/project-profile.json` |
| `Invoke-Gate.ps1` | 唯一入口；调用 `tools/gate.py` |
| `tools/gate.py` | 变更分级、验收清单解析、检查执行、`completion.json` |
| `verify/Test-Report.ps1` | 报告对账：verdict/禁词/证据 |
| `verify/tools/check_compliance.py` | 收尾【验证回执】+【遵守自检】字段；头块禁粘行；汇报导语（与产/测同源） |
| `frontend/acceptance.md` | 只读说明/指针；**实际填写与门读取用 `design-qa.md`**（避免两份同源清单） |
| `frontend/design-qa.md` | 设计 QA 模板；复制到 `.gate/frontend/` 再填；L1 七项、L2+ 十五项 |
| `frontend/playwright.config.template.ts` | Playwright 模板；默认 list+json，不生成 HTML/trace/video；证据落 `.gate/frontend/` |
| `frontend/specs/*.spec.ts` | 主链路/状态/响应式/a11y 模板 |

## 4. 完成状态

> 状态语义、报告措辞与 COMPLETE/PARTIAL/BLOCKED/NOT_VERIFIED/DRY_RUN 条件见 `rules/core/verification.md` §4；本文件不重复，避免两套状态表漂移。

### 4.1 前端视觉验收（DEV-IQ-13/14，硬）

- L1+ 前端页面必须提供：**桌面截图 + 移动截图**，并与现有同类页面/原型逐项对照（导航层级/文案、复用组件、列/区块、空态/错误态）。
- **接口 200、DOM 有文字、class 名正确、控制台无报错，均不能替代视觉验收**。
- 截图不可用/窗口不可见 → `UNVERIFIED`，不得写 `COMPLETE` 或“页面正确”。
- 单 HTML 原型若将模块嵌入 `data:`/base64 importmap：先解码模块再判断页面是否存在；只搜原始 HTML 文本得出的“原型没有”结论无效（DEV-IQ-13）。

## 5. 成本纪律

- 配了 `*_scoped` → 定向；未配 → 全仓 `project-*`（诚实标 id）。全量回归仍留给发布/L3。
- 截图桌面+移动各 1/页；JPEG/WebP；不默认 HTML/trace/video。
- 门按本轮 `base_commit`+验收重跑；不复用旧回执；早于任务开始的截图 → BLOCKED。
- L1 验收嵌任务卡；L2+ 才落 `acceptance.yaml`。规则只读当前步。
