#!/usr/bin/env python3
"""Lean completion gate for the dev workflow.

Design goals:
- The spec package is read-only. Runtime state lives in <project>/.gate/; task state is archived under .gate/archive/<task>/.
- A gate result must belong to the current task, not a previous task or another package.
- Evidence must exist; stale screenshots/acceptance/review/coverage/tier/reports/回执 must not turn into COMPLETE.
- No code change => NOT_VERIFIED, not COMPLETE. Dry-run => DRY_RUN, never COMPLETE.

Usage:
  python gate.py --package-root <wf-development> --project-root <project> [options]

Options:
  --mode auto|frontend                    default auto
  --acceptance <file>                     acceptance checklist (md/yaml/json); relative to project root
  --task-id <id>                          current task id (also stored by --start-task)
  --start-task <id>                       write .gate/task.json (task_id/started_at/base_commit) and exit
  --json                                  print JSON summary
  --dry-run                               select checks only; verdict=DRY_RUN; never writes
  --reset-attempts                        clear per-check failure budget (after changing approach)
  --allow-missing-acceptance              L0 bootstrap only; L1+ is always blocked

Notes:
  - StartTask freezes base_commit; changed_files = diff(base)..工作区 + untracked（中途 commit 不丢任务窗口）。
  - 定向：profile 的 lint_scoped/test_scoped 含 {files} 才注入变更列表；否则跑全仓命令，检查 id 为 project-*。
  - L1 未配 test_scoped 且有 smoke → 只跑 smoke（不跑全仓 test）；全量 test 留 L2+/发布/L3。
  - L1 未配 e2e_scoped → 不跑全量 e2e；前端证据（capture/parity/design-qa/console）不降。
  - 同一检查连续失败 2 次 → STOP，不自动重跑；--reset-attempts 仅换路径后用。
  - shared_globs（profile）命中的文件改动须在验收清单写 impact_map（调用方/依赖模块+回归集）。

Exit: 0 = COMPLETE, 1 = PARTIAL/BLOCKED/NOT_VERIFIED/DRY_RUN, 2 = usage/config error.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from frontend_parity import validate as validate_frontend_parity  # noqa: E402
from plan_coverage import validate as validate_plan_coverage  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

PACKAGE_NAME = "wf-development"
RECEIPT_DIR = Path(".gate") / PACKAGE_NAME

def default_project_root(package_root: Path) -> Path:
    """Walk up to the project root marked by activeContext.md."""
    for p in (package_root, *package_root.parents):
        if (p / "activeContext.md").is_file():
            return p
    return package_root.parent
FRONTEND_GLOBS = (
    ".tsx", ".jsx", ".vue", ".svelte", ".css", ".scss", ".less", ".html", ".htm",
    "/pages/", "/components/", "/views/", "/templates/", "/layouts/",
    "static/", "/static/", "public/", "/public/", "frontend/", "/frontend/",
    "assets/", "/assets/", "workbench/",
)
API_GLOBS = ("/api/", "/controllers/", "/handlers/", "/routes/", "controller", "routes.", "handler.", ".proto", "openapi", "swagger")
DB_GLOBS = ("/migrations/", ".sql")
DATA_MODEL_GLOBS = ("/models/", "/entities/", "schema.prisma", "models.py", "entity.")
AUTH_PATH_RE = re.compile(
    r"(^|[/_.-])(auth|login|permission|permissions|rbac|acl|role|roles|payment|pay|security)([/_.-]|$)",
    re.I,
)
DOC_EXTS = (".md", ".txt")
EXCLUDE_PARTS = {
    ".git", ".gate", "node_modules", "__pycache__", ".venv", "venv", "dist", "build",
    "coverage", "html-report", "test-results", "_archive", ".draft", "verify/.state",
}
PATHISH = re.compile(r"(?:[A-Za-z]:[\\/]|\.{0,2}/|[\w.-]+\.(?:png|jpe?g|webp|gif|json|log|txt|md|ya?ml|xml|html?))", re.I)
COMMANDISH = re.compile(r"^(?:npm|npx|node|python|py|pytest|go|cargo|mvn|gradle|dotnet|git|powershell|pwsh|bash|sh)\b", re.I)


def _safe_task_name(task_id: str) -> str:
    safe = re.sub(r"[^0-9A-Za-z._-]+", "_", (task_id or "").strip()).strip("._-")
    return safe or datetime.now().strftime("%Y%m%d-%H%M%S")


def _read_task_id(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return ""
    m = re.search(r"(?im)^\s*task_id\s*[:：]\s*`?([^`\s|]+)", text)
    return m.group(1).strip().strip("`\"'") if m else ""


def _archive_file(path: Path, archive_root: Path, project_root: Path) -> int:
    try:
        dest = archive_root / path.relative_to(project_root)
        dest.parent.mkdir(parents=True, exist_ok=True)
        path.replace(dest)
        return 1
    except (OSError, ValueError):
        return 0


def archive_task_state(project_root: Path, task_id: str = "") -> int:
    """Archive task-scoped runtime on StartTask; never delete evidence.

    Keeps current-task acceptance/coverage (task_id matches), project-profile.json,
    logs/, prototype/, task.json and archive/. Moving review/coverage/acceptance/
    tier/reports prevents a new task from passing with stale artifacts.
    """
    archive_root = project_root / ".gate" / "archive" / _safe_task_name(task_id)
    moved = 0
    frontend = project_root / ".gate" / "frontend"
    if frontend.is_dir():
        for path in frontend.rglob("*"):
            if path.is_file():
                moved += _archive_file(path, archive_root, project_root)
        for path in sorted(frontend.rglob("*"), key=lambda p: len(p.parts), reverse=True):
            if path.is_dir():
                try:
                    path.rmdir()
                except OSError:
                    pass
    receipt_dir = project_root / ".gate" / PACKAGE_NAME
    if receipt_dir.is_dir():
        for path in receipt_dir.iterdir():
            if path.is_file():
                moved += _archive_file(path, archive_root, project_root)
    for name in ("acceptance.yaml", "plan-coverage.md"):
        path = project_root / ".gate" / name
        if path.is_file() and _read_task_id(path) != (task_id or "").strip():
            moved += _archive_file(path, archive_root, project_root)
    review = project_root / ".gate" / "review.md"
    if review.is_file():
        moved += _archive_file(review, archive_root, project_root)
    return moved


def run(cmd: str, cwd: Path, timeout: int = 600) -> dict[str, Any]:
    started = time.time()
    try:
        p = subprocess.run(
            cmd, cwd=str(cwd), shell=True, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout,
        )
        return {
            "command": cmd,
            "exit": p.returncode,
            "duration": round(time.time() - started, 2),
            "stdout_tail": (p.stdout or "").strip()[-4000:],
            "stderr_tail": (p.stderr or "").strip()[-4000:],
        }
    except subprocess.TimeoutExpired:
        return {"command": cmd, "exit": 124, "duration": round(time.time() - started, 2),
                "stdout_tail": "", "stderr_tail": f"TIMEOUT after {timeout}s"}
    except Exception as exc:
        return {"command": cmd, "exit": 125, "duration": round(time.time() - started, 2),
                "stdout_tail": "", "stderr_tail": f"EXEC_ERROR: {exc}"}


def git(project_root: Path, *args: str) -> str:
    try:
        p = subprocess.run(
            ["git", "-C", str(project_root), "-c", "core.quotepath=false", *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30,
        )
        return (p.stdout or "").strip() if p.returncode == 0 else ""
    except Exception:
        return ""


def git_z(project_root: Path, *args: str) -> list[str]:
    try:
        p = subprocess.run(
            ["git", "-C", str(project_root), "-c", "core.quotepath=false", *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30,
        )
        if p.returncode != 0:
            return []
        return [x for x in (p.stdout or "").split("\0") if x.strip()]
    except Exception:
        return []


def _norm(rel: str) -> str:
    rel = rel.strip().strip('"').replace("\\", "/")
    while rel.startswith("./"):
        rel = rel[2:]
    return rel


def changed_files(project_root: Path, package_root: Path, base_commit: str = "") -> list[str]:
    """Files changed in the task window.

    If base_commit is set (from -StartTask), diff against that commit so mid-task
    commits still count. Otherwise fall back to HEAD (or working-tree-only).
    """
    try:
        package_rel = _norm(str(package_root.relative_to(project_root))) if package_root != project_root else ""
    except ValueError:
        package_rel = ""
    files: set[str] = set()
    base = (base_commit or "").strip()
    if base and git(project_root, "rev-parse", "--verify", f"{base}^{{commit}}"):
        # working tree (+ index content via WT) vs task base; covers commits after StartTask
        for raw in git_z(project_root, "diff", "--name-only", "-z", base):
            files.add(_norm(raw))
        # also names that differ only in index vs base when WT matches index oddly — rare; kept simple
        for raw in git_z(project_root, "diff", "--name-only", "-z", "--cached", base):
            files.add(_norm(raw))
    else:
        has_head = bool(git(project_root, "rev-parse", "--verify", "HEAD"))
        diff_args = ["diff", "--name-only", "-z", "HEAD"] if has_head else ["diff", "--name-only", "-z"]
        for raw in git_z(project_root, *diff_args):
            files.add(_norm(raw))
        if has_head:
            for raw in git_z(project_root, "diff", "--name-only", "-z", "--cached", "HEAD"):
                files.add(_norm(raw))
    for raw in git_z(project_root, "ls-files", "--others", "--exclude-standard", "-z"):
        files.add(_norm(raw))

    out: list[str] = []
    for rel in sorted(files):
        if not rel:
            continue
        parts = set(rel.split("/"))
        if parts & EXCLUDE_PARTS:
            continue
        if any(p in rel for p in ("/__pycache__/", "/node_modules/", "/.venv/", "/dist/", "/build/")):
            continue
        if rel.endswith((".pyc", ".pyo")):
            continue
        if rel == ".gate" or rel.startswith(".gate/"):
            continue
        if package_rel and (rel == package_rel or rel.startswith(package_rel + "/")):
            continue
        out.append(rel)
    return out


def compute_diff_hash(project_root: Path, files: list[str], base_commit: str = "") -> str:
    """代码/配置指纹：只覆盖非文档文件。

    收尾阶段的计划/activeContext/INDEX/报告回写不应使完成回执失效；代码、测试、
    配置、迁移等变更仍会使回执过期（claim_check 同时核对代码 mtime）。
    """
    code_files = [f for f in files if not f.lower().endswith(DOC_EXTS)]
    ref = ""
    if base_commit and git(project_root, "rev-parse", "--verify", f"{base_commit}^{{commit}}"):
        ref = base_commit
    elif git(project_root, "rev-parse", "--verify", "HEAD"):
        ref = "HEAD"
    diff_text = (
        git(project_root, "diff", ref, "--", *code_files)
        if ref and code_files else ""
    )
    parts = [diff_text, "\n".join(code_files)]
    # git diff 不覆盖未跟踪文件的内容：补内容哈希，防止改内容不改名时回执不失效。
    tracked = set(git_z(project_root, "ls-files", "-z"))
    for rel in code_files:
        if rel in tracked:
            continue
        full = project_root / rel
        try:
            if full.is_file():
                parts.append(rel + ":" + hashlib.sha256(full.read_bytes()).hexdigest())
        except OSError:
            parts.append(rel + ":unreadable")
    return hashlib.sha256("\n".join(parts).encode("utf-8", errors="replace")).hexdigest()[:16]


def classify(files: list[str], frontend_hint: bool = False) -> tuple[str, list[str]]:
    if not files:
        return "L0", ["none"]
    types: list[str] = []
    lower = [f.lower() for f in files]
    if all(f.endswith(DOC_EXTS) for f in lower):
        return "L0", ["docs"]
    frontend_globs = FRONTEND_GLOBS
    if frontend_hint:
        # 普通 .js/.ts 可能是后端；仅在项目档案声明了 frontend 时按前端处理。
        frontend_globs = FRONTEND_GLOBS + (".js", ".ts")
    if any(any(g in f for g in frontend_globs) for f in lower):
        types.append("frontend")
    if any(any(g in f for g in API_GLOBS) for f in lower):
        types.append("api")
    if any(any(g in f for g in DB_GLOBS) for f in lower):
        types.append("db")
    if any(any(g in f for g in DATA_MODEL_GLOBS) for f in lower):
        types.append("data_model")
    if any(AUTH_PATH_RE.search(f) for f in lower):
        types.append("auth_payment")
    if not types:
        types.append("code")

    level = "L0"
    if "auth_payment" in types or "db" in types:
        level = "L3"
    elif "api" in types or "data_model" in types or len(files) > 3:
        level = "L2"
    elif "frontend" in types or "code" in types:
        level = "L1"
    return level, types


def level_rank(level: str) -> int:
    return {"L0": 0, "L1": 1, "L2": 2, "L3": 3}.get((level or "").upper(), 0)


def max_level(a: str, b: str) -> str:
    return a if level_rank(a) >= level_rank(b) else b


def resolve_path(project_root: Path, raw: str) -> Path:
    p = Path(raw)
    return p if p.is_absolute() else (project_root / p)


def find_acceptance(project_root: Path, explicit: str | None) -> Path | None:
    if explicit:
        p = resolve_path(project_root, explicit)
        return p if p.is_file() else None
    p = project_root / ".gate" / "acceptance.yaml"
    return p if p.is_file() else None


def _iq_empty() -> dict[str, str]:
    return {
        "implement_preflight": "",
        "sc_trace": "",
        "impact_map": "",
        "cross_layer": "",
        "baseline_smoke": "",
    }


def _extract_iq_from_text(text: str) -> dict[str, str]:
    """Pull IQ fields from YAML-style keys or Markdown 实施预检 / SC 表."""
    out = _iq_empty()
    for key in ("implement_preflight", "sc_trace", "impact_map", "cross_layer", "baseline_smoke"):
        m = re.search(rf"(?im)^[ \t-]*{key}\s*[:：]\s*(.+)$", text)
        if m:
            out[key] = m.group(1).strip().strip("`\"'")
    if not out["implement_preflight"]:
        m = re.search(r"实施预检[^\n]*[:：]\s*(.+)", text)
        if m:
            body = m.group(1).strip()
            if body and not re.search(r"待填|待补|\{\.\.\.\}|\{命中", body):
                if re.search(r"(?i)^\s*na\b|不适用", body):
                    out["implement_preflight"] = body if re.match(r"(?i)^na\b", body) else f"na: {body}"
                else:
                    out["implement_preflight"] = "done"
    if not out["sc_trace"]:
        if re.search(r"(?m)^\|\s*SC-\d+\b", text):
            out["sc_trace"] = "done: SC table"
        elif re.search(r"(?:方案条款|SC)[^\n]{0,40}不适用", text):
            out["sc_trace"] = "na: 无行为变化"
    return out


def parse_acceptance(path: Path | None) -> dict[str, Any]:
    empty = {
        "items": [], "task_id": "", "level": "", "process": {}, "nfr": None,
        "scope_files": [], **_iq_empty(),
    }
    if path is None:
        return empty
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    if path.suffix.lower() in (".yaml", ".yml", ".json"):
        try:
            if path.suffix.lower() == ".json":
                data = json.loads(text)
            else:
                import yaml  # type: ignore
                data = yaml.safe_load(text)
        except Exception:
            return empty
        if not isinstance(data, dict):
            return empty
        items = data.get("acceptance", [])
        out: list[dict[str, str]] = []
        if isinstance(items, list):
            for i, item in enumerate(items, 1):
                if isinstance(item, dict):
                    out.append({
                        "id": str(item.get("id") or f"AC-{i:02d}"),
                        "statement": str(item.get("statement") or item.get("desc") or ""),
                        "check": str(item.get("check") or item.get("checks") or ""),
                        "evidence": str(item.get("evidence") or ""),
                        "result": str(item.get("result") or item.get("status") or ""),
                    })
        iq = _iq_empty()
        for key in iq:
            raw = data.get(key)
            if raw is not None and str(raw).strip():
                iq[key] = str(raw).strip()
        return {
            "items": out,
            "task_id": str(data.get("task_id") or ""),
            "level": str(data.get("level") or ""),
            "process": data.get("process") if isinstance(data.get("process"), dict) else {},
            "nfr": data.get("nfr") if isinstance(data.get("nfr"), dict) else None,
            "scope_files": [str(x) for x in data.get("scope_files", [])] if isinstance(data.get("scope_files"), list) else [],
            **iq,
        }

    # Markdown task card: one or more acceptance tables; L2+ should use YAML.
    rows: list[dict[str, str]] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip().startswith("|"):
            i += 1
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            i += 1
            continue
        header = " ".join(cells).lower()
        has_ac = "验收" in header or re.search(r"\bac\b", header) is not None
        has_check = "检查" in header or "check" in header or "证据" in header
        if not (has_ac and has_check):
            i += 1
            continue

        def col(*names: str) -> int | None:
            for idx, cell in enumerate(cells):
                low = cell.lower()
                if any(name.lower() in low for name in names):
                    return idx
            return None

        i_id = col("AC", "验收", "编号")
        i_judge = col("判定", "结果", "状态")
        i_check = col("检查", "验证", "方法")
        i_evidence = col("证据")
        i_id = 0 if i_id is None else i_id
        i_check = 2 if i_check is None else i_check
        i_evidence = 3 if i_evidence is None else i_evidence
        j = i + 2
        while j < len(lines) and lines[j].strip().startswith("|"):
            vals = [c.strip() for c in lines[j].strip().strip("|").split("|")]
            if vals and vals[i_id]:
                def at(idx: int | None) -> str:
                    return vals[idx] if idx is not None and idx < len(vals) else ""
                judge = at(i_judge)
                rows.append({
                    "id": at(i_id),
                    "statement": judge or at(i_check),
                    "check": at(i_check),
                    "evidence": at(i_evidence),
                    "result": judge,
                })
            j += 1
        i = j

    task_id = ""
    m = re.search(r"task_id\s*[:：]\s*([A-Za-z0-9._-]+)", text)
    if m:
        task_id = m.group(1)
    else:
        m = re.search(r"^###\s+(T-\d+)\b", text, re.M)
        if m:
            task_id = m.group(1)
    level = ""
    m = re.search(r"\bL([0-3])\b", text[:800])
    if m:
        level = f"L{m.group(1)}"
    process: dict[str, str] = {}
    for key, pattern in (
        ("review", r"(?:评审记录|review)\s*[:：]\s*`?([^`\n]+?)`?(?:\s|$)"),
        ("understanding", r"(?:理解包|需求理解)\s*[:：]\s*`?([^`\n]+?)`?(?:\s|$)"),
        ("design", r"(?:设计|方案)\s*[:：]\s*`?([^`\n]+?)`?(?:\s|$)"),
        ("security", r"(?:安全|security)\s*[:：]\s*`?([^`\n]+?)`?(?:\s|$)"),
        ("rollback", r"(?:回滚|rollback)\s*[:：]\s*`?([^`\n]+?)`?(?:\s|$)"),
    ):
        mm = re.search(pattern, text, re.I)
        if mm:
            process[key] = mm.group(1).strip()
    scope: list[str] = []
    for mm in re.finditer(r"改动范围[^\n:：]*[:：]\s*([^\n]+)", text):
        scope += [x.strip().strip("`") for x in re.split(r"[;,；、]", mm.group(1)) if x.strip()]
    scope = list(dict.fromkeys(scope))
    return {
        "items": rows, "task_id": task_id, "level": level, "process": process,
        "nfr": None, "scope_files": scope, **_extract_iq_from_text(text),
    }


def _evidence_tokens(raw: str) -> list[str]:
    return [x.strip().strip("`") for x in re.split(r"[;；,，]", raw or "") if x.strip()]


def check_acceptance(items: list[dict[str, str]], project_root: Path) -> dict[str, Any]:
    missing: list[str] = []
    duplicates: list[str] = []
    seen: set[str] = set()
    for item in items:
        item_id = item.get("id", "?")
        if item_id in seen:
            duplicates.append(item_id)
        seen.add(item_id)
        for key in ("id", "statement", "check", "evidence"):
            if not item.get(key) or item[key] in ("{…}", "…", "TBD", "待定"):
                missing.append(f"{item.get('id', '?')}: 缺少 {key}")
                break
        result = (item.get("result") or "").strip()
        if not result or result in ("{…}", "…", "TBD", "待定", "待填", "未判定"):
            missing.append(f"{item_id}: 缺判定结果（须写通过/失败/阻塞/未测+理由）")
        elif any(x in result.upper() for x in ("未通过", "不通过", "未验证", "待定", "TODO", "未完成", "FAIL", "BLOCKED")):
            missing.append(f"{item_id}: 判定未通过/未验证（{result}）")
        elif re.fullmatch(r"(?:通过|正常|成功|符合预期|无报错|看起来?对|ok|pass)[.。!！]*", result, re.I):
            # 「通过」可作判定列终态；但检查列须有可观测断言，禁检查/陈述也是空话
            check = (item.get("check") or item.get("statement") or "").strip()
            if not check or re.fullmatch(
                r"(?:通过|正常|成功|符合预期|无报错|看起来?对|ok|pass|已验证)[.。!！]*", check, re.I
            ):
                missing.append(f"{item_id}: 判定/检查过弱（须对照原文/AC 的可观测断言，禁仅「通过/正常」）")
        for token in _evidence_tokens(item.get("evidence", "")):
            if token in ("无", "—", "-", "TBD", "待补", "见日志"):
                missing.append(f"{item_id}: 证据不具体（{token}）")
                break
    return {"total": len(items), "covered": len(items) - len(missing), "missing": missing, "duplicates": duplicates}


def check_evidence(items: list[dict[str, str]], project_root: Path, task_started: str = "",
                   min_ts: float = 0.0) -> list[str]:
    """Evidence paths are verified after checks have run (screenshots may be produced by the gate)."""
    missing: list[str] = []
    started_ts = min_ts
    if not started_ts and task_started:
        try:
            started_ts = datetime.fromisoformat(task_started.replace("Z", "+00:00")).timestamp()
        except Exception:
            started_ts = 0.0
    for item in items:
        item_id = item.get("id", "?")
        for token in _evidence_tokens(item.get("evidence", "")):
            if COMMANDISH.match(token):
                continue
            if PATHISH.search(token):
                p = resolve_path(project_root, token)
                if not p.exists():
                    missing.append(f"{item_id}: 证据不存在 {token}")
                    break
                if started_ts and p.is_file() and p.stat().st_mtime < started_ts:
                    missing.append(f"{item_id}: 证据早于任务开始 {token}")
                    break
    return missing


def _path_exists(project_root: Path, raw: str) -> bool:
    raw = (raw or "").strip().strip("`")
    if not raw or raw in ("无", "—", "-", "不适用"):
        return False
    return resolve_path(project_root, raw).exists()


SC_TRACE_RE = re.compile(r"(?:SC\s*对账|SC\s*覆盖|方案条款对账|sc[_ -]?trace)", re.I)
SC_NEG_RE = re.compile(
    r"(?<!无)未覆盖|(?<!无)未通过|(?<!无)不通过|(?<!无)缺口\s*[:：]?\s*[1-9]|(?<!无)需修|部分覆盖|部分通过",
    re.I,
)
SC_POS_RE = re.compile(
    r"已覆盖|全部覆盖|全覆盖|无未覆盖|无缺口|未覆盖\s*[:：]?\s*(?:无|0)\b|缺口\s*[:：]?\s*(?:无|0)\b|覆盖\s*\d|\d+\s*/\s*\d+",
    re.I,
)


def _sc_values(text: str) -> list[str]:
    """Extract the value after an SC reconciliation marker, one per line."""
    lines = text.splitlines()
    values: list[str] = []
    for i, line in enumerate(lines):
        if not SC_TRACE_RE.search(line):
            continue
        value = re.sub(
            r".*?(?:SC\s*对账|SC\s*覆盖|方案条款对账|sc[_ -]?trace)\s*",
            "",
            line,
            count=1,
            flags=re.I,
        )
        value = value.strip().strip("`*_| ").lstrip("（(：:= |").strip()
        if not value and i + 1 < len(lines):
            value = lines[i + 1].strip().lstrip("-*| ").strip()
        values.append(value)
    return values


def _sc_reconciliation(text: str, has_code_change: bool) -> tuple[bool, str]:
    """SC 对账 must state a positive result; explicit gaps or na-with-code are blocked."""
    values = _sc_values(text)
    if not values:
        return False, "评审记录缺少 SC 对账（或 na）"
    seen_ok = False
    for value in values:
        # 评审记录里若粘了技能模板的枚举（已覆盖/未覆盖/不适用+依据），不当作实际对账。
        if re.search(r"已覆盖\s*/\s*未覆盖|未覆盖\s*/\s*不适用", value):
            continue
        low = value.lower().lstrip("（(= |").strip()
        if low.startswith("na") or low.startswith("不适用"):
            if has_code_change:
                return False, "有代码变更时 SC 对账不得 na/不适用"
            seen_ok = True
            continue
        clean = re.sub(r"(未覆盖|缺口)\s*[:：]?\s*(?:无|0)\b", r"无\1", value)
        if SC_NEG_RE.search(clean):
            return False, f"SC 对账含未覆盖/缺口/需修：{value[:40]}"
        if SC_POS_RE.search(clean) or re.search(r"通过|pass", clean, re.I):
            seen_ok = True
    if seen_ok:
        return True, ""
    return False, "SC 对账未给出覆盖结论（须已覆盖/未覆盖/na）"


def check_process(meta: dict[str, Any], level: str, project_root: Path, files: list[str],
                  task_started: str = "") -> dict[str, Any]:
    missing: list[str] = []
    warnings: list[str] = []
    code_files = [f for f in files if not f.lower().endswith(DOC_EXTS)]
    scope = meta.get("scope_files") or []
    if scope:
        normalized = {_norm(str(x)) for x in scope}
        for rel in code_files:
            if not any(rel == s or rel.startswith(s.rstrip("/") + "/") for s in normalized):
                (missing if level_rank(level) >= 2 else warnings).append(f"改动超出声明范围：{rel}")
                break
    elif code_files and level_rank(level) >= 2:
        missing.append("L2+ 有代码变更须声明改动范围（scope_files/改动范围）")
    elif code_files:
        warnings.append("未声明改动范围（scope_files/改动范围）")
    if level_rank(level) < 2:
        return {"missing": missing, "warnings": warnings}
    process = meta.get("process") or {}
    if not isinstance(process, dict):
        process = {}

    review = process.get("review", "")
    if not review:
        missing.append("L2+ 缺少独立评审记录（process.review）")
    elif not _path_exists(project_root, review):
        missing.append(f"评审记录不存在：{review}")
    else:
        review_path = resolve_path(project_root, review)
        if _older_than(review_path, _parse_iso_mtime(task_started)):
            missing.append(f"评审记录早于本轮任务开始：{review}")
        text = review_path.read_text(encoding="utf-8-sig", errors="replace")
        verdict_match = re.search(r"verdict\s*[:：=]\s*([^\n|]+)", text, re.I)
        if verdict_match:
            verdict = verdict_match.group(1).strip().strip("`*_ ")
            positive = re.match(r"^(通过|PASS|APPROVED)(?:\s|$|[（(])", verdict, re.I)
            negative = re.search(r"(需修|不通过|未通过|部分通过)", verdict, re.I)
            if not positive or negative:
                missing.append(f"评审 verdict 非通过：{verdict[:40]}")
        else:
            # No explicit verdict: accept a clear pass conclusion, but never a negation/partial.
            if re.search(r"(未通过|不通过|部分通过|需修|驳回|CHANGES_REQUESTED|REJECT)", text, re.I):
                missing.append("评审记录含未通过/需修结论，不能视为通过")
            elif not re.search(r"(评审通过|结论\s*[:：]\s*通过|\bPASS\b|\bAPPROVED\b)", text, re.I):
                missing.append("评审记录未给出通过结论（需 verdict=通过/PASS/APPROVED）")
        rv = re.search(r"(?:reviewer|评审人)\s*[:：]\s*(\S+)", text, re.I)
        im = re.search(r"(?:implementer|实施人|作者)\s*[:：]\s*(\S+)", text, re.I)
        if not rv:
            missing.append("评审记录缺少 reviewer/评审人")
        if not im:
            missing.append("评审记录缺少 implementer/实施人")
        if rv and im and rv.group(1).strip() == im.group(1).strip():
            missing.append("评审人不能等于实施者")
        # L2+：须有 SC 对账（或 na）；与 code-review §4.0 / review.md 字段对齐，禁只勾 AC。
        # 内容也要看：自报“未覆盖/缺口/需修”或 L2+ 有代码却写 na → 不能算通过。
        sc_ok, sc_why = _sc_reconciliation(
            text, any(not f.lower().endswith(DOC_EXTS) for f in files)
        )
        if not sc_ok:
            missing.append(sc_why)

    for key, label in (("understanding", "需求理解包"), ("design", "方案/设计")):
        val = process.get(key, "")
        if val and not _path_exists(project_root, val):
            missing.append(f"{label}不存在：{val}")
        elif not val:
            if level_rank(level) >= 3:
                missing.append(f"L3 缺少{label}证据")
            else:
                warnings.append(f"未声明{label}路径")

    if level_rank(level) >= 3:
        for key, label in (("security", "安全扫描/评审"), ("rollback", "回滚演练/预案")):
            val = process.get(key, "")
            if not val:
                missing.append(f"L3 缺少{label}证据（process.{key}）")
            elif not _path_exists(project_root, val) and not COMMANDISH.match(val):
                missing.append(f"{label}证据不存在：{val}")
    return {"missing": missing, "warnings": warnings}


NFR_PATH_RE = re.compile(r"[^\s()（）,，;；]+\.(?:md|json|log|txt|ya?ml|png|jpe?g|csv|html?)", re.I)
NFR_METRIC_RE = re.compile(r"(p\d{2}|ms\b|SQL|KB|MB|GB|%|QPS|TPS|耗时|字节)", re.I)
NFR_WEAK_NA_RE = re.compile(r"^(?:无风险|已关注|无影响|不涉及|无|ok|n/?a)$", re.I)
NFR_SEC_NA_OK = re.compile(r"无鉴权|无登录|无权限|无上传|纯文案|无认证|无支付|无密钥")
NFR_PERF_NA_OK = re.compile(r"无列表|无导出|无批量|无查询|无聚合|纯文案|无运行时|无接口")
PERF_HINT_RE = re.compile(r"(?:list|export|batch|query|aggregat|/search|/report)", re.I)


def _shared_hits(files: list[str], profile: dict[str, Any]) -> list[str]:
    """Profile shared_globs 命中的文件（被多处引用的公共路径）。"""
    raw = profile.get("shared_globs") if isinstance(profile, dict) else None
    if not isinstance(raw, list):
        return []
    patterns = [str(p).strip().lower() for p in raw if str(p).strip()]
    if not patterns:
        return []
    return [f for f in files if any(fnmatch.fnmatch(f.replace("\\", "/").lower(), p) for p in patterns)]


def check_iq_fields(meta: dict[str, Any], level: str, files: list[str], docs_only: bool,
                    profile: dict[str, Any] | None = None) -> dict[str, Any]:
    """L1+ 有代码时硬拦 implement_preflight / sc_trace（DEV-IQ-09/12、DEV-VER-11）。

    profile.shared_globs 命中时另须 impact_map（共享/被引用面：调用方/依赖模块+回归集）。
    """
    missing: list[str] = []
    if level_rank(level) < 1 or docs_only or not files:
        return {"missing": missing}
    if not any(not f.lower().endswith(DOC_EXTS) for f in files):
        return {"missing": missing}

    pre = str(meta.get("implement_preflight") or "").strip()
    if not pre or pre.lower() == "missing":
        missing.append("有代码变更须写 implement_preflight=done|na（或 Markdown「实施预检」行）")
    else:
        m = re.match(r"^(done|na)\b\s*[:：]?\s*(.*)$", pre, re.I)
        if m:
            if m.group(1).lower() == "na" and len(m.group(2).strip()) < 2:
                missing.append("implement_preflight=na 需一句理由")
        elif not re.search(r"不适用|命中\s*=", pre):
            missing.append("implement_preflight 须为 done|na（或含命中=/不适用 的实施预检行）")

    sc = str(meta.get("sc_trace") or "").strip()
    if not sc or sc.lower() == "missing":
        missing.append("有代码变更须写 sc_trace（SC 表/路径/done，或 na+理由）")
    else:
        m = re.match(r"^(done|na)\b\s*[:：]?\s*(.*)$", sc, re.I)
        if m and m.group(1).lower() == "na" and len(m.group(2).strip()) < 2:
            missing.append("sc_trace=na 需一句理由")
        elif not m and not re.search(r"SC-\d+|方案条款|任务清单|开发卡", sc):
            # bare path or inline label still ok if it looks like a pointer
            if len(sc) < 4:
                missing.append("sc_trace 过短；须指向 SC 表或 na+理由")

    shared = _shared_hits([f for f in files if not f.lower().endswith(DOC_EXTS)], profile or {})
    if shared:
        impact = str(meta.get("impact_map") or "").strip()
        if not impact or impact.lower() == "missing":
            missing.append(
                "共享路径改动须写 impact_map（调用方/依赖模块+回归集，或 na+理由）："
                + ", ".join(shared[:3])
            )
        elif any(x in impact for x in ("{", "待填", "待补", "TBD")):
            missing.append("impact_map 仍为占位符/未填")
        else:
            m = re.match(r"^(done|na)\b\s*[:：]?\s*(.*)$", impact, re.I)
            if m and m.group(1).lower() == "na":
                if len(m.group(2).strip()) < 2:
                    missing.append("impact_map=na 需一句理由")
            elif m and m.group(1).lower() == "done":
                if len(m.group(2).strip()) < 4:
                    missing.append("impact_map=done 需列调用方/依赖模块与回归集")
            elif not m and len(impact) < 6:
                missing.append("impact_map 过短：须列调用方/依赖模块与回归集")
    return {"missing": missing}


def check_nfr(meta: dict[str, Any], level: str, project_root: Path,
              files: list[str] | None = None) -> dict[str, Any]:
    """L2+ 非功能影响与证据：nfr.security / nfr.performance（DEV-VER-19）。

    值必须是 `done: <证据>`（存在的路径、可复跑命令或可量化指标）或
    `na: <理由>`；缺省、空写、无依据的 done 均视为缺口。
    """
    missing: list[str] = []
    declared: dict[str, str] = {}
    files = files or []
    if level_rank(level) < 2:
        return {"missing": missing, "declared": declared}
    nfr = meta.get("nfr")
    if not isinstance(nfr, dict):
        return {"missing": ["L2+ 缺少 nfr（安全/性能影响结论；done 或 na+理由）"],
                "declared": declared}
    auth_hit = any(
        AUTH_PATH_RE.search(f.replace("\\", "/").lower())
        for f in files
        if not f.lower().endswith(DOC_EXTS)
    )
    perf_hit = any(
        PERF_HINT_RE.search(f.replace("\\", "/"))
        for f in files
        if not f.lower().endswith(DOC_EXTS)
    )
    for key, label in (("security", "安全"), ("performance", "性能")):
        raw = str(nfr.get(key) or "").strip()
        if not raw:
            missing.append(f"L2+ 缺少 nfr.{key}（{label}：done+证据 或 na+理由）")
            continue
        status_m = re.match(r"^(done|na)\b\s*[:：]?\s*(.*)$", raw, re.I)
        if not status_m:
            missing.append(f"nfr.{key} 格式无效（应为 done: … 或 na: …）")
            continue
        status, body = status_m.group(1).lower(), status_m.group(2).strip()
        declared[key] = status
        if status == "na":
            if len(body) < 4 or NFR_WEAK_NA_RE.match(body):
                missing.append(f"nfr.{key}=na 须写具体理由（禁「无风险/已关注」空话）")
            elif key == "security" and auth_hit and not NFR_SEC_NA_OK.search(body):
                missing.append("触及鉴权/支付路径时 nfr.security=na 须说明为何无安全面")
            elif key == "performance" and perf_hit and not NFR_PERF_NA_OK.search(body):
                missing.append("触及列表/导出/批量等路径时 nfr.performance=na 须说明为何无性能面")
            continue
        if not body:
            missing.append(f"nfr.{key}=done 需证据（路径/命令/指标）")
            continue
        paths = NFR_PATH_RE.findall(body)
        if paths:
            if not any(resolve_path(project_root, p).exists() for p in paths):
                missing.append(f"nfr.{key} 证据不存在：{paths[0]}")
            continue
        if not COMMANDISH.match(body) and not NFR_METRIC_RE.search(body):
            missing.append(f"nfr.{key}=done 需可复核证据（路径/命令/指标）")
    return {"missing": missing, "declared": declared}


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def check_docs(project_root: Path, files: list[str]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    broken_links: list[str] = []
    placeholders: list[str] = []
    for rel in files:
        if not rel.lower().endswith(DOC_EXTS):
            continue
        p = project_root / rel
        if not p.is_file():
            continue
        text = p.read_text(encoding="utf-8-sig", errors="replace")
        for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = m.group(1).split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if not (p.parent / target).exists() and not (project_root / target).exists():
                broken_links.append(f"{rel}: {target}")
        scan = strip_code(text)
        for m in re.finditer(r"(\{[^{}\n]{1,80}\}|TBD|TODO)", scan, re.I):
            snippet = m.group(1)
            line_start = scan.rfind("\n", 0, m.start()) + 1
            line_end = scan.find("\n", m.start())
            line = scan[line_start:line_end if line_end >= 0 else len(scan)]
            if not re.search(r"(责任人|owner|期限|due|截止)", line, re.I):
                placeholders.append(f"{rel}: {snippet}")
    results.append({"id": "docs-links", "status": "fail" if broken_links else "pass",
                    "detail": broken_links[:10] if broken_links else "no broken relative links"})
    results.append({"id": "docs-placeholders", "status": "fail" if placeholders else "pass",
                    "detail": placeholders[:10] if placeholders else "no unowned placeholders"})
    return results


def package_json_scripts(project_root: Path) -> dict[str, str]:
    p = project_root / "package.json"
    if not p.is_file():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8-sig"))
        return data.get("scripts", {}) if isinstance(data.get("scripts"), dict) else {}
    except Exception:
        return {}


def load_profile(project_root: Path) -> tuple[dict[str, Any], str]:
    p = project_root / ".gate" / "project-profile.json"
    if not p.is_file():
        return {}, ""
    try:
        data = json.loads(p.read_text(encoding="utf-8-sig"))
        return (data if isinstance(data, dict) else {}), ""
    except Exception as exc:
        return {}, f"project-profile.json 无法解析：{exc}"


def resolve_cmd(profile: dict[str, Any], scripts: dict[str, str], key: str) -> str | None:
    if key == "capture":
        frontend = profile.get("frontend")
        if isinstance(frontend, dict) and frontend.get("capture"):
            return str(frontend["capture"])
    if profile.get(key):
        return str(profile[key])
    mapping = {
        "build": ("build", "npm run build"),
        "lint": ("lint", "npm run lint"),
        "test": ("test", "npm test"),
        "smoke": ("test:smoke", "npm run test:smoke"),
        "e2e": ("test:e2e", "npm run test:e2e"),
        "security": ("security", "npm run security"),
        "integration": ("test:integration", "npm run test:integration"),
    }
    script, fallback = mapping.get(key, (None, None))
    if script and script in scripts:
        return fallback
    if key == "e2e" and (project_root_has_playwright(scripts)):
        return "npx playwright test"
    return None


def _files_for_scope(files: list[str], key: str) -> list[str]:
    """Pick paths suitable for lint/test injection (cap length for argv).

    超过 40 个匹配文件时返回空，调用方回退到全仓命令：宁可跑全仓，也不能只测前 40 个。
    """
    if key == "lint":
        exts = (".ts", ".tsx", ".js", ".jsx", ".vue", ".svelte", ".py", ".go", ".java", ".cs")
    elif key == "e2e":
        exts = (".ts", ".js", ".spec.ts", ".spec.js", ".feature")
    else:
        exts = (".ts", ".tsx", ".js", ".jsx", ".vue", ".py", ".go", ".java", ".cs")
    out: list[str] = []
    seen: set[str] = set()
    for f in files:
        fl = f.lower()
        if not any(fl.endswith(e) for e in exts):
            continue
        if f in seen:
            continue
        seen.add(f)
        out.append(f)
        if len(out) > 40:
            return []
    return out


def resolve_check_cmd(profile: dict[str, Any], scripts: dict[str, str], key: str,
                      files: list[str]) -> tuple[str | None, bool]:
    """Return (command, is_scoped). Scoped only when profile has *_scoped with {files}."""
    scoped_key = f"{key}_scoped"
    tmpl = profile.get(scoped_key)
    if isinstance(tmpl, str) and "{files}" in tmpl:
        scoped_files = _files_for_scope(files, key)
        if scoped_files:
            return tmpl.replace("{files}", " ".join(scoped_files)), True
        # template present but no matching files → fall through to project-wide
    return resolve_cmd(profile, scripts, key), False


def check_id_for(key: str, scoped: bool) -> str:
    if key == "test":
        return "targeted-test" if scoped else "project-test"
    if key == "lint":
        return "targeted-lint" if scoped else "project-lint"
    if key == "e2e":
        return "affected-e2e" if scoped else "project-e2e"
    return key


def project_root_has_playwright(scripts: dict[str, str]) -> bool:
    return any("playwright" in str(v).lower() for v in scripts.values())


def run_cmd_check(check_id: str, cmd: str | None, project_root: Path, timeout: int) -> dict[str, Any]:
    if not cmd:
        return {"id": check_id, "status": "skip", "detail": "no command configured"}
    r = run(cmd, project_root, timeout)
    return {"id": check_id, "status": "pass" if r["exit"] == 0 else "fail", "command": cmd, **r}


def _parse_iso_mtime(iso: str) -> float:
    if not iso:
        return 0.0
    try:
        s = iso.strip().replace("Z", "+00:00")
        return datetime.fromisoformat(s).timestamp()
    except Exception:
        return 0.0


def _older_than(path: Path, floor: float, tolerance: float = 2.0) -> bool:
    if not floor:
        return False
    try:
        return path.is_file() and path.stat().st_mtime + tolerance < floor
    except OSError:
        return False


def prototype_manifest(project_root: Path, profile: dict[str, Any]) -> dict[str, Any]:
    """Verify the prototype was decoded this round (source hash bound manifest)."""
    fe = profile.get("frontend", {}) if isinstance(profile.get("frontend"), dict) else {}
    raw = str(fe.get("prototype") or "").strip()
    if not raw:
        return {"id": "prototype-manifest", "status": "warn", "detail": "未配置 frontend.prototype"}
    proto = resolve_path(project_root, raw)
    if not proto.is_file():
        return {"id": "prototype-manifest", "status": "blocked", "detail": f"原型不存在: {raw}"}
    manifest_path = resolve_path(
        project_root, str(fe.get("prototypeManifest") or ".gate/prototype/prototype.json")
    )
    if not manifest_path.is_file():
        return {"id": "prototype-manifest", "status": "blocked",
                "detail": "缺少 prototype.json：先跑 rules/tools/extract_prototype_modules.py <原型> .gate/prototype"}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return {"id": "prototype-manifest", "status": "blocked", "detail": f"prototype.json 不可解析: {exc}"}
    digest = hashlib.sha256(proto.read_bytes()).hexdigest()
    recorded = str(manifest.get("source_sha256") or "").lower()
    modules = manifest.get("modules") or []
    if recorded != digest:
        return {"id": "prototype-manifest", "status": "blocked",
                "detail": "prototype.json 的 source_sha256 与当前原型不一致（原型换了/未重新解码）"}
    return {"id": "prototype-manifest", "status": "pass",
            "detail": f"modules={len(modules)} sha={digest[:12]}"}


def frontend_tier(evidence_dir: Path, fe: dict[str, Any], not_before: float = 0.0) -> str:
    """读取证据分级：.gate/frontend/tier.json（A/B/C），缺省 A（兼容旧行为）。

    早于本轮任务的 tier 不读（按 A 校验），避免上一任务的 C 级降级证据漏到新任务。
    """
    tier_file = evidence_dir / "tier.json"
    tier = ""
    if tier_file.is_file() and not _older_than(tier_file, not_before):
        try:
            data = json.loads(tier_file.read_text(encoding="utf-8-sig")) or {}
            tier = str(data.get("tier", "")).strip().upper()
        except Exception:
            tier = ""
    if tier not in ("A", "B", "C"):
        tier = str(fe.get("evidenceTier", "A")).strip().upper()
    return tier if tier in ("A", "B", "C") else "A"


def frontend_evidence(project_root: Path, profile: dict[str, Any], level: str,
                      freshness_floor: float, task_started_at: str = "",
                      base_commit: str = "", require_generated: bool = False) -> dict[str, Any]:
    fe = profile.get("frontend", {}) if isinstance(profile.get("frontend"), dict) else {}
    evidence_dir = resolve_path(project_root, str(fe.get("evidenceDir", ".gate/frontend")))
    if not evidence_dir.is_dir():
        return {"id": "frontend-evidence", "status": "blocked", "detail": f"missing {evidence_dir}"}
    tier = frontend_tier(evidence_dir, fe, _parse_iso_mtime(task_started_at))
    if tier == "C":
        routes = []
        route_file = evidence_dir / "route-coverage.json"
        if route_file.is_file():
            try:
                data = json.loads(route_file.read_text(encoding="utf-8-sig"))
                routes = data if isinstance(data, list) else (data.get("routes") or [])
            except Exception:
                routes = []
        if level_rank(level) >= 2 or len(routes) > 1:
            tier = "A"
            problems_tier = "tier=C 与 L2+/多路由不符，按 A 校验"
        else:
            problems_tier = ""
    else:
        problems_tier = ""
    images = [p for p in evidence_dir.rglob("*") if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")]
    qa = evidence_dir / "design-qa.md"
    problems: list[str] = []
    if problems_tier:
        problems.append(problems_tier)
    min_images = 1 if tier == "C" else 2
    if len(images) < min_images:
        problems.append(f"only {len(images)} screenshot(s); need >={min_images} (tier {tier})")
    names = " ".join(p.name.lower() for p in images)
    if not any(x in names for x in ("desktop", "1280", "1440")):
        problems.append("缺少桌面截图（文件名含 desktop/1280/1440）")
    if tier != "C" and not any(x in names for x in ("mobile", "360", "375", "390")):
        problems.append("缺少移动截图（文件名含 mobile/360/375/390）")
    floor = max(freshness_floor or 0.0, _parse_iso_mtime(task_started_at))
    if floor:
        stale = [p.name for p in images if p.stat().st_mtime + 1 < floor]
        if stale:
            label = "任务开始/验收清单"
            problems.append(f"截图早于本轮{label}：{stale[:3]}")
    results_json = evidence_dir / "playwright-results.json"
    if results_json.is_file():
        if _older_than(results_json, freshness_floor):
            problems.append("playwright-results.json 早于本轮（重新执行）")
        else:
            try:
                stats = (json.loads(results_json.read_text(encoding="utf-8-sig")) or {}).get("stats", {})
                expected = int(stats.get("expected", 0) or 0)
                skipped = int(stats.get("skipped", 0) or 0)
                unexpected = int(stats.get("unexpected", 0) or 0)
                if unexpected:
                    problems.append(f"Playwright unexpected={unexpected}")
                if skipped and expected == 0:
                    problems.append("Playwright 全部 skipped（模板未适配或 APP_READY 未设置）")
            except Exception:
                problems.append("playwright-results.json 不可解析")

    # L1 includes interaction-honesty rows 14/20; L2+ all 20
    required = list(range(1, 21)) if level_rank(level) >= 2 else [1, 2, 3, 6, 7, 8, 9, 10, 14, 15, 16, 17, 18, 19, 20]
    if not qa.is_file():
        problems.append("missing design-qa.md")
    else:
        text = qa.read_text(encoding="utf-8-sig", errors="replace")
        rows: dict[int, tuple[str, str]] = {}
        for line in text.splitlines():
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not cells or not cells[0].isdigit():
                continue
            n = int(cells[0])
            if 1 <= n <= 20:
                rows[n] = (cells[2] if len(cells) > 2 else "", cells[3] if len(cells) > 3 else "")
        missing_rows = [n for n in required if n not in rows]
        if missing_rows:
            problems.append(f"design-qa.md 缺验收项: {missing_rows}")
        blank = [n for n in required if n in rows and not rows[n][0]]
        if blank:
            problems.append(f"design-qa.md 结果未填: {blank}")
        no_evidence = []
        for n in required:
            if n not in rows:
                continue
            result, evidence = rows[n]
            if not evidence or evidence in ("{…}", "…"):
                no_evidence.append(n)
                continue
            if "通过" in result:
                tokens = [t for t in _evidence_tokens(evidence) if PATHISH.search(t)]
                # 描述性证据（如“03/04 布局正常”）允许保留；只有显式路径不存在才阻断。
                if tokens and not any(resolve_path(evidence_dir, t).exists() or resolve_path(project_root, t).exists()
                                      for t in tokens):
                    no_evidence.append(n)
            elif "不适用" in result:
                if "依据" not in evidence and "原因" not in evidence and len(evidence) < 8:
                    no_evidence.append(n)
        if no_evidence:
            problems.append(f"design-qa.md 证据不具体/不存在: {no_evidence}")
        m = re.search(r"结论[：:]\s*([^\n]+)", text)
        conclusion = m.group(1).strip() if m else ""
        if not conclusion:
            problems.append("design-qa.md 缺少结论")
        elif "不通过" in conclusion:
            problems.append(f"design-qa.md 结论=不通过（{conclusion[:30]}）")
        elif "有条件" not in conclusion:
            bad = [n for n, (r, _) in rows.items() if "不通过" in r]
            if bad:
                problems.append(f"design-qa.md 存在不通过项 {bad} 但结论未列条件")

        if tier != "C" or fe.get("requireConsoleClean") or fe.get("requireNetworkCheck"):
            reports = list(evidence_dir.glob("*report*.json")) + list(evidence_dir.glob("*console*.json")) + list(evidence_dir.glob("*network*.json"))
            if not reports:
                problems.append("缺少 console/network 报告 JSON")
            else:
                fresh_reports = [rp for rp in reports if not _older_than(rp, freshness_floor)]
                if len(fresh_reports) != len(reports):
                    stale = [rp.name for rp in reports if rp not in fresh_reports]
                    problems.append(f"console/network 报告早于本轮：{stale[:3]}")
                for rp in fresh_reports[:3]:
                    try:
                        data = json.loads(rp.read_text(encoding="utf-8-sig"))
                    except Exception:
                        continue
                    for key in ("consoleErrors", "pageErrors", "failedRequests"):
                        val = data.get(key)
                        if isinstance(val, list) and val:
                            problems.append(f"{rp.name}: {key} 非空")

    require_parity = bool(fe.get("requireParity", level_rank(level) >= 1)) and tier != "C"
    if require_parity:
        parity_problems, parity_stats = validate_frontend_parity(
            evidence_dir, since=floor, base_commit=base_commit,
            require_matrix=bool(fe.get("requireParityMatrix", True)),
            require_generated=require_generated,
            require_matrix_routes=bool(fe.get("requireMatrixRoutes", False)),
        )
        problems.extend(parity_problems)
        if not parity_problems:
            problems_detail = (f"parity routes={parity_stats.get('routes')} "
                               f"menus={parity_stats.get('menus')} "
                               f"deep_links={parity_stats.get('deep_links')}")
        else:
            problems_detail = ""
    else:
        problems_detail = ""

    if tier == "A" and level_rank(level) <= 1:
        review_record = project_root / ".gate" / "review.md"
        if not review_record.is_file():
            problems.append("A 级前端缺独立评审记录 .gate/review.md")

    if problems:
        return {"id": "frontend-evidence", "status": "blocked", "detail": problems}
    detail = f"tier={tier} {len(images)} screenshots + design-qa.md"
    if problems_detail:
        detail += " + " + problems_detail
    return {"id": "frontend-evidence", "status": "pass", "detail": detail}


def write_receipt(project_root: Path, mode: str, data: dict[str, Any]) -> Path:
    out_dir = project_root / RECEIPT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{mode}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    out = out_dir / "completion.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


MAX_FAILED_ATTEMPTS = 2


def attempts_path(project_root: Path) -> Path:
    return project_root / RECEIPT_DIR / "attempts.json"


def load_attempts(project_root: Path, task_id: str) -> dict[str, Any]:
    p = attempts_path(project_root)
    if not p.is_file():
        return {"task_id": task_id, "checks": {}}
    try:
        data = json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception:
        return {"task_id": task_id, "checks": {}}
    if not isinstance(data, dict) or str(data.get("task_id") or "") != task_id:
        return {"task_id": task_id, "checks": {}}
    checks = data.get("checks")
    data["checks"] = checks if isinstance(checks, dict) else {}
    return data


def save_attempts(project_root: Path, data: dict[str, Any]) -> None:
    checks: dict[str, int] = {}
    for key, value in (data.get("checks") or {}).items():
        try:
            n = int(value)
        except (TypeError, ValueError):
            continue
        if n > 0:
            checks[str(key)] = n
    p = attempts_path(project_root)
    if not checks:
        try:
            p.unlink()
        except FileNotFoundError:
            pass
        return
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        json.dumps(
            {
                "task_id": data.get("task_id", ""),
                "checks": checks,
                "updated": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def code_mtime_floor(project_root: Path, files: list[str]) -> float:
    """本轮代码/配置的最新 mtime；截图与证据须晚于它（文档回写不算）。"""
    newest = 0.0
    for rel in files:
        if rel.lower().endswith(DOC_EXTS):
            continue
        p = project_root / rel
        try:
            if p.is_file():
                newest = max(newest, p.stat().st_mtime)
        except OSError:
            pass
    return newest


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package-root", default=str(Path(__file__).resolve().parents[2]))
    ap.add_argument("--project-root", default=None)
    ap.add_argument("--mode", choices=["auto", "frontend"], default="auto")
    ap.add_argument("--acceptance", default=None)
    ap.add_argument("--task-id", default="")
    ap.add_argument("--start-task", default="")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--reset-attempts", action="store_true")
    ap.add_argument("--allow-missing-acceptance", action="store_true")
    args = ap.parse_args()

    package_root = Path(args.package_root).resolve()
    project_root = Path(args.project_root).resolve() if args.project_root else default_project_root(package_root)
    if not (package_root / "AGENTS.md").is_file():
        print(f"PACKAGE_ROOT_INVALID: {package_root} (AGENTS.md not found)")
        return 2
    if project_root == package_root or package_root in project_root.parents:
        print("PROJECT_ROOT_INVALID: 项目根不能是规范包本身或在规范包内；运行态只写项目根 .gate/")
        return 2

    if args.start_task:
        if not args.start_task.strip():
            print("TASK_ID_REQUIRED: -StartTask 需要非空 TaskId")
            return 2
        task_file = project_root / ".gate" / "task.json"
        task_file.parent.mkdir(parents=True, exist_ok=True)
        cleared = archive_task_state(project_root, args.start_task)
        try:
            attempts_path(project_root).unlink()
        except FileNotFoundError:
            pass
        base_commit = git(project_root, "rev-parse", "HEAD") or ""
        payload = {
            "task_id": args.start_task,
            "started_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            "base_commit": base_commit or None,
        }
        task_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(
            f"task started: {args.start_task} base={base_commit or 'nogit'} "
            f"archived_files={cleared} -> {task_file}"
        )
        return 0

    task_file = project_root / ".gate" / "task.json"
    task_id = args.task_id
    task_started = ""
    base_commit = ""
    if task_file.is_file():
        try:
            task_data = json.loads(task_file.read_text(encoding="utf-8-sig"))
            task_started = str(task_data.get("started_at") or "")
            base_commit = str(task_data.get("base_commit") or "")
            if not task_id:
                task_id = str(task_data.get("task_id") or "")
            elif task_data.get("task_id") and task_data["task_id"] != task_id:
                print(f"TASK_MISMATCH: .gate/task.json={task_data['task_id']} != --task-id={task_id}")
                return 2
        except Exception as exc:
            print(f"TASK_FILE_INVALID: {exc}")
            return 2

    files = changed_files(project_root, package_root, base_commit=base_commit)
    profile, profile_error = load_profile(project_root)
    level, types = classify(files, frontend_hint=bool(profile.get("frontend")))
    if args.mode == "frontend":
        types = sorted(set(types + ["frontend"]))
        level = max_level(level, "L1")

    acceptance_path = find_acceptance(project_root, args.acceptance)
    meta = parse_acceptance(acceptance_path)
    level = max_level(level, str(meta.get("level") or "L0"))
    acceptance_mtime = acceptance_path.stat().st_mtime if acceptance_path and acceptance_path.is_file() else 0.0

    acc = check_acceptance(meta["items"], project_root)
    if task_id and meta.get("task_id") and str(meta["task_id"]).strip() != task_id:
        acc["missing"].append(f"验收清单 task_id={str(meta['task_id']).strip()} 与当前任务 {task_id} 不一致")
    if (level_rank(level) >= 2 and acceptance_path
            and acceptance_path.suffix.lower() in (".yaml", ".yml")
            and not str(meta.get("task_id") or "").strip()):
        acc["missing"].append("L2+ 验收清单缺 task_id（须与本轮 task.json 一致）")
    process = check_process(meta, level, project_root, files, task_started)
    docs_only = bool(files) and all(f.lower().endswith(DOC_EXTS) for f in files)
    freshness_floor = max(_parse_iso_mtime(task_started), code_mtime_floor(project_root, files))
    attempts: dict[str, Any] = {"task_id": task_id, "checks": {}}
    if not args.dry_run and task_id and files and not docs_only:
        if args.reset_attempts:
            save_attempts(project_root, {"task_id": task_id, "checks": {}})
        attempts = load_attempts(project_root, task_id)
        exhausted: list[str] = []
        for cid, n in (attempts.get("checks") or {}).items():
            try:
                if int(n) >= MAX_FAILED_ATTEMPTS:
                    exhausted.append(str(cid))
            except (TypeError, ValueError):
                continue
        if exhausted:
            print("RETRY_BUDGET_EXCEEDED: " + ", ".join(sorted(exhausted)) + " 已连续失败 2 次；停止自动重跑。")
            print("  换路径/缩小范围/请人确认后，加 -ResetAttempts 再跑；不得原样重复。")
            return 1
    nfr = check_nfr(meta, level, project_root, files)
    iq = check_iq_fields(meta, level, files, docs_only, profile)
    acceptance_unusable = acceptance_path is None or not meta["items"]
    if level_rank(level) >= 1 and not args.allow_missing_acceptance:
        if acceptance_unusable:
            acc = {"total": 0, "covered": 0, "duplicates": [],
                   "missing": ["缺少可解析验收清单；L1+ 须写 .gate/acceptance.yaml 或 --acceptance"]}
        elif acc.get("duplicates"):
            acc["missing"].append(f"验收清单 AC 重复：{', '.join(acc['duplicates'][:5])}")
    if args.allow_missing_acceptance and level_rank(level) >= 1:
        acc["missing"].append("--allow-missing-acceptance 仅允许 L0；L1+ 必须提供验收清单")
    if iq["missing"]:
        acc["missing"].extend(iq["missing"])
    bug_task_id = (task_id or str(meta.get("task_id") or "")).strip().upper()
    if bug_task_id.startswith("BUG-") and meta["items"]:
        blob = " ".join(f"{i.get('statement', '')} {i.get('check', '')}" for i in meta["items"])
        if not re.search(r"原单|复现|红证", blob):
            acc["missing"].append("缺陷修复验收须含原单复现/红证项")
        if not re.search(r"回归|同类", blob):
            acc["missing"].append("缺陷修复验收须含回归/同类路径项")
    if level_rank(level) >= 1 and not docs_only and not task_file.is_file():
        acc["missing"].append("有代码/配置变更须先 -StartTask 冻结任务窗口（.gate/task.json）")

    scripts = package_json_scripts(project_root)
    timeouts = profile.get("timeouts", {}) if isinstance(profile.get("timeouts"), dict) else {}
    checks: list[dict[str, Any]] = []

    def scoped_configured(key: str) -> bool:
        tmpl = profile.get(f"{key}_scoped")
        return isinstance(tmpl, str) and "{files}" in tmpl

    if not files:
        checks = []
    elif docs_only:
        checks += check_docs(project_root, files)
    else:
        smoke_cmd = resolve_cmd(profile, scripts, "smoke")
        l1 = level_rank(level) <= 1
        build_failed = False
        test_failed = False
        for key in ("build", "lint", "test", "smoke"):
            if key in ("test", "smoke") and build_failed:
                cid = check_id_for("test", scoped_configured("test")) if key == "test" else "smoke"
                checks.append({"id": cid, "status": "deferred",
                               "detail": "build 失败；跳过，修复后重跑门"})
                continue
            if key == "test":
                cmd, scoped = resolve_check_cmd(profile, scripts, "test", files)
                cid = check_id_for("test", scoped)
                if l1 and not scoped and smoke_cmd:
                    checks.append({"id": cid, "status": "deferred",
                                   "detail": "L1 未配 test_scoped：已跑 smoke + 验收证据；全量 test 留 L2+/发布"})
                    continue
            elif key == "lint":
                cmd, scoped = resolve_check_cmd(profile, scripts, "lint", files)
                cid = check_id_for("lint", scoped)
            else:
                cmd = resolve_cmd(profile, scripts, key)
                cid = key
            if args.dry_run:
                checks.append({"id": cid, "status": "dry-run", "command": cmd})
                continue
            res = run_cmd_check(cid, cmd, project_root, int(timeouts.get(key, 600)))
            checks.append(res)
            if key == "build" and res.get("status") == "fail":
                build_failed = True
            if key == "test" and res.get("status") == "fail":
                test_failed = True
        if "frontend" in types or args.mode == "frontend":
            if build_failed or test_failed:
                checks.append({"id": "frontend", "status": "deferred",
                               "detail": "build/test 失败；跳过 e2e/capture/前端证据，修复后重跑门"})
            else:
                e2e, e2e_scoped = resolve_check_cmd(profile, scripts, "e2e", files)
                e2e_id = check_id_for("e2e", e2e_scoped)
                if l1 and not e2e_scoped:
                    checks.append({"id": e2e_id, "status": "deferred",
                                   "detail": "L1 未配 e2e_scoped：不跑全量 e2e；前端证据仍必"})
                elif args.dry_run:
                    checks.append({"id": e2e_id, "status": "dry-run", "command": e2e})
                else:
                    checks.append(run_cmd_check(e2e_id, e2e, project_root, int(timeouts.get("e2e", 900))))
                fe = profile.get("frontend", {}) if isinstance(profile.get("frontend"), dict) else {}
                require_generated = bool(fe.get("requireGeneratedEvidence", level_rank(level) >= 2))
                capture = resolve_cmd(profile, scripts, "capture")
                if capture:
                    if args.dry_run:
                        checks.append({"id": "frontend-capture", "status": "dry-run", "command": capture})
                    else:
                        checks.append(run_cmd_check("frontend-capture", capture, project_root,
                                                    int(timeouts.get("capture", 900))))
                elif require_generated and level_rank(level) >= 2:
                    checks.append({
                        "id": "frontend-capture",
                        "status": "blocked",
                        "detail": "未配置 frontend.capture：L2+ 前端证据必须由 gate 调用的 capture 命令生成（参考 verify/frontend/capture_example.py）；手写 route-coverage/截图不作为证据",
                    })
                else:
                    checks.append({"id": "frontend-capture", "status": "warn",
                                   "detail": "未配置 frontend.capture，仅校验手写证据（L1 允许）"})
                checks.append(prototype_manifest(project_root, profile))
                checks.append(frontend_evidence(project_root, profile, level, freshness_floor,
                                                task_started, base_commit, require_generated))
        if level_rank(level) >= 2:
            heavy_blocked = build_failed or test_failed
            integration = resolve_cmd(profile, scripts, "integration")
            if integration:
                if heavy_blocked:
                    checks.append({"id": "integration", "status": "deferred",
                                   "detail": "build/test 失败；跳过集成/性能/安全命令"})
                else:
                    checks.append(run_cmd_check("integration", integration, project_root,
                                                int(timeouts.get("integration", 900))))
            problems, stats = validate_plan_coverage(project_root, level, files, task_id=task_id)
            checks.append({
                "id": "plan-coverage",
                "status": "blocked" if problems else "pass",
                "detail": "; ".join(problems[:5]) or f"{stats.get('rows', 0)} rows",
            })
            # 企业级基线：项目声明 perf/security 命令时，L2+ 一律执行；L3 仍须安全证据。
            # dry-run 只列出命令，不执行（避免误触发压测/扫描）。
            for key in ("perf", "security"):
                cmd = resolve_cmd(profile, scripts, key)
                if cmd:
                    if heavy_blocked:
                        checks.append({"id": key, "status": "deferred",
                                       "detail": "build/test 失败；跳过"})
                    elif args.dry_run:
                        checks.append({"id": key, "status": "dry-run", "command": cmd})
                    else:
                        checks.append(run_cmd_check(key, cmd, project_root, int(timeouts.get(key, 900))))
                elif key == "security" and level_rank(level) >= 3:
                    process_meta = meta.get("process") if isinstance(meta.get("process"), dict) else {}
                    if not process_meta.get("security"):
                        checks.append({"id": "security", "status": "blocked",
                                       "detail": "L3 需要 security 命令或 process.security 证据"})

    evidence_missing = (check_evidence(meta["items"], project_root, task_started, freshness_floor)
                        if meta["items"] else [])
    if evidence_missing:
        acc["missing"].extend(evidence_missing)

    if args.dry_run:
        verdict = "DRY_RUN"
        reasons = ["dry-run：未执行检查，不代表完成"]
        deferred: list[dict[str, Any]] = []
    else:
        failed = [c for c in checks if c.get("status") == "fail"]
        blocked = [c for c in checks if c.get("status") == "blocked"]
        skipped = [c for c in checks if c.get("status") == "skip"]
        deferred = [c for c in checks if c.get("status") == "deferred"]
        verdict = "COMPLETE"
        reasons: list[str] = []
        if not files:
            verdict = "NOT_VERIFIED"
            reasons.append("没有可验证的改动；空 diff 不代表完成")
        elif failed or blocked or acc["missing"] or process["missing"] or nfr["missing"] or profile_error:
            verdict = "BLOCKED"
        elif skipped:
            verdict = "PARTIAL"
            reasons.append(f"{len(skipped)} check(s) skipped")
        if level_rank(level) >= 1 and "docs" not in types and not any(c.get("status") == "pass" for c in checks):
            verdict = "BLOCKED"
            reasons.append("没有可执行检查；填写 .gate/project-profile.json 或项目命令")
        if acc["missing"]:
            reasons += acc["missing"][:5]
        if process["missing"]:
            reasons += process["missing"][:5]
        if nfr["missing"]:
            reasons += nfr["missing"][:5]
        if profile_error:
            reasons.append(profile_error)
        if failed:
            reasons += [f"{c['id']} failed" for c in failed]
        if blocked:
            reasons += [f"{c['id']} blocked: {c.get('detail', '')}" for c in blocked]
        if task_id and files and not docs_only and not args.dry_run:
            cur = dict(attempts.get("checks") or {})
            for c in checks:
                cid = str(c.get("id") or "")
                if not cid:
                    continue
                if c.get("status") == "pass":
                    cur.pop(cid, None)
                elif c.get("status") == "fail":
                    cur[cid] = int(cur.get(cid, 0)) + 1
            if verdict == "COMPLETE":
                cur = {}
            save_attempts(project_root, {"task_id": task_id, "checks": cur})

    diff_hash = compute_diff_hash(project_root, files, base_commit)
    commit = git(project_root, "rev-parse", "--short", "HEAD")
    gate_id = f"{commit or 'nogit'}-{diff_hash}"
    completion = {
        "gate_version": "2.3",
        "package": PACKAGE_NAME,
        "mode": args.mode,
        "gate_id": gate_id,
        "task_id": task_id or meta.get("task_id") or "",
        "task_started_at": task_started,
        "base_commit": base_commit or None,
        "verdict": verdict,
        "level": level,
        "change_types": types,
        "changed_files": files[:200],
        "changed_count": len(files),
        "acceptance": {"path": str(acceptance_path) if acceptance_path else None,
                       "mtime": acceptance_mtime, **acc},
        "process": {"missing": process["missing"], "warnings": process["warnings"]},
        "iq": {"implement_preflight": meta.get("implement_preflight") or "",
               "sc_trace": meta.get("sc_trace") or "",
               "missing": iq["missing"]},
        "nfr": nfr,
        "checks": checks,
        "deferred": [{"id": c.get("id"), "detail": c.get("detail", "")} for c in deferred],
        "blocked": reasons,
        "timestamp": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "commit": commit,
        "diff_hash": diff_hash,
    }

    if args.json:
        print(json.dumps(completion, ensure_ascii=False, indent=2))
    else:
        print("=== 完成门（开发规范）===")
        print(f"verdict: {verdict}")
        print(f"level: {level} | types: {', '.join(types)} | changed: {len(files)} file(s)")
        print(f"acceptance: {acc['covered']}/{acc['total']} covered")
        if level_rank(level) >= 2:
            declared = ", ".join(f"{k}={v}" for k, v in nfr["declared"].items()) or "missing"
            print(f"nfr: {declared}")
        print(f"checks: {sum(1 for c in checks if c.get('status') == 'pass')}/{len(checks)} pass")
        for c in checks:
            extra = c.get("command") or c.get("detail") or ""
            print(f"- {c['id']}: {c.get('status')} {extra}".rstrip())
        if deferred:
            print("deferred（按风险裁剪，不阻断 Claim）:")
            for c in deferred[:10]:
                print(f"  - {c.get('id')}: {c.get('detail', '')}")
        if reasons:
            print("blocked/notes:")
            for r in reasons[:10]:
                print(f"  - {r}")

    if args.dry_run:
        return 0
    out = write_receipt(project_root, args.mode, completion)
    print(f"written: {out}")
    return 0 if verdict == "COMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
