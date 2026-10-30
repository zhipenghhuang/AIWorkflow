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

function Resolve-DeployAskpassExe {
  $temp = Join-Path $env:TEMP 'deploy-askpass.exe'
  $persist = Join-Path $env:LOCALAPPDATA 'deploy-unlock\askpass.exe'
  if (Test-Path -LiteralPath $temp) { return $temp }
  if (Test-Path -LiteralPath $persist) { return $persist }
  return $null
}

function Test-DeployBrokerAlive {
  $infoPath = Join-Path $env:TEMP 'deploy-broker.info'
  if (-not (Test-Path -LiteralPath $infoPath)) { return $false }
  try {
    $kv = @{}
    foreach ($line in Get-Content -LiteralPath $infoPath) {
      $p = $line.Trim() -split '=', 2
      if ($p.Count -eq 2) { $kv[$p[0].Trim()] = $p[1].Trim() }
    }
    if ($kv['port'] -notmatch '^\d+$') { return $false }
    if ($kv['pid'] -match '^\d+$') {
      $proc = Get-Process -Id ([int]$kv['pid']) -ErrorAction SilentlyContinue
      if (-not $proc) { return $false }
    }
    $t = New-Object System.Net.Sockets.TcpClient
    try {
      $iar = $t.BeginConnect('127.0.0.1', [int]$kv['port'], $null, $null)
      if (-not $iar.AsyncWaitHandle.WaitOne(800)) { return $false }
      $t.EndConnect($iar)
      return $t.Connected
    } finally {
      $t.Close()
    }
  } catch {
    return $false
  }
}

function Restore-DeployCredentialHelpers {
  git config --global --unset-all credential.helper 2>$null
  $bak = Join-Path $env:TEMP 'deploy-helper.bak'
  $restored = @()
  if (Test-Path -LiteralPath $bak) {
    foreach ($h in Get-Content -LiteralPath $bak) {
      if (-not [string]::IsNullOrWhiteSpace($h)) {
        git config --global --add credential.helper $h
        $restored += $h
      }
    }
    Remove-Item -LiteralPath $bak -Force -ErrorAction SilentlyContinue
  }
  $hasStore = @($restored) | Where-Object { $_ -match '(?i)manager|wincred|store' }
  if (-not $hasStore) {
    if (Get-Command git-credential-manager -ErrorAction SilentlyContinue) {
      git config --global --add credential.helper manager
    } else {
      git config --global --add credential.helper wincred
    }
  }
}

function Ensure-DeployCredentialHelpers {
  $cur = @(git config --global --get-all credential.helper 2>$null)
  if ($cur.Count -eq 0) {
    Restore-DeployCredentialHelpers
    Write-Host '已补回 git credential.helper（manager/wincred）。' -ForegroundColor Yellow
  }
}

function Import-UserSshAskpassEnv {
  if (-not $env:SSH_ASKPASS) {
    $u = [Environment]::GetEnvironmentVariable('SSH_ASKPASS', 'User')
    if ($u) { $env:SSH_ASKPASS = $u }
  }
  if (-not $env:SSH_ASKPASS_REQUIRE) {
    $r = [Environment]::GetEnvironmentVariable('SSH_ASKPASS_REQUIRE', 'User')
    if ($r) { $env:SSH_ASKPASS_REQUIRE = $r }
  }
}

function Enable-ProcessAskpass {
  param([string]$Exe, [switch]$ForGit)
  if ([string]::IsNullOrWhiteSpace($Exe) -or -not (Test-Path -LiteralPath $Exe)) { return }
  if ($ForGit) { $env:GIT_ASKPASS = $Exe }
  $env:SSH_ASKPASS = $Exe
  $env:SSH_ASKPASS_REQUIRE = 'force'
  if (-not $env:DISPLAY) { $env:DISPLAY = '1' }
}

function Enable-DeploySshAskpass {
  Import-UserSshAskpassEnv
  $exe = Resolve-DeployAskpassExe
  if ($exe) { Enable-ProcessAskpass -Exe $exe }
}

function Clear-DeployAskpassFromProcess {
  foreach ($name in @('GIT_ASKPASS', 'SSH_ASKPASS', 'SSH_ASKPASS_REQUIRE')) {
    $v = [Environment]::GetEnvironmentVariable($name, 'Process')
    if ($v -and ($v -like '*deploy-askpass*' -or $v -like '*deploy-unlock*')) {
      Remove-Item "Env:$name" -ErrorAction SilentlyContinue
    }
  }
}

# 返回 $true = unlock 会话可用；$false = 常规本机凭据（credential.helper / 凭据管理器）
function Initialize-SharedMode {
  $askpassExe = Resolve-DeployAskpassExe
  $brokerOk = Test-DeployBrokerAlive
  $flag = @(git config --global --get deploy.sharedMode 2>$null) | Select-Object -First 1
  $sharedFlag = ("$flag".Trim() -eq 'true')

  if ($brokerOk -and $askpassExe) {
    Enable-ProcessAskpass -Exe $askpassExe -ForGit
    return $true
  }

  if ($sharedFlag -and -not $brokerOk) {
    Write-Host 'unlock 会话未就绪（broker 无响应）。' -ForegroundColor Yellow
    git config --global --unset deploy.sharedMode 2>$null
    Restore-DeployCredentialHelpers
    Write-Host '已切回常规模式。' -ForegroundColor Yellow
  }

  Ensure-DeployCredentialHelpers
  Clear-DeployAskpassFromProcess
  return $false
}