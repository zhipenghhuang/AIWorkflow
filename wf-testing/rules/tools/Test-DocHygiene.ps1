# Doc hygiene / read budget check (warnings, no file changes)
# Usage: powershell -ExecutionPolicy Bypass -File rules/tools/Test-DocHygiene.ps1
param(
    [string]$Root = (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent)
)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path -LiteralPath $Root).Path
$warnings = New-Object System.Collections.Generic.List[string]
$errors = New-Object System.Collections.Generic.List[string]

function Get-Lines([string]$path) {
    if (-not (Test-Path -LiteralPath $path)) { return 0 }
    return (Get-Content -LiteralPath $path -Encoding UTF8 | Measure-Object -Line).Lines
}

function Get-ApproxTokens([string]$text) {
    if (-not $text) { return 0 }
    $cjk = ([regex]::Matches($text, '[\u4e00-\u9fff]')).Count
    $ascii = [Math]::Max(0, $text.Length - $cjk)
    return [int][Math]::Round($cjk + ($ascii / 4))
}

function Test-ReferenceDoc([string]$path) {
    $head = (Get-Content -LiteralPath $path -Encoding UTF8 -TotalCount 10) -join "`n"
    return ($head -match '读取级别[：:]\s*参考' -or $head -match '参考手册')
}

if (-not (Test-Path -LiteralPath (Join-Path $Root 'AGENTS.md'))) { $errors.Add("MISSING_CORE: AGENTS.md") }
foreach ($rel in @('rules/gates.md', 'rules/doc-governance.md')) {
    if (-not (Test-Path -LiteralPath (Join-Path $Root $rel))) { $errors.Add("MISSING_CORE: $rel") }
}
foreach ($rel in @('workflows', 'rules')) {
    if (-not (Test-Path -LiteralPath (Join-Path $Root $rel))) { $errors.Add("MISSING_DIR: $rel") }
}

$agents = Join-Path $Root 'AGENTS.md'
$agentsLines = Get-Lines $agents
if ($agentsLines -gt 220) { $errors.Add("AGENTS_TOO_LONG: $agentsLines lines (>220)") }
elseif ($agentsLines -gt 170) { $warnings.Add("AGENTS_LONG: $agentsLines lines (>170; target <=150)") }

if (Test-Path -LiteralPath $agents) {
    $nums = @()
    foreach ($line in Get-Content -LiteralPath $agents -Encoding UTF8) {
        if ($line -match '^(\d+)\.\s') { $nums += [int]$Matches[1] }
    }
    $dups = $nums | Where-Object { $_ -ge 10 } | Group-Object | Where-Object Count -gt 1 | ForEach-Object { $_.Name }
    if ($dups) { $warnings.Add("AGENTS_DUP_NUMBER(>=10): " + ($dups -join ',')) }
}

$ctx = Join-Path (Split-Path $Root -Parent) 'activeContext.md'
if (Test-Path -LiteralPath $ctx) {
    $ctxLines = Get-Lines $ctx
    if ($ctxLines -gt 60) { $warnings.Add("ACTIVE_CONTEXT_LONG: $ctxLines lines (>60; target <=30)") }
    $ctxText = [System.IO.File]::ReadAllText($ctx, [System.Text.Encoding]::UTF8)
    foreach ($spec in @(
        @{ H = '生效中的偏好'; N = 5; Code = 'ACTIVE_CONTEXT_PREF_LONG' },
        @{ H = '洞见与易踩坑'; N = 3; Code = 'ACTIVE_CONTEXT_INSIGHT_LONG' }
    )) {
        $m = [regex]::Match($ctxText, "(?ms)^###\s*$([regex]::Escape($spec.H))\s*\r?\n(.*?)(?=^###\s|\z)")
        if ($m.Success) {
            $bullets = @($m.Groups[1].Value -split "\r?\n" | Where-Object { $_ -match '^\s*-\s+' })
            if ($bullets.Count -gt $spec.N) { $warnings.Add("$($spec.Code): $($spec.H) $($bullets.Count) entries (>$($spec.N))") }
        }
    }
}

