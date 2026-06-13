# -*- coding: utf-8 -*-
"""把 SQL Server 里的 canonical QA chunk 同步成 Qdrant collection。"""

# 修改日期：2026-06-01 17:52:00。
# 修改理由：把 SQL Server 2022 中已清洗、已校验、已融合后的 canonical QA chunk，用官方 qdrant-client API 封装成 Qdrant 向量检索 collection。

# 导入 argparse，用于把同步参数暴露成命令行接口。
import argparse
# 导入 hashlib，用于生成稳定的同步状态主键。
import hashlib
# 导入 json，用于解析 SQL Server 里的 JSON 字段和构造同步消息。
import json
# 导入 os，用于读取环境变量。
import os
# 导入 textwrap，用于拼接更稳定的向量化文本。
import textwrap
# 导入 uuid，用于把 chunk_id 稳定映射成 Qdrant 支持的 UUID point id。
import uuid
# 导入 dataclass，用于定义同步配置和同步记录结构。
from dataclasses import dataclass, replace
# 导入 datetime，用于记录同步时间。
from datetime import datetime, timezone
# 导入 Path，用于定位项目根目录和 .env 文件。
from pathlib import Path
# 导入 Any，用于标注 SQL/Qdrant payload 的动态字段。
from typing import Any

# 导入 OpenAI 官方 SDK，用 OpenAI-compatible embedding 服务生成生产向量。
from openai import OpenAI
# 导入 python-dotenv，用于读取项目 .env 配置。
from dotenv import load_dotenv
# 导入 pyodbc，用于从 SQL Server 2022 读取主数据。
import pyodbc
# 导入 Qdrant 官方 Python 客户端。
from qdrant_client import QdrantClient
# 导入 Qdrant 官方模型定义，创建 collection、payload index 和 point 时使用。
from qdrant_client import models

# 2026-06-11 15:54:56 修改：导入动态数据源 mapping profile；作用：让不同外部库自己决定向量化字段、prompt 字段和 payload 字段；理由：不能把所有外部库硬塞成固定 QA 模板。
try:
    # 2026-06-12 10:24:31 修改：优先按当前包相对导入 mapping profile；作用：兼容 python -m app.SQL_RAG.data_cleaning.Qdrant.qdrant_sqlserver_sync；理由：生成 getai hybrid 影子 collection 时必须能以包入口运行。
    from . import qdrant_mapping_profile
except ImportError:
    try:
        # 2026-06-12 10:24:31 修改：保留 data_cleaning 目录运行时的包导入兜底；作用：兼容已有外部转换脚本从 data_cleaning 根目录导入 Qdrant；理由：不能因为修复 -m 入口而破坏旧执行方式。
        from Qdrant import qdrant_mapping_profile
    except ImportError:
        # 2026-06-12 10:24:31 修改：保留同目录脚本直跑兜底；作用：兼容 python qdrant_sqlserver_sync.py；理由：同步层工具脚本仍需支持本地单文件排查。
        import qdrant_mapping_profile


# 定义当前同步脚本所在目录。
CURRENT_DIR = Path(__file__).resolve().parent
# 定义 data_cleaning 目录。
DATA_CLEANING_DIR = CURRENT_DIR.parent
# 2026-06-02 10:06:01 修改：SQL_RAG 作为独立后端运行时，配置必须读取 SQL_RAG 根目录。
SQL_RAG_DIR = DATA_CLEANING_DIR.parent
# 2026-06-02 10:06:01 修改：Qdrant 同步不再读取外层 ai-ie-backend/.env，避免拿错数据库和向量库地址。
ENV_PATH = SQL_RAG_DIR / ".env"

# 2026-06-10 18:01:50 修改：定义 LlamaIndex 默认 doc_id payload key。理由：兼容官方 QdrantVectorStore。
LLAMAINDEX_DOCUMENT_ID_PAYLOAD_KEY = "doc_id"
# 2026-06-11 08:23:49 修改：定义 LlamaIndex 默认 dense 向量名。理由：显式 hybrid collection 要匹配官方 QdrantVectorStore。
LLAMAINDEX_DEFAULT_DENSE_VECTOR_NAME = "text-dense"
# 2026-06-11 08:23:49 修改：定义 LlamaIndex 默认 sparse 向量名。理由：显式 hybrid collection 要匹配官方 QdrantVectorStore。
LLAMAINDEX_DEFAULT_SPARSE_VECTOR_NAME = "text-sparse-new"
# 2026-06-12 09:52:34 修改：定义 LlamaIndex/FastEmbed BM25 sparse 模型名；作用：对齐外部 QdrantVectorStore(fastembed_sparse_model="Qdrant/bm25")；理由：collection 有 sparse 但文档侧模型不一致仍会影响召回。
LLAMAINDEX_BM25_FASTEMBED_SPARSE_MODEL = "Qdrant/bm25"
# 2026-06-12 09:52:34 修改：按 sparse 模型名缓存 encoder；作用：同一进程可兼容 BM25 和后续其他 sparse 模型；理由：动态 profile 不能只缓存一个默认 encoder。
LLAMAINDEX_SPARSE_DOC_ENCODERS: dict[str, Any] = {}


@dataclass(frozen=True)
class SqlServerConfig:
    # SQL Server 主机，本机默认走 127.0.0.1。
    server: str
    # SQL Server 数据库名。
    database: str
    # SQL Server 用户名。
    user: str
    # SQL Server 密码。
    password: str
    # SQL Server ODBC 驱动名。
    driver: str


@dataclass(frozen=True)
class EmbeddingConfig:
    # OpenAI-compatible embedding 服务地址。
    api_base: str
    # OpenAI-compatible embedding API key。
    api_key: str
    # embedding 模型名，必须和后续 RAG 查询阶段保持一致。
    model: str
    # Qdrant collection 向量维度，必须和 embedding 返回维度一致。
    dimension: int
    # 每批发送给 embedding 服务的文本数量。
    batch_size: int


@dataclass(frozen=True)
class QdrantSyncConfig:
    # Qdrant HTTP 地址。
    url: str
    # Qdrant collection 名称。
    collection_name: str
    # Qdrant collection 距离度量。
    distance: str
    # 是否重建 collection。
    recreate_collection: bool
    # 每批 upsert 到 Qdrant 的 point 数量。
    upsert_batch_size: int
    # 是否只做 dry-run，不实际写入 Qdrant 和 SQL Server 同步状态。
    dry_run: bool
    # 2026-06-11 08:23:49 修改：是否启用 LlamaIndex hybrid dense+sparse 写入。理由：默认关闭保护现有 agent collection。
    enable_hybrid: bool = False
    # 2026-06-11 08:23:49 修改：hybrid dense 向量名。理由：匹配 LlamaIndex 官方默认 text-dense。
    dense_vector_name: str = LLAMAINDEX_DEFAULT_DENSE_VECTOR_NAME
    # 2026-06-11 08:23:49 修改：hybrid sparse 向量名。理由：匹配 LlamaIndex 官方默认 text-sparse-new。
    sparse_vector_name: str = LLAMAINDEX_DEFAULT_SPARSE_VECTOR_NAME
    # 2026-06-12 09:52:34 修改：新增 sparse encoder 模型名；作用：文档侧 sparse vector 按 Qdrant/bm25 生成；理由：匹配外部 fastembed_sparse_model 参数。
    fastembed_sparse_model: str = LLAMAINDEX_BM25_FASTEMBED_SPARSE_MODEL
    # 2026-06-11 15:54:56 修改：新增 source profile 名称/路径；作用：把字段映射策略交给 data_cleaning/source_profiles；理由：主库和外部库共用同一 Qdrant 写入器但不共用业务字段模板。
    source_profile: str = ""


@dataclass(frozen=True)
class CanonicalChunk:
    # QA chunk 主键。
    chunk_id: str
    # 文档主键。
    document_id: str
    # 音频编号。
    audio_no: int
    # 音频标题。
    audio_title: str
    # chunk 在文档内的序号。
    chunk_index: int
    # 业务场景。
    scene: str
    # 已分离并校验的问题。
    question: str
    # 已分离并校验的答案。
    answer: str
    # 清洗后的问答全文。
    cleaned_text: str
    # 处理步骤。
    resolution_steps: str
    # 关键词文本。
    keywords: str
    # 实体 JSON。
    entities_json: str
    # 来源片段。
    source_excerpt: str
    # 内容 hash。
    content_hash: str
    # QA 成对 ID。
    qa_pair_id: str
    # QA 成对序号。
    qa_pair_index: int
    # QA 相似度分数。
    qa_similarity_score: float
    # QA 相似度阈值。
    qa_similarity_threshold: float
    # QA 是否已通过 LlamaIndex evaluator 校验。
    qa_pair_validated: bool
    # 文档内聚类 ID。
    cluster_id: str
    # 文档内聚类标签。
    cluster_label: str
    # 文档内聚类层级。
    cluster_level: str
    # 文档内聚类路径。
    cluster_path: str
    # 全局聚类 ID。
    global_cluster_id: str
    # 全局聚类标签。
    global_cluster_label: str
    # 全局聚类层级。
    global_cluster_level: str
    # 全局聚类路径。
    global_cluster_path: str
    # 问题 hash。
    question_hash: str
    # 答案 hash。
    answer_hash: str
    # canonical chunk ID。
    canonical_chunk_id: str
    # 融合状态，canonical 才进入 Qdrant。
    fusion_status: str
    # payload schema 版本。
    payload_schema_version: str
    # 原始 payload JSON。
    payload_json: dict[str, Any]
    # RAG 消费契约版本。
    rag_contract_version: str
    # 规范问题。
    canonical_question: str
    # 答案优先字段。
    answer_text: str
    # query 口语/业务别名。
    query_aliases: list[str]
    # 完整来源摘录。
    source_excerpt_full: str
    # LLM 消费文本。
    llm_text: str
    # 向量检索文本。
    retrieval_text: str
    # 已融合 duplicate 上下文。
    duplicate_contexts: list[dict[str, Any]]
    # 已合并 duplicate chunk IDs。
    merged_duplicate_chunk_ids: list[str]
    # 是否满足 Qdrant 同步契约。
    qdrant_ready: bool
    # 校验标记。
    validation_flags: list[str]


def read_env_value(name: str, default: str = "") -> str:
    # 从环境变量读取配置。
    value = os.getenv(name)
    # 环境变量存在时直接返回。
    if value not in (None, ""):
        # 返回环境变量值。
        return value
    # 环境变量不存在时返回默认值。
    return default



def parse_bool_value(raw_value: Any) -> bool:
    # 2026-06-11 08:23:49 修改：把环境变量/命令行布尔值归一化。理由：hybrid 默认关闭但可显式开启。
    normalized = str(raw_value or "").strip().lower()
    # 2026-06-11 08:23:49 修改：识别常见真值。作用：兼容 true/1/yes/on 写法。
    return normalized in {"1", "true", "yes", "y", "on"}


def load_project_env() -> None:
    # 如果项目 .env 文件存在，就加载它。
    if ENV_PATH.exists():
        # 加载 .env，override=True 用来处理同一个键在文件里多次出现时取后面的有效值。
        load_dotenv(ENV_PATH, override=True)


def parse_args() -> argparse.Namespace:
    # 创建命令行解析器。
    parser = argparse.ArgumentParser(description="把 SQL Server canonical QA chunks 同步到 Qdrant collection。")
    # 添加 SQL Server 主机参数。
    parser.add_argument("--sql-server", default=read_env_value("DB_HOST", "127.0.0.1"))
    # 添加 SQL Server 数据库参数。
    parser.add_argument("--sql-database", default=read_env_value("DB_NAME", "getai"))
    # 添加 SQL Server 用户参数。
    parser.add_argument("--sql-user", default=read_env_value("DB_USER", "dev"))
    # 添加 SQL Server 密码参数。
    parser.add_argument("--sql-password", default=read_env_value("DB_PASSWORD", "123456"))
    # 添加 SQL Server ODBC 驱动参数。
    parser.add_argument("--sql-driver", default=read_env_value("DB_DRIVER", "ODBC Driver 17 for SQL Server"))
    # 添加 Qdrant URL 参数。
    parser.add_argument("--qdrant-url", default=read_env_value("QDRANT_URL", "http://127.0.0.1:6333"))
    # 添加 Qdrant collection 参数。
    parser.add_argument("--collection", default=read_env_value("QDRANT_COLLECTION", "sql_rag_qa_chunks_v1"))
    # 添加距离度量参数。
    parser.add_argument("--distance", default=read_env_value("QDRANT_DISTANCE", "Cosine"))
    # 添加是否重建 collection 参数。
    parser.add_argument("--recreate", action="store_true", help="删除并重建目标 Qdrant collection。")
    # 2026-06-11 08:23:49 修改：添加 hybrid 开关。理由：只在新/重建 collection 时启用 LlamaIndex dense+sparse 结构。
    parser.add_argument("--enable-hybrid", action="store_true", default=parse_bool_value(read_env_value("QDRANT_ENABLE_HYBRID", "false")), help="显式创建 LlamaIndex hybrid dense+sparse collection。")
    # 2026-06-11 08:23:49 修改：添加 dense 向量名参数。理由：外部消费者可按 LlamaIndex 默认 text-dense 查询。
    parser.add_argument("--dense-vector-name", default=read_env_value("QDRANT_DENSE_VECTOR_NAME", LLAMAINDEX_DEFAULT_DENSE_VECTOR_NAME))
    # 2026-06-11 08:23:49 修改：添加 sparse 向量名参数。理由：外部消费者可按 LlamaIndex 默认 text-sparse-new 查询。
    parser.add_argument("--sparse-vector-name", default=read_env_value("QDRANT_SPARSE_VECTOR_NAME", LLAMAINDEX_DEFAULT_SPARSE_VECTOR_NAME))
    # 2026-06-12 09:52:34 修改：添加 sparse encoder 模型参数；作用：允许命令行或 profile 显式使用 Qdrant/bm25；理由：外部 QdrantVectorStore 会设置 fastembed_sparse_model="Qdrant/bm25"。
    parser.add_argument("--fastembed-sparse-model", default=read_env_value("QDRANT_FASTEMBED_SPARSE_MODEL", LLAMAINDEX_BM25_FASTEMBED_SPARSE_MODEL))
    # 2026-06-11 15:54:56 修改：添加 source profile 参数；作用：按数据源动态决定 embedding_text/prompt_text/payload/index 字段；理由：不同外部库不能共用固定 QA 字段模板。
    parser.add_argument("--source-profile", default=read_env_value("QDRANT_SOURCE_PROFILE", ""))
    # 添加 embedding 服务地址参数。
    parser.add_argument("--embedding-api-base", default=read_env_value("EMBEDDING_SERVICE_URL", "https://api.siliconflow.cn/v1"))
    # 添加 embedding API key 参数。
    parser.add_argument("--embedding-api-key", default=read_env_value("EMBEDDING_SERVICE_API_KEY", ""))
    # 添加 embedding 模型参数，默认跟现有 RAG.py 的 MODEL_EMBED 保持一致。
    parser.add_argument("--embedding-model", default=read_env_value("MODEL_EMBED", "Qwen/Qwen3-Embedding-0.6B"))
    # 添加 embedding 维度参数，默认 1024，和现有 RAG.py 里的 dimensions=1024 对齐。
    parser.add_argument("--embedding-dimension", type=int, default=int(read_env_value("EMBEDDING_DIMENSIONS", "1024")))
    # 添加 embedding 批量大小参数。
    parser.add_argument("--embedding-batch-size", type=int, default=int(read_env_value("EMBEDDING_MAX_CHUNKS_IN_BATCH", "10")))
    # 添加 Qdrant upsert 批量大小参数。
    parser.add_argument("--upsert-batch-size", type=int, default=64)
    # 添加 dry-run 参数。
    parser.add_argument("--dry-run", action="store_true", help="只读取和生成向量，不写入 Qdrant/SQL Server。")
    # 返回解析后的参数。
    return parser.parse_args()


