#!/usr/bin/env python3
"""Validate an API/interface domain test-case document.

Usage: python validate_api_testcase.py <api-testcase.md> [--legacy]

Checks (errors):
- required sections 0-7 (headings)
- overview has case IDs; detail headings match
- contract table present
- coverage sections: no empty dimension cells (「｜」only / blank after dim)
- each case has 前置 / 请求要点 / 期望 / 清理 / 追溯
- expect table has 判定面 + 失败判定 (or 期望值)
- banned fillers that block follow-along / fake-pass

Warnings:
- no P0-Smoke
- depth not declared in §0
- fewer than 2 expect rows
- script section missing rows while cases claim 是

Exit 0 = pass (warnings OK); 1 = errors; 2 = usage.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

CASE_HEADING = re.compile(
    r"^###\s+([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d+)\s+(.+)$", re.M
)
REQUIRED_SECTIONS = [
    "## 0. 域信息",
    "## 1. 用例总览",
    "## 2. 契约表",
    "## 3. 覆盖对照",
    "## 4. 用例详情",
    "## 5. 脚本清单",
    "## 6. 覆盖摘要",
    "## 7. 评审",
]
# Allow slight title variants
SECTION_ALIASES = {
    "## 0. 域信息": ["## 0. 域信息", "## 0. 模块信息"],
    "## 7. 评审": ["## 7. 评审与变更", "## 7. 评审"],
}

BANNED_FILLERS = [
    "调用接口成功",
    "返回正常",
    "接口正常",
    "按场景数据",
    "本步结果可在页面核对",
    "仅 2xx 即通过",
]


def section(text: str, start: str, end: str | None) -> str:
    i = text.find(start)
    if i < 0:
        return ""
    i += len(start)
    j = text.find(end, i) if end else -1
    return text[i:j] if j >= 0 else text[i:]


def find_section_start(text: str, canonical: str) -> str | None:
    for alias in SECTION_ALIASES.get(canonical, [canonical]):
        if alias in text:
            return alias
    # prefix match on ## N.
    m = re.search(
        r"^##\s*" + re.escape(canonical.split(".", 1)[0].replace("## ", "")) + r"\.",
        text,
        re.M,
    )
    if m:
        # find full line
        line_start = text.rfind("\n", 0, m.start()) + 1
        line_end = text.find("\n", m.start())
        return text[line_start:line_end] if line_end > 0 else text[line_start:]
    return canonical if canonical in text else None


def has_required_sections(text: str) -> list[str]:
    missing = []
    for s in REQUIRED_SECTIONS:
        aliases = SECTION_ALIASES.get(s, [s])
        if any(a in text for a in aliases):
            continue
        m = re.match(r"##\s*(\d+)\.", s)
        n = m.group(1) if m else None
        if n and re.search(rf"^##\s*{n}\.", text, re.M):
            continue
        missing.append(f"MISSING_SECTION: {s}")
    return missing


def table_headers(block: str) -> list[list[str]]:
    headers: list[list[str]] = []
    lines = block.splitlines()
    for i, line in enumerate(lines[:-1]):
        if not line.strip().startswith("|"):
            continue
        nxt = lines[i + 1].strip()
        if not re.match(r"^\|[\s:|-]+\|$", nxt):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        headers.append(cells)
    return headers


def has_cols(headers: list[list[str]], cols: list[str]) -> bool:
    return any(all(any(col in cell for cell in h) for col in cols) for h in headers)


def numbered_rows(block: str) -> int:
    return sum(1 for ln in block.splitlines() if re.match(r"^\|\s*\d+\s*\|", ln))


def coverage_empty_cells(block: str) -> list[str]:
    """Flag dimension rows whose second cell is empty or only placeholder braces."""
    errs: list[str] = []
    for ln in block.splitlines():
        if not ln.strip().startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        dim, val = cells[0], cells[1]
        if dim in ("维度", "") or set(dim) <= set("-: "):
            continue
        if val == "" or val in {"—", "-", "…", "{…}", "`{…}`"}:
            errs.append(f"COVERAGE_EMPTY: 「{dim}」对照为空")
    return errs


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    legacy = "--legacy" in sys.argv
    if not args:
        print("USAGE: validate_api_testcase.py <api-testcase.md> [--legacy]")
        return 2
    path = Path(args[0])
    if not path.exists():
        print(f"FILE_NOT_FOUND: {path}")
        return 2
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    errors.extend(has_required_sections(text))

    # Locate sections by number
    def sec_n(n: int, next_n: int | None) -> str:
        m = re.search(rf"^##\s*{n}\.", text, re.M)
        if not m:
            return ""
        start = m.start()
        if next_n is None:
            return text[start:]
        m2 = re.search(rf"^##\s*{next_n}\.", text[start + 1 :], re.M)
        if not m2:
            return text[start:]
        return text[start : start + 1 + m2.start()]

    overview = sec_n(1, 2)
    contract = sec_n(2, 3)
    coverage = sec_n(3, 4)
    details = sec_n(4, 5)
    scripts = sec_n(5, 6)
    meta0 = sec_n(0, 1)

    if contract and "方法" not in contract and "path" not in contract.lower():
        errors.append("CONTRACT: §2 契约表缺少方法/path 列意向")
    if coverage:
        for e in coverage_empty_cells(coverage):
            (warnings if legacy else errors).append(e)
    else:
        errors.append("MISSING_SECTION: ## 3. 覆盖对照")

    if overview and "P0-Smoke" not in overview and "P0" not in overview:
        warnings.append("NO_P0: 总览未见 P0-Smoke/P0（接口冒烟建议 ≥1）")
    if meta0 and not re.search(r"depth|Depth", meta0, re.I):
        warnings.append("DEPTH: §0 未声明本轮 depth")

    overview_ids = set(
        re.findall(
            r"^\|\s*([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d+)\s*\|", overview, re.M
        )
    )
    detail_ids = {m.group(1) for m in CASE_HEADING.finditer(details)}

    if not detail_ids:
        errors.append("NO_CASES: §4 未找到 `### {ID} {标题}`")
    for cid in sorted(detail_ids - overview_ids):
        errors.append(f"CASE_NOT_IN_OVERVIEW: {cid}")
    for cid in sorted(overview_ids - detail_ids):
        # overview may include non-case rows; only flag if looks like case id pattern already collected
        if re.match(r"^[A-Z].*-\d+$", cid):
            errors.append(f"CASE_NOT_IN_DETAILS: {cid}")

    matches = list(CASE_HEADING.finditer(details))
    for idx, m in enumerate(matches):
        cid = m.group(1)
        start = m.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(details)
        block = details[start:end]
        for label in ["**前置", "**请求要点", "**清理", "**追溯"]:
            if label not in block:
                errors.append(f"{cid}: MISSING {label}")
        if "**期望" not in block and "失败判定" not in block:
            errors.append(f"{cid}: MISSING **期望与失败判定**")
        h = table_headers(block)
        if h and not has_cols(h, ["判定面"]):
            # allow 期望表 without exact header if 失败判定 present in prose table
            if "失败判定" not in block:
                errors.append(f"{cid}: EXPECTED_TABLE 需要判定面/失败判定")
        exp_block = section(block, "**期望", "**写后") or section(
            block, "**期望", "**清理"
        )
        if exp_block and numbered_rows(exp_block) < 2:
            warnings.append(f"{cid}: 期望判定行 <2（建议状态码+业务信号）")
        if re.search(r"脚本\s*\|\s*是", block) or re.search(
            r"\*\*脚本\*\*.*是", block
        ):
            if cid not in scripts:
                warnings.append(f"{cid}: 标「是」脚本但 §5 未见同 ID")
        for phrase in BANNED_FILLERS:
            if phrase in block:
                msg = f"{cid}: FILLER: 「{phrase}」"
                (warnings if legacy else errors).append(msg)
        # fake pass: “only 2xx means pass” (not “only-2xx-without-biz-signal = fail”)
        if re.search(
            r"(仅\s*2xx|只要\s*2xx)\s*(即|就)?\s*(通过|判过|算过)|2xx\s*即可通过",
            block,
        ):
            ctx_ok = re.search(
                r"禁.{0,8}仅\s*2xx|仅\s*2xx.{0,12}(失败|≠|不得)", block
            )
            if not ctx_ok:
                errors.append(f"{cid}: FAKE_PASS: 禁止仅 2xx 判通过")

    for w in warnings:
        print(f"WARN: {w}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        print(
            f"API_TESTCASE_VALIDATION_FAILED: {len(errors)} error(s), "
            f"{len(warnings)} warning(s)"
        )
        return 1
    print(
        f"API_TESTCASE_VALIDATION_OK: {len(detail_ids)} case(s), "
        f"{len(warnings)} warning(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
