# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.vectorstore.qdrant_connector 的模块级声明
import json
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.vectorstore.qdrant_connector 的模块级声明
import logging
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.vectorstore.qdrant_connector 的模块级声明
import os
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.vectorstore.qdrant_connector 的模块级声明
from typing import Any, Dict
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.vectorstore.qdrant_connector 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.vectorstore.qdrant_connector 的模块级声明
import qdrant_client
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.vectorstore.qdrant_connector 的模块级声明
from llama_index.vector_stores.qdrant import QdrantVectorStore
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.vectorstore.qdrant_connector 的模块级声明
from qdrant_client.http.models import ScoredPoint
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.vectorstore.qdrant_connector 的模块级声明
from qdrant_client.models import VectorParams
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.vectorstore.qdrant_connector 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.vectorstore.qdrant_connector 的模块级声明
from app.query.query import DocumentWithScore, QueryResult, QueryWithEmbedding
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.vectorstore.qdrant_connector 的模块级声明
from app.vectorstore.base import VectorStoreConnector
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.vectorstore.qdrant_connector 的模块级声明
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.vectorstore.qdrant_connector 的模块级声明
logger = logging.getLogger(__name__)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.vectorstore.qdrant_connector 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.vectorstore.qdrant_connector 的模块级声明
# [2026-07-03 16:33:01] 作用：定义封装数据或行为的类；理由依据：公共程序层所有；本行属于类 QdrantVectorStoreConnector
class QdrantVectorStoreConnector(VectorStoreConnector):
    # [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
    def __init__(self, ctx: Dict[str, Any], **kwargs: Any) -> None:
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
        super().__init__(ctx, **kwargs)
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
        self.ctx = ctx
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
        self.collection_name = ctx.get("collection", "collection")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
        self.url = ctx.get("url", "http://127.0.0.1")
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
        self.port = ctx.get("port", 6333)
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
        self.grpc_port = ctx.get("grpc_port", 6334)
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
        self.prefer_grpc = ctx.get("prefer_grpc", False)
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
        self.https = ctx.get("https", False)
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
        self.timeout = ctx.get("timeout", 300)
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
        self.vector_size = ctx.get("vector_size", 1536)
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
        self.distance = ctx.get("distance", "Cosine")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
        if self.url == ":memory:":
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
            self.client = qdrant_client.QdrantClient(":memory:")
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
        else:
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
            self.client = qdrant_client.QdrantClient(
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
                url=self.url,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
                port=self.port,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
                grpc_port=self.grpc_port,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
                prefer_grpc=self.prefer_grpc,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
                https=self.https,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
                timeout=self.timeout,
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
                **kwargs,
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
            )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
        self.store = QdrantVectorStore(
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
            client=self.client,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
            collection_name=self.collection_name,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
            vectors_config=VectorParams(size=self.vector_size, distance=self.distance),
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.__init__
        )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 QdrantVectorStoreConnector
    # [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
    def search(self, query: QueryWithEmbedding, **kwargs):
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
        consistency = kwargs.get("consistency", "majority")
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
        search_params = kwargs.get("search_params")
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
        score_threshold = kwargs.get("score_threshold", 0.1)
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
        filter_conditions = kwargs.get("filter")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
        hits = self.client.query_points(
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
            collection_name=self.collection_name,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
            query=query.embedding,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
            with_vectors=True,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
            limit=query.top_k,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
            consistency=consistency,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
            search_params=search_params,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
            score_threshold=score_threshold,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
            query_filter=filter_conditions,
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
        )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
        results = [self._convert_scored_point_to_document_with_score(point) for point in hits.points]
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
        results = [result for result in results if result is not None]
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
        return QueryResult(
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
            query=query.query,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
            results=results,
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.search
        )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 QdrantVectorStoreConnector
    # [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
    def _convert_scored_point_to_document_with_score(self, scored_point: ScoredPoint) -> DocumentWithScore | None:
        # [2026-07-03 16:33:01] 作用：控制异常处理和资源清理；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
        try:
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
            payload = scored_point.payload or {}
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
            text = scored_point.payload.get("text") or json.loads(payload["_node_content"]).get("text")
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
            metadata = payload.get("metadata") or json.loads(payload["_node_content"]).get("metadata")
            # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
            # todo source phrase
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
            relationships = json.loads(payload["_node_content"]).get("relationships")
            # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
            if relationships is not None and metadata.get("source") is None:
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
                source = relationships.get("1").get("metadata").get("source")
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
                metadata["source"] = os.path.basename(source)
            # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
            return DocumentWithScore(
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
                id=scored_point.id,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
                text=text,  # type: ignore
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
                metadata=metadata,  # type: ignore
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
                embedding=scored_point.vector,  # type: ignore
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
                score=scored_point.score,
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
            )
        # [2026-07-03 16:33:01] 作用：控制异常处理和资源清理；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
        except Exception:
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
            logger.exception("Failed to convert scored point to document")
            # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector._convert_scored_point_to_document_with_score
            return None
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 QdrantVectorStoreConnector
    # [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.delete
    def delete(self, **delete_kwargs: Any):
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.delete
        ids = delete_kwargs.get("ids")
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.delete
        if ids:
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.delete
            self.store.delete_nodes(ids)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 QdrantVectorStoreConnector
    # [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.create_collection
    def create_collection(self, **kwargs: Any):
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.create_collection
        vector_size = kwargs.get("vector_size")
        # [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.create_collection
        from qdrant_client.http import models as rest
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.create_collection
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.create_collection
        self.client.recreate_collection(
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.create_collection
            collection_name=self.collection_name,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.create_collection
            vectors_config=rest.VectorParams(
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.create_collection
                size=vector_size,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.create_collection
                distance=rest.Distance.COSINE,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.create_collection
            ),
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.create_collection
        )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于类 QdrantVectorStoreConnector
    # [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.delete_collection
    def delete_collection(self, **kwargs: Any):
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 QdrantVectorStoreConnector.delete_collection
        self.client.delete_collection(collection_name=self.collection_name)
