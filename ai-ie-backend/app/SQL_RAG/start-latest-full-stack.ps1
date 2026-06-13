param(
  [switch]$RebuildExternalQdrant,
  [switch]$RunDatabaseInit,
  [switch]$RestartModel,
  [string]$ExternalSourceProfile='external_database'
)
$ErrorActionPreference='Stop'
try { $global:PSNativeCommandUseErrorActionPreference=$false } catch {}
$RepoRoot='D:\wkt\ai-ie-backend-feature-rag-new (1)\ai-ie-backend'
$SqlRag=Join-Path $RepoRoot 'app\SQL_RAG'
$Py=Join-Path $RepoRoot '.venv\Scripts\python.exe'
$EnvFile=Join-Path $SqlRag '.env'
$LogDir=Join-Path $RepoRoot 'logs\sql_rag_runtime'
# 2026-06-13 20:18:41 新增：把后端默认端口抽成变量；作用：默认端口被旧高权限进程锁住时可以自动换端口；理由：不能让新服务误连旧逻辑。
$BackendPort=18180
# 2026-06-13 20:18:41 新增：把 WebUI 默认端口抽成变量；作用：跟随后端端口重新生成代理地址；理由：前后端必须成对指向同一套最新逻辑。
$WebPort=18181
# 2026-06-13 20:18:41 新增：用当前端口生成后端 URL；作用：健康检查和 WebUI 代理都读取同一个地址；理由：避免脚本里散落硬编码。
$BackendUrl="http://127.0.0.1:$BackendPort"
# 2026-06-13 20:18:41 新增：用当前端口生成 WebUI URL；作用：输出给用户真实可访问入口；理由：默认端口不可用时也能明确知道最新地址。
$WebUrl="http://127.0.0.1:$WebPort"
$QwenUrl='http://127.0.0.1:18000/v1/models'
$LlamaExe=Join-Path $SqlRag 'module_config\model_service\runtimes\llama_cpp_win_cpu\llama-server.exe'
$ModelFile=Join-Path $SqlRag 'module_config\model_service\models\qwen35_2b\Qwen_Qwen3.5-2B-Q4_K_M.gguf'
$LlamaCwd=Split-Path -Parent $LlamaExe
chcp 65001 | Out-Null
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
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
        }
      }
    }
    # 2026-06-13 20:18:41 新增：等待端口实际释放；作用：避免刚杀完进程马上绑定导致 address in use；理由：Windows TCP 状态释放有延迟。
    $deadline=(Get-Date).AddSeconds(30)
    while((Get-Date) -lt $deadline){
      $still=Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
      if(!$still){break}
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
function Test-Qwen{
  try { Invoke-RestMethod $QwenUrl -TimeoutSec 5 | Out-Null; return $true } catch { return $false }
}
function Wait-Qwen($Seconds){
  $deadline=(Get-Date).AddSeconds($Seconds)
  while((Get-Date) -lt $deadline){
    if(Test-Qwen){Write-Host 'Qwen 模型服务已就绪：18000'; return}
    Start-Sleep -Seconds 2
  }
  throw 'Qwen 模型服务 18000 没有就绪'
}
function Wait-Port($Name,$Port,$Seconds){
  Write-Host "等待 $Name 端口 $Port ..."
  $deadline=(Get-Date).AddSeconds($Seconds)
  while((Get-Date) -lt $deadline){
    $c=New-Object System.Net.Sockets.TcpClient
    try{
      $t=$c.ConnectAsync('127.0.0.1',[int]$Port)
      if($t.Wait(1000) -and $c.Connected){Write-Host "$Name 已就绪：$Port"; return}
    }catch{}finally{$c.Close()}
    Start-Sleep -Seconds 2
  }
  throw "$Name 端口 $Port 超时未就绪"
}
function Test-Docker{
  $old=$ErrorActionPreference
  try{$ErrorActionPreference='SilentlyContinue'; docker info *> $null; return $LASTEXITCODE -eq 0}
  catch{return $false}
  finally{$ErrorActionPreference=$old}
}
function Ensure-Docker{
  if(Test-Docker){Write-Host 'Docker Engine 已就绪。'; return}
  $exe=@("$env:ProgramFiles\Docker\Docker\Docker Desktop.exe","$env:LocalAppData\Docker\Docker Desktop.exe") | Where-Object {Test-Path $_} | Select-Object -First 1
  if(!$exe){throw '找不到 Docker Desktop.exe'}
  Start-Process -FilePath $exe
  $deadline=(Get-Date).AddMinutes(10)
  while((Get-Date) -lt $deadline){
    if(Test-Docker){Write-Host 'Docker Engine 已就绪。'; return}
    Write-Host '等待 Docker Desktop / Linux Engine 启动中...'
    Start-Sleep -Seconds 5
  }
  throw 'Docker Engine 10分钟内没有就绪'
}
function Compose([string[]]$ComposeArgs){
  Push-Location $SqlRag
  try{
    docker compose --env-file .\.env -f .\docker-compose.yml @ComposeArgs
    if($LASTEXITCODE -ne 0){throw "docker compose $($ComposeArgs -join ' ') 失败"}
  }finally{Pop-Location}
}
if(!(Test-Path $Py)){throw "Python虚拟环境不存在：$Py"}
if(!(Test-Path $LlamaExe) -or !(Test-Path $ModelFile)){
  Write-Host '缺少模型文件或 llama-server，执行项目自带 prepare...'
  Push-Location $RepoRoot
  & $Py app\SQL_RAG\main.py qwen35-2b prepare
  if($LASTEXITCODE -ne 0){throw 'qwen35-2b prepare 失败'}
  Pop-Location
}
Set-EnvLine $EnvFile 'QWEN_AGENT_MODEL' 'Qwen3.5-2B-Q4_K_M'
Set-EnvLine $EnvFile 'QWEN_AGENT_MODEL_SERVER' 'http://127.0.0.1:18000/v1'
Set-EnvLine $EnvFile 'QWEN_AGENT_API_KEY' 'EMPTY'
Set-EnvLine $EnvFile 'QWEN_AGENT_MAX_TOKENS' '512'
Set-EnvLine $EnvFile 'QWEN_AGENT_TEMPERATURE' '0.1'
if($RestartModel -or !(Test-Qwen)){
  Write-Host '启动 Qwen3.5-2B 本机模型服务 18000...'
  $qwenPortReleased=Stop-Port @(18000)
  if(!$qwenPortReleased){throw 'Qwen 模型端口 18000 被旧高权限进程占用，无法重启模型服务'}
  Start-Sleep -Seconds 2
  $stamp=Get-Date -Format 'yyyyMMdd-HHmmss'
  $qout=Join-Path $LogDir "qwen-$stamp.out.log"
  $qerr=Join-Path $LogDir "qwen-$stamp.err.log"
  $qargs="-m `"$ModelFile`" --host 127.0.0.1 --port 18000 -c 8192 -t 6 -ngl 0 --temp 0.2 --top-p 0.8 -n 1024"
  $q=Start-Process -FilePath $LlamaExe -ArgumentList $qargs -WorkingDirectory $LlamaCwd -RedirectStandardOutput $qout -RedirectStandardError $qerr -WindowStyle Hidden -PassThru
  Wait-Qwen 180
}else{
  Write-Host 'Qwen 模型服务已存在，跳过启动。'
}
Ensure-Docker
Compose @('up','-d','sqlserver','qdrant','external-sqlserver','external-qdrant','neo4j')
Wait-Port '主SQL Server' 1433 420
Wait-Port '主Qdrant' 6333 240
Wait-Port 'External SQL Server' 14333 420
Wait-Port 'External Qdrant' 6334 240
Wait-Port 'Neo4j' 7474 300
if($RunDatabaseInit){
  Compose @('run','--rm','init-db')
  Compose @('run','--rm','init-external-db')
}
if($RebuildExternalQdrant){
  Push-Location $RepoRoot
  & $Py app\SQL_RAG\data_cleaning\test_External_database_connection_conversion\external_database_to_qdrant_conversion.py --recreate --source-profile $ExternalSourceProfile
  if($LASTEXITCODE -ne 0){throw 'sql_External_database 重建失败'}
  Pop-Location
}
$defaultPortsReleased=Stop-Port @($BackendPort,$WebPort)
if(!$defaultPortsReleased){
  Write-Warning '默认 18180/18181 被旧高权限进程占用，自动切换备用端口启动最新服务。'
  $BackendPort=Find-FreePort 18182
  $WebPort=Find-FreePort ($BackendPort+1)
  $BackendUrl="http://127.0.0.1:$BackendPort"
  $WebUrl="http://127.0.0.1:$WebPort"
  Write-Warning "本次最新后端使用 $BackendUrl，最新 WebUI 使用 $WebUrl。"
}
Start-Sleep -Seconds 2
$stamp=Get-Date -Format 'yyyyMMdd-HHmmss'
$berr=Join-Path $LogDir "backend-$stamp.err.log"
$bout=Join-Path $LogDir "backend-$stamp.out.log"
$werr=Join-Path $LogDir "webui-$stamp.err.log"
$wout=Join-Path $LogDir "webui-$stamp.out.log"
$backend=Start-Process -FilePath $Py -ArgumentList @('app\SQL_RAG\main.py','business-brain-service','--host','127.0.0.1','--port',"$BackendPort") -WorkingDirectory $RepoRoot -RedirectStandardOutput $bout -RedirectStandardError $berr -WindowStyle Hidden -PassThru
$web=Start-Process -FilePath $Py -ArgumentList @('app\SQL_RAG\agent_webUI\webui_server.py','--host','127.0.0.1','--port',"$WebPort",'--backend-url',$BackendUrl) -WorkingDirectory $RepoRoot -RedirectStandardOutput $wout -RedirectStandardError $werr -WindowStyle Hidden -PassThru
$backendReady=$false; $webReady=$false; $proxyReady=$false; $last=''
for($i=1;$i -le 90;$i++){
  try{$h=Invoke-RestMethod "$BackendUrl/agent/business-brain/health" -TimeoutSec 5; $last=$h|ConvertTo-Json -Depth 8; if($h.ready){$backendReady=$true}}catch{}
  try{$r=Invoke-WebRequest $WebUrl -TimeoutSec 5; if($r.StatusCode -eq 200){$webReady=$true}}catch{}
  try{$p=Invoke-RestMethod "$WebUrl/api/agent/business-brain/health" -TimeoutSec 5; if($p.ready){$proxyReady=$true}}catch{}
  if($backendReady -and $webReady -and $proxyReady){break}
  Start-Sleep -Seconds 2
}
Write-Host ''
Write-Host "Qwen模型：$(Test-Qwen)"
Write-Host "后端健康：$backendReady"
Write-Host "WebUI首页：$webReady"
Write-Host "WebUI代理健康：$proxyReady"
Write-Host "后端地址：$BackendUrl"
Write-Host "WebUI地址：$WebUrl"
Write-Host "后端错误日志：$berr"
Write-Host "WebUI错误日志：$werr"
Write-Host $last
if(!($backendReady -and $webReady -and $proxyReady)){throw '全量服务没有全部 ready，不能算完成'}
