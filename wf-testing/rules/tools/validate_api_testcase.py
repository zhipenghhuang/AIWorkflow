#!/usr/bin/env python3
"""Validate an API execution record (intent-v1).

Usage: python validate_api_testcase.py <api-record.md>

Checks:
- record_format=intent-v1 / 场景与结果
- §0 记录信息 / §1 契约清单 / §2 场景与结果 / §4 意图结论与本轮统计
- contract table: EP, method+path, success code/fields, source
- scene table: SC, EP, INT/AC, 维度, 请求, 预期, 结果, 证据
- fail/block/pending evidence; depth declared; only 2xx not considered pass (manual)

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
        print("Usage: validate_api_testcase.py <record.md>", file=sys.stderr)
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
    for h in ("## 0. 记录信息", "## 1. 契约清单", "## 2. 场景与结果"):
        if h not in text:
            errors.append(f"缺章节 {h}")
    if not any(h in text for h in ("## 4. 意图结论", "## 4. 本轮结论")):
        errors.append("缺章节 ## 4. 意图结论与本轮统计")
    if not re.search(r"depth\s*[：:]|\bdepth\b", text[:5000], re.I):
        warns.append("未声明 depth（core/standard/full）")

    block1 = text.split("## 1. 契约清单", 1)[1].split("## 2.", 1)[0] if "## 1. 契约清单" in text else ""
    t1 = None
    for headers, rows in tables(block1):
        if "EP" in headers and "方法" in " ".join(headers):
            t1 = (headers, rows)
            break
    if not t1:
        errors.append("§1 契约表缺失（需 EP/方法 + path/成功码/来源）")
    else:
        headers, rows = t1
        for row in rows:
            if not row or not row[0] or row[0] in ("EP", "—"):
                continue
            for name in ("方法 + path", "成功码", "来源"):
                if not cell(row, headers, name):
                    errors.append(f"契约 {row[0]} 缺 {name}")

    block2 = text.split("## 2. 场景与结果", 1)[1].split("## 3.", 1)[0] if "## 2. 场景与结果" in text else ""
    scene_ids: set[str] = set()
    table = None
    for headers, rows in tables(block2):
        if "SC" in headers and "结果" in " ".join(headers):
            table = (headers, rows)
            break
    if not table:
        errors.append("§2 未找到接口场景表（需 SC/EP/INT/维度/请求/预期/结果/证据）")
    else:
        headers, rows = table
        seen = 0
        for row in rows:
            if not row or not row[0] or row[0] in ("SC", "—"):
                continue
            seen += 1
            sc = row[0]
            scene_ids.add(sc)
            status = cell(row, headers, "结果")
            ev = cell(row, headers, "证据")
            intent = cell(row, headers, "INT/AC") or cell(row, headers, "INT")
            ep = cell(row, headers, "EP")
            req = cell(row, headers, "请求")
            expect = cell(row, headers, "预期")
            if status not in STATUSES:
                errors.append(f"{sc}: 结果不可识别 {status or '空'}")
            if not INT_RE.search(intent):
                errors.append(f"{sc}: 缺 INT-* 意图")
            if not ep:
                errors.append(f"{sc}: 缺 EP")
            for name, val in (("请求", req), ("预期", expect)):
                if not val or val in ("—", "-", "…"):
                    errors.append(f"{sc}: 缺 {name}")
            if status in FAIL and (not ev or ev in ("—", "-", "无")):
                errors.append(f"{sc}: {status} 缺证据")
        if seen == 0:
            errors.append("§2 场景表无数据行")

    # §4 意图结论：结论须回指实际场景
    itable = None
    for headers, rows in tables(text):
        joined = " ".join(headers)
        if "INT" in headers and "结论" in joined and "SC" not in headers:
            itable = (headers, rows)
            break
    if itable:
        headers, rows = itable
        for row in rows:
            if not row or not row[0] or row[0] in ("INT", "—"):
                continue
            iid = row[0].strip()
            if not INT_RE.fullmatch(iid):
                continue
            status = cell(row, headers, "结论")
            if status == "不适用":
                continue
            ref = cell(row, headers, "场景 ID") or cell(row, headers, "场景")
            refs = set(re.findall(r"SC-[A-Z0-9-]+", ref, re.I))
            if not refs:
                errors.append(f"意图 {iid}: 结论 {status or '空'} 未指向场景（场景 ID 必填）")
            elif not (refs & scene_ids):
                errors.append(f"意图 {iid}: 引用的场景不存在 {ref}")

    for w in warns:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    print(f"SUMMARY errors={len(errors)} warnings={len(warns)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
