# `.233` 第二套 GitHub 可恢复基线

建立时间：2026-09-03 18:03:27 +08:00

仓库：`https://github.com/wangyingqin28-design/ai-ie-backend-rag-can-index-yaml_pg`

## 固定发布边界

这份发布只记录已经通过真实 WebUI 和目标机报告的第二套成功组合：

1. `KM_SECOND_SERVER_FULL_SOURCE_SYNC_20260831_163555.zip`：第一套同源业务/部署逻辑的完整源同步底座。
2. `KM_KNOWLEDGE_STARTUP_NAS_REPAIR_20260902_1534.zip`：1534 构建、数据、网络基线窄包。
3. `KM_KNOWLEDGE_STARTUP_NAS_REPAIR_20260903_EGRESS_PROXY_R2.zip`：只修复 `.233` Docker/WSL 外部 HTTPS 出口和 Windows PowerShell 5.1 启动器绑定。

R2 没有修改解析、提取、提示词、数据库、队列、持久化或 WebUI 业务逻辑；第一套 `.212` 的运行态也不在发布范围内。

## 字节校验

| 文件 | 字节 | SHA256 |
| --- | ---: | --- |
| `KM_SECOND_SERVER_FULL_SOURCE_SYNC_20260831_163555.zip` | 1003030779 | `0D54F17BD1AEA1AB9BED1B53C84103BED283D7FD4888378FADB74969151A62F8` |
| `KM_KNOWLEDGE_STARTUP_NAS_REPAIR_20260902_1534.zip` | 2366827 | `AF8B69671450E984DDD28411C4DE43EC9960D3DE5670D0AFF26D4BDF27B55EE7` |
| `KM_KNOWLEDGE_STARTUP_NAS_REPAIR_20260903_EGRESS_PROXY_R2.zip` | 2364393 | `940704C648630DBB7067F1FCEC871F100A4B2A14531F1ECE3DC94BEF5825287E` |

1GB 全量源同步包不进入普通 Git 对象，避免 GitHub 单文件限制和仓库膨胀；它会作为同一发布的 Release asset 上传。两个小包和所有源同步边界/清单文件进入 Git 提交。Release asset 与 sidecar 的哈希必须和本表一致。

## 恢复方式

```powershell
git clone --branch codex/second-stack-success-baseline-20260903 --single-branch https://github.com/wangyingqin28-design/ai-ie-backend-rag-can-index-yaml_pg.git
git -C ai-ie-backend-rag-can-index-yaml_pg rev-parse HEAD
```

然后从 GitHub Release `sqlrag-second-stack-success-baseline-20260903` 下载全量源同步 ZIP 及其 `.sha256`，在 Windows PowerShell 5.1 中先执行 `Get-FileHash` 比对本表，再按 `README_FIRST_SET_FULL_SOURCE_SYNC_20260831.md`、1534 README、R2 README 的顺序安装。日常重启不重复安装，直接使用固定入口：

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

## 验收边界

当前已通过：`.233` 真实 WebUI 3 个音频 100%（成功 3、失败 0）、知识库 434 条及详情回读；目标报告已通过 Docker Linux Engine、PgBouncer/`SELECT 1`、LLM `/models`、Celery 9 节点和 33/33 监听。旧 58% 任务是历史记录。

尚未通过的唯一发布门：目标机“关机重启后直接执行固定入口”的冷启动重复验收。完成前不能把重启可重复性写成已验证。
