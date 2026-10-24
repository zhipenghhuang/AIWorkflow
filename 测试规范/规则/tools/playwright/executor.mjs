#!/usr/bin/env node
/**
 * executor.mjs — 用例脚本执行器（脚本档 · 通用引擎 V1，业务无关）
 *
 * 定位：把「可脚本化用例」按确定性脚本回放，产出台账可直接合并的结果与失败证据。
 * 纪律：本文件为通用引擎——复制到项目 `测试/脚本/` 后【勿改逻辑】；
 *       项目差异全部收敛到 `测试/脚本/case-executor.config.mjs`（登录钩子等）。
 *       规则见 `测试规范/规则/专项/脚本执行.md`；落地说明见 `测试规范/规则/tools/playwright/README.md`。
 *
 * 用法（在项目根执行）：
 *   node 测试/脚本/executor.mjs --plan=测试/脚本/01-xxx.script.mjs [选项]          # 默认 ui（浏览器）
 *   node 测试/脚本/executor.mjs --mode=api --plan=测试/接口测试/脚本/01-xxx.mjs     # api（接口轨 · 无浏览器）
 *
 * 选项：
 *   --mode=ui|api       ui=浏览器回放（默认）；api=纯接口回放（接口轨，不启浏览器）
 *   --plan=<脚本文件>   用例脚本（export default { module, doc, cases[] }）；必填（--check 同）
 *   --case=<ID 子串>    只跑匹配的用例（子集复跑；不改变脚本内顺序）
 *   --runStamp=<戳>     固定本轮数据戳（默认自动生成）
 *   --baseUrl=<URL>     覆盖 config.baseUrl / TEST_BASE_URL
 *   --headless=false    有头模式（调试；仅 ui）
 *   --check             只做同步检查（脚本 caseId ↔ 用例文档），不执行
 *   --config=<路径>     覆盖 config 位置（默认 测试/脚本/case-executor.config.mjs）
 *   --root=<目录>       项目根（默认当前工作目录）
 *   --draftDir=<目录>   覆盖 jsonl 输出目录（默认 测试/功能测试/.draft）
 *   --evidenceDir=<目录> 覆盖证据根目录（默认 测试/功能测试/证据）
 *
 * API 模式（接口轨）：
 *   登录钩子：config.apiLogin(api, baseUrl, ctx) → 返回鉴权头对象（并入每步请求；可选）
 *   步骤：api（含 expectStatus/expectMessage/expectFields/save）、note；其余 action 报错
 *   证据：失败自动落 {CASE-ID}-api-{runStamp}.json（请求+响应摘录）
 *
 * 产物：
 *   jsonl：{draftDir}/script-{module}-{runStamp}.jsonl（默认 测试/功能测试/.draft；一条一写，格式同拆分档 Worker）
 *   证据：UI：{evidenceDir}/{module}/{CASE-ID}-{result}-{runStamp}.png（失败自动全屏截图；默认 测试/功能测试/证据）
 *            + {CASE-ID}-net-{runStamp}.json（失败现场 HTTP≥400 摘要，如有）
 *         API：{evidenceDir}/{module}/{CASE-ID}-api-{runStamp}.json（失败现场）
 *
 * 退出码：0=全部通过；1=存在 fail/blocked；2=装载/配置错误。
 */

import { existsSync, mkdirSync, appendFileSync, writeFileSync, readFileSync } from 'node:fs'
import { dirname, join, resolve, isAbsolute } from 'node:path'
import { pathToFileURL } from 'node:url'

// ── CLI ────────────────────────────────────────────────────────────────────
const argv = process.argv.slice(2)
const arg = (name, def = undefined) => {
  const hit = argv.find((a) => a === `--${name}` || a.startsWith(`--${name}=`))
  if (hit === undefined) return def
  const eq = hit.indexOf('=')
  return eq === -1 ? true : hit.slice(eq + 1)
}
if (argv.includes('--help') || argv.includes('-h')) { printUsage(); process.exit(0) }

