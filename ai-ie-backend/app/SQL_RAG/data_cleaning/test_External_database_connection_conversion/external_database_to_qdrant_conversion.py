# -*- coding: utf-8 -*-
"""按节点复现外部关系型数据库转 Qdrant 向量库的现有执行链路。"""

# 导入 argparse，用来暴露外部数据库和目标 Qdrant 的命令行参数。
import argparse
# 导入 json，用来把执行摘要打印成机器可读结果。
import json
# 导入 os，用来读取外部接入方可配置的环境变量。
import os
# 导入 sys，用来把 data_cleaning 目录加入模块搜索路径。
import sys
# 从 pathlib 导入 Path，用来稳定定位当前脚本和 SQL_RAG 根目录。
from pathlib import Path
# 从 typing 导入 Any 和 Callable，用来标注可替换的测试依赖。
from typing import Any, Callable

# 定位当前测试复现目录。
CURRENT_DIR = Path(__file__).resolve().parent
# 定位 data_cleaning 功能包目录。
DATA_CLEANING_DIR = CURRENT_DIR.parent
# 定位 SQL_RAG 后端根目录。
SQL_RAG_DIR = DATA_CLEANING_DIR.parent
# 如果 data_cleaning 还不在模块搜索路径里，就加入最前面。
if str(DATA_CLEANING_DIR) not in sys.path:
    # 把 data_cleaning 放到最前，保证导入的是当前项目现有 API。
    sys.path.insert(0, str(DATA_CLEANING_DIR))

# 从现有 Qdrant 同步模块导入完整 SQL Server 到 Qdrant API 集合。
from Qdrant import qdrant_sqlserver_sync as qdrant_sync
# 2026-06-11 15:54:56 修改：导入 source profile 解析器；作用：外部库转换入口按 profile 动态映射字段；理由：不同外部库不能各自新拉一条写入逻辑。
from Qdrant import qdrant_mapping_profile
# 2026-06-10 18:01:50 修改：导入 External_database adapter。理由：外部 QA 表转 CanonicalChunk 后复用 Qdrant 链路。
from integration import external_database_adapter


