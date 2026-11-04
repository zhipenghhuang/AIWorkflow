"""Validate .gate/plan-coverage.md for L2+ plan/function coverage.

This is a lightweight machine gate, not a semantic reviewer:
- file exists;
- required sections exist;
- backend/function table has at least one real row when code/config changed;
- frontend table has at least one real row when page/static files changed (or explicit N/A);
- conclusion is 通过, not 需修/阻塞;
- no placeholder-only rows.
"""
from __future__ import annotations

import re
from pathlib import Path

REQUIRED = ("## 1.", "## 2.", "## 3.", "## 4.", "## 5.")
FRONTEND_SUFFIXES = (
    ".js", ".mjs", ".css", ".scss", ".sass", ".less", ".html",
    ".vue", ".tsx", ".jsx", ".svelte", ".astro",
)
FRONTEND_PREFIXES = ("static/", "templates/", "frontend/", "web/", "src/", "app/", "pages/", "components/", "views/")
BACKEND_SUFFIXES = (
    ".py", ".sql", ".yaml", ".yml", ".json", ".java", ".go", ".cs",
    ".php", ".rb", ".kt", ".rs", ".c", ".cc", ".cpp", ".scala",
)


def _level_rank(level: str) -> int:
    m = re.search(r"L(\d)", str(level or ""))
    return int(m.group(1)) if m else 0


def _table_rows(block: str) -> list[list[str]]:
    rows = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells or all(re.fullmatch(r":?-{2,}:?", c or "") for c in cells):
            continue
        rows.append(cells)
    return rows


def _has_real_row(block: str) -> bool:
    for cells in _table_rows(block):
        if not cells or cells[0] in ("方案条款/AC/SC", "页面/路由", "项"):
            continue
        joined = " ".join(cells)
        if "待填" in joined or "待补" in joined:
            continue
        if any(c and c not in ("—", "-", "不适用") for c in cells):
            return True
    return False


def _section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    nxt = text.find("\n## ", start + len(heading))
    return text[start:] if nxt < 0 else text[start:nxt]


def validate(project_root: Path, level: str, files: list[str]) -> tuple[list[str], dict]:
    problems: list[str] = []
    stats = {"rows": 0}
    if _level_rank(level) < 2:
        return problems, stats
    path = project_root / ".gate" / "plan-coverage.md"
    if not path.is_file():
        return ["missing .gate/plan-coverage.md（L2+ 方案/功能覆盖矩阵）"], stats
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    for heading in REQUIRED:
        if heading not in text:
            problems.append(f"plan-coverage.md 缺少章节 {heading}")
    backend = _section(text, "## 2.")
    frontend = _section(text, "## 3.")
    code_changed = any(
        f.endswith(BACKEND_SUFFIXES)
        or f.startswith(("apps/", "config/", "scripts/"))
        for f in files
    )
    frontend_changed = any(
        f.startswith(FRONTEND_PREFIXES) or f.endswith(FRONTEND_SUFFIXES) for f in files
    )
    if code_changed and not _has_real_row(backend):
        problems.append("plan-coverage.md 后端/功能覆盖无有效行")
    if frontend_changed and not _has_real_row(frontend) and "不适用" not in frontend:
        problems.append("plan-coverage.md 前端覆盖无有效行且未声明不适用")
    conclusion = _section(text, "## 5.")
    if "需修" in conclusion or "阻塞" in conclusion:
        problems.append("plan-coverage.md 结论为需修/阻塞")
    if "通过" not in conclusion:
        problems.append("plan-coverage.md 结论未写通过")
    stats["rows"] = len(_table_rows(backend)) + len(_table_rows(frontend))
    return problems, stats
