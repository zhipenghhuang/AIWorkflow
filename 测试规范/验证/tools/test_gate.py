#!/usr/bin/env python3
"""Lean completion gate for the test workflow.

Usage:
  python test_gate.py --package-root <测试规范> --project-root <project> [--mode execute|report|writeback]

Exit: 0 = PASS, 1 = CONDITIONAL/FAIL/BLOCKED, 2 = usage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

STATUSES = {"未执行", "通过", "失败", "阻塞", "待实现", "不适用"}
FAIL_STATUSES = {"失败", "阻塞", "待实现"}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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


def pick_table(block: str, required: list[str]) -> tuple[list[str], list[list[str]]] | None:
    for headers, rows in tables(block):
        joined = " ".join(headers)
        if all(r in joined for r in required):
            return headers, rows
    return None


def is_current(path: Path) -> bool:
    """Exclude archives, drafts and input materials from current-run accounting."""
    return not any(part in path.parts for part in ("_归档", ".draft", "资料"))


def resolve_evidence(ledger: Path, evidence: str) -> bool:
    if not evidence:
        return False
    p = Path(evidence)
    if p.is_absolute():
        return p.exists()
    for base in (ledger.parent, *ledger.parents):
        if (base / evidence).exists():
            return True
    return False


VERDICT_MAP = {
    "PASS": "PASS",
    "CONDITIONAL": "CONDITIONAL",
    "FAIL": "FAIL",
    "BLOCKED": "BLOCKED",
}


def parse_report_verdict(text: str) -> tuple[str, str]:
    """Read the single selected value from the report's 准出评估 row."""
    line = next((ln for ln in text.splitlines() if "准出评估" in ln), "")
    if not line:
        return "", "未找到准出评估行"
    raw = line.replace("**", "").replace("`", "")
    # Template left all options in place: do not guess.
    if sum(1 for w in ("有条件通过", "不通过", "通过") if w in raw) >= 3:
        return "", "准出评估未选择唯一结论"
    if all(w in raw.upper() for w in ("PASS", "CONDITIONAL", "FAIL", "BLOCKED")):
        return "", "准出评估未选择唯一结论"
    if "不通过" in raw or "FAIL" in raw.upper():
        return "FAIL", ""
    if "有条件" in raw or "CONDITIONAL" in raw.upper():
        return "CONDITIONAL", ""
    if "阻塞" in raw or "未验证" in raw or "BLOCKED" in raw.upper():
        return "BLOCKED", ""
    if "通过" in raw or re.search(r"\bPASS\b", raw, re.I):
        return "PASS", ""
    return "", "准出评估不可识别"


def to_int(s: str) -> int:
    m = re.search(r"-?\d+", s.replace(",", ""))
    return int(m.group(0)) if m else 0


