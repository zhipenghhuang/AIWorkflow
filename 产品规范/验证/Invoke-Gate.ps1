#Requires -Version 5.1
<#
.SYNOPSIS
  产品轨完成门。调用 验证/tools/product_gate.py，输出 .gate/completion.json。
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File "产品规范/验证/Invoke-Gate.ps1" -Mode prd -ProjectRoot "."
#>
[CmdletBinding()]
param(
    [string]$ProjectRoot = (Get-Location).Path,
    [ValidateSet('prd', 'review', 'uat', 'change', 'writeback')]
    [string]$Mode = 'prd',
    [string]$Artifact = '',
    [switch]$Json
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

$gateArgs = @($gate, '--package-root', $packageRoot, '--project-root', (Resolve-Path -LiteralPath $ProjectRoot).Path, '--mode', $Mode)
if ($Artifact) { $gateArgs += @('--artifact', $Artifact) }
if ($Json) { $gateArgs += '--json' }

& $python.Source -B @gateArgs
exit $LASTEXITCODE