def build_sqlserver_config(args: argparse.Namespace) -> SqlServerConfig:
    # 根据命令行参数构造 SQL Server 配置。
    return SqlServerConfig(
        # 写入 SQL Server 主机。
        server=args.sql_server,
        # 写入数据库名。
        database=args.sql_database,
        # 写入用户名。
        user=args.sql_user,
        # 写入密码。
        password=args.sql_password,
        # 写入 ODBC 驱动。
        driver=normalize_odbc_driver_name(args.sql_driver),
    )


def normalize_odbc_driver_name(driver_name: str) -> str:
    # URL 连接串常把空格写成加号，这里还原成 pyodbc 可识别的驱动名。
    normalized = driver_name.replace("+", " ").strip()
    # 如果外层已经带花括号，去掉花括号，后续 connection_string 会统一补。
    normalized = normalized.removeprefix("{").removesuffix("}")
    # 返回归一化后的驱动名。
    return normalized


def build_embedding_config(args: argparse.Namespace) -> EmbeddingConfig:
    # 如果没有配置 API key，就立刻报错，避免生成假向量。
    if not args.embedding_api_key:
        # 抛出明确异常。
        raise ValueError("缺少 EMBEDDING_SERVICE_API_KEY，不能生成生产 Qdrant 向量。")
    # 根据命令行参数构造 embedding 配置。
    return EmbeddingConfig(
        # 写入服务地址。
        api_base=args.embedding_api_base,
        # 写入 API key。
        api_key=args.embedding_api_key,
        # 写入模型名。
        model=args.embedding_model,
        # 写入向量维度。
        dimension=args.embedding_dimension,
        # 写入批量大小。
        batch_size=args.embedding_batch_size,
    )


def build_qdrant_config(args: argparse.Namespace) -> QdrantSyncConfig:
    # 根据命令行参数构造 Qdrant 同步配置。
    return QdrantSyncConfig(
        # 写入 Qdrant URL。
        url=args.qdrant_url,
        # 写入 collection 名称。
        collection_name=args.collection,
        # 写入距离度量。
        distance=args.distance,
        # 写入是否重建 collection。
        recreate_collection=args.recreate,
        # 写入 upsert 批量大小。
        upsert_batch_size=args.upsert_batch_size,
        # 写入 dry-run 标记。
        dry_run=args.dry_run,
        # 2026-06-11 08:23:49 修改：写入 hybrid 开关。理由：默认 dense 不变，显式开启才写 dense+sparse。
        enable_hybrid=getattr(args, "enable_hybrid", False),
        # 2026-06-11 08:23:49 修改：写入 dense 向量名。作用：匹配 LlamaIndex 官方默认。
        dense_vector_name=getattr(args, "dense_vector_name", LLAMAINDEX_DEFAULT_DENSE_VECTOR_NAME),
        # 2026-06-11 08:23:49 修改：写入 sparse 向量名。作用：匹配 LlamaIndex 官方默认。
        sparse_vector_name=getattr(args, "sparse_vector_name", LLAMAINDEX_DEFAULT_SPARSE_VECTOR_NAME),
        # 2026-06-12 09:52:34 修改：写入 sparse encoder 模型名；作用：传递给 LlamaIndex fastembed_sparse_encoder；理由：文档侧必须和外部查询侧 Qdrant/bm25 同源。
        fastembed_sparse_model=getattr(args, "fastembed_sparse_model", LLAMAINDEX_BM25_FASTEMBED_SPARSE_MODEL),
        # 2026-06-11 15:54:56 修改：写入 source profile 参数；作用：同步入口按 profile 解释字段；理由：保留统一 Qdrant 写入链路但支持动态数据源。
        source_profile=getattr(args, "source_profile", ""),
    )


# 2026-06-12 09:52:34 修改：定义 profile 到 Qdrant 配置的应用函数；作用：让数据源配置决定 collection、dense/hybrid、向量名和 sparse 模型；理由：不再靠人工记 --enable-hybrid，也不影响默认主链路。
def apply_source_profile_to_qdrant_config(config: QdrantSyncConfig, source_profile: Any) -> QdrantSyncConfig:
    # 2026-06-12 09:52:34 修改：读取 profile 声明的目标 collection；作用：外部库或 hybrid 影子库可独立落库；理由：不能误写主 agent collection。
    target_collection = getattr(source_profile, "target_collection", "") or config.collection_name
    # 2026-06-12 09:52:34 修改：读取 profile 声明的向量模式；作用：判断是否自动启用 hybrid；理由：修复实际同步时忘记 --enable-hybrid 的根因。
    qdrant_vector_mode = str(getattr(source_profile, "qdrant_vector_mode", "") or qdrant_mapping_profile.QDRANT_VECTOR_MODE_DENSE).strip().lower()
    # 2026-06-12 09:52:34 修改：判断 profile 是否要求 hybrid；作用：只让明确配置的外部库或影子库生成 sparse；理由：保护现有 dense-only 主 collection。
    profile_requests_hybrid = qdrant_vector_mode == qdrant_mapping_profile.QDRANT_VECTOR_MODE_HYBRID
    # 2026-06-12 09:52:34 修改：读取 dense 向量名；作用：profile 可覆盖但默认保持 LlamaIndex text-dense；理由：collection schema 和 point vector 必须同名。
    dense_vector_name = getattr(source_profile, "qdrant_dense_vector_name", "") or config.dense_vector_name
    # 2026-06-12 09:52:34 修改：读取 sparse 向量名；作用：profile 可覆盖但默认保持 LlamaIndex text-sparse-new；理由：外部 full hybrid 参数会按该名查询。
    sparse_vector_name = getattr(source_profile, "qdrant_sparse_vector_name", "") or config.sparse_vector_name
    # 2026-06-12 09:52:34 修改：读取 sparse 模型名；作用：把 Qdrant/bm25 传到文档侧 sparse encoder；理由：匹配外部 fastembed_sparse_model。
    fastembed_sparse_model = getattr(source_profile, "qdrant_fastembed_sparse_model", "") or config.fastembed_sparse_model
    # 2026-06-12 09:52:34 修改：返回替换后的 frozen 配置；作用：不原地修改调用方对象；理由：保持现有 dataclass 不可变语义。
    return replace(
        # 2026-06-12 09:52:34 修改：传入原配置；作用：只覆盖 profile 管辖字段；理由：URL、批大小、dry-run 等运行参数仍由调用方决定。
        config,
        # 2026-06-12 09:52:34 修改：写入 profile 目标 collection；作用：External_database 和 hybrid 影子库独立落库；理由：不污染 sql_rag_qa_chunks_v1。
        collection_name=target_collection,
        # 2026-06-12 09:52:34 修改：命令行显式开启或 profile 要求 hybrid 都开启；作用：兼容手动和配置驱动两种入口；理由：不能让 profile hybrid 被默认 False 覆盖。
        enable_hybrid=config.enable_hybrid or profile_requests_hybrid,
        # 2026-06-12 09:52:34 修改：写入 dense 向量名；作用：后续建库和写 point 共用；理由：避免 schema 和 point 不一致。
        dense_vector_name=dense_vector_name,
        # 2026-06-12 09:52:34 修改：写入 sparse 向量名；作用：后续建库和写 point 共用；理由：避免 text-sparse-new 缺失。
        sparse_vector_name=sparse_vector_name,
        # 2026-06-12 09:52:34 修改：写入 sparse 模型名；作用：build_qdrant_points 生成 sparse vector 时读取；理由：保证 BM25 查询侧和文档侧一致。
        fastembed_sparse_model=fastembed_sparse_model,
    )


def sqlserver_connection_string(config: SqlServerConfig) -> str:
    # 拼接 pyodbc 连接字符串。
    return (
        # 设置 ODBC 驱动。
        f"DRIVER={{{config.driver}}};"
        # 设置 SQL Server 地址。
        f"SERVER={config.server};"
        # 设置数据库名。
        f"DATABASE={config.database};"
        # 设置用户名。
        f"UID={config.user};"
        # 设置密码。
        f"PWD={config.password};"
        # 信任本地 SQL Server 证书。
        "TrustServerCertificate=yes;"
        # 关闭加密，匹配当前 Docker SQL Server 测试环境。
        "Encrypt=no;"
    )


def parse_json_object(raw_text: str | None) -> dict[str, Any]:
    # 空字符串直接返回空字典。
    if not raw_text:
        # 返回空字典。
        return {}
    # 尝试把 JSON 字符串解析成字典。
    try:
        # 执行 JSON 解析。
        parsed = json.loads(raw_text)
    # JSON 不合法时保留原文到 raw 字段。
    except json.JSONDecodeError:
        # 返回带 raw 的字典，避免同步中断。
        return {"raw": raw_text}
    # 解析结果是字典时直接返回。
    if isinstance(parsed, dict):
        # 返回字典。
        return parsed
    # 解析结果不是字典时包装成 value。
    return {"value": parsed}


def parse_json_list(raw_value: Any) -> list[Any]:
    # None 或空字符串返回空列表。
    if raw_value in (None, ""):
        return []
    # 已经是列表时直接返回。
    if isinstance(raw_value, list):
        return raw_value
    # 字符串尝试 JSON 解析。
    if isinstance(raw_value, str):
        try:
            parsed = json.loads(raw_value)
        except json.JSONDecodeError:
            return [raw_value] if raw_value.strip() else []
        if isinstance(parsed, list):
            return parsed
        if parsed in (None, ""):
            return []
        return [parsed]
    # 其他值作为单项列表。
    return [raw_value]


def normalize_string_list(raw_value: Any) -> list[str]:
    # 转成 JSON/list 后逐项清洗。
    return [str(item).strip() for item in parse_json_list(raw_value) if str(item).strip()]


def normalize_dict_list(raw_value: Any) -> list[dict[str, Any]]:
    # 只保留 dict 项。
    return [item for item in parse_json_list(raw_value) if isinstance(item, dict)]


def normalize_bool(value: Any, default: bool = True) -> bool:
    # None 使用默认值。
    if value is None:
        return default
    # bool 原样返回。
    if isinstance(value, bool):
        return value
    # 数字转 bool。
    if isinstance(value, (int, float)):
        return bool(value)
    # 字符串兼容常见写法。
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y"}:
        return True
    if text in {"0", "false", "no", "n"}:
        return False
    # 其他情况使用默认值。
    return default


def normalize_text(value: Any) -> str:
    # None 转空字符串。
    if value is None:
        # 返回空字符串。
        return ""
    # 非 None 统一转字符串并清理两侧空白。
    return str(value).strip()


