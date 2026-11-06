# Validate step packets: every YAML step has packet; 8 sections; must_read aligned.
param(
  [Parameter(Mandatory = $true)][string]$PackageRoot
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path -LiteralPath $PackageRoot).Path
$py = Join-Path $PSScriptRoot "validate_step_packets.py"
if (-not (Test-Path -LiteralPath $py)) {
  Write-Host "FAIL: missing validate_step_packets.py" -ForegroundColor Red
  exit 1
}
$pyCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pyCmd) { $pyCmd = Get-Command py -ErrorAction SilentlyContinue }
if (-not $pyCmd) {
  Write-Host "FAIL: python not found" -ForegroundColor Red
  exit 1
}
& $pyCmd.Source -B -X utf8 $py $root
if ($LASTEXITCODE -ne 0) {
  Write-Host "Validate-StepPackets: FAILED" -ForegroundColor Red
  exit 1
}
# 生成物漂移：packets 必须与 workflows/*.yaml + _orch.yaml 源一致（只渲染不落盘）
$builder = Join-Path $PSScriptRoot "build_step_packets.py"
if (Test-Path -LiteralPath $builder) {
  $buildOut = & $pyCmd.Source -B -X utf8 $builder $root --check 2>&1
  if ($LASTEXITCODE -ne 0) {
    $buildOut | Select-Object -Last 12 | ForEach-Object { Write-Host $_ }
    Write-Host "Validate-StepPackets: FAILED（生成物与 workflows/_orch 源不一致）" -ForegroundColor Red
    exit 1
  }
}
Write-Host "Validate-StepPackets: OK" -ForegroundColor Green
exit 0
