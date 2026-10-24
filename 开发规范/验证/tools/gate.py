#!/usr/bin/env python3
"""Lean completion gate for the dev workflow.

Usage:
  python gate.py --package-root <开发规范> --project-root <project> [options]

Options:
  --mode auto|frontend                    default auto
  --acceptance <file>                     acceptance checklist (md/yaml/json)
  --json                                  print JSON summary
  --dry-run                               show selected checks only
  --allow-missing-acceptance              bootstrap only; never use for L1+

Exit: 0 = COMPLETE, 1 = PARTIAL/BLOCKED, 2 = usage/config error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
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

FRONTEND_GLOBS = (
    ".tsx", ".jsx", ".vue", ".svelte", ".css", ".scss", ".less", ".html", ".htm",
    "/pages/", "/components/", "/views/", "/app/", "/templates/", "/layouts/",
)
API_GLOBS = ("/api/", "controller", ".proto", "openapi", "swagger")
DB_GLOBS = ("/migrations/", ".sql")
AUTH_GLOBS = ("/auth/", "/login/", "/payment/", "/pay/", "/security/", "/permission/", "/role/")
DOC_EXTS = (".md", ".txt")


def run(cmd: str, cwd: Path, timeout: int = 600) -> dict[str, Any]:
    started = time.time()
    try:
        p = subprocess.run(
            cmd,
            cwd=str(cwd),
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        out = (p.stdout or "").strip()
        err = (p.stderr or "").strip()
        return {
            "command": cmd,
            "exit": p.returncode,
            "duration": round(time.time() - started, 2),
            "stdout_tail": out[-4000:],
            "stderr_tail": err[-4000:],
        }
    except subprocess.TimeoutExpired:
        return {
            "command": cmd,
            "exit": 124,
            "duration": round(time.time() - started, 2),
            "stdout_tail": "",
            "stderr_tail": f"TIMEOUT after {timeout}s",
        }
    except Exception as exc:
        return {
            "command": cmd,
            "exit": 125,
            "duration": round(time.time() - started, 2),
            "stdout_tail": "",
            "stderr_tail": f"EXEC_ERROR: {exc}",
        }


def git(project_root: Path, *args: str) -> str:
    try:
        p = subprocess.run(
            ["git", "-C", str(project_root), *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30,
        )
        return (p.stdout or "").strip() if p.returncode == 0 else ""
    except Exception:
        return ""


def changed_files(project_root: Path) -> list[str]:
    files: set[str] = set()
    for line in git(project_root, "diff", "--name-only", "HEAD").splitlines():
        if line.strip():
            files.add(line.strip().replace("\\", "/"))
    for line in git(project_root, "ls-files", "--others", "--exclude-standard").splitlines():
        if line.strip():
            files.add(line.strip().replace("\\", "/"))
    return sorted(files)


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
    if level == "L1" and len(files) <= 1:
        # single-file code change can still be L0 only if tiny; keep L1 for safety
        level = "L1"
    return level, types


def find_acceptance(project_root: Path, package_root: Path, explicit: str | None) -> Path | None:
    if explicit:
        p = Path(explicit)
        return p if p.is_file() else None
    # 运行态只认实例侧 .gate/；包内 .state 仅作遗留只读回退，勿再写入规范包。
    candidates: list[Path] = [
        project_root / ".gate" / "acceptance.yaml",
        package_root / "验证" / ".state" / "acceptance.yaml",
        project_root / "验证" / ".state" / "acceptance.yaml",
    ]
    for pattern in ("任务清单*.md", "开发卡*.md", "*开发卡*.md"):
        found = [
            p for p in project_root.rglob(pattern)
            if "_归档" not in p.parts and ".draft" not in p.parts
            and "模板" not in p.parts and "node_modules" not in p.parts
            and "template" not in p.name.lower()
        ]
        candidates += sorted(found, key=lambda p: p.stat().st_mtime, reverse=True)
    for p in candidates:
        if p.is_file():
            text = p.read_text(encoding="utf-8", errors="replace")
            if "验收清单" in text or p.suffix.lower() in (".yaml", ".yml", ".json"):
                return p
    return None


def parse_acceptance(path: Path | None) -> list[dict[str, str]]:
    if path is None:
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml  # type: ignore
            data = yaml.safe_load(text)
            items = data.get("acceptance", data) if isinstance(data, dict) else data
            out = []
            if isinstance(items, list):
                for i, item in enumerate(items, 1):
                    if isinstance(item, dict):
                        out.append({
                            "id": str(item.get("id") or f"AC-{i:02d}"),
                            "statement": str(item.get("statement") or item.get("desc") or ""),
                            "check": str(item.get("check") or item.get("checks") or ""),
                            "evidence": str(item.get("evidence") or ""),
                        })
            return out
        except Exception:
            return []
    if path.suffix.lower() == ".json":
        try:
            data = json.loads(text)
            items = data.get("acceptance", data) if isinstance(data, dict) else data
            out = []
            if isinstance(items, list):
                for i, item in enumerate(items, 1):
                    if isinstance(item, dict):
                        out.append({
                            "id": str(item.get("id") or f"AC-{i:02d}"),
                            "statement": str(item.get("statement") or item.get("desc") or ""),
                            "check": str(item.get("check") or item.get("checks") or ""),
                            "evidence": str(item.get("evidence") or ""),
                        })
            return out
        except Exception:
            return []
    # Markdown: collect every acceptance table (a task list may contain one per task).
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
        is_acceptance = has_ac and has_check
        if not is_acceptance:
            i += 1
            continue
        j = i + 2
        while j < len(lines) and lines[j].strip().startswith("|"):
            vals = [c.strip() for c in lines[j].strip().strip("|").split("|")]
            if len(vals) >= 4 and vals[0]:
                rows.append({
                    "id": vals[0], "statement": vals[1], "check": vals[2], "evidence": vals[3],
                })
            j += 1
        i = j
    return rows


def check_acceptance(items: list[dict[str, str]]) -> dict[str, Any]:
    missing = []
    seen: set[str] = set()
    duplicates: list[str] = []
    for item in items:
        item_id = item.get("id", "?")
        if item_id in seen:
            duplicates.append(item_id)
        seen.add(item_id)
        for key in ("id", "statement", "check", "evidence"):
            if not item.get(key) or item[key] in ("{…}", "…", "TBD", "待定"):
                missing.append(f"{item.get('id', '?')}: 缺少 {key}")
                break
    return {
        "total": len(items),
        "covered": len(items) - len(missing),
        "missing": missing,
        "duplicates": duplicates,
    }


def strip_code(text: str) -> str:
    """Remove fenced/inline code so API/JSON/Mermaid braces are not treated as placeholders."""
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
        text = p.read_text(encoding="utf-8", errors="replace")
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
    if broken_links:
        results.append({"id": "docs-links", "status": "fail", "detail": broken_links[:10]})
    else:
        results.append({"id": "docs-links", "status": "pass", "detail": "no broken relative links"})
    if placeholders:
        results.append({"id": "docs-placeholders", "status": "fail", "detail": placeholders[:10]})
    else:
        results.append({"id": "docs-placeholders", "status": "pass", "detail": "no unowned placeholders"})
    return results


def package_json_scripts(project_root: Path) -> dict[str, str]:
    p = project_root / "package.json"
    if not p.is_file():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return data.get("scripts", {}) if isinstance(data.get("scripts"), dict) else {}
    except Exception:
        return {}


def load_profile(project_root: Path, package_root: Path) -> dict[str, Any]:
    # 实例配置落项目根 .gate/；包内路径仅遗留只读回退（规范包零改动）。
    candidates = [
        project_root / ".gate" / "project-profile.json",
        package_root / "验证" / "project-profile.json",
    ]
    for p in candidates:
        if not p.is_file():
            continue
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
    return {}


def resolve_cmd(profile: dict[str, Any], scripts: dict[str, str], key: str) -> str | None:
    if profile.get(key):
        return str(profile[key])
    mapping = {
        "build": ("build", "npm run build"),
        "lint": ("lint", "npm run lint"),
        "test": ("test", "npm test -- --run"),
        "smoke": ("test:smoke", "npm run test:smoke"),
        "e2e": ("test:e2e", "npx playwright test"),
    }
    script, fallback = mapping.get(key, (None, None))
    if script and script in scripts:
        return fallback
    return None


def run_cmd_check(check_id: str, cmd: str | None, project_root: Path, timeout: int) -> dict[str, Any]:
    if not cmd:
        return {"id": check_id, "status": "skip", "detail": "no command configured"}
    r = run(cmd, project_root, timeout)
    status = "pass" if r["exit"] == 0 else "fail"
    return {"id": check_id, "status": status, "command": cmd, **r}


def resolve_project_path(project_root: Path, raw: str) -> Path:
    p = Path(raw)
    return p if p.is_absolute() else (project_root / p)


def frontend_evidence(project_root: Path, profile: dict[str, Any]) -> dict[str, Any]:
    fe = profile.get("frontend", {}) if isinstance(profile.get("frontend"), dict) else {}
    evidence_dir = resolve_project_path(project_root, str(fe.get("evidenceDir", ".gate/frontend")))
    if not evidence_dir.is_dir():
        return {"id": "frontend-evidence", "status": "blocked", "detail": f"missing {evidence_dir}"}
    images = [p for p in evidence_dir.rglob("*") if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")]
    qa = evidence_dir / "design-qa.md"
    problems = []
    if len(images) < 2:
        problems.append(f"only {len(images)} screenshot(s); need >=2")
    if not qa.is_file():
        problems.append("missing design-qa.md")
    else:
        text = qa.read_text(encoding="utf-8", errors="replace")
        rows: dict[int, tuple[str, str]] = {}
        for line in text.splitlines():
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not cells or not cells[0].isdigit():
                continue
            n = int(cells[0])
            if 1 <= n <= 15:
                result = cells[2] if len(cells) > 2 else ""
                evidence = cells[3] if len(cells) > 3 else ""
                rows[n] = (result, evidence)
        missing = [n for n in range(1, 16) if n not in rows]
        if missing:
            problems.append(f"design-qa.md 缺验收项: {missing}")
        blank = [n for n, (r, _) in rows.items() if not r or r in ("{…}", "…")]
        if blank:
            problems.append(f"design-qa.md 结果未填: {blank}")
        no_evidence = [n for n, (_, e) in rows.items() if not e or e in ("{…}", "…")]
        if no_evidence:
            problems.append(f"design-qa.md 证据未填: {no_evidence}")
        m = re.search(r"结论[：:]\s*([^\n]+)", text)
        conclusion = m.group(1).strip() if m else ""
        if not conclusion:
            problems.append("design-qa.md 缺少结论")
        elif "不通过" in conclusion:
            problems.append(f"design-qa.md 结论=不通过（{conclusion[:30]}）")
        else:
            bad_rows = [n for n, (r, _) in rows.items() if "不通过" in r]
            if bad_rows and "有条件" not in conclusion:
                problems.append(f"design-qa.md 存在不通过项 {bad_rows} 但结论未列条件")
    if problems:
        return {"id": "frontend-evidence", "status": "blocked", "detail": problems}
    return {"id": "frontend-evidence", "status": "pass", "detail": f"{len(images)} screenshots + design-qa.md"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package-root", default=str(Path(__file__).resolve().parents[2]))
    ap.add_argument("--project-root", default=str(Path(__file__).resolve().parents[3]))
    ap.add_argument("--mode", choices=["auto", "frontend"], default="auto")
    ap.add_argument("--acceptance", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--allow-missing-acceptance", action="store_true")
    args = ap.parse_args()

    package_root = Path(args.package_root).resolve()
    project_root = Path(args.project_root).resolve()
    if not (package_root / "AGENTS.md").is_file():
        print(f"PACKAGE_ROOT_INVALID: {package_root} (AGENTS.md not found)")
        return 2

    files = changed_files(project_root)
    level, types = classify(files)
    if args.mode == "frontend":
        types = sorted(set(types + ["frontend"]))
        level = "L1" if level in ("L0", "L1") else level

    acceptance_path = find_acceptance(project_root, package_root, args.acceptance)
    items = parse_acceptance(acceptance_path)
    acc = check_acceptance(items)
    docs_only = bool(files) and all(f.lower().endswith(DOC_EXTS) for f in files)
    acceptance_unusable = acceptance_path is None or not items
    if not docs_only and level in ("L1", "L2", "L3") and not args.allow_missing_acceptance:
        if acceptance_unusable:
            acc = {"total": 0, "covered": 0, "duplicates": [], "missing": ["缺少可解析验收清单；L1+ 须写 AC/检查/证据"]}
        elif acc.get("duplicates"):
            acc["missing"].append(f"验收清单 AC 重复：{', '.join(acc['duplicates'][:5])}")

    profile = load_profile(project_root, package_root)
    scripts = package_json_scripts(project_root)
    timeouts = profile.get("timeouts", {}) if isinstance(profile.get("timeouts"), dict) else {}
    checks: list[dict[str, Any]] = []

    if "docs" in types and all(f.lower().endswith(DOC_EXTS) for f in files):
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
                checks.append(frontend_evidence(project_root, profile))

    applicable = [c for c in checks if c.get("status") not in ("skip", "dry-run")]
    failed = [c for c in checks if c.get("status") == "fail"]
    blocked = [c for c in checks if c.get("status") == "blocked"]
    skipped = [c for c in checks if c.get("status") == "skip"]

    verdict = "COMPLETE"
    reasons: list[str] = []
    if failed or blocked or acc["missing"]:
        verdict = "BLOCKED"
    elif skipped:
        verdict = "PARTIAL"
        reasons.append(f"{len(skipped)} check(s) skipped")
    if level in ("L1", "L2", "L3") and "docs" not in types and not any(c.get("status") == "pass" for c in checks):
        verdict = "BLOCKED"
        reasons.append("没有可执行检查；填写 .gate/project-profile.json 或项目命令")
    if acc["missing"]:
        reasons += acc["missing"][:5]
    if failed:
        reasons += [f"{c['id']} failed" for c in failed]
    if blocked:
        reasons += [f"{c['id']} blocked: {c.get('detail', '')}" for c in blocked]

    diff_text = git(project_root, "diff", "HEAD")
    diff_hash = hashlib.sha256((diff_text + "\n" + "\n".join(files)).encode("utf-8", errors="replace")).hexdigest()[:16]
    commit = git(project_root, "rev-parse", "--short", "HEAD")
    gate_id = commit or diff_hash
    completion = {
        "gate_version": "1.0",
        "package": "开发规范",
        "mode": args.mode,
        "gate_id": gate_id,
        "verdict": verdict,
        "level": level,
        "change_types": types,
        "changed_files": files,
        "acceptance": {"path": str(acceptance_path) if acceptance_path else None, **acc},
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
        print(f"checks: {len(applicable) - len(failed) - len(blocked)}/{len(applicable)} pass")
        for c in checks:
            extra = c.get("command") or c.get("detail") or ""
            print(f"- {c['id']}: {c.get('status')} {extra}".rstrip())
        if reasons:
            print("blocked/notes:")
            for r in reasons[:10]:
                print(f"  - {r}")

    if not args.dry_run:
        out_dir = project_root / ".gate"
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / "completion.json"
        out.write_text(json.dumps(completion, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"written: {out}")
    return 0 if verdict == "COMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