def load_canonical_chunks_from_sqlserver(config: SqlServerConfig) -> list[CanonicalChunk]:
    # 定义 canonical chunk 查询 SQL。
    sql = """
SELECT
    chunks.chunk_id,
    chunks.document_id,
    chunks.audio_no,
    chunks.audio_title,
    chunks.chunk_index,
    chunks.scene,
    chunks.question,
    chunks.answer,
    chunks.cleaned_text,
    chunks.resolution_steps,
    chunks.keywords,
    chunks.entities_json,
    chunks.source_excerpt,
    chunks.content_hash,
    chunks.qa_pair_id,
    chunks.qa_pair_index,
    chunks.qa_similarity_score,
    chunks.qa_similarity_threshold,
    chunks.qa_pair_validated,
    chunks.cluster_id,
    chunks.cluster_label,
    chunks.cluster_level,
    chunks.cluster_path,
    chunks.global_cluster_id,
    chunks.global_cluster_label,
    chunks.global_cluster_level,
    chunks.global_cluster_path,
    chunks.question_hash,
    chunks.answer_hash,
    chunks.canonical_chunk_id,
    chunks.fusion_status,
    chunks.payload_schema_version,
    chunks.payload_json
FROM dbo.rag_qa_chunks AS chunks
WHERE chunks.qa_pair_validated = 1
  AND ISNULL(chunks.fusion_status, N'canonical') <> N'duplicate'
  AND chunks.chunk_id NOT IN (
      SELECT fusion.duplicate_chunk_id
      FROM dbo.rag_chunk_fusion_map AS fusion
  )
  AND NOT EXISTS (
      SELECT 1
      FROM dbo.rag_validation_issues AS issues
      WHERE issues.chunk_id = chunks.chunk_id
        AND issues.issue_level = N'error'
  )
ORDER BY chunks.document_id, chunks.chunk_index;
"""
    # 打开 SQL Server 连接。
    with pyodbc.connect(sqlserver_connection_string(config)) as connection:
        # 创建 cursor。
        cursor = connection.cursor()
        # 执行 canonical 查询。
        rows = cursor.execute(sql).fetchall()
    # 创建 chunk 列表。
    chunks: list[CanonicalChunk] = []
    # 遍历 SQL 查询结果。
    for row in rows:
        # 解析 payload_json，优先使用新契约字段。
        payload_json = parse_json_object(row.payload_json)
        # 读取问题。
        question = normalize_text(payload_json.get("question") or row.question)
        # 读取答案。
        answer = normalize_text(payload_json.get("answer_text") or payload_json.get("answer") or row.answer)
        # 读取清洗文本。
        cleaned_text = normalize_text(payload_json.get("cleaned_text") or row.cleaned_text)
        # 读取完整来源摘录。
        source_excerpt_full = normalize_text(payload_json.get("source_excerpt_full") or payload_json.get("source_excerpt") or row.source_excerpt)
        # 旧 v2 数据可能只有截断 source_excerpt，必须用完整 question + answer 重建同步契约。
        if answer and answer not in source_excerpt_full:
            source_excerpt_full = f"问题：{question}\n答案：{answer}"
        # 读取 LLM 消费文本。
        llm_text = normalize_text(payload_json.get("llm_text"))
        # 读取检索文本。
        retrieval_text = normalize_text(payload_json.get("retrieval_text"))
        # 把当前行转换成 CanonicalChunk。
        chunks.append(
            CanonicalChunk(
                # 读取 chunk_id。
                chunk_id=normalize_text(row.chunk_id),
                # 读取 document_id。
                document_id=normalize_text(row.document_id),
                # 读取 audio_no。
                audio_no=int(row.audio_no or 0),
                # 读取 audio_title。
                audio_title=normalize_text(row.audio_title),
                # 读取 chunk_index。
                chunk_index=int(row.chunk_index or 0),
                # 读取 scene。
                scene=normalize_text(row.scene),
                # 读取 question。
                question=question,
                # 读取 answer。
                answer=answer,
                # 读取 cleaned_text。
                cleaned_text=cleaned_text,
                # 读取 resolution_steps。
                resolution_steps=normalize_text(row.resolution_steps),
                # 读取 keywords。
                keywords=normalize_text(row.keywords),
                # 读取 entities_json。
                entities_json=normalize_text(row.entities_json),
                # 读取 source_excerpt。
                source_excerpt=normalize_text(payload_json.get("source_excerpt") or row.source_excerpt),
                # 读取 content_hash。
                content_hash=normalize_text(row.content_hash),
                # 读取 qa_pair_id。
                qa_pair_id=normalize_text(row.qa_pair_id),
                # 读取 qa_pair_index。
                qa_pair_index=int(row.qa_pair_index or 0),
                # 读取 qa_similarity_score。
                qa_similarity_score=float(row.qa_similarity_score or 0.0),
                # 读取 qa_similarity_threshold。
                qa_similarity_threshold=float(row.qa_similarity_threshold or 0.0),
                # 读取 qa_pair_validated。
                qa_pair_validated=bool(row.qa_pair_validated),
                # 读取 cluster_id。
                cluster_id=normalize_text(row.cluster_id),
                # 读取 cluster_label。
                cluster_label=normalize_text(row.cluster_label),
                # 读取 cluster_level。
                cluster_level=normalize_text(row.cluster_level),
                # 读取 cluster_path。
                cluster_path=normalize_text(row.cluster_path),
                # 读取 global_cluster_id。
                global_cluster_id=normalize_text(row.global_cluster_id),
                # 读取 global_cluster_label。
                global_cluster_label=normalize_text(row.global_cluster_label),
                # 读取 global_cluster_level。
                global_cluster_level=normalize_text(row.global_cluster_level),
                # 读取 global_cluster_path。
                global_cluster_path=normalize_text(row.global_cluster_path),
                # 读取 question_hash。
                question_hash=normalize_text(row.question_hash),
                # 读取 answer_hash。
                answer_hash=normalize_text(row.answer_hash),
                # 读取 canonical_chunk_id。
                canonical_chunk_id=normalize_text(row.canonical_chunk_id),
                # 读取 fusion_status。
                fusion_status=normalize_text(row.fusion_status or "canonical"),
                # 读取 payload_schema_version。
                payload_schema_version=normalize_text(payload_json.get("payload_schema_version") or row.payload_schema_version),
                # 解析 payload_json。
                payload_json=payload_json,
                # 读取 RAG 消费契约版本。
                rag_contract_version=normalize_text(payload_json.get("rag_contract_version") or "qa-rag-contract-v1"),
                # 读取规范问题。
                canonical_question=normalize_text(payload_json.get("canonical_question") or question),
                # 读取答案优先字段。
                answer_text=answer,
                # 读取 query aliases。
                query_aliases=normalize_string_list(payload_json.get("query_aliases")),
                # 读取完整来源摘录。
                source_excerpt_full=source_excerpt_full,
                # 读取 LLM 消费文本。
                llm_text=llm_text,
                # 读取向量检索文本。
                retrieval_text=retrieval_text,
                # 读取 duplicate 上下文。
                duplicate_contexts=normalize_dict_list(payload_json.get("duplicate_contexts")),
                # 读取合并 duplicate chunk IDs。
                merged_duplicate_chunk_ids=normalize_string_list(payload_json.get("merged_duplicate_chunk_ids")),
                # 读取 Qdrant ready。
                qdrant_ready=normalize_bool(payload_json.get("qdrant_ready"), default=True),
                # 读取校验标记。
                validation_flags=normalize_string_list(payload_json.get("validation_flags")),
            )
        )
    # 返回 canonical chunks。
    return chunks


def build_answer_first_text(chunk: CanonicalChunk) -> str:
    # 2026-06-11 15:54:56 修改：优先读取 profile 生成的 prompt_text；作用：外部库可只把干净正文交给 LlamaIndex text；理由：避免全量 payload 或硬编码 QA 拼接给模型制造噪声。
    profile_prompt_text = normalize_text(qdrant_mapping_profile.profile_payload_value(chunk, qdrant_mapping_profile.PROFILE_PROMPT_TEXT_KEY))
    # 读取答案优先字段。
    answer = chunk.answer_text or chunk.answer
    # 2026-06-11 15:54:56 修改：如果 profile 已生成 prompt_text 就直接返回；作用：让字段映射配置成为 prompt 正文来源；理由：外部库 prompt 字段必须由 profile 决定。
    if profile_prompt_text and (qdrant_mapping_profile.is_generic_profile_chunk(chunk) or not answer or answer in profile_prompt_text):
        # 2026-06-11 15:54:56 修改：返回 profile prompt_text；作用：保护外部库动态模板；理由：不再强制把 answer/evidence/scene 全部拼进去。
        return profile_prompt_text
    # 已有 llm_text 且包含完整答案时优先使用。
    if chunk.llm_text and answer and answer in chunk.llm_text:
        return chunk.llm_text
    # 解析操作步骤。
    steps = normalize_string_list(chunk.resolution_steps)
    # 组装 duplicate 融合上下文。
    duplicate_texts = [
        normalize_text(context.get("cleaned_text") or context.get("source_excerpt"))
        for context in chunk.duplicate_contexts
        if normalize_text(context.get("cleaned_text") or context.get("source_excerpt"))
    ]
    # 构造答案优先文本。
    parts = [
        f"标准答案：{answer}",
        f"用户问题：{chunk.question}",
        f"规范问题：{chunk.canonical_question or chunk.question}",
        f"业务场景：{chunk.scene}",
        f"全局主题：{chunk.global_cluster_label}",
    ]
    # 追加操作步骤。
    if steps:
        parts.append("操作步骤：" + "；".join(steps))
    # 追加 query aliases。
    if chunk.query_aliases:
        parts.append("相关问法：" + "；".join(chunk.query_aliases))
    # 追加兼容问答文本。
    if chunk.cleaned_text:
        parts.append("兼容问答文本：" + chunk.cleaned_text)
    # 追加完整来源摘录。
    if chunk.source_excerpt_full and chunk.source_excerpt_full != chunk.cleaned_text:
        parts.append("完整来源摘录：" + chunk.source_excerpt_full)
    # 追加 duplicate 上下文。
    if duplicate_texts:
        parts.append("已融合重复上下文：" + "\n".join(duplicate_texts))
    # 返回完整消费文本。
    return "\n".join(part for part in parts if part and not part.endswith("：")).strip()


def build_embedding_text(chunk: CanonicalChunk) -> str:
    # 2026-06-11 15:54:56 修改：优先读取 profile 生成的 embedding_text；作用：外部库可指定 standard_question 等字段单独向量化；理由：向量召回字段不能硬编码成 QA 全字段拼接。
    profile_embedding_text = normalize_text(qdrant_mapping_profile.profile_payload_value(chunk, qdrant_mapping_profile.PROFILE_EMBEDDING_TEXT_KEY))
    # 读取答案优先字段。
    answer = chunk.answer_text or chunk.answer
    # 2026-06-11 15:54:56 修改：如果 profile 已生成 embedding_text 就直接返回；作用：让 embedding 字段选择由 source_profiles 管理；理由：避免答案和证据文本带偏召回方向。
    if profile_embedding_text and (qdrant_mapping_profile.is_generic_profile_chunk(chunk) or not answer or answer in profile_embedding_text):
        # 2026-06-11 15:54:56 修改：返回 profile embedding_text；作用：支持不同库使用不同召回字段；理由：不影响没有 profile 的旧 getai 数据。
        return profile_embedding_text
    # 优先使用 payload_json 中的 retrieval_text。
    if chunk.retrieval_text and answer and answer in chunk.retrieval_text:
        return chunk.retrieval_text
    # 拼接问题、答案、别名、场景和聚类信息，让向量表达更贴近问答检索。
    return textwrap.dedent(
        f"""
        业务场景：{chunk.scene}
        全局主题：{chunk.global_cluster_label}
        问题：{chunk.question}
        规范问题：{chunk.canonical_question or chunk.question}
        相关问法：{"；".join(chunk.query_aliases)}
        答案：{answer}
        操作/上下文：{build_answer_first_text(chunk)}
        """
    ).strip()


def build_qdrant_point_id(chunk_id: str) -> str:
    # 用 UUID5 把业务 chunk_id 稳定映射成 Qdrant 官方支持的 UUID 字符串。
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"sql-rag-qa-chunk:{chunk_id}"))



def append_unique_keyword_terms(keyword_terms: list[str], raw_terms: Any) -> None:
    # 2026-06-10 18:01:50 修改：合并多来源关键词。理由：Qdrant KEYWORD index 需要 list[str]。
    for term in normalize_string_list(raw_terms):
        # 2026-06-10 18:01:50 修改：清理单个关键词。作用：过滤空白和 None。
        normalized_term = normalize_text(term)
        # 2026-06-10 18:01:50 修改：跳过空关键词。理由：空值不应进入 Qdrant filter。
        if not normalized_term:
            # 2026-06-10 18:01:50 修改：继续下一项。作用：保持列表干净。
            continue
        # 2026-06-10 18:01:50 修改：跳过重复词。理由：减少 payload 噪声。
        if normalized_term in keyword_terms:
            # 2026-06-10 18:01:50 修改：继续下一项。作用：保留首次出现顺序。
            continue
        # 2026-06-10 18:01:50 修改：追加唯一关键词。作用：生成 Qdrant 可索引字段。
        keyword_terms.append(normalized_term)


def build_qdrant_keyword_terms(chunk: CanonicalChunk) -> list[str]:
    # 2026-06-10 18:01:50 修改：创建规范关键词列表。理由：原 keywords 是字符串。
    keyword_terms: list[str] = []
    # 2026-06-11 15:54:56 修改：优先合入 profile 生成的关键词；作用：让外部库 keyword_index.fields 进入统一 keyword_terms；理由：不同库可按自己的字段建立 Qdrant KEYWORD 过滤入口。
    append_unique_keyword_terms(keyword_terms, qdrant_mapping_profile.profile_payload_value(chunk, qdrant_mapping_profile.PROFILE_KEYWORD_TERMS_KEY, []))
    # 2026-06-10 18:01:50 修改：合入 keywords。作用：兼容清洗阶段关键词。
    append_unique_keyword_terms(keyword_terms, chunk.keywords)
    # 2026-06-10 18:01:50 修改：合入 query_aliases。理由：外部 RAG 常用别名问法过滤。
    append_unique_keyword_terms(keyword_terms, chunk.query_aliases)
    # 2026-06-10 18:01:50 修改：合入 scene。作用：让 Qdrant WEB UI 可见场景词。
    append_unique_keyword_terms(keyword_terms, chunk.scene)
    # 2026-06-10 18:01:50 修改：合入 canonical_question。理由：标准问法是稳定索引入口。
    append_unique_keyword_terms(keyword_terms, chunk.canonical_question or chunk.question)
    # 2026-06-10 18:01:50 修改：合入 question。作用：兼容用户原始问法。
    append_unique_keyword_terms(keyword_terms, chunk.question)
    # 2026-06-10 18:01:50 修改：返回去重列表。理由：Qdrant KEYWORD index 支持 list[str]。
    return keyword_terms