const ROOT = resolve(String(arg('root', process.cwd())))
const PLAN_ARG = arg('plan')
const CASE_FILTER = arg('case')
const TAG_FILTER = arg('tag')
const SUITE_FILTER = arg('suite')
const CHECK_ONLY = !!arg('check')
const HEADLESS = String(arg('headless', 'true')) !== 'false'
const MODE = String(arg('mode', 'ui')).toLowerCase()
if (!['ui', 'api'].includes(MODE)) fail(`--mode 仅支持 ui|api（当前：${MODE}）`)
const CONFIG_PATH = resolve(ROOT, String(arg('config', '测试/脚本/case-executor.config.mjs')))

if (!PLAN_ARG) { printUsage(); process.exit(2) }
const PLAN_PATH = resolve(ROOT, String(PLAN_ARG))
if (!existsSync(PLAN_PATH)) fail(`脚本文件不存在：${PLAN_PATH}`)

const runStamp = String(arg('runStamp') || defaultStamp())
const bus = new Map([['runStamp', runStamp]])
const DRAFT_DIR = resolve(ROOT, String(arg('draftDir', join('测试', '执行台账', '.draft'))))
const EVIDENCE_ROOT = resolve(ROOT, String(arg('evidenceDir', join('测试', '执行台账', '证据'))))

function defaultStamp() {
  const d = new Date()
  const p = (n, w = 2) => String(n).padStart(w, '0')
  return `${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}${p(d.getHours())}${p(d.getMinutes())}${p(d.getSeconds())}`
}
function printUsage() {
  console.log([
    '用例脚本执行器（脚本档 · ui=浏览器 / api=接口轨无浏览器）',
    '用法: node 测试/脚本/executor.mjs --plan=测试/脚本/xx.script.mjs [--mode=api] [--case=ID] [--tag=smoke|regression] [--suite=名] [--runStamp=戳] [--headless=false] [--check] [--draftDir=…] [--evidenceDir=…]',
    '规则: 测试规范/规则/专项/脚本执行.md',
  ].join('\n'))
}
function fail(msg) { console.error(`[executor] ${msg}`); process.exit(2) }

// ── 装载 ───────────────────────────────────────────────────────────────────
async function loadModule(p) {
  const url = `${pathToFileURL(p).href}?t=${Date.now()}`
  const mod = await import(url)
  return mod.default ?? mod
}

let config = {}
if (existsSync(CONFIG_PATH)) {
  config = (await loadModule(CONFIG_PATH)) ?? {}
} else {
  console.warn(`[executor] 未找到配置（${CONFIG_PATH}），使用最小默认（无登录钩子）`)
}
const BASE_URL = String(arg('baseUrl', config.baseUrl || process.env.TEST_BASE_URL || '')).replace(/\/+$/, '')
if (!BASE_URL && !CHECK_ONLY) fail('缺少 baseUrl（config.baseUrl / --baseUrl / TEST_BASE_URL）')

const TIME = { action: 15000, nav: 30000, case: 180000, ...(config.timeouts || {}) }

const plan = await loadModule(PLAN_PATH)
if (!plan?.cases?.length) fail(`脚本无 cases：${PLAN_PATH}`)
const moduleName = plan.module || '未命名模块'

