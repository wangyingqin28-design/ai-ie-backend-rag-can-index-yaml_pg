<#
.SYNOPSIS
Publishes a clean SQL_RAG recovery baseline after a successful full-stack launch.
#>

[CmdletBinding()]
param(
    [string]$RepoRoot = 'D:\wkt\ai-ie-backend-feature-rag-new (1)\ai-ie-backend',
    [string]$SqlRag = 'D:\wkt\ai-ie-backend-feature-rag-new (1)\ai-ie-backend\app\SQL_RAG',
    [string]$BackupRoot = 'D:\wkt\ai-ie-backend-feature-rag-new (1)\ai-ie-backend\runtime_backups',
    [ValidateRange(1, 1000)]
    [int]$RetentionCount = 2,
    [switch]$FullStackReady,
    [string[]]$HealthGates,
    [switch]$Quiet
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

function Test-PathInside {
    param([string]$Path, [string]$Parent)
    $fullPath = [System.IO.Path]::GetFullPath($Path).TrimEnd('\')
    $fullParent = [System.IO.Path]::GetFullPath($Parent).TrimEnd('\')
    $fullPath.Equals($fullParent, [System.StringComparison]::OrdinalIgnoreCase) -or
        $fullPath.StartsWith($fullParent + '\', [System.StringComparison]::OrdinalIgnoreCase)
}

$NormalizedHealthGates = @(
    $HealthGates |
        ForEach-Object { $_ -split ',' } |
        ForEach-Object { $_.Trim() } |
        Where-Object { $_ }
)
if (!$FullStackReady -or $NormalizedHealthGates.Count -eq 0) {
    throw 'Refusing recovery baseline: full-stack ready proof is required.'
}

if (!(Test-Path -LiteralPath $RepoRoot -PathType Container)) {
    throw "Repository root does not exist: $RepoRoot"
}
if (!(Test-Path -LiteralPath $SqlRag -PathType Container)) {
    throw "SQL_RAG directory does not exist: $SqlRag"
}
$ResolvedRepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path.TrimEnd('\')
$ResolvedSqlRag = (Resolve-Path -LiteralPath $SqlRag).Path.TrimEnd('\')
if (!(Test-PathInside -Path $ResolvedSqlRag -Parent $ResolvedRepoRoot)) {
    throw "SQL_RAG is outside the repository root: $ResolvedSqlRag"
}

$ToolsDir = Split-Path -Parent $PSCommandPath
$IntegrityScript = Join-Path $ToolsDir 'test_onedlp_runtime_integrity.ps1'
if (!(Test-Path -LiteralPath $IntegrityScript -PathType Leaf)) {
    throw "Missing ONEDLP integrity script: $IntegrityScript"
}
$integrityJson = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $IntegrityScript `
    -RepoRoot $ResolvedRepoRoot -SqlRag $ResolvedSqlRag
if ($LASTEXITCODE -ne 0) {
    throw "ONEDLP integrity command failed with exit code $LASTEXITCODE"
}
$Integrity = $integrityJson | ConvertFrom-Json
if (!$Integrity.ready) {
    throw ('Refusing polluted recovery baseline: ' + ($Integrity | ConvertTo-Json -Depth 8 -Compress))
}

New-Item -ItemType Directory -Force -Path $BackupRoot | Out-Null
$ResolvedBackupRoot = (Resolve-Path -LiteralPath $BackupRoot).Path.TrimEnd('\')
if (!(Test-PathInside -Path $ResolvedBackupRoot -Parent $ResolvedRepoRoot)) {
    throw "Backup root is outside the repository root: $ResolvedBackupRoot"
}

function Invoke-SafeRobocopy {
    param(
        [string]$Source,
        [string]$Destination,
        [string[]]$ExcludeDirectoryNames = @(),
        [string[]]$ExcludeDirectoryPaths = @(),
        [string[]]$ExcludeFiles = @('*.pyc', '*.pyo')
    )
    if (!(Test-Path -LiteralPath $Source -PathType Container)) {
        throw "Backup source directory does not exist: $Source"
    }
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    $arguments = @($Source, $Destination, '/MIR', '/R:1', '/W:1')
    # [2026-09-01 12:38:08] 作用：声明 Robocopy 失败日志的持久诊断目录；理由依据：原实现丢弃全部原生输出，退出码 9 时无法确定具体失败文件。
    $robocopyLogRoot = Join-Path $ResolvedBackupRoot 'diagnostics'
    # [2026-09-01 12:38:08] 作用：创建恢复基线备份诊断目录；理由依据：失败日志必须位于已校验的备份根目录中且不能被部分基线清理。
    New-Item -ItemType Directory -Force -Path $robocopyLogRoot | Out-Null
    # [2026-09-01 12:38:08] 作用：为当前复制阶段生成唯一的 Unicode 日志路径；理由依据：根环境、SQL_RAG 源码和 Knowledge 环境三次复制不得互相覆盖证据。
    $robocopyLogPath = Join-Path $robocopyLogRoot ("robocopy-{0}-{1}.log" -f ((Split-Path -Leaf $Source) -replace '[^A-Za-z0-9_.-]', '_'), [guid]::NewGuid().ToString('N'))
    # [2026-09-01 12:38:08] 作用：要求 Robocopy 将完整原生诊断写入独立日志；理由依据：必须保留具体错误码、源路径和重试结果才能精确定位部署收尾故障。
    $arguments += "/UNILOG:$robocopyLogPath"
    $excludedDirectories = @($ExcludeDirectoryNames) + @($ExcludeDirectoryPaths)
    if ($excludedDirectories.Count -gt 0) {
        $arguments += '/XD'
        $arguments += $excludedDirectories
    }
    if (@($ExcludeFiles).Count -gt 0) {
        $arguments += '/XF'
        $arguments += @($ExcludeFiles)
    }
    & robocopy.exe @arguments *> $null
    $code = $LASTEXITCODE
    # [2026-09-01 12:38:08] 作用：在 Robocopy 报告真实复制失败时保留日志并终止基线发布；理由依据：退出码大于 7 表示至少一个文件未复制，不能发布不完整恢复源。
    if ($code -gt 7) {
        # [2026-09-01 12:38:08] 作用：在异常中返回可直接读取的 Robocopy 日志路径；理由依据：运维人员应看到真实失败文件而不是只得到模糊退出码。
        throw "Robocopy failed: source=$Source destination=$Destination exit=$code log=$robocopyLogPath"
    }
    # [2026-09-01 12:38:08] 作用：复制成功后删除当次临时 Robocopy 日志；理由依据：成功基线已由元数据和完整性报告记录，避免每次启动累积无故障日志。
    Remove-Item -LiteralPath $robocopyLogPath -Force -ErrorAction SilentlyContinue
}

function Move-DirectoryWithRetry {
    param(
        [string]$Source,
        [string]$Destination,
        [int]$MaximumAttempts = 40,
        [int]$DelayMilliseconds = 500
    )

    for ($attempt = 1; $attempt -le $MaximumAttempts; $attempt++) {
        try {
            Move-Item -LiteralPath $Source -Destination $Destination -ErrorAction Stop
            return
        }
        catch {
            if ($attempt -eq $MaximumAttempts) {
                throw "Failed to publish runtime backup after $MaximumAttempts attempts: source=$Source destination=$Destination error=$($_.Exception.Message)"
            }
            if (!$Quiet) {
                Write-Warning "Runtime backup publish is temporarily blocked; retrying ($attempt/$MaximumAttempts): $($_.Exception.Message)"
            }
            Start-Sleep -Milliseconds $DelayMilliseconds
        }
    }
}

function Test-SuccessfulRuntimeBaseline {
    param([System.IO.DirectoryInfo]$Directory)

    if (($Directory.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
        Write-Warning "Skipping runtime backup reparse point: $($Directory.FullName)"
        return $false
    }
    if ($Directory.Name -notmatch '^sql_rag_runtime_\d{14,17}$') {
        return $false
    }
    $metaPath = Join-Path $Directory.FullName 'BACKUP_META.json'
    try {
        if (!(Test-Path -LiteralPath $metaPath -PathType Leaf)) {
            Write-Warning "Preserving runtime backup with missing metadata: $($Directory.FullName)"
            return $false
        }
        $meta = Get-Content -LiteralPath $metaPath -Raw -Encoding UTF8 | ConvertFrom-Json
        $valid = $meta.baselineKind -eq 'full_stack_ready' -and
            [bool]$meta.fullStackReady -and
            $null -ne $meta.integrity -and
            [bool]$meta.integrity.ready
        if (!$valid) {
            Write-Warning "Preserving runtime backup with invalid success metadata: $($Directory.FullName)"
        }
        return $valid
    }
    catch {
        Write-Warning "Preserving runtime backup with unreadable metadata: path=$($Directory.FullName) error=$($_.Exception.Message)"
        return $false
    }
}

function Invoke-RuntimeBackupRetention {
    param(
        [string]$BackupRoot,
        [string]$LatestFile,
        [int]$KeepCount
    )

    $resolvedRoot = (Resolve-Path -LiteralPath $BackupRoot).Path.TrimEnd('\')
    $latestTarget = (Get-Content -LiteralPath $LatestFile -Raw -Encoding UTF8).Trim()
    $resolvedLatest = (Resolve-Path -LiteralPath $latestTarget).Path.TrimEnd('\')
    if (!(Test-PathInside -Path $resolvedLatest -Parent $resolvedRoot) -or
        $resolvedLatest.Equals($resolvedRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "LATEST runtime backup is outside the backup root: $resolvedLatest"
    }

    $successful = @(
        Get-ChildItem -LiteralPath $resolvedRoot -Directory -Force |
            Where-Object { $_.Name -match '^sql_rag_runtime_\d{14,17}$' } |
            Sort-Object Name -Descending |
            Where-Object { Test-SuccessfulRuntimeBaseline -Directory $_ }
    )

    foreach ($directory in @($successful | Select-Object -Skip $KeepCount)) {
        try {
            if (($directory.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
                throw "Refusing to prune a reparse point: $($directory.FullName)"
            }
            $resolvedCandidate = (Resolve-Path -LiteralPath $directory.FullName).Path.TrimEnd('\')
            if (!(Test-PathInside -Path $resolvedCandidate -Parent $resolvedRoot) -or
                $resolvedCandidate.Equals($resolvedRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
                throw "Refusing to prune outside the backup root: $resolvedCandidate"
            }
            if ((Split-Path -Leaf $resolvedCandidate) -notmatch '^sql_rag_runtime_\d{14,17}$') {
                throw "Refusing to prune an unexpected directory name: $resolvedCandidate"
            }
            $refreshed = Get-Item -LiteralPath $resolvedCandidate -Force
            if (!(Test-SuccessfulRuntimeBaseline -Directory $refreshed)) {
                throw "Runtime backup no longer has valid success metadata: $resolvedCandidate"
            }
            if ($resolvedCandidate.Equals($resolvedLatest, [System.StringComparison]::OrdinalIgnoreCase)) {
                throw "Refusing to prune LATEST runtime backup: $resolvedCandidate"
            }
            Remove-Item -LiteralPath $resolvedCandidate -Recurse -Force -ErrorAction Stop
        }
        catch {
            Write-Warning "Could not prune old runtime backup: path=$($directory.FullName) error=$($_.Exception.Message)"
        }
    }
}

$Stamp = (Get-Date).ToString('yyyyMMddHHmmssfff')
$BackupDir = Join-Path $ResolvedBackupRoot "sql_rag_runtime_$Stamp"
$PartialDir = "$BackupDir.partial"
if (!(Test-PathInside -Path $PartialDir -Parent $ResolvedBackupRoot)) {
    throw "Partial backup path is outside the backup root: $PartialDir"
}

try {
    New-Item -ItemType Directory -Force -Path $PartialDir | Out-Null
    $environmentExclusions = @('__pycache__', '.pytest_cache', '.mypy_cache', '.cache', '.git')
    Invoke-SafeRobocopy -Source (Join-Path $ResolvedRepoRoot '.venv') `
        -Destination (Join-Path $PartialDir '.venv') `
        -ExcludeDirectoryNames $environmentExclusions

    $programDirectoryExclusions = @(
        '__pycache__', '.pytest_cache', '.mypy_cache', '.cache', '.git', '.idea', '.venv', 'node_modules'
        # [2026-08-31 08:56:00] 作用：排除可移植种子导出失败后遗留的随机临时目录；理由依据：该目录可能被 ACL 隔离，robocopy 会以退出码 9 使已启动的一键流程在收尾阶段失败，而正式 portable_clone_seed 目录不匹配此通配名。
        'portable_clone_seed_*'
        # [2026-07-22 18:49:52] 作用：按目录名排除部署制品目录；理由：Windows PowerShell 调用 robocopy 时，含空格父路径下的绝对 /XD 路径在本机完整启动链中未生效，而 SQL_RAG 源码树中仅部署包使用该目录名，改为目录名排除可稳定阻止每份恢复基线重复约 4 GB 离线资产。
        'artifacts'
    )
    $programPathExclusions = @(
        # [2026-09-01 12:38:08] 作用：排除 SQL_RAG 的临时运行与部署诊断目录；理由依据：该目录不属于业务源码，且第二套 ACL 回归夹具中的受保护 seed 文件已实锤导致第一套收尾 Robocopy 退出 9。
        (Join-Path $ResolvedSqlRag '.runtime'),
        (Join-Path $ResolvedSqlRag '.stack-logs'),
        (Join-Path $ResolvedSqlRag 'logs'),
        (Join-Path $ResolvedSqlRag 'runtime_logs'),
        (Join-Path $ResolvedSqlRag 'runtime_data'),
        (Join-Path $ResolvedSqlRag 'runtime_backups'),
        (Join-Path $ResolvedSqlRag 'module_config\model_service\models'),
        (Join-Path $ResolvedSqlRag 'module_config\model_service\runtimes')
    )
    Invoke-SafeRobocopy -Source $ResolvedSqlRag `
        -Destination (Join-Path $PartialDir 'app\SQL_RAG') `
        -ExcludeDirectoryNames $programDirectoryExclusions `
        -ExcludeDirectoryPaths $programPathExclusions

    # [2026-07-23 09:06:32] 作用：在恢复基线原子发布前移除仍被 robocopy 带入的阿里云离线制品副本；理由：权威离线制品保留在项目 deployment 目录，恢复基线只保存业务源码与 Python 环境，避免每次启动重复增长约 4 GB。.
    $duplicatedDeploymentArtifacts = Join-Path $PartialDir 'app\SQL_RAG\deployment\alicloud_win11_migration\artifacts'
    if (Test-Path -LiteralPath $duplicatedDeploymentArtifacts) {
        if (!(Test-PathInside -Path $duplicatedDeploymentArtifacts -Parent $PartialDir)) {
            throw "Refusing to remove deployment artifacts outside partial backup: $duplicatedDeploymentArtifacts"
        }
        Remove-Item -LiteralPath $duplicatedDeploymentArtifacts -Recurse -Force -ErrorAction Stop
    }

    Invoke-SafeRobocopy -Source (Join-Path $ResolvedSqlRag 'Knowledge_management\.venv') `
        -Destination (Join-Path $PartialDir 'app\SQL_RAG\Knowledge_management\.venv') `
        -ExcludeDirectoryNames $environmentExclusions
    Copy-Item -LiteralPath (Join-Path $ResolvedRepoRoot 'pyproject.toml') `
        -Destination (Join-Path $PartialDir 'pyproject.toml') -Force -ErrorAction SilentlyContinue
    Copy-Item -LiteralPath (Join-Path $ResolvedRepoRoot 'requirements.txt') `
        -Destination (Join-Path $PartialDir 'requirements.txt') -Force -ErrorAction SilentlyContinue

    [pscustomobject]@{
        baselineKind = 'full_stack_ready'
        fullStackReady = $true
        healthGates = @($NormalizedHealthGates)
        createdAt = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
        repoRoot = $ResolvedRepoRoot
        sqlRag = $ResolvedSqlRag
        baselineScope = 'sql_rag_full_program_two_python_environments'
        retentionCount = $RetentionCount
        integrity = $Integrity
    } | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $PartialDir 'BACKUP_META.json') -Encoding UTF8

    Move-DirectoryWithRetry -Source $PartialDir -Destination $BackupDir

    $LatestFile = Join-Path $ResolvedBackupRoot 'LATEST_SQL_RAG_RUNTIME.txt'
    $LatestTemporary = "$LatestFile.tmp-$PID"
    $BackupDir | Set-Content -LiteralPath $LatestTemporary -Encoding UTF8
    if (Test-Path -LiteralPath $LatestFile -PathType Leaf) {
        $PreviousLatest = "$LatestFile.previous-$PID"
        [System.IO.File]::Replace($LatestTemporary, $LatestFile, $PreviousLatest, $true)
        Remove-Item -LiteralPath $PreviousLatest -Force -ErrorAction SilentlyContinue
    }
    else {
        Move-Item -LiteralPath $LatestTemporary -Destination $LatestFile
    }
}
catch {
    $publishFailure = $_
    if (Test-Path -LiteralPath $PartialDir) {
        try {
            Remove-Item -LiteralPath $PartialDir -Recurse -Force -ErrorAction Stop
        }
        catch {
            Write-Warning "Could not clean partial runtime backup after failure: path=$PartialDir error=$($_.Exception.Message)"
        }
    }
    throw $publishFailure
}

try {
    Invoke-RuntimeBackupRetention -BackupRoot $ResolvedBackupRoot -LatestFile $LatestFile -KeepCount $RetentionCount
}
catch {
    Write-Warning "Runtime backup retention could not run: root=$ResolvedBackupRoot error=$($_.Exception.Message)"
}

if (!$Quiet) {
    Write-Host "SQL_RAG successful full-stack baseline created: $BackupDir"
}