def parse_ledger(path: Path) -> dict[str, Any]:
    text = read(path)
    sec = sections(text)
    summary_block = next((v for k, v in sec.items() if "模块结论与汇总" in k or "汇总" in k), text)
    result_block = next((v for k, v in sec.items() if "结果表" in k), text)
    summary = pick_table(summary_block, ["总数", "通过", "失败"])
    results = pick_table(result_block, ["用例 ID", "结果"])
    issues: list[str] = []
    if re.search(r"\{\…\}|\{\.\.\.\}", text):
        issues.append(f"{path}: 仍有模板占位符")
    counts = {"total": 0, "pass": 0, "fail": 0, "blocked": 0, "not_run": 0, "pending": 0, "na": 0}
    p0_fail: list[str] = []
    evidence_missing: list[str] = []
    blocked_bad: list[str] = []

    if results:
        headers, rows = results
        idx = {h: i for i, h in enumerate(headers)}
        def cell(row: list[str], name: str, default: str = "") -> str:
            i = idx.get(name)
            return row[i] if i is not None and i < len(row) else default
        for row in rows:
            cid = cell(row, "用例 ID")
            status = cell(row, "结果")
            if not status:
                issues.append(f"{cid or row[0]}: 结果为空")
                continue
            if status not in STATUSES:
                issues.append(f"{cid or row[0]}: 未知结果状态 {status}")
                continue
            counts["total"] += 1
            if status == "通过":
                counts["pass"] += 1
            elif status == "失败":
                counts["fail"] += 1
            elif status == "阻塞":
                counts["blocked"] += 1
            elif status == "未执行":
                counts["not_run"] += 1
            elif status == "待实现":
                counts["pending"] += 1
            elif status == "不适用":
                counts["na"] += 1
            priority = cell(row, "优先级")
            evidence = cell(row, "证据路径")
            summary_text = cell(row, "摘要")
            if "P0" in priority and status != "通过":
                p0_fail.append(f"{cid}:{status}")
            if status in FAIL_STATUSES:
                if not evidence or evidence in ("—", "-", "无"):
                    evidence_missing.append(f"{cid}: 缺证据")
                elif not resolve_evidence(path, evidence):
                    evidence_missing.append(f"{cid}: 证据不存在 {evidence}")
                if status == "阻塞" and not re.search(r"(尝试|恢复|卡点|穷尽)", summary_text):
                    blocked_bad.append(f"{cid}: 阻塞缺已尝试/恢复条件")
        if counts["total"] == 0:
            issues.append(f"{path}: 结果表无可识别用例（结果为空/未知）")
    else:
        issues.append(f"{path}: 未找到 §2 结果表（用例 ID/结果）")

    if summary:
        headers, rows = summary
        if rows:
            row = rows[0]
            idx = {h: i for i, h in enumerate(headers)}
            def cell(name: str) -> str:
                i = idx.get(name)
                return row[i] if i is not None and i < len(row) else "0"
            declared = {
                "total": to_int(cell("总数")),
                "pass": to_int(cell("通过")),
                "fail": to_int(cell("失败")),
                "blocked": to_int(cell("阻塞")),
                "not_run": to_int(cell("未执行")),
                "pending": to_int(cell("待实现")),
                "na": to_int(cell("不适用")),
            }
            for k, v in declared.items():
                if v != counts.get(k, 0):
                    issues.append(f"{path}: {k} 汇总={v} 结果表={counts.get(k, 0)}")
    else:
        issues.append(f"{path}: 未找到 §1 汇总表（总数/通过/失败）")

    return {"path": str(path), "counts": counts, "issues": issues, "p0_fail": p0_fail,
            "evidence_missing": evidence_missing, "blocked_bad": blocked_bad}


def parse_report(path: Path, ledger_counts: dict[str, int]) -> dict[str, Any]:
    text = read(path)
    sec = sections(text)
    count_block = next((v for k, v in sec.items() if "统计" in k or "轮次" in k), text)
    counts = pick_table(count_block, ["总数", "通过", "失败"])
    issues: list[str] = []
    if re.search(r"\{\…\}|\{\.\.\.\}", text):
        issues.append("报告仍有模板占位符")
    verdict, verdict_issue = parse_report_verdict(text)
    if verdict_issue:
        issues.append(verdict_issue)
    if verdict == "PASS" and any(ledger_counts.get(k, 0) for k in ("fail", "blocked", "pending", "not_run")):
        issues.append("台账有失败/阻塞/待实现/未执行但报告写通过")
    if counts:
        headers, rows = counts
        if rows:
            row = rows[0]
            idx = {h: i for i, h in enumerate(headers)}
            def cell(name: str) -> str:
                i = idx.get(name)
                return row[i] if i is not None and i < len(row) else "0"
            declared = {
                "total": to_int(cell("总数")), "pass": to_int(cell("通过")),
                "fail": to_int(cell("失败")), "blocked": to_int(cell("阻塞")),
                "not_run": to_int(cell("未执行")), "pending": to_int(cell("待实现")),
                "na": to_int(cell("不适用")),
            }
            for k, v in declared.items():
                if v != ledger_counts.get(k, 0):
                    issues.append(f"报告 {k}={v} 与台账 {ledger_counts.get(k, 0)} 不一致")
    else:
        issues.append("报告未找到 §4 统计表（总数/通过/失败）")
    return {"path": str(path), "issues": issues, "verdict": verdict}


