#!/usr/bin/env python3
"""Validate a functional execution record (intent-v1).

Usage: python validate_testcase.py <record.md>

Checks:
- record_format=intent-v1 or 场景与结果
- §0 记录信息 / §1 场景与结果 / §3 意图结论与本轮统计
- scene table headers: SC, INT/AC, 场景, 步骤, 预期/Oracle, 结果, 证据
- every row: valid status; intent id; non-empty scene/oracle/steps
- fail/block/pending: evidence present
- high-risk rows: evidence on pass, key depth hints? (manual)

Exit 0 = pass; 1 = errors; 2 = usage.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

STATUSES = {"未执行", "通过", "失败", "阻塞", "待实现", "不适用", "未本轮验证"}
FAIL = {"失败", "阻塞", "待实现"}
INT_RE = re.compile(r"\bINT-[A-Z0-9-]+\b")


def tables(block: str):
    lines = block.splitlines()
    out = []
    i = 0
    while i < len(lines) - 1:
        line = lines[i].strip()
        nxt = lines[i + 1].strip()
        if line.startswith("|") and re.match(r"^\|[\s:|-]+\|$", nxt):
            headers = [c.strip() for c in line.strip().strip("|").split("|")]
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append([c.strip() for c in lines[j].strip().strip("|").split("|")])
                j += 1
            out.append((headers, rows))
            i = j
        else:
            i += 1
    return out


def cell(row, headers, name):
    try:
        i = headers.index(name)
    except ValueError:
        i = next((j for j, h in enumerate(headers) if h.startswith(name)), -1)
    return row[i].strip() if 0 <= i < len(row) else ""


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate_testcase.py <record.md>", file=sys.stderr)
        return 2
    p = Path(sys.argv[1])
    if not p.is_file():
        print(f"ERROR: file not found {p}", file=sys.stderr)
        return 2
    text = p.read_text(encoding="utf-8-sig", errors="replace")
    errors: list[str] = []
    warns: list[str] = []

    if not (re.search(r"record_format\**\s*[:：]\s*`?intent-v1`?", text[:4000], re.I) or "场景与结果" in text):
        errors.append("缺 record_format=intent-v1 / 场景与结果")
    if "原文对账" not in text:
        errors.append("缺 §0 原文对账行")
    for h in ("## 0. 记录信息", "## 1. 场景与结果"):
        if h not in text:
            errors.append(f"缺章节 {h}")
    if not any(h in text for h in ("## 3. 意图结论", "## 3. 本轮结论")):
        errors.append("缺章节 ## 3. 意图结论与本轮统计")

    block = text.split("## 1. 场景与结果", 1)[1] if "## 1. 场景与结果" in text else text
    block = block.split("## 2.", 1)[0]
    table = None
    for headers, rows in tables(block):
        if "SC" in headers and "结果" in " ".join(headers):
            table = (headers, rows)
            break
    if not table:
        errors.append("§1 未找到场景表（需 SC/INT/场景/步骤/预期/Oracle/结果/证据）")
    else:
        headers, rows = table
        seen = 0
        for row in rows:
            if not row or not row[0] or row[0] in ("SC", "—", "---"):
                continue
            seen += 1
            sc = row[0]
            status = cell(row, headers, "结果")
            ev = cell(row, headers, "证据")
            intent = cell(row, headers, "INT/AC") or cell(row, headers, "INT")
            scene = cell(row, headers, "场景")
            steps = cell(row, headers, "步骤")
            oracle = cell(row, headers, "预期/Oracle")
            if status not in STATUSES:
                errors.append(f"{sc}: 结果不可识别 {status or '空'}")
            if not INT_RE.search(intent):
                errors.append(f"{sc}: 缺 INT-* 意图")
            for name, val in (("场景", scene), ("步骤", steps), ("Oracle", oracle)):
                if not val or val in ("—", "-", "…"):
                    errors.append(f"{sc}: 缺 {name}")
            if steps and steps not in ("—", "-"):
                n = len(re.findall(r"\d+\s*[.、)）]", steps)) or steps.count("→") + 1
                if n < 3:
                    warns.append(f"{sc}: 步骤过少（建议 3～7 步；至少 2 个动作）")
                if n > 7:
                    warns.append(f"{sc}: 步骤过多（建议 3～7 步）")
                if not re.search(r"字段|状态|码|提示|按钮|列表|详情|接口|Network|值|=", steps):
                    warns.append(f"{sc}: 步骤未见核对点（建议每步带字段/状态/码/提示等可观测对象）")
            if status in FAIL and (not ev or ev in ("—", "-", "无")):
                errors.append(f"{sc}: {status} 缺证据")
        if seen == 0:
            errors.append("§1 场景表无数据行")

    for w in warns:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    print(f"SUMMARY errors={len(errors)} warnings={len(warns)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

