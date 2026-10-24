#Requires -Version 5.1
<#
.SYNOPSIS
  测试轨完成门。调用 验证/tools/test_gate.py，输出项目根 .gate/测试规范/。
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File "测试规范/验证/Invoke-Gate.ps1" -Mode report -ProjectRoot "."
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File "测试规范/验证/Invoke-Gate.ps1" -Mode coverage -ProjectRoot "."
#>
[CmdletBinding()]
param(
    [string]$ProjectRoot = (Get-Location).Path,
    [ValidateSet('execute', 'report', 'writeback', 'coverage')]
    [string]$Mode = 'report',
    [switch]$Json
)

$ErrorActionPreference = 'Stop'
$packageRoot = Split-Path -Parent $PSScriptRoot
$gate = Join-Path $PSScriptRoot 'tools/test_gate.py'

if (-not (Test-Path -LiteralPath $gate)) {
    Write-Error "GATE_NOT_FOUND: $gate"
    exit 2
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command py -ErrorAction SilentlyContinue }
if (-not $python) {
    Write-Output 'GATE_PYTHON_MISSING: 需要 Python 3；结果=BLOCKED，不得声称通过。'
    exit 1
}

$root = (Resolve-Path -LiteralPath $ProjectRoot).Path
$gateArgs = @($gate, '--package-root', $packageRoot, '--project-root', $root, '--mode', $Mode)
if ($Json) { $gateArgs += '--json' }

& $python.Source -B @gateArgs
exit $LASTEXITCODE
