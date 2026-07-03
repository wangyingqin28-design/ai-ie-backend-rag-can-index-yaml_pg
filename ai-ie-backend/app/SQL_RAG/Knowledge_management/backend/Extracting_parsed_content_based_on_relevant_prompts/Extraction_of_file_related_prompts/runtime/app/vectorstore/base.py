# [2026-07-03 14:26:28] 中文迁移说明：本文件完整复制自 app/vectorstore/base.py；纳入依据为 DeepSeek 提取入库链 的项目内传递依赖闭包。
from abc import ABC, abstractmethod
from typing import Any, Dict

from llama_index.core.embeddings import BaseEmbedding
from llama_index.core.vector_stores.types import VectorStore

from app.query.query import QueryResult, QueryWithEmbedding


class VectorStoreConnector(ABC):
    def __init__(self, ctx: Dict[str, Any], **kwargs: Any) -> None:
        self.ctx = ctx
        self.client = None
        self.embedding: BaseEmbedding = None
        self.store: VectorStore = None

    @abstractmethod
    def search(self, query: QueryWithEmbedding, **kwargs) -> QueryResult:
        pass

    @abstractmethod
    def delete(self, **delete_kwargs: Any):
        pass

    @abstractmethod
    def create_collection(self, **create_kwargs: Any):
        pass

    @abstractmethod
    def delete_collection(self, **delete_kwargs: Any):
        pass
