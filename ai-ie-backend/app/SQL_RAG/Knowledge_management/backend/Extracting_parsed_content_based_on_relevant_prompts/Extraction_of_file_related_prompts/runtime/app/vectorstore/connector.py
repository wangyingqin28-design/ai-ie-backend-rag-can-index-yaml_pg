# [2026-07-03 14:26:28] 中文迁移说明：本文件完整复制自 app/vectorstore/connector.py；纳入依据为 DeepSeek 提取入库链 的项目内传递依赖闭包。
from typing import Any, Dict


class VectorStoreConnectorAdaptor:
    def __init__(self, vector_store_type, ctx: Dict[str, Any], **kwargs: Any) -> None:
        self.ctx = ctx
        self.vector_store_type = vector_store_type

        # only import the connector class when it is needed
        match vector_store_type:
            case "qdrant":
                from app.vectorstore.qdrant_connector import QdrantVectorStoreConnector

                self.connector = QdrantVectorStoreConnector(ctx, **kwargs)
            case _:
                raise ValueError("unsupported vector store type:", vector_store_type)