# 定义本复现脚本按执行顺序使用到的现有 API 节点清单。
API_CALL_CHAIN: list[dict[str, str]] = [
    # 节点 1：从外部关系型库读取已经清洗好的 canonical QA chunk。
    {
        # 记录节点名称。
        "node": "01_关系型数据库读取节点",
        # 记录实际调用的现有 API。
        "api": "load_canonical_chunks_from_sqlserver",
        # 记录该节点依赖的上游。
        "depends_on": "SqlServerConfig",
        # 记录该节点产出的下游输入。
        "produces": "list[CanonicalChunk]",
    },
    # 节点 2：校验 chunk 是否满足 Qdrant/RAG payload 消费契约。
    {
        # 记录节点名称。
        "node": "02_Qdrant同步前契约校验节点",
        # 记录实际调用的现有 API。
        "api": "validate_chunks_before_qdrant",
        # 记录该节点依赖的上游。
        "depends_on": "list[CanonicalChunk]",
        # 记录该节点产出的下游输入。
        "produces": "contract_validation",
    },
    # 节点 3：创建 Qdrant 官方客户端。
    {
        # 记录节点名称。
        "node": "03_Qdrant客户端节点",
        # 记录实际调用的现有 API。
        "api": "QdrantClient",
        # 记录该节点依赖的上游。
        "depends_on": "QdrantSyncConfig.url",
        # 记录该节点产出的下游输入。
        "produces": "qdrant_client",
    },
    # 节点 4：确保目标 collection 存在、维度一致，并补齐 payload index。
    {
        # 记录节点名称。
        "node": "04_Qdrant集合准备节点",
        # 记录实际调用的现有 API。
        "api": "ensure_qdrant_collection",
        # 记录该节点依赖的上游。
        "depends_on": "qdrant_client + QdrantSyncConfig + EmbeddingConfig",
        # 记录该节点产出的下游输入。
        "produces": "ready_collection",
    },
    # 节点 5：创建 OpenAI-compatible embedding 客户端。
    {
        # 记录节点名称。
        "node": "05_Embedding客户端节点",
        # 记录实际调用的现有 API。
        "api": "create_embedding_client",
        # 记录该节点依赖的上游。
        "depends_on": "EmbeddingConfig",
        # 记录该节点产出的下游输入。
        "produces": "embedding_client",
    },
    # 节点 6：按 embedding 批量大小切分 canonical chunks。
    {
        # 记录节点名称。
        "node": "06_分批节点",
        # 记录实际调用的现有 API。
        "api": "chunk_list",
        # 记录该节点依赖的上游。
        "depends_on": "list[CanonicalChunk] + EmbeddingConfig.batch_size",
        # 记录该节点产出的下游输入。
        "produces": "list[list[CanonicalChunk]]",
    },
    # 节点 7：为每个 chunk 构造现有链路定义的向量检索文本。
    {
        # 记录节点名称。
        "node": "07_向量化文本构造节点",
        # 记录实际调用的现有 API。
        "api": "build_embedding_text",
        # 记录该节点依赖的上游。
        "depends_on": "CanonicalChunk",
        # 记录该节点产出的下游输入。
        "produces": "embedding_text",
    },
    # 节点 8：调用 embedding 服务生成向量。
    {
        # 记录节点名称。
        "node": "08_Embedding生成节点",
        # 记录实际调用的现有 API。
        "api": "embed_texts",
        # 记录该节点依赖的上游。
        "depends_on": "embedding_client + embedding_texts + EmbeddingConfig",
        # 记录该节点产出的下游输入。
        "produces": "list[list[float]]",
    },
    # 节点 9：把 chunk、向量和 payload 打包成 Qdrant PointStruct。
    {
        # 记录节点名称。
        "node": "09_Qdrant点构造节点",
        # 记录实际调用的现有 API。
        "api": "build_qdrant_points",
        # 记录该节点依赖的上游。
        "depends_on": "chunk_batch + embeddings + EmbeddingConfig",
        # 记录该节点产出的下游输入。
        "produces": "list[PointStruct]",
    },
    # 节点 10：把当前批次 point 写入 Qdrant。
    {
        # 记录节点名称。
        "node": "10_Qdrant写入节点",
        # 记录实际调用的现有 API。
        "api": "upsert_points_to_qdrant",
        # 记录该节点依赖的上游。
        "depends_on": "qdrant_client + QdrantSyncConfig + point_batch",
        # 记录该节点产出的下游输入。
        "produces": "upserted_points",
    },
    # 节点 11：回写 SQL Server 同步状态，供后续判断是否已同步。
    {
        # 记录节点名称。
        "node": "11_SQL同步状态回写节点",
        # 记录实际调用的现有 API。
        "api": "update_sqlserver_sync_state",
        # 记录该节点依赖的上游。
        "depends_on": "SqlServerConfig + QdrantSyncConfig + EmbeddingConfig + chunks + point_count",
        # 记录该节点产出的下游输入。
        "produces": "dbo.rag_rag_sync_state",
    },
    # 节点 12：用 Qdrant count/query_points 做写入后自检。
    {
        # 记录节点名称。
        "node": "12_Qdrant自检节点",
        # 记录实际调用的现有 API。
        "api": "verify_qdrant_collection",
        # 记录该节点依赖的上游。
        "depends_on": "qdrant_client + QdrantSyncConfig + first_vector",
        # 记录该节点产出的下游输入。
        "produces": "verify_result",
    },
]


def build_api_call_chain() -> list[dict[str, str]]:
    # 返回 API 调用链的浅拷贝，避免调用方误改全局清单。
    return [dict(item) for item in API_CALL_CHAIN]


