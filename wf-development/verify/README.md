# 验证（开发轨）

> 目的：把“完成”从 AI 自述变成可复跑的证据。日常只跑一个门；全绿不打断，失败才列阻断项。
> 读取时机：`implement` 收尾前、`verify` 步、`review` 前、`closeout` 前。维护/改规则时读 `rules/core/rule-governance.md`。

## 1. 三条快路径

| 路径 | 适用 | 必跑 | 证据 |
| --- | --- | --- | --- |
| L0 | 纯文档/文案/注释，无代码/配置/行为/契约/权限/数据变化 | `docs-links` + `docs-placeholders` | 链接/占位检查结果；空任务窗口 = NOT_VERIFIED |
| L1 | 单点/≤3 文件/≤1 模块，无接口/数据/权限变化 | build + lint（定向或全仓）+ smoke；配 `test_scoped` 时加定向 test；无定向且无 smoke 才跑全仓 test | 命令+退出码；每条变更路由桌面+移动截图、route-coverage.json、console/network |
| L2/L3 | 跨模块、接口/数据、权限/资金/迁移/破坏性 | L1 + 集成/契约/安全/回滚 + 独立评审 + parity-matrix + **nfr 非功能结论** | 评审记录、security/rollback、parity-matrix、plan-coverage、`nfr.security`/`nfr.performance` |

**定向名实**：仅当 `.gate/project-profile.json` 配了 `lint_scoped`/`test_scoped`/`e2e_scoped`（含 `{files}`）时，门注入本任务变更路径，检查 id=`targeted-*`/`affected-e2e`；**未配则跑全仓命令**，id=`project-*`，不得写「只跑受影响」。升全量条件与禁静默升级见 `rules/core/verification.md` §7；Claim/回写分离见 `global-rules` §9。
前端最低 L1；纯文案/文档可 L0，代码/配置至少 L1，仍要受影响页截图 + console 无 error。**前端证据按 `rules/core/frontend-gate.md` §2.1 分级**：`.gate/frontend/tier.json` 的 A/B/C——A 全量矩阵+每路由桌面/移动；B 受影响路由矩阵+桌面/移动；C 1 张桌面截图、免 parity（gate 读取 tier，缺省 A）。**免审不免自测/证据/门禁**。工具缺失 → `BLOCKED`。

**自包含链（solo）**：方案卡 §4 验收表即完成门输入；`solo.test` 按 `skills/test-design-and-execution` 出按风险完整集并实测（大改动/高风险全节），报告落 `{workroot}/50-verification/`。完成门仍按本文件执行；P0 未过不得判通过。

**任务清单 `[P]`/SC 机检**：`python wf-development/rules/tools/validate_tasklist.py <任务清单.md> --root .`；SC 表缺行/无来源路径或锚点/空原文/非法入口类型，来源文件不存在、`§x` 在目标文档无对应编号标题，方案 §4.1 设计要点 `D-xx` 未被 SC 覆盖，§4.1 漏 `R-xx` 或引用不存在的 `T-xx`，或 `[P]` 文件重叠/相互依赖/并行>3 → FAIL，不 confirm、不派工。完成门加 `-Tasklist <任务清单.md>` 在准出前再硬拦一次；存在 `.gate/plan-coverage.md` 时同轮核 SC ↔ 覆盖矩阵双向闭合。
**实施质量字段**：L1+ 有代码时验收清单须含 `implement_preflight` + `sc_trace`（Markdown 可用「实施预检」行 + SC 表）；命中 profile `shared_globs`（共享/被引用文件）另须 `impact_map`（调用方/依赖模块 + 回归集）；缺或 `missing` → BLOCKED。

**缺陷修复字段**：`task_id=BUG-*` 时验收表须含「原单复现/红证」与「回归/同类路径」项；缺项 → BLOCKED（词项是下限，证据仍按 `rules/defects/fix-collaboration.md` §4.5）。
**方案覆盖矩阵**：`tools/plan_coverage.py` 校验 §1 来源行非空且可解析（禁凭空虚设）、§2/§3 行状态、结论；前端无变更按模板写一行「不适用：…」，该行视为已填而非未完成。


## 2. 一次任务怎么跑

