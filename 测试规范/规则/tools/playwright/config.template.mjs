/**
 * case-executor.config.mjs — 脚本档项目适配配置（模板）
 *
 * 落地：复制为项目根 `测试/脚本/case-executor.config.mjs`，替换 {占位}。
 * 约束：凭据只走环境变量；本文件是「登录契约」在脚本侧的唯一承接点——
 *       登录接口/字段/存储键变更时，只改这里。
 * 规则：测试规范/规则/专项/脚本执行.md。
 */

// ── SVG 验证码解析（P1 路径：base64 SVG 内 <text> 即明文；requester=page.request 或 APIRequestContext）──
let lastToken = null   // 会话守护与 apiLogin 共用（登录后记住）
// 单一存储键：写入与读取共用，避免“写入键与读取键不一致”这类漂移。
// 复制模板时把 {app} 替换为项目实际前缀，或用 APP_STORAGE_KEY 环境变量覆盖。
const storageKey = process.env.APP_STORAGE_KEY || '{app}_auth'
async function svgCaptchaText(requester, captchaApi) {
  const res = await requester.get(captchaApi, { failOnStatusCode: false })
  const body = await res.json().catch(() => null)
  const data = body?.data ?? {}
  const challengeId = data.challengeId ?? data.captchaId
  const image = data.captchaImage ?? data.imageDataUrl ?? ''
  if (!challengeId) throw new Error(`[脚本档] 验证码接口无 challengeId：${JSON.stringify(body).slice(0, 200)}`)
  const m = String(image).match(/^data:image\/svg\+xml;base64,(.+)$/)
  if (!m) return { challengeId, text: null, note: '非 SVG（png/jpeg）——需 OCR 或改用 UI 登录/固定码' }
  const svg = Buffer.from(m[1], 'base64').toString('utf8')
  const text = [...svg.matchAll(/<text[^>]*>([^<]+)<\/text>/g)].map((x) => x[1]).join('').replace(/\s+/g, '')
  return { challengeId, text, note: 'SVG 解析' }
}

