# -*- coding: utf-8 -*-
"""PostgreSQL 外部库 adapter。"""

# 2026-06-13 17:18:04 新增：导入 Any，作用是标注 profile 和 row 的动态结构；理由是外部库字段由 YAML 决定。
from typing import Any

# 2026-06-13 17:18:04 新增：兼容 data_cleaning 直接运行和 SQL_RAG 包运行；作用是导入 profile SQL 工具；理由是测试和服务入口的 sys.path 不同。
try:
    # 2026-06-13 17:18:04 新增：按 data_cleaning 顶层导入；作用是兼容现有测试路径；理由是测试把 data_cleaning 放进 sys.path。
    from Qdrant import qdrant_mapping_profile
except ImportError:
    # 2026-06-13 17:18:04 新增：按 SQL_RAG 包路径导入；作用是兼容后端服务运行；理由是服务从 SQL_RAG 根目录启动。
    from data_cleaning.Qdrant import qdrant_mapping_profile

# 2026-06-13 17:18:04 新增：导入连接配置；作用是接收 registry 解析后的参数；理由是 adapter 不直接读取 YAML。
from .base import ExternalDbConnectionConfig


# 2026-06-13 17:18:04 新增：定义 PostgreSQL adapter；作用是连接并读取别人 PG 数据库；理由是截图目标库是 krauss PostgreSQL。
class PostgresExternalAdapter:
    # 2026-06-13 17:18:04 新增：初始化 adapter；作用是保存连接配置；理由是每个 profile 可对应不同外部 PG。
    def __init__(self, config: ExternalDbConnectionConfig) -> None:
        # 2026-06-13 17:18:04 新增：保存 config；作用是 fetch/update 时复用；理由是连接参数不应散落。
        self.config = config

    # 2026-06-13 17:18:04 新增：打开 PG 连接；作用是集中设置 psycopg row_factory；理由是读取结果必须是 dict。
    def _connect(self) -> Any:
        # 2026-06-13 17:18:04 新增：延迟导入 psycopg；作用是没有 PG 依赖时只在使用 PG 时失败；理由是 SQL Server 主链路不应受 PG 包影响。
        import psycopg
        # 2026-06-13 17:18:04 新增：导入 dict_row；作用是让 cursor.fetchall 返回 dict；理由是 profile row_to_canonical_chunk 统一消费字段名。
        from psycopg.rows import dict_row

        # 2026-06-13 17:18:04 新增：创建 PG 连接；作用是连接截图中的 krauss/postgres；理由是实时同步需要长周期反复查询。
        return psycopg.connect(
            # 2026-06-13 17:18:04 新增：设置 host；作用是连接外部 PG 主机；理由是 host 来自 .env。
            host=self.config.host,
            # 2026-06-13 17:18:04 新增：设置 port；作用是连接外部 PG 端口；理由是截图端口 5432。
            port=self.config.port,
            # 2026-06-13 17:18:04 新增：设置 dbname；作用是进入目标数据库；理由是截图初始数据库 postgres。
            dbname=self.config.database,
            # 2026-06-13 17:18:04 新增：设置 user；作用是认证；理由是截图账号 ai_ie_dev。
            user=self.config.user,
            # 2026-06-13 17:18:04 新增：设置 password；作用是认证；理由是密码从 .env 注入。
            password=self.config.password,
            # 2026-06-13 17:18:04 新增：设置 sslmode；作用是兼容局域网/远程 SSL；理由是不同 PG 连接策略不同。
            sslmode=self.config.sslmode,
            # 2026-06-13 17:18:04 新增：设置 row_factory；作用是返回 dict row；理由是后续字段名大小写必须保留。
            row_factory=dict_row,
        )

    # 2026-06-13 17:18:04 新增：读取外部 PG 行；作用是把 source_table/select.fields 转成结果集；理由是 Qdrant 同步源头在这里。
    def fetch_rows(self, profile: Any) -> list[dict[str, Any]]:
        # 2026-06-13 17:18:04 新增：读取 sync.where；作用是支持 YAML 限定同步范围；理由是不同外部库可能只同步部分行。
        where_clause = (getattr(profile, "sync", {}) or {}).get("where")
        # 2026-06-13 17:18:04 新增：构造 PG SELECT；作用是正确引用 public."AI_erp_Wendajilu" 和 "MiaoShu"；理由是 PG 大小写字段必须双引号。
        sql = qdrant_mapping_profile.build_select_sql(profile, dialect="postgresql", where_clause=where_clause)
        # 2026-06-13 17:18:04 新增：打开连接；作用是执行 SELECT；理由是每次轮询都要读取最新数据。
        with self._connect() as connection:
            # 2026-06-13 17:18:04 新增：创建 cursor；作用是执行参数化/普通查询；理由是 psycopg 操作入口。
            with connection.cursor() as cursor:
                # 2026-06-13 17:18:04 新增：执行 SELECT；作用是获取外部行；理由是 adapter 只负责读源数据。
                cursor.execute(sql)
                # 2026-06-13 17:18:04 新增：返回 dict 列表；作用是交给 profile 转 chunk；理由是后续不依赖 psycopg row 类型。
                return [dict(row) for row in cursor.fetchall()]

    # 2026-06-13 17:18:04 新增：回写单行同步状态；作用是把 ZhuangTai 更新成已入库；理由是用户要求每条 point 存好后回写外部 PG。
    def mark_row_synced(self, profile: Any, source_pk: Any, status_value: str) -> None:
        # 2026-06-13 17:18:04 新增：读取 sync 配置；作用是获得状态字段名；理由是不同外部库状态字段可能不叫 ZhuangTai。
        sync_config = getattr(profile, "sync", {}) or {}
        # 2026-06-13 17:18:04 新增：读取状态字段；作用是决定 UPDATE 哪一列；理由是回写字段必须由 YAML 控制。
        status_field = str(sync_config.get("status_field") or "").strip()
        # 2026-06-13 17:18:04 新增：没有状态字段时跳过；作用是兼容只读外部库；理由是不是所有外部库都允许回写。
        if not status_field:
            # 2026-06-13 17:18:04 新增：直接返回；作用是不执行 UPDATE；理由是 YAML 未声明就不应写外部库。
            return
        # 2026-06-13 17:18:04 新增：解析 schema/table；作用是生成 UPDATE 目标表；理由是 PG 大小写表名要引用。
        schema_name, table_name = qdrant_mapping_profile.split_source_table_for_dialect(profile.source_table, "postgresql")
        # 2026-06-13 17:18:04 新增：引用 schema/table；作用是构造安全 UPDATE；理由是表名来自配置但仍需按标识符处理。
        table_sql = f"{qdrant_mapping_profile.quote_sql_identifier(schema_name, 'postgresql')}.{qdrant_mapping_profile.quote_sql_identifier(table_name, 'postgresql')}"
        # 2026-06-13 17:18:04 新增：引用状态字段；作用是保留 ZhuangTai 大小写；理由是 PG 字段大小写敏感。
        status_sql = qdrant_mapping_profile.quote_sql_identifier(status_field, "postgresql")
        # 2026-06-13 17:18:04 新增：引用主键字段；作用是按 wdjl_id 定位行；理由是不能用普通 id 猜测主键。
        pk_sql = qdrant_mapping_profile.quote_sql_identifier(profile.id_field, "postgresql")
        # 2026-06-13 17:18:04 新增：构造参数化 UPDATE；作用是只把值作为参数传入；理由是避免中文状态值和主键转义问题。
        sql = f"UPDATE {table_sql} SET {status_sql} = %s WHERE {pk_sql} = %s"
        # 2026-06-13 17:18:04 新增：打开连接；作用是执行回写；理由是每条 point 成功后要同步状态。
        with self._connect() as connection:
            # 2026-06-13 17:18:04 新增：创建 cursor；作用是执行 UPDATE；理由是 psycopg 标准操作入口。
            with connection.cursor() as cursor:
                # 2026-06-13 17:18:04 新增：执行参数化 UPDATE；作用是写回已入库；理由是用户要求同步回 PG 的 ZhuangTai 字段。
                cursor.execute(sql, (status_value, source_pk))
            # 2026-06-13 17:18:04 新增：提交事务；作用是确保状态持久化到外部 PG；理由是回写成功才算一条 point 完成。
            connection.commit()
