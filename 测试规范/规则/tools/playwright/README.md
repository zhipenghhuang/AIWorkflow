# playwright/（脚本档工具 · 默认不读）

> 规则与纪律见 `../../脚本执行.md`（**必读**）；本文件只讲落地与字段细节。首次落地或变更时才读。

## 1. 落地（一次性 · 每项目）

```bash
npm i -D playwright
npx playwright install chromium
```

1. 建目录 `测试/脚本/`，复制两份文件（**复制而非重写**）：
   - `executor.mjs` → `测试/脚本/executor.mjs`（通用引擎，勿改逻辑）
   - `config.template.mjs` → `测试/脚本/case-executor.config.mjs`（按项目替换 `{占位}`）
2. 凭据走环境变量（`E2E_USERNAME` / `E2E_PASSWORD`），**禁**写入 config / 仓库。
3. `环境基线.md` §16 填实例绑定；`.gitignore` 确认不含 `测试/脚本/`（脚本是资产，应入库）。
4. 冒烟：先写 1 条只读用例脚本跑通，再批量。

> `.gitignore` 建议排除：`node_modules/`。

## 2. 命令

```bash
node 测试/脚本/executor.mjs --plan=测试/脚本/01-xxx.script.mjs        # UI 全量跑
node 测试/脚本/executor.mjs --plan=测试/脚本/01-xxx.script.mjs --case=KPI-01   # 子集复跑
node 测试/脚本/executor.mjs --plan=测试/脚本/01-xxx.script.mjs --tag=smoke      # 按标签（冒烟）
node 测试/脚本/executor.mjs --plan=测试/脚本/01-xxx.script.mjs --suite=regression # 按套件
node 测试/脚本/executor.mjs --plan=测试/脚本/01-xxx.script.mjs --check        # 同步检查（不执行）
node 测试/脚本/executor.mjs --plan=… --headless=false               # 有头调试
node 测试/脚本/executor.mjs --plan=… --runStamp=20261015-01         # 固定数据戳
node 测试/脚本/executor.mjs --mode=api --plan=测试/接口测试/脚本/01-xxx.script.mjs --draftDir=测试/接口测试/.draft --evidenceDir=测试/接口测试/证据   # 接口轨（无浏览器）
```

| 选项 | 说明 |
| --- | --- |
| `--mode` | `ui`=浏览器回放（默认）；`api`=接口轨回放（无浏览器） |
| `--plan` | 用例脚本（必填）；`--check` 也用它 |
| `--case` | 单条/子集复跑（按 ID 子串；不改脚本顺序）；**子集默认新 runStamp**——依赖同轮数据时带 `--runStamp=` 原戳或连带被依赖用例 |
| `--tag` | 按 `tags` 选型（如 `smoke`/`regression`/`module:order`）；跨版本回归不改脚本列表 |
| `--suite` | 按脚本 `suites` 名选型（如 `smoke`/`regression`）；未定义 fail（退出码 2） |
| `--runStamp` | 固定本轮数据戳；缺省自动生成 |
| `--baseUrl` | 覆盖 `config.baseUrl` / `TEST_BASE_URL` |
| `--headless=false` | 有头模式 |
| `--check` | 校验脚本 caseId 与用例文档（缺 ID 报 STALE，退出码 1） |
| `--config` / `--root` | 覆盖配置位置 / 项目根 |
| `--draftDir` / `--evidenceDir` | 覆盖 jsonl 输出目录 / 证据根目录（默认 `测试/功能测试/.draft`、`测试/功能测试/证据`；接口/发布前轨指到本轨目录） |

## 3. 产出

| 产出 | 位置 | 说明 |
| --- | --- | --- |
| jsonl | `测试/功能测试/.draft/script-{模块}-{runStamp}.jsonl` | 一条一写；`{caseId,result,summary,evidencePaths}` + `source/runStamp/durationMs`；**合并规则同拆分档 Worker**；默认落点可被 `--draftDir` 覆盖 |
| 失败截图 | `测试/功能测试/证据/{模块}/{CASE-ID}-fail-{runStamp}.png` | 自动全屏 |
| 失败现场 | `测试/功能测试/证据/{模块}/{CASE-ID}-net-{runStamp}.json` | HTTP≥400 + console 摘要（如有） |

`result`：`pass` / `fail` / `blocked`（`ctx.blocked()`，纪律见 `脚本执行.md` §3 第7条）；异常= `fail`。执行器只产这三态（`--case` 未匹配 = 配置错误，退出码 2）；`na`/`pending` 为台账六态的合并容错映射（供拆分档 Worker jsonl 混用）。

**合并提速**：`node 测试规范/规则/tools/merge-ledger.mjs --ledger=测试/功能测试/xx.md --jsonl=…` 机械合并 §1 计数与 §2 行（结论说明仍由 AI 写）。

## 3.1 API 模式（接口轨 · 无浏览器）

