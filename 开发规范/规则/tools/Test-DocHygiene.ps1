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

if (-not (Test-Path -LiteralPath (Join-Path $Root 'AGENTS.md'))) { $errors.Add("MISSING_CORE: AGENTS.md") }
foreach ($rel in @('规则/门.md', '规则/读取索引.md', '规则/文档治理.md')) {
    if (-not (Test-Path -LiteralPath (Join-Path $Root $rel))) { $errors.Add("MISSING_CORE: $rel") }
}
foreach ($rel in @('workflows', '规则')) {
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
}

$rulesDir = Join-Path $Root '规则'
$rules = @()
if (Test-Path -LiteralPath $rulesDir) { $rules = @(Get-ChildItem -LiteralPath $rulesDir -File -Filter *.md -ErrorAction SilentlyContinue) }
foreach ($f in $rules) {
    $n = Get-Lines $f.FullName
    if ($n -gt 240) {
        $head = (Get-Content -LiteralPath $f.FullName -Encoding UTF8 -TotalCount 5) -join "`n"
        if ($head -notmatch 'longform') { $warnings.Add("RULE_LONG: $($f.Name) $n lines (>240; add longform or split)") }
    }
}

$wfDir = Join-Path $Root 'workflows'
if (Test-Path -LiteralPath $wfDir) {
    foreach ($f in Get-ChildItem -LiteralPath $wfDir -File -Filter *.yaml) {
        $t = Get-Content -LiteralPath $f.FullName -Raw -Encoding UTF8
        if ($t -notmatch 'read_index:') { $warnings.Add("WF_NO_READ_INDEX: $($f.Name)") }
    }
}

$readIndexPath = Join-Path $Root '规则/读取索引.md'
if (Test-Path -LiteralPath $readIndexPath) {
    $readIndex = Get-Content -LiteralPath $readIndexPath -Raw -Encoding UTF8
    foreach ($f in Get-ChildItem -LiteralPath $wfDir -File -Filter *.yaml -ErrorAction SilentlyContinue) {
        if ($readIndex -notmatch [regex]::Escape($f.BaseName)) { $warnings.Add("READ_INDEX_NO_WORKFLOW: $($f.BaseName)") }
    }
}

$tplDir = Join-Path $Root '规则/模板'
if (Test-Path -LiteralPath $tplDir) {
    $corpus = @()
    foreach ($f in Get-ChildItem -LiteralPath $Root -Recurse -File -Include *.md,*.yaml) {
        if ($f.FullName.StartsWith($tplDir + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) { continue }
        $corpus += (Get-Content -LiteralPath $f.FullName -Raw -Encoding UTF8)
    }
    $text = $corpus -join "`n"
    foreach ($tpl in Get-ChildItem -LiteralPath $tplDir -File) {
        if ($text -notmatch [regex]::Escape($tpl.Name)) { $warnings.Add("ORPHAN_TEMPLATE: $($tpl.Name)") }
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