1. **StartTask**：`Invoke-Gate.ps1 -StartTask -TaskId "<任务ID>"` → `.gate/task.json`（`task_id`/`started_at`/`base_commit`）；并把 `.gate/frontend/` 旧媒体与 `.gate/wf-development/` 下误放的媒体**归档**到 `.gate/archive/<task_id>/`（JSON 回执保留；不删除，避免文档引用失效）。门按 **base..工作区** 算变更（中途 commit 不丢窗口）。验收：L1 开发卡/任务卡 + `-Acceptance`；L2+ `.gate/acceptance.yaml`。命令写 `.gate/project-profile.json`；**L1+ 有代码/配置变更未 StartTask → 完成门 BLOCKED**。
   > **L2+ 非功能**：`.gate/acceptance.yaml` 必写 `nfr.security` / `nfr.performance`（`done: <路径/命令/指标>` 或 `na: <理由>`）；缺省或空写 → BLOCKED。项目配 `perf`/`security` 命令时，门在 L2+ 自动执行。
   > **L0/L1 自动口径**：纯文档 → L0，只核 `docs-links`/`docs-placeholders`；代码/配置 → 至少 L1，核 build、lint、smoke 中已配置的命令；L1 未配 `test_scoped` 且有 smoke → 不跑全仓 test；未配置项记 `skip` → 总体 `PARTIAL`，不能 `-Claim`。首次落地先写 `.gate/project-profile.json`（优先配 `*_scoped`）。
2. 实施按验收清单；前端把 `design-qa.md` 拷到 `.gate/frontend/`（L1 十五项含交互诚实与视觉协调 / L2+ 二十项）；**截图只写 `.gate/frontend/`**（勿写入 `.gate/wf-development/`）；**截图须晚于本轮代码 mtime 与 `started_at` 的较晚者（验收文档回写不触发重拍）**；L2+ 另写 `parity-matrix.md` + `route-coverage.json`（每条路由桌面/移动各一张，哈希不重复）。
   - **L2+ 截图必须由 capture 生成**：`.gate/project-profile.json` 配 `frontend.capture`（参考 `frontend/capture_example.py`，输出 `evidence.json` + 每路由桌面/移动截图）。门会先跑 capture，再把 `evidence.json` 与 `route-coverage.json` 逐路由对哈希；手写台账/截图不算证据。
3. 收尾：

```powershell
powershell -ExecutionPolicy Bypass -File "wf-development/verify/Invoke-Gate.ps1" -ProjectRoot "." -Acceptance "{workroot}/40-tasks/任务清单-xxx.md" -Tasklist "{workroot}/40-tasks/任务清单-xxx.md"
# 门末自动输出 CLAIM: ALLOWED；写完成前只需复核（-Claim），不要重复跑全量
powershell -ExecutionPolicy Bypass -File "wf-development/verify/Invoke-Gate.ps1" -Claim -ProjectRoot "."
```

4. 回执 `.gate/wf-development/completion.json`；空任务窗口 → `NOT_VERIFIED`；`-DryRun` → `DRY_RUN`。门 COMPLETE 时末行自动给 `CLAIM: ALLOWED`；`-Claim` 再核三件事：verdict 可放行、无 blocked/失败检查、**回执之后代码/产物未被改动（含已提交）**；任何一项不满足 → `CLAIM: DENIED`，此时只能写“未完成/阻塞/部分完成”。
   > `diff_hash` 只覆盖代码/配置/测试/迁移等非文档文件；计划、`activeContext`、INDEX、验收报告等收尾文档回写不会使回执失效；代码/测试/证据文件变更仍会。
