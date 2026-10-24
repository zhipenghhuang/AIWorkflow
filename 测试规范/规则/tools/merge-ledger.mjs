#!/usr/bin/env node
/**
 * merge-ledger.mjs — 执行结果 jsonl 机械合并进台账（脚本档/拆分档通用 · 双格式）
 *
 * 支持两种台账格式（自动识别表头首列）：
 *   ① 功能台账：`| 用例 ID | 标题 | 结果 | 摘要 | 证据路径 | … |`
 *      → 更新「结果/摘要/证据路径」；§1 统计表（总数…通过率）全表重算。
 *   ② 接口台账：`| caseId | 接口 | 预期 | 实际… | 判定 | 证据链接 | 备注 |`
 *      → 更新「判定(PASS/FAIL/BLOCKED…)」「证据链接」；失败时摘要补入空备注；计数行重算。
 * 不做什么：不动「模块结论/结论说明/执行日期」等需要业务语言的字段（由 AI 按专规补写）。
 *
 * 用法（项目根执行）：
 *   node 测试规范/规则/tools/merge-ledger.mjs --ledger=测试/功能测试/01-xxx执行台账.md --jsonl=测试/功能测试/.draft/script-xxx.jsonl
 *   [--dry-run] [--root=<项目根>]
 *
 * jsonl 行格式（执行器与拆分档 Worker 同格式）：
 *   {"caseId","result","summary","evidencePaths":[], ...}   result ∈ pass|fail|blocked|na|pending|todo
 *
 * 退出码：0=全部合并；1=有警告（caseId 不在台账/结果值未知）；2=硬错误（文件缺失/未找到表）。
 */

import { readFileSync, writeFileSync, existsSync } from 'node:fs'
import { resolve } from 'node:path'

const argv = process.argv.slice(2)
const arg = (name, def = undefined) => {
  const hit = argv.find((a) => a === `--${name}` || a.startsWith(`--${name}=`))
  if (hit === undefined) return def
  const eq = hit.indexOf('=')
  return eq === -1 ? true : hit.slice(eq + 1)
}
const ROOT = resolve(String(arg('root', process.cwd())))
const LEDGER = arg('ledger')
const JSONL = arg('jsonl')
const DRY = !!arg('dry-run')
if (argv.includes('--help') || argv.includes('-h') || !LEDGER || !JSONL) {
  console.log('用法: node 测试规范/规则/tools/merge-ledger.mjs --ledger=测试/功能测试/xx.md --jsonl=测试/功能测试/.draft/script-xx.jsonl [--dry-run] [--root=项目根]')
  process.exit(LEDGER && JSONL ? 0 : 2)
}

const FUNC_MAP = { pass: '通过', fail: '失败', blocked: '阻塞', na: '不适用', pending: '待实现', todo: '未执行' }
const IFACE_MAP = { pass: 'PASS', fail: 'FAIL', blocked: 'BLOCKED', na: 'N/A', pending: 'PENDING', todo: '未执行' }
const STATES = ['未执行', '通过', '失败', '阻塞', '待实现', '不适用']
const err = (m) => { console.error(`[merge-ledger] ${m}`); process.exit(2) }

const ledgerPath = resolve(ROOT, String(LEDGER))
const jsonlPath = resolve(ROOT, String(JSONL))
if (!existsSync(ledgerPath)) err(`台账不存在：${ledgerPath}`)
if (!existsSync(jsonlPath)) err(`jsonl 不存在：${jsonlPath}`)

// ── 读 jsonl ───────────────────────────────────────────────────────────────
const warnings = []
const updates = new Map()
for (const line of readFileSync(jsonlPath, 'utf8').split(/\r?\n/)) {
  const t = line.trim()
  if (!t) continue
  let o
  try { o = JSON.parse(t) } catch { warnings.push(`jsonl 行不可解析：${t.slice(0, 80)}`); continue }
  if (!o.caseId) { warnings.push(`jsonl 行缺 caseId：${t.slice(0, 80)}`); continue }
  const key = String(o.result).toLowerCase()
  if (!FUNC_MAP[key]) { warnings.push(`结果值未知：${o.caseId} result=${o.result}`); continue }
  updates.set(String(o.caseId), {
    key,
    summary: String(o.summary ?? '').replace(/\|/g, '/').trim(),
    evidence: Array.isArray(o.evidencePaths) ? o.evidencePaths.join('；') : String(o.evidencePaths ?? ''),
  })
}
if (!updates.size) err('jsonl 无有效行')