export default {
  baseUrl: process.env.TEST_BASE_URL || '{站点根URL}',

  timeouts: { action: 15000, nav: 30000, case: 180000 },

  auth: {
    captchaApi: '{/api/auth/captcha}',
    loginApi: '{/api/auth/login}',
    userinfoApi: '{/api/auth/userinfo}',
    // 登录 body 字段名（以 Network 实测为准；示例系统样例：username/password/captchaId/captcha）
    bodyFields: { user: 'username', pass: 'password', captchaId: 'captchaId', captchaText: 'captcha' },
    tokenPath: 'data.token',
    // 前端真实读取的存储键（对照 src 中 httpClient / 状态持久化代码；变更即改此）
    localStorage: {
      [storageKey]: (t) => JSON.stringify({ state: { token: t }, version: 0 }),
    },
    // api 动作的鉴权头：多数后端要求「Authorization: Bearer <token>」请求头（Cookie 常不够，见实测）
    tokenStorageKey: storageKey,           // 与写入键同源；不再单独硬编码
    apiAuthHeader: (t) => ({ Authorization: `Bearer ${t}` }),
    cookie: { name: 'Authorization', value: (t) => t },   // 无 Cookie 形态则删本行
  },

  /** api 动作鉴权头（执行器在每次 api 步前调用；从页面 localStorage 读 token） */
  async apiHeaders(page) {
    if (!this.auth.tokenStorageKey) return {}
    const t = await page.evaluate((k) => localStorage.getItem(k), this.auth.tokenStorageKey)
    return t ? this.auth.apiAuthHeader(t) : {}
  },

  /**
   * 会话守护（执行器在每次 goto 及登录后调用）。
   * 适用：前端在启动期可能「清会话」的项目（典型成因：启动期有未带鉴权头的接口 401
   * → 前端拦截器清 token；注入式登录特别容易踩到）。无此问题的项目可整段删除。
   */
  async afterNavigate(page, url) {
    const key = this.auth.tokenStorageKey
    if (!key) return
    for (let attempt = 1; attempt <= 3; attempt++) {
      const has = await page.evaluate((k) => !!localStorage.getItem(k), key).catch(() => true)
      if (has) return
      if (!lastToken) throw new Error('[脚本档] 会话丢失且无可复用 token')
      console.log(`[脚本档] 会话被清（第${attempt}次）→ 重注入`)
      await this.applySession(page, lastToken)
      const go = url && !url.includes('/login') ? url : this.baseUrl
      await page.goto(go, { waitUntil: 'domcontentloaded' }).catch(() => {})
    }
    const ok = await page.evaluate((k) => !!localStorage.getItem(k), key).catch(() => true)
    if (!ok) throw new Error('[脚本档] 会话恢复失败（已重试 3 次）')
  },

  /** 注入会话（登录与守护共用；页面须已在应用同源下） */
  async applySession(page, token) {
    const lsResolved = Object.fromEntries(
      Object.entries(this.auth.localStorage || {}).map(([k, v]) => [k, typeof v === 'function' ? v(token) : v])
    )
    const ck = this.auth.cookie
      ? { name: this.auth.cookie.name, value: typeof this.auth.cookie.value === 'function' ? this.auth.cookie.value(token) : this.auth.cookie.value }
      : null
    await page.evaluate(({ ls, c }) => {
      for (const [k, v] of Object.entries(ls)) localStorage.setItem(k, v)
      if (c) document.cookie = `${c.name}=${c.value}; path=/`
    }, { ls: lsResolved, c: ck })
  },

  /** API 模式登录（接口轨 · `--mode=api`）：返回鉴权头对象，执行器并入每步请求 */
  async apiLogin(api, baseUrl) {
    const username = process.env.E2E_USERNAME
    const password = process.env.E2E_PASSWORD
    if (!username || !password) throw new Error('[脚本档] 缺少 E2E_USERNAME / E2E_PASSWORD 环境变量')
    const cap = await svgCaptchaText(api, baseUrl + this.auth.captchaApi)
    if (!cap.text) throw new Error(`[脚本档] 验证码不可解析：${cap.note}`)
    const f = this.auth.bodyFields
    const payload = { [f.user]: username, [f.pass]: password, [f.captchaId]: cap.challengeId, [f.captchaText]: cap.text }
    const res = await api.post(baseUrl + this.auth.loginApi, { data: payload, failOnStatusCode: false })
    const json = await res.json().catch(() => null)
    const token = String(this.auth.tokenPath).split('.').reduce((o, k) => (o == null ? undefined : o[k]), json)
    if (!token) throw new Error(`[脚本档] 登录失败 HTTP ${res.status()}：${JSON.stringify(json).slice(0, 200)}`)
    lastToken = token
    return this.auth.apiAuthHeader(token)
  },

  /** 登录（每轮一次；登录态跨用例复用） */
  async login(page, baseUrl, ctx) {
    const username = process.env.E2E_USERNAME
    const password = process.env.E2E_PASSWORD
    if (!username || !password) throw new Error('[脚本档] 缺少 E2E_USERNAME / E2E_PASSWORD 环境变量')

    // ① 取验证码（固定码项目：跳过本段，captchaId/码 按 §1 基线固定值填）
    const cap = await svgCaptchaText(page.request, baseUrl + this.auth.captchaApi)
    if (!cap.text) throw new Error(`[脚本档] 验证码不可解析：${cap.note}`)

    // ② API 登录
    const f = this.auth.bodyFields
    const payload = { [f.user]: username, [f.pass]: password, [f.captchaId]: cap.challengeId, [f.captchaText]: cap.text }
    const res = await page.request.post(baseUrl + this.auth.loginApi, { data: payload, failOnStatusCode: false })
    const json = await res.json().catch(() => null)
    const token = String(this.auth.tokenPath).split('.').reduce((o, k) => (o == null ? undefined : o[k]), json)
    if (!token) throw new Error(`[脚本档] 登录失败 HTTP ${res.status()}：${JSON.stringify(json).slice(0, 200)}`)

    // ③ 存储直注 + reload 触发前端 hydrate（回调在 Node 侧先求值，浏览器只收字符串；复用 applySession）
    lastToken = token
    await page.goto(baseUrl, { waitUntil: 'domcontentloaded' })
    await this.applySession(page, token)
    await page.reload({ waitUntil: 'domcontentloaded' })
    await page.waitForTimeout(400)                        // 给启动期竞态留出窗口（有 afterNavigate 时可缩短）
    await this.afterNavigate(page, baseUrl)

    // ④ 校验登录态（带鉴权头——多数后端仅 Cookie 不够，见实测）
    const who = await page.request.get(baseUrl + this.auth.userinfoApi, {
      headers: this.auth.apiAuthHeader(token),
      failOnStatusCode: false,
    })
    if (!who.ok()) throw new Error(`[脚本档] 登录态校验失败 HTTP ${who.status()}`)
  },

  /** 整轮前置（可选）：清历史测试数据、灌金样本（优先 API，快且可核对） */
  async beforeAll(ctx) {
    // 例：await ctx.context.request.post(ctx.baseUrl + '/api/...', { data: { prefix: `REG-${ctx.bus.get('runStamp')}` } })
  },

  /** 整轮收尾（可选）：按基线 §14/§15 停用/作废本轮 REG- 数据 */
  async afterAll(ctx) {
  },
}