5. 先写中文 `【验证回执】` + `【遵守自检】`（route/mode/reads/gates/sync/skip/deviation）；`Test-Report.ps1` 对账（iterate/change/**defect-fix** closeout 均跑）；无门/阶段收尾用 `python verify/tools/report_lint.py --format-only --report <收尾文件>`，只校验版式不读 completion.json。

**落盘**：`wf-development/verify/` 只读；运行态写项目根 `.gate/wf-development/`（仅 JSON）与 `.gate/frontend/`（截图 + design-qa）。

## 3. 文件

| 文件 | 作用 |
| --- | --- |
| `checks.yaml` | 人读的策略：变更类型 → 最低检查集（含 L2+ `nfr-baseline`） |
| `templates/project-profile.example.json` | 项目命令/前端 URL/视口的可选配置（含可选 `perf` 性能基准命令）；复制为 `.gate/project-profile.json` |
| `Invoke-Gate.ps1` | 唯一入口；调用 `tools/gate.py` |
| `tools/gate.py` | 变更分级、验收清单解析、nfr 校验、检查执行、`completion.json` |
| `verify/Test-Report.ps1` | 报告对账：verdict/禁词/证据 |
| `verify/tools/report_lint.py` | 收尾对账：回执/verdict/禁词/证据 + 六点版式、汇报块、第 2/4/6 点固定子字段、附录；`--format-only` 跳过门禁 |
| `frontend/acceptance.md` | 只读说明/指针；**实际填写与门读取用 `design-qa.md`**（避免两份同源清单） |
| `frontend/design-qa.md` | 设计 QA 模板；复制到 `.gate/frontend/` 再填；L1 十五项（含交互诚实与视觉协调）、L2+ 二十项 |
| `frontend/route-coverage.example.json` | 路由/菜单/深链/截图机读台账模板；复制为 `.gate/frontend/route-coverage.json` |
| `templates/plan-coverage.md` | 方案/功能覆盖矩阵模板；复制为 `.gate/plan-coverage.md`；L2+ 门内校验 |
| `tools/plan_coverage.py` | 校验 `.gate/plan-coverage.md` 章节、后端/功能/前端行、行状态、结论；L2+ 自动调用 |
| `tools/frontend_parity.py` | 校验 parity-matrix + route-coverage + 截图哈希/新鲜度；`--require-generated` 时强制 `evidence.json`；门内自动调用 |
| `frontend/capture_example.py` | capture 参考实现（Playwright）：登录→逐路由→就绪判定（骨架/登录页不算）→桌面/移动截图→`evidence.json`；复制到项目并配 `frontend.capture` |
| `tools/claim_check.py` | 完成口令锁：回执 verdict/blocked/代码新鲜度三合一，输出 `CLAIM: ALLOWED/DENIED` |
| `frontend/playwright.config.template.ts` | Playwright 模板；默认 list+json，不生成 HTML/trace/video；证据落 `.gate/frontend/` |
| `frontend/specs/*.spec.ts` | 主链路/状态/响应式/a11y 模板 |

## 4. 完成状态

> 状态语义、报告措辞与 COMPLETE/PARTIAL/BLOCKED/NOT_VERIFIED 条件见 `rules/core/verification.md` §4（`DRY_RUN` 仅 `-DryRun` 运行态，不是完成状态）；本文件不重复，避免两套状态表漂移。

### 4.1 前端视觉验收（DEV-IQ-13/14/17，硬）

- L1+ 前端页面必须提供：**每条变更/新增路由的桌面截图 + 移动截图**，并与现有同类页面/原型逐项对照（导航层级/文案、复用组件、列/区块/字段网格、状态/空态/交互/权限）。
- **接口 200、DOM 有文字、class 名正确、测试绿，均不能替代视觉验收**。
- 截图不可用/窗口不可见 → `UNVERIFIED`，不得写 `COMPLETE` 或“页面正确”。
- 单 HTML 原型若将模块嵌入 `data:`/base64 importmap：先解码模块再判断页面是否存在；只搜原始 HTML 文本得出的“原型没有”结论无效（DEV-IQ-13）。
- L1+ 必须另交 `.gate/frontend/parity-matrix.md` + `.gate/frontend/route-coverage.json`：
  - 覆盖全部一级/二级菜单、深链、变更/新增路由；
  - 每条路由桌面+移动截图，路径/哈希/时间可追溯；同一截图哈希不得跨路由复用；
  - console error / failed request 为 0；菜单可见或可滚动到达；深链无 404；
  - 详情/表单类页面字段网格、日期/期间控件语义按原型核对，不得简化单列或生搬通用筛选。
- **L2+ 证据必须由 capture 生成**（`frontend.capture`）：`evidence.json` 需含 `generator`、逐路由 `ready=true`、桌面/移动截图哈希；门用哈希对回 `route-coverage.json`。手写截图、骨架页截图、只跑 DOM 文本都不算。
- 自检命令（门内也会跑）：

```powershell
python wf-development/verify/tools/frontend_parity.py --evidence-dir .gate/frontend --since "2026-11-04T10:30:00+08:00" --base-commit 6e4610e
```

## 5. 成本纪律

- 配了 `*_scoped` → 定向；未配 → 全仓 `project-*`（诚实标 id）。全量回归仍留给发布/L3。
- **L1 不全量**：未配 `test_scoped` 且有 smoke → 跑 smoke + 验收证据，不跑全仓 test；未配 `e2e_scoped` 的 L1 不跑全量 e2e（前端证据不降）。
- **失败不空转**：同一检查连续失败 2 次 → 停，换路径/请人确认；`-ResetAttempts` 仅换路径后用。build/test 失败时门跳过 e2e/capture/integration/perf/security。
- 配了 `perf`/`security` 命令 → L2+ 必跑；失败即 BLOCKED，不降级为“人工看过”。
- 全量测试单实例串行，日志落 `.gate/logs/`；中断/并发/超时 = 未验证，不得用旧数字补报告。
- 截图桌面+移动各 1/页；JPEG/WebP；不默认 HTML/trace/video；同一截图哈希不得跨路由复用。
- 门按本轮 `base_commit`+验收重跑；不复用旧回执；早于任务开始的截图 → BLOCKED；`-StartTask` 会递归清理 `.gate/frontend/` 旧媒体。
- L1 验收嵌任务卡；L2+ 才落 `acceptance.yaml`。规则只读当前步。