def build_qdrant_payload(chunk: CanonicalChunk, embedding_config: EmbeddingConfig) -> dict[str, Any]:
    # 构造答案优先 LLM 消费文本。
    llm_text = build_answer_first_text(chunk)
    # 构造向量检索文本。
    retrieval_text = build_embedding_text(chunk)
    # 读取答案优先字段。
    answer_text = chunk.answer_text or chunk.answer
    # 读取完整来源摘录。
    source_excerpt_full = chunk.source_excerpt_full or chunk.source_excerpt or chunk.cleaned_text
    # 2026-06-11 15:54:56 修改：读取 profile 嵌套 payload；作用：保留外部库原字段；理由：字段不做向量化也必须可展示、过滤和回表。
    profile_source_payload = qdrant_mapping_profile.profile_payload_value(chunk, qdrant_mapping_profile.PROFILE_SOURCE_PAYLOAD_KEY, {})
    # 2026-06-11 15:54:56 修改：兜底规范 profile payload 类型；作用：避免非 dict 写入破坏 Qdrant payload；理由：外部库字段结构不完全可控。
    if not isinstance(profile_source_payload, dict):
        # 2026-06-11 15:54:56 修改：非字典时降为空字典；作用：保持 payload 契约稳定；理由：Qdrant 顶层 payload 需要明确字段。
        profile_source_payload = {}
    # 2026-06-11 15:54:56 修改：读取 profile 来源名；作用：Qdrant WebUI 可区分 getai 和外部库；理由：统一写入后必须可追溯。
    profile_source_name = normalize_text(qdrant_mapping_profile.profile_payload_value(chunk, qdrant_mapping_profile.PROFILE_SOURCE_NAME_KEY))
    # 2026-06-11 15:54:56 修改：读取 profile 来源表；作用：支持外部库回表定位；理由：不同外部表进入 Qdrant 后不能丢来源。
    profile_source_table = normalize_text(qdrant_mapping_profile.profile_payload_value(chunk, qdrant_mapping_profile.PROFILE_SOURCE_TABLE_KEY))
    # 2026-06-11 15:54:56 修改：读取 profile 来源主键；作用：支持定位原始行；理由：外部库不一定有 chunk_id 语义。
    profile_source_pk = normalize_text(qdrant_mapping_profile.profile_payload_value(chunk, qdrant_mapping_profile.PROFILE_SOURCE_PK_KEY))
    # 2026-06-11 15:54:56 修改：读取 profile 名称；作用：payload 里可看到使用的映射策略；理由：多数据源排查必须知道字段策略来源。
    mapping_profile_name = normalize_text(qdrant_mapping_profile.profile_payload_value(chunk, qdrant_mapping_profile.PROFILE_NAME_PAYLOAD_KEY))
    # 2026-06-11 15:54:56 修改：读取 profile 契约模式；作用：区分 QA 严格契约和 generic 泛化契约；理由：校验和排查都需要可见。
    profile_contract_mode = normalize_text(qdrant_mapping_profile.profile_payload_value(chunk, qdrant_mapping_profile.PROFILE_CONTRACT_MODE_KEY))
    # 2026-06-11 15:54:56 修改：读取 profile 目标 collection；作用：排查命令行覆盖时可见；理由：避免外部库误写主 collection 难以发现。
    profile_target_collection = normalize_text(qdrant_mapping_profile.profile_payload_value(chunk, qdrant_mapping_profile.PROFILE_TARGET_COLLECTION_KEY))
    # 2026-06-12 14:40:11 修改：读取 profile payload 模式；作用：决定输出旧 QA 大 payload 还是外部库严格 payload；理由：sql_External_database 不能混入 getai 专用字段。
    profile_payload_mode = normalize_text(qdrant_mapping_profile.profile_payload_value(chunk, qdrant_mapping_profile.PROFILE_PAYLOAD_MODE_KEY))
    # 2026-06-12 15:30:17 修改：读取 YAML Qdrant payload 布局；作用：profile_rendered 模式按配置渲染最终字段；理由：未来外部库字段形态变化时不能再新增 Python 分支。
    profile_qdrant_payload_layout = qdrant_mapping_profile.profile_payload_value(chunk, qdrant_mapping_profile.PROFILE_QDRANT_PAYLOAD_LAYOUT_KEY, {})
    # 2026-06-12 14:40:11 修改：构造统一关键词列表；作用：严格和旧 QA 两种 payload 都复用同一关键词生成逻辑；理由：避免外部库过滤字段和 legacy 逻辑分叉。
    keyword_terms = build_qdrant_keyword_terms(chunk)
    # 2026-06-12 15:30:17 修改：判断是否为 YAML 渲染 payload；作用：让每个外部库完全按自己的 qdrant_payload 布局写 Qdrant；理由：程序只做解释器，不按外部库字段形态写死分支。
    if profile_payload_mode == qdrant_mapping_profile.PAYLOAD_MODE_PROFILE_RENDERED:
        # 2026-06-12 15:30:17 修改：返回 YAML 渲染结果；作用：只写 top_level/objects 声明的字段；理由：sql_External_database 不能自动混入 doc_id/text/source_* 等无用顶层字段。
        return qdrant_mapping_profile.render_qdrant_payload_from_layout(
            # 2026-06-12 15:30:17 修改：传入 chunk；作用：允许未来 YAML 显式引用 chunk.xxx；理由：保留灵活性但不自动输出内部字段。
            chunk=chunk,
            # 2026-06-12 15:30:17 修改：传入 profile 布局；作用：由 YAML 决定最终 payload 结构；理由：一库一配置、一库一结构。
            qdrant_payload_layout=profile_qdrant_payload_layout,
            # 2026-06-12 15:30:17 修改：传入向量文本；作用：支持 from: embedding_text；理由：当前 retrieval_text 要等于 standard_question + id。
            embedding_text=retrieval_text,
            # 2026-06-12 15:30:17 修改：传入 prompt 文本；作用：需要时 YAML 可显式存 text；理由：是否保留答案正文由配置决定。
            prompt_text=llm_text,
            # 2026-06-12 15:30:17 修改：传入打包业务 payload；作用：支持 payload.xxx 和 objects.payload.include；理由：其他字段必须由 YAML 打包。
            source_payload=profile_source_payload,
            # 2026-06-12 15:30:17 修改：传入关键词列表；作用：未来外部库可显式声明 keyword_terms；理由：当前库不声明则不输出。
            keyword_terms=keyword_terms,
        )
    # 2026-06-12 14:40:11 修改：判断是否为严格 profile payload；作用：外部库只输出最小 Qdrant 消费契约；理由：用户要求其他字段全部打包进 payload，不能摊平成 getai 字段。
    if profile_payload_mode == qdrant_mapping_profile.PAYLOAD_MODE_PROFILE_STRICT:
        # 2026-06-12 14:40:11 修改：返回严格 payload；作用：仅保留 LlamaIndex 检索和回表必需字段；理由：sql_External_database 要和 sql_rag_qa_chunks_v1 字段隔离。
        return {
            # 2026-06-12 14:40:11 修改：写入 LlamaIndex doc_id；作用：兼容 index_doc_id=True 的官方默认过滤；理由：外部消费者无需知道旧 document_id 字段。
            LLAMAINDEX_DOCUMENT_ID_PAYLOAD_KEY: chunk.document_id,
            # 2026-06-12 14:40:11 修改：写入 text 正文；作用：供 LlamaIndex/外部 RAG 读取答案上下文；理由：只向量化问题不代表丢答案。
            "text": llm_text,
            # 2026-06-12 14:40:11 修改：写入 retrieval_text；作用：让 WebUI 可直接核对实际向量文本；理由：standard_question + id 必须可见且不含答案噪声。
            "retrieval_text": retrieval_text,
            # 2026-06-12 14:40:11 修改：写入来源名；作用：区分 External_database 和后续其他外部库；理由：统一 collection 排查必须可追溯。
            "source_name": profile_source_name,
            # 2026-06-12 14:40:11 修改：写入来源表；作用：支持回表定位；理由：外部库字段打包后仍要知道原始表。
            "source_table": profile_source_table,
            # 2026-06-12 14:40:11 修改：写入来源主键；作用：保持 point 身份和回表稳定；理由：新增 id 只是普通序号，source_pk 仍应使用 external_id。
            "source_pk": profile_source_pk,
            # 2026-06-12 14:40:11 修改：写入嵌套业务 payload；作用：保存 id、external_id、question、answer 等外部字段；理由：其他字段必须打包而不是混到顶层。
            "payload": profile_source_payload,
            # 2026-06-12 14:40:11 修改：写入关键词列表；作用：支持 Qdrant 关键词过滤和 WebUI 检查；理由：严格模式仍需要最小检索辅助字段。
            "keyword_terms": keyword_terms,
            # 2026-06-12 14:40:11 修改：写入 profile 名；作用：排查 point 使用的字段策略；理由：多外部库接入时需要知道配置来源。
            "mapping_profile_name": mapping_profile_name,
        }
    # 构造 Qdrant point payload，payload 只放检索过滤和回表所需的元数据。
    payload = {
        # 保存原始 chunk_id，RAG 命中后可回 SQL Server 补全完整关系。
        "chunk_id": chunk.chunk_id,
        # 2026-06-11 15:54:56 修改：写入统一 record_id；作用：给外部消费者一个不依赖 QA 命名的主键字段；理由：不同数据源统一最小消费契约需要 record_id。
        "record_id": chunk.chunk_id,
        # 保存 Qdrant point id，方便外部机器直接 retrieve。
        "point_id": build_qdrant_point_id(chunk.chunk_id),
        # 保存 document_id，支持按文档过滤。
        "document_id": chunk.document_id,
        # 2026-06-10 18:01:50 修改：写入 LlamaIndex doc_id。理由：兼容 index_doc_id=True 默认查询。
        LLAMAINDEX_DOCUMENT_ID_PAYLOAD_KEY: chunk.document_id,
        # 2026-06-11 15:54:56 修改：写入 profile 来源名；作用：区分不同数据源；理由：统一写入链路必须保留来源身份。
        "source_name": profile_source_name or "getai",
        # 2026-06-11 15:54:56 修改：写入 profile 来源表；作用：支持回表定位；理由：外部库接入时不能丢原表信息。
        "source_table": profile_source_table or "dbo.rag_qa_chunks",
        # 2026-06-11 15:54:56 修改：写入 profile 来源主键；作用：支持定位原始行；理由：外部库主键不一定等于 chunk_id。
        "source_pk": profile_source_pk or chunk.chunk_id,
        # 2026-06-11 15:54:56 修改：写入 mapping profile 名称；作用：排查当前 point 用哪份字段策略；理由：多外部库共存时必须透明。
        "mapping_profile_name": mapping_profile_name or qdrant_mapping_profile.DEFAULT_SOURCE_PROFILE_NAME,
        # 2026-06-11 15:54:56 修改：写入 profile 契约模式；作用：标记 qa/generic；理由：避免外部消费者误按 QA 严格契约理解所有 point。
        "profile_contract_mode": profile_contract_mode or "qa",
        # 2026-06-11 15:54:56 修改：写入 profile 目标 collection；作用：调试命令行覆盖；理由：降低误写 collection 的排查成本。
        "profile_target_collection": profile_target_collection,
        # 2026-06-11 15:54:56 修改：写入嵌套业务 payload；作用：保存 profile.include 字段；理由：模型正文、向量字段、业务 metadata 需要隔离。
        "payload": profile_source_payload,
        # 保存音频编号。
        "audio_no": chunk.audio_no,
        # 保存音频标题。
        "audio_title": chunk.audio_title,
        # 保存 chunk 序号。
        "chunk_index": chunk.chunk_index,
        # 保存业务场景。
        "scene": chunk.scene,
        # 保存问题文本。
        "question": chunk.question,
        # 保存答案文本。
        "answer": chunk.answer,
        # 保存规范问题。
        "canonical_question": chunk.canonical_question or chunk.question,
        # 保存答案优先字段。
        "answer_text": answer_text,
        # 保存 query aliases。
        "query_aliases": chunk.query_aliases,
        # 保存清洗文本。
        "cleaned_text": chunk.cleaned_text,
        # 保存解决步骤。
        "resolution_steps": chunk.resolution_steps,
        # 保存关键词。
        "keywords": chunk.keywords,
        # 2026-06-10 18:01:50 修改：写入 keyword_terms。作用：Qdrant KEYWORD index 和 WEB UI 可见。
        "keyword_terms": keyword_terms,
        # 保存实体 JSON 字符串。
        "entities_json": chunk.entities_json,
        # 保存来源片段。
        "source_excerpt": chunk.source_excerpt,
        # 保存完整来源片段。
        "source_excerpt_full": source_excerpt_full,
        # 保存 LLM 直接消费文本。
        "llm_text": llm_text,
        # 保存向量检索文本。
        "retrieval_text": retrieval_text,
        # 保存 duplicate 融合上下文。
        "duplicate_contexts": chunk.duplicate_contexts,
        # 保存已合入 canonical 的 duplicate chunk IDs。
        "merged_duplicate_chunk_ids": chunk.merged_duplicate_chunk_ids,
        # 保存 Qdrant 同步契约状态。
        "qdrant_ready": chunk.qdrant_ready,
        # 保存校验标记。
        "validation_flags": chunk.validation_flags,
        # 保存内容 hash。
        "content_hash": chunk.content_hash,
        # 保存 QA 成对 ID。
        "qa_pair_id": chunk.qa_pair_id,
        # 保存 QA 成对序号。
        "qa_pair_index": chunk.qa_pair_index,
        # 保存 QA 相似度分数。
        "qa_similarity_score": chunk.qa_similarity_score,
        # 保存 QA 相似度阈值。
        "qa_similarity_threshold": chunk.qa_similarity_threshold,
        # 保存 QA 校验状态。
        "qa_pair_validated": chunk.qa_pair_validated,
        # 保存文档内聚类 ID。
        "cluster_id": chunk.cluster_id,
        # 保存文档内聚类标签。
        "cluster_label": chunk.cluster_label,
        # 保存文档内聚类层级。
        "cluster_level": chunk.cluster_level,
        # 保存文档内聚类路径。
        "cluster_path": chunk.cluster_path,
        # 保存全局聚类 ID。
        "global_cluster_id": chunk.global_cluster_id,
        # 保存全局聚类标签。
        "global_cluster_label": chunk.global_cluster_label,
        # 保存全局聚类层级。
        "global_cluster_level": chunk.global_cluster_level,
        # 保存全局聚类路径。
        "global_cluster_path": chunk.global_cluster_path,
        # 保存问题 hash。
        "question_hash": chunk.question_hash,
        # 保存答案 hash。
        "answer_hash": chunk.answer_hash,
        # 保存 canonical chunk ID。
        "canonical_chunk_id": chunk.canonical_chunk_id,
        # 保存融合状态。
        "fusion_status": chunk.fusion_status,
        # 保存 payload schema 版本。
        "payload_schema_version": chunk.payload_schema_version,
        # 保存 RAG 消费契约版本。
        "rag_contract_version": chunk.rag_contract_version,
        # 保存 embedding 模型名。
        "embedding_model": embedding_config.model,
        # 保存 embedding 维度。
        "embedding_dimension": embedding_config.dimension,
        # 2026-06-11 15:54:56 修改：按 profile 写入同步来源；作用：外部库 point 不再误显示 getai；理由：多数据源统一写入后必须能准确回溯来源库表。
        "sync_source": f"sqlserver:{profile_source_name or 'getai'}.{profile_source_table or 'dbo.rag_qa_chunks'}",
        # 保存文本字段，兼容部分 RAG loader 默认读取 text 的习惯。
        "text": llm_text,
    }
    # 2026-06-11 15:54:56 修改：把 profile.include 字段同时补到顶层但不覆盖核心字段；作用：Qdrant WebUI 和 filter 能直接看到外部字段；理由：外部消费者按字段过滤时不应必须解析嵌套 payload。
    for profile_field_name, profile_field_value in profile_source_payload.items():
        # 2026-06-11 15:54:56 修改：使用 setdefault 保留核心字段优先级；作用：避免外部字段覆盖 text/doc_id/chunk_id 等统一契约；理由：最小消费契约必须稳定。
        payload.setdefault(profile_field_name, profile_field_value)
    # 2026-06-11 15:54:56 修改：返回最终 payload；作用：兼容旧字段并追加动态字段；理由：主 agent 和外部 RAG 都能消费。
    return payload


def chunk_list(items: list[Any], batch_size: int) -> list[list[Any]]:
    # 创建批次结果。
    batches: list[list[Any]] = []
    # 按 batch_size 切分列表。
    for start_index in range(0, len(items), batch_size):
        # 追加当前批次。
        batches.append(items[start_index : start_index + batch_size])
    # 返回批次列表。
    return batches


def create_embedding_client(config: EmbeddingConfig) -> OpenAI:
    # 创建 OpenAI-compatible embedding 客户端。
    return OpenAI(api_key=config.api_key, base_url=config.api_base)