def parse_coverage(root: Path) -> dict[str, Any]:
    """Check functional test assets. Returns issues plus how many assets have a coverage map."""
    issues: list[str] = []
    missing: list[str] = []
    seen = 0
    files = 0
    base = root / "功能测试"
    if not base.is_dir():
        return {"issues": issues, "missing": missing, "seen": 0, "files": 0}
    for p in base.rglob("*.md"):
        if not is_current(p):
            continue
        if any(x in p.name for x in ("台账", "报告", "证据", "评审", "计划", "分析短表", "需求理解", "索引", "README")):
            continue
        files += 1
        text = read(p)
        if "设计点覆盖映射" not in text:
            missing.append(f"{p.relative_to(root)}: 缺少「设计点覆盖映射」")
            continue
        seen += 1
        sec = sections(text)
        block = next((v for k, v in sec.items() if "设计点覆盖映射" in k), "")
        table = pick_table(block, ["设计点"])
        if not table:
            issues.append(f"{p.relative_to(root)}: §3 映射表不可读")
            continue
        headers, rows = table
        for row in rows:
            if len(row) < 2:
                continue
            point = row[0].strip()
            mapping = " ".join(row[1:]).strip()
            if not point or point in ("设计点", "—", "-"):
                continue
            if not mapping or mapping in ("—", "-", "待补"):
                issues.append(f"{p.relative_to(root)}: 设计点「{point}」无映射")
    return {"issues": issues, "missing": missing, "seen": seen, "files": files}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package-root", default=str(Path(__file__).resolve().parents[2]))
    ap.add_argument("--project-root", default=str(Path(__file__).resolve().parents[3]))
    ap.add_argument("--mode", choices=["execute", "report", "writeback"], default="report")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    package_root = Path(args.package_root).resolve()
    project_root = Path(args.project_root).resolve()
    test_root = project_root / "测试"
    checks: list[dict[str, Any]] = []
    blocked: list[str] = []

    aggregate = {"total": 0, "pass": 0, "fail": 0, "blocked": 0, "not_run": 0, "pending": 0, "na": 0}
    p0_fail: list[str] = []
    reported_verdict = ""

    if args.mode in ("execute", "report"):
        plan = test_root / "测试计划.md"
        if not plan.is_file():
            blocked.append("缺少 测试/测试计划.md")
            checks.append({"id": "plan-exists", "status": "blocked", "detail": "missing"})
        else:
            checks.append({"id": "plan-exists", "status": "pass", "detail": str(plan)})

        ledgers = [
            p for p in test_root.rglob("*.md")
            if "台账" in p.name and is_current(p)
        ] if test_root.is_dir() else []
        if not ledgers:
            blocked.append("未找到执行台账（测试/功能测试/**/*台账*.md）")
            checks.append({"id": "ledger-counts", "status": "blocked", "detail": "no ledger"})
        else:
            evidence_missing: list[str] = []
            blocked_bad: list[str] = []
            ledger_issues: list[str] = []
            for ledger in ledgers:
                parsed = parse_ledger(ledger)
                for k in aggregate:
                    aggregate[k] += parsed["counts"].get(k, 0)
                p0_fail += parsed["p0_fail"]
                evidence_missing += parsed["evidence_missing"]
                blocked_bad += parsed["blocked_bad"]
                ledger_issues += parsed["issues"]
            checks.append({"id": "ledger-counts", "status": "fail" if ledger_issues else "pass", "detail": ledger_issues[:10]})
            checks.append({"id": "evidence-exists", "status": "fail" if evidence_missing else "pass", "detail": evidence_missing[:10]})
            checks.append({"id": "blocked-reasons", "status": "fail" if blocked_bad else "pass", "detail": blocked_bad[:10]})
            checks.append({"id": "p0-status", "status": "fail" if p0_fail else "pass", "detail": p0_fail[:10]})

        report = test_root / "测试报告.md"
        if not report.is_file():
            if args.mode == "report":
                blocked.append("缺少 测试/测试报告.md")
                checks.append({"id": "report-counts", "status": "blocked", "detail": "missing"})
                checks.append({"id": "report-verdict", "status": "blocked", "detail": "missing report"})
            else:
                checks.append({"id": "report-counts", "status": "skip", "detail": "execute mode"})
                checks.append({"id": "report-verdict", "status": "skip", "detail": "execute mode"})
        else:
            parsed = parse_report(report, aggregate)
            checks.append({"id": "report-counts", "status": "fail" if parsed["issues"] else "pass", "detail": parsed["issues"][:10]})
            reported_verdict = parsed["verdict"]
            checks.append({
                "id": "report-verdict",
                "status": "pass" if reported_verdict else "fail",
                "detail": reported_verdict or "准出评估缺失/不可识别",
            })
            if p0_fail and reported_verdict in ("PASS", "CONDITIONAL"):
                checks.append({"id": "p0-vs-verdict", "status": "fail", "detail": "P0 未过但报告写通过/有条件通过"})
            else:
                checks.append({"id": "p0-vs-verdict", "status": "pass", "detail": "consistent"})

        cov = parse_coverage(test_root) if test_root.is_dir() else {"issues": [], "missing": [], "seen": 0, "files": 0}
        cov_issues = list(cov["issues"])
        if args.mode == "report":
            cov_issues += cov["missing"]
            if cov["files"] > 0 and cov["seen"] == 0:
                cov_issues.append("功能测试资产缺少设计点覆盖映射（覆盖三闸）")
        checks.append({"id": "coverage-map", "status": "fail" if cov_issues else "pass", "detail": cov_issues[:10]})
    else:
        receipts = [
            p for p in test_root.rglob("*.md")
            if ("回执" in p.name or "回写" in p.name) and is_current(p)
        ] if test_root.is_dir() else []
        if not receipts:
            blocked.append("未找到回写回执（测试/**/*回执*.md）")
            checks.append({"id": "writeback-receipt", "status": "blocked", "detail": "missing"})
        else:
            receipt = max(receipts, key=lambda p: p.stat().st_mtime)
            text = read(receipt)
            issues = []
            if not re.search(r"(BUG[-_]?\d+|#\d+)", text, re.I):
                issues.append("回执缺少平台单号")
            if "备注" not in text:
                issues.append("回执缺少备注")
            if "状态" not in text:
                issues.append("回执缺少状态")
            if "附件" not in text:
                issues.append("回执缺少附件回查")
            checks.append({"id": "writeback-receipt", "status": "fail" if issues else "pass", "detail": issues or str(receipt)})

    failed = [c for c in checks if c.get("status") == "fail"]
    blocked_checks = [c for c in checks if c.get("status") == "blocked"]
    if blocked or blocked_checks:
        verdict = "BLOCKED"
    elif failed or p0_fail:
        verdict = "FAIL"
    elif reported_verdict == "BLOCKED":
        verdict = "BLOCKED"
    elif reported_verdict == "FAIL":
        verdict = "FAIL"
    elif aggregate.get("fail", 0) or aggregate.get("blocked", 0) or aggregate.get("pending", 0) or aggregate.get("not_run", 0):
        verdict = "CONDITIONAL"
    elif reported_verdict == "CONDITIONAL":
        verdict = "CONDITIONAL"
    elif args.mode == "report" and not reported_verdict:
        verdict = "FAIL"
    else:
        verdict = "PASS"

    now_dt = datetime.now(timezone.utc).astimezone()
    now = now_dt.isoformat(timespec="seconds")
    gate_id = f"{args.mode}-{now_dt.strftime('%Y%m%dT%H%M%S')}-{hashlib.sha256(str(test_root).encode('utf-8')).hexdigest()[:8]}"
    completion = {
        "gate_version": "1.0",
        "package": "测试规范",
        "mode": args.mode,
        "gate_id": gate_id,
        "verdict": verdict,
        "counts": aggregate,
        "p0_fail": p0_fail,
        "checks": checks,
        "blocked": blocked,
        "timestamp": now,
    }

    if args.json:
        print(json.dumps(completion, ensure_ascii=False, indent=2))
    else:
        print("=== 完成门（测试规范）===")
        print(f"verdict: {verdict}")
        print(f"counts: total={aggregate['total']} pass={aggregate['pass']} fail={aggregate['fail']} blocked={aggregate['blocked']} pending={aggregate['pending']}")
        for c in checks:
            print(f"- {c['id']}: {c.get('status')} {str(c.get('detail', ''))[:160]}")
        if blocked:
            print("blocked:")
            for b in blocked[:8]:
                print(f"  - {b}")

    out_dir = project_root / ".gate"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "completion.json").write_text(json.dumps(completion, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"written: {out_dir / 'completion.json'}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
