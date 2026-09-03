# 第二套 `.233` WebUI 成功基线

日期：2026-09-03
部署包代码基线：`2bd3c7ed7754891df869bb6904a9e626117476ae`
成功记录提交：`b66162fbb26c111b4c015cc614d8bcc4ed99db14`
成功标签：`sqlrag-second-stack-webui-success-baseline-20260903`
修复包：`KM_KNOWLEDGE_STARTUP_NAS_REPAIR_20260903_EGRESS_PROXY_R2`
固定 profile：`server_second_ports`，目标：`172.18.1.233`

## 当前结论

本次三张 WebUI 截图证明第二套已经按第一套相同的业务链路完成真实解析：同一批 3 个音频均为 `100%`，结果为“成功 3 个、失败 0 个、解析成功”；知识库列表显示 `434` 条，详情页能够读回原始解析文本。该结论覆盖上传、NAS 回调、解析、持久化结果展示和详情回读，不是静态页面或单独健康接口的推断。

本次修复只在部署层处理第二套 Docker/WSL 外部 HTTPS 出口，并修正 Windows PowerShell 5.1 对泛型 `List[object]` 的返回值绑定。14 项载荷明确排除了解析/提取 Worker 源码、提示词、数据库/队列实现和 WebUI 业务代码；第一套 `.212` profile、容器、网络、卷和数据均未改动。

## 证据分层

### 真实 WebUI 证据

- 上传页：3 个文件全部 `100%`，每项显示解析成功；汇总为成功 3、失败 0。
- 知识库页：显示 `434` 条文档，新增记录时间为 2026-09-03 16:36--16:38。
- 详情页：可见标题、知识正文和“原始内容解析”，证明结果已持久化并可再次读取。

### 当前开发机可达的 `.233` 组件证据

采集时间：2026-09-03 17:30 左右。

| 地址 | 结果 |
| --- | --- |
| `http://172.18.1.233:28191/knowledgeManagement/` | HTTP 200 |
| `http://172.18.1.233:28191/knowledgeManagement/api/health` | HTTP 200，`ready=true`、数据库已配置、模型为 `FunAudioLLM/SenseVoiceSmall` |
| `http://172.18.1.233:28320/health` | HTTP 200 |
| `http://172.18.1.233:28321/health` | HTTP 200 |
| `http://172.18.1.233:28320/knowledge/nas/health` | HTTP 200，`ready=true`、`nasAdminReady=true`、`parseAgentReady=true`、`physicalRootReady=true` |

这些是当前页面/组件事实，不能替代目标机启动报告。当前开发机无法使用 WinRM 读取 `.233` 的 Docker、PgBouncer、Worker 和监听端口。

### 目标机采集报告（已收到）

目标机管理员在 Windows PowerShell 5.1 运行只读采集器，报告为
`SQLRAG-233-PersistenceEvidence-20260903-173257.txt`，`COLLECTOR_EXIT=0`，并确认
`DeploymentProfile=server_second_ports`、`DockerHost=npipe:////./pipe/docker_engine_linux`、`Mutation=NONE_READ_ONLY`。关键事实如下：

- Docker Linux Engine `DOCKER_VERSION_EXIT=0`，第二套容器均为 `Up`；PgBouncer 状态为 `healthy`。
- `PGBOUNCER_SQL_EXIT=0 VALUE=1`，真实 SQL 已通过。
- LLM 鉴权模型探针 `MODELS_STATUS=200`、`LLM_PROBE_EXIT=0`；Celery ping 显示 9 个节点在线。
- 端口合同 `ExpectedCount=33`、`ListeningExpectedCount=33`、`Missing` 为空。
- 当前成功任务 `8c748300-9197-4915-b481-f0553a880725` 为 `completed / WAITING_REVIEW / 100 / total=3 / completed=3 / failed=0`；3 个文件均为 `business_sync_verified`，`nas_verified`、`parse_completed`、`db_sync_verified` 全为真。

采集器的 HTTP 子段有几项使用 `127.0.0.1` 访问 LAN 绑定端口而显示连接失败；这不是服务未启动证据。开发机随后对 `.233` 实际地址的 `28191`、`28320`、`28321` 和 NAS 健康入口均得到 HTTP 200。报告同时保留旧任务的 58% 失败行，它们是历史数据，不影响上述新任务结论。报告中 Docker 日志读取还会出现 PowerShell `NativeCommandError` 包装和 Worker 的 `Event loop is closed` 清理警告，但对应任务和探针退出码均成功；这些是观测噪声/非致命警告，不能借此修改业务逻辑。

