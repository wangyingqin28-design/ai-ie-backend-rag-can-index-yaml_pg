# -*- coding: utf-8 -*-
"""SQL Server 外部库 adapter。"""

# 2026-06-13 17:18:04 新增：导入 Any，作用是标注 profile 和 row 的动态结构；理由是 SQL Server 外部库字段同样由 YAML 决定。
from typing import Any

# 2026-06-13 17:18:04 新增：兼容 data_cleaning 直接运行和 SQL_RAG 包运行；作用是导入 profile SQL 工具；理由是测试和服务入口的 sys.path 不同。
try:
    # 2026-06-13 17:18:04 新增：按 data_cleaning 顶层导入；作用是兼容现有外部转换脚本；理由是旧脚本从 data_cleaning 根目录运行。
    from Qdrant import qdrant_mapping_profile
except ImportError:
    # 2026-06-13 17:18:04 新增：按 SQL_RAG 包路径导入；作用是兼容后端服务启动；理由是服务从 SQL_RAG 根目录导入 data_cleaning。
    from data_cleaning.Qdrant import qdrant_mapping_profile

# 2026-06-13 17:18:04 新增：导入连接配置；作用是接收 registry 解析后的 SQL Server 参数；理由是 adapter 不直接读 YAML。
from .base import ExternalDbConnectionConfig


