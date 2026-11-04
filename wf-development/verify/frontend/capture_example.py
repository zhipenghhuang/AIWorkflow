#!/usr/bin/env python3
"""Capture reference implementation for frontend evidence.

Gate integration (recommended):
  1) copy this file into the project (e.g. `scripts/frontend_capture.py`)
  2) write `capture.json` (example below)
  3) in `.gate/project-profile.json` set
       "frontend": { "capture": "python scripts/frontend_capture.py --config capture.json", ... }
  4) run the gate; it executes capture and only then validates evidence.

Why: hand-written `route-coverage.json` + screenshots can claim anything. This
script opens a real browser, waits for the page to be ready (not skeleton),
keeps console/network records, and writes `evidence.json` with screenshot
hashes. The gate cross-checks coverage against that file.

capture.json:
{
  "base_url": "http://127.0.0.1:8000",
  "login": {
    "url": "/",
    "steps": [
      {"fill": ["input[name='username']", "admin"]},
      {"fill": ["input[name='password']", "123456"]},
      {"click": "button[type='submit']"}
    ],
    "wait_for": "nav"
  },
  "routes": [
    {"route": "#/dashboard", "name": "dashboard", "ready": "h1"},
    {"route": "#/contracts", "name": "contracts", "ready": "h1"},
    {"route": "#/contracts/1", "name": "contract-detail", "ready": "h1"},
    {"route": "#/receipts/new", "name": "receipt-new", "ready": "h1"}
  ],
  "viewports": {"desktop": {"width": 1440, "height": 900},
                "mobile": {"width": 390, "height": 844}},
  "ready_timeout_ms": 20000,
  "settle_ms": 600,
  "max_pages": 40
}

Exit code: 0 = all routes captured & ready; 1 = at least one route failed
(evidence.json still written so the gate can report exact failures).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

SKELETON_SELECTORS = (".skeleton", "[data-skeleton]", ".loading-skeleton", ".placeholder-glow")


def chromium_executable() -> str | None:
    """Honor PLAYWRIGHT_CHROMIUM, else newest LOCALAPPDATA ms-playwright chromium."""
    import os

    configured = os.environ.get("PLAYWRIGHT_CHROMIUM")
    if configured and Path(configured).is_file():
        return configured
    root = Path(os.environ.get("LOCALAPPDATA", "")) / "ms-playwright"
    candidates = sorted(root.glob("chromium-*/chrome-win64/chrome.exe"))
    return str(candidates[-1]) if candidates else None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_config(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise SystemExit("CONFIG_INVALID: top level must be an object")
    if not data.get("routes"):
        raise SystemExit("CONFIG_INVALID: routes is empty")
    return data


def login(page, base_url: str, login: dict, timeout_ms: int) -> None:
    if not login:
        return
    url = str(login.get("url") or "/")
    page.goto(base_url.rstrip("/") + url, wait_until="networkidle")
    for step in login.get("steps") or []:
        if not isinstance(step, dict):
            continue
        if "fill" in step:
            selector, value = step["fill"]
            page.locator(selector).first.fill(str(value))
        elif "click" in step:
            page.locator(step["click"]).first.click()
        elif "press" in step:
            selector, key = step["press"]
            page.locator(selector).first.press(key)
    wait_for = str(login.get("wait_for") or "").strip()
    if wait_for:
        page.wait_for_selector(wait_for, timeout=timeout_ms)
    page.wait_for_load_state("networkidle")


def route_url(base_url: str, route: str, stamp: str) -> str:
    base = base_url.rstrip("/")
    if route.startswith("#"):
        return f"{base}/?capture={stamp}{route}"
    if route.startswith("/"):
        return f"{base}{route}"
    return route


def page_ready(page, ready_selector: str, timeout_ms: int) -> tuple[bool, str]:
    if ready_selector:
        try:
            page.wait_for_selector(ready_selector, timeout=timeout_ms)
        except Exception:
            return False, f"ready selector timeout: {ready_selector}"
    try:
        page.wait_for_load_state("networkidle", timeout=timeout_ms)
    except Exception:
        pass
    state = page.evaluate(
        """(selectors) => {
            const visible = (el) => {
                if (!el) return false;
                const s = getComputedStyle(el);
                return s.display !== 'none' && s.visibility !== 'hidden' && el.getClientRects().length > 0;
            };
            const skeletons = selectors.flatMap((s) => Array.from(document.querySelectorAll(s))).filter(visible);
            const body = document.body ? document.body.innerText.trim() : '';
            const loginish = /登录|sign in/i.test(body) && body.length < 400;
            return { skeletons: skeletons.length, textLen: body.length, loginish };
        }""",
        list(SKELETON_SELECTORS),
    )
    if state.get("skeletons"):
        return False, f"skeleton visible x{state['skeletons']}"
    if state.get("loginish"):
        return False, "still on login page"
    if int(state.get("textLen") or 0) < 20:
        return False, "page text too short"
    return True, "ready"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", default=".gate/frontend")
    ap.add_argument("--storage-state", default="")
    ap.add_argument("--headless", action="store_true", default=True)
    args = ap.parse_args()

    config = load_config(Path(args.config))
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    base_url = str(config.get("base_url") or "http://127.0.0.1:8000")
    viewports = config.get("viewports") or {
        "desktop": {"width": 1440, "height": 900},
        "mobile": {"width": 390, "height": 844},
    }
    timeout_ms = int(config.get("ready_timeout_ms") or 20000)
    settle_ms = int(config.get("settle_ms") or 600)
    routes = [r for r in config["routes"] if isinstance(r, dict) and r.get("route")]
    routes = routes[: int(config.get("max_pages") or 40)]

    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:  # pragma: no cover
        print(f"CAPTURE_FAILED: playwright not installed ({exc})")
        return 1

    started = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    results: list[dict] = []
    failures = 0

    with sync_playwright() as p:
        launch_kwargs = {"headless": True}
        executable = chromium_executable()
        if executable:
            launch_kwargs["executable_path"] = executable
        browser = p.chromium.launch(**launch_kwargs)
        context_kwargs = {"locale": "zh-CN"}
        if args.storage_state and Path(args.storage_state).is_file():
            context_kwargs["storage_state"] = args.storage_state
        context = browser.new_context(**context_kwargs)
        page = context.new_page()
        console_errors: list[str] = []
        failed_requests: list[str] = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("requestfailed", lambda req: failed_requests.append(f"{req.method} {req.url} {req.failure}"))
        page.on("response", lambda res: failed_requests.append(f"{res.status} {res.url}") if res.status >= 500 else None)

        login(page, base_url, config.get("login") or {}, timeout_ms)
        stamp = str(int(time.time()))
        for index, item in enumerate(routes, 1):
            route = str(item["route"])
            name = str(item.get("name") or f"route-{index}")
            ready_selector = str(item.get("ready") or "")
            console_errors.clear()
            failed_requests.clear()
            record: dict = {"route": route, "name": name, "ready": False, "detail": "", "console_errors": 0,
                            "failed_requests": 0}
            try:
                page.goto(route_url(base_url, route, stamp), wait_until="networkidle", timeout=timeout_ms)
                ok, detail = page_ready(page, ready_selector, timeout_ms)
                if settle_ms:
                    page.wait_for_timeout(settle_ms)
                record["ready"] = bool(ok)
                record["detail"] = detail
                if not ok:
                    failures += 1
                for view, size in viewports.items():
                    page.set_viewport_size({"width": int(size["width"]), "height": int(size["height"])})
                    page.wait_for_timeout(150)
                    shot = out_dir / f"{name}-{view}.png"
                    page.screenshot(path=str(shot), full_page=True)
                    record[view] = {"path": shot.name, "sha256": sha256_file(shot)}
                record["text_len"] = page.evaluate("document.body.innerText.trim().length")
            except Exception as exc:
                failures += 1
                record["detail"] = f"{type(exc).__name__}: {exc}"
            record["console_errors"] = len(console_errors)
            record["failed_requests"] = len(failed_requests)
            if console_errors:
                record["console_samples"] = console_errors[:3]
            if failed_requests:
                record["request_samples"] = failed_requests[:3]
            results.append(record)

        browser.close()

    evidence = {
        "schema": 1,
        "generator": "capture_example.py",
        "engine": "playwright",
        "base_url": base_url,
        "generated_at": started,
        "finished_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "viewports": list(viewports.keys()),
        "console": {
            "errors": sum(r["console_errors"] for r in results),
            "failed_requests": sum(r["failed_requests"] for r in results),
        },
        "routes": results,
    }
    (out_dir / "evidence.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    report = {
        "generated_at": evidence["generated_at"],
        "errors": [s for r in results for s in r.get("console_samples") or []],
        "failed": [s for r in results for s in r.get("request_samples") or []],
        "results": [{"route": r["route"], "name": r["name"], "ready": r["ready"],
                     "hash": r["route"], "overflow": False, "noAccess": False} for r in results],
    }
    (out_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    bad = [r for r in results if not r["ready"]]
    print(f"capture: {len(results) - len(bad)}/{len(results)} routes ready -> {out_dir / 'evidence.json'}")
    for r in bad[:10]:
        print(f"  - {r['route']}: {r['detail']}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