def read_env(name: str, default: str = "") -> str:
    # 从环境变量读取外部接入配置。
    value = os.getenv(name)
    # 如果环境变量有值，就返回环境变量。
    if value not in (None, ""):
        # 返回非空环境变量值。
        return value
    # 如果环境变量为空，就返回默认值。
    return default


def parse_bool_env(name: str, default: bool = False) -> bool:
    # 读取原始环境变量文本。
    raw_value = read_env(name, "")
    # 没有配置时返回默认布尔值。
    if raw_value == "":
        # 返回调用方给出的默认值。
        return default
    # 统一大小写并去掉两侧空白。
    normalized = raw_value.strip().lower()
    # 识别常见真值写法。
    return normalized in {"1", "true", "yes", "y", "on"}


def normalize_collection_piece(raw_text: str) -> str:
    # 把数据库名转成 Qdrant collection 可读片段。
    lowered = raw_text.strip().lower()
    # 把非字母数字字符统一替换成下划线。
    normalized = "".join(character if character.isalnum() else "_" for character in lowered)
    # 连续下划线折叠成单个下划线。
    while "__" in normalized:
        # 执行一次下划线折叠。
        normalized = normalized.replace("__", "_")
    # 去掉首尾下划线。
    normalized = normalized.strip("_")
    # 空数据库名时使用 external_database 兜底。
    return normalized or "external_database"


def default_collection_name(database_name: str) -> str:
    # 2026-06-10 18:01:50 修改：External_database 固定映射 sql_External_database。理由：避免冲突现有 collection。
    if normalize_collection_piece(database_name) == normalize_collection_piece(external_database_adapter.EXTERNAL_DATABASE_NAME):
        # 2026-06-10 18:01:50 修改：返回外部库专用 collection。作用：隔离 sql_rag_qa_chunks_v1。
        return external_database_adapter.EXTERNAL_QDRANT_COLLECTION
    # 2026-06-10 18:01:50 修改：其他外部库统一加 sql_ 前缀。理由：便于多库接入。
    return f"sql_{normalize_collection_piece(database_name)}"