$rulesDir = Join-Path $Root 'rules'
# 存量预算基线（可选）：rules/tools/doc-budget-baseline.json = { "相对路径": 允许上限 }。
# 基线内的文件只在「超出基线」时告警（只减不增）；未登记文件一律按阈值。
$budgetBaseline = @{}
$baselinePath = Join-Path $rulesDir 'tools/doc-budget-baseline.json'
if (Test-Path -LiteralPath $baselinePath) {
    try {
        $raw = [System.IO.File]::ReadAllText($baselinePath, [System.Text.Encoding]::UTF8) | ConvertFrom-Json
        foreach ($p in $raw.PSObject.Properties) { $budgetBaseline[$p.Name] = [int]$p.Value }
    } catch { $warnings.Add("BUDGET_BASELINE_UNREADABLE: doc-budget-baseline.json") }
}
$rules = @()
if (Test-Path -LiteralPath $rulesDir) { $rules = @(Get-ChildItem -LiteralPath $rulesDir -Recurse -File -Filter *.md -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch '[\\/](模板|special|tools)[\\/]' }) }
foreach ($f in $rules) {
    $n = Get-Lines $f.FullName
    $tok = Get-ApproxTokens ([System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8))
    $isTemplate = $f.FullName -match '[\\/]templates[\\/]'
    $isReference = Test-ReferenceDoc $f.FullName
    $relKey = $f.FullName.Substring($Root.Length).TrimStart('\', '/').Replace('\', '/')
    if ($budgetBaseline.ContainsKey($relKey)) {
        if ($tok -gt $budgetBaseline[$relKey]) {
            $warnings.Add("RULE_TOKEN_GROWTH: $($f.Name) ~$tok tokens (>baseline $($budgetBaseline[$relKey]); 只减不增，新增内容改指针)")
        }
        continue
    }
    if (-not $isTemplate -and -not $isReference -and $tok -gt 3000) {
        $warnings.Add("RULE_TOKEN_BUDGET: $($f.Name) ~$tok tokens (>3000; split or move detail to skills/special)")
    }
    if ($isReference -and $tok -gt 10000) {
        $warnings.Add("REFERENCE_TOO_LONG: $($f.Name) ~$tok tokens (>10000; split reference)")
    }
    if ($n -gt 240 -and -not $isReference -and -not $isTemplate) {
        $head = (Get-Content -LiteralPath $f.FullName -Encoding UTF8 -TotalCount 5) -join "`n"
        if ($head -notmatch 'longform') { $warnings.Add("RULE_LONG: $($f.Name) $n lines (>240; add longform or split)") }
    }
}
$agentsText = [System.IO.File]::ReadAllText($agents, [System.Text.Encoding]::UTF8)
$agentsTok = Get-ApproxTokens $agentsText
if ($agentsTok -gt 7000) { $warnings.Add("AGENTS_TOKEN_BUDGET: ~$agentsTok tokens (>7000; quality-first resident hard rules; trim only conflicting restatements)") }
$s0Match = [regex]::Match($agentsText, '(?s)## 0\..*?(?=\r?\n## 1\.)')
if ($s0Match.Success) {
    $s0Tok = Get-ApproxTokens $s0Match.Value
    if ($s0Tok -gt 5500) { $warnings.Add("AGENTS_S0_TOKEN_BUDGET: ~$s0Tok tokens (>5500; pointerize into SSOT, keep hard one-liners)") }
}
$skillsDir = Join-Path $Root 'skills'
if (Test-Path -LiteralPath $skillsDir) {
    foreach ($sf in Get-ChildItem -LiteralPath $skillsDir -Recurse -File -Filter SKILL.md) {
        $tok = Get-ApproxTokens ([System.IO.File]::ReadAllText($sf.FullName, [System.Text.Encoding]::UTF8))
        if ($tok -gt 4500) { $warnings.Add("SKILL_TOKEN_BUDGET: $($sf.Directory.Name) ~$tok tokens (>4500; split references)") }
    }
}

$wfDir = Join-Path $Root 'workflows'

$tplDir = Join-Path $Root 'rules/templates'
$tplIndex = Join-Path $Root 'rules/templates/index.md'
if ((Test-Path -LiteralPath $tplDir) -and (Test-Path -LiteralPath $tplIndex)) {
    $indexText = Get-Content -LiteralPath $tplIndex -Raw -Encoding UTF8
    foreach ($tpl in Get-ChildItem -LiteralPath $tplDir -Recurse -File) {
        if ($tpl.Name -eq 'index.md') { continue }
        if ($indexText -notmatch [regex]::Escape($tpl.Name)) {
            $warnings.Add("TEMPLATE_NOT_INDEXED: $($tpl.Name)（模板索引未登记）")
        }
    }
    # 只检查表格第一列的模板名；目标路径（project-profile.md、{workroot}/…）不是模板文件。
    foreach ($line in $indexText -split "`r?`n") {
        $m = [regex]::Match($line, '^\|\s*`([^`]+\.(?:md|html|ya?ml|json|ts|mjs))`\s*\|')
        if (-not $m.Success) { continue }
        $name = $m.Groups[1].Value
        if (-not (Test-Path -LiteralPath (Join-Path $tplDir $name))) {
            $warnings.Add("TEMPLATE_INDEX_BROKEN: $name（索引指向不存在的模板）")
        }
    }
}

# Materials layout echoes (warn only): deprecate 项目文档/ and pack-root _archive/.../inbound/
$gov = Join-Path $Root 'rules/doc-governance.md'
if (Test-Path -LiteralPath $gov) {
    $govText = Get-Content -LiteralPath $gov -Raw -Encoding UTF8
    if ($govText -match '默认结构[：:].*项目文档' -or ($govText -match 'inbound/项目文档/\{' -and $govText -notmatch '旧.*项目文档')) {
        $warnings.Add('GOV_LEGACY_MATERIALS_LAYOUT: 文档治理仍把 项目文档/ 当默认（应为 inbound/{ver|topic}/）')
    }
}
$scanRoots = @()
foreach ($rel in @('workflows', 'AGENTS.md', 'README.md', 'rules/workflow.md')) {
    $p = Join-Path $Root $rel
    if (Test-Path -LiteralPath $p) { $scanRoots += $p }
}
foreach ($p in $scanRoots) {
    $files = if ((Get-Item -LiteralPath $p).PSIsContainer) {
        Get-ChildItem -LiteralPath $p -Recurse -File -Include *.md,*.yaml -ErrorAction SilentlyContinue
    } else { @(Get-Item -LiteralPath $p) }
    foreach ($f in $files) {
        $t = Get-Content -LiteralPath $f.FullName -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
        if (-not $t) { continue }
        if ($t -match '本步不改名/不移动/不标记旧' -or $t -match '本步不标记旧资料失效') {
            $warnings.Add("STALE_NO_ARCHIVE_PHRASE: $($f.Name)（确认采纳后应对 S1/S2/S3 同批归档）")
        }
        if ($t -match 'inbound/`（\*\*扁平\*\*' -or $t -match '强制扁平' -or $t -match '新项目强制扁平') {
            $warnings.Add("STALE_FLAT_MATERIALS: $($f.Name)")
        }
        if ($t -match '默认.*inbound/项目文档/' -and $t -notmatch '旧.*项目文档' -and $t -notmatch '迁') {
            $warnings.Add("STALE_PROJECT_DOC_PATH: $($f.Name)")
        }
    }
}

Write-Output "=== Doc hygiene ($Root) ==="
Write-Output ("AGENTS={0} lines; rule files={1}; workflows={2}" -f $agentsLines, $rules.Count, (Get-ChildItem -LiteralPath $wfDir -File -Filter *.yaml -ErrorAction SilentlyContinue).Count)
if ($warnings.Count -eq 0 -and $errors.Count -eq 0) {
    Write-Output 'Result: OK (no warnings)'
    exit 0
}
foreach ($w in $warnings) { Write-Output ("WARN  " + $w) }
foreach ($e in $errors) { Write-Output ("ERROR " + $e) }
if ($errors.Count -gt 0) { Write-Output ("Result: {0} error(s), {1} warning(s)" -f $errors.Count, $warnings.Count); exit 1 }
Write-Output ("Result: 0 error(s), {0} warning(s)" -f $warnings.Count)
exit 0
