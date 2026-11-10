"""Validate .gate/plan-coverage.md for L2+ plan/function coverage.

This is a lightweight machine gate, not a semantic reviewer:
- file exists;
- required sections exist;
- backend/function table has at least one real row when code/config changed;
- frontend table has at least one real row when page/static files changed (or explicit N/A);
- rows with pending/negative status are blocked;
- conclusion is exactly 通过, not 未通过/不通过/需修/阻塞, and the raw template enum is blocked.
"""
from __future__ import annotations

import re
from pathlib import Path

REQUIRED = ("## 1.", "## 2.", "## 3.", "## 4.", "## 5.")
HEADER_FIRST = {"方案条款/AC/SC", "页面/路由", "项"}
FRONTEND_SUFFIXES = (
    ".js", ".mjs", ".css", ".scss", ".sass", ".less", ".html",
    ".vue", ".tsx", ".jsx", ".svelte", ".astro",
)
FRONTEND_PREFIXES = ("static/", "templates/", "frontend/", "web/", "src/", "app/", "pages/", "components/", "views/")
BACKEND_SUFFIXES = (
    ".py", ".sql", ".yaml", ".yml", ".json", ".java", ".go", ".cs",
    ".php", ".rb", ".kt", ".rs", ".c", ".cc", ".cpp", ".scala",
)
BAD_STATUS_RE = re.compile(r"未完成|未通过|不通过|需修|阻塞|未覆盖|待填|待补|部分")
NEG_RE = re.compile(r"未通过|不通过|需修|阻塞|部分|未覆盖|缺口\s*[:：]?\s*[1-9]")
POS_RE = re.compile(r"^(?:通过|PASS|pass)(?:\s|$|[（(：:，,])", re.I)


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
        if not cells or cells[0] in HEADER_FIRST:
            continue
        joined = " ".join(cells)
        if "待填" in joined or "待补" in joined:
            continue
        if any(c and c not in ("—", "-", "不适用") for c in cells):
            return True
    return False


def _data_rows(block: str) -> list[list[str]]:
    return [cells for cells in _table_rows(block) if cells and cells[0] not in HEADER_FIRST]


def _bad_status_rows(block: str) -> list[str]:
    """Rows whose status is missing or explicitly not done must not pass."""
    bad: list[str] = []
    for cells in _table_rows(block):
        if not cells or not cells[0] or cells[0] in HEADER_FIRST:
            continue
        status = (cells[-1] or "").strip()
        if not status or BAD_STATUS_RE.search(status):
            bad.append(cells[0] or "?")
    return bad


def _explicit_na(block: str) -> bool:
    """Only a filled line starting with 不适用 counts as N/A.

    The template's instruction line (which starts with '>') must not count.
    """
    for line in block.splitlines():
        text = line.strip().lstrip("-* ").strip()
        if text.startswith("不适用"):
            return True
    return False


def _section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    nxt = text.find("\n## ", start + len(heading))
    return text[start:] if nxt < 0 else text[start:nxt]


def _conclusion_value(block: str) -> str:
    for line in block.splitlines():
        m = re.match(r"^[-*]?\s*覆盖结论\s*[:：]\s*(.+)$", line.strip())
        if m:
            return m.group(1).strip()
    return ""


def _conclusion_verdict(value: str) -> tuple[bool, str]:
    text = value.strip().strip("`*_ ").strip()
    text = re.sub(r"[。.!！]+$", "", text).strip()
    if not text:
        return False, "缺少「覆盖结论」行或结论为空"
    # Unfilled template enum: 通过 / 需修 / 阻塞
    if "/" in text and ("需修" in text or "阻塞" in text):
        return False, "结论仍为模板枚举（通过 / 需修 / 阻塞），未填写实际结论"
    normalized = re.sub(
        r"(无未覆盖|无缺口|无需修改|无需修|未覆盖\s*[:：]?\s*(?:无|0)|缺口\s*[:：]?\s*(?:无|0))",
        "",
        text,
    )
    if NEG_RE.search(normalized):
        return False, f"结论非通过：{text[:40]}"
    if POS_RE.match(normalized):
        return True, ""
    return False, f"结论须为 通过/需修/阻塞：{text[:40]}"


def validate(project_root: Path, level: str, files: list[str]) -> tuple[list[str], dict]:
    problems: list[str] = []
    stats = {"rows": 0, "conclusion": ""}
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
    if frontend_changed and not _has_real_row(frontend) and not _explicit_na(frontend):
        problems.append("plan-coverage.md 前端覆盖无有效行且未声明不适用")
    bad_backend = _bad_status_rows(backend)
    if bad_backend:
        problems.append("plan-coverage.md 后端/功能覆盖存在未完成行：" + ", ".join(bad_backend[:5]))
    bad_frontend = _bad_status_rows(frontend)
    if bad_frontend:
        problems.append("plan-coverage.md 前端覆盖存在未完成行：" + ", ".join(bad_frontend[:5]))
    conclusion = _conclusion_value(_section(text, "## 5."))
    stats["conclusion"] = conclusion
    ok, why = _conclusion_verdict(conclusion)
    if not ok:
        problems.append(f"plan-coverage.md 结论不通过：{why}")
    stats["rows"] = len(_data_rows(backend)) + len(_data_rows(frontend))
    return problems, stats
