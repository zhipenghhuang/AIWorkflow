#Requires -Version 5.1
<#
.SYNOPSIS
  测试轨完成门。调用 verify/tools/test_gate.py，输出项目根 .gate/wf-testing/。
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Mode report -ProjectRoot "."
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Mode execute -Scope "<模块目录名>" -ProjectRoot "."
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Mode coverage -ProjectRoot "."
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Mode report -ProjectRoot "." -Strict
.EXAMPLE
  # 完成表述前先取口令：只有 CLAIM: ALLOWED 才能写“通过/准出”
  powershell -ExecutionPolicy Bypass -File "wf-testing/verify/Invoke-Gate.ps1" -Claim -Mode report -ProjectRoot "."
#>
[CmdletBinding()]
param(
    [string]$ProjectRoot = (Get-Location).Path,
    [ValidateSet('execute', 'report', 'writeback', 'coverage', 'review')]
    [string]$Mode = 'report',
    [string]$Scope = '',
    [switch]$Json,
    [switch]$Strict,
    [switch]$AllowLegacy,
    [switch]$Claim
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

if ($Claim) {
    $claimTool = Join-Path $PSScriptRoot 'tools/claim_check.py'
    if (-not (Test-Path -LiteralPath $claimTool)) {
        Write-Output 'CLAIM: DENIED - claim_check.py 缺失'
        exit 1
    }
    # 完成口径按声明的 Mode 取回执：report → report.json；writeback → writeback.json。
    $claimMode = if ($PSBoundParameters.ContainsKey('Mode')) { $Mode } else { 'report' }
    if ($claimMode -notin @('report', 'writeback')) {
        Write-Output "CLAIM: DENIED - 完成口径只认 report/writeback（当前 Mode=$claimMode）"
        exit 1
    }
    $receipt = ".gate/wf-testing/$claimMode.json"
    if (-not (Test-Path -LiteralPath (Join-Path $root $receipt))) {
        $receipt = '.gate/wf-testing/completion.json'
    }
    & $python.Source -B $claimTool --project-root $root --receipt $receipt --mode $claimMode
    exit $LASTEXITCODE
}

$gateArgs = @($gate, '--package-root', $packageRoot, '--project-root', $root, '--mode', $Mode)
if ($Scope) { $gateArgs += @('--scope', $Scope) }
if ($Json) { $gateArgs += '--json' }
if ($Strict) { $gateArgs += '--strict' }
if ($AllowLegacy) { $gateArgs += '--allow-legacy' }

& $python.Source -B @gateArgs
exit $LASTEXITCODE

