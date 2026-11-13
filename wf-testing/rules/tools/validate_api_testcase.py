#!/usr/bin/env python3
"""Validate an API execution record (intent-v1).

Usage: python validate_api_testcase.py <api-record.md>

Checks:
- record_format=intent-v1 / 场景与结果
- §0 记录信息 / §1 契约清单 / §2 场景与结果 / §4 意图结论与本轮统计
- contract table: EP, method+path, success code/fields, source
- scene table: SC, EP, INT/AC, 维度, 请求, 预期, 结果, 证据
- §2.1 维表：每契约 EP 有行；处置=SC-* 或 不适用；depth 底线维
- 成功契约通过行：预期含字段级 Oracle（非仅 2xx/成功）
- fail/block/pending evidence; depth declared

Exit 0 = pass; 1 = errors; 2 = usage.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

STATUSES = {"未执行", "通过", "失败", "阻塞", "待实现", "不适用", "未本轮验证"}
FAIL = {"失败", "阻塞", "待实现"}
INT_RE = re.compile(r"\bINT-[A-Z0-9-]+\b")
SC_RE = re.compile(r"SC-[A-Z0-9-]+", re.I)
EP_RE = re.compile(r"^EP-[A-Z0-9-]+$", re.I)

# depth 底线维名（命中即认；别名用子串）
CORE_DIMS = ("成功契约", "无 token", "无token", "鉴权")
STANDARD_EXTRA = ("错误 METHOD", "错误METHOD", "METHOD")
FIELD_ORACLE_RE = re.compile(
    r"(data\.|字段|code\s*[=＝]|status\s*[=＝]|[=＝]\s*[`'\"]?\w|[a-zA-Z_][\w.]*\s*[=＝]|非空|为空)",
    re.I,
)
WEAK_EXPECT_RE = re.compile(r"^(?:200|2xx|成功|ok|通过|success)(?:[/+\s,，、]+(?:200|2xx|成功|ok|通过|success))*$", re.I)


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


def norm_dim(s: str) -> str:
    return re.sub(r"\s+", "", s or "").lower().replace("／", "/").replace("｜", "|")


def dim_match(cell_text: str, aliases: tuple[str, ...]) -> bool:
    n = norm_dim(cell_text)
    for a in aliases:
        if norm_dim(a) in n:
            return True
    return False


def detect_depth(text: str) -> str:
    head = text[:8000]
    m = re.search(r"depth\s*[=：:]\s*`?(core|standard|full)`?", head, re.I)
    if m:
        return m.group(1).lower()
    for line in head.splitlines():
        if "depth" not in line.lower():
            continue
        m = re.search(r"\b(core|standard|full)\b", line, re.I)
        if m:
            return m.group(1).lower()
    return ""


def disposition_ok(disp: str) -> tuple[bool, str]:
    d = (disp or "").strip()
    if not d or d in ("—", "-", "…", "待定"):
        return False, "空"
    if SC_RE.search(d):
        return True, "sc"
    if "不适用" in d or re.search(r"\bN/?A\b", d, re.I):
        # 须带依据（不止「不适用」二字）
        if len(re.sub(r"不适用|N/?A|[+\s：:·|]", "", d, flags=re.I)) < 2:
            return False, "不适用无依据"
        return True, "na"
    if "未装" in d or "本轮 depth" in d:
        return True, "deferred"
    return False, "非SC/非不适用"


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python validate_api_testcase.py <record.md>", file=sys.stderr)
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
    depth = detect_depth(text)
    if not depth:
        warns.append("未声明 depth（core/standard/full）")

    # §1 契约 EP
    block1 = text.split("## 1. 契约清单", 1)[1].split("## 2.", 1)[0] if "## 1. 契约清单" in text else ""
    contract_eps: list[str] = []
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
            ep = row[0].strip().strip("`")
            if EP_RE.match(ep):
                contract_eps.append(ep)
            for name in ("方法 + path", "成功码", "来源"):
                if not cell(row, headers, name):
                    errors.append(f"契约 {row[0]} 缺 {name}")

    # §2 场景
    block2 = text.split("## 2. 场景与结果", 1)[1].split("## 3.", 1)[0] if "## 2. 场景与结果" in text else ""
    scene_ids: set[str] = set()
    scene_by_ep_dim: dict[str, set[str]] = {}
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
            sc = row[0].strip().strip("`")
            scene_ids.add(sc)
            status = cell(row, headers, "结果")
            ev = cell(row, headers, "证据")
            intent = cell(row, headers, "INT/AC") or cell(row, headers, "INT")
            ep = cell(row, headers, "EP").strip().strip("`")
            dim = cell(row, headers, "维度") or cell(row, headers, "维")
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
            if ep and dim:
                scene_by_ep_dim.setdefault(ep, set()).add(dim)
            # 成功契约通过 → 字段级 Oracle
            if status == "通过" and dim_match(dim, ("成功契约", "成功")):
                exp = (expect or "").strip()
                if WEAK_EXPECT_RE.match(exp) or (not FIELD_ORACLE_RE.search(exp) and "code" not in exp.lower()):
                    # 允许「200 + code=0 + data.id」类；拒绝纯 200/成功
                    if not re.search(r"code|data\.|字段|非空|[=＝]", exp, re.I):
                        errors.append(f"{sc}: 成功契约通过但预期缺字段级 Oracle（禁仅 2xx/成功）")
        if seen == 0:
            errors.append("§2 场景表无数据行")

    # §2.1 维表
    dim_block = ""
    if "### 2.1" in block2:
        dim_block = block2.split("### 2.1", 1)[1]
    elif "维度适用" in block2:
        dim_block = block2.split("维度适用", 1)[1]
    dim_rows: list[tuple[str, str, str]] = []
    dim_eps: set[str] = set()
    dim_table = None
    for headers, rows in tables(dim_block if dim_block else ""):
        joined = " ".join(headers)
        if "EP" in headers and ("维度" in joined or "维" in joined) and ("处置" in joined or "SC" in joined or "适用" in joined):
            dim_table = (headers, rows)
            break
    if not dim_table:
        errors.append("缺 §2.1 维度适用性表（EP/维度/处置）")
    else:
        headers, rows = dim_table
        for row in rows:
            if not row or not row[0] or row[0] in ("EP", "—"):
                continue
            ep = row[0].strip().strip("`")
            dim = cell(row, headers, "维度") or cell(row, headers, "维")
            disp = cell(row, headers, "处置") or cell(row, headers, "SC") or cell(row, headers, "适用")
            if not EP_RE.match(ep):
                continue
            dim_eps.add(ep)
            ok, kind = disposition_ok(disp)
            if not dim or dim in ("—", "-", "…"):
                errors.append(f"§2.1 {ep}: 缺维度")
            if not ok:
                errors.append(f"§2.1 {ep}/{dim or '?'}: 处置无效（{kind}；须 SC-* 或 不适用+依据）")
            else:
                dim_rows.append((ep, dim, disp))
                if kind == "sc":
                    refs = set(SC_RE.findall(disp))
                    missing = refs - scene_ids
                    if missing:
                        errors.append(f"§2.1 {ep}/{dim}: 引用场景不存在 {','.join(sorted(missing))}")

        for ep in contract_eps:
            if ep not in dim_eps:
                errors.append(f"§2.1 缺契约 EP 行: {ep}")

        # depth 底线：每 EP 须有成功契约 + 无 token（或 N/A）；standard+ 另要 METHOD
        check_sets = [
            ("成功契约", ("成功契约", "成功")),
            ("无 token", ("无 token", "无token", "鉴权", "token")),
        ]
        if depth in ("standard", "full", ""):
            # 未声明 depth 时按 standard 底线机检（与迭代默认一致）
            check_sets.append(("错误 METHOD", ("错误 METHOD", "错误METHOD", "METHOD", "Content-Type")))
        by_ep: dict[str, list[tuple[str, str]]] = {}
        for ep, dim, disp in dim_rows:
            by_ep.setdefault(ep, []).append((dim, disp))
        for ep in contract_eps:
            rows_e = by_ep.get(ep, [])
            for label, aliases in check_sets:
                hit = [(d, disp) for d, disp in rows_e if dim_match(d, aliases)]
                if not hit:
                    errors.append(f"§2.1 {ep}: 缺 depth 底线维「{label}」（SC 或 不适用+依据）")

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
            iid = row[0].strip().strip("`")
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
