#!/usr/bin/env python3
"""Validate frontend prototype-parity and route-coverage evidence.

Used by the completion gate and runnable standalone before the gate.

Expected artifacts:
  - {workroot}/00-governance/iteration-context.yaml  current iteration inputs/baseline/interactions/waves
  - .gate/frontend/parity-matrix.md   human matrix (decoded prototype or design baseline -> route/nav/component/field/state)
  - .gate/frontend/route-coverage.json  machine ledger (routes, menus, deep links, screenshots, console/network)
  - .gate/frontend/ui-audit.md        independent UI completion audit (A/B; --require-audit)
  - .gate/frontend/interactions.yaml + playwright-results.json  flow spec/results (when interactions=required)

The JSON ledger is the machine source of truth. Each route must point to a
desktop and a mobile screenshot; screenshot bytes must be unique per route.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception as exc:  # pragma: no cover
    print(f"FRONTEND_CONTEXT_YAML_UNAVAILABLE: {exc}")
    yaml = None

from validate_interactions import load_results, load_spec, validate_spec

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
PLACEHOLDERS = ("{主题}", "{…}", "{...}", "TODO", "待填", "示例路由")
AUDIT_SECTIONS = (
    "## 1. 路由清单",
    "## 2. 逐路由操作审计",
    "## 3. 二十维核验（与 design-qa 同 ID）",
    "## 4. 交互流审计",
    "## 5. 跨页一致性",
    "## 6. 后端可达",
    "## 7. 缺陷族、原型缺陷与真实数据",
    "## 8. 未覆盖",
    "## 9. 结论",
    "## 10. 独立复核",
)
AUDIT_PLACEHOLDERS = (
    "{主题}", "{任务ID}", "{…}", "{...}", "TODO", "待填",
    "{A/B}", "{pass/缺口}", "{证据}", "{/path}", "{flow-id}",
    "{PASS/DENIED}", "{通过 / 不通过}", "{无 / 列表}",
)
AUDIT_UNFINISHED = ("待验收", "待验证", "待补", "待验", "待确认", "未点通", "pending", "partial")
AUDIT_CONSISTENCY = ("术语", "状态词", "组件", "密度", "主操作", "日期", "空态")


def parse_ts(value: Any) -> float:
    if not value:
        return 0.0
    text = str(value).strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text).timestamp()
    except Exception:
        return 0.0


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_inside(evidence_dir: Path, rel: str) -> Path | None:
    raw = Path(str(rel))
    candidate = raw if raw.is_absolute() else (evidence_dir / raw)
    try:
        resolved = candidate.resolve()
        root = evidence_dir.resolve()
        if root not in resolved.parents and resolved != root:
            return None
        return resolved
    except OSError:
        return None


def _check_image(problems: list[str], evidence_dir: Path, rel: Any, label: str,
                 since: float) -> Path | None:
    if not isinstance(rel, str) or not rel.strip():
        problems.append(f"{label}: 缺少截图路径")
        return None
    path = resolve_inside(evidence_dir, rel)
    if path is None:
        problems.append(f"{label}: 截图路径越界或不可解析: {rel}")
        return None
    if not path.is_file():
        problems.append(f"{label}: 截图不存在: {rel}")
        return None
    if path.suffix.lower() not in IMAGE_SUFFIXES:
        problems.append(f"{label}: 不是图片: {rel}")
        return None
    if since and path.stat().st_mtime + 1 < since:
        problems.append(f"{label}: 截图早于本轮任务/验收清单: {rel}")
    return path


def _tier_problems(evidence_dir: Path) -> list[str]:
    """tier.json 必须存在且合法：分级只裁剪证据量，不裁剪质量底。"""
    path = evidence_dir / "tier.json"
    if not path.is_file():
        return ["缺 .gate/frontend/tier.json（实施开工前必须声明 A/B/C + reason + routes）"]
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return [f"tier.json 不可解析: {exc}"]
    if not isinstance(data, dict):
        return ["tier.json 顶层必须是对象"]
    tier = str(data.get("tier", "")).strip().upper()
    problems: list[str] = []
    if tier not in ("A", "B", "C"):
        problems.append("tier.json: tier 必须是 A/B/C")
    if not str(data.get("reason", "")).strip():
        problems.append("tier.json: reason 不能为空（为何可降级）")
    routes = data.get("routes")
    if not isinstance(routes, list) or not routes:
        problems.append("tier.json: routes 至少一条")
    return problems


BASELINES = {"prototype", "design_spec", "existing_page", "prd", "none"}
INTERACTION_MODES = {"required", "none"}


def _profile_text(project_root: Path) -> str:
    profile = project_root / "project-profile.md"
    return profile.read_text(encoding="utf-8", errors="ignore") if profile.is_file() else ""


def workroot(project_root: Path) -> str:
    """Read the instance workroot from project-profile.md §1; default docs/."""
    for line in _profile_text(project_root).splitlines():
        m = re.match(r"\|\s*workroot\s*\|\s*([^|]+)", line, re.IGNORECASE)
        if not m:
            m = re.search(r"workroot\s*[=:]\s*([^\s|`]+)", line, re.IGNORECASE)
        if m:
            raw = m.group(1).strip().strip("`")
            found = re.search(r"(docs(?:/[A-Za-z0-9._-]+)?)/?", raw)
            if found:
                return found.group(1).rstrip("/")
    return "docs"


def iteration_context_path(project_root: Path) -> Path | None:
    """Current iteration context: workroot/00-governance, then .gate fallback."""
    candidate = project_root / workroot(project_root) / "00-governance" / "iteration-context.yaml"
    if candidate.is_file():
        return candidate
    for fallback in (
        project_root / ".gate" / "frontend" / "iteration-context.yaml",
        project_root / ".gate" / "frontend" / "context.yaml",
    ):
        if fallback.is_file():
            return fallback
    return None


def load_iteration_context(project_root: Path) -> tuple[dict[str, Any] | None, Path | None]:
    path = iteration_context_path(project_root)
    if path is None:
        return None, None
    if yaml is None:
        return None, path
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return None, path
    return (data if isinstance(data, dict) else None), path


def _input_path(project_root: Path, raw: Any) -> Path | None:
    s = str(raw or "").strip().strip("`\"'")
    if not s or s.lower() in ("none", "na", "不适用"):
        return None
    path = Path(s)
    return path if path.is_absolute() else project_root / path


def _prototype_decode_problems(decoded: Path, proto: Path | None = None) -> list[str]:
    if not decoded.is_dir() or not any(p.is_file() for p in decoded.rglob("*")):
        return [f"未解码原型：{decoded} 为空（先跑 extract_prototype_modules.py）"]
    problems: list[str] = []
    structural = [decoded / name for name in ("prototype.json", "structure.md", "routes.json", "README.md")]
    if not any(p.is_file() for p in structural):
        problems.append(f"未解码原型：{decoded} 仅有截图/散件，缺少 prototype.json/structure.md/routes.json")
    manifest = decoded / "prototype.json"
    if manifest.is_file():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8-sig"))
        except Exception as exc:
            problems.append(f"prototype.json 不可解析: {exc}")
        else:
            if isinstance(data, dict):
                modules = data.get("modules") or []
                routes = data.get("routes") or []
                if not modules and not routes and not (decoded / "structure.md").is_file():
                    problems.append("prototype.json 解码为空（modules/routes 均空且无 structure.md）")
                recorded = str(data.get("source_sha256") or "").lower()
                if proto is not None and proto.is_file() and recorded:
                    if recorded != sha256_file(proto):
                        problems.append("prototype.json 的 source_sha256 与当前原型不一致（换版须重解码）")
    return problems


def _context_problems(project_root: Path) -> list[str]:
    """Validate the current iteration-context.yaml (per-iteration, not project config)."""
    ctx, path = load_iteration_context(project_root)
    if path is None:
        return [
            "缺本期 iteration-context.yaml：应在 {workroot}/00-governance/iteration-context.yaml "
            "（模板 rules/templates/10-planning/iteration-context-template.md）；不得把本期原型/交互路径写进项目档案"
        ]
    if ctx is None:
        return [f"iteration-context.yaml 不可解析: {path}"]
    problems: list[str] = []
    if str(ctx.get("schema", "")).strip() not in ("1", "1.0"):
        problems.append("iteration-context.yaml: schema 必须为 1")
    frontend = ctx.get("frontend")
    if not isinstance(frontend, dict):
        return problems + ["iteration-context.yaml: 缺 frontend（scope/baseline/interactions）"]
    scope = frontend.get("scope")
    if not isinstance(scope, list):
        return problems + ["iteration-context.yaml: frontend.scope 必须是列表（无 UI 写 [] ）"]
    if not scope:
        # No UI: prototype/interaction/baseline are not required.
        return problems
    baseline = str(frontend.get("baseline") or "").strip().lower()
    interactions = str(frontend.get("interactions") or "").strip().lower()
    if baseline not in BASELINES:
        problems.append(f"iteration-context.yaml: frontend.baseline 必须是 {'/'.join(sorted(BASELINES))}")
    if baseline == "none":
        problems.append("iteration-context.yaml: 有 UI 时 baseline 不能为 none（无原型用 design_spec/existing_page/prd）")
    if interactions not in INTERACTION_MODES:
        problems.append("iteration-context.yaml: frontend.interactions 必须是 required/none")
    inputs = ctx.get("inputs")
    if not isinstance(inputs, dict):
        return problems + ["iteration-context.yaml: 缺 inputs"]
    if baseline == "prototype":
        proto = _input_path(project_root, inputs.get("prototype"))
        if proto is None:
            problems.append("iteration-context.yaml: baseline=prototype 但 inputs.prototype 为空/none")
        elif not proto.is_file():
            problems.append(f"原型文件不存在: {proto}")
        else:
            recorded = str(inputs.get("prototype_sha256") or "").strip().lower()
            if recorded and recorded not in ("na", "none"):
                digest = sha256_file(proto)
                if recorded != digest:
                    problems.append("iteration-context.yaml: prototype_sha256 与当前原型不一致（换版须重解码/重对照）")
            problems.extend(_prototype_decode_problems(project_root / ".gate" / "prototype", proto))
    elif baseline == "design_spec":
        spec = _input_path(project_root, inputs.get("design_spec"))
        if spec is None:
            problems.append("iteration-context.yaml: baseline=design_spec 但 inputs.design_spec 为空/none")
        elif not spec.is_file():
            problems.append(f"设计说明不存在: {spec}")
    elif baseline == "prd":
        prd = _input_path(project_root, inputs.get("prd"))
        if prd is None:
            problems.append("iteration-context.yaml: baseline=prd 但 inputs.prd 为空/none")
        elif not prd.is_file():
            problems.append(f"PRD 不存在: {prd}")
    elif baseline == "existing_page":
        pass  # scope is the baseline; the audit records route/screenshot
    if interactions == "required":
        spec = _input_path(project_root, inputs.get("interaction_spec"))
        if spec is None:
            problems.append("iteration-context.yaml: interactions=required 但 inputs.interaction_spec 为空/none")
        elif not spec.is_file():
            problems.append(f"交互规格不存在: {spec}")
    waves = ctx.get("waves")
    if not isinstance(waves, list) or not waves:
        problems.append("iteration-context.yaml: waves 至少一条（单波次写 W1）")
    else:
        for index, wave in enumerate(waves, 1):
            if not isinstance(wave, dict) or not str(wave.get("id") or "").strip():
                problems.append(f"iteration-context.yaml: waves[{index}] 缺 id")
    domains = ctx.get("domains")
    if domains is not None and not isinstance(domains, dict):
        problems.append("iteration-context.yaml: domains 必须是对象")
    return problems


def context_problems(project_root: Path) -> list[str]:
    """Public wrapper used by the completion/pre-commit gates."""
    return _context_problems(project_root)


def _prototype_problems(project_root: Path) -> list[str]:
    """Backward-compatible alias: prototype rules now live in the iteration context."""
    return _context_problems(project_root)


def interactions_spec_path(project_root: Path) -> Path | None:
    """Resolve interaction spec from the current iteration context, then .gate fallback."""
    ctx, _path = load_iteration_context(project_root)
    if ctx:
        frontend = ctx.get("frontend") if isinstance(ctx.get("frontend"), dict) else {}
        scope = frontend.get("scope") if isinstance(frontend.get("scope"), list) else []
        mode = str(frontend.get("interactions") or "").strip().lower()
        if not scope or mode == "none":
            return None
        inputs = ctx.get("inputs") if isinstance(ctx.get("inputs"), dict) else {}
        resolved = _input_path(project_root, inputs.get("interaction_spec"))
        if resolved is not None:
            return resolved
    fallback = project_root / ".gate" / "frontend" / "interactions.yaml"
    return fallback if fallback.is_file() else None


def interactions_problems(project_root: Path, evidence_dir: Path,
                          require_results: bool = True) -> tuple[dict[str, Any] | None, list[str]]:
    """Load and validate the current interaction spec + flow results. Returns (spec, problems)."""
    ctx, _path = load_iteration_context(project_root)
    if ctx:
        frontend = ctx.get("frontend") if isinstance(ctx.get("frontend"), dict) else {}
        scope = frontend.get("scope") if isinstance(frontend.get("scope"), list) else []
        mode = str(frontend.get("interactions") or "").strip().lower()
        if not scope or mode == "none":
            return None, []
    spec_path = interactions_spec_path(project_root)
    if spec_path is None:
        return None, [
            "缺交互规格：本期 iteration-context.yaml 的 inputs.interaction_spec 为空/不存在，"
            "且无 `.gate/frontend/interactions.yaml`（模板 rules/templates/20-design/frontend-interaction-spec-template.md）"
        ]
    if not spec_path.is_file():
        return None, [f"交互规格不存在: {spec_path}"]
    try:
        spec = load_spec(spec_path)
    except Exception as exc:  # noqa: BLE001 - report exact parse failure
        return None, [f"interactions.yaml 不可解析: {exc}"]
    results = None
    results_path = evidence_dir / "playwright-results.json"
    if results_path.is_file():
        try:
            results = load_results(results_path)
        except Exception as exc:  # noqa: BLE001
            return spec, [f"playwright-results.json 不可解析: {exc}"]
    elif require_results:
        return spec, [
            "缺 playwright-results.json：交互流须先跑 flow suite（Playwright JSON reporter）"
        ]
    problems = validate_spec(spec, results, require_results=require_results)
    return spec, problems


def _section_text(text: str, heading: str) -> str:
    """Return the body between a heading and the next level-2 heading."""
    start = text.find(heading)
    if start < 0:
        return ""
    start += len(heading)
    tail = text[start:]
    nxt = re.search(r"\n## ", tail)
    return tail[: nxt.start()] if nxt else tail


def _prose_lines(text: str) -> list[str]:
    """Drop blockquote instructions so a filled audit is not judged by template prose."""
    return [line for line in text.splitlines() if line.strip() and not line.lstrip().startswith(">")]


def _route_block(section: str, route: str) -> str:
    chunks = re.split(r"(?m)^###\s+", section)[1:]
    for chunk in chunks:
        first = chunk.splitlines()[0] if chunk.splitlines() else ""
        if route in first:
            return chunk
    return ""


def _audit_routes(ev: Path, routes: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    if routes is not None:
        return routes
    coverage = ev / "route-coverage.json"
    if not coverage.is_file():
        return []
    try:
        data = json.loads(coverage.read_text(encoding="utf-8-sig"))
    except Exception:
        return []
    if not isinstance(data, dict) or not isinstance(data.get("routes"), list):
        return []
    skip = {str(item).strip() for item in (data.get("matrix_skip") or [])}
    return [
        r for r in data["routes"]
        if isinstance(r, dict)
        and str(r.get("route") or r.get("matrix_route") or "").strip() not in skip
    ]


def audit_problems(evidence_dir: Path | str, routes: list[dict[str, Any]] | None = None,
                   since: float = 0.0, interactions: dict[str, Any] | None = None,
                   require_interactions: bool = False) -> list[str]:
    """Validate .gate/frontend/ui-audit.md against the current audit template.

    The audit is the independent completion record: route blocks, the 20-dim
    comparison, interaction-flow results, cross-page consistency, backend
    reachability, prototype/data evidence, conclusion, and independent review.
    """
    ev = Path(evidence_dir)
    path = ev / "ui-audit.md"
    if not path.is_file():
        return ["缺少 ui-audit.md（A/B UI 须由独立 ui-auditor 逐路由/操作/交互审计）"]
    problems: list[str] = []
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    if len(text.strip()) < 800:
        problems.append("ui-audit.md 内容过短，疑似未填")
    for heading in AUDIT_SECTIONS:
        if heading not in text:
            problems.append(f"ui-audit.md 缺少章节: {heading}")
    for token in (*PLACEHOLDERS, *AUDIT_PLACEHOLDERS):
        if token in text:
            problems.append(f"ui-audit.md 仍含占位符: {token}")

    head = "\n".join(text.splitlines()[:25])
    if not re.search(r"task_id[：:]\s*\S+", head):
        problems.append("ui-audit.md 缺 task_id")
    tier_m = re.search(r"tier[：:]\s*([ABC])", head, re.I)
    if not tier_m:
        problems.append("ui-audit.md 缺 tier（A/B）")
    elif tier_m.group(1).upper() not in ("A", "B"):
        problems.append("ui-audit.md tier 只接受 A/B（C 档免独立审计）")

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = {cell.strip().lower() for cell in stripped.strip("|").split("|")}
        hit = cells & {t.lower() for t in AUDIT_UNFINISHED}
        if hit or cells & {"未测", "未验证"}:
            problems.append(f"ui-audit.md 存在未完成状态: {'/'.join(sorted(hit)) or '未测/未验证'}")
            break
    if "区块间距" not in text or "并排" not in text:
        problems.append("ui-audit.md 缺少同视口并排对照/区块间距证据")
    if since and path.stat().st_mtime + 1 < since:
        problems.append("ui-audit.md 早于本轮任务/代码变更（重新审计）")

    sec1 = _section_text(text, "## 1. 路由清单")
    if len(sec1.strip()) < 40:
        problems.append("ui-audit.md §1 路由清单未填")

    audit_routes = _audit_routes(ev, routes)
    sec2 = _section_text(text, "## 2. 逐路由操作审计")
    for route in audit_routes:
        route_name = str(route.get("route") or "").strip()
        matrix_route = str(route.get("matrix_route") or route_name).strip()
        if not matrix_route:
            continue
        block = _route_block(sec2, matrix_route)
        if not block:
            problems.append(f"ui-audit.md §2 缺少路由区块: {matrix_route}（### 标题含路由）")
            continue
        if len(block.strip()) < 80:
            problems.append(f"ui-audit.md §2 路由 {matrix_route} 区块未填")
        operations = route.get("operations")
        if isinstance(operations, list):
            for operation in operations:
                name = str(operation).strip()
                if name and name not in block:
                    problems.append(f"ui-audit.md §2 路由 {matrix_route} 缺操作: {name}")

    sec3 = _section_text(text, "## 3. 二十维对照")
    dim_routes = [
        str(r.get("matrix_route") or r.get("route") or "").strip()
        for r in audit_routes
        if str(r.get("matrix_route") or r.get("route") or "").strip()
    ]
    for matrix_route in dim_routes:
        block = _route_block(sec3, matrix_route)
        if not block:
            problems.append(f"ui-audit.md §3 缺少路由区块: {matrix_route}（每路由各 20 维）")
            continue
        for number in range(1, 21):
            m = re.search(rf"(?m)^\|\s*{number}\s*\|(.*)$", block)
            if not m:
                problems.append(f"ui-audit.md §3 {matrix_route} 缺第 {number} 维")
                continue
            cells = [c.strip() for c in m.group(1).strip().strip("|").split("|")]
            verdict = (cells[-1] if cells else "").strip().lower()
            if not (verdict.startswith("pass") or verdict.startswith("na") or verdict.startswith("通过")):
                problems.append(f"ui-audit.md §3 {matrix_route} 第 {number} 维结论须 pass/na+理由")
            elif verdict.startswith("na") and not re.search(r"[:：（(]\s*\S+", verdict):
                problems.append(f"ui-audit.md §3 {matrix_route} 第 {number} 维 na 缺理由")

    sec4 = _section_text(text, "## 4. 交互流审计")
    if interactions:
        for flow in interactions.get("flows") or []:
            if not isinstance(flow, dict):
                continue
            fid = str(flow.get("id") or "").strip()
            if not fid:
                continue
            if fid not in sec4:
                problems.append(f"ui-audit.md §4 缺交互流: {fid}")
                continue
            targets: list[str] = []
            for item in (flow.get("transitions") or []):
                if isinstance(item, dict) and item.get("id"):
                    targets.append(str(item["id"]))
            for item in (flow.get("invariants") or []):
                if isinstance(item, dict) and item.get("id"):
                    targets.append(str(item["id"]))
            for target in targets:
                if target not in sec4:
                    problems.append(f"ui-audit.md §4 缺 {fid}/{target}")
    elif require_interactions:
        problems.append("缺 interactions.yaml：A/B UI 须先有交互规格再审计")

    sec5 = _section_text(text, "## 5. 跨页一致性")
    missing = [item for item in AUDIT_CONSISTENCY if item not in sec5]
    if missing:
        problems.append(f"ui-audit.md §5 跨页一致性缺项: {missing}")

    sec6 = _section_text(text, "## 6. 后端可达")
    if not re.search(r"无写|不适用|non-ui", sec6) and "/" not in sec6:
        problems.append("ui-audit.md §6 后端可达未填（写端点→页面入口/结果）")

    sec7 = _section_text(text, "## 7. 缺陷族、原型缺陷与真实数据")
    if "无原型" not in text:
        if not all(word in sec7 for word in ("原型缺陷", "照搬", "择优")):
            problems.append("ui-audit.md §7 缺原型缺陷清单（照搬/择优）")
    if not all(word in sec7 for word in ("真实数据", "稀疏", "大数")):
        problems.append("ui-audit.md §7 缺真实数据三形态（稀疏/空/大数）")

    sec8 = _section_text(text, "## 8. 未覆盖")
    prose8 = _prose_lines(sec8)
    if not any(re.match(r"^\s*(?:-\s*)?无", line) for line in prose8):
        problems.append("ui-audit.md §8 未覆盖必须写「无」；有缺口=未完成")
    if any(token in "\n".join(prose8) for token in ("缺口", "待验", "待补", "未测")):
        problems.append("ui-audit.md §8 仍有未覆盖项")

    sec9 = _section_text(text, "## 9. 结论")
    if "不通过" in sec9 or "有条件" in sec9:
        problems.append("ui-audit.md 结论必须为通过（不通过/有条件=未完成）")
    elif not re.search(r"结论[：:]\s*(通过|pass)", sec9, re.I):
        problems.append("ui-audit.md 结论缺「通过」")

    sec10 = _section_text(text, "## 10. 独立复核")
    if "INDEPENDENT_REVIEW: PASS" not in sec10:
        problems.append("ui-audit.md 缺独立复核通过行 INDEPENDENT_REVIEW: PASS")
    if "DENIED" in sec10:
        problems.append("ui-audit.md 独立复核结论为 DENIED")
    if "复核人" not in sec10:
        problems.append("ui-audit.md §10 缺复核人（≠实施者）")
    return problems


def measure_problems(evidence_dir: Path | str, require: bool = False) -> list[str]:
    """Read measure-diff.json; a present-but-failed diff always blocks."""
    path = Path(evidence_dir) / "measure-diff.json"
    if not path.is_file():
        return ["缺少 measure-diff.json（视觉几何/token 未测量）"] if require else []
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001
        return [f"measure-diff.json 不可解析: {exc}"]
    if not isinstance(data, dict):
        return ["measure-diff.json 顶层必须是对象"]
    if data.get("ok") is True:
        return []
    issues = [str(x) for x in (data.get("problems") or []) if str(x).strip()]
    return [f"视觉度量: {x}" for x in issues[:20]] or ["measure-diff 未通过（ok != true）"]


def validate(evidence_dir: Path | str, since: float = 0.0, base_commit: str = "",
             require_matrix: bool = True, require_generated: bool = False,
             require_matrix_routes: bool = False,
             require_tier: bool = False, require_prototype: bool = False,
             require_context: bool = False,
             require_audit: bool = False, require_interactions: bool = False,
             require_measure: bool = False,
             project_root: Path | str | None = None) -> tuple[list[str], dict[str, Any]]:
    ev = Path(evidence_dir)
    problems: list[str] = []
    stats: dict[str, Any] = {"routes": 0, "menus": 0, "deep_links": 0, "screenshots": 0}

    if not ev.is_dir():
        return [f"证据目录不存在: {ev}"], stats

    root = Path(project_root) if project_root else ev.parent.parent
    if require_tier:
        problems.extend(_tier_problems(ev))
    if require_context or require_prototype:
        problems.extend(_context_problems(root))
    problems.extend(measure_problems(ev, require=require_measure))
    interaction_spec: dict[str, Any] | None = None
    if require_interactions:
        interaction_spec, interaction_issues = interactions_problems(root, ev)
        problems.extend(interaction_issues)
    flow_required = bool(interaction_spec)

    coverage_path = ev / "route-coverage.json"
    if not coverage_path.is_file():
        problems.append("缺少 route-coverage.json（前端路由/菜单/深链覆盖清单）")
        if require_audit:
            problems.extend(audit_problems(ev, routes=[], since=since,
                                           interactions=interaction_spec,
                                           require_interactions=flow_required))
        return problems, stats
    try:
        data = json.loads(coverage_path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        problems.append(f"route-coverage.json 不可解析: {exc}")
        if require_audit:
            problems.extend(audit_problems(ev, routes=[], since=since,
                                           interactions=interaction_spec,
                                           require_interactions=flow_required))
        return problems, stats
    if not isinstance(data, dict):
        return ["route-coverage.json 顶层必须是对象"], stats
    matrix_skip = {str(item).strip() for item in (data.get("matrix_skip") or [])}

    if str(data.get("schema", "")).strip() not in ("1", "1.0"):
        problems.append("route-coverage.json: schema 必须为 1")
    if str(data.get("result", "")).strip().lower() not in ("pass", "通过"):
        problems.append("route-coverage.json: result 必须为 pass")

    generated = parse_ts(data.get("generated_at"))
    if since and (not generated or generated + 1 < since):
        problems.append("route-coverage.json: generated_at 缺失或早于本轮任务开始")

    base = str(data.get("base_commit") or "").strip()
    if base_commit and base and not (base.startswith(base_commit) or base_commit.startswith(base)):
        problems.append(f"route-coverage.json: base_commit={base} 与本轮 {base_commit} 不一致")

    console = data.get("console")
    if not isinstance(console, dict):
        problems.append("route-coverage.json: 缺少 console 汇总（errors/failed_requests）")
    else:
        if int(console.get("errors", 0) or 0) > 0:
            problems.append(f"route-coverage.json: console errors={console.get('errors')}")
        if int(console.get("failed_requests", 0) or 0) > 0:
            problems.append(f"route-coverage.json: failed_requests={console.get('failed_requests')}")

    report_results: list[dict[str, Any]] = []
    report = ev / "report.json"
    if report.is_file():
        try:
            report_data = json.loads(report.read_text(encoding="utf-8-sig"))
            if isinstance(report_data, dict):
                for key in ("errors", "failed", "consoleErrors", "pageErrors", "failedRequests"):
                    value = report_data.get(key)
                    if isinstance(value, list) and value:
                        problems.append(f"report.json: {key} 非空（{len(value)}）")
                if isinstance(report_data.get("results"), list):
                    report_results = [r for r in report_data["results"] if isinstance(r, dict)]
        except Exception as exc:
            problems.append(f"report.json 不可解析: {exc}")

    # evidence.json 只能由 capture 脚本生成：它绑定“实际打开过、页面已就绪、截图哈希”。
    # 手写 route-coverage 仍可能蒙混，因此 L2+ 必须同时提供 evidence.json。
    evidence: dict[str, Any] | None = None
    evidence_path = ev / "evidence.json"
    if evidence_path.is_file():
        try:
            loaded = json.loads(evidence_path.read_text(encoding="utf-8-sig"))
            if isinstance(loaded, dict):
                evidence = loaded
            else:
                problems.append("evidence.json 顶层必须是对象")
        except Exception as exc:
            problems.append(f"evidence.json 不可解析: {exc}")
    elif require_generated:
        problems.append(
            "缺少 evidence.json：前端证据必须由 capture 命令生成（gate 运行 frontend.capture）；"
            "手写 parity-matrix/route-coverage 不算证据"
        )

    if evidence is not None:
        generated = parse_ts(evidence.get("generated_at"))
        if since and (not generated or generated + 1 < since):
            problems.append("evidence.json: generated_at 缺失或早于本轮任务开始")
        if not str(evidence.get("generator") or "").strip():
            problems.append("evidence.json: 缺少 generator（无法证明由 capture 生成）")
        console = evidence.get("console")
        if isinstance(console, dict):
            if int(console.get("errors", 0) or 0) > 0:
                problems.append(f"evidence.json: console errors={console.get('errors')}")
            if int(console.get("failed_requests", 0) or 0) > 0:
                problems.append(f"evidence.json: failed_requests={console.get('failed_requests')}")

    evidence_by_route: dict[str, dict[str, Any]] = {}
    if evidence is not None and isinstance(evidence.get("routes"), list):
        for item in evidence["routes"]:
            if isinstance(item, dict) and str(item.get("route") or "").strip():
                evidence_by_route[str(item["route"]).strip()] = item

    report_by_key: dict[str, dict[str, Any]] = {}
    for item in report_results:
        for key in (str(item.get("route") or "").strip(), str(item.get("hash") or "").strip()):
            if key:
                report_by_key[key] = item

    hash_owner: dict[str, str] = {}
    routes = data.get("routes")
    if not isinstance(routes, list) or not routes:
        problems.append("route-coverage.json: routes 不能为空")
        routes = []
    for index, route in enumerate(routes, 1):
        label = f"routes[{index}]"
        if not isinstance(route, dict):
            problems.append(f"{label}: 必须是对象")
            continue
        route_name = str(route.get("route") or "").strip()
        page = str(route.get("page") or "").strip()
        if not re.match(r"^(#?/|\.{1,2}/)", route_name):
            problems.append(f"{label}: route 必须以 /、#/ 或相对路径开头")
        if not page:
            problems.append(f"{label}: 缺少 page")
        if str(route.get("status", "")).strip().lower() not in ("pass", "通过"):
            problems.append(f"{label} {route_name or ''}: status 必须为 pass")
        for key in ("console_errors", "consoleErrors"):
            value = route.get(key)
            if value not in (None, 0, "0", ""):
                problems.append(f"{label} {route_name or ''}: {key}={value}")
        for key in ("failed_requests", "failedRequests"):
            value = route.get(key)
            if value not in (None, 0, "0", ""):
                problems.append(f"{label} {route_name or ''}: {key}={value}")
        desktop = _check_image(problems, ev, route.get("desktop"), f"{label} {route_name} desktop", since)
        mobile = _check_image(problems, ev, route.get("mobile"), f"{label} {route_name} mobile", since)
        for shot in (desktop, mobile):
            if shot is None:
                continue
            stats["screenshots"] += 1
            digest = sha256_file(shot)
            owner = hash_owner.get(digest)
            if owner:
                problems.append(f"{label} {route_name}: 截图与 {owner} 字节相同（疑似复用旧图/占位图）")
            else:
                hash_owner[digest] = f"{label} {route_name} ({shot.name})"
        if report_by_key:
            report_item = report_by_key.get(route_name)
            if not report_item:
                problems.append(f"{label} {route_name}: report.json 未覆盖该路由（未实际打开或 hash 不符）")
            else:
                if report_item.get("overflow") is True:
                    problems.append(f"{label} {route_name}: report.json overflow=true")
                if report_item.get("noAccess") is True:
                    problems.append(f"{label} {route_name}: report.json noAccess=true")
        if require_generated:
            entry = evidence_by_route.get(route_name)
            if not entry:
                problems.append(f"{label} {route_name}: evidence.json 未覆盖该路由（capture 未实际打开）")
            else:
                if entry.get("ready") is not True:
                    problems.append(f"{label} {route_name}: 页面未就绪 ready!=true（截图可能是骨架/空态）")
                for view, shot in (("desktop", desktop), ("mobile", mobile)):
                    item = entry.get(view)
                    if not isinstance(item, dict):
                        problems.append(f"{label} {route_name}: evidence.json 缺 {view} 截图记录")
                        continue
                    if shot is not None:
                        if Path(str(item.get("path") or "")).name != shot.name:
                            problems.append(f"{label} {route_name}: evidence.json {view} 路径与 route-coverage 不一致")
                        recorded = str(item.get("sha256") or "").strip().lower()
                        if recorded and recorded != sha256_file(shot):
                            problems.append(f"{label} {route_name}: {view} 截图哈希与 evidence.json 不符（图片被替换）")
                for key in ("console_errors", "failed_requests"):
                    if entry.get(key) not in (None, 0, "0", ""):
                        problems.append(f"{label} {route_name}: evidence.json {key}={entry.get(key)}")
    stats["routes"] = len(routes)

    menus = data.get("menus")
    if not isinstance(menus, list) or not menus:
        problems.append("route-coverage.json: menus 不能为空（一级/二级菜单清单）")
        menus = []
    for index, menu in enumerate(menus, 1):
        label = f"menus[{index}]"
        if not isinstance(menu, dict):
            problems.append(f"{label}: 必须是对象（label/route/visible/reachable）")
            continue
        if not str(menu.get("label") or "").strip():
            problems.append(f"{label}: 缺少 label")
        is_group = menu.get("group") is True or str(menu.get("level", "")) == "0"
        if not is_group and not re.match(r"^(#?/|\.{1,2}/)", str(menu.get("route") or "").strip()):
            problems.append(f"{label}: route 必须以 /、#/ 或相对路径开头（分组项标 group=true 可空）")
        if not (menu.get("visible") is True or menu.get("reachable") is True):
            problems.append(f"{label} {menu.get('label') or ''}: 不可见且不可滚动到达")
    stats["menus"] = len(menus)

    deep_links = data.get("deep_links")
    if not isinstance(deep_links, list) or not deep_links:
        problems.append("route-coverage.json: deep_links 不能为空（登记/新建/详情/授权等深链）")
        deep_links = []
    for index, link in enumerate(deep_links, 1):
        label = f"deep_links[{index}]"
        if not isinstance(link, dict):
            problems.append(f"{label}: 必须是对象（route/status）")
            continue
        if not re.match(r"^(#?/|\.{1,2}/)", str(link.get("route") or "").strip()):
            problems.append(f"{label}: route 必须以 /、#/ 或相对路径开头")
        if str(link.get("status", "")).strip().lower() not in ("pass", "通过"):
            problems.append(f"{label} {link.get('route') or ''}: status 必须为 pass")
    stats["deep_links"] = len(deep_links)

    matrix = ev / "parity-matrix.md"
    if require_matrix:
        if not matrix.is_file():
            problems.append("缺少 parity-matrix.md（原型对齐矩阵）")
        else:
            text = matrix.read_text(encoding="utf-8-sig", errors="replace")
            if len(text.strip()) < 300:
                problems.append("parity-matrix.md 内容过短，疑似未填")
            for token in PLACEHOLDERS:
                if token in text:
                    problems.append(f"parity-matrix.md 仍含占位符: {token}")
            unchecked = [line.strip() for line in text.splitlines()
                         if line.strip().startswith("- [ ]")]
            if unchecked:
                problems.append(f"parity-matrix.md 仍有未完成判据: {len(unchecked)} 项")
            unfinished = {
                "partial", "pending", "待验收", "待验证", "待补", "待验", "待确认", "部分",
            }
            for line in text.splitlines():
                stripped = line.strip()
                if not stripped.startswith("|"):
                    continue
                cells = {cell.strip().lower() for cell in stripped.strip("|").split("|")}
                hit = cells & unfinished
                if hit:
                    problems.append(
                        f"parity-matrix.md 存在未完成状态: {'/'.join(sorted(hit))}"
                    )
                    break

            headings = [line.strip() for line in text.splitlines()
                        if line.lstrip().startswith("#")]
            if require_matrix_routes:
                for route in routes:
                    route_name = str(route.get("route") or "").strip()
                    matrix_route = str(route.get("matrix_route") or route_name).strip()
                    if not route_name or route_name in matrix_skip:
                        continue
                    if not any(matrix_route in heading for heading in headings):
                        problems.append(
                            f"parity-matrix.md 缺少路由区块: {matrix_route}（需 ### 标题含路由）"
                        )
            for route in routes:
                route_name = str(route.get("route") or "").strip()
                matrix_route = str(route.get("matrix_route") or route_name).strip()
                operations = route.get("operations")
                if not route_name or not isinstance(operations, list) or not operations:
                    continue
                section: list[str] = []
                active = False
                for line in text.splitlines():
                    if line.lstrip().startswith("#"):
                        active = matrix_route in line
                    if active:
                        section.append(line)
                body = "\n".join(section)
                for operation in operations:
                    name = str(operation).strip()
                    if name and name not in body:
                        problems.append(
                            f"parity-matrix.md 路由 {matrix_route} 缺少操作: {name}"
                        )

    if require_audit:
        audit_routes = [
            r for r in routes
            if str(r.get("route") or r.get("matrix_route") or "").strip() not in matrix_skip
        ]
        problems.extend(audit_problems(ev, routes=audit_routes, since=since,
                                       interactions=interaction_spec,
                                       require_interactions=flow_required))

    return problems, stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate frontend parity/route coverage evidence")
    parser.add_argument("--evidence-dir", default=".gate/frontend")
    parser.add_argument("--since", default="", help="task started_at / acceptance mtime (ISO)")
    parser.add_argument("--base-commit", default="")
    parser.add_argument("--no-matrix", action="store_true")
    parser.add_argument("--require-matrix-routes", action="store_true",
                        help="要求 route-coverage 的每条路由在 parity-matrix 有 ### 区块标题")
    parser.add_argument("--require-generated", action="store_true",
                        help="要求 evidence.json（由 capture 生成）；A/B 门禁默认开启")
    parser.add_argument("--require-tier", action="store_true",
                        help="要求 tier.json 存在且合法（实施开工前声明）")
    parser.add_argument("--require-context", "--require-prototype", dest="require_context",
                        action="store_true",
                        help="要求本期 iteration-context.yaml（原型/设计基线/交互；A/B 必带）")
    parser.add_argument("--require-audit", action="store_true",
                        help="要求 ui-audit.md 结论通过，并与 route-coverage 的路由/操作对账")
    parser.add_argument("--require-interactions", action="store_true",
                        help="要求 interactions.yaml + 流用例结果；A/B UI 必带")
    parser.add_argument("--require-measure", action="store_true",
                        help="要求 measure-diff.json（视觉几何/token）；A 档有可运行基线时")
    parser.add_argument("--project-root", default="",
                        help="项目根（默认由 evidence-dir 推断）")
    parser.add_argument("--write", default="", help="把结果 JSON 写入该路径（实施出口回执）")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    problems, stats = validate(Path(args.evidence_dir), parse_ts(args.since),
                               args.base_commit, not args.no_matrix,
                               require_generated=args.require_generated,
                               require_matrix_routes=args.require_matrix_routes,
                               require_tier=args.require_tier,
                               require_context=args.require_context,
                               require_audit=args.require_audit,
                               require_interactions=args.require_interactions,
                               require_measure=args.require_measure,
                               project_root=args.project_root or None)
    if args.write:
        receipt = {
            "ok": not problems,
            "problems": problems,
            "stats": stats,
            "evidence_dir": str(args.evidence_dir),
            "checked_at": datetime.now().isoformat(timespec="seconds"),
        }
        target = Path(args.write)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.json:
        print(json.dumps({"ok": not problems, "problems": problems, "stats": stats},
                         ensure_ascii=False, indent=2))
    else:
        if problems:
            print("FRONTEND-PARITY BLOCKED")
            for item in problems:
                print(f"- {item}")
        else:
            print(f"FRONTEND-PARITY PASS routes={stats['routes']} menus={stats['menus']} "
                  f"deep_links={stats['deep_links']} screenshots={stats['screenshots']}")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
