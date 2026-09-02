# [2026-09-01 11:45:06] 作用：声明第二套知识启动与 NAS 边界修复的目标、只读和启动开关；理由依据：安装、验证和改变服务状态必须由同一版本化入口显式区分。
param([string]$SuiteRoot='D:\MonFangAI\GetDAM',[switch]$ValidateOnly,[switch]$StartServices)
# [2026-09-01 11:45:06] 作用：启用严格变量与属性检查；理由依据：缺失路径、清单或 profile 时必须在写目标前失败关闭。
Set-StrictMode -Version 2.0
# [2026-09-01 11:45:06] 作用：把非终止错误提升为终止错误；理由依据：哈希、备份、替换或验收任一步失败都不能输出成功。
$ErrorActionPreference='Stop'
# [2026-09-01 11:45:06] 作用：拒绝同时请求只读验证和服务启动；理由依据：ValidateOnly 必须保证目标文件和运行状态均不变化。
if($ValidateOnly-and$StartServices){throw 'ValidateOnly 与 StartServices 不能同时指定。'}
# [2026-09-01 11:45:06] 作用：拒绝空白目标套件根；理由依据：禁止因路径缺失在当前目录生成伪目标。
if([string]::IsNullOrWhiteSpace([string]$SuiteRoot)){throw '第二套套件根目录为空。'}
# [2026-09-01 11:45:06] 作用：确认目标套件根实际存在；理由依据：修复只能应用到既有第二套安装目录。
if(-not(Test-Path -LiteralPath $SuiteRoot -PathType Container)){throw "第二套套件根目录不存在：$SuiteRoot"}
# [2026-09-01 11:45:06] 作用：解析目标套件绝对路径；理由依据：后续路径边界、备份和回滚必须使用同一规范根。
$resolvedSuiteRoot=(Resolve-Path -LiteralPath $SuiteRoot -ErrorAction Stop).Path.TrimEnd('\')
# [2026-09-01 17:23:10] 作用：定位第二套后端源码根；理由依据：14 项载荷只能写入本套 ai-ie-backend，不能触碰第一套工作区或其他项目。
$targetOwnerRoot=Join-Path $resolvedSuiteRoot 'ai-ie-backend-feature-rag-new (1)\ai-ie-backend'
# [2026-09-01 11:45:06] 作用：确认第二套后端源码根存在；理由依据：禁止安装器为错误目录补建一套空项目。
if(-not(Test-Path -LiteralPath $targetOwnerRoot -PathType Container)){throw "第二套后端根目录不存在：$targetOwnerRoot"}
# [2026-09-01 11:45:06] 作用：规范化允许写入的后端路径前缀；理由依据：每个清单目标都必须通过路径越界检查。
$targetOwnerPrefix=[IO.Path]::GetFullPath($targetOwnerRoot).TrimEnd('\')+'\'
# [2026-09-01 11:45:06] 作用：定位第二套 SQL_RAG 根；理由依据：固定入口、profile 和安装后验收均从目标实际路径读取。
$targetSqlRag=Join-Path $targetOwnerRoot 'app\SQL_RAG'
# [2026-09-01 11:45:06] 作用：定位包内载荷根；理由依据：所有待安装字节必须来自当前版本目录内的 payload。
$payloadRoot=Join-Path $PSScriptRoot 'payload'
# [2026-09-01 11:45:06] 作用：确认载荷根存在；理由依据：缺少实体时不得只凭清单继续。
if(-not(Test-Path -LiteralPath $payloadRoot -PathType Container)){throw "修复载荷目录不存在：$payloadRoot"}
# [2026-09-01 11:45:06] 作用：规范化载荷路径前缀；理由依据：阻断绝对路径或 .. 越出当前包。
$payloadPrefix=[IO.Path]::GetFullPath($payloadRoot).TrimEnd('\')+'\'
# [2026-09-01 17:23:10] 作用：定位逐文件 SHA256 清单；理由依据：目标只接收构建机验证过的精确 14 项字节。
$payloadManifestPath=Join-Path $PSScriptRoot 'payload.sha256.json'
# [2026-09-01 11:45:06] 作用：确认逐文件清单存在；理由依据：残缺共享复制不得进入任何目标检查或写入。
if(-not(Test-Path -LiteralPath $payloadManifestPath -PathType Leaf)){throw "修复载荷清单不存在：$payloadManifestPath"}
# [2026-09-01 11:45:06] 作用：定位安装器自身哈希边车；理由依据：从 UNC 执行前先排除脚本传输截断或被替换。
$selfHashPath=$PSCommandPath+'.sha256'
# [2026-09-01 11:45:06] 作用：确认安装器自身边车存在；理由依据：没有版本哈希约束的脚本不得操作目标。
if(-not(Test-Path -LiteralPath $selfHashPath -PathType Leaf)){throw "安装器 SHA256 边车不存在：$selfHashPath"}
# [2026-09-01 11:45:06] 作用：读取安装器期望哈希；理由依据：边车使用标准 SHA256 首字段格式。
$expectedSelfHash=((Get-Content -LiteralPath $selfHashPath -Raw -Encoding ASCII).Trim()-split'\s+')[0].ToUpperInvariant()
# [2026-09-01 11:45:06] 作用：计算安装器当前实际哈希；理由依据：执行中的文件必须与发布边车逐字节一致。
$actualSelfHash=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToUpperInvariant()
# [2026-09-01 11:45:06] 作用：阻断安装器自身哈希漂移；理由依据：目标写入不能建立在未验真的控制程序上。
if($expectedSelfHash-notmatch'^[0-9A-F]{64}$'-or$actualSelfHash-ne$expectedSelfHash){throw "安装器 SHA256 校验失败：expected=$expectedSelfHash actual=$actualSelfHash"}
# [2026-09-01 17:23:10] 作用：声明唯一允许进入本包的 14 个相对路径；理由依据：新增项仅为第二套网络 profile，继续严格排除解析算法、数据库、队列、Worker、卷和业务数据。
$requiredRelativePaths=@('app\SQL_RAG\start-latest-full-stack.ps1','app\SQL_RAG\tools\backup_sql_rag_runtime.ps1','app\SQL_RAG\Knowledge_management\webui\src\nasJobService.mjs','app\SQL_RAG\Knowledge_management\backend\large-scale_commercialization_upgrade\until\Start-KnowledgeCommercialServices.ps1','app\SQL_RAG\deployment\windows_workstation\server-second-ports-profile.json','app\SQL_RAG\deployment\alicloud_win11_migration\artifacts\wheelhouse\knowledge-requirements.lock.txt','app\SQL_RAG\deployment\alicloud_win11_migration\artifacts\wheelhouse\wheelhouse-metadata.json','app\SQL_RAG\deployment\alicloud_win11_migration\artifacts\wheelhouse\SHA256SUMS.json','app\SQL_RAG\deployment\alicloud_win11_migration\artifacts\wheelhouse\knowledge\minio-7.2.16-py3-none-any.whl','app\SQL_RAG\deployment\alicloud_win11_migration\artifacts\wheelhouse\knowledge\argon2_cffi-25.1.0-py3-none-any.whl','app\SQL_RAG\deployment\alicloud_win11_migration\artifacts\wheelhouse\knowledge\argon2_cffi_bindings-25.1.0-cp39-abi3-win_amd64.whl','app\SQL_RAG\deployment\alicloud_win11_migration\artifacts\wheelhouse\knowledge\cffi-2.1.0-cp313-cp313-win_amd64.whl','app\SQL_RAG\deployment\alicloud_win11_migration\artifacts\wheelhouse\knowledge\pycparser-3.0-py3-none-any.whl','app\SQL_RAG\deployment\alicloud_win11_migration\artifacts\wheelhouse\knowledge\pycryptodome-3.23.0-cp37-abi3-win_amd64.whl')
# [2026-09-01 11:55:06] 作用：读取包内逐文件清单原始数组；理由依据：Windows PowerShell 5.1 会把顶层 JSON 数组作为单个对象返回，必须与后续枚举显式分开。
$manifestData=Get-Content -LiteralPath $payloadManifestPath -Raw -Encoding UTF8|ConvertFrom-Json
# [2026-09-01 17:23:10] 作用：经管道显式展开清单数组为逐项集合；理由依据：目标 PS5.1 必须稳定得到 14 条记录而不是计为一个数组对象。
$manifestEntries=@($manifestData|ForEach-Object{$_})
# [2026-09-01 17:23:10] 作用：阻断载荷数量扩大或缩小；理由依据：本次修复边界固定为 14 项且禁止隐含业务代码。
if($manifestEntries.Count-ne$requiredRelativePaths.Count){throw "修复载荷数量错误：expected=$($requiredRelativePaths.Count) actual=$($manifestEntries.Count)"}
# [2026-09-01 11:45:06] 作用：声明通过哈希和路径门禁的载荷集合；理由依据：写入阶段只能消费已经验证的结构化记录。
$validated=New-Object System.Collections.Generic.List[object]
# [2026-09-01 17:23:10] 作用：逐项验证包内 14 个实体；理由依据：任一共享传输损坏必须在目标备份前停止。
foreach($entry in $manifestEntries){
  # [2026-09-01 11:45:06] 作用：读取并规范清单相对路径；理由依据：空路径、绝对路径和父目录跳转均不可接受。
  $relativePath=([string]$entry.relative_path).Trim()
  # [2026-09-01 11:45:06] 作用：阻断清单路径越界形式；理由依据：载荷只能相对于后端根安装。
  if([string]::IsNullOrWhiteSpace($relativePath)-or[IO.Path]::IsPathRooted($relativePath)-or$relativePath-split'[\\/]' -contains '..'){throw "修复载荷路径非法：$relativePath"}
  # [2026-09-01 11:45:06] 作用：阻断清单出现未授权路径；理由依据：不能借本修复夹带解析、数据库或其他业务源码。
  if($requiredRelativePaths-notcontains$relativePath){throw "修复载荷包含越界文件：$relativePath"}
  # [2026-09-01 11:45:06] 作用：解析包内实体绝对路径；理由依据：路径前缀检查必须基于规范化结果。
  $sourcePath=[IO.Path]::GetFullPath((Join-Path $payloadRoot $relativePath))
  # [2026-09-01 11:45:06] 作用：阻断实体越出 payload 根；理由依据：清单文本不能读取包外任意文件。
  if(-not$sourcePath.StartsWith($payloadPrefix,[StringComparison]::OrdinalIgnoreCase)){throw "修复载荷越出包根：$relativePath"}
  # [2026-09-01 11:45:06] 作用：确认载荷实体存在；理由依据：清单记录不能替代真实文件。
  if(-not(Test-Path -LiteralPath $sourcePath -PathType Leaf)){throw "修复载荷文件不存在：$relativePath"}
  # [2026-09-01 11:45:06] 作用：读取清单期望 SHA256；理由依据：统一按大写十六进制比较。
  $expectedHash=([string]$entry.sha256).ToUpperInvariant()
  # [2026-09-01 11:45:06] 作用：计算载荷实体实际 SHA256；理由依据：文件名和长度都不能替代内容身份。
  $actualHash=(Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToUpperInvariant()
  # [2026-09-01 11:45:06] 作用：读取载荷实体实际长度；理由依据：同时阻断截断和错误替换。
  $actualBytes=(Get-Item -LiteralPath $sourcePath).Length
  # [2026-09-01 11:45:06] 作用：阻断长度或哈希不一致；理由依据：共享目录复制成功不等于字节正确。
  if($expectedHash-notmatch'^[0-9A-F]{64}$'-or$actualHash-ne$expectedHash-or$actualBytes-ne[int64]$entry.bytes){throw "修复载荷验真失败：$relativePath"}
  # [2026-09-01 11:45:06] 作用：解析目标绝对路径；理由依据：安装与回滚必须绑定同一目标。
  $targetPath=[IO.Path]::GetFullPath((Join-Path $targetOwnerRoot $relativePath))
  # [2026-09-01 11:45:06] 作用：阻断目标越出第二套后端根；理由依据：禁止触碰套件外、第一套或其他项目文件。
  if(-not$targetPath.StartsWith($targetOwnerPrefix,[StringComparison]::OrdinalIgnoreCase)){throw "修复目标越出第二套后端根：$relativePath"}
  # [2026-09-01 11:45:06] 作用：保存经过验证的安装记录；理由依据：写入阶段不再重新解释不可信清单字段。
  $validated.Add([pscustomobject]@{RelativePath=$relativePath;SourcePath=$sourcePath;TargetPath=$targetPath;Sha256=$actualHash;Bytes=[int64]$actualBytes})
}
# [2026-09-01 17:23:10] 作用：逐项确认 14 个固定路径全部出现且无重复；理由依据：数量相同仍可能用重复项掩盖缺失项。
foreach($requiredRelativePath in $requiredRelativePaths){if(@($validated|Where-Object{$_.RelativePath-eq$requiredRelativePath}).Count-ne1){throw "修复载荷固定文件缺失或重复：$requiredRelativePath"}}
# [2026-09-01 11:45:06] 作用：读取共享启动引擎载荷文本；理由依据：哈希之外还要证明 MinIO 门禁和第一套原入口合同同版存在。
$engineText=Get-Content -LiteralPath (Join-Path $payloadRoot 'app\SQL_RAG\start-latest-full-stack.ps1') -Raw -Encoding UTF8
# [2026-09-01 11:45:06] 作用：验证共享引擎只新增 MinIO 直接依赖门禁且保留固定入口身份；理由依据：缺一项都会让第二套在绑定 28320 前退出或让两套串线。
if(-not$engineText.Contains("'minio==7.2.16'")-or-not$engineText.Contains('import jsonpointer, sklearn, celery, minio')-or-not$engineText.Contains('SQL_RAG_LOCAL_ENTRY')-or-not$engineText.Contains("DeploymentProfile-eq'server_second_ports'")){throw '共享引擎缺少 MinIO 或两套固定入口隔离合同。'}
# [2026-09-01 13:58:12] 作用：定位包内运行时备份脚本；理由依据：文本、字节编码和 AST 门禁必须检查同一个已验真载荷实体。
$backupPayloadPath=Join-Path $payloadRoot 'app\SQL_RAG\tools\backup_sql_rag_runtime.ps1'
# [2026-09-01 13:58:12] 作用：读取备份脚本原始字节；理由依据：Windows PowerShell 5.1 会误解码无 BOM 中文注释并吞掉其后的排除代码，单纯 UTF-8 文本检查不能发现该故障。
$backupBytes=[IO.File]::ReadAllBytes($backupPayloadPath)
# [2026-09-01 13:58:12] 作用：阻断不带 UTF-8 BOM 的备份脚本；理由依据：必须保证目标 PS5.1 按正确字符集执行随机种子、制品和运行时目录排除项。
if($backupBytes.Length-lt3-or$backupBytes[0]-ne0xEF-or$backupBytes[1]-ne0xBB-or$backupBytes[2]-ne0xBF){throw '运行时备份脚本缺少 UTF-8 BOM，禁止交给 Windows PowerShell 5.1 执行。'}
# [2026-09-01 13:58:12] 作用：以显式 UTF-8 读取备份脚本载荷文本；理由依据：后续合同检查必须基于发布源码字符而不是当前控制台代码页。
$backupText=Get-Content -LiteralPath $backupPayloadPath -Raw -Encoding UTF8
# [2026-09-01 13:58:12] 作用：验证随机种子、SQL_RAG 运行时目录和 Robocopy 诊断均被闭合且正式种子仍保留；理由依据：修复第一套收尾 exit 9 不能牺牲正式恢复基线或再次丢失具体失败路径。
if(-not$backupText.Contains("'portable_clone_seed_*'")-or$backupText.Contains("'portable_clone_seed'")-or-not$backupText.Contains("(Join-Path `$ResolvedSqlRag '.runtime')")-or-not$backupText.Contains('/UNILOG:')-or-not$backupText.Contains(' log=$robocopyLogPath')){throw '运行时备份的临时目录排除、PS5.1 或原生诊断合同不成立。'}
# [2026-09-01 11:45:06] 作用：读取 NAS 前端载荷文本；理由依据：502 修复必须局限于浏览器单文件上传边界。
$nasText=Get-Content -LiteralPath (Join-Path $payloadRoot 'app\SQL_RAG\Knowledge_management\webui\src\nasJobService.mjs') -Raw -Encoding UTF8
# [2026-09-01 11:45:06] 作用：验证三路并发保持且仅 502/503/504 最多重试三次；理由依据：不能改 NAS 路径、后端解析或无限重传。
if(-not$nasText.Contains('const NAS_UPLOAD_CONCURRENCY = 3;')-or-not$nasText.Contains('const NAS_UPLOAD_MAX_ATTEMPTS = 3;')-or-not$nasText.Contains('new Set([502, 503, 504])')-or-not$nasText.Contains('requestNasUploadWithRetry')){throw 'NAS 有界重传合同不成立。'}
# [2026-09-01 11:45:06] 作用：读取商业启动器载荷文本；理由依据：第二套 PgBouncer 必须继续使用本 profile 私网数据库路由。
$commercialText=Get-Content -LiteralPath (Join-Path $payloadRoot 'app\SQL_RAG\Knowledge_management\backend\large-scale_commercialization_upgrade\until\Start-KnowledgeCommercialServices.ps1') -Raw -Encoding UTF8
# [2026-09-02 15:34:17] 作用：验证 PS5.1 结构化标签读取、网络数组展开、固定 IPAM、数据库错网双向清理和 PgBouncer 私网闭环；理由依据：1447 已走到 recreate=True，但原生 Go-template 标签键双引号被剥离并报 function com not defined。
if(-not$commercialText.Contains('$actualEndpointInspectText=((& docker.exe inspect $recreateEndpointName 2>$null)|Out-String)')-or-not$commercialText.Contains('$actualEndpointInspectDocument=($actualEndpointInspectText|ConvertFrom-Json)[0]')-or-not$commercialText.Contains('$actualEndpointLabels=$actualEndpointInspectDocument.Config.Labels')-or$commercialText.Contains('index .Config.Labels')-or-not$commercialText.Contains('$dockerNetworkDocuments=@(($dockerNetworkInspectText|ConvertFrom-Json)|ForEach-Object{$_})')-or-not$commercialText.Contains('$migratedPostgresReportsCommercialNetwork=($null-ne$migratedPostgresCurrentNetworks.PSObject.Properties[$commercialNetwork])')-or-not$commercialText.Contains('$migratedPostgresReportsCommercialNetwork-ne$commercialNetworkReportsMigratedPostgres')-or-not$commercialText.Contains('KNOWLEDGE_COMMERCIAL_MIGRATED_POSTGRES_ORPHAN_ENDPOINT_REPAIRED')-or-not$commercialText.Contains('docker network connect $migratedPostgresNetwork $pgbouncerContainer')-or-not$commercialText.Contains('KNOWLEDGE_COMMERCIAL_PGBOUNCER_PREFLIGHT_READY')-or-not$commercialText.Contains('KNOWLEDGE_COMMERCIAL_NETWORK_PREFLIGHT_READY')-or-not$commercialText.Contains('KNOWLEDGE_COMMERCIAL_NETWORK_RECREATED')-or-not$commercialText.Contains('$expectedCommercialContainerNames')-or-not$commercialText.Contains('docker.exe rm --force @commercialContainersToRemove')-or-not$commercialText.Contains('docker.exe network disconnect --force $commercialNetwork $migratedPostgresContainer')-or-not$commercialText.Contains('$remainingCommercialNetworkEndpoints.Count-gt0')-or$commercialText.Contains('@composeCommandArguments down')-or$commercialText.Contains('down -v')-or$commercialText.Contains('down --volumes')-or$commercialText.Contains('$pgbouncerUpstreamHost=if($knowledgeDatabaseUri.Host-in@(''127.0.0.1'',''localhost'')){''host.docker.internal''}else{$knowledgeDatabaseUri.Host}')){throw '商业结构化标签、固定网段、PS5.1 网络数组、迁移数据库 endpoint 或 PgBouncer 私网闭环合同不成立。'}
# [2026-09-01 17:23:10] 作用：读取包内第二套独立 profile；理由依据：网络修复必须由目标 profile 持有而不是污染第一套或写死临时命令。
$payloadServerProfile=Get-Content -LiteralPath (Join-Path $payloadRoot 'app\SQL_RAG\deployment\windows_workstation\server-second-ports-profile.json') -Raw -Encoding UTF8|ConvertFrom-Json
# [2026-09-01 17:23:10] 作用：验证包内第二套固定网段、网关和直连 Engine；理由依据：只有 10.253.233.0/24 与当前目标证据不重叠且运行时仍必须使用 docker_engine_linux。
if([string]$payloadServerProfile.profile_name-ne'server_second_ports'-or[string]$payloadServerProfile.docker.engine_endpoint-ne'npipe:////./pipe/docker_engine_linux'-or[string]$payloadServerProfile.docker.commercial_network.subnet-ne'10.253.233.0/24'-or[string]$payloadServerProfile.docker.commercial_network.gateway-ne'10.253.233.1'){throw '第二套固定商业网段或 Docker Engine profile 合同不成立。'}
# [2026-09-01 11:45:06] 作用：定位包内 Knowledge wheelhouse 根；理由依据：MinIO 直接依赖、锁文件、元数据和总清单必须作为一个原子版本验证。
$payloadWheelhouse=Join-Path $payloadRoot 'app\SQL_RAG\deployment\alicloud_win11_migration\artifacts\wheelhouse'
# [2026-09-01 11:45:06] 作用：读取 Knowledge 锁文件；理由依据：离线修复只能消费固定版本依赖闭包。
$knowledgeLockText=Get-Content -LiteralPath (Join-Path $payloadWheelhouse 'knowledge-requirements.lock.txt') -Raw -Encoding UTF8
# [2026-09-01 11:57:36] 作用：逐项验证 MinIO 九依赖锁定版本并使用锁文件实际的 typing_extensions 规范名；理由依据：第二套不得在启动时联网猜版本或把名称规范差异误报成缺包。
foreach($lockedRequirement in @('minio==7.2.16','argon2-cffi==25.1.0','argon2-cffi-bindings==25.1.0','cffi==2.1.0','pycparser==3.0','certifi==2026.6.17','pycryptodome==3.23.0','typing_extensions==4.16.0','urllib3==2.7.0')){if(-not$knowledgeLockText.Contains($lockedRequirement)){throw "Knowledge MinIO 锁文件缺少：$lockedRequirement"}}
# [2026-09-01 11:45:06] 作用：读取 wheelhouse 元数据；理由依据：依赖数量必须与更新后的 193 个 Knowledge 轮子一致。
$wheelhouseMetadata=Get-Content -LiteralPath (Join-Path $payloadWheelhouse 'wheelhouse-metadata.json') -Raw -Encoding UTF8|ConvertFrom-Json
# [2026-09-01 11:45:06] 作用：提取 Knowledge 元数据记录；理由依据：root 与 getsoft 数量不能替代知识环境事实。
$knowledgeMetadata=@($wheelhouseMetadata|Where-Object{$_.name-eq'knowledge'})[0]
# [2026-09-01 11:45:06] 作用：阻断 Knowledge 元数据不是 193/193；理由依据：旧 187 清单会让新轮子脱离发布合同。
if($null-eq$knowledgeMetadata-or[int]$knowledgeMetadata.wheel_count-ne193-or[int]$knowledgeMetadata.requirement_count-ne193){throw 'Knowledge wheelhouse 元数据不是 193/193。'}
# [2026-09-01 11:45:06] 作用：读取总 SHA256 清单；理由依据：窄包中的锁文件、元数据和六个新轮子必须属于同一份 671 项发布事实。
$wheelhouseShaManifest=Get-Content -LiteralPath (Join-Path $payloadWheelhouse 'SHA256SUMS.json') -Raw -Encoding UTF8|ConvertFrom-Json
# [2026-09-01 11:45:06] 作用：阻断总清单数量漂移；理由依据：本次已逐文件验证的完整 wheelhouse 固定为 671 项。
if(@($wheelhouseShaManifest.files).Count-ne671){throw "Wheelhouse SHA256 清单数量错误：$(@($wheelhouseShaManifest.files).Count)"}
# [2026-09-01 11:45:06] 作用：验证窄包内八个可被总清单约束的实体；理由依据：SHA256SUMS 自身除外，其余元数据和轮子必须逐项同哈希同长度。
foreach($wheelRelativePath in @('knowledge-requirements.lock.txt','wheelhouse-metadata.json','knowledge\minio-7.2.16-py3-none-any.whl','knowledge\argon2_cffi-25.1.0-py3-none-any.whl','knowledge\argon2_cffi_bindings-25.1.0-cp39-abi3-win_amd64.whl','knowledge\cffi-2.1.0-cp313-cp313-win_amd64.whl','knowledge\pycparser-3.0-py3-none-any.whl','knowledge\pycryptodome-3.23.0-cp37-abi3-win_amd64.whl')){
  # [2026-09-01 11:45:06] 作用：提取当前文件的总清单记录；理由依据：每项必须唯一出现。
  $wheelRecord=@($wheelhouseShaManifest.files|Where-Object{([string]$_.path).Replace('/','\')-eq$wheelRelativePath})
  # [2026-09-01 11:45:06] 作用：阻断总清单缺失或重复记录；理由依据：不能仅依赖外层 payload 哈希掩盖 wheelhouse 清单漂移。
  if($wheelRecord.Count-ne1){throw "Wheelhouse 总清单记录缺失或重复：$wheelRelativePath"}
  # [2026-09-01 11:45:06] 作用：定位当前窄包 wheelhouse 实体；理由依据：以包内实际字节完成双重验证。
  $wheelPath=Join-Path $payloadWheelhouse $wheelRelativePath
  # [2026-09-01 11:45:06] 作用：计算当前窄包实体 SHA256；理由依据：总清单必须与 payload 实际文件一致。
  $wheelHash=(Get-FileHash -LiteralPath $wheelPath -Algorithm SHA256).Hash.ToLowerInvariant()
  # [2026-09-01 11:45:06] 作用：读取当前窄包实体长度；理由依据：阻断同名截断文件。
  $wheelBytes=(Get-Item -LiteralPath $wheelPath).Length
  # [2026-09-01 11:45:06] 作用：阻断总清单哈希或长度漂移；理由依据：目标离线环境只能安装被 671 项清单确认的字节。
  if($wheelHash-ne[string]$wheelRecord[0].sha256-or$wheelBytes-ne[int64]$wheelRecord[0].bytes){throw "Wheelhouse 总清单验真失败：$wheelRelativePath"}
}
# [2026-09-01 11:45:06] 作用：以显式 UTF-8 文本解析包内三个 PowerShell 程序；理由依据：目标 Windows PowerShell 5.1 不能因无 BOM 中文注释制造伪语法错误。
foreach($scriptRelativePath in @('app\SQL_RAG\start-latest-full-stack.ps1','app\SQL_RAG\tools\backup_sql_rag_runtime.ps1','app\SQL_RAG\Knowledge_management\backend\large-scale_commercialization_upgrade\until\Start-KnowledgeCommercialServices.ps1')){
  # [2026-09-01 11:45:06] 作用：读取当前 PowerShell 载荷 UTF-8 文本；理由依据：解析结果必须与发布源码字符一致。
  $scriptText=Get-Content -LiteralPath (Join-Path $payloadRoot $scriptRelativePath) -Raw -Encoding UTF8
  # [2026-09-01 11:45:06] 作用：初始化语法令牌和错误集合；理由依据：严格模式下显式赋值避免残留状态。
  $tokens=$null;$errors=$null
  # [2026-09-01 11:45:06] 作用：执行 PowerShell AST 解析；理由依据：任何目标脚本语法错误必须在安装前阻断。
  [void][Management.Automation.Language.Parser]::ParseInput($scriptText,[ref]$tokens,[ref]$errors)
  # [2026-09-01 11:45:06] 作用：阻断载荷 PowerShell 语法错误；理由依据：不能把不可执行脚本写入两套共享逻辑。
  if($errors.Count-ne0){throw "修复载荷 PowerShell 语法错误：$scriptRelativePath；$($errors.Message-join'; ')"}
}
# [2026-09-01 11:45:06] 作用：定位目标第二套固定入口；理由依据：安装与启动只允许复用既有 server wrapper。
$targetLauncher=Join-Path $targetSqlRag 'start-server-full-stack.ps1'
# [2026-09-01 11:45:06] 作用：定位目标第二套独立 profile；理由依据：地址、容器、网络和 33 端口均以当前目标事实为准。
$targetProfilePath=Join-Path $targetSqlRag 'deployment\windows_workstation\server-second-ports-profile.json'
# [2026-09-01 11:45:06] 作用：确认第二套固定入口和 profile 同时存在；理由依据：窄包不得创建新部署分支或回落第一套。
foreach($targetContractPath in @($targetLauncher,$targetProfilePath)){if(-not(Test-Path -LiteralPath $targetContractPath -PathType Leaf)){throw "第二套目标合同文件不存在：$targetContractPath"}}
# [2026-09-01 11:45:06] 作用：读取目标固定入口文本；理由依据：写入前证明操作对象确为 .233 第二套。
$targetLauncherText=Get-Content -LiteralPath $targetLauncher -Raw -Encoding UTF8
# [2026-09-01 11:45:06] 作用：阻断固定入口身份或地址错误；理由依据：第一套 local wrapper 绝不能被本安装器调用或覆盖。
if(-not$targetLauncherText.Contains('server_second_ports')-or-not$targetLauncherText.Contains('172.18.1.233')){throw '目标固定入口不是 172.18.1.233 server_second_ports。'}
# [2026-09-01 11:45:06] 作用：读取目标第二套 profile；理由依据：端口和 Docker 身份验收必须来自目标当前配置。
$targetProfile=Get-Content -LiteralPath $targetProfilePath -Raw -Encoding UTF8|ConvertFrom-Json
# [2026-09-01 17:23:10] 作用：验证目标第二套 profile、IP、源码构建模式、容器前缀和直连 Engine；理由依据：安装器父子进程必须使用同一个独立 Docker 端点且禁止依赖第一套。
if([string]$targetProfile.profile_name-ne'server_second_ports'-or[string]$targetProfile.lan_ip-ne'172.18.1.233'-or[string]$targetProfile.commercial_runtime_mode-ne'source_build'-or[string]$targetProfile.docker.container_name_prefix-ne'sql-rag-server'-or[string]$targetProfile.docker.engine_endpoint-ne'npipe:////./pipe/docker_engine_linux'){throw '目标第二套 profile 身份、IP、运行模式、容器前缀或 Docker Engine 不符合合同。'}
# [2026-09-01 11:45:06] 作用：读取并去重目标第二套端口清单；理由依据：完整服务验收固定覆盖 33 个独立监听。
$expectedPorts=@($targetProfile.ports.PSObject.Properties|ForEach-Object{[int]$_.Value}|Sort-Object -Unique)
# [2026-09-01 11:45:06] 作用：阻断目标端口数量漂移；理由依据：旧 31 项或重复端口均不能继续安装。
if($expectedPorts.Count-ne33){throw "目标第二套端口合同不是 33 项：$($expectedPorts.Count)"}
# [2026-09-01 17:23:10] 作用：在只读模式返回包、目标、固定子网和边界验真结果；理由依据：目标管理员可先确认零写入 READY 与 10.253.233.0/24 合同再正式安装。
if($ValidateOnly){[pscustomobject]@{Result='READY';Update='knowledge_startup_nas_repair';Mode='validate_only';PayloadFiles=$validated.Count;Profile='server_second_ports';RuntimeMode='source_build';CommercialNetworkSubnet=[string]$payloadServerProfile.docker.commercial_network.subnet;PortContract=33;BusinessParsingFilesChanged=0;ServicesStarted=$false}|ConvertTo-Json -Depth 5;return}
# [2026-09-01 11:45:06] 作用：确认正式安装在管理员令牌下运行；理由依据：目标源码、备份目录和服务编排需要明确提升权限。
$isAdministrator=([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
# [2026-09-01 11:45:06] 作用：阻断非管理员正式安装；理由依据：只读验证可普通运行，写入与启动不可静默部分成功。
if(-not$isAdministrator){throw '请在 172.18.1.233 管理员 PowerShell 执行正式修复。'}
# [2026-09-01 17:23:10] 作用：生成本次精确回滚目录；理由依据：14 个目标旧文件必须在替换前保留原相对层级。
$backupRoot=Join-Path $resolvedSuiteRoot ('.runtime\deployment_backups\knowledge-startup-nas-repair_'+(Get-Date -Format 'yyyyMMdd-HHmmss'))
# [2026-09-01 11:45:06] 作用：创建回滚目录；理由依据：任何目标替换开始前先确保恢复位置可写。
[void](New-Item -ItemType Directory -Force -Path $backupRoot)
# [2026-09-01 11:45:06] 作用：声明已经成功替换的目标记录；理由依据：中途失败时按逆序自动恢复。
$installed=New-Object System.Collections.Generic.List[object]
# [2026-09-01 11:45:06] 作用：在事务边界内逐项备份并原子替换；理由依据：任一文件失败都必须回滚先前已替换项。
try{
  # [2026-09-01 11:45:06] 作用：遍历全部已验证载荷；理由依据：写入顺序完全由固定清单决定。
  foreach($item in $validated){
    # [2026-09-01 11:45:06] 作用：记录目标文件安装前是否存在；理由依据：回滚时区分恢复旧文件和删除本次新增轮子。
    $targetExisted=Test-Path -LiteralPath $item.TargetPath -PathType Leaf
    # [2026-09-01 11:45:06] 作用：定位当前目标的回滚副本路径；理由依据：保留原相对层级便于逐项审计。
    $backupPath=Join-Path $backupRoot $item.RelativePath
    # [2026-09-01 15:05:58] 作用：为既有目标创建回滚父目录；理由依据：Windows PowerShell 5.1 的 File.Replace 必须接收尚不存在的真实备份路径，并由原子替换自身生成旧字节副本。
    if($targetExisted){[void](New-Item -ItemType Directory -Force -Path (Split-Path -Parent $backupPath))}
    # [2026-09-01 11:45:06] 作用：确保目标父目录存在；理由依据：六个新轮子可能尚未落盘。
    [void](New-Item -ItemType Directory -Force -Path (Split-Path -Parent $item.TargetPath))
    # [2026-09-01 11:45:06] 作用：声明与目标同目录的临时文件；理由依据：最终替换必须在同一卷完成。
    $temporaryPath=$item.TargetPath+'.km-knowledge-repair-'+[guid]::NewGuid().ToString('N')+'.tmp'
    # [2026-09-01 11:45:06] 作用：把发布字节复制到目标同目录临时文件；理由依据：复制中断不能损坏当前正式目标。
    Copy-Item -LiteralPath $item.SourcePath -Destination $temporaryPath -Force
    # [2026-09-01 11:45:06] 作用：回读临时文件哈希；理由依据：只有目标卷字节正确才允许原子切换。
    $temporaryHash=(Get-FileHash -LiteralPath $temporaryPath -Algorithm SHA256).Hash.ToUpperInvariant()
    # [2026-09-01 11:45:06] 作用：阻断临时文件哈希漂移；理由依据：保留原目标并清理仅本次生成的临时文件。
    if($temporaryHash-ne$item.Sha256){Remove-Item -LiteralPath $temporaryPath -Force -ErrorAction SilentlyContinue;throw "目标临时文件 SHA256 不一致：$($item.RelativePath)"}
    # [2026-09-01 15:05:58] 作用：按目标是否存在选择原子替换或首次移动；理由依据：既有文件必须同时形成可恢复旧字节，新文件则不能调用只适用于既有目标的 Replace。
    if($targetExisted){
      # [2026-09-01 15:05:58] 作用：以真实回滚路径原子替换既有目标；理由依据：Windows PowerShell 5.1 对四参数 File.Replace 的空备份路径会稳定抛出“路径的形式不合法”。
      [IO.File]::Replace($temporaryPath,$item.TargetPath,$backupPath,$true)
    }else{
      # [2026-09-01 15:05:58] 作用：把同卷临时文件原子移动为首次安装目标；理由依据：六个新增轮子没有可被 Replace 的旧目标。
      [IO.File]::Move($temporaryPath,$item.TargetPath)
    }
    # [2026-09-01 11:45:06] 作用：保存已安装项及回滚事实；理由依据：后续失败时按逆序精确恢复。
    $installed.Add([pscustomobject]@{RelativePath=$item.RelativePath;TargetPath=$item.TargetPath;BackupPath=$backupPath;TargetExisted=$targetExisted;Sha256=$item.Sha256})
    # [2026-09-01 11:45:06] 作用：回读正式目标哈希；理由依据：原子调用成功仍不能替代最终字节证据。
    $installedHash=(Get-FileHash -LiteralPath $item.TargetPath -Algorithm SHA256).Hash.ToUpperInvariant()
    # [2026-09-01 11:45:06] 作用：阻断最终目标哈希不一致；理由依据：立即进入统一回滚分支而不继续下一项。
    if($installedHash-ne$item.Sha256){throw "正式目标 SHA256 不一致：$($item.RelativePath)"}
  }
}
# [2026-09-01 17:23:10] 作用：捕获 14 项事务中首个备份、复制、原子替换或回读错误；理由依据：正式失败必须进入统一逆序回滚并保留原始诊断。
catch{
  # [2026-09-01 11:45:06] 作用：保存触发事务失败的原始诊断；理由依据：回滚动作不能覆盖首个真实错误。
  $installError=$_.Exception.Message
  # [2026-09-01 11:50:11] 作用：从最后一项初始化显式倒序索引；理由依据：Windows PowerShell 5.1 没有 Select-Object -Reverse，回滚路径必须在目标原生环境可执行。
  for($rollbackIndex=$installed.Count-1;$rollbackIndex-ge0;$rollbackIndex--){
    # [2026-09-01 11:50:11] 作用：按当前倒序索引读取已安装记录；理由依据：依赖清单和启动器必须以安装相反顺序恢复。
    $installedItem=$installed[$rollbackIndex]
    # [2026-09-01 15:05:58] 作用：按安装前存在状态恢复旧目标或删除本次新增目标；理由依据：失败事务必须精确回到安装前文件集合。
    if($installedItem.TargetExisted){
      # [2026-09-01 15:05:58] 作用：声明与目标同目录的回滚临时文件；理由依据：旧字节恢复也必须在目标卷内原子完成。
      $rollbackTemporary=$installedItem.TargetPath+'.km-rollback-'+[guid]::NewGuid().ToString('N')+'.tmp'
      # [2026-09-01 15:05:58] 作用：把已验真的旧字节复制到回滚临时文件；理由依据：保留审计备份本体供失败后的人工复核。
      Copy-Item -LiteralPath $installedItem.BackupPath -Destination $rollbackTemporary -Force
      # [2026-09-01 15:05:58] 作用：按失败时正式目标是否仍存在选择替换或移动；理由依据：兼容目标被外部删除的极端恢复边界。
      if(Test-Path -LiteralPath $installedItem.TargetPath -PathType Leaf){
        # [2026-09-01 15:05:58] 作用：声明回滚替换时接收失败版本的非空路径；理由依据：Windows PowerShell 5.1 的四参数 File.Replace 禁止传入空备份路径。
        $rollbackDisplacedPath=$installedItem.TargetPath+'.km-rollback-displaced-'+[guid]::NewGuid().ToString('N')+'.tmp'
        # [2026-09-01 15:05:58] 作用：以真实被替换文件路径原子恢复安装前字节；理由依据：回滚不能再次触发本次已实锤的空路径异常。
        [IO.File]::Replace($rollbackTemporary,$installedItem.TargetPath,$rollbackDisplacedPath,$true)
        # [2026-09-01 15:05:58] 作用：删除仅用于满足原子替换合同的失败版本副本；理由依据：原始旧字节已在正式目标和审计备份各保留一份。
        Remove-Item -LiteralPath $rollbackDisplacedPath -Force -ErrorAction SilentlyContinue
      }else{
        # [2026-09-01 15:05:58] 作用：在正式目标缺失时直接移动回滚临时文件；理由依据：不存在目标无法调用 File.Replace。
        [IO.File]::Move($rollbackTemporary,$installedItem.TargetPath)
      }
    }else{
      # [2026-09-01 15:05:58] 作用：删除安装前不存在的本次新增目标；理由依据：回滚后的文件集合必须与安装前一致。
      Remove-Item -LiteralPath $installedItem.TargetPath -Force -ErrorAction SilentlyContinue
    }
  }
  # [2026-09-01 11:45:06] 作用：抛出包含原始故障和回滚目录的终止错误；理由依据：不得把已回滚事务描述成安装成功。
  throw "修复安装失败且已回滚：$installError；backup=$backupRoot"
}
# [2026-09-01 11:45:06] 作用：初始化服务启动验收状态；理由依据：文件安装成功不能冒充运行成功。
$servicesStarted=$false
# [2026-09-01 11:45:06] 作用：初始化 PgBouncer 运行证据；理由依据：未请求启动时结构化结果仍需明确空值边界。
$pgbouncerHealth='not_checked';$selectValue='not_checked'
# [2026-09-01 17:23:10] 作用：初始化商业网络、LLM 鉴权和 HTTP 健康证据；理由依据：未请求启动时不得把这些目标验收项默认为成功。
$commercialNetworkSubnet='not_checked';$llmModelsStatus='not_checked';$httpHealthCount=0
# [2026-09-01 11:45:06] 作用：按显式开关执行第二套既有固定入口；理由依据：修复不创建新启动流程且不调用第一套生命周期。
if($StartServices){
  # [2026-09-01 17:23:10] 作用：保存安装器父进程原 Docker Host；理由依据：验收结束必须恢复调用者环境且不能永久影响第一套或后续命令。
  $previousInstallerDockerHost=[Environment]::GetEnvironmentVariable('DOCKER_HOST','Process')
  # [2026-09-01 17:23:10] 作用：保存安装器父进程原 Docker Context；理由依据：DOCKER_CONTEXT 优先于 DOCKER_HOST，恢复时两者必须成对处理。
  $previousInstallerDockerContext=[Environment]::GetEnvironmentVariable('DOCKER_CONTEXT','Process')
  # [2026-09-01 17:23:10] 作用：进入父进程 Docker 端点事务；理由依据：子一键入口和其后的 inspect、exec 必须命中同一个 docker_engine_linux。
  try{
    # [2026-09-01 17:23:10] 作用：清除父进程可能残留的 Docker Context；理由依据：默认 desktop-linux 会覆盖第二套直连端点并产生已实锤 HTTP 500。
    [Environment]::SetEnvironmentVariable('DOCKER_CONTEXT',$null,'Process')
    # [2026-09-01 17:23:10] 作用：把父进程固定到第二套 profile 的 Linux Engine；理由依据：安装器验收不能在子进程退出后回落 dockerDesktopLinuxEngine。
    [Environment]::SetEnvironmentVariable('DOCKER_HOST',[string]$targetProfile.docker.engine_endpoint,'Process')
    # [2026-09-01 17:23:10] 作用：输出不含凭据的安装器 Docker 端点证据；理由依据：现场红错必须能从日志证明已命中正确 Engine。
    Write-Host "INSTALLER_SECOND_DOCKER_ENDPOINT_READY host=$([string]$env:DOCKER_HOST) context=$([string]$env:DOCKER_CONTEXT)"
    # [2026-09-01 11:45:06] 作用：运行目标原有第二套一键启动器；理由依据：共享业务行为继续由 server_second_ports profile 注入。
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $targetLauncher
    # [2026-09-01 11:45:06] 作用：保存固定入口真实退出码；理由依据：后续 Docker 探针会覆盖 LASTEXITCODE。
    $launcherExitCode=$LASTEXITCODE
    # [2026-09-01 11:45:06] 作用：阻断一键入口非零退出；理由依据：不能用单项健康探针掩盖全栈启动失败。
    if($launcherExitCode-ne0){throw "第二套固定一键入口失败：exit=$launcherExitCode"}
    # [2026-09-01 11:45:06] 作用：声明第二套 PgBouncer 容器身份；理由依据：验收不得误读第一套连接池。
    $pgbouncerContainer='sql-rag-server-km-pgbouncer'
    # [2026-09-01 11:45:06] 作用：声明第二套迁移 PostgreSQL 私网；理由依据：连接池必须永久加入本 profile 的 Compose default 网络。
    $migratedNetwork='sql-rag-server-migrated-source_default'
    # [2026-09-01 11:45:06] 作用：读取 PgBouncer 最终 Docker 健康状态；理由依据：端口监听不能替代容器真实 SQL 健康门禁。
    $pgbouncerHealth=([string](& docker.exe inspect --format '{{.State.Health.Status}}' $pgbouncerContainer|Select-Object -First 1)).Trim()
    # [2026-09-01 11:45:06] 作用：阻断 PgBouncer 非健康状态；理由依据：不能再次把 35/36 依赖失败报告为完成。
    if($LASTEXITCODE-ne0-or$pgbouncerHealth-ne'healthy'){throw "PgBouncer 未健康：$pgbouncerHealth"}
    # [2026-09-01 11:45:06] 作用：读取 PgBouncer 网络成员；理由依据：healthy 之外还要证明没有依赖宿主回环路由。
    $pgbouncerNetworks=(& docker.exe inspect --format '{{json .NetworkSettings.Networks}}' $pgbouncerContainer|Select-Object -First 1)|ConvertFrom-Json
    # [2026-09-01 11:45:06] 作用：阻断缺失当前迁移 PostgreSQL 私网；理由依据：第二套必须与第一套网络和生命周期完全隔离。
    if($null-eq$pgbouncerNetworks.PSObject.Properties[$migratedNetwork]){throw "PgBouncer 未接入第二套迁移私网：$migratedNetwork"}
    # [2026-09-01 11:45:06] 作用：经 PgBouncer 执行无空格真 SQL；理由依据：Windows Docker 会吞掉旧 SELECT 1 的嵌套引号，SELECT/**/1 保持同一 SQL 语义且已由 PowerShell 5.1 实测。
    $selectResult=@(& docker.exe exec $pgbouncerContainer sh -lc 'PGPASSWORD="$KM_PG_PASSWORD" psql -w -h 127.0.0.1 -p 6432 -U "$KM_PG_USER" -d "$KM_PG_DATABASE" -tAc SELECT/**/1' 2>&1)
    # [2026-09-01 11:45:06] 作用：保存 PgBouncer 真 SQL 退出码；理由依据：结果归一化会覆盖 LASTEXITCODE。
    $selectExitCode=$LASTEXITCODE
    # [2026-09-01 11:45:06] 作用：规范化 PgBouncer 查询单值；理由依据：只接受精确 1，不能把连接成功或空输出判绿。
    $selectValue=($selectResult-join'').Trim()
    # [2026-09-01 11:45:06] 作用：阻断真 SQL 失败或空值；理由依据：修复的正是旧安装器 exit=0 value= 假失败边界。
    if($selectExitCode-ne0-or$selectValue-ne'1'){throw "PgBouncer SELECT/**/1 未通过：exit=$selectExitCode value=$selectValue output=$($selectResult-join' | ')"}
    # [2026-09-01 17:23:10] 作用：声明第二套商业网络身份；理由依据：IPAM 验收不得读取第一套 sql-rag-km-commercial-internal。
    $commercialNetworkName='sql-rag-server-km-commercial-internal'
    # [2026-09-01 17:23:10] 作用：读取第二套商业网络 IPAM；理由依据：容器已启动仍不能替代固定不冲突子网的运行态证据。
    $commercialNetworkIpamDocument=((& docker.exe network inspect $commercialNetworkName --format '{{json .IPAM.Config}}'|Select-Object -First 1)|ConvertFrom-Json)
    # [2026-09-01 17:23:10] 作用：显式展开 PowerShell 5.1 返回的 IPAM 数组；理由依据：只接受单一 IPv4 配置。
    $commercialNetworkIpam=@($commercialNetworkIpamDocument|ForEach-Object{$_})
    # [2026-09-01 17:23:10] 作用：阻断商业网络子网或网关漂移；理由依据：172.20.0.0/16 会再次让 LLM Worker 外网路由失败。
    if($LASTEXITCODE-ne0-or$commercialNetworkIpam.Count-ne1-or[string]$commercialNetworkIpam[0].Subnet-ne[string]$payloadServerProfile.docker.commercial_network.subnet-or[string]$commercialNetworkIpam[0].Gateway-ne[string]$payloadServerProfile.docker.commercial_network.gateway){throw "第二套商业网络 IPAM 未修复：$($commercialNetworkIpam|ConvertTo-Json -Compress)"}
    # [2026-09-01 17:23:10] 作用：记录已验收的第二套商业子网；理由依据：最终 JSON 必须给出具体网络事实而不是布尔值。
    $commercialNetworkSubnet=[string]$commercialNetworkIpam[0].Subnet
    # [2026-09-01 17:23:10] 作用：声明 LLM Worker 容器身份；理由依据：真实模型鉴权必须从执行提示词提取的同一容器发起。
    $llmWorkerContainer='sql-rag-server-km-worker-llm'
    # [2026-09-01 17:23:10] 作用：构造不输出密钥的容器内 `/models` 鉴权探针；理由依据：宿主 443 成功不能代替 Worker 经新 bridge 的真实 HTTPS 路由。
    $llmModelsProbe=@'
# [2026-09-01 17:23:10] 作用：读取容器 LLM 环境并调用其实际模型入口；理由依据：验证与业务 Worker 完全一致的 URL 和凭据来源。
import os, urllib.request
# [2026-09-01 17:23:10] 作用：按业务客户端兼容顺序选择模型服务 URL；理由依据：不得在验收器另写一个目标地址。
url = (os.getenv("LLM_SERVICE_URL") or os.getenv("OPENAI_BASE_URL") or "https://api.siliconflow.cn/v1").rstrip("/")
# [2026-09-01 17:23:10] 作用：按业务客户端兼容顺序选择 API 密钥；理由依据：只验证存在性且绝不打印密钥。
key = os.getenv("LLM_SERVICE_API_KEY") or os.getenv("LLM_BINDING_API_KEY") or os.getenv("OPENAI_API_KEY") or ""
# [2026-09-01 17:23:10] 作用：阻断容器缺失密钥；理由依据：无鉴权请求不能证明真实模型服务可用。
assert key, "LLM API key missing"
# [2026-09-01 17:23:10] 作用：创建带 Bearer 鉴权的模型列表请求；理由依据：与实际 OpenAI-compatible 客户端协议一致。
request = urllib.request.Request(url + "/models", headers={"Authorization": "Bearer " + key})
# [2026-09-01 17:23:10] 作用：在二十秒硬上限内读取响应；理由依据：路由冲突必须快速成为具名失败而不是 WebUI 58% 长时间超时。
with urllib.request.urlopen(request, timeout=20) as response:
    # [2026-09-01 17:23:10] 作用：只输出 HTTP 状态；理由依据：不泄露模型正文或任何凭据。
    print("STATUS=" + str(response.status))
'@
    # [2026-09-01 17:23:10] 作用：通过标准输入在 LLM Worker 内执行探针；理由依据：避免 Windows PowerShell 5.1 的 python -c 多层引号错误。
    $llmModelsProbeOutput=@($llmModelsProbe|& docker.exe exec -i $llmWorkerContainer python - 2>&1)
    # [2026-09-01 17:23:10] 作用：保存容器模型探针退出码；理由依据：输出归一化会覆盖 LASTEXITCODE。
    $llmModelsProbeExitCode=$LASTEXITCODE
    # [2026-09-01 17:23:10] 作用：提取不含凭据的 HTTP 状态证据；理由依据：只接受精确认证成功 200。
    $llmModelsStatus=([string](@($llmModelsProbeOutput|Where-Object{[string]$_-match'^STATUS='}|Select-Object -Last 1)-join'')).Replace('STATUS=','').Trim()
    # [2026-09-01 17:23:10] 作用：阻断容器外网路由或鉴权失败；理由依据：该门禁直接覆盖本次 58% 超时的第一处分歧。
    if($llmModelsProbeExitCode-ne0-or$llmModelsStatus-ne'200'){throw "第二套 LLM Worker /models 未通过：exit=$llmModelsProbeExitCode status=$llmModelsStatus output=$($llmModelsProbeOutput-join' | ')"}
    # [2026-09-01 17:23:10] 作用：声明第二套四个固定 HTTP 健康入口；理由依据：后端、WebUI 直连及统一挂载必须与一键启动同次验收。
    $healthUrls=@('http://172.18.1.233:28320/health','http://172.18.1.233:28321/health','http://172.18.1.233:28321/api/health','http://172.18.1.233:28191/knowledgeManagement/api/health')
    # [2026-09-01 17:23:10] 作用：逐项执行有限时 HTTP 探针；理由依据：33 个监听不能证明反向代理和应用路由返回成功。
    foreach($healthUrl in $healthUrls){
      # [2026-09-01 17:23:10] 作用：读取当前健康入口响应；理由依据：只接受真实 HTTP 状态码。
      $healthResponse=Invoke-WebRequest -UseBasicParsing -Uri $healthUrl -TimeoutSec 10
      # [2026-09-01 17:23:10] 作用：阻断非 200 健康响应；理由依据：红色超时修复不能只验证容器内部状态。
      if([int]$healthResponse.StatusCode-ne200){throw "第二套 HTTP 健康未通过：url=$healthUrl status=$([int]$healthResponse.StatusCode)"}
      # [2026-09-01 17:23:10] 作用：累计已通过 HTTP 入口；理由依据：最终必须精确为四项而不是至少一项。
      $httpHealthCount++
    }
    # [2026-09-01 11:45:06] 作用：读取目标当前全部 TCP 监听端口；理由依据：一键成功必须覆盖完整 33 端口 profile。
    $listeningPorts=@(Get-NetTCPConnection -State Listen|Select-Object -ExpandProperty LocalPort -Unique)
    # [2026-09-01 11:45:06] 作用：计算第二套缺失监听；理由依据：任一业务、模型、数据库或商业端口缺失都不能声明完成。
    $missingPorts=@($expectedPorts|Where-Object{$listeningPorts-notcontains$_})
    # [2026-09-01 11:45:06] 作用：阻断 33 端口未完整监听；理由依据：ServicesStarted 必须对应完整第二套而非单独修好 PgBouncer。
    if($missingPorts.Count-ne0){throw "第二套缺少监听端口：$($missingPorts-join',')"}
    # [2026-09-01 17:23:10] 作用：标记固定入口、IPAM、私网、真 SQL、容器鉴权、HTTP 和端口全部通过；理由依据：只有此时才允许输出 ServicesStarted=true。
    $servicesStarted=$true
  }
  # [2026-09-01 17:23:10] 作用：无论启动或验收成功失败都恢复父进程 Docker 环境；理由依据：安装器不能把第二套端点泄漏给调用者后续命令。
  finally{
    # [2026-09-01 17:23:10] 作用：恢复调用前 DOCKER_HOST；理由依据：保留空值或原自定义端点的精确状态。
    [Environment]::SetEnvironmentVariable('DOCKER_HOST',$previousInstallerDockerHost,'Process')
    # [2026-09-01 17:23:10] 作用：恢复调用前 DOCKER_CONTEXT；理由依据：与 DOCKER_HOST 一起还原 Docker CLI 优先级环境。
    [Environment]::SetEnvironmentVariable('DOCKER_CONTEXT',$previousInstallerDockerContext,'Process')
  }
}
# [2026-09-01 17:23:10] 作用：输出文件安装、固定网络与运行验收的结构化结果；理由依据：明确区分本地包验证、目标落盘、容器外网和目标服务完成四种证据。
[pscustomobject]@{Result='READY';Update='knowledge_startup_nas_repair';Mode='installed';PayloadFiles=$installed.Count;BackupDirectory=$backupRoot;Profile='server_second_ports';RuntimeMode='source_build';PortContract=33;BusinessParsingFilesChanged=0;CommercialNetworkSubnet=$commercialNetworkSubnet;PgBouncerHealth=$pgbouncerHealth;PgBouncerSelectValue=$selectValue;LlmModelsStatus=$llmModelsStatus;HttpHealthCount=$httpHealthCount;ServicesStarted=$servicesStarted}|ConvertTo-Json -Depth 5
