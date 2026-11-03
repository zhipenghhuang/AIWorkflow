#Requires -Version 5.1
<#
.SYNOPSIS
    初始化项目文档骨架（只建目录/索引，不移动、不删除任何文件）。
.DESCRIPTION
    按 layout.yaml 的单/多包布局创建工作区、docs/materials、inbound、handoff 与 _archive，
    并生成索引骨架：
      - 单包：docs/INDEX.md 即工作区索引
      - 多包：docs/{owner}/INDEX.md 为工作区索引；docs/INDEX.md 为项目总览
    已有目录/文件跳过；无内容不建空目录。
.PARAMETER ProjectRoot
    项目根目录；默认当前目录。
.PARAMETER Mode
    single（包在根下、工作区 docs 平铺）或 multi（包在 wf/、工作区 docs/{owner}）。
.PARAMETER Owner
    product / development / testing；默认 development。
.PARAMETER DryRun
    只输出将创建的目录/文件，不落盘。
.EXAMPLE
    powershell -NoProfile -ExecutionPolicy Bypass -File "rules/tools/Initialize-Docs.ps1" -ProjectRoot "." -Mode single -Owner development
#>
[CmdletBinding()]
param(
    [string]$ProjectRoot = (Get-Location).Path,
    [ValidateSet('single', 'multi')]
    [string]$Mode = 'single',
    [ValidateSet('product', 'development', 'testing')]
    [string]$Owner = 'development',
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

$ProjectRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
$packageId = "wf-$Owner"
$workrootRel = if ($Mode -eq 'single') { 'docs' } else { "docs/$Owner" }
$workroot = Join-Path $ProjectRoot ($workrootRel -replace '/', [IO.Path]::DirectorySeparatorChar)
$docs = Join-Path $ProjectRoot 'docs'
$inbound = Join-Path $ProjectRoot 'inbound'
$materials = Join-Path $docs 'materials'
$planFile = switch ($Owner) {
    'product' { 'product-plan.md' }
    'testing' { 'test-plan.md' }
    default { 'development-plan.md' }
}

$commonDirs = @('docs', 'docs/materials', 'inbound')
$workDirs = switch ($Owner) {
    'development' {
        @('00-governance', '10-requirements', '20-design', '30-architecture/ADR', '40-tasks', '50-verification', '60-release', '70-ops', '80-retrospectives', 'capabilities', 'handoff', '_archive')
    }
    'product' {
        @('00-governance', 'user', 'capabilities', 'handoff', '_archive')
    }
    'testing' {
        @('functional', 'api', 'exploratory', 'random-flows', 'pre-release', 'changes', 'scripts', 'capabilities', 'handoff', '_archive')
    }
}

$created = @()
function New-DirIfMissing([string]$Path) {
    if (Test-Path -LiteralPath $Path -PathType Container) { return }
    if (-not $DryRun) { New-Item -ItemType Directory -Path $Path -Force | Out-Null }
    $script:created += $Path
}
function New-FileIfMissing([string]$Path, [string]$Content) {
    if (Test-Path -LiteralPath $Path -PathType Leaf) { return }
    if (-not $DryRun) {
        $dir = Split-Path -Parent $Path
        if ($dir) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
        [IO.File]::WriteAllText($Path, $Content, (New-Object System.Text.UTF8Encoding $false))
    }
    $script:created += $Path
}

foreach ($rel in $commonDirs) { New-DirIfMissing (Join-Path $ProjectRoot ($rel -replace '/', [IO.Path]::DirectorySeparatorChar)) }
foreach ($rel in $workDirs) { New-DirIfMissing (Join-Path $workroot ($rel -replace '/', [IO.Path]::DirectorySeparatorChar)) }

$layoutPath = Join-Path $ProjectRoot 'layout.yaml'
if (-not (Test-Path -LiteralPath $layoutPath)) {
    $packageBlock = if ($Mode -eq 'single') {
        @"
  packages:
    ${packageId}:
      root: $packageId
      workroot: docs
      handoff_root: docs/handoff
      archive_root: docs/_archive
"@
    } else {
        @"
  packages:
    ${packageId}:
      root: wf/$packageId
      workroot: docs/$Owner
      handoff_root: docs/$Owner/handoff
      archive_root: docs/$Owner/_archive
"@
    }
    $layout = @"
layout:
  mode: $Mode
  version: 2
  inbound_root: inbound
  ssot_root: docs
  materials_root: docs/materials
$packageBlock
"@
    New-FileIfMissing $layoutPath $layout
} else {
    $layoutText = Get-Content -LiteralPath $layoutPath -Raw -Encoding UTF8
    if ($layoutText -notmatch "mode:\s*$Mode") {
        throw "LAYOUT_MODE_CONFLICT: layout.yaml 不是 mode=$Mode；先确认布局或改用正确 Mode。"
    }
}

$now = (Get-Date).ToString('yyyy-MM-dd HH:mm')

$wsIndexTpl = @'
# 文档索引 — __OWNER__

> 更新：__NOW__ ｜ 工作根：`__WORKROOT__/`
> 导航文件：当前入口 + 文档清单 + 版本/材料包 + 归档 + 缺失；不写阶段/门状态。
> 状态权威＝计划 §0（`__PLAN__`）；热快照＝`activeContext.md`。

## 1. 当前入口

| 项 | 路径 |
| --- | --- |
| 当前计划 | `__PLAN__` |
| 当前需求基线 | — |
| 当前方案/设计 | — |
| 当前任务清单 | — |
| 当前验证/发布 | — |
| 当前交接台账 | `__WORKROOT__/handoff/handoff-ledger.md` |

## 2. 文档清单

| 类别 | 文档 | 版本/日期 | 状态 | 说明 |
| --- | --- | --- | --- | --- |

## 3. 版本与材料包

| 版本 | 材料包 README | 状态 | 更新时间 |
| --- | --- | --- | --- |

## 4. 归档

| 批次 | 路径 | 内容 | 时间 |
| --- | --- | --- | --- |

## 5. 缺失与待补

- 无
'@

$overviewTpl = @'
# 项目文档总览

> 更新：__NOW__
> 只做入口与既有目录说明；不写阶段/门/状态。布局真值：`layout.yaml`。

## 工作区索引

| 包 | 工作区 | 索引 |
| --- | --- | --- |
| __OWNER__ | `__WORKROOT__/` | `__WORKROOT__/INDEX.md` |

## 权威文档库

- `docs/materials/INDEX.md`

## 外部原件

- `inbound/INDEX.md`

## 既有项目目录（未迁移）

| 目录 | 内容 | 处置 |
| --- | --- | --- |
| — | — | — |
'@

$wsIndex = $wsIndexTpl.Replace('__OWNER__', $Owner).Replace('__NOW__', $now).Replace('__WORKROOT__', $workrootRel).Replace('__PLAN__', "$workrootRel/$planFile")
if ($Mode -eq 'single') {
    New-FileIfMissing (Join-Path $docs 'INDEX.md') $wsIndex
} else {
    New-FileIfMissing (Join-Path $workroot 'INDEX.md') $wsIndex
    New-FileIfMissing (Join-Path $docs 'INDEX.md') ($overviewTpl.Replace('__OWNER__', $Owner).Replace('__NOW__', $now).Replace('__WORKROOT__', $workrootRel))
}

New-FileIfMissing (Join-Path $materials 'INDEX.md') @'
# Materials Index

> 项目级权威文档库总目录；只收定稿、完整、可发送内容。
> 每个版本目录自包含；旧版本保留，状态标 current / superseded。

current_version:
current_readme:
last_published_at:

| 版本 | 域 | 文档 | 来源 | 状态 | 更新时间 |
| --- | --- | --- | --- | --- | --- |
'@

New-FileIfMissing (Join-Path $inbound 'INDEX.md') @'
# Inbound Index

> 全项目外部输入唯一全量登记；不登记工作文档。
> 状态：current / reference / pending / superseded；失效只改状态，不归档。

| ID | 文件 | 类型 | 主题/版本 | 来源 | 关联 | 状态 | 覆盖/替代 | 登记时间 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
'@

New-FileIfMissing (Join-Path $workroot 'handoff/handoff-ledger.md') @'
# 交接台账

| 日期 | 方向 | category | 对象 | 版本/包 | 状态 | 回执 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
'@

New-FileIfMissing (Join-Path $workroot 'work-log.md') @'
# 工作日志

> 岗位里程碑侧记；只追加事件，不写产品发版史。
'@

if ($created.Count -eq 0) {
    Write-Output "文档骨架已存在，无需创建：$ProjectRoot"
} else {
    $verb = if ($DryRun) { '将创建' } else { '已创建' }
    Write-Output "$verb $($created.Count) 项："
    foreach ($c in $created) { Write-Output ("  - " + $c) }
}
Write-Output "布局：mode=$Mode owner=$Owner workroot=$workrootRel index=$(if ($Mode -eq 'single') { 'docs/INDEX.md' } else { "$workrootRel/INDEX.md + docs/INDEX.md" })"