- 适用：接口用例（契约明确、断言可写死）；判定口径见 `../../脚本执行.md` §1。
- 脚本位置：`测试/接口测试/脚本/{NN}-{模块}.script.mjs`；登录钩子 `config.apiLogin(api, baseUrl, ctx)` 返回鉴权头对象（并入每步请求；可选，无则匿名）。
- 步骤动作：仅 `api` 与 `note`；字段：`method`｜`path`｜`body`｜`headers`（覆盖鉴权头）｜`expectStatus`（默认 200）｜`expectMessage`（响应 message 含）｜`expectFields`（JSON 路径非空）｜`save`（`{bus 键: JSON 路径}`，供下游 `:key` 占位）。
- 产出：jsonl 同上（`source=script-api`；通过行摘要默认带 `METHOD path -> 状态码;code=` 供落账）；失败自动落 `测试/功能测试/证据/{模块}/{CASE-ID}-api-{runStamp}.json`（请求+响应摘录）。
- 实测：示例系统冒烟 4 条（登录/列表/401 负向/save 提取）≈105ms，全程无浏览器。

## 4. 脚本字段字典

顶层：`module`（模块名，用于产物命名）｜`doc`（用例文档相对路径，`--check` 用）｜`cases[]`。

用例：`id`｜`title`｜`steps[]`｜`run(ctx)`（复杂复算逃逸口，可选）｜`summary`（通过摘要，可选）。

`ctx`（run 内）：`page` `context` `baseUrl` `bus`（`bus.set(k,v)` 写占位符上下文）`config` `blocked(msg)`（仅外部不可用；禁缺样直调，见 `脚本执行.md` §3 第7条）`expect(cond,msg)` `evidence(name)`。

步骤字段：`action`｜`target`｜`value`｜（api 专属）`method` `path` `body` `headers` `expectStatus` `expectMessage` `expectFields` `save`｜（screenshot）`name`。

**占位符**：任意字符串字段中 `:key` 由 `bus` 替换；`:runStamp` 预置。跨用例传参：上游用例 `bus.set('orderId', …)`，下游写 `:orderId`。

**定位优先级**：选择器直通（含 `>>`/`.#[:>*`/伪类）→ 弹层内优先 → `data-testid` → 按钮/文本（antd 两字空格自动兼容）→ label/placeholder/name。字段类动作统一「弹层内 → 页面级」两级回退。

**已内置的坑兼容**（对应实测经验，用例侧直接写自然目标即可）：antd 两字按钮空格、弹层内字段优先、DatePicker 自动回车、select 选中重试、点击两次重试 + Escape 清场、失败自动降级留证。

## 5. 与 AI 通道的边界（复核用）

脚本失败 → **AI 用浏览器 MCP 复核一次**再定性（`../../脚本执行.md` §3）；
`--check` 报 STALE → 用例文档变了，**先同步脚本**再跑，不得带病回归。

## 6. 实测要点（已对真实系统验证，落地时照抄要点即可）

| 要点 | 结论 | 处置 |
| --- | --- | --- |
| SVG 验证码 | base64 SVG 的 `<text>` 即明文，解析 100% 稳定（示例系统 A/B） | 模板 `svgCaptchaText` 直接用；png 类才需 OCR |
| API 鉴权 | 多数后端要求 `Authorization: Bearer <token>` **请求头**；仅注入 Cookie 会被 401（实测「未按照指定前缀提交 token」） | `api` 动作已内置 `config.apiHeaders(page)` 钩子（模板已实现：从 localStorage 读 token + Bearer 头） |
| 存储注入 | 回调函数不能进浏览器（序列化报错）——在 Node 侧先求值再注入 | 模板已按此实现，照抄 |
| 登录提速 | 登录一次/轮 + 跨用例复用会话；实测 2 条用例（登录 + 真实页面断言）~4s、0 token | 冒烟集直接从登录+首屏断言起步 |
| **会话守护** | 部分前端在启动期会发一次**未带鉴权头**的接口（如 notifications）→ 401 → 拦截器清 token → 跳登录页（竞态；注入式登录易踩，偶发） | 已内置 `afterNavigate` 钩子 + `applySession` 重注入（模板/示例系统实例均已实现）：会话被清自动恢复，不重新过验证码；**同时这是应用侧缺陷线索，按脚本失败升级纪律交 AI 复核** |

## 7. CI 落地（可选 · 任意 CI 平台通用）

```bash
npm ci
npx playwright install --with-deps chromium
node 测试/脚本/executor.mjs --check --plan=测试/脚本/{NN}-{模块}.script.mjs   # 可选：用例↔脚本同步体检（STALE 即红）
node 测试/脚本/executor.mjs --plan=测试/脚本/{NN}-{模块}.script.mjs [--mode=api]
```

- 退出码：**0=全过／1=有非通过／2=配置或环境硬错**——按退出码判红绿，不解析日志。
- 制品留存：jsonl（默认 `测试/功能测试/.draft/`）＋ 证据目录；**CI 不写台账/基线/平台**（结论由本包流程补）。
- 凭据：CI secrets 注入环境变量（同 `../../脚本执行.md` §5），禁明文入库。
- 范围与失败处置：只跑已脚本化冒烟/稳定回归；红先通知人、再按 `../../脚本执行.md` §3 有界复核分流（CI 范围与边界见该文 §7）。
- 扩展（项目按需）：视觉回归（Playwright `toHaveScreenshot` 等）、报告看板（消费 jsonl/台账）——母版不内置、不绑定平台。

