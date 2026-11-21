#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate the UI interaction spec (`interactions.yaml`) and its flow tests.

The spec is the pre-code oracle for interaction behaviour: states, transitions,
guards, effects, invariants, component contract, persistence, and the test cases
that cover them. This validator is intentionally strict for A/B UI: every
transition and every class-required invariant must have a passing case in the
Playwright JSON report.

Usage:
    python validate_interactions.py --spec .gate/frontend/interactions.yaml
    python validate_interactions.py --spec ... --results .gate/frontend/playwright-results.json --require-results
    python validate_interactions.py --spec ... --inventory .gate/prototype/inventory.json

Exit code 0 = pass; 1 = problems; 2 = usage/parse error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception as exc:  # pragma: no cover
    print(f"INTERACTIONS_VALIDATOR_UNAVAILABLE: {exc}")
    raise SystemExit(2)

CLASSES = {"overlay", "list", "form", "linked", "static"}
REQUIRED_INVARIANTS: dict[str, tuple[str, ...]] = {
    "overlay": (
        "cancel-no-write",
        "reopen-reset",
        "submit-lock",
        "failure-keep-open",
        "focus-return",
    ),
    "list": (
        "filter-page-reset",
        "refresh-preserve",
        "selection-scope",
        "bulk-partial",
    ),
    "form": (
        "validate-timing",
        "first-error-focus",
        "submit-lock",
        "leave-guard",
        "draft",
    ),
    "linked": ("clear", "disable", "reload", "default", "reset"),
}
PLACEHOLDERS = ("{…}", "{...}", "TODO", "待填", "{主题}", "{任务ID}", "{flow-id}")
ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")
TARGET_RE = re.compile(r"^[TI]\d+$")
CASE_TAG_RE = re.compile(r"\[CASE:([a-z0-9-]+)\]", re.I)
FLOW_TAG_RE = re.compile(r"\[FLOW:([a-z0-9-]+)\]", re.I)


