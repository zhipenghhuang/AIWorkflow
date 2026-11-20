<#
.SYNOPSIS
  安装/检查提交前机检钩子（pre-commit）。

.DESCRIPTION
  把 wf-development 的「实施出口机检」接到目标项目的 git pre-commit：
  前端改动必须有本轮 .gate/frontend/gate.json（A/B 另须 ui-audit 通过）；L2+ 代码改动必须有完整的
  .gate/plan-coverage.md（含 §6 十三维）。

.EXAMPLE
  pwsh -File wf-development/verify/Install-GitHooks.ps1
  pwsh -File wf-development/verify/Install-GitHooks.ps1 -Check
#>
param(
  [string]$ProjectRoot = ".",
  [switch]$Check
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path $ProjectRoot).Path
$hookDir = Join-Path $root ".git\hooks"
$hookPath = Join-Path $hookDir "pre-commit"

if (-not (Test-Path (Join-Path $root ".git"))) {
  throw "不是 git 仓库：$root"
}

$content = @'
#!/bin/sh
# 由 wf-development/verify/Install-GitHooks.ps1 生成；实现见 precommit_gate.py
root="$(git rev-parse --show-toplevel)"
exec python "$root/wf-development/verify/tools/precommit_gate.py" --project-root "$root"
'@

if ($Check) {
  if (-not (Test-Path $hookPath)) { Write-Output "HOOK_MISSING"; exit 1 }
  $current = Get-Content $hookPath -Raw
  if ($current -like "*precommit_gate.py*") { Write-Output "HOOK_OK"; exit 0 }
  Write-Output "HOOK_FOREIGN"; exit 1
}

New-Item -ItemType Directory -Force -Path $hookDir | Out-Null
if (Test-Path $hookPath) {
  $existing = Get-Content $hookPath -Raw
  if ($existing -notlike "*precommit_gate.py*") {
    Copy-Item $hookPath "$hookPath.bak" -Force
    Write-Output "已备份原钩子到 pre-commit.bak"
  }
}
Set-Content -Path $hookPath -Value $content -Encoding utf8 -NoNewline
Write-Output "HOOK_INSTALLED: $hookPath"
Write-Output "验证：git commit 时若前端改动无本轮 gate.json/A-B ui-audit 会被阻断；绕过用 DSH_GATE_BYPASS=1（留痕）。"
