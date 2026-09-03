# [2026-08-15 22:04:00] 作用：声明强类型启动参数；理由依据：固定入口必须把 profile、数据库、Docker 身份和公开地址作为一个原子合同传入。
param(
  # [2026-08-15 22:04:00] 作用：接收仓库根目录；理由依据：Compose、.env 和 Knowledge 源码均从当前工作区解析。
  [Parameter(Mandatory=$true)][string]$RepoRoot,
  # [2026-08-15 22:04:00] 作用：接收 SQL_RAG 根目录；理由依据：profile 文件和运行目录不依赖当前工作目录。
  [Parameter(Mandatory=$true)][string]$SqlRagRoot,
  # [2026-08-15 22:04:00] 作用：接收部署 profile；理由依据：第一套与第二套拥有完全隔离的端口、容器、网络、桶和缓存 key。
  [Parameter(Mandatory=$true)][string]$DeploymentProfile,
  # [2026-08-15 22:04:00] 作用：接收本次唯一服务合同；理由依据：独立第二套不得回读本地双 profile 文件。
  [Parameter(Mandatory=$true)]$ServicePortProfile,
  # [2026-08-15 22:04:00] 作用：接收当前 PostgreSQL URL；理由依据：Celery Worker 与 Windows API 必须共享同一强一致业务真相。
  [Parameter(Mandatory=$true)][string]$KnowledgeDatabaseUrl,
  # [2026-08-15 22:04:00] 作用：接收 Docker 容器前缀；理由依据：同机两套容器名称不能冲突。
  [Parameter(Mandatory=$true)][string]$ContainerNamePrefix,
  # [2026-08-15 22:04:00] 作用：接收主 Compose 项目名；理由依据：商业卷和网络归属必须随 profile 隔离。
  [Parameter(Mandatory=$true)][string]$ComposeProjectName,
  # [2026-08-15 22:04:00] 作用：接收当前公开主机；理由依据：输出给 WebUI 和运维的 URL 不得串到另一台服务器。
  [Parameter(Mandatory=$true)][string]$PublicHost
)
# [2026-08-15 22:04:00] 作用：启用严格错误处理；理由依据：任何 Broker、缓存、对象或 Worker 未就绪都阻止 API 接收商业任务。
$ErrorActionPreference='Stop'