// ── 读台账 ─────────────────────────────────────────────────────────────────
const raw = readFileSync(ledgerPath, 'utf8')
const eol = raw.includes('\r\n') ? '\r\n' : '\n'
const hadTrailing = raw.endsWith('\n')
const lines = raw.split(/\r?\n/)
if (hadTrailing && lines[lines.length - 1] === '') lines.pop()

const cell = (s) => s.trim()
const isSep = (s) => /^\|[\s:|-]+\|$/.test(s.trim())
const rowCells = (s) => { const t = s.trim(); if (!t.startsWith('|')) return null; return t.replace(/^\||\|$/g, '').split('|') }

// 格式识别：表头首列 用例 ID（功能） / caseId（接口）
let ifaceMode = false
let funcHeaders = []
for (const ln of lines) {
  const c = rowCells(ln)
  if (!c) continue
  const first = cell(c[0])
  if (first === '用例 ID') { ifaceMode = false; funcHeaders = c.map(cell); break }
  if (first === 'caseId') { ifaceMode = true; break }
}

let merged = 0
const touched = new Set()
const counts = { 总数: 0, 通过: 0, 失败: 0, 阻塞: 0, 未执行: 0, 待实现: 0, 不适用: 0 }
const ifaceCounts = { PASS: 0, FAIL: 0, BLOCKED: 0 }

