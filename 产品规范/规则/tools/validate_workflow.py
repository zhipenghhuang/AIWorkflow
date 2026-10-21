#!/usr/bin/env python3
"""Validate workflow/agent YAML syntax and basic references.

Usage: python validate_workflow.py <package-root>

Exit code 0 = all good; 1 = errors. Prints one line per error.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except Exception as exc:  # pragma: no cover
    print(f"YAML_VALIDATOR_UNAVAILABLE: {exc}")
    sys.exit(2)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def declared_tokens(agents_text: str) -> tuple[set[str], set[str], set[str]]:
    hitl: set[str] = set()
    when: set[str] = set()
    gates: set[str] = set()
    for m in re.finditer(r"`([^`\r\n]+)`", agents_text):
        tok = m.group(1).strip()
        if re.fullmatch(r"(confirm|select)_[a-z_]+", tok):
            hitl.add(tok)
        elif re.fullmatch(r"[a-z]+(_[a-z]+)+", tok):
            when.add(tok)
        gate = re.fullmatch(r"gate:\s*([a-z][a-z0-9-]*)", tok)
        if gate:
            gates.add(gate.group(1))
    return hitl, when, gates


def main() -> int:
    if len(sys.argv) < 2:
        print("USAGE: validate_workflow.py <package-root>")
        return 2
    root = Path(sys.argv[1]).resolve()
    agents_dir = root / "agents"
    workflows_dir = root / "workflows"
    errors: list[str] = []

    if not agents_dir.is_dir():
        errors.append("MISSING_DIR: agents/")
    if not workflows_dir.is_dir():
        errors.append("MISSING_DIR: workflows/")

    agent_ids: set[str] = set()
    agent_docs: dict[Path, dict] = {}

    for path in sorted(agents_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(read_text(path))
        except Exception as exc:
            errors.append(f"YAML_SYNTAX: {path.relative_to(root)}: {str(exc).splitlines()[0]}")
            continue
        if not isinstance(data, dict):
            errors.append(f"AGENT_SCHEMA: {path.relative_to(root)}: root must be a mapping")
            continue
        agent_docs[path] = data
        for key in ("id", "role", "goal"):
            if not data.get(key):
                errors.append(f"AGENT_SCHEMA: {path.relative_to(root)}: missing {key}")
        agent_id = str(data.get("id") or path.stem)
        if agent_id in agent_ids:
            errors.append(f"AGENT_DUPLICATE: {path.relative_to(root)}: id={agent_id}")
        agent_ids.add(agent_id)
        for key in ("reads", "must", "outputs"):
            if key in data and not isinstance(data[key], list):
                errors.append(f"AGENT_SCHEMA: {path.relative_to(root)}: {key} must be a list")

    agents_text = read_text(root / "AGENTS.md") if (root / "AGENTS.md").exists() else ""
    hitl_decl, when_decl, gate_decl = declared_tokens(agents_text)

    for path in sorted(workflows_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(read_text(path))
        except Exception as exc:
            errors.append(f"YAML_SYNTAX: {path.relative_to(root)}: {str(exc).splitlines()[0]}")
            continue
        if not isinstance(data, dict):
            errors.append(f"WORKFLOW_SCHEMA: {path.relative_to(root)}: root must be a mapping")
            continue
        wf = data.get("workflow")
        steps = data.get("steps")
        if not isinstance(wf, dict):
            errors.append(f"WORKFLOW_SCHEMA: {path.relative_to(root)}: missing workflow mapping")
            continue
        for key in ("id", "name", "version"):
            if not wf.get(key):
                errors.append(f"WORKFLOW_SCHEMA: {path.relative_to(root)}: workflow.{key} missing")
        if wf.get("id") and str(wf["id"]) != path.stem:
            errors.append(f"WORKFLOW_ID: {path.relative_to(root)}: workflow.id={wf['id']} != filename")
        if not isinstance(steps, list) or not steps:
            errors.append(f"WORKFLOW_SCHEMA: {path.relative_to(root)}: steps must be a non-empty list")
            continue

        step_ids: set[str] = set()
        for idx, step in enumerate(steps, 1):
            if not isinstance(step, dict):
                errors.append(f"STEP_SCHEMA: {path.relative_to(root)}: step {idx} must be a mapping")
                continue
            for key in ("name", "id", "agent"):
                if not step.get(key):
                    errors.append(f"STEP_SCHEMA: {path.relative_to(root)}: step {idx} missing {key}")
            sid = str(step.get("id") or "")
            if sid:
                if sid in step_ids:
                    errors.append(f"STEP_DUPLICATE: {path.relative_to(root)}: id={sid}")
                step_ids.add(sid)
            agent = str(step.get("agent") or "")
            if agent and agent_ids and agent not in agent_ids:
                errors.append(f"STEP_AGENT: {path.relative_to(root)}: {sid or idx} agent={agent} not found")
            hitl = step.get("hitl")
            names: list[str] = []
            if isinstance(hitl, str):
                names = [hitl]
            elif isinstance(hitl, list):
                names = [str(x.get("name")) for x in hitl if isinstance(x, dict) and x.get("name")]
            for name in names:
                if hitl_decl and name not in hitl_decl:
                    errors.append(f"HITL_UNDECLARED: {path.relative_to(root)}: {sid}: {name}")
            whens: list[str] = []
            if step.get("hitl_when"):
                whens.append(str(step["hitl_when"]))
            if step.get("when"):
                whens.append(str(step["when"]))
            if isinstance(hitl, list):
                whens += [str(x.get("when")) for x in hitl if isinstance(x, dict) and x.get("when")]
            for w in whens:
                if when_decl and w not in when_decl:
                    errors.append(f"WHEN_UNDECLARED: {path.relative_to(root)}: {sid}: {w}")
            gate = step.get("gate")
            if gate and gate_decl and str(gate) not in gate_decl:
                errors.append(f"GATE_UNDECLARED: {path.relative_to(root)}: {sid}: {gate}")

        eps = data.get("entry_points")
        if isinstance(eps, dict):
            for name, sid in eps.items():
                if str(sid) not in step_ids:
                    errors.append(f"ENTRY_POINT: {path.relative_to(root)}: {name} -> {sid} (step not found)")

    if errors:
        for e in errors:
            print(e)
        print(f"YAML_VALIDATION_FAILED: {len(errors)} issue(s)")
        return 1
    print("YAML_VALIDATION_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
