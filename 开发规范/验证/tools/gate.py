#!/usr/bin/env python3
"""Lean completion gate for the dev workflow.

Design goals:
- The spec package is read-only. Runtime state lives in <project>/.gate/开发规范/.
- A gate result must belong to the current task, not a previous task or another package.
- Evidence must exist; a stale screenshot/acceptance/回执 must not turn into COMPLETE.
- No code change => NOT_VERIFIED, not COMPLETE. Dry-run => DRY_RUN, never COMPLETE.

Usage:
  python gate.py --package-root <开发规范> --project-root <project> [options]

Options:
  --mode auto|frontend                    default auto
  --acceptance <file>                     acceptance checklist (md/yaml/json); relative to project root
  --task-id <id>                          current task id (also stored by --start-task)
  --start-task <id>                       write .gate/task.json and exit
  --json                                  print JSON summary
  --dry-run                               select checks only; verdict=DRY_RUN; never writes
  --allow-missing-acceptance              L0 bootstrap only; L1+ is always blocked

Exit: 0 = COMPLETE, 1 = PARTIAL/BLOCKED/NOT_VERIFIED/DRY_RUN, 2 = usage/config error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

PACKAGE_NAME = "开发规范"
RECEIPT_DIR = Path(".gate") / PACKAGE_NAME
FRONTEND_GLOBS = (
    ".tsx", ".jsx", ".vue", ".svelte", ".css", ".scss", ".less", ".html", ".htm",
    "/pages/", "/components/", "/views/", "/app/", "/templates/", "/layouts/",
)
API_GLOBS = ("/api/", "controller", ".proto", "openapi", "swagger")
DB_GLOBS = ("/migrations/", ".sql")
AUTH_GLOBS = ("/auth/", "/login/", "/payment/", "/pay/", "/security/", "/permission/", "/role/")
DOC_EXTS = (".md", ".txt")
EXCLUDE_PARTS = {
    ".git", ".gate", "node_modules", "__pycache__", ".venv", "venv", "dist", "build",
    "coverage", "html-report", "test-results", "_归档", ".draft", "验证/.state",
}
PATHISH = re.compile(r"(?:[A-Za-z]:[\\/]|\.{0,2}/|[\w.-]+\.(?:png|jpe?g|webp|gif|json|log|txt|md|ya?ml|xml|html?))", re.I)
COMMANDISH = re.compile(r"^(?:npm|npx|node|python|py|pytest|go|cargo|mvn|gradle|dotnet|git|powershell|pwsh|bash|sh)\b", re.I)


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


def changed_files(project_root: Path, package_root: Path) -> list[str]:
    try:
        package_rel = _norm(str(package_root.relative_to(project_root))) if package_root != project_root else ""
    except ValueError:
        package_rel = ""
    files: set[str] = set()
    has_head = bool(git(project_root, "rev-parse", "--verify", "HEAD"))
    diff_args = ["diff", "--name-only", "-z", "HEAD"] if has_head else ["diff", "--name-only", "-z"]
    for raw in git_z(project_root, *diff_args):
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


def classify(files: list[str]) -> tuple[str, list[str]]:
    if not files:
        return "L0", ["none"]
    types: list[str] = []
    lower = [f.lower() for f in files]
    if all(f.endswith(DOC_EXTS) for f in lower):
        types.append("docs")
    if any(any(g in f for g in FRONTEND_GLOBS) for f in lower):
        types.append("frontend")
    if any(any(g in f for g in API_GLOBS) for f in lower):
        types.append("api")
    if any(any(g in f for g in DB_GLOBS) for f in lower):
        types.append("db")
    if any(any(g in f for g in AUTH_GLOBS) for f in lower):
        types.append("auth_payment")
    if not types:
        types.append("code")

    level = "L0"
    if "auth_payment" in types or "db" in types:
        level = "L3"
    elif "api" in types or len(files) > 10:
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


def parse_acceptance(path: Path | None) -> dict[str, Any]:
    empty = {"items": [], "task_id": "", "level": "", "process": {}, "scope_files": []}
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
        return {
            "items": out,
            "task_id": str(data.get("task_id") or ""),
            "level": str(data.get("level") or ""),
            "process": data.get("process") if isinstance(data.get("process"), dict) else {},
            "scope_files": [str(x) for x in data.get("scope_files", [])] if isinstance(data.get("scope_files"), list) else [],
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
        j = i + 2
        while j < len(lines) and lines[j].strip().startswith("|"):
            vals = [c.strip() for c in lines[j].strip().strip("|").split("|")]
            if len(vals) >= 4 and vals[0]:
                rows.append({"id": vals[0], "statement": vals[1], "check": vals[2],
                             "evidence": vals[3], "result": vals[4] if len(vals) > 4 else ""})
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
    mm = re.search(r"改动范围[^\n:：]*[:：]\s*([^\n]+)", text)
    if mm:
        scope = [x.strip().strip("`") for x in re.split(r"[;,；、]", mm.group(1)) if x.strip()]
    return {"items": rows, "task_id": task_id, "level": level, "process": process, "scope_files": scope}


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
        if result and any(x in result for x in ("未通过", "未验证", "待定", "TODO", "未完成")):
            missing.append(f"{item_id}: 判定未通过/未验证（{result}）")
        for token in _evidence_tokens(item.get("evidence", "")):
            if token in ("无", "—", "-", "TBD", "待补", "见日志"):
                missing.append(f"{item_id}: 证据不具体（{token}）")
                break
    return {"total": len(items), "covered": len(items) - len(missing), "missing": missing, "duplicates": duplicates}


def check_evidence(items: list[dict[str, str]], project_root: Path) -> list[str]:
    """Evidence paths are verified after checks have run (screenshots may be produced by the gate)."""
    missing: list[str] = []
    for item in items:
        item_id = item.get("id", "?")
        for token in _evidence_tokens(item.get("evidence", "")):
            if COMMANDISH.match(token):
                continue
            if PATHISH.search(token) and not resolve_path(project_root, token).exists():
                missing.append(f"{item_id}: 证据不存在 {token}")
                break
    return missing


def _path_exists(project_root: Path, raw: str) -> bool:
    raw = (raw or "").strip().strip("`")
    if not raw or raw in ("无", "—", "-", "不适用"):
        return False
    return resolve_path(project_root, raw).exists()


def check_process(meta: dict[str, Any], level: str, project_root: Path, files: list[str]) -> dict[str, Any]:
    missing: list[str] = []
    warnings: list[str] = []
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
        text = resolve_path(project_root, review).read_text(encoding="utf-8-sig", errors="replace")
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

    scope = meta.get("scope_files") or []
    if scope:
        normalized = {_norm(str(x)) for x in scope}
        for rel in files:
            if rel.lower().endswith(DOC_EXTS):
                continue
            if not any(rel == s or rel.startswith(s.rstrip("/") + "/") for s in normalized):
                missing.append(f"改动超出声明范围：{rel}")
                break
    else:
        warnings.append("未声明改动范围（scope_files/改动范围）")
    return {"missing": missing, "warnings": warnings}


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


def project_root_has_playwright(scripts: dict[str, str]) -> bool:
    return any("playwright" in str(v).lower() for v in scripts.values())


def run_cmd_check(check_id: str, cmd: str | None, project_root: Path, timeout: int) -> dict[str, Any]:
    if not cmd:
        return {"id": check_id, "status": "skip", "detail": "no command configured"}
    r = run(cmd, project_root, timeout)
    return {"id": check_id, "status": "pass" if r["exit"] == 0 else "fail", "command": cmd, **r}


def frontend_evidence(project_root: Path, profile: dict[str, Any], level: str,
                      acceptance_mtime: float) -> dict[str, Any]:
    fe = profile.get("frontend", {}) if isinstance(profile.get("frontend"), dict) else {}
    evidence_dir = resolve_path(project_root, str(fe.get("evidenceDir", ".gate/frontend")))
    if not evidence_dir.is_dir():
        return {"id": "frontend-evidence", "status": "blocked", "detail": f"missing {evidence_dir}"}
    images = [p for p in evidence_dir.rglob("*") if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")]
    qa = evidence_dir / "design-qa.md"
    problems: list[str] = []
    if len(images) < 2:
        problems.append(f"only {len(images)} screenshot(s); need >=2")
    names = " ".join(p.name.lower() for p in images)
    if not any(x in names for x in ("desktop", "1280", "1440")):
        problems.append("缺少桌面截图（文件名含 desktop/1280/1440）")
    if not any(x in names for x in ("mobile", "360", "375", "390")):
        problems.append("缺少移动截图（文件名含 mobile/360/375/390）")
    if acceptance_mtime:
        stale = [p.name for p in images if p.stat().st_mtime + 1 < acceptance_mtime]
        if stale:
            problems.append(f"截图早于本轮验收清单：{stale[:3]}")
    results_json = evidence_dir / "playwright-results.json"
    if results_json.is_file():
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

    required = list(range(1, 16)) if level_rank(level) >= 2 else [1, 2, 3, 6, 7, 10, 15]
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
            if 1 <= n <= 15:
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

        if fe.get("requireConsoleClean") or fe.get("requireNetworkCheck"):
            reports = list(evidence_dir.glob("*report*.json")) + list(evidence_dir.glob("*console*.json")) + list(evidence_dir.glob("*network*.json"))
            if not reports:
                problems.append("缺少 console/network 报告 JSON")
            else:
                for rp in reports[:3]:
                    try:
                        data = json.loads(rp.read_text(encoding="utf-8-sig"))
                    except Exception:
                        continue
                    for key in ("consoleErrors", "pageErrors", "failedRequests"):
                        val = data.get(key)
                        if isinstance(val, list) and val:
                            problems.append(f"{rp.name}: {key} 非空")
    if problems:
        return {"id": "frontend-evidence", "status": "blocked", "detail": problems}
    return {"id": "frontend-evidence", "status": "pass", "detail": f"{len(images)} screenshots + design-qa.md"}


def write_receipt(project_root: Path, mode: str, data: dict[str, Any]) -> Path:
    out_dir = project_root / RECEIPT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{mode}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    out = out_dir / "completion.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package-root", default=str(Path(__file__).resolve().parents[2]))
    ap.add_argument("--project-root", default=str(Path(__file__).resolve().parents[3]))
    ap.add_argument("--mode", choices=["auto", "frontend"], default="auto")
    ap.add_argument("--acceptance", default=None)
    ap.add_argument("--task-id", default="")
    ap.add_argument("--start-task", default="")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--allow-missing-acceptance", action="store_true")
    args = ap.parse_args()

    package_root = Path(args.package_root).resolve()
    project_root = Path(args.project_root).resolve()
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
        task_file.write_text(json.dumps({"task_id": args.start_task,
                                         "started_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")},
                                        ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"task started: {args.start_task} -> {task_file}")
        return 0

    task_file = project_root / ".gate" / "task.json"
    task_id = args.task_id
    task_started = ""
    if task_file.is_file():
        try:
            task_data = json.loads(task_file.read_text(encoding="utf-8-sig"))
            task_started = str(task_data.get("started_at") or "")
            if not task_id:
                task_id = str(task_data.get("task_id") or "")
            elif task_data.get("task_id") and task_data["task_id"] != task_id:
                print(f"TASK_MISMATCH: .gate/task.json={task_data['task_id']} != --task-id={task_id}")
                return 2
        except Exception as exc:
            print(f"TASK_FILE_INVALID: {exc}")
            return 2

    files = changed_files(project_root, package_root)
    level, types = classify(files)
    if args.mode == "frontend":
        types = sorted(set(types + ["frontend"]))
        level = max_level(level, "L1")

    acceptance_path = find_acceptance(project_root, args.acceptance)
    meta = parse_acceptance(acceptance_path)
    level = max_level(level, str(meta.get("level") or "L0"))
    acceptance_mtime = acceptance_path.stat().st_mtime if acceptance_path and acceptance_path.is_file() else 0.0

    acc = check_acceptance(meta["items"], project_root)
    process = check_process(meta, level, project_root, files)
    docs_only = bool(files) and all(f.lower().endswith(DOC_EXTS) for f in files)
    acceptance_unusable = acceptance_path is None or not meta["items"]
    if level_rank(level) >= 1 and not args.allow_missing_acceptance:
        if acceptance_unusable:
            acc = {"total": 0, "covered": 0, "duplicates": [],
                   "missing": ["缺少可解析验收清单；L1+ 须写 .gate/acceptance.yaml 或 --acceptance"]}
        elif acc.get("duplicates"):
            acc["missing"].append(f"验收清单 AC 重复：{', '.join(acc['duplicates'][:5])}")
    if args.allow_missing_acceptance and level_rank(level) >= 1:
        acc["missing"].append("--allow-missing-acceptance 仅允许 L0；L1+ 必须提供验收清单")

    profile, profile_error = load_profile(project_root)
    scripts = package_json_scripts(project_root)
    timeouts = profile.get("timeouts", {}) if isinstance(profile.get("timeouts"), dict) else {}
    checks: list[dict[str, Any]] = []

    if not files:
        checks = []
    elif docs_only:
        checks += check_docs(project_root, files)
    else:
        for key, cid in (("build", "build"), ("lint", "lint"), ("test", "targeted-test"), ("smoke", "smoke")):
            cmd = resolve_cmd(profile, scripts, key)
            if args.dry_run:
                checks.append({"id": cid, "status": "dry-run", "command": cmd})
            else:
                checks.append(run_cmd_check(cid, cmd, project_root, int(timeouts.get(key, 600))))
        if "frontend" in types or args.mode == "frontend":
            e2e = resolve_cmd(profile, scripts, "e2e")
            if args.dry_run:
                checks.append({"id": "affected-e2e", "status": "dry-run", "command": e2e})
            else:
                checks.append(run_cmd_check("affected-e2e", e2e, project_root, int(timeouts.get("e2e", 900))))
                checks.append(frontend_evidence(project_root, profile, level, acceptance_mtime))
        if level_rank(level) >= 2:
            integration = resolve_cmd(profile, scripts, "integration")
            if integration:
                checks.append(run_cmd_check("integration", integration, project_root, int(timeouts.get("integration", 900))))
        if level_rank(level) >= 3:
            security = resolve_cmd(profile, scripts, "security")
            if security:
                checks.append(run_cmd_check("security", security, project_root, int(timeouts.get("security", 900))))
            elif not process.get("security"):
                checks.append({"id": "security", "status": "blocked", "detail": "L3 需要 security 命令或 process.security 证据"})

    evidence_missing = check_evidence(meta["items"], project_root) if meta["items"] else []
    if evidence_missing:
        acc["missing"].extend(evidence_missing)

    if args.dry_run:
        verdict = "DRY_RUN"
        reasons = ["dry-run：未执行检查，不代表完成"]
    else:
        applicable = [c for c in checks if c.get("status") not in ("skip", "dry-run")]
        failed = [c for c in checks if c.get("status") == "fail"]
        blocked = [c for c in checks if c.get("status") == "blocked"]
        skipped = [c for c in checks if c.get("status") == "skip"]
        verdict = "COMPLETE"
        reasons: list[str] = []
        if not files:
            verdict = "NOT_VERIFIED"
            reasons.append("没有可验证的改动；空 diff 不代表完成")
        elif failed or blocked or acc["missing"] or process["missing"] or profile_error:
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
        if profile_error:
            reasons.append(profile_error)
        if failed:
            reasons += [f"{c['id']} failed" for c in failed]
        if blocked:
            reasons += [f"{c['id']} blocked: {c.get('detail', '')}" for c in blocked]

    diff_text = git(project_root, "diff", "HEAD") if git(project_root, "rev-parse", "--verify", "HEAD") else ""
    diff_hash = hashlib.sha256((diff_text + "\n" + "\n".join(files)).encode("utf-8", errors="replace")).hexdigest()[:16]
    commit = git(project_root, "rev-parse", "--short", "HEAD")
    gate_id = f"{commit or 'nogit'}-{diff_hash}"
    completion = {
        "gate_version": "2.0",
        "package": PACKAGE_NAME,
        "mode": args.mode,
        "gate_id": gate_id,
        "task_id": task_id or meta.get("task_id") or "",
        "task_started_at": task_started,
        "verdict": verdict,
        "level": level,
        "change_types": types,
        "changed_files": files[:200],
        "changed_count": len(files),
        "acceptance": {"path": str(acceptance_path) if acceptance_path else None,
                       "mtime": acceptance_mtime, **acc},
        "process": {"missing": process["missing"], "warnings": process["warnings"]},
        "checks": checks,
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
        print(f"checks: {sum(1 for c in checks if c.get('status') == 'pass')}/{len(checks)} pass")
        for c in checks:
            extra = c.get("command") or c.get("detail") or ""
            print(f"- {c['id']}: {c.get('status')} {extra}".rstrip())
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
