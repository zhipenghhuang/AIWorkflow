#!/usr/bin/env python3
"""Validate frontend prototype-parity and route-coverage evidence.

Used by the completion gate and runnable standalone before the gate.

Expected artifacts in the evidence directory:
  - parity-matrix.md          human matrix (decoded prototype -> route/nav/component/field/state)
  - route-coverage.json       machine ledger (routes, menus, deep links, screenshots, console/network)

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

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
PLACEHOLDERS = ("{主题}", "{…}", "{...}", "TODO", "待填", "示例路由")


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


def validate(evidence_dir: Path | str, since: float = 0.0, base_commit: str = "",
             require_matrix: bool = True, require_generated: bool = False,
             require_matrix_routes: bool = False) -> tuple[list[str], dict[str, Any]]:
    ev = Path(evidence_dir)
    problems: list[str] = []
    stats: dict[str, Any] = {"routes": 0, "menus": 0, "deep_links": 0, "screenshots": 0}

    if not ev.is_dir():
        return [f"证据目录不存在: {ev}"], stats

    coverage_path = ev / "route-coverage.json"
    if not coverage_path.is_file():
        return ["缺少 route-coverage.json（前端路由/菜单/深链覆盖清单）"], stats
    try:
        data = json.loads(coverage_path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return [f"route-coverage.json 不可解析: {exc}"], stats
    if not isinstance(data, dict):
        return ["route-coverage.json 顶层必须是对象"], stats

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
            matrix_skip = {str(item).strip() for item in (data.get("matrix_skip") or [])}
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
                        help="要求 evidence.json（由 capture 生成）；L2+ 门禁默认开启")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    problems, stats = validate(Path(args.evidence_dir), parse_ts(args.since),
                               args.base_commit, not args.no_matrix,
                               require_generated=args.require_generated,
                               require_matrix_routes=args.require_matrix_routes)
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
