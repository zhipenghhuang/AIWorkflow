#Requires -Version 5.1
<#
.SYNOPSIS
    初始化项目文档事实源目录（只建目录/索引，不移动、不删除任何文件）。
.DESCRIPTION
    在项目根创建标准文档树：开发计划.md / 文档索引.md / 资料（扁平：PRD/需求/迭代/专项/原型/设计/接口/技术/测试/验收/反馈/调研/竞品/会议/数据/原始/其他 + 资料索引） /
    00-项目治理 / 01-需求基线 / 02-设计基线（含缺陷评估/） / 03-计划与状态 / 04-测试与验收 / 05-发布与交付 / 06-复盘与改进 / _归档。
    已有目录/索引跳过；不覆盖用户内容。搬迁/归档由 AI 按 规则/工作流.md §5 另行确认后执行。
.PARAMETER ProjectRoot
    项目根目录；默认当前目录。
.PARAMETER DocsRoot
    文档事实源目录；新项目默认 开发；旧项目可传 docs。若项目档案 §9 有映射，以档案为准。
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
    '01-需求基线',
    '02-设计基线',
    '02-设计基线/缺陷评估',
    '03-计划与状态',
    '04-测试与验收',
    '05-发布与交付',
    '06-复盘与改进',
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

> 更新：$(Get-Date -Format 'yyyy-MM-dd HH:mm') ｜ 文档事实源目录：``$DocsRoot`` ｜ 维护：AI 自动更新
> 分类：开发计划 / 根 CHANGELOG / 资料（扁平：PRD/需求/迭代/专项/原型/设计/接口/技术/测试/验收/反馈/调研/竞品/会议/数据/原始/其他 + 资料索引） / 00-项目治理 / 01-需求基线 / 02-设计基线（含缺陷评估） / 03-计划与状态 / 04-测试与验收 / 05-发布与交付 / 06-复盘与改进 / _归档

## 1. 当前版本

| 项 | 值 |
| --- | --- |
| 当前版本/迭代 | {…} |
| 当前开发计划 | {path} |
| 当前版本记录 | ``CHANGELOG.md``（项目根；长期版本/迭代/迁移） |
| 当前需求台账 | {path} |
| 变更记录 CR | {path} |
| 待决项 OPEN | {path} |
| 决策记录 DEC | {path} |
| 当前需求基线 | {path} |
| 当前方案 | {path} |
| 当前缺陷评估 | {path；无则「无」} |
| 当前任务清单 | {path} |
| 当前提测单 | {path} |
| 当前测试计划/报告 | {path} |
| 当前发布说明 | {path} |
| 当前 UAT/验收 | {path} |

## 2. 文档清单

| 类别 | 文档 | 版本/日期 | 类型 | 最近复核 | 状态 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| 01-需求基线 | {path} | {…} | {常青/版本/过程} | {yyyy-MM-dd} | {现行/已归档} | {…} |
| 02-设计基线/缺陷评估 | {path} | {…} | {…} | {…} | {…} | 产品缺陷评估单（非技术方案） |

> 类型=常青 的文档按 `规则/文档治理.md` §4.1 复核；超期在状态列标「待复核」，不自动归档。

## 3. 归档

| 归档批次 | 内容 | 位置 | 日期 |
| --- | --- | --- | --- |
| {版本/日期} | {…} | ``_归档/{…}/`` | {…} |

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
> 只登记输入资料；工作文档不要登记在本表。分类/覆盖对照/归档见 规则/资料治理.md。
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
Write-Output "提示：搬迁/归档按 规则/资料治理.md 与 规则/工作流.md §5，先确认再执行；本脚本不删除、不覆盖。"
