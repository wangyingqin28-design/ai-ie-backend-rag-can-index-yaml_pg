#!/usr/bin/env bash
# 2026-06-11 19:42:30 新增原因：启用严格模式，作用是 External_database 初始化失败时立即退出，避免误以为三条数据已写入。
set -euo pipefail

# 2026-06-11 19:42:30 新增原因：优先使用 SQL Server 2022 镜像中的 mssql-tools18，作用是兼容新版容器。
SQLCMD="/opt/mssql-tools18/bin/sqlcmd"
# 2026-06-11 19:42:30 新增原因：mssql-tools18 默认要求证书参数，作用是本地自签证书场景仍可连接。
SQLCMD_EXTRA=(-C)

# 2026-06-11 19:42:30 新增原因：兼容部分镜像只带旧版 mssql-tools 的情况，作用是降低 Docker 镜像差异风险。
if [ ! -x "$SQLCMD" ]; then
  # 2026-06-11 19:42:30 新增原因：回退旧版 sqlcmd 路径，作用是继续完成 External_database 初始化。
  SQLCMD="/opt/mssql-tools/bin/sqlcmd"
  # 2026-06-11 19:42:30 新增原因：旧版 sqlcmd 不支持 -C，作用是避免参数错误。
  SQLCMD_EXTRA=()
# 2026-06-11 19:42:30 新增原因：结束 sqlcmd 路径兼容判断，作用是让后续命令使用最终可执行文件。
fi

# 2026-06-11 19:42:30 新增原因：输出初始化目标，作用是 docker logs 能看清本次处理的库和用户。
echo "[sql-rag-external] Initializing database ${EXTERNAL_DB_NAME} and login ${EXTERNAL_DB_USER}"

# 2026-06-11 19:42:30 新增原因：通过 Docker 内部服务名 external-sqlserver 连接外部库 SQL Server，作用是和原 sqlserver 服务隔离。
"$SQLCMD" \
  -S external-sqlserver \
  -U sa \
  -P "$EXTERNAL_MSSQL_SA_PASSWORD" \
  "${SQLCMD_EXTRA[@]}" \
  -v EXTERNAL_DB_NAME="$EXTERNAL_DB_NAME" EXTERNAL_DB_USER="$EXTERNAL_DB_USER" EXTERNAL_DB_PASSWORD="$EXTERNAL_DB_PASSWORD" \
  -i /init/init-external-db.sql

# 2026-06-11 19:42:30 新增原因：输出完成信息，作用是验收时确认初始化容器正常结束。
echo "[sql-rag-external] External_database initialization completed"
