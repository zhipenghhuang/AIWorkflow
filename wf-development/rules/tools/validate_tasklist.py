#!/usr/bin/env python3
"""Validate a task-list Markdown file generated from task-list-template.md.

Usage: python validate_tasklist.py <task-list.md> [--lenient]

Checks:
- required sections and summary-table columns
- unique task IDs, valid status
- every task has a task card with 验收标准/改动范围/verify/完成定义/方案条款
- 方案条款（SC）表存在（或标不适用）；每条 SC 有非空原文、可打开来源、落点、合法入口类型
- 来源文件可解析，来源 §章节在目标文档中存在（可打开，不靠自述）
- 方案设计要点 D-xx 全覆盖：来源文档的设计要点表逐条须被本清单引用
- 覆盖矩阵 §4.1 覆盖总表全部 R-xx，引用的 T-xx 必须存在
- 给了 --coverage 时：清单 SC ↔ `.gate/plan-coverage.md` 双向闭合
- dependency references resolve; no self-dependency
- every summary row has a requirement point (R-xx)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "## 1. 范围与约束",
    "## 2. 任务总表",
    "## 3. 任务卡",
    "## 4. 覆盖矩阵",
    "## 5. 检查点",
    "## 6. 变更记录",
    "## 7. 未决与假设",
]
REQUIRED_COLUMNS = ["ID", "阶段", "任务", "要求点", "优先级", "风险", "依赖", "并行", "负责人", "预估", "状态"]
STATUSES = {"未开始", "进行中", "阻塞", "待验收", "完成", "取消"}
ID_RE = re.compile(r"^T-\d+$")
RP_RE = re.compile(r"\bR-\d+\b")
SC_ID_RE = re.compile(r"^SC-\d+$")
SC_ENTRY_TYPES = {"create", "generate", "submit", "query-enrich", "na"}
SC_SOURCE_OK = re.compile(r"[/\\.]|§|#|章|节|画板|锚点|\.md|\.html|\.yaml|\.yml", re.I)
SC_PLACEHOLDER = {"", "—", "-", "待填", "待补", "…", "{…}", "...", "原文", "来源", "不适用"}
SOURCE_FILE_RE = re.compile(
    r"[^\s`'\"|｜，,；;：:（）()\[\]【】<>§]+?\.(?:md|markdown|html?|ya?ml|json|txt)", re.I
)
SECTION_REF_RE = re.compile(r"§\s*(\d+(?:\.\d+)*)")
HEADING_NUM_RE = re.compile(r"^#{1,6}\s*(\d+(?:\.\d+)*)")
DESIGN_POINT_ROW_RE = re.compile(r"^\|\s*(D-\d{2})\s*\|")
DESIGN_POINT_RE = re.compile(r"\bD-\d{2}\b")
SC_REF_RE = re.compile(r"\bSC-\d+\b")
NA_MARK = "不适用"


def project_bases(doc: Path, root: Path | None) -> list[Path]:
    """Directories a source path may be written relative to (root first)."""
    out: list[Path] = []

    def add(p: Path) -> None:
        try:
            rp = p.resolve()
        except OSError:
            return
        if rp.is_dir() and rp not in out:
            out.append(rp)

    if root is not None:
        add(root)
    p = doc.resolve().parent
    for _ in range(6):
        add(p)
        if p.parent == p:
            break
        p = p.parent
    add(Path.cwd())
    return out


def source_candidates(token: str, bases: list[Path]) -> list[Path]:
    t = token.replace("\\", "/")
    while t.startswith("./"):
        t = t[2:]
    cands: list[Path] = []
    if t.startswith("{workroot}/"):
        rest = t[len("{workroot}/"):]
        for sub in ("docs/development", "docs/product", "docs/testing", "docs"):
            for b in bases:
                cands.append(b / sub / rest)
        for b in bases:
            cands.append(b / rest)
        return cands
    for b in bases:
        cands.append(b / t)
    return cands


def resolve_source_file(token: str, bases: list[Path]) -> Path | None:
    if re.search(r"[{}…*?<>]", token):
        return None
    for cand in source_candidates(token, bases):
        try:
            if cand.is_file():
                return cand.resolve()
        except OSError:
            continue
    return None


def scan_doc(path: Path, cache: dict[Path, tuple[set[str], set[str]]]) -> tuple[set[str], set[str]]:
    """Return (numbered heading sections, design-point ids from table rows)."""
    if path in cache:
        return cache[path]
    sections: set[str] = set()
    points: set[str] = set()
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        cache[path] = (sections, points)
        return sections, points
    for line in lines:
        hm = HEADING_NUM_RE.match(line)
        if hm:
            sections.add(hm.group(1))
        dm = DESIGN_POINT_ROW_RE.match(line.strip())
        if dm:
            points.add(dm.group(1))
    cache[path] = (sections, points)
    return sections, points


def section_exists(sections: set[str], sec: str) -> bool:
    if sec in sections:
        return True
    return any(n.startswith(sec + ".") or sec.startswith(n + ".") for n in sections)


def split_row(line: str) -> list[str]:
    # Split a Markdown table row on unescaped pipes.
    cells: list[str] = []
    buf: list[str] = []
    escaped = False
    for ch in line.strip().strip("|"):
        if escaped:
            buf.append(ch)
            escaped = False
        elif ch == "\\":
            escaped = True
        elif ch == "|":
            cells.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    cells.append("".join(buf).strip())
    return cells


def main() -> int:
    argv = sys.argv[1:]
    positional = [a for a in argv if not a.startswith("--")]
    if not positional:
        print(
            "USAGE: validate_tasklist.py <task-list.md> [--lenient] "
            "[--root <project-root>] [--coverage <.gate/plan-coverage.md>]"
        )
        return 2
    path = Path(positional[0])
    lenient = "--lenient" in argv

    def opt(name: str) -> str:
        if name in argv:
            i = argv.index(name)
            if i + 1 < len(argv) and not argv[i + 1].startswith("--"):
                return argv[i + 1]
        return ""

    root_opt = Path(opt("--root")) if opt("--root") else None
    coverage_opt = Path(opt("--coverage")) if opt("--coverage") else None
    if not path.exists():
        print(f"TASKLIST_MISSING: {path}")
        return 1
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []
    bases = project_bases(path, root_opt)
    doc_cache: dict[Path, tuple[set[str], set[str]]] = {}
    source_docs: set[Path] = set()
    all_sc: set[str] = set()

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"MISSING_SECTION: {section}")

    # Summary table
    lines = text.splitlines()
    header_idx = None
    header: list[str] = []
    for i, line in enumerate(lines):
        if line.strip().startswith("|") and "ID" in line and "状态" in line and "任务" in line:
            header = split_row(line)
            header_idx = i
            break
    if header_idx is None:
        errors.append("MISSING_SUMMARY_TABLE: no table with ID/任务/状态")
        header = []
    else:
        for col in REQUIRED_COLUMNS:
            if col not in header:
                errors.append(f"MISSING_COLUMN: {col}")
        if len(header) != len(REQUIRED_COLUMNS):
            warnings.append(f"COLUMN_COUNT: header has {len(header)} columns, template expects {len(REQUIRED_COLUMNS)}")

    rows: list[list[str]] = []
    if header_idx is not None:
        for line in lines[header_idx + 2:]:
            if not line.strip().startswith("|"):
                if rows:
                    break
                continue
            rows.append(split_row(line))
    ids: list[str] = []
    deps: dict[str, list[str]] = {}
    parallel: dict[str, str] = {}
    summary_rps: set[str] = set()
    for row in rows:
        if not row or not row[0]:
            continue
        tid = row[0].strip("` ")
        if not ID_RE.match(tid):
            errors.append(f"BAD_ID: {tid!r} (expect T-01)")
            continue
        ids.append(tid)
        if len(row) < len(REQUIRED_COLUMNS):
            errors.append(f"BAD_ROW: {tid}: expected {len(REQUIRED_COLUMNS)} cells, got {len(row)}")
            continue
        status = row[header.index("状态")] if "状态" in header else ""
        if status and status not in STATUSES and not status.startswith("{"):
            errors.append(f"BAD_STATUS: {tid}: {status!r}")
        rp = row[header.index("要求点")] if "要求点" in header else ""
        if not RP_RE.search(rp) and not rp.startswith("{"):
            warnings.append(f"NO_RP: {tid}: {rp!r}")
        summary_rps.update(RP_RE.findall(rp))
        dep = row[header.index("依赖")] if "依赖" in header else ""
        deps[tid] = re.findall(r"T-\d+", dep)
        parallel[tid] = row[header.index("并行")] if "并行" in header else ""

    if len(ids) != len(set(ids)):
        errors.append("DUPLICATE_ID: summary table has duplicate IDs")

    # Dependency validation after all IDs are known (supports forward refs).
    id_set = set(ids)
    for tid, refs in deps.items():
        for ref in refs:
            if ref == tid:
                errors.append(f"SELF_DEPENDENCY: {tid}")
            elif ref not in id_set:
                errors.append(f"UNKNOWN_DEPENDENCY: {tid} -> {ref}")

    # Cycle detection (DFS; T-xx is small, no need for graph library).
    state: dict[str, int] = {}

    def visit(node: str, stack: list[str]) -> None:
        if state.get(node) == 1:
            cycle = " -> ".join(stack[stack.index(node):] + [node]) if node in stack else node
            errors.append(f"DEPENDENCY_CYCLE: {cycle}")
            return
        if state.get(node) == 2:
            return
        state[node] = 1
        for nxt in deps.get(node, []):
            if nxt in id_set:
                visit(nxt, stack + [node])
        state[node] = 2

    for tid in ids:
        visit(tid, [])

    # Task cards
    card_ids = re.findall(r"^###\s+(T-\d+)\b", text, flags=re.M)
    card_blocks: dict[str, str] = {}
    for tid in ids:
        if tid not in card_ids:
            errors.append(f"MISSING_CARD: {tid}")
    for tid in card_ids:
        if tid not in ids:
            errors.append(f"ORPHAN_CARD: {tid} not in summary table")
            continue
        start = text.find(f"### {tid}")
        next_card = text.find("\n### ", start + 1)
        block = text[start: next_card if next_card != -1 else len(text)]
        card_blocks[tid] = block
        for key in ("验收标准", "改动范围", "验证", "完成定义", "方案条款"):
            if key not in block:
                errors.append(f"CARD_FIELD: {tid}: missing {key}")
        # 方案条款（SC）是覆盖载体：允许「不适用」，但不允许整段缺失/无来源/空原文。
        sc_rows = [ln for ln in block.splitlines() if ln.strip().startswith("| SC-")]
        if not sc_rows and "不适用" not in block:
            errors.append(f"CARD_SC: {tid}: 缺少方案条款（SC）表或「不适用」理由")
        seen_sc: list[str] = []
        for line in sc_rows:
            cells = split_row(line)
            if len(cells) < 7:
                errors.append(
                    f"CARD_SC_ROW: {tid}: SC 行列数不足 7（SC|原文|来源|落点|入口类型|证据|状态）"
                )
                continue
            sid = cells[0].strip()
            if not SC_ID_RE.match(sid):
                errors.append(f"CARD_SC_ID: {tid}: {sid!r} 须为 SC-01 形式")
            elif sid in seen_sc:
                errors.append(f"CARD_SC_DUP: {tid}: 重复 {sid}")
            else:
                seen_sc.append(sid)
            gist = cells[1].strip()
            if gist in SC_PLACEHOLDER or gist.startswith("{"):
                errors.append(f"CARD_SC_GIST: {tid}: {sid} 原文要点为空或占位")
            source = cells[2].strip()
            if source in SC_PLACEHOLDER or source.startswith("{"):
                errors.append(f"CARD_SC_SOURCE: {tid}: {sid} 缺少来源")
            elif not SC_SOURCE_OK.search(source):
                errors.append(f"CARD_SC_SOURCE: {tid}: {sid} 来源须含路径或章节/画板/锚点")
            else:
                # 来源可打开：文件必须存在，§章节必须在目标文档里存在（禁自述覆盖）。
                for token in SOURCE_FILE_RE.findall(source):
                    doc = resolve_source_file(token, bases)
                    if doc is None:
                        errors.append(
                            f"CARD_SC_SOURCE_UNRESOLVED: {tid}: {sid} 来源文件不存在或不可解析：{token}"
                        )
                        continue
                    source_docs.add(doc)
                    if sid and SC_ID_RE.match(sid):
                        all_sc.add(sid)
                    sec = SECTION_REF_RE.search(source)
                    if sec:
                        sections, _ = scan_doc(doc, doc_cache)
                        if sections and not section_exists(sections, sec.group(1)):
                            errors.append(
                                f"CARD_SC_SOURCE_ANCHOR: {tid}: {sid} 来源章节 §{sec.group(1)} "
                                f"在 {token} 中不存在"
                            )
                        elif not sections:
                            warnings.append(
                                f"CARD_SC_ANCHOR_UNVERIFIABLE: {tid}: {sid} {token} 无编号标题，"
                                f"§{sec.group(1)} 无法机检（建议给文档加编号标题）"
                            )
            landing = cells[3].strip()
            if landing in SC_PLACEHOLDER or landing.startswith("{"):
                errors.append(f"CARD_SC_LANDING: {tid}: {sid} 实现落点为空或占位")
            entry_raw = cells[4].strip().lower()
            if entry_raw in (
                "create/generate/submit/query-enrich/na",
                "create|generate|submit|query-enrich|na",
            ):
                errors.append(f"CARD_SC_ENTRY: {tid}: {sid} 入口类型仍为模板枚举，未选定")
            else:
                entry_parts = [p.strip() for p in re.split(r"[/,|]", entry_raw) if p.strip()]
                if not entry_parts or not all(p in SC_ENTRY_TYPES for p in entry_parts):
                    errors.append(
                        f"CARD_SC_ENTRY: {tid}: {sid} 入口类型须为 "
                        f"create/generate/submit/query-enrich/na（可组合）"
                    )

    # 方案设计要点（D-xx）闭环：来源文档里的设计要点表须被本清单逐条引用。
    point_docs: dict[Path, set[str]] = {}
    for doc in source_docs:
        _, points = scan_doc(doc, doc_cache)
        if points:
            point_docs[doc] = points
    if point_docs:
        referenced = set(DESIGN_POINT_RE.findall(text))
        for doc, points in point_docs.items():
            missing = sorted(points - referenced)
            if missing:
                errors.append(
                    f"DESIGN_POINT_UNCOVERED: {doc.name} 的设计要点未被任何 SC 引用："
                    + ", ".join(missing)
                )

    # 覆盖矩阵 §4.1 与总表要求点对齐（双向：不漏、不凭空）。
    if "## 4. 覆盖矩阵" in text:
        matrix = text.split("## 4. 覆盖矩阵", 1)[1].split("## 5.", 1)[0]
        missing_rp = sorted(summary_rps - set(RP_RE.findall(matrix)))
        if missing_rp:
            errors.append(f"COVERAGE_MISSING_RP: 覆盖矩阵未列 {', '.join(missing_rp)}")
        unknown_tasks = sorted({t for t in re.findall(r"\bT-\d+\b", matrix) if t not in id_set})
        if unknown_tasks:
            errors.append(f"COVERAGE_UNKNOWN_TASK: 覆盖矩阵引用不存在的任务 {', '.join(unknown_tasks)}")

    # 计划 SC ↔ 方案覆盖矩阵双向闭合（由完成门在 L2+ 传入 --coverage）。
    if coverage_opt and coverage_opt.is_file():
        cov_text = coverage_opt.read_text(encoding="utf-8", errors="replace")
        cov_sc = set(SC_REF_RE.findall(cov_text))
        missing_sc = sorted(all_sc - cov_sc)
        if missing_sc:
            errors.append(
                "COVERAGE_MISSING_SC: `.gate/plan-coverage.md` 未覆盖清单 SC："
                + ", ".join(missing_sc)
            )
        fabricated = sorted(cov_sc - all_sc)
        if fabricated:
            errors.append(
                "COVERAGE_UNKNOWN_SC: `.gate/plan-coverage.md` 引用了清单不存在的 SC："
                + ", ".join(fabricated)
            )
    elif coverage_opt:
        warnings.append(f"COVERAGE_FILE_MISSING: {coverage_opt}")

    # Parallel safety: [P] tasks must not depend on each other and must have
    # disjoint file scopes; at most 3 [P] tasks per wave.
    p_ids = [tid for tid in ids if "[P]" in parallel.get(tid, "")]
    if len(p_ids) > 3:
        errors.append(f"PARALLEL_LIMIT: {len(p_ids)} [P] tasks > 3; split into waves")

    def reachable(start: str, target: str) -> bool:
        stack = [start]
        seen: set[str] = set()
        while stack:
            cur = stack.pop()
            for nxt in deps.get(cur, []):
                if nxt == target:
                    return True
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return False

    path_re = re.compile(r"[A-Za-z0-9_.@*?-]+(?:[\\/][A-Za-z0-9_.@*?-]+)+")
    scopes: dict[str, set[str]] = {}
    for tid in p_ids:
        block = card_blocks.get(tid, "")
        m = re.search(r"改动范围[^\n]*[：:]\s*(.+)", block)
        scope_line = m.group(1) if m else ""
        paths = {p.replace("\\", "/").lstrip("./") for p in path_re.findall(scope_line)}
        paths |= {
            p.replace("\\", "/").lstrip("./")
            for p in re.findall(r"`([^`]+)`", scope_line)
            if "/" in p or "\\" in p or "." in p
        }
        scopes[tid] = paths
        if not paths:
            errors.append(f"PARALLEL_SCOPE_UNKNOWN: {tid} [P] 无精确文件路径，无法证明与其它 [P] 互斥")

    for i, a in enumerate(p_ids):
        for b in p_ids[i + 1:]:
            if reachable(a, b) or reachable(b, a):
                errors.append(f"PARALLEL_DEPENDENCY_CONFLICT: {a} / {b} 互相依赖，不能并行")
            for pa in scopes.get(a, set()):
                for pb in scopes.get(b, set()):
                    if pa == pb or pa.startswith(pb + "/") or pb.startswith(pa + "/"):
                        errors.append(f"PARALLEL_FILE_CONFLICT: {a} / {b} 共享路径 {pa} / {pb}")

    for w in warnings:
        print(f"WARN: {w}")
    if errors and not lenient:
        for e in errors:
            print(f"ERROR: {e}")
        print(f"TASKLIST_VALIDATION_FAILED: {len(errors)} error(s)")
        return 1
    if errors and lenient:
        for e in errors:
            print(f"WARN(lenient): {e}")
    print(f"TASKLIST_VALIDATION_OK: {len(ids)} task(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
