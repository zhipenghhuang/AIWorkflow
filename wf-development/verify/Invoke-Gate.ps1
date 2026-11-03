#Requires -Version 5.1
<#
.SYNOPSIS
  开发轨完成门（唯一入口）。调用 verify/tools/gate.py，输出项目根 .gate/wf-development/。
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File "wf-development/verify/Invoke-Gate.ps1" -ProjectRoot "."
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File "wf-development/verify/Invoke-Gate.ps1" -StartTask -TaskId "DEV-20261024-01" -ProjectRoot "."
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File "wf-development/verify/Invoke-Gate.ps1" -Mode frontend -Acceptance "{workroot}/40-tasks/任务清单.md" -ProjectRoot "."
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File "wf-development/verify/Invoke-Gate.ps1" -Acceptance "{workroot}/40-tasks/任务清单.md" -Tasklist "{workroot}/40-tasks/任务清单.md" -ProjectRoot "."
#>
[CmdletBinding()]
param(
    [string]$ProjectRoot = (Get-Location).Path,
    [ValidateSet('auto', 'frontend')]
    [string]$Mode = 'auto',
    [string]$Acceptance = '',
    [string]$Tasklist = '',
    [string]$TaskId = '',
    [switch]$StartTask,
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
    Write-Output 'GATE_PYTHON_MISSING: need Python 3; result=BLOCKED.'
    exit 1
}

$root = (Resolve-Path -LiteralPath $ProjectRoot).Path

if ($Tasklist) {
    $tasklistPath = if ([System.IO.Path]::IsPathRooted($Tasklist)) { $Tasklist } else { Join-Path $root $Tasklist }
    if (-not (Test-Path -LiteralPath $tasklistPath)) {
        Write-Output "TASKLIST_MISSING: $tasklistPath"
        exit 1
    }
    $validator = Join-Path $packageRoot 'rules/tools/validate_tasklist.py'
    & $python.Source -B $validator $tasklistPath
    if ($LASTEXITCODE -ne 0) {
        Write-Output 'TASKLIST_INVALID: [P] 文件重叠/相互依赖/并行>3 或结构不合法；不进入完成门'
        exit 1
    }
}

$gateArgs = @($gate, '--package-root', $packageRoot, '--project-root', $root, '--mode', $Mode)
if ($Acceptance) { $gateArgs += @('--acceptance', $Acceptance) }
if ($TaskId) { $gateArgs += @('--task-id', $TaskId) }
if ($StartTask) { $gateArgs += @('--start-task', $TaskId) }
if ($Json) { $gateArgs += '--json' }
if ($DryRun) { $gateArgs += '--dry-run' }
if ($AllowMissingAcceptance) { $gateArgs += '--allow-missing-acceptance' }

& $python.Source -B @gateArgs
exit $LASTEXITCODE
