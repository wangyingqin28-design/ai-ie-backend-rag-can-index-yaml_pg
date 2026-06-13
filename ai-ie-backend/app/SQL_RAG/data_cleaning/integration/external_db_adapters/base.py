# -*- coding: utf-8 -*-
"""外部关系型数据库 adapter 基础契约。"""

# 2026-06-13 17:18:04 新增：导入 os，作用是从环境变量读取连接密钥；理由是密码不能写死在 YAML 里。
import os
# 2026-06-13 17:18:04 新增：导入 dataclass，作用是定义不可变连接配置；理由是 adapter 连接参数要稳定传递。
from dataclasses import dataclass
# 2026-06-13 17:18:04 新增：导入 Protocol，作用是声明 adapter 必须实现的接口；理由是 worker 不关心具体数据库类型。
from typing import Any, Callable, Protocol


# 2026-06-13 17:18:04 新增：定义外部库连接配置；作用是统一 PG/SQL Server 的连接参数；理由是不能在 worker 里按库类型拆字段。
@dataclass(frozen=True)
class ExternalDbConnectionConfig:
    # 2026-06-13 17:18:04 新增：保存数据库引擎，作用是选择 adapter；理由是 YAML 只需要声明 engine。
    engine: str
    # 2026-06-13 17:18:04 新增：保存主机，作用是连接外部数据库；理由是截图提供 krauss 主机。
    host: str
    # 2026-06-13 17:18:04 新增：保存端口，作用是连接外部数据库；理由是 PG 默认 5432 但仍需配置。
    port: int
    # 2026-06-13 17:18:04 新增：保存数据库名，作用是连接指定库；理由是截图数据库为 postgres。
    database: str
    # 2026-06-13 17:18:04 新增：保存用户名，作用是认证外部库；理由是截图用户为 ai_ie_dev。
    user: str
    # 2026-06-13 17:18:04 新增：保存密码，作用是认证外部库；理由是运行时从 .env 读取，避免 YAML 明文。
    password: str
    # 2026-06-13 17:18:04 新增：保存 SSL 模式，作用是兼容局域网/远程 PG；理由是不同外部库 SSL 要求不同。
    sslmode: str = "prefer"
    # 2026-06-13 17:18:04 新增：保存 SQL Server ODBC 驱动，作用是兼容旧 SQL Server adapter；理由是 PG 和 SQL Server 共用配置对象。
    driver: str = "ODBC Driver 17 for SQL Server"


# 2026-06-13 17:18:04 新增：定义 adapter 协议；作用是让 worker 只调用读取和状态回写；理由是避免在同步编排里出现 PG/SQLServer 分支。
class ExternalDbAdapter(Protocol):
    # 2026-06-13 17:18:04 新增：声明读取行接口，作用是返回 dict row；理由是后续 profile 解释器统一消费字典。
    def fetch_rows(self, profile: Any) -> list[dict[str, Any]]:
        # 2026-06-13 17:18:04 新增：协议空实现，作用是类型占位；理由是具体 adapter 负责实现。
        ...

    # 2026-06-13 17:18:04 新增：声明状态回写接口，作用是把已入库写回外部库；理由是用户要求每条 point 存好后更新 ZhuangTai。
    def mark_row_synced(self, profile: Any, source_pk: Any, status_value: str) -> None:
        # 2026-06-13 17:18:04 新增：协议空实现，作用是类型占位；理由是具体 adapter 负责实现。
        ...


# 2026-06-13 17:18:04 新增：从配置或环境变量读取值；作用是支持 host_env/password_env 等写法；理由是敏感信息必须放 .env。
def read_connection_value(connection: dict[str, Any], key: str, default: str = "") -> str:
    # 2026-06-13 17:18:04 新增：优先读取 key_env 指向的环境变量名；作用是 YAML 不直接保存密钥；理由是密码和主机可按环境切换。
    env_name = str(connection.get(f"{key}_env") or "").strip()
    # 2026-06-13 17:18:04 新增：判断环境变量名是否存在；作用是决定是否从 os.environ 取值；理由是兼容直接值和 env 间接值。
    if env_name:
        # 2026-06-13 17:18:04 新增：返回环境变量值或默认值；作用是本地缺配置时不立刻类型异常；理由是后续连接时给出明确错误。
        return os.getenv(env_name, default)
    # 2026-06-13 17:18:04 新增：读取直接配置值；作用是支持非敏感字段直接写 YAML；理由是端口/engine 等可读性更好。
    return str(connection.get(key, default) or default)


