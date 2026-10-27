#!/usr/bin/env python3
"""Lean completion gate for the product workflow.

Design goals:
- The spec package is read-only. Runtime state lives in <project>/.gate/产品规范/.
- UAT must cover PRD ACs; review must contain a real checklist/verdict; release must use the UAT gate.
- A gate result must belong to the current artifact (content hash gate_id), not a previous version.

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

PACKAGE_NAME = "产品规范"
RECEIPT_DIR = Path(".gate") / PACKAGE_NAME
PLACEHOLDER_RE = re.compile(r"\{[^{}\n]{1,80}\}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


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


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def unfilled_placeholders(text: str) -> list[str]:
    return [m.group(0) for m in PLACEHOLDER_RE.finditer(strip_code(text))]


def artifact_score(path: Path) -> tuple[int, float]:
    try:
        fm = frontmatter(read(path))
    except Exception:
        fm = {}
    return (1 if fm.get("source_of_truth", "").lower() == "true" else 0, path.stat().st_mtime)


def resolve_path(root: Path, raw: str) -> Path:
    p = Path(raw)
    return p if p.is_absolute() else (root / p)


def find_artifact(root: Path, mode: str, explicit: str | None = None) -> Path | None:
    if explicit:
        p = resolve_path(root, explicit)
        return p if p.is_file() else None
    base = root / "产品"
    if not base.is_dir():
        return None
    patterns = {
        "prd": ["PRD-*.md"],
        "review": ["评审-*.md"],
        "uat": ["UAT-*.md"],
        "change": ["受理-*.md", "变更-*.md"],
        "writeback": ["缺陷处置-*.md", "受理-*.md"],
    }.get(mode, ["*.md"])
    candidates: list[Path] = []
    for pat in patterns:
        candidates += [p for p in base.rglob(pat)
                       if "资料" not in p.parts and "_归档" not in p.parts and "模板" not in p.parts]
    if not candidates:
        return None
    if mode == "prd":
        return max(candidates, key=artifact_score)
    return max(candidates, key=lambda p: p.stat().st_mtime)


def pick_table(text: str, heading_keywords: tuple[str, ...], required: tuple[str, ...]) -> tuple[list[str], list[list[str]]] | None:
    sec = sections(text)
    block = next((v for k, v in sec.items() if any(x in k for x in heading_keywords)), text)
    for headers, rows in tables(block):
        joined = " ".join(headers)
        if all(r in joined for r in required):
            return headers, rows
    return None


def check_tbd(text: str) -> list[str]:
    issues: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", ">")) or s.startswith("| ---"):
            continue
        if "{" in s or "}" in s:
            continue
        if not re.search(r"(待确认|TBD|待定)", s):
            continue
        if re.search(r"(责任人|owner|期限|due|截止)", s, re.I):
            continue
        issues.append(s[:120])
    return issues


def check_light_prd(text: str) -> tuple[list[str], list[str]]:
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
        _, rows = table
        usable = 0
        for row in rows:
            if len(row) >= 3 and row[0].strip() and row[2].strip() not in ("", "—", "-", "待补"):
                usable += 1
        if usable == 0:
            issues.append("轻量 PRD 验收表无有效行（功能+验收标准）")
    return issues, warnings


def extract_prd_acs(text: str) -> set[str]:
    table = pick_table(text, ("验收场景", "## 13."), ("场景", "AC"))
    ids: set[str] = set()
    if table:
        _, rows = table
        for row in rows:
            for cell in row[:2]:
                ids.update(re.findall(r"\b(?:AC|A)-\d+\b", cell))
    if not ids:
        ids.update(re.findall(r"\bAC-\d+\b", text))
    return ids


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
            p = subprocess.run([sys.executable, "-B", str(validator), str(path)],
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
            if p.returncode != 0:
                issues.append("validate_prd.py 未通过")
                issues += [ln for ln in (p.stdout or "").splitlines() if ln.startswith("ERROR")][:10]
            else:
                warnings += [ln for ln in (p.stdout or "").splitlines() if ln.startswith("WARN")][:10]
        else:
            issues.append("validate_prd.py 不存在；全量 PRD 不能跳过结构校验")
    status = fm.get("status", "").upper()
    placeholders = unfilled_placeholders(text)
    if status == "APPROVED":
        if placeholders:
            issues.append(f"status=APPROVED 但仍有 {len(placeholders)} 处模板占位符：{', '.join(placeholders[:5])}")
        if fm.get("source_of_truth", "").lower() != "true":
            issues.append("status=APPROVED 但 source_of_truth 不是 true")
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
                rfm = frontmatter(read(review))
                if not rfm.get("gate_id"):
                    issues.append("评审记录缺少 gate_id（将 review 回执回填后复跑）")
                elif fm.get("gate_id") and rfm.get("gate_id") != fm.get("gate_id"):
                    issues.append("PRD 与评审记录的 gate_id 不一致")
    elif placeholders:
        warnings.append(f"草稿仍有 {len(placeholders)} 处占位符")
    issues += check_tbd(text)

    # Traceability: header + at least one row with F/R/A/AC values.
    sec = sections(text)
    trace_block = next((v for k, v in sec.items() if "追溯" in k), "")
    if trace_block:
        table = None
        for headers, rows in tables(trace_block):
            joined = " ".join(headers)
            if all(x in joined for x in ("F", "R", "A", "AC")):
                table = (headers, rows)
                break
        if not table:
            issues.append("追溯矩阵不可读（需 F/R/A/AC 列）")
        else:
            headers, rows = table
            nonempty = [r for r in rows if sum(1 for c in r if c.strip()) >= 4]
            if not nonempty:
                issues.append("追溯矩阵无有效行（F/R/A/AC 不能为空）")
    else:
        issues.append("缺少追溯矩阵")

    return {"path": str(path), "issues": issues, "warnings": warnings,
            "status": status, "level": level, "ac_ids": sorted(extract_prd_acs(text))}


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
    sec = sections(text)
    checklist = next((v for k, v in sec.items() if "清单" in k or "核对" in k), "")
    if not checklist:
        issues.append("缺少评审清单/核对节")
    elif "全部通过" in checklist and "例外" in checklist:
        issues.append("评审清单未选择唯一结果（全部通过/例外 仍是模板选项）")
    elif "全部通过" not in checklist:
        table = next((t for t in tables(checklist) if "级别" in " ".join(t[0]) or "结果" in " ".join(t[0])), None)
        if not table or not any(sum(1 for c in r if c.strip()) >= 3 for r in table[1]):
            issues.append("评审清单未填写（需 全部通过 或 逐条例外表）")
    conclusion = next((v for k, v in sec.items() if "结论" in k), "")
    if not conclusion:
        issues.append("评审结论节缺失")
    elif re.search(r"(需修|不通过|未通过|部分通过)", conclusion):
        issues.append("评审结论为需修/未通过，不能视为通过")
    elif "通过" not in conclusion:
        issues.append("评审结论节缺少 通过")
    return {"path": str(path), "issues": issues, "verdict": verdict}


def check_uat(path: Path, prd_path: Path | None) -> dict[str, Any]:
    text = read(path)
    issues: list[str] = []
    if unfilled_placeholders(text):
        issues.append("UAT 记录仍有模板占位符")
    fm = frontmatter(text)
    verdict = fm.get("verdict") or ""
    if verdict in ("不适用", "N/A", "NOT_APPLICABLE"):
        if not re.search(r"(依据|原因|理由)\s*[:：]?\s*\S+", text):
            issues.append("UAT 不适用需写依据/原因")
        if not re.search(r"(批准人|接受人|责任人)", text):
            issues.append("UAT 不适用需写批准人/接受人")
        return {"path": str(path), "issues": issues, "verdict": verdict,
                "warnings": ["UAT 标记不适用；请确认本期确无真实用户验收要求"]}
    if not verdict:
        issues.append("缺少 verdict（通过/有条件/不通过）")
    elif verdict not in ("通过", "PASS", "APPROVED", "有条件通过", "CONDITIONAL"):
        issues.append(f"UAT verdict={verdict} 非通过")

    table = pick_table(text, ("逐条验收", "## 2."), ("验收编号", "结果"))
    if not table:
        table = pick_table(text, ("逐条验收", "## 2."), ("AC", "结果"))
    if not table:
        issues.append("UAT 缺少逐条验收表（验收编号/AC + 结果 + 证据）")
        rows: list[list[str]] = []
        headers: list[str] = []
    else:
        headers, rows = table
        if not rows:
            issues.append("UAT 逐条验收表无数据行")
        id_idx = next((i for i, h in enumerate(headers) if "编号" in h or "AC" in h), 0)
        result_idx = next((i for i, h in enumerate(headers) if "结果" in h), 2)
        evidence_idx = next((i for i, h in enumerate(headers) if "证据" in h), 3)
        for row in rows:
            if len(row) <= max(id_idx, result_idx, evidence_idx):
                continue
            ac_id = row[id_idx].strip()
            result = row[result_idx].strip()
            evidence = row[evidence_idx].strip()
            if not ac_id or not result:
                issues.append(f"UAT 行不完整：{row[:4]}")
                continue
            if result not in ("通过", "不通过", "带条件", "有条件", "有条件通过"):
                issues.append(f"{ac_id}: 结果不可识别 {result}")
            if not evidence or evidence in ("—", "-", "无") or re.search(r"口头|口述|聊天确认", evidence):
                issues.append(f"{ac_id}: 缺少可回查证据")
            if "条件" in result and not re.search(r"(责任人|接受人)", " ".join(row), re.I):
                issues.append(f"{ac_id}: 有条件通过缺少责任人/接受人")

    conditional = verdict in ("有条件通过", "CONDITIONAL") or any("条件" in r[2] for r in rows if len(r) > 2)
    if conditional:
        block = next((v for k, v in sections(text).items() if "结论" in k), "")
        if not re.search(r"(责任人|owner)", block, re.I) or not re.search(r"(接受人|acceptor)", block, re.I):
            issues.append("有条件通过缺少责任人/接受人")

    if prd_path and prd_path.is_file():
        prd_acs = extract_prd_acs(read(prd_path))
        uat_acs = {row[0].strip() for row in rows if row and re.fullmatch(r"(?:AC|A)-\d+", row[0].strip())}
        missing = sorted(prd_acs - uat_acs)
        if missing:
            issues.append(f"UAT 未覆盖 PRD AC：{', '.join(missing[:10])}")
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
        _, rows = table
        for row in rows:
            line = " ".join(row)
            if not line.strip():
                continue
            if "待补" in line and not re.search(r"(责任人|owner|截止|期限|due)", line, re.I):
                issues.append(f"待补项缺少责任人/截止：{line[:100]}")
            if not any(s in line for s in ("已更新", "不适用", "待补")):
                issues.append(f"联动项状态不明确：{line[:100]}")
    close_block = next((v for k, v in sec.items() if "验证" in k or "7." in k), "")
    if close_block and not re.search(r"结果\s*[:：]\s*(通过|不通过|待验证|不适用)", close_block):
        issues.append("§7 缺少验证结果（通过/不通过/待验证/不适用）")
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
    if "已回写" in text and "待回写" not in text and not re.search(r"(noteId|备注ID|回写时间|回执)", text, re.I):
        issues.append("声称已回写但缺少回执/noteId/时间")
    return {"path": str(path), "issues": issues}


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
    ap.add_argument("--mode", choices=["prd", "review", "uat", "change", "writeback"], default="prd")
    ap.add_argument("--artifact", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    package_root = Path(args.package_root).resolve()
    project_root = Path(args.project_root).resolve()
    if not (package_root / "AGENTS.md").is_file():
        print(f"PACKAGE_ROOT_INVALID: {package_root} (AGENTS.md not found)")
        return 2
    if project_root == package_root or package_root in project_root.parents:
        print("PROJECT_ROOT_INVALID: 项目根不能是规范包本身或在规范包内；运行态只写项目根 .gate/")
        return 2

    path = find_artifact(project_root, args.mode, args.artifact)
    checks: list[dict[str, Any]] = []
    blocked: list[str] = []
    result: dict[str, Any] = {"issues": []}

    if path is None or not path.is_file():
        blocked.append(f"未找到 {args.mode} 产物（产品/**）；请用 --artifact 指定当前版本文件")
    else:
        if args.mode == "prd":
            result = check_prd(package_root, path)
        elif args.mode == "review":
            result = check_review(path)
        elif args.mode == "uat":
            prd = find_artifact(project_root, "prd")
            result = check_uat(path, prd)
        elif args.mode == "change":
            result = check_change(path)
        else:
            result = check_writeback(path)
        checks.append({"id": args.mode, "status": "fail" if result.get("issues") else "pass",
                       "detail": result.get("issues", [])[:10]})

    failed = [c for c in checks if c.get("status") == "fail"]
    verdict = "READY"
    if blocked or failed:
        verdict = "BLOCKED"
    elif args.mode == "prd" and result.get("status") != "APPROVED":
        verdict = "DRAFT"
    elif args.mode == "review" and result.get("verdict") not in ("通过", "PASS", "APPROVED"):
        verdict = "DRAFT"
    elif args.mode == "uat" and result.get("verdict") not in ("通过", "PASS", "APPROVED", "有条件通过", "CONDITIONAL", "不适用", "N/A", "NOT_APPLICABLE"):
        verdict = "DRAFT"

    content = read(path) if path and path.is_file() else ""
    gate_id = f"{args.mode}-{hashlib.sha256(content.encode('utf-8', errors='replace')).hexdigest()[:12]}"
    completion = {
        "gate_version": "2.0",
        "package": PACKAGE_NAME,
        "mode": args.mode,
        "gate_id": gate_id,
        "verdict": verdict,
        "artifact": str(path) if path else None,
        "checks": checks,
        "blocked": blocked,
        "warnings": result.get("warnings", []) if isinstance(result, dict) else [],
        "timestamp": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
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

    out = write_receipt(project_root, args.mode, completion)
    print(f"written: {out}")
    return 0 if verdict == "READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