def _text(value: Any) -> str:
    return str(value or "").strip()


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def load_spec(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("interactions.yaml 顶层必须是对象")
    return data


def _iter_specs(data: Any):
    """Yield spec title/status pairs from Playwright JSON reporter output."""
    if not isinstance(data, dict):
        return
    for spec in _list(data.get("specs")):
        if not isinstance(spec, dict):
            continue
        title = _text(spec.get("title"))
        tests = _list(spec.get("tests"))
        if not tests:
            continue
        statuses = [_text(t.get("status")).lower() for t in tests if isinstance(t, dict)]
        # expected = passed; skipped = skipped; unexpected/flaky = fail
        if statuses and all(s == "expected" for s in statuses):
            status = "pass"
        elif statuses and all(s in ("expected", "skipped") for s in statuses) and "skipped" in statuses:
            status = "skip"
        else:
            status = "fail"
        yield title, status
    for suite in _list(data.get("suites")):
        yield from _iter_specs(suite)


def load_results(path: Path) -> dict[str, str]:
    """case_id -> pass|skip|fail, from `[CASE:<id>]` in spec titles."""
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    out: dict[str, str] = {}
    for title, status in _iter_specs(data):
        ids = CASE_TAG_RE.findall(title)
        for case_id in ids:
            key = case_id.strip().lower()
            prev = out.get(key)
            if prev is None:
                out[key] = status
            elif prev == "fail":
                continue
            elif status == "fail":
                out[key] = "fail"
            elif prev == "skip" and status == "pass":
                out[key] = "pass"
            # pass + skip keeps pass; skip + skip keeps skip
        # Titles without [CASE:] are advisory only.
    return out


def _check_flow(flow: dict[str, Any], index: int, problems: list[str]) -> tuple[str, set[str], set[str]]:
    label = f"flows[{index}]"
    fid = _text(flow.get("id"))
    if not fid or not ID_RE.match(fid):
        problems.append(f"{label}: id 必须是 a-z0-9- 短横线格式")
        fid = fid or f"flow-{index}"
    cls = _text(flow.get("class")).lower()
    if cls not in CLASSES:
        problems.append(f"{fid}: class 必须是 {'/'.join(sorted(CLASSES))}")
    source = _text(flow.get("source"))
    if not source:
        problems.append(f"{fid}: 缺 source（原型 handler/PRD 条款/现有实现路径）")
    entry = _dict(flow.get("entry"))
    if cls != "static" and not _text(entry.get("control")):
        problems.append(f"{fid}: entry.control 不能为空（可见控件名/role）")
    if cls != "static" and not _text(entry.get("guard", "")) and cls in ("overlay", "form"):
        # guard may be "none"; but it must be explicit for destructive/overlay flows
        problems.append(f"{fid}: entry.guard 必须显式写（无守卫写 none）")

    transitions = _list(flow.get("transitions"))
    invariants = _list(flow.get("invariants"))
    tests = _list(flow.get("tests"))
    tid: set[str] = set()
    iid: set[str] = set()

    if cls != "static":
        states = [_text(s) for s in _list(flow.get("states")) if _text(s)]
        if len(states) < 2:
            problems.append(f"{fid}: states 至少 2 个（含关闭/初始态）")
        if not transitions:
            problems.append(f"{fid}: transitions 不能为空")
    for t in transitions:
        if not isinstance(t, dict):
            problems.append(f"{fid}: transition 必须是对象")
            continue
        xid = _text(t.get("id"))
        if not TARGET_RE.match(xid) or not xid.startswith("T"):
            problems.append(f"{fid}: transition id 须为 T1/T2…，实际 {xid!r}")
        elif xid in tid:
            problems.append(f"{fid}: transition id 重复 {xid}")
        tid.add(xid)
        for key in ("from", "event", "to"):
            if not _text(t.get(key)):
                problems.append(f"{fid}/{xid or '?'}: transition 缺 {key}")
        if _text(t.get("to")) and _text(t.get("from")) and _text(t.get("to")) == _text(t.get("from")):
            # self-loops are legitimate but must carry an effect; otherwise it is a no-op claim
            if not _text(t.get("effect")):
                problems.append(f"{fid}/{xid}: 自环迁移必须写 effect")
    for inv in invariants:
        if not isinstance(inv, dict):
            problems.append(f"{fid}: invariant 必须是对象（id/name/check）")
            continue
        xid = _text(inv.get("id"))
        name = _text(inv.get("name"))
        if xid and (not TARGET_RE.match(xid) or not xid.startswith("I")):
            problems.append(f"{fid}: invariant id 须为 I1/I2…，实际 {xid!r}")
        if not xid:
            # allow name-only; derive a stable id for coverage checks
            xid = f"I{len(iid) + 1}"
        if xid in iid:
            problems.append(f"{fid}: invariant id 重复 {xid}")
        iid.add(xid)
        if not name:
            problems.append(f"{fid}/{xid}: invariant 缺 name")
        if not _text(inv.get("check")):
            problems.append(f"{fid}/{xid}: invariant 缺 check（可观测断言）")

    required = REQUIRED_INVARIANTS.get(cls, ())
    declared_names = {_text(i.get("name")) for i in invariants if isinstance(i, dict)}
    exceptions = _dict(flow.get("class_exceptions"))
    for name in required:
        if name not in declared_names:
            if not _text(exceptions.get(name)):
                problems.append(
                    f"{fid}: {cls} 类必填不变量缺 {name}（如确定不适用，在 class_exceptions 写理由）"
                )

    if cls == "static":
        if transitions or invariants or tests:
            problems.append(f"{fid}: static 不写 transitions/invariants/tests")
        return fid, tid, iid

    if not tests:
        problems.append(f"{fid}: tests 不能为空（每条迁移/不变量至少一条）")
    covered: set[str] = set()
    case_ids: set[str] = set()
    for t in tests:
        if not isinstance(t, dict):
            problems.append(f"{fid}: test 必须是对象（id/covers）")
            continue
        cid = _text(t.get("id"))
        if not cid or not ID_RE.match(cid):
            problems.append(f"{fid}: test id 必须是 a-z0-9- 短横线格式")
        elif cid in case_ids:
            problems.append(f"{fid}: test id 重复 {cid}")
        case_ids.add(cid)
        covers = [_text(x) for x in _list(t.get("covers")) if _text(x)]
        if not covers:
            problems.append(f"{fid}/{cid}: covers 不能为空")
        for target in covers:
            if target not in tid and target not in iid:
                problems.append(f"{fid}/{cid}: covers 指向不存在的迁移/不变量 {target}")
            covered.add(target)
    missing = sorted((tid | iid) - covered)
    if missing:
        problems.append(f"{fid}: 迁移/不变量未被任何用例覆盖: {missing}")

    component = _dict(flow.get("component"))
    if cls in ("overlay", "form"):
        if not _text(component.get("name")):
            problems.append(f"{fid}: 缺 component.name（复用组件契约）")
        if not _list(component.get("controlled")):
            problems.append(f"{fid}: 缺 component.controlled（受控字段）")
        if not _list(component.get("callbacks")):
            problems.append(f"{fid}: 缺 component.callbacks（回调归属）")
        if not _text(component.get("api_owner")):
            problems.append(f"{fid}: 缺 component.api_owner（接口调用层级）")

    persistence = _dict(flow.get("persistence"))
    if cls in ("list", "form", "linked") and not persistence:
        problems.append(f"{fid}: 缺 persistence（url/reload/back 至少写一项或 na+理由）")
    return fid, tid, iid


def validate_spec(
    spec: dict[str, Any],
    results: dict[str, str] | None = None,
    inventory: dict[str, Any] | None = None,
    require_results: bool = False,
) -> list[str]:
    problems: list[str] = []
    if str(spec.get("schema", "")).strip() not in ("1", "1.0"):
        problems.append("interactions.yaml: schema 必须为 1")
    surface = _text(spec.get("surface"))
    if not surface:
        problems.append("interactions.yaml: 缺 surface（路由/页面）")
    flows = _list(spec.get("flows"))
    if not flows:
        problems.append("interactions.yaml: flows 不能为空")
        return problems

    seen: set[str] = set()
    all_targets: set[str] = set()
    all_cases: set[str] = set()
    flow_ids: list[str] = []
    for index, flow in enumerate(flows, 1):
        if not isinstance(flow, dict):
            problems.append(f"flows[{index}]: 必须是对象")
            continue
        fid, _tid, _iid = _check_flow(flow, index, problems)
        if fid in seen:
            problems.append(f"flows[{index}]: flow id 重复 {fid}")
        seen.add(fid)
        flow_ids.append(fid)
        for t in _list(flow.get("transitions")):
            if isinstance(t, dict) and _text(t.get("id")):
                all_targets.add(_text(t.get("id")))
        for inv in _list(flow.get("invariants")):
            if isinstance(inv, dict) and _text(inv.get("id")):
                all_targets.add(_text(inv.get("id")))
        for t in _list(flow.get("tests")):
            if isinstance(t, dict) and _text(t.get("id")):
                all_cases.add(_text(t.get("id")).lower())

    if require_results and results is None:
        problems.append("缺 playwright-results.json：交互流须有用例结果（先跑 flow suite）")
    if results is not None:
        for case_id in sorted(all_cases):
            status = results.get(case_id)
            if status is None:
                problems.append(f"用例未在 playwright-results.json 出现: {case_id}")
            elif status == "skip":
                problems.append(f"用例被 skip: {case_id}")
            elif status != "pass":
                problems.append(f"用例未通过: {case_id} ({status})")

    # Inventory coverage is checked by the gate when a stable inventory is available;
    # accessible names are project-specific, so this validator does not hard-fail on them.
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate interactions.yaml and flow test results")
    ap.add_argument("--spec", required=True)
    ap.add_argument("--results", default="")
    ap.add_argument("--inventory", default="")
    ap.add_argument("--require-results", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.is_file():
        print(f"INTERACTIONS_MISSING: {spec_path}")
        return 1
    try:
        spec = load_spec(spec_path)
    except Exception as exc:  # noqa: BLE001 - report exact parse failure
        print(f"INTERACTIONS_PARSE: {exc}")
        return 2
    results = None
    if args.results:
        path = Path(args.results)
        if not path.is_file():
            print(f"INTERACTIONS_RESULTS_MISSING: {path}")
            return 1
        try:
            results = load_results(path)
        except Exception as exc:  # noqa: BLE001
            print(f"INTERACTIONS_RESULTS_PARSE: {exc}")
            return 2
    inventory = None
    if args.inventory:
        path = Path(args.inventory)
        if path.is_file():
            try:
                inventory = json.loads(path.read_text(encoding="utf-8-sig"))
            except Exception as exc:  # noqa: BLE001
                print(f"INTERACTIONS_INVENTORY_PARSE: {exc}")
                return 2
    problems = validate_spec(spec, results, inventory, args.require_results)
    if args.json:
        print(json.dumps({"ok": not problems, "problems": problems}, ensure_ascii=False, indent=2))
    elif problems:
        print("INTERACTIONS BLOCKED")
        for item in problems:
            print(f"- {item}")
    else:
        print(f"INTERACTIONS PASS flows={len(_list(spec.get('flows')))} cases={len(results or {})}")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