def build_arg_parser() -> argparse.ArgumentParser:
    # 创建命令行解析器。
    parser = argparse.ArgumentParser(description="复现现有 SQL Server canonical QA chunks 到 Qdrant 的节点化同步链路。")
    # 添加外部 SQL Server 主机参数，同时兼容原同步脚本的 --sql-server 名称。
    parser.add_argument("--external-sql-server", "--sql-server", dest="sql_server", default=read_env("EXTERNAL_DB_HOST", external_database_adapter.EXTERNAL_SQL_SERVER_DEFAULT))
    # 添加外部 SQL Server 数据库名参数，同时兼容原同步脚本的 --sql-database 名称。
    # 2026-06-10 18:01:50 修改：外部库默认使用 External_database。理由：不回到 getai。
    parser.add_argument("--external-sql-database", "--sql-database", dest="sql_database", default=read_env("EXTERNAL_DB_NAME", external_database_adapter.EXTERNAL_DATABASE_NAME))
    # 添加外部 SQL Server 用户名参数，同时兼容原同步脚本的 --sql-user 名称。
    parser.add_argument("--external-sql-user", "--sql-user", dest="sql_user", default=read_env("EXTERNAL_DB_USER", read_env("DB_USER", "dev")))
    # 添加外部 SQL Server 密码参数，同时兼容原同步脚本的 --sql-password 名称。
    parser.add_argument("--external-sql-password", "--sql-password", dest="sql_password", default=read_env("EXTERNAL_DB_PASSWORD", read_env("DB_PASSWORD", "123456")))
    # 添加外部 SQL Server ODBC 驱动参数，同时兼容原同步脚本的 --sql-driver 名称。
    parser.add_argument("--external-sql-driver", "--sql-driver", dest="sql_driver", default=read_env("EXTERNAL_DB_DRIVER", read_env("DB_DRIVER", "ODBC Driver 17 for SQL Server")))
    # 添加 Qdrant URL 参数。
    parser.add_argument("--qdrant-url", default=read_env("EXTERNAL_QDRANT_URL", external_database_adapter.EXTERNAL_QDRANT_URL_DEFAULT))
    # 添加目标 Qdrant collection 参数。
    parser.add_argument("--collection", default=read_env("EXTERNAL_QDRANT_COLLECTION", ""))
    # 添加 Qdrant 距离度量参数。
    parser.add_argument("--distance", default=read_env("EXTERNAL_QDRANT_DISTANCE", read_env("QDRANT_DISTANCE", "Cosine")))
    # 添加是否重建 collection 参数。
    parser.add_argument("--recreate", action="store_true", default=parse_bool_env("EXTERNAL_QDRANT_RECREATE", False))
    # 2026-06-11 08:23:49 修改：添加外部库 hybrid 开关。理由：External_database 可选择输出 LlamaIndex dense+sparse collection。
    parser.add_argument("--enable-hybrid", action="store_true", default=parse_bool_env("EXTERNAL_QDRANT_ENABLE_HYBRID", False))
    # 2026-06-11 08:23:49 修改：添加外部库 dense 向量名。理由：与 Qdrant 同步层统一 LlamaIndex 官方默认名。
    parser.add_argument("--dense-vector-name", default=read_env("EXTERNAL_QDRANT_DENSE_VECTOR_NAME", qdrant_sync.LLAMAINDEX_DEFAULT_DENSE_VECTOR_NAME))
    # 2026-06-11 08:23:49 修改：添加外部库 sparse 向量名。理由：与 Qdrant 同步层统一 LlamaIndex 官方默认名。
    parser.add_argument("--sparse-vector-name", default=read_env("EXTERNAL_QDRANT_SPARSE_VECTOR_NAME", qdrant_sync.LLAMAINDEX_DEFAULT_SPARSE_VECTOR_NAME))
    # 2026-06-12 09:52:34 修改：添加外部库 sparse encoder 模型名；作用：默认使用 Qdrant/bm25；理由：匹配外部 QdrantVectorStore(fastembed_sparse_model="Qdrant/bm25")。
    parser.add_argument("--fastembed-sparse-model", default=read_env("EXTERNAL_QDRANT_FASTEMBED_SPARSE_MODEL", qdrant_sync.LLAMAINDEX_BM25_FASTEMBED_SPARSE_MODEL))
    # 2026-06-11 15:54:56 修改：添加外部库 source profile 参数；作用：让 External_database 默认走 external_database.yml，也允许后续外部库只换配置；理由：动态字段映射不能写死在转换脚本。
    parser.add_argument("--source-profile", default=read_env("EXTERNAL_SOURCE_PROFILE", "external_database"))
    # 添加 embedding 服务地址参数。
    parser.add_argument("--embedding-api-base", default=read_env("EXTERNAL_EMBEDDING_SERVICE_URL", read_env("EMBEDDING_SERVICE_URL", "https://api.siliconflow.cn/v1")))
    # 添加 embedding API key 参数。
    parser.add_argument("--embedding-api-key", default=read_env("EXTERNAL_EMBEDDING_SERVICE_API_KEY", read_env("EMBEDDING_SERVICE_API_KEY", "")))
    # 添加 embedding 模型参数。
    parser.add_argument("--embedding-model", default=read_env("EXTERNAL_MODEL_EMBED", read_env("MODEL_EMBED", "Qwen/Qwen3-Embedding-0.6B")))
    # 添加 embedding 维度参数。
    parser.add_argument("--embedding-dimension", type=int, default=int(read_env("EXTERNAL_EMBEDDING_DIMENSIONS", read_env("EMBEDDING_DIMENSIONS", "1024"))))
    # 添加 embedding 批量大小参数。
    parser.add_argument("--embedding-batch-size", type=int, default=int(read_env("EXTERNAL_EMBEDDING_MAX_CHUNKS_IN_BATCH", read_env("EMBEDDING_MAX_CHUNKS_IN_BATCH", "10"))))
    # 添加 Qdrant upsert 批量大小参数。
    parser.add_argument("--upsert-batch-size", type=int, default=int(read_env("EXTERNAL_QDRANT_UPSERT_BATCH_SIZE", "64")))
    # 添加 dry-run 参数，用于只跑读取、校验和向量生成而不写入。
    parser.add_argument("--dry-run", action="store_true", default=parse_bool_env("EXTERNAL_QDRANT_DRY_RUN", False))
    # 添加只打印节点 API 链路参数。
    # 2026-06-10 18:01:50 修改：增加外部库初始化参数。理由：创建 External_database 和三条样例。
    parser.add_argument("--init-external-demo", action="store_true", default=parse_bool_env("EXTERNAL_INIT_DEMO", False))
    parser.add_argument("--print-api-chain", action="store_true")
    # 返回配置完成的解析器。
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    # 创建命令行解析器。
    parser = build_arg_parser()
    # 解析调用方传入或系统传入的命令行参数。
    args = parser.parse_args(argv)
    # 如果没有显式指定 collection，就按外部数据库名生成一个新 collection。
    if not args.collection:
        # 写回自动生成的 collection 名称。
        args.collection = default_collection_name(args.sql_database)
    # 返回解析后的参数对象。
    return args


