# 前端验收清单（开发轨）

> **唯一填写与门读取模板：`design-qa.md`**。本文件只保留说明，避免两份清单漂移。
> 证据落点：`.gate/frontend/`（每条路由桌面 + 移动截图、console/network 报告、`design-qa.md`、`parity-matrix.md`、`route-coverage.json`、`ui-audit.md`）；规范包 `verify/` 只读，勿写运行态。
> C 档只填 `design-qa.md` 的 1/2/5/6/12/19；L1 至少填 1/2/3/6/7/8/9/10/14/15/16/17/18/19/20 十五项（含交互诚实与视觉协调）；L2+ 填满 20 项；结论非「不通过」。
> A/B 档另须 `interactions.yaml` + flow 用例结果（`playwright-results.json`）与独立 `ui-audit.md`（审计者≠实施者；路由/20 维/flow/一致性/后端可达/真实数据；§10 `INDEPENDENT_REVIEW: PASS`；结论=通过）；C 档免独立审计。
> L2+ 还须通过 `verify/tools/frontend_parity.py`（矩阵 + 路由/菜单/深链台账 + 截图哈希/新鲜度 + `--require-audit --require-interactions`）。
