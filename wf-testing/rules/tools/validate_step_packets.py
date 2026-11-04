#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate step packets vs workflows."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

SECTIONS = [
    "## 1. 元信息",
    "## 2. 本步目标",
    "## 3. 本步硬约束",
    "## 4. 本步门",
    "## 5. 做法",
    "## 6. 打开/填写",
    "## 7. 完成信号",
    "## 8. 回执字段",
]


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate_step_packets.py <package-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    fail = 0
    for ypath in sorted((root / "workflows").glob("*.yaml")):
        data = yaml.safe_load(ypath.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or "workflow" not in data:
            print(f"FAIL: bad yaml {ypath.name}")
            fail += 1
            continue
        wid = data["workflow"].get("id") or ypath.stem
        for step in data.get("steps") or []:
            if not isinstance(step, dict) or "id" not in step:
                continue
            sid = step["id"]
            rel = f"rules/packets/{wid}/{sid}.md"
            path = root / rel
            mr = step.get("must_read") or []
            if not mr:
                print(f"FAIL: {wid}/{sid} missing must_read")
                fail += 1
            else:
                first = str(mr[0]).replace("\\", "/")
                if first != rel:
                    print(f"FAIL: {wid}/{sid} must_read[0]={first} != {rel}")
                    fail += 1
                pkt = [
                    str(x).replace("\\", "/")
                    for x in mr
                    if str(x).replace("\\", "/").startswith("rules/packets/")
                ]
                if len(pkt) > 1:
                    print(f"FAIL: {wid}/{sid} duplicate packet must_read {pkt}")
                    fail += 1
            if not path.is_file():
                print(f"FAIL: missing packet {rel}")
                fail += 1
                continue
            text = path.read_text(encoding="utf-8")
            for h in SECTIONS:
                if h not in text:
                    print(f"FAIL: {rel} missing section {h}")
                    fail += 1
            for m in re.finditer(r"详见\s*`rules/([^`]+)`", text):
                target = m.group(1)
                if target.startswith("packets/"):
                    continue
                if target.startswith("templates/") or target.startswith("core/cold-start"):
                    continue
                print(f"FAIL: {rel} runtime pointer 详见 `rules/{target}`")
                fail += 1
            if "reads=" in text and rel not in text:
                print(f"FAIL: {rel} receipt missing self path")
                fail += 1
    print(f"SUMMARY fail={fail}")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