# [2026-08-15 22:04:00] 作用：生成密码学随机文本；理由依据：RabbitMQ、Redis、MinIO、Flower、Grafana 和内部缓存令牌禁止固定默认密码。
function New-KmSecret {
  # [2026-08-15 22:04:00] 作用：创建 32 字节随机缓冲；理由依据：服务凭据具有足够熵且适合 URL 编码。
  $bytes=New-Object byte[] 32
  # [2026-08-15 22:04:00] 作用：使用系统随机源填充；理由依据：不得以时间戳或伪随机数生成生产密钥。
  [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
  # [2026-08-15 22:04:00] 作用：返回 URL 安全文本；理由依据：Broker URL 和 Compose 环境无需额外转义斜杠与加号。
  return [Convert]::ToBase64String($bytes).TrimEnd('=').Replace('+','-').Replace('/','_')
}

# [2026-08-15 22:04:00] 作用：读取并校验 profile 端口；理由依据：Compose 不允许使用硬编码或另一套残留环境值。
function Get-KmPort {
  # [2026-08-15 22:04:00] 作用：声明端口键参数；理由依据：每项工具服务拥有具名 URL 合同。
  param([Parameter(Mandatory=$true)][string]$Name)
  # [2026-08-15 22:04:00] 作用：读取端口属性；理由依据：缺项代表发行包与启动脚本版本漂移。
  $property=$ServicePortProfile.ports.PSObject.Properties[$Name]
  # [2026-08-15 22:04:00] 作用：阻断缺失端口；理由依据：商业服务不能静默回落默认端口。
  if($null-eq$property){throw "商业知识服务缺少端口：$Name"}
  # [2026-08-15 22:04:00] 作用：转换端口值；理由依据：后续 URL 和 Docker 发布合同使用整数。
  $port=[int]$property.Value
  # [2026-08-15 22:04:00] 作用：校验 TCP 端口范围；理由依据：无效值必须在修改 Docker 状态前失败。
  if($port-lt1-or$port-gt65535){throw "商业知识服务端口无效：$Name=$port"}
  # [2026-08-15 22:04:00] 作用：返回已验证端口；理由依据：调用方统一消费同一事实源。
  return $port
}

# [2026-09-03 11:14:29] 作用：读取并验证第二套容器出口代理合同；理由依据：只有 profile 明确声明的代理候选和内部绕行名单才能进入商业 Worker 环境。
function Get-KmEgressProxyContract {
  # [2026-09-03 11:14:29] 作用：接收当前服务 profile；理由依据：第一套 profile 没有出口修复权限且必须保持原 Compose 行为。
  param([Parameter(Mandatory=$true)]$Profile)
  # [2026-09-03 11:14:29] 作用：让第一套直接返回未配置状态；理由依据：第二套出口修复不得扩散到 local 或 Alibaba Cloud 入口。
  if($DeploymentProfile-ne'server_second_ports'){return $null}
  # [2026-09-03 11:14:29] 作用：读取 Docker profile 属性；理由依据：出口合同必须属于第二套独立 Docker 身份而不是顶层共享配置。
  $dockerProperty=$Profile.PSObject.Properties['docker']
  # [2026-09-03 11:14:29] 作用：阻断缺失 Docker profile；理由依据：没有独立 Docker 身份时不能判断代理作用域。
  if($null-eq$dockerProperty-or$null-eq$dockerProperty.Value){throw '第二套出口代理合同缺少 docker profile。'}
  # [2026-09-03 11:14:29] 作用：读取出口代理属性；理由依据：目标机必须从版本化 profile 取得代理候选而不能依赖临时用户环境变量。
  $egressProperty=$dockerProperty.Value.PSObject.Properties['egress_proxy']
  # [2026-09-03 11:14:29] 作用：阻断缺失出口代理合同；理由依据：容器无可达外部 LLM 时必须在部署层明确失败。
  if($null-eq$egressProperty-or$null-eq$egressProperty.Value){throw '第二套出口代理合同缺失。'}
  # [2026-09-03 11:14:29] 作用：保存结构化出口代理对象；理由依据：后续校验和 override 生成必须复用同一事实源。
  $egress=$egressProperty.Value
  # [2026-09-03 11:14:29] 作用：读取只读供应商探针 URL；理由依据：候选代理必须实际建立到业务 LLM 供应商的 HTTPS 路径。
  $probeUrl=([string]$egress.probe_url).Trim()
  # [2026-09-03 11:14:29] 作用：阻断空白供应商探针 URL；理由依据：空地址会把出口故障伪装成代理配置成功。
  if([string]::IsNullOrWhiteSpace($probeUrl)){throw '第二套出口代理探针 URL 为空。'}
  # [2026-09-03 11:14:29] 作用：解析供应商探针 URI；理由依据：字符串前缀不能证明目标是 HTTPS 且没有用户凭据。
  try{$probeUri=[uri]$probeUrl}catch{throw "第二套出口代理探针 URL 无效：$probeUrl"}
  # [2026-09-03 11:14:29] 作用：限制探针为 HTTPS 无凭据 URL；理由依据：只读 401/403 也足以证明 TLS 出口，不能把密钥放入 profile。
  if($probeUri.Scheme-ne'https'-or[string]::IsNullOrWhiteSpace($probeUri.Host)-or-not[string]::IsNullOrWhiteSpace($probeUri.UserInfo)){throw "第二套出口代理探针 URL 必须是无凭据 HTTPS：$probeUrl"}
  # [2026-09-03 11:14:29] 作用：读取代理候选集合；理由依据：Docker Desktop 网关地址可能在重启后变化，必须保留有序候选而非写死单点。
  $candidateValues=@($egress.candidates|ForEach-Object{$_})
  # [2026-09-03 11:14:29] 作用：阻断空代理候选集合；理由依据：没有可验证候选时不能让 Worker 继续无代理超时。
  if($candidateValues.Count-eq0){throw '第二套出口代理候选为空。'}
  # [2026-09-03 11:14:29] 作用：初始化已验证代理候选列表；理由依据：后续选择必须保留候选名称、URI 主机和端口的结构化值。
  $candidates=New-Object 'System.Collections.Generic.List[object]'
  # [2026-09-03 11:14:29] 作用：逐项验证代理候选字段；理由依据：未经校验的 URL 不能安全写入 Compose YAML 或 Docker 参数。
  foreach($candidate in $candidateValues){
    # [2026-09-03 11:14:29] 作用：读取代理候选名称；理由依据：现场日志需要指出实际命中的网关而不输出任何密钥。
    $candidateName=([string]$candidate.name).Trim()
    # [2026-09-03 11:14:29] 作用：读取代理候选 URL；理由依据：同一候选 URL 同时用于容器探针和 Worker 环境。
    $candidateUrl=([string]$candidate.url).Trim()
    # [2026-09-03 11:14:29] 作用：阻断空白候选字段；理由依据：空值会导致 Docker run 参数和 YAML 合同不确定。
    if([string]::IsNullOrWhiteSpace($candidateName)-or[string]::IsNullOrWhiteSpace($candidateUrl)){throw '第二套出口代理候选名称或 URL 为空。'}
    # [2026-09-03 11:14:29] 作用：解析代理候选 URI；理由依据：必须结构化确认 HTTP 代理主机、端口且不含凭据或路径。
    try{$candidateUri=[uri]$candidateUrl}catch{throw "第二套出口代理候选 URL 无效：$candidateUrl"}
    # [2026-09-03 11:14:29] 作用：限制代理 URI 形态；理由依据：仅允许无凭据的 HTTP/HTTPS host:port，避免把任意字符串注入 Docker 配置。
    if($candidateUri.Scheme-notin@('http','https')-or[string]::IsNullOrWhiteSpace($candidateUri.Host)-or$candidateUri.Port-lt1-or$candidateUri.Port-gt65535-or-not[string]::IsNullOrWhiteSpace($candidateUri.UserInfo)-or$candidateUri.AbsolutePath-ne'/'-or-not[string]::IsNullOrWhiteSpace($candidateUri.Query)-or-not[string]::IsNullOrWhiteSpace($candidateUri.Fragment)){throw "第二套出口代理候选必须是无凭据 host:port：$candidateUrl"}
    # [2026-09-03 11:14:29] 作用：限制代理主机字符；理由依据：当前 Docker Desktop 网关只允许 DNS/IPv4 主机名，禁止控制字符进入 YAML。
    if($candidateUri.Host-notmatch'^[A-Za-z0-9][A-Za-z0-9._-]*$'){throw "第二套出口代理候选主机无效：$candidateUrl"}
    # [2026-09-03 11:14:29] 作用：保存已解析的代理候选；理由依据：后续选择不再重新解析 profile 原始文本。
    [void]$candidates.Add([pscustomobject]@{Name=$candidateName;Url=$candidateUrl;Host=$candidateUri.Host;Port=[int]$candidateUri.Port})
  }
  # [2026-09-03 11:14:29] 作用：阻断重复代理候选；理由依据：重复地址会造成无意义探针并掩盖候选顺序证据。
  if(@($candidates|ForEach-Object{$_.Url}|Sort-Object -Unique).Count-ne$candidates.Count){throw '第二套出口代理候选 URL 重复。'}
  # [2026-09-03 11:14:29] 作用：读取允许代理绕行的 Worker 服务集合；理由依据：只有 LLM、ASR 和视觉外部模型 Worker 需要代理，其他队列不得改变。
  $workerServices=@($egress.worker_services|ForEach-Object{([string]$_).Trim()}|Where-Object{$_})
  # [2026-09-03 11:14:29] 作用：声明唯一允许注入代理的服务；理由依据：避免把外部出口环境扩散到 RabbitMQ、Redis、MinIO、持久化或索引服务。
  $expectedWorkerServices=@('km-worker-llm','km-worker-asr','km-worker-vision')
  # [2026-09-03 11:14:29] 作用：比较 profile 服务集合；理由依据：代理注入范围必须精确固定为三个模型 Worker。
  if(($workerServices|Sort-Object)-join',' -ne($expectedWorkerServices|Sort-Object)-join','){throw "第二套出口代理 Worker 集合无效：$($workerServices-join',')"}
  # [2026-09-03 11:14:29] 作用：读取内部绕行主机集合；理由依据：代理只能承载外部模型请求，商业私网和迁移数据库必须保持直连。
  $noProxyValues=@($egress.no_proxy|ForEach-Object{([string]$_).Trim()}|Where-Object{$_})
  # [2026-09-03 11:14:29] 作用：阻断空内部绕行集合；理由依据：缺少 NO_PROXY 会把内部队列和数据库请求错误送往外部代理。
  if($noProxyValues.Count-eq0){throw '第二套出口代理 NO_PROXY 集合为空。'}
  # [2026-09-03 11:14:29] 作用：验证内部绕行值字符；理由依据：Compose 环境值只允许主机、网段和通配符，不允许换行或命令字符。
  foreach($noProxyValue in $noProxyValues){if($noProxyValue-notmatch'^[A-Za-z0-9.*:_/-]+$'){throw "第二套出口代理 NO_PROXY 值无效：$noProxyValue"}}
  # [2026-09-03 11:14:29] 作用：返回完整出口代理合同；理由依据：调用方统一消费已验证 URL、候选、服务和绕行集合。
  return [pscustomobject]@{ProbeUrl=$probeUrl;Candidates=@($candidates);WorkerServices=$expectedWorkerServices;NoProxy=($noProxyValues-join',')}
}

# [2026-09-03 13:26:00] 作用：通过 .NET 进程向 Docker stdin 写入多行探针；理由依据：PowerShell 管道向原生 Docker 的 stdin 在当前运行时可能为空，不能把空脚本的 exit=0 当作网络证据。
function Invoke-KmDockerPythonScript {
  # [2026-09-03 13:26:01] 作用：接收 Docker 参数和待执行 Python 文本；理由依据：所有候选探针必须复用同一无引号歧义的原生进程入口。
  param([Parameter(Mandatory=$true)][string[]]$Arguments,[Parameter(Mandatory=$true)][string]$Script)
  # [2026-09-03 13:26:02] 作用：解析 Docker 可执行文件；理由依据：目标管理员环境的 PATH 可能不同，必须使用当前实际 CLI。
  $dockerCommand=Get-Command docker.exe -ErrorAction Stop
  # [2026-09-03 13:26:03] 作用：创建不经 shell 的进程启动描述；理由依据：重定向 stdin/stdout/stderr 才能保留真实容器脚本结果。
  $processStartInfo=New-Object System.Diagnostics.ProcessStartInfo
  # [2026-09-03 13:26:04] 作用：绑定当前 Docker CLI 路径；理由依据：不能让系统选择另一版本 Docker 覆盖目标 Linux Engine。
  $processStartInfo.FileName=$dockerCommand.Source
  # [2026-09-03 13:26:05] 作用：初始化安全的双引号参数集合；理由依据：参数值均已由 profile/调用方限制为无换行、无引号文本。
  $quotedArguments=New-Object 'System.Collections.Generic.List[string]'
  # [2026-09-03 13:26:06] 作用：逐项校验并引用 Docker 参数；理由依据：Windows PowerShell 5.1 的 ProcessStartInfo 不支持 ArgumentList，必须显式避免参数拼接注入。
  foreach($argument in @($Arguments)){
    # [2026-09-03 13:26:07] 作用：阻断换行或双引号参数；理由依据：这两类字符会改变 Windows 原生命令行边界并破坏 Docker 合同。
    if(([string]$argument)-match'[\r\n"]'){throw '第二套出口探针 Docker 参数包含非法引号或换行。'}
    # [2026-09-03 13:26:08] 作用：保存单个双引号参数；理由依据：统一参数边界可兼容 Windows PowerShell 5.1 和 PowerShell 7。
    [void]$quotedArguments.Add('"'+[string]$argument+'"')
  }
  # [2026-09-03 13:26:09] 作用：生成 Docker 原生命令行；理由依据：所有参数已逐项验证，不能再依赖 PowerShell 管道转换。
  $processStartInfo.Arguments=($quotedArguments-join' ')
  # [2026-09-03 13:26:10] 作用：关闭 shell 执行；理由依据：Docker 参数和目标 Engine 必须由同一子进程直接接收。
  $processStartInfo.UseShellExecute=$false
  # [2026-09-03 13:26:11] 作用：隐藏探针窗口；理由依据：一键启动不应额外弹出控制台，但日志仍需保留在返回对象。
  $processStartInfo.CreateNoWindow=$true
  # [2026-09-03 13:26:12] 作用：开启标准输入重定向；理由依据：多行 Python 必须逐字写入容器而不是依赖失真的 PowerShell pipeline。
  $processStartInfo.RedirectStandardInput=$true
  # [2026-09-03 13:26:13] 作用：开启标准输出重定向；理由依据：机器可读状态码必须从容器 stdout 提取。
  $processStartInfo.RedirectStandardOutput=$true
  # [2026-09-03 13:26:14] 作用：开启标准错误重定向；理由依据：Docker/网络错误不能被 stdout 成功文本掩盖。
  $processStartInfo.RedirectStandardError=$true
  # [2026-09-03 13:26:15] 作用：创建可释放的 Docker 子进程对象；理由依据：每个候选和网络探针都必须结束并释放句柄。
  $process=New-Object System.Diagnostics.Process
  # [2026-09-03 13:26:16] 作用：绑定进程启动描述；理由依据：后续 Start、stdin 和输出读取必须作用于同一 Docker 调用。
  $process.StartInfo=$processStartInfo
  try{
    # [2026-09-03 13:26:17] 作用：启动 Docker 原生进程；理由依据：只有真实子进程退出码才可作为探针门禁事实。
    [void]$process.Start()
    # [2026-09-03 13:26:18] 作用：写入完整多行 Python 探针；理由依据：避免空 stdin 造成无脚本 exit=0 的假结果。
    $process.StandardInput.Write($Script)
    # [2026-09-03 13:26:19] 作用：关闭探针 stdin；理由依据：Python 读取到 EOF 后才会执行并退出，避免一直等待输入。
    $process.StandardInput.Close()
    # [2026-09-03 13:26:20] 作用：异步读取 stdout；理由依据：同时消费两个输出流以避免 Docker 错误较多时发生管道死锁。
    $stdoutTask=$process.StandardOutput.ReadToEndAsync()
    # [2026-09-03 13:26:21] 作用：异步读取 stderr；理由依据：保留 Docker 原生诊断且不阻塞 stdout 消费。
    $stderrTask=$process.StandardError.ReadToEndAsync()
    # [2026-09-03 13:26:22] 作用：等待 Docker 进程完成；理由依据：退出码和完整输出必须来自同一次容器执行。
    $process.WaitForExit()
    # [2026-09-03 13:26:23] 作用：取得 stdout 任务结果；理由依据：状态行只在进程结束后解析，避免半行误判。
    $stdout=[string]$stdoutTask.Result
    # [2026-09-03 13:26:24] 作用：取得 stderr 任务结果；理由依据：失败日志需要与 stdout 一起返回给候选选择器。
    $stderr=[string]$stderrTask.Result
    # [2026-09-03 13:26:25] 作用：初始化统一输出集合；理由依据：调用方必须稳定处理空输出、尾换行和双流结果。
    $output=New-Object 'System.Collections.Generic.List[string]'
    # [2026-09-03 13:26:26] 作用：逐行加入 stdout；理由依据：供应商状态行按行正则提取且不应携带空白尾项。
    foreach($line in @($stdout -split "`r?`n")){if(-not[string]::IsNullOrWhiteSpace($line)){[void]$output.Add($line)}}
    # [2026-09-03 13:26:27] 作用：逐行加入 stderr；理由依据：Docker 错误需保留但仍通过有限输出返回，避免日志无限增长。
    foreach($line in @($stderr -split "`r?`n")){if(-not[string]::IsNullOrWhiteSpace($line)){[void]$output.Add($line)}}
    # [2026-09-03 13:26:28] 作用：返回原生退出码和有限输出；理由依据：探针门禁必须同时判断脚本状态、Docker 状态和供应商 HTTP 状态。
    return [pscustomobject]@{ExitCode=[int]$process.ExitCode;Output=@($output|Select-Object -Last 24)}
  }finally{
    # [2026-09-03 13:26:29] 作用：释放 Docker 子进程句柄；理由依据：重复冷启动不能积累原生进程资源。
    $process.Dispose()
  }
}

# [2026-09-03 13:26:30] 作用：在 Docker 容器内验证代理到供应商的 HTTPS；理由依据：宿主或 Docker daemon 的代理字段不能证明业务 Worker 实际可出站。
function Invoke-KmEgressProxyProbe {
  # [2026-09-03 11:14:29] 作用：接收已验证的镜像、目标 URL、代理和绕行值；理由依据：探针必须与将写入 Worker 的同一环境完全一致。
  # [2026-09-03 13:18:00] 作用：接收实际 Docker 网络名；理由依据：default bridge 的出口结果不能替代商业 Worker 网络的真实路由证据。
  param([Parameter(Mandatory=$true)][string]$Image,[Parameter(Mandatory=$true)][string]$ProbeUrl,[Parameter(Mandatory=$true)][string]$ProxyUrl,[Parameter(Mandatory=$true)][string]$NoProxy,[string]$Network='bridge')
  # [2026-09-03 13:18:01] 作用：阻断空 Docker 网络名；理由依据：空值会让探针落到 Docker 默认网络并伪造商业网络通过结果。
  if([string]::IsNullOrWhiteSpace($Network)){throw '第二套出口代理探针 Docker 网络为空。'}
  # [2026-09-03 11:14:29] 作用：定义无凭据 Python HTTPS 探针；理由依据：显式 ProxyHandler 可区分代理通路与环境继承，并接受供应商 200/401/403。
  $probeScript=@'
# Import the standard HTTPS probe modules; the worker image already contains Python.
import os, urllib.error, urllib.request
# Read the read-only target and proxy supplied by the launcher.
target = os.environ["KM_EGRESS_PROBE_URL"]
proxy = os.environ["HTTPS_PROXY"]
# Build an explicit HTTP/HTTPS proxy handler.
handler = urllib.request.ProxyHandler({"http": proxy, "https": proxy})
# Build an opener that does not inherit a host-wide proxy.
opener = urllib.request.build_opener(handler)
# Create an unauthenticated read-only models request.
request = urllib.request.Request(target, headers={"User-Agent": "SQLRAG-233-egress-preflight"})
# Initialize the provider status.
status = 0
# Execute a bounded HTTPS request so an unreachable proxy fails before startup.
try:
    # Keep only the status code and never print a response body or secret.
    with opener.open(request, timeout=20) as response:
        status = response.status
# An authentication rejection still proves the network path.
except urllib.error.HTTPError as exc:
    status = exc.code
# Report the exception type without credentials and fail the probe.
except Exception as exc:
    print("PROXY_ERROR_TYPE=" + type(exc).__name__)
    print("PROXY_ERROR=" + str(exc)[:200])
    raise SystemExit(21)
# Emit only the provider HTTP status.
print("PROXY_HTTP_STATUS=" + str(status))
# Accept only success or authentication-rejection statuses.
if status not in (200, 401, 403):
    raise SystemExit(22)
'@
  # [2026-09-03 13:26:31] 作用：声明与实际 Worker 相同的 Docker 探针参数；理由依据：镜像、网络、代理和 NO_PROXY 必须作为一个不可拆分命令执行。
  $probeArguments=@('run','--rm','--interactive','--pull','never','--network',$Network,'--env',"KM_EGRESS_PROBE_URL=$ProbeUrl",'--env',"HTTP_PROXY=$ProxyUrl",'--env',"HTTPS_PROXY=$ProxyUrl",'--env','ALL_PROXY=','--env',"NO_PROXY=$NoProxy",'--entrypoint','python',$Image,'-')
  # [2026-09-03 13:26:32] 作用：通过显式 stdin 进程执行容器探针；理由依据：PowerShell 原生管道可能不传递多行脚本，必须保留真实输出和退出码。
  $probeExecution=Invoke-KmDockerPythonScript -Arguments $probeArguments -Script $probeScript
  # [2026-09-03 13:26:33] 作用：提取容器探针输出；理由依据：候选选择器需要同时读取供应商状态行和 Docker 诊断行。
  $probeOutput=@($probeExecution.Output)
  # [2026-09-03 13:26:34] 作用：保存容器探针原生退出码；理由依据：输出归一化或后续候选循环不能覆盖 Docker 失败事实。
  $probeExitCode=[int]$probeExecution.ExitCode
  # [2026-09-03 11:14:29] 作用：提取非密钥供应商状态；理由依据：代理选择只依赖明确状态码而不依赖任意文本。
  $statusLine=[string](@($probeOutput|Where-Object{[string]$_-match'^PROXY_HTTP_STATUS='}|Select-Object -Last 1)-join'')
  # [2026-09-03 11:14:29] 作用：规范化探针状态值；理由依据：返回对象需要稳定比较而不是依赖 PowerShell 数组类型。
  $probeStatus=if($statusLine-match'^PROXY_HTTP_STATUS=(\d+)$'){[int]$Matches[1]}else{0}
  # [2026-09-03 11:14:29] 作用：计算候选代理是否通过；理由依据：必须同时满足 Docker 退出码和供应商允许状态。
  $probePassed=($probeExitCode-eq0-and$probeStatus-in@(200,401,403))
  # [2026-09-03 11:14:29] 作用：返回候选探针结构化证据；理由依据：调用方需要继续尝试下一个候选并保留首个失败原因。
  return [pscustomobject]@{Passed=$probePassed;ExitCode=$probeExitCode;Status=$probeStatus;Output=@($probeOutput|Select-Object -Last 12)}
}

# [2026-09-01 17:23:10] 作用：把 IPv4 CIDR 转换为可比较的无符号起止地址；理由依据：第二套固定商业网段必须在任何容器变更前与 Windows 路由和全部 Docker 网络做精确重叠检查。
function ConvertTo-KmIpv4CidrRange {
  # [2026-09-01 17:23:10] 作用：接收待验证的 IPv4 CIDR 与证据标签；理由依据：失败信息必须指出来自 profile、Windows 路由还是 Docker 网络。
  param([Parameter(Mandatory=$true)][string]$Cidr,[Parameter(Mandatory=$true)][string]$Source)
  # [2026-09-01 17:23:10] 作用：规范化 CIDR 文本；理由依据：空格不得改变网段身份。
  $cidrText=$Cidr.Trim()
  # [2026-09-01 17:23:10] 作用：拆分地址和前缀长度；理由依据：非 CIDR 文本不能进入路由比较。
  if($cidrText-notmatch'^([^/]+)/([0-9]{1,2})$'){throw "IPv4 CIDR 格式无效：source=$Source value=$cidrText"}
  # [2026-09-01 17:23:10] 作用：解析 IPv4 地址对象；理由依据：正则只能分段，不能验证每个八位组范围。
  try{$ipAddress=[Net.IPAddress]::Parse($Matches[1])}catch{throw "IPv4 CIDR 地址无效：source=$Source value=$cidrText"}
  # [2026-09-01 17:23:10] 作用：拒绝 IPv6 或其他地址族；理由依据：当前 Windows、Docker 和 profile 合同只比较 IPv4。
  if($ipAddress.AddressFamily-ne[Net.Sockets.AddressFamily]::InterNetwork){throw "CIDR 不是 IPv4：source=$Source value=$cidrText"}
  # [2026-09-01 17:23:10] 作用：读取前缀长度；理由依据：后续块大小必须由结构化整数计算。
  $prefixLength=[int]$Matches[2]
  # [2026-09-01 17:23:10] 作用：限制 IPv4 前缀范围；理由依据：负数或超过 32 位会制造无效掩码。
  if($prefixLength-lt0-or$prefixLength-gt32){throw "IPv4 CIDR 前缀无效：source=$Source value=$cidrText"}
  # [2026-09-01 17:23:10] 作用：读取网络字节序地址；理由依据：避免依赖已弃用且受端序影响的 IPAddress.Address。
  $bytes=$ipAddress.GetAddressBytes()
  # [2026-09-01 17:23:10] 作用：把四个八位组转换为稳定无符号整数；理由依据：PowerShell 5.1 的有符号位移会在高位地址产生负数。
  $addressValue=([uint64]$bytes[0]*16777216)+([uint64]$bytes[1]*65536)+([uint64]$bytes[2]*256)+[uint64]$bytes[3]
  # [2026-09-01 17:23:10] 作用：计算当前前缀的地址块大小；理由依据：起止范围比较不依赖字符串前缀猜测。
  $blockSize=[uint64][Math]::Pow(2,32-$prefixLength)
  # [2026-09-01 17:23:10] 作用：计算规范网络起始值；理由依据：profile 必须写网络地址而不是任意宿主地址。
  $rangeStart=[uint64]([Math]::Floor($addressValue/[double]$blockSize)*[double]$blockSize)
  # [2026-09-01 17:23:10] 作用：计算规范网络结束值；理由依据：两个 CIDR 的闭区间相交即可证明重叠。
  $rangeEnd=[uint64]($rangeStart+$blockSize-1)
  # [2026-09-01 17:23:10] 作用：阻断非规范网络地址；理由依据：固定网段不能因宿主位非零产生歧义。
  if($addressValue-ne$rangeStart){throw "IPv4 CIDR 不是规范网络地址：source=$Source value=$cidrText"}
  # [2026-09-01 17:23:10] 作用：返回结构化 CIDR 范围；理由依据：Windows 路由与 Docker IPAM 使用同一比较模型。
  return [pscustomobject]@{Cidr=$cidrText;PrefixLength=$prefixLength;Start=$rangeStart;End=$rangeEnd;Source=$Source}
}

# [2026-09-01 17:23:10] 作用：判断两个 IPv4 CIDR 闭区间是否相交；理由依据：目标商业网段不得覆盖宿主或其他 Docker 网络的任何地址。
function Test-KmIpv4RangeOverlap {
  # [2026-09-01 17:23:10] 作用：接收两个已验证范围；理由依据：比较函数不再重新解析不可信文本。
  param([Parameter(Mandatory=$true)]$Left,[Parameter(Mandatory=$true)]$Right)
  # [2026-09-01 17:23:10] 作用：返回闭区间重叠结果；理由依据：边界地址相同也属于路由冲突。
  return ([uint64]$Left.Start-le[uint64]$Right.End-and[uint64]$Right.Start-le[uint64]$Left.End)
}

# [2026-09-02 10:18:30] 作用：定义第二套 PgBouncer 商业网络运行态验真；理由依据：固定网络已存在时，残留容器可能没有 endpoint，必须在 Compose create 前闭合该状态。
function Ensure-KmPgbouncerCommercialNetwork {
  # [2026-09-02 10:18:30] 作用：声明容器、网络、项目和是否强制存在参数；理由依据：同一 helper 同时服务 create 前探测和 create 后硬门禁。
  param([Parameter(Mandatory=$true)][string]$ContainerName,[Parameter(Mandatory=$true)][string]$NetworkName,[Parameter(Mandatory=$true)][string]$ExpectedProject,[Parameter(Mandatory=$true)][bool]$RequireNetwork)
  # [2026-09-02 10:18:30] 作用：按完整名称枚举既有 PgBouncer 容器；理由依据：停止容器也可能触发 Compose 重建，不能只看运行中列表。
  $containerNames=@(& docker.exe ps -a --filter "name=^$ContainerName$" --format '{{.Names}}' 2>$null)
  # [2026-09-02 10:18:30] 作用：保存容器枚举退出码；理由依据：Docker Engine 错误不能被空列表误判成首次安装。
  $containerListExitCode=$LASTEXITCODE
  # [2026-09-02 10:18:30] 作用：阻断容器枚举失败；理由依据：未知运行态下禁止对网络或容器做任何修复。
  if($containerListExitCode-ne0){throw "PgBouncer 容器枚举失败：container=$ContainerName exit=$containerListExitCode"}
  # [2026-09-02 10:18:30] 作用：允许 create 前跳过不存在的容器；理由依据：首次启动应由 Compose 创建容器而不是手工制造旁路对象。
  if($containerNames-notcontains$ContainerName){
    # [2026-09-02 10:18:30] 作用：在 create 后阻断缺失容器；理由依据：完成创建后必须有可验真的 PgBouncer 身份。
    if($RequireNetwork){throw "PgBouncer 容器在网络验真时不存在：container=$ContainerName"}
    # [2026-09-02 10:18:30] 作用：返回首次创建的明确空状态；理由依据：调用方需要区分首次安装和残留容器接线。
    return [pscustomobject]@{Present=$false;NetworkPresent=$false;Attached=$false;AliasReady=$false}
  }
  # [2026-09-02 10:18:30] 作用：读取既有 PgBouncer 完整 JSON；理由依据：网络和 Compose 标签必须来自 daemon 事实而不是名称猜测。
  $containerInspectText=(& docker.exe container inspect $ContainerName 2>$null|Out-String)
  # [2026-09-02 10:18:30] 作用：保存容器结构读取退出码；理由依据：后续 ConvertFrom-Json 不能覆盖 daemon 失败。
  $containerInspectExitCode=$LASTEXITCODE
  # [2026-09-02 10:18:30] 作用：阻断容器结构读取失败；理由依据：无法确认归属时不得接入任何网络。
  if($containerInspectExitCode-ne0){throw "PgBouncer 容器详情读取失败：container=$ContainerName exit=$containerInspectExitCode"}
  # [2026-09-02 10:41:12] 作用：解析 Docker 容器 JSON 数组的首个对象；理由依据：Windows PowerShell 5.1 对数组子表达式会再套一层，必须先取管道结果再索引才能读取 Labels。
  try{$containerDocument=($containerInspectText|ConvertFrom-Json)[0]}catch{throw "PgBouncer 容器详情不是合法 JSON：container=$ContainerName"}
  # [2026-09-02 10:18:30] 作用：读取容器标签集合；理由依据：同名容器不等于当前商业 Compose 项目所有权。
  $containerLabels=@{}
  # [2026-09-02 10:18:30] 作用：读取可选 Labels 属性；理由依据：旧 Docker 对空标签可能返回 null，StrictMode 下不能直接访问。
  $containerLabelsProperty=$containerDocument.Config.PSObject.Properties['Labels']
  # [2026-09-02 10:18:30] 作用：保存非空容器标签；理由依据：缺失标签必须在下一行以空值形式参与归属比较。
  if($null-ne$containerLabelsProperty-and$null-ne$containerLabelsProperty.Value){$containerLabels=$containerLabelsProperty.Value}
  # [2026-09-02 10:18:30] 作用：读取容器 Compose 项目标签；理由依据：只允许当前第二套商业项目修复自己的 PgBouncer。
  $containerProject=[string]$containerLabels.'com.docker.compose.project'
  # [2026-09-02 10:18:30] 作用：读取容器 Compose 服务标签；理由依据：前缀相同的其他服务不能被误接线。
  $containerService=[string]$containerLabels.'com.docker.compose.service'
  # [2026-09-02 10:18:30] 作用：阻断归属或服务标签漂移；理由依据：网络修复不应触碰第一套或未知项目容器。
  if($containerProject-ne$ExpectedProject-or$containerService-ne'km-pgbouncer'){throw "PgBouncer 容器归属不匹配：container=$ContainerName expected_project=$ExpectedProject actual_project=$containerProject service=$containerService"}
  # [2026-09-02 10:18:30] 作用：按完整名称查找商业网络；理由依据：网络不存在时应让 Compose 原子创建，而不是猜测网络 ID。
  $networkNames=@(& docker.exe network ls --filter "name=^$NetworkName$" --format '{{.Name}}' 2>$null)
  # [2026-09-02 10:18:30] 作用：保存商业网络枚举退出码；理由依据：引擎故障不能被首次网络创建分支吞掉。
  $networkListExitCode=$LASTEXITCODE
  # [2026-09-02 10:18:30] 作用：阻断商业网络枚举失败；理由依据：未知 endpoint 状态下不得连接或断开容器。
  if($networkListExitCode-ne0){throw "PgBouncer 商业网络枚举失败：network=$NetworkName exit=$networkListExitCode"}
  # [2026-09-02 10:18:30] 作用：允许 create 前等待 Compose 创建缺失网络；理由依据：首次部署不需要额外网络旁路。
  if($networkNames-notcontains$NetworkName){
    # [2026-09-02 10:18:30] 作用：在 create 后阻断仍缺失的商业网络；理由依据：容器无法在不存在的固定网络上安全启动。
    if($RequireNetwork){throw "PgBouncer 商业网络在 create 后不存在：network=$NetworkName"}
    # [2026-09-02 10:18:30] 作用：返回网络尚未创建的明确状态；理由依据：调用方可继续唯一的 Compose create 路径。
    return [pscustomobject]@{Present=$true;NetworkPresent=$false;Attached=$false;AliasReady=$false}
  }
  # [2026-09-02 10:18:30] 作用：读取商业网络完整 JSON；理由依据：网络标签和 endpoint 必须与容器侧状态交叉验证。
  $networkInspectText=(& docker.exe network inspect $NetworkName 2>$null|Out-String)
  # [2026-09-02 10:18:30] 作用：保存商业网络详情退出码；理由依据：JSON 解析成功不能覆盖 daemon 返回错误。
  $networkInspectExitCode=$LASTEXITCODE
  # [2026-09-02 10:18:30] 作用：阻断商业网络详情读取失败；理由依据：未知网络所有权时禁止修改 endpoint。
  if($networkInspectExitCode-ne0){throw "PgBouncer 商业网络详情读取失败：network=$NetworkName exit=$networkInspectExitCode"}
  # [2026-09-02 10:41:12] 作用：解析 Docker 商业网络 JSON 数组的首个对象；理由依据：PS5.1 必须避免数组子表达式嵌套，否则网络 Labels 与 Containers 会被误读为空。
  try{$networkDocument=($networkInspectText|ConvertFrom-Json)[0]}catch{throw "PgBouncer 商业网络详情不是合法 JSON：network=$NetworkName"}
  # [2026-09-02 10:18:30] 作用：读取网络标签集合；理由依据：同名 bridge 可能属于另一套项目，必须再次验证所有权。
  $networkLabels=@{}
  # [2026-09-02 10:18:30] 作用：读取可选网络 Labels 属性；理由依据：旧网络缺标签时应明确失败而不是默认放行。
  $networkLabelsProperty=$networkDocument.PSObject.Properties['Labels']
  # [2026-09-02 10:18:30] 作用：保存非空网络标签；理由依据：标签比较需要稳定的空值语义。
  if($null-ne$networkLabelsProperty-and$null-ne$networkLabelsProperty.Value){$networkLabels=$networkLabelsProperty.Value}
  # [2026-09-02 10:18:30] 作用：读取网络 Compose 项目标签；理由依据：固定 IPAM 只允许当前商业项目拥有。
  $networkProject=[string]$networkLabels.'com.docker.compose.project'
  # [2026-09-02 10:18:30] 作用：读取网络 Compose 逻辑名标签；理由依据：商业内部网络不能误认成其他逻辑网络。
  $networkLogicalName=[string]$networkLabels.'com.docker.compose.network'
  # [2026-09-02 10:18:30] 作用：阻断网络归属漂移；理由依据：同名网络被其他项目占用时自动接线会造成跨 profile 串线。
  if($networkProject-ne$ExpectedProject-or$networkLogicalName-ne'knowledge-commercial'){throw "PgBouncer 商业网络归属不匹配：network=$NetworkName expected_project=$ExpectedProject actual_project=$networkProject logical=$networkLogicalName"}
  # [2026-09-02 10:52:41] 作用：读取网络侧 Containers 可选属性；理由依据：停止容器接线时 Docker 网络可能暂时没有 active endpoint。
  $networkContainersProperty=$networkDocument.PSObject.Properties['Containers']
  # [2026-09-02 10:52:41] 作用：初始化网络侧 PgBouncer endpoint 属性；理由依据：缺失或空 Containers 必须形成确定的空状态。
  $networkEndpointProperty=$null
  # [2026-09-02 10:52:41] 作用：仅在网络确实有容器集合时查找 PgBouncer endpoint；理由依据：避免 PS5.1 对 null.PSObject 的访问异常。
  if($null-ne$networkContainersProperty-and$null-ne$networkContainersProperty.Value){$networkEndpointProperty=@($networkContainersProperty.Value.PSObject.Properties|Where-Object{[string]$_.Value.Name-eq$ContainerName}|Select-Object -First 1)}
  # [2026-09-02 10:58:07] 作用：判定网络是否真实持有 PgBouncer active endpoint；理由依据：PowerShell 空数组不是 null，必须用元素数量避免把空集合误判成 endpoint。
  $networkHasEndpoint=($networkEndpointProperty.Count-eq1)
  # [2026-09-02 10:18:30] 作用：读取容器 NetworkSettings 属性；理由依据：PowerShell 5.1 对缺失可选属性必须显式处理。
  $networkSettingsProperty=$containerDocument.PSObject.Properties['NetworkSettings']
  # [2026-09-02 10:18:30] 作用：初始化容器网络对象；理由依据：首次或异常 inspect 返回 null 时保持确定空状态。
  $containerNetworks=$null
  # [2026-09-02 10:18:30] 作用：保存容器网络集合；理由依据：后续精确检查当前商业网络键是否存在。
  if($null-ne$networkSettingsProperty-and$null-ne$networkSettingsProperty.Value){$containerNetworks=$networkSettingsProperty.Value.Networks}
  # [2026-09-02 10:18:30] 作用：读取容器侧商业网络属性；理由依据：必须与网络侧 endpoint 做双向一致性验证。
  $containerNetworkProperty=$null
  # [2026-09-02 10:18:30] 作用：在存在网络集合时查找当前商业网络；理由依据：避免 StrictMode 下直接索引 null。
  if($null-ne$containerNetworks){$containerNetworkProperty=$containerNetworks.PSObject.Properties[$NetworkName]}
  # [2026-09-02 10:52:41] 作用：判定容器侧是否登记商业网络；理由依据：Compose 重建前必须消除单侧残留状态。
  $containerHasNetwork=($null-ne$containerNetworkProperty)
  # [2026-09-02 10:52:41] 作用：读取容器侧网络别名集合；理由依据：停止容器没有 active endpoint 时仍可先验证其启动配置。
  $containerAliases=if($containerHasNetwork){@($containerNetworkProperty.Value.Aliases)}else{@()}
  # [2026-09-02 10:52:41] 作用：判定容器侧 km-pgbouncer 别名是否已写入；理由依据：Compose create 需要配置级 DNS 别名而不是仅网络名称。
  $containerAliasReady=($containerAliases-contains'km-pgbouncer')
  # [2026-09-02 10:52:41] 作用：读取容器当前状态；理由依据：运行中容器不允许被无提示断网重接。
  $containerState=[string]$containerDocument.State.Status
  # [2026-09-02 11:14:25] 作用：读取容器登记的 Docker 网络 ID；理由依据：网络按新 IPAM 重建后停止容器可能保留旧 ID，单看网络名称会漏掉失效连接。
  $containerNetworkId=if($containerHasNetwork){[string]$containerNetworkProperty.Value.NetworkID}else{''}
  # [2026-09-02 11:14:25] 作用：读取当前商业网络的 Docker 网络 ID；理由依据：必须与容器登记值比较才能识别同名网络重建造成的陈旧状态。
  $currentNetworkId=[string]$networkDocument.Id
  # [2026-09-02 11:14:25] 作用：判定停止容器是否仍指向旧网络；理由依据：只有两侧都有非空 ID 且不一致时才触发补接，避免对正常空 ID 停止配置反复抖动。
  $networkIdMismatch=($containerHasNetwork-and-not[string]::IsNullOrWhiteSpace($containerNetworkId)-and-not[string]::IsNullOrWhiteSpace($currentNetworkId)-and$containerNetworkId-ne$currentNetworkId)
  # [2026-09-02 11:14:25] 作用：读取容器登记的 endpoint ID；理由依据：异常停止态残留 endpoint 也必须在下一次启动前清理。
  $containerEndpointId=if($containerHasNetwork){[string]$containerNetworkProperty.Value.EndpointID}else{''}
  # [2026-09-02 11:14:25] 作用：判定停止态 endpoint 是否与网络事实脱节；理由依据：停止容器正常没有 active endpoint，非空残留则代表必须重接。
  $stoppedEndpointMismatch=($containerState-ne'running'-and-not$networkHasEndpoint-and-not[string]::IsNullOrWhiteSpace($containerEndpointId))
  # [2026-09-02 11:04:36] 作用：判断是否需要补接或重建 endpoint；理由依据：停止态以容器配置和别名为准，运行态再要求网络侧 active endpoint。
  $needsReconnect=(-not$containerHasNetwork-or-not$containerAliasReady-or$networkIdMismatch-or$stoppedEndpointMismatch-or($containerState-eq'running'-and-not$networkHasEndpoint))
  # [2026-09-02 11:04:36] 作用：阻断运行中容器的隐式网络抖动；理由依据：必须先由人工确认业务窗口再变更正在服务的网络。
  if($needsReconnect-and$containerState-eq'running'){throw "PgBouncer 运行中网络状态不一致，拒绝隐式断网：container=$ContainerName state=$containerState network=$NetworkName container_network=$containerHasNetwork container_alias=$containerAliasReady network_endpoint=$networkHasEndpoint"}
  # [2026-09-02 10:18:30] 作用：在停止残留容器上清理当前商业 endpoint；理由依据：重接 alias 前必须移除旧 endpoint，且不触碰卷或数据库。
  if($needsReconnect-and($containerHasNetwork-or$networkHasEndpoint)){
    & docker.exe network disconnect --force $NetworkName $ContainerName|Out-Host
    # [2026-09-02 10:18:30] 作用：保存旧 endpoint 断开退出码；理由依据：不能把断网失败吞掉后继续 create。
    $disconnectExitCode=$LASTEXITCODE
    # [2026-09-02 10:18:30] 作用：阻断旧 endpoint 断开失败；理由依据：半连接状态会再次触发 Docker active endpoint 或 not connected 错误。
    if($disconnectExitCode-ne0){throw "PgBouncer 旧商业 endpoint 断开失败：network=$NetworkName container=$ContainerName exit=$disconnectExitCode"}
  }
  # [2026-09-02 10:18:30] 作用：在缺失或不完整时接入商业网络并声明服务别名；理由依据：Compose create 前必须具备可解析的 km-pgbouncer endpoint。
  if($needsReconnect){
    # [2026-09-02 11:14:25] 作用：整理重接时需要保留的网络别名；理由依据：修复旧 NetworkID 不得丢失 Compose 已登记的容器名和服务别名。
    $reconnectAliases=@($containerAliases|Where-Object{-not[string]::IsNullOrWhiteSpace([string]$_)}|Select-Object -Unique)
    # [2026-09-02 11:14:25] 作用：确保重接集合包含 km-pgbouncer 服务别名；理由依据：Worker 和 API 的既有 DNS 合同必须始终可解析。
    if($reconnectAliases-notcontains'km-pgbouncer'){$reconnectAliases=@($reconnectAliases+'km-pgbouncer')}
    # [2026-09-02 11:14:25] 作用：对单一服务别名使用稳定的 Docker connect 调用；理由依据：保留原有简单路径并兼容 PowerShell 5.1。
    if($reconnectAliases.Count-eq1-and$reconnectAliases[0]-eq'km-pgbouncer'){
      # [2026-09-02 11:14:25] 作用：用 km-pgbouncer 别名接入商业网络；理由依据：这是首次残留补接和无其他别名容器的固定 DNS 入口。
      & docker.exe network connect --alias km-pgbouncer $NetworkName $ContainerName|Out-Host
    }else{
      # [2026-09-02 11:14:25] 作用：初始化保留别名的 Docker 参数；理由依据：Docker CLI 需要把每个 alias 作为独立参数传入。
      $networkConnectArguments=@('network','connect')
      # [2026-09-02 11:14:25] 作用：逐个加入原有网络别名；理由依据：容器名、Compose 服务名和 km-pgbouncer 解析行为必须保持不变。
      foreach($reconnectAlias in $reconnectAliases){$networkConnectArguments+=@('--alias',[string]$reconnectAlias)}
      # [2026-09-02 11:14:25] 作用：追加网络和容器身份；理由依据：参数顺序必须符合 Docker network connect 合同。
      $networkConnectArguments+=@($NetworkName,$ContainerName)
      # [2026-09-02 11:14:25] 作用：执行带完整别名集合的商业网络重接；理由依据：旧网络 ID 修复不能引入新的 DNS 回归。
      & docker.exe @networkConnectArguments|Out-Host
    }
    # [2026-09-02 10:18:30] 作用：保存新 endpoint 接入退出码；理由依据：接线失败时禁止继续启动连接池。
    $connectExitCode=$LASTEXITCODE
    # [2026-09-02 10:18:30] 作用：阻断商业 endpoint 接入失败；理由依据：错误必须停在部署层并保留明确容器和网络身份。
    if($connectExitCode-ne0){throw "PgBouncer 商业 endpoint 接入失败：network=$NetworkName container=$ContainerName exit=$connectExitCode"}
  }
  # [2026-09-02 10:18:30] 作用：重新读取接线后的网络对象；理由依据：docker network connect 的零退出码不能替代真实 endpoint 事实。
  $verifyNetworkText=(& docker.exe network inspect $NetworkName 2>$null|Out-String)
  # [2026-09-02 10:18:30] 作用：保存接线后网络读取退出码；理由依据：最终门禁必须能区分 daemon 失败和 JSON 失败。
  $verifyNetworkExitCode=$LASTEXITCODE
  # [2026-09-02 10:18:30] 作用：阻断接线后网络无法读取；理由依据：未知状态下不得让 Compose 继续重建。
  if($verifyNetworkExitCode-ne0){throw "PgBouncer 接线后商业网络回读失败：network=$NetworkName exit=$verifyNetworkExitCode"}
  # [2026-09-02 10:41:12] 作用：解析接线后 Docker 网络 JSON 数组的首个对象；理由依据：PS5.1 的嵌套数组会让最终 endpoint 验收永远看不到真实容器。
  try{$verifyNetworkDocument=($verifyNetworkText|ConvertFrom-Json)[0]}catch{throw "PgBouncer 接线后商业网络 JSON 无效：network=$NetworkName"}
  # [2026-09-02 10:52:41] 作用：读取接线后网络 Containers 可选属性；理由依据：停止容器补接成功后网络侧仍可能没有 active endpoint。
  $verifyNetworkContainersProperty=$verifyNetworkDocument.PSObject.Properties['Containers']
  # [2026-09-02 10:52:41] 作用：初始化接线后 PgBouncer endpoint 属性；理由依据：最终门禁必须区分停止态配置和运行态 endpoint。
  $verifyEndpointProperty=$null
  # [2026-09-02 10:52:41] 作用：仅在接线后网络有容器集合时查找 PgBouncer endpoint；理由依据：PS5.1 空集合不能被误当成一个 endpoint。
  if($null-ne$verifyNetworkContainersProperty-and$null-ne$verifyNetworkContainersProperty.Value){$verifyEndpointProperty=@($verifyNetworkContainersProperty.Value.PSObject.Properties|Where-Object{[string]$_.Value.Name-eq$ContainerName}|Select-Object -First 1)}
  # [2026-09-02 10:58:07] 作用：判定接线后网络是否持有 active endpoint；理由依据：PS5.1 空数组不是 null，必须按 endpoint 数量判断运行态事实。
  $verifyNetworkHasEndpoint=($verifyEndpointProperty.Count-eq1)
  # [2026-09-02 10:18:30] 作用：重新读取接线后容器网络集合；理由依据：网络侧存在 endpoint 仍不能证明容器侧状态同步。
  $verifyContainerText=(& docker.exe container inspect $ContainerName 2>$null|Out-String)
  # [2026-09-02 10:18:30] 作用：保存接线后容器读取退出码；理由依据：最终双向门禁不能依赖前一次快照。
  $verifyContainerExitCode=$LASTEXITCODE
  # [2026-09-02 10:18:30] 作用：阻断接线后容器无法回读；理由依据：Compose 重建前必须有可重复验证的容器网络事实。
  if($verifyContainerExitCode-ne0){throw "PgBouncer 接线后容器回读失败：container=$ContainerName exit=$verifyContainerExitCode"}
  # [2026-09-02 10:41:12] 作用：解析接线后 Docker 容器 JSON 数组的首个对象；理由依据：PS5.1 需要直接索引管道结果才能验证 NetworkSettings。
  try{$verifyContainerDocument=($verifyContainerText|ConvertFrom-Json)[0]}catch{throw "PgBouncer 接线后容器 JSON 无效：container=$ContainerName"}
  # [2026-09-02 10:52:41] 作用：读取接线后容器网络集合；理由依据：PowerShell 5.1 下显式处理可选属性。
  $verifyContainerNetworks=$verifyContainerDocument.NetworkSettings.Networks
  # [2026-09-02 10:52:41] 作用：读取接线后容器商业网络属性；理由依据：停止态配置必须与网络侧事实分开验收。
  $verifyContainerNetworkProperty=$null
  # [2026-09-02 10:52:41] 作用：仅在容器网络集合存在时查找商业网络；理由依据：避免对缺失 Networks 的容器直接索引。
  if($null-ne$verifyContainerNetworks){$verifyContainerNetworkProperty=$verifyContainerNetworks.PSObject.Properties[$NetworkName]}
  # [2026-09-02 10:52:41] 作用：判定接线后容器侧网络配置和别名；理由依据：Compose create 至少需要这两个配置级条件。
  $verifyContainerHasNetwork=($null-ne$verifyContainerNetworkProperty)
  # [2026-09-02 10:52:41] 作用：读取接线后容器别名集合；理由依据：停止容器的 DNS 合同保存在容器网络配置中。
  $verifyContainerAliases=if($verifyContainerHasNetwork){@($verifyContainerNetworkProperty.Value.Aliases)}else{@()}
  # [2026-09-02 11:04:36] 作用：判定接线后容器别名是否就绪；理由依据：缺别名时服务名解析仍会失败，别名事实只存在容器侧。
  $verifyContainerAliasReady=($verifyContainerAliases-contains'km-pgbouncer')
  # [2026-09-02 11:04:36] 作用：阻断接线后容器缺少商业网络或别名；理由依据：配置级缺口必须在 Compose 重建前停止。
  if(-not$verifyContainerHasNetwork-or-not$verifyContainerAliasReady){throw "PgBouncer 接线后容器缺少商业网络或别名：network=$NetworkName container=$ContainerName alias=km-pgbouncer"}
  # [2026-09-02 11:04:36] 作用：仅对运行中容器要求网络侧 active endpoint；理由依据：停止态 endpoint 由 Docker 在 start 时创建，不能提前误报。
  if($containerState-eq'running'-and-not$verifyNetworkHasEndpoint){throw "PgBouncer 运行态商业 endpoint 回读不完整：network=$NetworkName container=$ContainerName"}
  # [2026-09-02 11:04:36] 作用：返回当前网络配置与 active endpoint 状态；理由依据：调用方日志需要区分停止态补接和运行态闭环。
  return [pscustomobject]@{Present=$true;NetworkPresent=$true;Attached=$true;AliasReady=$verifyContainerAliasReady;ActiveEndpoint=$verifyNetworkHasEndpoint}
}

# [2026-08-29 18:32:00] 作用：识别第二套是否绕过Docker Desktop代理直连Linux Engine；理由依据：只有该路径不会自动把Windows盘符转换为Docker VM宿主盘路径。
$directLinuxEngine=($DeploymentProfile-eq'server_second_ports'-and[string]$env:DOCKER_HOST-eq'npipe:////./pipe/docker_engine_linux')
# [2026-08-29 18:32:01] 作用：把商业服务Windows bind源转换为已实测的Docker VM路径；理由依据：复用主启动器已通过init文件验证的宿主盘映射根，避免把D:\原样交给Linux daemon。
function Convert-ToKmDockerVmBindSource {
  param([Parameter(Mandatory=$true)][string]$WindowsPath)
  $resolvedWindowsPath=[IO.Path]::GetFullPath($WindowsPath)
  if(-not$directLinuxEngine){return $resolvedWindowsPath}
  $selectedInitPath=([string]$env:SQL_RAG_INIT_BIND_SOURCE).Trim().Replace('\','/')
  if([string]::IsNullOrWhiteSpace($selectedInitPath)-or-not$selectedInitPath.StartsWith('/')){throw '第二套商业挂载缺少已验证的SQL_RAG_INIT_BIND_SOURCE。'}
  $windowsInitPath=(Resolve-Path -LiteralPath (Join-Path $SqlRagRoot 'init') -ErrorAction Stop).Path
  # [2026-08-31 08:34:07] 作用：用双反斜杠表达盘符根正则；理由依据：PowerShell 正则末尾单反斜杠会触发 Illegal \ at end of pattern 并阻断九个商业挂载源转换。
  if($windowsInitPath-notmatch'^[A-Za-z]:\\'-or$resolvedWindowsPath-notmatch'^[A-Za-z]:\\'){throw "第二套商业挂载只支持已验证的Windows盘符路径：$resolvedWindowsPath"}
  if(-not[string]::Equals($windowsInitPath.Substring(0,1),$resolvedWindowsPath.Substring(0,1),[StringComparison]::OrdinalIgnoreCase)){throw "第二套商业挂载与已验证init不在同一宿主盘：init=$windowsInitPath bind=$resolvedWindowsPath"}
  $initRelative=$windowsInitPath.Substring(3).Replace('\','/')
  if(-not$selectedInitPath.EndsWith($initRelative,[StringComparison]::OrdinalIgnoreCase)){throw "第二套init Linux路径与Windows路径无法建立同源映射：windows=$windowsInitPath linux=$selectedInitPath"}
  $dockerVmDriveRoot=$selectedInitPath.Substring(0,$selectedInitPath.Length-$initRelative.Length).TrimEnd('/')
  $bindRelative=$resolvedWindowsPath.Substring(3).Replace('\','/')
  return "$dockerVmDriveRoot/$bindRelative"
}

# [2026-08-15 22:04:00] 作用：解析 Knowledge 根目录；理由依据：Compose 构建上下文只包含知识模块而不发送整个仓库。
$knowledgeRoot=(Resolve-Path -LiteralPath (Join-Path $SqlRagRoot 'Knowledge_management')).Path
# [2026-08-15 22:04:00] 作用：解析商业 Compose 文件；理由依据：所有工具服务逻辑统一位于用户指定 until 目录。
$composeFile=Join-Path $knowledgeRoot 'backend\large-scale_commercialization_upgrade\until\docker-compose.commercial.yml'
# [2026-08-15 22:04:00] 作用：阻断 Compose 缺失；理由依据：禁止只启动旧 API 形成进程内伪异步。
if(!(Test-Path -LiteralPath $composeFile -PathType Leaf)){throw "商业知识 Compose 不存在：$composeFile"}
# [2026-08-29 18:05:00] 作用：读取目标机实际落盘的商业 Compose；理由依据：V5D 可能遇到旧闭包覆盖新文件，必须以即将交给 Docker 的正文为准。
$composeRawBeforeNormalize=Get-Content -LiteralPath $composeFile -Raw -Encoding UTF8
# [2026-08-29 18:05:01] 作用：定义所有历史 Windows 短卷挂载形态；理由依据：Redis、RabbitMQ、环境文件、对象目录和观测配置都不能把盘符冒号传入 Linux volume parser。
$legacyCommercialBindPattern='(?mi)^(?:\s*-\s+|\s*volumes:\s+\[).*(?::/usr/local/etc/redis/redis\.conf:ro|:/etc/rabbitmq/rabbitmq\.conf:ro|:/etc/rabbitmq/enabled_plugins:ro|:/opt/km-rabbit/init_cluster\.sh:ro|:/workspace/app/SQL_RAG/\.env:ro|:/workspace/app/SQL_RAG/Knowledge_management/backend/public_program_files/runtime/\.env:ro|:/km-objects|:/etc/prometheus/prometheus\.yml:ro|:/etc/grafana/provisioning:ro)"?\s*$'
# [2026-08-29 18:05:02] 作用：判断是否需要就地规范化旧 Compose；理由依据：新版长语法重复写入会制造无意义备份和文件抖动。
$legacyCommercialRedisArrayPattern='(?mi)^\s*volumes:\s+\["[^"]*:/usr/local/etc/redis/redis\.conf:ro"?\s*,\s*"redis-[1-6]-data:/data"\]\s*$'
$composeNeedsNormalize=($composeRawBeforeNormalize -match $legacyCommercialBindPattern -or $composeRawBeforeNormalize -match $legacyCommercialRedisArrayPattern)
# [2026-08-29 18:05:03] 作用：以统一长语法替换 RabbitMQ 配置文件挂载；理由依据：相对路径由 Compose 文件目录解析，不受 D: 盘符影响。
$composeRawNormalized=[regex]::Replace($composeRawBeforeNormalize,'(?mi)^(\s*)-\s+[^\r\n]*:/etc/rabbitmq/rabbitmq\.conf:ro"?\s*$',{param($m) $i=$m.Groups[1].Value;($i+"- type: bind`r`n"+$i+'  source: ${KM_RABBITMQ_CONFIG_BIND_SOURCE:-./RabbitMQ/rabbitmq.conf}'+"`r`n"+$i+"  target: /etc/rabbitmq/rabbitmq.conf`r`n"+$i+'  read_only: true')})
# [2026-08-29 18:05:04] 作用：以统一长语法替换 RabbitMQ 插件挂载；理由依据：第一套和第二套必须共用同一可解析配置而不依赖宿主路径格式。
$composeRawNormalized=[regex]::Replace($composeRawNormalized,'(?mi)^(\s*)-\s+[^\r\n]*:/etc/rabbitmq/enabled_plugins:ro"?\s*$',{param($m) $i=$m.Groups[1].Value;($i+"- type: bind`r`n"+$i+'  source: ${KM_RABBITMQ_PLUGINS_BIND_SOURCE:-./RabbitMQ/enabled_plugins}'+"`r`n"+$i+"  target: /etc/rabbitmq/enabled_plugins`r`n"+$i+'  read_only: true')})
# [2026-08-29 18:05:05] 作用：以统一长语法替换 RabbitMQ 初始化脚本挂载；理由依据：集群初始化不得因 Windows 绝对路径在 Linux Engine 端被误判。
$composeRawNormalized=[regex]::Replace($composeRawNormalized,'(?mi)^(\s*)-\s+[^\r\n]*:/opt/km-rabbit/init_cluster\.sh:ro"?\s*$',{param($m) $i=$m.Groups[1].Value;($i+"- type: bind`r`n"+$i+'  source: ${KM_RABBITMQ_INIT_BIND_SOURCE:-./RabbitMQ/init_cluster.sh}'+"`r`n"+$i+"  target: /opt/km-rabbit/init_cluster.sh`r`n"+$i+'  read_only: true')})
# [2026-08-29 18:05:06] 作用：把六个 Redis 节点的一行数组卷改成结构化长语法；理由依据：截图中的失败正是 redis.conf 短语法被 Docker daemon 拒绝。
$composeRawNormalized=[regex]::Replace($composeRawNormalized,'(?mi)^(\s*)volumes:\s+\["[^"]*:/usr/local/etc/redis/redis\.conf:ro",\s*"redis-(?<node>[1-6])-data:/data"\]\s*$',{param($m) $i=$m.Groups[1].Value;$n=$m.Groups['node'].Value;($i+"volumes:`r`n"+$i+"  - type: bind`r`n"+$i+'    source: ${KM_REDIS_CONFIG_BIND_SOURCE:-./Redis/redis.conf}'+"`r`n"+$i+"    target: /usr/local/etc/redis/redis.conf`r`n"+$i+"    read_only: true`r`n"+$i+"  - redis-$n-data:/data")})
# [2026-08-29 18:05:06] 作用：把 Redis 多行列表中的旧宿主 bind 改成结构化长语法；理由依据：兼容目标机旧 Compose 的数组和多行两种历史形态。
$composeRawNormalized=[regex]::Replace($composeRawNormalized,'(?mi)^(\s*)-\s+[^\r\n]*:/usr/local/etc/redis/redis\.conf:ro"?\s*$',{param($m) $i=$m.Groups[1].Value;($i+"- type: bind`r`n"+$i+'  source: ${KM_REDIS_CONFIG_BIND_SOURCE:-./Redis/redis.conf}'+"`r`n"+$i+"  target: /usr/local/etc/redis/redis.conf`r`n"+$i+'  read_only: true')})
# [2026-08-29 18:05:07] 作用：把 SQL_RAG 环境文件改成结构化长语法；理由依据：env 文件绝对路径同样可能带 Windows 盘符。
$composeRawNormalized=[regex]::Replace($composeRawNormalized,'(?m)^(\s*)-\s+[^\r\n]*:/workspace/app/SQL_RAG/\.env:ro"?\s*$',{param($m) $i=$m.Groups[1].Value;($i+"- type: bind`r`n"+$i+'  source: ${KM_SQL_RAG_ENV_BIND_SOURCE:?KM_SQL_RAG_ENV_BIND_SOURCE is required}'+"`r`n"+$i+"  target: /workspace/app/SQL_RAG/.env`r`n"+$i+'  read_only: true')})
# [2026-08-29 18:05:08] 作用：把 Knowledge 环境文件改成结构化长语法；理由依据：Worker 启动必须读取第二套自己的配置而不能在挂载解析阶段失败。
$composeRawNormalized=[regex]::Replace($composeRawNormalized,'(?m)^(\s*)-\s+[^\r\n]*:/workspace/app/SQL_RAG/Knowledge_management/backend/public_program_files/runtime/\.env:ro"?\s*$',{param($m) $i=$m.Groups[1].Value;($i+"- type: bind`r`n"+$i+'  source: ${KM_KNOWLEDGE_ENV_BIND_SOURCE:?KM_KNOWLEDGE_ENV_BIND_SOURCE is required}'+"`r`n"+$i+"  target: /workspace/app/SQL_RAG/Knowledge_management/backend/public_program_files/runtime/.env`r`n"+$i+'  read_only: true')})
# [2026-08-29 18:05:09] 作用：把对象目录改成结构化长语法；理由依据：第二套对象 spool 必须独立挂载且不能把 D: 盘符拼入短字符串。
$composeRawNormalized=[regex]::Replace($composeRawNormalized,'(?m)^(\s*)-\s+[^\r\n]*:/km-objects"?\s*$',{param($m) $i=$m.Groups[1].Value;($i+"- type: bind`r`n"+$i+'  source: ${KM_OBJECT_BIND_SOURCE:?KM_OBJECT_BIND_SOURCE is required}'+"`r`n"+$i+'  target: /km-objects')})
# [2026-08-29 18:05:10] 作用：把 Prometheus 配置改成结构化长语法；理由依据：观测服务也必须与 Redis/RabbitMQ 使用同一 Windows 兼容挂载合同。
$composeRawNormalized=[regex]::Replace($composeRawNormalized,'(?mi)^(\s*)-\s+[^\r\n]*:/etc/prometheus/prometheus\.yml:ro"?\s*$',{param($m) $i=$m.Groups[1].Value;($i+"- type: bind`r`n"+$i+'  source: ${KM_PROMETHEUS_CONFIG_BIND_SOURCE:-./Observability/prometheus.yml}'+"`r`n"+$i+"  target: /etc/prometheus/prometheus.yml`r`n"+$i+'  read_only: true')})
# [2026-08-29 18:05:11] 作用：把 Grafana provisioning 目录改成结构化长语法；理由依据：最后一个宿主目录挂载也不得留在旧短语法中。
$composeRawNormalized=[regex]::Replace($composeRawNormalized,'(?mi)^(\s*)-\s+[^\r\n]*:/etc/grafana/provisioning:ro"?\s*$',{param($m) $i=$m.Groups[1].Value;($i+"- type: bind`r`n"+$i+'  source: ${KM_GRAFANA_PROVISIONING_BIND_SOURCE:-./Observability/grafana-provisioning}'+"`r`n"+$i+"  target: /etc/grafana/provisioning`r`n"+$i+'  read_only: true')})
# [2026-08-29 18:05:12] 作用：仅在旧语法真实存在时备份并落盘规范化 Compose；理由依据：保留目标机可恢复证据且不触碰任何数据库或 Docker volume。
$normalizeBackup=$null
if($composeNeedsNormalize-and$composeRawNormalized-ne$composeRawBeforeNormalize){$normalizeBackup="$composeFile.before-long-volume-normalize-$(Get-Date -Format 'yyyyMMdd-HHmmss').yml";Copy-Item -LiteralPath $composeFile -Destination $normalizeBackup -Force;[IO.File]::WriteAllText($composeFile,$composeRawNormalized,(New-Object Text.UTF8Encoding($false)))}
# [2026-08-29 18:05:15] 作用：输出就地规范化证据；理由依据：目标日志必须证明旧 Compose 已在 config/up 前被替换。
if($null-ne$normalizeBackup){Write-Host "KNOWLEDGE_COMMERCIAL_COMPOSE_NORMALIZED backup=$normalizeBackup"}
# [2026-08-29 18:05:13] 作用：重新读取规范化后的 Compose 正文；理由依据：后续 config/up 必须消费刚校验过的磁盘内容。
$composeRawAfterNormalize=Get-Content -LiteralPath $composeFile -Raw -Encoding UTF8
# [2026-08-29 18:05:14] 作用：阻断残留短卷语法；理由依据：任何未替换的宿主 bind 都会把失败推迟到容器创建阶段。
if($composeRawAfterNormalize-match$legacyCommercialBindPattern){throw "商业知识 Compose 仍残留 Windows 短卷挂载语法：$composeFile"}
# [2026-08-29 18:05:16] 作用：输出最终 Compose 格式和哈希证据；理由依据：无论本轮是否触发自愈，都必须证明 Docker config/up 消费的是已验证正文。
$composeVerifiedHash=(Get-FileHash -LiteralPath $composeFile -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "KNOWLEDGE_COMMERCIAL_COMPOSE_FORMAT_OK sha256=$composeVerifiedHash"
# [2026-08-15 22:04:00] 作用：解析 SQL_RAG 私密运行配置；理由依据：Worker 继续复用原模型和业务数据库配置且不复制密钥到镜像。
$sqlRagEnv=Join-Path $SqlRagRoot '.env'
# [2026-08-15 22:04:00] 作用：阻断运行配置缺失；理由依据：无模型和数据库密钥时不能启动消费 Worker。
if(!(Test-Path -LiteralPath $sqlRagEnv -PathType Leaf)){throw "SQL_RAG 运行配置不存在：$sqlRagEnv"}
# [2026-08-15 18:22:00] 作用：解析 Knowledge 原业务运行配置；理由依据：Worker 容器继续消费已验收的模型、ASR 和 PostgreSQL 参数但镜像不得内嵌密钥。
$knowledgeEnv=Join-Path $knowledgeRoot 'backend\public_program_files\runtime\.env'
# [2026-08-15 18:22:00] 作用：阻断 Knowledge 运行配置缺失；理由依据：无原业务模型和数据库参数时不能启动空壳 Worker。
if(!(Test-Path -LiteralPath $knowledgeEnv -PathType Leaf)){throw "Knowledge 运行配置不存在：$knowledgeEnv"}
# [2026-08-15 22:04:00] 作用：创建 profile 专属运行目录；理由依据：对象、密钥和启动证据不进入源码或系统临时目录。
$runtimeRoot=Join-Path $knowledgeRoot ("runtime\commercial\"+$DeploymentProfile)
# [2026-08-15 22:04:00] 作用：确保运行目录存在；理由依据：第一次一键启动无需人工创建基础目录。
New-Item -ItemType Directory -Path $runtimeRoot -Force|Out-Null
# [2026-08-15 22:04:00] 作用：创建 profile 专属对象 spool；理由依据：上传分块跨请求、进程和整机重启保持稳定。
$objectRoot=Join-Path $runtimeRoot 'objects'
# [2026-08-15 22:04:00] 作用：确保对象目录存在；理由依据：API 与 Worker 挂载同一受控位置。
New-Item -ItemType Directory -Path $objectRoot -Force|Out-Null
# [2026-08-29 18:32:02] 作用：集中声明商业服务九个唯一宿主挂载源；理由依据：46个实际挂载必须一次覆盖Redis、RabbitMQ、环境、对象和观测配置而不是逐个遇错再补。
$commercialUntilRoot=Split-Path -Parent $composeFile
$commercialWindowsBindSources=[ordered]@{
  KM_RABBITMQ_CONFIG_BIND_SOURCE=(Join-Path $commercialUntilRoot 'RabbitMQ\rabbitmq.conf')
  KM_RABBITMQ_PLUGINS_BIND_SOURCE=(Join-Path $commercialUntilRoot 'RabbitMQ\enabled_plugins')
  KM_RABBITMQ_INIT_BIND_SOURCE=(Join-Path $commercialUntilRoot 'RabbitMQ\init_cluster.sh')
  KM_REDIS_CONFIG_BIND_SOURCE=(Join-Path $commercialUntilRoot 'Redis\redis.conf')
  KM_SQL_RAG_ENV_BIND_SOURCE=$sqlRagEnv
  KM_KNOWLEDGE_ENV_BIND_SOURCE=$knowledgeEnv
  KM_OBJECT_BIND_SOURCE=$objectRoot
  KM_PROMETHEUS_CONFIG_BIND_SOURCE=(Join-Path $commercialUntilRoot 'Observability\prometheus.yml')
  KM_GRAFANA_PROVISIONING_BIND_SOURCE=(Join-Path $commercialUntilRoot 'Observability\grafana-provisioning')
}
# [2026-08-29 18:32:03] 作用：在任何Docker调用前一次检查九个Windows源；理由依据：本地缺文件与Linux路径格式问题必须被分开诊断。
$missingCommercialWindowsSources=@($commercialWindowsBindSources.GetEnumerator()|Where-Object{-not(Test-Path -LiteralPath ([string]$_.Value))}|ForEach-Object{"$($_.Key)=$($_.Value)"})
if($missingCommercialWindowsSources.Count-gt0){throw "商业知识Windows挂载源缺失：$($missingCommercialWindowsSources-join'; ')"}
# [2026-08-29 18:32:04] 作用：为当前Docker端点生成九个实际bind源；理由依据：第一套保留Windows路径并由Desktop代理转换，第二套改用同盘已实测Docker VM路径。
$commercialDockerBindSources=[ordered]@{}
foreach($bindEntry in $commercialWindowsBindSources.GetEnumerator()){$commercialDockerBindSources[[string]$bindEntry.Key]=Convert-ToKmDockerVmBindSource -WindowsPath ([string]$bindEntry.Value)}
# [2026-08-29 18:32:05] 作用：输出两套路径策略分流证据；理由依据：必须能从日志直接证明第二套未再把D:\路径交给Linux daemon且第一套行为未改。
Write-Host "KNOWLEDGE_COMMERCIAL_BIND_MODE mode=$(if($directLinuxEngine){'docker_vm_host_path'}else{'desktop_proxy_windows_path'}) unique_sources=$($commercialDockerBindSources.Count)"
# [2026-08-15 22:04:00] 作用：定位持久密钥文件；理由依据：每次重启复用凭据且不同 profile 不共享。
$secretPath=Join-Path $runtimeRoot 'commercial-secrets.json'
# [2026-08-15 22:04:00] 作用：读取既有密钥或生成新密钥；理由依据：容器重建不造成 Broker、Redis 和对象存储认证漂移。
if(Test-Path -LiteralPath $secretPath -PathType Leaf){$secrets=Get-Content -LiteralPath $secretPath -Raw -Encoding UTF8|ConvertFrom-Json}else{$secrets=[ordered]@{rabbit_user='km_app';rabbit_password=(New-KmSecret);rabbit_cookie=(New-KmSecret);redis_password=(New-KmSecret);cache_token=(New-KmSecret);minio_user='kmminio';minio_password=(New-KmSecret);flower_user='kmops';flower_password=(New-KmSecret);grafana_user='kmops';grafana_password=(New-KmSecret)};$secrets|ConvertTo-Json -Depth 4|Set-Content -LiteralPath $secretPath -Encoding UTF8}
# [2026-08-15 22:04:00] 作用：约束密钥文件 ACL；理由依据：其他本机普通账户不得读取商业服务凭据。
& icacls.exe $secretPath /inheritance:r /grant:r "${env:USERNAME}:(R,W)" *> $null
# [2026-08-21 09:00:49] 作用：读取上传进度网关、全景独立缓存及全部商业工具端口；理由依据：全景缓存必须拥有独立 profile 端口且不能复用消息队列加速层。
$cachePort=Get-KmPort 'knowledge_cache_gateway';$panoramaCachePort=Get-KmPort 'knowledge_panorama_cache';$minioApiPort=Get-KmPort 'knowledge_minio_api';$minioConsolePort=Get-KmPort 'knowledge_minio_console';$tusdPort=Get-KmPort 'knowledge_tusd';$rabbitAmqpPort=Get-KmPort 'knowledge_rabbitmq_amqp';$rabbitManagementPort=Get-KmPort 'knowledge_rabbitmq_management';$flowerPort=Get-KmPort 'knowledge_flower';$prometheusPort=Get-KmPort 'knowledge_prometheus';$grafanaPort=Get-KmPort 'knowledge_grafana';$pgbouncerPort=Get-KmPort 'knowledge_pgbouncer'
# [2026-08-15 22:04:00] 作用：把宿主回环数据库地址映射为 Docker Host Gateway；理由依据：Linux Worker 内的 127.0.0.1 指向自身而不是当前 profile PostgreSQL。
$containerDatabaseUrl=$KnowledgeDatabaseUrl -replace '@(?:127\.0\.0\.1|localhost):','@host.docker.internal:'
# [2026-08-17 08:45:11] 作用：结构化解析 Knowledge PostgreSQL URL；理由依据：PgBouncer 上游主机、端口、库名和认证不允许用字符串拼接猜测。
try{$knowledgeDatabaseUri=[uri]$KnowledgeDatabaseUrl}catch{throw 'Knowledge DATABASE_URL 无法用于 PgBouncer 结构化解析。'}
# [2026-08-17 08:45:11] 作用：分离 URL 编码的用户和密码；理由依据：PgBouncer userlist 需要原始凭据而 Worker URL 继续保留编码安全边界。
$databaseUserInfo=@($knowledgeDatabaseUri.UserInfo-split':',2)
# [2026-08-17 08:45:11] 作用：要求 PostgreSQL URL 同时含用户和密码；理由依据：生产连接池禁止 trust 认证。
if($databaseUserInfo.Count-ne2){throw 'Knowledge DATABASE_URL 缺少 PgBouncer 所需的用户或密码。'}
# [2026-08-17 08:45:11] 作用：解码 PostgreSQL 应用用户；理由依据：最小权限账户在 userlist 和上游连接中必须完全一致。
$pgbouncerDatabaseUser=[uri]::UnescapeDataString($databaseUserInfo[0])
# [2026-08-17 08:45:11] 作用：解码 PostgreSQL 应用密码；理由依据：特殊字符不得被当作 URL 分隔符传给 userlist。
$pgbouncerDatabasePassword=[uri]::UnescapeDataString($databaseUserInfo[1])
# [2026-08-17 08:45:11] 作用：解析不带斜杠的业务库名；理由依据：PgBouncer databases 映射与 SQL 健康探针必须命中同一库。
$pgbouncerDatabaseName=$knowledgeDatabaseUri.AbsolutePath.Trim('/')
# [2026-08-17 08:45:11] 作用：阻断空数据库名；理由依据：禁止 PgBouncer 回落到同名用户库。
if([string]::IsNullOrWhiteSpace($pgbouncerDatabaseName)){throw 'Knowledge DATABASE_URL 缺少数据库名。'}
# [2026-08-31 17:58:58] 作用：识别当前数据库是否为本 profile 的宿主回环恢复库；理由依据：目标机已实证容器访问 host.docker.internal:25434 无路由，而数据库容器自身健康。
$pgbouncerUsesProfileMigratedPostgres=($knowledgeDatabaseUri.Host-in@('127.0.0.1','localhost'))
# [2026-08-31 17:58:59] 作用：按当前 profile 容器前缀声明迁移 PostgreSQL 身份；理由依据：两套必须直连各自容器且不能使用第一套名称。
$migratedPostgresContainer="$ContainerNamePrefix-migrated-source-postgres"
# [2026-08-31 17:59:00] 作用：读取当前 profile 已由共享引擎固定的迁移 Compose 项目；理由依据：PgBouncer 只能加入该项目自己的 default 私有网络。
$migratedPostgresProject=([string]$env:SQL_RAG_MIGRATED_PG_PROJECT).Trim()
# [2026-08-31 17:59:01] 作用：阻断回环数据库缺少独立 Compose 身份；理由依据：禁止重新回退到不可达的宿主网关或猜测另一套网络。
if($pgbouncerUsesProfileMigratedPostgres-and[string]::IsNullOrWhiteSpace($migratedPostgresProject)){throw '当前 profile 缺少迁移 PostgreSQL Compose 项目合同。'}
# [2026-08-31 17:59:02] 作用：推导当前 profile 迁移 PostgreSQL 的 Compose 私有网络；理由依据：同一项目 default 网络提供容器 DNS 和内部 5432 且不暴露数据库。
$migratedPostgresNetwork=if($pgbouncerUsesProfileMigratedPostgres){"$migratedPostgresProject`_default"}else{''}
# [2026-08-31 17:59:03] 作用：回环数据库改用本 profile 容器 DNS，非回环数据库保留原主机；理由依据：移除第二套 Docker Linux Engine 到 Windows 回环端口的错误绕行。
$pgbouncerUpstreamHost=if($pgbouncerUsesProfileMigratedPostgres){$migratedPostgresContainer}else{$knowledgeDatabaseUri.Host}
# [2026-08-31 17:59:04] 作用：容器直连使用 PostgreSQL 内部 5432，外部数据库保留 URL 端口；理由依据：25434 和 5432 分别属于宿主发布合同与容器私网合同。
$pgbouncerUpstreamPort=if($pgbouncerUsesProfileMigratedPostgres){5432}else{$knowledgeDatabaseUri.Port}
# [2026-08-17 08:45:11] 作用：构造 Worker 容器内 PgBouncer SQLAlchemy URL；理由依据：所有 Celery 队列进程统一经事务池访问 PostgreSQL。
$pgbouncerContainerDatabaseUrl="$($knowledgeDatabaseUri.Scheme)://$($knowledgeDatabaseUri.UserInfo)@km-pgbouncer:6432$($knowledgeDatabaseUri.AbsolutePath)$($knowledgeDatabaseUri.Query)"
# [2026-08-17 08:45:11] 作用：构造不含凭据的宿主 PgBouncer 公开合同；理由依据：运维输出可定位服务 URL 但不泄露密码。
$pgbouncerPublicContract="postgresql://127.0.0.1:$pgbouncerPort/$pgbouncerDatabaseName"
# [2026-08-15 22:04:00] 作用：URL 编码 RabbitMQ 用户；理由依据：随机凭据进入 AMQP URL 时不得破坏解析。
$rabbitUserEncoded=[uri]::EscapeDataString([string]$secrets.rabbit_user)
# [2026-08-15 22:04:00] 作用：URL 编码 RabbitMQ 密码；理由依据：特殊字符不改变认证字段边界。
$rabbitPasswordEncoded=[uri]::EscapeDataString([string]$secrets.rabbit_password)
# [2026-08-15 22:04:00] 作用：声明 profile 专属 RabbitMQ vhost；理由依据：第一套第二套即使误连同一节点也不会共享队列。
$rabbitVhost=('knowledge-'+($DeploymentProfile-replace'[^a-z0-9-]','-')).ToLowerInvariant()
# [2026-08-15 22:04:00] 作用：构造容器内 RabbitMQ Broker URL；理由依据：Celery 只连接三节点集群入口且不使用 Redis Broker。
$brokerUrl="amqp://$rabbitUserEncoded`:$rabbitPasswordEncoded@km-rabbit-1:5672/$rabbitVhost"
# [2026-08-17 15:43:14] 作用：构造宿主 Knowledge API 可访问的 RabbitMQ 控制面 URL；理由依据：运行中硬暂停需要从 Windows API 精确 revoke Linux Celery 子任务，不能使用容器内部 DNS 名。
$hostBrokerUrl="amqp://$rabbitUserEncoded`:$rabbitPasswordEncoded@127.0.0.1:$rabbitAmqpPort/$rabbitVhost"
# [2026-08-15 22:04:00] 作用：URL 编码 Redis 密码；理由依据：短期 Result Backend URL 保持合法。
$redisPasswordEncoded=[uri]::EscapeDataString([string]$secrets.redis_password)
# [2026-08-15 22:04:00] 作用：构造 Celery 专用短期结果 URL；理由依据：完整业务结果只写 PostgreSQL/MinIO，Redis 仅保留六小时诊断。
$resultBackend="redis://:$redisPasswordEncoded@km-celery-result:6379/0"
# [2026-08-15 22:04:00] 作用：生成 MinIO Bucket 名；理由依据：S3 命名规范和 profile 隔离同时满足。
$minioBucket=('knowledge-'+($DeploymentProfile-replace'[^a-z0-9-]','-')).Trim('-').ToLowerInvariant()
# [2026-08-15 22:04:00] 作用：声明商业 Compose 项目；理由依据：卷生命周期与原数据库 Compose 分离且随 profile 归属。
$commercialProject="$ComposeProjectName-km-commercial"
# [2026-08-15 22:04:00] 作用：声明商业内部网络；理由依据：Redis/RabbitMQ/MinIO 原生端口不暴露给业务局域网。
$commercialNetwork="$ContainerNamePrefix-km-commercial-internal"
# [2026-09-01 17:23:10] 作用：建立复用同一基础 Compose 的参数列表；理由依据：第一套保持原单文件调用，只有显式配置固定网段的第二套才追加隔离 override。
$composeCommandArguments=New-Object 'System.Collections.Generic.List[string]'
# [2026-09-01 17:23:10] 作用：加入 Compose 子命令、当前项目和原商业文件；理由依据：服务、镜像、卷和业务环境继续复用第一套成熟定义。
foreach($argument in @('compose','--project-name',$commercialProject,'-f',$composeFile)){[void]$composeCommandArguments.Add([string]$argument)}
# [2026-09-01 17:23:10] 作用：初始化商业网络重建标志；理由依据：匹配固定 IPAM 时重复一键启动不得中断现有容器。
$commercialNetworkRequiresRecreate=$false
# [2026-09-01 17:23:10] 作用：初始化 profile 的可选固定商业网络属性；理由依据：第一套旧 profile 没有 docker 对象时不得访问空对象或改变启动行为。
$commercialNetworkContractProperty=$null
# [2026-09-01 17:23:10] 作用：仅在 profile 明确包含 docker 对象时读取商业网络属性；理由依据：第二套持有固定 IPAM，第一套继续沿用原 Compose 自动分配。
if($null-ne$ServicePortProfile.PSObject.Properties['docker']-and$null-ne$ServicePortProfile.docker){$commercialNetworkContractProperty=$ServicePortProfile.docker.PSObject.Properties['commercial_network']}
# [2026-09-01 17:23:10] 作用：标记本 profile 是否启用固定 IPAM；理由依据：第二套修复不能扩散为第一套网络迁移。
$commercialNetworkUsesFixedIpam=($null-ne$commercialNetworkContractProperty)
# [2026-09-01 17:23:10] 作用：仅对显式固定 IPAM 的 profile 执行路由验真和 override 构造；理由依据：第一套继续走其已验收的原 Compose 路径。
if($commercialNetworkUsesFixedIpam){
  # [2026-09-01 17:23:10] 作用：读取第二套固定子网；理由依据：Docker 不再自动挑选与目标宿主虚拟网卡重叠的 172.20.0.0/16。
  $commercialSubnet=([string]$commercialNetworkContractProperty.Value.subnet).Trim()
  # [2026-09-01 17:23:10] 作用：读取第二套固定网关；理由依据：Compose IPAM 必须由同一 profile 原子声明子网和网关。
  $commercialGateway=([string]$commercialNetworkContractProperty.Value.gateway).Trim()
  # [2026-09-01 17:23:10] 作用：解析并规范固定商业子网；理由依据：无效或非网络地址必须在任何 Docker 状态变化前失败。
  $commercialSubnetRange=ConvertTo-KmIpv4CidrRange -Cidr $commercialSubnet -Source 'profile.docker.commercial_network.subnet'
  # [2026-09-01 17:23:10] 作用：把固定网关解析为单地址范围；理由依据：网关字符串也必须通过 IPv4 结构验证。
  $commercialGatewayRange=ConvertTo-KmIpv4CidrRange -Cidr "$commercialGateway/32" -Source 'profile.docker.commercial_network.gateway'
  # [2026-09-01 17:23:10] 作用：要求网关位于子网可用宿主区间；理由依据：网络地址和广播地址不能作为 Docker bridge 网关。
  if($commercialGatewayRange.Start-le$commercialSubnetRange.Start-or$commercialGatewayRange.Start-ge$commercialSubnetRange.End){throw "商业知识固定网关不在可用子网内：subnet=$commercialSubnet gateway=$commercialGateway"}
  # [2026-09-01 17:23:10] 作用：收集与候选子网冲突的 Windows 活跃路由；理由依据：目标机 172.20.192.1 已证明宿主路由重叠会让容器外网请求错误命中本地链路。
  $windowsRouteConflicts=New-Object 'System.Collections.Generic.List[string]'
  # [2026-09-01 17:23:10] 作用：逐条检查非默认 IPv4 活跃路由；理由依据：默认路由承载正常外网出口，不应被视为覆盖全部候选私网。
  foreach($windowsRoute in @(Get-NetRoute -AddressFamily IPv4 -State Alive -ErrorAction Stop)){
    # [2026-09-01 17:23:10] 作用：规范当前 Windows 目标前缀；理由依据：路由对象可能包含空白文本。
    $windowsRouteCidr=([string]$windowsRoute.DestinationPrefix).Trim()
    # [2026-09-01 17:23:10] 作用：跳过空前缀和唯一默认路由；理由依据：只有更具体的宿主路由才会与 Docker 私网争用。
    if([string]::IsNullOrWhiteSpace($windowsRouteCidr)-or$windowsRouteCidr-eq'0.0.0.0/0'){continue}
    # [2026-09-01 17:23:10] 作用：解析当前 Windows 路由范围；理由依据：候选网段必须与操作系统真实路由表比较。
    $windowsRouteRange=ConvertTo-KmIpv4CidrRange -Cidr $windowsRouteCidr -Source "windows_route:$([string]$windowsRoute.InterfaceAlias)"
    # [2026-09-01 17:23:10] 作用：记录任一 Windows 路由重叠；理由依据：不能再次把容器 No route to host 留到业务解析阶段。
    if(Test-KmIpv4RangeOverlap -Left $commercialSubnetRange -Right $windowsRouteRange){[void]$windowsRouteConflicts.Add("$windowsRouteCidr@$([string]$windowsRoute.InterfaceAlias)")}
  }
  # [2026-09-01 17:23:10] 作用：阻断与 Windows 路由重叠的固定网段；理由依据：发生冲突时不得停容器、移除网络或继续构建。
  if($windowsRouteConflicts.Count-gt0){throw "商业知识固定网段与 Windows 路由重叠：subnet=$commercialSubnet conflicts=$($windowsRouteConflicts-join',')"}
  # [2026-09-01 17:23:10] 作用：枚举当前 Engine 全部 Docker 网络名；理由依据：第二套不能抢占数据库、Qdrant 或其他项目已经使用的私网。
  $dockerNetworkNames=@(& docker.exe network ls --format '{{.Name}}')
  # [2026-09-01 17:23:10] 作用：阻断 Docker 网络枚举失败；理由依据：缺少完整冲突事实时不能修改现有商业网络。
  if($LASTEXITCODE-ne0){throw "商业知识固定网段无法枚举 Docker 网络，exit=$LASTEXITCODE"}
  # [2026-09-01 17:23:10] 作用：初始化 Docker 网络文档集合；理由依据：无自定义网络的新环境也应继续生成固定 override。
  $dockerNetworkDocuments=@()
  # [2026-09-02 14:41:08] 作用：一次读取全部现有 Docker 网络 JSON；理由依据：IPAM、标签和端点所有权必须来自 daemon 当前事实且退出码需在解析前保存。
  if($dockerNetworkNames.Count-gt0){$dockerNetworkInspectText=((& docker.exe network inspect @dockerNetworkNames)|Out-String)}
  # [2026-09-02 14:41:08] 作用：保存 Docker 网络详情读取退出码；理由依据：ConvertFrom-Json 不得掩盖 daemon 失败。
  $dockerNetworkInspectExitCode=if($dockerNetworkNames.Count-gt0){$LASTEXITCODE}else{0}
  # [2026-09-02 14:41:08] 作用：阻断 Docker 网络详情读取失败；理由依据：不能以空集合误判候选网段安全。
  if($dockerNetworkInspectExitCode-ne0){throw "商业知识固定网段无法检查 Docker IPAM，exit=$dockerNetworkInspectExitCode"}
  # [2026-09-02 14:41:08] 作用：在 PowerShell 5.1 中逐项展开 network inspect 的 JSON 数组；理由依据：直接再套 @() 会把全部网络包成单个 System.Object[] 并导致商业网络永远匹配不到。
  if($dockerNetworkNames.Count-gt0){try{$dockerNetworkDocuments=@(($dockerNetworkInspectText|ConvertFrom-Json)|ForEach-Object{$_})}catch{throw '商业知识 Docker 网络详情不是合法 JSON。'}}
  # [2026-09-01 17:23:10] 作用：初始化当前商业网络文档；理由依据：首次创建与旧冲突网络迁移需要分开处理。
  $currentCommercialNetworkDocument=$null
  # [2026-09-01 17:23:10] 作用：收集其他 Docker 网络与候选子网的冲突；理由依据：只允许当前商业网络在受控重建前暂时使用不同 IPAM。
  $dockerNetworkConflicts=New-Object 'System.Collections.Generic.List[string]'
  # [2026-09-01 17:23:10] 作用：逐网络比较全部 IPv4 IPAM 配置；理由依据：Docker 网络可以声明多个子网，不能只检查第一项。
  foreach($dockerNetworkDocument in $dockerNetworkDocuments){
    # [2026-09-01 17:23:10] 作用：读取当前 Docker 网络名；理由依据：冲突和所有权诊断必须指向唯一对象。
    $dockerNetworkName=[string]$dockerNetworkDocument.Name
    # [2026-09-01 17:23:10] 作用：保存当前 profile 商业网络并排除其旧 IPAM 冲突；理由依据：该网络将在验证归属后由本项目自己重建。
    if([string]::Equals($dockerNetworkName,$commercialNetwork,[StringComparison]::OrdinalIgnoreCase)){$currentCommercialNetworkDocument=$dockerNetworkDocument;continue}
    # [2026-09-01 17:23:10] 作用：遍历当前网络所有 IPv4 子网；理由依据：host、none 或仅 IPv6 网络不参与当前冲突比较。
    foreach($dockerIpamConfig in @($dockerNetworkDocument.IPAM.Config|Where-Object{-not[string]::IsNullOrWhiteSpace([string]$_.Subnet)-and([string]$_.Subnet)-notmatch':'})){
      # [2026-09-01 17:23:10] 作用：解析其他 Docker 子网；理由依据：比较必须使用同一 CIDR 算法而不是字符串首段。
      $dockerSubnetRange=ConvertTo-KmIpv4CidrRange -Cidr ([string]$dockerIpamConfig.Subnet) -Source "docker_network:$dockerNetworkName"
      # [2026-09-01 17:23:10] 作用：记录候选与其他 Docker 网络的任何交叠；理由依据：容器间错误路由会破坏独立项目故障域。
      if(Test-KmIpv4RangeOverlap -Left $commercialSubnetRange -Right $dockerSubnetRange){[void]$dockerNetworkConflicts.Add("$dockerNetworkName=$([string]$dockerIpamConfig.Subnet)")}
    }
  }
  # [2026-09-01 17:23:10] 作用：阻断候选子网与其他 Docker 网络冲突；理由依据：不得通过删除或改写不属于第二套商业项目的网络解决冲突。
  if($dockerNetworkConflicts.Count-gt0){throw "商业知识固定网段与其他 Docker 网络重叠：subnet=$commercialSubnet conflicts=$($dockerNetworkConflicts-join',')"}
  # [2026-09-01 17:23:10] 作用：检查既有商业网络是否已经精确采用固定子网和网关；理由依据：通过时重复启动不重建 33 个容器。
  if($null-ne$currentCommercialNetworkDocument){
    # [2026-09-01 17:23:10] 作用：读取既有商业网络 IPv4 IPAM 集合；理由依据：多余子网也属于合同漂移。
    $currentCommercialIpv4Configs=@($currentCommercialNetworkDocument.IPAM.Config|Where-Object{-not[string]::IsNullOrWhiteSpace([string]$_.Subnet)-and([string]$_.Subnet)-notmatch':'})
    # [2026-09-01 17:23:10] 作用：判断既有商业网络是否精确匹配 profile；理由依据：子网或网关任一不同都需要一次受控重建。
    $commercialNetworkMatches=($currentCommercialIpv4Configs.Count-eq1-and[string]$currentCommercialIpv4Configs[0].Subnet-eq$commercialSubnet-and[string]$currentCommercialIpv4Configs[0].Gateway-eq$commercialGateway)
    # [2026-09-01 17:23:10] 作用：仅对漂移的既有商业网络验证归属并计划重建；理由依据：不能移除同名但不属于当前 Compose 项目的网络。
    if(-not$commercialNetworkMatches){
      # [2026-09-01 17:23:10] 作用：读取既有网络的 Compose 项目标签；理由依据：同名不足以证明生命周期所有权。
      $currentNetworkProject=[string]$currentCommercialNetworkDocument.Labels.'com.docker.compose.project'
      # [2026-09-01 17:23:10] 作用：读取既有网络的 Compose 逻辑键标签；理由依据：必须精确对应 knowledge-commercial。
      $currentNetworkLogicalName=[string]$currentCommercialNetworkDocument.Labels.'com.docker.compose.network'
      # [2026-09-01 17:23:10] 作用：枚举既有网络全部容器名称；理由依据：任何非当前前缀端点都会阻断自动移除。
      $currentNetworkContainerNames=@($currentCommercialNetworkDocument.Containers.PSObject.Properties|ForEach-Object{[string]$_.Value.Name})
      # [2026-09-01 18:25:18] 作用：找出既非当前商业容器也非当前迁移 PostgreSQL 的网络端点；理由依据：历史错误可能把本 profile 数据库接入商业网络，修复只能断开该网络而不能删除数据库容器。
      $foreignCommercialNetworkContainers=@($currentNetworkContainerNames|Where-Object{-not$_.StartsWith("$ContainerNamePrefix-km-",[StringComparison]::OrdinalIgnoreCase)-and-not($pgbouncerUsesProfileMigratedPostgres-and[string]::Equals($_,$migratedPostgresContainer,[StringComparison]::OrdinalIgnoreCase))})
      # [2026-09-01 17:23:10] 作用：阻断标签或端点所有权不一致；理由依据：只有当前第二套商业 Compose 网络可由一键入口重建。
      if($currentNetworkProject-ne$commercialProject-or$currentNetworkLogicalName-ne'knowledge-commercial'-or$foreignCommercialNetworkContainers.Count-gt0){throw "商业知识既有网络不属于当前 profile，禁止重建：name=$commercialNetwork project=$currentNetworkProject logical=$currentNetworkLogicalName foreign=$($foreignCommercialNetworkContainers-join',')"}
      # [2026-09-01 17:23:10] 作用：标记在镜像预检通过后重建旧商业网络；理由依据：最大限度缩短第二套停机时间且不删除任何命名卷。
      $commercialNetworkRequiresRecreate=$true
    }
  }
  # [2026-09-01 17:23:10] 作用：定位不含密钥的 profile 专属 Compose 网络 override；理由依据：第一套基础 YAML 和业务服务定义保持逐字不变。
  $commercialNetworkOverridePath=Join-Path $runtimeRoot 'docker-compose.network.override.yml'
  # [2026-09-01 17:23:10] 作用：生成只覆盖 knowledge-commercial IPAM 的 YAML；理由依据：修复范围不得触碰服务、镜像、卷、环境或业务命令。
  $commercialNetworkOverrideText=@('networks:','  knowledge-commercial:','    ipam:','      config:',"        - subnet: $commercialSubnet","          gateway: $commercialGateway")-join"`r`n"
  # [2026-09-01 17:23:10] 作用：以 UTF-8 无 BOM 原子语义写入当前 profile 运行目录；理由依据：override 不进入第一套路径且不包含任何凭据。
  [IO.File]::WriteAllText($commercialNetworkOverridePath,$commercialNetworkOverrideText+"`r`n",(New-Object Text.UTF8Encoding($false)))
  # [2026-09-01 17:23:10] 作用：把第二套网络 override 加入所有后续 Compose 调用；理由依据：config、build、create、up、ps 和 down 必须消费同一 IPAM 合同。
  foreach($argument in @('-f',$commercialNetworkOverridePath)){[void]$composeCommandArguments.Add([string]$argument)}
  # [2026-09-01 17:23:10] 作用：输出第二套固定网段预检证据；理由依据：目标日志必须区分安全复用和待重建状态。
  Write-Host "KNOWLEDGE_COMMERCIAL_NETWORK_PREFLIGHT_READY subnet=$commercialSubnet gateway=$commercialGateway recreate=$commercialNetworkRequiresRecreate windows_conflicts=0 docker_conflicts=0"
}
# [2026-08-21 09:00:49] 作用：建立包含全景独立缓存端口的 Compose 原子合同；理由依据：容器、健康门禁和宿主 API 必须消费同一 profile 事实源。
$composeEnvironment=[ordered]@{KM_RABBITMQ_ERLANG_COOKIE=[string]$secrets.rabbit_cookie;KM_RABBITMQ_USER=[string]$secrets.rabbit_user;KM_RABBITMQ_PASSWORD=[string]$secrets.rabbit_password;KM_RABBITMQ_VHOST=$rabbitVhost;KM_REDIS_PASSWORD=[string]$secrets.redis_password;KM_MINIO_ROOT_USER=[string]$secrets.minio_user;KM_MINIO_ROOT_PASSWORD=[string]$secrets.minio_password;KM_KNOWLEDGE_ROOT=$knowledgeRoot;KM_SQL_RAG_ENV_FILE=$sqlRagEnv;KM_KNOWLEDGE_ENV_FILE=$knowledgeEnv;KM_CONTAINER_DATABASE_URL=$containerDatabaseUrl;KM_PGBOUNCER_DATABASE_URL=$pgbouncerContainerDatabaseUrl;KM_PG_HOST=$pgbouncerUpstreamHost;KM_PG_PORT="$pgbouncerUpstreamPort";KM_PG_DATABASE=$pgbouncerDatabaseName;KM_PG_USER=$pgbouncerDatabaseUser;KM_PG_PASSWORD=$pgbouncerDatabasePassword;KM_PGBOUNCER_PORT="$pgbouncerPort";SQL_RAG_DEPLOYMENT_PROFILE=$DeploymentProfile;KM_CELERY_BROKER_URL=$brokerUrl;KM_CELERY_RESULT_BACKEND=$resultBackend;KM_CACHE_GATEWAY_TOKEN=[string]$secrets.cache_token;KM_OBJECT_ROOT=$objectRoot;KM_MINIO_BUCKET=$minioBucket;KM_RABBITMQ_AMQP_PORT="$rabbitAmqpPort";KM_RABBITMQ_MANAGEMENT_PORT="$rabbitManagementPort";KM_CACHE_GATEWAY_PORT="$cachePort";KM_PANORAMA_CACHE_PORT="$panoramaCachePort";KM_MINIO_API_PORT="$minioApiPort";KM_MINIO_CONSOLE_PORT="$minioConsolePort";KM_TUSD_PORT="$tusdPort";KM_FLOWER_PORT="$flowerPort";KM_FLOWER_USER=[string]$secrets.flower_user;KM_FLOWER_PASSWORD=[string]$secrets.flower_password;KM_PROMETHEUS_PORT="$prometheusPort";KM_GRAFANA_PORT="$grafanaPort";KM_GRAFANA_USER=[string]$secrets.grafana_user;KM_GRAFANA_PASSWORD=[string]$secrets.grafana_password;KM_COMMERCIAL_NETWORK=$commercialNetwork;KM_CONTAINER_PREFIX=$ContainerNamePrefix}
# [2026-08-29 18:32:06] 作用：把九个已按端点转换的bind源加入同一Compose环境合同；理由依据：业务路径变量继续保留Windows值，只有daemon挂载源使用Docker VM路径。
foreach($bindEntry in $commercialDockerBindSources.GetEnumerator()){$composeEnvironment[[string]$bindEntry.Key]=[string]$bindEntry.Value}
# [2026-08-15 22:04:00] 作用：向当前进程注入 Compose 合同；理由依据：docker compose 插值与后续 Knowledge API 使用同一已验证值。
foreach($entry in $composeEnvironment.GetEnumerator()){[Environment]::SetEnvironmentVariable([string]$entry.Key,[string]$entry.Value,'Process')}
# [2026-08-31 14:43:17] 作用：默认两套商业服务都走同一源码按需构建路径；理由依据：第二套只是无VPN且具有互联网，不得因profile身份被硬编码成永久离线。
$commercialRuntimeMode='source_build'
# [2026-08-31 14:43:17] 作用：读取目标profile显式声明的商业运行模式；理由依据：真正断网时仍可人工切换到随包镜像导入兜底，日常第二套必须与第一套同构建逻辑。
if($null-ne$ServicePortProfile-and$null-ne$ServicePortProfile.PSObject.Properties['commercial_runtime_mode']-and-not[string]::IsNullOrWhiteSpace([string]$ServicePortProfile.commercial_runtime_mode)){$commercialRuntimeMode=([string]$ServicePortProfile.commercial_runtime_mode).Trim().ToLowerInvariant()}
# [2026-08-31 14:43:17] 作用：限制商业运行模式为源码构建或离线导入两种确定分支；理由依据：禁止未知值静默回落并形成源码、镜像和运行状态漂移。
if($commercialRuntimeMode-notin@('source_build','offline_import')){throw "商业运行模式不受支持：$commercialRuntimeMode"}
# [2026-08-31 14:43:17] 作用：仅在profile明确要求时启用离线资产导入；理由依据：无VPN不等于无互联网，server_second_ports本身不再触发离线锁死。
$offlineAssetImport=($commercialRuntimeMode-eq'offline_import')
# [2026-08-31 14:43:17] 作用：输出不含密钥的商业运行模式证据；理由依据：现场日志必须能直接证明第二套实际走源码构建还是离线兜底。
Write-Host "KNOWLEDGE_COMMERCIAL_RUNTIME_MODE mode=$commercialRuntimeMode profile=$DeploymentProfile vpn_required=false"
# [2026-08-17 15:23:16] 作用：定位商业离线镜像加载器；理由依据：显式离线兜底启动前必须从随包归档恢复十个精确镜像。
$offlineAssetLoader=Join-Path $knowledgeRoot 'backend\large-scale_commercialization_upgrade\until\Offline_deployment\Initialize-KnowledgeCommercialOfflineAssets.ps1'
# [2026-08-31 14:43:17] 作用：只在显式离线模式阻断加载器缺失；理由依据：源码构建模式不依赖离线归档，断网兜底仍须闭环验真。
if($offlineAssetImport-and-not(Test-Path -LiteralPath $offlineAssetLoader -PathType Leaf)){throw "商业离线镜像加载器缺失：$offlineAssetLoader"}
# [2026-08-31 14:43:17] 作用：仅为显式离线模式导入并验明随包镜像；理由依据：第二套可联网正式路径必须直接消费当前源码并按需构建。
if($offlineAssetImport){& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $offlineAssetLoader|Out-Host}
# [2026-08-31 14:43:17] 作用：阻断显式离线镜像导入失败；理由依据：离线兜底不能在缺镜像时隐式切换到联网构建。
if($offlineAssetImport-and$LASTEXITCODE-ne0){throw "商业离线镜像导入失败，exit=$LASTEXITCODE"}
# [2026-08-29 18:32:07] 作用：由直连Linux daemon一次实测九个商业挂载源；理由依据：Compose文本展开成功不能证明Docker VM实际可读Redis、RabbitMQ、环境文件、对象目录和观测配置。
if($directLinuxEngine){
  $uniqueDirectBindSources=@($commercialDockerBindSources.Values|Sort-Object -Unique)
  $bindProbeArguments=New-Object 'System.Collections.Generic.List[string]'
  foreach($argument in @('run','--pull','never','--rm')){[void]$bindProbeArguments.Add($argument)}
  $bindProbeTests=New-Object 'System.Collections.Generic.List[string]'
  for($bindIndex=0;$bindIndex-lt$uniqueDirectBindSources.Count;$bindIndex++){$probeTarget="/km-bind-probe-$bindIndex";[void]$bindProbeArguments.Add('--mount');[void]$bindProbeArguments.Add("type=bind,source=$($uniqueDirectBindSources[$bindIndex]),target=$probeTarget,readonly");[void]$bindProbeTests.Add("test -r '$probeTarget'")}
  foreach($argument in @('--entrypoint','/bin/sh','redis:8.0.1-bookworm','-ec',($bindProbeTests-join' && '))){[void]$bindProbeArguments.Add($argument)}
  & docker.exe @bindProbeArguments|Out-Host
  $bindProbeExitCode=$LASTEXITCODE
  if($bindProbeExitCode-ne0){throw "第二套直连Engine商业挂载总探针失败：exit=$bindProbeExitCode sources=$($uniqueDirectBindSources.Count)；data_destructive_actions=0"}
  Write-Host "KNOWLEDGE_COMMERCIAL_DIRECT_ENGINE_BINDS_READY unique_sources=$($uniqueDirectBindSources.Count) readonly=true"
}
# [2026-09-01 17:23:10] 作用：用当前 profile 的完整文件列表验证 Compose 展开结果；理由依据：第二套固定网络 override 必须与第一套成熟基础 Compose 同时通过且不能在创建容器后才暴露错误。
& docker.exe @composeCommandArguments config --quiet|Out-Host
# [2026-08-15 22:04:00] 作用：阻断 Compose 合同失败；理由依据：固定入口不能继续启动旧同步 API。
if($LASTEXITCODE-ne0){throw "商业知识 Compose 配置验证失败，exit=$LASTEXITCODE"}
# [2026-09-01 17:23:10] 作用：用当前 profile 的完整文件列表读取展开 Compose 结构；理由依据：容器、挂载、卷和固定 IPAM 必须来自 Docker 将实际消费的同一配置。
$expandedComposeJson=(& docker.exe @composeCommandArguments config --format json|Out-String)
# [2026-08-29 17:35:01] 作用：阻断 Compose 结构化展开失败；理由依据：无法展开时不得对第二套 Docker 状态产生部分写入。
if($LASTEXITCODE-ne0){throw "商业知识 Compose 结构化预检失败，exit=$LASTEXITCODE"}
# [2026-08-29 17:35:02] 作用：解析展开后的服务、网络和卷事实；理由依据：隔离合同必须依据 Docker 将实际消费的配置而不是源 YAML 猜测。
$expandedCompose=$expandedComposeJson|ConvertFrom-Json
# [2026-08-29 17:35:03] 作用：枚举第二套商业服务；理由依据：每个容器都必须归属于当前 profile 专属前缀。
$expandedServices=@($expandedCompose.services.PSObject.Properties)
# [2026-08-29 17:35:04] 作用：找出空名称或越过第二套容器前缀的服务；理由依据：禁止任何商业组件复用第一套容器身份。
$unexpectedContainerNames=@($expandedServices|ForEach-Object{[string]$_.Value.container_name}|Where-Object{[string]::IsNullOrWhiteSpace($_)-or-not$_.StartsWith("$ContainerNamePrefix-",[StringComparison]::OrdinalIgnoreCase)})
# [2026-08-29 17:35:05] 作用：阻断第二套容器身份串线；理由依据：关闭任一后台时不得停止或依赖另一套同名容器。
if($unexpectedContainerNames.Count-gt0){throw "商业知识容器身份未独立：$($unexpectedContainerNames -join ', ')"}
# [2026-08-29 17:35:06] 作用：读取实际商业内部网络名称；理由依据：同逻辑两后台必须拥有不同网络故障域。
$expandedCommercialNetwork=[string]$expandedCompose.networks.'knowledge-commercial'.name
# [2026-08-29 17:35:07] 作用：阻断网络复用或漂移；理由依据：Redis、RabbitMQ、MinIO、Worker 只能在当前第二套内部网络通信。
if(-not[string]::Equals($expandedCommercialNetwork,$commercialNetwork,[StringComparison]::OrdinalIgnoreCase)){throw "商业知识内部网络未独立：actual=$expandedCommercialNetwork expected=$commercialNetwork"}
# [2026-09-01 17:23:10] 作用：仅对固定 IPAM profile 回读完全展开的网络配置；理由依据：写出 override 不等于 Docker Compose 实际消费了目标子网和网关。
if($commercialNetworkUsesFixedIpam){
  # [2026-09-01 17:23:10] 作用：读取展开后的商业网络 IPAM 项；理由依据：第二套合同只允许一个精确 IPv4 子网。
  $expandedCommercialIpamConfigs=@($expandedCompose.networks.'knowledge-commercial'.ipam.config)
  # [2026-09-01 17:23:10] 作用：阻断展开后的子网数量、地址或网关漂移；理由依据：自动分配 172.20.0.0/16 正是本次 58% 超时根因。
  if($expandedCommercialIpamConfigs.Count-ne1-or[string]$expandedCommercialIpamConfigs[0].subnet-ne$commercialSubnet-or[string]$expandedCommercialIpamConfigs[0].gateway-ne$commercialGateway){throw "商业知识固定 IPAM 展开失败：expected=$commercialSubnet/$commercialGateway actual=$($expandedCommercialIpamConfigs|ConvertTo-Json -Compress)"}
}
# [2026-08-29 17:35:08] 作用：枚举 Compose 展开后的全部命名卷；理由依据：缓存、队列、对象和监控数据必须由第二套项目名隔离。
$expandedVolumeNames=@($expandedCompose.volumes.PSObject.Properties|ForEach-Object{[string]$_.Value.name})
# [2026-08-29 17:35:09] 作用：找出未归属于当前商业 Compose 项目的命名卷；理由依据：第二套不得读取或销毁第一套持久卷。
$unexpectedVolumeNames=@($expandedVolumeNames|Where-Object{[string]::IsNullOrWhiteSpace($_)-or-not$_.StartsWith("$commercialProject`_",[StringComparison]::OrdinalIgnoreCase)})
# [2026-08-29 17:35:10] 作用：阻断命名卷跨后台复用；理由依据：停止或重建任一后台不能影响另一套数据平面。
if($unexpectedVolumeNames.Count-gt0){throw "商业知识命名卷未独立：$($unexpectedVolumeNames -join ', ')"}
# [2026-08-29 17:35:11] 作用：收集所有展开后的宿主机bind源；理由依据：RabbitMQ、Redis、环境文件、对象目录和观测配置必须在up前一次查全。
$expandedBindSources=@()
# [2026-08-29 17:35:12] 作用：逐服务检查结构化挂载；理由依据：只处理 type=bind，命名卷由独立项目名前缀门禁负责。
# [2026-08-31 09:38:00] 作用：只读取实际声明了 volumes 属性的 Compose 服务；理由依据：config --format json 会省略无挂载服务的可选属性，StrictMode 下直接访问会触发 PropertyNotFoundStrict 并阻断第二套启动。
foreach($serviceProperty in $expandedServices){
  $serviceVolumesProperty=$serviceProperty.Value.PSObject.Properties['volumes']
  if($null -eq $serviceVolumesProperty){continue}
  foreach($volume in @($serviceVolumesProperty.Value)){
    if($null-ne$volume-and[string]$volume.type-eq'bind'){$expandedBindSources+=[string]$volume.source}
  }
}
# [2026-08-29 17:35:13] 作用：规范化展开后的唯一bind源；理由依据：46个挂载会复用九个文件或目录，比较唯一集合可精确发现遗漏和额外路径。
$expandedUniqueBindSources=@($expandedBindSources|Sort-Object -Unique)
# [2026-08-29 18:32:08] 作用：直连Engine时禁止任何Windows盘符并要求九个Docker VM源完整命中；理由依据：这正是第一套Desktop代理与第二套Linux daemon之间的关键差异。
if($directLinuxEngine){
  $unexpectedWindowsBindSources=@($expandedUniqueBindSources|Where-Object{$_-match'^[A-Za-z]:[\\/]'})
  $expectedDirectBindSources=@($commercialDockerBindSources.Values|Sort-Object -Unique)
  $directBindDifference=@(Compare-Object -ReferenceObject $expectedDirectBindSources -DifferenceObject $expandedUniqueBindSources)
  if($unexpectedWindowsBindSources.Count-gt0-or$expectedDirectBindSources.Count-ne9-or$directBindDifference.Count-gt0){throw "第二套直连Engine商业挂载合同失败：windows=$($unexpectedWindowsBindSources-join'; ') expected=$($expectedDirectBindSources.Count) actual=$($expandedUniqueBindSources.Count) diff=$($directBindDifference|ForEach-Object{"$($_.SideIndicator)$($_.InputObject)"}-join'; ')"}
}else{
  # [2026-08-29 17:35:14] 作用：Desktop代理模式按Windows文件系统一次性报告全部缺失源；理由依据：第一套继续使用原宿主路径合同且不得受第二套转换变量污染。
  $missingBindSources=@($expandedUniqueBindSources|Where-Object{[string]::IsNullOrWhiteSpace($_)-or-not(Test-Path -LiteralPath $_)})
  if($missingBindSources.Count-gt0){throw "商业知识宿主挂载源缺失：$($missingBindSources -join '; ')"}
}
# [2026-08-31 14:43:17] 作用：读取商业镜像清单；理由依据：源码构建和离线兜底都必须保持相同十镜像服务闭包。
$commercialImageManifestPath=Join-Path $knowledgeRoot 'backend\large-scale_commercialization_upgrade\until\Offline_deployment\commercial-images.manifest.json'
# [2026-08-29 17:35:16] 作用：取得十个精确镜像名称；理由依据：Compose 不能暗中引入未随包验证的软件服务。
$expectedCommercialImages=@((Get-Content -LiteralPath $commercialImageManifestPath -Raw -Encoding UTF8|ConvertFrom-Json).images|ForEach-Object{[string]$_.image}|Sort-Object -Unique)
# [2026-09-01 17:23:10] 作用：用当前 profile 的完整 Compose 文件列表读取全部镜像；理由依据：固定网络 override 不得改变 Redis、RabbitMQ、MinIO、Worker、PgBouncer 和监控的既有闭包。
$composeCommercialImageOutput=@(& docker.exe @composeCommandArguments config --images)
# [2026-08-29 17:35:18] 作用：阻断镜像清单展开失败；理由依据：不能把未知软件依赖留到正式创建阶段。
if($LASTEXITCODE-ne0){throw "商业知识镜像闭包预检失败，exit=$LASTEXITCODE"}
# [2026-08-29 17:35:19] 作用：规范化实际十镜像集合；理由依据：多服务复用同一 Worker 或 Redis 镜像时只比较唯一身份。
$composeCommercialImages=@($composeCommercialImageOutput|ForEach-Object{([string]$_).Trim()}|Where-Object{-not[string]::IsNullOrWhiteSpace($_)}|Sort-Object -Unique)
# [2026-08-29 17:35:20] 作用：比较随包镜像清单与 Compose 完整依赖；理由依据：任何遗漏或额外镜像都必须在创建容器前一次报清。
$commercialImageClosureDiff=@(Compare-Object -ReferenceObject $expectedCommercialImages -DifferenceObject $composeCommercialImages)
# [2026-08-31 14:43:17] 作用：阻断商业镜像闭包漂移；理由依据：两套只能在运行身份、端口和数据故障域上不同，服务及镜像集合必须一致。
if($expectedCommercialImages.Count-ne10-or$composeCommercialImages.Count-ne10-or$commercialImageClosureDiff.Count-gt0){throw "商业知识十镜像闭包不一致：expected=$($expectedCommercialImages.Count) actual=$($composeCommercialImages.Count) diff=$($commercialImageClosureDiff|ForEach-Object{"$($_.SideIndicator)$($_.InputObject)"}-join'; ')"}
# [2026-08-29 17:35:22] 作用：输出第二套商业启动前总闭包标记；理由依据：日志必须证明容器、网络、卷、挂载和十镜像均已独立完整后才允许 up。
Write-Host "KNOWLEDGE_COMMERCIAL_PRESTART_CLOSURE_READY services=$($expandedServices.Count) images=$($composeCommercialImages.Count) bind_mounts=$(@($expandedBindSources).Count) volumes=$($expandedVolumeNames.Count) network=$expandedCommercialNetwork"
# [2026-08-31 17:59:05] 作用：显式离线兜底跳过现场镜像构建并进入统一启动阶段；理由依据：镜像已由验真加载器准备，网络和 PgBouncer 门禁仍须与源码构建模式完全相同。
if($offlineAssetImport){Write-Host '商业知识离线镜像已验真，进入统一 PgBouncer 私网预检。'}
# [2026-08-31 14:43:17] 作用：两套源码构建模式共用同一镜像时效和增量构建逻辑；理由依据：第二套应与第一套业务和部署逻辑一致，只保留端口、URL、容器、网络与数据卷隔离。
else{
  # [2026-08-18 15:21:08] 作用：固定本地 Worker 镜像合同；理由依据：九类 Worker、Beat、Flower和队列初始化必须复用同一源码版本。
  $workerImage='sql-rag-knowledge-worker:commercial'
  # [2026-08-18 15:21:08] 作用：固定 Worker 源码覆盖基础标签；理由依据：覆盖构建不能一边读取一边改写同一最终标签。
  $workerSourceBaseImage='sql-rag-knowledge-worker:commercial-source-base'
  # [2026-08-18 15:21:08] 作用：定位 Worker 完整依赖 Dockerfile；理由依据：仅该文件或依赖锁变化才允许重跑apt和pip。
  $workerDockerfile=Join-Path $knowledgeRoot 'backend\large-scale_commercialization_upgrade\until\Worker\Dockerfile'
  # [2026-08-18 15:21:08] 作用：定位 Worker Python 依赖锁；理由依据：业务源码变化不得被误判为依赖变化。
  $workerRequirements=Join-Path $knowledgeRoot 'backend\large-scale_commercialization_upgrade\until\Worker\requirements-worker.txt'
  # [2026-08-18 15:21:08] 作用：定位轻量源码覆盖 Dockerfile；理由依据：已安装的系统与Python依赖应跨业务源码升级复用。
  $workerSourceOverlayDockerfile=Join-Path $knowledgeRoot 'backend\large-scale_commercialization_upgrade\until\Worker\Dockerfile.source-overlay'
  # [2026-08-18 15:21:08] 作用：读取当前 Worker 镜像创建时间；理由依据：启动入口以镜像事实而不是人工开关判断是否需要构建。
  $workerImageCreatedText=(& docker image inspect --format '{{.Created}}' $workerImage 2>$null|Select-Object -First 1)
  # [2026-08-18 15:21:08] 作用：把存在的 Worker 镜像时间转换为UTC；理由依据：与Windows文件LastWriteTimeUtc比较时避免时区误判。
  $workerImageCreatedUtc=if([string]::IsNullOrWhiteSpace($workerImageCreatedText)){$null}else{[DateTimeOffset]::Parse($workerImageCreatedText).UtcDateTime}
  # [2026-08-18 15:21:08] 作用：计算 Worker 依赖定义的最新时间；理由依据：依赖文件晚于镜像时必须执行完整可复现构建。
  $workerDependencyNewestUtc=@($workerDockerfile,$workerRequirements|ForEach-Object{(Get-Item -LiteralPath $_).LastWriteTimeUtc}|Sort-Object -Descending|Select-Object -First 1)[0]
  # [2026-08-18 15:21:08] 作用：枚举会进入 Worker 的运行源码；理由依据：只因Python、配置或模板业务文件变化时创建轻量覆盖层。
  $workerSourceFiles=Get-ChildItem -LiteralPath (Join-Path $knowledgeRoot 'backend') -Recurse -File|Where-Object{$_.Extension-in@('.py','.json','.yaml','.yml','.toml','.ini','.cfg','.sql','.txt','.md')-and$_.FullName-notmatch'[\\/](?:\.venv|runtime|__pycache__|\.pytest_cache|tests?|Offline_deployment|Cache_gateway|PgBouncer|Prometheus|Grafana)[\\/]'-and$_.Name-notmatch'^\.env$'}
  # [2026-08-18 15:21:08] 作用：计算业务运行源码的最新时间；理由依据：镜像已包含更新源码时再次启动应零构建复用现有容器。
  $workerSourceNewestUtc=@($workerSourceFiles|ForEach-Object{$_.LastWriteTimeUtc}|Sort-Object -Descending|Select-Object -First 1)[0]
  # [2026-08-18 15:21:08] 作用：记录本轮是否已做完整 Worker 构建；理由依据：完整镜像已经包含当前源码，无需紧接着再做覆盖构建。
  $workerFullyBuilt=$false
  # [2026-09-01 17:23:10] 作用：用当前 profile 的完整 Compose 文件列表按需构建唯一控制 Worker；理由依据：网络 override 不得改变第一套成熟源码构建判断。
  if($null-eq$workerImageCreatedUtc-or$workerDependencyNewestUtc-gt$workerImageCreatedUtc){& docker.exe @composeCommandArguments build --pull=false km-worker-control|Out-Host;$workerFullyBuilt=$true}
  # [2026-08-18 15:21:08] 作用：阻断 Worker 完整构建失败；理由依据：禁止以旧依赖镜像继续启动形成代码与运行环境漂移。
  if($workerFullyBuilt-and$LASTEXITCODE-ne0){throw "商业知识 Worker 完整构建失败，exit=$LASTEXITCODE"}
  # [2026-08-18 15:21:08] 作用：在仅业务源码更新时为当前依赖镜像创建基础标签；理由依据：轻量构建必须从已验证依赖层复制而不访问软件源。
  if(-not$workerFullyBuilt-and$null-ne$workerImageCreatedUtc-and$workerSourceNewestUtc-gt$workerImageCreatedUtc){& docker tag $workerImage $workerSourceBaseImage|Out-Host}
  # [2026-08-18 15:21:08] 作用：阻断 Worker 基础标签失败；理由依据：禁止源码覆盖构建静默回退到错误或缺失基础镜像。
  if(-not$workerFullyBuilt-and$null-ne$workerImageCreatedUtc-and$workerSourceNewestUtc-gt$workerImageCreatedUtc-and$LASTEXITCODE-ne0){throw "商业知识 Worker 基础镜像标记失败，exit=$LASTEXITCODE"}
  # [2026-08-18 15:21:08] 作用：构建不运行apt和pip的Worker源码覆盖镜像；理由依据：日常业务代码升级应在秒级完成且不依赖外网下载。
  if(-not$workerFullyBuilt-and$null-ne$workerImageCreatedUtc-and$workerSourceNewestUtc-gt$workerImageCreatedUtc){& docker build --pull=false --build-arg "KM_WORKER_BASE_IMAGE=$workerSourceBaseImage" --file $workerSourceOverlayDockerfile --tag $workerImage $knowledgeRoot|Out-Host}
  # [2026-08-18 15:21:08] 作用：阻断 Worker 源码覆盖构建失败；理由依据：解析修复未进入镜像时不得把旧Worker声明为已更新。
  if(-not$workerFullyBuilt-and$null-ne$workerImageCreatedUtc-and$workerSourceNewestUtc-gt$workerImageCreatedUtc-and$LASTEXITCODE-ne0){throw "商业知识 Worker 源码覆盖构建失败，exit=$LASTEXITCODE"}
  # [2026-08-31 16:10:00] 作用：声明缓存网关镜像合同；理由依据：网关只在自身最小依赖或运行入口变化时重建。
  $cacheGatewayImage='sql-rag-knowledge-cache-gateway:commercial'
  # [2026-08-31 16:10:01] 作用：把全景独立网关程序加入缓存镜像最小构建输入；理由依据：新增页面缓存端点必须持久进入一键构建镜像且不触发 Worker 完整依赖安装。
  $cacheGatewayInputs=@((Join-Path $knowledgeRoot 'backend\large-scale_commercialization_upgrade\until\Cache_gateway\Dockerfile'),(Join-Path $knowledgeRoot 'backend\large-scale_commercialization_upgrade\until\Cache_gateway\requirements-gateway.txt'),(Join-Path $knowledgeRoot 'backend\large-scale_commercialization_upgrade\until\Redis\progress_gateway.py'),(Join-Path $knowledgeRoot 'backend\large-scale_commercialization_upgrade\until\Redis\panorama_gateway.py'))+@(Get-ChildItem -LiteralPath (Join-Path $knowledgeRoot 'backend\large-scale_commercialization_upgrade\Database_logic_at_eachstage\stage_04_progress_cache') -File|Select-Object -ExpandProperty FullName)
  # [2026-08-31 16:10:02] 作用：读取缓存网关镜像时间；理由依据：无输入变化时保留正在运行的既有容器。
  $cacheGatewayImageCreatedText=(& docker image inspect --format '{{.Created}}' $cacheGatewayImage 2>$null|Select-Object -First 1)
  # [2026-08-31 16:10:03] 作用：转换缓存网关镜像 UTC 时间；理由依据：Windows 与 Docker 时间比较必须处于同一时区基准。
  $cacheGatewayImageCreatedUtc=if([string]::IsNullOrWhiteSpace($cacheGatewayImageCreatedText)){$null}else{[DateTimeOffset]::Parse($cacheGatewayImageCreatedText).UtcDateTime}
  # [2026-08-31 16:10:04] 作用：计算缓存网关输入最新时间；理由依据：先保持第一套既有增量判断，再由内容和镜像 ID 契约消除同步时间戳误报。
  $cacheGatewayNewestUtc=@($cacheGatewayInputs|ForEach-Object{(Get-Item -LiteralPath $_).LastWriteTimeUtc}|Sort-Object -Descending|Select-Object -First 1)[0]
  # [2026-08-31 16:10:05] 作用：固定缓存网关是否需要刷新；理由依据：后续每个 Docker 调用都会改变 LASTEXITCODE，必须先保存同一判定。
  $cacheGatewayRefreshRequired=($null-eq$cacheGatewayImageCreatedUtc-or$cacheGatewayNewestUtc-gt$cacheGatewayImageCreatedUtc)
  # [2026-08-31 16:10:06] 作用：定位单镜像验真导入工具；理由依据：在线构建失败时只能恢复缓存网关，禁止调用十镜像加载器回滚 Worker。
  $cacheGatewayVerifiedOverlayLoader=Join-Path $knowledgeRoot 'backend\large-scale_commercialization_upgrade\until\Offline_deployment\Import-KnowledgeCommercialVerifiedOverlayImage.ps1'
  # [2026-08-31 16:10:07] 作用：初始化内容相同镜像复用标记；理由依据：文件时间晚于镜像不等于业务字节已变化。
  $cacheGatewayVerifiedImageReady=$false
  # [2026-08-31 16:10:08] 作用：仅在时间戳要求刷新且验真工具存在时检查当前镜像；理由依据：普通无变化启动保持零额外开销。
  if($cacheGatewayRefreshRequired-and(Test-Path -LiteralPath $cacheGatewayVerifiedOverlayLoader -PathType Leaf)){
    # [2026-08-31 16:10:09] 作用：以只读 Check 模式比对清单、八个源码输入和当前镜像 ID；理由依据：CRLF/LF 或同步时间不得触发无谓 Docker Hub 请求。
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $cacheGatewayVerifiedOverlayLoader -Mode Check -ImageName $cacheGatewayImage|Out-Host
    # [2026-08-31 16:10:10] 作用：保存只读检查退出码；理由依据：退出码 0 才证明本地镜像与当前源码契约完全一致。
    $cacheGatewayVerifiedImageReady=($LASTEXITCODE-eq0)
  }
  # [2026-08-31 16:10:11] 作用：初始化正式在线构建退出码；理由依据：未执行构建时不得继承前一个镜像检查命令的状态。
  $cacheGatewayBuildExitCode=0
  # [2026-08-31 16:10:12] 作用：初始化单镜像恢复标记；理由依据：只有验真导入成功才能吸收在线构建失败。
  $cacheGatewayVerifiedFallbackReady=$false
  # [2026-09-01 17:23:10] 作用：用当前 profile 的完整 Compose 文件列表优先构建缓存网关；理由依据：固定网络只修路由，第二套仍消费第一套同版源码构建逻辑。
  if($cacheGatewayRefreshRequired-and-not$cacheGatewayVerifiedImageReady){& docker.exe @composeCommandArguments build --pull=false km-cache-gateway|Out-Host;$cacheGatewayBuildExitCode=$LASTEXITCODE}
  # [2026-08-31 16:10:14] 作用：仅在正式构建失败且验真工具存在时导入单一缓存网关镜像；理由依据：失效 Engine 代理不能阻断整套服务，也不能回滚其他九个镜像。
  if($cacheGatewayRefreshRequired-and-not$cacheGatewayVerifiedImageReady-and$cacheGatewayBuildExitCode-ne0-and(Test-Path -LiteralPath $cacheGatewayVerifiedOverlayLoader -PathType Leaf)){
    # [2026-08-31 16:10:15] 作用：验真并按需导入当前包的缓存网关覆盖 tar；理由依据：Ensure 会同时校验清单、源码、tar SHA256、大小和加载后镜像 ID。
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $cacheGatewayVerifiedOverlayLoader -Mode Ensure -ImageName $cacheGatewayImage|Out-Host
    # [2026-08-31 16:10:16] 作用：记录单镜像恢复结果；理由依据：只有退出码 0 才允许继续 PgBouncer 和 Compose up。
    $cacheGatewayVerifiedFallbackReady=($LASTEXITCODE-eq0)
    # [2026-08-31 16:10:17] 作用：输出不含密钥的恢复证据；理由依据：现场日志必须能证明只恢复缓存网关且没有回滚 Worker。
    if($cacheGatewayVerifiedFallbackReady){Write-Host "KNOWLEDGE_COMMERCIAL_CACHE_GATEWAY_VERIFIED_FALLBACK_READY image=$cacheGatewayImage online_build_exit=$cacheGatewayBuildExitCode other_images_changed=0"}
  }
  # [2026-08-31 16:10:18] 作用：阻断在线构建和验真单镜像恢复均失败的状态；理由依据：未知源码或损坏 tar 不能以旧缓存网关静默运行。
  if($cacheGatewayRefreshRequired-and-not$cacheGatewayVerifiedImageReady-and$cacheGatewayBuildExitCode-ne0-and-not$cacheGatewayVerifiedFallbackReady){throw "商业知识缓存网关构建失败且验真单镜像恢复未通过，build_exit=$cacheGatewayBuildExitCode"}
  # [2026-08-18 15:21:08] 作用：声明PgBouncer镜像合同；理由依据：连接池仅在自身Dockerfile或入口变化时重建。
  $pgbouncerImage='sql-rag-knowledge-pgbouncer:commercial'
  # [2026-08-18 15:21:08] 作用：收集PgBouncer最小构建输入；理由依据：解析和模型代码变化不得触发apt安装连接池。
  $pgbouncerInputs=@((Join-Path $knowledgeRoot 'backend\large-scale_commercialization_upgrade\until\PgBouncer\Dockerfile'),(Join-Path $knowledgeRoot 'backend\large-scale_commercialization_upgrade\until\PgBouncer\entrypoint.py'))
  # [2026-08-18 15:21:08] 作用：读取PgBouncer镜像时间；理由依据：启动入口依据真实镜像时效判断构建。
  $pgbouncerImageCreatedText=(& docker image inspect --format '{{.Created}}' $pgbouncerImage 2>$null|Select-Object -First 1)
  # [2026-08-18 15:21:08] 作用：转换PgBouncer镜像UTC时间；理由依据：消除宿主时区与Docker时间格式差异。
  $pgbouncerImageCreatedUtc=if([string]::IsNullOrWhiteSpace($pgbouncerImageCreatedText)){$null}else{[DateTimeOffset]::Parse($pgbouncerImageCreatedText).UtcDateTime}
  # [2026-08-18 15:21:08] 作用：计算PgBouncer输入最新时间；理由依据：只在真实配置生成逻辑变化时重建。
  $pgbouncerNewestUtc=@($pgbouncerInputs|ForEach-Object{(Get-Item -LiteralPath $_).LastWriteTimeUtc}|Sort-Object -Descending|Select-Object -First 1)[0]
  # [2026-09-01 17:23:10] 作用：用当前 profile 的完整 Compose 文件列表按需构建 PgBouncer；理由依据：正常一键启动不重复下载且网络 override 与镜像内容解耦。
  if($null-eq$pgbouncerImageCreatedUtc-or$pgbouncerNewestUtc-gt$pgbouncerImageCreatedUtc){& docker.exe @composeCommandArguments build --pull=false km-pgbouncer|Out-Host}
  # [2026-08-18 15:21:08] 作用：阻断PgBouncer增量构建失败；理由依据：连接池与业务数据库合同必须保持同版本。
  if(($null-eq$pgbouncerImageCreatedUtc-or$pgbouncerNewestUtc-gt$pgbouncerImageCreatedUtc)-and$LASTEXITCODE-ne0){throw "商业知识 PgBouncer 构建失败，exit=$LASTEXITCODE"}
}
# [2026-09-03 11:14:29] 作用：初始化出口代理运行证据；理由依据：第一套未配置出口修复时也必须输出确定的未配置状态。
$egressProxyName='not_configured';$egressProxyUrl='';$egressProxyStatus='not_checked';$egressOverridePath=$null;$egressOverrideHash='not_configured'
# [2026-09-03 11:14:29] 作用：读取当前第二套出口代理合同；理由依据：只有独立 profile 才允许为模型 Worker 追加运行时网络覆盖。
$egressProxyContract=Get-KmEgressProxyContract -Profile $ServicePortProfile
# [2026-09-03 11:14:29] 作用：在商业容器变更前选择真实可达的代理；理由依据：每次冷启动都必须从容器视角确认外部 LLM 出口，而不是复用过期环境变量。
if($null-ne$egressProxyContract){
  # [2026-09-03 11:14:29] 作用：从已展开 Compose 读取实际 Worker 镜像；理由依据：探针必须运行在与三类业务 Worker 相同的依赖镜像内。
  $egressWorkerServiceProperty=$expandedCompose.services.PSObject.Properties['km-worker-llm']
  # [2026-09-03 11:14:29] 作用：阻断无法确定 Worker 镜像的状态；理由依据：不能用不同镜像的网络结果替代真实 LLM Worker 出口。
  if($null-eq$egressWorkerServiceProperty){throw '第二套出口代理探针找不到 km-worker-llm Compose 服务。'}
  # [2026-09-03 11:14:29] 作用：读取 LLM Worker 镜像标签；理由依据：Compose 展开结果是 Docker 将实际消费的唯一镜像事实。
  $egressProbeImage=([string]$egressWorkerServiceProperty.Value.image).Trim()
  # [2026-09-03 11:14:29] 作用：阻断空 Worker 镜像标签；理由依据：无镜像身份时禁止启动或选择代理。
  if([string]::IsNullOrWhiteSpace($egressProbeImage)){throw '第二套出口代理探针 Worker 镜像为空。'}
  # [2026-09-03 11:14:29] 作用：确认探针镜像已存在于本机；理由依据：冷启动不能为网络探针隐式拉取未经发布清单验证的新镜像。
  $egressImageInspect=@(& docker.exe image inspect $egressProbeImage 2>&1)
  # [2026-09-03 11:14:29] 作用：保存镜像检查原生退出码；理由依据：后续候选探针不能把镜像缺失误判成网络不可达。
  $egressImageInspectExitCode=$LASTEXITCODE
  # [2026-09-03 11:14:29] 作用：阻断缺失探针镜像；理由依据：当前 1534 基线应保留 Worker 镜像，缺失必须先恢复镜像而不是改业务逻辑。
  if($egressImageInspectExitCode-ne0){throw "第二套出口代理探针镜像不存在：image=$egressProbeImage exit=$egressImageInspectExitCode"}
  # [2026-09-03 11:14:29] 作用：初始化最后一个候选失败证据；理由依据：所有候选失败时必须报告具体出口状态而不是笼统超时。
  $egressLastProbe=$null
  # [2026-09-03 11:14:29] 作用：依次尝试 profile 声明的代理候选；理由依据：Docker Desktop 网关地址可能随重启变化，启动逻辑必须可自选已验证地址。
  foreach($egressCandidate in @($egressProxyContract.Candidates)){
    # [2026-09-03 11:14:29] 作用：输出当前候选的非密钥身份；理由依据：现场日志需要可审计选择过程但不能暴露凭据。
    Write-Host "KNOWLEDGE_COMMERCIAL_EGRESS_PROXY_PROBE candidate=$($egressCandidate.Name) host=$($egressCandidate.Host) port=$($egressCandidate.Port)"
    # [2026-09-03 11:14:29] 作用：执行容器内供应商 HTTPS 探针；理由依据：只接受真实 Docker bridge 经代理返回的 200/401/403。
    $egressProbeResult=Invoke-KmEgressProxyProbe -Image $egressProbeImage -ProbeUrl $egressProxyContract.ProbeUrl -ProxyUrl $egressCandidate.Url -NoProxy $egressProxyContract.NoProxy -Network 'bridge'
    # [2026-09-03 11:14:29] 作用：保存最近候选探针结果；理由依据：最终失败诊断必须保留退出码、HTTP 状态和有限输出。
    $egressLastProbe=[pscustomobject]@{Candidate=$egressCandidate;Result=$egressProbeResult}
    # [2026-09-03 11:14:29] 作用：锁定首个通过的代理候选；理由依据：后续 override 和实际 Worker 必须使用同一个已经证明的 URL。
    if($egressProbeResult.Passed){$egressProxyName=$egressCandidate.Name;$egressProxyUrl=$egressCandidate.Url;$egressProxyStatus=[string]$egressProbeResult.Status;break}
    # [2026-09-03 11:14:29] 作用：记录候选失败但继续尝试；理由依据：单个 Docker 网关失效不应掩盖其他 profile 候选的可用性。
    Write-Warning "第二套出口代理候选未通过：candidate=$($egressCandidate.Name) exit=$($egressProbeResult.ExitCode) status=$($egressProbeResult.Status) output=$(($egressProbeResult.Output)-join' | ')"
  }
  # [2026-09-03 11:14:29] 作用：阻断全部代理候选失败；理由依据：没有经容器验证的外部出口时继续启动会再次把真实任务卡在 58%。
  if([string]::IsNullOrWhiteSpace($egressProxyUrl)){throw "第二套容器外部 LLM 出口未通过：last_candidate=$($egressLastProbe.Candidate.Name) exit=$($egressLastProbe.Result.ExitCode) status=$($egressLastProbe.Result.Status) output=$(($egressLastProbe.Result.Output)-join' | ')"}
  # [2026-09-03 11:14:29] 作用：转义将写入 YAML 的代理值；理由依据：即使未来候选扩展，也不能让引号改变 Compose 结构。
  $egressProxyYamlValue=$egressProxyUrl.Replace("'","''")
  # [2026-09-03 11:14:29] 作用：转义将写入 YAML 的内部绕行值；理由依据：NO_PROXY 必须作为一个稳定逗号列表传入每个模型 Worker。
  $egressNoProxyYamlValue=$egressProxyContract.NoProxy.Replace("'","''")
  # [2026-09-03 11:14:29] 作用：初始化第二套出口 Compose override 行集合；理由依据：基础商业 Compose 和第一套文件保持逐字不变。
  $egressOverrideLines=New-Object 'System.Collections.Generic.List[string]'
  # [2026-09-03 11:14:29] 作用：声明 override 的 services 根；理由依据：Compose 合并只需覆盖选定 Worker 的 environment 映射。
  [void]$egressOverrideLines.Add('services:')
  # [2026-09-03 11:14:29] 作用：逐个生成模型 Worker 的代理环境覆盖；理由依据：LLM、ASR、视觉是已证实的外部模型调用边界。
  foreach($egressWorkerService in @($egressProxyContract.WorkerServices)){
    # [2026-09-03 11:14:29] 作用：写入当前 Worker 服务键；理由依据：环境覆盖必须精确命中 Compose 服务名。
    [void]$egressOverrideLines.Add("  $egressWorkerService`:")
    # [2026-09-03 11:14:29] 作用：声明当前 Worker 的环境映射；理由依据：Compose map merge 可覆盖 env_file 中的漂移代理值。
    [void]$egressOverrideLines.Add('    environment:')
    # [2026-09-03 12:08:00] 作用：注入标准大写 HTTP 代理；理由依据：Python/OpenAI/urllib 的环境代理合同使用该标准变量名，且避免 PowerShell 5.1 回读重复大小写键。
    [void]$egressOverrideLines.Add("      HTTP_PROXY: '$egressProxyYamlValue'")
    # [2026-09-03 12:08:00] 作用：注入标准大写 HTTPS 代理；理由依据：SiliconFlow HTTPS 请求必须沿已验证代理建立 TLS。
    [void]$egressOverrideLines.Add("      HTTPS_PROXY: '$egressProxyYamlValue'")
    # [2026-09-03 12:08:00] 作用：清空标准大写 ALL_PROXY；理由依据：SOCKS 或旧全局代理不能抢占已验证 HTTP CONNECT 路径。
    [void]$egressOverrideLines.Add("      ALL_PROXY: ''")
    # [2026-09-03 12:08:00] 作用：注入标准大写 NO_PROXY；理由依据：商业私网、迁移数据库和 Docker 内部 DNS 必须绕过外部代理。
    [void]$egressOverrideLines.Add("      NO_PROXY: '$egressNoProxyYamlValue'")
  }
  # [2026-09-03 11:14:29] 作用：定位 profile 专属出口 override 文件；理由依据：重启时可重复生成且不污染源码或第一套运行目录。
  $egressOverridePath=Join-Path $runtimeRoot 'docker-compose.egress.override.yml'
  # [2026-09-03 11:14:29] 作用：以 UTF-8 无 BOM 写入出口 override；理由依据：Docker Compose 读取的字节必须跨 Windows PowerShell 版本稳定。
  [IO.File]::WriteAllText($egressOverridePath,($egressOverrideLines-join"`r`n")+"`r`n",(New-Object Text.UTF8Encoding($false)))
  # [2026-09-03 11:14:29] 作用：计算出口 override SHA256；理由依据：现场日志需要证明实际消费的环境覆盖没有被运行时篡改。
  $egressOverrideHash=(Get-FileHash -LiteralPath $egressOverridePath -Algorithm SHA256).Hash.ToLowerInvariant()
  # [2026-09-03 11:14:29] 作用：把出口 override 加入所有后续 Compose 调用；理由依据：config、start、up、ps 必须共享同一 Worker 网络合同。
  foreach($egressComposeArgument in @('-f',$egressOverridePath)){[void]$composeCommandArguments.Add([string]$egressComposeArgument)}
  # [2026-09-03 11:14:29] 作用：重新验证含出口 override 的 Compose 结构；理由依据：生成文件成功不能替代 Docker 对最终合并合同的解析。
  & docker.exe @composeCommandArguments config --quiet|Out-Host
  # [2026-09-03 11:14:29] 作用：保存出口 override Compose 解析退出码；理由依据：后续 JSON 读取不能覆盖 Docker 原生失败。
  $egressComposeConfigExitCode=$LASTEXITCODE
  # [2026-09-03 11:14:29] 作用：阻断出口 override 语法失败；理由依据：不能让环境覆盖错误推迟到容器创建阶段。
  if($egressComposeConfigExitCode-ne0){throw "第二套出口代理 Compose override 无法解析：exit=$egressComposeConfigExitCode path=$egressOverridePath"}
  # [2026-09-03 11:14:29] 作用：读取最终合并 Compose JSON；理由依据：三类 Worker 的代理环境必须从 Docker 实际合并结果验收。
  $egressComposeJson=(& docker.exe @composeCommandArguments config --format json|Out-String)
  # [2026-09-03 11:14:29] 作用：保存最终合并 JSON 退出码；理由依据：合法 JSON 不能掩盖 Docker config 失败。
  $egressComposeJsonExitCode=$LASTEXITCODE
  # [2026-09-03 11:14:29] 作用：阻断最终合并 JSON 失败；理由依据：无法读取环境事实时不得启动商业容器。
  if($egressComposeJsonExitCode-ne0){throw "第二套出口代理 Compose 合并 JSON 失败：exit=$egressComposeJsonExitCode"}
  # [2026-09-03 11:14:29] 作用：解析最终合并 Compose 文档；理由依据：动态属性校验必须基于结构化对象而不是字符串搜索。
  $egressComposeDocument=$egressComposeJson|ConvertFrom-Json
  # [2026-09-03 11:14:29] 作用：声明期望的大小写代理环境集合；理由依据：同一代理合同必须覆盖不同 Linux 客户端的读取习惯并清空 ALL_PROXY，且 PowerShell 5.1 哈希表键名不区分大小写。
  $expectedEgressEnvironment=@(
    # [2026-09-03 12:02:00] 作用：登记大写 HTTP 代理期望值；理由依据：PowerShell 5.1 不能在同一哈希表中安全保存大小写相同的环境键。
    [pscustomobject]@{Key='HTTP_PROXY';Value=$egressProxyUrl}
    # [2026-09-03 12:02:00] 作用：登记大写 HTTPS 代理期望值；理由依据：模型 HTTPS 请求必须沿已验证代理建立 TLS。
    [pscustomobject]@{Key='HTTPS_PROXY';Value=$egressProxyUrl}
    # [2026-09-03 12:02:00] 作用：登记大写 ALL_PROXY 清空值；理由依据：旧 SOCKS 或全局代理不得抢占已验证 HTTP CONNECT 路径。
    [pscustomobject]@{Key='ALL_PROXY';Value=''}
    # [2026-09-03 12:02:00] 作用：登记大写 NO_PROXY 期望值；理由依据：商业私网和迁移数据库必须绕过外部代理。
    [pscustomobject]@{Key='NO_PROXY';Value=$egressProxyContract.NoProxy}
  )
  # [2026-09-03 11:14:29] 作用：逐个回读三类 Worker 的最终环境；理由依据：只对外部模型边界做覆盖，其他服务不进入验收集合。
  foreach($egressWorkerService in @($egressProxyContract.WorkerServices)){
    # [2026-09-03 11:14:29] 作用：读取最终 Compose Worker 属性；理由依据：服务缺失代表 override 没有命中当前商业定义。
    $egressExpandedServiceProperty=$egressComposeDocument.services.PSObject.Properties[$egressWorkerService]
    # [2026-09-03 11:14:29] 作用：阻断最终 Worker 服务缺失；理由依据：代理覆盖必须对每一个模型队列生效。
    if($null-eq$egressExpandedServiceProperty){throw "第二套出口代理 Worker 缺失：service=$egressWorkerService"}
    # [2026-09-03 11:14:29] 作用：读取最终 Worker environment 映射；理由依据：只检查 Docker 合并后的结构化环境。
    $egressEnvironmentProperty=$egressExpandedServiceProperty.Value.PSObject.Properties['environment']
    # [2026-09-03 11:14:29] 作用：阻断最终 Worker 环境映射缺失；理由依据：没有映射时代理变量不会进入容器。
    if($null-eq$egressEnvironmentProperty){throw "第二套出口代理 Worker 环境缺失：service=$egressWorkerService"}
    # [2026-09-03 11:14:29] 作用：逐项比较代理和绕行值；理由依据：环境变量任一漂移都会让内部调用或外部 LLM 走错路由。
    foreach($egressEnvironmentEntry in $expectedEgressEnvironment.GetEnumerator()){
      # [2026-09-03 11:14:29] 作用：读取单个最终环境属性；理由依据：PowerShell 5.1 对动态属性必须显式访问。
      $egressActualEnvironmentProperty=$egressEnvironmentProperty.Value.PSObject.Properties[$egressEnvironmentEntry.Key]
      # [2026-09-03 11:14:29] 作用：阻断单个代理环境缺失或漂移；理由依据：不能以部分注入宣称模型 Worker 出口已修复。
      if($null-eq$egressActualEnvironmentProperty-or[string]$egressActualEnvironmentProperty.Value-ne[string]$egressEnvironmentEntry.Value){throw "第二套出口代理环境回读失败：service=$egressWorkerService key=$($egressEnvironmentEntry.Key)"}
    }
  }
  # [2026-09-03 11:14:29] 作用：输出第二套出口代理就绪标记；理由依据：日志必须能与 58% 业务故障及第一套未改状态明确区分。
  Write-Host "KNOWLEDGE_COMMERCIAL_EGRESS_PROXY_READY candidate=$egressProxyName status=$egressProxyStatus services=$(@($egressProxyContract.WorkerServices).Count) override_sha256=$egressOverrideHash first_stack_changed=false"
}
# [2026-09-01 18:25:18] 作用：在镜像预检通过后仅重建已确认归属当前 profile 的冲突商业网络；理由依据：保留全部命名卷并缩短第二套停机窗口，第一套和数据库网络不参与。
if($commercialNetworkRequiresRecreate){
  # [2026-09-01 18:25:18] 作用：从已展开的同一 Compose 合同提取全部商业容器名；理由依据：只按项目名执行 down 已在目标机漏掉旧网络上的活跃端点。
  $expectedCommercialContainerNames=@($expandedServices|ForEach-Object{[string]$_.Value.container_name}|Sort-Object -Unique)
  # [2026-09-01 18:25:18] 作用：读取旧商业网络预检快照中的全部端点名；理由依据：任何容器状态变化前必须完成精确所有权验真。
  $recreateNetworkEndpointNames=@($currentCommercialNetworkDocument.Containers.PSObject.Properties|ForEach-Object{[string]$_.Value.Name}|Sort-Object -Unique)
  # [2026-09-01 18:25:18] 作用：找出不在展开商业清单且不是本 profile 迁移 PostgreSQL 的端点；理由依据：未知端点必须阻断而不能被强制删除或断网。
  $unexpectedRecreateEndpointNames=@($recreateNetworkEndpointNames|Where-Object{$expectedCommercialContainerNames-notcontains$_-and-not($pgbouncerUsesProfileMigratedPostgres-and[string]::Equals($_,$migratedPostgresContainer,[StringComparison]::OrdinalIgnoreCase))})
  # [2026-09-01 18:25:18] 作用：阻断旧网络存在任何未知端点；理由依据：网络名称和容器前缀均不能替代完整 Compose 清单所有权。
  if($unexpectedRecreateEndpointNames.Count-gt0){throw "第二套商业网络存在未知端点，禁止重建：$($unexpectedRecreateEndpointNames-join',')"}
  # [2026-09-01 18:25:18] 作用：逐端点核对其 Compose 项目标签；理由依据：同名容器也可能来自其他项目，删除前必须验证生命周期归属。
  foreach($recreateEndpointName in $recreateNetworkEndpointNames){
    # [2026-09-01 18:25:18] 作用：按端点身份确定唯一允许的 Compose 项目；理由依据：商业容器与迁移 PostgreSQL 分属两个独立项目。
    $expectedEndpointProject=if($pgbouncerUsesProfileMigratedPostgres-and[string]::Equals($recreateEndpointName,$migratedPostgresContainer,[StringComparison]::OrdinalIgnoreCase)){$migratedPostgresProject}else{$commercialProject}
    # [2026-09-02 15:29:04] 作用：读取端点容器完整 Docker JSON；理由依据：Windows PowerShell 5.1 会剥掉 Go-template 标签键的内层双引号并把 com 误解析为函数。
    $actualEndpointInspectText=((& docker.exe inspect $recreateEndpointName 2>$null)|Out-String)
    # [2026-09-02 15:29:04] 作用：保存端点容器详情读取退出码；理由依据：后续 JSON 转换会覆盖 daemon 的原始失败状态。
    $actualEndpointInspectExitCode=$LASTEXITCODE
    # [2026-09-02 15:29:04] 作用：阻断缺失容器或 Docker daemon 读取失败；理由依据：未知容器身份不能进入商业端点清理。
    if($actualEndpointInspectExitCode-ne0){throw "第二套商业网络端点容器读取失败：container=$recreateEndpointName exit=$actualEndpointInspectExitCode"}
    # [2026-09-02 15:29:04] 作用：解析端点容器首个结构化 Docker 文档；理由依据：Compose 项目标签必须从 JSON 属性读取而不是依赖原生命令引号转义。
    try{$actualEndpointInspectDocument=($actualEndpointInspectText|ConvertFrom-Json)[0]}catch{throw "第二套商业网络端点容器详情不是合法 JSON：container=$recreateEndpointName"}
    # [2026-09-02 15:29:04] 作用：读取端点容器标签对象；理由依据：缺少标签时必须形成空项目身份并由后续所有权门禁拒绝。
    $actualEndpointLabels=$actualEndpointInspectDocument.Config.Labels
    # [2026-09-02 15:29:04] 作用：按结构化键读取 Compose 项目标签；理由依据：带点号的标签键不能再经过 PowerShell 5.1 原生参数转义。
    $actualEndpointProject=if($null-eq$actualEndpointLabels){''}else{[string]$actualEndpointLabels.'com.docker.compose.project'}
    # [2026-09-02 15:29:04] 作用：阻断端点项目标签缺失或漂移；理由依据：不得停止其他 Compose 项目的同名容器。
    if($actualEndpointProject-ne$expectedEndpointProject){throw "第二套商业网络端点项目不匹配：container=$recreateEndpointName expected=$expectedEndpointProject actual=$actualEndpointProject exit=$actualEndpointInspectExitCode"}
  }
  # [2026-09-01 18:25:18] 作用：枚举当前 Engine 的全部容器名；理由依据：同时覆盖运行中、已停止和一次性初始化容器且不猜测存在性。
  $allDockerContainerNames=@(& docker.exe ps -a --format '{{.Names}}')
  # [2026-09-01 18:25:18] 作用：阻断容器枚举失败；理由依据：不完整集合可能留下活跃端点并再次触发半迁移。
  if($LASTEXITCODE-ne0){throw "第二套商业网络重建无法枚举容器，exit=$LASTEXITCODE"}
  # [2026-09-01 18:25:18] 作用：选择当前真实存在且属于展开商业清单的容器；理由依据：仅这些容器允许停止和重建，数据库容器永不进入删除集合。
  $commercialContainersToRemove=@($expectedCommercialContainerNames|Where-Object{$allDockerContainerNames-contains$_})
  # [2026-09-01 18:25:18] 作用：精确强制移除全部第二套商业容器且不附带卷参数；理由依据：活跃端点必须先离开旧 bridge，18 个命名卷及业务数据继续保留。
  if($commercialContainersToRemove.Count-gt0){& docker.exe rm --force @commercialContainersToRemove|Out-Host}
  # [2026-09-01 18:25:18] 作用：保存精确商业容器移除退出码；理由依据：后续数据库断网和网络检查会覆盖原始状态。
  $commercialContainerRemoveExitCode=if($commercialContainersToRemove.Count-gt0){$LASTEXITCODE}else{0}
  # [2026-09-01 18:25:18] 作用：阻断任一商业容器移除失败；理由依据：不得在仍有已知活跃端点时继续删除网络。
  if($commercialContainerRemoveExitCode-ne0){throw "第二套商业容器精确移除失败：exit=$commercialContainerRemoveExitCode containers=$($commercialContainersToRemove-join',') volumes_removed=false"}
  # [2026-09-01 18:25:18] 作用：记录迁移 PostgreSQL 是否历史性误接入商业网络；理由依据：该容器只允许断开错误 bridge，禁止停止或删除。
  $migratedPostgresNeedsCommercialDisconnect=($pgbouncerUsesProfileMigratedPostgres-and$recreateNetworkEndpointNames-contains$migratedPostgresContainer)
  # [2026-09-01 18:25:18] 作用：在断开错误 bridge 前读取迁移 PostgreSQL 状态和健康；理由依据：数据库必须继续在自身私网运行且不得因网络修复中断。
  if($migratedPostgresNeedsCommercialDisconnect){$migratedPostgresPreDisconnectState=(& docker.exe inspect --format '{{.State.Status}}|{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' $migratedPostgresContainer 2>$null|Select-Object -First 1)}
  # [2026-09-01 18:25:18] 作用：阻断未运行或不健康数据库的网络变更；理由依据：异常数据库应单独诊断而不能混入商业网络迁移。
  if($migratedPostgresNeedsCommercialDisconnect-and([string]$migratedPostgresPreDisconnectState).Trim()-ne'running|healthy'){throw "第二套迁移 PostgreSQL 状态不允许断开错误商业网络：$migratedPostgresPreDisconnectState"}
  # [2026-09-01 18:25:18] 作用：读取迁移 PostgreSQL 当前网络集合；理由依据：断开商业 bridge 前必须证明其自身数据库网络仍存在。
  if($migratedPostgresNeedsCommercialDisconnect){$migratedPostgresPreDisconnectNetworks=((& docker.exe inspect --format '{{json .NetworkSettings.Networks}}' $migratedPostgresContainer 2>$null|Select-Object -First 1)|ConvertFrom-Json)}
  # [2026-09-01 18:25:18] 作用：阻断数据库缺少 profile 专属私网；理由依据：商业网络不能成为迁移 PostgreSQL 的唯一网络。
  if($migratedPostgresNeedsCommercialDisconnect-and$null-eq$migratedPostgresPreDisconnectNetworks.PSObject.Properties[$migratedPostgresNetwork]){throw "第二套迁移 PostgreSQL 缺少自身私网，禁止断开：$migratedPostgresNetwork"}
  # [2026-09-01 18:25:18] 作用：仅断开迁移 PostgreSQL 历史残留的商业 bridge；理由依据：保留数据库容器、卷、进程和 profile 私网不变。
  if($migratedPostgresNeedsCommercialDisconnect){& docker.exe network disconnect --force $commercialNetwork $migratedPostgresContainer|Out-Host}
  # [2026-09-01 18:25:18] 作用：保存数据库错误网络断开退出码；理由依据：重新检查网络前必须保留原始 Docker 结果。
  $migratedPostgresDisconnectExitCode=if($migratedPostgresNeedsCommercialDisconnect){$LASTEXITCODE}else{0}
  # [2026-09-01 18:25:18] 作用：阻断迁移 PostgreSQL 错误网络断开失败；理由依据：绝不通过删除数据库容器来绕过活跃端点。
  if($migratedPostgresDisconnectExitCode-ne0){throw "第二套迁移 PostgreSQL 断开错误商业网络失败：exit=$migratedPostgresDisconnectExitCode"}
  # [2026-09-01 18:25:18] 作用：重新读取旧商业网络完整结构；理由依据：删除网络前必须以 daemon 当前事实证明活跃端点为零。
  $remainingCommercialNetworkDocument=(((& docker.exe network inspect $commercialNetwork)|Out-String)|ConvertFrom-Json)
  # [2026-09-01 18:25:18] 作用：保存旧商业网络回读退出码；理由依据：解析和端点枚举不能覆盖 daemon 失败。
  $remainingCommercialNetworkInspectExitCode=$LASTEXITCODE
  # [2026-09-01 18:25:18] 作用：阻断旧商业网络无法回读；理由依据：未知网络状态下不得继续执行删除。
  if($remainingCommercialNetworkInspectExitCode-ne0){throw "第二套旧商业网络回读失败：network=$commercialNetwork exit=$remainingCommercialNetworkInspectExitCode"}
  # [2026-09-01 18:25:18] 作用：枚举精确清理后的残余端点；理由依据：Docker CLI 的进度文本不能替代零端点事实。
  $remainingCommercialNetworkEndpoints=@($remainingCommercialNetworkDocument.Containers.PSObject.Properties|ForEach-Object{[string]$_.Value.Name})
  # [2026-09-01 18:25:18] 作用：阻断任何残余端点；理由依据：网络删除必须失败关闭且不强制影响未知容器。
  if($remainingCommercialNetworkEndpoints.Count-gt0){throw "第二套旧商业网络仍有活跃端点：$($remainingCommercialNetworkEndpoints-join',')"}
  # [2026-09-01 18:25:18] 作用：移除已验明归属且零端点的旧第二套商业网络；理由依据：固定 IPAM 只能在重新创建网络时生效且网络本身不承载卷数据。
  & docker.exe network rm $commercialNetwork|Out-Host
  # [2026-09-01 18:25:18] 作用：保存旧商业网络精确移除退出码；理由依据：后续 Compose 创建会覆盖 LASTEXITCODE。
  $commercialNetworkRemoveExitCode=$LASTEXITCODE
  # [2026-09-01 18:25:18] 作用：阻断旧网络精确移除失败；理由依据：不能让 Compose 继续复用冲突的 172.20.0.0/16。
  if($commercialNetworkRemoveExitCode-ne0){throw "第二套旧商业网络移除失败：network=$commercialNetwork exit=$commercialNetworkRemoveExitCode volumes_removed=false"}
  # [2026-09-01 18:25:18] 作用：输出仅第二套网络迁移完成证据；理由依据：现场日志必须明确商业容器重建、数据库仅断网且命名卷未删除。
  Write-Host "KNOWLEDGE_COMMERCIAL_NETWORK_RECREATED name=$commercialNetwork subnet=$commercialSubnet gateway=$commercialGateway containers_removed=$($commercialContainersToRemove.Count) migrated_postgres_disconnected=$migratedPostgresNeedsCommercialDisconnect volumes_removed=false first_stack_changed=false"
}
# [2026-09-02 14:33:58] 作用：仅对固定 IPAM 且使用本 profile 迁移 PostgreSQL 的部署检查历史错网；理由依据：第一套没有固定网络字段，当前修复不得进入其已验收路径。
if($commercialNetworkUsesFixedIpam-and$pgbouncerUsesProfileMigratedPostgres){
  # [2026-09-02 14:33:58] 作用：按完整名称枚举当前商业网络；理由依据：首次部署或已完成网络重建时网络可能尚不存在，此时必须由 Compose 原子创建。
  $currentCommercialNetworkNames=@(& docker.exe network ls --filter "name=^$commercialNetwork$" --format '{{.Name}}' 2>$null)
  # [2026-09-02 14:33:58] 作用：保存商业网络枚举退出码；理由依据：Docker Engine 故障不能被误判为无需清理。
  $currentCommercialNetworkListExitCode=$LASTEXITCODE
  # [2026-09-02 14:33:58] 作用：阻断商业网络清单读取失败；理由依据：未知网络状态下禁止断开数据库 endpoint。
  if($currentCommercialNetworkListExitCode-ne0){throw "迁移 PostgreSQL 历史商业 endpoint 检查无法枚举网络：exit=$currentCommercialNetworkListExitCode"}
  # [2026-09-02 14:33:58] 作用：只在同名商业网络真实存在时交叉检查数据库连接；理由依据：缺失网络应继续进入首次 Compose 创建路径。
  if($currentCommercialNetworkNames-contains$commercialNetwork){
    # [2026-09-02 14:33:58] 作用：读取迁移 PostgreSQL 当前网络集合；理由依据：必须从容器侧确认历史商业连接并证明 profile 私网仍在。
    $migratedPostgresCurrentNetworkJson=(& docker.exe inspect --format '{{json .NetworkSettings.Networks}}' $migratedPostgresContainer 2>$null|Select-Object -First 1)
    # [2026-09-02 14:33:58] 作用：保存迁移 PostgreSQL 网络读取退出码；理由依据：容器缺失或 daemon 失败时不得继续任何网络变更。
    $migratedPostgresCurrentNetworkInspectExitCode=$LASTEXITCODE
    # [2026-09-02 14:33:58] 作用：阻断迁移 PostgreSQL 网络读取失败；理由依据：不能用空对象推断数据库未误接商业网络。
    if($migratedPostgresCurrentNetworkInspectExitCode-ne0){throw "迁移 PostgreSQL 当前网络读取失败：container=$migratedPostgresContainer exit=$migratedPostgresCurrentNetworkInspectExitCode"}
    # [2026-09-02 14:33:58] 作用：解析迁移 PostgreSQL 网络对象；理由依据：网络名称必须按结构化属性比较而不是搜索 JSON 文本。
    try{$migratedPostgresCurrentNetworks=$migratedPostgresCurrentNetworkJson|ConvertFrom-Json}catch{throw "迁移 PostgreSQL 当前网络不是合法 JSON：container=$migratedPostgresContainer"}
    # [2026-09-02 14:33:58] 作用：读取商业网络完整结构；理由依据：断开前必须验证 Compose 所有权并从网络侧确认同一数据库 endpoint。
    $commercialNetworkBeforeOrphanDisconnectText=(& docker.exe network inspect $commercialNetwork 2>$null|Out-String)
    # [2026-09-02 14:33:58] 作用：保存商业网络结构读取退出码；理由依据：网络详情失败不能被 JSON 解析覆盖。
    $commercialNetworkBeforeOrphanDisconnectExitCode=$LASTEXITCODE
    # [2026-09-02 14:33:58] 作用：阻断商业网络结构读取失败；理由依据：未知网络归属时禁止修改数据库 endpoint。
    if($commercialNetworkBeforeOrphanDisconnectExitCode-ne0){throw "迁移 PostgreSQL 历史商业 endpoint 检查无法读取网络：network=$commercialNetwork exit=$commercialNetworkBeforeOrphanDisconnectExitCode"}
    # [2026-09-02 14:33:58] 作用：解析商业网络首个 Docker 文档；理由依据：PowerShell 5.1 需要显式索引网络 inspect 返回数组。
    try{$commercialNetworkBeforeOrphanDisconnectDocument=($commercialNetworkBeforeOrphanDisconnectText|ConvertFrom-Json)[0]}catch{throw "迁移 PostgreSQL 历史商业 endpoint 网络详情不是合法 JSON：network=$commercialNetwork"}
    # [2026-09-02 14:33:58] 作用：读取商业网络 Compose 项目标签；理由依据：同名网络不足以授权一键入口断开数据库。
    $commercialNetworkBeforeOrphanDisconnectProject=[string]$commercialNetworkBeforeOrphanDisconnectDocument.Labels.'com.docker.compose.project'
    # [2026-09-02 14:33:58] 作用：读取商业网络 Compose 逻辑名；理由依据：必须精确对应 knowledge-commercial 生命周期。
    $commercialNetworkBeforeOrphanDisconnectLogicalName=[string]$commercialNetworkBeforeOrphanDisconnectDocument.Labels.'com.docker.compose.network'
    # [2026-09-02 14:33:58] 作用：阻断未知项目或逻辑网络；理由依据：只允许第二套当前商业项目修复自己的历史 endpoint。
    if($commercialNetworkBeforeOrphanDisconnectProject-ne$commercialProject-or$commercialNetworkBeforeOrphanDisconnectLogicalName-ne'knowledge-commercial'){throw "迁移 PostgreSQL 历史商业 endpoint 网络归属不匹配：network=$commercialNetwork expected_project=$commercialProject actual_project=$commercialNetworkBeforeOrphanDisconnectProject logical=$commercialNetworkBeforeOrphanDisconnectLogicalName"}
    # [2026-09-02 14:33:58] 作用：从容器侧判断数据库是否仍登记商业网络；理由依据：当前 recreate=False 漏洞正是未检查该独立生命周期事实。
    $migratedPostgresReportsCommercialNetwork=($null-ne$migratedPostgresCurrentNetworks.PSObject.Properties[$commercialNetwork])
    # [2026-09-02 14:33:58] 作用：枚举商业网络侧全部 endpoint 名；理由依据：daemon 的 active endpoints 才是 Compose create 失败的直接证据。
    $commercialNetworkBeforeOrphanDisconnectEndpointNames=@($commercialNetworkBeforeOrphanDisconnectDocument.Containers.PSObject.Properties|ForEach-Object{[string]$_.Value.Name})
    # [2026-09-02 14:33:58] 作用：从商业网络侧判断数据库 endpoint 是否仍活跃；理由依据：网络侧和容器侧必须一致后才能自动断开。
    $commercialNetworkReportsMigratedPostgres=($commercialNetworkBeforeOrphanDisconnectEndpointNames-contains$migratedPostgresContainer)
    # [2026-09-02 14:33:58] 作用：阻断数据库与网络两侧不一致的半连接状态；理由依据：单侧残留需要独立诊断，不能以强制断网掩盖 daemon 漂移。
    if($migratedPostgresReportsCommercialNetwork-ne$commercialNetworkReportsMigratedPostgres){throw "迁移 PostgreSQL 商业网络双向状态不一致：container_side=$migratedPostgresReportsCommercialNetwork network_side=$commercialNetworkReportsMigratedPostgres"}
    # [2026-09-02 14:33:58] 作用：只在两侧均确认历史误接时进入受控断开；理由依据：正常冷启动和重复一键必须零变更跳过。
    if($migratedPostgresReportsCommercialNetwork){
      # [2026-09-02 14:33:58] 作用：读取断网前数据库运行和健康状态；理由依据：异常数据库不能混入网络修复。
      $migratedPostgresBeforeOrphanDisconnectState=(& docker.exe inspect --format '{{.State.Status}}|{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' $migratedPostgresContainer 2>$null|Select-Object -First 1)
      # [2026-09-02 14:33:58] 作用：要求断网前数据库运行且健康；理由依据：网络修复不得中断或替代数据库恢复。
      if(([string]$migratedPostgresBeforeOrphanDisconnectState).Trim()-ne'running|healthy'){throw "迁移 PostgreSQL 状态不允许清理历史商业 endpoint：state=$migratedPostgresBeforeOrphanDisconnectState"}
      # [2026-09-02 14:33:58] 作用：要求断网前数据库仍连接 profile 专属私网；理由依据：商业 bridge 绝不能成为数据库唯一网络。
      if($null-eq$migratedPostgresCurrentNetworks.PSObject.Properties[$migratedPostgresNetwork]){throw "迁移 PostgreSQL 缺少自身私网，禁止清理历史商业 endpoint：network=$migratedPostgresNetwork"}
      # [2026-09-02 14:33:58] 作用：仅断开迁移 PostgreSQL 历史误接的商业 bridge；理由依据：保留数据库容器、进程、命名卷和私网不变。
      & docker.exe network disconnect --force $commercialNetwork $migratedPostgresContainer|Out-Host
      # [2026-09-02 14:33:58] 作用：保存数据库历史商业 endpoint 断开退出码；理由依据：后续回读会覆盖 Docker 原始结果。
      $migratedPostgresOrphanDisconnectExitCode=$LASTEXITCODE
      # [2026-09-02 14:33:58] 作用：阻断历史商业 endpoint 断开失败；理由依据：不得继续进入必然失败的 PgBouncer create。
      if($migratedPostgresOrphanDisconnectExitCode-ne0){throw "迁移 PostgreSQL 历史商业 endpoint 断开失败：network=$commercialNetwork exit=$migratedPostgresOrphanDisconnectExitCode"}
      # [2026-09-02 14:33:58] 作用：重新读取数据库网络集合；理由依据：断开退出码不能替代私网保留和错网消失事实。
      $migratedPostgresAfterOrphanDisconnectNetworkJson=(& docker.exe inspect --format '{{json .NetworkSettings.Networks}}' $migratedPostgresContainer 2>$null|Select-Object -First 1)
      # [2026-09-02 14:33:58] 作用：保存断网后数据库网络读取退出码；理由依据：回读失败必须阻止商业服务继续启动。
      $migratedPostgresAfterOrphanDisconnectNetworkExitCode=$LASTEXITCODE
      # [2026-09-02 14:33:58] 作用：阻断断网后数据库网络读取失败；理由依据：未知结果不能声明修复完成。
      if($migratedPostgresAfterOrphanDisconnectNetworkExitCode-ne0){throw "迁移 PostgreSQL 历史商业 endpoint 断开后网络读取失败：exit=$migratedPostgresAfterOrphanDisconnectNetworkExitCode"}
      # [2026-09-02 14:33:58] 作用：解析断网后数据库网络对象；理由依据：后置门禁必须按结构化网络键执行。
      try{$migratedPostgresAfterOrphanDisconnectNetworks=$migratedPostgresAfterOrphanDisconnectNetworkJson|ConvertFrom-Json}catch{throw "迁移 PostgreSQL 历史商业 endpoint 断开后网络不是合法 JSON"}
      # [2026-09-02 14:33:58] 作用：重新读取断网后数据库状态；理由依据：网络修复必须证明数据库进程和健康均未受影响。
      $migratedPostgresAfterOrphanDisconnectState=(& docker.exe inspect --format '{{.State.Status}}|{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' $migratedPostgresContainer 2>$null|Select-Object -First 1)
      # [2026-09-02 14:33:58] 作用：要求断网后数据库仍运行且健康；理由依据：只有无中断修复才允许创建 PgBouncer。
      if(([string]$migratedPostgresAfterOrphanDisconnectState).Trim()-ne'running|healthy'){throw "迁移 PostgreSQL 清理历史商业 endpoint 后状态异常：state=$migratedPostgresAfterOrphanDisconnectState"}
      # [2026-09-02 14:33:58] 作用：要求断网后数据库仍保留 profile 私网；理由依据：PgBouncer 后续必须经该网络直连内部 5432。
      if($null-eq$migratedPostgresAfterOrphanDisconnectNetworks.PSObject.Properties[$migratedPostgresNetwork]){throw "迁移 PostgreSQL 清理历史商业 endpoint 后丢失自身私网：network=$migratedPostgresNetwork"}
      # [2026-09-02 14:33:58] 作用：要求断网后数据库容器侧不再登记商业网络；理由依据：重复一键必须稳定进入幂等跳过分支。
      if($null-ne$migratedPostgresAfterOrphanDisconnectNetworks.PSObject.Properties[$commercialNetwork]){throw "迁移 PostgreSQL 清理历史商业 endpoint 后仍登记商业网络：network=$commercialNetwork"}
      # [2026-09-02 14:33:58] 作用：回读商业网络结构；理由依据：必须从 daemon 网络侧证明 active endpoint 已消失。
      $commercialNetworkAfterOrphanDisconnectText=(& docker.exe network inspect $commercialNetwork 2>$null|Out-String)
      # [2026-09-02 14:33:58] 作用：保存断网后商业网络回读退出码；理由依据：网络侧验真失败不得被视为修复成功。
      $commercialNetworkAfterOrphanDisconnectExitCode=$LASTEXITCODE
      # [2026-09-02 14:33:58] 作用：阻断断网后商业网络回读失败；理由依据：PgBouncer create 依赖网络侧零数据库 endpoint 事实。
      if($commercialNetworkAfterOrphanDisconnectExitCode-ne0){throw "迁移 PostgreSQL 历史商业 endpoint 断开后网络回读失败：exit=$commercialNetworkAfterOrphanDisconnectExitCode"}
      # [2026-09-02 14:33:58] 作用：解析断网后商业网络文档；理由依据：网络 inspect 数组必须在 PowerShell 5.1 中显式取首项。
      try{$commercialNetworkAfterOrphanDisconnectDocument=($commercialNetworkAfterOrphanDisconnectText|ConvertFrom-Json)[0]}catch{throw "迁移 PostgreSQL 历史商业 endpoint 断开后网络详情不是合法 JSON"}
      # [2026-09-02 14:33:58] 作用：枚举断网后商业网络 endpoint；理由依据：任何同名数据库残留都会再次阻断 Compose create。
      $commercialNetworkAfterOrphanDisconnectEndpointNames=@($commercialNetworkAfterOrphanDisconnectDocument.Containers.PSObject.Properties|ForEach-Object{[string]$_.Value.Name})
      # [2026-09-02 14:33:58] 作用：阻断商业网络侧仍存在数据库 endpoint；理由依据：容器单侧结果不能替代 daemon active endpoint 事实。
      if($commercialNetworkAfterOrphanDisconnectEndpointNames-contains$migratedPostgresContainer){throw "迁移 PostgreSQL 历史商业 endpoint 断开后仍存在于网络侧：network=$commercialNetwork"}
      # [2026-09-02 14:33:58] 作用：输出数据库历史错网的无中断修复证据；理由依据：目标日志需要区分网络已匹配但仍清理旧 endpoint 的路径。
      Write-Host "KNOWLEDGE_COMMERCIAL_MIGRATED_POSTGRES_ORPHAN_ENDPOINT_REPAIRED container=$migratedPostgresContainer commercial_network=$commercialNetwork private_network=$migratedPostgresNetwork state=$migratedPostgresAfterOrphanDisconnectState volumes_removed=false first_stack_changed=false"
    }
  }
}
# [2026-09-02 10:30:25] 作用：声明当前 profile 的 PgBouncer 容器身份；理由依据：创建前残留容器的网络修复和创建后验收必须命中同一容器。
$pgbouncerContainer="$ContainerNamePrefix-km-pgbouncer"
# [2026-09-02 10:30:25] 作用：只在固定 IPAM profile 创建前校正 PgBouncer 商业网络 endpoint；理由依据：第二套网络可能已正确存在但停止残留容器没有 endpoint，正是 Compose create 的已复现失败边界。
if($commercialNetworkUsesFixedIpam){
  # [2026-09-02 10:30:25] 作用：执行当前第二套 PgBouncer 商业网络创建前验真与幂等补接；理由依据：仅允许归属正确的停止容器补回 km-pgbouncer 别名，不触碰第一套或命名卷。
  $pgbouncerCommercialNetworkPreflight=Ensure-KmPgbouncerCommercialNetwork -ContainerName $pgbouncerContainer -NetworkName $commercialNetwork -ExpectedProject $commercialProject -RequireNetwork $false
  # [2026-09-02 10:30:25] 作用：输出创建前 PgBouncer endpoint 事实；理由依据：目标日志必须能区分首次创建、已接线复用和残留容器补接。
  Write-Host "KNOWLEDGE_COMMERCIAL_PGBOUNCER_NETWORK_PREFLIGHT_READY container=$pgbouncerContainer network=$commercialNetwork present=$($pgbouncerCommercialNetworkPreflight.Present) attached=$($pgbouncerCommercialNetworkPreflight.Attached) alias_ready=$($pgbouncerCommercialNetworkPreflight.AliasReady)"
}
# [2026-09-01 17:23:10] 作用：用当前 profile 的完整 Compose 文件列表先创建 PgBouncer；理由依据：必须在其余三十五个服务等待依赖前完成固定商业网络和数据库私网接线。
& docker.exe @composeCommandArguments create --no-build --pull never km-pgbouncer|Out-Host
# [2026-08-31 17:59:07] 作用：保存 PgBouncer 创建退出码；理由依据：后续 Docker 检查会覆盖 LASTEXITCODE。
$pgbouncerCreateExitCode=$LASTEXITCODE
# [2026-08-31 17:59:08] 作用：阻断 PgBouncer 容器创建失败；理由依据：禁止把镜像、Compose 或环境错误改写成健康超时。
if($pgbouncerCreateExitCode-ne0){throw "商业知识 PgBouncer 容器创建失败，exit=$pgbouncerCreateExitCode"}
# [2026-09-03 13:18:02] 作用：在商业网络真实创建后复用已选代理执行第二次容器出口探针；理由依据：最终模型 Worker 位于该网络，必须证明其路由与 default bridge 一致可用。
if($null-ne$egressProxyContract){
  # [2026-09-03 13:18:03] 作用：以选定代理和商业网络执行模型供应商 HTTPS 探针；理由依据：同一代理、同一镜像和同一 NO_PROXY 才能闭合冷启动出口合同。
  $commercialEgressProbeResult=Invoke-KmEgressProxyProbe -Image $egressProbeImage -ProbeUrl $egressProxyContract.ProbeUrl -ProxyUrl $egressProxyUrl -NoProxy $egressProxyContract.NoProxy -Network $commercialNetwork
  # [2026-09-03 13:18:04] 作用：阻断商业网络出口探针失败；理由依据：不能让已创建的 PgBouncer 继续扩展成会在 58% 超时的完整服务图。
  if(-not$commercialEgressProbeResult.Passed){throw "第二套商业网络出口未通过：network=$commercialNetwork proxy=$egressProxyName exit=$($commercialEgressProbeResult.ExitCode) status=$($commercialEgressProbeResult.Status) output=$(($commercialEgressProbeResult.Output)-join' | ')"}
  # [2026-09-03 13:18:05] 作用：输出商业网络出口已验证标记；理由依据：现场日志必须区分 default bridge 探针和真实 Worker 网络探针。
  Write-Host "KNOWLEDGE_COMMERCIAL_EGRESS_PROXY_NETWORK_READY network=$commercialNetwork candidate=$egressProxyName status=$($commercialEgressProbeResult.Status) first_stack_changed=false"
}
# [2026-09-02 10:30:25] 作用：只在固定 IPAM profile 创建后再次双向验真 PgBouncer endpoint；理由依据：Compose create 的零退出码不能证明网络侧和容器侧都已同步。
if($commercialNetworkUsesFixedIpam){
  # [2026-09-02 10:30:25] 作用：执行当前第二套 PgBouncer 商业网络创建后硬门禁；理由依据：缺 endpoint 或缺 km-pgbouncer 别名必须在启动连接池前明确失败。
  $pgbouncerCommercialNetworkPostCreate=Ensure-KmPgbouncerCommercialNetwork -ContainerName $pgbouncerContainer -NetworkName $commercialNetwork -ExpectedProject $commercialProject -RequireNetwork $true
  # [2026-09-02 10:30:25] 作用：输出创建后 PgBouncer endpoint 闭环事实；理由依据：后续迁移 PostgreSQL 接线和健康探针必须消费已验证的商业 DNS。
  Write-Host "KNOWLEDGE_COMMERCIAL_PGBOUNCER_NETWORK_READY container=$pgbouncerContainer network=$commercialNetwork attached=$($pgbouncerCommercialNetworkPostCreate.Attached) alias_ready=$($pgbouncerCommercialNetworkPostCreate.AliasReady)"
}
# [2026-08-31 17:59:10] 作用：仅为本机恢复库执行容器私网接线；理由依据：外部 PostgreSQL 继续使用其原网络主机合同。
if($pgbouncerUsesProfileMigratedPostgres){
  # [2026-08-31 17:59:11] 作用：读取本 profile 迁移 PostgreSQL 的运行和健康状态；理由依据：宿主 25434 监听不能替代上游容器自身 ready。
  $migratedPostgresState=(& docker inspect --format '{{.State.Status}}|{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' $migratedPostgresContainer 2>$null|Select-Object -First 1)
  # [2026-08-31 17:59:12] 作用：要求迁移 PostgreSQL 已运行且健康；理由依据：连接池不得对停止或初始化中的数据库创建客户端池。
  if(([string]$migratedPostgresState).Trim()-ne'running|healthy'){throw "商业知识上游 PostgreSQL 未就绪：container=$migratedPostgresContainer state=$migratedPostgresState"}
  # [2026-08-31 17:59:13] 作用：确认 profile 专属迁移网络真实存在；理由依据：项目名推导不能替代 Docker 运行态事实。
  & docker network inspect $migratedPostgresNetwork *> $null
  # [2026-08-31 17:59:14] 作用：阻断缺失迁移网络；理由依据：禁止回退到 host.docker.internal 或临时开放数据库宿主绑定。
  if($LASTEXITCODE-ne0){throw "商业知识上游 PostgreSQL 私有网络不存在：$migratedPostgresNetwork"}
  # [2026-08-31 17:59:15] 作用：读取 PgBouncer 当前接入的网络集合；理由依据：重复一键启动必须幂等跳过已完成接线。
  $pgbouncerNetworkJson=(& docker inspect --format '{{json .NetworkSettings.Networks}}' $pgbouncerContainer 2>$null|Select-Object -First 1)
  # [2026-08-31 17:59:16] 作用：解析 PgBouncer 网络对象；理由依据：不得依赖 docker network connect 的错误文本判断已连接状态。
  $pgbouncerNetworks=$pgbouncerNetworkJson|ConvertFrom-Json
  # [2026-08-31 17:59:17] 作用：仅在未接入时连接本 profile 迁移网络；理由依据：保持第一套和第二套网络、容器及生命周期完全隔离。
  if($null-eq$pgbouncerNetworks.PSObject.Properties[$migratedPostgresNetwork]){
    # [2026-08-31 17:59:18] 作用：把 PgBouncer 接入迁移 PostgreSQL 私网；理由依据：容器 DNS 与内部 5432 消除 Windows 回环不可路由问题。
    & docker network connect $migratedPostgresNetwork $pgbouncerContainer|Out-Host
    # [2026-08-31 17:59:19] 作用：阻断私网接线失败；理由依据：禁止继续等待必然 unhealthy 的 PgBouncer。
    if($LASTEXITCODE-ne0){throw "商业知识 PgBouncer 接入 PostgreSQL 私网失败：network=$migratedPostgresNetwork exit=$LASTEXITCODE"}
  }
  # [2026-08-31 17:59:20] 作用：输出不含凭据的上游拓扑证据；理由依据：现场可直接证明不再绕行 192.168.65.254:25434。
  Write-Host "KNOWLEDGE_COMMERCIAL_PGBOUNCER_PRIVATE_ROUTE_READY host=$pgbouncerUpstreamHost port=$pgbouncerUpstreamPort network=$migratedPostgresNetwork"
}
# [2026-09-01 17:23:10] 作用：用当前 profile 的完整 Compose 文件列表单独启动 PgBouncer；理由依据：先让固定网络上的真实 SQL 健康门禁具名通过再展开完整依赖图。
& docker.exe @composeCommandArguments start km-pgbouncer|Out-Host
# [2026-08-31 17:59:22] 作用：保存 PgBouncer 启动退出码；理由依据：健康轮询会覆盖 native 命令结果。
$pgbouncerStartExitCode=$LASTEXITCODE
# [2026-08-31 17:59:23] 作用：阻断 PgBouncer 进程启动失败；理由依据：容器未运行时健康等待没有意义。
if($pgbouncerStartExitCode-ne0){throw "商业知识 PgBouncer 启动失败，exit=$pgbouncerStartExitCode"}
# [2026-09-02 11:21:53] 作用：在 PgBouncer 启动后复核固定商业网络 active endpoint；理由依据：关机重启或同名网络重建的陈旧状态必须在健康轮询前被明确拦截。
if($commercialNetworkUsesFixedIpam){
  # [2026-09-02 11:21:53] 作用：执行运行态 PgBouncer 网络双向硬门禁；理由依据：容器已运行时必须同时具备当前 NetworkID、active endpoint 和 km-pgbouncer 别名。
  $pgbouncerCommercialNetworkRuntime=Ensure-KmPgbouncerCommercialNetwork -ContainerName $pgbouncerContainer -NetworkName $commercialNetwork -ExpectedProject $commercialProject -RequireNetwork $true
  # [2026-09-02 11:21:53] 作用：阻断运行态缺失 active endpoint；理由依据：后续服务依赖图不能把 Docker 网络故障改写成解析或队列超时。
  if(-not$pgbouncerCommercialNetworkRuntime.ActiveEndpoint){throw "商业知识 PgBouncer 运行态缺少 active endpoint：network=$commercialNetwork container=$pgbouncerContainer"}
  # [2026-09-02 11:21:53] 作用：输出运行态网络稳定证据；理由依据：目标日志必须区分容器启动成功和网络真正可用。
  Write-Host "KNOWLEDGE_COMMERCIAL_PGBOUNCER_NETWORK_RUNTIME_READY container=$pgbouncerContainer network=$commercialNetwork active_endpoint=$($pgbouncerCommercialNetworkRuntime.ActiveEndpoint) alias_ready=$($pgbouncerCommercialNetworkRuntime.AliasReady)"
}
# [2026-08-31 17:59:24] 作用：初始化 PgBouncer 健康状态；理由依据：等待循环结束后必须有确定值参与门禁。
$pgbouncerPreflightHealth=''
# [2026-08-31 17:59:25] 作用：最多等待六十秒完成真实 SELECT 1 健康探针；理由依据：正常私网连接无需进入四分钟 Compose 依赖超时。
for($pgbouncerAttempt=1;$pgbouncerAttempt-le30;$pgbouncerAttempt++){
  # [2026-08-31 17:59:26] 作用：读取当前 profile PgBouncer 健康状态；理由依据：探针同时验证客户端认证、池配置和上游查询。
  $pgbouncerPreflightHealth=([string](& docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' $pgbouncerContainer 2>$null|Select-Object -First 1)).Trim()
  # [2026-08-31 17:59:27] 作用：健康后立即结束预检等待；理由依据：避免给正常重复启动增加固定延迟。
  if($pgbouncerPreflightHealth-eq'healthy'){break}
  # [2026-08-31 17:59:28] 作用：在下一次健康探测前短暂退避；理由依据：Compose 探针按十秒周期运行且禁止忙轮询 Docker Engine。
  Start-Sleep -Seconds 2
}
# [2026-08-31 17:59:29] 作用：阻断未通过真实查询的 PgBouncer；理由依据：不得再让其余服务把上游根因改写成 dependency failed to start。
if($pgbouncerPreflightHealth-ne'healthy'){throw "商业知识 PgBouncer 私网查询未就绪：host=$pgbouncerUpstreamHost port=$pgbouncerUpstreamPort network=$migratedPostgresNetwork health=$pgbouncerPreflightHealth"}
# [2026-08-31 17:59:30] 作用：输出 PgBouncer 独立预检成功标记；理由依据：目标日志必须具名证明终极故障点已越过。
Write-Host "KNOWLEDGE_COMMERCIAL_PGBOUNCER_PREFLIGHT_READY host=$pgbouncerUpstreamHost port=$pgbouncerUpstreamPort health=$pgbouncerPreflightHealth"
# [2026-09-01 17:23:10] 作用：用当前 profile 的完整 Compose 文件列表启动完整商业服务图；理由依据：第二套全部容器必须进入固定不冲突网段，第一套继续消费原单文件配置。
& docker.exe @composeCommandArguments up -d --no-build --pull never --remove-orphans|Out-Host
# [2026-08-31 17:59:32] 作用：保存完整 Compose 启动退出码；理由依据：后续错误处理不得读取被其它命令覆盖的 LASTEXITCODE。
$composeExitCode=$LASTEXITCODE
# [2026-08-31 17:59:33] 作用：阻断完整 Compose 启动失败；理由依据：不允许无 Broker、缓存或 Worker 的降级商业模式。
if($composeExitCode-ne0){throw "商业知识服务启动失败，exit=$composeExitCode"}
# [2026-08-15 22:04:00] 作用：准备 RabbitMQ Basic Auth；理由依据：健康门禁验证真实管理 API 和三节点集群。
$rabbitCredential=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("$($secrets.rabbit_user):$($secrets.rabbit_password)"))
# [2026-08-17 08:40:59] 作用：准备 Flower Basic Auth；理由依据：联合门禁必须验证四类 Celery Worker 已真实注册而不是只看容器进程。
$flowerCredential=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("$($secrets.flower_user):$($secrets.flower_password)"))
# [2026-08-15 22:04:00] 作用：初始化联合健康状态；理由依据：缓存、Broker、对象、tusd、Flower、Prometheus 和 Grafana 必须全部 ready。
$ready=$false;$lastError=''
# [2026-08-15 22:04:00] 作用：有界等待商业服务；理由依据：首次镜像创建较慢但禁止无限卡住一键入口。
for($attempt=1;$attempt-le120;$attempt++){
  # [2026-08-15 22:04:00] 作用：逐轮执行应用层健康探针；理由依据：容器 running 和端口监听都不足以证明可用。
  try{
    # [2026-08-15 22:04:00] 作用：验证 Redis Cluster 缓存网关；理由依据：API 热状态和 SSE 依赖真实 PING。
    $cacheHealth=Invoke-RestMethod "http://127.0.0.1:$cachePort/health" -TimeoutSec 5
    # [2026-08-21 09:00:49] 作用：验证全景独立缓存网关和专用 Redis；理由依据：公司页面硬指标不能借上传进度集群假绿或在缓存缺失时启动。
    $panoramaCacheHealth=Invoke-RestMethod "http://127.0.0.1:$panoramaCachePort/health" -TimeoutSec 5
    # [2026-08-17 08:40:59] 作用：调用 RabbitMQ 4.1 的客户端可服务健康探针；理由依据：旧 ready 路径已返回 404，此探针同时检查节点本地告警、监听器和元数据库。
    $rabbitHealth=Invoke-RestMethod "http://127.0.0.1:$rabbitManagementPort/api/health/checks/ready-to-serve-clients" -Headers @{Authorization="Basic $rabbitCredential"} -TimeoutSec 5
    # [2026-08-17 08:40:59] 作用：读取 RabbitMQ 实时节点视图；理由依据：种子节点 ready 不代表三副本 Quorum Queue 所需的三节点已全部入群。
    $rabbitNodes=Invoke-RestMethod "http://127.0.0.1:$rabbitManagementPort/api/nodes" -Headers @{Authorization="Basic $rabbitCredential"} -TimeoutSec 5
    # [2026-08-17 08:40:59] 作用：确认三个预期 RabbitMQ 磁盘节点均运行且无分区；理由依据：商业队列不允许用单节点假集群通过启动门禁。
    $rabbitNodesReady=(@($rabbitNodes|Where-Object {$_.running-eq$true-and@('rabbit@km-rabbit-1','rabbit@km-rabbit-2','rabbit@km-rabbit-3')-contains$_.name-and@($_.partitions).Count-eq0}).Count-eq3)
    # [2026-08-15 22:04:00] 作用：验证 MinIO 四节点集群；理由依据：单节点 live 不代表对象纠删码集群可写。
    $minioHealth=Invoke-WebRequest "http://127.0.0.1:$minioApiPort/minio/health/cluster" -UseBasicParsing -TimeoutSec 5
    # [2026-08-15 22:04:00] 作用：验证 Prometheus ready；理由依据：监控存储和配置加载失败不得被容器状态掩盖。
    $prometheusHealth=Invoke-WebRequest "http://127.0.0.1:$prometheusPort/-/ready" -UseBasicParsing -TimeoutSec 5
    # [2026-08-15 22:04:00] 作用：验证 Grafana API；理由依据：观测入口必须真实可访问。
    $grafanaHealth=Invoke-RestMethod "http://127.0.0.1:$grafanaPort/api/health" -TimeoutSec 5
    # [2026-08-17 10:26:00] 作用：验证 Flower 观测页面真实可访问；理由依据：Flower 刷新 Worker 注册表可能在启动期超时，不能把观测接口延迟误判为执行池离线。
    $flowerHealth=Invoke-WebRequest "http://127.0.0.1:$flowerPort/" -Headers @{Authorization="Basic $flowerCredential"} -UseBasicParsing -TimeoutSec 5
    # [2026-08-17 10:26:00] 作用：通过 Broker 广播直接探测九类 Celery Worker；理由依据：任务是否可消费必须由执行平面 pong 证明，而不是依赖 Flower 的二级缓存。
    $workerInspect=(& docker exec "$ContainerNamePrefix-km-worker-control" celery -A until.Celery.celery_app:celery_app inspect ping --timeout 10 2>$null|Out-String)
    # [2026-08-17 10:26:00] 作用：核对全部九类 Worker 的逻辑主机名和在线节点总数；理由依据：任一资源队列无消费者时禁止 API 接收会永久排队的任务。
    $workerPoolsReady=(@('document','audio','vision','upload','asr','llm','persist','index','control'|Where-Object {$workerInspect-notmatch("(?m)^->\s+"+[regex]::Escape($_)+"@")}).Count-eq0-and$workerInspect-match'9 nodes online\.')
    # [2026-08-15 22:04:00] 作用：验证 tusd TCP 端口；理由依据：标准断点上传服务已监听固定 URL。
    $tusdReady=Test-NetConnection -ComputerName 127.0.0.1 -Port $tusdPort -InformationLevel Quiet -WarningAction SilentlyContinue
    # [2026-08-17 08:45:11] 作用：读取 PgBouncer 容器 SQL 健康状态；理由依据：Compose 探针已经用真实 SELECT 1 验证客户、池和上游三层链路。
    $pgbouncerHealth=(& docker inspect --format '{{.State.Health.Status}}' "$ContainerNamePrefix-km-pgbouncer" 2>$null|Select-Object -First 1)
    # [2026-08-17 08:45:11] 作用：判定 PgBouncer 真实查询门禁；理由依据：连接池不健康时禁止 Worker 或 API 继续接收任务。
    $pgbouncerReady=([string]$pgbouncerHealth).Trim()-eq'healthy'
    # [2026-08-15 22:04:00] 作用：联合判定所有必备服务；理由依据：任意关键组件缺失都不能声明商业任务平面 ready。
    # [2026-08-21 09:00:49] 作用：把全景独立缓存加入商业联合 ready 门禁；理由依据：任一缓存、队列、对象、Worker 或连接池缺失都不能报告一键启动成功。
    if($cacheHealth.redisCluster-eq$true-and$panoramaCacheHealth.ready-eq$true-and$panoramaCacheHealth.independentRedis-eq$true-and$rabbitHealth.status-eq'ok'-and$rabbitNodesReady-and$minioHealth.StatusCode-eq200-and$prometheusHealth.StatusCode-eq200-and$grafanaHealth.database-eq'ok'-and$flowerHealth.StatusCode-eq200-and$workerPoolsReady-and$tusdReady-and$pgbouncerReady){$ready=$true;break}
  # [2026-08-15 22:04:00] 作用：记录当前探针失败；理由依据：超时时给出最后真实错误而不是笼统连接失败。
  }catch{$lastError=$_.Exception.Message}
  # [2026-08-15 22:04:00] 作用：短暂等待下一轮；理由依据：服务内部选主和首次迁移需要有限稳定窗口。
  Start-Sleep -Seconds 2
}
# [2026-09-01 17:23:10] 作用：失败时用当前 profile 的完整 Compose 文件列表输出状态并终止；理由依据：固定网络和基础服务任一未就绪都不能继续启动 API。
if(-not$ready){& docker.exe @composeCommandArguments ps|Out-Host;throw "商业知识服务健康门禁未通过：$lastError"}
# [2026-08-15 22:04:00] 作用：向 Windows Knowledge API 启用商业路由；理由依据：只有基础设施全部 ready 后才接受 job-first 上传。
[Environment]::SetEnvironmentVariable('KM_COMMERCIAL_ASYNC_ENABLED','1','Process')
# [2026-08-17 15:43:14] 作用：向随后启动的宿主 Knowledge API 注入 RabbitMQ 控制面地址；理由依据：点击暂停必须在本机端口上精确终止长原子阶段并由晚确认消息安全重投到暂停检查点。
[Environment]::SetEnvironmentVariable('KM_CELERY_BROKER_URL',$hostBrokerUrl,'Process')
# [2026-08-15 22:04:00] 作用：注入缓存网关 URL；理由依据：API 通过固定 HTTP 服务访问 Redis Cluster 而不持有拓扑。
[Environment]::SetEnvironmentVariable('KM_CACHE_GATEWAY_URL',"http://127.0.0.1:$cachePort",'Process')
# [2026-08-15 22:04:00] 作用：注入缓存内部令牌；理由依据：浏览器不能直接读取或修改 Redis 热状态。
[Environment]::SetEnvironmentVariable('KM_CACHE_GATEWAY_TOKEN',[string]$secrets.cache_token,'Process')
# [2026-08-21 09:00:49] 作用：向随后启动的 Windows Knowledge API 注入全景独立缓存网关；理由依据：页面命中路径不得复用上传进度 Redis Cluster 或直接每次查库。
[Environment]::SetEnvironmentVariable('KM_PANORAMA_CACHE_GATEWAY_URL',"http://127.0.0.1:$panoramaCachePort",'Process')
# [2026-08-15 22:04:00] 作用：注入稳定对象 spool；理由依据：上传断点跨 FastAPI 重启保持且与 Worker 挂载一致。
[Environment]::SetEnvironmentVariable('KM_OBJECT_ROOT',$objectRoot,'Process')
# [2026-08-15 22:04:00] 作用：注入当前部署 profile；理由依据：Redis Key、Bucket 和任务记录防止两套串线。
[Environment]::SetEnvironmentVariable('SQL_RAG_DEPLOYMENT_PROFILE',$DeploymentProfile,'Process')
# [2026-08-15 22:04:00] 作用：注入浏览器可见 tusd URL；理由依据：WebUI 可按固定协议服务进行标准断点直传升级。
[Environment]::SetEnvironmentVariable('KM_TUSD_PUBLIC_URL',"http://$PublicHost`:$tusdPort/files/",'Process')
# [2026-08-15 22:04:00] 作用：注入 MinIO 内部 API；理由依据：对象归档和 Worker 物化使用当前 profile 私网服务。
[Environment]::SetEnvironmentVariable('KM_MINIO_ENDPOINT',"127.0.0.1:$minioApiPort",'Process')
# [2026-08-15 22:04:00] 作用：注入 MinIO Bucket；理由依据：API/维护任务按 profile 隔离对象生命周期。
[Environment]::SetEnvironmentVariable('KM_MINIO_BUCKET',$minioBucket,'Process')
# [2026-08-24 09:00:02] 作用：向随后启动的 Windows Knowledge API 注入 MinIO 访问账号；理由依据：NAS 远端解析回调必须复用当前 profile 的正式对象存储合同。
[Environment]::SetEnvironmentVariable('KM_MINIO_ACCESS_KEY',[string]$secrets.minio_user,'Process')
# [2026-08-24 09:00:02] 作用：向随后启动的 Windows Knowledge API 注入 MinIO 访问密钥；理由依据：回调不得依赖仅存在于 Worker 容器的临时环境。
[Environment]::SetEnvironmentVariable('KM_MINIO_SECRET_KEY',[string]$secrets.minio_password,'Process')
# [2026-08-24 09:00:02] 作用：向随后启动的 Windows Knowledge API 注入宿主对象根；理由依据：对象适配器的受控物化与清理路径必须和本地商业上传使用同一持久目录。
[Environment]::SetEnvironmentVariable('KM_OBJECT_CONTAINER_ROOT',$objectRoot,'Process')
# [2026-08-15 22:04:00] 作用：注入分块请求硬上限；理由依据：浏览器八兆分块低于十六兆服务端防护边界。
[Environment]::SetEnvironmentVariable('KM_UPLOAD_CHUNK_MAX_BYTES','16777216','Process')
# [2026-08-21 09:00:49] 作用：返回包含全景缓存 URL 的非密钥服务合同；理由依据：主启动器和验收报告需要区分两个缓存平面。
[pscustomobject]@{Ready=$true;Profile=$DeploymentProfile;ComposeProject=$commercialProject;Network=$commercialNetwork;ObjectRoot=$objectRoot;CacheGatewayUrl="http://$PublicHost`:$cachePort";PanoramaCacheUrl="http://$PublicHost`:$panoramaCachePort";RabbitMqUrl="amqp://$PublicHost`:$rabbitAmqpPort";RabbitMqManagementUrl="http://$PublicHost`:$rabbitManagementPort";MinioApiUrl="http://$PublicHost`:$minioApiPort";MinioConsoleUrl="http://$PublicHost`:$minioConsolePort";TusdUrl="http://$PublicHost`:$tusdPort/files/";FlowerUrl="http://$PublicHost`:$flowerPort";PrometheusUrl="http://$PublicHost`:$prometheusPort";GrafanaUrl="http://$PublicHost`:$grafanaPort";PgbouncerUrl=$pgbouncerPublicContract}
