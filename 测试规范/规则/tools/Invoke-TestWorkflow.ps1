#Requires -Version 5.1
<#
.SYNOPSIS
    测试规范包自检（精简版）：⓪ YAML 语法/基本 schema（需 python + PyYAML） ① 包内引用可解析（含 workflows/agents YAML） ② 章节锚点（`file.md`/简称 §x 标题存在；含 YAML） ③ workflows→agents 引用 + 步标记词表（hitl/when/gate）+ 能力名声明（tools/tools_allowed ⊆ 能力注册表） ④ AGENTS.md 版本单点存在。
.DESCRIPTION
    在资产目录（含 AGENTS.md）执行。实例文件引用（环境基线.md / activeContext.md / 测试/ 等）与示例占位路径不参与检查。
    自检时机：改本包后、用户点名。接入核验由 onboard 清单执行，不再依赖本脚本。
.PARAMETER Action
    保留入口动作名（默认 ValidateTemplateRefs）。
.PARAMETER Root
    资产目录（含 AGENTS.md）；默认按脚本位置（规则/tools）自动推导。
.PARAMETER Quiet
    仅输出分类结论，不列出明细。
.EXAMPLE
    规则/tools/Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs
#>
[CmdletBinding()]
param(
    [ValidateSet('ValidateTemplateRefs')]
    [string]$Action = 'ValidateTemplateRefs',
    [string]$Root = "",
    [switch]$Quiet
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

if ([string]::IsNullOrWhiteSpace($Root)) {
    $toolsDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $rulesDir = Split-Path -Parent $toolsDir
    $Root = Split-Path -Parent $rulesDir
}
$Root = (Resolve-Path -LiteralPath $Root).Path
$rulesDir = Join-Path $Root "规则"
$repoRoot = Split-Path -Parent $Root

$refFindings = New-Object System.Collections.Generic.List[string]
$anchorFindings = New-Object System.Collections.Generic.List[string]
$wfFindings = New-Object System.Collections.Generic.List[string]
$verFindings = New-Object System.Collections.Generic.List[string]
$toolFindings = New-Object System.Collections.Generic.List[string]
$refCount = 0
$anchorCount = 0

$instanceLeafs = @('activeContext.md', '环境基线.md', '测试计划.md', '测试报告.md', '交接台账.md', '00-交接说明.md', '01-交接清单.md', '接收回执.md')
$instancePrefixes = @('测试/', 'docs/', '项目资料/', '.gate/', '04-回执/')

function Test-InstanceRef {
    param([string]$Token)
    $t = $Token.Replace('\', '/')
    if ($t -match '[{}…]') { return $true }
    if ($instanceLeafs -contains (Split-Path $t -Leaf)) { return $true }
    foreach ($p in $instancePrefixes) {
        if ($t.StartsWith($p, [StringComparison]::OrdinalIgnoreCase)) { return $true }
    }
    return $false
}

function Get-RefTargetPath {
    param([string]$Token, [string]$SrcDir)
    $t = $Token.Replace('\', '/')
    $leaf = Split-Path $t -Leaf
    $hasPath = [bool]($t -match '[\\/]')
    $candidates = @(
        (Join-Path $SrcDir $t),
        (Join-Path $Root $t),
        (Join-Path $rulesDir $t),
        (Join-Path $repoRoot $t)
    )
    if ($t.StartsWith('规则/')) { $candidates += (Join-Path $rulesDir $t.Substring(3)) }
    if (-not $hasPath) {
        $candidates += @(
            (Join-Path $SrcDir $leaf),
            (Join-Path $Root $leaf),
            (Join-Path $rulesDir $leaf),
            (Join-Path $repoRoot $leaf)
        )
    }
    foreach ($c in $candidates) {
        if (Test-Path -LiteralPath $c -PathType Leaf) { return (Resolve-Path -LiteralPath $c).Path }
    }
    if (-not $hasPath) {
        $hits = @(Get-ChildItem -LiteralPath $rulesDir -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -eq $leaf })
        if ($hits.Count -ge 1) { return $hits[0].FullName }
    }
    return $null
}

$sectionCache = @{}
function Get-SectionNumbers {
    param([string]$Path)
    if ($sectionCache.ContainsKey($Path)) { return , $sectionCache[$Path] }
    $set = New-Object System.Collections.Generic.HashSet[string]
    foreach ($hl in [System.IO.File]::ReadAllLines($Path, [System.Text.Encoding]::UTF8)) {
        $hm = [regex]::Match($hl, '^#{1,6}\s*(\d+(?:\.\d+)*)')
        if ($hm.Success) { [void]$set.Add($hm.Groups[1].Value) }
    }
    $sectionCache[$Path] = $set
    return , $set
}

function Get-RelPath {
    param([string]$Path)
    if ($Path.StartsWith($Root, [StringComparison]::OrdinalIgnoreCase)) {
        return $Path.Substring($Root.Length).TrimStart('\', '/')
    }
    return $Path
}

# ---------- 扫描文件清单 ----------
$scanFiles = New-Object System.Collections.Generic.List[string]
foreach ($rel in @('AGENTS.md', 'README.md')) {
    $p = Join-Path $Root $rel
    if (Test-Path -LiteralPath $p) { $scanFiles.Add($p) }
}
if (Test-Path -LiteralPath $rulesDir) {
    Get-ChildItem -LiteralPath $rulesDir -Recurse -File -Filter '*.md' -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notmatch '[\\/]tools[\\/]' } |
        ForEach-Object { $scanFiles.Add($_.FullName) }
}
$capDir = Join-Path $Root '能力'
if (Test-Path -LiteralPath $capDir) {
    Get-ChildItem -LiteralPath $capDir -Recurse -File -Filter '*.md' -ErrorAction SilentlyContinue |
        ForEach-Object { $scanFiles.Add($_.FullName) }
}
$skillDir = Join-Path $Root '技能'
if (Test-Path -LiteralPath $skillDir) {
    Get-ChildItem -LiteralPath $skillDir -Recurse -File -Filter '*.md' -ErrorAction SilentlyContinue |
        ForEach-Object { $scanFiles.Add($_.FullName) }
}

# ---------- [1/4] 引用可解析 ----------
foreach ($file in $scanFiles) {
    $srcDir = Split-Path -Parent $file
    $lineNo = 0
    foreach ($line in [System.IO.File]::ReadAllLines($file, [System.Text.Encoding]::UTF8)) {
        $lineNo++
        foreach ($m in [regex]::Matches($line, '`([^`]+?\.(?:md|ps1))`')) {
            $token = $m.Groups[1].Value.Trim()
            $refCount++
            if ($token -match '^(https?:|mailto:)') { continue }
            if ($token -match '[{}…*|<>]') { continue }
            if (Test-InstanceRef -Token $token) { continue }
            if (Get-RefTargetPath -Token $token -SrcDir $srcDir) { continue }
            $refFindings.Add("MISSING_REF: $(Get-RelPath $file):${lineNo}: $token")
        }
    }
}

# ---------- [2/4] 章节锚点（`file.md` §x 须在目标文件中存在对应标题） ----------
foreach ($file in $scanFiles) {
    $srcDir = Split-Path -Parent $file
    $lineNo = 0
    foreach ($line in [System.IO.File]::ReadAllLines($file, [System.Text.Encoding]::UTF8)) {
        $lineNo++
        foreach ($m in [regex]::Matches($line, '`([^`]+\.md)`(?:\*\*)?\s*§\s*(\d+(?:\.\d+)*)(?![\d\-/])')) {
            $token = $m.Groups[1].Value.Trim()
            $sec = $m.Groups[2].Value
            $anchorCount++
            if ($token -match '^(https?:|mailto:)') { continue }
            if ($token -match '[{}…*|<>]') { continue }
            if (Test-InstanceRef -Token $token) { continue }
            $tgt = Get-RefTargetPath -Token $token -SrcDir $srcDir
            if (-not $tgt) { continue }
            if (-not (Get-SectionNumbers -Path $tgt).Contains($sec)) {
                $anchorFindings.Add("STALE_ANCHOR: $(Get-RelPath $file):${lineNo}: $token §$sec")
            }
        }
    }
}

# ---------- [1/4][2/4] 扩展：workflows / agents 的 YAML ----------
$yamlFiles = New-Object System.Collections.Generic.List[string]
foreach ($sub in @('workflows', 'agents')) {
    $subDir = Join-Path $Root $sub
    if (Test-Path -LiteralPath $subDir) {
        Get-ChildItem -LiteralPath $subDir -Filter '*.yaml' -File -ErrorAction SilentlyContinue |
            ForEach-Object { $yamlFiles.Add($_.FullName) }
    }
}

$shorthandMap = @{
    '工作流'  = '规则/工作流.md'
    '多Agent' = '规则/专项/多Agent与输出.md'
    'AGENTS'  = 'AGENTS.md'
    '基线'    = '环境基线.md'
}

function Test-SectionMatch {
    param($Set, [string]$Piece)
    if ($Set.Contains($Piece)) { return $true }
    foreach ($h in $Set) { if ($h.StartsWith($Piece + '.')) { return $true } }
    return $false
}

foreach ($file in $yamlFiles) {
    $srcDir = Split-Path -Parent $file
    $lineNo = 0
    foreach ($line in [System.IO.File]::ReadAllLines($file, [System.Text.Encoding]::UTF8)) {
        $lineNo++
        if ($line -match '^\s*#') { continue }

        $cands = New-Object System.Collections.Generic.List[object]
        foreach ($m in [regex]::Matches($line, '([^\s`（）()【】「」《》、：:，,；;。*…§{}<>|]+\.(?:yaml|ps1|md))')) {
            $tok = $m.Groups[1].Value.Trim()
            $refCount++
            $isInstance = Test-InstanceRef -Token $tok
            $tgt = $null
            if (-not $isInstance -and $tok -notmatch '^(https?:|mailto:)') {
                $tgt = Get-RefTargetPath -Token $tok -SrcDir $srcDir
                if (-not $tgt) {
                    $refFindings.Add("MISSING_REF: $(Get-RelPath $file):${lineNo}: $tok")
                }
            }
            $cands.Add([pscustomobject]@{ Index = $m.Index; Target = $tgt; Skip = $isInstance })
        }
        foreach ($name in $shorthandMap.Keys) {
            $idx = 0
            while (($idx = $line.IndexOf($name, $idx, [System.StringComparison]::Ordinal)) -ge 0) {
                $rootTok = $shorthandMap[$name]
                $isInstance = Test-InstanceRef -Token $rootTok
                $tgt = $null
                if (-not $isInstance) { $tgt = Get-RefTargetPath -Token $rootTok -SrcDir $srcDir }
                $cands.Add([pscustomobject]@{ Index = $idx; Target = $tgt; Skip = $isInstance })
                $idx += $name.Length
            }
        }

        if ($cands.Count -eq 0) { continue }
        foreach ($am in [regex]::Matches($line, '§\s*([\d.\-/]+)')) {
            $anchorCount++
            $before = @($cands | Where-Object { $_.Index -lt $am.Index })
            if ($before.Count -eq 0) { continue }
            $c = $before | Sort-Object Index | Select-Object -Last 1
            if ($c.Skip -or -not $c.Target) { continue }
            $chunk = $am.Groups[1].Value.Trim([char[]]@('/', '.'))
            if ([string]::IsNullOrWhiteSpace($chunk) -or $chunk -notmatch '\d') { continue }
            if ($chunk.Contains('-')) { $pieces = @(($chunk -split '-')[0]) } else { $pieces = @($chunk -split '/') }
            $set = Get-SectionNumbers -Path $c.Target
            foreach ($p in $pieces) {
                if ([string]::IsNullOrWhiteSpace($p)) { continue }
                if (-not (Test-SectionMatch -Set $set -Piece $p)) {
                    $leaf = Split-Path $c.Target -Leaf
                    $anchorFindings.Add("STALE_ANCHOR: $(Get-RelPath $file):${lineNo}: $leaf §$p")
                }
            }
        }
    }
}

# ---------- [3/4] workflows → agents ----------
$wfDir = Join-Path $Root 'workflows'
$agDir = Join-Path $Root 'agents'
$agentIds = @{}
if (Test-Path -LiteralPath $agDir) {
    Get-ChildItem -LiteralPath $agDir -Filter '*.yaml' -File -ErrorAction SilentlyContinue | ForEach-Object {
        $agentIds[$_.BaseName] = $true
        $text = [System.IO.File]::ReadAllText($_.FullName, [System.Text.Encoding]::UTF8)
        $idm = [regex]::Match($text, '(?m)^id:\s*(\S+)')
        if ($idm.Success) { $agentIds[$idm.Groups[1].Value.Trim([char[]]@("'", '"'))] = $true }
    }
}
else { $wfFindings.Add('WF_MISSING: agents/') }
if (Test-Path -LiteralPath $wfDir) {
    Get-ChildItem -LiteralPath $wfDir -Filter '*.yaml' -File -ErrorAction SilentlyContinue | ForEach-Object {
        $wfName = $_.Name
        foreach ($line in [System.IO.File]::ReadAllLines($_.FullName, [System.Text.Encoding]::UTF8)) {
            $am = [regex]::Match($line, '^\s*agent:\s*(\S+)\s*$')
            if ($am.Success) {
                $id = $am.Groups[1].Value.Trim([char[]]@("'", '"'))
                if (-not $agentIds.ContainsKey($id)) {
                    $wfFindings.Add("WF_AGENT_MISSING: ${wfName}: agent '$id' 未在 agents/ 找到")
                }
            }
        }
    }
}
else { $wfFindings.Add('WF_MISSING: workflows/') }

# ---------- [3/4] 步标记词表（YAML 使用 ⊆ AGENTS.md 声明） ----------
$agentsPath = Join-Path $Root 'AGENTS.md'
$agentsText = ''
if (Test-Path -LiteralPath $agentsPath) { $agentsText = [System.IO.File]::ReadAllText($agentsPath, [System.Text.Encoding]::UTF8) }
foreach ($declRel in @('规则/门.md', '规则/读取索引.md', '规则/核心/维护.md')) {
    $declPath = Join-Path $Root $declRel
    if (Test-Path -LiteralPath $declPath) { $agentsText += "`n" + [System.IO.File]::ReadAllText($declPath, [System.Text.Encoding]::UTF8) }
}
$declaredNames = New-Object System.Collections.Generic.HashSet[string]
$declaredWhen = New-Object System.Collections.Generic.HashSet[string]
$declaredGates = New-Object System.Collections.Generic.HashSet[string]
foreach ($m in [regex]::Matches($agentsText, '`([^`\r\n]+)`')) {
    $tok = $m.Groups[1].Value.Trim()
    if ($tok -match '^(select|confirm)_[a-z_]+$') { [void]$declaredNames.Add($tok) }
    elseif ($tok -match '^[a-z]+(_[a-z]+)+$') { [void]$declaredWhen.Add($tok) }
    if ($tok -match '^gate:\s*([a-z][a-z0-9-]*)$') { [void]$declaredGates.Add($Matches[1]) }
}
if (Test-Path -LiteralPath $wfDir) {
    Get-ChildItem -LiteralPath $wfDir -Filter '*.yaml' -File -ErrorAction SilentlyContinue | ForEach-Object {
        $fName = $_.Name
        $ln = 0
        $hitlIndent = -1
        foreach ($line in [System.IO.File]::ReadAllLines($_.FullName, [System.Text.Encoding]::UTF8)) {
            $ln++
            if ($line -match '^\s*$' -or $line -match '^\s*#') { continue }
            $ind = 0
            if ($line -match '^(\s+)') { $ind = $Matches[1].Length }
            if ($line -match '^\s*hitl:\s*(\S+)?') {
                $hitlIndent = $ind
                $v = $Matches[1]
                if ($v -and -not $declaredNames.Contains($v)) { $wfFindings.Add("TOKEN_UNDECLARED: ${fName}:${ln}: 门名 '$v' 未在 AGENTS/门/读取索引 声明") }
                continue
            }
            if ($hitlIndent -ge 0) {
                if ($ind -le $hitlIndent) { $hitlIndent = -1 }
                else {
                    if ($line -match '^\s*-\s*name:\s*(\S+)') {
                        $v = $Matches[1]
                        if (-not $declaredNames.Contains($v)) { $wfFindings.Add("TOKEN_UNDECLARED: ${fName}:${ln}: 门名 '$v' 未在 AGENTS/门/读取索引 声明") }
                    }
                    if ($line -match '^\s*when:\s*(\S+)') {
                        $v = $Matches[1]
                        if (-not $declaredWhen.Contains($v)) { $wfFindings.Add("TOKEN_UNDECLARED: ${fName}:${ln}: when '$v' 未在 AGENTS/门/读取索引 声明") }
                    }
                    continue
                }
            }
            if ($line -match '^\s*hitl_when:\s*(\S+)') {
                $v = $Matches[1]
                if (-not $declaredWhen.Contains($v)) { $wfFindings.Add("TOKEN_UNDECLARED: ${fName}:${ln}: when '$v' 未在 AGENTS/门/读取索引 声明") }
            }
            if ($line -match '^\s*gate:\s*(\S+)') {
                $v = $Matches[1]
                if (-not $declaredGates.Contains($v)) { $wfFindings.Add("TOKEN_UNDECLARED: ${fName}:${ln}: gate '$v' 未在 AGENTS/门/读取索引 声明") }
            }
            if ($line -match '^\s*gate_when:\s*(\S+)') {
                $v = $Matches[1]
                if (-not $declaredWhen.Contains($v)) { $wfFindings.Add("TOKEN_UNDECLARED: ${fName}:${ln}: gate_when '$v' 未在 AGENTS/门/读取索引 声明") }
            }
        }
    }
}

# ---------- [3/4] 能力名声明（YAML tools/tools_allowed ⊆ 能力/00-能力注册表.md） ----------
$capRegistryPath = Join-Path $Root '能力/00-能力注册表.md'
if (Test-Path -LiteralPath $capRegistryPath) {
    $declaredCaps = New-Object System.Collections.Generic.HashSet[string]
    foreach ($line in [System.IO.File]::ReadAllLines($capRegistryPath, [System.Text.Encoding]::UTF8)) {
        $cm = [regex]::Match($line, '^\|\s*`([^`|]+)`\s*\|')
        if ($cm.Success) { [void]$declaredCaps.Add($cm.Groups[1].Value.Trim()) }
    }
    foreach ($sub in @('workflows', 'agents')) {
        $subDir = Join-Path $Root $sub
        if (-not (Test-Path -LiteralPath $subDir)) { continue }
        Get-ChildItem -LiteralPath $subDir -Filter '*.yaml' -File -ErrorAction SilentlyContinue | ForEach-Object {
            $capFile = $_.Name
            $capLn = 0
            $blockIndent = -1
            foreach ($line in [System.IO.File]::ReadAllLines($_.FullName, [System.Text.Encoding]::UTF8)) {
                $capLn++
                if ($line -match '^\s*$' -or $line -match '^\s*#') { continue }
                $ind = 0
                if ($line -match '^(\s+)') { $ind = $Matches[1].Length }
                if ($line -match '^\s*(tools|tools_allowed):\s*$') { $blockIndent = $ind; continue }
                if ($blockIndent -ge 0) {
                    if ($ind -le $blockIndent) { $blockIndent = -1 }
                    elseif ($line -match '^\s*-\s*(.+)$') {
                        $item = $Matches[1].Trim()
                        $im = [regex]::Match($item, '^([^\s（(：:，,]+)')
                        if ($im.Success) {
                            $cap = $im.Groups[1].Value.Trim()
                            if (-not $declaredCaps.Contains($cap)) {
                                $wfFindings.Add("CAP_UNDECLARED: ${capFile}:${capLn}: 能力名 '$cap' 未在 能力/00-能力注册表.md 声明")
                            }
                        }
                    }
                    continue
                }
            }
        }
    }
}

# ---------- [4/4] 版本单点（AGENTS.md） ----------
$version = $null
$agentsPath = Join-Path $Root 'AGENTS.md'
if (Test-Path -LiteralPath $agentsPath) {
    foreach ($line in ([System.IO.File]::ReadAllLines($agentsPath, [System.Text.Encoding]::UTF8) | Select-Object -First 20)) {
        if ($line -notmatch 'template_version') { continue }
        $vm = [regex]::Match($line, '`(\d{4}\.\d{2}\.\d{2}[^`]*)`')
        if ($vm.Success) { $version = $vm.Groups[1].Value.Trim() }
    }
}
if (-not $version) { $verFindings.Add('VERSION_MISSING: AGENTS.md 未找到 template_version（版本单点）') }

# ---------- [0/5] YAML 语法 / 基本 schema（需要 python + PyYAML） ----------
$yamlStatus = '跳过（未找到 python）'
$pyCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pyCmd) { $pyCmd = Get-Command py -ErrorAction SilentlyContinue }
$validator = Join-Path $rulesDir 'tools/validate_workflow.py'
if ($pyCmd -and (Test-Path -LiteralPath $validator)) {
    $yamlOut = & $pyCmd.Source -B -X utf8 $validator $Root 2>&1
    if ($LASTEXITCODE -eq 0) {
        $yamlStatus = 'OK'
    }
    else {
        $yamlStatus = '失败'
        foreach ($l in $yamlOut) { $toolFindings.Add("YAML: $l") }
    }
}
elseif ($pyCmd -and -not (Test-Path -LiteralPath $validator)) {
    $yamlStatus = '缺少 validate_workflow.py'
}
elseif (-not $pyCmd) {
    $toolFindings.Add('YAML_SKIPPED: 未找到 python，YAML 语法未验证')
}

# ---------- 输出 ----------
Write-Output "=== 测试规范自检（$Action · 精简版） ==="
Write-Output "根目录：$Root"
Write-Output ("[0/5] YAML 语法/schema：{0}" -f $yamlStatus)
Write-Output ("[1/5] 引用可解析（扫描 {0} 处）：{1}" -f $refCount, $(if ($refFindings.Count -eq 0) { 'OK' } else { "$($refFindings.Count) 处待处理" }))
Write-Output ("[2/5] 章节锚点（扫描 {0} 处）：{1}" -f $anchorCount, $(if ($anchorFindings.Count -eq 0) { 'OK' } else { "$($anchorFindings.Count) 处待处理" }))
Write-Output ("[3/5] workflows→agents + 步标记词表 + 能力名：{0}" -f $(if ($wfFindings.Count -eq 0) { 'OK' } else { "$($wfFindings.Count) 处待处理" }))
Write-Output ("[4/5] 版本单点：{0}" -f $(if ($verFindings.Count -eq 0) { "OK（$version）" } else { '未通过' }))

$total = $refFindings.Count + $anchorFindings.Count + $wfFindings.Count + $verFindings.Count + $toolFindings.Count
if ($total -eq 0) {
    Write-Output '结果：全部通过。'
    exit 0
}
if (-not $Quiet) {
    foreach ($f in ($toolFindings + $refFindings + $anchorFindings + $wfFindings + $verFindings)) { Write-Output ("  - " + $f) }
}
Write-Output "结果：存在 $total 处待处理项。"
exit 1
