"""Extract modules embedded in a single-file HTML prototype.

Many prototypes ship as one HTML file whose <script type="importmap"> maps
module names to `data:text/javascript;base64,...` or percent-encoded data URLs.
Searching the raw HTML for UI strings then gives false negatives.

Writes `prototype.json` next to the modules (source sha256 + module list), so a
gate can prove the prototype was actually opened/decoded this round.

Usage:
    python rules/tools/extract_prototype_modules.py <prototype.html> <out_dir>

Exit code 0 = extracted (or no data: modules); 2 = input/parse error.
"""
from __future__ import annotations

import base64
import hashlib
import json
import re
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    src = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    if not src.is_file():
        print(f"input not found: {src}")
        return 2
    html = src.read_text(encoding="utf-8", errors="replace")
    manifest = {
        "schema": 1,
        "tool": "extract_prototype_modules.py",
        "source": str(src).replace("\\", "/"),
        "source_sha256": sha256_file(src),
        "source_bytes": src.stat().st_size,
        "extracted_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "modules": [],
    }
    match = re.search(r'<script type="importmap">(.*?)</script>', html, re.S)
    if not match:
        print("no <script type=importmap> found; treat as ordinary HTML")
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "prototype.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        return 0
    try:
        imports = json.loads(match.group(1)).get("imports", {})
    except json.JSONDecodeError as exc:
        print(f"invalid importmap JSON: {exc}")
        return 2

    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for name, url in imports.items():
        if not isinstance(url, str) or not url.startswith("data:"):
            continue
        header, _, payload = url.partition(",")
        try:
            if ";base64" in header:
                text = base64.b64decode(payload).decode("utf-8", "replace")
            else:
                text = urllib.parse.unquote(payload)
        except Exception as exc:  # noqa: BLE001 - report and continue
            print(f"skip {name}: {exc}")
            continue
        target = out_dir / re.sub(r"[^A-Za-z0-9._-]+", "_", name.split("/")[-1] or f"module_{count}")
        target.write_text(text, encoding="utf-8")
        manifest["modules"].append({
            "name": name,
            "file": target.name,
            "chars": len(text),
            "sha256": sha256_text(text),
        })
        print(f"{target}  {len(text)} chars  <- {name}")
        count += 1
    (out_dir / "prototype.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"decoded {count} data: module(s); manifest -> {out_dir / 'prototype.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
