#Requires -Version 5.1
<#
.SYNOPSIS
    初始化项目工作文档根（只建目录/索引，不移动、不删除任何文件）。
.DESCRIPTION
    在项目根创建标准文档树：开发计划.md / 文档索引.md / 资料（{版本或主题}/ + _通用/ + 资料/_归档/ + 资料索引） /
    00-项目治理（含缺陷评估/） / 01-需求基线 / 02-方案设计 / 03-技术设计 / 04-计划与任务 / 05-测试与验收 / 06-发布与交付 / 07-运维与协作 / 08-复盘与改进 / _归档。
    已有目录/索引跳过；不覆盖用户内容。搬迁/归档由 AI 按 规则/工作流.md §5 与 规则/文档治理.md 另行确认后执行。
    默认开发/；-DocsRoot 仅兼容旧仓（如 docs/），不是第三套日常路径概念。
.PARAMETER ProjectRoot
    项目根目录；默认当前目录。
.PARAMETER DocsRoot
    工作文档根；默认开发/。参数保留供旧仓迁移（如 docs/），映射记档案 §9；非第三套概念。
.PARAMETER DryRun
    只输出将创建的目录/索引，不落盘。
.EXAMPLE
    powershell -NoProfile -ExecutionPolicy Bypass -File "规则/tools/Initialize-Docs.ps1" -ProjectRoot "C:\proj"
#>
[CmdletBinding()]
param(
    [string]$ProjectRoot = (Get-Location).Path,
    [string]$DocsRoot = '开发',
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

$ProjectRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
$docs = Join-Path $ProjectRoot $DocsRoot
$dirs = @(
    '00-项目治理',
    '00-项目治理/缺陷评估',
    '01-需求基线',
    '02-方案设计',
    '03-技术设计',
    '04-计划与任务',
    '05-测试与验收',
    '06-发布与交付',
    '07-运维与协作',
    '08-复盘与改进',
    '资料',
    '_归档'
)

$created = @()
foreach ($d in $dirs) {
    $p = Join-Path $docs $d
    if (Test-Path -LiteralPath $p -PathType Container) { continue }
    if ($DryRun) { $created += $p; continue }
    New-Item -ItemType Directory -Path $p -Force | Out-Null
    $created += $p
}

$index = Join-Path $docs '文档索引.md'
if (-not (Test-Path -LiteralPath $index)) {
    $content = @"
# 文档索引 — $(Split-Path -Leaf $ProjectRoot)

> 更新：$(Get-Date -Format 'yyyy-MM-dd HH:mm') ｜ 工作文档根：``$DocsRoot/``（旧项目可登记为 docs/ 等） ｜ 维护：AI 自动更新
> 分类：开发计划 / 根 CHANGELOG / 资料（{版本或主题}/ + _通用/ + 资料/_归档/ + 资料索引） / 00-项目治理（含缺陷评估） / 01-需求基线 / 02-方案设计 / 03-技术设计 / 04-计划与任务 / 05-测试与验收 / 06-发布与交付 / 07-运维与协作 / 08-复盘与改进 / 交接 / _归档

## 1. 现行实施入口

| 项 | 值 |
| --- | --- |
| 当前版本/迭代 | {…} |
| 当前开发计划 | {path} |
| 当前版本记录 | ``CHANGELOG.md``（项目根） |
| 当前方案 | {path} |
| 当前任务清单 | {path} |
| 技术设计入口 | ``03-技术设计/`` |
| 运维与协作入口 | ``07-运维与协作/`` |
| 当前需求基线 | {path} |
| 当前缺陷评估 | {path；无则「无」} |
| 当前提测单 / 发布说明 / UAT | {path} |
| 治理：台账 / CR / OPEN / DEC | {path} |

## 2. 文档清单

| 类别 | 文档 | 版本/日期 | 状态 | 说明 |
| --- | --- | --- | --- | --- |
| 01-需求基线 | {path} | {…} | {现行/已归档} | {…} |
| 02-方案设计 | {path} | {…} | {…} | 方案/前端设计说明 |
| 03-技术设计 | {path} | {…} | 现行 | API/架构 SSOT、ADR |
| 00-项目治理/缺陷评估 | {path} | {…} | {…} | 产品缺陷评估单（非技术方案） |
| 04-计划与任务 | {path} | {…} | {…} | {…} |
| 05-测试与验收 | {path} | {…} | {…} | {…} |
| 06-发布与交付 | {path} | {…} | {…} | 提测/发布 |
| 07-运维与协作 | {path} | {…} | 现行 | 常青操作说明 |
| 08-复盘与改进 | {path} | {…} | {…} | {…} |

## 3. 已归档

| 归档批次 | 内容 | 位置 | 日期 |
| --- | --- | --- | --- |
| {版本/日期} | {…} | ``_归档/{…}/`` 或同类 ``归档/`` | {…} |

## 4. 缺失与待补

- {应有但缺失的文档；负责人/截止；无则「无」}
"@
    if ($DryRun) {
        $created += $index
    }
    else {
        [System.IO.File]::WriteAllText($index, $content, (New-Object System.Text.UTF8Encoding $false))
        $created += $index
    }
}

$materialsIndex = Join-Path $docs '资料/资料索引.md'
if (-not (Test-Path -LiteralPath $materialsIndex)) {
    $materialsContent = @"
# 资料索引 — $(Split-Path -Leaf $ProjectRoot)

> 更新：$(Get-Date -Format 'yyyy-MM-dd HH:mm') ｜ 维护：AI 自动更新
> 只登记输入资料；工作文档不要登记在本表。分类/覆盖对照/归档见 规则/文档治理.md。
> 状态：现行 / 参考 / 待确认 / 失效 / 已归档 ｜ 覆盖关系：全量替代 / 全量覆盖 / 部分覆盖 / 增量补充 / 仅新增 / 重复 / 冲突

| ID | 文件 | 类型 | 主题/范围 | 版本/日期 | 来源 | 关联 | 状态 | 覆盖关系/失效依据 | 替代/归档 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DOC-001 | {path} | {PRD/迭代/专项/原型/…} | {…} | {…} | {…} | {…} | 现行 | — | — |
"@
    if ($DryRun) {
        $created += $materialsIndex
    }
    else {
        [System.IO.File]::WriteAllText($materialsIndex, $materialsContent, (New-Object System.Text.UTF8Encoding $false))
        $created += $materialsIndex
    }
}

if ($created.Count -eq 0) {
    Write-Output "文档树已存在，无需创建：$docs"
}
else {
    $verb = if ($DryRun) { '将创建' } else { '已创建' }
    Write-Output "$verb $($created.Count) 项："
    foreach ($c in $created) { Write-Output ("  - " + $c) }
}
Write-Output "文档根：$docs"
Write-Output "提示：搬迁/归档按 规则/文档治理.md 与 规则/工作流.md §5，先确认再执行；本脚本不删除、不覆盖。"
