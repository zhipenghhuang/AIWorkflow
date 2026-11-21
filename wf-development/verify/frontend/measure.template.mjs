// 视觉几何/token 度量（Playwright · 模板）
//
// 复制到项目 scripts/frontend_measure.mjs，按项目改 config 路径/登录。
// 一次运行同时抓 baseline 与 impl；输出 metrics-baseline.json / metrics-impl.json，
// 再由 verify/tools/frontend_measure.py 比对为 measure-diff.json。
//
// 设计取舍：只抓“可见交互控件 + 标题/标签文案 + 声明的关键 target 的 computed style/box”；
// 不做全元素、不做像素 diff、不抓 canvas 图表内部；动态数据只影响名称集合时按 role+name 去重。
//
// 用法：
//   node scripts/frontend_measure.mjs --config .gate/frontend/measure.json --out .gate/frontend

import fs from "node:fs";
import path from "node:path";
import { chromium } from "playwright";

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function arg(name, fallback = "") {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}

function urlOf(baseUrl, route) {
  if (/^(https?:|file:)/i.test(route)) return route;
  const base = String(baseUrl || "");
  if (!route || route === "/") return base;
  if (/\.html?$/i.test(base)) return base + route;
  return base.replace(/\/$/, "") + (route.startsWith("/") ? route : `/${route}`);
}

async function login(page, baseUrl, login, timeout) {
  if (!login) return;
  await page.goto(urlOf(baseUrl, login.url || "/"), { waitUntil: "networkidle", timeout });
  for (const step of login.steps || []) {
    if (step.fill) await page.locator(step.fill[0]).first().fill(String(step.fill[1]));
    else if (step.click) await page.locator(step.click).first().click();
    else if (step.press) await page.locator(step.press[0]).first().press(step.press[1]);
  }
  if (login.wait_for) await page.waitForSelector(login.wait_for, { timeout });
}

async function collect(page, targets) {
  return page.evaluate((targetList) => {
    const norm = (s) => String(s || "").replace(/\s+/g, " ").trim();
    const visible = (el) => {
      const r = el.getBoundingClientRect();
      const s = getComputedStyle(el);
      return r.width > 0 && r.height > 0 && s.visibility !== "hidden" &&
        s.display !== "none" && Number(s.opacity || "1") > 0;
    };
    const roleOf = (el) => {
      const r = el.getAttribute("role");
      if (r) return r;
      const tag = el.tagName.toLowerCase();
      if (tag === "input") {
        const type = (el.getAttribute("type") || "text").toLowerCase();
        if (type === "checkbox") return "checkbox";
        if (type === "radio") return "radio";
        if (type === "search") return "searchbox";
        return "textbox";
      }
      return ({ a: "link", button: "button", select: "combobox", textarea: "textbox",
        h1: "heading", h2: "heading", h3: "heading", h4: "heading", th: "columnheader", label: "label" })[tag] || tag;
    };
    const nameOf = (el) => {
      const aria = el.getAttribute("aria-label");
      if (aria && aria.trim()) return norm(aria);
      const by = el.getAttribute("aria-labelledby");
      if (by) {
        const text = by.split(/\s+/).map((id) => document.getElementById(id)?.textContent || "").join(" ");
        if (norm(text)) return norm(text);
      }
      const tag = el.tagName.toLowerCase();
      if (tag === "input" || tag === "textarea" || tag === "select") {
        const label = el.labels && el.labels[0] ? el.labels[0].textContent : "";
        if (norm(label)) return norm(label);
        return norm(el.getAttribute("placeholder") || el.getAttribute("name") ||
          el.getAttribute("title") || "");
      }
      return norm(el.textContent || "") || norm(el.getAttribute("title") || "");
    };
    const selector = "button,a[href],input:not([type=hidden]),select,textarea,[role=button],[role=link],[role=tab],[role=menuitem],[role=switch],[role=checkbox],h1,h2,h3,h4,legend,th,label";
    const seen = new Set();
    const controls = [];
    for (const el of document.querySelectorAll(selector)) {
      if (!visible(el)) continue;
      const role = roleOf(el);
      const name = nameOf(el);
      if (!name) continue;
      const key = `${role}|${name}`;
      if (seen.has(key)) continue;
      seen.add(key);
      controls.push({ role, name, tag: el.tagName.toLowerCase() });
    }
    const targets = [];
    for (const item of targetList || []) {
      const el = document.querySelector(item.selector || "");
      if (!el || !visible(el)) continue;
      const s = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      targets.push({
        name: item.name || item.selector,
        selector: item.selector,
        text: norm(el.textContent || "").slice(0, 200),
        box: { top: r.top, left: r.left, width: r.width, height: r.height },
        styles: {
          "font-size": s.fontSize,
          "line-height": s.lineHeight,
          color: s.color,
          "background-color": s.backgroundColor,
          "border-radius": s.borderRadius,
          padding: s.padding,
          margin: s.margin,
          gap: s.gap || s.columnGap || "",
        },
      });
    }
    return { controls, targets };
  }, targets);
}

async function captureSide(browser, sideName, side, cfg, viewports, timeout) {
  const baseUrl = side.baseUrl || "";
  const routes = [];
  for (const viewport of viewports) {
    for (const route of side.routes || []) {
      const context = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height } });
      const page = await context.newPage();
      const errors = [];
      page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
      try {
        await login(page, baseUrl, side.login, timeout);
        await page.goto(urlOf(baseUrl, route.route || "/"), { waitUntil: "domcontentloaded", timeout });
        if (route.ready) await page.waitForSelector(route.ready, { timeout });
        if (cfg.settleMs) await page.waitForTimeout(Number(cfg.settleMs));
        const data = await collect(page, cfg.targets || []);
        routes.push({ name: route.name || route.route, route: route.route, viewport: viewport.name,
          url: page.url(), console_errors: errors.length, ...data });
      } catch (error) {
        routes.push({ name: route.name || route.route, route: route.route, viewport: viewport.name,
          url: page.url(), error: String(error), console_errors: errors.length, controls: [], targets: [] });
      } finally {
        await context.close();
      }
    }
  }
  return { side: sideName, generated_at: new Date().toISOString(), routes };
}

async function main() {
  const configPath = arg("config", ".gate/frontend/measure.json");
  const outDir = arg("out", ".gate/frontend");
  const cfg = readJson(configPath);
  const viewports = cfg.viewports && cfg.viewports.length
    ? cfg.viewports
    : [{ name: "desktop", width: 1440, height: 900 }, { name: "mobile", width: 390, height: 844 }];
  const timeout = Number(cfg.timeoutMs || 20000);
  const executablePath = process.env.PLAYWRIGHT_CHROMIUM || cfg.executablePath || undefined;
  const browser = await chromium.launch({ headless: true, executablePath });
  fs.mkdirSync(outDir, { recursive: true });
  let failed = 0;
  try {
    for (const [side, spec] of Object.entries(cfg.sides || {})) {
      const data = await captureSide(browser, side, spec, cfg, viewports, timeout);
      const file = path.join(outDir, `metrics-${side}.json`);
      fs.writeFileSync(file, JSON.stringify(data, null, 2), "utf8");
      const errors = data.routes.filter((r) => r.error).length;
      failed += errors;
      console.log(`${side}: ${data.routes.length - errors}/${data.routes.length} routes -> ${file}`);
    }
  } finally {
    await browser.close();
  }
  return failed ? 1 : 0;
}

main().then((code) => process.exit(code)).catch((error) => {
  console.error(error);
  process.exit(1);
});