仍需单独安排一次“关机重启后重复固定入口”的冷启动复验，才能把重启可重复性从当前运行态成功提升为完整发布验收；在此之前，状态准确表述为“当前目标运行态与 WebUI 已通过，冷重启复验待执行”。历史的 `SQLRAG-233-PersistenceEvidence-20260902-175349.txt` 和冷启动网络报告只记录旧失败/启动前状态，不得当作当前成功状态。

## 为什么之前会停在 58%

旧报告的首个失败是 LLM Worker 在 `QA_EXTRACTING` 阶段的 `APITimeoutError`/`Request timed out`；容器桥接网络报 `No route to host`，而宿主机经已验证代理可得到供应商预期的 `401`。因此拥有故障的是第二套 Docker/WSL/NAT 出站路径，不是 NAS 路径、切分、提示词、数据库 schema、队列容量或提取算法。R2 只把已验证代理注入 `km-worker-llm`、`km-worker-asr`、`km-worker-vision`，并在实际商业网络再次探测；没有修改业务逻辑来掩盖网络故障。

## 下次重启时 PowerShell 为什么可能一片黑

一键链路会启动隐藏的 Python/Compose 子进程，父 PowerShell 对若干探针和健康门禁同步等待，服务进程的标准输出/错误也被重定向到运行目录日志。因此“窗口暂时没有文字”本身不是错误，也不是构建回退；它通常表示子进程仍在等待 Docker/健康门禁。QuickEdit/选中文本造成的暂停是次要可能性。判断依据应是进程、退出码和日志，而不是窗口颜色或是否有滚动文字。

日常启动使用固定入口并保留实时输出，不要用 `@(...)` 收集整个子进程输出，也不要重复运行安装器或重建 1534 基线：

```powershell
$ErrorActionPreference='Stop'
Remove-Item Env:DOCKER_CONTEXT -ErrorAction SilentlyContinue
$env:DOCKER_HOST='npipe:////./pipe/docker_engine_linux'
docker version
if($LASTEXITCODE -ne 0){throw 'Docker Linux Engine 不可用。'}
docker info --format 'SERVER={{.ServerVersion}} CONTAINERS={{.Containers}} RUNNING={{.ContainersRunning}}'
if($LASTEXITCODE -ne 0){throw 'Docker Linux Engine 尚未就绪。'}
& powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File 'D:\MonFangAI\GetDAM\ai-ie-backend\app\SQL_RAG\start-server-full-stack.ps1'
$secondStackExit=$LASTEXITCODE
Write-Host "SECOND_STACK_START_EXIT=$secondStackExit"
if($secondStackExit -ne 0){throw "第二套固定入口失败：exit=$secondStackExit"}
```

首次安装/更新才使用 R2 安装器的 `-ValidateOnly` 后 `-StartServices` 两步；日常关机重启直接执行上面的 `start-server-full-stack.ps1`。管理员 PowerShell 必须与 Docker Desktop 的普通交互用户会话保持一致。

## 保留制品

| 制品 | 字节 | SHA256 |
| --- | ---: | --- |
| `KM_KNOWLEDGE_STARTUP_NAS_REPAIR_20260902_1534.zip` | 2,366,827 | `AF8B69671450E984DDD28411C4DE43EC9960D3DE5670D0AFF26D4BDF27B55EE7` |
| `KM_SECOND_SERVER_FULL_SOURCE_SYNC_20260831_163555.zip` | 1,003,030,779 | `0D54F17BD1AEA1AB9BED1B53C84103BED283D7FD4888378FADB74969151A62F8` |
| `KM_KNOWLEDGE_STARTUP_NAS_REPAIR_20260903_EGRESS_PROXY_R2.zip` | 2,364,393 | `940704C648630DBB7067F1FCEC871F100A4B2A14531F1ECE3DC94BEF5825287E` |

1534 窄修复包依赖完整源同步底座；R2 是当前成功的部署层更新包。三者都保留，其他已明确失败或被 R2 取代的候选包按同目录的清理账册处理。

## 回滚与不变边界

回滚只使用保留的 1534、完整源同步底座和 R2 包；不删除源码、`.runtime`、Docker 卷、数据库、密钥或历史证据。若目标机最终验收报告缺项，状态应标为“WebUI 已成功、目标全量验收待补”，不得倒退修改解析业务逻辑。
