# 第二套 1534 构建、数据与网络里程碑

## 结论边界

`KM_KNOWLEDGE_STARTUP_NAS_REPAIR_20260902_1534` 已在 `172.18.1.233` 真实目标机跨过此前反复失败的构建、依赖闭包、数据恢复、固定商业网络、36 服务启动和最终就绪合同阶段。这是必须冻结的部署阶段成功基线，不等于 WebUI 端到端验收完成。

当前仍有两个相互独立的未完成项：

1. 安装器第 285 行在可见健康文本为 `healthy` 时仍抛出 `PgBouncer 未健康`。本机 Windows PowerShell 5.1 已证明字符串、字符码、无空格运算符及比较表达式本身正常，下一步必须读取目标机该次 `docker inspect` 的原生退出码和完整 JSON，不能猜测后改包。
2. 三个真实 NAS 文件均已到达 `parsed_queued_for_persistence`，WebUI 显示 58% 和 `Request timed out`，但完成数仍为 0。该状态说明 NAS 解析已完成，首个待证明的分歧位于 `km.persist.business` Outbox、persist Worker、后续 LLM Worker或文件阶段事务，而不是构建、NAS 路径或页面健康入口。

在上述首个运行态分歧被当前证据证明前，不得重建、替换或回滚 `1534`，不得重跑早期部署阶段，也不得修改解析、提取、提示词、数据库、队列或 Worker 业务逻辑。

## 不可变制品

| 制品 | 字节 | SHA256 |
| --- | ---: | --- |
| `KM_KNOWLEDGE_STARTUP_NAS_REPAIR_20260902_1534.zip` | 2,366,827 | `AF8B69671450E984DDD28411C4DE43EC9960D3DE5670D0AFF26D4BDF27B55EE7` |
| `Install-MonFangAiKnowledgeStartupNasRepair.ps1` | 50,017 | `9ACD352DEA9CB2ED47940DEBF4002CAF110F210D9000901840E4A8270F4DC88D` |
| `Start-KnowledgeCommercialServices.ps1` | 149,365 | `3AD843099292A2301F2540EFF4C31C5AFE539E4857AF70D6D29FBBF56FD1FFE9` |

本地和共享路径逐文件读回哈希一致：

`\\win2024-server\项目升级文件\王映钦\王映钦_ERP\SQL_RAG_packages\win11_workstation\KM_KNOWLEDGE_STARTUP_NAS_REPAIR_20260902_1534`

完整重建底座保留 `KM_SECOND_SERVER_FULL_SOURCE_SYNC_20260831_163555.zip`，字节数 `1,003,030,779`，SHA256 `0D54F17BD1AEA1AB9BED1B53C84103BED283D7FD4888378FADB74969151A62F8`。`1534` 是 14 文件窄修复包，不能单独替代完整底座。

## 已关闭的首个分歧

1. Windows PowerShell 5.1 将多网络 JSON 包成单个 `System.Object[]`，导致网络重建判断假阴性。修复后显式展开数组再比较单一 IPAM 配置。
2. 迁移 PostgreSQL 保留在旧商业网络的孤儿 endpoint，导致 `docker network rm` 报 active endpoints。修复只断开已证明属于当前商业网络的历史 endpoint，保留数据库容器、私网和卷。
3. Windows PowerShell 5.1 调用 Docker Go template 时丢失带点标签键的内层引号，Docker 报 `function "com" not defined`。修复读取完整 `docker inspect` JSON，并通过 `Config.Labels` 结构化访问 Compose 标签。
4. 第二套商业网络固定为 `10.253.233.0/24`，避开宿主 `172.20.192.1` 与旧 Docker 自动分配 `172.20.0.0/16` 的路由冲突。

这些修复只修改部署生命周期所有者：

- `Knowledge_management/backend/large-scale_commercialization_upgrade/until/Start-KnowledgeCommercialServices.ps1`
- `Knowledge_management/tests/test_full_stack_launcher.py`

制品清单明确记录：`business_parsing_files_changed=0`、`business_extraction_files_changed=0`、`database_queue_worker_files_changed=0`、`first_stack_network_profile_changed=false`。

## 已通过证据

- Windows PowerShell 5.1 AST：0 错误。
- 启动器聚焦回归：35/35 通过。
- 本地与 UNC payload 哈希：14/14 一致。
- ZIP 解包与归档哈希：22/22 一致。
- `.233` 数据恢复：PostgreSQL 18 表、5,534 行；Qdrant 75 points。
- `.233` 最终就绪合同中的 36 项服务为真，商业子网为 `10.253.233.0/24`。
- 当前 `.233` 与 `.212` 对应的后端、WebUI、WebUI 代理和统一挂载四个 HTTP 健康入口均返回 200。
- 全局历史注释套件仍为 7 failed / 3 passed，失败位于本次未改的历史文件，不属于此里程碑。

## 为什么同样业务逻辑仍出现差异

第一套与第二套共享业务代码不代表运行态必然相同。第二套已经证明部署与健康入口一致，但截图中的状态停在 NAS 回调写入 `parsed_queued_for_persistence` 之后。此后结果取决于当前 profile 自己的 PostgreSQL Outbox、RabbitMQ 队列、persist/LLM Worker、对象存储和外部模型调用。任一运行态消息未发布、未消费、租约未取得或 Worker 异常，都会让相同业务代码在第二套停留于 58%。因此必须比较同一阶段的数据库事实和 Worker 日志，而不能再次改业务代码。

## 固定续接顺序

1. 保持当前 `.233` 服务和三个失败文件不变，保存 jobId/fileId 作为同一证据样本。
2. 一次性采集 PgBouncer 完整 inspect JSON、原生退出码、健康日志、网络、33 端口和四个 HTTP 入口。
3. 读取最近任务、文件、阶段检查点、Outbox 的状态，并抓取 persist、LLM、control、API、RabbitMQ 日志尾部。
4. 对照 `.212` 同名 Worker、队列绑定、环境差异和已成功任务的同阶段事实，确定第一处分歧。
5. 只在拥有层修复；先跑组件回归，再以同一 jobId 恢复，最后才做真实 WebUI 热验证和关机重启后的冷验证。

Git 固定标签：`sqlrag-second-stack-1534-build-data-network-baseline-20260902`。
