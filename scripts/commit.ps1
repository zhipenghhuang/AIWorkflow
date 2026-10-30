# 双击 commit.bat 运行：提交推送本项目；在 deploy 环境下且项目已登记上线（online.txt）时同步更新服务器
# 本项目可脱离 deploy 单独使用：独立环境仅做提交推送（含失败补推），不依赖任何 deploy 文件。
# 在 deploy 环境下：读 surfaces.txt 区分 mirror/split；有协作待推时 split 可选仅协作/仅公开/两者（回车=两者）；
# 无待推则跳过（split 仍检查公开面，与 github/main 一致则跳过，否则补推）；
# 自动写入 projects.txt（避免漏登记）；共享 .commit-deployed（纯文档/部署成功后登记，避免重复补部署）。
# 纯文档改动（开发规范/、开发/、docs/、extras/、根说明 Markdown 等）只提交推送：不询问、不触发服务器更新。
# AI 代跑：powershell -File scripts/commit.ps1 -Message '…' [-StagedOnly] [-PushTarget both|collab|public|skip] [-NoServer|-UpdateServer]
# AI 代跑参数（人工双击 bat 不传参，仍走 Read-Host）：
#   -Message       有内容的提交信息（AI 必填；禁止空/仅空白）
#   -PushTarget    both|collab|public|skip（split 推送目标；不传则询问）
#   -StagedOnly    只提交已 git add 的暂存区（分批用；禁止 git add -A）
#   -NoServer      跳过服务器更新询问
#   -UpdateServer  AI 模式下仍更新服务器（默认 AI 模式不询问、不更新）
param(
  [string]$Message,
  [string]$PushTarget = '',
  [switch]$StagedOnly,
  [switch]$NoServer,
  [switch]$UpdateServer
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
Set-Location $repoRoot

$repoName = Split-Path $repoRoot -Leaf
$parent = Split-Path $repoRoot -Parent

# 共用电脑模式（deploy 的 unlock.bat 开启）：凭据由内存 broker 提供，不落盘、关窗失效
. (Join-Path $PSScriptRoot 'shared-mode.ps1')
$sharedMode = Initialize-SharedMode
if ($sharedMode) {
  # 防止无凭据时在终端等待输入而卡住，失败直接报错（提示重新解锁）
  $env:GIT_TERMINAL_PROMPT = '0'
  $env:GCM_INTERACTIVE = 'never'
}

# 检测是否位于 deploy 下（deploy 特征：install.sh + nginx/all-projects.conf）
$isUnderDeploy = (Test-Path (Join-Path $parent 'install.sh')) -and (Test-Path (Join-Path $parent 'nginx\all-projects.conf'))
$statePath = Join-Path $parent '.commit-deployed'
$hasState = $isUnderDeploy -and (Test-Path $statePath)
$deployed = @{}
if ($hasState) {
  foreach ($line in Get-Content $statePath) {
    $kv = $line.Trim() -split '=', 2
    if ($kv.Count -eq 2 -and $kv[0]) { $deployed[$kv[0]] = $kv[1] }
  }
}
$deployedSha = $deployed[$repoName]

# deploy 环境下：确保已写入 projects.txt（避免只跑项目 commit 导致漏登记、他机 setup 拉不到）
if ($isUnderDeploy) {
  $listPath = Join-Path $parent 'projects.txt'
  $listed = (Test-Path $listPath) -and (@(Get-Content $listPath | ForEach-Object { $_.Trim() } | Where-Object { $_ -and -not $_.StartsWith('#') }) -contains $repoName)
  if (-not $listed) {
    Add-Content -LiteralPath $listPath -Value $repoName
    Write-Host "已将本项目加入 projects.txt（未登记上线前不会部署）" -ForegroundColor Yellow
  }
}

# deploy 环境下：项目是否已登记上线（online.txt）；未登记项目只提交推送、不更新服务器
$isOnline = $true
if ($isUnderDeploy) {
  $isOnline = $false
  $onlinePath = Join-Path $parent 'online.txt'
  if (Test-Path $onlinePath) {
    $isOnline = @(Get-Content $onlinePath | ForEach-Object { $_.Trim() } | Where-Object { $_ -and -not $_.StartsWith('#') }) -contains $repoName
  }
}

# 协作面 / 公开面：优先用 deploy 的 surfaces.ps1；独立环境无 surfaces 则按 mirror
$surface = [pscustomobject]@{ Name = $repoName; Mode = 'mirror'; PublicList = ''; Topology = '' }
$hasSurfaces = $false
if ($isUnderDeploy) {
  $surfacesPs1 = Join-Path $parent 'tools\surfaces.ps1'
  if (Test-Path -LiteralPath $surfacesPs1) {
    . $surfacesPs1
    $hasSurfaces = $true
    $surface = Get-ProjectSurface -DeployRoot $parent -Name $repoName
  }
}

# 记录处理前状态：脏工作区 / 已有未推送提交 / 与已部署版本不一致 => 推送成功后需要部署
$dirty = [bool](git status --porcelain)
$branch = @(git symbolic-ref --short -q HEAD 2>$null) | Select-Object -First 1
if ([string]::IsNullOrWhiteSpace($branch)) { $branch = 'main' }
git rev-parse --verify --quiet "refs/remotes/origin/$branch" 2>$null | Out-Null
$hasUpstream = ($LASTEXITCODE -eq 0)
$aheadBefore = 0
$remoteShaBefore = ''
if ($hasUpstream) {
  $remoteShaBefore = (@(git rev-parse --verify --quiet "refs/remotes/origin/$branch" 2>$null) | Select-Object -First 1)
  if ($remoteShaBefore) { $remoteShaBefore = "$remoteShaBefore".Trim() }
  $aheadText = @(git rev-list --count "origin/$branch..HEAD" 2>$null) | Select-Object -First 1
  if ($aheadText -match '^\d+$') { $aheadBefore = [int]$aheadText }
}

# 有 .githooks 时确保钩子生效（换机后首次运行自动启用）
if (Test-Path (Join-Path $repoRoot '.githooks')) {
  $hooksPath = @(git config --get core.hooksPath 2>$null) | Select-Object -First 1
  if ([string]::IsNullOrWhiteSpace($hooksPath) -or "$hooksPath".Trim() -ne '.githooks') {
    Write-Host "启用提交钩子（.githooks）" -ForegroundColor Yellow
    git config core.hooksPath .githooks
    if ($LASTEXITCODE -ne 0) { throw '启用钩子失败' }
  }
}

$originUrl = @(git config --get remote.origin.url 2>$null) | Select-Object -First 1
$pushurls = @(git config --get-all remote.origin.pushurl 2>$null)
$githubUrl = @(git config --get remote.github.url 2>$null) | Select-Object -First 1
if ([string]::IsNullOrWhiteSpace($originUrl)) {
  Write-Host '未配置任何远程仓库：本次仅提交到本地、无法推送；配置地址后重跑即可补推' -ForegroundColor Yellow
} elseif ($surface.Mode -eq 'mirror' -and $pushurls.Count -lt 2) {
  Write-Host '提示：mirror 建议配置 gitee+github 双远程推送（见 deploy 的 DEPLOY.md 第三节第2步）' -ForegroundColor Yellow
} elseif ($hasSurfaces -and $surface.Mode -eq 'split') {
  # split 禁止 origin 双 pushurl：否则 git push origin 会把协作全量推到 GitHub，绕过公开面导出
  if ($pushurls.Count -gt 0) {
    throw "split 远程残留双 pushurl（旧 mirror 配置）。请先双击 deploy 根目录 setup.bat 或 pull.bat 校正远程后再提交（会清掉 pushurl，并确保有独立 github 公开仓）"
  }
  if ([string]::IsNullOrWhiteSpace($githubUrl)) {
    throw 'split 缺少独立 remote.github（公开仓）。请先双击 deploy 根目录 setup.bat 或 pull.bat 校正远程后再提交'
  }
}

Write-Host "=== [$repoName] 当前分支与变更 ===" -ForegroundColor Cyan
git status --short --branch

# --- AI / 非交互参数校验 ---
$hasMessageParam = $PSBoundParameters.ContainsKey('Message')
$hasPushTargetParam = -not [string]::IsNullOrWhiteSpace($PushTarget)
$aiMode = $hasMessageParam -or $StagedOnly -or $hasPushTargetParam
if ($hasMessageParam -and [string]::IsNullOrWhiteSpace($Message)) {
  throw '[-Message] 不能为空；AI 代跑须写入有内容的提交信息（主题/版本 + 简述）'
}
if ($StagedOnly -and -not $hasMessageParam) {
  throw '[-StagedOnly] 必须同时提供 -Message'
}
if ($hasMessageParam -and -not $StagedOnly) {
  throw '[-Message] AI 代跑须同时加 -StagedOnly（先 git add 本批路径）；人工双击勿传 -Message'
}
if ($hasPushTargetParam) {
  $PushTarget = $PushTarget.Trim().ToLowerInvariant()
  if ($PushTarget -notin @('both', 'collab', 'public', 'skip')) {
    throw "[-PushTarget] 无效：$PushTarget（允许 both / collab / public / skip）"
  }
}
$stagedFiles = @(git diff --cached --name-only 2>$null)
$hasStaged = $stagedFiles.Count -gt 0
$needCommit = $false
if ($StagedOnly) {
  if (-not $hasStaged) { throw '[-StagedOnly] 暂存区为空：请先对本批路径执行 git add' }
  $needCommit = $true
} elseif ($dirty) {
  $needCommit = $true
} elseif ($hasMessageParam -and -not ($aheadBefore -gt 0)) {
  throw '[-Message] 已提供但工作区无变更可提交（若只补推请去掉 -Message，或先改文件/git add）'
}

$pushed = $false
$publicPushed = $false
$needCollab = $needCommit -or ($aheadBefore -gt 0)
try {
  if ($needCommit) {
    if ($hasMessageParam) {
      $msg = $Message.Trim()
    } else {
      # 默认时间戳仅供人工双击；AI 代跑须传 -Message，禁止空回车用默认。
      $defaultMsg = 'update ' + (Get-Date -Format 'yyyy-MM-dd HH:mm')
      $msg = Read-Host "[$repoName] 提交信息（回车使用默认：$defaultMsg）"
      if ([string]::IsNullOrWhiteSpace($msg)) { $msg = $defaultMsg }
    }
    if ($StagedOnly) {
      Write-Host "[$repoName] 分批提交（仅暂存区 $($stagedFiles.Count) 个路径）..." -ForegroundColor Cyan
    } else {
      git add -A
      if ($LASTEXITCODE -ne 0) { throw 'git add 失败' }
    }
    git commit -m $msg
    if ($LASTEXITCODE -ne 0) { throw 'git commit 失败（见上方输出）' }
  } elseif ($needCollab) {
    Write-Host "[$repoName] 工作区干净，补推未同步的提交..." -ForegroundColor DarkGray
  }

  if (-not $hasSurfaces -or $surface.Mode -ne 'split') {
    if (-not $needCollab) {
      Write-Host "[$repoName] 已与远端同步，跳过推送。" -ForegroundColor DarkGray
    } else {
      if ($hasSurfaces) { Assert-CollabHeadSafeForPush -RepoPath $repoRoot -RepoName $repoName -Branch $branch }
      if ($hasUpstream) { git -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=30 push } else { git -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=30 push -u origin HEAD }
      if ($LASTEXITCODE -ne 0) { throw 'git push 失败' }
      $pushed = $true
      Write-Host "[$repoName] 提交与推送完成。" -ForegroundColor Green
    }
  } elseif (-not $needCollab) {
    $statusLine = Get-SurfaceStatusLine -RepoPath $repoRoot -Surface $surface
    Write-Host $statusLine -ForegroundColor Cyan
    Write-Host "[$repoName] 协作面已同步，检查公开面..." -ForegroundColor DarkGray
    $publicResult = Invoke-SyncPublicSurface -RepoPath $repoRoot -RepoName $repoName -ListFileName $surface.PublicList
    if ($publicResult -eq 'pushed') {
      $pushed = $true
      $publicPushed = $true
      Write-Host "[$repoName] 公开面补推完成。" -ForegroundColor Green
    }
  } else {
    $statusLine = Get-SurfaceStatusLine -RepoPath $repoRoot -Surface $surface
    if ($hasPushTargetParam) {
      $pushChoice = $PushTarget
      Write-Host "[$repoName] 推送目标（-PushTarget）：$pushChoice" -ForegroundColor Cyan
    } else {
      $pushChoice = Read-PushTargetChoice -RepoName $repoName -Surface $surface -StatusLine $statusLine
    }
    if ($pushChoice -eq 'skip') {
      Write-Host "[$repoName] 已跳过推送（本地提交保留，重跑可补推）。" -ForegroundColor Yellow
    } else {
      $doCollab = ($pushChoice -eq 'collab' -or $pushChoice -eq 'both')
      $doPublic = ($pushChoice -eq 'public' -or $pushChoice -eq 'both')
      if ($doCollab) {
        Assert-CollabHeadSafeForPush -RepoPath $repoRoot -RepoName $repoName -Branch $branch
        if ($hasUpstream) { git -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=30 push origin HEAD } else { git -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=30 push -u origin HEAD }
        if ($LASTEXITCODE -ne 0) { throw '推送协作面（origin/gitee）失败' }
        Write-Host "[$repoName] 协作面已推送到 origin。" -ForegroundColor Green
        $pushed = $true
      }
      if ($doPublic) {
        $publicResult = Invoke-SyncPublicSurface -RepoPath $repoRoot -RepoName $repoName -ListFileName $surface.PublicList
        if ($publicResult -eq 'pushed') {
          $pushed = $true
          $publicPushed = $true
        } elseif ($publicResult -eq 'skipped' -and -not $doCollab) {
          Write-Host "[$repoName] 公开面无变化。" -ForegroundColor DarkGray
        }
      }
      Write-Host "[$repoName] 提交与推送完成（$pushChoice）。" -ForegroundColor Green
    }
  }
} catch {
  Write-Host "[$repoName] 失败：$_" -ForegroundColor Red
  Write-Host '网络恢复后重跑本脚本会自动补推。' -ForegroundColor Yellow
  exit 1
}

$headSha = (git rev-parse HEAD).Trim()

# 跳过推送：不部署、不写已部署记录
if (-not $pushed) {
  Write-Host '未推送，结束。' -ForegroundColor Yellow
  exit 0
}

# 与已部署版本一致且本次无新推送 => 无需部署
$needDeploy = $isOnline -and $hasState -and ($deployedSha -ne $headSha)
$realPush = $dirty -or $aheadBefore -gt 0 -or $publicPushed
if (-not ($realPush -or $needDeploy)) {
  Write-Host '本项目无新内容，结束。' -ForegroundColor Yellow
  exit 0
}

# 纯文档：对比「已部署版本」或「推送前远端」到 HEAD 的文件清单；全部为文档则跳过服务器更新
$isDocsOnly = $false
$compareFrom = ''
if (-not [string]::IsNullOrWhiteSpace($deployedSha)) {
  $compareFrom = $deployedSha
} elseif (-not [string]::IsNullOrWhiteSpace($remoteShaBefore)) {
  $compareFrom = $remoteShaBefore
}
$files = @()
$baseOk = $false
if ($compareFrom) {
  git cat-file -e "$compareFrom^{commit}" 2>$null
  if ($LASTEXITCODE -eq 0) {
    $baseOk = $true
    $files = @(git -c core.quotepath=false diff --name-only "$compareFrom..HEAD" 2>$null)
  }
} elseif ($dirty -and $aheadBefore -eq 0) {
  $baseOk = $true
  $files = @(git -c core.quotepath=false show --pretty='' --name-only --diff-filter=ACDMRT HEAD 2>$null)
}
if ($baseOk) {
  $isDocsOnly = Test-CommitDocsOnly -Paths $files
}
if ($publicPushed) { $isDocsOnly = $false }
if ($isDocsOnly) {
  # 已登记上线：写入 .commit-deployed，避免下次再当「待补部署」反复询问
  if ($isUnderDeploy -and $isOnline -and $hasState -and $headSha -match '^[0-9a-f]{7,40}$') {
    $deployed[$repoName] = $headSha
    $lines = @($deployed.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" } | Sort-Object)
    Set-Content -LiteralPath $statePath -Value $lines
  }
  Write-Host '纯文档改动，已提交推送，跳过服务器更新。' -ForegroundColor DarkGray
  exit 0
}

# 服务器更新：deploy 环境下回车即更新；独立环境默认回车跳过。
# AI 代跑（传了 -Message/-StagedOnly/-PushTarget）默认跳过；-UpdateServer 才更新；-NoServer 强制跳过。
if ($isUnderDeploy) {
  if (-not $isOnline) {
    Write-Host '本项目未登记上线（online.txt），只提交推送、不更新服务器。' -ForegroundColor Yellow
    exit 0
  }
}
$skipServer = $NoServer -or ($aiMode -and -not $UpdateServer)
if ($skipServer) {
  Write-Host '已跳过服务器更新（AI 代跑默认跳过；需要时加 -UpdateServer）。' -ForegroundColor DarkGray
  exit 0
}
if ($aiMode -and $UpdateServer) {
  $doServer = $true
} elseif ($isUnderDeploy) {
  $goServer = Read-Host '是否同步更新服务器？(回车更新，输入 n 跳过)'
  $doServer = [string]::IsNullOrWhiteSpace($goServer) -or $goServer.Trim() -eq 'y'
} else {
  $goServer = Read-Host '未检测到 deploy 环境，如需同步更新服务器请输入 y(回车跳过)'
  $doServer = $goServer.Trim() -eq 'y'
}
if (-not $doServer) {
  Write-Host '已跳过服务器更新（重跑本脚本会再次提示）。' -ForegroundColor Yellow
  exit 0
}

if (-not (Get-Command ssh -ErrorAction SilentlyContinue)) { throw '未找到 ssh 命令，请先安装 OpenSSH 客户端' }
if ($sharedMode) {
  Write-Host "=== 正在更新服务器：$repoName ===" -ForegroundColor Cyan
  $sshAuth = @('-o', 'PreferredAuthentications=password', '-o', 'PubkeyAuthentication=no', '-o', 'NumberOfPasswordPrompts=1', '-o', 'ConnectTimeout=15')
} else {
  Write-Host "=== 正在更新服务器：$repoName ===" -ForegroundColor Cyan
  $sshAuth = @()
}
# 实时回显服务器输出；失败详情段与失败标记标红（失败详情只由 update.sh 输出这一次，末尾不再重打）
# 与 deploy/tools/commit.ps1 同一套判定：git/ssh 进度走 stderr，$ErrorActionPreference=Stop 下需降级处理
$sshLines = [System.Collections.Generic.List[string]]::new()
$inFailDetail = $false
$prevEap = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
try {
  & ssh @sshAuth root@218.244.142.65 "cd /opt/deploy && bash update.sh $repoName" 2>&1 | ForEach-Object {
    if ($_ -is [System.Management.Automation.ErrorRecord]) {
      $line = $_.Exception.Message
      if ([string]::IsNullOrEmpty($line)) { $line = "$_" }
    } else {
      $line = "$_"
    }
    [void]$sshLines.Add($line)
    if ($line -match '失败详情（可复制）') { $inFailDetail = $true }
    if ($inFailDetail -or $line -match '^==>\s+\S+\s+失败\s*$' -or $line -match '^以下项目更新失败：' -or $line -match '^失败项目：') {
      Write-Host $line -ForegroundColor Red
    } else {
      Write-Host $line
    }
    if ($inFailDetail -and $line -match '失败详情结束') { $inFailDetail = $false }
  }
} finally {
  $ErrorActionPreference = $prevEap
}

# 成败以输出标记为准（管道可能冲掉退出码）：有失败标记即失败；否则需见完成标记
$projFailed = [bool]($sshLines | Where-Object { $_ -match ("^==>\s+" + [regex]::Escape($repoName) + "\s+失败\s*$") })
$projDone = [bool]($sshLines | Where-Object { $_ -match ("^==>\s+" + [regex]::Escape($repoName) + "\s+完成\s*$") })
$allDone = [bool]($sshLines | Where-Object { $_ -match '^==>\s+全部更新完成\s*$' })

if (-not $projFailed -and ($allDone -or $projDone)) {
  # 部署成功：更新共享部署记录（保留其他项目行），避免下次重复补部署
  if ($isUnderDeploy) {
    $deployed[$repoName] = $headSha
    $lines = @($deployed.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" } | Sort-Object)
    Set-Content -LiteralPath $statePath -Value $lines
  }
  Write-Host '服务器更新完成。' -ForegroundColor Green
  exit 0
}

# 失败详情已由 update.sh 在上方输出并标红，这里只补一句结论，不重复重打
Write-Host '服务器更新失败：失败详情见上方标红部分。本地提交不受影响，重跑本脚本会自动重试。' -ForegroundColor Yellow
exit 1