def embed_texts(client: OpenAI, texts: list[str], config: EmbeddingConfig) -> list[list[float]]:
    # 调用 OpenAI-compatible embeddings API 生成向量。
    response = client.embeddings.create(
        # 传入 embedding 模型名。
        model=config.model,
        # 传入当前批次文本。
        input=texts,
        # 显式指定维度，确保和 Qdrant collection vector size 一致。
        dimensions=config.dimension,
    )
    # 按 API 返回顺序取出 embedding。
    embeddings = [item.embedding for item in response.data]
    # 如果返回数量不一致，立即报错。
    if len(embeddings) != len(texts):
        # 抛出明确异常。
        raise RuntimeError(f"embedding 返回数量不一致：请求 {len(texts)} 条，返回 {len(embeddings)} 条。")
    # 校验每条向量维度。
    for embedding in embeddings:
        # 维度不一致时立即报错，避免写入错误 collection。
        if len(embedding) != config.dimension:
            # 抛出明确异常。
            raise RuntimeError(f"embedding 维度不一致：期望 {config.dimension}，实际 {len(embedding)}。")
    # 返回向量列表。
    return embeddings


def qdrant_distance(distance_name: str) -> models.Distance:
    # 统一距离名大小写。
    normalized = distance_name.strip().upper()
    # Cosine 距离。
    if normalized == "COSINE":
        # 返回 Qdrant 官方 Cosine 枚举。
        return models.Distance.COSINE
    # Dot 距离。
    if normalized == "DOT":
        # 返回 Qdrant 官方 Dot 枚举。
        return models.Distance.DOT
    # Euclid 距离。
    if normalized in {"EUCLID", "EUCLIDEAN"}:
        # 返回 Qdrant 官方 Euclid 枚举。
        return models.Distance.EUCLID
    # 未知距离直接报错。
    raise ValueError(f"不支持的 Qdrant distance：{distance_name}")


def ensure_qdrant_collection(client: QdrantClient, config: QdrantSyncConfig, embedding_config: EmbeddingConfig) -> None:
    # 2026-06-11 15:54:56 修改：加载 source profile；作用：payload index 可按数据源动态补齐；理由：不同外部库过滤字段不应写死在 Python 里。
    source_profile = qdrant_mapping_profile.load_source_profile(config.source_profile)
    # 判断 collection 是否存在。
    exists = client.collection_exists(config.collection_name)
    # 如果 dry-run，跳过实际建库动作。
    if config.dry_run:
        # 直接返回。
        return
    # 如果要求重建且 collection 已存在，先删除。
    if exists and config.recreate_collection:
        # 使用 Qdrant 官方 delete_collection API 删除旧 collection。
        client.delete_collection(collection_name=config.collection_name)
        # 更新存在状态。
        exists = False
    # 2026-06-11 08:23:49 修改：构造 dense VectorParams。理由：dense 与 hybrid 两种 collection 共用同一维度和距离。
    dense_vector_config = models.VectorParams(
        # 2026-06-11 08:23:49 修改：设置向量维度。作用：保持 embedding 维度契约不变。
        size=embedding_config.dimension,
        # 2026-06-11 08:23:49 修改：设置距离度量。作用：保持原相似度排序逻辑。
        distance=qdrant_distance(config.distance),
    )
    # 如果 collection 不存在，创建新 collection。
    if not exists:
        # 2026-06-11 08:23:49 修改：hybrid 模式创建命名 dense+sparse collection。理由：匹配 LlamaIndex enable_hybrid=True。
        if config.enable_hybrid:
            # 2026-06-11 08:23:49 修改：使用 Qdrant 官方 create_collection 创建 hybrid collection。作用：外部 RAG 可同时查 dense 和 sparse。
            client.create_collection(
                # 2026-06-11 08:23:49 修改：指定 collection 名称。作用：保持目标库可控。
                collection_name=config.collection_name,
                # 2026-06-11 08:23:49 修改：写入命名 dense vector。理由：LlamaIndex hybrid 默认 using=text-dense。
                vectors_config={config.dense_vector_name: dense_vector_config},
                # 2026-06-11 08:23:49 修改：写入 sparse vector 配置。理由：LlamaIndex hybrid 默认 using=text-sparse-new。
                sparse_vectors_config={config.sparse_vector_name: models.SparseVectorParams(index=models.SparseIndexParams())},
            )
        # 2026-06-11 08:23:49 修改：默认模式仍创建旧单 dense collection。理由：不影响当前 agent 消费链路。
        else:
            # 使用 Qdrant 官方 create_collection API 创建向量集合。
            client.create_collection(
                # 指定 collection 名称。
                collection_name=config.collection_name,
                # 指定向量维度和距离度量。
                vectors_config=dense_vector_config,
            )
        # 创建 payload 索引，方便其他机器按字段过滤。
        create_payload_indexes(client, config.collection_name, source_profile)
        # 创建完成后返回。
        return
    # collection 已存在时读取 collection 信息。
    collection_info = client.get_collection(collection_name=config.collection_name)
    # 读取当前 collection 的向量配置。
    vectors_config = collection_info.config.params.vectors
    # 2026-06-11 08:23:49 修改：读取当前 collection 的 sparse 配置。理由：hybrid 模式必须校验 sparse vector 存在。
    sparse_vectors_config = getattr(collection_info.config.params, "sparse_vectors", None) or {}
    # 2026-06-11 08:23:49 修改：hybrid 不能套用旧单向量 collection。理由：否则 LlamaIndex 查询 using=text-dense/text-sparse-new 会失败。
    if config.enable_hybrid and not isinstance(vectors_config, dict):
        # 2026-06-11 08:23:49 修改：抛出明确异常。作用：要求新建或显式 --recreate hybrid collection。
        raise RuntimeError("Qdrant collection 已存在但不是 LlamaIndex hybrid 命名向量结构，请使用新 collection 或加 --recreate 重建。")
    # 2026-06-11 08:23:49 修改：hybrid 必须存在指定 dense 名。理由：外部 LlamaIndex 查询会用 text-dense。
    if config.enable_hybrid and config.dense_vector_name not in vectors_config:
        # 2026-06-11 08:23:49 修改：抛出明确异常。作用：避免写入一个外部无法 hybrid 查询的 collection。
        raise RuntimeError(f"Qdrant hybrid collection 缺少 dense 向量名：{config.dense_vector_name}。")
    # 2026-06-11 08:23:49 修改：hybrid 必须存在指定 sparse 名。理由：外部 LlamaIndex 查询会用 text-sparse-new。
    if config.enable_hybrid and config.sparse_vector_name not in sparse_vectors_config:
        # 2026-06-11 08:23:49 修改：抛出明确异常。作用：避免 sparse 查询时运行期失败。
        raise RuntimeError(f"Qdrant hybrid collection 缺少 sparse 向量名：{config.sparse_vector_name}。")
    # 兼容单向量 collection 的 VectorParams 结构。
    if isinstance(vectors_config, models.VectorParams):
        # 读取当前向量维度。
        current_size = vectors_config.size
    # 兼容命名向量 collection 的字典结构。
    elif isinstance(vectors_config, dict):
        # 2026-06-11 08:23:49 修改：hybrid 模式读取指定 dense 维度。理由：不能误读其他命名向量。
        current_size = vectors_config[config.dense_vector_name].size if config.enable_hybrid else next(iter(vectors_config.values())).size
    # 其他结构直接报错。
    else:
        # 抛出明确异常。
        raise RuntimeError(f"无法识别 Qdrant collection 向量配置：{vectors_config}")
    # 如果维度不一致，必须让用户显式 --recreate。
    if current_size != embedding_config.dimension:
        # 抛出明确异常。
        raise RuntimeError(
            f"Qdrant collection 已存在但维度不一致：当前 {current_size}，期望 {embedding_config.dimension}。请加 --recreate 重建。"
        )
    # 已存在且维度正确时补齐 payload index。
    create_payload_indexes(client, config.collection_name, source_profile)


def create_payload_indexes(client: QdrantClient, collection_name: str, source_profile: Any | None = None) -> None:
    # 定义需要建索引的 payload 字段。
    indexes = {
        # chunk_id 用于回表。
        "chunk_id": models.PayloadSchemaType.KEYWORD,
        # document_id 用于按文档过滤。
        "document_id": models.PayloadSchemaType.KEYWORD,
        # 2026-06-10 18:01:50 修改：给 doc_id 建 KEYWORD index。理由：兼容 LlamaIndex DOCUMENT_ID_KEY。
        LLAMAINDEX_DOCUMENT_ID_PAYLOAD_KEY: models.PayloadSchemaType.KEYWORD,
        # scene 用于按业务场景过滤。
        "scene": models.PayloadSchemaType.KEYWORD,
        # 2026-06-10 18:01:50 修改：给 keyword_terms 建 KEYWORD index。作用：支持原生关键词过滤。
        "keyword_terms": models.PayloadSchemaType.KEYWORD,
        # 2026-06-10 18:01:50 修改：给 query_aliases 建 KEYWORD index。作用：保留别名问法过滤。
        "query_aliases": models.PayloadSchemaType.KEYWORD,
        # cluster_id 用于按文档内聚类过滤。
        "cluster_id": models.PayloadSchemaType.KEYWORD,
        # global_cluster_id 用于按全局聚类过滤。
        "global_cluster_id": models.PayloadSchemaType.KEYWORD,
        # fusion_status 用于只取 canonical。
        "fusion_status": models.PayloadSchemaType.KEYWORD,
        # qa_pair_validated 用于过滤已校验问答。
        "qa_pair_validated": models.PayloadSchemaType.BOOL,
        # question_hash 用于同问消歧。
        "question_hash": models.PayloadSchemaType.KEYWORD,
        # answer_hash 用于同答融合。
        "answer_hash": models.PayloadSchemaType.KEYWORD,
        # payload schema 版本用于兼容排查。
        "payload_schema_version": models.PayloadSchemaType.KEYWORD,
        # RAG 消费契约版本用于下游筛选。
        "rag_contract_version": models.PayloadSchemaType.KEYWORD,
        # qdrant_ready 用于同步后自检。
        "qdrant_ready": models.PayloadSchemaType.BOOL,
        # 2026-06-10 18:01:50 修改：给 text 建 TEXT index。理由：兼容外部 RAG loader 默认 text_key。
        "text": models.PayloadSchemaType.TEXT,
        # 2026-06-10 18:01:50 修改：给 retrieval_text 建 TEXT index。作用：支持全文过滤和调试。
        "retrieval_text": models.PayloadSchemaType.TEXT,
    }
    # 2026-06-12 14:40:11 修改：判断当前 profile 是否要求严格 payload；作用：索引字段也跟随严格模式隔离；理由：sql_External_database 不能继承 getai 专用 QA 索引。
    strict_payload_mode = getattr(source_profile, "payload_mode", "") == qdrant_mapping_profile.PAYLOAD_MODE_PROFILE_STRICT
    # 2026-06-12 15:30:17 修改：判断当前 profile 是否由 YAML 渲染 payload；作用：索引集合也完全跟随 qdrant_payload.indexes；理由：字段由 YAML 控制时索引不能继续自动补 doc_id/source_*。
    rendered_payload_mode = getattr(source_profile, "payload_mode", "") == qdrant_mapping_profile.PAYLOAD_MODE_PROFILE_RENDERED
    # 2026-06-12 15:30:17 修改：YAML 渲染模式重置索引集合；作用：只创建 qdrant_payload.indexes 明确声明的索引；理由：当前 sql_External_database 不应残留 getai 或 strict 固定索引。
    if rendered_payload_mode:
        # 2026-06-12 15:30:17 修改：读取 profile 上的 payload 布局；作用：找到 indexes 配置；理由：每个外部库索引策略都应独立配置。
        qdrant_payload_layout = getattr(source_profile, "qdrant_payload_layout", {}) or {}
        # 2026-06-12 15:30:17 修改：规范化布局类型；作用：防止错误配置触发类型异常；理由：索引创建应可防御坏 YAML。
        if not isinstance(qdrant_payload_layout, dict):
            # 2026-06-12 15:30:17 修改：非字典布局降为空；作用：避免无效索引创建；理由：后续 verify 会暴露配置缺失。
            qdrant_payload_layout = {}
        # 2026-06-12 15:30:17 修改：读取 indexes 小节；作用：区分 keyword/text 索引；理由：Qdrant 两种 schema 必须分别声明。
        rendered_index_layout = qdrant_payload_layout.get("indexes") if isinstance(qdrant_payload_layout.get("indexes"), dict) else {}
        # 2026-06-12 15:30:17 修改：重置索引字典；作用：禁止默认索引和 strict 索引自动进入外部库；理由：deny_extra_top_level 要求 collection 干净。
        indexes = {}
        # 2026-06-12 15:30:17 修改：遍历 YAML 声明的 keyword 索引；作用：未来外部库可按需声明 tenant_id/supplier_code 等过滤字段；理由：不改程序也能扩展索引。
        for field_name in rendered_index_layout.get("keyword") or []:
            # 2026-06-12 15:30:17 修改：规范化字段名；作用：过滤空白配置；理由：Qdrant 不接受空字段索引。
            normalized_field_name = normalize_text(field_name)
            # 2026-06-12 15:30:17 修改：非空才创建 KEYWORD 索引；作用：保持索引集合干净；理由：配置错误不应污染 collection。
            if normalized_field_name:
                # 2026-06-12 15:30:17 修改：写入 KEYWORD 索引；作用：按 YAML 创建过滤索引；理由：索引字段由 profile 决定。
                indexes.setdefault(normalized_field_name, models.PayloadSchemaType.KEYWORD)
        # 2026-06-12 15:30:17 修改：遍历 YAML 声明的 text 索引；作用：当前只给 retrieval_text 建全文索引；理由：截图要求其余无用字段不建索引。
        for field_name in rendered_index_layout.get("text") or []:
            # 2026-06-12 15:30:17 修改：规范化字段名；作用：过滤空白配置；理由：Qdrant TEXT index 字段名必须有效。
            normalized_field_name = normalize_text(field_name)
            # 2026-06-12 15:30:17 修改：非空才创建 TEXT 索引；作用：保持索引集合可控；理由：字段不存在时不应自动补别的索引。
            if normalized_field_name:
                # 2026-06-12 15:30:17 修改：写入 TEXT 索引；作用：按 YAML 创建全文索引；理由：当前 external_database 只声明 retrieval_text。
                indexes.setdefault(normalized_field_name, models.PayloadSchemaType.TEXT)
    # 2026-06-12 14:40:11 修改：严格模式重置基础索引集合；作用：只给最小契约字段建索引；理由：不能在外部库 collection 中出现 cluster_id/qa_pair_validated 等 getai 字段索引。
    if strict_payload_mode:
        # 2026-06-12 14:40:11 修改：定义严格模式基础索引；作用：覆盖 LlamaIndex 检索、来源回表和文本调试；理由：这些是外部库最小消费契约。
        indexes = {
            # 2026-06-12 14:40:11 修改：索引 doc_id；作用：兼容 LlamaIndex index_doc_id=True；理由：外部消费者默认会按 doc_id 过滤。
            LLAMAINDEX_DOCUMENT_ID_PAYLOAD_KEY: models.PayloadSchemaType.KEYWORD,
            # 2026-06-12 14:40:11 修改：索引来源名；作用：支持多外部库过滤；理由：严格模式仍要能追溯数据源。
            "source_name": models.PayloadSchemaType.KEYWORD,
            # 2026-06-12 14:40:11 修改：索引来源表；作用：支持回表定位过滤；理由：外部库可能按表分组消费。
            "source_table": models.PayloadSchemaType.KEYWORD,
            # 2026-06-12 14:40:11 修改：索引来源主键；作用：支持按 external_id 精确定位；理由：新增 id 不替代稳定业务主键。
            "source_pk": models.PayloadSchemaType.KEYWORD,
            # 2026-06-12 14:40:11 修改：索引 profile 名；作用：排查字段策略；理由：多个 profile 共存时需要可过滤。
            "mapping_profile_name": models.PayloadSchemaType.KEYWORD,
            # 2026-06-12 14:40:11 修改：索引关键词列表；作用：支持 Qdrant KEYWORD 过滤；理由：严格模式仍需要通用过滤入口。
            "keyword_terms": models.PayloadSchemaType.KEYWORD,
            # 2026-06-12 14:40:11 修改：索引 text；作用：支持正文全文调试；理由：外部 RAG 默认 text_key 仍可用。
            "text": models.PayloadSchemaType.TEXT,
            # 2026-06-12 14:40:11 修改：索引 retrieval_text；作用：支持向量文本全文调试；理由：验收 standard_question + id 时要可查。
            "retrieval_text": models.PayloadSchemaType.TEXT,
        }
    # 2026-06-11 15:54:56 修改：按 source profile 动态补 KEYWORD index；作用：外部库可为 standard_question/question_scene 等字段建原生索引；理由：别人用 LlamaIndex/Qdrant 过滤时不用硬编码 false 绕过。
    if source_profile is not None and not rendered_payload_mode:
        # 2026-06-11 15:54:56 修改：遍历 profile.keyword_index.fields；作用：把配置字段转成 Qdrant KEYWORD index；理由：每个外部库过滤字段不同。
        for field_name in getattr(source_profile, "keyword_index_fields", ()):
            # 2026-06-11 15:54:56 修改：跳过空字段名；作用：避免 Qdrant 创建无效索引；理由：profile 配置错误不能污染 collection。
            if field_name:
                # 2026-06-12 14:40:11 修改：严格模式把业务字段索引放到 payload.*；作用：支持过滤但不摊平业务字段；理由：外部库字段必须留在嵌套 payload 内。
                indexed_field_name = f"payload.{field_name}" if strict_payload_mode else field_name
                # 2026-06-11 15:54:56 修改：写入动态 KEYWORD index；作用：补齐外部库过滤字段；理由：WebUI 和外部 RAG 可直接使用这些字段。
                indexes.setdefault(indexed_field_name, models.PayloadSchemaType.KEYWORD)
        # 2026-06-11 15:54:56 修改：遍历 profile.text_index.fields；作用：把配置字段转成 Qdrant TEXT index；理由：全文过滤和排查字段也应配置化。
        for field_name in getattr(source_profile, "text_index_fields", ()):
            # 2026-06-11 15:54:56 修改：跳过空字段名；作用：避免无效索引；理由：保持索引创建稳健。
            if field_name:
                # 2026-06-12 14:40:11 修改：严格模式下顶层 text/retrieval_text 保持顶层，其他全文字段走 payload.*；作用：文本调试可用且业务字段不摊平；理由：保持外部库 payload 隔离。
                indexed_field_name = field_name if not strict_payload_mode or field_name in {"text", "retrieval_text"} else f"payload.{field_name}"
                # 2026-06-11 15:54:56 修改：写入动态 TEXT index；作用：支持 text/retrieval_text 或外部自定义全文字段；理由：不同数据源调试字段不同。
                indexes.setdefault(indexed_field_name, models.PayloadSchemaType.TEXT)
    # 遍历索引定义。
    for field_name, field_schema in indexes.items():
        # 创建 payload index。
        try:
            # 使用 Qdrant 官方 create_payload_index API。
            client.create_payload_index(
                # 指定 collection。
                collection_name=collection_name,
                # 指定字段名。
                field_name=field_name,
                # 指定字段类型。
                field_schema=field_schema,
            )
        # 索引已存在或版本差异时不阻断主流程。
        except Exception:
            # 继续下一个字段。
            continue