if (!ifaceMode) {
  // ── ① 功能台账：更新 结果/摘要/证据路径（按表头定位，兼容旧台账） ──────
  const idx = (name, fallback) => {
    const i = funcHeaders.indexOf(name)
    return i >= 0 ? i : fallback
  }
  const iResult = idx('结果', 2)
  const iSummary = idx('摘要', 3)
  const iEvidence = idx('证据路径', 4)
  for (let i = 0; i < lines.length; i++) {
    const cells = rowCells(lines[i])
    if (!cells || isSep(lines[i]) || cells.length <= Math.max(iResult, iSummary, iEvidence)) continue
    const id = cell(cells[0])
    const u = updates.get(id)
    if (!u) continue
    if (!STATES.includes(cell(cells[iResult]))) continue
    const before = cell(cells[iResult])
    cells[iResult] = ` ${FUNC_MAP[u.key]} `
    cells[iSummary] = ` ${u.summary} `
    cells[iEvidence] = ` ${u.evidence} `
    lines[i] = '|' + cells.join('|') + '|'
    merged++
    touched.add(id)
    if (DRY) console.log(`  [dry] ${id}: ${before} → ${FUNC_MAP[u.key]}｜${u.summary.slice(0, 60)}`)
  }

  // §1 统计表全表重算（按表头定位“结果”列）
  const iResultForStats = idx('结果', 2)
  for (const ln of lines) {
    const cells = rowCells(ln)
    if (!cells || isSep(ln) || cells.length <= iResultForStats) continue
    const st = cell(cells[iResultForStats])
    if (!STATES.includes(st)) continue
    if (!/^[A-Za-z]/.test(cell(cells[0]))) continue
    counts.总数++
    counts[st]++
  }
  const rate = counts.总数 ? `${Math.round((counts.通过 / counts.总数) * 1000) / 10}%（${counts.通过}/${counts.总数}）` : '0%（0/0）'
  let statsAt = -1
  for (let i = 0; i < lines.length; i++) if (/^\|\s*总数\s*\|/.test(lines[i].trim())) { statsAt = i; break }
  let statsBefore = null
  if (statsAt >= 0) {
    for (let i = statsAt + 1; i < Math.min(statsAt + 4, lines.length); i++) {
      const cells = rowCells(lines[i])
      if (!cells || isSep(lines[i])) continue
      statsBefore = lines[i]
      lines[i] = `| ${counts.总数} | ${counts.通过} | ${counts.失败} | ${counts.阻塞} | ${counts.未执行} | ${counts.待实现} | ${counts.不适用} | ${rate} |`
      break
    }
    if (statsBefore === null) warnings.push('找到统计表头但未找到数据行')
  } else {
    warnings.push('未找到 §1 统计表（| 总数 | … 表头）')
  }
  console.log(`[merge-ledger] 格式=功能台账｜合并行=${merged}/${updates.size}｜${STATES.map((s) => `${s}=${counts[s]}`).join(' ')}｜通过率=${rate}`)
  if (statsBefore) console.log(`[merge-ledger] 统计行：${statsBefore.trim()}  →  | ${counts.总数} | ${counts.通过} | ${counts.失败} | ${counts.阻塞} | ${counts.未执行} | ${counts.待实现} | ${counts.不适用} | ${rate} |`)
} else {
  // ── ② 接口台账：更新 判定/证据链接（失败补空备注），计数行重算 ──────────
  for (let i = 0; i < lines.length; i++) {
    const cells = rowCells(lines[i])
    if (!cells || isSep(lines[i]) || cells.length < 6) continue
    const id = cell(cells[0])
    const u = updates.get(id)
    if (!u) continue
    const before = cell(cells[4])
    cells[4] = ` ${IFACE_MAP[u.key]} `
    cells[5] = ` ${u.evidence} `
    if (u.key === 'pass' && u.summary && u.summary !== '通过' && cells.length >= 4 && !cell(cells[3])) cells[3] = ` ${u.summary} `   // 通过行空列补摘要（不覆盖人工内容）
    if (u.key !== 'pass' && u.key !== 'na' && cells.length >= 7 && !cell(cells[6])) cells[6] = ` ${u.summary} `
    lines[i] = '|' + cells.join('|') + '|'
    merged++
    touched.add(id)
    if (DRY) console.log(`  [dry] ${id}: ${before} → ${IFACE_MAP[u.key]}｜${u.summary.slice(0, 60)}`)
  }
  for (const ln of lines) {
    const cells = rowCells(ln)
    if (!cells || isSep(ln) || cells.length < 5) continue
    if (!/^[A-Za-z]/.test(cell(cells[0]))) continue
    const v = cell(cells[4])
    if (v in ifaceCounts) ifaceCounts[v]++
  }
  let cntAt = -1
  for (let i = 0; i < lines.length; i++) if (/^\|\s*计数\s*\|/.test(lines[i].trim())) { cntAt = i; break }
  let cntBefore = null
  if (cntAt >= 0) {
    cntBefore = lines[cntAt]
    lines[cntAt] = `| 计数 | PASS ${ifaceCounts.PASS} / FAIL ${ifaceCounts.FAIL} / BLOCKED ${ifaceCounts.BLOCKED} |`
  } else {
    warnings.push('未找到「| 计数 |」行（接口台账计数未更新）')
  }
  console.log(`[merge-ledger] 格式=接口台账｜合并行=${merged}/${updates.size}｜PASS=${ifaceCounts.PASS} FAIL=${ifaceCounts.FAIL} BLOCKED=${ifaceCounts.BLOCKED}`)
  if (cntBefore) console.log(`[merge-ledger] 计数行：${cntBefore.trim()}  →  | 计数 | PASS ${ifaceCounts.PASS} / FAIL ${ifaceCounts.FAIL} / BLOCKED ${ifaceCounts.BLOCKED} |`)
}

for (const id of updates.keys()) if (!touched.has(id)) warnings.push(`台账无此 caseId 行：${id}`)

// ── 输出 ───────────────────────────────────────────────────────────────────
console.log(`[merge-ledger] 台账=${LEDGER}`)
console.log('[merge-ledger] 提示：结论/说明类字段与执行日期需按专规由 AI 补写（本工具不动）。')
if (warnings.length) { console.log(`[merge-ledger] 警告 ${warnings.length} 条：`); warnings.forEach((w) => console.log(`  - ${w}`)) }

if (DRY) { console.log('[merge-ledger] dry-run：未写入。'); process.exit(warnings.length ? 1 : 0) }
writeFileSync(ledgerPath, lines.join(eol) + (hadTrailing ? eol : ''), 'utf8')
console.log('[merge-ledger] 已写入。')
process.exit(warnings.length ? 1 : 0)