def build_sqlserver_config(args: argparse.Namespace) -> qdrant_sync.SqlServerConfig:
    # 复用现有 qdrant_sqlserver_sync.build_sqlserver_config 构造 SQL Server 配置。
    return qdrant_sync.build_sqlserver_config(args)


def build_embedding_config(args: argparse.Namespace) -> qdrant_sync.EmbeddingConfig:
    # 复用现有 qdrant_sqlserver_sync.build_embedding_config 构造 embedding 配置。
    return qdrant_sync.build_embedding_config(args)


def build_qdrant_config(args: argparse.Namespace) -> qdrant_sync.QdrantSyncConfig:
    # 复用现有 qdrant_sqlserver_sync.build_qdrant_config 构造 Qdrant 配置。
    return qdrant_sync.build_qdrant_config(args)


def run_external_database_to_qdrant_conversion(
    sql_config: qdrant_sync.SqlServerConfig,
    embedding_config: qdrant_sync.EmbeddingConfig,
    qdrant_config: qdrant_sync.QdrantSyncConfig,
    sync_module: Any = qdrant_sync,
    qdrant_client_factory: Callable[..., Any] = qdrant_sync.QdrantClient,
    source_loader: Callable[[qdrant_sync.SqlServerConfig], list[Any]] | None = None,
) -> dict[str, Any]:
    # 2026-06-11 15:54:56 修改：真实 Qdrant 同步模块才加载 profile；作用：保持单测 fake sync_module 不被生产 profile 逻辑干扰；理由：测试替身只验证链路调用顺序。
    source_profile = (
        qdrant_mapping_profile.load_source_profile(getattr(qdrant_config, "source_profile", "") or "external_database", sql_config.database)
        if sync_module is qdrant_sync
        else None
    )
    # 2026-06-12 09:52:34 修改：真实 Qdrant 同步模块才应用 profile 到配置；作用：让 External_database 自动生成 hybrid/BM25 collection；理由：避免转换入口忘记传 --enable-hybrid。
    if source_profile is not None and sync_module is qdrant_sync:
        # 2026-06-12 09:52:34 修改：替换为 profile 驱动后的配置；作用：collection、向量名、sparse 模型都按 profile 生效；理由：外部库只换配置不换写入链路。
        qdrant_config = sync_module.apply_source_profile_to_qdrant_config(qdrant_config, source_profile)
    # 2026-06-10 18:01:50 修改：优先使用 source_loader。理由：外部库只替换读取 adapter。
    if source_loader is not None:
        # 2026-06-10 18:01:50 修改：从 loader 读取 CanonicalChunk。作用：Qdrant 后续链路不变。
        chunks = source_loader(sql_config)
        # 2026-06-10 18:01:50 修改：记录来源 adapter。作用：执行摘要可排查。
        source_adapter = "custom_source_loader"
    # 2026-06-13 17:18:04 新增：声明 connection.engine 的 profile 走通用 adapter registry；作用：PG/SQLServer 外部库都能离线重建 Qdrant；理由：不能为每个外部库改转换脚本分支。
    elif source_profile is not None and getattr(source_profile, "connection", {}):
        # 2026-06-13 17:18:04 新增：按 profile 读取并转换外部库；作用：krauss PG 可用同一手动重建入口；理由：字段、连接、payload 都来自 YAML。
        chunks = external_database_adapter.load_external_canonical_chunks_from_profile(source_profile)
        # 2026-06-13 17:18:04 新增：记录来源 adapter；作用：摘要可证明走的是通用外部库读取层；理由：排查时能区分旧 SQL Server canonical 入口。
        source_adapter = "integration.external_database_adapter.profile_registry"
    # 2026-06-10 18:01:50 修改：External_database 默认走新 adapter。理由：它跳过原清洗入库表。
    elif sql_config.database == external_database_adapter.EXTERNAL_DATABASE_NAME and sync_module is qdrant_sync:
        # 2026-06-10 18:01:50 修改：外部 QA 表转 CanonicalChunk。作用：复用统一 Qdrant 写入链路。
        chunks = external_database_adapter.load_external_canonical_chunks_from_sqlserver(sql_config, source_profile)
        # 2026-06-10 18:01:50 修改：记录来源 adapter。作用：明确没有走 getai 清洗表。
        source_adapter = "integration.external_database_adapter"
    # 2026-06-10 18:01:50 修改：其他库仍走 canonical chunk 读取。理由：保持兼容。
    else:
        # 节点 1：调用现有 API 从外部 SQL Server 读取 canonical chunks。
        chunks = sync_module.load_canonical_chunks_from_sqlserver(sql_config)
        # 2026-06-11 15:54:56 修改：真实同步模块读取到 canonical chunk 后应用 profile；作用：让 getai 和其他 canonical 来源也走统一字段解释层；理由：不改后续 validate/embed/build/upsert 顺序。
        if source_profile is not None:
            # 2026-06-11 15:54:56 修改：批量应用 profile；作用：生成 embedding_text/prompt_text/source_payload；理由：字段策略应在校验前落地。
            chunks = qdrant_mapping_profile.apply_profile_to_chunks(chunks, source_profile)
        # 2026-06-10 18:01:50 修改：记录原读取方式。作用：摘要里可见兼容路径。
        source_adapter = "qdrant_sqlserver_sync.load_canonical_chunks_from_sqlserver"
    # 如果外部库没有可同步 chunk，就沿用原链路语义直接报错。
    if not chunks:
        # 抛出明确错误，避免创建空 Qdrant collection 误导别人消费。
        raise RuntimeError("外部关系型数据库中没有可同步到 Qdrant 的 canonical QA chunk。")
    # 节点 2：调用现有 API 做 Qdrant/RAG 消费契约校验。
    contract_validation = sync_module.validate_chunks_before_qdrant(chunks)
    # 节点 3：调用 Qdrant 官方客户端构造器连接目标 Qdrant。
    qdrant_client = qdrant_client_factory(url=qdrant_config.url)
    # 节点 4：调用现有 API 创建或校验 Qdrant collection。
    sync_module.ensure_qdrant_collection(qdrant_client, qdrant_config, embedding_config)
    # 节点 5：调用现有 API 创建 embedding 客户端。
    embedding_client = sync_module.create_embedding_client(embedding_config)
    # 创建全量 points 容器，用来统计写入数量和做最终自检。
    all_points: list[Any] = []
    # 节点 6：调用现有 API 按 embedding batch_size 切分 chunk。
    chunk_batches = sync_module.chunk_list(chunks, embedding_config.batch_size)
    # 遍历每个 chunk 批次。
    for chunk_batch in chunk_batches:
        # 节点 7：调用现有 API 为当前批次每个 chunk 构造向量化文本。
        texts = [sync_module.build_embedding_text(chunk) for chunk in chunk_batch]
        # 节点 8：调用现有 API 生成当前批次 embedding。
        embeddings = sync_module.embed_texts(embedding_client, texts, embedding_config)
        # 节点 9：调用现有 API 构造当前批次 Qdrant points。
        # 2026-06-12 09:52:34 修改：真实同步模块才传 qdrant_config；作用：hybrid 模式才能写 text-dense 和 text-sparse-new；理由：测试替身仍保持旧签名以验证原链路顺序。
        if sync_module is qdrant_sync:
            # 2026-06-12 09:52:34 修改：把 qdrant_config 传入生产 point 构造；作用：启用 profile 驱动的 hybrid 写入；理由：不传配置会退回旧 dense list。
            point_batch = sync_module.build_qdrant_points(chunk_batch, embeddings, embedding_config, qdrant_config)
        else:
            # 2026-06-12 09:52:34 修改：测试替身走旧参数；作用：保持链路回放测试不被生产扩展参数误伤；理由：fake sync 只验证节点顺序不是 hybrid 行为。
            point_batch = sync_module.build_qdrant_points(chunk_batch, embeddings, embedding_config)
        # 记录当前批次 points，供状态回写和最终自检使用。
        all_points.extend(point_batch)
        # 节点 10：调用现有 API upsert 当前批次到 Qdrant。
        sync_module.upsert_points_to_qdrant(qdrant_client, qdrant_config, point_batch)
    # 2026-06-13 17:18:04 新增：判断是否为声明 connection.engine 的通用外部库；作用：PG 离线重建不再误写 SQL Server 状态表；理由：PG 状态回写由后台 worker 按 adapter 处理。
    profile_has_external_connection = bool(source_profile is not None and getattr(source_profile, "connection", {}))
    # 2026-06-13 17:18:04 新增：非通用外部连接才沿用 SQL Server 状态表；作用：保护旧 External_database/getai 行为；理由：不能破坏已有转换链路。
    if not profile_has_external_connection:
        # 节点 11：调用现有 API 回写 SQL Server 同步状态。
        sync_module.update_sqlserver_sync_state(sql_config, qdrant_config, embedding_config, chunks, len(all_points))
        # 2026-06-13 17:18:04 新增：记录状态回写方式；作用：执行摘要可见；理由：多外部库排查需要。
        sync_state_adapter = "sqlserver_rag_rag_sync_state"
    else:
        # 2026-06-13 17:18:04 新增：跳过 SQL Server 状态回写；作用：避免 PG 转换误写本地 SQL Server；理由：实时同步 worker 会逐条回写外部状态字段。
        sync_state_adapter = "skipped_for_profile_connection"
    # 节点 12：调用现有 API 用第一条向量对 Qdrant collection 做自检。
    # 2026-06-12 09:52:34 修改：hybrid 自检时取 dense 命名向量；作用：verify_qdrant_collection 仍用 dense 相似度做写入校验；理由：point.vector 在 hybrid 模式下是 dict。
    first_verify_vector = all_points[0].vector[qdrant_config.dense_vector_name] if getattr(qdrant_config, "enable_hybrid", False) else all_points[0].vector
    # 节点 12：调用现有 API 用第一条向量对 Qdrant collection 做自检。
    verify_result = sync_module.verify_qdrant_collection(qdrant_client, qdrant_config, first_verify_vector)
    # 返回复现链路摘要。
    return {
        # 返回外部关系型数据库地址。
        "source_server": sql_config.server,
        # 返回外部关系型数据库名。
        "source_database": sql_config.database,
        # 2026-06-10 18:01:50 修改：返回来源 adapter。理由：排查外部库是否走统一入口。
        "source_adapter": source_adapter,
        # 2026-06-11 15:54:56 修改：返回 source profile 名称；作用：证明当前转换使用哪份字段映射；理由：多外部库同步必须可审计。
        "source_profile": source_profile.profile_name if source_profile is not None else "",
        # 2026-06-13 17:18:04 新增：返回状态回写方式；作用：说明 PG profile 不再写 SQL Server 状态表；理由：避免误判同步状态位置。
        "sync_state_adapter": sync_state_adapter,
        # 2026-06-12 09:52:34 修改：返回是否启用 hybrid；作用：摘要能直接证明是否创建 sparse 向量；理由：排查 text-sparse-new 缺失问题。
        "enable_hybrid": qdrant_config.enable_hybrid,
        # 2026-06-12 09:52:34 修改：返回 dense 向量名；作用：证明对齐 LlamaIndex text-dense；理由：外部消费者默认会用该名。
        "dense_vector_name": qdrant_config.dense_vector_name,
        # 2026-06-12 09:52:34 修改：返回 sparse 向量名；作用：证明对齐 LlamaIndex text-sparse-new；理由：外部 enable_hybrid=True 会用该名。
        "sparse_vector_name": qdrant_config.sparse_vector_name,
        # 2026-06-12 09:52:34 修改：返回 sparse 模型名；作用：证明文档侧 sparse 使用 Qdrant/bm25；理由：对齐外部 fastembed_sparse_model 参数。
        "fastembed_sparse_model": qdrant_config.fastembed_sparse_model,
        # 返回目标 Qdrant URL。
        "qdrant_url": qdrant_config.url,
        # 返回目标 Qdrant collection。
        "collection": qdrant_config.collection_name,
        # 返回读取到的 canonical chunk 数量。
        "source_chunk_count": len(chunks),
        # 返回写入或 dry-run 构造出的 point 数量。
        "upserted_point_count": len(all_points),
        # 返回同步前契约校验摘要。
        "contract_validation": contract_validation,
        # 返回 embedding 模型名。
        "embedding_model": embedding_config.model,
        # 返回 embedding 维度。
        "embedding_dimension": embedding_config.dimension,
        # 返回 dry-run 标记。
        "dry_run": qdrant_config.dry_run,
        # 返回 Qdrant 自检结果。
        "verify": verify_result,
        # 返回按节点提取出来的 API 调用链。
        "api_call_chain": build_api_call_chain(),
    }