def validate_chunks_before_qdrant(chunks: list[CanonicalChunk]) -> dict[str, Any]:
    # 创建错误列表。
    errors: list[str] = []
    # 遍历 canonical chunks。
    for chunk in chunks:
        # 2026-06-11 15:54:56 修改：识别 generic profile chunk；作用：外部库可只要求 embedding_text/prompt_text/source_pk/payload 存在；理由：generic 外部库不应被 QA 答案必须进 retrieval_text 的旧规则误伤。
        if qdrant_mapping_profile.is_generic_profile_chunk(chunk):
            # 2026-06-11 15:54:56 修改：读取 generic 向量文本；作用：校验外部库召回字段是否存在；理由：没有 embedding_text 就不能入 Qdrant。
            generic_embedding_text = build_embedding_text(chunk)
            # 2026-06-11 15:54:56 修改：读取 generic prompt 文本；作用：校验模型正文是否存在；理由：只向量化问题时仍要有回答正文。
            generic_prompt_text = build_answer_first_text(chunk)
            # 2026-06-11 15:54:56 修改：读取来源主键；作用：校验外部库原始行可回溯；理由：外部库必须保留 source_pk。
            generic_source_pk = normalize_text(qdrant_mapping_profile.profile_payload_value(chunk, qdrant_mapping_profile.PROFILE_SOURCE_PK_KEY))
            # 2026-06-11 15:54:56 修改：读取嵌套 payload；作用：校验业务 metadata 是否被保留；理由：字段映射不能只留下 text。
            generic_source_payload = qdrant_mapping_profile.profile_payload_value(chunk, qdrant_mapping_profile.PROFILE_SOURCE_PAYLOAD_KEY, {})
            # 2026-06-11 15:54:56 修改：校验 chunk_id；作用：point id 必须稳定；理由：Qdrant upsert 依赖它。
            if not chunk.chunk_id:
                errors.append(f"{chunk.chunk_id}: missing chunk_id")
            # 2026-06-11 15:54:56 修改：校验 embedding_text；作用：阻断空向量文本；理由：外部库召回字段可能配置错。
            if not generic_embedding_text:
                errors.append(f"{chunk.chunk_id}: missing profile embedding_text")
            # 2026-06-11 15:54:56 修改：校验 prompt_text；作用：阻断空模型正文；理由：外部消费者至少要能拿到 text。
            if not generic_prompt_text:
                errors.append(f"{chunk.chunk_id}: missing profile prompt_text")
            # 2026-06-11 15:54:56 修改：校验 source_pk；作用：保证可回表；理由：外部库不是原清洗链路，必须自己有主键。
            if not generic_source_pk:
                errors.append(f"{chunk.chunk_id}: missing profile source_pk")
            # 2026-06-11 15:54:56 修改：校验 source_payload 类型；作用：保证 metadata 可写入 Qdrant；理由：外部字段要保留但不能破坏 payload。
            if not isinstance(generic_source_payload, dict):
                errors.append(f"{chunk.chunk_id}: profile source_payload must be object")
            # 2026-06-11 15:54:56 修改：校验同步标记；作用：保留原 qdrant_ready 阻断能力；理由：上游 profile 映射可显式拒绝入库。
            if not chunk.qdrant_ready:
                errors.append(f"{chunk.chunk_id}: qdrant_ready is false")
            # 2026-06-11 15:54:56 修改：generic 校验结束跳过 QA 严格答案规则；作用：允许 standard_question 单独向量化；理由：外部库不一定需要答案进入 retrieval_text。
            continue
        # 读取答案优先字段。
        answer = chunk.answer_text or chunk.answer
        # 构造 LLM 消费文本。
        llm_text = build_answer_first_text(chunk)
        # 构造检索文本。
        retrieval_text = build_embedding_text(chunk)
        # 读取完整来源摘录。
        source_excerpt_full = chunk.source_excerpt_full or chunk.source_excerpt or chunk.cleaned_text
        # 缺问题。
        if not chunk.question:
            errors.append(f"{chunk.chunk_id}: missing question")
        # 缺答案。
        if not answer:
            errors.append(f"{chunk.chunk_id}: missing answer_text")
        # payload 显式标记不可同步。
        if not chunk.qdrant_ready:
            errors.append(f"{chunk.chunk_id}: qdrant_ready is false")
        # LLM 消费文本漏答案。
        if answer and answer not in llm_text:
            errors.append(f"{chunk.chunk_id}: llm_text missing full answer")
        # 检索文本漏答案。
        if answer and answer not in retrieval_text:
            errors.append(f"{chunk.chunk_id}: retrieval_text missing full answer")
        # 完整摘录漏答案。
        if answer and answer not in source_excerpt_full:
            errors.append(f"{chunk.chunk_id}: source_excerpt_full missing full answer")
    # 有错误时阻断同步。
    if errors:
        preview = "\n".join(errors[:20])
        raise RuntimeError(f"Qdrant 同步前契约校验失败，共 {len(errors)} 个问题：\n{preview}")
    # 返回校验摘要。
    return {
        "checked_chunk_count": len(chunks),
        # 2026-06-11 15:54:56 修改：根据 chunk 类型返回契约版本；作用：摘要能区分 QA 主库和 generic 外部库；理由：测试和排查需要知道走了哪套校验。
        "contract_version": "mapping-profile-contract-v1" if any(qdrant_mapping_profile.is_generic_profile_chunk(chunk) for chunk in chunks) else "qa-rag-contract-v1",
        "error_count": 0,
    }


def get_llamaindex_sparse_doc_encoder(fastembed_sparse_model: str | None = None) -> Any:
    # 2026-06-12 09:52:34 修改：归一化 sparse 模型名；作用：空值兜底成 Qdrant/bm25；理由：外部消费者明确使用 fastembed_sparse_model="Qdrant/bm25"。
    selected_sparse_model = (fastembed_sparse_model or LLAMAINDEX_BM25_FASTEMBED_SPARSE_MODEL).strip() or LLAMAINDEX_BM25_FASTEMBED_SPARSE_MODEL
    # 2026-06-12 09:52:34 修改：按模型名检查缓存；作用：同一进程多个 profile 不互相污染；理由：未来其他外部库可能换 sparse 模型。
    if selected_sparse_model not in LLAMAINDEX_SPARSE_DOC_ENCODERS:
        # 2026-06-11 08:23:49 修改：懒加载 LlamaIndex 官方 Qdrant sparse encoder。理由：默认 dense 路径不增加依赖成本。
        from llama_index.vector_stores.qdrant.utils import fastembed_sparse_encoder
        # 2026-06-12 09:52:34 修改：按 profile/配置传入 model_name；作用：文档侧 sparse vector 使用 Qdrant/bm25；理由：和外部查询侧 fastembed_sparse_model 完全一致。
        LLAMAINDEX_SPARSE_DOC_ENCODERS[selected_sparse_model] = fastembed_sparse_encoder(model_name=selected_sparse_model)
    # 2026-06-12 09:52:34 修改：返回指定模型的缓存 encoder；作用：供 point 构造批量生成 sparse vector；理由：避免每批重复初始化模型。
    return LLAMAINDEX_SPARSE_DOC_ENCODERS[selected_sparse_model]


def build_llamaindex_sparse_vectors(texts: list[str], fastembed_sparse_model: str = LLAMAINDEX_BM25_FASTEMBED_SPARSE_MODEL) -> list[models.SparseVector]:
    # 2026-06-12 09:52:34 修改：按配置获取 LlamaIndex sparse doc encoder；作用：让 BM25 文档侧与查询侧同源；理由：hybrid collection 不能只建名不建同模型 sparse。
    sparse_doc_encoder = get_llamaindex_sparse_doc_encoder(fastembed_sparse_model)
    # 2026-06-11 08:23:49 修改：调用 encoder 生成 indices/values。作用：形成 Qdrant SparseVector 所需结构。
    sparse_indices, sparse_values = sparse_doc_encoder(texts)
    # 2026-06-11 08:23:49 修改：校验 sparse 数量。理由：防止 sparse 和 dense 批次错位。
    if len(sparse_indices) != len(texts) or len(sparse_values) != len(texts):
        # 2026-06-11 08:23:49 修改：抛出明确异常。作用：阻断错误 point 写入。
        raise RuntimeError(f"LlamaIndex sparse vector 返回数量不一致：请求 {len(texts)} 条，indices {len(sparse_indices)} 条，values {len(sparse_values)} 条。")
    # 2026-06-11 08:23:49 修改：组装 Qdrant SparseVector 列表。作用：直接写入 PointStruct 命名 sparse vector。
    return [
        # 2026-06-11 08:23:49 修改：创建 SparseVector。理由：Qdrant hybrid sparse 向量要求 indices + values。
        models.SparseVector(indices=indices, values=values)
        # 2026-06-11 08:23:49 修改：逐条合并 indices/values。作用：保持文档顺序不变。
        for indices, values in zip(sparse_indices, sparse_values, strict=True)
    ]


def build_qdrant_point_vector(embedding: list[float], sparse_vector: models.SparseVector | None, config: QdrantSyncConfig | None) -> Any:
    # 2026-06-11 08:23:49 修改：默认或未传 config 时返回旧 dense list。理由：保护现有 agent collection。
    if config is None or not config.enable_hybrid:
        # 2026-06-11 08:23:49 修改：返回原始 embedding。作用：保持未命名 dense 写入结构。
        return embedding
    # 2026-06-11 08:23:49 修改：hybrid 模式必须有 sparse vector。理由：外部 LlamaIndex sparse 查询不能缺向量。
    if sparse_vector is None:
        # 2026-06-11 08:23:49 修改：抛出明确异常。作用：避免写入半个 hybrid point。
        raise RuntimeError("启用 hybrid 写入时缺少 sparse vector。")
    # 2026-06-11 08:23:49 修改：返回命名 dense+sparse 向量字典。理由：匹配 LlamaIndex QdrantVectorStore hybrid point 结构。
    return {
        # 2026-06-11 08:23:49 修改：写入命名 dense 向量。作用：支持 using=text-dense 查询。
        config.dense_vector_name: embedding,
        # 2026-06-11 08:23:49 修改：写入命名 sparse 向量。作用：支持 using=text-sparse-new 查询。
        config.sparse_vector_name: sparse_vector,
    }


