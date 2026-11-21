#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compare baseline vs implementation DOM metrics (control/text inventory + key targets).

The browser extractor (`verify/frontend/measure.template.mjs`) writes
`metrics-baseline.json` / `metrics-impl.json`; this script compares them and
writes `measure-diff.json` / `measure-diff.md`.

Scope (deliberately narrow, high ROI):
- visible interactive controls + headings/labels: missing control or changed
  accessible name is a parity defect;
- declared `targets`: computed styles (font-size/line-height/color/background/
  border-radius/padding/margin/gap) and box (top/left/width/height) with
  tolerances;
- no pixel diff, no canvas/chart internals, no every-element diff.

Usage:
    python frontend_measure.py --baseline .gate/frontend/metrics-baseline.json \
      --impl .gate/frontend/metrics-impl.json --config .gate/frontend/measure.json \
      --out .gate/frontend/measure-diff.json --md .gate/frontend/measure-diff.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

STYLE_KEYS = (
    "font-size", "line-height", "color", "background-color", "border-radius",
    "padding", "margin", "gap",
)
BOX_KEYS = ("top", "left", "width", "height")
DEFAULT_TOLERANCE = {"box": 2.0, "space": 1.0, "font": 0.5}


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top level must be object")
    return data


def norm_name(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def control_key(control: dict[str, Any]) -> str:
    return f"{str(control.get('role') or '').lower()}|{norm_name(control.get('name'))}"


def numeric_tokens(value: Any) -> list[float]:
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", str(value or ""))]


def color_norm(value: Any) -> str:
    text = str(value or "").strip().lower().replace(" ", "")
    match = re.fullmatch(r"rgba?\(([^)]+)\)", text)
    if match:
        parts = [p for p in match.group(1).split(",") if p]
        try:
            nums = [float(p) for p in parts]
        except ValueError:
            return text
        if len(nums) == 4 and abs(nums[3] - 1.0) >= 0.001:
            return "rgba(" + ",".join(f"{n:g}" for n in nums) + ")"
        return "rgb(" + ",".join(f"{n:g}" for n in nums[:3]) + ")"
    hex_match = re.fullmatch(r"#([0-9a-f]{3}|[0-9a-f]{6})", text)
    if hex_match:
        raw = hex_match.group(1)
        if len(raw) == 3:
            raw = "".join(ch * 2 for ch in raw)
        return "rgb(" + ",".join(str(int(raw[i:i + 2], 16)) for i in (0, 2, 4)) + ")"
    return text


def route_index(doc: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    out: dict[tuple[str, str], dict[str, Any]] = {}
    for route in doc.get("routes") or []:
        if not isinstance(route, dict):
            continue
        key = (norm_name(route.get("name")), norm_name(route.get("viewport")))
        if key[0]:
            out[key] = route
    return out


def compare_controls(base: dict[str, Any], impl: dict[str, Any],
                     problems: list[str], warnings: list[str], stats: dict[str, int]) -> None:
    base_controls = [c for c in base.get("controls") or [] if isinstance(c, dict)]
    impl_controls = [c for c in impl.get("controls") or [] if isinstance(c, dict)]
    base_keys = {control_key(c) for c in base_controls if control_key(c) != "|"}
    impl_keys = {control_key(c) for c in impl_controls if control_key(c) != "|"}
    missing = sorted(base_keys - impl_keys)
    extra = sorted(impl_keys - base_keys)
    stats["controls_baseline"] = len(base_keys)
    stats["controls_impl"] = len(impl_keys)
    stats["controls_missing"] = len(missing)
    stats["controls_extra"] = len(extra)
    for key in missing[:20]:
        role, name = key.split("|", 1)
        problems.append(f"缺少控件/文案: {role or '?'} {name or '?'}")
    for key in extra[:10]:
        role, name = key.split("|", 1)
        warnings.append(f"实现多出控件（确认是否需要）: {role or '?'} {name or '?'}")


def _num(value: Any) -> float | None:
    tokens = numeric_tokens(value)
    return tokens[0] if tokens else None


def compare_target(base: dict[str, Any], impl: dict[str, Any], tol: dict[str, float],
                   problems: list[str], stats: dict[str, int]) -> None:
    name = norm_name(base.get("name")) or "?"
    base_styles = base.get("styles") if isinstance(base.get("styles"), dict) else {}
    impl_styles = impl.get("styles") if isinstance(impl.get("styles"), dict) else {}
    for key in STYLE_KEYS:
        if key not in base_styles:
            continue
        bv, iv = base_styles.get(key), impl_styles.get(key)
        if key in ("color", "background-color"):
            if color_norm(bv) != color_norm(iv):
                problems.append(f"target {name}: {key} {bv!r} != {iv!r}")
            continue
        if key in ("font-size", "line-height"):
            bn, inn = _num(bv), _num(iv)
            if bn is None or inn is None:
                if str(bv).strip() != str(iv).strip():
                    problems.append(f"target {name}: {key} {bv!r} != {iv!r}")
                continue
            if abs(bn - inn) > tol.get("font", 0.5):
                problems.append(f"target {name}: {key} {bv} != {iv} (> {tol.get('font')}px)")
            continue
        bnums, inums = numeric_tokens(bv), numeric_tokens(iv)
        if len(bnums) != len(inums) or any(abs(a - b) > tol.get("space", 1.0)
                                           for a, b in zip(bnums, inums)):
            problems.append(f"target {name}: {key} {bv!r} != {iv!r} (> {tol.get('space')}px)")
    base_box = base.get("box") if isinstance(base.get("box"), dict) else {}
    impl_box = impl.get("box") if isinstance(impl.get("box"), dict) else {}
    for key in BOX_KEYS:
        if key not in base_box:
            continue
        try:
            diff = abs(float(base_box[key]) - float(impl_box.get(key)))
        except (TypeError, ValueError):
            problems.append(f"target {name}: box.{key} 不可比较 {base_box.get(key)!r} / {impl_box.get(key)!r}")
            continue
        if diff > tol.get("box", 2.0):
            problems.append(f"target {name}: box.{key} {base_box[key]} != {impl_box.get(key)} (> {tol.get('box')}px)")
    stats["targets_checked"] = stats.get("targets_checked", 0) + 1


def compare(baseline: dict[str, Any], impl: dict[str, Any],
            tolerance: dict[str, float] | None = None) -> dict[str, Any]:
    tol = dict(DEFAULT_TOLERANCE)
    tol.update(tolerance or {})
    problems: list[str] = []
    warnings: list[str] = []
    stats: dict[str, int] = {}
    base_routes = route_index(baseline)
    impl_routes = route_index(impl)
    if not base_routes:
        problems.append("baseline 无 routes（检查抽取配置/输出）")
    if not impl_routes:
        problems.append("impl 无 routes（检查抽取配置/输出）")
    for key, base_route in base_routes.items():
        impl_route = impl_routes.get(key)
        label = "/".join(part for part in key if part) or "?"
        if impl_route is None:
            problems.append(f"缺少路由/视口: {label}")
            continue
        compare_controls(base_route, impl_route, problems, warnings, stats)
        base_targets = [t for t in base_route.get("targets") or [] if isinstance(t, dict)]
        impl_targets = {
            norm_name(t.get("name")): t
            for t in impl_route.get("targets") or [] if isinstance(t, dict)
        }
        for target in base_targets:
            name = norm_name(target.get("name"))
            if not name:
                continue
            impl_target = impl_targets.get(name)
            if impl_target is None:
                problems.append(f"target {name}: 实现未找到")
                continue
            compare_target(target, impl_target, tol, problems, stats)
    diff = {
        "ok": not problems,
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "tolerance": tol,
        "problems": problems,
        "warnings": warnings,
        "stats": stats,
    }
    return diff


def render_md(diff: dict[str, Any]) -> str:
    lines = ["# 视觉几何/token 差异（measure-diff）", ""]
    lines.append(f"- 结论：{'通过' if diff.get('ok') else '不通过'}")
    stats = diff.get("stats") or {}
    if stats:
        lines.append(f"- 统计：{json.dumps(stats, ensure_ascii=False)}")
    problems = diff.get("problems") or []
    warnings = diff.get("warnings") or []
    lines.append("")
    lines.append("## 阻断项")
    lines.extend([f"- {p}" for p in problems] or ["- 无"])
    lines.append("")
    lines.append("## 提示项")
    lines.extend([f"- {w}" for w in warnings] or ["- 无"])
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Compare baseline/impl frontend metrics")
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--impl", required=True)
    ap.add_argument("--config", default="")
    ap.add_argument("--out", default=".gate/frontend/measure-diff.json")
    ap.add_argument("--md", default=".gate/frontend/measure-diff.md")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        baseline = load_json(Path(args.baseline))
        impl = load_json(Path(args.impl))
    except Exception as exc:  # noqa: BLE001
        print(f"MEASURE_INPUT_INVALID: {exc}")
        return 2
    tolerance = None
    if args.config:
        try:
            cfg = load_json(Path(args.config))
            tolerance = cfg.get("tolerance") if isinstance(cfg.get("tolerance"), dict) else None
        except Exception as exc:  # noqa: BLE001
            print(f"MEASURE_CONFIG_INVALID: {exc}")
            return 2
    diff = compare(baseline, impl, tolerance)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(diff, ensure_ascii=False, indent=2), encoding="utf-8")
    md = Path(args.md)
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text(render_md(diff), encoding="utf-8")
    if args.json:
        print(json.dumps(diff, ensure_ascii=False, indent=2))
    elif diff["ok"]:
        print(f"MEASURE PASS {json.dumps(diff['stats'], ensure_ascii=False)}")
    else:
        print("MEASURE BLOCKED")
        for item in diff["problems"][:20]:
            print(f"- {item}")
    return 0 if diff["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
