# 前端交互规格模板（interactions.yaml）

> 用途：编码前的**交互状态机真源**。`design`/`plan` 产出，`confirm_ui_spec` 确认；`implement` 按 flow 实施，`ui-audit`/`review` 按 flow 核，门读用例结果。
> 落点：`{workroot}/20-design/交互规格-{主题}-{yyyyMMdd}.yaml`；在本期 `iteration-context.yaml` 的 `inputs.interaction_spec` 指向（缺省回退 `.gate/frontend/interactions.yaml`）；**不写进 `project-profile.md`**。
> 校验：`python <包>/verify/tools/validate_interactions.py --spec <路径> --results .gate/frontend/playwright-results.json --require-results`
> 纪律：一个 flow = 一个可独立验收的交互闭环；**先有规格和用例，再写 UI 代码**；基线阶段不写 `择优`。

## 1. 规格骨架（复制为 YAML）

```yaml
schema: 1
surface: /users                # 路由/页面
flows:
  - id: user-delete            # a-z0-9-；页面内唯一
    class: overlay             # overlay|list|form|linked|static
    entry:
      control: "row:删除"       # 可见控件名/role；必须是原型里真实存在的入口
      guard: "perm:user.delete && row.status=active"   # 无守卫写 none
    states: [closed, open, submitting, error]
    transitions:
      - {id: T1, from: closed, event: "click 删除", to: open, effect: "load name"}
      - {id: T2, from: open, event: "cancel|esc|overlay|close", to: closed, effect: "reset; request=0"}
      - {id: T3, from: open, event: confirm, to: submitting, effect: "POST /users/{id}/delete; lock"}
      - {id: T4, from: submitting, event: success, to: closed, effect: "refresh; toast"}
      - {id: T5, from: submitting, event: failure, to: error, effect: "keep open; show error"}
      - {id: T6, from: submitting, event: "cancel|esc|overlay", to: submitting, effect: "ignore"}
    invariants:
      - {id: I1, name: cancel-no-write, check: "取消/ESC/遮罩/关闭后 request=0 且列表不变"}
      - {id: I2, name: reopen-reset, check: "重开无上次输入/错误"}
      - {id: I3, name: submit-lock, check: "提交中按钮 disabled 且只发 1 次"}
      - {id: I4, name: failure-keep-open, check: "失败不关闭并显示错误"}
      - {id: I5, name: focus-return, check: "关闭后焦点回触发按钮"}
    component:
      name: ConfirmModal
      controlled: [open]
      callbacks: [onCancel, onOk]
      api_owner: page          # 接口调用在页面/hook，弹窗只回调
      forbidden: [api-in-modal, list-state-in-modal]
    persistence: {url: [], reload: reset, back: reset}
    tests:
      - {id: user-delete-cancel, covers: [T2, I1]}
      - {id: user-delete-ok, covers: [T3, T4]}
      - {id: user-delete-fail, covers: [T5, I4]}
      - {id: user-delete-double, covers: [T3, I3]}
      - {id: user-delete-reopen, covers: [T1, I2]}
      - {id: user-delete-focus, covers: [T2, I5]}
      - {id: user-delete-submit-close, covers: [T6]}
    source: "prototype:views-users.js#openDeleteModal L120; PRD §4.2"
```

## 2. 四类必填不变量

| class | 必填 `invariants[].name` | 必测迁移（至少） |
| --- | --- | --- |
| `overlay` | cancel-no-write、reopen-reset、submit-lock、failure-keep-open、focus-return | 打开；取消/ESC/遮罩/关闭；成功；失败；提交中关闭；双击/重开 |
| `list` | filter-page-reset、refresh-preserve、selection-scope、bulk-partial | 筛选→页码重置；刷新保留筛选/页码；选择范围；批量部分失败；空/错 |
| `form` | validate-timing、first-error-focus、submit-lock、leave-guard、draft | 非法提交；首个错误聚焦；提交中重复；离开确认；失败保留 |
| `linked` | clear、disable、reload、default、reset | A 改变→B 清空/禁用/重查；回退默认；重置 |

> 确实不适用 → 在 `class_exceptions` 写 `{invariant: 理由}`，不得静默删。`static` 只登记非交互可见控件（无 transitions/invariants/tests）。

## 3. 用例约定

- 标题：`[FLOW:<flow-id>][T:<T-id>] ...` 或 `[FLOW:<flow-id>][I:<I-id>] ...`，并带 `[CASE:<test-id>]`。
- 结果：Playwright JSON reporter 落 `.gate/frontend/playwright-results.json`；`validate_interactions.py` 按 `[CASE:]` 取状态。
- 两级证据：流用例可用 `page.route` mock（一级）；每个 flow 至少一条不打 mock 的真实入口 happy path（二级）。
- `skip`/失败/报告早于源码 = `BLOCKED`；只用“点通”不算交互验收。
- 只写一个 happy path 不算覆盖：守卫反例、失败、重复、关闭重置、竞态至少各一条。

## 4. 来源与写法

- 每条 flow 的 `source` 指向原型 handler（函数/行号）、PRD 条款或现有实现路径；无来源 = 猜的，A 档不过。
- `entry.control` 必须是原型/现网真实可见的按钮/链接/行操作/输入；不要写「查看/导出」大类。
- `effect` 写可观察结果（请求方法/路径、列表刷新、toast、跳转、焦点）；不要写「处理一下」。
- `component` 写复用组件的受控字段/回调/接口归属；不得在弹窗内直接改列表 state 或调接口。
- `persistence` 写 `url`（哪些筛选进 URL）、`reload`、`back` 的 `keep|reset`；不适用写 `na+理由`。

## 5. 与门/评审

- `confirm_ui_spec`：出示 flow 清单 + 页面/面板清单 + 差异/OPEN + 用例映射；确认后才写 UI 代码。
- `ui-audit` §4 按 flow 核每条 transition/invariant 的用例结果；探索发现新迁移 → 回写 spec + test。
- `review` 核 `flow → transition/invariant → case → 结果` 映射；抽 1 条改断言确认会红。
- 门：`frontend_parity.py --require-interactions`；缺 spec/缺用例/失败/skip/报告早于源码 = `BLOCKED`。
