#!/usr/bin/env python3
"""Lean completion gate for the product workflow.

Usage:
  python product_gate.py --package-root <产品规范> --project-root <project> [--mode prd|review|uat|change|writeback] [--artifact <file>]

Exit: 0 = READY, 1 = DRAFT/BLOCKED, 2 = usage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    out: dict[str, str] = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def sections(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    current = ""
    buf: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current:
                out[current] = "\n".join(buf)
            current = line.strip()
            buf = [line]
        else:
            buf.append(line)
    if current:
        out[current] = "\n".join(buf)
    return out


def tables(block: str) -> list[tuple[list[str], list[list[str]]]]:
    lines = block.splitlines()
    out: list[tuple[list[str], list[list[str]]]] = []
    i = 0
    while i < len(lines) - 1:
        line = lines[i].strip()
        nxt = lines[i + 1].strip()
        if line.startswith("|") and re.match(r"^\|[\s:|-]+\|$", nxt):
            headers = [c.strip() for c in line.strip().strip("|").split("|")]
            rows: list[list[str]] = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append([c.strip() for c in lines[j].strip().strip("|").split("|")])
                j += 1
            out.append((headers, rows))
            i = j
        else:
            i += 1
    return out


PLACEHOLDER_RE = re.compile(r"\{[^{}\n]{1,80}\}")


def strip_code(text: str) -> str:
    """Remove fenced/inline code so API/JSON/Mermaid braces are not treated as placeholders."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def unfilled_placeholders(text: str) -> list[str]:
    return [m.group(0) for m in PLACEHOLDER_RE.finditer(strip_code(text))]


def artifact_score(path: Path) -> tuple[int, float]:
    """Prefer the document marked as source_of_truth, then the newest file."""
    try:
        fm = frontmatter(read(path))
    except Exception:
        fm = {}
    return (1 if fm.get("source_of_truth", "").lower() == "true" else 0, path.stat().st_mtime)


def find_artifact(root: Path, mode: str) -> Path | None:
    base = root / "产品"
    if not base.is_dir():
        return None
    patterns = {
        "prd": ["PRD-*.md"],
        "review": ["评审-*.md"],
        "uat": ["UAT-*.md"],
        "change": ["变更-*.md", "受理-*.md"],
        "writeback": ["缺陷处置-*.md", "受理-*.md"],
    }.get(mode, ["*.md"])
    candidates: list[Path] = []
    for pat in patterns:
        candidates += [p for p in base.rglob(pat) if "资料" not in p.parts and "_归档" not in p.parts]
    if not candidates:
        return None
    if mode == "prd":
        return max(candidates, key=artifact_score)
    return max(candidates, key=lambda p: p.stat().st_mtime)


def check_tbd(text: str) -> list[str]:
    issues: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", ">")):
            continue
        if "{" in s or "}" in s:
            continue
        if not re.search(r"(待确认|TBD|待定)", s):
            continue
        if re.search(r"(责任人|owner|期限|due|截止)", s, re.I):
            continue
        if s.startswith("|") and "| 待确认 |" in s and not re.search(r"\b(Q|TBD)-\d+", s):
            continue
        issues.append(s[:120])
    return issues


def check_light_prd(text: str) -> tuple[list[str], list[str]]:
    """P0/P1 light PRD: minimum sections + a usable acceptance table; full 0~16/Mermaid not required."""
    issues: list[str] = []
    warnings: list[str] = ["轻量 PRD：按最小结构校验，免独立评审"]
    for sec in ("## 2.", "## 4.", "## 5.", "## 6.", "## 8."):
        if sec not in text:
            issues.append(f"轻量 PRD 缺少章节 {sec}")
    sec = sections(text)
    block = next((v for k, v in sec.items() if "功能与验收" in k), "")
    table = None
    for headers, rows in tables(block):
        if any("验收" in h or "AC" in h for h in headers):
            table = (headers, rows)
            break
    if table is None:
        issues.append("轻量 PRD 缺少功能/验收表")
    else:
        headers, rows = table
        usable = 0
        for row in rows:
            if len(row) >= 3 and row[0].strip() and row[2].strip() not in ("", "—", "-", "待补"):
                usable += 1
        if usable == 0:
            issues.append("轻量 PRD 验收表无有效行（功能+验收标准）")
    return issues, warnings


