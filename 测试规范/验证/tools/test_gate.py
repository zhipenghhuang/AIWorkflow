#!/usr/bin/env python3
"""Lean completion gate for the test workflow.

Design goals:
- The spec package is read-only. Runtime state lives in <project>/.gate/测试规范/.
- P0 is checked against the plan/stable smoke list, not only against rows that happen to exist.
- Report / execute / writeback receipts are separate, so a writeback cannot overwrite a report verdict.
- Coverage parsing only reads case documents, never evidence notes.

Usage:
  python test_gate.py --package-root <测试规范> --project-root <project> [--mode execute|report|writeback|coverage]

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

PACKAGE_NAME = "测试规范"
RECEIPT_DIR = Path(".gate") / PACKAGE_NAME
STATUSES = {"未执行", "通过", "失败", "阻塞", "待实现", "不适用"}
FAIL_STATUSES = {"失败", "阻塞", "待实现"}
CASE_ID_RE = re.compile(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d+\b")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


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
    return not any(part in path.parts for part in ("_归档", ".draft", "资料", "证据"))


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


def parse_report_verdict(text: str) -> tuple[str, str]:
    line = next((ln for ln in text.splitlines() if "准出评估" in ln), "")
    if not line:
        return "", "未找到准出评估行"
    raw = line.replace("**", "").replace("`", "")
    # Template left all options in place: do not guess.
    if sum(1 for w in ("有条件通过", "不通过", "通过") if w in raw) >= 3:
        return "", "准出评估未选择唯一结论"
    if all(w in raw.upper() for w in ("PASS", "CONDITIONAL", "FAIL", "BLOCKED")):
        return "", "准出评估未选择唯一结论"
    if "有条件" in raw or "CONDITIONAL" in raw.upper():
        return "CONDITIONAL", ""
    if re.search(r"不通过(?!项)", raw) or re.search(r"\bFAIL\b", raw, re.I):
        return "FAIL", ""
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
    ids: set[str] = set()

    if results:
        headers, rows = results
        idx = {h: i for i, h in enumerate(headers)}
        def cell(row: list[str], name: str, default: str = "") -> str:
            i = idx.get(name)
            return row[i] if i is not None and i < len(row) else default
        for row in rows:
            cid = cell(row, "用例 ID")
            status = cell(row, "结果")
            if not cid:
                continue
            ids.add(cid)
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
            # 用例优先级（P0-Smoke/P0-HighRisk/P1-Core/P2-Low）；兼容旧台账的“优先级”列。
            priority = cell(row, "用例优先级") or cell(row, "优先级")
            evidence = cell(row, "证据路径")
            summary_text = cell(row, "摘要")
            if "P0" in priority and status != "通过":
                if status == "不适用" and re.search(r"(依据|不适用|原因)", summary_text):
                    pass
                else:
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
                "total": to_int(cell("总数")), "pass": to_int(cell("通过")),
                "fail": to_int(cell("失败")), "blocked": to_int(cell("阻塞")),
                "not_run": to_int(cell("未执行")), "pending": to_int(cell("待实现")),
                "na": to_int(cell("不适用")),
            }
            for k, v in declared.items():
                if v != counts.get(k, 0):
                    issues.append(f"{path}: {k} 汇总={v} 结果表={counts.get(k, 0)}")
    else:
        issues.append(f"{path}: 未找到 §1 汇总表（总数/通过/失败）")

    return {"path": str(path), "counts": counts, "issues": issues, "p0_fail": p0_fail,
            "evidence_missing": evidence_missing, "blocked_bad": blocked_bad, "ids": ids}


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
    receipt = re.search(r"【验证回执】\s*verdict\s*=\s*([A-Za-z]+)", text, re.I)
    receipt_verdict = receipt.group(1).upper() if receipt else ""
    if receipt_verdict and verdict and receipt_verdict != verdict:
        issues.append(f"报告回执 verdict={receipt_verdict} 与准出评估={verdict} 不一致")
    return {"path": str(path), "issues": issues, "verdict": verdict,
            "receipt_verdict": receipt_verdict}


def parse_coverage(root: Path) -> dict[str, Any]:
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
        if "用例" not in p.name and "testcase" not in p.name.lower():
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
        case_ids = set(re.findall(r"^###\s+([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d+)\b", text, re.M))
        for row in rows:
            if len(row) < 2:
                continue
            point = row[0].strip()
            mapping = " ".join(row[1:]).strip()
            if not point or point in ("设计点", "—", "-"):
                continue
            if not mapping or mapping in ("—", "-", "待补"):
                issues.append(f"{p.relative_to(root)}: 设计点「{point}」无映射")
                continue
            mapped_ids = set(CASE_ID_RE.findall(mapping))
            if case_ids and mapped_ids and not (mapped_ids & case_ids):
                issues.append(f"{p.relative_to(root)}: 设计点「{point}」映射到不存在的用例")
    return {"issues": issues, "missing": missing, "seen": seen, "files": files}


def extract_p0_ids(*texts: str) -> set[str]:
    ids: set[str] = set()
    for text in texts:
        for line in text.splitlines():
            if not re.search(r"P0-(?:Smoke|HighRisk)|P0\b", line, re.I):
                continue
            ids.update(x for x in CASE_ID_RE.findall(line)
                       if not x.startswith(("DP-", "RQ-", "AC-", "F-", "R-", "TP-")))
    return ids


def write_receipt(project_root: Path, mode: str, data: dict[str, Any], primary: bool = True) -> Path:
    out_dir = project_root / RECEIPT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{mode}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    if primary:
        (out_dir / "completion.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package-root", default=str(Path(__file__).resolve().parents[2]))
    ap.add_argument("--project-root", default=str(Path(__file__).resolve().parents[3]))
    ap.add_argument("--mode", choices=["execute", "report", "writeback", "coverage"], default="report")
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

    test_root = project_root / "测试"
    checks: list[dict[str, Any]] = []
    blocked: list[str] = []
    aggregate = {"total": 0, "pass": 0, "fail": 0, "blocked": 0, "not_run": 0, "pending": 0, "na": 0}
    p0_fail: list[str] = []
    p0_missing: list[str] = []
    reported_verdict = ""
    receipt_verdict = ""

    if args.mode in ("execute", "report", "coverage"):
        plan = test_root / "测试计划.md"
        if args.mode in ("execute", "report"):
            if not plan.is_file():
                blocked.append("缺少 测试/测试计划.md")
                checks.append({"id": "plan-exists", "status": "blocked", "detail": "missing"})
            else:
                checks.append({"id": "plan-exists", "status": "pass", "detail": str(plan)})

        if args.mode in ("execute", "report"):
            ledgers = [p for p in test_root.rglob("*.md") if "台账" in p.name and is_current(p)] if test_root.is_dir() else []
            ledger_ids: set[str] = set()
            if not ledgers:
                blocked.append("未找到执行台账（测试/功能测试/**/*台账*.md）")
                checks.append({"id": "ledger-counts", "status": "blocked", "detail": "no ledger"})
            else:
                evidence_missing: list[str] = []
                blocked_bad: list[str] = []
                ledger_issues: list[str] = []
                for ledger in ledgers:
                    parsed = parse_ledger(ledger)
                    ledger_ids |= parsed["ids"]
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
                plan_text = read(plan) if plan.is_file() else ""
                smoke = test_root / "00-稳定冒烟清单.md"
                smoke_text = read(smoke) if smoke.is_file() else ""
                planned_p0 = extract_p0_ids(plan_text, smoke_text)
                p0_missing = sorted(planned_p0 - ledger_ids)
                checks.append({"id": "p0-missing", "status": "fail" if p0_missing else "pass",
                               "detail": p0_missing[:10] if p0_missing else "all planned P0 present"})

        if args.mode == "report":
            report = test_root / "测试报告.md"
            if not report.is_file():
                blocked.append("缺少 测试/测试报告.md")
                checks.append({"id": "report-counts", "status": "blocked", "detail": "missing"})
                checks.append({"id": "report-verdict", "status": "blocked", "detail": "missing report"})
            else:
                parsed = parse_report(report, aggregate)
                checks.append({"id": "report-counts", "status": "fail" if parsed["issues"] else "pass", "detail": parsed["issues"][:10]})
                reported_verdict = parsed["verdict"]
                receipt_verdict = parsed["receipt_verdict"]
                checks.append({"id": "report-verdict", "status": "pass" if reported_verdict else "fail",
                               "detail": reported_verdict or "准出评估缺失/不可识别"})
                checks.append({"id": "p0-vs-verdict", "status": "fail" if p0_fail and reported_verdict in ("PASS", "CONDITIONAL") else "pass",
                               "detail": "P0 未过但报告写通过/有条件通过" if p0_fail and reported_verdict in ("PASS", "CONDITIONAL") else "consistent"})
                if not receipt_verdict:
                    checks.append({"id": "report-receipt", "status": "skip", "detail": "报告暂无回执；复跑时必须一致"})

        cov = parse_coverage(test_root) if test_root.is_dir() else {"issues": [], "missing": [], "seen": 0, "files": 0}
        cov_issues = list(cov["issues"])
        if args.mode in ("report", "coverage"):
            cov_issues += cov["missing"]
            if cov["files"] > 0 and cov["seen"] == 0:
                cov_issues.append("功能测试资产缺少设计点覆盖映射（覆盖三闸）")
        checks.append({"id": "coverage-map", "status": "fail" if cov_issues else "pass", "detail": cov_issues[:10]})
    else:
        receipts = [p for p in test_root.rglob("*.md") if ("回执" in p.name or "回写" in p.name) and is_current(p)] if test_root.is_dir() else []
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
            if "已回写" in text and "待回写" not in text and not re.search(r"(noteId|备注ID|回写时间|回执)", text, re.I):
                issues.append("声称已回写但缺少回执/noteId/时间")
            if "待回写" in text and not re.search(r"(export|无权限|待回写|原因)", text, re.I):
                issues.append("待回写缺少 export/无权限/原因")
            checks.append({"id": "writeback-receipt", "status": "fail" if issues else "pass", "detail": issues or str(receipt)})

    failed = [c for c in checks if c.get("status") == "fail"]
    blocked_checks = [c for c in checks if c.get("status") == "blocked"]
    if args.mode == "coverage":
        verdict = "FAIL" if failed else "PASS"
    elif args.mode == "writeback":
        verdict = "BLOCKED" if blocked or blocked_checks else ("FAIL" if failed else "PASS")
    else:
        if blocked or blocked_checks:
            verdict = "BLOCKED"
        elif failed or p0_fail or p0_missing:
            verdict = "FAIL"
        elif reported_verdict == "BLOCKED":
            verdict = "BLOCKED"
        elif reported_verdict == "FAIL":
            verdict = "FAIL"
        elif reported_verdict == "CONDITIONAL":
            verdict = "CONDITIONAL"
        elif any(aggregate.get(k, 0) for k in ("fail", "blocked", "pending", "not_run")):
            verdict = "CONDITIONAL" if args.mode == "execute" else "FAIL"
        elif args.mode == "report" and not reported_verdict:
            verdict = "FAIL"
        else:
            verdict = "PASS"

    now_dt = datetime.now(timezone.utc).astimezone()
    now = now_dt.isoformat(timespec="seconds")
    h = hashlib.sha256()
    for p in [test_root / "测试计划.md", test_root / "测试报告.md", test_root / "00-稳定冒烟清单.md"]:
        if p.is_file():
            h.update(read(p).encode("utf-8", errors="replace"))
    ledger_files = sorted(test_root.rglob("*.md")) if test_root.is_dir() else []
    for p in ledger_files:
        if "台账" in p.name and is_current(p):
            h.update(read(p).encode("utf-8", errors="replace"))
    gate_id = f"{args.mode}-{h.hexdigest()[:12]}"
    completion = {
        "gate_version": "2.0",
        "package": PACKAGE_NAME,
        "mode": args.mode,
        "gate_id": gate_id,
        "verdict": verdict,
        "counts": aggregate,
        "p0_fail": p0_fail,
        "p0_missing": p0_missing,
        "reported_verdict": reported_verdict,
        "receipt_verdict": receipt_verdict,
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

    out = write_receipt(project_root, args.mode, completion, primary=args.mode != "writeback")
    print(f"written: {out}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
