param(
  [switch]$RebuildExternalQdrant,
  [switch]$RunDatabaseInit,
  [switch]$RestartModel,
  [string]$ExternalSourceProfile='external_database',
  [switch]$ConfigureTrustedDataOnly,
  # [2026-07-30 16:11:00] 作用：接收普通用户入口序列化的非密钥部署环境；理由依据：Windows UAC ShellExecute 不保证继承调用进程的临时环境变量。
  [string]$InheritedDeploymentEnvironment='',
  # [2026-08-03 15:42:17] 作用：接收单profile独立运行合同路径；理由依据：第二套服务器不得再从本地与服务器共生JSON中选择路由。
  [string]$ServiceProfilePath='',
  # [2026-08-03 15:48:01] 作用：只读输出端口与Docker身份解析结果；理由依据：第一套和第二套必须能在不启动Docker或服务时做同构合同对照。
  [switch]$ValidateServiceProfileOnly
)
$ErrorActionPreference='Stop'
try { $global:PSNativeCommandUseErrorActionPreference=$false } catch {}
# [2026-07-30 16:11:01] 作用：在读取端口 profile 前恢复父进程传入的非密钥部署环境；理由依据：管理员子进程必须配置与普通用户入口完全相同的第二套端口。
if(-not [string]::IsNullOrWhiteSpace($InheritedDeploymentEnvironment)){
  # [2026-07-30 16:11:02] 作用：把 Base64 参数还原为 UTF-8 JSON；理由依据：Base64 可避免路径空格、中文和 CIDR 在 UAC 命令行中被错误拆分。
  $inheritedJson=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($InheritedDeploymentEnvironment))
  # [2026-07-30 16:11:03] 作用：解析父进程环境对象；理由依据：只恢复白名单变量而不传递密码、令牌或完整环境。
  $inheritedValues=$inheritedJson|ConvertFrom-Json
  # [2026-07-30 16:11:04] 作用：逐项写入当前管理员子进程环境；理由依据：后续原启动代码继续使用同一环境变量合同且无需复制业务逻辑。
  foreach($inheritedProperty in $inheritedValues.PSObject.Properties){Set-Item -LiteralPath "Env:$($inheritedProperty.Name)" -Value ([string]$inheritedProperty.Value)}
}
# [2026-07-28] 作用：一键启动在需要系统级可信数据端口代理时自动提升为管理员进程；理由依据：Qdrant 和关系数据库端口必须作为同一份可信局域网合同整体配置，用户不应再手工补防火墙命令。
$currentIdentity=[Security.Principal.WindowsIdentity]::GetCurrent()
$currentPrincipal=[Security.Principal.WindowsPrincipal]::new($currentIdentity)
$isAdministrator=$currentPrincipal.IsInRole(
  [Security.Principal.WindowsBuiltInRole]::Administrator
)
# [2026-07-28] 作用：只在当前端口配置的可信数据系统规则缺失或漂移时重新启动管理员子进程；理由依据：规则持久化后，普通重启不应每次重复弹 UAC。
function Invoke-ElevatedLauncher{
  # [2026-07-30 16:11:05] 作用：声明允许传给 UAC 子进程的非密钥部署变量白名单；理由依据：第二套端口、局域网和路径必须继承，但数据库密码与模型密钥不能进入命令行。
  $inheritedNames=@('SQL_RAG_REPO_ROOT','SQL_RAG_DEPLOYMENT_PROFILE','SQL_RAG_SERVICE_PROFILE_PATH','SQL_RAG_DOCKER_BACKEND','SQL_RAG_DATABASE_BIND','SQL_RAG_EXTERNAL_PG_HOST','SQL_RAG_PUBLIC_HOST','SQL_RAG_INTERNAL_NETWORK','SQL_RAG_COMPOSE_PROJECT','SQL_RAG_TRUSTED_QDRANT_LISTEN_ADDRESS','SQL_RAG_TRUSTED_QDRANT_CONNECT_ADDRESS','SQL_RAG_TRUSTED_QDRANT_REMOTE_ADDRESS','SQL_RAG_TRUSTED_RELATIONAL_DATABASE_LISTEN_ADDRESS','SQL_RAG_TRUSTED_RELATIONAL_DATABASE_CONNECT_ADDRESS','SQL_RAG_TRUSTED_RELATIONAL_DATABASE_REMOTE_ADDRESS')
  # [2026-07-30 16:11:06] 作用：初始化传给管理员子进程的白名单对象；理由依据：必须显式控制可跨 UAC 边界的配置范围。
  $inheritedMap=[ordered]@{}
  # [2026-07-30 16:11:07] 作用：从当前已解析入口收集非空白名单值；理由依据：管理员子进程应复用父进程真实生效值而不是重新猜测 profile。
  foreach($inheritedName in $inheritedNames){$inheritedValue=[Environment]::GetEnvironmentVariable($inheritedName,[EnvironmentVariableTarget]::Process);if(-not [string]::IsNullOrWhiteSpace($inheritedValue)){$inheritedMap[$inheritedName]=$inheritedValue}}
  # [2026-07-30 16:11:08] 作用：把白名单对象序列化为无换行 Base64；理由依据：保证路径空格和中文在 Start-Process ArgumentList 中保持一个参数。
  $inheritedBase64=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes(($inheritedMap|ConvertTo-Json -Compress)))
  $elevatedArguments=(
    '-NoProfile -ExecutionPolicy Bypass -File "' +
    $PSCommandPath +
    '" -ConfigureTrustedDataOnly -InheritedDeploymentEnvironment "' +
    $inheritedBase64 +
    '"'
  )
  Write-Host '一键启动只需管理员权限配置可信数据端口组；请在 Windows UAC 中点击“是”。'
  try{
    $elevatedProcess=Start-Process `
      -FilePath 'powershell.exe' `
      -Verb RunAs `
      -ArgumentList $elevatedArguments `
      -Wait `
      -PassThru
  }catch{
    throw "无法启动管理员一键进程：$($_.Exception.Message)"
  }
  if($elevatedProcess.ExitCode -ne 0){
    throw "管理员可信数据配置进程执行失败，退出码=$($elevatedProcess.ExitCode)"
  }
  # 管理员子进程只配置持久系统规则；Docker Desktop、模型和所有业务
  # 服务必须回到当前普通交互用户会话启动。
  return $false
}
# [2026-07-24 16:45:37] 作用：优先读取标准化部署仓库根目录；理由依据：同一启动脚本必须同时适配本机旧目录和阿里云 D:\MonFangAI\GetDAM 目录。
$RepoRoot=[string]$env:SQL_RAG_REPO_ROOT
# [2026-07-24 16:45:38] 作用：未配置云端环境变量时，从启动脚本自身位置反推仓库根目录；理由依据：源码目录整体移动后不应再依赖任何写死盘符路径。
if([string]::IsNullOrWhiteSpace($RepoRoot)){
  $RepoRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..')).Path
}else{
  # [2026-07-24 16:45:39] 作用：严格解析显式仓库路径；理由依据：路径缺失时要在拉起服务前立即失败，避免子服务分散报错。
  $RepoRoot=(Resolve-Path -LiteralPath $RepoRoot).Path
}
$SqlRag=Join-Path $RepoRoot 'app\SQL_RAG'
# [2026-07-24 16:45:40] 作用：校验 SQL_RAG 主入口确实属于解析后的仓库；理由依据：防止环境变量指向错误目录后继续启动部分服务。
$MainEntry=Join-Path $SqlRag 'main.py'
if(-not (Test-Path -LiteralPath $MainEntry -PathType Leaf)){throw "SQL_RAG 主入口不存在：$MainEntry"}
# [2026-08-03 15:42:18] 作用：允许固定入口通过参数或进程环境声明单profile合同；理由依据：UAC受控子进程也必须继承同一份第二套独立配置。
if([string]::IsNullOrWhiteSpace($ServiceProfilePath)){$ServiceProfilePath=[string]$env:SQL_RAG_SERVICE_PROFILE_PATH}
# [2026-08-03 15:42:19] 作用：区分单profile独立合同与本地历史兼容合同；理由依据：服务器必须完全跳过同时含两套配置的旧文件。
$usesIndependentServiceProfile=-not[string]::IsNullOrWhiteSpace($ServiceProfilePath)
# [2026-08-03 15:42:20] 作用：初始化运行profile集合；理由依据：后续端口与可信规则验证只遍历本次合同允许管理的实例。
$RuntimeServiceProfiles=@()
if($usesIndependentServiceProfile){
  # [2026-08-03 15:42:21] 作用：严格解析第二套独立合同路径；理由依据：路径缺失时禁止回落到local默认值。
  $PortProfilesPath=(Resolve-Path -LiteralPath $ServiceProfilePath -ErrorAction Stop).Path
  # [2026-08-03 15:42:22] 作用：读取单profile独立合同；理由依据：第二套端口、网络和Docker身份必须原子解析。
  $ServicePortProfile=Get-Content -LiteralPath $PortProfilesPath -Raw -Encoding UTF8|ConvertFrom-Json
  # [2026-08-03 15:42:23] 作用：从独立合同取得正式profile名称；理由依据：禁止使用历史aliyun兼容键进行条件路由。
  $DeploymentProfile=([string]$ServicePortProfile.profile_name).Trim().ToLowerInvariant()
  # [2026-08-03 15:42:24] 作用：把当前独立合同作为唯一可管理profile；理由依据：服务器启动不能检查、修改或停止第一套资源。
  $RuntimeServiceProfiles=@([pscustomobject]@{Name=$DeploymentProfile;Value=$ServicePortProfile})
}else{
  # [2026-08-03 15:42:25] 作用：仅为已验收本地第一套保留历史双profile文件兼容读取；理由依据：本次解耦不得破坏本地现有启动方式。
  $PortProfilesPath=Join-Path $SqlRag 'deployment\service-port-profiles.json'
  # [2026-08-03 15:42:26] 作用：阻断本地兼容合同缺失；理由依据：旧入口也不能在无端口事实源时继续。
  if(!(Test-Path -LiteralPath $PortProfilesPath -PathType Leaf)){throw "服务端口配置不存在：$PortProfilesPath"}
  # [2026-08-03 15:42:27] 作用：读取本地兼容合同；理由依据：第一套行为保持原样直到单独迁移。
  $PortProfiles=Get-Content -LiteralPath $PortProfilesPath -Raw -Encoding UTF8|ConvertFrom-Json
  # [2026-08-03 15:42:28] 作用：读取本地兼容入口显式profile；理由依据：未声明时只允许回落local而不是服务器第二套。
  $DeploymentProfile=[string]$env:SQL_RAG_DEPLOYMENT_PROFILE
  # [2026-08-03 15:42:29] 作用：保持本地固定默认profile；理由依据：不改变已跑通的第一套一键入口。
  if([string]::IsNullOrWhiteSpace($DeploymentProfile)){$DeploymentProfile='local'}
  # [2026-08-03 15:42:30] 作用：规范化本地兼容profile键；理由依据：配置查找必须大小写稳定。
  $DeploymentProfile=$DeploymentProfile.Trim().ToLowerInvariant()
  # [2026-08-03 15:42:31] 作用：按本地兼容键读取profile；理由依据：服务器独立入口不会进入该分支。
  $profileProperty=$PortProfiles.profiles.PSObject.Properties[$DeploymentProfile]
  # [2026-08-03 15:42:32] 作用：拒绝未知本地兼容profile；理由依据：禁止静默回落或跨套选择。
  if($null-eq$profileProperty){throw "不支持的本地兼容SQL_RAG_DEPLOYMENT_PROFILE：$DeploymentProfile。"}
  # [2026-08-03 15:42:33] 作用：取得本地兼容profile值；理由依据：后续业务编排继续复用既有合同。
  $ServicePortProfile=$profileProperty.Value
  # [2026-08-03 15:42:34] 作用：建立本地兼容校验集合；理由依据：只有旧入口仍检查历史两套端口不重叠。
  $RuntimeServiceProfiles=@($PortProfiles.profiles.PSObject.Properties|ForEach-Object{[pscustomobject]@{Name=$_.Name;Value=$_.Value}})
}
# [2026-08-03 15:42:35] 作用：锁定第二套独立合同的正式名称；理由依据：显式配置路径不能被伪装为local或历史aliyun键。
if($usesIndependentServiceProfile-and$DeploymentProfile-ne'server_second_ports'){throw "独立服务器profile名称无效：$DeploymentProfile"}
# [2026-08-03 15:48:05] 作用：阻断独立合同重新嵌入profiles路由集合；理由依据：数据结构必须保证第二套永远不能读取第一套值。
if($usesIndependentServiceProfile-and($null-ne$ServicePortProfile.PSObject.Properties['profiles']-or[int]$ServicePortProfile.schema_version-ne1)){throw '第二套独立运行合同结构无效或重新包含profiles集合。'}
# [2026-08-04 08:41:44] 作用：默认保留第一套在线刷新后回退随包基线的数据策略；理由依据：本地既有权威源同步行为不得被第二套独立部署修改。
$CloneRefreshMode='online_then_portable'
# [2026-08-04 08:41:45] 作用：仅从第二套独立profile读取其数据刷新策略；理由依据：新服务器必须由自己的合同决定只使用打包基线，禁止从第一套分支推导。
if($usesIndependentServiceProfile){$CloneRefreshMode=([string]$ServicePortProfile.data.clone_refresh_mode).Trim().ToLowerInvariant()}
# [2026-08-04 08:41:46] 作用：阻断缺失或未知的第二套数据刷新模式；理由依据：部署逻辑不能静默回落到会访问第一套权威源的在线克隆路径。
if($CloneRefreshMode-notin@('online_then_portable','portable_seed_only')){throw "数据克隆刷新模式无效：$CloneRefreshMode"}
# [2026-08-03 15:48:06] 作用：声明第二套Docker身份必备字段；理由依据：端口隔离之外还必须固定Compose、容器、网络与迁移卷归属。
$requiredIndependentDockerFields=@('backend','compose_project','container_name_prefix','internal_network','migration_compose_project')
# [2026-08-03 15:48:07] 作用：逐项阻断空白或非法Docker身份；理由依据：缺值不得再由local/else默认分支补齐。
if($usesIndependentServiceProfile){foreach($dockerField in $requiredIndependentDockerFields){$dockerProperty=$ServicePortProfile.docker.PSObject.Properties[$dockerField];if($null-eq$dockerProperty-or[string]::IsNullOrWhiteSpace([string]$dockerProperty.Value)-or([string]$dockerProperty.Value)-notmatch'^[A-Za-z0-9._-]+$'){throw "第二套独立运行合同Docker字段无效：$dockerField"}}}
# [2026-08-03 18:04:38] 作用：初始化当前运行合同的Docker Engine端点；理由依据：本地第一套继续由既有context管理，只有独立第二套拥有固定直连管道。
$DockerEngineEndpoint=''
# [2026-08-03 18:04:39] 作用：从第二套独立profile读取Docker Engine端点；理由依据：端点必须与端口、Compose和网络一样由第二套自己的配置持有。
if($usesIndependentServiceProfile){$DockerEngineEndpoint=([string]$ServicePortProfile.docker.engine_endpoint).Trim()}
# [2026-08-03 18:04:40] 作用：拒绝第二套继续指向Desktop API代理或任意外部daemon；理由依据：目标机已三次证明dockerDesktopLinuxEngine代理HTTP500，而docker_engine_linux是同机直连Linux Engine管道。
if($usesIndependentServiceProfile-and$DockerEngineEndpoint-ne'npipe:////./pipe/docker_engine_linux'){throw "第二套独立运行合同Docker直连端点无效：$DockerEngineEndpoint"}
# [2026-08-03 18:04:41] 作用：清除会覆盖DOCKER_HOST的第二套进程级context；理由依据：Docker官方规定DOCKER_CONTEXT优先于DOCKER_HOST，必须消除调用环境漂移。
if($usesIndependentServiceProfile){Remove-Item Env:DOCKER_CONTEXT -ErrorAction SilentlyContinue}
# [2026-08-03 18:04:42] 作用：把第二套全部Docker CLI与Compose调用绑定到直连Linux Engine管道；理由依据：仅设置当前进程环境不会更改第一套全局context或配置文件。
if($usesIndependentServiceProfile){$env:DOCKER_HOST=$DockerEngineEndpoint}
# [2026-08-03 15:42:36] 作用：取得当前合同的端口表；理由依据：全部服务只允许消费当前独立对象。
$ServicePorts=$ServicePortProfile.ports
# [2026-08-28 18:31:00] 作用：要求第二套独立合同恰好声明33个服务端口；理由依据：当前 profile 已包含全景缓存、Pgbouncer 及商业知识对象、断点上传、Broker和观测服务的完整33项合同。
if($usesIndependentServiceProfile-and@($ServicePorts.PSObject.Properties).Count-ne33){throw "第二套独立运行合同必须恰好包含33个端口，实际=$(@($ServicePorts.PSObject.Properties).Count)"}
# [2026-08-04 13:43:49] 作用：从当前唯一profile读取MinIO内部API端点；理由依据：第一套与第二套必须各自持有完整对象存储合同，不能再继承第三方.env中的失效krauss地址。
$MinioEndpoint=[string]$ServicePortProfile.minio_endpoint
# [2026-08-04 13:43:49] 作用：仅为旧profile兼容进程级MinIO内部端点；理由依据：新合同缺字段时仍允许受控运维覆盖，但正式两套始终以各自profile为准。
if([string]::IsNullOrWhiteSpace($MinioEndpoint)){$MinioEndpoint=[string]$env:MINIO_ENDPOINT}
# [2026-08-04 13:43:49] 作用：规范化当前profile的MinIO内部API端点；理由依据：空格不能进入SDK签名或DNS解析。
$MinioEndpoint=$MinioEndpoint.Trim()
# [2026-08-04 13:43:49] 作用：拒绝协议、路径和缺失端口的MinIO内部端点；理由依据：无效对象存储合同必须在启动Docker和业务服务前失败关闭。
if($MinioEndpoint-notmatch'^[A-Za-z0-9.-]+:\d{1,5}$'){throw "MinIO 内部端点必须为 host:port：$MinioEndpoint"}
# [2026-08-04 13:43:49] 作用：把当前profile的内部MinIO端点注入Getsoft适配器；理由依据：python-dotenv不得再把两套拉回172.18.1.166旧服务。
$env:MINIO_ENDPOINT=$MinioEndpoint
# [2026-08-04 13:43:49] 作用：优先读取当前profile的浏览器MinIO入口；理由依据：同一PowerShell先后启动两套时不能继承上一套残留环境而串线。
$MinioPublicEndpoint=[string]$ServicePortProfile.minio_public_endpoint
# [2026-08-04 13:43:49] 作用：仅为旧profile兼容运维显式浏览器入口；理由依据：正式两套配置完整时必须以各自profile为唯一事实源。
if([string]::IsNullOrWhiteSpace($MinioPublicEndpoint)){$MinioPublicEndpoint=[string]$env:MINIO_PUBLIC_ENDPOINT}
# [2026-07-31 13:55:38] 作用：规范化公开端点；理由依据：环境变量空格不能进入 S3 Host 签名。
$MinioPublicEndpoint=$MinioPublicEndpoint.Trim()
# [2026-07-31 13:55:38] 作用：拒绝协议、路径和缺失端口的公开端点；理由依据：MinIO SDK 需要 host:port 且签名地址不能被任意 URL 路径污染。
if($MinioPublicEndpoint -notmatch '^[A-Za-z0-9.-]+:\d{1,5}$'){throw "MinIO 公开端点必须为 host:port：$MinioPublicEndpoint"}
# [2026-07-31 13:55:38] 作用：把当前 profile 的公开 MinIO 入口注入 Getsoft 子进程；理由依据：python-dotenv 不覆盖父进程值，可确保一键启动不再回退 krauss 短主机名。
$env:MINIO_PUBLIC_ENDPOINT=$MinioPublicEndpoint
function Get-ServiceProfilePort{
  param([Parameter(Mandatory=$true)][string]$Name)
  $property=$ServicePorts.PSObject.Properties[$Name]
  if($null -eq $property){throw "端口配置 $DeploymentProfile 缺少服务：$Name"}
  $port=0
  if(
    -not [int]::TryParse([string]$property.Value,[ref]$port) -or
    $port -lt 1 -or
    $port -gt 65535
  ){throw "端口配置 $DeploymentProfile/$Name 无效：$($property.Value)"}
  return $port
}
$allProfilePorts=@(
  $ServicePorts.PSObject.Properties |
    ForEach-Object {Get-ServiceProfilePort -Name $_.Name}
)
if(($allProfilePorts | Select-Object -Unique).Count -ne $allProfilePorts.Count){
  throw "端口配置 $DeploymentProfile 存在重复宿主机端口。"
}
# [2026-07-31 09:45:01] 作用：收集两套 profile 的全部宿主机端口及归属；理由依据：分别启动成功仍不足以证明同时运行时不会发生跨 profile 端口碰撞。
$profilePortOwners=@{}
# [2026-07-31 09:45:02] 作用：对两套 profile 做全局端口唯一性断言；理由依据：服务器迁移 PostgreSQL 旧端口 15432 曾与本地 checkpoint PostgreSQL 冲突并造成截图中的假启动。
foreach($portProfileProperty in $RuntimeServiceProfiles){foreach($portProperty in $portProfileProperty.Value.ports.PSObject.Properties){$hostPort=[int]$portProperty.Value;$owner="$($portProfileProperty.Name)/$($portProperty.Name)";if($profilePortOwners.ContainsKey($hostPort)){throw "运行合同端口冲突：$hostPort 同时属于 $($profilePortOwners[$hostPort]) 和 $owner"};$profilePortOwners[$hostPort]=$owner}}
# [2026-07-31 09:45:03] 作用：区分本地第一套和新服务器第二套运行身份；理由依据：业务逻辑共用不等于 Docker 项目、容器、卷和网络可以共用。
$isLocalDeploymentProfile=($DeploymentProfile -eq 'local')
# [2026-07-31 09:45:04] 作用：为本地保留历史 Compose 项目名并给服务器分配新项目名；理由依据：保留本地既有卷数据，同时让服务器卷自动获得独立项目前缀。
# [2026-08-03 15:42:37] 作用：优先从独立合同读取Compose项目名；理由依据：第二套身份不再由local分支的else结果推导。
$ComposeProjectName=if($usesIndependentServiceProfile){([string]$ServicePortProfile.docker.compose_project).Trim()}elseif($isLocalDeploymentProfile){'sql_rag'}else{'sql_rag_server'}
# [2026-07-31 09:45:05] 作用：为两套数据库容器生成互不相同的身份前缀；理由依据：Docker 的 container_name 在整台主机全局唯一。
# [2026-08-03 15:42:38] 作用：优先从独立合同读取容器前缀；理由依据：服务器容器身份必须属于自己的配置文件。
$ContainerNamePrefix=if($usesIndependentServiceProfile){([string]$ServicePortProfile.docker.container_name_prefix).Trim()}elseif($isLocalDeploymentProfile){'sql-rag'}else{'sql-rag-server'}
# [2026-07-31 09:45:06] 作用：为两套 Compose 分配独立内部网络；理由依据：同名 bridge 会让两套数据库容器互相解析和串库。
# [2026-08-03 15:42:39] 作用：优先从独立合同读取Docker内部网络；理由依据：服务器网络身份不再依赖第一套分支。
$ProfileInternalDockerNetwork=if($usesIndependentServiceProfile){([string]$ServicePortProfile.docker.internal_network).Trim()}elseif($isLocalDeploymentProfile){'monfangai-sql-rag-internal'}else{'monfangai-sql-rag-server-internal'}
# [2026-07-31 09:45:07] 作用：为独立迁移 PostgreSQL 分配 profile 专属 Compose 项目；理由依据：该容器不在主 Compose 内，必须同步拆分容器与卷。
# [2026-08-03 15:42:40] 作用：优先从独立合同读取迁移库Compose项目；理由依据：迁移卷与容器也必须摆脱local/else派生关系。
$MigrationComposeProjectName=if($usesIndependentServiceProfile){([string]$ServicePortProfile.docker.migration_compose_project).Trim()}elseif($isLocalDeploymentProfile){'sql-rag-migrated-source'}else{'sql-rag-server-migrated-source'}
# [2026-07-31 09:45:08] 作用：定义当前 profile 的全部 Docker 身份环境；理由依据：Compose、运行态校验、种子恢复和 sqlcmd 必须引用同一组容器名。
$profileContainerEnvironment=[ordered]@{SQL_RAG_COMPOSE_PROJECT=$ComposeProjectName;SQL_RAG_INTERNAL_NETWORK=$ProfileInternalDockerNetwork;SQL_RAG_SQLSERVER_CONTAINER="$ContainerNamePrefix-sqlserver-2022";SQL_RAG_SQLSERVER_INIT_CONTAINER="$ContainerNamePrefix-sqlserver-init";SQL_RAG_QDRANT_CONTAINER="$ContainerNamePrefix-qdrant";SQL_RAG_CHECKPOINT_CONTAINER="$ContainerNamePrefix-postgres-checkpoint";WKT_PRASING_EXTRA_PG_CONTAINER="$ContainerNamePrefix-wkt-prasing-extra-postgres";SQL_RAG_WKT_EXTRA_QDRANT_CONTAINER="$ContainerNamePrefix-wkt-prasing-extra-qdrant";SQL_RAG_EXTERNAL_SQLSERVER_CONTAINER="$ContainerNamePrefix-external-sqlserver-2022";SQL_RAG_EXTERNAL_SQLSERVER_INIT_CONTAINER="$ContainerNamePrefix-external-sqlserver-init";SQL_RAG_EXTERNAL_QDRANT_CONTAINER="$ContainerNamePrefix-external-qdrant";SQL_RAG_NEO4J_CONTAINER="$ContainerNamePrefix-neo4j";SQL_RAG_MIGRATED_PG_CONTAINER="$ContainerNamePrefix-migrated-source-postgres";SQL_RAG_MIGRATED_PG_VOLUME="$ContainerNamePrefix-migrated-source-postgres-data";SQL_RAG_MIGRATED_PG_PROJECT=$MigrationComposeProjectName;RAG_SQLCMD_CONTAINER="$ContainerNamePrefix-sqlserver-2022"}
# [2026-07-31 09:45:09] 作用：把当前 profile 的 Docker 身份注入本次一键进程；理由依据：进程环境必须优先于另一安装目录遗留的 .env 或机器变量。
foreach($entry in $profileContainerEnvironment.GetEnumerator()){Set-Item -LiteralPath "Env:$($entry.Key)" -Value ([string]$entry.Value)}
# [2026-07-31 09:45:10] 作用：建立运行态安全校验使用的具名容器表；理由依据：校验不能继续写死本地容器名并误读另一套运行实例。
$DatabaseContainerNames=[ordered]@{SqlServer=$profileContainerEnvironment.SQL_RAG_SQLSERVER_CONTAINER;Qdrant=$profileContainerEnvironment.SQL_RAG_QDRANT_CONTAINER;Checkpoint=$profileContainerEnvironment.SQL_RAG_CHECKPOINT_CONTAINER;ClonePostgres=$profileContainerEnvironment.WKT_PRASING_EXTRA_PG_CONTAINER;CloneQdrant=$profileContainerEnvironment.SQL_RAG_WKT_EXTRA_QDRANT_CONTAINER;ExternalSqlServer=$profileContainerEnvironment.SQL_RAG_EXTERNAL_SQLSERVER_CONTAINER;ExternalQdrant=$profileContainerEnvironment.SQL_RAG_EXTERNAL_QDRANT_CONTAINER;Neo4j=$profileContainerEnvironment.SQL_RAG_NEO4J_CONTAINER}
$BackendPort=Get-ServiceProfilePort 'business_backend'
$WebPort=Get-ServiceProfilePort 'business_web'
$AssetTypeBackendPort=Get-ServiceProfilePort 'asset_backend'
$AssetTypeWebPort=Get-ServiceProfilePort 'asset_web'
$KnowledgeBackendPort=Get-ServiceProfilePort 'knowledge_backend'
$KnowledgeWebPort=Get-ServiceProfilePort 'knowledge_web'
# [2026-08-15 22:18:00] 作用：读取商业知识缓存网关端口；理由依据：API 不直接访问 Redis Cluster 拓扑。
$KnowledgeCacheGatewayPort=Get-ServiceProfilePort 'knowledge_cache_gateway'
# [2026-08-15 22:18:00] 作用：读取商业知识 MinIO API 端口；理由依据：原文件和解析产物使用 profile 专属对象入口。
$KnowledgeMinioApiPort=Get-ServiceProfilePort 'knowledge_minio_api'
# [2026-08-15 22:18:00] 作用：读取商业知识 MinIO 控制台端口；理由依据：对象容量和生命周期需要独立运维入口。
$KnowledgeMinioConsolePort=Get-ServiceProfilePort 'knowledge_minio_console'
# [2026-08-15 22:18:00] 作用：读取 tusd 标准断点上传端口；理由依据：浏览器大文件上传与 FastAPI 业务请求解耦。
$KnowledgeTusdPort=Get-ServiceProfilePort 'knowledge_tusd'
# [2026-08-15 22:18:00] 作用：读取 RabbitMQ AMQP 端口；理由依据：Celery 商业任务只使用正式 Broker。
$KnowledgeRabbitMqAmqpPort=Get-ServiceProfilePort 'knowledge_rabbitmq_amqp'
# [2026-08-15 22:18:00] 作用：读取 RabbitMQ 管理端口；理由依据：队列深度、消费者和 Quorum 状态进入启动验收。
$KnowledgeRabbitMqManagementPort=Get-ServiceProfilePort 'knowledge_rabbitmq_management'
# [2026-08-15 22:18:00] 作用：读取 Flower 端口；理由依据：Worker 与任务短期诊断拥有固定 URL。
$KnowledgeFlowerPort=Get-ServiceProfilePort 'knowledge_flower'
# [2026-08-15 22:18:00] 作用：读取 Prometheus 端口；理由依据：商业任务基础设施指标进入统一时序存储。
$KnowledgePrometheusPort=Get-ServiceProfilePort 'knowledge_prometheus'
# [2026-08-15 22:18:00] 作用：读取 Grafana 端口；理由依据：商业运维看板与第一套第二套端口隔离。
$KnowledgeGrafanaPort=Get-ServiceProfilePort 'knowledge_grafana'
# [2026-08-17 08:45:11] 作用：读取 Knowledge PgBouncer 端口；理由依据：Celery 多进程数据库池必须纳入两套 profile 的唯一端口合同。
$KnowledgePgbouncerPort=Get-ServiceProfilePort 'knowledge_pgbouncer'
$DashboardBackendPort=Get-ServiceProfilePort 'dashboard_backend'
$DashboardWebPort=Get-ServiceProfilePort 'dashboard_web'
$EmbeddingPort=Get-ServiceProfilePort 'embedding_model'
$QwenPort=Get-ServiceProfilePort 'qwen_model'
$GetsoftProfilePort=Get-ServiceProfilePort 'getsoft_api'
$MainSqlServerPort=Get-ServiceProfilePort 'main_sqlserver'
$ExternalSqlServerPort=Get-ServiceProfilePort 'external_sqlserver'
$MigratedPostgresPort=Get-ServiceProfilePort 'migrated_postgres'
$MainQdrantHttpPort=Get-ServiceProfilePort 'main_qdrant_http'
$ExternalQdrantHttpPort=Get-ServiceProfilePort 'external_qdrant_http'
$CloneQdrantHttpPort=Get-ServiceProfilePort 'clone_qdrant_http'
$CloneQdrantGrpcPort=Get-ServiceProfilePort 'clone_qdrant_grpc'
$Neo4jHttpPort=Get-ServiceProfilePort 'neo4j_http'
$Neo4jBoltPort=Get-ServiceProfilePort 'neo4j_bolt'
$PostgresCheckpointPort=Get-ServiceProfilePort 'langgraph_postgres'
$ClonePostgresPort=Get-ServiceProfilePort 'clone_postgres'
# [2026-08-06 11:08:00] 作用：读取当前唯一profile的前端挂载合同；理由依据：端口分套但门户入口未进入profile会继续把第二套页面挂到第一套212地址。
$FrontendMountProfile=$ServicePortProfile.frontend_mounts
# [2026-08-06 11:08:00] 作用：拒绝缺失前端挂载合同的启动；理由依据：不能再靠WebUI默认值或别人前端历史地址猜测实例归属。
if($null-eq$FrontendMountProfile){throw "端口配置 $DeploymentProfile 缺少 frontend_mounts 合同。"}
# [2026-08-06 11:08:00] 作用：读取当前profile的前端协议；理由依据：完整公开URL必须由同一个profile原子生成。
$FrontendScheme=([string]$FrontendMountProfile.scheme).Trim().ToLowerInvariant()
# [2026-08-06 11:08:00] 作用：读取统一挂载网关所属服务；理由依据：资产与知识库必须共用当前profile的asset_web端口而不是另一套历史入口。
$FrontendGatewayService=([string]$FrontendMountProfile.gateway_service).Trim()
# [2026-08-06 11:08:00] 作用：读取资产挂载路径；理由依据：路径与主机端口必须作为同一个profile合同发布。
$FrontendAssetPath=([string]$FrontendMountProfile.asset_path).Trim()
# [2026-08-06 11:08:00] 作用：读取知识库挂载路径；理由依据：只切资产入口而知识库仍走旧地址不算隔离完成。
$FrontendKnowledgePath=([string]$FrontendMountProfile.knowledge_path).Trim()
# [2026-08-06 11:08:00] 作用：锁定当前HTTP统一网关实现；理由依据：现有WebUI没有TLS监听能力，允许配置https会生成不可达的假成功地址。
if($FrontendScheme-ne'http'){throw "端口配置 $DeploymentProfile/frontend_mounts.scheme 必须为 http。"}
# [2026-08-06 11:08:00] 作用：锁定统一挂载网关到当前profile的asset_web；理由依据：启动器真实进程由该端口同时承载resourceType和knowledgeManagement。
if($FrontendGatewayService-ne'asset_web'){throw "端口配置 $DeploymentProfile/frontend_mounts.gateway_service 必须为 asset_web。"}
# [2026-08-06 11:08:00] 作用：校验两个挂载路径格式且禁止相同；理由依据：路径漂移或重叠会把两个业务路由到同一页面。
if($FrontendAssetPath-notmatch'^/[A-Za-z0-9_-]+/$'-or$FrontendKnowledgePath-notmatch'^/[A-Za-z0-9_-]+/$'-or$FrontendAssetPath-eq$FrontendKnowledgePath){throw "端口配置 $DeploymentProfile/frontend_mounts 路径无效。"}
# [2026-08-06 11:08:00] 作用：读取当前profile固定局域网身份；理由依据：第二套前端不能从第一套进程环境或自动网卡顺序取得212。
$FrontendProfileHost=([string]$ServicePortProfile.lan_ip).Trim()
# [2026-08-06 11:08:00] 作用：拒绝缺失或非IPv4的前端主机身份；理由依据：本次两套正式合同均以明确局域网IPv4隔离。
if($FrontendProfileHost-notmatch'^\d{1,3}(?:\.\d{1,3}){3}$'){throw "端口配置 $DeploymentProfile/lan_ip 不能生成前端挂载地址：$FrontendProfileHost"}
# [2026-08-06 11:08:00] 作用：从当前profile服务表取得统一网关端口；理由依据：不得另写18191或28191条件分支。
$FrontendGatewayPort=Get-ServiceProfilePort $FrontendGatewayService
# [2026-08-06 11:08:00] 作用：验证统一网关端口就是本次资产Web端口；理由依据：配置键别名或漂移必须在启动任何服务前失败。
if($FrontendGatewayPort-ne$AssetTypeWebPort){throw "端口配置 $DeploymentProfile 前端网关端口与asset_web不一致。"}
# [2026-08-06 11:08:00] 作用：由当前profile的协议、IP和端口生成唯一公开根；理由依据：第一套固定得到212:18191，第二套固定得到233:28191。
$FrontendPublicBaseUrl="$FrontendScheme`://$FrontendProfileHost`:$FrontendGatewayPort"
# [2026-08-06 11:08:00] 作用：生成当前profile资产挂载URL；理由依据：外部门户应只消费该机器生成的正式值。
$FrontendAssetMountUrl="$FrontendPublicBaseUrl$FrontendAssetPath"
# [2026-08-06 11:08:00] 作用：生成当前profile知识库挂载URL；理由依据：两项入口必须随同一profile原子切换。
$FrontendKnowledgeMountUrl="$FrontendPublicBaseUrl$FrontendKnowledgePath"
# [2026-08-06 11:08:00] 作用：把前端公开根注入本次进程及受控WebUI子进程；理由依据：子进程不得重新打开其它profile或回落默认212地址。
$env:SQL_RAG_FRONTEND_PUBLIC_BASE_URL=$FrontendPublicBaseUrl
$TrustedQdrantPorts=@(
  @($ServicePortProfile.trusted_qdrant_services) |
    ForEach-Object {Get-ServiceProfilePort -Name ([string]$_)}
)
$TrustedRelationalDatabasePorts=@(
  @($ServicePortProfile.trusted_relational_database_services) |
    ForEach-Object {Get-ServiceProfilePort -Name ([string]$_)}
)
$ManagedTrustedRelationalDatabasePorts=@(
  $RuntimeServiceProfiles |
  ForEach-Object {
      $profileValue=$_.Value
      @($profileValue.trusted_relational_database_services) |
        ForEach-Object {
          $portProperty=$profileValue.ports.PSObject.Properties[[string]$_]
          if($null -eq $portProperty){
            throw "端口配置 $($_.Name) 缺少可信关系数据库服务：$_"
          }
          [int]$portProperty.Value
        }
    } |
    Sort-Object -Unique
)
$TrustedQdrantHttpPorts=@(
  $MainQdrantHttpPort,
  $ExternalQdrantHttpPort,
  $CloneQdrantHttpPort
)
$profilePortEnvironment=[ordered]@{
  MSSQL_PORT=$MainSqlServerPort
  QDRANT_PORT=$MainQdrantHttpPort
  LANGGRAPH_POSTGRES_PORT=$PostgresCheckpointPort
  WKT_PRASING_EXTRA_PG_PORT=$ClonePostgresPort
  WKT_PRASING_EXTRA_QDRANT_HTTP_PORT=$CloneQdrantHttpPort
  WKT_PRASING_EXTRA_QDRANT_GRPC_PORT=$CloneQdrantGrpcPort
  EXTERNAL_MSSQL_PORT=$ExternalSqlServerPort
  EXTERNAL_QDRANT_PORT=$ExternalQdrantHttpPort
  NEO4J_HTTP_PORT=$Neo4jHttpPort
  NEO4J_BOLT_PORT=$Neo4jBoltPort
  SQL_RAG_MIGRATED_PG_PORT=$MigratedPostgresPort
  GETSOFT_AI_ERP_PORT=$GetsoftProfilePort
}
$env:SQL_RAG_DEPLOYMENT_PROFILE=$DeploymentProfile
$env:SQL_RAG_TRUSTED_QDRANT_PORTS=($TrustedQdrantPorts -join ',')
$env:SQL_RAG_TRUSTED_RELATIONAL_DATABASE_PORTS=(
  $TrustedRelationalDatabasePorts -join ','
)
foreach($entry in $profilePortEnvironment.GetEnumerator()){
  Set-Item -LiteralPath "Env:$($entry.Key)" -Value ([string]$entry.Value)
}
$env:GETSOFT_AI_ERP_QDRANT_URL="http://127.0.0.1:$ExternalQdrantHttpPort"
Write-Host (
  "服务端口配置已加载：$DeploymentProfile；Web=" +
  (@($ServicePortProfile.public_web_services |
    ForEach-Object {Get-ServiceProfilePort -Name ([string]$_)}) -join ',') +
  '；Qdrant=' +
  ($TrustedQdrantPorts -join ',') +
  '；关系数据库=' +
  ($TrustedRelationalDatabasePorts -join ',')
)
# [2026-07-22 17:08:00] 作用：读取可选 Docker 后端覆盖值；理由依据：Windows Server 不受 Docker Desktop 支持，必须允许同一启动命令改走 WSL2 内的 Linux Docker Engine。
$DockerBackend=[string]$env:SQL_RAG_DOCKER_BACKEND
# [2026-07-22 17:08:01] 作用：未显式配置时识别 Windows Server；理由依据：目标阿里云系统变更后，运维人员不应再额外记忆一套启动命令。
if([string]::IsNullOrWhiteSpace($DockerBackend)){
  # [2026-07-22 17:08:02] 作用：默认保留现有 Windows 11 Docker Desktop 路径；理由依据：不得改变当前已经验收通过的本机启动行为。
  $DockerBackend='desktop'
  # [2026-07-22 17:08:03] 作用：查询宿主操作系统名称；理由依据：仅 Windows Server 自动切换 WSL，普通 Windows 继续使用既有分支。
  try{if(([string](Get-CimInstance Win32_OperatingSystem -ErrorAction Stop).Caption) -match 'Windows Server'){$DockerBackend='wsl'}}catch{}
}
# [2026-07-22 17:08:04] 作用：规范化 Docker 后端名称；理由依据：环境变量大小写或首尾空格不能造成错误分支。
$DockerBackend=$DockerBackend.Trim().ToLowerInvariant()
# [2026-07-22 17:08:05] 作用：限制容器后端为已验证的 desktop 或 wsl；理由依据：未知后端必须在启动前明确阻断。
if($DockerBackend -notin @('desktop','wsl','remote_ssh')){throw "不支持的 SQL_RAG_DOCKER_BACKEND：$DockerBackend"}
# [2026-07-22 17:08:06] 作用：读取 Windows Server 使用的 WSL 发行版名称；理由依据：阿里云机器可按文档安装 Ubuntu，且允许运维重命名发行版。
$DockerWslDistro=[string]$env:SQL_RAG_DOCKER_WSL_DISTRO
# [2026-07-22 17:08:07] 作用：为空时使用文档中的 Ubuntu 默认名；理由依据：保持一键命令无需额外参数。
if([string]::IsNullOrWhiteSpace($DockerWslDistro)){$DockerWslDistro='Ubuntu'}
# [2026-07-22 17:08:08] 作用：把最终后端与发行版写回子进程环境；理由依据：可移植克隆种子工具也要调用同一个 Docker Engine。
$env:SQL_RAG_DOCKER_BACKEND=$DockerBackend
$env:SQL_RAG_DOCKER_WSL_DISTRO=$DockerWslDistro.Trim()
# [2026-08-28 18:31:01] 作用：在只读模式返回本次唯一运行合同；理由依据：部署包发布前必须证明第二套不读取第一套 profile 且33端口和 Docker 身份完整。
if($ValidateServiceProfileOnly){
  # [2026-08-28 18:31:02] 作用：输出可机器比较的 profile 合同及独立 Engine 端点；理由依据：发布门禁必须证明第二套33端口与 Docker 身份不再经过第一套 context 或 Desktop 代理。
  # [2026-08-04 13:43:49] 作用：在无副作用profile结果中输出当前MinIO内部与公开事实源；理由依据：两套发布前必须能机器核对对象存储没有串回旧主机。
  [pscustomobject]@{Result='READY';Mode='validate_service_profile_only';DeploymentProfile=$DeploymentProfile;IndependentServiceProfile=$usesIndependentServiceProfile;ServiceProfilePath=$PortProfilesPath;CloneRefreshMode=$CloneRefreshMode;Minio=[ordered]@{InternalEndpoint=$MinioEndpoint;PublicEndpoint=$MinioPublicEndpoint};Frontend=[ordered]@{ProfileName=$DeploymentProfile;PublicBaseUrl=$FrontendPublicBaseUrl;AssetMountUrl=$FrontendAssetMountUrl;KnowledgeMountUrl=$FrontendKnowledgeMountUrl;GatewayService=$FrontendGatewayService};PortCount=@($ServicePorts.PSObject.Properties).Count;Ports=[ordered]@{Embedding=$EmbeddingPort;Qwen=$QwenPort;BusinessBackend=$BackendPort;BusinessWeb=$WebPort;AssetBackend=$AssetTypeBackendPort;AssetWeb=$AssetTypeWebPort;KnowledgeBackend=$KnowledgeBackendPort;KnowledgeWeb=$KnowledgeWebPort;KnowledgeCacheGateway=$KnowledgeCacheGatewayPort;KnowledgeMinioApi=$KnowledgeMinioApiPort;KnowledgeMinioConsole=$KnowledgeMinioConsolePort;KnowledgeTusd=$KnowledgeTusdPort;KnowledgeRabbitMqAmqp=$KnowledgeRabbitMqAmqpPort;KnowledgeRabbitMqManagement=$KnowledgeRabbitMqManagementPort;KnowledgeFlower=$KnowledgeFlowerPort;KnowledgePrometheus=$KnowledgePrometheusPort;KnowledgeGrafana=$KnowledgeGrafanaPort;KnowledgePgbouncer=$KnowledgePgbouncerPort;DashboardBackend=$DashboardBackendPort;DashboardWeb=$DashboardWebPort;Getsoft=$GetsoftProfilePort;MainSqlServer=$MainSqlServerPort;ExternalSqlServer=$ExternalSqlServerPort;MigratedPostgres=$MigratedPostgresPort;MainQdrant=$MainQdrantHttpPort;ExternalQdrant=$ExternalQdrantHttpPort;CloneQdrantHttp=$CloneQdrantHttpPort;CloneQdrantGrpc=$CloneQdrantGrpcPort;Neo4jHttp=$Neo4jHttpPort;Neo4jBolt=$Neo4jBoltPort;LanggraphPostgres=$PostgresCheckpointPort;ClonePostgres=$ClonePostgresPort};Docker=[ordered]@{Backend=$DockerBackend;EngineEndpoint=$DockerEngineEndpoint;ComposeProject=$ComposeProjectName;ContainerNamePrefix=$ContainerNamePrefix;InternalNetwork=$ProfileInternalDockerNetwork;MigrationComposeProject=$MigrationComposeProjectName};ManagedProfileCount=$RuntimeServiceProfiles.Count}|ConvertTo-Json -Depth 6
  # [2026-08-03 15:48:04] 作用：只读合同输出后立即结束；理由依据：禁止触碰Docker、配置文件、模型、容器或业务端口。
  return
}
$RemoteDockerSettings=$null
if($DockerBackend -eq 'remote_ssh'){
  $RemoteDockerCommon=Join-Path $SqlRag `
    'deployment\alicloud_dual_host\RemoteDocker.Common.ps1'
  if(!(Test-Path -LiteralPath $RemoteDockerCommon -PathType Leaf)){
    throw "远程 Docker 公共脚本不存在：$RemoteDockerCommon"
  }
  . $RemoteDockerCommon
  $env:SQL_RAG_SQL_RAG_ROOT=$SqlRag
  $RemoteDockerSettings=Get-MonFangAiRemoteDockerSettings
}
$Py=Join-Path $RepoRoot '.venv\Scripts\python.exe'
# [2026-07-13 09:24:00] 作用：生成克隆工具绝对路径；理由依据：管理员 PowerShell 从 System32 启动时不能依赖当前工作目录解析 app 相对路径。
$CloneAiErpScript=Join-Path $RepoRoot 'app\SQL_RAG\tools\wkt_prasing_extra\clone_ai_erp.py'
# [2026-07-13 09:24:00] 作用：生成克隆校验工具绝对路径；理由依据：数据库复核必须与克隆步骤具备相同的工作目录无关性。
$VerifyWktCloneScript=Join-Path $RepoRoot 'app\SQL_RAG\tools\wkt_prasing_extra\verify_clone.py'
# [2026-07-20 14:31:00] 作用：定位两个克隆库的可移植种子工具；理由依据：Docker Desktop 命名卷不在项目目录，压缩包迁移后必须先从随包 dump/snapshot 幂等恢复。
$PortableCloneScript=Join-Path $RepoRoot 'app\SQL_RAG\tools\wkt_prasing_extra\portable_clone_data.py'
# [2026-07-20 14:31:00] 作用：定位随项目发布的数据库种子目录；理由依据：另一台电脑只解压整个项目即可获得 PG 与 Qdrant 基线。
$PortableCloneSeedDir=Join-Path $RepoRoot 'app\SQL_RAG\deployment\portable_clone_seed'
# [2026-07-31 15:27:20] 作用：定位第二套服务器核心 SQL Server 与 Qdrant 可移植种子；理由依据：商业 Agent 依赖的 getai 和 sql_rag_qa_chunks_v1 不能在新服务器上保持空库。
$PortableCoreSeedDir=Join-Path $RepoRoot 'app\SQL_RAG\deployment\portable_core_seed'
# [2026-07-31 15:27:20] 作用：定位核心数据幂等恢复工具；理由依据：首次部署恢复与日常启动必须走同一固定一键入口。
$PortableCoreSeedRestoreScript=Join-Path $RepoRoot 'app\SQL_RAG\tools\restore_portable_core_seed.ps1'
# [2026-07-29 16:58:54] 作用：定位固定入口启动前的可移植种子权限恢复器；理由依据：管理员进程生成的种子可能存在但普通 WebUI 启动用户不可读，必须在耗时服务启动前从最近成功基线安全恢复。
$PortableCloneSeedRepairScript=Join-Path $RepoRoot 'app\SQL_RAG\tools\repair_portable_clone_seed.ps1'
# [2026-07-04 10:18:20] 作用：定位知识库服务经过依赖校验的独立 Python 解释器；理由依据：知识库语音解析依赖与主 SQL_RAG 环境隔离，必须使用已安装完整依赖的专用虚拟环境。
$KnowledgePy=Join-Path $RepoRoot 'app\SQL_RAG\Knowledge_management\.venv\Scripts\python.exe'
$EnvFile=Join-Path $SqlRag '.env'
# [2026-07-24 19:40:00] 作用：固定一键启动实际使用的 Compose 文件绝对路径；理由依据：数据库隔离预检必须核对同一份文件，不能受管理员 PowerShell 当前目录影响。
$ComposeFile=Join-Path $SqlRag 'docker-compose.yml'
if(!(Test-Path -LiteralPath $ComposeFile -PathType Leaf)){throw "Docker Compose 文件不存在：$ComposeFile"}
$LogDir=Join-Path $RepoRoot 'logs\sql_rag_runtime'
# [2026-07-23 10:28:57] 作用：定位对方 ERP AI 服务的稳定部署适配器；理由依据：只接入标准 main 合同，不把对方业务模块复制或硬编码进本启动器。
$GetsoftAdapterScript=Join-Path $SqlRag 'deployment\external_services\start-getsoft-ai-erp.ps1'
# [2026-07-23 10:28:57] 作用：定位对方服务的集中配置；理由依据：目录、端口和健康合同变化只维护配置文件，不频繁改一键启动命令。
$GetsoftConfigPath=Join-Path $SqlRag 'deployment\external_services\getsoft-ai-erp.json'
# [2026-07-23 10:28:57] 作用：在启动任何进程前验证适配器资产完整；理由依据：缺少隔离层时不能退回共享环境或临时命令。
if(!(Test-Path -LiteralPath $GetsoftAdapterScript)){throw "对方 ERP AI 服务适配器不存在：$GetsoftAdapterScript"}
if(!(Test-Path -LiteralPath $GetsoftConfigPath)){throw "对方 ERP AI 服务配置不存在：$GetsoftConfigPath"}
# [2026-07-25 13:27:00] 作用：与 Getsoft 适配器使用同一个机器运行时根目录；理由依据：适配器已经把 startup-result.json 移到源码包外，父启动器不能继续从旧 runtime_data 路径读取。
$GetsoftRuntimeRoot=[string]$env:SQL_RAG_EXTERNAL_RUNTIME_ROOT
if([string]::IsNullOrWhiteSpace($GetsoftRuntimeRoot)){
  $OwnerPackageRoot=Split-Path -Parent $RepoRoot
  $ProjectContainer=Split-Path -Parent $OwnerPackageRoot
  $GetsoftRuntimeRoot=Join-Path $ProjectContainer `
    '.sql_rag_runtime\external_services\getsoft_ai_erp'
}
$GetsoftRuntimeRoot=[System.IO.Path]::GetFullPath($GetsoftRuntimeRoot)
# [2026-07-31 15:43:10] 作用：为当前 local/aliyun profile 建立独立 Getsoft 状态目录；理由依据：两套服务同时运行时不能共用 service-state.json、startup-result.json 和日志。
$GetsoftInstanceRuntimeRoot=Join-Path $GetsoftRuntimeRoot $DeploymentProfile
# [2026-07-31 15:43:10] 作用：把 profile 独立状态目录传给 Getsoft 适配器；理由依据：适配器只能清理本 profile 精确记录的 PID 和端口。
$env:SQL_RAG_EXTERNAL_INSTANCE_RUNTIME_ROOT=$GetsoftInstanceRuntimeRoot
# [2026-07-31 15:43:10] 作用：从当前 profile 状态目录读取启动结果；理由依据：第二套启动不得覆盖第一套仍在线服务的验收记录。
$GetsoftStartupResultPath=Join-Path $GetsoftInstanceRuntimeRoot 'startup-result.json'
# [2026-07-23 10:28:57] 作用：读取对方服务部署合同供最终健康检查复用；理由依据：父启动器与适配器必须使用同一端口和路由定义。
$GetsoftConfig=Get-Content -LiteralPath $GetsoftConfigPath -Raw -Encoding UTF8 | ConvertFrom-Json
# [2026-07-23 10:28:57] 作用：允许同机其他开发者通过环境变量调整对方服务端口；理由依据：多个独立 ps1 可以并存而不争抢固定端口。
$GetsoftPort=[int]$GetsoftConfig.port
if(![string]::IsNullOrWhiteSpace([string]$env:GETSOFT_AI_ERP_PORT)){$GetsoftPort=[int]$env:GETSOFT_AI_ERP_PORT}
# [2026-07-29 13:16:00] 作用：保留回环地址只供模型、数据库和兼容诊断使用；理由依据：数据层继续隔离，业务层不再借回环端口增加转发网关。
$InternalHost='127.0.0.1'
# [2026-08-06 11:08:00] 作用：把自动探测的优先LAN地址固定为当前profile身份；理由依据：共享启动器不能继续把第一套212作为第二套服务器的默认候选。
$PreferredPublicHost=$FrontendProfileHost
# [2026-07-07 18:32:41] 作用：读取可选公开主机覆盖值；理由依据：后续换服务器时可通过 SQL_RAG_PUBLIC_HOST 调整，不需要再次修改脚本源码。
$PublicHost=[string]$env:SQL_RAG_PUBLIC_HOST
# [2026-07-07 18:32:41] 作用：在未显式指定公开主机时自动识别本机 LAN 地址；理由依据：优先使用 172.18.1.212，同时保留迁移到其它机器后的可运行性。
if([string]::IsNullOrWhiteSpace($PublicHost)){
  # [2026-07-07 18:32:41] 作用：清空公开主机变量等待自动探测；理由依据：避免空白环境变量被误当成有效访问地址。
  $PublicHost=$null
  # [2026-07-07 18:32:41] 作用：捕获网卡探测异常；理由依据：部分精简 Windows 环境可能缺少完整网络命令，不能因此阻断本机启动。
  try{
    # [2026-07-07 18:32:41] 作用：优先查找截图里的固定 IPv4 地址；理由依据：用户要求别人前端直接挂载 172.18.1.212。
    $preferredIp=Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue | Where-Object {$_.IPAddress -eq $PreferredPublicHost} | Select-Object -First 1
    # [2026-07-07 18:32:41] 作用：命中固定 IPv4 时直接使用；理由依据：避免多网卡环境选择到 Docker、虚拟网卡或其它内网地址。
    if($preferredIp){$PublicHost=$PreferredPublicHost}
    # [2026-07-07 18:32:41] 作用：固定 IP 未命中时选择第一个可用非回环 IPv4；理由依据：让脚本在其它机器也能输出可访问地址。
    if([string]::IsNullOrWhiteSpace($PublicHost)){
      # [2026-07-07 18:32:41] 作用：过滤掉 127 与 APIPA 地址后排序取候选；理由依据：这些地址不能作为别人前端的稳定挂载入口。
      $fallbackIp=Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue | Where-Object {$_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*'} | Sort-Object InterfaceIndex | Select-Object -First 1
      # [2026-07-07 18:32:41] 作用：保存自动探测到的候选 IP；理由依据：没有固定 LAN IP 时仍需提供可访问入口。
      if($fallbackIp){$PublicHost=$fallbackIp.IPAddress}
    }
  }catch{}
}
# [2026-07-07 18:32:41] 作用：公开主机最终兜底到本机回环地址；理由依据：网络探测失败时仍允许本机调试启动。
if([string]::IsNullOrWhiteSpace($PublicHost)){$PublicHost=$InternalHost}
# [2026-07-07 18:32:41] 作用：规范化公开主机字符串；理由依据：避免环境变量前后空格导致 URL 拼接错误。
$PublicHost=$PublicHost.Trim()
# [2026-08-06 11:08:00] 作用：验证进程公开主机与当前profile身份完全一致；理由依据：环境残留或手工覆盖到另一套IP时必须在启动服务前失败关闭。
if($PublicHost-ne$FrontendProfileHost){throw "前端profile主机串线：profile=$DeploymentProfile；expected=$FrontendProfileHost；actual=$PublicHost"}
# [2026-07-29 13:16:00] 作用：把全部业务 API 与页面进程统一绑定到选定的可信 LAN 地址；理由依据：直连进程可以消除 18191 和 18520 二次网关对长响应的截断。
$BusinessListenHost=$PublicHost
# [2026-07-29 13:16:00] 作用：保留旧 WebUI 监听变量作为业务直连别名；理由依据：现有启动参数无需重复分叉且端口归属仍由同一 LAN 地址唯一确定。
$WebListenHost=$BusinessListenHost
# [2026-07-29 16:39:49] 作用：让 Knowledge 单个业务进程直接接受全部受防火墙约束的局域网连接；理由依据：浏览器上传与最终 JSON 必须始终停留在公开18320业务端口，禁止307回环第二跳。
$KnowledgeBackendListenHost='0.0.0.0'
# [2026-07-07 18:32:41] 作用：把最终公开主机写回当前进程环境；理由依据：子进程或后续诊断脚本可复用同一个对外挂载主机。
$env:SQL_RAG_PUBLIC_HOST=$PublicHost
# [2026-07-10 16:02:00] 作用：读取外部 PostgreSQL 主机覆盖值；理由依据：krauss 在本机可能优先解析到 IPv6 链路地址，导致 Knowledge 后端和外部同步连接失败。
$ExternalPgHost=[string]$env:SQL_RAG_EXTERNAL_PG_HOST
# [2026-07-22 17:08:21] 作用：Windows Server 迁移机默认连接随包恢复到本机 5432 的 krauss；理由依据：新阿里云服务器不在源电脑局域网，不能继续依赖旧地址 172.18.1.166。
if([string]::IsNullOrWhiteSpace($ExternalPgHost) -and $DockerBackend -in @('wsl','remote_ssh')){$ExternalPgHost='127.0.0.1'}
# [2026-07-10 16:02:00] 作用：非迁移环境未显式覆盖时保留已验证可达的 IPv4；理由依据：当前 Windows 11 商业链路行为不得被服务器部署适配改变。
if([string]::IsNullOrWhiteSpace($ExternalPgHost)){$ExternalPgHost='172.18.1.166'}
# [2026-07-10 16:02:00] 作用：规范化外部 PostgreSQL 主机字符串；理由依据：避免环境变量前后空格导致 psycopg/psycopg2 连接串不可用。
$ExternalPgHost=$ExternalPgHost.Trim()
# [2026-07-10 16:02:00] 作用：把外部 PostgreSQL 主机写回当前进程环境；理由依据：业务脑外部同步、资产类型服务和知识库服务都应继承同一个稳定主机。
$env:SQL_RAG_EXTERNAL_PG_HOST=$ExternalPgHost
# [2026-07-24 19:40:00] 作用：读取全部 Docker 数据库服务共享的宿主机监听地址；理由依据：数据库只允许本机业务进程访问，禁止随公网 WebUI 一起暴露。
$DatabaseBind=[string]$env:SQL_RAG_DATABASE_BIND
# [2026-07-24 19:40:00] 作用：未配置时强制采用 IPv4 回环地址；理由依据：Compose 默认值和一键启动运行时必须执行同一条最小暴露契约。
if([string]::IsNullOrWhiteSpace($DatabaseBind)){$DatabaseBind='127.0.0.1'}
# [2026-07-24 19:40:00] 作用：去除部署环境变量首尾空格；理由依据：避免看似回环但实际生成无效 Docker 端口映射。
$DatabaseBind=$DatabaseBind.Trim()
# [2026-07-24 19:40:00] 作用：拒绝 0.0.0.0、公网 IP、内网 IP 和空 HostIp；理由依据：用户明确要求数据库只供同机内部业务链路使用，错误配置必须失败关闭。
if($DatabaseBind -ne '127.0.0.1'){throw "安全阻断：SQL_RAG_DATABASE_BIND 只允许 127.0.0.1，当前值=$DatabaseBind"}
# [2026-07-24 19:40:00] 作用：把已校验的数据库监听地址传递给 Docker Compose；理由依据：所有数据库容器必须共享同一条不可漂移的回环绑定。
$env:SQL_RAG_DATABASE_BIND=$DatabaseBind
$RuntimeDatabaseBind=if($DockerBackend -eq 'remote_ssh'){
  [string]$RemoteDockerSettings.Host
}else{
  $DatabaseBind
}
# [2026-07-25 13:05:01] 作用：判断一个 IPv4 是否属于回环或 RFC1918 私网；理由依据：一键启动自动选择的 Qdrant 入口绝不能漂移到公网网卡。
function Test-TrustedPrivateIPv4{
  param([string]$Address)
  $parsed=$null
  if(
    -not [System.Net.IPAddress]::TryParse($Address,[ref]$parsed) -or
    $parsed.AddressFamily -ne
      [System.Net.Sockets.AddressFamily]::InterNetwork
  ){return $false}
  $bytes=$parsed.GetAddressBytes()
  return (
    $bytes[0] -eq 127 -or
    $bytes[0] -eq 10 -or
    ($bytes[0] -eq 172 -and $bytes[1] -ge 16 -and $bytes[1] -le 31) -or
    ($bytes[0] -eq 192 -and $bytes[1] -eq 168)
  )
}
$TrustedQdrantConnectAddress=[string]$env:SQL_RAG_TRUSTED_QDRANT_CONNECT_ADDRESS
if([string]::IsNullOrWhiteSpace($TrustedQdrantConnectAddress)){
  $TrustedQdrantConnectAddress='127.0.0.1'
}
$TrustedQdrantConnectAddress=$TrustedQdrantConnectAddress.Trim()
if(!(Test-TrustedPrivateIPv4 -Address $TrustedQdrantConnectAddress)){
  throw "可信 Qdrant 代理目标不是回环或 RFC1918 私网 IPv4：$TrustedQdrantConnectAddress"
}
if(
  $DockerBackend -eq 'remote_ssh' -and
  $TrustedQdrantConnectAddress -ne [string]$RemoteDockerSettings.Host
){
  throw (
    '远程 Docker 的 Qdrant 代理目标必须等于 Linux 数据机私网 IP：' +
    "$TrustedQdrantConnectAddress != $($RemoteDockerSettings.Host)"
  )
}
# [2026-07-25 13:05:02] 作用：从实际网卡 IPv4 和前缀长度计算可信来源 CIDR；理由依据：172.18.1.212/24 应自动得到 172.18.1.0/24，避免用户再次手工输入。
function ConvertTo-IPv4NetworkCidr{
  param(
    [string]$Address,
    [int]$PrefixLength
  )
  if($PrefixLength -lt 8 -or $PrefixLength -gt 32){
    throw "可信 Qdrant 网卡前缀无效：$Address/$PrefixLength"
  }
  $bytes=([System.Net.IPAddress]::Parse($Address)).GetAddressBytes()
  $remaining=$PrefixLength
  $networkBytes=@()
  for($index=0;$index -lt 4;$index++){
    $bits=[Math]::Min(8,[Math]::Max(0,$remaining))
    $mask=if($bits -eq 0){0}else{256-(1 -shl (8-$bits))}
    $networkBytes+=([int]$bytes[$index] -band $mask)
    $remaining-=8
  }
  return (($networkBytes -join '.') + '/' + $PrefixLength)
}
# [2026-07-25 13:18:01] 作用：把前缀 CIDR 转为 Windows 防火墙回读使用的点分掩码形式；理由依据：`172.18.1.0/24` 会被系统规范化为 `172.18.1.0/255.255.255.0`。
function ConvertTo-FirewallRemoteNotation{
  param([string]$Value)
  $parts=$Value.Split('/')
  if($parts.Count -ne 2){return $Value}
  $prefix=0
  if(-not [int]::TryParse($parts[1],[ref]$prefix)){return $Value}
  $maskBytes=@()
  $remaining=$prefix
  for($index=0;$index -lt 4;$index++){
    $bits=[Math]::Min(8,[Math]::Max(0,$remaining))
    $maskBytes+=if($bits -eq 0){0}else{256-(1 -shl (8-$bits))}
    $remaining-=8
  }
  return ($parts[0] + '/' + ($maskBytes -join '.'))
}
# [2026-07-25 13:05:03] 作用：定位可信 Qdrant 配置工具；理由依据：一键启动必须同时完成 Windows 端口代理和来源受限防火墙规则。
$TrustedQdrantAccessScript=Join-Path $SqlRag `
  'deployment\alicloud_windows_server_migration\Set-MonFangAiTrustedQdrantAccess.ps1'
if(!(Test-Path -LiteralPath $TrustedQdrantAccessScript -PathType Leaf)){
  throw "可信 Qdrant 配置工具不存在：$TrustedQdrantAccessScript"
}
$TrustedQdrantListenAddress=[string]$env:SQL_RAG_TRUSTED_QDRANT_LISTEN_ADDRESS
$trustedAddressRow=$null
if(-not [string]::IsNullOrWhiteSpace($TrustedQdrantListenAddress)){
  $TrustedQdrantListenAddress=$TrustedQdrantListenAddress.Trim()
  $trustedAddressRow=Get-NetIPAddress `
    -AddressFamily IPv4 `
    -IPAddress $TrustedQdrantListenAddress `
    -ErrorAction SilentlyContinue |
    Where-Object {
      $_.AddressState -eq 'Preferred' -and
      -not $_.SkipAsSource
    } |
    Select-Object -First 1
}
if($null -eq $trustedAddressRow){
  $privateAddressRows=@(
    Get-NetIPAddress -AddressFamily IPv4 -ErrorAction Stop |
      Where-Object {
        $_.AddressState -eq 'Preferred' -and
        -not $_.SkipAsSource -and
        (Test-TrustedPrivateIPv4 -Address $_.IPAddress) -and
        $_.IPAddress -notlike '127.*'
      }
  )
  $trustedAddressRow=$privateAddressRows |
    Where-Object {$_.IPAddress -eq $PublicHost} |
    Select-Object -First 1
  if($null -eq $trustedAddressRow){
    $defaultInterfaceIndexes=@(
      Get-NetRoute `
        -AddressFamily IPv4 `
        -DestinationPrefix '0.0.0.0/0' `
        -ErrorAction SilentlyContinue |
        Sort-Object RouteMetric,InterfaceMetric |
        Select-Object -ExpandProperty InterfaceIndex -Unique
    )
    foreach($interfaceIndex in $defaultInterfaceIndexes){
      $trustedAddressRow=$privateAddressRows |
        Where-Object {$_.InterfaceIndex -eq $interfaceIndex} |
        Select-Object -First 1
      if($null -ne $trustedAddressRow){break}
    }
  }
  if($null -eq $trustedAddressRow){
    $trustedAddressRow=$privateAddressRows |
      Sort-Object InterfaceIndex |
      Select-Object -First 1
  }
  if($null -eq $trustedAddressRow){
    throw '未找到可用于可信 Qdrant 访问的 RFC1918 私网 IPv4。'
  }
  $TrustedQdrantListenAddress=[string]$trustedAddressRow.IPAddress
}
if(-not (Test-TrustedPrivateIPv4 -Address $TrustedQdrantListenAddress)){
  throw "可信 Qdrant 监听地址不是私网 IPv4：$TrustedQdrantListenAddress"
}
$TrustedQdrantRemoteAddresses=@(
  ([string]$env:SQL_RAG_TRUSTED_QDRANT_REMOTE_ADDRESS) -split ',' |
    ForEach-Object {$_.Trim()} |
    Where-Object {-not [string]::IsNullOrWhiteSpace($_)}
)
if($TrustedQdrantRemoteAddresses.Count -eq 0){
  if($null -eq $trustedAddressRow){
    $trustedAddressRow=Get-NetIPAddress `
      -AddressFamily IPv4 `
      -IPAddress $TrustedQdrantListenAddress `
      -ErrorAction Stop |
      Select-Object -First 1
  }
  $TrustedQdrantRemoteAddresses=@(
    ConvertTo-IPv4NetworkCidr `
      -Address $TrustedQdrantListenAddress `
      -PrefixLength ([int]$trustedAddressRow.PrefixLength)
  )
}
# [2026-07-28] 作用：关系数据库默认复用已经验证过的可信私网监听、目标和来源；理由依据：两类数据服务必须共享同一条最小暴露边界，同时保留独立环境变量供双机部署覆盖。
$TrustedRelationalDatabaseListenAddress=(
  [string]$env:SQL_RAG_TRUSTED_RELATIONAL_DATABASE_LISTEN_ADDRESS
).Trim()
if([string]::IsNullOrWhiteSpace($TrustedRelationalDatabaseListenAddress)){
  $TrustedRelationalDatabaseListenAddress=$TrustedQdrantListenAddress
}
$TrustedRelationalDatabaseConnectAddress=(
  [string]$env:SQL_RAG_TRUSTED_RELATIONAL_DATABASE_CONNECT_ADDRESS
).Trim()
if([string]::IsNullOrWhiteSpace($TrustedRelationalDatabaseConnectAddress)){
  $TrustedRelationalDatabaseConnectAddress=$TrustedQdrantConnectAddress
}
$TrustedRelationalDatabaseRemoteAddresses=@(
  ([string]$env:SQL_RAG_TRUSTED_RELATIONAL_DATABASE_REMOTE_ADDRESS) -split ',' |
    ForEach-Object {$_.Trim()} |
    Where-Object {-not [string]::IsNullOrWhiteSpace($_)}
)
if($TrustedRelationalDatabaseRemoteAddresses.Count -eq 0){
  $TrustedRelationalDatabaseRemoteAddresses=@($TrustedQdrantRemoteAddresses)
}
if(!(Test-TrustedPrivateIPv4 -Address $TrustedRelationalDatabaseListenAddress)){
  throw "可信关系数据库监听地址不是私网 IPv4：$TrustedRelationalDatabaseListenAddress"
}
if(!(Test-TrustedPrivateIPv4 -Address $TrustedRelationalDatabaseConnectAddress)){
  throw "可信关系数据库代理目标不是回环或 RFC1918 私网 IPv4：$TrustedRelationalDatabaseConnectAddress"
}
if(
  $DockerBackend -eq 'remote_ssh' -and
  $TrustedRelationalDatabaseConnectAddress -ne [string]$RemoteDockerSettings.Host
){
  throw (
    '远程 Docker 的关系数据库代理目标必须等于 Linux 数据机私网 IP：' +
    "$TrustedRelationalDatabaseConnectAddress != $($RemoteDockerSettings.Host)"
  )
}
# [2026-07-29 13:16:00] 作用：汇总全部业务 API 与页面端口的直连防火墙合同；理由依据：业务进程直接绑定可信 LAN，但仍只允许同网段客户端访问。
$TrustedBusinessListenAddress=$TrustedQdrantListenAddress
# [2026-07-29 13:16:00] 作用：复用可信数据入口推导出的局域网来源范围；理由依据：业务层开放范围不得比用户确认的 172.18.1.0/24 更宽。
$TrustedBusinessRemoteAddresses=@($TrustedQdrantRemoteAddresses)
# [2026-07-29 13:16:00] 作用：列出全部业务 API 与页面固定端口；理由依据：一次配置和读回可阻止遗漏、串服务或单独依赖临时手工防火墙。
$TrustedBusinessListenPorts=@(
  # [2026-07-29 13:16:00] 作用：纳入主业务脑 API；理由依据：别人或页面需要直接访问固定 18182/28182。
  [int]$BackendPort,
  # [2026-07-29 13:16:00] 作用：纳入主业务脑页面；理由依据：页面端口属于业务直连合同。
  [int]$WebPort,
  # [2026-07-29 13:16:00] 作用：纳入资产类型 API；理由依据：资产业务不能继续只绑定回环。
  [int]$AssetTypeBackendPort,
  # [2026-07-29 13:16:00] 作用：纳入资产与知识统一页面；理由依据：18191 现在由 Python 页面进程直接持有。
  [int]$AssetTypeWebPort,
  # [2026-07-29 13:16:00] 作用：纳入知识解析 API；理由依据：真实 M4A 必须从浏览器直达 18320/28320。
  [int]$KnowledgeBackendPort,
  # [2026-07-29 13:16:00] 作用：纳入知识独立页面；理由依据：18321/28321 继续作为兼容入口。
  [int]$KnowledgeWebPort,
  # [2026-07-29 13:16:00] 作用：纳入客户风险看板 API；理由依据：看板后端同属局域网业务层。
  [int]$DashboardBackendPort,
  # [2026-07-29 13:16:00] 作用：纳入客户风险看板页面；理由依据：页面和后端共享直连边界。
  [int]$DashboardWebPort,
  # [2026-07-29 13:16:00] 作用：纳入 Getsoft ERP AI API；理由依据：18520 已证明必须由 Selector ASGI 直接监听。
  [int]$GetsoftPort
)
# [2026-07-29 14:55:40] 作用：列出旧 Getsoft 独立防火墙规则的精确名称；理由依据：18520 已并入统一业务直连合同，重复旧规则会让端口边界与运维读回产生歧义。
$ObsoleteBusinessFirewallRuleNames=@(
  # [2026-07-29 14:55:40] 作用：标记昨天 Node/portproxy 拓扑遗留的 18520 规则；理由依据：当前唯一有效规则必须是 MonFangAI Business TCP 18520 Trusted。
  'MonFangAI Getsoft API TCP 18520 Trusted'
)
# [2026-07-28] 作用：逐项读回一组可信数据代理和防火墙规则；理由依据：端口存在不等于来源、目标地址和规则仍符合安全合同。
function Test-TrustedPortConfiguration{
  param(
    [int[]]$Ports,
    [int[]]$ConnectPorts=@(),
    [string]$ListenAddress,
    [string]$ConnectAddress,
    [string[]]$RemoteAddresses,
    [string]$RulePrefix,
    [switch]$DirectListener
  )
  try{
    if($ConnectPorts.Count -eq 0){$ConnectPorts=@($Ports)}
    if($ConnectPorts.Count -ne $Ports.Count){return $false}
    $expectedPortMappings=@(
      for($mappingIndex=0;$mappingIndex -lt $Ports.Count;$mappingIndex++){
        [pscustomobject]@{
          ListenPort=[int]$Ports[$mappingIndex]
          ConnectPort=[int]$ConnectPorts[$mappingIndex]
        }
      }
    )
    $proxyRows=@(
      netsh.exe interface portproxy show v4tov4 |
        ForEach-Object {
          $columns=@(
            ([string]$_).Trim() -split '\s+' |
              Where-Object {$_ -ne ''}
          )
          $listenPortValue=0
          $connectPortValue=0
          if(
            $columns.Count -eq 4 -and
            [int]::TryParse($columns[1],[ref]$listenPortValue) -and
            [int]::TryParse($columns[3],[ref]$connectPortValue)
          ){
            [pscustomobject]@{
              ListenAddress=$columns[0]
              ListenPort=$listenPortValue
              ConnectAddress=$columns[2]
              ConnectPort=$connectPortValue
            }
          }
        }
    )
    $expectedRemoteKeys=@(
      $RemoteAddresses |
        ForEach-Object {
          ConvertTo-FirewallRemoteNotation -Value $_
        } |
        Sort-Object -Unique
    )
    foreach($expectedPortMapping in $expectedPortMappings){
      $trustedPort=[int]$expectedPortMapping.ListenPort
      $matchingProxyRows=@(
        $proxyRows |
          Where-Object {
            if(
              $_.ListenAddress -ne $ListenAddress -or
              $_.ListenPort -ne $trustedPort
            ){return $false}
            if($DirectListener){return $true}
            return (
              $_.ConnectAddress -eq $ConnectAddress -and
              $_.ConnectPort -eq [int]$expectedPortMapping.ConnectPort
            )
          }
      )
      if(
        ($DirectListener -and $matchingProxyRows.Count -ne 0) -or
        (-not $DirectListener -and $matchingProxyRows.Count -ne 1)
      ){return $false}
      # [2026-08-04 18:44:45] 作用：对非直连数据入口同时读取 Windows 真实 TCP 监听；理由依据：电脑重启后已出现 netsh 规则完整但 172.18.1.212:6333-6336 无监听，只验证配置表会在全栈中途才失败。
      $activeProxyListeners=@(
        # [2026-08-04 18:44:45] 作用：按当前 profile 的精确私网地址和端口筛选监听；理由依据：回环容器端口就绪不能代表 LAN portproxy 已生效。
        Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
          # [2026-08-05 08:51:18] 作用：以单行精确条件拒绝把其他地址或相同端口的监听当成本入口；理由依据：两套服务端口和网络身份必须保持独立，且新增可执行行必须逐行满足注释合同。
          Where-Object {$_.LocalAddress-eq$ListenAddress-and[int]$_.LocalPort-eq$trustedPort}
      )
      # [2026-08-04 18:44:45] 作用：在真实代理监听缺失时立即把配置标记为未就绪；理由依据：父启动器将在 Docker 和业务服务前进入受控 UAC 子进程精确重建规则。
      if(-not$DirectListener-and$activeProxyListeners.Count-ne1){return $false}
      $trustedRule=Get-NetFirewallRule `
        -DisplayName "$RulePrefix TCP $trustedPort Trusted" `
        -ErrorAction Stop
      $trustedPortFilter=$trustedRule | Get-NetFirewallPortFilter
      $trustedAddressFilter=$trustedRule | Get-NetFirewallAddressFilter
      $actualRemoteKeys=@(
        $trustedAddressFilter.RemoteAddress |
          ForEach-Object {
            ConvertTo-FirewallRemoteNotation -Value $_
          } |
          Sort-Object -Unique
      )
      if(
        [string]$trustedRule.Enabled -ne 'True' -or
        [string]$trustedRule.Direction -ne 'Inbound' -or
        [string]$trustedRule.Action -ne 'Allow' -or
        @('TCP','6') -notcontains [string]$trustedPortFilter.Protocol -or
        [string]$trustedPortFilter.LocalPort -ne [string]$trustedPort -or
        @($trustedAddressFilter.LocalAddress) -notcontains
          $ListenAddress -or
        ($actualRemoteKeys -join ',') -ne ($expectedRemoteKeys -join ',')
      ){return $false}
    }
    return $true
  }catch{
    return $false
  }
}
function Test-TrustedQdrantConfiguration{
  return [bool](
    Test-TrustedPortConfiguration `
      -Ports $TrustedQdrantPorts `
      -ListenAddress $TrustedQdrantListenAddress `
      -ConnectAddress $TrustedQdrantConnectAddress `
      -RemoteAddresses $TrustedQdrantRemoteAddresses `
      -RulePrefix 'MonFangAI Qdrant'
  )
}
function Test-TrustedRelationalDatabaseConfiguration{
  return [bool](
    Test-TrustedPortConfiguration `
      -Ports $TrustedRelationalDatabasePorts `
      -ListenAddress $TrustedRelationalDatabaseListenAddress `
      -ConnectAddress $TrustedRelationalDatabaseConnectAddress `
      -RemoteAddresses $TrustedRelationalDatabaseRemoteAddresses `
      -RulePrefix 'MonFangAI RelationalDB'
  )
}
# [2026-07-29 13:16:00] 作用：验证全部业务直连端口没有残留 portproxy 且防火墙范围精确；理由依据：业务层只能由真实业务进程持有。
function Test-TrustedBusinessConfiguration{
  return [bool](
    Test-TrustedPortConfiguration `
      -Ports $TrustedBusinessListenPorts `
      -ListenAddress $TrustedBusinessListenAddress `
      -ConnectAddress $InternalHost `
      -RemoteAddresses $TrustedBusinessRemoteAddresses `
      -RulePrefix 'MonFangAI Business' `
      -DirectListener
  )
}
# [2026-07-29 15:01:20] 作用：只用当前唯一有效的业务规则判断普通重启是否需要 UAC；理由依据：已读回旧 18520 规则与新规则的地址、来源、协议和动作完全相同，重复名称不应阻塞服务重启。
function Test-TrustedDataConfiguration{
  return (
    (Test-TrustedQdrantConfiguration) -and
    (Test-TrustedRelationalDatabaseConfiguration) -and
    (Test-TrustedBusinessConfiguration)
  )
}
$trustedDataConfigurationReady=$false
if(-not $isAdministrator){
  $trustedDataConfigurationReady=Test-TrustedDataConfiguration
  if(-not $trustedDataConfigurationReady){
    [void](Invoke-ElevatedLauncher)
    $trustedDataConfigurationReady=Test-TrustedDataConfiguration
    if(-not $trustedDataConfigurationReady){
      throw '管理员子进程返回后可信 Qdrant 与关系数据库端口组仍未就绪。'
    }
  }
}
if($isAdministrator){
  # [2026-07-29 15:01:20] 作用：仅在系统数据合同本来就需要提权修复时顺手清除旧同范围规则；理由依据：不为一个安全边界完全相同的重复显示名单独打断普通一键重启。
  # [2026-07-29 14:55:40] 作用：在提升后的固定入口中清除精确识别的旧 Getsoft 防火墙规则；理由依据：规则删除需要管理员权限，且不能留给用户手工执行第二条命令。
  foreach($obsoleteRuleName in $ObsoleteBusinessFirewallRuleNames){
    # [2026-07-29 14:55:40] 作用：只在旧规则真实存在时删除；理由依据：重复一键启动必须幂等且不产生无意义错误。
    if(Get-NetFirewallRule -DisplayName $obsoleteRuleName -ErrorAction SilentlyContinue){
      # [2026-07-29 14:55:40] 作用：按精确名称移除旧 18520 开放边界；理由依据：当前统一业务规则已覆盖同一可信来源和端口。
      Remove-NetFirewallRule -DisplayName $obsoleteRuleName -ErrorAction Stop
    }
  }
  # [2026-07-31 15:08:31] 作用：用参数表完整传递当前 profile 的 Qdrant 安全入口配置；理由依据：续行命令中夹入注释会截断 ManagedPort 和 RemoteAddress，导致全新服务器首次启动误判为未配置可信来源。
  $trustedQdrantConfigurationParameters=@{
    # [2026-07-31 15:08:31] 作用：限定 Qdrant 只监听当前 profile 配置的局域网地址；理由依据：两套部署必须使用各自固定地址边界。
    ListenAddress=$TrustedQdrantListenAddress
    # [2026-07-31 15:08:31] 作用：把 Qdrant 安全入口回送到当前 profile 的内部数据地址；理由依据：数据容器不能直接暴露公网。
    ConnectAddress=$TrustedQdrantConnectAddress
    # [2026-07-31 15:08:31] 作用：声明当前 profile 需要开放的 Qdrant 端口；理由依据：第一套与第二套端口集合必须互不覆盖。
    Port=$TrustedQdrantPorts
    # [2026-07-31 15:08:31] 作用：仅管理当前 profile 的 Qdrant 代理和防火墙端口；理由依据：启动任一套服务不得删除另一套可信入口。
    ManagedPort=$TrustedQdrantPorts
    # [2026-07-31 15:08:31] 作用：只允许 profile 指定的可信私网来源访问；理由依据：保留同局域网可用性同时收紧数据层边界。
    RemoteAddress=$TrustedQdrantRemoteAddresses
  }
  # [2026-07-31 15:08:31] 作用：执行参数完整的 Qdrant 安全入口配置并收集结构化结果；理由依据：新服务器第一次一键启动必须与重复启动同样可靠。
  $trustedQdrantConfigurationOutput=@(& $TrustedQdrantAccessScript @trustedQdrantConfigurationParameters)
  # [2026-07-31 15:08:32] 作用：用参数表完整传递当前 profile 的关系数据库安全入口配置；理由依据：避免续行注释截断可信来源和受管端口。
  $trustedRelationalDatabaseConfigurationParameters=@{
    # [2026-07-31 15:08:32] 作用：限定关系数据库代理监听当前 profile 的局域网地址；理由依据：两套数据库入口必须独立。
    ListenAddress=$TrustedRelationalDatabaseListenAddress
    # [2026-07-31 15:08:32] 作用：把关系数据库代理回送到当前 profile 的内部地址；理由依据：数据库容器继续保持回环监听。
    ConnectAddress=$TrustedRelationalDatabaseConnectAddress
    # [2026-07-31 15:08:32] 作用：声明当前 profile 的关系数据库端口集合；理由依据：避免第一套和第二套端口串用。
    Port=$TrustedRelationalDatabasePorts
    # [2026-07-31 15:08:32] 作用：仅管理当前 profile 的关系数据库规则；理由依据：任一套启动不能清理另一套规则。
    ManagedPort=$TrustedRelationalDatabasePorts
    # [2026-07-31 15:08:32] 作用：限定关系数据库可信私网来源；理由依据：数据层只通过安全回环对局域网授权。
    RemoteAddress=$TrustedRelationalDatabaseRemoteAddresses
    # [2026-07-31 15:08:32] 作用：为关系数据库使用独立防火墙规则前缀；理由依据：便于与 Qdrant 和业务端口分离审计。
    RulePrefix='MonFangAI RelationalDB'
    # [2026-07-31 15:08:32] 作用：设置关系数据库配置结果的资源名称；理由依据：启动错误必须准确指向对应数据服务。
    ResourceName='关系数据库'
  }
  # [2026-07-31 15:08:32] 作用：执行参数完整的关系数据库安全入口配置并收集结构化结果；理由依据：保证全新服务器恢复数据后可由可信局域网访问。
  $trustedRelationalDatabaseConfigurationOutput=@(& $TrustedQdrantAccessScript @trustedRelationalDatabaseConfigurationParameters)
  # [2026-07-29 13:16:00] 作用：创建或修复全部业务直连端口的局域网防火墙规则；理由依据：业务层不再创建任何端口转发映射。
  $trustedBusinessConfigurationOutput=@(
    & $TrustedQdrantAccessScript `
      -ListenAddress $TrustedBusinessListenAddress `
      -ConnectAddress $InternalHost `
      -Port $TrustedBusinessListenPorts `
      -ManagedPort $TrustedBusinessListenPorts `
      -RemoteAddress $TrustedBusinessRemoteAddresses `
      -RulePrefix 'MonFangAI Business' `
      -ResourceName '业务服务' `
      -DirectListener
  )
  # [2026-07-27 作用] 只保留配置工具的结构化结果；理由依据：netsh 在成功时会向标准输出写入文本，
  # 旧逻辑把这些成功文本也计入数组，导致四条代理实际已创建却被误报为配置失败。
  $trustedQdrantConfiguration=@(
    $trustedQdrantConfigurationOutput |
      Where-Object {
        $null -ne $_ -and
        $null -ne $_.PSObject.Properties['Result']
      }
  )
  $trustedRelationalDatabaseConfiguration=@(
    $trustedRelationalDatabaseConfigurationOutput |
      Where-Object {
        $null -ne $_ -and
        $null -ne $_.PSObject.Properties['Result']
      }
  )
  # [2026-07-29 13:16:00] 作用：过滤业务防火墙配置工具的结构化结果；理由依据：netsh 文本不能混入最终门禁。
  $trustedBusinessConfiguration=@(
    $trustedBusinessConfigurationOutput |
      Where-Object {
        $null -ne $_ -and
        $null -ne $_.PSObject.Properties['Result']
      }
  )
}else{
  $trustedQdrantConfiguration=@(
    [pscustomobject]@{
      Result='READY'
      ListenAddress=$TrustedQdrantListenAddress
      ConnectAddress=$TrustedQdrantConnectAddress
      ListenPorts=$TrustedQdrantPorts
      RemoteAddress=$TrustedQdrantRemoteAddresses
      ExistingConfigurationReused=$true
    }
  )
  $trustedRelationalDatabaseConfiguration=@(
    [pscustomobject]@{
      Result='READY'
      ListenAddress=$TrustedRelationalDatabaseListenAddress
      ConnectAddress=$TrustedRelationalDatabaseConnectAddress
      ListenPorts=$TrustedRelationalDatabasePorts
      RemoteAddress=$TrustedRelationalDatabaseRemoteAddresses
      ExistingConfigurationReused=$true
    }
  )
  # [2026-07-29 13:16:00] 作用：普通用户会话复用管理员子进程已验证的业务直连规则；理由依据：Docker 和业务进程继续在交互用户会话启动。
  $trustedBusinessConfiguration=@(
    [pscustomobject]@{
      Result='READY'
      ListenAddress=$TrustedBusinessListenAddress
      ListenPorts=$TrustedBusinessListenPorts
      RemoteAddress=$TrustedBusinessRemoteAddresses
      ExistingConfigurationReused=$true
    }
  )
}
if(
  $trustedQdrantConfiguration.Count -ne 1 -or
  $trustedQdrantConfiguration[0].Result -ne 'READY'
){
  throw '一键启动未能完成可信 Qdrant 端口组配置。'
}
if(
  $trustedRelationalDatabaseConfiguration.Count -ne 1 -or
  $trustedRelationalDatabaseConfiguration[0].Result -ne 'READY'
){
  throw '一键启动未能完成可信关系数据库端口组配置。'
}
if(
  $trustedBusinessConfiguration.Count -ne 1 -or
  $trustedBusinessConfiguration[0].Result -ne 'READY'
){
  throw '一键启动未能完成可信业务直连端口组配置。'
}
$env:SQL_RAG_TRUSTED_QDRANT_LISTEN_ADDRESS=$TrustedQdrantListenAddress
$env:SQL_RAG_TRUSTED_QDRANT_CONNECT_ADDRESS=$TrustedQdrantConnectAddress
$env:SQL_RAG_TRUSTED_QDRANT_REMOTE_ADDRESS=(
  $TrustedQdrantRemoteAddresses -join ','
)
$env:SQL_RAG_TRUSTED_RELATIONAL_DATABASE_LISTEN_ADDRESS=(
  $TrustedRelationalDatabaseListenAddress
)
$env:SQL_RAG_TRUSTED_RELATIONAL_DATABASE_CONNECT_ADDRESS=(
  $TrustedRelationalDatabaseConnectAddress
)
$env:SQL_RAG_TRUSTED_RELATIONAL_DATABASE_REMOTE_ADDRESS=(
  $TrustedRelationalDatabaseRemoteAddresses -join ','
)
if($isAdministrator){
  [Environment]::SetEnvironmentVariable(
    'SQL_RAG_TRUSTED_QDRANT_LISTEN_ADDRESS',
    $TrustedQdrantListenAddress,
    [EnvironmentVariableTarget]::Machine
  )
  [Environment]::SetEnvironmentVariable(
    'SQL_RAG_TRUSTED_QDRANT_CONNECT_ADDRESS',
    $TrustedQdrantConnectAddress,
    [EnvironmentVariableTarget]::Machine
  )
  [Environment]::SetEnvironmentVariable(
    'SQL_RAG_TRUSTED_QDRANT_REMOTE_ADDRESS',
    ($TrustedQdrantRemoteAddresses -join ','),
    [EnvironmentVariableTarget]::Machine
  )
  [Environment]::SetEnvironmentVariable(
    'SQL_RAG_TRUSTED_QDRANT_PORTS',
    ($TrustedQdrantPorts -join ','),
    [EnvironmentVariableTarget]::Machine
  )
  [Environment]::SetEnvironmentVariable(
    'SQL_RAG_TRUSTED_RELATIONAL_DATABASE_LISTEN_ADDRESS',
    $TrustedRelationalDatabaseListenAddress,
    [EnvironmentVariableTarget]::Machine
  )
  [Environment]::SetEnvironmentVariable(
    'SQL_RAG_TRUSTED_RELATIONAL_DATABASE_CONNECT_ADDRESS',
    $TrustedRelationalDatabaseConnectAddress,
    [EnvironmentVariableTarget]::Machine
  )
  [Environment]::SetEnvironmentVariable(
    'SQL_RAG_TRUSTED_RELATIONAL_DATABASE_REMOTE_ADDRESS',
    ($TrustedRelationalDatabaseRemoteAddresses -join ','),
    [EnvironmentVariableTarget]::Machine
  )
  [Environment]::SetEnvironmentVariable(
    'SQL_RAG_TRUSTED_RELATIONAL_DATABASE_PORTS',
    ($TrustedRelationalDatabasePorts -join ','),
    [EnvironmentVariableTarget]::Machine
  )
}
Write-Host (
  '可信 Qdrant 入口已自动配置：' +
  $TrustedQdrantListenAddress +
  ':[' +
  ($TrustedQdrantPorts -join ',') +
  ']；来源=' +
  ($TrustedQdrantRemoteAddresses -join ',')
)
Write-Host (
  '可信关系数据库入口已自动配置：' +
  $TrustedRelationalDatabaseListenAddress +
  ':[' +
  ($TrustedRelationalDatabasePorts -join ',') +
  ']；来源=' +
  ($TrustedRelationalDatabaseRemoteAddresses -join ',')
)
Write-Host (
  '可信业务直连入口已自动配置：' +
  $TrustedBusinessListenAddress +
  ':[' +
  ($TrustedBusinessListenPorts -join ',') +
  ']；无业务网关；来源=' +
  ($TrustedBusinessRemoteAddresses -join ',')
)
if($ConfigureTrustedDataOnly){
  if(-not $isAdministrator){
    throw 'ConfigureTrustedDataOnly 只能由管理员子进程执行。'
  }
  Write-Host '可信数据代理与业务直连防火墙规则配置完成，返回普通用户会话继续启动全栈。'
  exit 0
}
# [2026-08-03 17:14:05] 作用：只接受第二套独立profile固定入口的管理员编排标记；理由依据：历史aliyun键、本地入口和直接调用不得获得第二套系统配置权限。
$isServerAdministratorEntry=($DeploymentProfile-eq'server_second_ports'-and$usesIndependentServiceProfile-and[string]$env:SQL_RAG_SERVER_ADMIN_ENTRY-eq'1')
# [2026-08-04 17:02:00] 作用：为第二套分阶段启动建立独立故障账本；理由依据：任何单个外部依赖失败都必须在其余可启动服务完成后统一汇总，第一套local仍保持原有严格合同。
$ServerSecondStartupFailures=New-Object 'System.Collections.Generic.List[string]'
# [2026-08-04 17:02:01] 作用：集中记录第二套被隔离的阶段故障；理由依据：现场必须同时看到失败阶段、原始异常和“继续启动”动作，不能再把有界降级误判为卡死。
function Add-ServerSecondStartupFailure([string]$Stage,[string]$Message){
  # [2026-08-04 17:02:02] 作用：生成稳定的阶段故障记录；理由依据：最终汇总和回归测试需要可机器读取的stage=message形式。
  $failureRecord="$Stage=$Message"
  # [2026-08-04 17:02:03] 作用：把记录加入当前第二套启动账本；理由依据：后续成功启动其他服务不能覆盖先前真实失败。
  [void]$ServerSecondStartupFailures.Add($failureRecord)
  # [2026-08-04 17:02:04] 作用：立即报告故障隔离与继续动作；理由依据：运维窗口不能在失败点无输出退出或静默等待。
  Write-Warning "第二套阶段故障已隔离，继续拉起其余服务：$failureRecord"
}
# [2026-08-04 17:02:05] 作用：以统一边界启动一个业务子进程；理由依据：第二套某一Start-Process异常不得阻止后续WebUI、Knowledge、看板或Getsoft被逐个尝试，第一套仍原样抛错。
function Start-SqlRagServiceProcess([string]$Stage,[scriptblock]$StartAction){
  # [2026-08-04 17:02:06] 作用：捕获单服务创建异常；理由依据：进程创建失败与其他独立端口服务没有全局中止关系。
  try{
    # [2026-08-04 17:02:07] 作用：返回真实Start-Process对象；理由依据：成功路径必须保持原有进程引用和日志行为。
    return & $StartAction
  }catch{
    # [2026-08-31 14:43:17] 作用：两套统一传播业务子进程创建失败；理由依据：第二套继续运行会把首个原始故障埋成后续健康汇总错误，无法形成确定修复闭环。
    throw
  }
}
# [2026-08-04 08:31:03] 作用：只接受第一套固定local入口的管理员编排标记；理由依据：本地wrapper必须与第二套身份互斥且直接调用共享引擎仍不可启动Docker Desktop。
$isLocalAdministratorEntry=($DeploymentProfile-eq'local'-and-not$usesIndependentServiceProfile-and[string]$env:SQL_RAG_LOCAL_ENTRY-eq'1')
# [2026-08-04 08:31:04] 作用：允许两套各自固定wrapper在管理员窗口编排并阻断共享引擎直启；理由依据：截图故障源于门禁只认可第二套，导致local在Docker检查前被错误拒绝。
if($DockerBackend-eq'desktop'-and$isAdministrator-and-not($isServerAdministratorEntry-or$isLocalAdministratorEntry)){throw '管理员PowerShell必须通过start-local-full-stack.ps1或start-server-full-stack.ps1固定入口运行；禁止直接调用共享启动引擎。'}
# [2026-08-03 17:14:07] 作用：读取当前Windows身份SID；理由依据：内置Administrator的RID 500必须验证管理员审批模式后才能取得标准Explorer令牌。
$currentUserSid=[string]$currentIdentity.User.Value
# [2026-08-03 17:14:08] 作用：识别内置Administrator身份；理由依据：该账户默认使用完整令牌，正是目标机与已跑通第一套的关键差异。
$isBuiltinAdministrator=$currentUserSid.EndsWith('-500',[StringComparison]::Ordinal)
# [2026-08-03 17:14:09] 作用：读取实际UAC策略；理由依据：不能根据窗口标题猜测Docker Desktop可用令牌。
$uacPolicy=Get-ItemProperty -LiteralPath 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System' -ErrorAction SilentlyContinue
# [2026-08-03 17:14:10] 作用：判断UAC是否启用；理由依据：EnableLUA关闭时Explorer无法提供与管理员入口分离的标准令牌。
$uacEnabled=($null-ne$uacPolicy-and[int]$uacPolicy.EnableLUA-eq1)
# [2026-08-03 17:14:11] 作用：判断内置Administrator管理员审批模式；理由依据：RID 500需要FilterAdministratorToken=1才能形成拆分令牌。
$builtinAdministratorApprovalMode=($null-ne$uacPolicy-and[int]$uacPolicy.FilterAdministratorToken-eq1)
# [2026-08-03 17:14:12] 作用：在宿主令牌策略不满足时立即阻断；理由依据：V12实机已证明此状态会让Linux Engine内部就绪但Windows API proxy持续HTTP500。
if($DockerBackend-eq'desktop'-and$isServerAdministratorEntry-and(-not$uacEnabled-or($isBuiltinAdministrator-and-not$builtinAdministratorApprovalMode))){throw 'builtin_administrator_full_token_no_desktop_user_context：请先执行最新逻辑更新入口；若其返回RestartRequired=true，正常重启Windows一次后再运行本入口。'}
# [2026-08-03 17:14:13] 作用：明确记录管理员编排与普通交互Docker Desktop分离模式；理由依据：现场必须能确认没有再次从管理员PowerShell直接创建Desktop进程。
if($DockerBackend-eq'desktop'-and$isServerAdministratorEntry){Write-Host '第二套管理员入口已启用；Docker Desktop将经当前登录会话Explorer标准令牌启动，业务CLI与22端口仍在本窗口顺序编排。'}
# [2026-08-04 08:31:05] 作用：明确记录第一套固定入口已通过管理员门禁；理由依据：用户需要从控制台确认local身份没有再次被第二套管理员策略拦截。
if($DockerBackend-eq'desktop'-and$isLocalAdministratorEntry){Write-Host '第一套本地固定入口已启用；Docker Desktop沿用当前交互会话，local端口与容器合同不会进入第二套恢复分支。'}
# [2026-07-24 18:05:00] 作用：读取供同机其他项目容器加入的数据服务网络名；理由依据：数据库不对公网监听，但同一服务器上的容器仍需要通过 Docker 内部网络互通。
$InternalDockerNetwork=[string]$env:SQL_RAG_INTERNAL_NETWORK
# [2026-07-31 09:45:11] 作用：未配置时使用当前 profile 的独立商业部署网络名；理由依据：本地与服务器 Compose 不得通过同名 bridge 互相发现数据库。
if([string]::IsNullOrWhiteSpace($InternalDockerNetwork)){$InternalDockerNetwork=$ProfileInternalDockerNetwork}
# [2026-07-24 18:05:00] 作用：规范化网络名；理由依据：避免环境变量空白字符导致 Compose 创建错误网络。
$InternalDockerNetwork=$InternalDockerNetwork.Trim()
# [2026-07-24 18:05:00] 作用：限制网络名为 Docker 可稳定复用的安全字符；理由依据：阻止换行、空格或命令字符污染 Compose 参数。
if($InternalDockerNetwork -notmatch '^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$'){throw "安全阻断：SQL_RAG_INTERNAL_NETWORK 名称无效：$InternalDockerNetwork"}
# [2026-07-24 18:05:00] 作用：把已校验网络名传给 Docker Compose；理由依据：一键启动和其他同机容器必须引用同一个固定网络。
$env:SQL_RAG_INTERNAL_NETWORK=$InternalDockerNetwork
# [2026-07-25 15:10:03] 作用：LangGraph checkpoint 端口已由当前端口配置统一解析；理由依据：local 与 aliyun 不能继续共用硬编码宿主机端口。
# 2026-06-13 20:18:41 新增：用当前端口生成后端 URL；作用：健康检查和 WebUI 代理都读取同一个地址；理由：避免脚本里散落硬编码。
$BackendUrl="http://$BusinessListenHost`:$BackendPort"
# 2026-06-13 20:18:41 新增：用当前端口生成 WebUI URL；作用：输出给用户真实可访问入口；理由：默认端口不可用时也能明确知道最新地址。
$WebUrl="http://$PublicHost`:$WebPort"
# 2026-07-01 12:16:02 新增：生成资产类型后端 URL；作用：WebUI 代理和健康检查共用；理由：资产类型模块有独立后端服务。
$AssetTypeBackendUrl="http://$BusinessListenHost`:$AssetTypeBackendPort"
# [2026-08-06 11:08:00] 作用：复用当前profile已验证的统一前端公开根；理由依据：禁止在后续阶段重新拼接并意外采用另一套主机或端口。
$AssetTypeWebUrl=$FrontendPublicBaseUrl
# [2026-07-04 10:18:20] 作用：根据知识库后端端口生成健康检查和代理目标地址；理由依据：端口回退时必须由同一变量同步更新，避免 WebUI 指向旧实例。
$KnowledgeBackendUrl="http://$BusinessListenHost`:$KnowledgeBackendPort"
# [2026-07-04 10:18:20] 作用：根据知识库 WebUI 端口生成浏览器访问地址；理由依据：启动完成后需要输出并验证用户可访问的新入口。
$KnowledgeWebUrl="http://$PublicHost`:$KnowledgeWebPort"
# [2026-07-31 10:41:00] 作用：读取部署 profile 声明的外部门户精确 Origin；理由依据：mofang.bao1998.com 页面直接调用局域网 18320/28320 时必须通过浏览器 CORS 预检。
$PortalWebOrigins=@($ServicePortProfile.portal_web_origins | ForEach-Object {[string]$_})
# [2026-07-31 10:41:01] 作用：允许运维在不改代码时用逗号分隔值覆盖门户 Origin；理由依据：后续域名迁移应更新配置而不是放开通配符。
$PortalWebOriginsOverride=[string]$env:SQL_RAG_PORTAL_WEB_ORIGINS
# [2026-07-31 10:41:02] 作用：显式覆盖存在时仅采用覆盖列表；理由依据：环境配置优先级必须确定且不与旧域名暗中叠加。
if(-not [string]::IsNullOrWhiteSpace($PortalWebOriginsOverride)){$PortalWebOrigins=@($PortalWebOriginsOverride.Split(',') | ForEach-Object {$_.Trim()} | Where-Object {$_})}
# [2026-07-31 10:41:03] 作用：把 profile 自有页面与外部门户合并成精确白名单；理由依据：18191、18321 和门户代理三类页面都需要上传与编辑知识。
$AllowedKnowledgeWebOrigins=@($AssetTypeWebUrl,$KnowledgeWebUrl)+@($PortalWebOrigins)
# [2026-07-31 10:41:04] 作用：逐项校验白名单只包含无路径的 HTTP/HTTPS Origin；理由依据：拒绝通配符、路径和非网页协议，保持业务端口最小跨域边界。
foreach($allowedOrigin in $AllowedKnowledgeWebOrigins){
  # [2026-07-31 10:41:05] 作用：解析当前候选 Origin；理由依据：字符串拼接不能证明它是合法且精确的浏览器来源。
  $allowedOriginUri=$null
  # [2026-07-31 10:41:06] 作用：拒绝无法解析、非绝对、非 HTTP(S)、带路径查询或通配符的来源；理由依据：错误白名单不能在启动后静默扩大访问面。
  if(-not [Uri]::TryCreate([string]$allowedOrigin,[UriKind]::Absolute,[ref]$allowedOriginUri) -or $allowedOriginUri.Scheme -notin @('http','https') -or $allowedOriginUri.AbsolutePath -ne '/' -or $allowedOriginUri.Query -or $allowedOriginUri.Fragment -or ([string]$allowedOrigin).Contains('*')){throw "知识服务门户 Origin 非法：$allowedOrigin"}
}
# [2026-07-31 10:41:07] 作用：去重后把精确 Origin 列表传给 18320/28320；理由依据：浏览器预检和实际响应必须由同一运行进程读取稳定白名单。
$env:SQL_RAG_ALLOWED_WEB_ORIGINS=(@($AllowedKnowledgeWebOrigins | Select-Object -Unique) -join ',')
# [2026-07-21 13:38:02] 作用：生成看板后端回环地址；理由依据：WebUI代理与健康检查必须使用同一目标。
$DashboardBackendUrl="http://$BusinessListenHost`:$DashboardBackendPort"
# [2026-07-21 13:38:03] 作用：生成看板对外WebUI地址；理由依据：启动完成后输出局域网可访问入口。
$DashboardWebUrl="http://$PublicHost`:$DashboardWebPort"
$GetsoftPublicUrl="http://$PublicHost`:$GetsoftPort"
# [2026-07-29 13:34:14] 作用：让父启动器对 Getsoft 的健康验收使用固定公开端口；理由依据：方案 A 仅运行一个 18520 ASGI 业务进程，本机 SSE 由该进程内部规范化到回环。
$GetsoftInternalPort=$GetsoftPort
# [2026-07-29 13:34:14] 作用：把兼容变量指向同一个可信 LAN ASGI 地址；理由依据：所有门禁验证固定公开入口且不再启动相邻内部服务。
$GetsoftInternalUrl=$GetsoftPublicUrl
$GetsoftBrowserUrl="$GetsoftPublicUrl$([string]$GetsoftConfig.browser_path)"
# [2026-08-06 11:08:00] 作用：采用当前profile原子生成的资产挂载入口；理由依据：外部门户不应继续维护18191或28191条件分支。
$AssetTypeMountedWebUrl=$FrontendAssetMountUrl
# [2026-08-06 11:08:00] 作用：从当前资产挂载入口生成同源API；理由依据：API与页面必须共享同一profile主机和端口。
$AssetTypeMountedApiUrl="$($AssetTypeMountedWebUrl.TrimEnd('/'))/api"
# [2026-08-06 11:08:00] 作用：采用当前profile原子生成的知识库挂载入口；理由依据：资产与知识库必须一起从212切换到233。
$KnowledgeMountedWebUrl=$FrontendKnowledgeMountUrl
# [2026-08-06 11:08:00] 作用：从当前知识库挂载入口生成同源API；理由依据：知识请求不得因独立字符串拼接回落到第一套。
$KnowledgeMountedApiUrl="$($KnowledgeMountedWebUrl.TrimEnd('/'))/api"
# [2026-07-25 15:10:04] 作用：Qwen 端口由当前端口配置统一解析；理由依据：云端宿主机端口与本地开发端口必须完全分离。
$QwenUrl="http://127.0.0.1:$QwenPort/v1/models"
# [2026-07-25 15:10:05] 作用：Embedding 端口由当前端口配置统一解析；理由依据：两套部署仍复用相同业务路由但不复用宿主机端口。
# [2026-07-17 13:56:30] 作用：生成 Embedding OpenAI-compatible 模型列表地址；理由：最终 ready 必须验证真实 HTTP 模型端点而非仅检查端口。
$EmbeddingUrl="http://127.0.0.1:$EmbeddingPort/v1/models"
# [2026-07-17 13:56:30] 作用：声明 Embedding 对外模型别名；理由：调用方 MODEL_EMBED 与 `/v1/models` 返回值必须稳定一致。
$EmbeddingModelAlias='Qwen3-Embedding-0.6B-Q8_0'
$LlamaExe=Join-Path $SqlRag 'module_config\model_service\runtimes\llama_cpp_win_cpu\llama-server.exe'
$ModelFile=Join-Path $SqlRag 'module_config\model_service\models\qwen35_2b\Qwen_Qwen3.5-2B-Q4_K_M.gguf'
# [2026-07-17 13:56:30] 作用：定位仓库内已验收的 Qwen3 Embedding 模型；理由：全本地链路不能在一键启动时回退远程 API 或未知模型。
$EmbeddingModelFile=Join-Path $SqlRag 'module_config\model_service\models\qwen3_embedding_06b\Qwen3-Embedding-0.6B-Q8_0.gguf'
$LlamaCwd=Split-Path -Parent $LlamaExe
chcp 65001 | Out-Null
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
# [2026-07-17 13:56:30] 作用：按 Pydantic 全禁用合同关闭第三方插件入口扫描；理由：值 `__all__` 才与当前已验收的前后端运行环境一致并避免 DLP 污染元数据被加载。
$env:PYDANTIC_DISABLE_PLUGINS='__all__'
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
# [2026-07-08 14:32:16] 作用：定位 SQL_RAG 运行时工具目录；理由依据：ONEDLP 检测、修复和备份脚本集中放在 app\SQL_RAG\tools 下。
$RuntimeToolsDir=Join-Path $SqlRag 'tools'
# [2026-07-08 14:32:16] 作用：定位启动前 ONEDLP 修复脚本；理由依据：根 .venv 若被加密头污染，主业务脑后端会在 import 阶段直接失败。
$RuntimeRepairScript=Join-Path $RuntimeToolsDir 'repair_sql_rag_runtime_onedlp.ps1'
# [2026-07-15 10:04:45] 作用：定位统一 ONEDLP 完整性检测脚本；理由依据：全量服务 ready 后必须再次确认整个 SQL_RAG 未在启动期间被污染。
$RuntimeIntegrityScript=Join-Path $RuntimeToolsDir 'test_onedlp_runtime_integrity.ps1'
# [2026-07-08 14:32:16] 作用：定位启动成功后的运行时备份脚本；理由依据：全量服务跑通后要保存可恢复基线，避免下次重新安装依赖。
$RuntimeBackupScript=Join-Path $RuntimeToolsDir 'backup_sql_rag_runtime.ps1'
# [2026-07-08 14:32:16] 作用：定位仓库级运行时备份目录；理由依据：备份目录不能放在 SQL_RAG 内部，避免递归自包含。
$RuntimeBackupRoot=Join-Path $RepoRoot 'runtime_backups'
# [2026-07-08 14:32:16] 作用：在启动 Python 服务前执行 ONEDLP 检测/修复；理由依据：污染依赖必须先恢复，否则服务启动会出现 source code string cannot contain null bytes。
if(Test-Path -LiteralPath $RuntimeRepairScript){
  # [2026-07-08 14:32:16] 作用：调用修复脚本并传入当前仓库路径；理由依据：修复脚本需要按本次项目边界读取备份和检测源码。
  & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $RuntimeRepairScript -RepoRoot $RepoRoot -SqlRag $SqlRag -BackupRoot $RuntimeBackupRoot -RestoreSource
  # [2026-07-08 14:37:44] 作用：读取修复脚本退出码；理由依据：powershell.exe 是 native 命令，失败不会在当前脚本里自动 throw。
  $RuntimeRepairExitCode=$LASTEXITCODE
  # [2026-07-08 14:37:44] 作用：修复脚本失败时中止全量启动；理由依据：依赖污染未解决时继续启动只会得到假 ready 或 import 崩溃。
  if($RuntimeRepairExitCode -ne 0){throw "ONEDLP 修复脚本执行失败，退出码=$RuntimeRepairExitCode"}
# [2026-07-08 14:32:16] 作用：结束启动前修复脚本调用；理由依据：PowerShell 代码块必须闭合。
}
# [2026-07-29 16:58:54] 作用：要求可移植种子权限恢复器随固定一键入口存在；理由依据：缺少该门禁会在 Docker 启动完成后才因 manifest 拒绝访问而浪费时间并中断全部 WebUI 服务。
if(!(Test-Path -LiteralPath $PortableCloneSeedRepairScript -PathType Leaf)){
  # [2026-07-29 16:58:54] 作用：在启动任何模型、Docker 或业务进程前明确阻断；理由依据：不能退回临时复制命令或忽略数据库基线权限问题。
  throw "可移植克隆种子权限恢复器不存在：$PortableCloneSeedRepairScript"
}
# [2026-07-29 16:58:54] 作用：用当前普通交互用户执行可移植种子可读性、哈希和基线恢复门禁；理由依据：最终 WebUI 服务由该用户启动，管理员能读不代表实际业务进程能读。
& powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File $PortableCloneSeedRepairScript `
  -RepoRoot $RepoRoot `
  -SqlRag $SqlRag `
  -BackupRoot $RuntimeBackupRoot `
  -SeedDir $PortableCloneSeedDir
# [2026-07-29 16:58:54] 作用：保存种子恢复器真实退出码；理由依据：native powershell.exe 失败不会可靠触发当前脚本的 Stop 策略。
$PortableCloneSeedRepairExitCode=$LASTEXITCODE
# [2026-07-29 16:58:54] 作用：恢复器失败时终止固定一键入口；理由依据：不可读或哈希不一致的数据种子不能进入 Docker 数据恢复流程。
if($PortableCloneSeedRepairExitCode -ne 0){
  # [2026-07-29 16:58:54] 作用：输出可直接定位的固定入口错误；理由依据：用户无需等待完整服务启动后再从 Python PermissionError 反推原因。
  throw "可移植克隆种子启动前恢复失败，退出码=$PortableCloneSeedRepairExitCode"
}
function Set-EnvLine($Path,$Key,$Value){
  $lines=@()
  if(Test-Path $Path){$lines=Get-Content -LiteralPath $Path}
  $found=$false
  $out=@()
  foreach($line in $lines){
    if($line -match "^\s*$([regex]::Escape($Key))\s*="){
      $out += "$Key=$Value"; $found=$true
    } else { $out += $line }
  }
  if(!$found){$out += "$Key=$Value"}
  $out | Set-Content -LiteralPath $Path -Encoding UTF8
  [Environment]::SetEnvironmentVariable($Key,$Value,'Process')
}
# [2026-07-22 10:31:19] 作用：从指定.env读取单个值且不输出内容；理由依据：一键启动需安全继承既有硅基流动密钥而不能把它写进日志或源码。
function Get-EnvLineValue($Path,$Key){
  # [2026-07-22 10:31:20] 作用：处理环境文件缺失；理由依据：缺少真实密钥源时后续门禁应明确失败而不是读取空路径。
  if(!(Test-Path -LiteralPath $Path)){return ''}
  # [2026-07-22 10:31:21] 作用：按精确变量名读取最后一个有效赋值；理由依据：避免同名前缀或历史重复行污染聊天模型配置。
  $line=Get-Content -LiteralPath $Path -Encoding UTF8 | Where-Object {$_ -match ('^\s*'+[regex]::Escape($Key)+'\s*=')} | Select-Object -Last 1
  # [2026-07-22 10:31:22] 作用：处理变量未配置；理由依据：调用方继续按兼容密钥顺序寻找。
  if($null -eq $line){return ''}
  # [2026-07-22 10:31:23] 作用：返回等号后的原值并去除首尾空白；理由依据：密钥只进入子进程环境且不打印。
  return (($line -split '=',2)[1]).Trim()
}
function Set-DatabaseUrlHost($Path,$HostValue){
  # [2026-07-10 16:02:00] 作用：在保留用户名、密码、端口和库名的前提下替换 DATABASE_URL 主机；理由依据：不能在脚本里重写或泄露保存的数据库密码。
  if(!(Test-Path -LiteralPath $Path)){return}
  # [2026-07-10 16:02:00] 作用：读取运行时环境文件全部行；理由依据：只替换目标键，避免破坏其它 API Key、模型和数据库配置。
  $lines=Get-Content -LiteralPath $Path
  # [2026-07-10 17:07:00] 作用：缓存环境文件键值；理由依据：当 DATABASE_URL 已被旧脚本破坏时，需要从同文件 DB_* 配置安全重建。
  $envMap=@{}
  # [2026-07-10 17:07:00] 作用：遍历原始环境变量行；理由依据：只识别 KEY=VALUE 格式，避免注释和空行参与重建。
  foreach($rawLine in $lines){
    # [2026-07-10 17:07:00] 作用：解析单行环境变量；理由依据：PowerShell 正则捕获可以保留等号右侧完整值。
    if($rawLine -match '^\s*([^#=\s]+)=(.*)$'){
      # [2026-07-10 17:07:00] 作用：把键值写入临时字典；理由依据：后续修复 DATABASE_URL 时按键读取，不依赖固定行号。
      $envMap[$Matches[1]]=$Matches[2]
    }
  }
  # [2026-07-10 16:02:00] 作用：初始化输出行集合；理由依据：PowerShell 逐行重写可以稳定保留未知配置行。
  $out=@()
  # [2026-07-10 16:02:00] 作用：逐行扫描环境变量；理由依据：DATABASE_URL 可能位于文件任意位置，不能依赖固定行号。
  foreach($line in $lines){
    # [2026-07-10 16:02:00] 作用：只处理 DATABASE_URL 键；理由依据：其它连接串如 Neo4j 不属于本次 PostgreSQL 同步故障。
    if($line -match '^\s*DATABASE_URL=(.+)$'){
      # [2026-07-10 16:02:00] 作用：提取原始连接串值；理由依据：后续替换只允许改主机字段。
      $url=$Matches[1]
      # [2026-07-10 17:29:00] 作用：读取数据库用户名；理由依据：只换 host 会保留旧认证段，旧密码会继续导致 Knowledge 后端 database=false。
      $dbUser=[string]$envMap['DB_USER']
      # [2026-07-10 17:29:00] 作用：读取数据库密码；理由依据：DATABASE_URL 必须和同文件 DB_PASSWORD 保持一致。
      $dbPassword=[string]$envMap['DB_PASSWORD']
      # [2026-07-10 17:29:00] 作用：读取数据库端口；理由依据：AIERP 外部 PostgreSQL 使用截图授权的 5432。
      $dbPort=[string]$envMap['DB_PORT']
      # [2026-07-10 17:29:00] 作用：读取数据库名；理由依据：知识库、资产类型和问答联动表位于 AIERP。
      $dbName=[string]$envMap['DB_NAME']
      # [2026-07-10 17:29:00] 作用：在缺省端口时回退到 5432；理由依据：避免空端口生成不可解析连接串。
      if([string]::IsNullOrWhiteSpace($dbPort)){$dbPort=[string]$MigratedPostgresPort}
      # [2026-07-10 17:29:00] 作用：在缺省库名时回退到 AIERP；理由依据：业务表不在 lightrag 数据库。
      if([string]::IsNullOrWhiteSpace($dbName)){$dbName='AIERP'}
      # [2026-07-10 17:29:00] 作用：对用户名做 URL 编码；理由依据：避免特殊字符破坏 SQLAlchemy URL 结构。
      $safeUser=[uri]::EscapeDataString($dbUser)
      # [2026-07-10 17:29:00] 作用：对密码做 URL 编码；理由依据：避免密码中的 @、:、/ 被误解析为 URL 分隔符。
      $safePassword=[uri]::EscapeDataString($dbPassword)
      # [2026-07-10 17:29:00] 作用：重建完整 psycopg2 同步数据库连接串；理由依据：同时修复旧脚本破坏的 URL 和旧认证段残留问题。
      $url="postgresql+psycopg2://${safeUser}:${safePassword}@${HostValue}:${dbPort}/${dbName}"
      # [2026-07-10 16:02:00] 作用：写回替换后的 DATABASE_URL；理由依据：Knowledge 后端优先读取该连接串连接 AIERP。
      $out += "DATABASE_URL=$url"
    }else{
      # [2026-07-10 16:02:00] 作用：原样保留非 DATABASE_URL 行；理由依据：避免启动脚本改动无关运行参数。
      $out += $line
    }
  }
  # [2026-07-10 16:02:00] 作用：用 UTF-8 写回运行时环境文件；理由依据：后续知识库进程从该文件读取稳定 IPv4 连接串。
  $out | Set-Content -LiteralPath $Path -Encoding UTF8
}
function Stop-Port($Ports){
  # 2026-06-13 20:18:41 新增：记录所有端口是否释放成功；作用：调用方可决定失败时退出还是切备用端口；理由：不能再假阳性启动。
  $allReleased=$true
  foreach($port in $Ports){
    # 2026-06-13 20:18:41 新增：查找监听当前端口的进程；作用：定位旧后端或旧 WebUI；理由：新版服务启动前必须清理旧监听。
    $owners=@(Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue |
      Select-Object -ExpandProperty OwningProcess -Unique |
      Where-Object {$_})
    foreach($ownerPid in $owners){
      # 2026-06-13 20:18:41 新增：优先把端口 owner 放入清理列表；作用：清掉真正监听端口的进程；理由：端口释放是启动新服务的前提。
      $targetPids=@($ownerPid)
      # 2026-06-13 20:18:41 新增：读取 owner 的父进程；作用：处理 uv/python wrapper 进程树；理由：只杀子进程时 Windows 可能拒绝释放。
      $ownerProcess=Get-CimInstance Win32_Process -Filter "ProcessId=$ownerPid" -ErrorAction SilentlyContinue
      if($ownerProcess -and $ownerProcess.ParentProcessId){
        # 2026-06-13 20:18:41 新增：把父进程也加入清理列表；作用：连带关闭 wrapper；理由：旧服务常由父进程托管。
        $targetPids += [int]$ownerProcess.ParentProcessId
      }
      foreach($targetPid in ($targetPids | Select-Object -Unique)){
        # 2026-06-13 20:18:41 新增：输出正在释放的进程树；作用：让用户知道卡在哪个 PID；理由：端口问题需要可诊断。
        Write-Host "释放端口 $port，占用进程树 PID=$targetPid ..."
        # 2026-06-13 20:18:41 新增：临时降低 native 错误打断；作用：taskkill 失败后继续走 Stop-Process fallback；理由：旧高权限进程会拒绝 taskkill。
        $oldNative=$ErrorActionPreference
        try{
          $ErrorActionPreference='SilentlyContinue'
          # 2026-06-13 20:18:41 新增：尝试按进程树强杀；作用：优先释放完整服务树；理由：只杀一个 python 子进程不稳定。
          & taskkill.exe /PID $targetPid /T /F *> $null
          # 2026-06-13 20:18:41 新增：保存 taskkill 返回码；作用：判断是否需要 fallback；理由：native 命令失败不能被吞掉。
          $taskkillExit=$LASTEXITCODE
        }finally{
          # 2026-06-13 20:18:41 新增：恢复错误策略；作用：不影响后续脚本严格失败；理由：只有释放端口这一步需要容错。
          $ErrorActionPreference=$oldNative
        }
        if($taskkillExit -ne 0){
          # 2026-06-13 20:18:41 新增：PowerShell fallback 停进程；作用：兼容 taskkill 无法处理的场景；理由：尽量释放普通权限旧服务。
          Stop-Process -Id $targetPid -Force -ErrorAction SilentlyContinue
          # [2026-07-08 14:41:52] 作用：读取 Stop-Process 后仍存在的进程对象；理由依据：旧管理员窗口启动的 Python 可能拒绝 Stop-Process，但 WMI Terminate 可释放。
          $wmiTarget=Get-CimInstance Win32_Process -Filter "ProcessId=$targetPid" -ErrorAction SilentlyContinue
          # [2026-07-08 14:41:52] 作用：对残留旧进程执行 WMI Terminate；理由依据：本次 18191 高权限旧 Python 只能通过该方式释放成功。
          if($wmiTarget){Invoke-CimMethod -InputObject $wmiTarget -MethodName Terminate -ErrorAction SilentlyContinue | Out-Null}
        }
      }
    }
    # 2026-06-13 20:18:41 新增：等待端口实际释放；作用：避免刚杀完进程马上绑定导致 address in use；理由：Windows TCP 状态释放有延迟。
    $deadline=(Get-Date).AddSeconds(30)
    while((Get-Date) -lt $deadline){
      $still=Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
      if(!$still){break}
      # [2026-08-24 08:38:21] 作用：重新枚举首轮终止后新接管该端口的监听进程；理由依据：同参数旧模型可能存在两份，杀掉第一份后第二份会立即绑定 18001，单次枚举会误报无法释放。
      $resurfacedOwnerPids=@($still|Select-Object -ExpandProperty OwningProcess -Unique|Where-Object{$_})
      # [2026-08-24 08:38:21] 作用：逐个终止当前真实监听者而不追杀其未知父进程；理由依据：端口归属足以证明该进程在阻塞本轮启动，同时避免误伤与项目无关的 PowerShell 父窗口。
      foreach($resurfacedOwnerPid in $resurfacedOwnerPids){
        # [2026-08-24 08:38:21] 作用：输出重新接管端口的精确 PID；理由依据：现场日志必须能解释为何首轮结束后仍继续回收。
        Write-Host "端口 $port 被另一旧实例重新接管，继续释放监听 PID=$resurfacedOwnerPid ..."
        # [2026-08-24 08:38:21] 作用：保存严格错误策略；理由依据：taskkill 失败后仍需进入 WMI 回退且不污染后续启动步骤。
        $resurfacedPreviousErrorActionPreference=$ErrorActionPreference
        # [2026-08-24 08:38:21] 作用：初始化本次重新接管进程的 taskkill 退出码；理由依据：每个 PID 必须独立判定是否需要回退。
        $resurfacedTaskkillExit=0
        # [2026-08-24 08:38:21] 作用：用进程树模式结束当前真实监听者；理由依据：监听进程自己的子进程也不能在下一轮再次接管同端口。
        try{$ErrorActionPreference='SilentlyContinue';& taskkill.exe /PID $resurfacedOwnerPid /T /F *> $null;$resurfacedTaskkillExit=$LASTEXITCODE}finally{$ErrorActionPreference=$resurfacedPreviousErrorActionPreference}
        # [2026-08-24 08:38:21] 作用：在 taskkill 非零时使用 PowerShell 强制结束监听者；理由依据：普通用户启动的旧模型仍应由固定一键可靠回收。
        if($resurfacedTaskkillExit-ne0){Stop-Process -Id $resurfacedOwnerPid -Force -ErrorAction SilentlyContinue}
        # [2026-08-24 08:38:21] 作用：读取 PowerShell 回退后仍存在的同一监听进程；理由依据：高权限残留只对已证明占用目标端口的 PID 使用 WMI 终止。
        $resurfacedWmiTarget=Get-CimInstance Win32_Process -Filter "ProcessId=$resurfacedOwnerPid" -ErrorAction SilentlyContinue
        # [2026-08-24 08:38:21] 作用：终止仍残留的精确监听 PID；理由依据：不扩大到其他 Node、Python、PowerShell 或另一套 profile 进程。
        if($resurfacedWmiTarget){Invoke-CimMethod -InputObject $resurfacedWmiTarget -MethodName Terminate -ErrorAction SilentlyContinue|Out-Null}
      }
      Start-Sleep -Milliseconds 500
    }
    # 2026-06-13 20:18:41 新增：复查端口是否仍被占用；作用：把高权限旧服务占用识别出来；理由：不能继续用旧端口做假健康检查。
    $left=Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if($left){
      # 2026-06-13 20:18:41 新增：释放失败只记录为 false；作用：业务端口可切备用，模型端口可由调用方决定失败；理由：一键脚本要能自恢复。
      Write-Warning "端口 $port 释放失败，仍有进程占用。"
      $allReleased=$false
    }
  }
  # 2026-06-13 20:18:41 新增：返回释放结果；作用：上层决定是否 fallback；理由：启动脚本不能再无条件继续。
  return $allReleased
}
function Test-PortFree($Port){
  # 2026-06-13 20:18:41 新增：初始化 TCP listener；作用：用真实 bind 判断端口是否可用；理由：只看连接表可能漏掉瞬态占用。
  $listener=$null
  try{
    # 2026-06-13 20:18:41 新增：尝试绑定 127.0.0.1 指定端口；作用：验证后端/WebUI 能否监听；理由：最终服务只绑定本机地址。
    $listener=[System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Parse('127.0.0.1'),[int]$Port)
    # 2026-06-13 20:18:41 新增：启动监听器；作用：触发端口占用检测；理由：成功 start 才说明端口可用。
    $listener.Start()
    # 2026-06-13 20:18:41 新增：返回 true；作用：告诉调用方端口空闲；理由：可作为备用端口。
    return $true
  }catch{
    # 2026-06-13 20:18:41 新增：返回 false；作用：跳过不可用端口；理由：被旧服务占用时必须继续寻找。
    return $false
  }finally{
    # 2026-06-13 20:18:41 新增：释放临时 listener；作用：避免检测本身占住端口；理由：后续真实服务还要绑定该端口。
    if($listener){$listener.Stop()}
  }
}
function Find-FreePort($StartPort){
  # 2026-06-13 20:18:41 新增：从给定端口向后扫描；作用：默认端口被锁死时找备用端口；理由：服务仍要能拉起最新逻辑。
  for($candidate=[int]$StartPort;$candidate -lt ([int]$StartPort+200);$candidate++){
    # 2026-06-13 20:18:41 新增：检查候选端口是否空闲；作用：保证启动不会再次 address in use；理由：备用端口必须真实可绑定。
    if(Test-PortFree $candidate){
      # 2026-06-13 20:18:41 新增：返回第一个可用端口；作用：稳定生成最新服务地址；理由：用户只需看脚本输出 URL。
      return $candidate
    }
  }
  # 2026-06-13 20:18:41 新增：找不到端口时报错；作用：避免无限等待；理由：没有可用端口就不能说服务已拉起。
  throw "从 $StartPort 开始没有找到可用端口"
}
function Stop-SqlRagPythonApps{
  # 2026-07-01 10:42:00 新增：清理本项目旧 Python 服务进程；作用：释放上次备用端口启动的主后端、主 WebUI、资产类型后端和资产类型 WebUI；理由：默认端口被旧高权限进程占用时，不能让备用端口每次运行继续漂移。
  # [2026-07-07 09:18:35] 作用：把仓库绝对路径转为安全正则；理由依据：路径包含“(1)”时普通字符串会被当成正则分组，导致旧服务进程无法被匹配清理。
  $repoPattern=[regex]::Escape($RepoRoot)
  # 2026-07-01 10:42:01 新增：定义只属于本项目的服务特征；作用：避免误杀无关 Python 进程；理由：端口清理应该精确限定在 SQL_RAG 服务。
  $patterns=@(
    # [2026-07-07 09:21:10] 作用：安全匹配主业务脑后端命令行；理由依据：Windows 路径反斜杠必须 regex 转义，否则 \m 等片段会触发正则解析错误。
    ([regex]::Escape('app\SQL_RAG\main.py') + '.*business-brain-service'),
    # [2026-07-07 09:21:10] 作用：安全匹配主 WebUI 命令行；理由依据：服务清理需要识别旧前端进程，且不能让路径反斜杠被正则解释。
    [regex]::Escape('app\SQL_RAG\agent_webUI\webui_server.py'),
    # [2026-07-07 09:21:10] 作用：安全匹配资产类型后端命令行；理由依据：资产类型 API 必须随全量脚本重启，避免旧端口实例残留。
    [regex]::Escape('app\SQL_RAG\Asset_type_management\Data_storage_logic\mian_Asset_type_logic\run_asset_type_service.py'),
    # [2026-07-07 09:21:10] 作用：安全匹配资产类型 WebUI 命令行；理由依据：资产类型前端代理必须指向本次启动的后端实例。
    [regex]::Escape('app\SQL_RAG\Asset_type_management\webui\webui_server.py'),
    # [2026-07-04 10:18:20] 作用：识别本项目上一次启动的知识库后端进程；理由依据：重复执行全量脚本前必须释放备用端口并避免请求落到旧代码。
    [regex]::Escape('app\SQL_RAG\Knowledge_management\backend\knowledge_api\run_server.py'),
    # [2026-07-04 10:18:20] 作用：识别本项目上一次启动的知识库 WebUI 进程；理由依据：同源代理也必须与后端成对重启，避免代理目标残留。
    [regex]::Escape('app\SQL_RAG\Knowledge_management\webui\webui_server.py'),
    # [2026-07-31 15:43:11] 作用：识别客户风险与商机看板后端；理由依据：看板也必须按当前 profile 端口清理，不能误杀另一套服务。
    [regex]::Escape('app\SQL_RAG\Knowledge_Analysis\Customer_Risk_BusinessOpportunity_Perception_Dashboard\backend\run_server.py'),
    # [2026-07-31 15:43:11] 作用：识别客户风险与商机看板 WebUI；理由依据：两套看板进程需要与各自端口合同成对隔离。
    [regex]::Escape('app\SQL_RAG\Knowledge_Analysis\Customer_Risk_BusinessOpportunity_Perception_Dashboard\webui\webui_server.py')
  )
  # [2026-07-31 15:43:11] 作用：汇总当前 profile 全部 Python 业务端口；理由依据：源码路径相同不能证明进程属于当前 local 或 aliyun 实例。
  $profilePorts=@($BackendPort,$WebPort,$AssetTypeBackendPort,$AssetTypeWebPort,$KnowledgeBackendPort,$KnowledgeWebPort,$DashboardBackendPort,$DashboardWebPort)
  # [2026-07-31 15:43:11] 作用：把当前 profile 端口转换为边界安全正则；理由依据：18182 不能误匹配 28182，也不能依赖参数引号形式。
  $profilePortPatterns=@($profilePorts|ForEach-Object{'(?<!\d)'+[regex]::Escape([string]$_)+'(?!\d)'})
  # 2026-07-01 10:42:02 新增：读取 Python 进程命令行；作用：识别旧服务实例；理由：备用端口服务可能不在默认端口列表里。
  $processes=Get-CimInstance Win32_Process -Filter "Name='python.exe' OR Name='pythonw.exe'" -ErrorAction SilentlyContinue
  foreach($proc in $processes){
    # 2026-07-01 10:42:03 新增：跳过没有命令行的进程；作用：避免空值匹配报错；理由：部分系统进程可能隐藏 CommandLine。
    $cmd=[string]$proc.CommandLine
    if(!$cmd){continue}
    # 2026-07-01 10:42:04 新增：限定仓库路径；作用：只处理当前项目启动的 Python 服务；理由：保护用户其它 Python 程序。
    if($cmd -notmatch $repoPattern){continue}
    # 2026-07-01 10:42:05 新增：逐个匹配服务特征；作用：识别要清理的旧服务；理由：主后端和两个 WebUI 都可能占用备用端口。
    $matched=$false
    foreach($pattern in $patterns){
      if($cmd -match $pattern){$matched=$true; break}
    }
    if(!$matched){continue}
    # [2026-07-31 15:43:11] 作用：要求命令行同时包含当前 profile 的精确端口；理由依据：local 与 aliyun 使用同一源码路径，不能再按路径全局结束另一套在线进程。
    $matchesCurrentProfile=$false
    # [2026-07-31 15:43:11] 作用：逐项核对当前 profile 端口；理由依据：后端端口、WebUI 端口及代理 URL 任一命中即可证明实例归属。
    foreach($portPattern in $profilePortPatterns){if($cmd -match $portPattern){$matchesCurrentProfile=$true;break}}
    # [2026-07-31 15:43:11] 作用：跳过另一套 profile 进程；理由依据：一键重启其中一套时另一套必须持续提供服务。
    if(!$matchesCurrentProfile){continue}
    # 2026-07-01 10:42:06 新增：输出清理 PID；作用：让用户排查端口漂移时可见；理由：一键脚本需要可诊断。
    Write-Host "清理旧 SQL_RAG Python 服务 PID=$($proc.ProcessId) ..."
    # 2026-07-01 10:42:07 新增：停止旧服务进程；作用：释放备用端口；理由：后续 Find-FreePort 应优先复用固定备用端口。
    Stop-Process -Id $proc.ProcessId -Force -ErrorAction SilentlyContinue
  }
  # 2026-07-01 10:42:08 新增：给 Windows 释放端口的时间；作用：避免刚杀进程立刻绑定失败；理由：TCP 监听释放存在短延迟。
  Start-Sleep -Seconds 2
}
# [2026-07-17 13:56:30] 作用：读取指定监听端口的真实进程命令行；理由：只凭 HTTP ready 无法区分旧模型参数和当前已验收运行合同。
function Get-ListenerCommandLine($Port){
  # [2026-07-17 13:56:30] 作用：定位端口唯一监听 PID；理由：模型合同必须绑定真正提供该端口的进程。
  $listener=Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
  # [2026-07-17 13:56:30] 作用：端口无监听时返回空命令；理由：调用方据此进入启动分支而不是抛出无关 WMI 异常。
  if(!$listener){return ''}
  # [2026-07-17 13:56:30] 作用：通过监听 PID 读取 Win32_Process；理由：ExecutablePath 不包含线程、slot、token 和 embedding 参数。
  $process=Get-CimInstance Win32_Process -Filter "ProcessId=$($listener.OwningProcess)" -ErrorAction SilentlyContinue
  # [2026-07-17 13:56:30] 作用：返回可比较的完整命令行；理由：复用旧进程前必须逐项核对模型文件和运行参数。
  return [string]$process.CommandLine
}
# [2026-07-17 13:56:30] 作用：通用校验监听进程是否包含全部必需参数片段；理由：Qwen 与 Embedding 共享同一套无硬编码问题答案的进程真实性门禁。
function Test-ListenerRuntimeContract($Port,$RequiredFragments){
  # [2026-07-17 13:56:30] 作用：读取当前监听进程命令；理由：旧服务即使健康也不能直接视为最新版。
  $commandLine=Get-ListenerCommandLine $Port
  # [2026-07-17 13:56:30] 作用：拒绝空命令；理由：无监听或 WMI 不可读时必须重新拉起受控实例。
  if([string]::IsNullOrWhiteSpace($commandLine)){return $false}
  # [2026-07-17 13:56:30] 作用：逐项检查不区分大小写的运行参数；理由：任一模型、端口、线程或用途参数漂移都不应复用。
  foreach($fragment in $RequiredFragments){
    # [2026-07-17 13:56:30] 作用：缺少必需片段时立即判定旧实例；理由：避免健康探针把错误模型或高资源参数误报为 latest。
    if($commandLine.IndexOf([string]$fragment,[System.StringComparison]::OrdinalIgnoreCase) -lt 0){return $false}
  }
  # [2026-07-17 13:56:30] 作用：全部参数命中后允许安全复用；理由：减少不必要模型重载，同时保持最新版保证。
  return $true
}
# [2026-07-17 13:56:30] 作用：验证 Qwen HTTP 模型端点；理由：规划与最终回答必须由本地 18002 真实服务生成。
function Test-Qwen{
  # [2026-07-17 13:56:30] 作用：请求 OpenAI-compatible models 并将异常转换为 false；理由：一键脚本应进入自动启动分支而不是暴露网络异常。
  try { Invoke-RestMethod $QwenUrl -TimeoutSec 5 | Out-Null; return $true } catch { return $false }
}
# [2026-07-17 13:56:30] 作用：校验 18002 是否为本轮五线程、单 slot、160 token 的 Qwen 实例；理由：只复用参数完全一致的最新版模型进程。
function Test-QwenRuntimeContract{
  # [2026-07-17 13:56:30] 作用：声明 Qwen 最小不可漂移参数集合；理由：资源上限和时延优化必须在以后每次一键启动中持续生效。
  # [2026-07-18 09:50:44] 作用：把本地模型进程匹配合同提升到 1024 输出 token 和 90 秒服务截止；理由：检测到 820 字答案被旧 512-token 进程在半句处截断，必须拒绝复用该旧实例。
  # [2026-07-20 12:19:30] 作用：把三分钟服务截止纳入最新版进程合同；理由依据：健康但仍使用 90 秒的旧实例必须被一键脚本识别并重启。
  $required=@($ModelFile,"--port $QwenPort",'-c 4096','-t 5','-tb 5','--parallel 1','-n 1024','--reasoning off','--reasoning-budget 0','--cpu-mask 155','--cache-ram 256','--timeout 180')
  # [2026-07-17 13:56:30] 作用：复用通用进程合同校验；理由：避免为两个本地模型维护不同判定语义。
  return Test-ListenerRuntimeContract $QwenPort $required
}
# [2026-07-17 13:56:30] 作用：验证本地 Embedding HTTP 端点及模型别名；理由：端口存在但模型错误时不能让 RAG 建立不兼容向量。
function Test-Embedding{
  # [2026-07-17 13:56:30] 作用：请求模型列表并核对固定别名；理由：确保调用方实际得到 Qwen3-Embedding-0.6B-Q8_0。
  try{$response=Invoke-RestMethod $EmbeddingUrl -TimeoutSec 5; return @($response.data | ForEach-Object {[string]$_.id}) -contains $EmbeddingModelAlias}catch{return $false}
}
# [2026-07-17 13:56:30] 作用：校验 18001 是否为仓库模型和专用 embedding 模式；理由：健康的聊天模型不能冒充向量模型。
function Test-EmbeddingRuntimeContract{
  # [2026-07-17 13:56:30] 作用：声明低资源 Embedding 不可漂移参数集合；理由：单线程、单 slot、512 batch 可避免与问答模型和 Docker 争满 CPU。
  $required=@($EmbeddingModelFile,"--port $EmbeddingPort",'-c 2048','-t 1','-tb 1','--parallel 1','-b 512','-ub 512','--embedding','--pooling last','--cache-ram 128','--threads-http 1')
  # [2026-07-17 13:56:30] 作用：复用通用监听进程合同校验；理由：模型路径或任何资源参数漂移都触发自动重启。
  return Test-ListenerRuntimeContract $EmbeddingPort $required
}
function Wait-Qwen($Seconds){
  $deadline=(Get-Date).AddSeconds($Seconds)
  while((Get-Date) -lt $deadline){
    if(Test-Qwen){Write-Host "Qwen 模型服务已就绪：$QwenPort"; return}
    Start-Sleep -Seconds 2
  }
  throw "Qwen 模型服务 $QwenPort 没有就绪"
}
# [2026-07-17 13:56:30] 作用：在限定时间内等待本地 Embedding 模型 ready；理由：后续容器同步与后端启动都依赖真实向量端点。
function Wait-Embedding($Seconds){
  # [2026-07-17 13:56:30] 作用：计算 Embedding 等待截止时间；理由：模型加载失败不能让一键命令无限卡住。
  $deadline=(Get-Date).AddSeconds($Seconds)
  # [2026-07-17 13:56:30] 作用：在截止时间前轮询模型端点；理由：加载 GGUF 与 HTTP 监听存在短暂异步窗口。
  while((Get-Date) -lt $deadline){
    # [2026-07-17 13:56:30] 作用：模型别名健康后结束等待；理由：`/v1/models` 成功是调用方可用的最小证据。
    if(Test-Embedding){Write-Host "Embedding 模型服务已就绪：$EmbeddingPort"; return}
    # [2026-07-17 13:56:30] 作用：采用短间隔而非忙轮询；理由：启动阶段不能无意义占满 CPU。
    Start-Sleep -Seconds 2
  }
  # [2026-07-17 13:56:30] 作用：超时后明确阻断全栈启动；理由：缺少 18001 时不能继续报告商业 Agent ready。
  throw "Embedding 模型服务 $EmbeddingPort 没有就绪"
}
# [2026-08-04 18:14:19] 作用：让统一端口等待器接收可选目标地址并默认保持第一套回环合同；理由依据：可信私网入口也需要复用同一套可重试连接逻辑，不能在瞬时拒绝时抛出AggregateException中断全栈。
function Wait-Port($Name,$Port,$Seconds,$Address='127.0.0.1'){
  Write-Host "等待 $Name 端口 $Port ..."
  $deadline=(Get-Date).AddSeconds($Seconds)
  # [2026-08-04 17:02:11] 作用：建立端口等待的首次进度播报时间；理由依据：长启动容器每20秒必须证明仍在有界轮询而不是脚本卡死。
  $nextWaitProgress=(Get-Date).AddSeconds(20)
  while((Get-Date) -lt $deadline){
    $c=New-Object System.Net.Sockets.TcpClient
    try{
      # [2026-08-04 18:14:19] 作用：向调用方指定的回环或可信私网地址发起异步TCP连接；理由依据：第一套本地端口和两套LAN端口必须使用同一个捕获瞬时连接失败的等待器。
      $t=$c.ConnectAsync($Address,[int]$Port)
      if($t.Wait(1000) -and $c.Connected){Write-Host "$Name 已就绪：$Port"; return}
    }catch{}finally{$c.Close()}
    # [2026-08-04 17:02:12] 作用：在等待跨过20秒边界时输出剩余时间；理由依据：第二套首次拉镜像或恢复数据库期间必须持续可观察。
    if((Get-Date)-ge$nextWaitProgress){
      # [2026-08-04 17:02:13] 作用：计算当前端口门禁的非负剩余秒数；理由依据：现场需要区分正常有界等待与超时后的继续启动。
      $remainingWaitSeconds=[Math]::Max(0,[int][Math]::Ceiling(($deadline-(Get-Date)).TotalSeconds))
      # [2026-08-04 17:02:14] 作用：输出具名端口等待进度；理由依据：不再出现PowerShell窗口长时间停在同一行的误判。
      Write-Host "端口等待仍在进行：name=$Name；port=$Port；remaining_seconds=$remainingWaitSeconds"
      # [2026-08-04 17:02:15] 作用：推进下一次20秒进度播报；理由依据：避免每次2秒轮询都刷屏。
      $nextWaitProgress=(Get-Date).AddSeconds(20)
    }
    Start-Sleep -Seconds 2
  }
  throw "$Name 端口 $Port 超时未就绪"
}
# [2026-07-25 15:10:09] 作用：验证当前配置的全部 Qdrant 可信私网入口；理由依据：主库、External、克隆 HTTP 和克隆 gRPC 任一端口缺失都不能报告局域网可用。
function Assert-TrustedQdrantAccess{
  $trustedAddress=[string]$env:SQL_RAG_TRUSTED_QDRANT_LISTEN_ADDRESS
  if([string]::IsNullOrWhiteSpace($trustedAddress) -or $trustedAddress -eq '127.0.0.1'){return}
  $parsedAddress=$null
  if(
    -not [System.Net.IPAddress]::TryParse(
      $trustedAddress,
      [ref]$parsedAddress
    ) -or
    $parsedAddress.AddressFamily -ne
      [System.Net.Sockets.AddressFamily]::InterNetwork -or
    [System.Net.IPAddress]::IsLoopback($parsedAddress) -or
    $parsedAddress.Equals([System.Net.IPAddress]::Any)
  ){
    throw "可信 Qdrant 监听地址无效：$trustedAddress"
  }
  foreach($trustedPort in $TrustedQdrantPorts){
    # [2026-08-04 18:14:19] 作用：以30秒有界重试验证当前可信Qdrant私网端口；理由依据：Windows端口代理在Docker容器刚重建时会短暂拒绝连接，瞬时AggregateException不能阻断其余完好服务。
    Wait-Port -Name "可信 Qdrant 私网入口 $trustedAddress" -Port $trustedPort -Seconds 30 -Address $trustedAddress
  }
  foreach($trustedHttpPort in $TrustedQdrantHttpPorts){
    # [2026-07-31 09:08:50] 作用：为单个 Qdrant HTTP 入口设置最长两分钟的稳定就绪窗口；理由依据：Docker 已开放 TCP 端口时 Qdrant 仍可能处于集合加载阶段，立即请求会被服务端关闭。
    $qdrantHttpDeadline=(Get-Date).AddSeconds(120)
    # [2026-07-31 09:08:51] 作用：清空上一个端口的成功响应；理由依据：必须让每个 HTTP 端口独立完成真实健康验证，不能复用前一个端口的结果。
    $qdrantResponse=$null
    # [2026-07-31 09:08:52] 作用：初始化当前端口的末次异常信息；理由依据：超时失败时需要输出真实网络原因，便于部署排障。
    $qdrantLastError=''
    # [2026-07-31 09:08:53] 作用：在限定窗口内轮询当前 Qdrant 集合接口；理由依据：以 HTTP status=ok 而不是仅 TCP 已监听作为可用标准。
    while((Get-Date) -lt $qdrantHttpDeadline){
      try{
        # [2026-07-31 09:08:54] 作用：调用当前可信局域网 Qdrant 的集合接口；理由依据：该接口能同时证明端口转发、HTTP 服务和存储集合加载均已完成。
        $qdrantResponse=Invoke-RestMethod `
          -Uri "http://$trustedAddress`:$trustedHttpPort/collections" `
          -TimeoutSec 15
        # [2026-07-31 09:08:55] 作用：在 Qdrant 返回 ok 后结束当前端口轮询；理由依据：只有业务级健康响应才允许继续启动后端。
        if([string]$qdrantResponse.status -eq 'ok'){break}
        # [2026-07-31 09:08:56] 作用：保存非 ok 响应的状态；理由依据：若持续未就绪，最终错误必须包含服务端实际状态。
        $qdrantLastError="status=$([string]$qdrantResponse.status)"
      }catch{
        # [2026-07-31 09:08:57] 作用：记录本次 HTTP 连接异常但不立即终止；理由依据：容器重建后的短暂连接关闭属于可恢复的启动窗口。
        $qdrantLastError=$_.Exception.Message
      }
      # [2026-07-31 09:08:58] 作用：在下次健康探测前等待两秒；理由依据：避免启动阶段对 Qdrant 忙轮询并给集合加载留出时间。
      Start-Sleep -Seconds 2
    }
    # [2026-07-31 09:08:59] 作用：仅在稳定等待窗口耗尽后阻断全栈启动；理由依据：不能把短暂启动抖动当成永久失败，也不能在服务未就绪时报告成功。
    if($null -eq $qdrantResponse -or [string]$qdrantResponse.status -ne 'ok'){
      throw (
        "可信 Qdrant HTTP 验证超时：http://$trustedAddress`:" +
        "$trustedHttpPort/collections；$qdrantLastError"
      )
    }
  }
  Write-Host (
    "可信 Qdrant 私网入口已全部就绪：$trustedAddress`:" +
    '[' + ($TrustedQdrantPorts -join ',') + ']'
  )
}
# [2026-07-28] 作用：验证当前配置的全部关系数据库可信私网入口；理由依据：只创建 portproxy/防火墙不能证明 SQL Server 与 PostgreSQL 的实际 TCP 链路已经可用。
function Assert-TrustedRelationalDatabaseAccess{
  $trustedAddress=(
    [string]$env:SQL_RAG_TRUSTED_RELATIONAL_DATABASE_LISTEN_ADDRESS
  )
  if(
    [string]::IsNullOrWhiteSpace($trustedAddress) -or
    $trustedAddress -eq '127.0.0.1'
  ){return}
  foreach($trustedPort in $TrustedRelationalDatabasePorts){
    $client=New-Object System.Net.Sockets.TcpClient
    try{
      $task=$client.ConnectAsync($trustedAddress,[int]$trustedPort)
      if(-not $task.Wait(5000) -or -not $client.Connected){
        throw (
          "可信关系数据库私网入口未就绪：$trustedAddress`:$trustedPort"
        )
      }
    }finally{
      $client.Close()
    }
  }
  Write-Host (
    "可信关系数据库私网入口已全部就绪：$trustedAddress`:" +
    '[' + ($TrustedRelationalDatabasePorts -join ',') + ']'
  )
}
function Test-Docker{
  if($DockerBackend -eq 'remote_ssh'){
    return [bool](Test-MonFangAiRemoteDocker)
  }
  # [2026-07-07 08:39:10] 作用：为 Docker CLI 健康检查创建唯一临时输出前缀；理由依据：Docker Engine 异常时 stdout/stderr 仍需隔离保存，避免并发启动互相覆盖日志。
  $probePrefix=Join-Path $env:TEMP ("sql-rag-docker-probe-" + [guid]::NewGuid().ToString())
  # [2026-07-07 08:39:10] 作用：声明 Docker CLI 标准输出临时文件；理由依据：Start-Process 需要文件承接输出，才能给 docker info 增加可控超时。
  $probeOut="$probePrefix.out"
  # [2026-07-07 08:39:10] 作用：声明 Docker CLI 标准错误临时文件；理由依据：Docker 未就绪时错误信息不应打断主启动脚本。
  $probeErr="$probePrefix.err"
  try{
    # [2026-07-22 17:08:09] 作用：Windows Server 下通过 WSL2 探测 Linux Docker Engine；理由依据：Docker Desktop 官方不支持 Windows Server，但项目容器均为 Linux 镜像。
    if($DockerBackend -eq 'wsl'){$probeFile='wsl.exe';$probeArguments=@('-d',$DockerWslDistro,'-u','root','--','docker','info')}
    # [2026-07-22 17:08:10] 作用：Windows 11 下继续探测现有 docker.exe；理由依据：保持已验收 Docker Desktop 路径不变。
    else{$probeFile='docker.exe';$probeArguments=@('info')}
    # [2026-07-07 08:39:10] 作用：以独立子进程执行 docker info；理由依据：直接调用 docker info 在容器引擎异常时可能长时间阻塞当前 PS1。
    $probe=Start-Process -FilePath $probeFile -ArgumentList $probeArguments -RedirectStandardOutput $probeOut -RedirectStandardError $probeErr -WindowStyle Hidden -PassThru
    # [2026-07-07 08:39:10] 作用：最多等待 10 秒获取 Docker Engine 状态；理由依据：健康检查必须有上限，避免截图中的启动脚本长时间卡在 Docker 等待。
    if(-not $probe.WaitForExit(10000)){
      # [2026-07-07 08:39:10] 作用：超时时主动结束 docker info 子进程；理由依据：Docker CLI 卡死时必须释放探测进程，保证下一轮等待可继续。
      Stop-Process -Id $probe.Id -Force -ErrorAction SilentlyContinue
      # [2026-07-07 08:39:10] 作用：返回 Docker 未就绪；理由依据：超时说明 Engine 不能稳定响应，本轮不能继续启动依赖 Docker 的容器。
      # [2026-08-03 09:05:51] 作用：保存 Docker CLI 单次探测超时诊断；理由依据：最终失败必须区分 CLI 卡死与 Engine 尚未创建命名管道。
      $script:LastDockerProbeDiagnostic='docker info 单次探测超过10秒'
      return $false
    }
    # [2026-07-07 09:01:20] 作用：刷新 Docker 探测进程对象；理由依据：本机 Start-Process 返回对象可能不回填 ExitCode，必须先刷新再做兼容判断。
    $probe.Refresh()
    # [2026-07-07 09:01:20] 作用：读取 docker info 标准输出文本；理由依据：当 ExitCode 为空但 Engine 已返回 Server 信息时，需要用输出内容判断真实就绪状态。
    $probeStdout=Get-Content -LiteralPath $probeOut -Raw -ErrorAction SilentlyContinue
    # [2026-07-07 09:01:20] 作用：读取 docker info 标准错误文本；理由依据：Docker 未就绪时错误通常写入 stderr，必须排除 failed to connect 等失败状态。
    $probeStderr=Get-Content -LiteralPath $probeErr -Raw -ErrorAction SilentlyContinue
    # [2026-08-03 09:05:52] 作用：保存本轮 Docker stdout 与 stderr 摘要；理由依据：过去循环清理临时文件后只剩“10分钟未就绪”而丢失真实根因。
    $script:LastDockerProbeDiagnostic=((([string]$probeStdout)+"`n"+([string]$probeStderr)).Trim())
    # [2026-07-07 09:01:20] 作用：判断 docker info 是否已经返回服务端版本；理由依据：Server Version 是 Docker Linux Engine 真正响应 API 的可观察证据。
    $probeHasServer=([string]$probeStdout) -match 'Server Version:'
    # [2026-07-07 09:01:20] 作用：判断 docker info 是否出现连接失败文本；理由依据：只看到客户端信息或管道错误时不能继续启动依赖容器的服务。
    $probeHasConnectError=(([string]$probeStdout) + "`n" + ([string]$probeStderr)) -match 'failed to connect|cannot find|The system cannot find|error during connect'
    # [2026-07-07 09:01:20] 作用：优先使用 Docker 输出内容判定 Engine 就绪；理由依据：本机 Start-Process ExitCode 为空但 stdout 已有 Server Version，单看退出码会误判。
    if($probeHasServer -and -not $probeHasConnectError){return $true}
    # [2026-07-07 09:01:20] 作用：保留退出码为 0 的兼容判断；理由依据：其他机器上 ExitCode 正常时仍可按 Docker CLI 标准成功码确认就绪。
    return $probe.ExitCode -eq 0
  }catch{
    # [2026-07-07 08:39:10] 作用：捕获 Docker CLI 启动或探测异常并返回未就绪；理由依据：启动脚本应继续等待或明确超时，而不是被探测异常中断。
    # [2026-08-03 09:05:53] 作用：保存 Docker CLI 无法启动的真实异常；理由依据：PATH 缺失、权限错误和文件损坏不能再被折叠成同一条等待提示。
    $script:LastDockerProbeDiagnostic=$_.Exception.Message
    return $false
  }finally{
    # [2026-07-07 08:39:10] 作用：清理 Docker 探测临时文件；理由依据：高频等待循环不应在 Temp 目录累计无用文件。
    Remove-Item -LiteralPath $probeOut,$probeErr -Force -ErrorAction SilentlyContinue
  }
}
# [2026-08-03 13:38:26] 作用：验证第二套 Windows 工作站的 Docker Desktop 静态运行前置条件；理由依据：V9 第17步未检查宿主机合同，导致程序更新 READY 与 Docker 可运行被错误混为一谈。
function Assert-DockerDesktopRuntimePrerequisites{
  # [2026-08-03 13:38:27] 作用：声明本轮实际使用的 Docker CLI 路径；理由依据：上下文、版本与 JSON 检查必须对应同一个目标安装。
  param([Parameter(Mandatory=$true)][string]$DockerCli)
  # [2026-08-03 13:38:28] 作用：让本地第一套跳过服务器专属宿主机修复；理由依据：共享引擎变更不能改动已经跑通的本地 profile 系统设置。
  # [2026-08-03 15:42:42] 作用：只对第二套独立服务器profile执行宿主机门禁；理由依据：本地第一套不应被服务器Docker恢复策略改变。
  if($DeploymentProfile-ne'server_second_ports'-or-not$usesIndependentServiceProfile){return}
  # [2026-08-03 13:38:29] 作用：读取 Windows 版本与工作站型号；理由依据：Docker Desktop 只在受支持的 Windows 11 客户端系统上运行。
  $operatingSystem=Get-CimInstance Win32_OperatingSystem
  # [2026-08-03 13:38:30] 作用：拒绝把第二套实体工作站入口运行在 Windows Server；理由依据：Docker 官方不支持 Windows Server 上的 Docker Desktop。
  if(([string]$operatingSystem.Caption)-notmatch 'Windows 11'){throw "第二套 Docker Desktop 要求 Windows 11：$($operatingSystem.Caption)"}
  # [2026-08-03 13:38:31] 作用：读取 WSL 与虚拟机平台功能状态；理由依据：WSL2 Linux Engine 缺少任一功能都无法启动 dockerd。
  $requiredFeatures=@('Microsoft-Windows-Subsystem-Linux','VirtualMachinePlatform')|ForEach-Object{Get-WindowsOptionalFeature -Online -FeatureName $_}
  # [2026-08-03 13:38:32] 作用：阻断未启用的 WSL2 必需功能；理由依据：UI 进程和 docker-desktop 发行版存在不能替代功能启用状态。
  if(@($requiredFeatures|Where-Object{$_.State-ne'Enabled'}).Count-ne0){throw ('WSL2 必需功能未启用：'+((@($requiredFeatures|Where-Object{$_.State-ne'Enabled'}|ForEach-Object{$_.FeatureName}))-join','))}
  # [2026-08-03 13:38:33] 作用：读取 Docker 官方要求的 Windows Server 文件服务；理由依据：LanmanServer 必须启用且自动启动才满足 Windows Docker Desktop 系统合同。
  $lanmanServer=Get-Service -Name 'LanmanServer' -ErrorAction Stop
  # [2026-08-03 13:38:34] 作用：把第二套工作站的 LanmanServer 固定为自动启动；理由依据：目标机安全基线可能禁用官方明确要求的系统服务。
  if($lanmanServer.StartType-ne'Automatic'){Set-Service -Name 'LanmanServer' -StartupType Automatic}
  # [2026-08-03 13:38:35] 作用：启动尚未运行的 LanmanServer；理由依据：只修改启动类型不能修复本次登录会话的 Docker 后端依赖。
  if($lanmanServer.Status-ne'Running'){Start-Service -Name 'LanmanServer'}
  # [2026-08-03 13:38:36] 作用：声明两份只读 Docker JSON 配置路径；理由依据：4.84 对损坏 JSON 会明确报错，启动器应在进入长等待前给出准确路径。
  $dockerJsonPaths=@((Join-Path $env:ProgramData 'DockerDesktop\install-settings.json'),(Join-Path $env:USERPROFILE '.docker\config.json'))
  # [2026-08-03 13:38:37] 作用：逐份验证存在且非空的 Docker JSON；理由依据：任何格式损坏都不应继续伪装成 Engine 启动慢。
  foreach($dockerJsonPath in $dockerJsonPaths){if(Test-Path -LiteralPath $dockerJsonPath -PathType Leaf){$dockerJsonText=Get-Content -LiteralPath $dockerJsonPath -Raw -ErrorAction Stop;if([string]::IsNullOrWhiteSpace($dockerJsonText)){throw "Docker JSON 配置为空：$dockerJsonPath"};try{[void]($dockerJsonText|ConvertFrom-Json)}catch{throw "Docker JSON 配置无效：$dockerJsonPath；$($_.Exception.Message)"}}}
  # [2026-08-03 18:04:44] 作用：确认第二套当前进程确实使用profile固定的直连Linux Engine管道；理由依据：HOTFIX1仍强制desktop-linux全局context并重复命中同一Windows API proxy HTTP500。
  if([string]$env:DOCKER_HOST-ne$DockerEngineEndpoint){throw "第二套Docker直连端点未生效：expected=$DockerEngineEndpoint actual=$([string]$env:DOCKER_HOST)"}
  # [2026-08-03 18:04:45] 作用：阻断任何会覆盖第二套直连端点的Docker context环境；理由依据：不能让管理员会话或旧部署变量把CLI重新路由到Desktop代理。
  if(-not[string]::IsNullOrWhiteSpace([string]$env:DOCKER_CONTEXT)){throw "第二套禁止设置DOCKER_CONTEXT：$([string]$env:DOCKER_CONTEXT)"}
  # [2026-08-03 13:38:40] 作用：定位 Docker Desktop 主程序；理由依据：产品版本来自实际安装文件而不是可能漂移的 CLI 插件版本。
  $dockerDesktopExecutable=Join-Path $env:ProgramFiles 'Docker\Docker\Docker Desktop.exe'
  # [2026-08-03 13:38:41] 作用：阻断缺失的全用户 Docker Desktop 安装；理由依据：第二套管理员原生交付固定使用 Program Files 安装模式。
  if(-not(Test-Path -LiteralPath $dockerDesktopExecutable -PathType Leaf)){throw "Docker Desktop 主程序缺失：$dockerDesktopExecutable"}
  # [2026-08-03 13:38:42] 作用：解析目标机 Docker Desktop 产品版本；理由依据：V10 固定要求包含 Windows 启动挂死修复的 4.84.0 或更高版本。
  $dockerDesktopVersion=[version]((Get-Item -LiteralPath $dockerDesktopExecutable).VersionInfo.ProductVersion)
  # [2026-08-03 15:14:39] 作用：拒绝继续使用目标机已复现Engine长时间HTTP500的4.83；理由依据：V12只能在已安装4.84及以上后执行宿主状态机。
  if($dockerDesktopVersion-lt[version]'4.84.0'){throw "Docker Desktop版本过旧：installed=$dockerDesktopVersion required=4.84.0；请先执行最新第17步更新入口。"}
  # [2026-08-03 18:04:46] 作用：输出宿主机与第二套独立直连端点摘要；理由依据：现场必须明确区分Desktop UI状态和实际承载Compose的Linux Engine管道。
  Write-Host "Docker 运行前置检查通过：OS=$($operatingSystem.Caption) build=$($operatingSystem.BuildNumber)；Desktop=$dockerDesktopVersion；engine_endpoint=$DockerEngineEndpoint；global_context_mutation=false；LanmanServer=Running/Automatic。"
}
# [2026-08-03 13:38:45] 作用：等待 Docker Linux Engine 在单次非破坏启动后真实响应；理由依据：第一套成功路径只启动一次并持续探测，不在初始化中途 stop 或关闭 WSL。
function Wait-DockerEngineReady{
  # [2026-08-03 09:06:00] 作用：声明等待秒数；理由依据：首次 WSL2 后端创建和普通冷启动采用不同但有限的等待窗口。
  param([Parameter(Mandatory=$true)][int]$TimeoutSeconds)
  # [2026-08-03 09:06:01] 作用：计算 Docker Engine 等待截止时间；理由依据：任何轮询都必须有确定上限。
  $dockerDeadline=(Get-Date).AddSeconds($TimeoutSeconds)
  # [2026-08-03 13:38:46] 作用：初始化 Docker Engine 探测轮次；理由依据：长窗口只应低频输出进度，避免重复刷屏和干扰后端。
  $dockerProbeAttempt=0
  # [2026-08-03 09:06:02] 作用：循环探测 Docker Server API；理由依据：只有 docker info 返回服务端信息才允许启动容器和模型。
  while((Get-Date) -lt $dockerDeadline){
    # [2026-08-03 13:38:47] 作用：累计本轮 Engine 探测次数；理由依据：控制可观察日志频率且保留等待进度。
    $dockerProbeAttempt++
    # [2026-08-03 09:06:03] 作用：在 Engine 就绪时立即结束等待；理由依据：避免固定睡满窗口增加每次一键启动耗时。
    if(Test-Docker){return $true}
    # [2026-08-03 13:38:48] 作用：每六轮输出一次最后探测摘要；理由依据：用户能看见脚本仍在有界运行且不再出现无限重复窗口。
    if(($dockerProbeAttempt%6)-eq0){Write-Host "等待 Docker Linux Engine 就绪：attempt=$dockerProbeAttempt；最后探测=$script:LastDockerProbeDiagnostic"}
    # [2026-08-03 13:38:49] 作用：等待十秒后再探测；理由依据：减少 docker info 对正在初始化的 WSL dockerd 产生的压力。
    Start-Sleep -Seconds 10
  }
  # [2026-08-03 09:06:05] 作用：返回等待超时结果；理由依据：调用方需要进入一次确定的冷恢复而不是无限重复 start。
  return $false
}
# [2026-08-03 15:13:09] 作用：声明通用外部诊断命令硬超时执行器；理由依据：V11总等待结束后又被无边界Docker和WSL采集阻塞，导致现场永不出红字。
function Invoke-BoundedDiagnosticCommand{
  # [2026-08-03 15:13:10] 作用：接收可执行文件、参数、超时和诊断标签；理由依据：每个宿主机探针都必须有独立的机器可判定边界。
  param([Parameter(Mandatory=$true)][string]$FilePath,[string[]]$ArgumentList=@(),[Parameter(Mandatory=$true)][int]$TimeoutSeconds,[Parameter(Mandatory=$true)][string]$Label)
  # [2026-08-03 15:13:11] 作用：为本次命令创建唯一临时前缀；理由依据：串行诊断也不得相互覆盖标准输出。
  $commandPrefix=Join-Path $env:TEMP ('sql-rag-bounded-diagnostic-'+[guid]::NewGuid().ToString('N'))
  # [2026-08-03 15:13:12] 作用：声明命令标准输出路径；理由依据：超时时仍需保留已产生的部分证据。
  $commandOut=$commandPrefix+'.out.log'
  # [2026-08-03 15:13:13] 作用：声明命令标准错误路径；理由依据：Docker后端错误不能与正常状态文本混淆。
  $commandErr=$commandPrefix+'.err.log'
  # [2026-08-03 15:13:14] 作用：初始化子进程引用；理由依据：异常发生在Start-Process前时也要安全进入清理。
  $commandProcess=$null
  # [2026-08-03 15:13:15] 作用：初始化超时标记；理由依据：JSON必须区分命令失败与命令无响应。
  $commandTimedOut=$false
  # [2026-08-03 15:13:16] 作用：初始化退出码；理由依据：被终止或未启动的命令不得伪装为零退出。
  $commandExitCode=$null
  # [2026-08-03 15:13:17] 作用：初始化命令证据行；理由依据：无输出、超时和异常都需结构稳定。
  $commandLines=@()
  # [2026-08-03 15:14:45] 作用：初始化命令异常字段；理由依据：PowerShell 5.1可能不回填ExitCode，仍需准确区分正常空码与Start-Process异常。
  $commandException=$null
  # [2026-08-03 15:13:18] 作用：开始有界外部命令事务；理由依据：任一探针异常都必须转为诊断内容而不能阻断JSON落盘。
  try{
    # [2026-08-03 15:14:43] 作用：在无参数时以隐藏子进程启动诊断命令；理由依据：Windows PowerShell 5.1会拒绝空ArgumentList而不是将其视为无参数。
    if($ArgumentList.Count-eq0){$commandProcess=Start-Process -FilePath $FilePath -RedirectStandardOutput $commandOut -RedirectStandardError $commandErr -WindowStyle Hidden -PassThru}
    # [2026-08-03 15:14:44] 作用：在存在参数时以隐藏子进程启动诊断命令；理由依据：现场只保留一个PowerShell窗口且输出可受控。
    if($ArgumentList.Count-ne0){$commandProcess=Start-Process -FilePath $FilePath -ArgumentList $ArgumentList -RedirectStandardOutput $commandOut -RedirectStandardError $commandErr -WindowStyle Hidden -PassThru}
    # [2026-08-03 15:13:20] 作用：在超时内等待子进程结束；理由依据：不再允许docker desktop status或wsl.exe无限占用主启动器。
    $commandFinished=$commandProcess.WaitForExit($TimeoutSeconds*1000)
    # [2026-08-03 15:13:21] 作用：在子进程超时时记录确定状态；理由依据：现场需要看到是哪一项宿主命令卡死。
    if(-not$commandFinished){$commandTimedOut=$true}
    # [2026-08-03 15:13:22] 作用：终止超时的受控子进程；理由依据：诊断不应该在后台遗留持续堆积的Docker或WSL探针。
    if(-not$commandFinished){Stop-Process -Id $commandProcess.Id -Force -ErrorAction SilentlyContinue}
    # [2026-08-03 15:13:23] 作用：等待被终止进程释放日志句柄；理由依据：立即读取和删除文件可能再次卡住诊断链。
    if(-not$commandFinished){[void]$commandProcess.WaitForExit(5000)}
    # [2026-08-03 15:14:40] 作用：对已结束子进程执行无参数回收；理由依据：Windows PowerShell 5.1实测中WaitForExit(毫秒)返回成功后ExitCode仍可为空。
    if($commandFinished){$commandProcess.WaitForExit()}
    # [2026-08-03 15:14:41] 作用：刷新已完成子进程对象；理由依据：参数等待与无参数回收后才能稳定读取ExitCode。
    if($commandFinished){$commandProcess.Refresh()}
    # [2026-08-03 15:14:42] 作用：记录正常完成命令的退出码；理由依据：超时进程的强制终止码不具有业务含义。
    if($commandFinished){$commandExitCode=$commandProcess.ExitCode}
    # [2026-08-03 15:14:50] 作用：回读并强制规范化标准输出与错误为纯字符串；理由依据：PowerShell文件提供程序附加的PSPath属性会使诊断JSON膨胀上万字。
    $commandLines=@(Get-Content -LiteralPath $commandOut,$commandErr -ErrorAction SilentlyContinue|ForEach-Object{[string]$_})
  }catch{
    # [2026-08-03 15:13:27] 作用：把诊断执行异常保存为证据行；理由依据：PATH、权限或文件损坏也必须进入同一JSON。
    $commandLines=@($_.Exception.Message)
    # [2026-08-03 15:14:46] 作用：单独保存Start-Process或回收异常；理由依据：调用方不得通过输出文本样式猜测是否执行成功。
    $commandException=$_.Exception.Message
  }finally{
    # [2026-08-03 15:13:28] 作用：清理本次命令临时文件；理由依据：反复一键启动不应在Temp累积日志。
    Remove-Item -LiteralPath $commandOut,$commandErr -Force -ErrorAction SilentlyContinue
  }
  # [2026-08-03 15:14:47] 作用：返回标签、超时、退出码、异常和输出结构；理由依据：调用方不得再依赖PowerShell 5.1可能为空的ExitCode单点判定。
  return [pscustomobject]@{label=$Label;timed_out=$commandTimedOut;exit_code=$commandExitCode;exception=$commandException;lines=@($commandLines)}
}
# [2026-08-03 15:13:30] 作用：保存全部有界Docker Desktop、WSL、Engine、VHD、虚拟化和官方诊断；理由依据：启动失败必须在确定时间内生成可直接分类的JSON。
function Save-DockerStartupDiagnostic{
  # [2026-08-03 15:13:31] 作用：接收实际Docker CLI路径与诊断阶段；理由依据：首次启动与恢复后失败必须分开留证。
  param([Parameter(Mandatory=$true)][string]$DockerCli,[string]$Stage='initial_wait_failed')
  # [2026-08-03 18:04:47] 作用：建立包含实际CLI端点且不含密钥的诊断主对象；理由依据：HOTFIX1的launch_mode标签不能证明CLI真正绕过了Desktop代理，必须记录DOCKER_HOST事实。
  $dockerDiagnostic=[ordered]@{timestamp=(Get-Date).ToString('o');deployment_profile=$DeploymentProfile;stage=$Stage;docker_host=[string]$env:DOCKER_HOST;docker_context=[string]$env:DOCKER_CONTEXT;last_probe=[string]$script:LastDockerProbeDiagnostic;all_external_probes_bounded=$true}
  # [2026-08-03 15:13:33] 作用：初始化故障分类；理由依据：后续只能按命中证据选择恢复分支。
  $script:LastDockerFailureClassification='unknown'
  # [2026-08-03 15:13:34] 作用：输出有界诊断阶段进度；理由依据：现场不能再将诊断运行误判为脚本永久卡死。
  Write-Host "Docker启动进入有界诊断：stage=$Stage；每个Docker/WSL子命令均有独立超时。"
  # [2026-08-03 15:13:35] 作用：有界采集Docker Desktop状态；理由依据：V11正是在该直接调用中无限等待。
  $desktopStatus=Invoke-BoundedDiagnosticCommand -FilePath $DockerCli -ArgumentList @('desktop','status','--format','json') -TimeoutSeconds 8 -Label 'docker_desktop_status'
  # [2026-08-03 15:13:36] 作用：有界采集WSL版本；理由依据：版本与发行版状态需分别判定。
  $wslVersion=Invoke-BoundedDiagnosticCommand -FilePath 'wsl.exe' -ArgumentList @('--version') -TimeoutSeconds 8 -Label 'wsl_version'
  # [2026-08-03 15:13:37] 作用：有界采集WSL发行版状态；理由依据：docker-desktop未注册、Stopped和Running的恢复方式不同。
  $wslDistributions=Invoke-BoundedDiagnosticCommand -FilePath 'wsl.exe' -ArgumentList @('--list','--verbose') -TimeoutSeconds 8 -Label 'wsl_distributions'
  # [2026-08-03 15:13:38] 作用：有界采集docker-desktop文件系统容量；理由依据：VHD满盘不得被误修为重装或端口补丁。
  $wslDisk=Invoke-BoundedDiagnosticCommand -FilePath 'wsl.exe' -ArgumentList @('-d','docker-desktop','-u','root','--','df','-h') -TimeoutSeconds 12 -Label 'wsl_disk'
  # [2026-08-03 15:13:39] 作用：有界采集docker-desktop inode使用率；理由依据：小文件耗尽inode时剩余字节不能反映真实故障。
  $wslInodes=Invoke-BoundedDiagnosticCommand -FilePath 'wsl.exe' -ArgumentList @('-d','docker-desktop','-u','root','--','df','-i') -TimeoutSeconds 12 -Label 'wsl_inodes'
  # [2026-08-03 15:13:40] 作用：有界采集docker-desktop全部进程；理由依据：dockerd、containerd或wsl-bootstrap缺失是Engine API无响应的直接分支证据。
  $wslProcesses=Invoke-BoundedDiagnosticCommand -FilePath 'wsl.exe' -ArgumentList @('-d','docker-desktop','-u','root','--','ps','-ef') -TimeoutSeconds 12 -Label 'wsl_processes'
  # [2026-08-03 15:13:41] 作用：有界采集Docker boot日志；理由依据：需同时保留首次启动失败与末尾重复症状。
  $desktopLogs=Invoke-BoundedDiagnosticCommand -FilePath $DockerCli -ArgumentList @('desktop','logs','--boot','0') -TimeoutSeconds 25 -Label 'docker_desktop_logs'
  # [2026-08-03 17:14:30] 作用：定位Docker官方诊断工具；理由依据：自建探针不能取代产品自身完整诊断包。
  $dockerDiagnoseExecutable=Join-Path $env:ProgramFiles 'Docker\Docker\resources\com.docker.diagnose.exe'
  # [2026-08-03 17:14:31] 作用：生成本轮Docker官方gather诊断包路径；理由依据：4.84已废弃check命令，V12采到的只有弃用提示而非产品证据。
  $officialBundlePath=Join-Path $LogDir ('docker-diagnostics-'+(Get-Date -Format 'yyyyMMdd-HHmmss')+'.zip')
  # [2026-08-03 17:14:32] 作用：在工具存在时有界执行官方gather且不上传；理由依据：完整诊断必须留在本机并受硬超时约束。
  $officialDiagnose=if(Test-Path -LiteralPath $dockerDiagnoseExecutable -PathType Leaf){Invoke-BoundedDiagnosticCommand -FilePath $dockerDiagnoseExecutable -ArgumentList @('gather',$officialBundlePath) -TimeoutSeconds 90 -Label 'docker_official_gather'}else{[pscustomobject]@{label='docker_official_gather';timed_out=$false;exit_code=$null;exception=$null;lines=@("missing: $dockerDiagnoseExecutable")}}
  # [2026-08-03 17:14:33] 作用：把实际生成的官方诊断包路径附加到探针结果；理由依据：JSON不能只记录命令退出码而丢失可交付制品位置。
  $officialDiagnose|Add-Member -NotePropertyName bundle_path -NotePropertyValue $(if(Test-Path -LiteralPath $officialBundlePath -PathType Leaf){$officialBundlePath}else{$null}) -Force
  # [2026-08-03 15:13:44] 作用：采集Windows虚拟化实际运行态；理由依据：只启用Windows可选功能不能证明当前开机已加载Hypervisor。
  $virtualizationState=Get-CimInstance Win32_ComputerSystem|Select-Object HypervisorPresent,Manufacturer,Model
  # [2026-08-03 15:13:45] 作用：采集Windows服务状态；理由依据：com.docker.service、LxssManager和虚拟化计算服务的故障需独立判定。
  $windowsServices=@(Get-Service -Name 'com.docker.service','LxssManager','vmcompute' -ErrorAction SilentlyContinue|Select-Object Name,Status,StartType)
  # [2026-08-03 15:13:46] 作用：采集Docker Desktop相关Windows进程；理由依据：只有UI、backend重复或跨会话启动都会影响恢复选择。
  $windowsProcesses=@(Get-Process -ErrorAction SilentlyContinue|Where-Object{$_.ProcessName -like '*docker*'}|Select-Object ProcessName,Id,SessionId)
  # [2026-08-03 18:04:48] 作用：只读确认第二套直连Linux Engine命名管道是否存在；理由依据：内部dockerd日志ready不等于Windows直连管道已经发布。
  $directEnginePipePresent=@(Get-ChildItem -LiteralPath '\\.\pipe\' -ErrorAction SilentlyContinue|Where-Object{$_.Name-eq'docker_engine_linux'}).Count-gt0
  # [2026-08-03 15:13:47] 作用：定位Docker WSL数据目录；理由依据：任何恢复前都必须明确VHD是否存在以及字节规模。
  $dockerWslRoot=Join-Path $env:LOCALAPPDATA 'Docker\wsl'
  # [2026-08-03 15:13:48] 作用：只读列出Docker WSL VHD文件元数据；理由依据：不得在不知道数据盘位置时运行注销、清理或重置。
  $dockerVhds=@(Get-ChildItem -LiteralPath $dockerWslRoot -Filter '*.vhdx' -File -Recurse -ErrorAction SilentlyContinue|Select-Object FullName,Length,LastWriteTimeUtc)
  # [2026-08-03 15:13:49] 作用：筛选可能解释Engine故障的日志行；理由依据：重复普通信息不应淹没首个panic、bootstrap或HTTP500。
  $desktopRootCauseLines=@($desktopLogs.lines|Where-Object{$_-match 'engine|wsl|bootstrap|panic|failed|failure|error|fatal|timeout|proxy|auth\.enforcer|HTTP 500|_ping'})
  # [2026-08-03 17:14:34] 作用：合并全部诊断文本；理由依据：故障分类需同时考虑WSL进程、Docker日志和官方gather。
  $combinedDiagnosticText=((@($desktopRootCauseLines)+@($wslProcesses.lines)+@($officialDiagnose.lines))-join"`n")
  # [2026-08-03 15:14:51] 作用：生成Docker boot日志命令的紧凑元数据；理由依据：完整一百万字节日志与根因首尾重复，使现场JSON无法快速回读。
  $desktopLogsCompact=[pscustomobject]@{label=$desktopLogs.label;timed_out=$desktopLogs.timed_out;exit_code=$desktopLogs.exit_code;exception=$desktopLogs.exception;total_lines=@($desktopLogs.lines).Count;root_cause_lines=@($desktopRootCauseLines).Count}
  # [2026-08-03 15:13:51] 作用：识别宿主Hypervisor未加载；理由依据：该状态必须通过开机配置与重启恢复而不是修端口。
  if($virtualizationState.HypervisorPresent-eq$false){$script:LastDockerFailureClassification='hypervisor_not_running'}
  # [2026-08-03 15:13:52] 作用：识别任一docker-desktop WSL内部探针超时；理由依据：这说明故障位于Linux VM进入层而不是Docker CLI context。
  elseif($wslDisk.timed_out-or$wslInodes.timed_out-or$wslProcesses.timed_out){$script:LastDockerFailureClassification='docker_wsl_probe_timeout'}
  # [2026-08-03 18:04:49] 作用：优先识别第二套直连Linux Engine管道缺失或未响应；理由依据：V12.2禁止再用Desktop代理HTTP500掩盖本次实际DOCKER_HOST失败。
  elseif($usesIndependentServiceProfile-and(-not$directEnginePipePresent-or([string]$script:LastDockerProbeDiagnostic)-match'docker_engine_linux')){$script:LastDockerFailureClassification='direct_linux_engine_pipe_missing_or_unresponsive'}
  # [2026-08-03 17:14:35] 作用：识别Linux daemon已就绪而Windows API proxy仍返回HTTP500；理由依据：目标机两轮V12日志均明确出现daemon ready、engine running及随后持续_ping HTTP500。
  elseif(($combinedDiagnosticText-match 'docker daemon is ready')-and($combinedDiagnosticText-match 'engine linux/wsl.*running')-and($combinedDiagnosticText-match 'waiting for the engine to respond to _ping')-and($combinedDiagnosticText-match 'HTTP 500')){$script:LastDockerFailureClassification='windows_api_proxy_http_500_after_internal_engine_ready'}
  # [2026-08-03 17:14:36] 作用：保留缺少内部Engine就绪证据时的通用HTTP500类别；理由依据：不同宿主故障不得被新专用分类错误合并。
  elseif(($combinedDiagnosticText-match 'waiting for the engine to respond to _ping')-and($combinedDiagnosticText-match 'HTTP 500')){$script:LastDockerFailureClassification='engine_ping_http_500'}
  # [2026-08-03 15:13:54] 作用：识别dockerd或containerd未创建；理由依据：WSL可进入但核心进程缺失时需进入Desktop恢复而不是业务Compose。
  elseif((($wslProcesses.lines-join"`n")-notmatch 'dockerd')-or(($wslProcesses.lines-join"`n")-notmatch 'containerd')){$script:LastDockerFailureClassification='docker_daemon_process_missing'}
  # [2026-08-03 15:13:55] 作用：识别Docker WSL数据VHD缺失；理由依据：无数据盘时不得继续假设现有容器可恢复。
  elseif($dockerVhds.Count-eq0){$script:LastDockerFailureClassification='docker_wsl_vhd_missing'}
  # [2026-08-03 15:14:52] 作用：写入全部有界探针及紧凑日志元数据；理由依据：现场不再复制多条命令也不会因重复日志撑大JSON。
  $dockerDiagnostic.probes=[ordered]@{desktop_status=$desktopStatus;wsl_version=$wslVersion;wsl_distributions=$wslDistributions;wsl_disk=$wslDisk;wsl_inodes=$wslInodes;wsl_processes=$wslProcesses;desktop_logs=$desktopLogsCompact;official_diagnose=$officialDiagnose}
  # [2026-08-03 18:04:50] 作用：写入Windows宿主运行态及直连管道事实；理由依据：虚拟化、服务、会话进程和docker_engine_linux发布状态必须共同交付。
  $dockerDiagnostic.windows=[ordered]@{virtualization=$virtualizationState;services=$windowsServices;processes=$windowsProcesses;direct_linux_engine_pipe_present=$directEnginePipePresent}
  # [2026-08-03 15:13:58] 作用：写入Docker VHD元数据；理由依据：后续任何可能影响数据的步骤都必须先以该清单为保护边界。
  $dockerDiagnostic.docker_vhds=$dockerVhds
  # [2026-08-03 15:13:59] 作用：保存根因日志首尾样本；理由依据：限制JSON体积的同时保留首次与最终故障。
  $dockerDiagnostic.root_cause=[ordered]@{first=@($desktopRootCauseLines|Select-Object -First 250);last=@($desktopRootCauseLines|Select-Object -Last 250)}
  # [2026-08-03 15:14:00] 作用：写入最终故障分类；理由依据：JSON和控制台必须输出同一准信。
  $dockerDiagnostic.failure_classification=$script:LastDockerFailureClassification
  # [2026-08-03 15:14:01] 作用：生成本次诊断JSON路径；理由依据：每次冷启动需要独立证据且不覆盖旧记录。
  $dockerDiagnosticPath=Join-Path $LogDir ('docker-startup-'+(Get-Date -Format 'yyyyMMdd-HHmmss')+'.json')
  # [2026-08-03 15:14:02] 作用：以UTF-8写入结构化诊断；理由依据：即使所有外部探针失败也必须落盘返回。
  $dockerDiagnostic|ConvertTo-Json -Depth 10|Set-Content -LiteralPath $dockerDiagnosticPath -Encoding UTF8
  # [2026-08-03 15:14:03] 作用：返回诊断JSON路径；理由依据：启动器只通过该事实源选择恢复或阻断。
  return $dockerDiagnosticPath
}
# [2026-08-03 15:14:04] 作用：声明同一开机周期最多执行一次的Docker Desktop非破坏恢复器；理由依据：无状态重启会重现V9的stop/start循环并继续浪费时间。
function Invoke-DockerDesktopRecoveryOnce{
  # [2026-08-03 15:14:05] 作用：接收Docker CLI路径与实际Desktop版本；理由依据：恢复状态必须与当前二进制和开机标识共同绑定。
  param([Parameter(Mandatory=$true)][string]$DockerCli,[Parameter(Mandatory=$true)][string]$DockerDesktopVersion)
  # [2026-08-03 15:14:06] 作用：定位宿主恢复状态JSON；理由依据：重复执行固定入口也必须知道本轮开机已做过恢复。
  $recoveryStatePath=Join-Path $LogDir 'docker-host-recovery-state.json'
  # [2026-08-03 15:14:07] 作用：读取Windows当前开机标识；理由依据：重启Windows后才允许新一轮宿主恢复。
  $bootIdentity=(Get-CimInstance Win32_OperatingSystem).LastBootUpTime.ToUniversalTime().ToString('o')
  # [2026-08-03 15:14:08] 作用：初始化旧恢复状态；理由依据：首次部署不存在JSON也必须正常进入恢复。
  $previousRecoveryState=$null
  # [2026-08-03 15:14:09] 作用：安全回读旧恢复JSON；理由依据：损坏的状态文件不得让一键入口无说明退出。
  if(Test-Path -LiteralPath $recoveryStatePath -PathType Leaf){try{$previousRecoveryState=Get-Content -LiteralPath $recoveryStatePath -Raw -Encoding UTF8|ConvertFrom-Json}catch{$previousRecoveryState=$null}}
  # [2026-08-03 15:14:10] 作用：判断当前开机和Docker版本是否已执行过恢复；理由依据：同一故障不得因用户重跑命令而循环restart。
  $alreadyAttempted=($null-ne$previousRecoveryState-and[string]$previousRecoveryState.boot_identity-eq$bootIdentity-and[string]$previousRecoveryState.docker_desktop_version-eq$DockerDesktopVersion)
  # [2026-08-03 15:14:11] 作用：在本轮开机已恢复时设置专用分类；理由依据：现场应转入Windows重启或数据保护修复而不是继续循环。
  if($alreadyAttempted){$script:LastDockerFailureClassification='recovery_already_attempted_same_boot'}
  # [2026-08-03 15:14:12] 作用：在同开机周期重复调用时返回失败；理由依据：严格保证官方restart最多执行一次。
  if($alreadyAttempted){return $false}
  # [2026-08-03 15:14:13] 作用：定位Docker WSL数据根；理由依据：恢复前必须记录数据VHD而不是盲目重置。
  $dockerWslRoot=Join-Path $env:LOCALAPPDATA 'Docker\wsl'
  # [2026-08-03 15:14:14] 作用：采集恢复前Docker VHD元数据；理由依据：本状态机承诺不删除、注销或覆盖这些数据盘。
  $protectedVhds=@(Get-ChildItem -LiteralPath $dockerWslRoot -Filter '*.vhdx' -File -Recurse -ErrorAction SilentlyContinue|Select-Object FullName,Length,LastWriteTimeUtc)
  # [2026-08-03 15:14:15] 作用：在任何restart前落盘已开始状态；理由依据：即使PowerShell被意外关闭也不得在下次启动重复恢复。
  $recoveryState=[ordered]@{schema_version=1;boot_identity=$bootIdentity;docker_desktop_version=$DockerDesktopVersion;started_at=(Get-Date).ToString('o');status='attempting';protected_vhds=$protectedVhds;operation='docker desktop restart';data_destructive_actions=@()}
  # [2026-08-03 15:14:16] 作用：写入恢复事务初始JSON；理由依据：状态机必须跨进程保持幂等。
  $recoveryState|ConvertTo-Json -Depth 8|Set-Content -LiteralPath $recoveryStatePath -Encoding UTF8
  # [2026-08-03 15:14:17] 作用：告知现场正在执行唯一非破坏恢复；理由依据：操作员必须能区分有界restart与黑窗口卡死。
  Write-Host 'Docker Engine首轮未就绪；同一开机周期执行唯一一次Docker官方非破坏restart，不关闭WSL、不清空数据。'
  # [2026-08-03 15:14:18] 作用：有界调用Docker官方restart；理由依据：即使产品CLI在Engine卡死时不返回，主启动器也会继续进入验证。
  $restartResult=Invoke-BoundedDiagnosticCommand -FilePath $DockerCli -ArgumentList @('desktop','restart') -TimeoutSeconds 120 -Label 'docker_desktop_restart_once'
  # [2026-08-03 15:14:19] 作用：记录restart命令结果；理由依据：成功、非零退出与超时必须在同一恢复JSON中留证。
  $recoveryState.restart_result=$restartResult
  # [2026-08-03 15:14:20] 作用：在restart后有界等待真实Engine API；理由依据：CLI退出不代表dockerd已能承接Compose。
  $engineRecovered=Wait-DockerEngineReady -TimeoutSeconds 180
  # [2026-08-03 15:14:21] 作用：写入恢复最终状态；理由依据：下一次固定入口必须按事实跳过或直接复用。
  $recoveryState.status=if($engineRecovered){'recovered'}else{'failed'}
  # [2026-08-03 15:14:22] 作用：记录恢复完成时间；理由依据：现场可审计restart和Engine等待的真实耗时。
  $recoveryState.completed_at=(Get-Date).ToString('o')
  # [2026-08-03 15:14:23] 作用：回写恢复最终JSON；理由依据：重跑和重启后的分支选择需依赖稳定事实源。
  $recoveryState|ConvertTo-Json -Depth 8|Set-Content -LiteralPath $recoveryStatePath -Encoding UTF8
  # [2026-08-03 15:14:24] 作用：返回Engine是否恢复；理由依据：只有docker info真实就绪才允许后续Compose和22端口。
  return $engineRecovered
}
# [2026-08-03 17:14:14] 作用：以当前登录会话的标准Explorer令牌启动Docker Desktop；理由依据：第一套成功形态是普通UI令牌加管理员CLI，而目标机V12从管理员入口直接Start-Process导致Windows API proxy持续HTTP500。
function Start-DockerDesktopForInteractiveUser{
  # [2026-08-03 17:14:15] 作用：接收已验证的Docker Desktop主程序路径；理由依据：启动函数不得自行猜测安装位置。
  param([Parameter(Mandatory=$true)][string]$DockerDesktopExecutable)
  # [2026-08-03 17:14:16] 作用：取得当前PowerShell所在交互会话；理由依据：不能复用其他远程桌面会话中的Docker UI。
  $currentSessionId=(Get-Process -Id $PID).SessionId
  # [2026-08-03 17:14:17] 作用：检查当前会话已有Docker Desktop UI；理由依据：重复创建会导致后台竞争和多窗口。
  $existingDesktopProcess=Get-Process -Name 'Docker Desktop' -ErrorAction SilentlyContinue|Where-Object{$_.SessionId-eq$currentSessionId}|Select-Object -First 1
  # [2026-08-03 17:14:18] 作用：已有当前会话UI时直接返回；理由依据：该函数只负责确保单实例启动。
  if($null-ne$existingDesktopProcess){return $existingDesktopProcess}
  # [2026-08-03 17:14:19] 作用：普通用户入口继续直接启动Docker Desktop；理由依据：保持已跑通第一套本地逻辑和令牌完全不变。
  if(-not$isAdministrator){return Start-Process -FilePath $DockerDesktopExecutable -WindowStyle Hidden -PassThru}
  # [2026-08-04 08:31:06] 作用：阻断不属于任一固定wrapper的管理员调用；理由依据：第一套与第二套均可编排自己的合同，但共享引擎不能成为任意提升Desktop进程的入口。
  if(-not($isServerAdministratorEntry-or$isLocalAdministratorEntry)){throw '管理员调用缺少第一套或第二套固定入口合同，拒绝启动Docker Desktop。'}
  # [2026-08-03 17:14:21] 作用：查找当前会话的Explorer桌面Shell；理由依据：只有Explorer持有与管理员终端分离的交互标准令牌。
  $explorerProcess=Get-Process -Name 'explorer' -ErrorAction SilentlyContinue|Where-Object{$_.SessionId-eq$currentSessionId}|Select-Object -First 1
  # [2026-08-04 08:31:07] 作用：在没有交互Shell时立即阻断；理由依据：两套Docker Desktop入口都必须运行在真实桌面登录会话，不能由计划任务或服务会话伪装。
  if($null-eq$explorerProcess){throw 'interactive_explorer_shell_missing：请登录Windows桌面后在该会话运行对应固定入口。'}
  # [2026-08-03 17:14:23] 作用：连接当前桌面Shell COM服务；理由依据：通过Explorer ShellExecute才能避免Docker Desktop继承管理员PowerShell完整令牌。
  $interactiveShell=New-Object -ComObject Shell.Application
  # [2026-08-03 17:14:24] 作用：由Explorer以标准交互令牌启动Docker Desktop；理由依据：管理员入口只保留业务CLI权限，不再直接创建Desktop UI和Windows API proxy。
  $interactiveShell.ShellExecute($DockerDesktopExecutable,'',(Split-Path -Parent $DockerDesktopExecutable),'open',0)
  # [2026-08-03 17:14:25] 作用：释放Shell COM引用；理由依据：固定入口结束后不得长期持有Explorer自动化对象。
  [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($interactiveShell)
  # [2026-08-03 17:14:26] 作用：为UI进程创建设置短截止时间；理由依据：ShellExecute返回不代表进程已登记，但也不能无界等待。
  $desktopProcessDeadline=(Get-Date).AddSeconds(15)
  # [2026-08-03 17:14:27] 作用：短轮询当前会话Docker Desktop进程；理由依据：后续Engine等待前先确认Explorer启动请求确实生效。
  do{$launchedDesktopProcess=Get-Process -Name 'Docker Desktop' -ErrorAction SilentlyContinue|Where-Object{$_.SessionId-eq$currentSessionId}|Select-Object -First 1;if($null-ne$launchedDesktopProcess){return $launchedDesktopProcess};Start-Sleep -Milliseconds 500}while((Get-Date)-lt$desktopProcessDeadline)
  # [2026-08-03 17:14:28] 作用：在Explorer未创建UI时给出确定错误；理由依据：不进入后续120秒Engine等待掩盖令牌或桌面会话问题。
  throw 'docker_desktop_explorer_launch_failed：Explorer未在15秒内创建Docker Desktop进程。'
}
function Ensure-Docker{
  if(Test-Docker){Write-Host 'Docker Engine 已就绪。'; return}
  if($DockerBackend -eq 'remote_ssh'){
    Invoke-MonFangAiRemoteCommand `
      -Command 'set -euo pipefail; sudo -n systemctl start docker'
    $deadline=(Get-Date).AddMinutes(5)
    while((Get-Date) -lt $deadline){
      if(Test-Docker){
        Write-Host "远程 Linux Docker Engine 已就绪：$($RemoteDockerSettings.Host)"
        return
      }
      Write-Host '等待远程 Linux Docker Engine 启动中...'
      Start-Sleep -Seconds 5
    }
    throw '远程 Linux Docker Engine 5分钟内没有就绪'
  }
  # [2026-07-22 17:08:11] 作用：Windows Server 下启动 WSL2 内的 docker.service；理由依据：同一条一键命令必须能自行拉起容器引擎，且不能依赖不受支持的 Docker Desktop。
  if($DockerBackend -eq 'wsl'){
    & wsl.exe -d $DockerWslDistro -u root -- systemctl start docker
    if($LASTEXITCODE -ne 0){throw "WSL Docker Engine 启动失败：distro=$DockerWslDistro"}
    $deadline=(Get-Date).AddMinutes(10)
    while((Get-Date) -lt $deadline){
      if(Test-Docker){Write-Host "WSL Docker Engine 已就绪：$DockerWslDistro"; return}
      Write-Host '等待 WSL2 / Linux Docker Engine 启动中...'
      Start-Sleep -Seconds 5
    }
    throw 'WSL Docker Engine 10分钟内没有就绪'
  }
  # [2026-08-03 09:06:16] 作用：优先定位当前 PATH 中的 Docker CLI；理由依据：离线安装后的实际版本和插件必须由同一 docker.exe 管理。
  $dockerCliCommand=Get-Command docker.exe -ErrorAction SilentlyContinue|Select-Object -First 1
  # [2026-08-03 09:06:17] 作用：读取已解析 Docker CLI 路径；理由依据：生命周期命令不得依赖管理员窗口与普通窗口不同的 PATH。
  $dockerCli=if($dockerCliCommand){[string]$dockerCliCommand.Source}else{''}
  # [2026-08-03 09:06:18] 作用：PATH 缺失时回落到 Docker Desktop 标准安装目录；理由依据：新服务器首次登录可能尚未刷新机器 PATH。
  if([string]::IsNullOrWhiteSpace($dockerCli)){$dockerCli=Join-Path $env:ProgramFiles 'Docker\Docker\resources\bin\docker.exe'}
  # [2026-08-03 09:06:19] 作用：阻断缺失的 Docker CLI；理由依据：只有 Desktop UI 可执行文件无法完成可诊断的 daemon 和生命周期管理。
  if(-not (Test-Path -LiteralPath $dockerCli -PathType Leaf)){throw "找不到 Docker CLI：$dockerCli"}
  # [2026-08-03 13:39:03] 作用：验证或修复第二套宿主机静态 Docker 前置条件；理由依据：版本、系统服务、context 与 JSON 问题必须早于任何启动等待失败。
  Assert-DockerDesktopRuntimePrerequisites -DockerCli $dockerCli
  # [2026-08-03 13:39:04] 作用：定位 Docker Desktop 图形入口；理由依据：第一套成功逻辑依赖真实交互式 Desktop 进程而不是同步生命周期命令。
  $dockerDesktopExecutable=Join-Path $env:ProgramFiles 'Docker\Docker\Docker Desktop.exe'
  # [2026-08-03 13:39:05] 作用：阻断缺失的 Docker Desktop 主程序；理由依据：仅有 docker.exe 无法创建 Windows 11 WSL2 后端。
  if(-not(Test-Path -LiteralPath $dockerDesktopExecutable -PathType Leaf)){throw "找不到 Docker Desktop：$dockerDesktopExecutable"}
  # [2026-08-03 17:14:29] 作用：按第一套已验证令牌边界确保当前会话只有一个Docker Desktop UI；理由依据：第二套管理员入口不得再直接创建提升的Windows API proxy进程。
  [void](Start-DockerDesktopForInteractiveUser -DockerDesktopExecutable $dockerDesktopExecutable)
  # [2026-08-04 08:31:08] 作用：让第一套恢复原有单次启动与十分钟纯等待路径；理由依据：第二套新增的120秒诊断、直连管道和restart状态机不得改变已跑通local行为。
  if(-not$usesIndependentServiceProfile){Write-Host 'Docker Desktop只启动一次；第一套沿用既有desktop-linux context，最长等待10分钟，不执行第二套宿主恢复状态机。';if(Wait-DockerEngineReady -TimeoutSeconds 600){Write-Host 'Docker Engine 已就绪。';return};throw '本地第一套 Docker Engine 10分钟内没有就绪；未执行第二套直连管道诊断或restart。'}
  # [2026-08-04 08:31:09] 作用：说明第二套直连Engine的确定边界；理由依据：只有独立server_second_ports合同才使用docker_engine_linux、120秒诊断与专属恢复。
  Write-Host "Docker Desktop只启动一次；第二套仅探测直连Engine端点 $DockerEngineEndpoint，首轮上限120秒，不使用或修改全局Docker context。"
  # [2026-08-03 15:14:26] 作用：在单次启动后最多等待120秒的真实Engine Server API；理由依据：目标机42轮同类超时已证明继续等待不会改变故障类别。
  if(Wait-DockerEngineReady -TimeoutSeconds 120){Write-Host 'Docker Engine 已就绪。';return}
  # [2026-08-03 15:14:27] 作用：保存首轮失败的全部有界诊断；理由依据：只允许根据实际命中的宿主分类选择恢复。
  $initialDockerDiagnosticPath=Save-DockerStartupDiagnostic -DockerCli $dockerCli -Stage 'initial_wait_failed'
  # [2026-08-03 15:14:28] 作用：记录首轮诊断得出的故障分类；理由依据：恢复后重新采集可能改写全局分类。
  $initialDockerFailureClassification=$script:LastDockerFailureClassification
  # [2026-08-03 18:04:52] 作用：在第二套直连Linux Engine管道缺失或未响应时立即停止；理由依据：不得再退回已知HTTP500的Desktop代理，也不得用restart循环掩盖独立端点合同失败。
  if($usesIndependentServiceProfile-and$initialDockerFailureClassification-eq'direct_linux_engine_pipe_missing_or_unresponsive'){throw "第二套Docker直连Engine管道未就绪；classification=$initialDockerFailureClassification；docker_host=$DockerEngineEndpoint；diagnostic=$initialDockerDiagnosticPath；fallback_to_desktop_proxy=false；data_destructive_actions=0"}
  # [2026-08-03 17:14:37] 作用：对内部Engine已就绪但Windows API proxy HTTP500立即停止重复restart；理由依据：目标机V12已实证同一开机周期官方restart后分类完全不变。
  # [2026-08-03 18:04:53] 作用：保留Desktop代理故障证据但明确第二套不会使用该端点；理由依据：若直连探针仍未成功，必须报告实际DOCKER_HOST而不能再把launch_mode标签当作根因结论。
  if($usesIndependentServiceProfile-and$initialDockerFailureClassification-eq'windows_api_proxy_http_500_after_internal_engine_ready'){throw "Docker Desktop代理仍为HTTP500且第二套直连Engine尚未成功；classification=$initialDockerFailureClassification；docker_host=$DockerEngineEndpoint；diagnostic=$initialDockerDiagnosticPath；fallback_to_desktop_proxy=false；data_destructive_actions=0"}
  # [2026-08-03 15:14:29] 作用：解析当前Docker Desktop产品版本；理由依据：恢复幂等键必须在升级后自动更换。
  $dockerDesktopVersion=[string](Get-Item -LiteralPath $dockerDesktopExecutable).VersionInfo.ProductVersion
  # [2026-08-03 15:14:30] 作用：尝试同开机周期唯一一次官方非破坏恢复；理由依据：restart不删除VHD、发行版、镜像、容器或卷。
  $dockerRecovered=Invoke-DockerDesktopRecoveryOnce -DockerCli $dockerCli -DockerDesktopVersion $dockerDesktopVersion
  # [2026-08-03 15:14:31] 作用：在恢复后Engine就绪时继续全栈；理由依据：真实docker info已通过时不应要求手工重跑固定命令。
  if($dockerRecovered){Write-Host 'Docker Engine经唯一非破坏恢复后已就绪。';return}
  # [2026-08-03 15:14:32] 作用：保存恢复仍失败的第二份有界诊断；理由依据：恢复前后证据差异决定是否需要Windows重启或VHD保护修复。
  $finalDockerDiagnosticPath=Save-DockerStartupDiagnostic -DockerCli $dockerCli -Stage 'official_restart_failed'
  # [2026-08-03 15:14:33] 作用：以可操作的下一步和两份诊断阻断全栈；理由依据：故障仍在Docker/WSL宿主层，Compose、模型和22端口不得部分启动。
  throw "Docker/WSL宿主恢复失败；initial_classification=$initialDockerFailureClassification；final_classification=$script:LastDockerFailureClassification；initial_diagnostic=$initialDockerDiagnosticPath；final_diagnostic=$finalDockerDiagnosticPath；next_action=restart_windows_once_then_rerun_same_entrypoint；data_destructive_actions=0"
}
# [2026-08-03 09:06:30] 作用：以独立进程和硬超时执行在线权威库克隆；理由依据：连接、锁或大表异常不能再次无限阻塞全部 WebUI 启动。
function Invoke-BoundedOnlineClone{
  # [2026-08-03 09:06:31] 作用：接收在线克隆总秒数上限；理由依据：连接超时只覆盖建连，完整事务仍必须有父进程边界。
  param([Parameter(Mandatory=$true)][int]$TimeoutSeconds)
  # [2026-08-03 09:06:32] 作用：生成在线克隆日志时间戳；理由依据：超时、退出码和数据库异常需要保留独立证据。
  $onlineCloneStamp=Get-Date -Format 'yyyyMMdd-HHmmss'
  # [2026-08-03 09:06:33] 作用：生成在线克隆标准输出日志；理由依据：成功时的表数和行数不能因独立进程执行而丢失。
  $onlineCloneOut=Join-Path $LogDir "wkt-online-clone-$onlineCloneStamp.out.log"
  # [2026-08-03 09:06:34] 作用：生成在线克隆标准错误日志；理由依据：网络、锁和字段适配错误必须可直接定位。
  $onlineCloneErr=Join-Path $LogDir "wkt-online-clone-$onlineCloneStamp.err.log"
  # [2026-08-03 09:06:35] 作用：为含空格的克隆脚本路径增加命令行引号；理由依据：D:\MonFangAI 与开发目录都必须从任意当前目录稳定执行。
  $onlineCloneArguments='"'+$CloneAiErpScript+'"'
  # [2026-08-03 09:06:36] 作用：以独立 Python 进程启动在线克隆并重定向日志；理由依据：父启动器必须能在总超时后可靠结束该事务连接。
  $onlineCloneProcess=Start-Process -FilePath $Py -ArgumentList $onlineCloneArguments -WorkingDirectory $SqlRag -RedirectStandardOutput $onlineCloneOut -RedirectStandardError $onlineCloneErr -WindowStyle Hidden -PassThru
  # [2026-08-03 09:06:37] 作用：按毫秒硬上限等待完整在线克隆；理由依据：任何数据库状态都不能让一键启动永久停在无输出阶段。
  $onlineCloneFinished=$onlineCloneProcess.WaitForExit($TimeoutSeconds*1000)
  # [2026-08-03 09:06:38] 作用：在超时后结束在线克隆进程；理由依据：连接关闭会让 PostgreSQL 回滚未提交的 DROP/CREATE/COPY 原子事务。
  if(-not $onlineCloneFinished){Stop-Process -Id $onlineCloneProcess.Id -Force -ErrorAction SilentlyContinue}
  # [2026-08-03 09:06:39] 作用：等待被终止进程释放数据库连接和日志句柄；理由依据：本地基线验证不能与尚未回滚的在线事务并发。
  if(-not $onlineCloneFinished){[void]$onlineCloneProcess.WaitForExit(10000)}
  # [2026-08-03 09:06:40] 作用：刷新已结束进程的退出状态；理由依据：Windows PowerShell 5.1 的 Start-Process 对象可能延迟回填 ExitCode。
  $onlineCloneProcess.Refresh()
  # [2026-08-03 09:06:41] 作用：把安全的克隆标准输出回显到单窗口；理由依据：成功的表数与行数仍属于部署验收证据。
  if(Test-Path -LiteralPath $onlineCloneOut -PathType Leaf){Get-Content -LiteralPath $onlineCloneOut -Encoding UTF8|Write-Host}
  # [2026-08-03 09:06:42] 作用：把克隆错误摘要作为告警回显；理由依据：离线基线回退不应隐藏在线刷新未完成的具体原因。
  if((Test-Path -LiteralPath $onlineCloneErr -PathType Leaf) -and (Get-Item -LiteralPath $onlineCloneErr).Length -gt 0){Get-Content -LiteralPath $onlineCloneErr -Encoding UTF8|Write-Warning}
  # [2026-08-03 09:06:43] 作用：返回在线克隆的超时、退出码和日志合同；理由依据：调用方只能在完整成功后进入在线深度复核。
  return [pscustomobject]@{TimedOut=(-not $onlineCloneFinished);ExitCode=if($onlineCloneFinished){$onlineCloneProcess.ExitCode}else{-1};StdoutLog=$onlineCloneOut;StderrLog=$onlineCloneErr}
}
function Compose([string[]]$ComposeArgs){
  Push-Location $SqlRag
  try{
    # [2026-07-13 12:11:00] 作用：保存进入 Docker Compose 前的 PowerShell 错误策略；理由依据：调用结束后必须恢复全量启动脚本的严格失败语义。
    $composePreviousErrorAction=$ErrorActionPreference
    # [2026-07-13 12:11:00] 作用：初始化 Docker Compose 退出码；理由依据：finally 恢复策略后仍需依据真实 native 退出码判断结果。
    $composeExitCode=-1
    # [2026-07-13 12:11:00] 作用：进入仅包围 Docker Compose 的兼容区块；理由依据：状态输出兼容范围不能扩散到后续服务启动逻辑。
    try{
      # [2026-07-13 12:11:00] 作用：暂时允许 Docker 写入 stderr 的 Running 状态行；理由依据：Windows PowerShell 5 会把 native stderr 包装成 ErrorRecord 并受 Stop 策略终止。
      $ErrorActionPreference='Continue'
      # [2026-07-22 17:08:12] 作用：Windows Server 下把项目绝对路径转换为 WSL 路径；理由依据：Compose 相对绑定挂载必须由 Linux Docker Engine 从 /mnt/d 正确解析。
      if($DockerBackend -eq 'wsl'){
        $wslSqlRag=((& wsl.exe -d $DockerWslDistro -u root -- wslpath -a $SqlRag) -join '').Trim()
        if($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($wslSqlRag)){throw "SQL_RAG 路径转换失败：$SqlRag"}
        # [2026-07-31 09:45:12] 作用：在 WSL 中用 profile 专属项目名执行 Compose；理由依据：项目名决定命名卷归属，省略时两套部署会共享或接管容器。
        & wsl.exe -d $DockerWslDistro -u root --cd $wslSqlRag -- docker compose --project-name $ComposeProjectName --env-file ./.env -f ./docker-compose.yml @ComposeArgs 2>&1 | ForEach-Object { Write-Host $_ }
      }elseif($DockerBackend -eq 'remote_ssh'){
        $remoteComposeArguments=@(
          'compose',
          # [2026-07-31 09:45:13] 作用：把 profile 专属 Compose 项目名传给远程 Docker；理由依据：所有 Docker 后端必须遵守同一容器卷隔离合同。
          '--project-name',$ComposeProjectName,
          '--env-file',$EnvFile,
          '-f',$ComposeFile
        ) + @($ComposeArgs)
        Invoke-MonFangAiRemoteDocker `
          -Arguments $remoteComposeArguments `
          -WorkingDirectory $SqlRag `
          -SqlRagRoot $SqlRag
        $composeExitCode=0
      }else{
        # [2026-07-31 09:45:14] 作用：用 profile 专属项目名启动或复用 SQL_RAG 容器；理由依据：同一 Docker Desktop 上两套部署必须拥有独立项目和命名卷。
        docker compose --project-name $ComposeProjectName --env-file .\.env -f .\docker-compose.yml @ComposeArgs 2>&1 | ForEach-Object { Write-Host $_ }
      }
      # [2026-07-13 12:11:00] 作用：紧邻 native 调用保存 Docker 真实退出码；理由依据：stderr 内容不是 Compose 成败契约，退出码才是。
      if($DockerBackend -ne 'remote_ssh'){$composeExitCode=$LASTEXITCODE}
    # [2026-07-13 12:11:00] 作用：无论 Compose 是否输出错误记录都进入恢复分支；理由依据：后续 Python 和健康检查仍必须保持 Stop 严格策略。
    }finally{
      # [2026-07-13 12:11:00] 作用：恢复调用前的 PowerShell 错误策略；理由依据：只兼容 Docker 状态流，不吞掉后续真实异常。
      $ErrorActionPreference=$composePreviousErrorAction
    # [2026-07-13 12:11:00] 作用：闭合 Docker Compose 兼容恢复分支；理由依据：保证作用域清晰且脚本可解析。
    }
    # [2026-07-13 12:11:00] 作用：仅在 Docker 真实返回非零时终止全量启动；理由依据：既消除 Running 假失败，也保留真实故障阻断。
    if($composeExitCode -ne 0){throw "docker compose $($ComposeArgs -join ' ') 失败，退出码=$composeExitCode"}
  }finally{Pop-Location}
}
# [2026-08-03 18:38:02] 作用：定义第二套直连 Engine 的 init 只读绑定路径解析器；理由依据：Windows Docker CLI 绕过 Desktop API proxy 后不再自动翻译 D:\ 宿主路径。
function Resolve-DockerDesktopDirectInitBindSource{
  # [2026-08-03 18:38:03] 作用：判定当前运行是否为第二套独立 profile 与直连 Linux Engine；理由依据：第一套、WSL 和远程 Docker 仍应使用各自已验收的相对路径逻辑。
  $requiresDirectLinuxBind=($usesIndependentServiceProfile-and$DockerBackend-eq'desktop'-and$DockerEngineEndpoint-eq'npipe:////./pipe/docker_engine_linux')
  # [2026-08-03 18:38:04] 作用：在非直连第二套路径中清除可能继承的 init 覆盖；理由依据：共享编排器不得让第一套误用第二套 Docker VM 路径。
  if(-not$requiresDirectLinuxBind){
    # [2026-08-03 18:38:05] 作用：删除当前进程的第二套 init bind 覆盖；理由依据：Compose 默认值 ./init 必须继续服务本地第一套。
    Remove-Item Env:SQL_RAG_INIT_BIND_SOURCE -ErrorAction SilentlyContinue
    # [2026-08-03 18:38:06] 作用：结束不需要路径翻译的分支；理由依据：禁止在其他 Docker 后端上启动多余探测容器。
    return
  }
  # [2026-08-03 18:38:07] 作用：解析仓库 init 目录的 Windows 绝对路径；理由依据：转换源必须是当前实际部署根而不是写死开发机目录。
  $windowsInitPath=(Resolve-Path -LiteralPath (Join-Path $SqlRag 'init') -ErrorAction Stop).Path
  # [2026-08-03 18:38:08] 作用：限制 init 源为标准 Windows 盘符路径；理由依据：UNC 或相对路径不能按 Docker Desktop VM 盘符挂载合同猜测转换。
  if($windowsInitPath-notmatch'^[A-Za-z]:\\'){throw "第二套 init 目录不是可转换的 Windows 盘符路径：$windowsInitPath"}
  # [2026-08-03 18:38:09] 作用：提取小写盘符；理由依据：Docker Desktop Linux VM 的宿主盘映射目录按 d 等小写盘符命名。
  $driveLetter=$windowsInitPath.Substring(0,1).ToLowerInvariant()
  # [2026-08-03 18:38:10] 作用：把盘符后目录转为 Linux 斜杠；理由依据：Linux daemon 拒绝包含反斜杠的 bind source。
  $relativeInitPath=$windowsInitPath.Substring(3).Replace('\','/')
  # [2026-08-03 18:47:11] 作用：固定init路径探针复用的本地SQL Server镜像；理由依据：该镜像已是正式Compose离线资产且具备bash。
  $initProbeImage='mcr.microsoft.com/mssql/server:2022-latest'
  # [2026-08-03 18:47:12] 作用：只读检查init探针镜像已在本机Engine；理由依据：预检不得因缺镜像隐式访问网络而再次长时无输出。
  $null=& docker.exe image inspect $initProbeImage 2>$null
  # [2026-08-03 18:47:13] 作用：记录本地镜像查询退出码；理由依据：仅有Engine返回0才允许进入禁止拉取的短命探针。
  $initProbeImageExitCode=$LASTEXITCODE
  # [2026-08-03 18:47:14] 作用：镜像不存在时立即输出离线资产缺失；理由依据：不能将镜像拉取超时误判为bind路径失败。
  if($initProbeImageExitCode-ne0){throw "第二套init路径探针镜像缺失：$initProbeImage；请恢复正式离线镜像后重跑同一入口；data_destructive_actions=0"}
  # [2026-08-03 18:38:11] 作用：声明 Docker Desktop 版本间的三种非代理宿主盘映射候选；理由依据：实机探测比对 4.84 路径形式做单值假设更稳定。
  $candidatePaths=@("/run/desktop/mnt/host/$driveLetter/$relativeInitPath","/host_mnt/$driveLetter/$relativeInitPath","/mnt/$driveLetter/$relativeInitPath")
  # [2026-08-03 18:38:12] 作用：初始化未选中的 Linux bind source；理由依据：只有真实读到两个初始化脚本的候选才能进入 Compose。
  $selectedPath=''
  # [2026-08-03 18:38:13] 作用：建立候选探测结果列表；理由依据：所有候选失败时必须输出可定位证据而不是再次无输出等待。
  $probeSummaries=New-Object System.Collections.Generic.List[string]
  # [2026-08-03 18:38:14] 作用：逐个验证 Docker Desktop VM 宿主盘映射候选；理由依据：不同 Desktop 版本的内部 mount root 可能不同。
  foreach($candidatePath in $candidatePaths){
    # [2026-08-03 18:38:15] 作用：组装当前候选的只读 bind mount 参数；理由依据：--mount 在源不存在时会失败且不会静默创建空目录。
    $mountSpecification="type=bind,source=$candidatePath,target=/sql-rag-init-probe,readonly"
    # [2026-08-03 18:38:16] 作用：保存直连探测前的 PowerShell 错误策略；理由依据：Docker 对不存在候选的 stderr 不应跳过后续兼容路径。
    $previousProbeErrorAction=$ErrorActionPreference
    # [2026-08-03 18:38:17] 作用：初始化当前 bind 候选输出；理由依据：探测摘要必须区分 daemon 拒绝与脚本缺失。
    $probeOutput=@()
    # [2026-08-03 18:38:18] 作用：初始化当前 bind 候选退出码；理由依据：只能以 Docker 真实退出码判定路径是否可用。
    $probeExitCode=-1
    # [2026-08-03 18:38:19] 作用：进入仅包围当前 Docker bind 探测的错误兼容区；理由依据：严格启动语义必须在探测结束后恢复。
    try{
      # [2026-08-03 18:38:20] 作用：允许 Docker 将当前候选失败写入 stderr；理由依据：候选失败是可预期分支而不是 PowerShell 未处理异常。
      $ErrorActionPreference='Continue'
      # [2026-08-03 18:38:21] 作用：用只读短命容器验证两个 init 脚本真实可见；理由依据：Compose config 文本成功不能证明 Linux daemon 能读取 Windows 文件。
      $probeOutput=@(& docker.exe run --pull never --rm --mount $mountSpecification --entrypoint /bin/bash $initProbeImage -lc 'test -r /sql-rag-init-probe/init-db.sh -a -r /sql-rag-init-probe/init-external-db.sh' 2>&1)
      # [2026-08-03 18:38:22] 作用：紧邻探测命令记录 Docker 退出码；理由依据：后续输出处理不得覆盖真实成败状态。
      $probeExitCode=$LASTEXITCODE
    }finally{
      # [2026-08-03 18:38:23] 作用：恢复 bind 探测前的 PowerShell 错误策略；理由依据：后续数据库、模型和 WebUI 仍需失败关闭。
      $ErrorActionPreference=$previousProbeErrorAction
    }
    # [2026-08-03 18:38:24] 作用：记录当前候选路径与退出码摘要；理由依据：全部失败时要一次性给出已探测路径范围。
    $probeSummaries.Add("$candidatePath=$probeExitCode")
    # [2026-08-03 18:38:25] 作用：在当前候选真实可读时选定 Linux bind source；理由依据：第一个通过实机验证的路径即是本次 daemon 的有效映射。
    if($probeExitCode-eq0){
      # [2026-08-03 18:38:26] 作用：保存已验证的 Docker VM init 路径；理由依据：后续两个 Compose init 服务必须复用同一实体。
      $selectedPath=$candidatePath
      # [2026-08-03 18:38:27] 作用：结束已成功的候选探测循环；理由依据：不再启动无意义的额外短命容器。
      break
    }
  }
  # [2026-08-03 18:38:28] 作用：在所有 Docker VM 宿主路径均不可读时立即阻断；理由依据：不得再把 Windows D:\ 路径交给 Linux daemon 后才在 init-db 阶段失败。
  if([string]::IsNullOrWhiteSpace($selectedPath)){throw "第二套直连Engine无法读取init目录；windows_path=$windowsInitPath；candidates=$($probeSummaries-join';')；data_destructive_actions=0"}
  # [2026-08-03 18:38:29] 作用：把已验证 Linux 路径注入当前 Compose 进程；理由依据：环境覆盖仅影响第二套当次启动且不修改第一套文件或全局 context。
  $env:SQL_RAG_INIT_BIND_SOURCE=$selectedPath
  # [2026-08-03 18:38:30] 作用：输出第二套实际使用的 init bind 合同；理由依据：运维窗口必须能直接区分路径转换成功与 Docker Desktop UI 转圈。
  Write-Host "第二套直连Engine init路径验证通过：windows=$windowsInitPath；linux=$selectedPath；readonly=true。"
}
# [2026-07-24 19:40:00] 作用：在调用 Docker 前核验 Compose 中每个数据库端口都显式引用统一回环绑定变量；理由依据：默认环境值不足以防止某个新增数据库服务遗漏 HostIp。
function Assert-DatabaseComposeIsolation{
  # [2026-07-24 19:40:00] 作用：读取本次实际启动使用的 Compose 原文；理由依据：检查对象必须与一键启动传给 Docker 的文件完全一致。
  $composeText=Get-Content -LiteralPath $ComposeFile -Raw -Encoding UTF8
  # [2026-07-24 19:40:00] 作用：列出当前商业链路全部 10 个数据库宿主端口映射合同；理由依据：SQL Server、PostgreSQL、Qdrant、Neo4j 任一遗漏都会形成公网暴露面。
  $requiredMappings=@(
    '${SQL_RAG_DATABASE_BIND:-127.0.0.1}:${MSSQL_PORT:-1433}:1433',
    '${SQL_RAG_DATABASE_BIND:-127.0.0.1}:${QDRANT_PORT:-6333}:6333',
    '${SQL_RAG_DATABASE_BIND:-127.0.0.1}:${LANGGRAPH_POSTGRES_PORT:-15432}:5432',
    '${SQL_RAG_DATABASE_BIND:-127.0.0.1}:${WKT_PRASING_EXTRA_PG_PORT:-15433}:5432',
    '${SQL_RAG_DATABASE_BIND:-127.0.0.1}:${WKT_PRASING_EXTRA_QDRANT_HTTP_PORT:-6335}:6333',
    '${SQL_RAG_DATABASE_BIND:-127.0.0.1}:${WKT_PRASING_EXTRA_QDRANT_GRPC_PORT:-6336}:6334',
    '${SQL_RAG_DATABASE_BIND:-127.0.0.1}:${EXTERNAL_MSSQL_PORT:-14333}:1433',
    '${SQL_RAG_DATABASE_BIND:-127.0.0.1}:${EXTERNAL_QDRANT_PORT:-6334}:6333',
    '${SQL_RAG_DATABASE_BIND:-127.0.0.1}:${NEO4J_HTTP_PORT:-7474}:7474',
    '${SQL_RAG_DATABASE_BIND:-127.0.0.1}:${NEO4J_BOLT_PORT:-7687}:7687'
  )
  # [2026-07-24 19:40:00] 作用：逐项确认数据库端口合同存在；理由依据：一旦文件被后续提交改回无 HostIp 形式，一键启动必须立刻阻断。
  foreach($mapping in $requiredMappings){
    if(!$composeText.Contains($mapping)){throw "安全阻断：Docker Compose 数据库端口未受回环地址保护：$mapping"}
  }
  # [2026-08-03 18:38:31] 作用：声明两个初始化服务必须使用的可覆盖 bind 合同；理由依据：第二套直连 Linux Engine 需要注入 VM 可见路径而第一套仍需默认 ./init。
  $initBindContract='${SQL_RAG_INIT_BIND_SOURCE:-./init}:/init:ro'
  # [2026-08-03 18:38:32] 作用：计数 Compose 中参数化 init bind 实体；理由依据：主库与外部库初始化容器必须同时受路径合同保护。
  $initBindContractCount=[regex]::Matches($composeText,[regex]::Escape($initBindContract)).Count
  # [2026-08-03 18:38:33] 作用：要求 Compose 恰好包含两个参数化 init bind；理由依据：任一旧 ./init 残留都会让直连 daemon 再次收到 Windows 路径。
  if($initBindContractCount-ne2){throw "安全阻断：Docker Compose init bind合同数量必须为2，实际=$initBindContractCount"}
  # [2026-07-24 18:05:00] 作用：确认 Compose 声明固定命名的 bridge 网络；理由依据：同机其他项目容器要访问数据库时必须走 Docker 内网，不能改回公网端口。
  $networkContract='${SQL_RAG_INTERNAL_NETWORK:-monfangai-sql-rag-internal}'
  # [2026-07-24 18:05:00] 作用：在网络合同缺失时失败关闭；理由依据：避免部署后只能通过放开数据库网卡监听来实现跨项目访问。
  if(!$composeText.Contains($networkContract)){throw "安全阻断：Docker Compose 缺少固定内部网络合同：$networkContract"}
  # [2026-07-24 18:05:00] 作用：输出本次生效的两层访问边界；理由依据：运维人员必须明确 Windows 进程走回环、容器走 Docker bridge。
  Write-Host "数据库 Compose 隔离校验通过：$($requiredMappings.Count) 个端口统一受绑定变量保护；运行目标=$RuntimeDatabaseBind；容器内部网络=$InternalDockerNetwork。"
}
# [2026-07-24 19:40:00] 作用：读取单个数据库容器实际生效的 Docker 端口绑定；理由依据：静态 Compose 正确并不代表旧容器或运行时覆盖没有产生漂移。
function Get-DatabaseContainerBindings([string]$ContainerName){
  # [2026-07-24 19:40:00] 作用：保存严格错误策略；理由依据：只对 Docker 原生命令的标准错误流做局部兼容。
  $previousErrorAction=$ErrorActionPreference
  # [2026-07-24 19:40:00] 作用：初始化检查输出和退出码；理由依据：finally 恢复策略后仍需依据真实 native 结果判断。
  $inspectOutput=@()
  $inspectExitCode=-1
  try{
    $ErrorActionPreference='Continue'
    # [2026-07-24 19:40:00] 作用：Windows Server 从指定 WSL 发行版检查 Linux Docker 容器；理由依据：服务器部署不依赖 Docker Desktop。
    if($DockerBackend -eq 'remote_ssh'){
      $inspectOutput=@(
        Invoke-MonFangAiRemoteDocker `
          -Arguments @(
            'inspect','--format',
            '{{json .HostConfig.PortBindings}}',
            $ContainerName
          ) `
          -SqlRagRoot $SqlRag `
          -CaptureOutput
      )
      $inspectExitCode=0
    }elseif($DockerBackend -eq 'wsl'){
      $inspectOutput=@(& wsl.exe -d $DockerWslDistro -u root -- docker inspect --format '{{json .HostConfig.PortBindings}}' $ContainerName 2>&1)
    }else{
      # [2026-07-24 19:40:00] 作用：本机 Docker Desktop 环境执行同一检查；理由依据：开发机与服务器共用一套一键启动安全合同。
      $inspectOutput=@(docker inspect --format '{{json .HostConfig.PortBindings}}' $ContainerName 2>&1)
    }
    $inspectExitCode=$LASTEXITCODE
  }finally{
    $ErrorActionPreference=$previousErrorAction
  }
  # [2026-07-24 19:40:00] 作用：容器不存在或 inspect 失败时阻断；理由依据：不能在未验证实际监听范围时继续报告全量服务就绪。
  if($inspectExitCode -ne 0){throw "安全阻断：无法检查数据库容器 $ContainerName 的端口绑定，退出码=$inspectExitCode，输出=$($inspectOutput -join ' ')"}
  $inspectJson=($inspectOutput -join '').Trim()
  if([string]::IsNullOrWhiteSpace($inspectJson)){throw "安全阻断：数据库容器 $ContainerName 没有返回端口绑定信息"}
  return ($inspectJson | ConvertFrom-Json)
}
# [2026-07-25 10:55:29] 作用：判断可选数据库容器是否已经存在；理由依据：迁移源 PostgreSQL 由数据库恢复步骤创建，本地开发机和首次部署阶段允许尚未创建，但一旦存在就必须执行同样的回环隔离检查。
function Test-DockerContainerExists([string]$ContainerName){
  # [2026-07-25 10:55:29] 作用：局部保存严格错误策略；理由依据：docker inspect 对不存在容器返回非零属于可判定状态，不能污染一键启动的全局错误策略。
  $previousErrorAction=$ErrorActionPreference
  $inspectOutput=@()
  $inspectExitCode=-1
  try{
    $ErrorActionPreference='Continue'
    # [2026-07-25 10:55:29] 作用：Windows Server 通过项目 WSL Docker Engine 查询；理由依据：云端不依赖 Docker Desktop。
    if($DockerBackend -eq 'remote_ssh'){
      try{
        $inspectOutput=@(
          Invoke-MonFangAiRemoteDocker `
            -Arguments @('inspect','--format','{{.Id}}',$ContainerName) `
            -SqlRagRoot $SqlRag `
            -CaptureOutput
        )
        $inspectExitCode=0
      }catch{
        $inspectOutput=@($_.Exception.Message)
        $inspectExitCode=1
      }
    }elseif($DockerBackend -eq 'wsl'){
      $inspectOutput=@(& wsl.exe -d $DockerWslDistro -u root -- docker inspect --format '{{.Id}}' $ContainerName 2>&1)
    }else{
      # [2026-07-25 10:55:29] 作用：本地 Docker Desktop 使用同一容器存在性检查；理由依据：同一套程序必须同时兼容本机和阿里云服务器。
      $inspectOutput=@(docker inspect --format '{{.Id}}' $ContainerName 2>&1)
    }
    $inspectExitCode=$LASTEXITCODE
  }finally{
    $ErrorActionPreference=$previousErrorAction
  }
  return ($inspectExitCode -eq 0 -and -not [string]::IsNullOrWhiteSpace(($inspectOutput -join '').Trim()))
}
# [2026-07-24 19:40:00] 作用：核验所有已启动数据库容器的实际 HostIp；理由依据：只有运行态也为 127.0.0.1 才能证明数据库没有暴露到阿里云公网网卡。
function Assert-DatabaseRuntimeIsolation{
  $contracts=@(
    [pscustomobject]@{Container=$DatabaseContainerNames.SqlServer;Ports=@('1433/tcp')},
    [pscustomobject]@{Container=$DatabaseContainerNames.Qdrant;Ports=@('6333/tcp')},
    [pscustomobject]@{Container=$DatabaseContainerNames.Checkpoint;Ports=@('5432/tcp')},
    [pscustomobject]@{Container=$DatabaseContainerNames.ClonePostgres;Ports=@('5432/tcp')},
    [pscustomobject]@{Container=$DatabaseContainerNames.CloneQdrant;Ports=@('6333/tcp','6334/tcp')},
    [pscustomobject]@{Container=$DatabaseContainerNames.ExternalSqlServer;Ports=@('1433/tcp')},
    [pscustomobject]@{Container=$DatabaseContainerNames.ExternalQdrant;Ports=@('6333/tcp')},
    [pscustomobject]@{Container=$DatabaseContainerNames.Neo4j;Ports=@('7474/tcp','7687/tcp')}
  )
  foreach($contract in $contracts){
    $bindings=Get-DatabaseContainerBindings $contract.Container
    foreach($containerPort in $contract.Ports){
      $portProperty=$bindings.PSObject.Properties[$containerPort]
      if($null -eq $portProperty){throw "安全阻断：数据库容器 $($contract.Container) 缺少预期端口 $containerPort 的运行态绑定"}
      foreach($binding in @($portProperty.Value)){
        $hostIp=[string]$binding.HostIp
        if($hostIp -ne $RuntimeDatabaseBind){throw "安全阻断：数据库容器 $($contract.Container) 的 $containerPort 实际监听 $hostIp，要求 $RuntimeDatabaseBind"}
      }
    }
  }
  Write-Host "数据库运行态隔离校验通过：全部容器仅监听 $RuntimeDatabaseBind。"
}
# [2026-07-25 10:55:29] 作用：核验已恢复的迁移源 PostgreSQL 运行态绑定；理由依据：该容器不属于主 Compose，但同样承载业务数据，存在时只能供 Windows 同机进程通过回环地址访问。
function Assert-OptionalMigratedPostgresRuntimeIsolation{
  $containerName=if([string]::IsNullOrWhiteSpace([string]$env:SQL_RAG_MIGRATED_PG_CONTAINER)){'sql-rag-migrated-source-postgres'}else{[string]$env:SQL_RAG_MIGRATED_PG_CONTAINER}
  # [2026-07-25 10:55:29] 作用：迁移库尚未恢复时明确跳过；理由依据：不把“可选数据恢复顺序”误判成业务逻辑故障。
  if(!(Test-DockerContainerExists $containerName)){
    Write-Host "迁移源 PostgreSQL 尚未创建，跳过可选运行态隔离校验：$containerName"
    return
  }
  $bindings=Get-DatabaseContainerBindings $containerName
  $portProperty=$bindings.PSObject.Properties['5432/tcp']
  if($null -eq $portProperty){throw "安全阻断：迁移源 PostgreSQL 容器 $containerName 缺少 5432/tcp 运行态绑定"}
  foreach($binding in @($portProperty.Value)){
    $hostIp=[string]$binding.HostIp
    if($hostIp -ne $RuntimeDatabaseBind){throw "安全阻断：迁移源 PostgreSQL 容器 $containerName 实际监听 $hostIp，要求 $RuntimeDatabaseBind"}
    # [2026-07-30 16:27:00] 作用：读取迁移源 PostgreSQL 的实际宿主机端口；理由依据：只检查 127.0.0.1 会漏掉服务器第二套端口误用本地 5432 的串线。
    $hostPort=[int]$binding.HostPort
    # [2026-07-31 09:45:15] 作用：断言迁移源容器使用当前 profile 的独立端口；理由依据：本地为 5432，新采购服务器为 25434，不能再与本地 checkpoint 的 15432 重叠。
    if($hostPort -ne [int]$MigratedPostgresPort){throw "安全阻断：迁移源 PostgreSQL 容器 $containerName 实际端口 $hostPort，当前部署要求 $MigratedPostgresPort"}
  }
  Write-Host "迁移源 PostgreSQL 运行态隔离校验通过：$containerName 仅监听 $RuntimeDatabaseBind。"
}
# [2026-08-04 16:18:30] 作用：读取迁移源业务库的真实用户表数量；理由依据：端口监听和容器healthy不能证明AIERP/AIIE已经恢复，知识与资产页面必须以数据实体作为门禁。
function Get-MigratedPostgresBusinessTableCount{
  # [2026-08-04 16:18:30] 作用：接收要验收的迁移业务库名；理由依据：只允许调用方明确检查AIERP或AIIE，禁止模糊命中其它数据库。
  param(
    [Parameter(Mandatory=$true)][ValidateSet('AIERP','AIIE')][string]$Database,
    # [2026-08-04 16:18:30] 作用：接收当前profile已经解析的独立容器名；理由依据：函数不得依赖调用作用域中的偶然同名变量而产生跨profile查询。
    [Parameter(Mandatory=$true)][string]$ContainerName
  )
  # [2026-08-04 16:18:30] 作用：构造不读取业务内容的用户表计数SQL；理由依据：验收仅需证明恢复实体存在，不能把客户数据打印到启动日志。
  $inventorySql="SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE c.relkind IN ('r','p') AND n.nspname NOT IN ('pg_catalog','information_schema');"
  # [2026-08-04 16:18:30] 作用：初始化数据库命令输出；理由依据：本地Docker与远程SSH后端必须汇入同一解析合同。
  $inventoryOutput=@()
  # [2026-08-04 16:18:30] 作用：初始化数据库命令退出码；理由依据：空输出不能被误判为零表或已恢复。
  $inventoryExitCode=0
  # [2026-08-04 16:18:30] 作用：远程Docker后端通过公共适配器在目标容器内查询；理由依据：不得绕过既有SSH参数编码与主机校验。
  if($DockerBackend -eq 'remote_ssh'){
    # [2026-08-04 16:18:30] 作用：捕获远程psql用户表计数；理由依据：同一函数必须兼容Windows控制Linux Docker的交付模式。
    $inventoryOutput=@(Invoke-MonFangAiRemoteDocker -Arguments @('exec',$ContainerName,'psql','-U','postgres','-d',$Database,'-At','-c',$inventorySql) -SqlRagRoot $SqlRag -CaptureOutput)
  }else{
    # [2026-08-04 16:18:30] 作用：在当前Docker Desktop迁移容器内执行只读计数；理由依据：第二套Windows服务器应直接验收自己的独立容器。
    $inventoryOutput=@(& docker exec $ContainerName psql -U postgres -d $Database -At -c $inventorySql 2>&1)
    # [2026-08-04 16:18:30] 作用：记录本地docker exec退出码；理由依据：数据库不存在、容器异常和SQL错误都必须显式失败而不是返回假零值。
    $inventoryExitCode=$LASTEXITCODE
  }
  # [2026-08-04 16:18:30] 作用：阻断任何用户表计数命令失败；理由依据：无法读取恢复结果时不能继续宣称知识与资产数据已就绪。
  if($inventoryExitCode -ne 0){throw "迁移源 PostgreSQL 数据实体检查失败：database=$Database；exit=$inventoryExitCode；output=$($inventoryOutput -join ' | ')"}
  # [2026-08-04 16:18:30] 作用：只提取psql返回的单个十进制计数；理由依据：Docker提示或额外输出不得被当成业务表数。
  $inventoryNumbers=@($inventoryOutput|ForEach-Object{([string]$_).Trim()}|Where-Object{$_ -match '^\d+$'})
  # [2026-08-04 16:18:30] 作用：要求计数输出唯一；理由依据：无值或多值都代表运行态合同不确定。
  if($inventoryNumbers.Count -ne 1){throw "迁移源 PostgreSQL 数据实体输出无效：database=$Database；output=$($inventoryOutput -join ' | ')"}
  # [2026-08-04 16:18:30] 作用：返回强类型用户表数；理由依据：调用方需以大于零作为自动恢复后的最低实体门禁。
  return [int]$inventoryNumbers[0]
}
# [2026-07-30 16:27:02] 作用：把已有迁移源 PostgreSQL 对齐到当前端口 profile；理由依据：该容器不属于主 Compose，切换本地/服务器端口时不会被主 Compose 自动重建。
function Ensure-OptionalMigratedPostgresProfile{
  # [2026-07-30 16:27:03] 作用：解析迁移源容器名；理由依据：复用既有可覆盖容器名合同，避免写死第二套启动逻辑。
  $containerName=if([string]::IsNullOrWhiteSpace([string]$env:SQL_RAG_MIGRATED_PG_CONTAINER)){'sql-rag-migrated-source-postgres'}else{[string]$env:SQL_RAG_MIGRATED_PG_CONTAINER}
  # [2026-08-04 16:18:30] 作用：记录迁移源容器是否已经存在；理由依据：第二套首次部署恰好是容器缺失场景，不能继续沿用无声return。
  $migratedContainerExists=Test-DockerContainerExists $containerName
  # [2026-08-04 16:18:30] 作用：只为非第二套profile保留历史可选语义；理由依据：第一套可能继续使用局域网源库，第二套则明确依赖随包恢复的127.0.0.1:25434。
  if(!$migratedContainerExists -and $DeploymentProfile-ne 'server_second_ports'){return}
  # [2026-07-30 16:27:05] 作用：定位既有迁移源 Compose 启动器；理由依据：必须复用同一 Docker Desktop/WSL/远程适配器和健康检查。
  $migrationStartScript=Join-Path $SqlRag 'deployment\alicloud_win11_migration\05-start-source-postgres.ps1'
  # [2026-07-30 16:27:06] 作用：阻断缺少迁移启动器的残缺程序包；理由依据：不能在端口无法对齐时继续报告全栈 ready。
  if(!(Test-Path -LiteralPath $migrationStartScript -PathType Leaf)){throw "缺少迁移源 PostgreSQL 启动器：$migrationStartScript"}
  # [2026-07-30 16:32:00] 作用：定位迁移源环境配置；理由依据：独立 Compose 的密码模板可能仍是占位值，需要在不打印密码的前提下判断是否可用。
  $migrationConfigPath=Join-Path $SqlRag 'deployment\alicloud_win11_migration\config\migration.env'
  # [2026-07-30 16:32:01] 作用：读取进程中已提供的迁移源密码；理由依据：管理员显式配置优先级最高，不得被默认资产库密码覆盖。
  $migrationPassword=[string]$env:SQL_RAG_MIGRATED_PG_PASSWORD
  # [2026-07-30 16:32:02] 作用：进程未提供密码时读取迁移配置文件；理由依据：保留现有恢复部署配置且不在控制台输出内容。
  if([string]::IsNullOrWhiteSpace($migrationPassword)){$migrationPassword=Get-EnvLineValue $migrationConfigPath 'SQL_RAG_MIGRATED_PG_PASSWORD'}
  # [2026-07-30 16:32:03] 作用：迁移配置仍是占位值时复用已启动资产库的同机密码；理由依据：当前迁移源容器由同一一键链恢复，既有本机合同与 ASSET_TYPE_PG_PASSWORD 一致。
  if([string]::IsNullOrWhiteSpace($migrationPassword) -or $migrationPassword.StartsWith('<')){$migrationPassword=Get-EnvLineValue $EnvFile 'ASSET_TYPE_PG_PASSWORD'}
  # [2026-07-30 16:32:04] 作用：没有任何真实密码来源时显式阻断；理由依据：禁止把占位符传给 Compose 后制造无法连接的假健康容器。
  if([string]::IsNullOrWhiteSpace($migrationPassword) -or $migrationPassword.StartsWith('<')){throw '迁移源 PostgreSQL 密码尚未配置。'}
  # [2026-07-30 16:32:05] 作用：仅在当前进程传递迁移源密码；理由依据：Compose 与健康检查需要同值，但程序包和日志不能保存明文副本。
  [Environment]::SetEnvironmentVariable('SQL_RAG_MIGRATED_PG_PASSWORD',$migrationPassword,'Process')
  # [2026-07-31 09:45:16] 作用：用当前 profile 的端口、容器、卷和 Compose 项目重建迁移源；理由依据：只切端口仍会让两套部署共享同一个迁移数据库身份。
  & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $migrationStartScript -ProjectName $MigrationComposeProjectName -HealthTimeoutSeconds 180
  # [2026-07-30 16:27:08] 作用：读取迁移源启动器退出码；理由依据：native PowerShell 子进程失败不会自动进入当前脚本的 Stop 策略。
  $migrationStartExitCode=$LASTEXITCODE
  # [2026-07-30 16:27:09] 作用：端口重建或健康检查失败时中止全量启动；理由依据：数据库端口串线不能降级成警告。
  if($migrationStartExitCode -ne 0){throw "迁移源 PostgreSQL 当前端口 profile 对齐失败，退出码=$migrationStartExitCode"}
  # [2026-08-04 16:18:30] 作用：仅为第二套进入随包业务库幂等恢复；理由依据：本地第一套既有数据库不能被服务器交付逻辑触碰。
  if($DeploymentProfile-eq 'server_second_ports'){
    # [2026-08-04 16:18:30] 作用：定位具备哈希门禁的PostgreSQL恢复器；理由依据：第二套不能只创建空容器后让Knowledge、Asset和Dashboard连接空库。
    $migrationRestoreScript=Join-Path $SqlRag 'deployment\alicloud_win11_migration\06-restore-postgresql.ps1'
    # [2026-08-04 16:18:30] 作用：阻断缺少恢复器的残缺热修包；理由依据：空数据库继续启动会再次表现为页面无新数据。
    if(!(Test-Path -LiteralPath $migrationRestoreScript -PathType Leaf)){throw "缺少迁移源 PostgreSQL 恢复器：$migrationRestoreScript"}
    # [2026-08-04 16:18:30] 作用：从已校验SHA的随包归档仅补齐缺失或空库；理由依据：首次部署必须自动恢复，重复启动又必须保留目标机新增数据。
    # [2026-08-05 10:13:50] 作用：第二套强制使用已healthy的PostgreSQL容器内置16.x工具恢复；理由依据：新服务器无宿主PG_CLIENT与无VPN不应阻断AIERP/AIIE随包数据恢复。
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $migrationRestoreScript -EnvFile $migrationConfigPath -ArtifactRoot (Join-Path $SqlRag 'deployment\alicloud_win11_migration\artifacts\postgresql') -SqlRagEnvFile $EnvFile -RestoreMissingOnly -UseContainerTools
    # [2026-08-04 16:18:30] 作用：记录业务库幂等恢复退出码；理由依据：原生PowerShell子进程失败不会自动进入当前Stop策略。
    $migrationRestoreExitCode=$LASTEXITCODE
    # [2026-08-04 16:18:30] 作用：阻断恢复失败的第二套继续冒充数据库ready；理由依据：用户要求看到随包新数据，静态页面或开放端口都不能替代恢复成功。
    if($migrationRestoreExitCode -ne 0){throw "第二套 PostgreSQL 业务数据恢复失败，退出码=$migrationRestoreExitCode"}
    # [2026-08-04 16:18:30] 作用：回读AIERP真实用户表数量；理由依据：资产类型和Getsoft均依赖该库，必须证明不是空数据库。
    $aiErpBusinessTables=Get-MigratedPostgresBusinessTableCount -Database 'AIERP' -ContainerName $containerName
    # [2026-08-04 16:18:30] 作用：回读AIIE真实用户表数量；理由依据：知识管理和看板依赖该库，必须证明备份实体已落地。
    $aiIeBusinessTables=Get-MigratedPostgresBusinessTableCount -Database 'AIIE' -ContainerName $containerName
    # [2026-08-04 16:18:30] 作用：要求两个业务库均包含用户表；理由依据：只恢复其中一个仍会让28191挂载页面出现一半空数据。
    if($aiErpBusinessTables-le0-or$aiIeBusinessTables-le0){throw "第二套 PostgreSQL 业务数据实体不完整：AIERP_tables=$aiErpBusinessTables；AIIE_tables=$aiIeBusinessTables"}
    # [2026-08-04 16:18:30] 作用：输出第二套数据库已恢复并回读成功的具名证据；理由依据：现场不应再把后续Getsoft MinIO预检误认为数据库仍未启动。
    Write-Host "第二套 PostgreSQL 业务数据已就绪：AIERP_tables=$aiErpBusinessTables；AIIE_tables=$aiIeBusinessTables；port=$MigratedPostgresPort。"
  }
}
# [2026-07-31 10:32:00] 作用：为当前 profile 的恢复库补齐 Getsoft ORM 已使用的会话公司名称字段；理由依据：旧备份的 AI_liaotianzhu 缺少 gs_name 会让 18520 在读取历史会话时返回 SSE_STREAM_FAILED。
function Ensure-MigratedPostgresGetsoftSchemaCompatibility{
  # [2026-07-31 10:32:01] 作用：读取当前 profile 已隔离的迁移源容器名；理由依据：本地与新服务器必须迁移各自容器，禁止固定命中第一套数据库。
  $containerName=[string]$profileContainerEnvironment.SQL_RAG_MIGRATED_PG_CONTAINER
  # [2026-07-31 10:32:02] 作用：尚未恢复迁移库时保持首次部署的可选顺序；理由依据：数据库恢复步骤完成后的一键启动会再次执行本门禁。
  if(!(Test-DockerContainerExists $containerName)){
    # [2026-07-31 10:32:03] 作用：输出可观察的跳过原因；理由依据：运维必须区分“尚未恢复”与“兼容迁移失败”。
    Write-Host "迁移源 PostgreSQL 尚未创建，跳过 Getsoft 表结构兼容迁移：$containerName"
    # [2026-07-31 10:32:04] 作用：结束当前可选迁移；理由依据：没有容器时不能执行数据库命令。
    return
  }
  # [2026-07-31 10:32:05] 作用：定义幂等兼容迁移；理由依据：重复一键启动不得重复建列或破坏已有公司名称。
  $ddl=@'
SET client_min_messages TO warning;
ALTER TABLE public."AI_liaotianzhu" ADD COLUMN IF NOT EXISTS gs_name varchar(64);
UPDATE public."AI_liaotianzhu"
SET gs_name=COALESCE(NULLIF(btrim(gs_id),''),'unknown')
WHERE gs_name IS NULL OR btrim(gs_name)='';
ALTER TABLE public."AI_liaotianzhu" ALTER COLUMN gs_name SET NOT NULL;
ALTER TABLE public."AI_Wendajilu" ADD COLUMN IF NOT EXISTS wenti_jd varchar(64);
ALTER TABLE public."AI_YuanShishuju" ADD COLUMN IF NOT EXISTS wenti_jd varchar(64);
ALTER TABLE public."AI_YongHuShiYongTongJi" ADD COLUMN IF NOT EXISTS "Wenti_jd" text;
-- [2026-08-24 08:50:00] 作用：由当前 profile 的数据库管理员一次性持久化 NAS 三门禁和媒体强绑定字段；理由依据：18320 业务角色不拥有历史原文表，不能在 API 启动时执行 ALTER TABLE。
ALTER TABLE public."AI_YuanShishuju" ADD COLUMN IF NOT EXISTS "nas_file_verified_flag" boolean NOT NULL DEFAULT false;
ALTER TABLE public."AI_YuanShishuju" ADD COLUMN IF NOT EXISTS "nas_parse_completed_flag" boolean NOT NULL DEFAULT false;
ALTER TABLE public."AI_YuanShishuju" ADD COLUMN IF NOT EXISTS "nas_database_sync_verified_flag" boolean NOT NULL DEFAULT false;
ALTER TABLE public."AI_YuanShishuju" ADD COLUMN IF NOT EXISTS "nas_remote_path" text NULL;
ALTER TABLE public."AI_YuanShishuju" ADD COLUMN IF NOT EXISTS "nas_remote_etag" text NULL;
ALTER TABLE public."AI_YuanShishuju" ADD COLUMN IF NOT EXISTS "commercial_file_id" varchar(36) NULL;
ALTER TABLE public."AI_YuanShishuju" ADD COLUMN IF NOT EXISTS "nas_source_program" varchar(128) NULL;
'@
  # [2026-08-24 08:50:00] 作用：定义迁移后的会话补值、既有兼容结构、共享提示词表与七个 NAS 持久字段计数查询；理由依据：一键启动必须在拉起 18320 前证明第二入口的数据库合同完整。
  $verifySql='SELECT count(*)||''|''||count(gs_name)||''|''||count(*) FILTER (WHERE btrim(gs_name)='''')||''|''||(SELECT count(*) FROM information_schema.columns WHERE table_schema=''public'' AND table_name=''AI_Wendajilu'' AND column_name=''wenti_jd'')||''|''||(SELECT count(*) FROM information_schema.columns WHERE table_schema=''public'' AND table_name=''AI_YuanShishuju'' AND column_name=''wenti_jd'')||''|''||(SELECT count(*) FROM information_schema.columns WHERE table_schema=''public'' AND table_name=''AI_YongHuShiYongTongJi'' AND column_name=''Wenti_jd'')||''|''||(SELECT count(*) FROM information_schema.tables WHERE table_schema=''public'' AND table_name=''AI_TiShiCiGuanLiBiao'')||''|''||(SELECT count(*) FROM information_schema.columns WHERE table_schema=''public'' AND table_name=''AI_YuanShishuju'' AND column_name=''nas_file_verified_flag'')||''|''||(SELECT count(*) FROM information_schema.columns WHERE table_schema=''public'' AND table_name=''AI_YuanShishuju'' AND column_name=''nas_parse_completed_flag'')||''|''||(SELECT count(*) FROM information_schema.columns WHERE table_schema=''public'' AND table_name=''AI_YuanShishuju'' AND column_name=''nas_database_sync_verified_flag'')||''|''||(SELECT count(*) FROM information_schema.columns WHERE table_schema=''public'' AND table_name=''AI_YuanShishuju'' AND column_name=''nas_remote_path'')||''|''||(SELECT count(*) FROM information_schema.columns WHERE table_schema=''public'' AND table_name=''AI_YuanShishuju'' AND column_name=''nas_remote_etag'')||''|''||(SELECT count(*) FROM information_schema.columns WHERE table_schema=''public'' AND table_name=''AI_YuanShishuju'' AND column_name=''commercial_file_id'')||''|''||(SELECT count(*) FROM information_schema.columns WHERE table_schema=''public'' AND table_name=''AI_YuanShishuju'' AND column_name=''nas_source_program'') FROM public."AI_liaotianzhu";'
  # [2026-07-31 10:32:07] 作用：初始化迁移输出与退出码；理由依据：三种 Docker 后端必须汇入同一失败关闭判定。
  $migrationOutput=@()
  # [2026-07-31 10:32:08] 作用：初始化验收输出；理由依据：后续必须解析真实数据库计数。
  $verificationOutput=@()
  # [2026-07-31 10:32:09] 作用：远程 Linux Docker 使用参数安全编码的公共适配器执行 SQL；理由依据：不能把 SQL 拼接进 SSH shell 导致引号丢失。
  if($DockerBackend -eq 'remote_ssh'){
    # [2026-07-31 10:32:10] 作用：在服务器 profile 容器内执行幂等 DDL；理由依据：第二套恢复库也必须与第一套保持相同 ORM 合同。
    $migrationOutput=@(Invoke-MonFangAiRemoteDocker -Arguments @('exec',$containerName,'psql','-U','postgres','-d','AIERP','-v','ON_ERROR_STOP=1','-c',$ddl) -SqlRagRoot $SqlRag -CaptureOutput)
    # [2026-07-31 10:32:11] 作用：读取远程迁移后的非空覆盖计数；理由依据：远程命令成功不能代替数据级验收。
    $verificationOutput=@(Invoke-MonFangAiRemoteDocker -Arguments @('exec',$containerName,'psql','-U','postgres','-d','AIERP','-At','-v','ON_ERROR_STOP=1','-c',$verifySql) -SqlRagRoot $SqlRag -CaptureOutput)
  # [2026-07-31 10:32:12] 作用：Windows Server WSL 后端通过标准输入保留 PostgreSQL 标识符引号；理由依据：PowerShell 5.1 直接传含双引号的 -c 参数可能改写 SQL。
  }elseif($DockerBackend -eq 'wsl'){
    # [2026-07-31 13:55:38] 作用：保存全局 PowerShell 错误策略；理由依据：原生 psql 会把非失败诊断写入 stderr，不能被 Stop 提前转换为脚本异常。
    $previousErrorActionPreference=$ErrorActionPreference
    # [2026-07-31 13:55:38] 作用：初始化 WSL 迁移退出码；理由依据：必须依据真实进程码而不是 stderr 文本判定成功。
    $migrationExitCode=-1
    # [2026-07-31 10:32:13] 作用：把 DDL 原文输入 WSL Docker 容器；理由依据：避免原生参数转义造成表名大小写失真。
    try{
      # [2026-07-31 13:55:38] 作用：暂时允许收集 psql 的 stderr 输出；理由依据：NOTICE 不是 SQL 失败且后续仍会检查 ON_ERROR_STOP 与退出码。
      $ErrorActionPreference='Continue'
      # [2026-07-31 13:55:38] 作用：把 DDL 原文输入 WSL Docker 容器并收集完整输出；理由依据：兼容迁移日志需要可审计且不能因 NOTICE 中断。
      $migrationOutput=@($ddl | & wsl.exe -d $DockerWslDistro -u root -- docker exec -i $containerName psql -U postgres -d AIERP -v ON_ERROR_STOP=1 2>&1)
      # [2026-07-31 13:55:38] 作用：在下一条 PowerShell 命令前保存原生进程退出码；理由依据：只有非零码才代表迁移失败。
      $migrationExitCode=$LASTEXITCODE
    }finally{
      # [2026-07-31 13:55:38] 作用：恢复启动器全局失败关闭策略；理由依据：仅 psql 输出采集允许非终止 stderr，后续步骤仍必须严格 Stop。
      $ErrorActionPreference=$previousErrorActionPreference
    }
    # [2026-07-31 10:32:14] 作用：迁移命令失败时立即阻断；理由依据：缺列状态下继续启动只会把故障延迟到浏览器。
    if($migrationExitCode -ne 0){throw "Getsoft 表结构兼容迁移失败：$containerName；$($migrationOutput -join ' ')"}
    # [2026-07-31 13:55:38] 作用：初始化 WSL 验收退出码；理由依据：验收查询也必须使用原生进程码判定。
    $verificationExitCode=-1
    # [2026-07-31 10:32:15] 作用：在同一 WSL 容器读取迁移后计数；理由依据：验收必须命中当前 profile 数据库。
    try{
      # [2026-07-31 13:55:38] 作用：允许验收查询收集原生 stderr；理由依据：非错误诊断不得让一键启动在已有兼容列时中止。
      $ErrorActionPreference='Continue'
      # [2026-07-31 13:55:38] 作用：执行并捕获当前 profile 的结构数据验收；理由依据：必须解析唯一计数证据。
      $verificationOutput=@($verifySql | & wsl.exe -d $DockerWslDistro -u root -- docker exec -i $containerName psql -U postgres -d AIERP -At -v ON_ERROR_STOP=1 2>&1)
      # [2026-07-31 13:55:38] 作用：立即保存验收进程退出码；理由依据：后续恢复错误策略会覆盖 LASTEXITCODE 使用时机。
      $verificationExitCode=$LASTEXITCODE
    }finally{
      # [2026-07-31 13:55:38] 作用：恢复启动器严格错误策略；理由依据：数据库验收之后的任一服务失败仍需阻断。
      $ErrorActionPreference=$previousErrorActionPreference
    }
    # [2026-07-31 10:32:16] 作用：计数查询失败时阻断；理由依据：无法证明兼容状态时禁止报告 ready。
    if($verificationExitCode -ne 0){throw "Getsoft 表结构兼容验收失败：$containerName；$($verificationOutput -join ' ')"}
  # [2026-07-31 10:32:17] 作用：Windows 11 Docker Desktop 通过标准输入执行同一 DDL；理由依据：本机第一套和新服务器第二套必须复用相同语义。
  }else{
    # [2026-07-31 13:55:38] 作用：保存本机启动器的严格错误策略；理由依据：Docker Desktop psql 的 NOTICE 会进入 PowerShell 错误流但退出码仍为零。
    $previousErrorActionPreference=$ErrorActionPreference
    # [2026-07-31 13:55:38] 作用：初始化本机迁移退出码；理由依据：迁移成败必须读取 docker/psql 真实返回值。
    $migrationExitCode=-1
    # [2026-07-31 10:32:18] 作用：把 DDL 原文输入本机 Docker 容器；理由依据：保留 AI_liaotianzhu 的大小写标识符。
    try{
      # [2026-07-31 13:55:38] 作用：暂时把原生 stderr 降为可收集输出；理由依据：重复启动时“列已存在”属于幂等信息而不是失败。
      $ErrorActionPreference='Continue'
      # [2026-07-31 13:55:38] 作用：在本机当前 profile 容器执行幂等 DDL；理由依据：第一套和第二套使用同一数据库合同。
      $migrationOutput=@($ddl | & docker exec -i $containerName psql -U postgres -d AIERP -v ON_ERROR_STOP=1 2>&1)
      # [2026-07-31 13:55:38] 作用：立即保存 docker exec 退出码；理由依据：避免被 finally 中的 PowerShell 赋值覆盖。
      $migrationExitCode=$LASTEXITCODE
    }finally{
      # [2026-07-31 13:55:38] 作用：恢复全量启动严格失败关闭；理由依据：只允许本次幂等 psql 采集非终止诊断。
      $ErrorActionPreference=$previousErrorActionPreference
    }
    # [2026-07-31 10:32:19] 作用：本机迁移失败时立即阻断；理由依据：不能让 18520 带着确定的数据库不兼容继续运行。
    if($migrationExitCode -ne 0){throw "Getsoft 表结构兼容迁移失败：$containerName；$($migrationOutput -join ' ')"}
    # [2026-07-31 13:55:38] 作用：初始化本机验收退出码；理由依据：验收失败必须独立于迁移输出判断。
    $verificationExitCode=-1
    # [2026-07-31 10:32:20] 作用：读取本机当前 profile 的补值计数；理由依据：验证所有历史会话均满足 NOT NULL ORM 合同。
    try{
      # [2026-07-31 13:55:38] 作用：允许完整捕获本机验收输出；理由依据：依据唯一计数行判定而非 stderr 通道。
      $ErrorActionPreference='Continue'
      # [2026-07-31 13:55:38] 作用：查询当前 profile 的会话、缺列和提示词表计数；理由依据：端口健康不能代替 ORM 数据合同验收。
      $verificationOutput=@($verifySql | & docker exec -i $containerName psql -U postgres -d AIERP -At -v ON_ERROR_STOP=1 2>&1)
      # [2026-07-31 13:55:38] 作用：保存本机验收原生退出码；理由依据：后续必须明确区分 SQL 失败与零行结果。
      $verificationExitCode=$LASTEXITCODE
    }finally{
      # [2026-07-31 13:55:38] 作用：恢复启动器全局 Stop 策略；理由依据：数据库兼容步骤之外继续保持失败关闭。
      $ErrorActionPreference=$previousErrorActionPreference
    }
    # [2026-07-31 10:32:21] 作用：本机计数查询失败时阻断；理由依据：不允许把未验证状态写入最终部署报告。
    if($verificationExitCode -ne 0){throw "Getsoft 表结构兼容验收失败：$containerName；$($verificationOutput -join ' ')"}
  }
  # [2026-08-24 08:50:00] 作用：从命令输出提取会话覆盖、四项既有结构和七项 NAS 字段的唯一证据行；理由依据：DDL 提示行与远程包装输出不能影响完整数据合同判定。
  $verificationLine=@($verificationOutput | ForEach-Object {[string]$_} | Where-Object {$_ -match '^\s*\d+\|\d+\|\d+(?:\|1){11}\s*$'} | Select-Object -Last 1)
  # [2026-07-31 10:32:23] 作用：拒绝缺失或歧义的计数证据；理由依据：解析不到唯一结果不能冒充迁移成功。
  if($verificationLine.Count -ne 1){throw "Getsoft 表结构兼容验收未返回唯一计数：$containerName；$($verificationOutput -join ' ')"}
  # [2026-07-31 10:55:05] 作用：拆分会话覆盖和完整表结构计数；理由依据：需要逐项核对历史数据与全部 ORM 依赖。
  $counts=([string]$verificationLine[0]).Trim().Split('|')
  # [2026-08-24 08:50:00] 作用：断言会话补值无空白并且四项既有结构与七项 NAS 字段全部存在；理由依据：任何遗漏都必须在服务启动前失败关闭，不能延迟成 WebUI 空白或 18320 退出。
  if([int]$counts[0] -ne [int]$counts[1] -or [int]$counts[2] -ne 0 -or @($counts[3..13] | Where-Object {[int]$_ -ne 1}).Count -ne 0){throw "Getsoft/NAS 表结构兼容验收未通过：$containerName；计数=$($verificationLine[0])"}
  # [2026-07-31 10:32:26] 作用：输出当前 profile 的确定验收证据；理由依据：运维日志必须能证明修复命中了哪套数据库及覆盖行数。
  Write-Host "Getsoft 表结构兼容验收通过：$containerName；AI_liaotianzhu=$($verificationLine[0])"
  # [2026-08-04 14:58:37] 作用：把当前profile应用账号编码为不含SQL元字符的传输值；理由依据：第一套与第二套账号不同，角色修复不能拼接用户名或把明文写入日志。
  $applicationRoleNameBase64=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($MigratedApplicationUser))
  # [2026-08-04 14:58:37] 作用：把当前profile应用密码编码为不含SQL元字符的临时值；理由依据：服务器强密码含保留字符时仍需与PostgreSQL登录角色严格同步且不能输出明文。
  $applicationRolePasswordBase64=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($MigratedApplicationPassword))
  # [2026-08-04 14:58:37] 作用：定义当前profile应用角色的幂等登录与授权合同；理由依据：容器管理员可读数据不代表28320/28190使用的应用账号能够登录，旧恢复卷或改密后必须在启动前自动对齐。
  $applicationRoleSql=@'
DO $do$
DECLARE
  role_name text := convert_from(decode('__ROLE_NAME_BASE64__','base64'),'UTF8');
  role_password text := convert_from(decode('__ROLE_PASSWORD_BASE64__','base64'),'UTF8');
BEGIN
  IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname=role_name) THEN
    EXECUTE format('ALTER ROLE %I WITH LOGIN PASSWORD %L',role_name,role_password);
  ELSE
    EXECUTE format('CREATE ROLE %I WITH LOGIN PASSWORD %L',role_name,role_password);
  END IF;
  EXECUTE format('GRANT CONNECT ON DATABASE %I TO %I',current_database(),role_name);
  EXECUTE format('GRANT USAGE, CREATE ON SCHEMA public TO %I',role_name);
  EXECUTE format('GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO %I',role_name);
  EXECUTE format('GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO %I',role_name);
  EXECUTE format('GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO %I',role_name);
  EXECUTE format('ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO %I',role_name);
  EXECUTE format('ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO %I',role_name);
  EXECUTE format('ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT EXECUTE ON FUNCTIONS TO %I',role_name);
END
$do$;
'@
  # [2026-08-04 14:58:37] 作用：只在内存中注入当前profile角色与密码编码；理由依据：正式脚本和发布包必须保持零数据库密钥。
  $applicationRoleSql=$applicationRoleSql.Replace('__ROLE_NAME_BASE64__',$applicationRoleNameBase64).Replace('__ROLE_PASSWORD_BASE64__',$applicationRolePasswordBase64)
  # [2026-08-04 14:58:37] 作用：构造不含密码的应用角色验收查询；理由依据：必须证明LOGIN、数据库连接、schema使用和知识表读取四项合同同时成立。
  $applicationRoleVerifySql=('SELECT CASE WHEN r.rolcanlogin AND has_database_privilege(r.rolname,current_database(),''CONNECT'') AND has_schema_privilege(r.rolname,''public'',''USAGE'') AND has_table_privilege(r.rolname,''public."AI_Wendajilu"'',''SELECT'') THEN ''APP_ROLE_READY'' ELSE ''APP_ROLE_INVALID'' END FROM pg_roles r WHERE r.rolname=convert_from(decode(''{0}'',''base64''),''UTF8'');' -f $applicationRoleNameBase64)
  # [2026-08-04 14:58:37] 作用：初始化应用角色变更退出码；理由依据：三种Docker后端必须汇入同一失败关闭结果。
  $applicationRoleExitCode=0
  # [2026-08-04 14:58:37] 作用：初始化应用角色验收输出；理由依据：只保留不含密钥的固定READY标记。
  $applicationRoleVerificationOutput=@()
  # [2026-08-24 08:31:09] 作用：限定应用角色幂等对齐最多尝试五次；理由依据：Docker 冷启动时恢复器或另一启动实例可能短暂并发更新 pg_authid，必须吸收 PostgreSQL tuple concurrently updated 竞态但仍有界失败。
  $applicationRoleMaxAttempts=5
  # [2026-08-24 08:31:09] 作用：在统一有界循环内执行当前 Docker 后端的角色变更和权限验收；理由依据：瞬时系统目录并发不能让一键启动误报永久失败，连续五次失败仍必须阻断。
  for($applicationRoleAttempt=1;$applicationRoleAttempt-le$applicationRoleMaxAttempts;$applicationRoleAttempt++){
    # [2026-08-24 08:31:09] 作用：重置本次应用角色命令退出码；理由依据：前一次瞬时失败不得污染下一次独立重试判定。
    $applicationRoleExitCode=0
    # [2026-08-24 08:31:09] 作用：清空本次授权验收输出；理由依据：只有最后一次实际执行返回的唯一 READY 标记有效。
    $applicationRoleVerificationOutput=@()
    # [2026-08-04 14:58:37] 作用：在远程Docker当前profile容器执行同一角色合同；理由依据：共享引擎的远程后端也不能保留只验管理员、不验应用账号的缺口。
    if($DockerBackend -eq 'remote_ssh'){
      # [2026-08-04 14:58:37] 作用：通过参数安全远程适配器执行角色对齐；理由依据：不得把SQL交给远端shell二次解释。
      [void](Invoke-MonFangAiRemoteDocker -Arguments @('exec',$containerName,'psql','-U','postgres','-d','AIERP','-v','ON_ERROR_STOP=1','-c',$applicationRoleSql) -SqlRagRoot $SqlRag -CaptureOutput)
      # [2026-08-04 14:58:37] 作用：远程读取固定授权标记；理由依据：远程命令返回零不能代替权限级验收。
      $applicationRoleVerificationOutput=@(Invoke-MonFangAiRemoteDocker -Arguments @('exec',$containerName,'psql','-U','postgres','-d','AIERP','-At','-v','ON_ERROR_STOP=1','-c',$applicationRoleVerifySql) -SqlRagRoot $SqlRag -CaptureOutput)
    # [2026-08-04 14:58:37] 作用：在WSL Docker当前profile容器通过标准输入执行角色合同；理由依据：保留强密码和大小写标识符原义。
    }elseif($DockerBackend -eq 'wsl'){
      # [2026-08-04 14:58:37] 作用：暂存严格错误策略；理由依据：psql可能把非失败诊断写入stderr，最终仍以退出码判定。
      $applicationRolePreviousErrorActionPreference=$ErrorActionPreference
      # [2026-08-04 14:58:37] 作用：执行WSL角色对齐与固定标记验收；理由依据：两条命令必须命中同一当前profile容器。
      try{$ErrorActionPreference='Continue';$null=@($applicationRoleSql|& wsl.exe -d $DockerWslDistro -u root -- docker exec -i $containerName psql -U postgres -d AIERP -v ON_ERROR_STOP=1 2>&1);$applicationRoleExitCode=$LASTEXITCODE;if($applicationRoleExitCode-eq0){$applicationRoleVerificationOutput=@($applicationRoleVerifySql|& wsl.exe -d $DockerWslDistro -u root -- docker exec -i $containerName psql -U postgres -d AIERP -At -v ON_ERROR_STOP=1 2>&1);$applicationRoleExitCode=$LASTEXITCODE}}finally{$ErrorActionPreference=$applicationRolePreviousErrorActionPreference}
    # [2026-08-04 14:58:37] 作用：在Docker Desktop当前profile容器通过标准输入执行角色合同；理由依据：本地第一套与新服务器第二套均需获得完全相同的应用登录自愈能力。
    }else{
      # [2026-08-04 14:58:37] 作用：暂存Docker Desktop分支的严格错误策略；理由依据：只允许本次psql完整收集退出码。
      $applicationRolePreviousErrorActionPreference=$ErrorActionPreference
      # [2026-08-04 14:58:37] 作用：执行本机角色对齐与固定标记验收；理由依据：管理员psql成功后必须继续证明28320实际应用角色可读知识表。
      try{$ErrorActionPreference='Continue';$null=@($applicationRoleSql|& docker exec -i $containerName psql -U postgres -d AIERP -v ON_ERROR_STOP=1 2>&1);$applicationRoleExitCode=$LASTEXITCODE;if($applicationRoleExitCode-eq0){$applicationRoleVerificationOutput=@($applicationRoleVerifySql|& docker exec -i $containerName psql -U postgres -d AIERP -At -v ON_ERROR_STOP=1 2>&1);$applicationRoleExitCode=$LASTEXITCODE}}finally{$ErrorActionPreference=$applicationRolePreviousErrorActionPreference}
    }
    # [2026-08-24 08:31:09] 作用：角色变更和权限查询都成功时立即结束重试；理由依据：幂等启动不得制造多余 PostgreSQL 系统目录写入。
    if($applicationRoleExitCode-eq0){break}
    # [2026-08-24 08:31:09] 作用：仅在仍有剩余次数时输出无密钥重试证据；理由依据：现场日志需要区分瞬时并发恢复和最终永久失败。
    if($applicationRoleAttempt-lt$applicationRoleMaxAttempts){Write-Host "PostgreSQL 应用角色对齐第 $applicationRoleAttempt 次未通过，等待后重试。"}
    # [2026-08-24 08:31:09] 作用：按尝试次数进行最多两秒半的线性退避；理由依据：让并发事务提交完成且总启动等待严格有界。
    if($applicationRoleAttempt-lt$applicationRoleMaxAttempts){Start-Sleep -Milliseconds (500*$applicationRoleAttempt)}
  }
  # [2026-08-04 14:58:37] 作用：拒绝任何角色变更或验收命令失败；理由依据：28320继续带错误凭据启动只会把真实数据库记录伪装成0条。
  if($applicationRoleExitCode-ne0){throw "当前profile PostgreSQL应用角色对齐失败：$containerName；退出码=$applicationRoleExitCode"}
  # [2026-08-04 14:58:37] 作用：提取唯一且不含密钥的READY标记；理由依据：NOTICE和包装输出不能冒充权限合同通过。
  $applicationRoleReadyLines=@($applicationRoleVerificationOutput|ForEach-Object{[string]$_}|Where-Object{$_.Trim()-eq'APP_ROLE_READY'})
  # [2026-08-04 14:58:37] 作用：阻断缺失或歧义的角色验收；理由依据：应用账号必须在启动服务前具备唯一确定的知识表读取权限。
  if($applicationRoleReadyLines.Count-ne1){throw "当前profile PostgreSQL应用角色授权验收失败：$containerName"}
  # [2026-08-04 14:58:37] 作用：清除内存中的密码编码与SQL文本；理由依据：后续诊断对象和异常堆栈不应保留数据库密钥材料。
  $applicationRolePasswordBase64=$null;$applicationRoleSql=$null
  # [2026-08-04 14:58:37] 作用：输出不含账号或密码的profile应用角色合同；理由依据：现场可直接区分管理员数据库健康与业务账号健康。
  Write-Host "当前profile PostgreSQL应用角色验收通过：$containerName；database=AIERP；knowledge_table=readable"
}
if(!(Test-Path $Py)){throw "Python虚拟环境不存在：$Py"}
if(!(Test-Path $LlamaExe) -or !(Test-Path $ModelFile)){
  Write-Host '缺少模型文件或 llama-server，执行项目自带 prepare...'
  Push-Location $RepoRoot
  & $Py app\SQL_RAG\main.py qwen35-2b prepare
  if($LASTEXITCODE -ne 0){throw 'qwen35-2b prepare 失败'}
  Pop-Location
}
# [2026-07-17 13:56:30] 作用：启动前验证本地 Embedding GGUF 存在；理由：缺模型时应给出确定错误，不能等到后端检索时才暴露连接失败。
if(!(Test-Path -LiteralPath $EmbeddingModelFile)){throw "Embedding 模型文件不存在：$EmbeddingModelFile"}
Set-EnvLine $EnvFile 'QWEN_AGENT_MODEL' 'Qwen3.5-2B-Q4_K_M'
Set-EnvLine $EnvFile 'QWEN_AGENT_MODEL_SERVER' "http://127.0.0.1:$QwenPort/v1"
Set-EnvLine $EnvFile 'QWEN_AGENT_API_KEY' 'EMPTY'
# [2026-07-18 09:50:44] 作用：把所有非 planner 本地生成的总容量统一为 1024；理由：最终答案预算与总预算取最小值，二者任一保留 512 都会继续截断原文。
Set-EnvLine $EnvFile 'QWEN_AGENT_MAX_TOKENS' '1024'
# [2026-07-18 14:06:00] 作用：为第一次本地模型的多子意图 JSON DAG 保留 512-token 闭合空间；理由：旧 24-token 只够函数名，会截断动态规划合同。
Set-EnvLine $EnvFile 'QWEN_AGENT_PLANNER_MAX_TOKENS' '512'
# [2026-07-18 14:06:00] 作用：把唯一 Planner 请求截止提升到 45 秒；理由：完整问题规划需自然闭合，同时整链仍受三分钟总预算约束。
Set-EnvLine $EnvFile 'QWEN_AGENT_PLANNER_TIMEOUT_SECONDS' '45'
# [2026-07-18 09:50:44] 作用：将第二模型最终回答容量与本地服务上限统一为 1024；理由：模型必须自然结束后再冻结全文，不能在完整性校验前裁掉后半段。
Set-EnvLine $EnvFile 'QWEN_AGENT_FINAL_MAX_TOKENS' '1024'
# [2026-07-18 09:50:44] 作用：给第二模型生成 90 秒单次截止；理由：扩大 token 空间后允许其完成自然收尾，不再用旧 70 秒边界制造另一种截断。
# [2026-07-20 12:19:30] 作用：固化第二模型客户端三分钟截止；理由依据：HTTP 客户端不得先于本地 llama.cpp 的完整答案自然结束。
Set-EnvLine $EnvFile 'QWEN_AGENT_FINAL_TIMEOUT_SECONDS' '180'
# [2026-07-18 09:50:44] 作用：一键启动固化第三模型 768-token JSON 容量；理由：长答案的校验结果也必须完整闭合，避免结构有效性失败掩盖真实语义裁决。
Set-EnvLine $EnvFile 'QWEN_AGENT_VERIFIER_MAX_TOKENS' '768'
# [2026-07-18 09:50:44] 作用：给第三模型 90 秒完成唯一一次结构化裁决；理由：不增加重试或并发，仅允许一次真实本地校验自然结束。
Set-EnvLine $EnvFile 'QWEN_AGENT_VERIFIER_TIMEOUT_SECONDS' '90'
# [2026-07-18 09:50:44] 作用：固定商业问答与校验的请求温度为零；理由：相同问题、Builder 与节点快照必须得到稳定裁决，不能靠 0.1 随机采样决定是否返回原文。
Set-EnvLine $EnvFile 'QWEN_AGENT_TEMPERATURE' '0'
# [2026-07-17 13:56:30] 作用：把所有 RAG 组件统一指向一键启动的本地 Embedding；理由：不得因旧环境变量静默回退到远程服务。
Set-EnvLine $EnvFile 'EMBEDDING_SERVICE_URL' "http://127.0.0.1:$EmbeddingPort/v1"
# [2026-07-17 13:56:30] 作用：写入本地 Embedding 空鉴权合同；理由：llama.cpp 本机端点无需外部 API Key。
Set-EnvLine $EnvFile 'EMBEDDING_SERVICE_API_KEY' 'EMPTY'
# [2026-07-17 13:56:30] 作用：写入稳定模型别名；理由：业务脑、Graphiti 和同步 worker 必须使用同一 `/v1/embeddings` 模型名。
Set-EnvLine $EnvFile 'MODEL_EMBED' $EmbeddingModelAlias
# [2026-07-17 13:56:30] 作用：固化 Qwen3 Embedding 输出维度；理由：Qdrant collection 向量合同为 1024 维，不能随环境漂移。
Set-EnvLine $EnvFile 'EMBEDDING_DIMENSIONS' '1024'
# [2026-07-24 19:40:00] 作用：把数据库回环监听合同持久化到 Compose 环境文件；理由依据：一键启动后续重用容器时仍必须保持仅本机可访问。
Set-EnvLine $EnvFile 'SQL_RAG_DATABASE_BIND' $DatabaseBind
# [2026-07-25 15:10:10] 作用：把当前端口配置及全部 Docker 宿主机端口写入同一环境文件；理由依据：Compose、业务进程和健康检查必须使用同一套 local/aliyun 端口。
Set-EnvLine $EnvFile 'SQL_RAG_DEPLOYMENT_PROFILE' $DeploymentProfile
foreach($entry in $profilePortEnvironment.GetEnumerator()){
  Set-EnvLine $EnvFile ([string]$entry.Key) ([string]$entry.Value)
}
# [2026-07-31 09:45:17] 作用：把当前 profile 的 Compose 项目和容器身份持久化到本安装目录；理由依据：重复一键启动、种子恢复和人工诊断必须继续引用同一套独立实例。
foreach($entry in $profileContainerEnvironment.GetEnumerator()){Set-EnvLine $EnvFile ([string]$entry.Key) ([string]$entry.Value)}
Set-EnvLine $EnvFile 'QDRANT_URL' "http://127.0.0.1:$MainQdrantHttpPort"
Set-EnvLine $EnvFile 'EXTERNAL_QDRANT_URL' "http://127.0.0.1:$ExternalQdrantHttpPort"
Set-EnvLine $EnvFile 'EXTERNAL_SOURCE_QDRANT_URL' "http://127.0.0.1:$ExternalQdrantHttpPort"
Set-EnvLine $EnvFile 'NEO4J_URI' "bolt://127.0.0.1:$Neo4jBoltPort"
# [2026-08-05 12:37:38] 作用：只为第二套初始化 SQL Server ODBC 驱动选择；理由依据：第一套已使用 ODBC Driver 17 全绿，不能因服务器缺驱动修复而改写本地成功合同。
if($usesIndependentServiceProfile){
  # [2026-08-05 12:37:39] 作用：固定 64 位 ODBC 驱动注册表事实源；理由依据：第二套 Python 为 x64，32 位注册项不能满足 pyodbc SQLDriverConnect。
  $sqlServerOdbcRegistryPath='HKLM:\SOFTWARE\ODBC\ODBCINST.INI\ODBC Drivers'
  # [2026-08-05 12:37:40] 作用：安全读取第二套可见的 64 位驱动属性；理由依据：全新服务器未安装驱动时应形成可隔离故障而不是空属性异常中止全部服务。
  $sqlServerOdbcRegistryObject=if(Test-Path -LiteralPath $sqlServerOdbcRegistryPath){Get-ItemProperty -LiteralPath $sqlServerOdbcRegistryPath}else{$null}
  # [2026-08-05 12:37:41] 作用：按 18 优先、17 兼容的顺序选择精确驱动名；理由依据：离线包安装 18，而已安装 17 的兼容环境仍需保持可运行。
  $selectedSqlServerOdbcDriver=''
  # [2026-08-05 12:38:14] 作用：逐项读取注册表属性而不在布尔表达式中赋值；理由依据：正式目标使用 Windows PowerShell 5.1，必须保持其解析器兼容。
  foreach($sqlServerOdbcCandidate in @('ODBC Driver 18 for SQL Server','ODBC Driver 17 for SQL Server')){
    # [2026-08-05 12:38:15] 作用：无注册表节点时结束选择循环；理由依据：缺失状态交给下一步隔离记录而非空对象成员异常。
    if($null-eq$sqlServerOdbcRegistryObject){break}
    # [2026-08-05 12:38:16] 作用：读取当前候选的精确注册属性；理由依据：名称存在且值为 Installed 才等价于 ODBC Driver Manager 可发现。
    $sqlServerOdbcCandidateProperty=$sqlServerOdbcRegistryObject.PSObject.Properties[$sqlServerOdbcCandidate]
    # [2026-08-05 12:38:17] 作用：锁定首个已安装候选并停止遍历；理由依据：18 优先、17 兼容的选择必须确定且可重复。
    if($null-ne$sqlServerOdbcCandidateProperty-and[string]$sqlServerOdbcCandidateProperty.Value-eq'Installed'){$selectedSqlServerOdbcDriver=$sqlServerOdbcCandidate;break}
  }
  # [2026-08-31 14:43:17] 作用：第二套缺少SQL Server客户端驱动时立即停止；理由依据：它与第一套一样是业务链硬依赖，继续启动只会制造二次连接错误和误导性汇总。
  if([string]::IsNullOrWhiteSpace([string]$selectedSqlServerOdbcDriver)){throw '未发现 64 位 ODBC Driver 18/17 for SQL Server；请先安装目标机SQL Server客户端驱动。'}
  # [2026-08-05 12:37:43] 作用：把实机已注册驱动写入第二套自己的 SQL_RAG .env；理由依据：从第一套复制来的 Driver 17 字符串不能在只安装 18 的服务器上继续触发 IM002。
  if(-not[string]::IsNullOrWhiteSpace([string]$selectedSqlServerOdbcDriver)){Set-EnvLine $EnvFile 'DB_DRIVER' ([string]$selectedSqlServerOdbcDriver)}
  # [2026-08-05 12:37:44] 作用：同步当前编排进程的驱动选择；理由依据：后续子进程若读取进程环境也必须与刚写入的第二套文件一致。
  if(-not[string]::IsNullOrWhiteSpace([string]$selectedSqlServerOdbcDriver)){[Environment]::SetEnvironmentVariable('DB_DRIVER',[string]$selectedSqlServerOdbcDriver,'Process')}
  # [2026-08-05 12:37:45] 作用：输出不含密钥的第二套驱动合同；理由依据：现场可直接区分驱动发现问题与 SQL 登录或数据库问题。
  if(-not[string]::IsNullOrWhiteSpace([string]$selectedSqlServerOdbcDriver)){Write-Host "第二套 SQL Server ODBC 驱动已锁定：$selectedSqlServerOdbcDriver"}
}
Set-EnvLine $EnvFile 'DB_PORT' "$MainSqlServerPort"
Set-EnvLine $EnvFile 'KRAUSS_PG_PORT' "$MigratedPostgresPort"
# [2026-07-24 18:05:00] 作用：持久化固定 Docker 内部网络名；理由依据：其他项目容器更新代码或重建后仍可加入同一网络访问数据服务。
Set-EnvLine $EnvFile 'SQL_RAG_INTERNAL_NETWORK' $InternalDockerNetwork
# 2026-06-16 11:33:28 新增：开启商业化记忆强验收；作用：Postgres/Graphiti 任一缺失时 health 顶层标红；理由：不能再把 InMemory 说成生产持久化。
Set-EnvLine $EnvFile 'MEMORY_COMMERCIAL_REQUIRED' '1'
# 2026-06-16 11:33:28 新增：写入 checkpoint PostgreSQL 端口；作用：docker-compose 和 DSN 使用同一个端口；理由：避免端口配置漂移。
Set-EnvLine $EnvFile 'LANGGRAPH_POSTGRES_PORT' "$PostgresCheckpointPort"
# 2026-06-16 11:33:28 新增：写入 checkpoint 数据库名；作用：Postgres 容器初始化专用数据库；理由：和业务 SQL Server 隔离。
Set-EnvLine $EnvFile 'LANGGRAPH_POSTGRES_DB' 'sqlrag_memory'
# 2026-06-16 11:33:28 新增：写入 checkpoint 用户；作用：PostgresSaver 用专用账户连接；理由：商业记忆后端需要最小隔离。
Set-EnvLine $EnvFile 'LANGGRAPH_POSTGRES_USER' 'sqlrag_memory'
# 2026-06-16 11:33:28 新增：写入 checkpoint 密码；作用：compose 环境和 DSN 对齐；理由：一键启动不需要手工填密钥。
Set-EnvLine $EnvFile 'LANGGRAPH_POSTGRES_PASSWORD' 'SqlRagMemory@2026!'
# 2026-06-16 11:33:28 新增：写入 LangGraph 官方 PostgresSaver DSN；作用：短期 thread checkpoint 真正持久化；理由：补齐截图最后一步商业持久化。
Set-EnvLine $EnvFile 'LANGGRAPH_POSTGRES_CHECKPOINT_DSN' "postgresql://sqlrag_memory:SqlRagMemory%402026%21@127.0.0.1:$PostgresCheckpointPort/sqlrag_memory?sslmode=disable"
# 2026-06-16 11:33:28 新增：关闭 InMemory checkpoint 兜底；作用：商业模式下缺 Postgres 直接失败/标红；理由：避免假绿。
Set-EnvLine $EnvFile 'LANGGRAPH_ALLOW_IN_MEMORY_CHECKPOINT' '0'
# 2026-06-16 11:33:28 新增：开启 Graphiti 长期情景记忆；作用：长期记忆走 Graphiti + Neo4j；理由：补齐未启用 Graphiti 的最后缺口。
Set-EnvLine $EnvFile 'GRAPHITI_ENABLED' '1'
# 2026-06-16 11:33:28 新增：写入 Graphiti group 前缀；作用：用户维度隔离长期记忆；理由：商业客服场景必须多用户隔离。
Set-EnvLine $EnvFile 'GRAPHITI_GROUP_PREFIX' 'sql_rag_user'
# 2026-07-01 12:16:04 新增：写入资产类型 PG 主机；作用：资产类型后端服务可直接连接 Navicat 截图中的 krauss；理由：后端入库不能再依赖手工配置。
Set-EnvLine $EnvFile 'ASSET_TYPE_PG_HOST' $ExternalPgHost
# [2026-07-10 16:02:00] 作用：写入外部源同步 PG 主机；理由依据：krauss profile 读取 KRAUSS_PG_HOST，必须和已验证 IPv4 保持一致才能实时同步 Qdrant。
Set-EnvLine $EnvFile 'KRAUSS_PG_HOST' $ExternalPgHost
# [2026-07-11 18:12:00] 作用：启用权威库与复制库四份动态同步 profile；理由依据：显式列表存在时管理器不会自动扫描，新 collection 必须随全量服务持续更新。
Set-EnvLine $EnvFile 'EXTERNAL_SOURCE_SYNC_PROFILES' 'krauss_ai_ie_dev,krauss_ai_ie_raw_data_dev,wkt_prasing_extra_qa_dev,wkt_prasing_extra_raw_data_dev'
# [2026-07-30 11:26:00] 作用：固定启用一键服务内置的 PostgreSQL 到 Qdrant 常驻同步管理器；理由依据：WebUI 编辑只写关系库时必须由同一启动链自动把已发布知识实时更新到向量库。
Set-EnvLine $EnvFile 'EXTERNAL_SOURCE_SYNC_ENABLED' 'true'
# [2026-07-11 18:12:00] 作用：声明复制库 PG 主机；理由依据：profile 运行时连接本机独立容器而非权威源库。
Set-EnvLine $EnvFile 'WKT_PRASING_EXTRA_PG_HOST' '127.0.0.1'
# [2026-07-25 15:10:11] 作用：声明当前配置的复制库 PG 端口；理由依据：云端必须改用第二套宿主机端口且不修改容器内部 5432。
Set-EnvLine $EnvFile 'WKT_PRASING_EXTRA_PG_PORT' "$ClonePostgresPort"
# [2026-07-11 18:12:00] 作用：声明复制数据库名；理由依据：用户固定命名为 wkt_prasing_extra。
Set-EnvLine $EnvFile 'WKT_PRASING_EXTRA_PG_DATABASE' 'wkt_prasing_extra'
# [2026-07-11 18:12:00] 作用：声明复制库用户；理由依据：本地 PostgreSQL 16 容器使用 postgres，密码继续复用环境变量且不新增明文副本。
Set-EnvLine $EnvFile 'WKT_PRASING_EXTRA_PG_USER' 'postgres'
# [2026-07-25 15:10:12] 作用：声明当前配置的复制库 Qdrant 地址；理由依据：profile 级分流保持不变，仅切换宿主机端口。
Set-EnvLine $EnvFile 'WKT_PRASING_EXTRA_QDRANT_URL' "http://127.0.0.1:$CloneQdrantHttpPort"
# [2026-07-11 18:12:00] 作用：启用业务脑复制库候选检索；理由依据：第三件事要求新 collection 命中进入 builder prompt。
Set-EnvLine $EnvFile 'WKT_EXTRA_RETRIEVE_ENABLED' '1'
# [2026-07-25 15:10:13] 作用：声明业务脑复制库 Qdrant 地址；理由依据：查询侧必须与同步侧同指当前配置的克隆 Qdrant。
Set-EnvLine $EnvFile 'WKT_EXTRA_QDRANT_URL' "http://127.0.0.1:$CloneQdrantHttpPort"
# [2026-07-11 18:12:00] 作用：声明业务脑复制库 collection；理由依据：候选读取固定 wkt_prasing_extra_dev。
Set-EnvLine $EnvFile 'WKT_EXTRA_QDRANT_COLLECTION' 'wkt_prasing_extra_dev'
# [2026-07-31 09:45:18] 作用：写入当前配置的迁移源 PostgreSQL 端口；理由依据：本地使用 5432，服务器使用完全不重叠的 25434。
Set-EnvLine $EnvFile 'ASSET_TYPE_PG_PORT' "$MigratedPostgresPort"
# 2026-07-01 12:16:06 新增：写入资产类型 PG 数据库；作用：连接实际存在 AI 表的 AIERP；理由：AI_ZiChanLeiXing 和 AI_TiShiCiGuanLiBiao 在该库中。
Set-EnvLine $EnvFile 'ASSET_TYPE_PG_DATABASE' 'AIERP'
# [2026-08-01 14:15:09] 作用：从当前安装目录读取迁移数据库应用账号；理由依据：本地第一套与服务器第二套拥有不同凭据，启动器不得再硬编码 postgres。
$MigratedApplicationUser=Get-EnvLineValue $EnvFile 'KRAUSS_PG_USER'
# [2026-08-01 14:15:10] 作用：从当前安装目录读取迁移数据库应用密码；理由依据：服务器第16步生成的强密码必须成为资产与知识服务的唯一认证来源。
$MigratedApplicationPassword=Get-EnvLineValue $EnvFile 'KRAUSS_PG_PASSWORD'
# [2026-08-01 14:15:11] 作用：阻断缺失或占位的迁移数据库应用账号；理由依据：继续启动会让资产和知识服务形成数据库假健康。
if([string]::IsNullOrWhiteSpace($MigratedApplicationUser) -or $MigratedApplicationUser.StartsWith('<')){throw 'KRAUSS_PG_USER 尚未配置真实迁移数据库应用账号。'}
# [2026-08-01 14:15:12] 作用：阻断缺失或占位的迁移数据库应用密码；理由依据：不得回退到第一套旧密码或把占位符传给第二套服务。
if([string]::IsNullOrWhiteSpace($MigratedApplicationPassword) -or $MigratedApplicationPassword.StartsWith('<')){throw 'KRAUSS_PG_PASSWORD 尚未配置真实迁移数据库应用密码。'}
# [2026-08-01 14:15:13] 作用：把当前 profile 的应用账号写入资产类型数据库配置；理由依据：本地与服务器必须分别使用各自 SQL_RAG .env 中已验证的账号。
Set-EnvLine $EnvFile 'ASSET_TYPE_PG_USER' $MigratedApplicationUser
# [2026-08-01 14:15:14] 作用：把当前 profile 的应用密码写入资产类型数据库配置；理由依据：服务器强密码不能在一键启动时被旧值 123456 覆盖。
Set-EnvLine $EnvFile 'ASSET_TYPE_PG_PASSWORD' $MigratedApplicationPassword
# 2026-07-01 12:16:09 新增：写入资产类型 PG SSL 模式；作用：兼容当前局域网 PostgreSQL；理由：psycopg 连接需要稳定参数。
Set-EnvLine $EnvFile 'ASSET_TYPE_PG_SSLMODE' 'prefer'
# [2026-07-10 16:02:00] 作用：定位知识库公共运行时环境文件；理由依据：18320 后端从该文件读取 AIERP 数据库连接参数。
$KnowledgeRuntimeEnv=Join-Path $RepoRoot 'app\SQL_RAG\Knowledge_management\backend\public_program_files\runtime\.env'
# [2026-07-28 14:44:00] 作用：读取语音转写专用服务地址；理由依据：通用 Embedding 地址会在本机部署中固定改写为 18001，不能再被音频链复用。
$KnowledgeAudioUrl=Get-EnvLineValue $KnowledgeRuntimeEnv 'AUDIO_TRANSCRIPTION_SERVICE_URL'
# [2026-07-28 14:44:01] 作用：为旧运行配置补齐硅基流动 ASR 官方端点；理由依据：升级后无需人工修改任何业务文件或启动命令。
if([string]::IsNullOrWhiteSpace($KnowledgeAudioUrl)){$KnowledgeAudioUrl='https://api.siliconflow.cn/v1'}
# [2026-07-28 14:44:02] 作用：读取语音转写专用密钥；理由依据：ASR 鉴权必须与本机 Embedding 的 EMPTY 占位彻底隔离。
$KnowledgeAudioApiKey=Get-EnvLineValue $KnowledgeRuntimeEnv 'AUDIO_TRANSCRIPTION_SERVICE_API_KEY'
# [2026-07-28 14:44:03] 作用：从旧版硅基流动 Embedding 密钥平滑迁移；理由依据：现有机器已经保存有效密钥，升级不要求用户重新填写。
if([string]::IsNullOrWhiteSpace($KnowledgeAudioApiKey)){$KnowledgeAudioApiKey=Get-EnvLineValue $KnowledgeRuntimeEnv 'EMBEDDING_SERVICE_API_KEY'}
# [2026-07-28 14:44:04] 作用：兼容当前公共运行时的 LLM 绑定密钥；理由依据：三条硅基流动链允许共享同一账号密钥但保持独立变量。
if([string]::IsNullOrWhiteSpace($KnowledgeAudioApiKey)){$KnowledgeAudioApiKey=Get-EnvLineValue $KnowledgeRuntimeEnv 'LLM_BINDING_API_KEY'}
# [2026-07-28 14:44:05] 作用：兼容现有 OpenAI 兼容密钥；理由依据：历史环境无需人工迁移。
if([string]::IsNullOrWhiteSpace($KnowledgeAudioApiKey)){$KnowledgeAudioApiKey=Get-EnvLineValue $KnowledgeRuntimeEnv 'OPENAI_API_KEY'}
# [2026-07-28 14:44:06] 作用：拒绝缺失或本地占位 ASR 密钥；理由依据：不能在上传后才把配置串线伪装成模型 501。
if([string]::IsNullOrWhiteSpace($KnowledgeAudioApiKey) -or $KnowledgeAudioApiKey -eq 'EMPTY'){throw '知识库音频转写密钥未配置，不能启动假健康服务'}
# [2026-07-28 14:44:07] 作用：读取并固定专用 ASR 模型；理由依据：聊天模型、视觉模型或 Embedding 模型变更都不得改变音频解析。
$KnowledgeAudioModel=Get-EnvLineValue $KnowledgeRuntimeEnv 'AUDIO_TRANSCRIPTION_MODEL'
if([string]::IsNullOrWhiteSpace($KnowledgeAudioModel)){$KnowledgeAudioModel='FunAudioLLM/SenseVoiceSmall'}
# [2026-07-28 14:44:08] 作用：把 ASR 三元组写回运行配置并导出给本轮全部子进程；理由依据：直接启动与固定一键启动必须得到同一确定配置。
Set-EnvLine $KnowledgeRuntimeEnv 'AUDIO_TRANSCRIPTION_SERVICE_URL' $KnowledgeAudioUrl
Set-EnvLine $KnowledgeRuntimeEnv 'AUDIO_TRANSCRIPTION_SERVICE_API_KEY' $KnowledgeAudioApiKey
Set-EnvLine $KnowledgeRuntimeEnv 'AUDIO_TRANSCRIPTION_MODEL' $KnowledgeAudioModel
# [2026-07-28 14:46:00] 作用：解析 ASR 专用端点并阻断本机 Embedding 串线；理由依据：旧故障正是 18001 收到 audio/transcriptions 后返回“不支持音频”。
try{$KnowledgeAudioUri=[uri]$KnowledgeAudioUrl}catch{throw "知识库音频转写地址无效：$KnowledgeAudioUrl"}
if(
  !$KnowledgeAudioUri.IsAbsoluteUri -or
  $KnowledgeAudioUri.Scheme -notin @('http','https')
){throw "知识库音频转写地址不是有效 HTTP URL：$KnowledgeAudioUrl"}
if(
  $KnowledgeAudioUri.IsLoopback -and
  $KnowledgeAudioUri.Port -eq $EmbeddingPort
){throw "知识库音频转写地址错误地指向本机 Embedding 端口 $EmbeddingPort"}
if($KnowledgeAudioModel -eq $EmbeddingModelAlias){
  throw "知识库音频转写模型错误地使用了 Embedding 模型：$KnowledgeAudioModel"
}
# [2026-07-28 14:46:01] 作用：输出不含密钥的 ASR 启动契约；理由依据：长期运维可直接确认模型和端点未漂移。
Write-Host "知识库音频转写：$KnowledgeAudioModel @ $($KnowledgeAudioUri.Scheme)://$($KnowledgeAudioUri.Authority)"
# [2026-07-22 10:31:24] 作用：读取知识运行时已配置的专用聊天模型地址；理由依据：允许以后显式迁移兼容端点且默认仍使用硅基流动。
$KnowledgeLlmUrl=Get-EnvLineValue $KnowledgeRuntimeEnv 'LLM_SERVICE_URL'
# [2026-07-22 10:31:25] 作用：在首次升级时补齐硅基流动默认地址；理由依据：聊天请求绝不能回退到18001本地Embedding服务。
if([string]::IsNullOrWhiteSpace($KnowledgeLlmUrl)){$KnowledgeLlmUrl='https://api.siliconflow.cn/v1'}
# [2026-07-22 10:31:26] 作用：优先读取专用聊天模型密钥；理由依据：LLM和Embedding具备独立鉴权边界。
$KnowledgeLlmApiKey=Get-EnvLineValue $KnowledgeRuntimeEnv 'LLM_SERVICE_API_KEY'
# [2026-07-22 10:31:27] 作用：兼容现有LLM绑定密钥；理由依据：截图二已运行环境无需人工迁移密钥。
if([string]::IsNullOrWhiteSpace($KnowledgeLlmApiKey)){$KnowledgeLlmApiKey=Get-EnvLineValue $KnowledgeRuntimeEnv 'LLM_BINDING_API_KEY'}
# [2026-07-22 10:31:28] 作用：兼容现有OpenAI兼容密钥；理由依据：公共runtime.env已保存同一硅基流动鉴权。
if([string]::IsNullOrWhiteSpace($KnowledgeLlmApiKey)){$KnowledgeLlmApiKey=Get-EnvLineValue $KnowledgeRuntimeEnv 'OPENAI_API_KEY'}
# [2026-07-22 10:31:29] 作用：拒绝缺失或本地占位密钥；理由依据：全量启动不能把EMPTY误报成可用DeepSeek服务。
if([string]::IsNullOrWhiteSpace($KnowledgeLlmApiKey) -or $KnowledgeLlmApiKey -eq 'EMPTY'){throw '知识与看板DeepSeek密钥未配置，不能启动假健康服务'}
# [2026-07-22 10:31:30] 作用：把聊天地址写回知识运行时环境；理由依据：直接启动18320或18430时也保持独立模型连接。
Set-EnvLine $KnowledgeRuntimeEnv 'LLM_SERVICE_URL' $KnowledgeLlmUrl
# [2026-07-22 10:31:31] 作用：向本轮全部子进程导出聊天模型地址；理由依据：父进程可能已有本地Embedding变量且其优先级高于.env。
$env:LLM_SERVICE_URL=$KnowledgeLlmUrl
# [2026-07-22 10:31:32] 作用：向本轮全部子进程导出独立聊天密钥；理由依据：DeepSeek鉴权不能继承EMBEDDING_SERVICE_API_KEY=EMPTY。
$env:LLM_SERVICE_API_KEY=$KnowledgeLlmApiKey
# [2026-07-10 16:02:00] 作用：写入知识库后端 PostgreSQL 主机；理由依据：DB_HOST 不能继续使用可能解析到 IPv6 的 krauss。
Set-EnvLine $KnowledgeRuntimeEnv 'DB_HOST' $ExternalPgHost
# [2026-07-25 15:10:15] 作用：写入知识库后端当前配置的 PostgreSQL 端口；理由依据：Knowledge 后端与资产后端必须随部署配置切换同一个 AIERP PostgreSQL 宿主机端口。
Set-EnvLine $KnowledgeRuntimeEnv 'DB_PORT' "$MigratedPostgresPort"
# [2026-07-10 17:16:00] 作用：写入知识库后端 PostgreSQL 数据库名；理由依据：知识库三表、提示词表、问答关联表都在 AIERP 数据库。
Set-EnvLine $KnowledgeRuntimeEnv 'DB_NAME' 'AIERP'
# [2026-08-01 14:15:15] 作用：把当前 profile 的应用账号同步到知识库运行配置；理由依据：Knowledge 与资产服务必须连接同一套已授权 AIERP 账号且不能串用管理员账号。
Set-EnvLine $KnowledgeRuntimeEnv 'DB_USER' $MigratedApplicationUser
# [2026-08-01 14:15:16] 作用：把当前 profile 的应用密码同步到知识库运行配置；理由依据：第16步服务器密码必须贯穿 WebUI 上传解析链并在重复一键启动后保持不变。
Set-EnvLine $KnowledgeRuntimeEnv 'DB_PASSWORD' $MigratedApplicationPassword
# [2026-07-10 16:02:00] 作用：写入 LightRAG PostgreSQL 主机；理由依据：同一运行时内的 PG 依赖也应避免 krauss IPv6 解析不稳定。
Set-EnvLine $KnowledgeRuntimeEnv 'POSTGRES_HOST' $ExternalPgHost
# [2026-08-01 15:27:00] 作用：把当前 profile 的迁移 PostgreSQL 端口同步到 Knowledge LightRAG 配置；理由依据：服务器第二套必须使用25434且不能遗留第一套5432。
Set-EnvLine $KnowledgeRuntimeEnv 'POSTGRES_PORT' "$MigratedPostgresPort"
# [2026-08-01 15:27:01] 作用：把当前 profile 的应用账号同步到 Knowledge LightRAG 配置；理由依据：DB_*与POSTGRES_*必须使用第16步同一授权账号。
Set-EnvLine $KnowledgeRuntimeEnv 'POSTGRES_USER' $MigratedApplicationUser
# [2026-08-01 15:27:02] 作用：把当前 profile 的应用密码同步到 Knowledge LightRAG 配置；理由依据：重复一键启动不能让LightRAG回退到第一套密码。
Set-EnvLine $KnowledgeRuntimeEnv 'POSTGRES_PASSWORD' $MigratedApplicationPassword
# [2026-08-01 15:27:03] 作用：把 Knowledge LightRAG 数据库名固定为AIERP；理由依据：知识三表和同步状态均位于恢复后的AIERP数据库。
Set-EnvLine $KnowledgeRuntimeEnv 'POSTGRES_DATABASE' 'AIERP'
# [2026-07-10 16:02:00] 作用：修正知识库后端 SQLAlchemy DATABASE_URL 主机；理由依据：实际报错来自 psycopg2 通过 DATABASE_URL 连接 krauss IPv6。
Set-DatabaseUrlHost $KnowledgeRuntimeEnv $ExternalPgHost
# [2026-08-04 15:00:55] 作用：从刚完成原子改写的Knowledge运行配置回读最终连接串；理由依据：load_dotenv默认不覆盖父进程同名变量，第二套曾因此监听28320但database=false并把真实知识记录显示成0条。
$KnowledgeDatabaseUrl=Get-EnvLineValue $KnowledgeRuntimeEnv 'DATABASE_URL'
# [2026-08-04 15:00:55] 作用：在创建任何业务进程前阻断空Knowledge连接串；理由依据：不能让WebUI静态回退数据掩盖数据库配置缺失。
if([string]::IsNullOrWhiteSpace($KnowledgeDatabaseUrl)){throw 'Knowledge DATABASE_URL 重建后为空，拒绝启动28320假健康服务。'}
# [2026-08-06 10:17:36] 作用：以Windows PowerShell实际URI解析器回读Knowledge最终连接串；理由依据：只写.env不能证明第二套没有保留第一套5432端口。
try{$KnowledgeDatabaseUri=[uri]$KnowledgeDatabaseUrl}catch{throw 'Knowledge DATABASE_URL 无法按结构化URI回读，拒绝启动。'}
# [2026-08-06 10:17:36] 作用：要求Knowledge数据库主机与当前profile的本机回环目标一致；理由依据：新服务器不得在第一套Docker停止后才暴露跨机依赖。
if($KnowledgeDatabaseUri.Host -ne $ExternalPgHost){throw "Knowledge DATABASE_URL 主机与当前profile不一致：actual=$($KnowledgeDatabaseUri.Host)；expected=$ExternalPgHost"}
# [2026-08-06 10:17:36] 作用：要求Knowledge数据库端口精确命中当前profile迁移库；理由依据：本地5432与服务器25434必须同时受单profile合同约束。
if(([int]$KnowledgeDatabaseUri.Port) -ne ([int]$MigratedPostgresPort)){throw "Knowledge DATABASE_URL 端口串线：actual=$($KnowledgeDatabaseUri.Port)；expected=$MigratedPostgresPort"}
# [2026-08-03 09:06:44] 作用：在加载两个本地模型前验证并自恢复 Docker Desktop Linux Engine；理由依据：当前截图先启动28001/28002再等待Docker，失败时会留下半套模型进程且重复启动更不确定。
Assert-DatabaseComposeIsolation
# [2026-08-03 09:06:45] 作用：完成 Docker Desktop 两阶段就绪门禁；理由依据：容器引擎是模型、数据库与WebUI编排的共同前置条件，应最先失败关闭。
Ensure-Docker
# [2026-08-19 09:55:00] 作用：在第一套启动任何模型、数据库或商业 Worker 前读取 Docker 冷启动自动恢复的外来 profile；理由依据：unless-stopped 会把第二套和 work-laptop 容器一并拉起并在验收前耗尽 CPU。
if($isLocalDeploymentProfile){
  # [2026-08-19 09:55:00] 作用：只匹配命名合同明确属于第二套或工作站演练 profile 的运行容器；理由依据：不得停止当前 sql-rag 第一套容器或用户未纳入合同的其他项目。
  $foreignProfileContainers=@(docker ps --format '{{.Names}}' | Where-Object {$_ -like 'sql-rag-server-*' -or $_ -like 'sql-rag-work-laptop-*'})
  # [2026-08-19 09:55:00] 作用：拒绝在 Docker 容器清单读取失败时继续启动；理由依据：无法证明 profile 隔离时不能把资源争用误报为第一套就绪。
  if($LASTEXITCODE-ne0){throw '读取 Docker 运行容器失败，无法执行第一套 profile 资源隔离。'}
  # [2026-08-19 09:55:00] 作用：处理已自动恢复的外来 profile；理由依据：第一套全量启动期间只允许第一套占用宿主 CPU、内存和磁盘队列。
  if($foreignProfileContainers.Count-gt0){
    # [2026-08-19 09:55:00] 作用：停止精确命中的外来 profile 容器但保留其卷和可恢复状态；理由依据：本机第一套商业验收不能与第二套或演练栈并跑。
    docker stop $foreignProfileContainers | Out-Host
    # [2026-08-19 09:55:00] 作用：阻断外来容器停止失败的启动；理由依据：资源隔离未达成时继续会再次造成 API 超时和 Docker 500。
    if($LASTEXITCODE-ne0){throw "外来 Docker profile 停止失败：$($foreignProfileContainers -join ', ')"}
  }
  # [2026-08-19 09:55:00] 作用：回读外来 profile 最终运行数；理由依据：docker stop 返回不替代最终状态验收。
  $remainingForeignProfileContainers=@(docker ps --format '{{.Names}}' | Where-Object {$_ -like 'sql-rag-server-*' -or $_ -like 'sql-rag-work-laptop-*'})
  # [2026-08-19 09:55:00] 作用：拒绝残留第二套或演练容器；理由依据：第一套启动成功必须包含资源调度边界而非仅端口可用。
  if($LASTEXITCODE-ne0-or$remainingForeignProfileContainers.Count-ne0){throw "第一套启动前仍有外来 Docker profile：$($remainingForeignProfileContainers -join ', ')"}
  # [2026-08-19 09:55:00] 作用：输出第一套容器资源隔离事实；理由依据：启动时长与 API 长尾排查需要可见证据。
  Write-Host '第一套 Docker profile 资源隔离完成：server/work-laptop 运行容器均为 0。'
}
# [2026-08-03 18:38:34] 作用：在任何 Compose 创建前解析并实测第二套 init bind 源；理由依据：要把 invalid volume specification 提前为可诊断路径门禁而不是运行到 init-db 才失败。
Resolve-DockerDesktopDirectInitBindSource
# [2026-07-17 13:56:30] 作用：在端点缺失、参数漂移或显式重启时拉起受控 Embedding；理由：一键命令必须覆盖 18001 而不是依赖人工预启动。
if($RestartModel -or !(Test-Embedding) -or !(Test-EmbeddingRuntimeContract)){
  # [2026-07-17 13:56:30] 作用：输出 Embedding 启动阶段；理由：单窗口日志需要明确当前进度和故障位置。
  Write-Host "启动 Qwen3 Embedding 本机模型服务 $EmbeddingPort..."
  # [2026-07-17 13:56:30] 作用：释放旧 18001 监听；理由：错误模型或参数漂移的健康实例也必须被当前受控进程替换。
  $embeddingPortReleased=Stop-Port @($EmbeddingPort)
  # [2026-07-17 13:56:30] 作用：端口无法释放时阻断；理由：不能切备用端口导致所有 RAG 配置失联。
  if(!$embeddingPortReleased){throw "Embedding 模型端口 $EmbeddingPort 被旧进程占用，无法启动最新版模型服务"}
  # [2026-07-17 13:56:30] 作用：等待 Windows 回收旧监听；理由：立即 bind 可能命中短暂端口占用。
  Start-Sleep -Seconds 2
  # [2026-07-17 13:56:30] 作用：生成本次 Embedding 日志时间戳；理由：每次一键启动都应保留独立诊断文件。
  $embeddingStamp=Get-Date -Format 'yyyyMMdd-HHmmss'
  # [2026-07-17 13:56:30] 作用：生成 Embedding 标准输出日志；理由：隐藏进程仍必须可追踪。
  $embeddingOut=Join-Path $LogDir "embedding-$embeddingStamp.out.log"
  # [2026-07-17 13:56:30] 作用：生成 Embedding 标准错误日志；理由：模型加载、维度或 llama.cpp 错误需要独立定位。
  $embeddingErr=Join-Path $LogDir "embedding-$embeddingStamp.err.log"
  # [2026-07-17 13:56:30] 作用：构建单线程、单 slot、512 batch 的专用 Embedding 参数；理由：保持 1024 维本地向量能力且不与五线程问答模型争满 CPU。
  $embeddingArgs="-m `"$EmbeddingModelFile`" --alias $EmbeddingModelAlias --host 127.0.0.1 --port $EmbeddingPort -c 2048 -t 1 -tb 1 --parallel 1 -ngl 0 -b 512 -ub 512 --embedding --pooling last --prio 0 --prio-batch 0 --poll 0 --poll-batch 0 --cache-ram 128 --offline --no-ui --timeout 50 --threads-http 1"
  # [2026-07-17 13:56:30] 作用：隐藏启动本地 Embedding 服务并重定向日志；理由：用户只操作一个 PowerShell 窗口。
  $embeddingProcess=Start-Process -FilePath $LlamaExe -ArgumentList $embeddingArgs -WorkingDirectory $LlamaCwd -RedirectStandardOutput $embeddingOut -RedirectStandardError $embeddingErr -WindowStyle Hidden -PassThru
  # [2026-07-17 13:56:30] 作用：保持 Embedding 进程 Normal 优先级；理由：问答 Qwen 使用 AboveNormal，向量服务不应反向抢占交互推理。
  $embeddingProcess.PriorityClass='Normal'
  # [2026-07-17 13:56:30] 作用：等待模型别名端点真实可用；理由：Docker 和业务后端不得在 18001 尚未加载完成时启动。
  Wait-Embedding 180
}else{
  # [2026-07-17 13:56:30] 作用：仅在健康与进程合同均匹配时复用 Embedding；理由：减少无意义重载但不牺牲最新版保证。
  Write-Host 'Embedding 模型服务参数与健康均为最新，跳过重启。'
}
# [2026-07-17 13:56:30] 作用：端点不可用或运行参数漂移时重启 Qwen；理由：健康的旧实例不能绕过五线程、单 slot、160 token 合同。
if($RestartModel -or !(Test-Qwen) -or !(Test-QwenRuntimeContract)){
  Write-Host "启动 Qwen3.5-2B 本机模型服务 $QwenPort..."
  $qwenPortReleased=Stop-Port @($QwenPort)
  if(!$qwenPortReleased){throw "Qwen 模型端口 $QwenPort 被旧进程占用，无法重启模型服务"}
  Start-Sleep -Seconds 2
  $stamp=Get-Date -Format 'yyyyMMdd-HHmmss'
  $qout=Join-Path $LogDir "qwen-$stamp.out.log"
  $qerr=Join-Path $LogDir "qwen-$stamp.err.log"
  # [2026-07-17 12:08:30] 作用：以五个物理核、单 slot、160 token、normal 工作线程和 50 秒传输边界启动本地 Qwen，再把 Windows 进程设为 AboveNormal；理由：不增加线程/token 即可抑制后台抢占，同时避免高/实时 llama 线程或六核争满导致电脑卡死。
  # [2026-07-20 12:19:30] 作用：以 1024-token 自然停止上限和 180 秒请求边界启动同一本地 Qwen；理由依据：只延长单请求生存期，不增加线程、并行 slot、CPU 核数或缓存，避免电脑卡死且不再在 743 token 处取消。
  $qargs="-m `"$ModelFile`" --alias Qwen3.5-2B-Q4_K_M-local-safe --host 127.0.0.1 --port $QwenPort -c 4096 -t 5 -tb 5 --parallel 1 -ngl 0 --temp 0.2 --top-p 0.8 -n 1024 --reasoning off --reasoning-budget 0 --prio 0 --prio-batch 0 --poll 0 --poll-batch 0 --cpu-mask 155 --cpu-mask-batch 155 --cpu-strict 1 --cpu-strict-batch 1 --cache-ram 256 --offline --no-ui --timeout 180 --threads-http 2"
  $q=Start-Process -FilePath $LlamaExe -ArgumentList $qargs -WorkingDirectory $LlamaCwd -RedirectStandardOutput $qout -RedirectStandardError $qerr -WindowStyle Hidden -PassThru
  # [2026-07-17 12:08:30] 作用：固化已实测有效的 Windows 进程级 AboveNormal；理由：Start-Process 默认 Normal 会在安全软件/容器争用时产生 55 秒长尾，AboveNormal 仍低于 High/Realtime 且五核亲和性继续限制资源上限。
  $q.PriorityClass='AboveNormal'
  Wait-Qwen 180
}else{
  Write-Host 'Qwen 模型服务已存在，跳过启动。'
}
if($DockerBackend -eq 'remote_ssh'){
  Sync-MonFangAiRemoteRuntime -SqlRagRoot $SqlRag
  Write-Host "远程 Linux Docker 运行配置已同步：$($RemoteDockerSettings.Host)"
}
# [2026-07-31 09:45:19] 作用：先对齐当前 profile 的独立迁移源容器；理由依据：必须在主 Compose 占用 checkpoint 端口前完成迁移库端口和身份校验。
# [2026-08-04 17:02:16] 作用：把迁移PostgreSQL的创建、补缺恢复和ORM迁移收敛为一个依赖组；理由依据：该组失败时Knowledge/资产/Getsoft会红，但模型与其余可创建服务仍必须继续尝试。
try{
  # [2026-08-04 17:02:17] 作用：创建并幂等恢复当前profile迁移库；理由依据：保留原第一套成功路径和第二套非覆盖式数据自愈。
  Ensure-OptionalMigratedPostgresProfile
  # [2026-08-04 17:02:18] 作用：验证迁移库容器、端口与profile隔离；理由依据：成功组仍必须满足原有防串线合同。
  Assert-OptionalMigratedPostgresRuntimeIsolation
  # [2026-07-31 10:32:27] 作用：在拉起 Getsoft 业务进程前固化恢复库的 ORM 兼容合同；理由依据：端口健康不能掩盖读取历史会话时的缺列故障。
  Ensure-MigratedPostgresGetsoftSchemaCompatibility
}catch{
  # [2026-08-31 14:43:17] 作用：两套统一传播迁移PostgreSQL失败；理由依据：第二套PgBouncer依赖25434数据库，带病继续只会把上游根因改写成pgbouncer unhealthy。
  throw
}
# [2026-07-31 09:45:20] 作用：强制按当前 profile 项目、容器名和端口重建基础容器；理由依据：旧容器可能保留“请求了 15432 但实际未发布”的半失效 HostConfig，普通 up 不会自动修复。
# [2026-08-04 17:02:21] 作用：把主Compose、数据端口与种子恢复收敛为第二个可隔离依赖组；理由依据：一个容器失败后仍需进入Python业务进程逐项启动，而不是停在数据层门禁。
try{
  # [2026-08-04 17:02:22] 作用：启动主数据平面的全部容器；理由依据：维持第一套已验证的同一Compose服务集合和顺序。
  Compose @('up','-d','--force-recreate','sqlserver','qdrant','postgres-checkpoint','external-sqlserver','external-qdrant','neo4j','wkt-prasing-extra-postgres','wkt-prasing-extra-qdrant')
Assert-DatabaseRuntimeIsolation
Wait-Port '主SQL Server' $MainSqlServerPort 420
Wait-Port '主Qdrant' $MainQdrantHttpPort 240
Wait-Port 'Postgres checkpoint' $PostgresCheckpointPort 240
Wait-Port 'External SQL Server' $ExternalSqlServerPort 420
Wait-Port 'External Qdrant' $ExternalQdrantHttpPort 240
Wait-Port 'Neo4j' $Neo4jHttpPort 300
Wait-Port 'wkt_prasing_extra PostgreSQL' $ClonePostgresPort 240
Wait-Port 'wkt_prasing_extra Qdrant HTTP' $CloneQdrantHttpPort 240
Wait-Port 'wkt_prasing_extra Qdrant gRPC' $CloneQdrantGrpcPort 240
# [2026-07-31 15:27:21] 作用：在实体 Windows 第二套 profile 首次启动时恢复核心关系库与向量库；理由依据：此前只恢复商业克隆库会让 28182 因空 getai 和空主 Qdrant 判定不健康。
# [2026-08-03 15:42:43] 作用：只为第二套独立profile启用管理员原生Docker全栈路径；理由依据：彻底移除历史aliyun兼容分支。
if($DeploymentProfile-eq'server_second_ports'-and$usesIndependentServiceProfile-and$DockerBackend-eq'desktop'){
  # [2026-07-31 15:27:21] 作用：要求核心种子目录随正式程序包存在；理由依据：新服务器不依赖外网或开发机即可恢复业务数据。
  if(-not (Test-Path -LiteralPath $PortableCoreSeedDir -PathType Container)){throw "核心数据可移植种子不存在：$PortableCoreSeedDir"}
  # [2026-07-31 15:27:21] 作用：要求核心恢复工具随正式程序包存在；理由依据：禁止用人工临时命令替代固定部署逻辑。
  if(-not (Test-Path -LiteralPath $PortableCoreSeedRestoreScript -PathType Leaf)){throw "核心数据恢复工具不存在：$PortableCoreSeedRestoreScript"}
  # [2026-07-31 15:27:21] 作用：对第二套独立容器执行哈希校验、空库恢复和数量复核；理由依据：只恢复缺失数据，已有实时数据在日常一键重启时保持不变。
  & $PortableCoreSeedRestoreScript `
    -SeedDir $PortableCoreSeedDir `
    -MainSqlContainer $DatabaseContainerNames.SqlServer `
    -ExternalSqlContainer $DatabaseContainerNames.ExternalSqlServer `
    -MainQdrantPort $MainQdrantHttpPort `
    -ExternalQdrantPort $ExternalQdrantHttpPort
  # [2026-07-31 15:27:21] 作用：核心恢复工具返回失败时阻断全栈启动；理由依据：端口监听不能掩盖数据恢复失败。
  if($LASTEXITCODE -ne 0){throw '第二套核心 SQL Server / Qdrant 可移植种子恢复失败'}
  # [2026-07-31 15:27:21] 作用：在主库恢复后幂等创建 dev 登录和数据库用户；理由依据：数据库备份不包含 SQL Server 实例级登录。
  Compose @('run','--rm','init-db')
  # [2026-07-31 15:27:21] 作用：在外部库恢复后幂等创建独立登录和数据库用户；理由依据：外部 SQL Server 也必须具备可用的应用身份。
  Compose @('run','--rm','init-external-db')
}elseif($RunDatabaseInit){
  # [2026-07-31 15:27:21] 作用：保留本地第一套显式初始化开关；理由依据：本地维护行为不因第二套自动恢复逻辑而改变。
  Compose @('run','--rm','init-db')
  # [2026-07-31 15:27:21] 作用：保留本地第一套外部库显式初始化；理由依据：两套入口继续共享同一维护合同。
  Compose @('run','--rm','init-external-db')
}
# [2026-07-25 15:10:16] 作用：四个 Qdrant 回环端口就绪后再验证可信私网入口；理由依据：任何代理丢失都必须阻断全量成功。
Assert-TrustedQdrantAccess
# [2026-07-28] 作用：四个常驻关系数据库端口就绪后再验证可信私网入口；理由依据：局域网调用方不能再因仅开放 Qdrant 而无法连接业务所需 SQL Server/PostgreSQL。
Assert-TrustedRelationalDatabaseAccess
# [2026-07-20 14:31:00] 作用：要求迁移恢复工具随项目存在；理由依据：缺少它时另一台电脑的空 Docker 卷无法自动恢复两个克隆库。
if(!(Test-Path -LiteralPath $PortableCloneScript)){throw "克隆库可移植恢复工具不存在：$PortableCloneScript"}
# [2026-07-20 14:31:00] 作用：在访问权威源前先从随包种子幂等恢复空 PG/Qdrant；理由依据：部署机即使暂时无法访问 172.18.1.166，也能在 Navicat 和 6335 dashboard 看到两个克隆库。
& $Py $PortableCloneScript ensure --seed-dir $PortableCloneSeedDir --env-file $EnvFile
# [2026-07-20 14:31:00] 作用：阻断损坏或半恢复的随包种子；理由依据：只有清单哈希与恢复数量通过才能继续启动商业服务。
if($LASTEXITCODE -ne 0){throw 'wkt_prasing_extra / wkt_prasing_extra_dev 可移植种子恢复失败'}
# [2026-07-20 14:31:00] 作用：初始化在线权威源刷新状态；理由依据：在线同步与离线种子验收必须给出明确分支而不是互相覆盖结果。
$WktOnlineCloneReady=$false
# [2026-08-04 08:41:47] 作用：只在第一套既有策略要求时执行有界在线克隆；理由依据：第二套portable_seed_only必须完全摆脱第一套权威源和重复复制超时。
if($CloneRefreshMode-eq'online_then_portable'){
  # [2026-08-03 09:06:46] 作用：读取在线权威库克隆总超时覆盖值；理由依据：允许大数据环境按运维配置延长，但固定入口仍不能无限等待。
  $OnlineCloneTimeoutSeconds=180
  # [2026-08-03 09:06:47] 作用：解析合法的在线克隆秒数覆盖；理由依据：超时必须限制在30至3600秒，避免零值或极大值重新制造无上限阻塞。
  if(-not [string]::IsNullOrWhiteSpace([string]$env:SQL_RAG_ONLINE_CLONE_TIMEOUT_SECONDS)){if(-not [int]::TryParse([string]$env:SQL_RAG_ONLINE_CLONE_TIMEOUT_SECONDS,[ref]$OnlineCloneTimeoutSeconds) -or $OnlineCloneTimeoutSeconds -lt 30 -or $OnlineCloneTimeoutSeconds -gt 3600){throw 'SQL_RAG_ONLINE_CLONE_TIMEOUT_SECONDS 必须为30至3600秒整数。'}}
  # [2026-08-03 09:06:48] 作用：在父进程硬上限内尝试刷新权威 AIERP 克隆；理由依据：成功时保留最新数据，超时或失败时继续验证已恢复基线。
  $OnlineCloneResult=Invoke-BoundedOnlineClone -TimeoutSeconds $OnlineCloneTimeoutSeconds
  # [2026-07-20 14:31:00] 作用：仅在全量克隆成功后执行源目标深度复核；理由依据：源库不可达时不得让 verify 的二次连接掩盖随包恢复结果。
  if(-not $OnlineCloneResult.TimedOut -and $OnlineCloneResult.ExitCode -eq 0){
    # [2026-07-11 18:12:00] 作用：执行结构、约束、索引和行数复核；理由依据：不能只相信克隆脚本自身返回成功。
    & $Py $VerifyWktCloneScript
    # [2026-07-20 14:31:00] 作用：记录在线刷新与复核同时成功；理由依据：后续输出需区分最新源数据和随包基线。
    if($LASTEXITCODE -eq 0){$WktOnlineCloneReady=$true}
  }
  # [2026-08-03 09:06:49] 作用：明确报告在线克隆超时并进入本地基线复核；理由依据：旧逻辑无输出卡住时用户无法区分正常复制与数据库死等。
  if($OnlineCloneResult.TimedOut){Write-Warning "在线权威库克隆超过${OnlineCloneTimeoutSeconds}秒，已终止并回滚未提交事务；继续验证随包基线。错误日志=$($OnlineCloneResult.StderrLog)"}
}
# [2026-07-20 14:31:00] 作用：权威源暂不可达或在线复核失败时验证本地可移植基线；理由依据：另一台电脑不应因 LAN 源库暂时离线而丢失两个克隆库。
if(!$WktOnlineCloneReady){
  # [2026-07-20 14:31:00] 作用：依据随包清单验证表、行和 point 数量；理由依据：只有真实本地数据完整时才允许离线继续。
  & $Py $PortableCloneScript verify --seed-dir $PortableCloneSeedDir --env-file $EnvFile
  # [2026-07-20 14:31:00] 作用：本地基线也不完整时终止；理由依据：禁止空库或残缺 collection 冒充可部署状态。
  if($LASTEXITCODE -ne 0){throw '权威源刷新失败，且随包 wkt_prasing_extra / wkt_prasing_extra_dev 基线不可用'}
  # [2026-08-04 08:41:48] 作用：为第二套输出确定的随包数据验收结论；理由依据：portable_seed_only是正式独立策略，不应继续被误报为权威源故障降级。
  if($CloneRefreshMode-eq'portable_seed_only'){Write-Host '第二套随包数据基线已校验通过；本次不连接第一套权威源，不执行重复在线克隆。'}
  # [2026-08-04 08:41:49] 作用：只为第一套在线刷新失败保留原告警；理由依据：本地既有降级可观察性不得因第二套修复而消失。
  if($CloneRefreshMode-eq'online_then_portable'){Write-Warning '权威 AIERP 当前不可达或深度复核失败；已使用随项目携带且校验通过的两个克隆库基线继续启动。'}
}
  # [2026-08-04 17:02:23] 作用：标记主数据平面完整走完；理由依据：仅用于明确try边界，不改变已有种子恢复或在线刷新判断。
  Write-Host '主数据平面启动与随包数据门禁已完成。'
}catch{
  # [2026-08-31 14:43:17] 作用：两套统一传播主数据平面失败；理由依据：独立运行不等于允许数据库或向量库失败后继续拉业务服务，必须在最初故障点停止。
  throw
}
if($RebuildExternalQdrant){
  Push-Location $RepoRoot
  & $Py app\SQL_RAG\data_cleaning\test_External_database_connection_conversion\external_database_to_qdrant_conversion.py --recreate --source-profile $ExternalSourceProfile
  if($LASTEXITCODE -ne 0){throw 'sql_External_database 重建失败'}
  Pop-Location
}
# 2026-07-01 10:42:09 新增：先清理本项目旧 Python 服务；作用：释放上一轮备用端口上的旧实例；理由：保证重复执行脚本时端口不会持续向后漂移。
Stop-SqlRagPythonApps
# [2026-07-04 10:18:20] 作用：在启动前校验知识库专用解释器真实存在；理由依据：缺失运行环境时应立即失败并给出明确原因，不能进入伪 ready 状态。
if(!(Test-Path -LiteralPath $KnowledgePy)){throw "知识库 Python 解释器不存在：$KnowledgePy"}
# [2026-08-29 09:02:10] 作用：声明知识库Python安全调用函数；理由依据：Windows PowerShell 5.1会把原生Python stderr包装成RemoteException并在ErrorActionPreference=Stop下提前终止，必须先捕获退出码再决定是否离线修复。
function Invoke-KnowledgePythonSafe{
  # [2026-08-29 09:02:11] 作用：接收知识库Python参数和失败提示；理由依据：导入探针与离线pip安装必须共用同一条不抛stderr的调用路径。
  param([Parameter(Mandatory=$true)][string[]]$Arguments,[Parameter(Mandatory=$true)][string]$FailureMessage)
  # [2026-08-29 09:02:12] 作用：初始化原生进程输出和退出码；理由依据：Python在异常路径可能尚未写入PowerShell的LASTEXITCODE。
  $capturedOutput=@()
  # [2026-08-29 09:02:13] 作用：初始化安全失败状态；理由依据：任何启动异常都必须进入离线依赖修复分支而不能伪装成功。
  $exitCode=1
  # [2026-08-29 09:02:14] 作用：执行知识库Python并合并标准输出与错误输出；理由依据：捕获ErrorRecord后由调用方按退出码处理，避免PS5.1把原生stderr直接升级为终止异常。
  try{
    # [2026-08-29 09:02:15] 作用：运行导入或pip命令并收集诊断文本；理由依据：同一解释器必须在无公网条件下验证和修复。
    $capturedOutput=@(& $KnowledgePy @Arguments 2>&1)
    # [2026-08-29 09:02:16] 作用：读取Python真实退出码；理由依据：stderr可能只是警告，只有非零退出才允许触发修复。
    $exitCode=[int]$LASTEXITCODE
  }catch{
    # [2026-08-29 09:02:17] 作用：把PowerShell包装的原生异常转换为可观察失败；理由依据：Windows PowerShell 5.1的RemoteException不应阻断后续离线安装逻辑。
    $capturedOutput+=@($_.Exception.Message)
    # [2026-08-29 09:02:18] 作用：保持失败退出码；理由依据：异常路径仍必须进入确定性的wheelhouse修复。
    $exitCode=1
  }
  # [2026-08-29 09:02:19] 作用：在命令失败时输出截断诊断；理由依据：运维需要知道缺少哪个模块，同时避免把完整环境或密钥写入日志。
  if($exitCode-ne0){$diagnostic=($capturedOutput|ForEach-Object{[string]$_}|Where-Object{$_})-join' | ';if($diagnostic.Length-gt800){$diagnostic=$diagnostic.Substring(0,800)};if([string]::IsNullOrWhiteSpace($diagnostic)){$diagnostic='无Python输出'};Write-Warning "$FailureMessage；exit=$exitCode；diagnostic=$diagnostic";return $false}
  # [2026-08-29 09:02:20] 作用：返回知识库Python调用成功；理由依据：只有零退出码才能跳过离线补包并继续启动服务。
  return $true
}
# [2026-09-01 11:29:06] 作用：声明知识库 API 的解析、Celery 硬暂停和 MinIO 对象存储依赖；理由依据：两套固定入口必须在绑定 Knowledge 端口前闭合已实锤缺失的 minio 7.2.16，不能等业务模块导入时退出。
$KnowledgeRequiredPackages=@('jsonpointer','scikit-learn','celery==5.6.3','minio==7.2.16')
# [2026-08-17 17:41:22] 作用：定位随迁移包携带的 Knowledge 离线轮子仓；理由依据：第一套修复和第二套无 VPN 服务器均不得在启动阶段访问公网。
$KnowledgeOfflineWheelhouse=Join-Path $RepoRoot 'app\SQL_RAG\deployment\alicloud_win11_migration\artifacts\wheelhouse\knowledge'
# [2026-09-01 11:29:06] 作用：用知识库专用解释器验证解析、Celery 控制和 MinIO SDK 可导入；理由依据：第一套现有健康环境与第二套已修复环境必须使用同一依赖门禁，禁止 28320 因缺少 minio 在导入阶段退出。
$knowledgeDependencyProbe=Invoke-KnowledgePythonSafe -Arguments @('-c',"import jsonpointer, sklearn, celery, minio; print('knowledge dependency check ok')") -FailureMessage '知识库依赖导入预检失败'
# [2026-07-07 11:16:42] 作用：判断知识库依赖预检是否失败；理由依据：失败时应在启动后端前修复依赖，而不是等前端页面出现空下拉。
if(-not$knowledgeDependencyProbe){
  # [2026-08-17 17:41:22] 作用：验证 Knowledge 离线轮子仓真实存在；理由依据：目标服务器禁止 VPN 和公网安装，缺少离线资产必须 fail-closed。
  if(!(Test-Path -LiteralPath $KnowledgeOfflineWheelhouse -PathType Container)){throw "知识库离线轮子仓不存在：$KnowledgeOfflineWheelhouse"}
  # [2026-08-17 17:41:22] 作用：仅从随包 wheelhouse 修复知识库专用虚拟环境；理由依据：启动过程必须可在完全断网条件下补齐 Celery 控制面及原解析依赖。
  # [2026-08-29 09:02:21] 作用：从完整Knowledge wheelhouse离线重装解析依赖和Celery控制面；理由依据：第二套永久离线且scikit-learn依赖闭包必须与更新包原子交付。
  $knowledgeInstallProbe=Invoke-KnowledgePythonSafe -Arguments (@('-m','pip','install','--disable-pip-version-check','--no-index','--find-links',$KnowledgeOfflineWheelhouse,'--reinstall')+$KnowledgeRequiredPackages) -FailureMessage '知识库依赖纯离线修复失败'
  # [2026-09-01 11:29:06] 作用：检查包含 MinIO 的纯离线安装返回码；理由依据：禁止静默切换公网源或在对象存储、解析及暂停控制能力缺失时报告 ready。
  if(-not$knowledgeInstallProbe){throw '知识库依赖纯离线修复失败：jsonpointer/scikit-learn/celery/minio 未能安装到 Knowledge_management\.venv'}
  # [2026-08-17 17:41:22] 作用：二次验证隔离依赖和 Celery 控制库可导入；理由依据：必须证明解析与硬暂停控制面均可用后才允许启动服务。
  # [2026-09-01 11:29:06] 作用：二次安全导入验证解析、Celery 控制和 MinIO 离线修复结果；理由依据：必须证明对象存储适配器的直接 SDK 依赖也可导入后才允许启动 Knowledge 服务。
  $knowledgeDependencyProbe=Invoke-KnowledgePythonSafe -Arguments @('-c',"import jsonpointer, sklearn, celery, minio; print('knowledge dependency check ok')") -FailureMessage '知识库依赖安装后二次导入失败'
  # [2026-07-07 11:16:42] 作用：检查二次导入验证返回码；理由依据：验证失败说明知识库后端仍然无法安全启动。
  if(-not$knowledgeDependencyProbe){throw '知识库依赖安装后仍无法导入，请检查 Knowledge_management\.venv'}
}
# [2026-07-04 12:08:00] 作用：定位知识库前端主模块；理由依据：全量启动必须在报告 WebUI ready 前验证浏览器实际加载的 JavaScript 文件。
$KnowledgeFrontendEntry=Join-Path $RepoRoot 'app\SQL_RAG\Knowledge_management\webui\src\app.mjs'
# [2026-07-04 12:08:00] 作用：验证 Node.js 命令真实可用；理由依据：前端语法门禁依赖 Node 解析器，缺少运行时应立即失败而不是继续启动空白页面。
if(!(Get-Command node -ErrorAction SilentlyContinue)){throw 'Node.js 不可用，无法校验知识库前端语法。'}
# [2026-07-04 12:08:00] 作用：执行知识库前端入口语法检查；理由依据：防止健康接口返回 200 但 app.mjs 因语法错误无法渲染的假 ready。
node --check $KnowledgeFrontendEntry
# [2026-07-04 12:08:00] 作用：在前端语法检查失败时终止全量启动；理由依据：页面不可执行时不能向用户报告前后端服务已全部就绪。
if($LASTEXITCODE -ne 0){throw "知识库前端 JavaScript 语法检查失败：$KnowledgeFrontendEntry"}
# [2026-07-21 13:38:04] 作用：定位客户风险与商机看板前端入口；理由依据：全量启动前必须阻断浏览器语法错误。
$DashboardFrontendEntry=Join-Path $RepoRoot 'app\SQL_RAG\Knowledge_Analysis\Customer_Risk_BusinessOpportunity_Perception_Dashboard\webui\src\app.mjs'
# [2026-07-21 13:38:05] 作用：检查看板入口JavaScript语法；理由依据：静态健康200不能证明动态页面可执行。
node --check $DashboardFrontendEntry
# [2026-07-21 13:38:06] 作用：在看板语法错误时中止；理由依据：不允许把空白页纳入全量ready。
if($LASTEXITCODE -ne 0){throw "客户风险与商机看板 JavaScript 语法检查失败：$DashboardFrontendEntry"}
# [2026-07-29 13:16:00] 作用：统一释放主业务与资产业务的固定直连端口；理由依据：每个端口必须由本轮对应业务进程唯一持有且不得漂移到内部网关端口。
$corePortsReleased=Stop-Port @($BackendPort,$WebPort,$AssetTypeBackendPort,$AssetTypeWebPort)
# [2026-07-29 13:16:00] 作用：计算旧 18192/28192 网关拓扑遗留端口；理由依据：首次切换到直连架构时必须清理昨天留下的 Python 内部页面进程。
$RetiredUnifiedWebPort=$AssetTypeWebPort+1
# [2026-07-29 13:16:00] 作用：停止旧内部页面端口但不再将其作为服务启动；理由依据：防止孤儿进程继续代理旧代码或造成运维误判。
$retiredUnifiedWebPortReleased=Stop-Port @($RetiredUnifiedWebPort)
# [2026-07-29 13:16:00] 作用：阻断无法释放的旧网关实例；理由依据：端口仍监听说明旧拓扑没有真正退出。
if(!$retiredUnifiedWebPortReleased -and (Get-NetTCPConnection -LocalPort $RetiredUnifiedWebPort -State Listen -ErrorAction SilentlyContinue)){
  # [2026-07-29 13:16:00] 作用：抛出旧网关端口的明确错误；理由依据：不能在残留服务并存时声称业务端口不再串线。
  throw "退役统一页面内部端口 $RetiredUnifiedWebPort 仍被旧进程占用。"
}
# [2026-07-07 12:00:18] 作用：单独释放知识库后端端口；理由依据：后端端口必须尽量保持 18320，才能继续服务固定 18321 WebUI 的代理请求。
$knowledgeBackendPortReleased=Stop-Port @($KnowledgeBackendPort)
# [2026-07-07 12:00:18] 作用：单独释放知识库 WebUI 端口；理由依据：18321 是用户实际访问入口，不能因为释放失败就静默改到备用入口。
$knowledgeWebPortReleased=Stop-Port @($KnowledgeWebPort)
# [2026-07-21 13:38:07] 作用：释放看板前后端固定端口；理由依据：必须启动本次工作区新进程而非复用旧代码。
$dashboardPortsReleased=Stop-Port @($DashboardBackendPort,$DashboardWebPort)
# [2026-07-25 15:10:19] 作用：端口配置中的固定入口无法释放时直接失败；理由依据：自动漂移会破坏 local/aliyun 两套端口合同和安全组配置。
if(!$corePortsReleased){
  $remainingCoreListeners=@(
    Get-NetTCPConnection `
      -LocalPort @(
        $BackendPort,
        $WebPort,
        $AssetTypeBackendPort,
        $AssetTypeWebPort
      ) `
      -State Listen `
      -ErrorAction SilentlyContinue
  )
  $listenerSummary=@(
    $remainingCoreListeners |
      ForEach-Object {
        "$($_.LocalAddress):$($_.LocalPort)/PID=$($_.OwningProcess)"
      } |
      Sort-Object -Unique
  ) -join '; '
  if([string]::IsNullOrWhiteSpace($listenerSummary)){
    $listenerSummary='端口释放检查返回失败但未读到监听 PID'
  }
  throw "端口配置 $DeploymentProfile 的固定服务端口未能释放：$listenerSummary"
}
# [2026-07-15 10:04:45] 作用：知识库后端端口无法释放时拒绝启动；理由依据：复用旧进程无法保证运行的是当前工作区最新逻辑。
if(!$knowledgeBackendPortReleased){
  # [2026-07-15 10:04:45] 作用：读取仍占用知识库后端端口的 PID；理由依据：失败信息必须指出需要关闭的旧服务实例。
  $knowledgeBackendLeft=Get-NetTCPConnection -LocalPort $KnowledgeBackendPort -State Listen -ErrorAction SilentlyContinue
  # [2026-07-15 10:04:45] 作用：仅在端口仍被占用时阻断；理由依据：停止函数返回失败但端口已经释放时允许继续创建新进程。
  if($knowledgeBackendLeft){
    # [2026-07-15 10:04:45] 作用：合并旧后端 PID；理由依据：用户需要明确识别阻止最新服务启动的进程。
    $knowledgeBackendPids=($knowledgeBackendLeft | Select-Object -ExpandProperty OwningProcess -Unique) -join ','
    # [2026-07-15 10:04:45] 作用：拒绝把旧后端当作当前服务；理由依据：当前逻辑保证要求本次必须创建新进程。
    throw "知识库后端端口 $KnowledgeBackendPort 仍被旧进程占用，PID=$knowledgeBackendPids；拒绝复用旧服务。"
  }
}
# [2026-07-15 10:04:45] 作用：知识库 WebUI 端口无法释放时拒绝启动；理由依据：旧页面进程可能仍代理旧后端，不能标记为当前最新服务。
if(!$knowledgeWebPortReleased){
  # [2026-07-15 10:04:45] 作用：读取仍占用知识库 WebUI 端口的 PID；理由依据：失败信息必须指出旧页面进程。
  $knowledgeWebLeft=Get-NetTCPConnection -LocalPort $KnowledgeWebPort -State Listen -ErrorAction SilentlyContinue
  # [2026-07-15 10:04:45] 作用：仅在端口仍被占用时阻断；理由依据：端口已释放时允许启动当前 WebUI。
  if($knowledgeWebLeft){
    # [2026-07-15 10:04:45] 作用：合并旧 WebUI PID；理由依据：用户需要知道哪个实例阻止新页面启动。
    $knowledgeWebPids=($knowledgeWebLeft | Select-Object -ExpandProperty OwningProcess -Unique) -join ','
    # [2026-07-15 10:04:45] 作用：拒绝复用旧 WebUI；理由依据：当前逻辑保证要求本次必须创建新进程。
    throw "知识库 WebUI 端口 $KnowledgeWebPort 仍被旧进程占用，PID=$knowledgeWebPids；拒绝复用旧服务。"
  }
}
# [2026-07-21 13:38:08] 作用：拒绝看板端口仍被旧进程占用；理由依据：复用旧实例无法证明运行的是当前动态后端逻辑。
if(!$dashboardPortsReleased){
  # [2026-07-21 13:38:09] 作用：读取仍占用看板端口的监听；理由依据：失败信息需要给出准确端口和进程。
  $dashboardLeft=Get-NetTCPConnection -LocalPort @($DashboardBackendPort,$DashboardWebPort) -State Listen -ErrorAction SilentlyContinue
  # [2026-07-21 13:38:10] 作用：仅在仍有监听时阻断；理由依据：停止函数报告失败但端口已释放时允许继续。
  if($dashboardLeft){
    # [2026-07-21 13:38:11] 作用：合并旧进程PID；理由依据：用户可据此识别阻挡最新服务的实例。
    $dashboardPids=($dashboardLeft | Select-Object -ExpandProperty OwningProcess -Unique) -join ','
    # [2026-07-21 13:38:12] 作用：抛出明确端口占用错误；理由依据：18430/18431是本模块固定合同。
    throw "客户风险与商机看板端口仍被旧进程占用，PID=$dashboardPids；拒绝复用旧服务。"
  }
}
Start-Sleep -Seconds 2
$stamp=Get-Date -Format 'yyyyMMdd-HHmmss'
$berr=Join-Path $LogDir "backend-$stamp.err.log"
$bout=Join-Path $LogDir "backend-$stamp.out.log"
$werr=Join-Path $LogDir "webui-$stamp.err.log"
$wout=Join-Path $LogDir "webui-$stamp.out.log"
# 2026-07-01 12:16:10 新增：资产类型后端日志路径；作用：排查 PG 入库服务启动失败；理由：不能只看主业务脑日志。
$assetBackendErr=Join-Path $LogDir "asset-type-backend-$stamp.err.log"
# 2026-07-01 12:16:11 新增：资产类型后端标准输出日志；作用：记录 uvicorn ready 和请求；理由：便于确认独立服务是否启动。
$assetBackendOut=Join-Path $LogDir "asset-type-backend-$stamp.out.log"
# 2026-07-01 12:16:12 新增：资产类型 WebUI 错误日志；作用：排查静态代理启动失败；理由：用户之前遇到 127.0.0.1 拒绝连接。
$assetWebErr=Join-Path $LogDir "asset-type-webui-$stamp.err.log"
# 2026-07-01 12:16:13 新增：资产类型 WebUI 标准输出日志；作用：记录代理目标和访问日志；理由：确认 /api 是否转发到正确后端。
$assetWebOut=Join-Path $LogDir "asset-type-webui-$stamp.out.log"
# [2026-07-04 10:18:20] 作用：生成知识库后端标准错误日志路径；理由依据：真实语音解析、DeepSeek 提取或数据库连接失败时必须保留可追溯证据。
$knowledgeBackendErr=Join-Path $LogDir "knowledge-backend-$stamp.err.log"
# [2026-07-04 10:18:20] 作用：生成知识库后端标准输出日志路径；理由依据：需要记录 Uvicorn 启动状态及端到端请求访问日志。
$knowledgeBackendOut=Join-Path $LogDir "knowledge-backend-$stamp.out.log"
# [2026-07-04 10:18:20] 作用：生成知识库 WebUI 标准错误日志路径；理由依据：静态服务或 API 代理失败必须能独立排查。
$knowledgeWebErr=Join-Path $LogDir "knowledge-webui-$stamp.err.log"
# [2026-07-04 10:18:20] 作用：生成知识库 WebUI 标准输出日志路径；理由依据：需要核对前端监听端口和实际后端代理目标。
$knowledgeWebOut=Join-Path $LogDir "knowledge-webui-$stamp.out.log"
# [2026-07-21 13:38:13] 作用：生成看板后端错误日志；理由依据：数据库或DeepSeek故障需与其他服务分离诊断。
$dashboardBackendErr=Join-Path $LogDir "dashboard-backend-$stamp.err.log"
# [2026-07-21 13:38:14] 作用：生成看板后端输出日志；理由依据：记录Uvicorn启动和动态请求。
$dashboardBackendOut=Join-Path $LogDir "dashboard-backend-$stamp.out.log"
# [2026-07-21 13:38:15] 作用：生成看板WebUI错误日志；理由依据：代理和静态服务问题需独立追踪。
$dashboardWebErr=Join-Path $LogDir "dashboard-webui-$stamp.err.log"
# [2026-07-21 13:38:16] 作用：生成看板WebUI输出日志；理由依据：记录18431监听与代理目标。
$dashboardWebOut=Join-Path $LogDir "dashboard-webui-$stamp.out.log"
# [2026-08-04 16:18:30] 作用：在主业务脑启动前复用Getsoft适配器准备当前profile的同版BM25缓存；理由依据：PostgreSQL到Qdrant实时同步在Getsoft正式进程之前运行，缓存若后注入会卡在隐式模型下载。
# [2026-08-04 17:02:26] 作用：初始化BM25缓存路径和准备结果；理由依据：第二套准备失败后必须能无歧义地跳过环境注入并继续创建其他服务。
$SqlRagBm25CacheDir=''; $bm25PrepareReady=$false
# [2026-08-04 17:02:27] 作用：把BM25准备收敛为可隔离的业务脑依赖阶段；理由依据：缓存失败只影响业务脑稀疏同步与Getsoft，不得阻止资产、Knowledge和看板进程创建。
try{
  # [2026-08-04 16:18:30] 作用：调用适配器准备当前profile的同版BM25缓存；理由依据：PostgreSQL到Qdrant实时同步必须优先使用随包离线实体。
  $bm25PrepareOutput=@(& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $GetsoftAdapterScript -OwnerRepoRoot $RepoRoot -PublicHost $PublicHost -ConfigPath $GetsoftConfigPath -PrepareBm25Only 2>&1)
  # [2026-08-04 16:18:30] 作用：记录BM25准备子进程退出码；理由依据：原生PowerShell错误不会自动服从父启动器的Stop策略。
  $bm25PrepareExitCode=$LASTEXITCODE
  # [2026-08-04 16:18:30] 作用：拒绝缓存安装、SHA或实体门禁失败；理由依据：异常由外层按local严格或第二套隔离策略处理。
  if($bm25PrepareExitCode-ne0){throw "SQL_RAG主链路BM25离线缓存准备失败：exit=$bm25PrepareExitCode；output=$($bm25PrepareOutput -join ' | ')"}
  # [2026-08-04 16:18:30] 作用：从适配器输出中提取唯一的缓存就绪标记；理由依据：普通诊断文本不能被误当成模型目录。
  $bm25PrepareMarkers=@($bm25PrepareOutput|ForEach-Object{[string]$_}|Where-Object{$_.StartsWith('SQL_RAG_BM25_CACHE_READY|')})
  # [2026-08-04 16:18:30] 作用：要求适配器只返回一个可审计路径；理由依据：缺失或多profile输出都会造成业务脑读取不确定缓存。
  if($bm25PrepareMarkers.Count-ne1){throw "SQL_RAG主链路BM25离线缓存标记无效：output=$($bm25PrepareOutput -join ' | ')"}
  # [2026-08-04 16:18:30] 作用：提取并规范化已验收缓存绝对路径；理由依据：FastEmbed需要实际目录而不是ZIP或模型名。
  $SqlRagBm25CacheDir=([string]$bm25PrepareMarkers[0]).Substring('SQL_RAG_BM25_CACHE_READY|'.Length).Trim()
  # [2026-08-04 16:18:30] 作用：再次确认父进程可见该缓存目录；理由依据：子进程成功输出后仍可能遇到路径权限或被清理的竞态。
  if([string]::IsNullOrWhiteSpace($SqlRagBm25CacheDir)-or!(Test-Path -LiteralPath $SqlRagBm25CacheDir -PathType Container)){throw "SQL_RAG主链路BM25离线缓存目录不可用：$SqlRagBm25CacheDir"}
  # [2026-08-04 17:02:28] 作用：标记缓存准备完成；理由依据：只有成功标记才允许向业务脑注入离线目录和禁止联网变量。
  $bm25PrepareReady=$true
}catch{
  # [2026-08-31 14:43:17] 作用：两套统一传播BM25缓存门禁失败；理由依据：缺失业务检索资产时继续启动不能算与第一套同逻辑的完整服务。
  throw
}
# [2026-08-04 16:18:30] 作用：保存父进程已有的主链路BM25缓存环境；理由依据：只允许业务脑子进程消费，不能把本次profile串到后续独立服务。
$previousSqlRagBm25CacheDir=[Environment]::GetEnvironmentVariable('SQL_RAG_BM25_CACHE_DIR','Process')
# [2026-08-04 16:18:30] 作用：保存父进程已有的Hugging Face离线状态；理由依据：事务结束必须完整恢复调用者环境。
$previousHfHubOffline=[Environment]::GetEnvironmentVariable('HF_HUB_OFFLINE','Process')
# [2026-08-04 16:18:30] 作用：保存父进程已有的Transformers离线状态；理由依据：独立Getsoft适配器稍后会注入自己的profile环境。
$previousTransformersOffline=[Environment]::GetEnvironmentVariable('TRANSFORMERS_OFFLINE','Process')
# [2026-08-04 16:18:30] 作用：进入业务脑单进程BM25环境注入事务；理由依据：无论Start-Process是否成功都必须恢复父环境。
try{
  # [2026-08-04 16:18:30] 作用：向主业务脑注入当前profile已验收缓存；理由依据：外部源实时同步必须确定性加载Qdrant/bm25。
  if($bm25PrepareReady){[Environment]::SetEnvironmentVariable('SQL_RAG_BM25_CACHE_DIR',$SqlRagBm25CacheDir,'Process')}
  # [2026-08-04 16:18:30] 作用：禁止业务脑子进程在缓存缺失时访问Hugging Face；理由依据：第二套无VPN环境不能以网络下载作为启动路径。
  if($bm25PrepareReady){[Environment]::SetEnvironmentVariable('HF_HUB_OFFLINE','1','Process')}
  # [2026-08-04 16:18:30] 作用：禁止下层模型组件隐式联网；理由依据：缓存实体已通过20文件和27774字节门禁。
  if($bm25PrepareReady){[Environment]::SetEnvironmentVariable('TRANSFORMERS_OFFLINE','1','Process')}
  # [2026-08-04 16:18:30] 作用：以隔离后的BM25环境启动主业务脑；理由依据：该进程内部负责PostgreSQL到Qdrant实时同步并必须继承缓存合同。
  $backend=Start-SqlRagServiceProcess -Stage 'business_brain_backend_process' -StartAction {Start-Process -FilePath $Py -ArgumentList @('app\SQL_RAG\main.py','business-brain-service','--host',$BusinessListenHost,'--port',"$BackendPort") -WorkingDirectory $RepoRoot -RedirectStandardOutput $bout -RedirectStandardError $berr -WindowStyle Hidden -PassThru}
# [2026-08-04 16:18:30] 作用：保证主业务脑启动尝试后恢复父进程环境；理由依据：后续WebUI、Knowledge、Dashboard与Getsoft必须继续按各自配置启动。
}finally{
  # [2026-08-04 16:18:30] 作用：恢复调用者原主链路缓存环境；理由依据：一键脚本重复或嵌套调用不得残留上一个profile目录。
  [Environment]::SetEnvironmentVariable('SQL_RAG_BM25_CACHE_DIR',$previousSqlRagBm25CacheDir,'Process')
  # [2026-08-04 16:18:30] 作用：恢复调用者原Hugging Face离线状态；理由依据：环境隔离必须双向完整。
  [Environment]::SetEnvironmentVariable('HF_HUB_OFFLINE',$previousHfHubOffline,'Process')
  # [2026-08-04 16:18:30] 作用：恢复调用者原Transformers离线状态；理由依据：不能改变后续独立服务的联网策略。
  [Environment]::SetEnvironmentVariable('TRANSFORMERS_OFFLINE',$previousTransformersOffline,'Process')
}
$web=Start-SqlRagServiceProcess -Stage 'business_brain_web_process' -StartAction {Start-Process -FilePath $Py -ArgumentList @('app\SQL_RAG\agent_webUI\webui_server.py','--host',$WebListenHost,'--port',"$WebPort",'--backend-url',$BackendUrl) -WorkingDirectory $RepoRoot -RedirectStandardOutput $wout -RedirectStandardError $werr -WindowStyle Hidden -PassThru}
# 2026-07-01 12:16:14 新增：启动资产类型后端服务；作用：提供资产类型和提示词 PG 入库 API；理由：不能把临时功能堆进 SQL_RAG/main.py。
$assetBackend=Start-SqlRagServiceProcess -Stage 'asset_backend_process' -StartAction {Start-Process -FilePath $Py -ArgumentList @('app\SQL_RAG\Asset_type_management\Data_storage_logic\mian_Asset_type_logic\run_asset_type_service.py','--host',$BusinessListenHost,'--port',"$AssetTypeBackendPort") -WorkingDirectory $RepoRoot -RedirectStandardOutput $assetBackendOut -RedirectStandardError $assetBackendErr -WindowStyle Hidden -PassThru}
# [2026-07-29 13:16:00] 作用：让 Python 统一资产与知识页面直接监听固定公开端口；理由依据：18191 到 18192 的 Node 二次网关会截断真实 M4A 最终 JSON。
$assetWeb=Start-SqlRagServiceProcess -Stage 'asset_web_process' -StartAction {Start-Process -FilePath $Py -ArgumentList @('app\SQL_RAG\Asset_type_management\webui\webui_server.py','--host',$BusinessListenHost,'--port',"$AssetTypeWebPort",'--backend-url',$AssetTypeBackendUrl,'--knowledge-backend-url',$KnowledgeBackendUrl,'--public-host',$PublicHost,'--deployment-profile',$DeploymentProfile,'--public-base-url',$FrontendPublicBaseUrl) -WorkingDirectory $RepoRoot -RedirectStandardOutput $assetWebOut -RedirectStandardError $assetWebErr -WindowStyle Hidden -PassThru}
# [2026-08-15 22:24:00] 作用：定位商业知识工具服务启动器；理由依据：RabbitMQ、Redis、MinIO、tusd、Celery 和观测组件统一位于用户指定 until 层级。
$KnowledgeCommercialLauncher=Join-Path $SqlRag 'Knowledge_management\backend\large-scale_commercialization_upgrade\until\Start-KnowledgeCommercialServices.ps1'
# [2026-08-15 22:24:00] 作用：阻断商业启动器缺失；理由依据：禁止 Knowledge API 回落到进程内任务字典和无缓存模式。
if(!(Test-Path -LiteralPath $KnowledgeCommercialLauncher -PathType Leaf)){throw "商业知识服务启动器不存在：$KnowledgeCommercialLauncher"}
# [2026-08-15 22:24:00] 作用：一键构建、启动并验收商业知识工具平面；理由依据：基础设施全部 ready 后才允许启动接收上传的 FastAPI。
$KnowledgeCommercialRuntime=& $KnowledgeCommercialLauncher -RepoRoot $RepoRoot -SqlRagRoot $SqlRag -DeploymentProfile $DeploymentProfile -ServicePortProfile $ServicePortProfile -KnowledgeDatabaseUrl $KnowledgeDatabaseUrl -ContainerNamePrefix $ContainerNamePrefix -ComposeProjectName $ComposeProjectName -PublicHost $PublicHost
# [2026-08-15 22:24:00] 作用：阻断缺失联合 ready 证据；理由依据：脚本退出但未返回结构化工具服务合同不能视为成功。
if($null-eq$KnowledgeCommercialRuntime-or$KnowledgeCommercialRuntime.Ready-ne$true){throw '商业知识服务未返回 ready 合同。'}
# [2026-08-04 15:00:55] 作用：保存父PowerShell原有DATABASE_URL；理由依据：Knowledge精确连接串只能注入28320子进程，不能串到业务脑、Getsoft或看板。
$KnowledgePreviousDatabaseUrl=[Environment]::GetEnvironmentVariable('DATABASE_URL','Process')
# [2026-08-04 15:00:55] 作用：进入Knowledge单进程环境注入事务；理由依据：无论Start-Process成功或失败都必须恢复父环境。
try{
  # [2026-08-04 15:00:55] 作用：把当前profile最终连接串显式注入28320子进程；理由依据：进程环境优先于dotenv，必须主动覆盖旧系统变量才能稳定命中本地5432或服务器25434。
  [Environment]::SetEnvironmentVariable('DATABASE_URL',$KnowledgeDatabaseUrl,'Process')
  # [2026-07-15 10:04:45] 作用：始终从当前工作区启动新的知识库后端；理由依据：不得复用加载旧源码的历史进程。
  $knowledgeBackend=Start-SqlRagServiceProcess -Stage 'knowledge_backend_process' -StartAction {Start-Process -FilePath $KnowledgePy -ArgumentList @('app\SQL_RAG\Knowledge_management\backend\knowledge_api\run_server.py','--host',$KnowledgeBackendListenHost,'--port',"$KnowledgeBackendPort") -WorkingDirectory $RepoRoot -RedirectStandardOutput $knowledgeBackendOut -RedirectStandardError $knowledgeBackendErr -WindowStyle Hidden -PassThru}
  # [2026-08-19 09:55:00] 作用：为商业任务查询、暂停和断点上传控制面保留 Windows 调度优先级；理由依据：20 文件阶段实测普通优先级在 CPU 满载时产生 10 至 20 秒超时和 Failed to fetch。
  if($knowledgeBackend){$knowledgeBackend.PriorityClass='AboveNormal'}
# [2026-08-04 15:00:55] 作用：保证Knowledge启动后恢复父环境；理由依据：后续看板和Getsoft必须继续读取各自独立配置。
}finally{
  # [2026-08-04 15:00:55] 作用：恢复父PowerShell原DATABASE_URL；理由依据：两套profile隔离不仅是端口隔离，也包括子进程连接串作用域隔离。
  [Environment]::SetEnvironmentVariable('DATABASE_URL',$KnowledgePreviousDatabaseUrl,'Process')
}
# [2026-07-15 10:04:45] 作用：始终从当前工作区启动新的知识库 WebUI；理由依据：页面和代理配置必须对应本次新后端。
$knowledgeWeb=Start-SqlRagServiceProcess -Stage 'knowledge_web_process' -StartAction {Start-Process -FilePath $KnowledgePy -ArgumentList @('app\SQL_RAG\Knowledge_management\webui\webui_server.py','--host',$WebListenHost,'--port',"$KnowledgeWebPort",'--backend-url',$KnowledgeBackendUrl) -WorkingDirectory $RepoRoot -RedirectStandardOutput $knowledgeWebOut -RedirectStandardError $knowledgeWebErr -WindowStyle Hidden -PassThru}
# [2026-08-06 10:17:36] 作用：保存父PowerShell中看板启动前的DATABASE_URL；理由依据：看板必须获得当前profile数据库且不能污染后续Getsoft。
$DashboardPreviousDatabaseUrl=[Environment]::GetEnvironmentVariable('DATABASE_URL','Process')
# [2026-08-06 10:17:36] 作用：保存看板原文跳转环境值；理由依据：同一PowerShell先后运行两套时不允许沿用上一套的公开地址。
$DashboardPreviousKnowledgeBaseUrl=[Environment]::GetEnvironmentVariable('CUSTOMER_RISK_KNOWLEDGE_BASE_URL','Process')
# [2026-08-06 10:17:36] 作用：进入看板单进程profile环境事务；理由依据：数据库和原文链接必须作为同一个不可分割的部署身份。
try{
  # [2026-08-06 10:17:36] 作用：向看板后端注入与Knowledge相同的当前profile连接串；理由依据：第二套不得继续依赖目录.env中的第一套127.0.0.1:5432历史值。
  [Environment]::SetEnvironmentVariable('DATABASE_URL',$KnowledgeDatabaseUrl,'Process')
  # [2026-08-06 10:17:36] 作用：向看板后端注入当前profile的知识挂载入口；理由依据：服务器响应中的28个原文链接已实测串回172.18.1.212:18191。
  [Environment]::SetEnvironmentVariable('CUSTOMER_RISK_KNOWLEDGE_BASE_URL',$KnowledgeMountedWebUrl,'Process')
  # [2026-08-06 10:17:36] 作用：使用Knowledge专用解释器启动已锁定profile的看板后端；理由依据：看板复用依赖代码但不得复用另一台机器的运行值。
  $dashboardBackend=Start-SqlRagServiceProcess -Stage 'dashboard_backend_process' -StartAction {Start-Process -FilePath $KnowledgePy -ArgumentList @('app\SQL_RAG\Knowledge_Analysis\Customer_Risk_BusinessOpportunity_Perception_Dashboard\backend\run_server.py','--host',$BusinessListenHost,'--port',"$DashboardBackendPort") -WorkingDirectory $RepoRoot -RedirectStandardOutput $dashboardBackendOut -RedirectStandardError $dashboardBackendErr -WindowStyle Hidden -PassThru}
# [2026-08-06 10:17:36] 作用：无论看板创建成功与否都退出profile环境事务；理由依据：子进程独立不允许以父进程污染作为代价。
}finally{
  # [2026-08-06 10:17:36] 作用：恢复父PowerShell原DATABASE_URL；理由依据：后续Getsoft使用自己的数据库合同。
  [Environment]::SetEnvironmentVariable('DATABASE_URL',$DashboardPreviousDatabaseUrl,'Process')
  # [2026-08-06 10:17:36] 作用：恢复父PowerShell原看板知识入口；理由依据：重复或嵌套调用不得留下当前profile残值。
  [Environment]::SetEnvironmentVariable('CUSTOMER_RISK_KNOWLEDGE_BASE_URL',$DashboardPreviousKnowledgeBaseUrl,'Process')
}
# [2026-07-21 13:38:18] 作用：启动看板独立WebUI并指向本次后端；理由依据：18431页面和/api必须同源且不得回退演示数据。
$dashboardWeb=Start-SqlRagServiceProcess -Stage 'dashboard_web_process' -StartAction {Start-Process -FilePath $KnowledgePy -ArgumentList @('app\SQL_RAG\Knowledge_Analysis\Customer_Risk_BusinessOpportunity_Perception_Dashboard\webui\webui_server.py','--host',$WebListenHost,'--port',"$DashboardWebPort",'--backend-url',$DashboardBackendUrl) -WorkingDirectory $RepoRoot -RedirectStandardOutput $dashboardWebOut -RedirectStandardError $dashboardWebErr -WindowStyle Hidden -PassThru}
# [2026-07-23 10:28:57] 作用：通过独立适配器拉起对方标准 app.main 全量服务；理由依据：对方使用自己的虚拟环境、工作目录、端口和日志，不污染我方业务链路。
$getsoftStartupReady=$false; $getsoftReady=$false; $getsoftBrowserReady=$false; $getsoftBusinessReady=$false; $getsoftSseReady=$false; $getsoftLast=''; $getsoftResult=$null
# [2026-08-18 13:02:26] 作用：初始化本地既有 Getsoft 实例的无提权预检结果；理由依据：只有强归属、真实监听和源码时效均成立时才能避免先弹 UAC。
$getsoftReusePreflightReady=$false
# [2026-08-18 13:02:26] 作用：初始化本地既有实例预检诊断；理由依据：预检异常不得阻断正常适配器替换路径，但必须可用于定位。
$getsoftReusePreflightLast=''
# [2026-08-18 13:02:26] 作用：把无提权预检严格限制到第一套 local profile；理由依据：第二套服务器必须继续执行管理员离线确定性替换，不能复用该捷径。
if($DeploymentProfile-eq'local'){
  # [2026-08-18 13:02:26] 作用：隔离本地既有实例预检异常；理由依据：无法证明可复用时必须回到原适配器流程而不是让整个启动器提前退出。
  try{
    # [2026-08-18 13:02:26] 作用：定位当前 local profile 的 Getsoft 状态文件；理由依据：未知 PID 或其他 checkout 的端口监听不能跳过 UAC 替换。
    $getsoftPreflightStatePath=Join-Path $GetsoftInstanceRuntimeRoot 'service-state.json'
    # [2026-08-18 13:02:26] 作用：仅在持久状态真实存在时评估既有实例；理由依据：首次启动仍必须由适配器创建服务。
    if(Test-Path -LiteralPath $getsoftPreflightStatePath -PathType Leaf){
      # [2026-08-18 13:02:26] 作用：读取既有实例的项目、应用、端口和 PID 合同；理由依据：预检与后续严格复验必须使用同一持久事实。
      $getsoftPreflightState=Get-Content -LiteralPath $getsoftPreflightStatePath -Raw -Encoding UTF8|ConvertFrom-Json
      # [2026-08-18 13:02:26] 作用：读取状态记录 PID 的当前进程；理由依据：陈旧状态或 PID 复用不能获得无提权资格。
      $getsoftPreflightProcess=Get-CimInstance Win32_Process -Filter "ProcessId=$([int]$getsoftPreflightState.backend_pid)" -ErrorAction SilentlyContinue
      # [2026-08-18 13:02:26] 作用：核对状态 PID 仍持有固定 Getsoft 监听；理由依据：仅状态文件匹配不足以证明当前数据面归属。
      $getsoftPreflightListener=Get-NetTCPConnection -LocalPort ([int]$GetsoftConfig.port) -State Listen -ErrorAction SilentlyContinue|Where-Object{[int]$_.OwningProcess-eq[int]$getsoftPreflightState.backend_pid}|Select-Object -First 1
      # [2026-08-18 13:02:26] 作用：定位 Getsoft 应用目录最近修改的运行源码；理由依据：旧进程不得复用到比自身更新的业务代码上。
      $getsoftPreflightLatestAppFile=Get-ChildItem -LiteralPath (Join-Path ([string]$GetsoftConfig.project_root) 'app') -Recurse -File -ErrorAction Stop|Where-Object{$_.Extension -in @('.py','.json','.yml','.yaml','.toml')}|Sort-Object LastWriteTimeUtc -Descending|Select-Object -First 1
      # [2026-08-18 13:02:26] 作用：初始化既有进程必须覆盖的最近写入时刻；理由依据：源码、适配器和配置中的任一更新都应要求重新创建服务。
      $getsoftPreflightLatestRequiredWriteUtc=if($getsoftPreflightLatestAppFile){$getsoftPreflightLatestAppFile.LastWriteTimeUtc}else{[datetime]::MinValue}
      # [2026-08-18 13:26:59] 作用：列出会被 Getsoft 业务进程实际加载的源码、依赖、环境和部署配置；理由依据：生命周期适配器与 SSE 探针修改不进入业务进程，其正确性由随后真实数据库、模型、MinIO、OpenAPI、Swagger、业务接口和 SSE 门禁证明。
      $getsoftPreflightFreshnessFiles=@($GetsoftConfigPath,(Join-Path ([string]$GetsoftConfig.project_root) 'pyproject.toml'),(Join-Path ([string]$GetsoftConfig.project_root) '.env'))
      # [2026-08-18 13:02:26] 作用：逐项推进既有实例必须覆盖的最近配置时刻；理由依据：预检不得漏掉依赖合同、环境或 SSE 探针更新。
      foreach($getsoftPreflightFreshnessFile in $getsoftPreflightFreshnessFiles){
        # [2026-08-18 13:02:26] 作用：仅比较真实存在的可选配置文件；理由依据：缺少可选 .env 不应产生空路径异常。
        if(Test-Path -LiteralPath $getsoftPreflightFreshnessFile -PathType Leaf){
          # [2026-08-18 13:02:26] 作用：读取当前配置文件的 UTC 修改时刻；理由依据：跨时区时效判断必须使用统一时间基准。
          $getsoftPreflightFreshnessWriteUtc=(Get-Item -LiteralPath $getsoftPreflightFreshnessFile).LastWriteTimeUtc
          # [2026-08-18 13:02:26] 作用：更新本次预检的最近必需写入时刻；理由依据：现存进程必须晚于全部运行合同。
          if($getsoftPreflightFreshnessWriteUtc-gt$getsoftPreflightLatestRequiredWriteUtc){$getsoftPreflightLatestRequiredWriteUtc=$getsoftPreflightFreshnessWriteUtc}
        }
      }
      # [2026-08-18 13:02:26] 作用：核对状态仍属于当前项目、应用和固定端口；理由依据：同机另一套 Getsoft 实例不得被当前入口复用。
      $getsoftPreflightIdentityReady=([System.IO.Path]::GetFullPath([string]$getsoftPreflightState.project_root)-eq[System.IO.Path]::GetFullPath([string]$GetsoftConfig.project_root)-and[string]$getsoftPreflightState.application-eq[string]$GetsoftConfig.application-and[int]$getsoftPreflightState.port-eq[int]$GetsoftConfig.port)
      # [2026-08-18 13:02:26] 作用：核对既有进程启动时间不早于全部源码和配置；理由依据：只有当前发布代次才能跳过管理员替换。
      $getsoftPreflightFreshReady=($getsoftPreflightProcess-and$getsoftPreflightProcess.CreationDate.ToUniversalTime()-ge$getsoftPreflightLatestRequiredWriteUtc)
      # [2026-08-18 13:02:26] 作用：合并状态身份、当前进程、真实监听和时效门禁；理由依据：四项同时成立才允许适配器不弹 UAC 并交回父入口做完整在线复验。
      $getsoftReusePreflightReady=($getsoftPreflightIdentityReady-and$getsoftPreflightProcess-and$getsoftPreflightListener-and$getsoftPreflightFreshReady)
    }
  # [2026-08-18 13:02:26] 作用：捕获本地既有实例预检失败原因；理由依据：失败应继续正常适配器流程且保留可诊断信息。
  }catch{
    # [2026-08-18 13:02:26] 作用：保存本地既有实例预检异常文本；理由依据：最终适配器失败时需要区分预检和业务健康问题。
    $getsoftReusePreflightLast=$_.Exception.Message
  }
}
# [2026-08-18 13:02:26] 作用：保存调用适配器前已有的跳过提权环境值；理由依据：本次启动不能污染父 PowerShell 或后续 profile。
$getsoftPreviousSkipElevatedStop=[Environment]::GetEnvironmentVariable('SQL_RAG_GETSOFT_SKIP_ELEVATED_STOP','Process')
# [2026-08-18 13:02:26] 作用：按强归属预检结果显式控制本次适配器是否跳过 UAC；理由依据：通过预检的本地旧实例交给父入口严格复验，其他场景保持原确定性替换流程。
[Environment]::SetEnvironmentVariable('SQL_RAG_GETSOFT_SKIP_ELEVATED_STOP',$(if($getsoftReusePreflightReady){'1'}else{$null}),'Process')
try{
  # [2026-07-23 10:28:57] 作用：把公开主机和稳定配置显式交给适配器；理由依据：一键入口保持不变，迁移机器只需环境覆盖路径或端口。
  # [2026-07-23 11:46:00] 作用：不通过 PowerShell 捕获管道调用独立适配器；理由依据：常驻 Uvicorn 子进程可能继承捕获管道，导致父启动器等待一个本应持续运行的服务。
  $getsoftResultPath=$GetsoftStartupResultPath
  if(Test-Path -LiteralPath $getsoftResultPath){Remove-Item -LiteralPath $getsoftResultPath -Force}
  $getsoftPreviousErrorActionPreference=$ErrorActionPreference
  try{
    # [2026-07-23 11:46:00] 作用：仅在外部 PowerShell 运行窗口允许其自行报告错误；理由依据：子启动失败由退出码、运行时结果文件和独立日志共同诊断。
    $ErrorActionPreference='Continue'
    # [2026-08-19 10:30:06] 作用：强归属、监听和版本时效预检通过时不再调用会尝试停止同一管理员进程的子适配器；理由依据：旧流程先设置跳过提权再进入停止函数，必然以退出码1返回并把本可严格复验的健康实例误报为启动失败。
    if($getsoftReusePreflightReady){
      # [2026-08-19 10:30:06] 作用：用非零受控退出码进入下方既有实例的SSE、OpenAPI、Swagger和业务接口严格复验分支；理由依据：复用只省略破坏性的重复停止，不能跳过任何在线健康门禁。
      $getsoftAdapterExitCode=197
      # [2026-08-19 10:30:06] 作用：向一键启动现场明确报告本轮采用严格复用路径；理由依据：操作者必须能区分复用验证与重新创建，避免把短路误解为未启动服务。
      Write-Host "Getsoft既有实例已通过强归属预检，跳过重复停止并进入完整在线复验；PID=$([int]$getsoftPreflightState.backend_pid)"
    }else{
      # [2026-08-19 10:30:06] 作用：仅在无法证明既有实例可安全复用时执行原确定性替换适配器；理由依据：首次启动、源码过期或归属不明仍必须真实创建当前版本服务。
      & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $GetsoftAdapterScript -OwnerRepoRoot $RepoRoot -PublicHost $PublicHost -ConfigPath $GetsoftConfigPath
      # [2026-08-19 10:30:06] 作用：保存真实适配器退出码供下方结果合同判断；理由依据：替换路径的任何失败仍须保持失败关闭，不能因新增复用分支被吞掉。
      $getsoftAdapterExitCode=$LASTEXITCODE
    }
  }finally{
    # [2026-08-18 13:02:26] 作用：恢复适配器调用前的跳过提权环境值；理由依据：第一套本地预检结果不得影响第二套或后续独立启动。
    [Environment]::SetEnvironmentVariable('SQL_RAG_GETSOFT_SKIP_ELEVATED_STOP',$getsoftPreviousSkipElevatedStop,'Process')
    # [2026-07-23 11:46:00] 作用：恢复父启动器原有严格错误策略；理由依据：外部适配调用不得削弱我方后续全量健康验收。
    $ErrorActionPreference=$getsoftPreviousErrorActionPreference
  }
  # [2026-07-23 11:46:00] 作用：仅从适配器原子生成的运行时合同读取健康结果；理由依据：依赖安装日志和常驻子进程输出均不能冒充 ready。
  if($getsoftAdapterExitCode -ne 0){
    # [2026-08-04 15:01:48] 作用：记录Getsoft独立适配器失败而不终止我方健康验收；理由依据：MinIO等外部依赖失败不能阻止已经创建的知识、资产、业务脑和看板服务继续完成就绪。
    $getsoftLast="外部隔离适配器退出码：$getsoftAdapterExitCode"
    # [2026-08-18 12:36:42] 作用：初始化Getsoft本地既有实例复用标记；理由依据：只有全部强归属和真实SSE门禁通过后才允许绕过被取消的UAC重启。
    $getsoftExistingReuseReady=$false
    # [2026-08-18 12:36:42] 作用：把既有实例复用严格限制到第一套本地profile；理由依据：第二套服务器必须继续由管理员固定入口和离线包完成确定性替换。
    if($DeploymentProfile-eq'local'){
      # [2026-08-18 12:36:42] 作用：隔离本地既有实例的归属、时效和SSE验证异常；理由依据：复用失败必须回到原失败状态而不能中断其余服务健康汇总。
      try{
        # [2026-08-18 12:36:42] 作用：定位当前local profile的Getsoft服务状态；理由依据：仅允许复用固定入口上一次明确记录的进程代次。
        $getsoftExistingStatePath=Join-Path $GetsoftInstanceRuntimeRoot 'service-state.json'
        # [2026-08-18 12:36:42] 作用：要求既有服务状态文件真实存在；理由依据：未知PID或仅凭端口存活不得进入复用路径。
        if(Test-Path -LiteralPath $getsoftExistingStatePath -PathType Leaf){
          # [2026-08-18 12:36:42] 作用：读取既有服务的项目、端口和PID合同；理由依据：后续每项强归属判断都使用同一持久事实。
          $getsoftExistingState=Get-Content -LiteralPath $getsoftExistingStatePath -Raw -Encoding UTF8|ConvertFrom-Json
          # [2026-08-18 12:36:42] 作用：读取状态记录PID当前进程；理由依据：陈旧或已复用PID不能仅凭历史JSON获得服务归属。
          $getsoftExistingProcess=Get-CimInstance Win32_Process -Filter "ProcessId=$([int]$getsoftExistingState.backend_pid)" -ErrorAction SilentlyContinue
          # [2026-08-18 12:36:42] 作用：读取当前Getsoft端口的真实监听；理由依据：状态进程必须仍实际承载18520数据面。
          $getsoftExistingListener=Get-NetTCPConnection -LocalPort ([int]$GetsoftConfig.port) -State Listen -ErrorAction SilentlyContinue|Where-Object{[int]$_.OwningProcess-eq[int]$getsoftExistingState.backend_pid}|Select-Object -First 1
          # [2026-08-18 12:36:42] 作用：定位Getsoft项目app目录的最近源码文件；理由依据：进程启动后出现的Python或配置修改必须阻断复用并要求真实重启。
          $getsoftLatestAppFile=Get-ChildItem -LiteralPath (Join-Path ([string]$GetsoftConfig.project_root) 'app') -Recurse -File -ErrorAction Stop|Where-Object{$_.Extension -in @('.py','.json','.yml','.yaml','.toml')}|Sort-Object LastWriteTimeUtc -Descending|Select-Object -First 1
          # [2026-08-18 12:36:42] 作用：初始化既有进程允许覆盖的最近配置修改时刻；理由依据：后续统一比较源码、适配器和环境文件而不遗漏任一运行合同。
          $getsoftLatestRequiredWriteUtc=if($getsoftLatestAppFile){$getsoftLatestAppFile.LastWriteTimeUtc}else{[datetime]::MinValue}
          # [2026-08-18 13:26:59] 作用：列出会被Getsoft业务进程实际加载的依赖、环境和部署配置；理由依据：适配器与SSE探针不进入业务进程且由后续全部在线门禁单独验证，不能仅因生命周期脚本更新强制弹出UAC。
          $getsoftFreshnessFiles=@($GetsoftConfigPath,(Join-Path ([string]$GetsoftConfig.project_root) 'pyproject.toml'),(Join-Path ([string]$GetsoftConfig.project_root) '.env'))
          # [2026-08-18 12:36:42] 作用：逐个合并关键文件的最近写入时刻；理由依据：任何晚于进程的配置变更都必须禁止静默复用。
          foreach($getsoftFreshnessFile in $getsoftFreshnessFiles){
            # [2026-08-18 12:36:42] 作用：只处理当前机器真实存在的关键文件；理由依据：可选.env缺失不应制造虚假最新时间但必备文件仍由原适配器校验。
            if(Test-Path -LiteralPath $getsoftFreshnessFile -PathType Leaf){
              # [2026-08-18 12:36:42] 作用：读取当前关键文件UTC修改时刻；理由依据：跨本地时区比较统一使用UTC避免夏令时或格式歧义。
              $getsoftFreshnessWriteUtc=(Get-Item -LiteralPath $getsoftFreshnessFile).LastWriteTimeUtc
              # [2026-08-18 12:36:42] 作用：推进最近必需修改时刻；理由依据：复用条件必须覆盖所有源码和配置中的最大值。
              if($getsoftFreshnessWriteUtc-gt$getsoftLatestRequiredWriteUtc){$getsoftLatestRequiredWriteUtc=$getsoftFreshnessWriteUtc}
            }
          }
          # [2026-08-18 12:36:42] 作用：核对既有状态仍属于当前项目、应用和公开端口；理由依据：同机其他Getsoft checkout或profile不得被当前入口复用。
          $getsoftExistingIdentityReady=([System.IO.Path]::GetFullPath([string]$getsoftExistingState.project_root)-eq[System.IO.Path]::GetFullPath([string]$GetsoftConfig.project_root)-and[string]$getsoftExistingState.application-eq[string]$GetsoftConfig.application-and[int]$getsoftExistingState.port-eq[int]$GetsoftConfig.port)
          # [2026-08-18 12:36:42] 作用：确认现存进程启动时间不早于最近源码和配置；理由依据：陈旧进程即使健康也不能冒充当前发布版本。
          $getsoftExistingFreshReady=($getsoftExistingProcess-and$getsoftExistingProcess.CreationDate.ToUniversalTime()-ge$getsoftLatestRequiredWriteUtc)
          # [2026-08-18 12:36:42] 作用：在强归属、真实监听和版本时效同时成立时执行SSE门禁；理由依据：避免因管理员旧进程无法停止让一键启动永久失败，同时不降低业务证据标准。
          if($getsoftExistingIdentityReady-and$getsoftExistingProcess-and$getsoftExistingListener-and$getsoftExistingFreshReady){
            # [2026-08-18 12:36:42] 作用：定位Getsoft真实SSE消费探针；理由依据：复用实例仍必须证明retrieved、answer、done和干净EOF完整成立。
            $getsoftExistingSseProbeScript=Join-Path (Split-Path -Parent $GetsoftAdapterScript) 'Test-GetsoftSseStream.ps1'
            # [2026-08-25 17:15:52] 作用：初始化现存Getsoft实例的严格SSE复验结果；理由依据：36个容器刚启动时资源瞬时拥塞不能让一次超时永久污染最终就绪合同。
            $getsoftExistingReuseReady=$false
            # [2026-08-25 17:15:52] 作用：初始化SSE探针结构化结果；理由依据：每次重试都必须重新取得完整终态，禁止沿用上一次残缺输出。
            $getsoftExistingSseProbe=$null
            # [2026-08-25 17:15:52] 作用：最多执行三次严格SSE复验；理由依据：只吸收启动峰值期的短暂抖动，三次均失败仍保持失败关闭。
            for($getsoftExistingSseAttempt=1;$getsoftExistingSseAttempt-le3;$getsoftExistingSseAttempt++){
              # [2026-08-25 17:15:52] 作用：隔离单次SSE输出或JSON解析异常；理由依据：一次瞬时空响应可以重试，但不得绕过最终字段门禁。
              try{
                # [2026-08-25 17:15:52] 作用：真实消费一次现存Getsoft局域网SSE；理由依据：每次尝试仍完整执行retrieved、answer、done和干净EOF验证。
                $getsoftExistingSseOutput=& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $getsoftExistingSseProbeScript -BaseUrl $GetsoftInternalUrl -Path ([string]$GetsoftConfig.sse_probe_path) -TimeoutSeconds ([int]$GetsoftConfig.sse_probe_timeout_seconds) -TransportOnly -CleanupSession
                # [2026-08-25 17:15:52] 作用：保存本次SSE探针原生退出码；理由依据：JSON文本存在不能掩盖探针进程失败。
                $getsoftExistingSseExitCode=$LASTEXITCODE
                # [2026-08-25 17:15:52] 作用：解析本次SSE探针最终结构化结果；理由依据：复用判定必须逐项检查真实传输终态。
                $getsoftExistingSseProbe=($getsoftExistingSseOutput|Select-Object -Last 1)|ConvertFrom-Json
                # [2026-08-25 17:15:52] 作用：合并本次退出码、就绪、干净EOF、done和错误门禁；理由依据：任何缺项都不能被重试机制降级为成功。
                $getsoftExistingReuseReady=($getsoftExistingSseExitCode-eq0-and$getsoftExistingSseProbe.ready-eq$true-and$getsoftExistingSseProbe.clean_eof-eq$true-and$getsoftExistingSseProbe.done-eq$true-and$getsoftExistingSseProbe.error-eq$false)
              # [2026-08-25 17:15:52] 作用：把单次异常保留为失败结果并交给有限重试；理由依据：瞬时空输出不能中断其余服务，但最终仍必须有一次完整成功证据。
              }catch{
                # [2026-08-25 17:15:52] 作用：清空异常尝试的结构化结果；理由依据：残缺JSON不得参与后续成功判断。
                $getsoftExistingSseProbe=$null
                # [2026-08-25 17:15:52] 作用：显式保持异常尝试失败；理由依据：捕获异常只用于重试而不是吞错放行。
                $getsoftExistingReuseReady=$false
              }
              # [2026-08-25 17:15:52] 作用：完整SSE证据一旦成立立即结束重试；理由依据：避免重复发起无必要的真实业务流请求。
              if($getsoftExistingReuseReady){break}
              # [2026-08-25 17:15:52] 作用：仅在尚有剩余尝试时等待五秒；理由依据：给启动峰值I/O和CPU释放窗口且不制造无限等待。
              if($getsoftExistingSseAttempt-lt3){Start-Sleep -Seconds 5}
            }
            # [2026-08-18 12:36:42] 作用：在现存实例通过完整SSE门禁时构造最终验收所需结果合同；理由依据：后续仍会再次验证OpenAPI、Swagger和数据库业务接口。
            if($getsoftExistingReuseReady){
              # [2026-08-18 12:36:42] 作用：记录现存实例已满足适配器等价就绪证据；理由依据：最终健康汇总不得因没有新startup-result.json而跳过真实在线检查。
              $getsoftResult=[pscustomobject]@{ready=$true;enabled=$true;sse_ready=$true;sse_probe=$getsoftExistingSseProbe;stderr_log=[string]$getsoftExistingState.stderr_log;reused_existing=$true}
              # [2026-08-18 12:36:42] 作用：允许最终阶段复验现存实例；理由依据：最终OpenAPI、浏览器和业务接口仍是全量READY必要条件。
              $getsoftStartupReady=$true
              # [2026-08-18 12:36:42] 作用：记录受限复用诊断；理由依据：操作者必须知道本轮未重新创建管理员遗留进程但已完成强证据复验。
              $getsoftLast='复用当前源码和配置之后启动且真实SSE通过的既有Getsoft实例'
              # [2026-08-18 12:36:42] 作用：输出本地既有实例复用结果；理由依据：现场不再把无UAC重启误判为静默忽略适配器失败。
              Write-Warning "Getsoft旧管理员进程无法无UAC替换，已按项目、PID、端口、源码时效和真实SSE门禁安全复用；PID=$([int]$getsoftExistingState.backend_pid)"
            }
          }
        }
      # [2026-08-18 12:36:42] 作用：捕获既有实例复用验证异常；理由依据：异常只能补充诊断，不得把Getsoft错误伪装为全量READY。
      }catch{
        # [2026-08-18 12:36:42] 作用：追加既有实例复用失败原因；理由依据：最终失败报告应区分适配器退出和严格复用门禁失败。
        $getsoftLast="$getsoftLast；既有实例复用失败：$($_.Exception.Message)"
      }
    }
    # [2026-08-18 12:36:42] 作用：仅在严格复用未通过时报告Getsoft启动失败；理由依据：通过全部在线门禁的现存实例不应继续被标记为四项false。
    if(!$getsoftExistingReuseReady){
      # [2026-08-04 15:01:48] 作用：明确告知操作者我方全量服务仍在继续验收；理由依据：旧逻辑虽然继续执行却静默最长180秒，现场被误判为卡死。
      Write-Warning "Getsoft独立服务启动失败，SQL_RAG其余服务不会中止，现继续执行全量健康验收；$getsoftLast"
    }
  }else{
    if(Test-Path -LiteralPath $getsoftResultPath){$getsoftResult=(Get-Content -LiteralPath $getsoftResultPath -Raw -Encoding UTF8 | ConvertFrom-Json)}
    if($getsoftResult -and $getsoftResult.ready){$getsoftStartupReady=$true}
  }
}catch{
  # [2026-07-23 10:28:57] 作用：保留对方启动失败的原始原因并继续验收我方已启动服务；理由依据：一个外部源码错误不能让已创建的我方进程失去健康证据。
  $getsoftLast=$_.Exception.Message
  # [2026-08-04 15:01:48] 作用：显示异常分支同样进入我方健康验收；理由依据：任何Getsoft适配器异常都不能表现成无输出的全栈卡死。
  Write-Warning "Getsoft独立服务出现异常，SQL_RAG其余服务不会中止，现继续执行全量健康验收；$getsoftLast"
}
$backendReady=$false; $webReady=$false; $proxyReady=$false; $assetBackendReady=$false; $assetWebReady=$false; $assetProxyReady=$false; $last=''; $assetLast=''
# [2026-07-04 10:18:20] 作用：初始化知识库后端、WebUI 和同源代理三项独立就绪标志及健康详情；理由依据：仅端口监听不能证明两条业务链已通过前端代理正确串联。
$knowledgeBackendReady=$false; $knowledgeWebReady=$false; $knowledgeProxyReady=$false; $knowledgeLast=''
# [2026-07-30 11:26:01] 作用：初始化已发布知识实时同步门禁；理由依据：一键启动不能把仅完成一次性全量转换误报为 WebUI 双库实时同步已就绪。
$knowledgeRealtimeSyncReady=$false
# [2026-07-30 11:26:02] 作用：初始化已发布知识实时同步诊断快照；理由依据：同步器启动失败或首轮失败时必须输出可定位的结构化原因。
$knowledgeRealtimeSyncLast=''
# [2026-08-06 10:17:36] 作用：初始化看板后端、页面、代理与profile依赖身份就绪标志；理由依据：能SELECT 1不代表数据库端口和原文地址没有串到第一套。
$dashboardBackendReady=$false; $dashboardWebReady=$false; $dashboardProxyReady=$false; $dashboardDependencyReady=$false; $dashboardLast=''
# [2026-07-07 19:08:17] 作用：初始化兼容版 A+ 新挂载入口就绪标志；理由依据：旧入口 ready 不代表 /resourceType/ 与 /knowledgeManagement/ 可被外部前端跳转。
$assetMountedWebReady=$false; $assetMountedProxyReady=$false; $knowledgeMountedWebReady=$false; $knowledgeMountedProxyReady=$false
# [2026-08-06 11:08:00] 作用：初始化统一前端profile身份门禁与诊断；理由依据：页面和API都健康仍不足以证明外部挂载根没有串到另一套。
$frontendProfileReady=$false; $frontendProfileLast=''
for($i=1;$i -le 90;$i++){
  # [2026-07-30 11:26:03] 作用：读取主业务脑健康并同步检查常驻外部源管理器；理由依据：同一个服务生命周期负责把 WebUI 已发布知识持续同步到 Qdrant。
  try{
    # [2026-07-30 11:26:04] 作用：请求主业务脑健康接口；理由依据：接口同时返回主业务和外部源实时同步状态。
    $h=Invoke-RestMethod "$BackendUrl/agent/business-brain/health" -TimeoutSec 5
    # [2026-07-30 11:26:05] 作用：保存完整主业务脑健康快照；理由依据：最终日志必须保留模型、数据库和同步器的联合诊断证据。
    $last=$h|ConvertTo-Json -Depth 8
    # [2026-07-30 11:26:06] 作用：在主业务脑健康时标记后端就绪；理由依据：保留原有一键启动健康合同不变。
    if($h.ready){$backendReady=$true}
    # [2026-07-30 11:26:07] 作用：提取外部源同步管理器状态；理由依据：后续门禁必须检查 krauss_ai_ie_dev 的首轮真实结果而不是只看线程存在。
    $knowledgeRealtimeSyncStatus=$h.checks.external_source_sync
    # [2026-07-30 11:26:08] 作用：序列化实时同步状态用于启动日志；理由依据：PG、Embedding 或 Qdrant 任一失败都要能直接定位。
    $knowledgeRealtimeSyncLast=$knowledgeRealtimeSyncStatus|ConvertTo-Json -Depth 10
    # [2026-07-30 11:26:09] 作用：仅在同步线程运行且知识问答 profile 首轮无失败时通过门禁；理由依据：WebUI 编辑实时进入 sql_krauss_ai_ie_dev 必须有运行时证据。
    if($knowledgeRealtimeSyncStatus.running -eq $true -and $knowledgeRealtimeSyncStatus.profiles.krauss_ai_ie_dev.ready -eq $true){$knowledgeRealtimeSyncReady=$true}
  }catch{}
  # [2026-08-04 08:31:11] 作用：以PowerShell 5.1非交互解析方式检查业务WebUI；理由依据：健康门禁不得因IE首次配置提示停住管理员一键窗口。
  try{$r=Invoke-WebRequest $WebUrl -UseBasicParsing -TimeoutSec 5; if($r.StatusCode -eq 200){$webReady=$true}}catch{}
  try{$p=Invoke-RestMethod "$WebUrl/api/agent/business-brain/health" -TimeoutSec 5; if($p.ready){$proxyReady=$true}}catch{}
  # 2026-07-01 12:16:16 新增：检查资产类型后端健康；作用：确认 PG 入库服务可连接数据库；理由：端口监听不等于业务 ready。
  try{$ah=Invoke-RestMethod "$AssetTypeBackendUrl/health" -TimeoutSec 5; $assetLast=$ah|ConvertTo-Json -Depth 8; if($ah.ready){$assetBackendReady=$true}}catch{}
  # 2026-07-01 12:16:17 新增：检查资产类型 WebUI 首页；作用：确认新的前端入口可访问；理由：避免再次出现连接被拒绝。
  # [2026-08-04 08:31:12] 作用：以PowerShell 5.1非交互解析方式检查资产类型WebUI；理由依据：页面HTTP验证必须在任何Windows 11管理员配置下自动完成。
  try{$ar=Invoke-WebRequest $AssetTypeWebUrl -UseBasicParsing -TimeoutSec 5; if($ar.StatusCode -eq 200){$assetWebReady=$true}}catch{}
  # [2026-08-06 11:08:00] 作用：读取统一网关自报的当前profile、挂载地址和内部上游；理由依据：必须在第一套Docker关闭时证明第二套页面从入口到API全程属于233。
  try{
    # [2026-08-06 11:08:00] 作用：请求无密钥前端运行时profile；理由依据：该端点与WebUI实际请求处理器同进程，不能被静态文件假绿替代。
    $frontendProfileState=Invoke-RestMethod "$AssetTypeWebUrl/runtime-profile.json" -TimeoutSec 5
    # [2026-08-06 11:08:00] 作用：保存前端profile完整诊断；理由依据：失败时控制台要直接展示actual URL而不是只返回False。
    $frontendProfileLast=$frontendProfileState|ConvertTo-Json -Depth 6 -Compress
    # [2026-08-06 11:08:00] 作用：逐项核对profile名、公开根、两项挂载和两个内部上游；理由依据：任意一项残留212都会重现用户截图中的0条数据。
    $frontendProfileReady=($frontendProfileState.ready-eq$true-and[string]$frontendProfileState.profile_name-eq$DeploymentProfile-and[string]$frontendProfileState.public_base_url-eq$FrontendPublicBaseUrl-and[string]$frontendProfileState.asset_mount_url-eq$AssetTypeMountedWebUrl-and[string]$frontendProfileState.knowledge_mount_url-eq$KnowledgeMountedWebUrl-and[string]$frontendProfileState.asset_backend_url-eq$AssetTypeBackendUrl-and[string]$frontendProfileState.knowledge_backend_url-eq$KnowledgeBackendUrl)
  }catch{
    # [2026-08-06 11:08:00] 作用：保留前端profile探针异常；理由依据：旧版WebUI缺少发现端点时必须明确等待新版进程而不能误用旧服务。
    $frontendProfileLast=$_.Exception.Message
  }
  # 2026-07-01 12:16:18 新增：检查资产类型 WebUI API 代理；作用：确认 /api 能转发到资产类型后端；理由：前端默认通过同源 /api 入库。
  try{$ap=Invoke-RestMethod "$AssetTypeWebUrl/api/health" -TimeoutSec 5; if($ap.ready){$assetProxyReady=$true}}catch{}
  # [2026-07-07 16:20:13] 作用：检查资产类型新挂载页面；理由依据：外部前端实际访问的是 /resourceType/，不能只验证 18191 根入口。
  # [2026-08-04 08:31:13] 作用：以PowerShell 5.1非交互解析方式检查资产类型挂载页面；理由依据：固定URL验收不得触发网页脚本安全询问。
  try{$amw=Invoke-WebRequest $AssetTypeMountedWebUrl -UseBasicParsing -TimeoutSec 5; if($amw.StatusCode -eq 200){$assetMountedWebReady=$true}}catch{}
  # [2026-07-07 16:20:13] 作用：检查资产类型新挂载 API 代理；理由依据：/resourceType/api 必须继续转发到资产类型后端 18190。
  try{$amp=Invoke-RestMethod "$AssetTypeMountedApiUrl/health" -TimeoutSec 5; if($amp.ready){$assetMountedProxyReady=$true}}catch{}
  # [2026-07-04 10:18:20] 作用：检查知识库后端是否具备 API 密钥、模型配置和数据库连接；理由依据：真实解析与入库前必须验证全部外部依赖可用。
  try{$kh=Invoke-RestMethod "$KnowledgeBackendUrl/health" -TimeoutSec 5; $knowledgeLast=$kh|ConvertTo-Json -Depth 8; if($kh.ready){$knowledgeBackendReady=$true}}catch{}
  # [2026-07-04 10:18:20] 作用：检查知识库 WebUI 静态页面服务是否可访问；理由依据：用户需要从新端口进入前端而非仅调用后端接口。
  # [2026-08-04 08:31:14] 作用：以PowerShell 5.1非交互解析方式检查知识库WebUI；理由依据：知识页面门禁必须无人值守返回结果而不是等待用户输入。
  try{$kw=Invoke-WebRequest "$KnowledgeWebUrl/health" -UseBasicParsing -TimeoutSec 5; if($kw.StatusCode -eq 200){$knowledgeWebReady=$true}}catch{}
  # [2026-07-04 10:18:20] 作用：通过知识库 WebUI 同源代理检查后端健康；理由依据：必须证明前端配置已连接本次知识库后端而非旧端口。
  try{$kp=Invoke-RestMethod "$KnowledgeWebUrl/api/health" -TimeoutSec 5; if($kp.ready){$knowledgeProxyReady=$true}}catch{}
  # [2026-07-07 19:08:17] 作用：检查知识库根级新挂载页面；理由依据：外部前端实际跳转到 18191/knowledgeManagement/。
  # [2026-08-04 08:31:15] 作用：以PowerShell 5.1非交互解析方式检查知识库挂载页面；理由依据：一键启动不能在最终页面验收阶段出现交互确认。
  try{$kmw=Invoke-WebRequest $KnowledgeMountedWebUrl -UseBasicParsing -TimeoutSec 5; if($kmw.StatusCode -eq 200){$knowledgeMountedWebReady=$true}}catch{}
  # [2026-07-07 16:20:13] 作用：检查知识库新挂载 API 代理；理由依据：知识库新页面必须通过该前缀访问 18320 的 options、prompts、parse。
  try{$kmp=Invoke-RestMethod "$KnowledgeMountedApiUrl/health" -TimeoutSec 5; if($kmp.ready){$knowledgeMountedProxyReady=$true}}catch{}
  # [2026-08-06 10:17:36] 作用：检查看板数据库查询、脱敏目标和原文入口的完整profile身份；理由依据：第二套响应曾实测返回28个172.18.1.212链接，普通ready无法阻断这种串线。
  try{
    # [2026-08-06 10:17:36] 作用：请求看板直连健康身份；理由依据：不经页面代理才能区分后端配置与代理故障。
    $dh=Invoke-RestMethod "$DashboardBackendUrl/health" -TimeoutSec 5
    # [2026-08-06 10:17:36] 作用：保留脱敏依赖身份诊断；理由依据：失败时须直接看到actual主机、端口和公开入口。
    $dashboardLast=$dh|ConvertTo-Json -Depth 8
    # [2026-08-06 10:17:36] 作用：对比看板实际数据库与当前profile的迁移库身份；理由依据：第一套5432与第二套25434必须在运行态可机器判定。
    $dashboardDatabaseIdentityReady=(([string]$dh.database.host -eq $ExternalPgHost) -and (([int]$dh.database.port) -eq ([int]$MigratedPostgresPort)) -and ([string]$dh.database.database -eq 'AIERP'))
    # [2026-08-06 10:17:36] 作用：对比看板原文跳转入口与当前profile挂载页；理由依据：数据来自本机但链接指向另一套同样属于未完全隔离。
    $dashboardKnowledgeIdentityReady=([string]$dh.knowledgeBaseUrl -eq $KnowledgeMountedWebUrl)
    # [2026-08-06 10:17:36] 作用：合并看板数据与链接两项身份门禁；理由依据：只有两项同时属于当前profile才允许全栈结束。
    $dashboardDependencyReady=($dashboardDatabaseIdentityReady -and $dashboardKnowledgeIdentityReady)
    # [2026-08-06 10:17:36] 作用：仅在真实查库和profile身份同时通过时标记看板后端就绪；理由依据：阻断静态页面或错库SELECT 1假绿。
    if($dh.ready -and $dashboardDependencyReady){$dashboardBackendReady=$true}
  }catch{}
  # [2026-07-21 13:38:21] 作用：检查看板WebUI页面健康；理由依据：用户实际通过18431访问前端。
  # [2026-08-04 08:31:16] 作用：以PowerShell 5.1非交互解析方式检查看板WebUI；理由依据：管理员环境的IE组件状态不得影响服务健康结论。
  try{$dw=Invoke-WebRequest "$DashboardWebUrl/health" -UseBasicParsing -TimeoutSec 5; if($dw.StatusCode -eq 200){$dashboardWebReady=$true}}catch{}
  # [2026-08-06 10:17:36] 作用：经看板同源代理复验数据库和原文入口身份；理由依据：页面代理健康不能掩盖后端仍指向第一套的配置串线。
  try{$dp=Invoke-RestMethod "$DashboardWebUrl/api/health" -TimeoutSec 5; if($dp.ready -and ([string]$dp.database.host -eq $ExternalPgHost) -and (([int]$dp.database.port) -eq ([int]$MigratedPostgresPort)) -and ([string]$dp.database.database -eq 'AIERP') -and ([string]$dp.knowledgeBaseUrl -eq $KnowledgeMountedWebUrl)){$dashboardProxyReady=$true}}catch{}
  # [2026-07-29 13:16:00] 作用：仅在全部直连业务端口及其兼容页面链通过时结束等待；理由依据：不再把已删除的 18192 网关层混入服务就绪判断。
  # [2026-07-30 11:26:10] 作用：把知识问答实时同步门禁加入全量服务提前结束条件；理由依据：全部页面健康但 Qdrant 仍是旧内容时不能宣布一键启动完成。
  if($backendReady -and $webReady -and $proxyReady -and $assetBackendReady -and $assetWebReady -and $assetProxyReady -and $frontendProfileReady -and $knowledgeBackendReady -and $knowledgeWebReady -and $knowledgeProxyReady -and $assetMountedWebReady -and $assetMountedProxyReady -and $knowledgeMountedWebReady -and $knowledgeMountedProxyReady -and $dashboardBackendReady -and $dashboardWebReady -and $dashboardProxyReady -and $knowledgeRealtimeSyncReady){break}
  # [2026-08-04 15:01:48] 作用：每20秒输出一次我方服务就绪进度；理由依据：即使外部Getsoft失败或个别数据库未就绪，也必须让现场明确脚本仍在主动验收而非卡死。
  if(($i%10)-eq0){Write-Host "SQL_RAG全量健康验收继续：attempt=$i/90；business=$backendReady；asset=$assetBackendReady；knowledge=$knowledgeBackendReady；dashboard=$dashboardBackendReady；realtime_sync=$knowledgeRealtimeSyncReady"}
  Start-Sleep -Seconds 2
}
# [2026-07-17 13:56:30] 作用：在所有前后端完成启动后重新探测 Qwen；理由：模型可能在较长的 Docker/服务启动阶段退出，最终门禁不能复用早期结果。
$qwenReady=Test-Qwen
# [2026-07-17 13:56:30] 作用：在最终验收时重新探测 Embedding；理由：18001 必须与全部前后端同时存活才算全栈 ready。
$embeddingReady=Test-Embedding
# [2026-07-23 10:28:57] 作用：在我方全部服务启动后重新验证对方 main、浏览器入口与数据库业务接口；理由依据：适配器早期成功不能代替最终同存活验收。
if($getsoftStartupReady -and $getsoftResult -and $getsoftResult.enabled -eq $false){
  # [2026-07-23 10:28:57] 作用：显式关闭时把外部门禁标记为跳过；理由依据：关闭必须是可观察配置，不能产生虚假连接请求。
  $getsoftReady=$true; $getsoftBrowserReady=$true; $getsoftBusinessReady=$true; $getsoftSseReady=$true; $getsoftLast='disabled by GETSOFT_AI_ERP_ENABLED'
}elseif($getsoftStartupReady){
  try{
    $getsoftOpenApi=Invoke-RestMethod "$GetsoftInternalUrl$([string]$GetsoftConfig.openapi_path)" -TimeoutSec 10
    $getsoftPaths=@($getsoftOpenApi.paths.PSObject.Properties.Name)
    $getsoftReady=($getsoftOpenApi.info.title -eq [string]$GetsoftConfig.expected_title -and $getsoftPaths -contains '/api/knowledge/options' -and $getsoftPaths -contains '/api/ai-chat/llamaindex/memory-chat/events')
  }catch{$getsoftLast=$_.Exception.Message}
  # [2026-08-04 08:31:17] 作用：以PowerShell 5.1非交互解析方式复验Getsoft Swagger页面；理由依据：外部服务最终合同不能弹出脚本执行确认并中断全栈汇总。
  try{$getsoftBrowserResponse=Invoke-WebRequest "$GetsoftInternalUrl$([string]$GetsoftConfig.browser_path)" -UseBasicParsing -TimeoutSec 10; $getsoftBrowserReady=($getsoftBrowserResponse.StatusCode -eq 200 -and $getsoftBrowserResponse.Content -match 'Swagger UI')}catch{$getsoftLast=$_.Exception.Message}
  try{$getsoftBusinessResponse=Invoke-RestMethod "$GetsoftInternalUrl$([string]$GetsoftConfig.business_probe_path)" -TimeoutSec 30; $getsoftBusinessReady=($null -ne $getsoftBusinessResponse)}catch{$getsoftLast=$_.Exception.Message}
  # [2026-07-28] 作用：复用适配器刚完成的真实 SSE 消费结果；理由依据：全量 ready 必须包含 clean EOF 和 done，不能再把仅有 HTTP 200 的断流响应标记为成功。
  $getsoftSseReady=(
    $getsoftResult.sse_ready -eq $true -and
    $getsoftResult.sse_probe.clean_eof -eq $true -and
    $getsoftResult.sse_probe.done -eq $true -and
    $getsoftResult.sse_probe.error -eq $false
  )
}
Write-Host ''
# [2026-07-17 13:56:30] 作用：输出最终 Qwen ready 结果；理由：单窗口中可直接确认本地规划与回答模型状态。
Write-Host "Qwen模型：$qwenReady"
# [2026-07-17 13:56:30] 作用：输出最终 Embedding ready 结果；理由：用户无需打开额外窗口检查 18001。
Write-Host "Embedding模型：$embeddingReady"
Write-Host "主业务脑后端健康：$backendReady"
# [2026-07-30 11:26:11] 作用：输出 WebUI 已发布知识双库实时同步状态；理由依据：运维人员必须在同一个一键启动窗口直接确认 PostgreSQL 到 Qdrant 联动已完成首轮。
Write-Host "知识库PostgreSQL→Qdrant实时同步：$knowledgeRealtimeSyncReady"
Write-Host "主业务脑WebUI首页：$webReady"
Write-Host "主业务脑WebUI代理健康：$proxyReady"
Write-Host "资产类型后端健康：$assetBackendReady"
Write-Host "资产类型WebUI首页：$assetWebReady"
Write-Host "资产类型WebUI代理健康：$assetProxyReady"
# [2026-08-06 11:08:00] 作用：输出统一前端profile隔离结果和实际身份；理由依据：运维必须能直接看到第二套是否仍含212地址。
Write-Host "统一前端profile隔离：$frontendProfileReady；诊断：$frontendProfileLast"
# [2026-07-07 16:20:13] 作用：输出资产类型新挂载页面健康状态；理由依据：需要确认 /resourceType/ 给外部前端跳转可用。
Write-Host "资产类型新挂载首页：$assetMountedWebReady"
# [2026-07-07 16:20:13] 作用：输出资产类型新挂载 API 健康状态；理由依据：需要确认 /resourceType/api 没有破坏资产入库链路。
Write-Host "资产类型新挂载代理健康：$assetMountedProxyReady"
# [2026-07-04 10:18:20] 作用：输出知识库后端健康结果；理由依据：便于直接核对解析、提取和数据库依赖是否 ready。
Write-Host "知识库后端健康：$knowledgeBackendReady"
# [2026-07-04 10:18:20] 作用：输出知识库 WebUI 页面结果；理由依据：确认新前端端口可供浏览器访问。
Write-Host "知识库WebUI首页：$knowledgeWebReady"
# [2026-07-04 10:18:20] 作用：输出知识库同源代理结果；理由依据：确认前端请求能够串联到知识库后端。
Write-Host "知识库WebUI代理健康：$knowledgeProxyReady"
# [2026-07-07 19:08:17] 作用：输出知识库新挂载页面健康状态；理由依据：需要确认 /knowledgeManagement/ 可被外部前端跳转。
Write-Host "知识库新挂载首页：$knowledgeMountedWebReady"
# [2026-07-07 16:20:13] 作用：输出知识库新挂载 API 健康状态；理由依据：需要确认知识库下拉、动态提示词和解析上传会打到 18320。
Write-Host "知识库新挂载代理健康：$knowledgeMountedProxyReady"
# [2026-07-21 13:38:24] 作用：输出看板后端健康；理由依据：确认数据库运行时已就绪。
Write-Host "客户风险与商机看板后端健康：$dashboardBackendReady"
# [2026-07-21 13:38:25] 作用：输出看板页面健康；理由依据：确认18431静态页面可访问。
Write-Host "客户风险与商机看板WebUI首页：$dashboardWebReady"
# [2026-07-21 13:38:26] 作用：输出看板代理健康；理由依据：确认18431/api可到达18430。
Write-Host "客户风险与商机看板代理健康：$dashboardProxyReady"
# [2026-08-06 10:17:36] 作用：输出看板当前profile数据库与原文入口隔离结果；理由依据：运维窗口必须能直接区分普通HTTP健康和无串线健康。
Write-Host "客户风险与商机看板profile隔离：$dashboardDependencyReady；诊断：$dashboardLast"
# [2026-07-23 10:28:57] 作用：输出对方后端、浏览器入口和真实数据库接口三项隔离门禁；理由依据：必须证明不是只占端口或只展示文档空壳。
Write-Host "Getsoft ERP AI标准main健康：$getsoftReady"
Write-Host "Getsoft ERP AI浏览器入口：$getsoftBrowserReady"
Write-Host "Getsoft ERP AI数据库业务探针：$getsoftBusinessReady"
Write-Host "Getsoft ERP AI SSE完整流探针：$getsoftSseReady"
# [2026-07-07 18:32:41] 作用：输出本次对外挂载使用的主机地址；理由依据：别人前端配置跳转时需要使用 LAN IP 而不是 127.0.0.1。
Write-Host "对外挂载主机：$PublicHost"
# [2026-07-07 18:32:41] 作用：输出 WebUI 实际监听地址；理由依据：确认 18191 已对局域网开放监听而不是只绑定回环地址。
Write-Host "WebUI监听地址：$WebListenHost"
# [2026-07-17 13:56:30] 作用：输出本地 Embedding 端点；理由：全量启动结果应明确展示 RAG 实际使用的模型服务地址。
Write-Host "Embedding模型地址：$EmbeddingUrl"
Write-Host "后端地址：$BackendUrl"
Write-Host "WebUI地址：$WebUrl"
Write-Host "资产类型后端地址：$AssetTypeBackendUrl"
Write-Host "资产类型WebUI地址：$AssetTypeWebUrl"
# [2026-07-07 16:20:13] 作用：输出资产类型新挂载地址；理由依据：用户和外部前端需要使用该 URL 跳转资产管理页面。
Write-Host "资产类型统一挂载地址：$AssetTypeMountedWebUrl"
# [2026-07-07 16:20:13] 作用：输出资产类型新挂载 API 地址；理由依据：排查 18191 统一代理时需要明确资产请求前缀。
Write-Host "资产类型统一挂载API：$AssetTypeMountedApiUrl"
# [2026-07-04 10:18:20] 作用：输出知识库后端实际地址；理由依据：端口可能回退，测试与排障必须使用本次地址。
Write-Host "知识库后端地址：$KnowledgeBackendUrl"
# [2026-07-04 10:18:20] 作用：输出知识库 WebUI 实际地址；理由依据：为用户提供本次全量启动后的正确页面入口。
Write-Host "知识库WebUI地址：$KnowledgeWebUrl"
# [2026-07-07 16:20:13] 作用：输出知识库新挂载地址；理由依据：用户和外部前端需要使用该 URL 跳转知识库管理页面。
Write-Host "知识库统一挂载地址：$KnowledgeMountedWebUrl"
# [2026-07-07 16:20:13] 作用：输出知识库新挂载 API 地址；理由依据：排查知识库下拉和上传解析时需要明确新代理前缀。
Write-Host "知识库统一挂载API：$KnowledgeMountedApiUrl"
# [2026-08-15 17:30:37] 作用：输出商业知识缓存网关的实际 URL；理由依据：运维验收必须直接确认 Redis Cluster 只能经受控网关被 API 与 Worker 消费。
Write-Host "商业知识缓存网关：$($KnowledgeCommercialRuntime.CacheGatewayUrl)"
# [2026-08-21 09:00:49] 作用：输出全景独立缓存网关实际 URL；理由依据：运维必须确认页面缓存与上传进度 Redis Cluster 是两个独立平面。
Write-Host "知识全景独立缓存：$($KnowledgeCommercialRuntime.PanoramaCacheUrl)"
# [2026-08-15 17:30:37] 作用：输出商业知识断点上传服务的实际 URL；理由依据：前端断点续传和故障排查必须使用当前 profile 的固定入口。
Write-Host "商业知识断点上传服务：$($KnowledgeCommercialRuntime.TusdUrl)"
# [2026-08-15 17:30:37] 作用：输出商业知识 MinIO API 的实际 URL；理由依据：对象存储探针和交付验收需要明确当前 profile 的对象入口。
Write-Host "商业知识对象存储API：$($KnowledgeCommercialRuntime.MinioApiUrl)"
# [2026-08-15 17:30:37] 作用：输出商业知识 MinIO 控制台的实际 URL；理由依据：运维人员需要检查分布式对象、副本和 Bucket 状态。
Write-Host "商业知识对象存储控制台：$($KnowledgeCommercialRuntime.MinioConsoleUrl)"
# [2026-08-17 09:40:50] 作用：输出商业知识 RabbitMQ 管理端的实际 URL；理由依据：使用启动器真实返回的 RabbitMqManagementUrl 字段，避免健康已通过但运维地址显示为空。
Write-Host "商业知识消息队列管理：$($KnowledgeCommercialRuntime.RabbitMqManagementUrl)"
# [2026-08-15 17:30:37] 作用：输出商业知识 Flower 的实际 URL；理由依据：分层 Worker 在线状态和任务执行必须具备独立观测入口。
Write-Host "商业知识Worker监控：$($KnowledgeCommercialRuntime.FlowerUrl)"
# [2026-08-15 17:30:37] 作用：输出商业知识 Prometheus 的实际 URL；理由依据：商业验收需要查看队列、对象存储和 Worker 指标采集状态。
Write-Host "商业知识Prometheus：$($KnowledgeCommercialRuntime.PrometheusUrl)"
# [2026-08-15 17:30:37] 作用：输出商业知识 Grafana 的实际 URL；理由依据：线上容量、延迟和故障告警必须具备可视化入口。
Write-Host "商业知识Grafana：$($KnowledgeCommercialRuntime.GrafanaUrl)"
# [2026-08-17 08:45:11] 作用：输出 Knowledge PgBouncer 实际 URL；理由依据：运维需要明确 Worker 的数据库连接池入口且输出不含凭据。
Write-Host "商业知识PgBouncer：$($KnowledgeCommercialRuntime.PgbouncerUrl)"
# [2026-07-21 13:38:27] 作用：输出看板后端地址；理由依据：接口测试和排障需使用本次固定地址。
Write-Host "客户风险与商机看板后端地址：$DashboardBackendUrl"
# [2026-07-21 13:38:28] 作用：输出看板WebUI地址；理由依据：给用户明确的动态页面入口。
Write-Host "客户风险与商机看板WebUI地址：$DashboardWebUrl"
# [2026-07-23 10:28:57] 作用：输出对方浏览器与 API 独立地址；理由依据：用户和另一位开发者无需进入我方 WebUI 即可继续使用自己的业务逻辑。
Write-Host "Getsoft ERP AI浏览器地址：$GetsoftBrowserUrl"
Write-Host "Getsoft ERP AI API地址：$GetsoftPublicUrl/api"
Write-Host "后端错误日志：$berr"
Write-Host "WebUI错误日志：$werr"
Write-Host "资产类型后端错误日志：$assetBackendErr"
Write-Host "资产类型WebUI错误日志：$assetWebErr"
# [2026-07-04 10:18:20] 作用：输出知识库后端错误日志位置；理由依据：外部 API 或数据库异常需要凭日志定位。
Write-Host "知识库后端错误日志：$knowledgeBackendErr"
# [2026-07-04 10:18:20] 作用：输出知识库 WebUI 错误日志位置；理由依据：代理和静态服务异常需要与后端日志分开诊断。
Write-Host "知识库WebUI错误日志：$knowledgeWebErr"
# [2026-07-21 13:38:29] 作用：输出看板后端错误日志；理由依据：DeepSeek或SQL异常可直接定位。
Write-Host "客户风险与商机看板后端错误日志：$dashboardBackendErr"
# [2026-07-21 13:38:30] 作用：输出看板WebUI错误日志；理由依据：代理异常可独立定位。
Write-Host "客户风险与商机看板WebUI错误日志：$dashboardWebErr"
# [2026-07-23 10:28:57] 作用：输出对方隔离日志与最后错误；理由依据：失败应直接定位对方源码/依赖，不与 SQL_RAG 日志混杂。
if($getsoftResult){Write-Host "Getsoft ERP AI错误日志：$($getsoftResult.stderr_log)"}
Write-Host "Getsoft ERP AI诊断：$getsoftLast"
Write-Host $last
# [2026-07-30 11:26:12] 作用：输出知识问答实时同步完整诊断；理由依据：门禁失败时必须显示 profile、计数和最后错误而不是只返回 false。
Write-Host $knowledgeRealtimeSyncLast
Write-Host $assetLast
# [2026-07-04 10:18:20] 作用：输出知识库健康接口的完整结构化结果；理由依据：保留 API 密钥、模型与数据库检查的可见证据。
Write-Host $knowledgeLast
# [2026-07-21 13:38:31] 作用：输出看板健康详情；理由依据：保留目标资产名和数据库错误诊断。
Write-Host $dashboardLast
# [2026-07-28] 作用：把最终门禁拆成具名合同并只报告实际失败项；理由依据：
# 原来的长布尔表达式只显示“没有全部 ready”，即使 22 项均正常也无法判断哪个外部探针造成误判。
$FinalReadiness=[ordered]@{
  qwen_model=$qwenReady
  embedding_model=$embeddingReady
  business_brain_backend=$backendReady
  # [2026-07-30 11:26:13] 作用：把知识问答实时同步加入最终具名就绪合同；理由依据：固定一键启动退出前必须验证 WebUI 修改能继续进入 Qdrant。
  knowledge_realtime_sync=$knowledgeRealtimeSyncReady
  business_brain_web=$webReady
  business_brain_proxy=$proxyReady
  asset_backend=$assetBackendReady
  asset_web=$assetWebReady
  asset_proxy=$assetProxyReady
  # [2026-08-06 11:08:00] 作用：把统一前端profile身份加入最终具名合同；理由依据：挂载串线必须与普通页面健康分开成为硬门禁。
  frontend_profile_isolation=$frontendProfileReady
  asset_mounted_web=$assetMountedWebReady
  asset_mounted_proxy=$assetMountedProxyReady
  knowledge_backend=$knowledgeBackendReady
  knowledge_web=$knowledgeWebReady
  knowledge_proxy=$knowledgeProxyReady
  knowledge_mounted_web=$knowledgeMountedWebReady
  knowledge_mounted_proxy=$knowledgeMountedProxyReady
  # [2026-08-15 17:30:37] 作用：把商业知识基础设施聚合健康结果加入最终硬门禁；理由依据：Redis、RabbitMQ、MinIO、tusd、Worker 和观测任一未就绪都不能报告全量成功。
  knowledge_commercial_infrastructure=$KnowledgeCommercialRuntime.Ready
  dashboard_backend=$dashboardBackendReady
  # [2026-08-06 10:17:36] 作用：把看板数据库与原文入口隔离结果写入最终具名合同；理由依据：部署验收需要与普通HTTP健康分开报告。
  dashboard_profile_isolation=$dashboardDependencyReady
  dashboard_web=$dashboardWebReady
  dashboard_proxy=$dashboardProxyReady
  getsoft_openapi=$getsoftReady
  getsoft_browser=$getsoftBrowserReady
  getsoft_business=$getsoftBusinessReady
  # 此项是适配器的 transport-only SSE：验证局域网端口、分块传输、done 和 clean EOF，
  # 不把第三方模型是否在 120 秒内回答混入“服务是否启动”的判断。
  getsoft_sse_transport=$getsoftSseReady
}
$FailedReadiness=@(
  $FinalReadiness.GetEnumerator() |
    Where-Object { $_.Value -ne $true } |
    ForEach-Object { $_.Key }
)
Write-Host ("最终就绪合同：" + ($FinalReadiness | ConvertTo-Json -Compress))
# [2026-08-04 17:02:31] 作用：在第二套健康验收结束后输出全部被隔离阶段；理由依据：运维人员先获得已启动服务事实，再一次性处理数据库、BM25、进程或Getsoft失败。
if($isServerAdministratorEntry){Write-Host ("第二套分阶段启动故障汇总：" + (@($ServerSecondStartupFailures) | ConvertTo-Json -Compress))}
# [2026-08-04 17:02:32] 作用：在所有服务均已逐项尝试和验收后统一决定退出状态；理由依据：第二套允许部分服务继续运行，但不能把阶段故障或健康红项误报为全量成功。
if($FailedReadiness.Count -gt 0 -or $ServerSecondStartupFailures.Count -gt 0){
  # [2026-08-04 17:02:33] 作用：构造阶段故障摘要；理由依据：最终异常必须同时携带健康红项和更早的原始依赖故障。
  $isolatedFailureSummary=if($ServerSecondStartupFailures.Count -gt 0){$ServerSecondStartupFailures -join ' | '}else{'none'}
  # [2026-08-04 17:02:34] 作用：在最后统一返回非零退出；理由依据：失败信号保留给自动化，但此前成功创建的其他服务不会被回收。
  throw ("全量服务未全部 ready；失败项：" + ($FailedReadiness -join ', ') + "；已隔离阶段：$isolatedFailureSummary")
}
# [2026-08-25 16:29:30] 作用：初始化克隆库可移植种子导出成功标志；理由依据：Qdrant 健康切换瞬间的单次连接拒绝不能误判整套已就绪服务失败。
$PortableCloneExportSucceeded=$false
# [2026-08-25 16:29:30] 作用：限定最多三次执行同一原子种子导出；理由依据：吸收短暂端口竞态且保持持续故障最终失败关闭。
for($PortableCloneExportAttempt=1;$PortableCloneExportAttempt -le 3;$PortableCloneExportAttempt++){
  # [2026-08-25 16:29:30] 作用：全量服务 ready 后把当前两个克隆库刷新为项目内可移植种子；理由依据：用户随后压缩整个项目时必须自动携带最新可用 PG dump 与 Qdrant snapshot。
  & $Py $PortableCloneScript export --seed-dir $PortableCloneSeedDir --env-file $EnvFile
  # [2026-08-25 16:29:30] 作用：在本轮导出完整成功时记录最终成功并停止重试；理由依据：避免无意义地重复生成数据库快照。
  if($LASTEXITCODE -eq 0){$PortableCloneExportSucceeded=$true;break}
  # [2026-08-25 16:29:30] 作用：仅在尚有剩余机会时记录瞬断重试原因；理由依据：运维日志需要区分瞬态恢复与最终失败。
  if($PortableCloneExportAttempt -lt 3){Write-Warning "克隆库可移植种子导出第 $PortableCloneExportAttempt 次失败，5 秒后重试。"}
  # [2026-08-25 16:29:30] 作用：在下一次导出前等待 Qdrant 端口稳定；理由依据：Docker 健康切换期间立即重连可能连续命中同一瞬断窗口。
  if($PortableCloneExportAttempt -lt 3){Start-Sleep -Seconds 5}
}
# [2026-08-25 16:29:30] 作用：三次导出均失败时阻断可迁移部署标记；理由依据：只有 PG、Qdrant、清单哈希和数量全部生成成功，当前目录才具备跨电脑运维能力。
if(-not $PortableCloneExportSucceeded){throw '两个克隆库可移植种子导出失败，不能把当前目录标记为可迁移部署'}
# [2026-07-15 10:04:45] 作用：全量服务 ready 后再次扫描根依赖和整个 SQL_RAG；理由依据：启动期间发生二次污染时不能报告成功或生成新基线。
$PostLaunchIntegrityJson=& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $RuntimeIntegrityScript -RepoRoot $RepoRoot -SqlRag $SqlRag
# [2026-07-15 10:04:45] 作用：记录启动后完整性命令退出码；理由依据：检测脚本自身失败也必须阻断备份。
$PostLaunchIntegrityExitCode=$LASTEXITCODE
# [2026-07-15 10:04:45] 作用：拒绝检测命令异常的启动结果；理由依据：无法证明代码干净时不能声称当前服务可靠。
if($PostLaunchIntegrityExitCode -ne 0){throw "启动后 ONEDLP 完整性检查失败，退出码=$PostLaunchIntegrityExitCode"}
# [2026-07-15 10:04:45] 作用：解析启动后结构化完整性结果；理由依据：必须读取 ready 和具体污染区域。
$PostLaunchIntegrity=$PostLaunchIntegrityJson | ConvertFrom-Json
# [2026-07-15 10:04:45] 作用：检测到任何二次污染时阻断；理由依据：被污染源码不能固化为最新成功基线。
if(!$PostLaunchIntegrity.ready){throw ("启动后 ONEDLP 完整性检查失败：" + ($PostLaunchIntegrity | ConvertTo-Json -Depth 8 -Compress))}
# [2026-07-15 10:04:45] 作用：记录本次全部通过的健康门禁名称；理由依据：备份元数据必须能证明前后端、代理和挂载入口都成功。
# [2026-07-29 13:16:00] 作用：记录业务直连拓扑下的全部成功门禁；理由依据：恢复基线不得再要求不存在的 asset_webui_internal 网关层。
# [2026-07-30 11:31:00] 作用：把知识问答实时同步门禁写入成功备份元数据；理由依据：以后恢复基线时必须能证明 PostgreSQL 与 Qdrant 联动曾真实通过。
# [2026-08-15 17:30:37] 作用：把商业知识基础设施门禁写入成功备份元数据；理由依据：以后恢复的基线必须证明持久任务、缓存、消息队列、对象存储和分层 Worker 曾真实通过验收。
$PassedHealthGates=@('local_qwen_model','local_embedding_model','business_brain_backend','knowledge_realtime_sync','business_brain_webui','business_brain_proxy','asset_backend','asset_webui','asset_proxy','frontend_profile_isolation','knowledge_backend','knowledge_webui','knowledge_proxy','asset_mounted_web','asset_mounted_proxy','knowledge_mounted_web','knowledge_mounted_proxy','knowledge_commercial_infrastructure','customer_risk_dashboard_backend','customer_risk_dashboard_profile_isolation','customer_risk_dashboard_webui','customer_risk_dashboard_proxy','getsoft_ai_erp_main','getsoft_ai_erp_browser','getsoft_ai_erp_business_probe','getsoft_ai_erp_sse_complete_stream')
# [2026-07-15 10:04:45] 作用：将健康门禁序列化为 Windows PowerShell 5.1 可稳定传递的单参数；理由依据：powershell.exe -File 不能可靠绑定多值数组。
$PassedHealthGatesCsv=$PassedHealthGates -join ','
# [2026-07-08 14:32:16] 作用：全量 ready 后执行运行时备份；理由依据：只有通过全部健康检查的状态才能作为以后恢复依赖和源码的成功基线。
if(Test-Path -LiteralPath $RuntimeBackupScript){
  # [2026-07-08 14:32:16] 作用：调用备份脚本并传入当前仓库路径；理由依据：备份必须覆盖根 .venv、资产类型、知识库和启动脚本。
  & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $RuntimeBackupScript -RepoRoot $RepoRoot -SqlRag $SqlRag -BackupRoot $RuntimeBackupRoot -FullStackReady -HealthGates $PassedHealthGatesCsv -Quiet
  # [2026-07-08 14:37:44] 作用：读取备份脚本退出码；理由依据：powershell.exe 是 native 命令，备份失败不会天然中断当前脚本。
  $RuntimeBackupExitCode=$LASTEXITCODE
  # [2026-07-08 14:37:44] 作用：备份脚本失败时中止全量启动；理由依据：没有成功基线就不能满足“以后优先对照备份恢复”的要求。
  if($RuntimeBackupExitCode -ne 0){throw "SQL_RAG 运行时备份脚本执行失败，退出码=$RuntimeBackupExitCode"}
# [2026-07-08 14:32:16] 作用：结束成功后备份脚本调用；理由依据：PowerShell 代码块必须闭合。
}
