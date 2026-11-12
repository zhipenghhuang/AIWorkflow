#!/usr/bin/env python3
"""Gate self-test: positive + adversarial fixtures for test_gate.py.

Run: python wf-testing/verify/tools/selftest_gate.py
Exit 0 = all cases behave as expected; 1 = regression.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GOOD = {'.gate/wf-testing/completion.json': '{\n  "gate_version": "3.5",\n  "package": "wf-testing",\n  "mode": "report",\n  "scope": "",\n  "gate_id": "report-0a774127363a",\n  "verdict": "PASS",\n  "counts": {\n    "未执行": 0,\n    "通过": 2,\n    "不适用": 0,\n    "阻塞": 0,\n    "待实现": 0,\n    "未本轮验证": 0,\n    "失败": 0\n  },\n  "by_priority": {\n    "P0": 1,\n    "P1": 0,\n    "P2": 1,\n    "其他": 0\n  },\n  "p0_fail": [],\n  "p0_missing": [],\n  "reported_verdict": "PASS",\n  "conditional_accepted": false,\n  "source_hashes": {\n    "C:\\\\Users\\\\Administrator\\\\AppData\\\\Local\\\\Temp\\\\wf-testing-audit\\\\proj-good\\\\env-baseline.md": "3e86e4b0388390bf49fcdd6c10051a2e1c7b5c70b6e1eca30edfc5903461b9a9",\n    "C:\\\\Users\\\\Administrator\\\\AppData\\\\Local\\\\Temp\\\\wf-testing-audit\\\\proj-good\\\\docs\\\\test-analysis.md": "77c45959e09d3fb66fffd3e566a6d447abe8625afa982d06c9cf0783975c6478",\n    "C:\\\\Users\\\\Administrator\\\\AppData\\\\Local\\\\Temp\\\\wf-testing-audit\\\\proj-good\\\\docs\\\\test-plan.md": "b85efaa751087fed67f9ba58d2277fad14b932855712061459a25e3de82dcb96",\n    "C:\\\\Users\\\\Administrator\\\\AppData\\\\Local\\\\Temp\\\\wf-testing-audit\\\\proj-good\\\\docs\\\\functional\\\\01-登录-执行记录.md": "6a0dd55529af862b0a487e7542f0044841380ab710dbddb76bc7e362144ef713",\n    "C:\\\\Users\\\\Administrator\\\\AppData\\\\Local\\\\Temp\\\\wf-testing-audit\\\\proj-good\\\\docs\\\\test-report.md": "81976b49a41744b2ea45299130979645facb64d1da69e1c8dc999177b1f50775"\n  },\n  "checks": [\n    {\n      "id": "env-baseline",\n      "status": "pass",\n      "detail": "C:\\\\Users\\\\Administrator\\\\AppData\\\\Local\\\\Temp\\\\wf-testing-audit\\\\proj-good\\\\env-baseline.md"\n    },\n    {\n      "id": "analysis-structure",\n      "status": "pass",\n      "detail": "intents=2 p0=1"\n    },\n    {\n      "id": "plan-structure",\n      "status": "pass",\n      "detail": "tier=full"\n    },\n    {\n      "id": "plan-analysis-link",\n      "status": "pass",\n      "detail": "plan linked to analysis"\n    },\n    {\n      "id": "plan-state",\n      "status": "pass",\n      "detail": "已确认"\n    },\n    {\n      "id": "execution-record",\n      "status": "pass",\n      "detail": "records=1"\n    },\n    {\n      "id": "evidence-exists",\n      "status": "pass",\n      "detail": []\n    },\n    {\n      "id": "blocked-reasons",\n      "status": "pass",\n      "detail": []\n    },\n    {\n      "id": "intent-analysis-link",\n      "status": "pass",\n      "detail": "INT linked to analysis"\n    },\n    {\n      "id": "p0-status",\n      "status": "pass",\n      "detail": []\n    },\n    {\n      "id": "p0-falsify",\n      "status": "pass",\n      "detail": "P0 has falsify/N/A"\n    },\n    {\n      "id": "intent-coverage",\n      "status": "pass",\n      "detail": "all 2 intents have scenes"\n    },\n    {\n      "id": "intent-scenes",\n      "status": "pass",\n      "detail": "every intent has a scene"\n    },\n    {\n      "id": "intent-conclusion",\n      "status": "pass",\n      "detail": "all intents terminal"\n    },\n    {\n      "id": "p0-missing",\n      "status": "pass",\n      "detail": "P0 intents have scenes"\n    },\n    {\n      "id": "report-structure",\n      "status": "pass",\n      "detail": "ok"\n    },\n    {\n      "id": "report-verdict",\n      "status": "pass",\n      "detail": "PASS"\n    },\n    {\n      "id": "conditional-acceptor",\n      "status": "pass",\n      "detail": "ok"\n    }\n  ],\n  "blocked": [],\n  "timestamp": "2026-11-10T11:51:50+08:00"\n}', '.gate/wf-testing/coverage.json': '{\n  "gate_version": "3.5",\n  "package": "wf-testing",\n  "mode": "coverage",\n  "scope": "",\n  "gate_id": "coverage-0a774127363a",\n  "verdict": "PASS",\n  "counts": {\n    "未本轮验证": 0,\n    "失败": 0,\n    "通过": 0,\n    "阻塞": 0,\n    "未执行": 0,\n    "不适用": 0,\n    "待实现": 0\n  },\n  "by_priority": {\n    "P0": 0,\n    "P1": 0,\n    "P2": 0,\n    "其他": 0\n  },\n  "p0_fail": [],\n  "p0_missing": [],\n  "reported_verdict": "",\n  "conditional_accepted": false,\n  "source_hashes": {\n    "C:\\\\Users\\\\Administrator\\\\AppData\\\\Local\\\\Temp\\\\wf-testing-audit\\\\proj-good\\\\env-baseline.md": "3e86e4b0388390bf49fcdd6c10051a2e1c7b5c70b6e1eca30edfc5903461b9a9",\n    "C:\\\\Users\\\\Administrator\\\\AppData\\\\Local\\\\Temp\\\\wf-testing-audit\\\\proj-good\\\\docs\\\\test-analysis.md": "77c45959e09d3fb66fffd3e566a6d447abe8625afa982d06c9cf0783975c6478",\n    "C:\\\\Users\\\\Administrator\\\\AppData\\\\Local\\\\Temp\\\\wf-testing-audit\\\\proj-good\\\\docs\\\\test-plan.md": "b85efaa751087fed67f9ba58d2277fad14b932855712061459a25e3de82dcb96"\n  },\n  "checks": [\n    {\n      "id": "env-baseline",\n      "status": "pass",\n      "detail": "C:\\\\Users\\\\Administrator\\\\AppData\\\\Local\\\\Temp\\\\wf-testing-audit\\\\proj-good\\\\env-baseline.md"\n    },\n    {\n      "id": "analysis-structure",\n      "status": "pass",\n      "detail": "intents=2 p0=1"\n    },\n    {\n      "id": "plan-structure",\n      "status": "pass",\n      "detail": "tier=full"\n    },\n    {\n      "id": "plan-analysis-link",\n      "status": "pass",\n      "detail": "plan linked to analysis"\n    }\n  ],\n  "blocked": [],\n  "timestamp": "2026-11-10T11:51:49+08:00"\n}', '.gate/wf-testing/report.json': '{\n  "gate_version": "3.5",\n  "package": "wf-testing",\n  "mode": "report",\n  "scope": "",\n  "gate_id": "report-0a774127363a",\n  "verdict": "PASS",\n  "counts": {\n    "未执行": 0,\n    "通过": 2,\n    "不适用": 0,\n    "阻塞": 0,\n    "待实现": 0,\n    "未本轮验证": 0,\n    "失败": 0\n  },\n  "by_priority": {\n    "P0": 1,\n    "P1": 0,\n    "P2": 1,\n    "其他": 0\n  },\n  "p0_fail": [],\n  "p0_missing": [],\n  "reported_verdict": "PASS",\n  "conditional_accepted": false,\n  "source_hashes": {\n    "C:\\\\Users\\\\Administrator\\\\AppData\\\\Local\\\\Temp\\\\wf-testing-audit\\\\proj-good\\\\env-baseline.md": "3e86e4b0388390bf49fcdd6c10051a2e1c7b5c70b6e1eca30edfc5903461b9a9",\n    "C:\\\\Users\\\\Administrator\\\\AppData\\\\Local\\\\Temp\\\\wf-testing-audit\\\\proj-good\\\\docs\\\\test-analysis.md": "77c45959e09d3fb66fffd3e566a6d447abe8625afa982d06c9cf0783975c6478",\n    "C:\\\\Users\\\\Administrator\\\\AppData\\\\Local\\\\Temp\\\\wf-testing-audit\\\\proj-good\\\\docs\\\\test-plan.md": "b85efaa751087fed67f9ba58d2277fad14b932855712061459a25e3de82dcb96",\n    "C:\\\\Users\\\\Administrator\\\\AppData\\\\Local\\\\Temp\\\\wf-testing-audit\\\\proj-good\\\\docs\\\\functional\\\\01-登录-执行记录.md": "6a0dd55529af862b0a487e7542f0044841380ab710dbddb76bc7e362144ef713",\n    "C:\\\\Users\\\\Administrator\\\\AppData\\\\Local\\\\Temp\\\\wf-testing-audit\\\\proj-good\\\\docs\\\\test-report.md": "81976b49a41744b2ea45299130979645facb64d1da69e1c8dc999177b1f50775"\n  },\n  "checks": [\n    {\n      "id": "env-baseline",\n      "status": "pass",\n      "detail": "C:\\\\Users\\\\Administrator\\\\AppData\\\\Local\\\\Temp\\\\wf-testing-audit\\\\proj-good\\\\env-baseline.md"\n    },\n    {\n      "id": "analysis-structure",\n      "status": "pass",\n      "detail": "intents=2 p0=1"\n    },\n    {\n      "id": "plan-structure",\n      "status": "pass",\n      "detail": "tier=full"\n    },\n    {\n      "id": "plan-analysis-link",\n      "status": "pass",\n      "detail": "plan linked to analysis"\n    },\n    {\n      "id": "plan-state",\n      "status": "pass",\n      "detail": "已确认"\n    },\n    {\n      "id": "execution-record",\n      "status": "pass",\n      "detail": "records=1"\n    },\n    {\n      "id": "evidence-exists",\n      "status": "pass",\n      "detail": []\n    },\n    {\n      "id": "blocked-reasons",\n      "status": "pass",\n      "detail": []\n    },\n    {\n      "id": "intent-analysis-link",\n      "status": "pass",\n      "detail": "INT linked to analysis"\n    },\n    {\n      "id": "p0-status",\n      "status": "pass",\n      "detail": []\n    },\n    {\n      "id": "p0-falsify",\n      "status": "pass",\n      "detail": "P0 has falsify/N/A"\n    },\n    {\n      "id": "intent-coverage",\n      "status": "pass",\n      "detail": "all 2 intents have scenes"\n    },\n    {\n      "id": "intent-scenes",\n      "status": "pass",\n      "detail": "every intent has a scene"\n    },\n    {\n      "id": "intent-conclusion",\n      "status": "pass",\n      "detail": "all intents terminal"\n    },\n    {\n      "id": "p0-missing",\n      "status": "pass",\n      "detail": "P0 intents have scenes"\n    },\n    {\n      "id": "report-structure",\n      "status": "pass",\n      "detail": "ok"\n    },\n    {\n      "id": "report-verdict",\n      "status": "pass",\n      "detail": "PASS"\n    },\n    {\n      "id": "conditional-acceptor",\n      "status": "pass",\n      "detail": "ok"\n    }\n  ],\n  "blocked": [],\n  "timestamp": "2026-11-10T11:51:50+08:00"\n}', 'docs/evidence/sc-001.txt': '401 / account or password error\\n', 'docs/evidence/sc-002.txt': '200 /home -> /login\\n', 'docs/functional/01-登录-执行记录.md': '# 登录 功能执行记录\n\n> **record_format**：`intent-v1`\n> **env-baseline**：env-baseline.md §1/§4/§8\n\n## 0. 记录信息\n\n| 项 | 值 |\n| --- | --- |\n| 轮次/批次 | R1 / B-R1-01 |\n| 原文对账 | 可验收单元 5 / 已覆盖 5 / 本轮补录 0 / 未关 0 |\n| 构建 | b1 |\n\n## 1. 场景与结果\n\n| SC | INT/AC | 原文/依据 | 优先级 | 场景 | 步骤 | 数据/前置 | 预期/Oracle | 结果 | 证据 | 实际/差异 | 缺陷 |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n| SC-001 | INT-001-LOGIN | PRD §2 / AC-01 | P0 | 错误密码登录被拒绝 | 1. 打开 /login 2. 输入 admin/错误密码 3. 点「登录」 4. 核对提示与状态码 | admin/错误密码 | 状态码 401 且提示账号或密码错误 | 通过 | evidence/sc-001.txt | 符合 | — |\n| SC-002 | INT-002-LOGIN | PRD §3 / AC-02 | P2 | 正确账号登录并退出 | 1. 打开 /login 2. 输入 admin/正确密码 3. 点「登录」 4. 点「退出」 | admin/正确密码 | 状态码 200 且跳转 /home，退出后回到 /login | 通过 | evidence/sc-002.txt | 符合 | — |\n\n## 2. 观察与问题\n\n无。\n\n## 3. 意图结论与本轮统计\n\n| INT | 优先级 | 场景 ID | 结论 | 证据 | 缺口/接受人 |\n| --- | --- | --- | --- | --- | --- |\n| INT-001-LOGIN | P0 | SC-001 | 通过 | evidence/sc-001.txt | — |\n| INT-002-LOGIN | P2 | SC-002 | 通过 | evidence/sc-002.txt | — |\n', 'docs/test-analysis.md': '# 审计样例 测试分析（必做）\n\n> **analysis_format**：`intent-v1` ｜ **analysis_mode**：`initial`\n\n## 0. 业务与变更简报\n\n### 0.1 基本信息\n\n| 项 | 值 |\n| --- | --- |\n| 主读 / 版本 / 日期 | PRD / V1 / 2026-11-10 |\n| 分析模式 | initial 初版 |\n| 风险档 | T1 |\n| 范围 / 非目标 | 登录 / 支付 |\n| 对照 | 原型 |\n| 置信度 | 中 |\n\n### 0.2 本期差量表\n\n| ID | 操作 | 简述 | 业务影响 | 依据 |\n| --- | --- | --- | --- | --- |\n| F-01 | 增 | 登录 | 核心 | PRD §2 |\n| F-02 | 增 | 退出 | 一般 | PRD §3 |\n\n### 0.3 影响摘要\n\n- 直接 / 邻接 / 上游 / 下游 / 共享数据 / 事件 / 回归：§5\n- 核心链路：§5.3\n- 环境基线：env-baseline.md §1\n- 建议 suite / 接口 depth / 发布前风险级：module / 不适用 / 基础\n\n## 1. 来源盘点与依据覆盖\n\n### 1.1 来源盘点\n\n| 来源 | 位置 / ID 范围 | 总数 | 已映射 | N/A | 缺口 |\n| --- | --- | ---: | ---: | ---: | ---: |\n| PRD 章节/F/R | §1-§3 | 3 | 3 | 0 | 0 |\n| AC/A | AC-01, AC-02 | 2 | 2 | 0 | 0 |\n\n### 1.2 章节回执\n\n| 章节/标题 | 可测内容 | 意图 / 无 | 落点 |\n| --- | --- | --- | --- |\n| §1 登录入口 | 入口与表单 | INT-001-LOGIN | §2.1 |\n| §2 登录校验 | 正确/错误密码 | INT-001-LOGIN / INT-002-LOGIN | §2.1 |\n| §3 退出 | 退出后状态 | INT-002-LOGIN | §2.1 |\n\n### 1.3 依据覆盖（PRD/方案/原型/接口）\n\n| 依据ID | 来源 | 页面/路由/状态 | 接口/字段/权限/错误码 | 意图ID | 结论 |\n| --- | --- | --- | --- | --- | --- |\n| AC-01 | PRD §2 | /login | — | INT-001-LOGIN | 已覆盖 |\n| AC-02 | PRD §3 | /home | — | INT-002-LOGIN | 已覆盖 |\n\n## 2. 意图与覆盖设计\n\n### 2.1 意图台账\n\n| INT | 来源 | 类型 | 意图（条件 → 动作 → 可观察结果） | Oracle / 验收边界 | 优先级 | 不可接受失败 | 处置 | 接受人 | 方式 |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n| INT-001-LOGIN | PRD §2 / AC-01 | 显式 | 错误密码登录被拒绝 | 状态码 401 且提示账号或密码错误 | P0 | 错误密码仍登录成功 | 测 | — | 功能 |\n| INT-002-LOGIN | PRD §3 / AC-02 | 显式 | 正确账号密码登录成功并可退出 | 状态码 200 且跳转 /home，退出后回到 /login | P2 | — | 测 | — | 功能 |\n\n### 2.1.1 AC / 设计点账本\n\n| 来源条目 | 类型 | 意图 | 处置 | 缺口/接受人 |\n| --- | --- | --- | --- | --- |\n| AC-01 | AC | INT-001-LOGIN | 测 | — |\n| AC-02 | AC | INT-002-LOGIN | 测 | — |\n| F-01 | F | INT-001-LOGIN | 测 | — |\n| F-02 | F | INT-002-LOGIN | 测 | — |\n\n### 2.2 模块/流程 × 覆盖面条矩阵\n\n| 模块/流程 | 主路径 | 状态/分支 | 边界/异常 | 权限/数据域 | 并发/幂等 | 审计/历史 | 通知/附件 | 迁移/兼容 | 非功能 | 视觉/UI | 集成/状态轴 | 计算/算例 | 负向/禁止 |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n| 登录 | INT-002-LOGIN | INT-002-LOGIN | INT-001-LOGIN | N/A+依据：无多角色 | N/A+依据：无并发写 | N/A+依据：不记审计 | N/A+依据：无通知 | N/A+依据：无迁移 | N/A+依据：无性能门槛 | INT-002-LOGIN | N/A+依据：无外部集成 | N/A+依据：无计算 | INT-001-LOGIN |\n\n### 2.3 方法 × 规则矩阵（P0/关键规则）\n\n| 规则/计算 | 等价类 | 边界 | 判定表/组合 | 状态迁移 | 场景 | 算例 | 意图 |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n| 密码校验 | INT-001-LOGIN | INT-001-LOGIN | N/A+依据：单条件 | INT-002-LOGIN | INT-001-LOGIN | INT-001-LOGIN | INT-001-LOGIN |\n\n### 2.4 细节设计覆盖（D01–D13 + S6/S7/S11）\n\n| 细节维 | 适用 | 意图/场景 | 判定面 / oracle | 缺口或依据 |\n| --- | --- | --- | --- | --- |\n| D01 列表/筛选/搜索/排序/分页 | 否 | — | — | 登录无列表 |\n| D02 列/字段/长文本/候选表 | 否 | — | — | 登录无列表 |\n| D03 空态/错误态/无权限/缺关系 | 是 | INT-001-LOGIN | 错误提示给原因 | — |\n| D04 状态与跨载体一致性 | 是 | INT-002-LOGIN | 退出后状态回到未登录 | — |\n| D05 按钮/入口/位置/门禁 | 否 | — | — | 无门禁按钮 |\n| D06 交互反馈/连点/异步 | 否 | — | — | 无异步 |\n| D07 响应式/窄屏/长文本/层级 | 否 | — | — | 本轮不测响应式 |\n| D08 文案/术语一致性 | 否 | — | — | 无跨模块术语 |\n| D09 跳转/返回/刷新/上下文 | 是 | INT-002-LOGIN | 退出回 /login | — |\n| D10 批量/部分失败 | 否 | — | — | 无批量 |\n| D11 导出/下载/文件 | 否 | — | — | 无导出 |\n| D12 规则/配置/数值/时效 | 否 | — | — | 无配置 |\n| D13 数据可信与可追溯 | 否 | — | — | 无汇总数据 |\n| S6 入口/可见/失败下一步 | 是 | INT-001-LOGIN | 失败给原因与下一步 | — |\n| S7 门禁假可点/禁用原因 | 是 | INT-001-LOGIN | 登录按钮非法输入不可提交 | — |\n| S11 提示/空态/同源一致 | 是 | INT-001-LOGIN | 提示与接口错误码同源 | — |\n\n## 3. 风险清单\n\n| RISK | 类别 | 不可接受失败 | 触发 / 边界 | 必须覆盖 | 优先级 | 关联意图 |\n| --- | --- | --- | --- | --- | --- | --- |\n| RISK-01 | 权限 | 错误密码仍登录成功 | 错误密码 | 负向登录 | P0 | INT-001-LOGIN |\n\n### 3.1 风险扫描（逐类，不得留空）\n\n| 类别 | 是否适用 | 结论 / 依据 | 关联意图/风险 |\n| --- | --- | --- | --- |\n| 资金/计费/对账 | 否 | 登录不涉及资金 | — |\n| 状态/生命周期 | 是 | 登录/退出状态 | INT-002-LOGIN |\n| 幂等/并发 | 否 | 无写操作 | — |\n| 跨系统/异步 | 否 | 无外部系统 | — |\n| 权限/数据域 | 是 | 错误密码拒绝 | INT-001-LOGIN |\n| 数据/迁移/回滚 | 否 | 无迁移 | — |\n| 外部依赖/降级 | 否 | 无外部依赖 | — |\n| 历史事故/高发缺陷 | 否 | 无历史事故 | — |\n| 业务语义/空值 | 是 | 空密码拒绝 | INT-001-LOGIN |\n| 可观测性/假成功 | 是 | 提示与状态码一致 | INT-001-LOGIN |\n| UX/可访问性 | 否 | 本轮不测 | — |\n\n## 4. 歧义 / 冲突 / 缺口\n\n| ID | 类 | 原文位置 | 问题 | 建议裁决 | 状态 / 接受人 |\n| --- | --- | --- | --- | --- | --- |\n| Q-01 | 术语 | PRD §2 | 登录失败提示文案未定稿 | 以现网提示为准 | 已确认 |\n\n## 5. 影响面与核心链路\n\n### 5.1 影响面矩阵\n\n| 层级 | 模块/接口/数据/事件 | 依据 | 受影响意图 | 覆盖/回归 | 责任人 |\n| --- | --- | --- | --- | --- | --- |\n| 直接改动 | 登录 | PRD §2 | INT-001-LOGIN | 测 | 测试 |\n| 邻接模块 | 首页 | 登录后跳转 | INT-002-LOGIN | 测 | 测试 |\n| 上游供给 | 账号服务 | 账号数据 | INT-001-LOGIN | 测 | 测试 |\n| 下游消费 | 无 | N/A+依据 | 无 | N/A+依据 | 测试 |\n| 共享数据 | 会话 | 登录态 | INT-002-LOGIN | 测 | 测试 |\n| 事件/异步 | 无 | N/A+依据 | 无 | N/A+依据 | 测试 |\n| 回归锚点 | SMK-01 | 冒烟 | INT-001-LOGIN | 测 | 测试 |\n\n### 5.2 变更影响追溯\n\n| 变更点 ID | 变更摘要 | 直接影响 | 邻接影响 | 上游/下游 | 回归点 | 意图 ID | 状态 |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n| F-01 | 登录 | 登录页 | 首页 | 账号服务 | SMK-01 | INT-001-LOGIN | 已覆盖 |\n| F-02 | 退出 | 退出 | 首页 | 会话 | SMK-01 | INT-002-LOGIN | 已覆盖 |\n\n### 5.3 核心链路\n\n| 链路 ID | 业务目标 | 入口 | 关键步骤 | 关联意图 | P0 冒烟 | 状态 |\n| --- | --- | --- | --- | --- | --- | --- |\n| CORE-01 | 用户登录并退出 | 首页→登录 | 1～4 | INT-001-LOGIN / INT-002-LOGIN | SMK-01 | 已覆盖 |\n\n## 6. 覆盖充分性自检（计划门前）\n\n| 检查 | 通过条件 | 结论/证据 |\n| --- | --- | --- |\n| 来源/章节 | 来源盘点无缺口；章节回执每章有意图或 N/A+依据 | §1 |\n| 依据覆盖 | PRD/方案/原型/接口逐条有意图或 N/A+依据 | §1.3 |\n| 意图 | 每个在范围项有意图；P0/P1/P2 都有处置；N/A 有接受人 | §2.1 |\n| 覆盖矩阵 | 模块/流程 × 面矩阵无空格；空格已在 §4 登记 | §2.2 |\n| 方法矩阵 | P0/关键规则逐方法有落点或 N/A+依据 | §2.3 |\n| 细节维 | D01–D13 + S6/S7/S11 逐维有结论或 N/A+依据 | §2.4 |\n| 风险 | 风险逐类有结论；历史事故已考虑 | §3 |\n| 影响面 | 直接/邻接/上下游/共享数据/事件/回归全行有落点或 N/A+依据 | §5.1 |\n| 变更追溯 | 每个差量点有直接/邻接/上下游/回归与意图 | §5.2 |\n| 核心链路 | 每条有 P0 冒烟/端到端场景或 N/A+依据 | §5.3 |\n| 结论 | 无未解释缺口；分析已确认 | 全表 |\n', 'docs/test-plan.md': '# 审计样例 测试计划（总排）\n\n> **plan_format**：`schedule-v1` ｜ **版本准出=是** ｜ **准出口径=迭代/提测**\n\n## 0. 一页状态\n\n| 项 | 值 |\n| --- | --- |\n| 计划状态 | 已确认 |\n| 计划路径 | 完整 plan_tier=full |\n| 版本准出 | 是 |\n| 准出口径 | 迭代/提测 |\n| 风险档 / 分析模式 | T1 / initial |\n| 版本 / 构建 / 环境 | V1 / b1 / 测试 |\n| 当前轮次 | R0 |\n| 分析文件 | docs/test-analysis.md（意图 2：P0 1 / P1 0 / P2 1；N/A 0；缺口 0） |\n| 执行进度 | 意图终态 0/2 |\n| 当前阶段 | 冒烟 |\n| 下一动作 | 执行 R0 |\n| 阻塞 / 待确认 | 无 |\n| 需人工决策 | 无 |\n| 准出预判 | 可准出 |\n| 最后更新 | 2026-11-10 11:00 |\n\n## 1. 范围与依据\n\n### 1.1 依据\n\n| 类型 | 路径 / 版本 / 日期 | 用途 |\n| --- | --- | --- |\n| 主读 | PRD / V1 | 需求与 AC |\n| 对照 | 原型 | 补充 |\n| 分析 | docs/test-analysis.md | 意图/风险/覆盖 |\n| 环境基线 | env-baseline.md | 环境/账号/数据 |\n\n### 1.2 范围\n\n- **范围内**：登录、退出\n- **明确排除**：支付 + 本期不交付 + 产品\n- **假设 / 约束**：无\n- **已确认决策**：提示文案以现网为准\n\n### 1.3 依据变更\n\n| CR / 日期 | 变化 | 影响意图/风险 | 计划调整 | 状态 |\n| --- | --- | --- | --- | --- |\n| — | 无 | 无 | 无 | 完成 |\n\n### 1.4 影响面与核心链路摘要\n\n| 类型 | 范围/链路 | 关联意图 | 覆盖/回归轮次 | 责任人 |\n| --- | --- | --- | --- | --- |\n| 直接改动 | 登录 | INT-001-LOGIN | R1 | 测试 |\n| 邻接 | 首页 | INT-002-LOGIN | R1 | 测试 |\n| 上游 | 账号服务 | INT-001-LOGIN | R1 | 测试 |\n| 下游 | 无 | N/A+依据 | N/A+依据 | 测试 |\n| 共享数据/权限 | 会话 | INT-002-LOGIN | R1 | 测试 |\n| 核心链路 | CORE-01 | INT-001-LOGIN / INT-002-LOGIN | R0/R1 | 测试 |\n\n## 2. 策略与轨道\n\n| 轨道 | 纳入 | 范围 | 轮次 | 入口/出口 | 负责人 |\n| --- | --- | --- | --- | --- | --- |\n| 功能 | 是 | 登录/退出 | R0/R1 | 环境就绪/终态 | 测试 |\n| 接口/契约 | 否 | 白名单：无服务端/无HTTP/无契约面·接受人=审计 | — | — | 测试 |\n| 回归 | 是 | 登录冒烟 | R2 | 修复后 | 测试 |\n| 探索式 | 是 | 登录体验 | R1 | 章程 | 测试 |\n| 发布前 | 否 | 白名单：无运行时交付/永不部署·接受人=审计 | — | — | 测试 |\n| UAT/灰度 | 否 | N/A+依据：本轮不涉及 | — | — | 业务 |\n\n> 本轮档位：功能 suite=`module`；接口 depth=`不适用`；发布前风险级=`不适用`。\n\n### 2.1 自动化与工具\n\n- **脚本优先**：登录冒烟优先脚本。\n- **脚本落点**：docs/scripts/\n- **证据**：截图 + Network。\n\n### 2.2 环境、账号与数据\n\n| 项 | 值 |\n| --- | --- |\n| 环境基线 | env-baseline.md §1/§4/§8 |\n| 环境 / BaseURL | http://127.0.0.1 |\n| 构建 / 版本 | b1 |\n| 账号 / 角色 / 数据域 | admin |\n| 数据 / 造数 | admin/正确密码、错误密码 |\n| 隔离 / 恢复 | 共享·串行 |\n| 开跑前核验 | 已核验 |\n\n## 3. 轮次与顺序\n\n| 轮次 | 目标 | 范围 | 入口 | 出口 | 记录 |\n| --- | --- | --- | --- | --- | --- |\n| R0 冒烟 | 主链可达 | 登录/退出 | 环境就绪 | 全绿 | smoke-checklist |\n| R1 正式 | 本期意图 | 全部意图 | R0 全绿 | 意图终态 | 执行记录 |\n\n### 3.1 批次与并行\n\n| 批次 | 模块/域 | 意图范围 | 执行形态 | 并行组 | 隔离套/账号/写域 | 依赖/门 | 合并核验 |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n| B-R1-01 | 登录 | INT-001-LOGIN / INT-002-LOGIN | 直跑 | 串行 | 共享·串行 | R0 全绿 | 执行记录+证据 |\n\n### 3.2 探索式安排（T1+）\n\n| 轴 | 章程（一句：看哪里/用什么/想发现什么） | 谱系/风险 | 状态 |\n| --- | --- | --- | --- |\n| S6 入口/可见/失败下一步 | 登录失败是否给原因与下一步 | 入口 | 本场 |\n| S7 门禁假可点/禁用原因 | 空密码时登录按钮是否可提交 | 门禁 | 本场 |\n| S11 提示/空态/同源一致 | 提示与接口错误码是否一致 | 提示 | 本场 |\n| 状态误读/跨载体冲突 | 退出后首页是否仍显示已登录 | 状态 | 本场 |\n\n## 4. 准入与准出\n\n### 4.1 准入\n\n- 分析已确认；计划已确认；P0 冒烟就绪。\n\n### 4.2 准出\n\n- 意图终态 100%；P0 全过；缺口显式列接受人。\n\n### 4.3 功能收口探针（T1+）\n\n| 轴 | 最小探针 | 着落 |\n| --- | --- | --- |\n| S6 入口/可见/失败下一步 | 失败时下一步诚实 | INT-001-LOGIN |\n| S7 门禁假可点/禁用原因 | 禁用有原因 | INT-001-LOGIN |\n| S11 提示/空态/同源一致 | 提示一致 | INT-001-LOGIN |\n\n### 4.4 有条件通过\n\n- 仅限 P0 全过。\n\n### 4.5 发布门槛（适用时）\n\n| 门槛 | 适用 | 要求 | 证据 |\n| --- | --- | --- | --- |\n| 功能 | 是 | 意图终态 + P0 | 执行记录 |\n\n## 5. 缺陷与变更\n\n### 5.1 缺陷分级与提交\n\n| 级别 | 判定 | 处置 |\n| --- | --- | --- |\n| S3 一般 | 非核心异常 | 排期修复 |\n\n### 5.2 修复与回归\n\n- 修复后立即回归。\n\n### 5.3 变更\n\n- A 就地更新。\n\n## 6. 执行日志与决策\n\n| 日期 | 轮次 | 范围 | 结果 | 决策/偏差/缺口 | 链接 |\n| --- | --- | --- | --- | --- | --- |\n| 2026-11-10 | R1 | 登录 | 待执行 | 无 | 执行记录 |\n', 'docs/test-report.md': '# 审计样例 V1 测试报告\n\n> **report_format**：`intent-v1`\n\n## 0. 结论与回执\n\n```text\n【验证回执】verdict=PASS | gate=audit | scenarios=2/2 | p0=全过 | gaps=0\n```\n\n- **准出评估**：通过\n\n## 1. 范围与执行概况\n\n| 项 | 值 |\n| --- | --- |\n| 版本 / 构建 / runId | V1 / b1 / run-1 |\n| 环境 / 环境基线 | 测试 / env-baseline.md §1 |\n| 分析 / 计划 | test-analysis.md / test-plan.md（已确认） |\n| 轮次 | R1 |\n| 功能 suite / 接口 depth / 发布前风险级 | `module` / `不适用` / `不适用` |\n| 本轮场景 / 意图 | 2 场景 / 2 意图 |\n| 执行记录 | docs/functional/01-登录-执行记录.md |\n\n## 2. 覆盖与结果\n\n### 2.1 场景统计\n\n| 优先级 | 场景数 | 通过 | 失败 | 阻塞 | 待实现 | N/A | 未执行 | 未本轮验证 | 结论率 |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n| P0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100% |\n| P1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — |\n| P2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100% |\n| 合计 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 100% |\n\n### 2.2 意图结论\n\n| 优先级 | 意图数 | 已测 | 通过 | 失败 | 阻塞 | 待实现 | N/A | 未测 | 结论率 |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n| P0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 100% |\n| P1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — |\n| P2 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 100% |\n| 合计 | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 100% |\n\n### 2.3 覆盖与收口探针\n\n| 项 | 结论 |\n| --- | --- |\n| 来源 / 章节回执 | 无未接受缺口 |\n| 原文对账（执行记录 §0） | 已填；未关 0 |\n| 依据覆盖（PRD/方案/原型/接口） | 已覆盖 2/2 |\n| AC / 设计点账本 | 已覆盖 4/4 |\n| 模块×面 / 方法×规则 | 无空格 |\n| 细节维 D01–D13 | 6/16；缺口 0 |\n| 影响面（直接/邻接/上游/下游/共享/事件/回归） | 7/7 |\n| 核心链路 | 1/1 |\n| S6 入口/失败下一步 | 齐 |\n| S7 门禁假可点/禁用原因 | 齐 |\n| S11 提示/空态/同源一致 | 齐 |\n| 探索式（T1+） | 章程 4；闭环 |\n| P0 意图 | 全过 |\n| 风险清单 | 逐类有结论；未接受风险 0 |\n\n## 3. 缺陷与回归\n\n| 类别 | 数量 | 说明 |\n| --- | ---: | --- |\n| 交平台/待提交 | 0 | 无 |\n\n- 分级：S1 0 / S2 0 / S3 0 / S4 0；未关闭 S1/S2：0。\n\n## 4. 缺口、风险与接受\n\n| 类型 | 内容 | 影响 | 接受人 | 复审点 |\n| --- | --- | --- | --- | --- |\n\n## 5. 发布建议与证据\n\n- **建议**：可准出。\n- **证据索引**：执行记录、证据目录。\n', 'env-baseline.md': '# 环境基线（审计样例）\n\n## 项目身份\n\n| 项 | 值 |\n| --- | --- |\n| 项目 | 审计样例 |\n| 当前版本/主题 | V1 |\n\n## 1. 登录\n\n| 项 | 值 |\n| --- | --- |\n| 入口 | http://127.0.0.1 |\n\n## 4. 账号\n\n| 项 | 值 |\n| --- | --- |\n| 账号 | admin |\n\n## 8. 浏览器\n\n| 项 | 值 |\n| --- | --- |\n| 浏览器 | Chrome |\n'}


GOOD["docs/exploratory/登录-20261110-1100-探索记录.md"] = (
    "# 登录 探索记录\n\n"
    "## 0. 本场\n\n| 项 | 值 |\n| --- | --- |\n| 章程一句 | 看登录页，用 admin，想发现失败下一步是否诚实 |\n\n"
    "## 0.1 本场风险点\n\n| # | 风险点 | 结论 |\n| ---: | --- | --- |\n| 1 | 失败提示 | 覆盖 |\n\n"
    "## 1. 会话记录\n\n| 项 | 记录 |\n| --- | --- |\n| 覆盖了什么 | 错误密码登录 |\n| 没碰到什么 | 多端 |\n| 疑问 | 无 |\n| 下一场一句 | 无 |\n\n"
    "## 2. 发现\n\n无。\n"
)

GOOD["docs/capabilities/00-能力清单.md"] = (
    "| 能力名 | 启用 | kind | impl | status | 详情 | 绑定 | verified |\n"
    "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
    "| `api-client` | 否 | none | — | missing | 降级 | — | 2026-11-10 |\n"
)


def _upgrade_plan(text: str) -> str:
    text = text.replace(
        "| 构建 / 版本 | b1 |",
        "| 构建 / 版本 | b1 |\n| 构建封板 | build-b1 / 2026-11-10 10:00 |\n| 数据快照 | SEED-1 / 登录账号样本 |",
    )
    block = (
        "\n### 3.3 冒烟清单\n\n"
        "| SMK ID | 入口/路由 | 检查点 | 期望 | 证据 |\n"
        "| --- | --- | --- | --- | --- |\n"
    )
    for i in range(1, 7):
        block += f"| SMK-{i:02d} | /login | 登录页 | 可打开 | 截图 |\n"
    return text + block


GOOD["docs/test-plan.md"] = _upgrade_plan(GOOD["docs/test-plan.md"])

_rec_path = "docs/functional/01-登录-执行记录.md"
_rec = GOOD[_rec_path]
_rec = _rec.replace("| 原文对账 |", "| 原文 / 对照 | PRD / 原型 #/login、#/home |\n| 原文对账 |")
_rec = _rec.replace("PRD §2 / AC-01", "PRD §2 / 原型 #/login")
_rec = _rec.replace("PRD §3 / AC-02", "PRD §3 / 原型 #/home")
_rec = _rec.replace(
    "## 2. 观察与问题",
    "### 1.1 场景覆盖说明\n\n- 正向：`SC-002`\n- 关键负向/失败：`SC-001`\n"
    "- 状态/非法跃迁：`SC-002`\n- 权限/数据域：`N/A+依据：本轮无多角色`\n"
    "- 幂等/并发/恢复/对账：`N/A+依据：无写并发`\n- UI/视觉：`SC-002`\n"
    "- 脚本：`N/A+依据：本轮直跑`\n\n## 2. 观察与问题",
)
GOOD[_rec_path] = _rec


def write_case(root: Path, files: dict[str, str]) -> None:
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")


def verdict(root: Path, mode: str, scope: str | None = None) -> str:
    gate = Path(__file__).with_name("test_gate.py")
    pkg = Path(__file__).resolve().parents[2]
    cmd = [sys.executable, str(gate), "--package-root", str(pkg), "--project-root", str(root), "--mode", mode]
    if scope:
        cmd += ["--scope", scope]
    out = subprocess.run(
        cmd,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    m = re.search(r"^verdict:\s*(\w+)", out.stdout, re.M)
    return (m.group(1) if m else "NO_VERDICT") + ("\n" + out.stdout if m is None else "")


def mutated(path: str, old: str, new: str, files: dict[str, str]) -> dict[str, str]:
    out = dict(files)
    if old not in out[path]:
        raise SystemExit(f"selftest fixture drift: {old!r} not in {path}")
    out[path] = out[path].replace(old, new)
    return out


def main() -> int:
    cases: list[tuple[str, dict[str, str], str, str, str | None]] = []
    cases.append(("good-coverage", GOOD, "coverage", "PASS", None))
    cases.append(("good-execute", GOOD, "execute", "PASS", "functional"))
    cases.append(("good-report", GOOD, "report", "PASS", None))
    cases.append((
        "count-vs-ledger", mutated(
            "docs/test-analysis.md",
            "| PRD 章节/F/R | §1-§3 | 3 | 3 | 0 | 0 |",
            "| PRD 章节/F/R | §1-§3 | 40 | 40 | 0 | 0 |",
            GOOD,
        ), "coverage", "FAIL", None,
    ))
    cases.append((
        "bogus-matrix-int", mutated(
            "docs/test-analysis.md",
            "| 登录 | INT-002-LOGIN | INT-002-LOGIN |",
            "| 登录 | INT-999-BOGUS | INT-002-LOGIN |",
            GOOD,
        ), "coverage", "FAIL", None,
    ))
    cases.append((
        "lite-version-release", mutated(
            "docs/test-plan.md", "plan_tier=full", "plan_tier=lite", GOOD,
        ), "coverage", "FAIL", None,
    ))
    cases.append((
        "ghost-intent", mutated(
            "docs/functional/01-登录-执行记录.md",
            "| INT-001-LOGIN | P0 | SC-001 |",
            "| INT-001-LOGIN | P0 | — |",
            GOOD,
        ), "report", "FAIL", None,
    ))
    cases.append((
        "p0-relabel", mutated(
            "docs/functional/01-登录-执行记录.md",
            "| SC-001 | INT-001-LOGIN | PRD §2 / 原型 #/login | P0 |",
            "| SC-001 | INT-001-LOGIN | PRD §2 / 原型 #/login | P2 |",
            GOOD,
        ), "report", "FAIL", None,
    ))
    cases.append((
        "p0-na-scene", mutated(
            "docs/functional/01-登录-执行记录.md",
            "| 状态码 401 且提示账号或密码错误 | 通过 |",
            "| 状态码 401 且提示账号或密码错误 | 不适用 |",
            GOOD,
        ), "report", "FAIL", None,
    ))
    cases.append((
        "no-p0", mutated(
            "docs/test-analysis.md",
            "| P0 | 错误密码仍登录成功 | 测 | — | 功能 |",
            "| P1 | 错误密码仍登录成功 | 测 | — | 功能 |",
            mutated(
                "docs/test-plan.md",
                "意图 2：P0 1 / P1 0 / P2 1",
                "意图 2：P0 0 / P1 1 / P2 1",
                GOOD,
            ),
        ), "coverage", "FAIL", None,
    ))
    cases.append((
        "plan-draft-state", mutated(
            "docs/test-plan.md", "| 计划状态 | 已确认 |", "| 计划状态 | 草稿 |", GOOD,
        ), "report", "FAIL", None,
    ))
    cases.append((
        "batch-id-mismatch", mutated(
            "docs/functional/01-登录-执行记录.md",
            "| 轮次/批次 | R1 / B-R1-01 |",
            "| 轮次/批次 | R1 / B-R1-99 |",
            GOOD,
        ), "execute", "FAIL", "functional",
    ))
    cases.append((
        "soft-prerelease-na", mutated(
            "docs/test-plan.md",
            "| 发布前 | 否 | 白名单：无运行时交付/永不部署·接受人=审计 | — | — | 测试 |",
            "| 发布前 | 否 | N/A+依据：小改无NFR·接受人=审计 | — | — | 测试 |",
            GOOD,
        ), "coverage", "FAIL", None,
    ))
    cases.append((
        "soft-api-na", mutated(
            "docs/test-plan.md",
            "| 接口/契约 | 否 | 白名单：无服务端/无HTTP/无契约面·接受人=审计 | — | — | 测试 |",
            "| 接口/契约 | 否 | N/A+依据：无接口文档·接受人=审计 | — | — | 测试 |",
            GOOD,
        ), "coverage", "FAIL", None,
    ))
    cases.append((
        "hollow-exploratory", {
            **GOOD,
            "docs/exploratory/登录-20261110-1100-探索记录.md": "\n",
            "docs/test-plan.md": GOOD["docs/test-plan.md"].replace(
                "| S6 入口/可见/失败下一步 | 登录失败是否给原因与下一步 | 入口 | 本场 |",
                "| S6 入口/可见/失败下一步 | 登录失败是否给原因与下一步 | 入口 | 已跑 |",
            ),
        }, "report", "FAIL", None,
    ))

    cases.append((
        "oracle-vague", mutated(
            "docs/test-analysis.md",
            "状态码 401 且提示账号或密码错误",
            "阻断并定位",
            GOOD,
        ), "coverage", "FAIL", None,
    ))
    cases.append((
        "batch-capacity", mutated(
            "docs/test-plan.md",
            "| B-R1-01 | 登录 | INT-001-LOGIN / INT-002-LOGIN | 直跑 |",
            "| B-R1-01 | 登录 | "
            + "、".join(f"INT-900-{i:02d}" for i in range(1, 37))
            + " | 直跑 |",
            GOOD,
        ), "coverage", "FAIL", None,
    ))
    cases.append((
        "batch-all-shortcut", mutated(
            "docs/test-plan.md",
            "| B-R1-01 | 登录 | INT-001-LOGIN / INT-002-LOGIN |",
            "| B-R1-01 | 登录 | 全部 |",
            GOOD,
        ), "coverage", "FAIL", None,
    ))
    cases.append((
        "plan-no-freeze", mutated(
            "docs/test-plan.md",
            "\n| 构建封板 | build-b1 / 2026-11-10 10:00 |",
            "",
            GOOD,
        ), "coverage", "FAIL", None,
    ))
    cases.append((
        "smk-undeclared", mutated(
            "docs/test-plan.md",
            "| SMK ID | 入口/路由 | 检查点 | 期望 | 证据 |",
            "| 编号 | 入口 | 检查点 | 期望 | 证据 |",
            GOOD,
        ), "coverage", "FAIL", None,
    ))
    cases.append((
        "capability-unaccepted", mutated(
            "docs/test-plan.md",
            "**脚本优先**：登录冒烟优先脚本。",
            "**脚本优先**：api-client 回放，登录冒烟优先。",
            GOOD,
        ), "coverage", "FAIL", None,
    ))

    cases.append((
        "no-data-batch", mutated(
            "docs/test-plan.md",
            "| 数据 / 造数 | admin/正确密码、错误密码 |",
            "| 数据 / 造数 | 造数：设备/工单/报工；REG- 前缀 |",
            GOOD,
        ), "coverage", "FAIL", None,
    ))
    cases.append((
        "data-batch-ok", mutated(
            "docs/test-plan.md",
            "| B-R1-01 | 登录 |",
            "| B-R0-DATA | 数据准备 | 无（数据前置） | 造数 | 串行 | 共享·串行 | 环境就绪 | 造数台账 |\n| B-R1-01 | 登录 |",
            mutated(
                "docs/test-plan.md",
                "| 数据 / 造数 | admin/正确密码、错误密码 |",
                "| 数据 / 造数 | 造数：设备/工单/报工；REG- 前缀 |",
                GOOD,
            ),
        ), "coverage", "PASS", None,
    ))

    failed = 0
    for name, files, mode, expected, scope in cases:
        root = Path(tempfile.mkdtemp(prefix="wf-gate-selftest-"))
        try:
            write_case(root, files)
            got = verdict(root, mode, scope)
            ok = got == expected
            print(f"{'PASS' if ok else 'FAIL'} {name} ({mode}): expected {expected}, got {got}")
            failed += 0 if ok else 1
        finally:
            shutil.rmtree(root, ignore_errors=True)
    print(f"SELFTEST {'OK' if failed == 0 else 'FAILED'} ({len(cases) - failed}/{len(cases)})")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