def build_qdrant_points(
    chunks: list[CanonicalChunk],
    embeddings: list[list[float]],
    embedding_config: EmbeddingConfig,
    qdrant_config: QdrantSyncConfig | None = None,
    sparse_vectors: list[models.SparseVector] | None = None,
) -> list[models.PointStruct]:
    # 2026-06-11 08:23:49 修改：如果启用 hybrid 且调用方未传 sparse_vectors，就用 LlamaIndex 官方 encoder 生成。理由：保持外部 hybrid RAG 兼容。
    if qdrant_config is not None and qdrant_config.enable_hybrid and sparse_vectors is None:
        # 2026-06-11 08:23:49 修改：构造 sparse 文本列表。作用：与 dense embedding 使用同一检索文本。
        sparse_texts = [build_embedding_text(chunk) for chunk in chunks]
        # 2026-06-11 08:23:49 修改：生成 sparse vectors。理由：Qdrant hybrid point 必须同时写 dense+sparse。
        # 2026-06-12 09:52:34 修改：把 Qdrant/bm25 模型名传给 sparse builder；作用：保证 text-sparse-new 的数值来自 BM25 encoder；理由：对齐外部 QdrantVectorStore fastembed_sparse_model 参数。
        sparse_vectors = build_llamaindex_sparse_vectors(sparse_texts, qdrant_config.fastembed_sparse_model)
    # 2026-06-11 08:23:49 修改：hybrid 模式校验 sparse 数量。理由：防止 point 和 sparse vector 错位。
    if qdrant_config is not None and qdrant_config.enable_hybrid and (sparse_vectors is None or len(sparse_vectors) != len(chunks)):
        # 2026-06-11 08:23:49 修改：抛出明确异常。作用：阻断错误写入。
        raise RuntimeError("启用 hybrid 写入时 sparse vector 数量必须和 chunk 数量一致。")
    # 创建 point 列表。
    points: list[models.PointStruct] = []
    # 同时遍历 chunk 和 embedding。
    for item_index, (chunk, embedding) in enumerate(zip(chunks, embeddings, strict=True)):
        # 2026-06-11 08:23:49 修改：读取当前 sparse vector。理由：默认 dense 路径保持 None，hybrid 路径按序写入。
        sparse_vector = sparse_vectors[item_index] if sparse_vectors is not None else None
        # 构造官方 PointStruct。
        points.append(
            models.PointStruct(
                # 设置稳定 UUID point id。
                id=build_qdrant_point_id(chunk.chunk_id),
                # 设置向量。
                vector=build_qdrant_point_vector(embedding, sparse_vector, qdrant_config),
                # 设置 payload。
                payload=build_qdrant_payload(chunk, embedding_config),
            )
        )
    # 返回 point 列表。
    return points


def upsert_points_to_qdrant(client: QdrantClient, config: QdrantSyncConfig, points: list[models.PointStruct]) -> None:
    # 如果 dry-run，跳过实际写入。
    if config.dry_run:
        # 直接返回。
        return
    # 按批次写入 Qdrant。
    for point_batch in chunk_list(points, config.upsert_batch_size):
        # 使用 Qdrant 官方 upsert API 写入 points。
        client.upsert(
            # 指定 collection。
            collection_name=config.collection_name,
            # 指定 point 批次。
            points=point_batch,
            # 等待写入完成，便于后续立即测试。
            wait=True,
        )


# 2026-06-13 17:18:04 新增：删除 Qdrant points；作用：外部 PG/SQL Server 源行软删或硬删后同步清理向量点；理由：实时同步不能只有 upsert。
def delete_points_from_qdrant(client: QdrantClient, config: QdrantSyncConfig, point_ids: list[str]) -> None:
    # 2026-06-13 17:18:04 新增：dry-run 时跳过真实删除；作用：调试链路不破坏 collection；理由：和 upsert dry-run 语义一致。
    if config.dry_run:
        # 2026-06-13 17:18:04 新增：直接返回；作用：不调用 Qdrant；理由：dry-run 不能改外部状态。
        return
    # 2026-06-13 17:18:04 新增：过滤空 point id；作用：避免 Qdrant SDK 因空值报错；理由：状态表可能有历史残缺。
    cleaned_point_ids = [point_id for point_id in point_ids if point_id]
    # 2026-06-13 17:18:04 新增：没有可删 id 时返回；作用：减少无效请求；理由：删除操作也要幂等。
    if not cleaned_point_ids:
        # 2026-06-13 17:18:04 新增：直接返回；作用：保持删除函数安全；理由：空列表不是错误。
        return
    # 2026-06-13 17:18:04 新增：按批次删除；作用：兼容大量外部删除；理由：避免一次请求过大。
    for point_id_batch in chunk_list(cleaned_point_ids, config.upsert_batch_size):
        # 2026-06-13 17:18:04 新增：调用 Qdrant 官方 delete API；作用：删除指定 point；理由：源库删除后向量库必须同步删除。
        client.delete(
            # 2026-06-13 17:18:04 新增：指定 collection；作用：只删除当前外部库 collection；理由：隔离保护主 QA collection。
            collection_name=config.collection_name,
            # 2026-06-13 17:18:04 新增：按 point id 删除；作用：精确清理 stale point；理由：point id 由 chunk_id 稳定生成。
            points_selector=models.PointIdsList(points=point_id_batch),
            # 2026-06-13 17:18:04 新增：等待删除完成；作用：后续测试/状态可立即观察；理由：同步结果要确定。
            wait=True,
        )


def build_document_chunk_counts(chunks: list[CanonicalChunk]) -> dict[str, int]:
    # 创建文档计数字典。
    counts: dict[str, int] = {}
    # 遍历所有 canonical chunk。
    for chunk in chunks:
        # 按 document_id 累计。
        counts[chunk.document_id] = counts.get(chunk.document_id, 0) + 1
    # 返回计数字典。
    return counts


def build_document_hashes(chunks: list[CanonicalChunk]) -> dict[str, str]:
    # 创建文档 hash 字典。
    hashes: dict[str, str] = {}
    # 遍历所有 canonical chunk。
    for chunk in chunks:
        # 首次出现该文档时记录内容 hash。
        hashes.setdefault(chunk.document_id, chunk.content_hash)
    # 返回 hash 字典。
    return hashes


def sync_state_id(document_id: str, collection_name: str) -> str:
    # 用 document_id 和 collection_name 生成稳定 hash。
    digest = hashlib.sha256(f"{document_id}|{collection_name}".encode("utf-8")).hexdigest()[:24]
    # 返回符合现有 NVARCHAR(80) 的同步 ID。
    return f"qdrantsync_{digest}"


def update_sqlserver_sync_state(
    sql_config: SqlServerConfig,
    qdrant_config: QdrantSyncConfig,
    embedding_config: EmbeddingConfig,
    chunks: list[CanonicalChunk],
    point_count: int,
) -> None:
    # dry-run 时不更新 SQL Server。
    if qdrant_config.dry_run:
        # 直接返回。
        return
    # 统计每个文档同步了多少 canonical chunk。
    chunk_counts = build_document_chunk_counts(chunks)
    # 读取每个文档的内容 hash。
    document_hashes = build_document_hashes(chunks)
    # 构造同步消息。
    sync_message = json.dumps(
        {
            # 写入 Qdrant URL。
            "qdrant_url": qdrant_config.url,
            # 写入 collection 名称。
            "collection": qdrant_config.collection_name,
            # 写入 embedding 模型。
            "embedding_model": embedding_config.model,
            # 写入 embedding 维度。
            "embedding_dimension": embedding_config.dimension,
            # 写入同步 point 数量。
            "point_count": point_count,
            # 写入同步时间。
            "synced_at": datetime.now(timezone.utc).isoformat(),
            # 2026-06-11 08:23:49 修改：写入 hybrid 开关。理由：后续排查 collection 结构来源。
            "enable_hybrid": qdrant_config.enable_hybrid,
            # 2026-06-11 08:23:49 修改：写入 dense 向量名。作用：记录 LlamaIndex 消费契约。
            "dense_vector_name": qdrant_config.dense_vector_name,
            # 2026-06-11 08:23:49 修改：写入 sparse 向量名。作用：记录 LlamaIndex 消费契约。
            "sparse_vector_name": qdrant_config.sparse_vector_name,
        },
        ensure_ascii=False,
    )
    # 打开 SQL Server 连接。
    with pyodbc.connect(sqlserver_connection_string(sql_config), autocommit=True) as connection:
        # 创建 cursor。
        cursor = connection.cursor()
        # 遍历每个文档的同步状态。
        for document_id, chunk_count in chunk_counts.items():
            # 执行 MERGE 更新同步状态。
            cursor.execute(
                """
MERGE dbo.rag_rag_sync_state AS target
USING (
    SELECT
        ? AS sync_id,
        ? AS document_id,
        ? AS content_hash,
        ? AS sync_target,
        ? AS sync_status,
        ? AS chunk_count,
        ? AS needs_reindex,
        ? AS sync_message
) AS source
ON target.sync_id = source.sync_id
WHEN MATCHED THEN
    UPDATE SET
        content_hash = source.content_hash,
        sync_target = source.sync_target,
        sync_status = source.sync_status,
        chunk_count = source.chunk_count,
        needs_reindex = source.needs_reindex,
        sync_message = source.sync_message,
        updated_at = SYSUTCDATETIME()
WHEN NOT MATCHED THEN
    INSERT (sync_id, document_id, content_hash, sync_target, sync_status, chunk_count, needs_reindex, sync_message)
    VALUES (source.sync_id, source.document_id, source.content_hash, source.sync_target, source.sync_status, source.chunk_count, source.needs_reindex, source.sync_message);
""",
                # 设置同步状态主键。
                sync_state_id(document_id, qdrant_config.collection_name),
                # 设置文档 ID。
                document_id,
                # 设置内容 hash。
                document_hashes.get(document_id, ""),
                # 设置同步目标。
                f"qdrant:{qdrant_config.collection_name}",
                # 设置同步状态。
                "synced",
                # 设置 chunk 数。
                chunk_count,
                # 设置 needs_reindex。
                0,
                # 设置同步消息。
                sync_message,
            )


