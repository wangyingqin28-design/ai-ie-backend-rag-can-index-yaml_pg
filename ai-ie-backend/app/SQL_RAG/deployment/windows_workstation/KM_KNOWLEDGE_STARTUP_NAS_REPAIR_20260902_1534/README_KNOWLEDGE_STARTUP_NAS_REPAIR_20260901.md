# SQL_RAG 第二套网络终态修复

版本：`KM_KNOWLEDGE_STARTUP_NAS_REPAIR_20260902_1534`

本版本取代 `KM_KNOWLEDGE_STARTUP_NAS_REPAIR_20260902_1447` 及更早版本。旧版本不要再次执行。

## 已锁定的故障边界

最新目标证据证明 Docker Engine 29.6.2 正常、迁移 PostgreSQL 为 `running/healthy`，且数据库正确保留在 `sql-rag-server-migrated-source_default`。真正失败由两个部署状态共同造成：

- 1447 已正确把旧商业网络判定为 `recreate=True`，随后在端点所有权校验处首次执行 `docker inspect --format '{{ index .Config.Labels "com.docker.compose.project" }}'`。Windows PowerShell 5.1 将标签键的内层双引号剥离，Docker 实际收到 `{{ index .Config.Labels com.docker.compose.project }}`，因此报 `function "com" not defined`。该失败发生在容器删除、数据库断网和网络移除之前。
- 商业网络真实 IPAM 仍是旧的 `172.20.0.0/16`，1154 却输出 `recreate=False`。原因是 Windows PowerShell 5.1 将 `docker network inspect` 返回数组再次套入 `@()` 后形成单个 `System.Object[]`，启动器无法按名称找到商业网络。
- 同一健康数据库还历史性误接在 `sql-rag-server-km-commercial-internal`。Compose 自己发现 override 与旧网段不同并尝试移除网络，随后被该 active endpoint 阻断。

缓存网关输出 `Result=READY` 只表示镜像预检成功，不表示 36 个商业服务已启动。正式就绪必须以后文结构化成功字段为准。

## 本版本确切修复

- 取消端点项目标签的 Docker Go-template 调用，改为读取完整 `docker inspect` JSON，并从 `Config.Labels` 结构化读取 `com.docker.compose.project`；不再依赖 PowerShell 5.1 的原生双引号传递。
- 在 Windows PowerShell 5.1 中显式逐项展开全部 Docker 网络文档。旧 `172.20.0.0/16` 必须判定 `recreate=True`，正确 `10.253.233.0/24` 必须判定 `recreate=False`。
- 旧网段重建时继续沿用已验证的精确商业容器清理，只断开迁移 PostgreSQL 的错误商业 bridge；数据库容器、进程、私网和命名卷均保留。
- 即使网段已经正确，也在 PgBouncer `compose create` 前交叉读取数据库容器侧网络与商业网络侧 endpoint。只有两侧一致、数据库 `running/healthy` 且仍有 profile 私网时才断开历史错网，断开后再次双向回读。
- 保留 PgBouncer `create` 前、`create` 后、`start` 后的 NetworkID、别名和 active endpoint 门禁，不再把部署网络错误拖成 WebUI 502 或解析超时。
- 启动器保持原有第一套路径和业务解析链不变。载荷不包含提取算法、提示词、数据库、队列、Worker 业务源码、Docker 卷、业务数据或凭据。

## 关机重启承诺边界

在 Docker Linux Engine API 正常的前提下，本修复具备冷重启幂等性：第一次遇到旧 `172.20` 会受控重建为 `10.253.233`；以后重复一键或关机重启会重新读取真实 IPAM，正确时不重建，只核对数据库和 PgBouncer endpoint、NetworkID、别名与运行态。任何状态不一致都会在完整服务图之前具名失败，不会伪报“就绪”。

## 目标机固定执行顺序

目标机 `172.18.1.233` 的 Docker Engine 和最终网络证据已经完成只读取证。管理员 Windows PowerShell 5.1 先执行包内验证：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "\\win2024-server\项目升级文件\王映钦\王映钦_ERP\SQL_RAG_packages\win11_workstation\KM_KNOWLEDGE_STARTUP_NAS_REPAIR_20260902_1534\Install-MonFangAiKnowledgeStartupNasRepair.ps1" -SuiteRoot "D:\MonFangAI\GetDAM" -ValidateOnly
```

必须看到 `Result=READY`、`Mode=validate_only`、`PayloadFiles=14`、`CommercialNetworkSubnet=10.253.233.0/24`、`BusinessParsingFilesChanged=0` 后，才执行正式安装和第二套原固定入口：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "\\win2024-server\项目升级文件\王映钦\王映钦_ERP\SQL_RAG_packages\win11_workstation\KM_KNOWLEDGE_STARTUP_NAS_REPAIR_20260902_1534\Install-MonFangAiKnowledgeStartupNasRepair.ps1" -SuiteRoot "D:\MonFangAI\GetDAM" -StartServices
```

正式成功必须同时满足：`ServicesStarted=true`、`PgBouncerHealth=healthy`、`PgBouncerSelectValue=1`、`LlmModelsStatus=200`、`HttpHealthCount=4`、`PortContract=33`、`BusinessParsingFilesChanged=0`，然后再用 Codex 内置 Knowledge WebUI 做真实请求验收。

## 验证状态

本地启动与验证合同：`35 passed`；商业启动器 Windows PowerShell 5.1 AST：`0` 个错误；PS5.1 原生参数探针已复现旧模板丢失双引号，结构化 Docker JSON 标签读取、多网络数组、旧网段重建和正确网段幂等跳过夹具均已通过；本次新增 PowerShell 行注释审计通过。全局历史注释套件仍为 `7 failed, 3 passed`，失败位于未改业务文件、旧共享引擎行或缺失的外部仓库。目标 `.233` 正式启动、冷重启和真实 Knowledge WebUI 文件解析仍需现场验收，不能由本地测试替代。
