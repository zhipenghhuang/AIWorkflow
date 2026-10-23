#Requires -Version 5.1
<#
.SYNOPSIS
  开发轨完成门（唯一入口）。调用 验证/tools/gate.py，输出 .gate/completion.json。
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File "开发规范/验证/Invoke-Gate.ps1" -ProjectRoot "."
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File "开发规范/验证/Invoke-Gate.ps1" -Mode frontend -Acceptance "开发/03-计划与状态/任务清单.md"
#>
[CmdletBinding()]
param(
    [string]$ProjectRoot = (Get-Location).Path,
    [ValidateSet('auto', 'frontend')]
    [string]$Mode = 'auto',
    [string]$Acceptance = '',
    [switch]$Json,
    [switch]$DryRun,
    [switch]$AllowMissingAcceptance
)

$ErrorActionPreference = 'Stop'
$packageRoot = Split-Path -Parent $PSScriptRoot
$gate = Join-Path $PSScriptRoot 'tools/gate.py'

if (-not (Test-Path -LiteralPath $gate)) {
    Write-Error "GATE_NOT_FOUND: $gate"
    exit 2
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command py -ErrorAction SilentlyContinue }
if (-not $python) {
    Write-Output 'GATE_PYTHON_MISSING: 需要 Python 3；无法运行完成门。结果=BLOCKED，不得声称完成。'
    exit 1
}

$gateArgs = @($gate, '--package-root', $packageRoot, '--project-root', (Resolve-Path -LiteralPath $ProjectRoot).Path, '--mode', $Mode)
if ($Acceptance) { $gateArgs += @('--acceptance', $Acceptance) }
if ($Json) { $gateArgs += '--json' }
if ($DryRun) { $gateArgs += '--dry-run' }
if ($AllowMissingAcceptance) { $gateArgs += '--allow-missing-acceptance' }

& $python.Source @gateArgs
exit $LASTEXITCODE
