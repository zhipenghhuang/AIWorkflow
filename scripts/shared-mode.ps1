# 共用电脑模式公共逻辑：检测 unlock.bat 的内存 broker，就绪时把 git / ssh 凭据来源指向 askpass 客户端。
# 由 scripts/ 下入口脚本调用：$sharedMode = Initialize-SharedMode（未开启共用模式时返回 $false）。
# 另含 commit 共用：无需服务器更新的改动判定（只提交推送、不询问服务器）。

# 路径是否全部「无需服务器更新」（不 rebuild / 不刷新入口）。
# - 子项目：规范包与开发文档树、说明类 Markdown、gitignore；代码/compose/Docker/依赖清单等仍需部署。
# - deploy：文档与本机入口脚本（bat/tools 下 Windows 侧）；nginx/portal/hooks/update.sh/install.sh/online.txt/projects.txt 等仍需部署（hooks 为服务器发版真源）。
function Test-CommitDocsOnly {
  param(
    [string[]]$Paths,
    [switch]$DeployRepo
  )
  if ($null -eq $Paths -or $Paths.Count -eq 0) { return $true }
  foreach ($raw in $Paths) {
    if ([string]::IsNullOrWhiteSpace($raw)) { continue }
    # git 默认 core.quotepath 可能把中文路径写成 "\345\274\200..."（UTF-8 八进制），需按字节还原后再匹配
    $name = $raw.Trim()
    if ($name.Length -ge 2 -and $name.StartsWith('"') -and $name.EndsWith('"')) {
      $esc = $name.Substring(1, $name.Length - 2)
      $buf = New-Object System.Collections.Generic.List[byte]
      for ($i = 0; $i -lt $esc.Length; $i++) {
        if ($esc[$i] -eq [char]'\' -and ($i + 3) -lt $esc.Length -and $esc.Substring($i + 1, 3) -match '^[0-7]{3}$') {
          $buf.Add([byte][Convert]::ToInt32($esc.Substring($i + 1, 3), 8)) | Out-Null
          $i += 3
        } elseif ($esc[$i] -eq [char]'\' -and ($i + 1) -lt $esc.Length) {
          $ch = switch ($esc[$i + 1]) { 'n' { "`n" } 't' { "`t" } 'r' { "`r" } '"' { '"' } '\' { '\' } default { [string]$esc[$i + 1] } }
          foreach ($b in [Text.Encoding]::UTF8.GetBytes($ch)) { $buf.Add($b) | Out-Null }
          $i += 1
        } else {
          foreach ($b in [Text.Encoding]::UTF8.GetBytes([string]$esc[$i])) { $buf.Add($b) | Out-Null }
        }
      }
      $name = [Text.Encoding]::UTF8.GetString($buf.ToArray())
    }
    $p = (($name -replace '\\', '/').Trim() -replace '^\./', '')
    if ($DeployRepo) {
      if ($p -match '^docs/') { continue }
      if ($p -match '^(README|AGENTS|activeContext)\.md$') { continue }
      if ($p -match '^\.gitattributes$') { continue }
      if ($p -match '^\.gitignore$') { continue }
      # 本机双击入口与 Windows 侧工具（不进服务器运行态）
      if ($p -match '^(commit|pull|setup|unlock)\.bat$') { continue }
      if ($p -match '^tools/(commit|pull|setup|shared-mode|unlock|surfaces|project-sync|broker-helper)\.ps1$') { continue }
      if ($p -match '^tools/(fix-opencode\.py|harden-server\.bat)$') { continue }
      if ($p -match '^surfaces\.txt$') { continue }
      # hooks/、update.sh、nginx、portal、online.txt 等均须部署
      return $false
    }
    if ($p -match '^(开发规范/|开发/|docs/|产品/|测试/|extras/)') { continue }
    if ($p -match '^(README|AGENTS|CHANGELOG|activeContext|项目档案|产品档案|运行说明|THIRD_PARTY|LICENSE)\.md$') { continue }
    if ($p -match '^(public-surface\.txt|public\.gitignore)$') { continue }
    if ($p -match '^\.public/') { continue }
    if ($p -match '^(AGENTS\.public|README\.public)\.md$') { continue }
    if ($p -match '^\.gitattributes$') { continue }
    if ($p -match '^\.gitignore$') { continue }
    # 项目本机入口脚本改动不触发该项目的服务器更新
    if ($p -match '^(commit|pull|setup|start)\.bat$') { continue }
    if ($p -match '^scripts/(commit|pull|setup|start|shared-mode)\.ps1$') { continue }
    return $false
  }
  return $true
}

function Initialize-SharedMode {
  $flag = @(git config --global --get deploy.sharedMode 2>$null) | Select-Object -First 1
  if ("$flag".Trim() -ne 'true') { return $false }

  $askpassExe = Join-Path $env:TEMP 'deploy-askpass.exe'
  $infoPath = Join-Path $env:TEMP 'deploy-broker.info'
  $brokerOk = $false
  if ((Test-Path $askpassExe) -and (Test-Path $infoPath)) {
    try {
      $kv = @{}
      foreach ($line in Get-Content -LiteralPath $infoPath) {
        $p = $line.Trim() -split '=', 2
        if ($p.Count -eq 2) { $kv[$p[0].Trim()] = $p[1].Trim() }
      }
      if ($kv['port'] -match '^\d+$') {
        $t = New-Object System.Net.Sockets.TcpClient
        $iar = $t.BeginConnect('127.0.0.1', [int]$kv['port'], $null, $null)
        $brokerOk = $iar.AsyncWaitHandle.WaitOne(800) -and $t.Connected
        $t.Close()
      }
    } catch {
      $brokerOk = $false
    }
  }
  if (-not $brokerOk) {
    # unlock 窗口被直接关闭时 finally 跑不到，会残留共用标记；这里自动复原并走常规模式
    git config --global --unset deploy.sharedMode 2>$null
    git config --global --unset-all credential.helper 2>$null
    $bak = Join-Path $env:TEMP 'deploy-helper.bak'
    if (Test-Path $bak) {
      foreach ($h in Get-Content -LiteralPath $bak) {
        if (-not [string]::IsNullOrWhiteSpace($h)) { git config --global --add credential.helper $h }
      }
      Remove-Item -LiteralPath $bak -Force -ErrorAction SilentlyContinue
    }
    Write-Host '已切回常规模式。' -ForegroundColor Yellow
    return $false
  }

  $env:GIT_ASKPASS = $askpassExe
  $env:SSH_ASKPASS = $askpassExe
  $env:SSH_ASKPASS_REQUIRE = 'force'
  return $true
}
