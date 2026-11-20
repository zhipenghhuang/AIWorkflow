#!/usr/bin/env python3
"""提交前机检（git pre-commit hook）。

作用：把「实施出口机检」从口头规则变成不可静默跳过的动作。
- 暂存区含前端文件 → 必须是「本轮证据 + 门禁回执」：`.gate/frontend/gate.json` 存在、ok=true、且晚于最新暂存文件；A/B 另须 `ui-audit.md` 结论通过且晚于最新暂存文件；否则阻断。
- 暂存区含代码文件（L2+）→ 必须是 `.gate/plan-coverage.md` 完整（§6 十三维无待填）且 task_id 与 `.gate/task.json` 一致；否则阻断。
- 文档/配置类改动放行。

绕过：仅 `git commit --no-verify` 或环境变量 `DSH_GATE_BYPASS=1`；后者会写 `.gate/precommit-bypass.log`，留痕可审计。
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from frontend_parity import audit_problems

FRONTEND_PREFIXES = ("static/", "templates/", "public/", "frontend/", "assets/")
FRONTEND_SUFFIXES = (".js", ".mjs", ".css", ".vue", ".html", ".ts", ".tsx")
CODE_PREFIXES = ("apps/", "config/", "scripts/", "src/")
DOC_PREFIXES = ("docs/", ".gate/", "wf-development/", "inbound/")


def git(*args: str, cwd: Path) -> str:
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True).stdout


def staged_files(root: Path) -> list[str]:
    out = git("diff", "--cached", "--name-only", "--diff-filter=ACMR", cwd=root)
    return [line.strip().replace("\\", "/") for line in out.splitlines() if line.strip()]


def classify(files: list[str]) -> tuple[list[str], list[str]]:
    frontend, code = [], []
    for name in files:
        lower = name.lower()
        if lower.startswith(DOC_PREFIXES):
            continue
        if lower.startswith(FRONTEND_PREFIXES) or lower.endswith(FRONTEND_SUFFIXES):
            frontend.append(name)
        elif lower.startswith(CODE_PREFIXES) or lower.endswith(".py"):
            code.append(name)
    return frontend, code


def newest_mtime(root: Path, files: list[str]) -> float:
    stamps = []
    for name in files:
        path = root / name
        if path.is_file():
            stamps.append(path.stat().st_mtime)
    return max(stamps) if stamps else 0.0


def level_of(root: Path) -> str:
    for candidate in (root / ".gate" / "task.json", root / ".gate" / "acceptance.yaml"):
        if not candidate.is_file():
            continue
        try:
            text = candidate.read_text(encoding="utf-8-sig")
        except OSError:
            continue
        for token in ("L0", "L1", "L2", "L3"):
            if f'"{token}"' in text or f": {token}" in text or f"level: {token}" in text:
                return token
    return "L2"


def tier_of(root: Path) -> str:
    path = root / ".gate" / "frontend" / "tier.json"
    if path.is_file():
        try:
            tier = str(json.loads(path.read_text(encoding="utf-8-sig")).get("tier", "")).strip().upper()
        except Exception:  # noqa: BLE001
            tier = ""
        if tier in ("A", "B", "C"):
            return tier
    return "A"


def check_frontend(root: Path, frontend: list[str]) -> list[str]:
    receipt = root / ".gate" / "frontend" / "gate.json"
    if not receipt.is_file():
        return [
            "前端改动缺少实施出口回执 .gate/frontend/gate.json；"
            "先跑：python wf-development/verify/tools/frontend_parity.py "
            "--evidence-dir .gate/frontend --require-prototype --require-tier "
            "--require-generated --require-matrix-routes --require-audit --write .gate/frontend/gate.json"
        ]
    try:
        data = json.loads(receipt.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001
        return [f"gate.json 不可解析: {exc}"]
    if not data.get("ok"):
        return [f"前端门未通过（gate.json ok=false）：{data.get('problems', [])[:3]}"]
    newest = newest_mtime(root, frontend)
    if receipt.stat().st_mtime + 1 < newest:
        return ["gate.json 早于本轮前端改动：改完前端后必须重跑门禁再提交"]
    if tier_of(root) != "C":
        audit_problems_list = audit_problems(root / ".gate" / "frontend")
        if audit_problems_list:
            return ["界面完善审计未通过：" + "；".join(audit_problems_list[:4])]
        audit_path = root / ".gate" / "frontend" / "ui-audit.md"
        if audit_path.is_file() and audit_path.stat().st_mtime + 1 < newest:
            return ["ui-audit.md 早于本轮前端改动：改完 UI 后必须重新审计再提交"]
    return []


def check_plan_coverage(root: Path) -> list[str]:
    path = root / ".gate" / "plan-coverage.md"
    if not path.is_file():
        return ["缺 .gate/plan-coverage.md（L2+ 代码改动须有方案覆盖矩阵，含 §6 企业级十三维）"]
    text = path.read_text(encoding="utf-8", errors="ignore")
    problems = []
    if "## 6." not in text:
        problems.append("plan-coverage.md 缺 §6 企业级完整性（按 implementation-quality §7 填写）")
    section = text.split("## 6.", 1)[1] if "## 6." in text else ""
    if "待填" in section or "未覆盖" in section:
        problems.append("plan-coverage.md §6 仍有 待填/未覆盖 行")
    task = root / ".gate" / "task.json"
    if task.is_file():
        try:
            task_id = str(json.loads(task.read_text(encoding="utf-8-sig")).get("task_id", "")).strip()
        except Exception:  # noqa: BLE001
            task_id = ""
        if task_id and f"task_id: {task_id}" not in text:
            problems.append(f"plan-coverage.md 的 task_id 与 .gate/task.json({task_id}) 不一致")
    return problems


def main() -> int:
    root = Path.cwd()
    for index, arg in enumerate(sys.argv[1:]):
        if arg == "--project-root" and index + 2 <= len(sys.argv) - 1:
            root = Path(sys.argv[index + 2]).resolve()

    bypass = os.environ.get("DSH_GATE_BYPASS") == "1"
    files = staged_files(root)
    if not files:
        return 0
    frontend, code = classify(files)
    problems: list[str] = []
    if frontend:
        problems.extend(check_frontend(root, frontend))
    if code and level_of(root) in ("L2", "L3"):
        problems.extend(check_plan_coverage(root))

    if not problems:
        return 0

    if bypass:
        log = root / ".gate" / "precommit-bypass.log"
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open("a", encoding="utf-8") as handle:
            handle.write(f"{datetime.now(timezone.utc).isoformat()} bypassed: {problems}\n")
        print("PRECOMMIT: 已按 DSH_GATE_BYPASS=1 绕过（已留痕 .gate/precommit-bypass.log）")
        return 0

    print("PRECOMMIT BLOCKED（规则：frontend-gate §2.5 实施出口机检 / global-rules §9 交付口径）")
    for item in problems:
        print(f"- {item}")
    print("修好后重新 git add 并提交；确需绕过用 DSH_GATE_BYPASS=1（会留痕）。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