def main(argv: list[str] | None = None) -> int:
    # 先复用现有 API 加载 SQL_RAG/.env。
    qdrant_sync.load_project_env()
    # 解析外部数据库和 Qdrant 参数。
    args = parse_args(argv)
    # 如果只需要查看 API 链路，就直接打印节点清单。
    if args.print_api_chain:
        # 打印 API 调用链 JSON。
        print(json.dumps(build_api_call_chain(), ensure_ascii=False, indent=2))
        # 返回成功退出码。
        return 0
    # 复用现有 API 构造外部 SQL Server 配置。
    sql_config = build_sqlserver_config(args)
    # 2026-06-10 18:01:50 修改：按需初始化 External_database。理由：一键创建表和样例。
    if args.init_external_demo:
        # 2026-06-10 18:01:50 修改：调用 adapter 初始化。作用：不把建库逻辑塞进 main agent。
        external_database_adapter.initialize_external_database(sql_config)
    # 复用现有 API 构造 embedding 配置。
    embedding_config = build_embedding_config(args)
    # 复用现有 API 构造 Qdrant 同步配置。
    qdrant_config = build_qdrant_config(args)
    # 按节点复现 SQL Server 到 Qdrant 的现有同步链路。
    summary = run_external_database_to_qdrant_conversion(sql_config, embedding_config, qdrant_config)
    # 打印执行摘要 JSON。
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    # 返回成功退出码。
    return 0


# 允许当前脚本直接运行。
if __name__ == "__main__":
    # 把 main 的返回码交给系统进程。
    raise SystemExit(main())