def verify_qdrant_collection(client: QdrantClient, config: QdrantSyncConfig, first_vector: list[float]) -> dict[str, Any]:
    # dry-run 时返回空校验结果。
    if config.dry_run:
        # 返回 dry-run 结果。
        return {"dry_run": True}
    # 调用 Qdrant 官方 count API 统计 collection point 数。
    count_result = client.count(collection_name=config.collection_name, exact=True)
    # 调用 Qdrant 官方 query_points API 验证向量可检索。
    # 2026-06-11 08:23:49 修改：构造自检查询参数。理由：hybrid collection 需要指定 using=text-dense。
    query_kwargs: dict[str, Any] = {
        # 指定 collection。
        "collection_name": config.collection_name,
        # 使用第一条向量做自检查询。
        "query": first_vector,
        # 只取前三条。
        "limit": 3,
        # 返回 payload 给后续排查。
        "with_payload": True,
        # 不返回向量，减少输出。
        "with_vectors": False,
    }
    # 2026-06-11 08:23:49 修改：hybrid 自检指定 dense 向量名。理由：命名向量 collection 不能按旧未命名方式查询。
    if config.enable_hybrid:
        # 2026-06-11 08:23:49 修改：设置 using 参数。作用：用 text-dense 做 dense 自检。
        query_kwargs["using"] = config.dense_vector_name
    # 调用 Qdrant 官方 query_points API 验证向量可检索。
    query_result = client.query_points(**query_kwargs)
    # 读取第一条命中 payload。
    first_payload = query_result.points[0].payload if query_result.points else {}
    # 2026-06-12 14:40:11 修改：读取严格模式嵌套 payload；作用：profile_strict 不再把 answer/question 摊平到顶层；理由：自检不能沿用旧 QA 顶层字段判断。
    first_nested_payload = first_payload.get("payload") if first_payload else {}
    # 2026-06-12 14:40:11 修改：规范嵌套 payload 类型；作用：避免非 dict 破坏后续读取；理由：Qdrant payload 来自外部服务时类型要防御。
    first_source_payload = first_nested_payload if isinstance(first_nested_payload, dict) else {}
    # 读取答案和默认 text。
    first_answer = str(first_payload.get("answer_text") or first_payload.get("answer") or first_source_payload.get("answer") or "") if first_payload else ""
    first_text = str(first_payload.get("text") or "") if first_payload else ""
    # 2026-06-12 14:40:11 修改：读取 strict payload 的向量文本；作用：验证 standard_question + id 是否作为 retrieval_text 写入；理由：外部库验收要看到真实向量文本。
    first_retrieval_text = str(first_payload.get("retrieval_text") or "") if first_payload else ""
    # 2026-06-12 15:30:17 修改：初始化 YAML 渲染 payload ready 标记；作用：让自检可按 profile_rendered 验收；理由：外部库字段布局不能再按固定 strict 字段判断。
    rendered_payload_ready = False
    # 2026-06-12 15:30:17 修改：初始化 YAML 渲染契约版本；作用：执行摘要能说明当前按通用渲染器验收；理由：多外部库排查需要看到模式。
    rendered_payload_contract_version = ""
    # 2026-06-12 15:30:17 修改：仅当配置声明 source_profile 时加载 profile；作用：读取 qdrant_payload 布局；理由：主链路没有 profile_rendered 时不能多做假设。
    if getattr(config, "source_profile", ""):
        # 2026-06-12 15:30:17 修改：加载当前 profile；作用：自检规则和写入配置保持一致；理由：验收必须证明“一库一配置、一库一结构”。
        verify_source_profile = qdrant_mapping_profile.load_source_profile(config.source_profile)
        # 2026-06-12 15:30:17 修改：判断是否为 YAML 渲染模式；作用：只让 profile_rendered 走布局验收；理由：legacy_qa 和 profile_strict 仍保持原逻辑。
        if getattr(verify_source_profile, "payload_mode", "") == qdrant_mapping_profile.PAYLOAD_MODE_PROFILE_RENDERED:
            # 2026-06-12 15:30:17 修改：读取 payload 布局；作用：检查 YAML 声明字段；理由：不能再固定要求 doc_id/source_pk/text。
            verify_layout = getattr(verify_source_profile, "qdrant_payload_layout", {}) or {}
            # 2026-06-12 15:30:17 修改：规范化布局类型；作用：避免坏配置触发类型异常；理由：自检应返回 not ready 而不是崩溃。
            if not isinstance(verify_layout, dict):
                # 2026-06-12 15:30:17 修改：非字典布局按空布局处理；作用：让后续 required 字段为空；理由：配置错误会导致 ready false。
                verify_layout = {}
            # 2026-06-12 15:30:17 修改：读取顶层字段声明；作用：得到必须存在的顶层字段集合；理由：top_level 是 profile_rendered 的唯一顶层字段来源。
            verify_top_level_entries = verify_layout.get("top_level") if isinstance(verify_layout.get("top_level"), list) else []
            # 2026-06-12 15:30:17 修改：解析顶层字段名；作用：验收每个 YAML 声明字段是否写入；理由：遗漏字段说明写入器没有按配置执行。
            required_top_level_keys = {
                # 2026-06-12 15:30:17 修改：从条目解析输出 key；作用：支持字符串和 {key, from} 两种写法；理由：验收逻辑必须和渲染器一致。
                qdrant_mapping_profile.parse_qdrant_payload_layout_field_entry(entry, "")[0]
                # 2026-06-12 15:30:17 修改：遍历 top_level 声明；作用：收集所有顶层字段；理由：字段数量由 YAML 决定。
                for entry in verify_top_level_entries
                # 2026-06-12 15:30:17 修改：跳过空字段名；作用：避免错误配置生成空 key；理由：保持集合有效。
                if qdrant_mapping_profile.parse_qdrant_payload_layout_field_entry(entry, "")[0]
            }
            # 2026-06-12 15:30:17 修改：读取对象布局声明；作用：得到必须存在的嵌套对象；理由：payload 对象也由 YAML 决定。
            verify_object_layouts = verify_layout.get("objects") if isinstance(verify_layout.get("objects"), dict) else {}
            # 2026-06-12 15:30:17 修改：解析对象名集合；作用：验收 payload 等嵌套对象是否写入；理由：对象字段不能自动摊平成顶层。
            required_object_keys = {normalize_text(object_name) for object_name in verify_object_layouts if normalize_text(object_name)}
            # 2026-06-12 15:30:17 修改：合并允许的顶层字段；作用：配合 deny_extra_top_level 检查多余字段；理由：当前外部库不允许 doc_id/text/source_* 混入。
            allowed_top_level_keys = required_top_level_keys | required_object_keys
            # 2026-06-12 15:30:17 修改：检查顶层字段都存在；作用：证明 top_level 渲染完成；理由：向量文本等字段是外部消费入口。
            top_level_keys_ready = bool(first_payload) and all(key in first_payload for key in required_top_level_keys)
            # 2026-06-12 15:30:17 修改：检查对象字段都存在；作用：证明 objects.payload.include 渲染完成；理由：业务字段必须打包保存。
            object_keys_ready = bool(first_payload) and all(isinstance(first_payload.get(object_name), dict) for object_name in required_object_keys)
            # 2026-06-12 15:30:17 修改：初始化对象字段明细 ready；作用：逐项检查 include 字段；理由：对象存在但字段缺失也不能算完成。
            object_include_fields_ready = True
            # 2026-06-12 15:30:17 修改：遍历每个对象布局；作用：检查 payload 内必须包含 YAML include 字段；理由：验收规则跟随 profile。
            for object_name, object_config in verify_object_layouts.items():
                # 2026-06-12 15:30:17 修改：规范化对象名；作用：读取 Qdrant payload 中的对象；理由：对象名可能来自 YAML。
                normalized_object_name = normalize_text(object_name)
                # 2026-06-12 15:30:17 修改：读取对象 payload；作用：检查 include 字段；理由：当前 sql_External_database 要校验 payload.id 等字段。
                rendered_object = first_payload.get(normalized_object_name) if first_payload else {}
                # 2026-06-12 15:30:17 修改：读取 include 列表；作用：兼容 objects.payload.include；理由：字段声明在 YAML 内。
                include_entries = object_config.get("include") if isinstance(object_config, dict) else object_config
                # 2026-06-12 15:30:17 修改：规范化 include 列表；作用：避免非列表配置导致异常；理由：错误配置应让 ready false。
                include_entries = include_entries if isinstance(include_entries, list) else []
                # 2026-06-12 15:30:17 修改：解析对象必需字段；作用：支持字符串和 {key, from}；理由：验收逻辑和渲染器保持一致。
                required_object_fields = {
                    # 2026-06-12 15:30:17 修改：解析输出字段名；作用：检查最终对象字段；理由：字段可重命名。
                    qdrant_mapping_profile.parse_qdrant_payload_layout_field_entry(entry, "payload.")[0]
                    # 2026-06-12 15:30:17 修改：遍历 include 声明；作用：得到所有对象字段；理由：payload 内容由 YAML 决定。
                    for entry in include_entries
                    # 2026-06-12 15:30:17 修改：过滤空字段名；作用：避免无意义字段影响验收；理由：防御错误配置。
                    if qdrant_mapping_profile.parse_qdrant_payload_layout_field_entry(entry, "payload.")[0]
                }
                # 2026-06-12 15:30:17 修改：检查对象字段是否全部存在；作用：确保 payload 打包完整；理由：不能只写对象壳不写字段。
                object_include_fields_ready = object_include_fields_ready and isinstance(rendered_object, dict) and all(field in rendered_object for field in required_object_fields)
            # 2026-06-12 15:30:17 修改：读取禁止多余顶层字段开关；作用：严格校验截图要求；理由：当前 sql_External_database 不允许未声明顶层字段。
            deny_extra_top_level = bool(verify_layout.get("deny_extra_top_level"))
            # 2026-06-12 15:30:17 修改：检查是否没有多余顶层字段；作用：拦截 doc_id/text/source_* 等污染；理由：字段隔离必须由测试证明。
            no_extra_top_level_keys = (not deny_extra_top_level) or (bool(first_payload) and set(first_payload).issubset(allowed_top_level_keys))
            # 2026-06-12 15:30:17 修改：合并 YAML 渲染 ready 条件；作用：自检完全按 profile 布局判断；理由：不再依赖固定 strict 契约。
            rendered_payload_ready = bool(top_level_keys_ready and object_keys_ready and object_include_fields_ready and no_extra_top_level_keys)
            # 2026-06-12 15:30:17 修改：记录契约版本；作用：成功摘要可见 profile_rendered；理由：排查时知道走了通用 YAML 渲染器。
            rendered_payload_contract_version = qdrant_mapping_profile.PAYLOAD_MODE_PROFILE_RENDERED if rendered_payload_ready else ""
    # 2026-06-12 14:40:11 修改：判断是否为严格 profile payload；作用：自检分流 legacy QA 和外部库最小契约；理由：strict payload 没有 chunk_id/qdrant_ready 顶层字段。
    strict_payload_ready = bool(
        first_payload
        and first_payload.get(LLAMAINDEX_DOCUMENT_ID_PAYLOAD_KEY)
        and first_payload.get("source_name")
        and first_payload.get("source_table")
        and first_payload.get("source_pk")
        and isinstance(first_source_payload, dict)
        and first_source_payload
        and isinstance(first_payload.get("keyword_terms"), list)
        and first_text
        and first_retrieval_text
        and (not first_answer or first_answer in first_text)
    )
    # 2026-06-12 14:40:11 修改：判断 legacy QA payload 是否 ready；作用：保持原 getai 自检语义；理由：主 agent collection 仍要完整答案在 text 中。
    legacy_payload_ready = bool(first_payload and first_answer and first_answer in first_text and first_payload.get("qdrant_ready", True))
    # 2026-06-12 14:40:11 修改：合并 ready 判断；作用：让严格外部库和旧 QA 库都能被正确验收；理由：两种 payload 形态都由同一 verify 函数处理。
    contract_ready = rendered_payload_ready or strict_payload_ready or legacy_payload_ready
    # 返回校验摘要。
    return {
        # 返回 point 总数。
        "point_count": count_result.count,
        # 返回命中数量。
        "query_hit_count": len(query_result.points),
        # 返回第一条命中的 chunk_id。
        "first_hit_chunk_id": first_payload.get("chunk_id") if first_payload else "",
        # 返回第一条命中的问题。
        "first_hit_question": first_payload.get("question") or first_source_payload.get("question") if first_payload else "",
        # 2026-06-12 14:40:11 修改：返回第一条命中的来源主键；作用：strict payload 没有 chunk_id 时仍能验收回表定位；理由：source_pk 是外部库稳定身份。
        "first_hit_source_pk": first_payload.get("source_pk") or "" if first_payload else "",
        # 2026-06-12 14:40:11 修改：返回第一条命中的检索文本；作用：直接展示 standard_question + id；理由：用户要求验证向量化字段。
        "first_hit_retrieval_text": first_retrieval_text,
        # 返回第一条命中是否满足 RAG 消费契约。
        "first_hit_contract_ready": contract_ready,
        # 返回第一条命中的契约版本。
        "first_hit_contract_version": rendered_payload_contract_version or (qdrant_mapping_profile.PAYLOAD_MODE_PROFILE_STRICT if strict_payload_ready else first_payload.get("rag_contract_version", "") if first_payload else ""),
    }


def sync_sqlserver_to_qdrant(sql_config: SqlServerConfig, embedding_config: EmbeddingConfig, qdrant_config: QdrantSyncConfig) -> dict[str, Any]:
    # 2026-06-11 15:54:56 修改：按数据库名和命令行参数加载 source profile；作用：getai 默认用 getai_rag_qa_chunks，External_database 可用 external_database；理由：字段映射不能写死也不能另起链路。
    source_profile = qdrant_mapping_profile.load_source_profile(qdrant_config.source_profile, sql_config.database)
    # 2026-06-12 09:52:34 修改：把 source profile 应用到 Qdrant 配置；作用：自动切换 collection、hybrid、向量名和 BM25 sparse 模型；理由：不能再靠人工记 --enable-hybrid。
    qdrant_config = apply_source_profile_to_qdrant_config(qdrant_config, source_profile)
    # 从 SQL Server 读取 canonical chunks。
    chunks = load_canonical_chunks_from_sqlserver(sql_config)
    # 没有可同步数据时直接报错。
    if not chunks:
        # 抛出明确异常。
        raise RuntimeError("SQL Server 中没有可同步到 Qdrant 的 canonical QA chunk。")
    # 2026-06-11 15:54:56 修改：在原 validate/embed/build/upsert 前应用 profile；作用：把不同数据源解释成统一 Qdrant 最小消费契约；理由：主链路顺序不变，只新增字段解释层。
    chunks = qdrant_mapping_profile.apply_profile_to_chunks(chunks, source_profile)
    # 同步前执行 RAG 消费契约校验，阻断缺字段或漏答案的 point。
    contract_validation = validate_chunks_before_qdrant(chunks)
    # 创建 Qdrant 官方客户端。
    # 2026-06-06 11:30:19 修改原因：禁用系统代理环境，避免 Windows no_proxy 里的 IPv6 CIDR 破坏本地 Qdrant 同步。
    qdrant_client = QdrantClient(url=qdrant_config.url, trust_env=False)
    # 确保 Qdrant collection 存在且维度正确。
    ensure_qdrant_collection(qdrant_client, qdrant_config, embedding_config)
    # 创建 OpenAI-compatible embedding 客户端。
    embedding_client = create_embedding_client(embedding_config)
    # 创建全部 point 列表。
    all_points: list[models.PointStruct] = []
    # 遍历 chunk 批次。
    for chunk_batch in chunk_list(chunks, embedding_config.batch_size):
        # 构造当前批次的向量化文本。
        texts = [build_embedding_text(chunk) for chunk in chunk_batch]
        # 生成当前批次 embedding。
        embeddings = embed_texts(embedding_client, texts, embedding_config)
        # 构造当前批次 Qdrant points。
        point_batch = build_qdrant_points(chunk_batch, embeddings, embedding_config, qdrant_config)
        # 追加到全部 point 列表。
        all_points.extend(point_batch)
        # 写入当前批次到 Qdrant。
        upsert_points_to_qdrant(qdrant_client, qdrant_config, point_batch)
    # 更新 SQL Server 同步状态。
    update_sqlserver_sync_state(sql_config, qdrant_config, embedding_config, chunks, len(all_points))
    # 执行 Qdrant 检索校验。
    # 2026-06-11 08:23:49 修改：取出用于自检的 dense vector。理由：hybrid point 的 vector 是命名字典。
    first_verify_vector = all_points[0].vector[qdrant_config.dense_vector_name] if qdrant_config.enable_hybrid else all_points[0].vector
    # 执行 Qdrant 检索校验。
    verify_result = verify_qdrant_collection(qdrant_client, qdrant_config, first_verify_vector)  # type: ignore[arg-type]
    # 返回同步摘要。
    return {
        # 返回 collection 名称。
        "collection": qdrant_config.collection_name,
        # 返回 Qdrant URL。
        "qdrant_url": qdrant_config.url,
        # 返回读取 chunk 数。
        "source_chunk_count": len(chunks),
        # 返回写入 point 数。
        "upserted_point_count": len(all_points),
        # 返回同步前契约校验摘要。
        "contract_validation": contract_validation,
        # 2026-06-11 15:54:56 修改：返回 source profile 名称；作用：执行摘要可证明使用了哪份字段策略；理由：多数据源同步后必须可审计。
        "source_profile": source_profile.profile_name,
        # 2026-06-12 09:52:34 修改：返回是否启用 hybrid；作用：执行摘要可证明是否生成 text-dense/text-sparse-new；理由：排查外部 LlamaIndex 全量参数报错需要直接看见。
        "enable_hybrid": qdrant_config.enable_hybrid,
        # 2026-06-12 09:52:34 修改：返回 dense 向量名；作用：执行摘要可审计 collection schema；理由：外部默认 dense_vector_name 必须对齐 text-dense。
        "dense_vector_name": qdrant_config.dense_vector_name,
        # 2026-06-12 09:52:34 修改：返回 sparse 向量名；作用：执行摘要可审计 collection schema；理由：外部默认 sparse_vector_name 必须对齐 text-sparse-new。
        "sparse_vector_name": qdrant_config.sparse_vector_name,
        # 2026-06-12 09:52:34 修改：返回 sparse 模型名；作用：执行摘要可审计 BM25 文档侧模型；理由：要和 fastembed_sparse_model="Qdrant/bm25" 一致。
        "fastembed_sparse_model": qdrant_config.fastembed_sparse_model,
        # 返回 embedding 模型。
        "embedding_model": embedding_config.model,
        # 返回 embedding 维度。
        "embedding_dimension": embedding_config.dimension,
        # 返回是否 dry-run。
        "dry_run": qdrant_config.dry_run,
        # 返回校验结果。
        "verify": verify_result,
    }


def main() -> None:
    # 加载项目 .env。
    load_project_env()
    # 解析命令行参数。
    args = parse_args()
    # 构造 SQL Server 配置。
    sql_config = build_sqlserver_config(args)
    # 构造 embedding 配置。
    embedding_config = build_embedding_config(args)
    # 构造 Qdrant 配置。
    qdrant_config = build_qdrant_config(args)
    # 执行 SQL Server 到 Qdrant 的同步。
    summary = sync_sqlserver_to_qdrant(sql_config, embedding_config, qdrant_config)
    # 输出同步摘要 JSON，便于命令行和 CI 读取。
    print(json.dumps(summary, ensure_ascii=False, indent=2))


# 作为脚本运行时进入 main。
if __name__ == "__main__":
    # 调用 main。
    main()
