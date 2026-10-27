# 验证（开发轨）

> 目的：把“完成”从 AI 自述变成可复跑的证据。日常只跑一个门；全绿不打断，失败才列阻断项。
> 读取时机：`implement` 收尾前、`verify` 步、`review` 前、`wrap` 前。维护/改规则时读 `规则/核心/规则治理.md`。

## 1. 三条快路径

| 路径 | 适用 | 必跑 | 证据 |
| --- | --- | --- | --- |
| L0 | 单文件/文案/配置，无行为/契约/权限/数据变化 | build/typecheck + 定向测试 + 冒烟（项目有则跑） | 命令+退出码；无代码改动 = NOT_VERIFIED |
| L1 | 多文件、普通功能、前端行为变化 | L0 + lint + 受影响 E2E（前端）+ 前端七项 QA | 桌面+移动截图、console/network 报告 |
| L2/L3 | 跨模块、接口/数据、权限/资金/迁移/破坏性 | L1 + 集成/契约/安全/回滚 + 独立评审 | 评审记录、security/rollback 证据 |

前端行为/布局变化最低 L1；纯文案可 L0-light，但仍要受影响页面截图 + console 无 error。
工具/环境缺失 → `BLOCKED`，不是完成；没有项目命令时先填 `.gate/project-profile.json`，不能用“项目没配”跳过。
时间只作参考，不作为跳检查的理由。

## 2. 一次任务怎么跑

1. 任务开始先写本轮标记：`Invoke-Gate.ps1 -StartTask -TaskId "<任务ID>" -ProjectRoot "."`（`.gate/task.json`）。`clarify`/`plan` 产出并确认验收清单（AC + 检查 + 证据）；L1 用任务卡并运行门时显式 `-Acceptance <任务清单>`；L2+ 落 `.gate/acceptance.yaml`（含 `task_id`/`level`/`process.review`，L3 另含 `security`/`rollback`）。项目档案的「质量门禁命令」同步到 `.gate/project-profile.json`。
2. 实施时按验收清单做；前端改动把 `frontend/design-qa.md` 复制到 `.gate/frontend/design-qa.md`：L1 填 1/2/3/6/7/10/15 七项，L2+ 填满 15 项；截图与 console/network 报告落 `.gate/frontend/`，截图必须晚于验收清单。
3. 收尾前运行：

```powershell
powershell -ExecutionPolicy Bypass -File "开发规范/验证/Invoke-Gate.ps1" -ProjectRoot "." -Acceptance "开发/04-计划与任务/任务清单-xxx.md"
```

4. 门输出 `.gate/开发规范/completion.json`（同时写 `auto.json`/`frontend.json`）与 ≤30 行摘要；`wrap` 只引用本轮回执。空 diff → `NOT_VERIFIED`；`--dry-run` → `DRY_RUN`，都不是完成。
5. 报告先写中文 `【验证回执】`（通过/部分通过/阻塞/未验证），再写完成内容；`验证/Test-Report.ps1` 会检查中文结论对应的英文 verdict、gate、checks 与措辞。

**落盘纪律**：本目录（`开发规范/验证/`）是规范工具与模板，**只读**；运行态一律写项目根 `.gate/开发规范/` 与 `.gate/frontend/`；禁止写包内 `.state`/`project-profile.json`。

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

- 只跑受影响范围；全量回归只留给发布/L3。
- 截图桌面+移动各 1 张/页（L2+ 可按状态补）；JPEG/WebP 优先；不默认生成 HTML report/trace/video。
- 门每次按当前 diff/验收清单重跑；不复用旧回执；任务开始 `-StartTask`，旧截图/旧验收直接 BLOCKED。
- 不为每个小改新增文档；L1 验收清单嵌在任务卡，L2+ 才落 `.gate/acceptance.yaml`。
- 规则/技能只读当前步；不通读全本。