def check_prd(package_root: Path, path: Path) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []
    text = read(path)
    fm = frontmatter(text)
    level = (fm.get("prd_level") or ("light" if "轻量" in text[:300] else "full")).lower()
    if level not in ("light", "full"):
        level = "full"
    for key in ("doc_id", "title", "status", "version", "owner", "source_of_truth", "updated"):
        if not fm.get(key):
            issues.append(f"frontmatter 缺少 {key}")
    if level == "light":
        light_issues, light_warnings = check_light_prd(text)
        issues += light_issues
        warnings += light_warnings
    else:
        validator = package_root / "规则" / "tools" / "validate_prd.py"
        if validator.is_file():
            p = subprocess.run([sys.executable, str(validator), str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace")
            if p.returncode != 0:
                issues.append("validate_prd.py 未通过")
                issues += [ln for ln in (p.stdout or "").splitlines() if ln.startswith("ERROR")][:10]
            else:
                warnings += [ln for ln in (p.stdout or "").splitlines() if ln.startswith("WARN")][:10]
        else:
            warnings.append("validate_prd.py 不存在，跳过结构校验")
    status = fm.get("status", "").upper()
    placeholders = unfilled_placeholders(text)
    if status == "APPROVED":
        if placeholders:
            issues.append(f"status=APPROVED 但仍有 {len(placeholders)} 处模板占位符：{', '.join(placeholders[:5])}")
        if level == "light":
            if fm.get("review_status", "").upper() not in ("SELF_CHECKED", "APPROVED", "NOT_REQUIRED"):
                issues.append("轻量 PRD status=APPROVED 需 review_status=SELF_CHECKED/APPROVED")
        else:
            if fm.get("review_status", "").upper() != "APPROVED":
                issues.append("status=APPROVED 但 review_status 不是 APPROVED")
            if not fm.get("gate_id"):
                issues.append("status=APPROVED 但缺少 gate_id（由 -Mode review 回执回填）")
            reviews = [p for p in path.parent.glob("评审-*.md")]
            if not reviews:
                issues.append("status=APPROVED 但同目录无评审记录")
            else:
                review = max(reviews, key=lambda p: p.stat().st_mtime)
                r = check_review(review)
                issues += [f"评审记录: {x}" for x in r["issues"]]
                if not frontmatter(read(review)).get("gate_id"):
                    issues.append("评审记录缺少 gate_id（将 review 回执回填后复跑）")
    elif placeholders:
        warnings.append(f"草稿仍有 {len(placeholders)} 处占位符")
    issues += check_tbd(text)
    # traceability table non-empty
    if "追溯" in text:
        for headers, rows in tables(text):
            joined = " ".join(headers)
            if "F" in joined and "AC" in joined:
                for row in rows:
                    if sum(1 for c in row if c.strip()) <= 1:
                        issues.append("追溯矩阵存在空链行")
                        break
    return {"path": str(path), "issues": issues, "warnings": warnings, "status": status, "level": level}


def check_review(path: Path) -> dict[str, Any]:
    text = read(path)
    fm = frontmatter(text)
    issues: list[str] = []
    if unfilled_placeholders(text):
        issues.append("评审记录仍有模板占位符")
    reviewer = fm.get("reviewer") or ""
    author = fm.get("author") or fm.get("owner") or ""
    verdict = fm.get("verdict") or ""
    if not reviewer:
        issues.append("缺少 reviewer")
    if not author:
        issues.append("缺少 author/owner")
    if reviewer and author and reviewer == author:
        issues.append("reviewer 不能等于 author（独立评审）")
    if not verdict:
        issues.append("缺少 verdict（通过/需修）")
    elif verdict not in ("通过", "PASS", "APPROVED"):
        issues.append(f"评审 verdict={verdict} 非通过")
    if "阻断" not in text and "评分" not in text and "清单" not in text:
        issues.append("评审记录缺少清单/评分/阻断项")
    return {"path": str(path), "issues": issues, "verdict": verdict}


def check_uat(path: Path) -> dict[str, Any]:
    text = read(path)
    issues: list[str] = []
    if unfilled_placeholders(text):
        issues.append("UAT 记录仍有模板占位符")
    fm = frontmatter(text)
    verdict = fm.get("verdict") or ""
    if not verdict:
        issues.append("缺少 verdict（通过/有条件/不通过）")
    elif verdict not in ("通过", "PASS", "APPROVED", "有条件通过", "CONDITIONAL"):
        issues.append(f"UAT verdict={verdict} 非通过")
    if "AC" not in text and "验收标准" not in text:
        issues.append("UAT 未对照 AC/验收标准")
    if "证据" not in text:
        issues.append("UAT 缺少证据")
    if "带条件" in text or "有条件" in text:
        if not re.search(r"(责任人|owner)", text) or not re.search(r"(接受人|acceptor)", text):
            issues.append("有条件通过缺少责任人或接受人")
    return {"path": str(path), "issues": issues, "verdict": verdict}


def check_change(path: Path) -> dict[str, Any]:
    text = read(path)
    sec = sections(text)
    issues: list[str] = []
    if unfilled_placeholders(text):
        issues.append("变更/受理记录仍有模板占位符")
    block = next((v for k, v in sec.items() if "联动" in k or "6." in k), text)
    table = None
    for headers, rows in tables(block):
        if any("状态" in h or "更新" in h for h in headers):
            table = (headers, rows)
            break
    if not table:
        issues.append("未找到联动清单表（含状态/更新列）")
    else:
        headers, rows = table
        joined = " ".join(headers)
        for row in rows:
            line = " ".join(row)
            if not line.strip():
                continue
            if "待补" in line and not re.search(r"(责任人|owner|截止|期限|due)", line, re.I):
                issues.append(f"待补项缺少责任人/截止：{line[:100]}")
            if not any(s in line for s in ("已更新", "不适用", "待补")):
                issues.append(f"联动项状态不明确：{line[:100]}")
    return {"path": str(path), "issues": issues}


def check_writeback(path: Path) -> dict[str, Any]:
    text = read(path)
    issues: list[str] = []
    if unfilled_placeholders(text):
        issues.append("回写记录仍有模板占位符")
    if not re.search(r"((BUG|缺陷)[-_]?\d+|#\d+)", text, re.I):
        issues.append("缺少平台单号")
    if "备注" not in text:
        issues.append("缺少备注")
    if "状态" not in text:
        issues.append("缺少状态")
    if "附件" not in text:
        issues.append("缺少附件回查")
    if "已回写" in text and not re.search(r"(noteId|备注ID|回写时间|回执)", text, re.I):
        issues.append("声称已回写但缺少回执/noteId/时间")
    return {"path": str(path), "issues": issues}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package-root", default=str(Path(__file__).resolve().parents[2]))
    ap.add_argument("--project-root", default=str(Path(__file__).resolve().parents[3]))
    ap.add_argument("--mode", choices=["prd", "review", "uat", "change", "writeback"], default="prd")
    ap.add_argument("--artifact", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    package_root = Path(args.package_root).resolve()
    project_root = Path(args.project_root).resolve()
    path = Path(args.artifact) if args.artifact else find_artifact(project_root, args.mode)
    checks: list[dict[str, Any]] = []
    blocked: list[str] = []

    if path is None or not path.is_file():
        blocked.append(f"未找到 {args.mode} 产物（产品/**）")
        result: dict[str, Any] = {"path": None, "issues": blocked}
    else:
        if args.mode == "prd":
            result = check_prd(package_root, path)
        elif args.mode == "review":
            result = check_review(path)
        elif args.mode == "uat":
            result = check_uat(path)
        elif args.mode == "change":
            result = check_change(path)
        else:
            result = check_writeback(path)
        checks.append({"id": args.mode, "status": "fail" if result.get("issues") else "pass", "detail": result.get("issues", [])[:10]})

    failed = [c for c in checks if c.get("status") == "fail"]
    verdict = "READY"
    if blocked or failed:
        verdict = "BLOCKED"
    elif args.mode == "prd" and result.get("status") != "APPROVED":
        verdict = "DRAFT"
    elif args.mode == "review" and result.get("verdict") not in ("通过", "PASS", "APPROVED"):
        verdict = "DRAFT"
    elif args.mode == "uat" and result.get("verdict") not in ("通过", "PASS", "APPROVED"):
        verdict = "DRAFT"

    now_dt = datetime.now(timezone.utc).astimezone()
    now = now_dt.isoformat(timespec="seconds")
    artifact_key = str(path) if path else "none"
    gate_id = f"{args.mode}-{now_dt.strftime('%Y%m%dT%H%M%S')}-{hashlib.sha256(artifact_key.encode('utf-8')).hexdigest()[:8]}"
    completion = {
        "gate_version": "1.0",
        "package": "产品规范",
        "mode": args.mode,
        "gate_id": gate_id,
        "verdict": verdict,
        "artifact": str(path) if path else None,
        "checks": checks,
        "blocked": blocked,
        "warnings": result.get("warnings", []) if isinstance(result, dict) else [],
        "timestamp": now,
    }

    if args.json:
        print(json.dumps(completion, ensure_ascii=False, indent=2))
    else:
        print("=== 完成门（产品规范）===")
        print(f"verdict: {verdict}")
        print(f"artifact: {path}")
        for c in checks:
            print(f"- {c['id']}: {c.get('status')} {str(c.get('detail', ''))[:200]}")
        if blocked:
            for b in blocked:
                print(f"  - {b}")

    out_dir = project_root / ".gate"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "completion.json").write_text(json.dumps(completion, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"written: {out_dir / 'completion.json'}")
    return 0 if verdict == "READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