# 2026-06-13 17:18:04 新增：解析 profile 的连接配置；作用是把 YAML connection 转成 dataclass；理由是 adapter 构造参数要统一。
def resolve_profile_connection_config(profile: Any) -> ExternalDbConnectionConfig:
    # 2026-06-13 17:18:04 新增：读取 profile.connection；作用是兼容没有连接配置的主库 profile；理由是默认仍走 SQL Server。
    connection = dict(getattr(profile, "connection", {}) or {})
    # 2026-06-13 17:18:04 新增：读取 engine；作用是选择外部库 adapter；理由是不能按 profile 名写死。
    engine = read_connection_value(connection, "engine", "sqlserver").strip().lower()
    # 2026-06-13 17:18:04 新增：读取端口文本；作用是安全转换 int；理由是 YAML/env 都是字符串。
    port_text = read_connection_value(connection, "port", "5432" if engine in {"postgresql", "postgres", "pg"} else "1433")
    # 2026-06-13 17:18:04 新增：构造连接配置；作用是交给具体 adapter；理由是连接字段只解析一次。
    return ExternalDbConnectionConfig(
        # 2026-06-13 17:18:04 新增：写入 engine；作用是 registry 查找；理由是配置驱动扩展。
        engine=engine,
        # 2026-06-13 17:18:04 新增：写入 host；作用是连接外部数据库；理由是 PG 主机来自截图和 .env。
        host=read_connection_value(connection, "host", "127.0.0.1"),
        # 2026-06-13 17:18:04 新增：写入端口；作用是连接外部数据库；理由是 PG/SQL Server 端口不同。
        port=int(port_text or 0),
        # 2026-06-13 17:18:04 新增：写入 database；作用是连接目标库；理由是不同外部库独立配置。
        database=read_connection_value(connection, "database", ""),
        # 2026-06-13 17:18:04 新增：写入 user；作用是认证；理由是不同库使用不同账号。
        user=read_connection_value(connection, "user", ""),
        # 2026-06-13 17:18:04 新增：写入 password；作用是认证；理由是从环境变量读取避免 YAML 明文。
        password=read_connection_value(connection, "password", ""),
        # 2026-06-13 17:18:04 新增：写入 sslmode；作用是 PG SSL 连接控制；理由是局域网和远程部署要求可能不同。
        sslmode=read_connection_value(connection, "sslmode", "prefer"),
        # 2026-06-13 17:18:04 新增：写入 driver；作用是 SQL Server adapter 使用；理由是保留旧外部 SQL Server 支持。
        driver=read_connection_value(connection, "driver", "ODBC Driver 17 for SQL Server"),
    )


# 2026-06-13 17:18:04 新增：定义 adapter 注册表；作用是按 engine 创建 adapter；理由是未来新增引擎只注册工厂。
class ExternalAdapterRegistry:
    # 2026-06-13 17:18:04 新增：初始化注册表；作用是保存 engine 到工厂的映射；理由是消除同步主流程 if 分支。
    def __init__(self) -> None:
        # 2026-06-13 17:18:04 新增：创建工厂字典；作用是记录已支持数据库引擎；理由是 adapter 扩展集中管理。
        self._factories: dict[str, Callable[[ExternalDbConnectionConfig], ExternalDbAdapter]] = {}

    # 2026-06-13 17:18:04 新增：注册 adapter 工厂；作用是绑定 engine 和实现；理由是新数据库类型不改 worker。
    def register(self, engine: str, factory: Callable[[ExternalDbConnectionConfig], ExternalDbAdapter]) -> None:
        # 2026-06-13 17:18:04 新增：规范 engine key；作用是大小写不敏感；理由是 YAML 维护者可能写法不同。
        normalized_engine = str(engine or "").strip().lower()
        # 2026-06-13 17:18:04 新增：保存工厂；作用是后续 create 使用；理由是 registry 是唯一分发点。
        self._factories[normalized_engine] = factory

    # 2026-06-13 17:18:04 新增：按 profile 创建 adapter；作用是 worker 无需知道连接细节；理由是一库一 YAML、一套通用流程。
    def create_from_profile(self, profile: Any) -> ExternalDbAdapter:
        # 2026-06-13 17:18:04 新增：解析连接配置；作用是获得 engine/host/user/password；理由是 adapter 只接收结构化配置。
        config = resolve_profile_connection_config(profile)
        # 2026-06-13 17:18:04 新增：读取对应工厂；作用是按 engine 选择实现；理由是避免业务代码写 if。
        factory = self._factories.get(config.engine)
        # 2026-06-13 17:18:04 新增：处理未注册引擎；作用是给出明确错误；理由是不能默默走错数据库 adapter。
        if factory is None:
            # 2026-06-13 17:18:04 新增：抛出 ValueError；作用是阻断错误同步；理由是未知 engine 写 Qdrant 风险高。
            raise ValueError(f"未注册外部库 adapter：{config.engine}")
        # 2026-06-13 17:18:04 新增：创建 adapter；作用是交给 worker 使用；理由是连接实现被封装到具体类。
        return factory(config)
