# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.vectorstore.base 的模块级声明
from abc import ABC, abstractmethod
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.vectorstore.base 的模块级声明
from typing import Any, Dict
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.vectorstore.base 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.vectorstore.base 的模块级声明
from llama_index.core.embeddings import BaseEmbedding
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.vectorstore.base 的模块级声明
from llama_index.core.vector_stores.types import VectorStore
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.vectorstore.base 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.vectorstore.base 的模块级声明
from app.query.query import QueryResult, QueryWithEmbedding
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.vectorstore.base 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.vectorstore.base 的模块级声明
# [2026-07-03 16:33:01] 作用：定义封装数据或行为的类；理由依据：公共程序层所有；本行属于类 VectorStoreConnector
class VectorStoreConnector(ABC):
    # [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 VectorStoreConnector.__init__
    def __init__(self, ctx: Dict[str, Any], **kwargs: Any) -> None:
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 VectorStoreConnector.__init__
        self.ctx = ctx
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 VectorStoreConnector.__init__
        self.client = None
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 VectorStoreConnector.__init__
        self.embedding: BaseEmbedding = None
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 VectorStoreConnector.__init__
        self.store: VectorStore = None
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 VectorStoreConnector
    # [2026-07-03 16:33:01] 作用：为下方定义注册装饰器行为；理由依据：公共程序层所有；本行属于类 VectorStoreConnector
    @abstractmethod
    # [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 VectorStoreConnector.search
    def search(self, query: QueryWithEmbedding, **kwargs) -> QueryResult:
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 VectorStoreConnector.search
        pass
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 VectorStoreConnector
    # [2026-07-03 16:33:01] 作用：为下方定义注册装饰器行为；理由依据：公共程序层所有；本行属于类 VectorStoreConnector
    @abstractmethod
    # [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 VectorStoreConnector.delete
    def delete(self, **delete_kwargs: Any):
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 VectorStoreConnector.delete
        pass
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 VectorStoreConnector
    # [2026-07-03 16:33:01] 作用：为下方定义注册装饰器行为；理由依据：公共程序层所有；本行属于类 VectorStoreConnector
    @abstractmethod
    # [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 VectorStoreConnector.create_collection
    def create_collection(self, **create_kwargs: Any):
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 VectorStoreConnector.create_collection
        pass
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 VectorStoreConnector
    # [2026-07-03 16:33:01] 作用：为下方定义注册装饰器行为；理由依据：公共程序层所有；本行属于类 VectorStoreConnector
    @abstractmethod
    # [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 VectorStoreConnector.delete_collection
    def delete_collection(self, **delete_kwargs: Any):
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 VectorStoreConnector.delete_collection
        pass
