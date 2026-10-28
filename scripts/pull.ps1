# 双击 pull.bat 运行：拉取本项目最新代码
# 更新涉及依赖/数据库/初始化文件时自动运行 scripts/setup.ps1 补齐；纯代码更新不做多余初始化。
# 可脱离 deploy 独立使用；有未提交变更时跳过，不覆盖本地改动。
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
Set-Location $repoRoot

$repoName = Split-Path $repoRoot -Leaf

# 共用电脑模式（deploy 的 unlock.bat 开启）：凭据由内存 broker 提供，不落盘、关窗失效
. (Join-Path $PSScriptRoot 'shared-mode.ps1')
$sharedMode = Initialize-SharedMode
if ($sharedMode) {
  # 防止无凭据时在终端等待输入而卡住，失败直接报错（提示重新解锁）
  $env:GIT_TERMINAL_PROMPT = '0'
  $env:GCM_INTERACTIVE = 'never'
}
$initPattern = '(?i)(^|/)(package\.json|package-lock\.json|pnpm-lock\.yaml|yarn\.lock|pom\.xml|build\.gradle|requirements\.txt|pyproject\.toml|Dockerfile|docker-compose[^/]*\.ya?ml|scripts/setup\.ps1)$|\.sql$|(^|/)(db|schema|migration|migrations|seed)/'

$dirty = git status --porcelain
if ($dirty) {
  Write-Host "[$repoName] 有未提交变更，已跳过拉取（先运行 commit.bat 提交或手动处理）。" -ForegroundColor Yellow
  exit 1
}

Write-Host "=== [$repoName] git pull ===" -ForegroundColor Cyan
$before = @(git rev-parse HEAD 2>$null) | Select-Object -First 1
git pull --ff-only
if ($LASTEXITCODE -ne 0) {
  Write-Host "[$repoName] 拉取失败（网络或分叉），请检查上方输出。" -ForegroundColor Red
  exit 1
}
$after = @(git rev-parse HEAD 2>$null) | Select-Object -First 1

if ($before -eq $after) {
  Write-Host "[$repoName] 已是最新，无需更新。" -ForegroundColor Green
  exit 0
}

Write-Host "[$repoName] 已更新。" -ForegroundColor Green
$files = @(git diff --name-only $before $after 2>$null)
$needsInit = @($files | Where-Object { $_ -match $initPattern }).Count -gt 0
if (-not $needsInit) {
  Write-Host "[$repoName] 纯代码改动，无需初始化，可直接启动。" -ForegroundColor Green
  exit 0
}

$init = Join-Path $repoRoot 'scripts\setup.ps1'
if (-not (Test-Path $init)) {
  Write-Host "[$repoName] 无 scripts/setup.ps1，跳过自动初始化。" -ForegroundColor Yellow
  exit 0
}
Write-Host "[$repoName] 更新涉及依赖/数据库，自动初始化..." -ForegroundColor Cyan
& powershell -NoProfile -ExecutionPolicy Bypass -File $init
if ($LASTEXITCODE -ne 0) {
  Write-Host "[$repoName] 初始化脚本返回失败（可手动重跑 scripts/setup.ps1）。" -ForegroundColor Red
  exit 1
}
Write-Host "[$repoName] 更新完成，可直接启动。" -ForegroundColor Green
