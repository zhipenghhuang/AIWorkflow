# 缺陷平台适配（通用 · 内置 zentao）

> 只在提交/回写/排障时读；`rules/defects/collaboration.md` 的平台适配指针指向本文件。
> **骨架（三包同名）**：配置 SSOT → 能力表 → Zentao 要点 → 其它 provider（本包能力表含最小能力契约）。

## 配置 SSOT

**一律先读 `env-baseline.md` §13**（或实例标注的缺陷协作节号）：provider、提交方式、备注格式、适配定义。端点/字段/枚举**只认基线映射**；未写「内置 zentao」时**禁止**调用下方 Zentao 要点路径或禅道字段名。

## 0. 探查与适配确认（通用 · 先于套默认值）

> 与 `classification.md` §0、`collaboration.md` §6.0 同向：**AI 自主探查实机 + 用户确认适配**；母版不写死某一家的类型全集。

1. **读基线**：若已有「本项目类型/优先级用法」且用户曾确认 → 直接用。  
2. **不足则探查**：打开实机建单页或读 API/文档，记下真实枚举（单据是否仅 Bug、类型、严重度、优先级、紧急度等——**以实机为准**）。  
3. **匹配**：把卡点成因（实现偏差 / 配置·环境 / 可测性 / 设计口径 / 脚本自身…）映射到实机字段；给主推，对不上就问用户。  
4. **确认入库**：首次或变更映射 → 向用户确认后写入实例基线适配表，后续复用；禁止把探查结果当成母版永久枚举。  
5. **禁**：未探查就默认「代码错误」类；禁假设「必须有独立任务模块」才能盯办（仅 Bug 时用对类型+指派即可）。

## 能力表

**最小能力契约**（基线「适配定义」须覆盖；缺任一项且提交方式≠`export` → 一问补齐；用户确认无平台/不允许代提交才改 `export`，禁静默落盘）：

| 能力 | 语义（平台无关） | 适配须给出 |
| --- | --- | --- |
| 认证 | 登录/取 Token | 端点、凭据字段、刷新方式 |
| 列表 / 查重 | 按指派/创建者/关键词拉未关闭单；**节流**：先列表再本地过滤，少次 search | 过滤参数、分页、标题/路径字段；禁 8+ 同质 search |
| 详情 | 读单全文 | 状态/指派/严重度/优先级/构建/历史备注/附件字段名 |
| 建单 / 提交 | 新建缺陷或盯办单据 | 标题/正文/严重度/优先级/**类型（实机枚举）**/指派/构建等字段与取值；类型用法见 §0 |
| 备注 | 追加评论（与状态同轮） | 评论端点、正文格式（html/md/text） |
| 状态变更 | 解决 / 关闭 / 激活·重开 / 非修复处置 | 语义→平台 transition 或 status/resolution 取值 |
| 指派 | 改负责人 | 字段与账号标识；默认策略可空，不明则问用户 |
| 附件 | 上传与回查挂载 | 上传端点/字段名；回查如何断言已挂到本单 |
| 用户查询 | 解析指派对象（可选） | 查询端点；不支持则备注写姓名 |

**语义动作**（对话与确认包用这些词；写平台时换成 §13 取值）：`submit` 建单｜`comment` 备注｜`resolve_fixed` 标已修复待验｜`close` 关闭｜`activate` 激活/重开｜`assign` 指派｜`mark_duplicate` 标重复｜`nonfix` 非修复（设计如此/不修/延期/外部/转需求等，细分取值见映射）。

通用纪律：