# 2026-06-13 17:18:04 新增：定义 SQL Server adapter；作用是保留原 External_database SQL Server 读取能力；理由是新增 PG 不能破坏旧外部库。
class SqlServerExternalAdapter:
    # 2026-06-13 17:18:04 新增：初始化 adapter；作用是保存连接配置；理由是每个 profile 可独立连接不同 SQL Server。
    def __init__(self, config: ExternalDbConnectionConfig) -> None:
        # 2026-06-13 17:18:04 新增：保存 config；作用是 fetch/update 时复用；理由是连接参数要集中管理。
        self.config = config

    # 2026-06-13 17:18:04 新增：构造 SQL Server ODBC 连接串；作用是连接外部 SQL Server；理由是 worker 不应该知道驱动细节。
    def _connection_string(self) -> str:
        # 2026-06-13 17:18:04 新增：返回 ODBC 连接串；作用是兼容本地 Docker SQL Server 和外部 SQL Server；理由是 pyodbc 只消费字符串。
        return (
            # 2026-06-13 17:18:04 新增：写入 ODBC 驱动；作用是选择本机安装的 SQL Server driver；理由是不同机器驱动名可配置。
            f"DRIVER={{{self.config.driver}}};"
            # 2026-06-13 17:18:04 新增：写入 host/port；作用是定位 SQL Server；理由是外部库可能不在本机。
            f"SERVER={self.config.host},{self.config.port};"
            # 2026-06-13 17:18:04 新增：写入数据库名；作用是进入目标库；理由是一份 profile 对应一个目标库。
            f"DATABASE={self.config.database};"
            # 2026-06-13 17:18:04 新增：写入用户名；作用是认证；理由是外部库账号由 .env/YAML 控制。
            f"UID={self.config.user};"
            # 2026-06-13 17:18:04 新增：写入密码；作用是认证；理由是密码不散落到业务代码里。
            f"PWD={self.config.password};"
            # 2026-06-13 17:18:04 新增：信任证书；作用是兼容本地和内网 SQL Server；理由是测试环境常用自签证书。
            "TrustServerCertificate=yes;"
            # 2026-06-13 17:18:04 新增：关闭加密；作用是兼容当前 Docker SQL Server；理由是旧链路使用相同连接策略。
            "Encrypt=no;"
        )

    # 2026-06-13 17:18:04 新增：打开 SQL Server 连接；作用是集中延迟导入 pyodbc；理由是未用 SQL Server 时不影响 PG 路径。
    def _connect(self) -> Any:
        # 2026-06-13 17:18:04 新增：延迟导入 pyodbc；作用是只有使用 SQL Server adapter 时才加载驱动；理由是 PG 同步不依赖 ODBC。
        import pyodbc

        # 2026-06-13 17:18:04 新增：返回连接；作用是执行 SELECT/UPDATE；理由是 adapter 封装数据库访问。
        return pyodbc.connect(self._connection_string(), timeout=10)

    # 2026-06-13 17:18:04 新增：读取外部 SQL Server 行；作用是把 YAML select.fields 转成 dict rows；理由是 worker 统一消费 dict。
    def fetch_rows(self, profile: Any) -> list[dict[str, Any]]:
        # 2026-06-13 17:18:04 新增：读取 sync.where；作用是支持 YAML 限定同步范围；理由是不同外部库可能只同步部分数据。
        where_clause = (getattr(profile, "sync", {}) or {}).get("where")
        # 2026-06-13 17:18:04 新增：构造 SQL Server SELECT；作用是沿用方括号引用；理由是保留旧 External_database 语义。
        sql = qdrant_mapping_profile.build_select_sql(profile, dialect="sqlserver", where_clause=where_clause)
        # 2026-06-13 17:18:04 新增：打开连接；作用是读取最新外部行；理由是后台同步每轮都要看源库状态。
        with self._connect() as connection:
            # 2026-06-13 17:18:04 新增：创建 cursor；作用是执行查询；理由是 pyodbc 标准操作入口。
            cursor = connection.cursor()
            # 2026-06-13 17:18:04 新增：执行 SELECT；作用是获取外部库行；理由是 adapter 是同步源入口。
            cursor.execute(sql)
            # 2026-06-13 17:18:04 新增：读取列名；作用是把 pyodbc.Row 转 dict；理由是 profile 转换按字段名读取。
            columns = [column[0] for column in cursor.description]
            # 2026-06-13 17:18:04 新增：返回 dict rows；作用是交给统一 chunk 转换；理由是 worker 不依赖 pyodbc.Row。
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    # 2026-06-13 17:18:04 新增：回写单行同步状态；作用是支持 SQL Server 外部库也能写回状态；理由是回写能力应跟 adapter 统一。
    def mark_row_synced(self, profile: Any, source_pk: Any, status_value: str) -> None:
        # 2026-06-13 17:18:04 新增：读取 sync 配置；作用是获得状态字段名；理由是不同库状态字段名不固定。
        sync_config = getattr(profile, "sync", {}) or {}
        # 2026-06-13 17:18:04 新增：读取状态字段；作用是决定 UPDATE 哪列；理由是未声明状态字段时不能乱写外部库。
        status_field = str(sync_config.get("status_field") or "").strip()
        # 2026-06-13 17:18:04 新增：没有状态字段就跳过；作用是兼容只读外部库；理由是有些外部库只给 SELECT 权限。
        if not status_field:
            # 2026-06-13 17:18:04 新增：直接返回；作用是不执行 UPDATE；理由是 YAML 未声明时不主动写源库。
            return
        # 2026-06-13 17:18:04 新增：解析 schema/table；作用是生成 UPDATE 目标表；理由是 SQL Server 表名需要方括号引用。
        schema_name, table_name = qdrant_mapping_profile.split_source_table_for_dialect(profile.source_table, "sqlserver")
        # 2026-06-13 17:18:04 新增：引用表名；作用是构造安全 UPDATE；理由是表名来自 profile，不能裸拼。
        table_sql = f"{qdrant_mapping_profile.quote_sql_identifier(schema_name, 'sqlserver')}.{qdrant_mapping_profile.quote_sql_identifier(table_name, 'sqlserver')}"
        # 2026-06-13 17:18:04 新增：引用状态字段；作用是保留字段名；理由是字段由 YAML 管理。
        status_sql = qdrant_mapping_profile.quote_sql_identifier(status_field, "sqlserver")
        # 2026-06-13 17:18:04 新增：引用主键字段；作用是按原始主键定位行；理由是 point id 不等于关系库主键。
        pk_sql = qdrant_mapping_profile.quote_sql_identifier(profile.id_field, "sqlserver")
        # 2026-06-13 17:18:04 新增：构造参数化 UPDATE；作用是写回同步状态；理由是中文状态值必须走参数。
        sql = f"UPDATE {table_sql} SET {status_sql} = ? WHERE {pk_sql} = ?"
        # 2026-06-13 17:18:04 新增：打开连接；作用是执行回写；理由是每条 point 成功后要状态持久化。
        with self._connect() as connection:
            # 2026-06-13 17:18:04 新增：执行 UPDATE；作用是写回状态；理由是同步完成要反馈给源库。
            connection.cursor().execute(sql, status_value, source_pk)
            # 2026-06-13 17:18:04 新增：提交事务；作用是确保状态落库；理由是未提交会导致下轮重复同步。
            connection.commit()
