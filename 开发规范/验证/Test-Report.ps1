#Requires -Version 5.1
<#
.SYNOPSIS
  开发轨报告对账：检查【验证回执】与 .gate/开发规范/completion.json 是否一致，拦截假完成措辞。
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File "开发规范/验证/Test-Report.ps1" -Report "开发/04-计划与任务/任务收尾.md"
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Report,
    [string]$Completion = ".gate/开发规范/completion.json"
)

$ErrorActionPreference = 'Stop'
$script = Join-Path $PSScriptRoot 'tools/report_lint.py'
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command py -ErrorAction SilentlyContinue }
if (-not $python) {
    Write-Output 'REPORT_LINT_PYTHON_MISSING: 需要 Python 3；结果=BLOCKED。'
    exit 1
}
& $python.Source -B $script --report $Report --completion $Completion
exit $LASTEXITCODE
