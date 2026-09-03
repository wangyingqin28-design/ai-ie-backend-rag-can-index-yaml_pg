# 第二套 58% 出站修复候选包

版本：`KM_KNOWLEDGE_STARTUP_NAS_REPAIR_20260903_EGRESS_PROXY`

本候选包以 `sqlrag-second-stack-1534-build-data-network-baseline-20260902`（提交
`fcdfd2cc29e5c59aad87d988eb8ff9e0d086a085`）为唯一基础，只增加第二套 Docker
模型 Worker 的外部 HTTPS 出口门禁和代理覆盖。`1534` 原包、完整源同步底座和第一套
`.212` 运行时均保持不变。

## 已实锤的首个失败点

`SQLRAG-233-PersistenceEvidence-20260902-175349.txt` 证明 NAS 上传/回调、PostgreSQL、
PgBouncer、RabbitMQ、Outbox 和 Worker 队列均已走通；任务在 `QA_EXTRACTING` 约 58% 的
第一个业务失败是 LLM Worker `APITimeoutError` / `Request timed out.`。`.233` 容器直连
公网出现 `No route to host` 或超时，而宿主经 `192.168.65.7:3128` 访问 SiliconFlow
得到预期 `401`。因此故障所有者是第二套 Docker/WSL/NAT 出站路径，不是 NAS、提取算法、
提示词、数据库 schema 或队列业务代码。

浏览器当前若显示 `ERR_CONNECTION_REFUSED`，只表示 `.233:28191` 没有监听（例如 Docker
尚未启动或服务已停止），不能据此判定本候选包失败。

## 本候选包的窄修复

- `Start-KnowledgeCommercialServices.ps1` 从第二套 profile 读取代理候选，先在 Docker
  `bridge` 中用实际 Worker 镜像探测 `https://api.siliconflow.cn/v1/models`，只接受
  `200/401/403`。
- 探针通过 `.NET ProcessStartInfo` 显式附着 stdin，并使用 `--interactive`；嵌入脚本为
  ASCII，避免 Windows PowerShell 5.1 代码页把中文注释传给 Python 时产生伪网络失败。
- 商业网络创建 `km-pgbouncer` 后，用相同镜像、代理和 `NO_PROXY` 在真实
  `sql-rag-server-km-commercial-internal` 网络再探一次。任一探针失败都在部署层停止，
  不创建完整服务图，不把问题拖到 58% 任务阶段。
- 仅给 `km-worker-llm`、`km-worker-asr`、`km-worker-vision` 生成运行目录内的
  `docker-compose.egress.override.yml`，注入标准大写 `HTTP_PROXY`、`HTTPS_PROXY`、
  `ALL_PROXY`、`NO_PROXY`；RabbitMQ、Redis、MinIO、PgBouncer、持久化和索引服务不变。
- `server-second-ports-profile.json` 保存候选代理和内部绕行名单；安装器在写目标前验证
  profile、14 项 payload、哈希、PowerShell AST 和代理合同。

未修改：解析/提取 Worker 源码、提示词、数据库/队列实现、WebUI 业务流程、第一套 profile、
第一套容器/网络/卷和任何业务数据。

## 本机验证（组件证据）

- Windows PowerShell 5.1 商业启动器 AST：`0` 个错误。
- PowerShell 5.1 与 PowerShell 7 的真实 `sql-rag-knowledge-worker:commercial` 探针：
  `PROXY_HTTP_STATUS=401`，退出码 `0`。
- 同一探针在现有商业网络 `sql-rag-km-commercial-internal`：`401`，退出码 `0`。
- 启动器聚焦回归和 `git diff --check` 必须在生成 ZIP 前再次通过。

这些是本机/组件结果，不能替代 `.233` 目标机和 Codex 内置浏览器的端到端验收。

## `.233` 执行顺序

请在目标机管理员 Windows PowerShell 5.1 中，先确认 Docker Linux Engine 已完全 Running：

```powershell
$ErrorActionPreference='Continue'
Remove-Item Env:DOCKER_CONTEXT -ErrorAction SilentlyContinue
$env:DOCKER_HOST='npipe:////./pipe/docker_engine_linux'
docker version
docker info --format 'SERVER={{.ServerVersion}} CONTAINERS={{.Containers}} RUNNING={{.ContainersRunning}}'
```

两条命令都必须退出 `0`，且不能返回 HTTP 500。然后只对新候选目录执行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "\\win2024-server\项目升级文件\王映钦\王映钦_ERP\SQL_RAG_packages\win11_workstation\KM_KNOWLEDGE_STARTUP_NAS_REPAIR_20260903_EGRESS_PROXY\Install-MonFangAiKnowledgeStartupNasRepair.ps1" -SuiteRoot "D:\MonFangAI\GetDAM" -ValidateOnly
```

必须看到 `Result=READY`、`PayloadFiles=14`、`CommercialNetworkSubnet=10.253.233.0/24`、
`BusinessParsingFilesChanged=0`。通过后再执行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "\\win2024-server\项目升级文件\王映钦\王映钦_ERP\SQL_RAG_packages\win11_workstation\KM_KNOWLEDGE_STARTUP_NAS_REPAIR_20260903_EGRESS_PROXY\Install-MonFangAiKnowledgeStartupNasRepair.ps1" -SuiteRoot "D:\MonFangAI\GetDAM" -StartServices
```

日志必须同时出现 `KNOWLEDGE_COMMERCIAL_EGRESS_PROXY_READY` 和
`KNOWLEDGE_COMMERCIAL_EGRESS_PROXY_NETWORK_READY`。正式目标验收还必须有：
`ServicesStarted=true`、PgBouncer `healthy`、真实 `SELECT 1` 为 `1`、LLM `/models` 为
`200`、四个 HTTP 健康入口为 `200`、33 个端口监听，以及同一 Codex 内置浏览器中的真实
知识文件请求超过 58% 并持久化完成。关机重启后重复上述固定入口，需再次满足同一门槛。

## 存储与回滚边界

在目标机验收通过前，保留 `1534` 成功包和
`KM_SECOND_SERVER_FULL_SOURCE_SYNC_20260831_163555.zip`；本候选包与失败日志单独列账。
不得删除源码、运行目录、Docker 卷、数据库、密钥或唯一完整重建底座。只有目标验收通过、
并确认候选包已取代旧失败候选后，才按精确路径、字节数和 SHA256 sidecar 清理过期包。
