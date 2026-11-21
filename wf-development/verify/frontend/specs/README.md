# 交互流用例（specs/flows）

> 目的：把 `interactions.yaml` 的每条 transition/invariant 变成可运行的 Playwright 用例；门读 `playwright-results.json`，不看“点通”自述。
> 模板：`flows.template.ts`；复制到 `specs/flows/<页面>.spec.ts` 后按项目改。

## 标题约定

```text
[FLOW:<flow-id>][T:<transition-id>][CASE:<case-id>] 描述
[FLOW:<flow-id>][I:<invariant-id>][CASE:<case-id>] 描述
```

- `flow-id` / `T*` / `I*` 必须与 `interactions.yaml` 一致。
- `case-id` 必须与 YAML `tests[].id` 一致；校验器按 `[CASE:]` 读取结果。
- 每个 transition/invariant 至少一条；`skip` 视同未过。

## 运行

```powershell
# 在项目根；config 需启用 JSON reporter -> .gate/frontend/playwright-results.json
npx playwright test specs/flows
```

在 `.gate/project-profile.json` 配：

```json
"frontend": { "flows": "npx playwright test specs/flows" }
```

未配 `flows` 时门复用 `e2e`；A/B UI 两者都未配 = `BLOCKED`。

## 一级 / 二级证据

- **一级（状态机）**：`page.route` mock 成功/失败/延迟；断言迁移、请求次数、关闭/重置、竞态、重复点击。
- **二级（集成）**：至少一条不打 mock 的真实入口 happy path；可由 e2e 主链承担。
- 只跑 mock 或只跑真实 happy path 都不够；两级都要。

## 写法

- 定位用 role/text 或 `data-testid`，不用脆弱 CSS/层级。
- 每个用例只验证一个 flow 的一条迁移或一条不变量，断言可观察结果（dialog 可见性、请求计数、URL、toast、列表行数）。
- 禁止 `test.skip`、`waitForTimeout` 代替等待、只断言“不报错”。
- 失败/关闭/重复/竞态至少各一条；守卫反例（无权限/状态不允许）单独一条。
- 语言无关：Vue/React/原生均可；只要求 Playwright 与 JSON reporter。
