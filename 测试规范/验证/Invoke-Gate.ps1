#Requires -Version 5.1
<#
.SYNOPSIS
  测试轨完成门。调用 验证/tools/test_gate.py，输出项目根 .gate/测试规范/。
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File "测试规范/验证/Invoke-Gate.ps1" -Mode report -ProjectRoot "."
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File "测试规范/验证/Invoke-Gate.ps1" -Mode execute -Scope "16-ASN" -ProjectRoot "."
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File "测试规范/验证/Invoke-Gate.ps1" -Mode coverage -ProjectRoot "."
#>
[CmdletBinding()]
param(
    [string]$ProjectRoot = (Get-Location).Path,
    [ValidateSet('execute', 'report', 'writeback', 'coverage', 'review')]
    [string]$Mode = 'report',
    [string]$Scope = '',
    [switch]$Json
)

$ErrorActionPreference = 'Stop'
# Python 输出为 UTF-8；PowerShell 5.1 默认按系统代码页解码，中文会变乱码。
$env:PYTHONIOENCODING = 'utf-8'
try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding = [System.Text.Encoding]::UTF8
} catch { }
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
if ($Scope) { $gateArgs += @('--scope', $Scope) }
if ($Json) { $gateArgs += '--json' }

& $python.Source -B @gateArgs
exit $LASTEXITCODE
