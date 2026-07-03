# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
import os
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
from llama_index.vector_stores.qdrant.utils import fastembed_sparse_encoder
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
os.environ["HF_HUB_ENDPOINT"] = "https://hf-mirror.com"
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
from typing import Any, Iterable
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
from app.config import Config
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
from llama_index.core import Document, Settings, StorageContext, VectorStoreIndex
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
from llama_index.embeddings.openai_like import OpenAILikeEmbedding
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
from llama_index.vector_stores.qdrant import QdrantVectorStore
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
from qdrant_client import QdrantClient
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
config = Config()
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
QDRANT_URL = "http://yulith:6333/"
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
DEFAULT_COLLECTION_NAME = "vlmcopy_default"
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
SPARSE_MODEL = "Qdrant/bm25"
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
BM25_MODEL_DIR = "D:/huangjing/Llamalndex/models"
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 configure_embedding
def configure_embedding() -> None:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 configure_embedding
    '\n    只配置 embedding，不配置 LLM。\n    当前文件只负责构建索引，不负责问答。\n    '
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 configure_embedding
    Settings.embed_model = OpenAILikeEmbedding(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 configure_embedding
        model_name=config.EMBEDDING_MODEL,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 configure_embedding
        api_base=config.embedding_service_url,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 configure_embedding
        api_key=config.embedding_service_api_key,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 configure_embedding
        dimensions=1024,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 configure_embedding
        truncate_dim=1024,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 configure_embedding
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 build_qdrant_vector_store
def build_qdrant_vector_store(
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_qdrant_vector_store
    collection_name: str = DEFAULT_COLLECTION_NAME,
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 build_qdrant_vector_store
) -> QdrantVectorStore:
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_qdrant_vector_store
    '\n    构建 Qdrant 混合向量库。\n    enable_hybrid=True 表示同时写入 dense 向量和 sparse 向量。\n    fastembed_sparse_model="Qdrant/bm25" 表示 sparse 部分使用 BM25。\n    '
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_qdrant_vector_store
    client = QdrantClient(url=QDRANT_URL)
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 build_qdrant_vector_store
    #本地模型导入
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_qdrant_vector_store
    sparse_encoder = fastembed_sparse_encoder(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_qdrant_vector_store
        model_name=SPARSE_MODEL,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_qdrant_vector_store
        cache_dir=BM25_MODEL_DIR,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 build_qdrant_vector_store
    )
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 build_qdrant_vector_store
    return QdrantVectorStore(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_qdrant_vector_store
        collection_name=collection_name,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_qdrant_vector_store
        client=client,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_qdrant_vector_store
        enable_hybrid=True,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_qdrant_vector_store
        sparse_doc_fn=sparse_encoder,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_qdrant_vector_store
        sparse_query_fn=sparse_encoder,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 build_qdrant_vector_store
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
def build_documents_from_items(
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
    items: Iterable[dict[str, Any]],
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
) -> list[Document]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
    '\n    将解析后的数据转换为 LlamaIndex Document。\n    markdown / text 是真正会被向量化的内容。\n    metadata 会写入 Qdrant payload。\n    '
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
    documents = []
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
    # [2026-07-03 16:33:01] 作用：逐项处理集合或重复任务；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
    for item in items:
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
        text = item.get("markdown") or item.get("text") or ""
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
        if not text.strip():
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
            continue
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
        documents.append(
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
            Document(
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
                text=text,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
                metadata={
                    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
                    "kb_id": item.get("kb_id", "default"),
                    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
                    "file_id": item.get("file_id", ""),
                    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
                    "file_path": item.get("file_path", ""),
                    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
                    "file_name": item.get("file_name", ""),
                    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
                    "file_type": item.get("file_type", ""),
                    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
                    "engine": item.get("engine", ""),
                    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
                    "mode": item.get("mode", ""),
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
                },
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
            )
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
        )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 build_documents_from_items
    return documents
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.rag.vector_index_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
def upsert_items_to_qdrant(
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    items: Iterable[dict[str, Any]],
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    collection_name: str = DEFAULT_COLLECTION_NAME,
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
) -> dict[str, Any]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    '\n    写入 Qdrant。\n    这里只负责入库，不做查询。\n    '
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    configure_embedding()
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    vector_store = build_qdrant_vector_store(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
        collection_name=collection_name,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    storage_context = StorageContext.from_defaults(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
        vector_store=vector_store,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    documents = build_documents_from_items(items)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    if not documents:
        # [2026-07-03 16:33:01] 作用：阻止无效状态继续传播；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
        raise ValueError("没有可写入向量库的文本内容")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    VectorStoreIndex.from_documents(
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
        documents,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
        storage_context=storage_context,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    return {
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
        "success": True,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
        "collection_name": collection_name,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
        "indexed_count": len(documents),
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
        "qdrant_url": QDRANT_URL,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
        "hybrid": True,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
        "sparse_model": SPARSE_MODEL,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 upsert_items_to_qdrant
    }