// ── --check：脚本 caseId ↔ 用例文档 同步检查 ──────────────────────────────
if (CHECK_ONLY) {
  if (!plan.doc) fail('--check 需要脚本声明 doc（用例文档路径）')
  const docPath = resolve(ROOT, plan.doc)
  if (!existsSync(docPath)) fail(`用例文档不存在：${docPath}`)
  const docText = readFileSync(docPath, 'utf8')
  const docIds = new Set([...docText.matchAll(/^#{2,4}\s+([A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)+)\s/gm)].map((m) => m[1]))
  let stale = 0
  for (const c of plan.cases) {
    if (!docIds.has(c.id)) { stale++; console.error(`STALE: 脚本用例 ${c.id} 未在用例文档标题找到`) }
  }
  const scriptIds = new Set(plan.cases.map((c) => c.id))
  const notScripted = [...docIds].filter((id) => !scriptIds.has(id))
  console.log(`[check] 脚本 ${scriptIds.size} 条；文档标题 ${docIds.size} 条；STALE ${stale} 条`)
  if (notScripted.length) console.log(`[check] 文档未脚本化（提示，非错误）：${notScripted.join(', ')}`)
  process.exit(stale ? 1 : 0)
}

// ── 工具：占位符 / 断言 / 摘要 ─────────────────────────────────────────────
const subst = (v) => typeof v === 'string' ? v.replace(/:([A-Za-z_][A-Za-z0-9_]*)/g, (m, k) => bus.has(k) ? String(bus.get(k)) : m) : v
const CJK2 = /^[\u4e00-\u9fa5]{2}$/
const looksLikeSelector = (s) => />>|^[.#\[:>*]|:(visible|has|not|nth|first|last)\b/.test(s)
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
const textRegex = (t) => CJK2.test(t) ? new RegExp(t.split('').map(esc).join('\\s*')) : new RegExp(esc(t))
const cut = (s, n = 160) => { s = String(s ?? ''); return s.length > n ? s.slice(0, n) + '…' : s }
// eslint-disable-next-line no-control-regex
const stripAnsi = (s) => String(s ?? '').replace(/\u001b\[[0-9;]*m/g, '')
const oneLine = (s, n = 200) => cut(stripAnsi(s).replace(/\s+/g, ' ').trim(), n)
const rel = (p) => { const s = String(p); return s.toLowerCase().startsWith(ROOT.toLowerCase()) ? s.slice(ROOT.length + 1).replaceAll('\\', '/') : s }

class BlockedError extends Error { constructor(m) { super(m); this.blocked = true } }

async function topLayer(page) {
  const layers = page.locator('.ant-modal:visible, .ant-drawer:visible')
  const n = await layers.count().catch(() => 0)
  return n > 0 ? layers.nth(n - 1) : null
}

async function resolveClickLocator(page, rawTarget) {
  const t = subst(String(rawTarget))
  if (looksLikeSelector(t)) return page.locator(t).last()
  const layer = await topLayer(page)
  const scopes = layer ? [layer, page] : [page]
  const variants = CJK2.test(t) ? [t, t.split('').join(' ')] : [t]
  for (const scope of scopes) {
    for (const v of variants) {
      const cands = [
        scope.getByRole('button', { name: v }).first(),
        scope.getByText(v, { exact: false }).first(),
      ]
      for (const c of cands) { if (await c.count() > 0) return c }
    }
    const tip = scope.getByTestId(t).first()
    if (await tip.count() > 0) return tip
  }
  return page.getByText(t, { exact: false }).first()
}

async function resolveFieldLocator(page, rawTarget) {
  const t = subst(String(rawTarget))
  if (looksLikeSelector(t)) return page.locator(t).last()
  const layer = await topLayer(page)
  const scopes = layer ? [layer, page] : [page]
  for (const scope of scopes) {
    const cands = [
      scope.getByLabel(t, { exact: false }).first(),
      scope.getByPlaceholder(t).first(),
      scope.locator(`[name="${t}"]`).first(),
      scope.getByTestId(t).first(),
    ]
    for (const c of cands) { if (await c.count() > 0) return c }
  }
  return page.getByLabel(t, { exact: false }).first()
}

async function clickWithRetry(page, target) {
  let lastErr
  for (let attempt = 1; attempt <= 2; attempt++) {
    try {
      const loc = await resolveClickLocator(page, target)
      await loc.scrollIntoViewIfNeeded({ timeout: TIME.action }).catch(() => {})
      await loc.click({ timeout: TIME.action })
      return
    } catch (e) {
      lastErr = e
      await page.keyboard.press('Escape').catch(() => {})
      await page.waitForTimeout(250)
    }
  }
  throw new Error(`点击「${target}」失败：${cut(lastErr?.message)}`)
}

// ── API 步骤（ui/api 两模式共用：requester = page.request 或 APIRequestContext）──
async function execApiStep(requester, s, authHeaders = {}) {
  const method = String(s.method || 'GET').toUpperCase()
  const path = subst(String(s.path || s.target || ''))
  const url = /^https?:\/\//.test(path) ? path : BASE_URL + (path.startsWith('/') ? path : '/' + path)
  const data = s.body !== undefined ? JSON.parse(JSON.stringify(s.body, (k, v) => subst(v))) : undefined
  const expect = Number(s.expectStatus ?? 200)
  let res
  try {
    res = await requester.fetch(url, { method, data, headers: { ...authHeaders, ...(s.headers || {}) }, failOnStatusCode: false, timeout: TIME.action })
  } catch (e) {
    const err = new Error(`api ${method} ${path} 请求失败：${oneLine(e?.message || e, 160)}`)
    err.api = { method, url, data, error: oneLine(e?.message || e, 240) }
    throw err
  }
  const status = res.status()
  const text = await res.text().catch(() => '')
  let json = null
  try { json = JSON.parse(text) } catch { /* 非 JSON 响应 */ }
  const mk = (msg) => { const err = new Error(msg); err.api = { method, url, data, status, bodyText: cut(text, 4000) }; return err }
  if (status !== expect) throw mk(`api ${method} ${path} 期望 ${expect} 实际 ${status}：${cut(oneLine(text), 180)}`)
  if (s.expectMessage) {
    const msg = String(json?.message ?? text)
    if (!msg.includes(String(s.expectMessage))) throw mk(`api ${method} ${path} message 不含「${s.expectMessage}」实际「${cut(oneLine(msg), 140)}」`)
  }
  for (const field of s.expectFields || []) {
    const v = String(field).split('.').reduce((o, k) => (o == null ? undefined : o[k]), json)
    if (v === undefined || v === null || v === '') throw mk(`api ${method} ${path} 字段 ${field} 为空`)
  }
  if (s.save && json) {
    for (const [key, expr] of Object.entries(s.save)) {
      const v = String(expr).split('.').reduce((o, k) => (o == null ? undefined : o[k]), json)
      if (v === undefined || v === null || v === '') throw mk(`api ${method} ${path} save 字段 ${expr} 为空`)
      bus.set(key, String(v))
    }
  }
  return { text: `api ${method} ${path} -> ${status}` + (json?.code !== undefined && String(json.code) !== String(status) ? `;code=${json.code}` : '') + (s.save ? `（save: ${Object.keys(s.save).join(',')}）` : '') }
}

// ── 步骤执行（UI）─────────────────────────────────────────────────────────
async function runStep(page, step) {
  const action = String(step.action || '').toLowerCase()
  const target = step.target !== undefined ? subst(String(step.target)) : undefined
  const value = step.value !== undefined ? subst(String(step.value)) : undefined
  switch (action) {
    case 'goto': {
      const url = /^https?:\/\//.test(target) ? target : BASE_URL + (target.startsWith('/') ? target : '/' + target)
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: TIME.nav })
      // 会话守护：导航后回调（配置可探测会话丢失并恢复；见 README「会话守护」）
      if (typeof config.afterNavigate === 'function') await config.afterNavigate(page, url)
      return `goto ${target}`
    }
    case 'click': await clickWithRetry(page, target); return `click ${target}`
    case 'fill': {
      if (value === undefined) throw new Error('fill 需要 value')
      const loc = await resolveFieldLocator(page, target)
      await loc.waitFor({ state: 'visible', timeout: TIME.action })
      await loc.click({ timeout: TIME.action }).catch(() => {})
      await loc.fill('', { timeout: TIME.action }).catch(() => {})
      await loc.fill(value, { timeout: TIME.action })
      if (/date|日期|时间/i.test(String(target)) || /picker/i.test(await loc.getAttribute('class').catch(() => '') || '')) {
        await page.keyboard.press('Enter').catch(() => {})
      }
      return `fill ${target}=${value}`
    }
    case 'select': {
      if (value === undefined) throw new Error('select 需要 value')
      const loc = await resolveFieldLocator(page, target)
      let lastErr
      for (let attempt = 1; attempt <= 2; attempt++) {
        try {
          const tag = await loc.evaluate((el) => el.tagName.toLowerCase()).catch(() => '')
          if (tag === 'select') { await loc.selectOption({ label: value }, { timeout: TIME.action }); return `select ${target}=${value}` }
          await loc.click({ timeout: TIME.action })
          const layer = await topLayer(page)
          const opt = (layer || page).getByText(textRegex(value), { exact: false }).first()
          await opt.waitFor({ state: 'visible', timeout: TIME.action })
          await opt.click({ timeout: TIME.action })
          return `select ${target}=${value}`
        } catch (e) { lastErr = e; await page.keyboard.press('Escape').catch(() => {}); await page.waitForTimeout(250) }
      }
      throw new Error(`选择「${target}=${value}」失败：${cut(lastErr?.message)}`)
    }
    case 'press': {
      const loc = await resolveFieldLocator(page, target)
      await loc.press(String(value || 'Enter'), { timeout: TIME.action })
      return `press ${target} ${value || 'Enter'}`
    }
    case 'wait': {
      if (value !== undefined && /^\d+$/.test(String(value))) { await page.waitForTimeout(Number(value)); return `wait ${value}ms` }
      if (target) { await page.locator(looksLikeSelector(target) ? target : `text=${target}`).first().waitFor({ state: 'visible', timeout: TIME.action }); return `wait ${target}` }
      throw new Error('wait 需要 target 或 value(ms)')
    }
    case 'assert':
    case 'assertnot': {
      const expectAbsent = action === 'assertnot'
      if (target?.startsWith('url:')) {
        const frag = target.slice(4)
        await page.waitForURL((u) => u.href.includes(frag), { timeout: TIME.action })
        return `assert url~${frag}`
      }
      if (looksLikeSelector(target)) {
        const loc = page.locator(target).last()
        await loc.waitFor({ state: expectAbsent ? 'hidden' : 'visible', timeout: TIME.action })
        return `assert${expectAbsent ? 'Not' : ''} ${target}`
      }
      const loc = page.getByText(textRegex(target), { exact: false }).first()
      await loc.waitFor({ state: expectAbsent ? 'hidden' : 'visible', timeout: TIME.action })
      return `assert${expectAbsent ? 'Not' : ''} 文本「${target}」`
    }
    case 'api': {
      const extraHeaders = config.apiHeaders ? await Promise.resolve().then(() => config.apiHeaders(page)).catch(() => ({})) : {}
      const r = await execApiStep(page.request, step, extraHeaders)
      return r.text
    }
    case 'eval': {
      const got = await page.evaluate(String(subst(String(step.target))))
      const want = subst(step.value)
      const ok = typeof want === 'string' && want.startsWith('~')
        ? String(got).includes(want.slice(1))
        : JSON.stringify(got) === JSON.stringify(want)
      if (!ok) throw new Error(`eval 期望 ${cut(JSON.stringify(want))} 实际 ${cut(JSON.stringify(got))}`)
      return `eval ${cut(String(step.target), 60)}`
    }
    case 'screenshot': {
      const file = join(EVIDENCE_ROOT, moduleName, `${subst(step.name || step.target || 'shot')}-${runStamp}.png`)
      mkdirSync(dirname(file), { recursive: true })
      await page.screenshot({ path: file, fullPage: true })
      return { note: `screenshot ${rel(file)}`, evidence: file }
    }
    case 'note': return `note ${target || ''}`
    default: throw new Error(`未知 action：${action}`)
  }
}

// ── 主流程 ────────────────────────────────────────────────────────────────
const { chromium, request } = await import('playwright').catch(() => fail('未安装 playwright：项目根执行 npm i -D playwright && npx playwright install chromium'))

const results = []
const jl = join(DRAFT_DIR, `script-${moduleName}-${runStamp}.jsonl`)
mkdirSync(DRAFT_DIR, { recursive: true })
mkdirSync(join(EVIDENCE_ROOT, moduleName), { recursive: true })
const suiteIds = SUITE_FILTER ? (plan.suites?.[String(SUITE_FILTER)] || []) : null
if (SUITE_FILTER && !suiteIds) fail(`--suite=${SUITE_FILTER} 未在脚本 suites 中定义`)
const cases = plan.cases.filter((c) => {
  if (CASE_FILTER && !c.id.includes(String(CASE_FILTER))) return false
  if (TAG_FILTER && !(c.tags || []).includes(String(TAG_FILTER))) return false
  if (suiteIds && !suiteIds.includes(c.id)) return false
  return true
})
if (!cases.length) fail(`筛选后无用例（case=${CASE_FILTER || '-'} tag=${TAG_FILTER || '-'} suite=${SUITE_FILTER || '-'}）`)

function pushResult(c, t0, result, summary, evidence) {
  const entry = {
    caseId: c.id, result, summary, evidencePaths: evidence.map(rel),
    source: MODE === 'api' ? 'script-api' : 'script', runStamp, durationMs: Date.now() - t0,
  }
  results.push(entry)
  appendFileSync(jl, JSON.stringify(entry) + '\n', 'utf8')   // 一条一写
  console.log(`[${result.toUpperCase()}] ${c.id} — ${summary}（${entry.durationMs}ms）`)
}

function stepError(stepNo, s, e) {
  if (e?.blocked) return e
  const tgt = s.target !== undefined ? `「${subst(String(s.target))}」` : (s.path !== undefined ? `「${subst(String(s.path))}」` : '')
  const err = new Error(`第${stepNo}步[${s.action}]${tgt} 失败：${oneLine(e?.message || String(e), 180)}`)
  err.blocked = false
  if (e?.api) err.api = e.api
  return err
}

if (MODE === 'api') {
  // ── API 模式（接口轨 · 无浏览器）─────────────────────────────────────
  const api = await request.newContext({ baseURL: BASE_URL, ignoreHTTPSErrors: true })
  let authHeaders = {}
  try {
    if (config.beforeAll) { console.log('[executor] beforeAll…'); await config.beforeAll({ bus, baseUrl: BASE_URL, api }) }
    if (typeof config.apiLogin === 'function') { console.log('[executor] apiLogin…'); authHeaders = (await config.apiLogin(api, BASE_URL, { bus })) || {} }
    for (const c of cases) {
      const t0 = Date.now()
      let result = 'pass'
      let summary = ''
      const evidence = []
      const digest = []
      try {
        let stepNo = 0
        for (const s of c.steps || []) {
          stepNo++
          const action = String(s.action || '').toLowerCase()
          let r
          try {
            if (action === 'api') { const rr = await execApiStep(api, s, authHeaders); r = rr.text; digest.push(rr.text.replace(/^api /, '')) }
            else if (action === 'note') r = `note ${subst(String(s.target ?? ''))}`
            else throw new Error(`API 模式仅支持 action=api/note（当前 ${action}；UI 步骤请用默认模式）`)
          } catch (e) { throw stepError(stepNo, s, e) }
          if (typeof r === 'string') console.log(`  [${c.id}] ${stepNo}. ${r}`)
        }
        if (typeof c.run === 'function') {
          await c.run({
            api, baseUrl: BASE_URL, bus, config,
            blocked: (m) => { throw new BlockedError(m) },
            expect: (cond, msg) => { if (!cond) throw new Error(msg || 'expect 断言失败') },
          })
        }
        summary = c.summary || (digest.length ? digest.join('；').slice(0, 110) : '通过')
      } catch (e) {
        if (e?.blocked) { result = 'blocked'; summary = oneLine(e.message) }
        else { result = 'fail'; summary = oneLine(e?.message || String(e), 220) }
        if (e?.api) {
          const f = join(EVIDENCE_ROOT, moduleName, `${c.id}-api-${runStamp}.json`)
          writeFileSync(f, JSON.stringify({ caseId: c.id, runStamp, ...e.api }, null, 2), 'utf8')
          evidence.push(f)
        }
      }
      pushResult(c, t0, result, summary, evidence)
    }
    if (config.afterAll) { console.log('[executor] afterAll…'); await config.afterAll({ bus, baseUrl: BASE_URL, api }) }
  } finally {
    await api.dispose().catch(() => {})
  }
} else {
  // ── UI 模式（默认 · 浏览器）─────────────────────────────────────────
  const browser = await chromium.launch({ headless: HEADLESS })
  const context = await browser.newContext({ viewport: { width: 1600, height: 900 } })
  let loginDone = false
  try {
    if (config.beforeAll) { console.log('[executor] beforeAll…'); await config.beforeAll({ bus, baseUrl: BASE_URL, context }) }

    for (const c of cases) {
      const t0 = Date.now()
      const page = await context.newPage()
      page.setDefaultTimeout(TIME.action)
      const consoleErrors = []
      const httpErrors = []
      page.on('console', (m) => { if (m.type() === 'error') consoleErrors.push(cut(m.text(), 200)) })
      page.on('pageerror', (e) => consoleErrors.push(cut(String(e), 200)))
      page.on('response', (r) => { if (r.status() >= 400) httpErrors.push({ status: r.status(), url: cut(r.url(), 220), method: r.request().method() }) })

      let result = 'pass'
      let summary = ''
      const evidence = []
      try {
        if (!loginDone && config.login) { await config.login(page, BASE_URL, { bus }); loginDone = true }
        if (typeof config.afterNavigate === 'function') await config.afterNavigate(page, page.url())
        let stepNo = 0
        for (const s of c.steps || []) {
          stepNo++
          let r
          try {
            r = await runStep(page, s)
          } catch (e) { throw stepError(stepNo, s, e) }
          if (r && typeof r === 'object' && r.evidence) evidence.push(r.evidence)
          if (typeof r === 'string') console.log(`  [${c.id}] ${stepNo}. ${r}`)
        }
        if (typeof c.run === 'function') {
          await c.run({
            page, context, baseUrl: BASE_URL, bus, config,
            blocked: (m) => { throw new BlockedError(m) },
            expect: (cond, msg) => { if (!cond) throw new Error(msg || 'expect 断言失败') },
            evidence: async (name) => {
              const f = join(EVIDENCE_ROOT, moduleName, `${c.id}-${name}-${runStamp}.png`)
              await page.screenshot({ path: f, fullPage: true }); evidence.push(f); return f
            },
          })
        }
        summary = c.summary || '通过'
      } catch (e) {
        if (e?.blocked) { result = 'blocked'; summary = oneLine(e.message) }
        else { result = 'fail'; summary = oneLine(e?.message || String(e), 220) }
        const shot = join(EVIDENCE_ROOT, moduleName, `${c.id}-${result}-${runStamp}.png`)
        await page.screenshot({ path: shot, fullPage: true }).catch(() => {})
        evidence.push(shot)
        if (httpErrors.length) {
          const netFile = join(EVIDENCE_ROOT, moduleName, `${c.id}-net-${runStamp}.json`)
          writeFileSync(netFile, JSON.stringify({ caseId: c.id, runStamp, httpErrors, consoleErrors }, null, 2), 'utf8')
          evidence.push(netFile)
        }
        if (consoleErrors.length) summary = oneLine(`${summary}｜console: ${consoleErrors.slice(0, 2).join(' / ')}`, 260)
      }

      pushResult(c, t0, result, summary, evidence)
      await page.close().catch(() => {})
    }

    if (config.afterAll) { console.log('[executor] afterAll…'); await config.afterAll({ bus, baseUrl: BASE_URL, context }) }
  } finally {
    await context.close().catch(() => {})
    await browser.close().catch(() => {})
  }
}

const pass = results.filter((r) => r.result === 'pass').length
const bad = results.length - pass
console.log(`\n[executor] 模块=${moduleName} runStamp=${runStamp}`)
console.log(`[executor] 通过=${pass} 非通过=${bad} 共=${results.length}｜jsonl=${jl}`)
process.exit(bad ? 1 : 0)