- 状态变更与 comment **同轮**；禁删缺陷对象；禁密码/绝对路径/场景路径入备注或 steps。  
- `steps` 正文 = 执行失败详情投影（协作 §5「同源/投影」；Schema：`defect-writeup-template.md` §5.0.1a）；禁交单现查补事实。  
- 写平台文本版式按 §13「备注格式」：`html` → **每块一个** `<p>…</p>`、块间 `</p>\n<p>`（禁 `\n\n`、禁粘连）、块内仅单 `<br>` 且 `<br>` 后无 `\n`（禁 `<br><br>`）、禁空 `<p></p>`、禁每行外包 `<p>`。`markdown`/`text` → 块内单换行、块间空一行。细则真源：`defect-writeup-template.md` §5.0.1。写入前按 payload 自检。  
- 读单：按缺陷协作语义字段经 §13 映射读取；api 读不全 → `browser`；仍不全 → 请用户补关键备注/附件，禁只看标题分析。  
- 读者过滤：只写事实、证据、请求；场景 ID/路径、执行记录/计划/报告路径、测试脚本、内部分类/评级理由、内部过程、无关测试数据、未标注猜测、PII/密钥不写入。  
- 端点只认 §13（或已声明的内置）；缺映射禁猜、禁探活冒充适配。  
- 回写回查：按 §13 核对状态·指派·备注·附件等**本轮写入字段已落盘**；HTTP 成功码不替代回查；记录 `noteId/time`；不一致按缺陷协作回查节；失败 → 一问重试/补适配/本批统一导出（确认前零落盘），不声称成功。附件失败重试 ≤1，禁反复重传。

## Zentao 要点

**内置 zentao**（仅 provider=zentao 且适配定义含「内置」）：

- Token：`POST /api.php/v1/tokens`；禁浏览器登录页。  
- 建单 REST v1：`openedBuild=trunk`（禁 `0`/空）；`severity`/`pri` 传字符串 `"1"`…`"4"`；`type` **以实机 Bug 类型枚举为准**（常见含代码错误/配置相关/安装部署/安全相关/性能问题/标准规范/测试脚本/设计defects/其他等——**探查后匹配**，实现偏差常用 `codeerror`，配置/环境/设计口径等勿一律 `codeerror`）；产品缺陷有 `designdefect`（或实机「设计缺陷」）则用，否则标题或【提交摘要】首行写「产品缺陷」。指派与类型不明 → 问用户，禁瞎填。  
- **首次建单**：十段只进 `steps`；建单 body 可带 `assignedTo`；**禁止**建单后再 `assign+comment` 刷首条备注（非状态回写不触发 `confirm_remark`）。  
- 附件：`POST /api.php/v2/files`，字段 **`file`** + `objectType=bug` + `objectID`（禁 v1）；非 ASCII 文件名按 UTF-8 原字节写入 multipart `filename`；回查优先 bug 详情 `files` 或 `GET /api.php/v2/files/{fileId}` 核对 `objectType/objectID`。  
- 备注（关/激/解决等）：`POST /api.php/v1/bugs/{id}/assign`，body=`assignedTo`+`comment`（可同指派）；勿仅 `PUT /bugs/{id}`+`{comment}`。  
- 读/回查：详情与列表用 v1；写后 `GET /api.php/v1/bugs/{id}` 核对 `status/resolution/assignedTo/lastEditedDate` 与最新 action（本轮若写备注则 `comment` 须可回读）；附件以 v2 元数据或详情 `files` 为准。  
- resolution 常用取值（写回前仍以 §13 为准）：`fixed` / `notrepro` / `bydesign` / `duplicate` / `external` / `postponed` / `willnotfix` / `tostory`。

### 列表 / 查重（Zentao · 节流）

- **推荐顺序**：`GET /api.php/v1/products/{productId}/bugs?limit=N`（或基线列表端点）→ 本地过滤 title/status/assignedTo → 必要时再 `search=` **至多 1～2 次**高信号词。  
- **禁止**：对十余个近义关键词连环 `search`（实测易返回同质近期单、无增量）。  
- 查重产出：一份 JSON/表（候选 id/title/status/判定=新建|重复|相关）；交 `search` 步主上下文 ≤30 行。

### 共用客户端（方法 · 可选脚本）

- 实例可在 `{workroot}/scripts/` 或 `docs/.draft/` 放**一份** token/create/upload/verify 封装；各批只填 BUGS[]（标题/十段/附件路径）。  
- 凭据只读基线 §13；禁把密码写入执行记录/平台 steps。  
- 不强制包内附带可执行客户端；无脚本时按上列 REST 直调即可。

## 其它 provider

- Jira / GitLab·GitHub Issue / ONES / TAPD 等：按 §13 最小能力契约补端点/字段；**禁**套用 Zentao 要点路径。  
- 补不齐 → 一问「补适配直提｜本批统一导出｜用户粘贴」；确认前零落盘；清单见 `capabilities/00-contract.md`。
