# -*- coding: utf-8 -*-
"""外部关系型数据库 adapter 注册入口。"""

# 2026-06-13 17:18:04 新增：导出基础 adapter 契约，作用是让 worker 只依赖统一接口；理由是不能为每个外部库改主链路。
from .base import ExternalAdapterRegistry, ExternalDbAdapter, ExternalDbConnectionConfig, resolve_profile_connection_config
# 2026-06-13 17:18:04 新增：导出 PostgreSQL adapter，作用是接入截图里的 krauss PG；理由是本次目标需要连接别人 PG 库。
from .postgres import PostgresExternalAdapter
# 2026-06-13 17:18:04 新增：导出 SQL Server adapter，作用是保留现有外部 SQL Server demo 能力；理由是新增 PG 不能破坏旧链路。
from .sqlserver import SqlServerExternalAdapter


# 2026-06-13 17:18:04 新增：构建默认 adapter registry，作用是用 engine 字符串找到对应 adapter；理由是避免业务代码无限 if 分支。
def build_default_external_adapter_registry() -> ExternalAdapterRegistry:
    # 2026-06-13 17:18:04 新增：创建 registry，作用是集中维护 adapter 工厂；理由是未来 MySQL/Oracle 只新增注册项。
    registry = ExternalAdapterRegistry()
    # 2026-06-13 17:18:04 新增：注册 postgresql，作用是支持截图中的 krauss PG；理由是 YAML connection.engine=postgresql 时要能自动选择。
    registry.register("postgresql", lambda config: PostgresExternalAdapter(config))
    # 2026-06-13 17:18:04 新增：注册 postgres 别名，作用是兼容人工 YAML 常见写法；理由是配置不应因为别名失败。
    registry.register("postgres", lambda config: PostgresExternalAdapter(config))
    # 2026-06-13 17:18:04 新增：注册 pg 别名，作用是兼容简写；理由是降低新外部库接入成本。
    registry.register("pg", lambda config: PostgresExternalAdapter(config))
    # 2026-06-13 17:18:04 新增：注册 sqlserver，作用是保留原 External_database SQL Server demo；理由是现有测试和旧命令不能失效。
    registry.register("sqlserver", lambda config: SqlServerExternalAdapter(config))
    # 2026-06-13 17:18:04 新增：注册 mssql 别名，作用是兼容 SQL Server 常见叫法；理由是配置层要宽容。
    registry.register("mssql", lambda config: SqlServerExternalAdapter(config))
    # 2026-06-13 17:18:04 新增：返回 registry，作用是交给 worker/manager 使用；理由是 adapter 选择集中化。
    return registry


# 2026-06-13 17:18:04 新增：声明公开符号，作用是让导入边界清晰；理由是维护时能一眼看到 adapter 层能力。
__all__ = [
    "ExternalAdapterRegistry",
    "ExternalDbAdapter",
    "ExternalDbConnectionConfig",
    "PostgresExternalAdapter",
    "SqlServerExternalAdapter",
    "build_default_external_adapter_registry",
    "resolve_profile_connection_config",
]
