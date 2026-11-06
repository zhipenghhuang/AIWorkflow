#Requires -Version 5.1
<#
.SYNOPSIS
  产品轨完成门。调用 verify/tools/product_gate.py，输出 .gate/wf-product/{mode}.json（兼容 completion.json）。
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File "wf-product/verify/Invoke-Gate.ps1" -Mode prd -ProjectRoot "."
.EXAMPLE
  # 完成表述前先取口令：只有 CLAIM: ALLOWED 才能写“完成/通过/准出”
  powershell -ExecutionPolicy Bypass -File "wf-product/verify/Invoke-Gate.ps1" -Claim -ProjectRoot "."
#>
[CmdletBinding()]
param(
    [string]$ProjectRoot = (Get-Location).Path,
    [ValidateSet('prd', 'review', 'design-review', 'uat', 'change', 'writeback')]
    [string]$Mode = 'prd',
    [string]$Artifact = '',
    [switch]$Json,
    [switch]$Claim
)

$ErrorActionPreference = 'Stop'
$packageRoot = Split-Path -Parent $PSScriptRoot
$gate = Join-Path $PSScriptRoot 'tools/product_gate.py'

if (-not (Test-Path -LiteralPath $gate)) {
    Write-Error "GATE_NOT_FOUND: $gate"
    exit 2
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command py -ErrorAction SilentlyContinue }
if (-not $python) {
    Write-Output 'GATE_PYTHON_MISSING: 需要 Python 3；结果=BLOCKED，不得声称完成。'
    exit 1
}

$root = (Resolve-Path -LiteralPath $ProjectRoot).Path
$env:PYTHONIOENCODING = 'utf-8'

if ($Claim) {
    $claimTool = Join-Path $PSScriptRoot 'tools/claim_check.py'
    if (-not (Test-Path -LiteralPath $claimTool)) {
        Write-Output 'CLAIM: DENIED - claim_check.py 缺失'
        exit 1
    }
    # 优先读本 Mode 的专属回执（同一会话先后跑多个门时 completion.json 会被后者覆盖）
    $receipt = ".gate/wf-product/$Mode.json"
    if (-not (Test-Path -LiteralPath (Join-Path $root $receipt))) {
        $receipt = '.gate/wf-product/completion.json'
    }
    & $python.Source -B $claimTool --project-root $root --receipt $receipt --mode $Mode
    exit $LASTEXITCODE
}

$gateArgs = @($gate, '--package-root', $packageRoot, '--project-root', $root, '--mode', $Mode)
if ($Artifact) { $gateArgs += @('--artifact', $Artifact) }
if ($Json) { $gateArgs += '--json' }

& $python.Source -B @gateArgs
exit $LASTEXITCODE

