# -*- coding: utf-8 -*-
"""验证 Qdrant/LlamaIndex 兼容和 External_database 外部库接入契约。"""

# 2026-06-10 18:01:50 修改：导入 json，用于构造真实 CanonicalChunk 的 keywords/payload_json。
import json
# 2026-06-10 18:01:50 修改：导入 sys，用于把测试目录和 data_cleaning 目录加入模块搜索路径。
import sys
# 2026-06-10 18:01:50 修改：导入 Path，用于稳定定位当前测试目录。
from pathlib import Path
# 2026-06-10 18:01:50 修改：导入 unittest，沿用仓库现有测试风格。
import unittest

# 2026-06-10 18:01:50 修改：定位当前测试目录，理由是直接运行测试文件时也能导入本目录脚本。
CURRENT_DIR = Path(__file__).resolve().parent
# 2026-06-10 18:01:50 修改：定位 data_cleaning 目录，作用是导入 Qdrant 和 integration 包。
DATA_CLEANING_DIR = CURRENT_DIR.parent
# 2026-06-10 18:01:50 修改：确保当前测试目录在 sys.path，理由是导入 external_database_to_qdrant_conversion。
if str(CURRENT_DIR) not in sys.path:
    # 2026-06-10 18:01:50 修改：插到最前，作用是优先使用当前目录脚本。
    sys.path.insert(0, str(CURRENT_DIR))
# 2026-06-10 18:01:50 修改：确保 data_cleaning 在 sys.path，理由是导入 integration adapter。
if str(DATA_CLEANING_DIR) not in sys.path:
    # 2026-06-10 18:01:50 修改：插到最前，作用是优先使用当前项目包。
    sys.path.insert(0, str(DATA_CLEANING_DIR))

# 2026-06-10 18:01:50 修改：导入外部库转换入口，作用是验证不另拉 Qdrant 写入链路。
import external_database_to_qdrant_conversion as conversion
# 2026-06-10 18:01:50 修改：导入待新增 adapter，作用是验证 External_database 建库/转换契约。
from integration import external_database_adapter


# 2026-06-10 18:01:50 修改：定义新合同测试类，理由是把三个准信点固化成自动测试。
class QdrantExternalContractsTest(unittest.TestCase):
    # 2026-06-10 18:01:50 修改：构造真实 CanonicalChunk，理由是 payload 改造必须测真实生产类型。
    def build_real_canonical_chunk(self):
        # 2026-06-10 18:01:50 修改：读取同步模块，作用是复用生产 CanonicalChunk dataclass。
        qdrant_sync = conversion.qdrant_sync
        # 2026-06-10 18:01:50 修改：构造答案文本，理由是校验 text/retrieval_text 必须包含完整答案。
        answer = "正常流程是发出去的时候先做好二次工艺单，把价格数量保存起来，打单给外发部门。"
        # 2026-06-10 18:01:50 修改：构造来源摘录，作用是让同步契约覆盖外部库 evidence 字段。
        source_excerpt = f"客户：二次工艺流程不对。\n客服：{answer}"
        # 2026-06-10 18:01:50 修改：返回真实 CanonicalChunk，作用是驱动 build_qdrant_payload 真实行为。
        return qdrant_sync.CanonicalChunk(
            # 2026-06-10 18:01:50 修改：设置 chunk 主键，理由是 Qdrant point id 需要稳定来源。
            chunk_id="external-chunk-1",
            # 2026-06-10 18:01:50 修改：设置文档主键，作用是后续 doc_id 直接引用。
            document_id="External_database:external_qa_samples",
            # 2026-06-10 18:01:50 修改：外部库没有音频编号，使用 0 保持类型稳定。
            audio_no=0,
            # 2026-06-10 18:01:50 修改：外部库没有音频标题，使用库名便于排查。
            audio_title="External_database",
            # 2026-06-10 18:01:50 修改：设置 chunk 序号，作用是保持排序字段存在。
            chunk_index=1,
            # 2026-06-10 18:01:50 修改：设置业务场景，理由是 keyword_terms 必须包含 scene。
            scene="二次工艺外发流程，涉及到加工单的创建和收货",
            # 2026-06-10 18:01:50 修改：设置问题，作用是覆盖截图第一条字段。
            question="二次工艺流程不对，是后补的，不是发出去的时候做",
            # 2026-06-10 18:01:50 修改：设置答案，作用是覆盖截图第一条字段。
            answer=answer,
            # 2026-06-10 18:01:50 修改：设置清洗文本，理由是 validate_chunks_before_qdrant 需要可消费文本。
            cleaned_text=f"问题：二次工艺流程不对，是后补的，不是发出去的时候做\n答案：{answer}",
            # 2026-06-10 18:01:50 修改：设置处理步骤 JSON，作用是测试关键词辅助字段不会破坏旧字段。
            resolution_steps=json.dumps(["先做二次工艺单", "保存价格数量", "打单给外发部门"], ensure_ascii=False),
            # 2026-06-10 18:01:50 修改：设置旧 keywords 字符串，理由是新 keyword_terms 要从这里规范化。
            keywords=json.dumps(["二次工艺", "外发部门", "加工单"], ensure_ascii=False),
            # 2026-06-10 18:01:50 修改：设置实体 JSON，作用是保持旧 payload 字段不变。
            entities_json="{}",
            # 2026-06-10 18:01:50 修改：设置来源片段，作用是保持旧 payload 字段不变。
            source_excerpt=source_excerpt,
            # 2026-06-10 18:01:50 修改：设置内容 hash，作用是保持旧同步状态字段不变。
            content_hash="external-content-hash-1",
            # 2026-06-10 18:01:50 修改：设置 QA 对 ID，作用是保持旧同步状态字段不变。
            qa_pair_id="external-qa-1",
            # 2026-06-10 18:01:50 修改：设置 QA 对序号，作用是保持旧同步状态字段不变。
            qa_pair_index=1,
            # 2026-06-10 18:01:50 修改：设置相似度分数，作用是保持旧字段类型稳定。
            qa_similarity_score=1.0,
            # 2026-06-10 18:01:50 修改：设置相似度阈值，作用是保持旧字段类型稳定。
            qa_similarity_threshold=0.0,
            # 2026-06-10 18:01:50 修改：设置 QA 已校验，理由是 Qdrant 同步只接受已校验 chunk。
            qa_pair_validated=True,
            # 2026-06-10 18:01:50 修改：设置文档内聚类 ID，作用是保持过滤字段不变。
            cluster_id="external-cluster-1",
            # 2026-06-10 18:01:50 修改：设置文档内聚类标签，作用是保持过滤字段不变。
            cluster_label="二次工艺流程",
            # 2026-06-10 18:01:50 修改：设置文档内聚类层级，作用是保持过滤字段不变。
            cluster_level="external",
            # 2026-06-10 18:01:50 修改：设置文档内聚类路径，作用是保持过滤字段不变。
            cluster_path="External_database/二次工艺流程",
            # 2026-06-10 18:01:50 修改：设置全局聚类 ID，作用是保持过滤字段不变。
            global_cluster_id="external-global-1",
            # 2026-06-10 18:01:50 修改：设置全局聚类标签，作用是保持过滤字段不变。
            global_cluster_label="外部库流程问答",
            # 2026-06-10 18:01:50 修改：设置全局聚类层级，作用是保持过滤字段不变。
            global_cluster_level="external",
            # 2026-06-10 18:01:50 修改：设置全局聚类路径，作用是保持过滤字段不变。
            global_cluster_path="External_database/外部库流程问答",
            # 2026-06-10 18:01:50 修改：设置问题 hash，作用是保持去重字段不变。
            question_hash="question-hash-1",
            # 2026-06-10 18:01:50 修改：设置答案 hash，作用是保持去重字段不变。
            answer_hash="answer-hash-1",
            # 2026-06-10 18:01:50 修改：设置 canonical chunk id，作用是保持融合字段不变。
            canonical_chunk_id="external-chunk-1",
            # 2026-06-10 18:01:50 修改：设置 canonical 状态，理由是 duplicate 不应入 Qdrant。
            fusion_status="canonical",
            # 2026-06-10 18:01:50 修改：设置 payload schema 版本，作用是标识外部扁平 QA 来源。
            payload_schema_version="external-flat-qa-v1",
            # 2026-06-10 18:01:50 修改：设置 payload_json，作用是覆盖现有链路读取的新契约字段。
            payload_json={
                # 2026-06-10 18:01:50 修改：设置规范问题，理由是 keyword_terms 要包含 canonical_question。
                "canonical_question": "二次工艺的正确操作流程是什么？",
                # 2026-06-10 18:01:50 修改：设置别名问法，理由是 keyword_terms 要包含 query_aliases。
                "query_aliases": ["二次工艺怎么做", "外发流程怎么走"],
                # 2026-06-10 18:01:50 修改：设置完整来源，作用是同步前契约校验。
                "source_excerpt_full": source_excerpt,
                # 2026-06-10 18:01:50 修改：设置检索文本，作用是保持现有向量内容逻辑。
                "retrieval_text": f"规范问题：二次工艺的正确操作流程是什么？\n答案：{answer}",
                # 2026-06-10 18:01:50 修改：设置 LLM 文本，作用是保持现有 text payload 逻辑。
                "llm_text": f"问题：二次工艺的正确操作流程是什么？\n答案：{answer}",
                # 2026-06-10 18:01:50 修改：设置 Qdrant ready，理由是同步校验必须通过。
                "qdrant_ready": True,
            },
            # 2026-06-10 18:01:50 修改：设置 RAG 契约版本，作用是保持旧过滤字段不变。
            rag_contract_version="qa-rag-contract-v1",
            # 2026-06-10 18:01:50 修改：设置规范问题，作用是直接驱动 payload 字段。
            canonical_question="二次工艺的正确操作流程是什么？",
            # 2026-06-10 18:01:50 修改：设置答案优先字段，作用是保持现有问答质量链路。
            answer_text=answer,
            # 2026-06-10 18:01:50 修改：设置别名问法，作用是驱动 keyword_terms。
            query_aliases=["二次工艺怎么做", "外发流程怎么走"],
            # 2026-06-10 18:01:50 修改：设置完整来源，作用是同步前契约校验。
            source_excerpt_full=source_excerpt,
            # 2026-06-10 18:01:50 修改：设置 LLM 文本，作用是保持 text payload。
            llm_text=f"问题：二次工艺的正确操作流程是什么？\n答案：{answer}",
            # 2026-06-10 18:01:50 修改：设置检索文本，作用是保持 retrieval_text payload。
            retrieval_text=f"规范问题：二次工艺的正确操作流程是什么？\n答案：{answer}",
            # 2026-06-10 18:01:50 修改：设置 duplicate 上下文为空，理由是外部样例没有融合重复项。
            duplicate_contexts=[],
            # 2026-06-10 18:01:50 修改：设置合并 duplicate IDs 为空，理由是外部样例没有融合重复项。
            merged_duplicate_chunk_ids=[],
            # 2026-06-10 18:01:50 修改：设置可同步，理由是 adapter 生成的数据要能进入 Qdrant。
            qdrant_ready=True,
            # 2026-06-10 18:01:50 修改：设置校验标记为空，理由是样例数据无错误标记。
            validation_flags=[],
        )

    # 2026-06-10 18:01:50 修改：测试 LlamaIndex 默认 doc_id 和关键词字段，理由是别人不能再靠 false 参数绕过。
    def test_qdrant_payload_exposes_llamaindex_document_id_and_keyword_terms(self) -> None:
        # 2026-06-10 18:01:50 修改：读取同步模块，作用是验证生产 payload 构造函数。
        qdrant_sync = conversion.qdrant_sync
        # 2026-06-10 18:01:50 修改：构造真实 chunk，作用是覆盖 getai 与外部库统一 CanonicalChunk 输入。
        chunk = self.build_real_canonical_chunk()
        # 2026-06-10 18:01:50 修改：构造 embedding 配置，作用是满足 build_qdrant_payload 签名。
        embedding_config = qdrant_sync.EmbeddingConfig(
            # 2026-06-10 18:01:50 修改：设置假 embedding 地址，理由是该测试不发网络请求。
            api_base="http://embedding-service/v1",
            # 2026-06-10 18:01:50 修改：设置假 API key，理由是该测试不发网络请求。
            api_key="fake-key",
            # 2026-06-10 18:01:50 修改：设置假模型名，作用是进入 payload 元数据。
            model="fake-embedding-model",
            # 2026-06-10 18:01:50 修改：设置维度，作用是进入 payload 元数据。
            dimension=2,
            # 2026-06-10 18:01:50 修改：设置批大小，理由是 dataclass 必填。
            batch_size=2,
        )
        # 2026-06-10 18:01:50 修改：构造 payload，作用是检查写入 Qdrant point 前的最终字段。
        payload = qdrant_sync.build_qdrant_payload(chunk, embedding_config)
        # 2026-06-10 18:01:50 修改：断言 LlamaIndex 默认 doc_id key 存在，理由是 index_doc_id=True 不能再失败。
        self.assertEqual(qdrant_sync.LLAMAINDEX_DOCUMENT_ID_PAYLOAD_KEY, "doc_id")
        # 2026-06-10 18:01:50 修改：断言 doc_id 值沿用 chunk.document_id，作用是不影响现有 document_id 字段。
        self.assertEqual(payload[qdrant_sync.LLAMAINDEX_DOCUMENT_ID_PAYLOAD_KEY], chunk.document_id)
        # 2026-06-10 18:01:50 修改：断言原 document_id 保留，理由是当前 agent 与回表链路不变。
        self.assertEqual(payload["document_id"], chunk.document_id)
        # 2026-06-10 18:01:50 修改：断言 keyword_terms 是列表，作用是让 Qdrant UI 可见关键词字段。
        self.assertIsInstance(payload["keyword_terms"], list)
        # 2026-06-10 18:01:50 修改：断言旧 keywords 被规范化，理由是旧字段只是字符串不是索引合同。
        self.assertIn("二次工艺", payload["keyword_terms"])
        # 2026-06-10 18:01:50 修改：断言 query_aliases 被规范化，作用是兼容别人关键词过滤。
        self.assertIn("二次工艺怎么做", payload["keyword_terms"])
        # 2026-06-10 18:01:50 修改：断言 scene 被规范化，作用是兼容业务场景关键词过滤。
        self.assertIn("二次工艺外发流程，涉及到加工单的创建和收货", payload["keyword_terms"])
        # 2026-06-10 18:01:50 修改：断言 canonical_question 被规范化，作用是提升外部 RAG 可见字段。
        self.assertIn("二次工艺的正确操作流程是什么？", payload["keyword_terms"])

    # 2026-06-10 18:01:50 修改：测试 Qdrant payload index 创建字段，理由是官方检索/filter 不能缺索引。
    def test_create_payload_indexes_adds_llamaindex_keyword_and_text_indexes(self) -> None:
        # 2026-06-10 18:01:50 修改：定义假 Qdrant client，作用是捕获 create_payload_index 调用。
        class FakePayloadIndexClient:
            # 2026-06-10 18:01:50 修改：初始化调用列表，理由是测试只关心字段契约不需要真实 Qdrant。
            def __init__(self) -> None:
                # 2026-06-10 18:01:50 修改：保存全部索引字段，作用是后续断言。
                self.calls: list[tuple[str, str, object]] = []

            # 2026-06-10 18:01:50 修改：复刻 Qdrant create_payload_index API，理由是隔离外部服务。
            def create_payload_index(self, collection_name: str, field_name: str, field_schema: object) -> None:
                # 2026-06-10 18:01:50 修改：记录入参，作用是验证字段和 collection。
                self.calls.append((collection_name, field_name, field_schema))

        # 2026-06-10 18:01:50 修改：创建假 client，作用是驱动生产 create_payload_indexes。
        client = FakePayloadIndexClient()
        # 2026-06-10 18:01:50 修改：调用生产索引函数，理由是保证新旧 collection 都补齐索引。
        conversion.qdrant_sync.create_payload_indexes(client, "sql_External_database")
        # 2026-06-10 18:01:50 修改：抽取字段名集合，作用是简化断言。
        indexed_fields = {field_name for _, field_name, _ in client.calls}
        # 2026-06-10 18:01:50 修改：断言 LlamaIndex doc_id payload index 存在，理由是默认 index_doc_id=True 可用。
        self.assertIn("doc_id", indexed_fields)
        # 2026-06-10 18:01:50 修改：断言规范化关键词索引存在，作用是让 Qdrant UI 和 filter 能看到关键词字段。
        self.assertIn("keyword_terms", indexed_fields)
        # 2026-06-10 18:01:50 修改：断言别名关键词索引存在，作用是兼容现有 query_aliases。
        self.assertIn("query_aliases", indexed_fields)
        # 2026-06-10 18:01:50 修改：断言默认 text 全文索引存在，理由是外部 RAG loader 常用 text_key。
        self.assertIn("text", indexed_fields)
        # 2026-06-10 18:01:50 修改：断言 retrieval_text 全文索引存在，作用是支持检索文本过滤/排查。
        self.assertIn("retrieval_text", indexed_fields)

    # 2026-06-11 08:23:49 修改：测试默认 Qdrant 写入仍保持旧 dense vector。理由：保护现有 agent RAG 精准链路。
    def test_default_qdrant_points_keep_legacy_dense_vector_shape(self) -> None:
        # 2026-06-11 08:23:49 修改：读取同步模块。作用：验证生产 point 构造函数。
        qdrant_sync = conversion.qdrant_sync
        # 2026-06-11 08:23:49 修改：构造真实 chunk。作用：覆盖统一 CanonicalChunk 输入。
        chunk = self.build_real_canonical_chunk()
        # 2026-06-11 08:23:49 修改：构造 embedding 配置。作用：满足 payload 构造依赖。
        embedding_config = qdrant_sync.EmbeddingConfig(
            # 2026-06-11 08:23:49 修改：设置假服务地址。理由：该测试不发网络请求。
            api_base="http://embedding-service/v1",
            # 2026-06-11 08:23:49 修改：设置假 API key。理由：该测试不发网络请求。
            api_key="fake-key",
            # 2026-06-11 08:23:49 修改：设置模型名。作用：写入 payload 元数据。
            model="fake-embedding-model",
            # 2026-06-11 08:23:49 修改：设置维度。作用：验证向量维度字段。
            dimension=2,
            # 2026-06-11 08:23:49 修改：设置批大小。理由：dataclass 必填。
            batch_size=2,
        )
        # 2026-06-11 08:23:49 修改：构造默认 Qdrant 配置。作用：模拟当前主 agent collection 写法。
        qdrant_config = qdrant_sync.QdrantSyncConfig(
            # 2026-06-11 08:23:49 修改：设置假 Qdrant 地址。理由：该测试不连接 Qdrant。
            url="http://127.0.0.1:6333",
            # 2026-06-11 08:23:49 修改：设置现有主 collection 名。作用：证明默认路径不改名。
            collection_name="sql_rag_qa_chunks_v1",
            # 2026-06-11 08:23:49 修改：设置距离。作用：满足配置构造。
            distance="Cosine",
            # 2026-06-11 08:23:49 修改：不重建 collection。理由：默认保护现有库。
            recreate_collection=False,
            # 2026-06-11 08:23:49 修改：设置批大小。作用：满足配置构造。
            upsert_batch_size=1,
            # 2026-06-11 08:23:49 修改：关闭 dry-run。作用：只测试 point 结构。
            dry_run=False,
        )
        # 2026-06-11 08:23:49 修改：构造 point。作用：验证默认仍是未命名 dense 向量。
        points = qdrant_sync.build_qdrant_points([chunk], [[0.1, 0.2]], embedding_config, qdrant_config)
        # 2026-06-11 08:23:49 修改：断言默认 vector 仍是 list。理由：不影响当前 QdrantVectorStore dense 消费。
        self.assertEqual(points[0].vector, [0.1, 0.2])

    # 2026-06-11 08:23:49 修改：测试显式 hybrid collection 使用 LlamaIndex 默认命名向量。理由：外部消费者可开启 enable_hybrid。
    def test_hybrid_qdrant_points_write_llamaindex_named_dense_and_sparse_vectors(self) -> None:
        # 2026-06-11 08:23:49 修改：读取同步模块。作用：验证生产 hybrid point 构造函数。
        qdrant_sync = conversion.qdrant_sync
        # 2026-06-11 08:23:49 修改：构造真实 chunk。作用：用实际文本生成 sparse term。
        chunk = self.build_real_canonical_chunk()
        # 2026-06-11 08:23:49 修改：构造 embedding 配置。作用：满足 point 构造签名。
        embedding_config = qdrant_sync.EmbeddingConfig(
            # 2026-06-11 08:23:49 修改：设置假服务地址。理由：该测试不发网络请求。
            api_base="http://embedding-service/v1",
            # 2026-06-11 08:23:49 修改：设置假 API key。理由：该测试不发网络请求。
            api_key="fake-key",
            # 2026-06-11 08:23:49 修改：设置模型名。作用：写入 payload 元数据。
            model="fake-embedding-model",
            # 2026-06-11 08:23:49 修改：设置维度。作用：验证 dense 向量维度。
            dimension=2,
            # 2026-06-11 08:23:49 修改：设置批大小。理由：dataclass 必填。
            batch_size=2,
        )
        # 2026-06-11 08:23:49 修改：构造 hybrid Qdrant 配置。作用：模拟外部新 collection 的兼容增强模式。
        qdrant_config = qdrant_sync.QdrantSyncConfig(
            # 2026-06-11 08:23:49 修改：设置独立 Qdrant 地址。理由：不和旧服务端口冲突。
            url="http://127.0.0.1:6334",
            # 2026-06-11 08:23:49 修改：设置外部 collection 名。作用：不污染主 agent collection。
            collection_name="sql_External_database",
            # 2026-06-11 08:23:49 修改：设置距离。作用：满足配置构造。
            distance="Cosine",
            # 2026-06-11 08:23:49 修改：允许新建时使用 hybrid 结构。理由：旧 collection 不原地改结构。
            recreate_collection=True,
            # 2026-06-11 08:23:49 修改：设置批大小。作用：满足配置构造。
            upsert_batch_size=1,
            # 2026-06-11 08:23:49 修改：关闭 dry-run。作用：只测试 point 结构。
            dry_run=False,
            # 2026-06-11 08:23:49 修改：显式打开 hybrid。理由：默认不影响旧 dense collection。
            enable_hybrid=True,
        )
        # 2026-06-11 08:23:49 修改：保存原 sparse builder。理由：测试结束后恢复生产函数。
        original_sparse_builder = getattr(qdrant_sync, "build_llamaindex_sparse_vectors", None)
        # 2026-06-11 08:23:49 修改：注入假 sparse builder。理由：单测不下载真实 LlamaIndex/FastEmbed 模型。
        # 2026-06-12 00:18:30 修改：记录 sparse 模型名；作用：验证文档侧 sparse encoder 真的使用 Qdrant/bm25；理由：别人查询侧会设置 fastembed_sparse_model="Qdrant/bm25"。
        captured_sparse_models: list[str] = []

        # 2026-06-12 00:18:30 修改：定义带模型名参数的假 sparse builder；作用：强制生产代码传入 fastembed_sparse_model；理由：只创建 text-sparse-new 但模型不一致仍会影响 hybrid RAG。
        def fake_sparse_builder(texts: list[str], fastembed_sparse_model: str) -> list[object]:
            # 2026-06-12 00:18:30 修改：记录模型名；作用：供断言检查；理由：避免默认 Splade 被误用。
            captured_sparse_models.append(fastembed_sparse_model)
            # 2026-06-12 00:18:30 修改：返回假 SparseVector；作用：不下载真实 FastEmbed 模型；理由：单测只验证调用契约。
            return [
                # 2026-06-12 00:18:30 修改：构造 Qdrant SparseVector；作用：模拟官方 BM25 sparse doc encoder 输出；理由：保持 point 结构校验真实。
                qdrant_sync.models.SparseVector(indices=[1, 2], values=[1.0, 0.5])
                # 2026-06-12 00:18:30 修改：逐条返回 sparse vector；作用：保持输入输出数量一致；理由：生产代码会校验数量。
                for _ in texts
            ]

        # 2026-06-12 00:18:30 修改：替换 sparse builder；作用：隔离真实模型下载；理由：红绿测试不依赖网络。
        qdrant_sync.build_llamaindex_sparse_vectors = fake_sparse_builder
        # 2026-06-11 08:23:49 修改：用 try/finally 包住 monkeypatch。理由：避免污染后续测试。
        try:
            # 2026-06-11 08:23:49 修改：构造 point。作用：验证 dense+sparse 同时写入。
            points = qdrant_sync.build_qdrant_points([chunk], [[0.1, 0.2]], embedding_config, qdrant_config)
        # 2026-06-11 08:23:49 修改：测试结束后恢复函数。理由：保护其他测试读取真实生产实现。
        finally:
            # 2026-06-11 08:23:49 修改：如果原函数存在就恢复。作用：保持模块状态干净。
            if original_sparse_builder is not None:
                # 2026-06-11 08:23:49 修改：恢复原函数。理由：撤销 monkeypatch。
                qdrant_sync.build_llamaindex_sparse_vectors = original_sparse_builder
            # 2026-06-11 08:23:49 修改：如果原函数不存在就删除临时属性。理由：保持失败状态也不污染模块。
            else:
                # 2026-06-11 08:23:49 修改：删除测试临时函数。作用：还原模块初始形态。
                delattr(qdrant_sync, "build_llamaindex_sparse_vectors")
        # 2026-06-11 08:23:49 修改：读取 vector。作用：断言命名向量结构。
        vector_payload = points[0].vector
        # 2026-06-11 08:23:49 修改：断言 vector 是 dict。理由：LlamaIndex hybrid 查询使用命名向量。
        self.assertIsInstance(vector_payload, dict)
        # 2026-06-11 08:23:49 修改：断言 dense 名称。理由：匹配 LlamaIndex QdrantVectorStore 默认 text-dense。
        self.assertIn(qdrant_sync.LLAMAINDEX_DEFAULT_DENSE_VECTOR_NAME, vector_payload)
        # 2026-06-11 08:23:49 修改：断言 sparse 名称。理由：匹配 LlamaIndex QdrantVectorStore 默认 text-sparse-new。
        self.assertIn(qdrant_sync.LLAMAINDEX_DEFAULT_SPARSE_VECTOR_NAME, vector_payload)
        # 2026-06-11 08:23:49 修改：断言 dense 值不变。作用：保护向量相似度检索质量。
        self.assertEqual(vector_payload[qdrant_sync.LLAMAINDEX_DEFAULT_DENSE_VECTOR_NAME], [0.1, 0.2])
        # 2026-06-11 08:23:49 修改：断言 sparse vector 有 indices。作用：外部 hybrid 查询不再缺 sparse vector。
        self.assertGreater(len(vector_payload[qdrant_sync.LLAMAINDEX_DEFAULT_SPARSE_VECTOR_NAME].indices), 0)
        # 2026-06-11 08:23:49 修改：断言 sparse vector 有 values。作用：外部 hybrid 查询可实际计算稀疏分数。
        self.assertGreater(len(vector_payload[qdrant_sync.LLAMAINDEX_DEFAULT_SPARSE_VECTOR_NAME].values), 0)
        # 2026-06-12 00:18:30 修改：断言使用 BM25 sparse 模型；作用：和外部 QdrantVectorStore(fastembed_sparse_model="Qdrant/bm25") 对齐；理由：模型名必须从 config 传到文档侧 encoder。
        self.assertEqual(captured_sparse_models, [qdrant_sync.LLAMAINDEX_BM25_FASTEMBED_SPARSE_MODEL])

    # 2026-06-11 08:23:49 修改：测试显式 hybrid collection 创建结构。理由：collection 必须同时有 dense 和 sparse 配置。
    def test_hybrid_collection_creation_uses_llamaindex_dense_and_sparse_configs(self) -> None:
        # 2026-06-11 08:23:49 修改：读取同步模块。作用：验证生产建 collection 函数。
        qdrant_sync = conversion.qdrant_sync
        # 2026-06-11 08:23:49 修改：定义假 Qdrant client。理由：测试配置结构不需要真实服务。
        class FakeHybridCollectionClient:
            # 2026-06-11 08:23:49 修改：初始化记录字段。作用：捕获 create_collection 入参。
            def __init__(self) -> None:
                # 2026-06-11 08:23:49 修改：保存 create_collection 入参。作用：后续断言。
                self.created_kwargs: dict[str, object] = {}
                # 2026-06-11 08:23:49 修改：保存 payload index 调用。作用：兼容 create_payload_indexes。
                self.index_calls: list[tuple[str, str, object]] = []

            # 2026-06-11 08:23:49 修改：模拟 collection 不存在。理由：驱动新建 hybrid collection 分支。
            def collection_exists(self, collection_name: str) -> bool:
                # 2026-06-11 08:23:49 修改：返回 False。作用：让生产代码调用 create_collection。
                return False

            # 2026-06-11 08:23:49 修改：模拟 Qdrant create_collection。作用：捕获 dense/sparse 配置。
            def create_collection(self, **kwargs: object) -> None:
                # 2026-06-11 08:23:49 修改：记录全部入参。理由：断言不依赖真实 Qdrant。
                self.created_kwargs = kwargs

            # 2026-06-11 08:23:49 修改：模拟 payload index API。作用：让 ensure_qdrant_collection 完整执行。
            def create_payload_index(self, collection_name: str, field_name: str, field_schema: object) -> None:
                # 2026-06-11 08:23:49 修改：记录索引调用。理由：确认新建后仍补 payload index。
                self.index_calls.append((collection_name, field_name, field_schema))

        # 2026-06-11 08:23:49 修改：创建假 client。作用：驱动生产函数。
        client = FakeHybridCollectionClient()
        # 2026-06-11 08:23:49 修改：构造 embedding 配置。作用：提供 dense 维度。
        embedding_config = qdrant_sync.EmbeddingConfig(
            # 2026-06-11 08:23:49 修改：设置假服务地址。理由：该测试不发网络请求。
            api_base="http://embedding-service/v1",
            # 2026-06-11 08:23:49 修改：设置假 API key。理由：该测试不发网络请求。
            api_key="fake-key",
            # 2026-06-11 08:23:49 修改：设置模型名。作用：满足 dataclass。
            model="fake-embedding-model",
            # 2026-06-11 08:23:49 修改：设置维度。作用：验证 VectorParams size。
            dimension=2,
            # 2026-06-11 08:23:49 修改：设置批大小。理由：dataclass 必填。
            batch_size=2,
        )
        # 2026-06-11 08:23:49 修改：构造 hybrid Qdrant 配置。作用：新 collection 才打开 hybrid。
        qdrant_config = qdrant_sync.QdrantSyncConfig(
            # 2026-06-11 08:23:49 修改：设置独立 Qdrant 地址。理由：不和旧服务端口冲突。
            url="http://127.0.0.1:6334",
            # 2026-06-11 08:23:49 修改：设置外部 collection 名。作用：不污染主 agent collection。
            collection_name="sql_External_database",
            # 2026-06-11 08:23:49 修改：设置距离。作用：满足配置构造。
            distance="Cosine",
            # 2026-06-11 08:23:49 修改：重建新 collection。理由：hybrid 结构不能原地套到旧 dense collection。
            recreate_collection=True,
            # 2026-06-11 08:23:49 修改：设置批大小。作用：满足配置构造。
            upsert_batch_size=1,
            # 2026-06-11 08:23:49 修改：关闭 dry-run。作用：允许执行建 collection 分支。
            dry_run=False,
            # 2026-06-11 08:23:49 修改：显式打开 hybrid。理由：默认不影响旧 dense collection。
            enable_hybrid=True,
        )
        # 2026-06-11 08:23:49 修改：调用生产建库函数。作用：检查 create_collection 结构。
        qdrant_sync.ensure_qdrant_collection(client, qdrant_config, embedding_config)
        # 2026-06-11 08:23:49 修改：读取 dense 配置。作用：断言使用 LlamaIndex 默认 dense 名。
        vectors_config = client.created_kwargs["vectors_config"]
        # 2026-06-11 08:23:49 修改：读取 sparse 配置。作用：断言使用 LlamaIndex 默认 sparse 名。
        sparse_vectors_config = client.created_kwargs["sparse_vectors_config"]
        # 2026-06-11 08:23:49 修改：断言 dense 配置是 dict。理由：hybrid 查询必须指定 using=text-dense。
        self.assertIsInstance(vectors_config, dict)
        # 2026-06-11 08:23:49 修改：断言 sparse 配置是 dict。理由：hybrid 查询必须指定 using=text-sparse-new。
        self.assertIsInstance(sparse_vectors_config, dict)
        # 2026-06-11 08:23:49 修改：断言 dense 名存在。作用：匹配 LlamaIndex 默认配置。
        self.assertIn(qdrant_sync.LLAMAINDEX_DEFAULT_DENSE_VECTOR_NAME, vectors_config)
        # 2026-06-11 08:23:49 修改：断言 sparse 名存在。作用：匹配 LlamaIndex 默认配置。
        self.assertIn(qdrant_sync.LLAMAINDEX_DEFAULT_SPARSE_VECTOR_NAME, sparse_vectors_config)

    # 2026-06-12 00:18:30 修改：验证 source profile 会驱动 Qdrant config 切到 hybrid；作用：修复真实运行忘记加 --enable-hybrid 导致 dense-only 的问题；理由：不能再靠人工记参数。
    def test_source_profile_applies_hybrid_bm25_to_qdrant_config(self) -> None:
        # 2026-06-12 00:18:30 修改：读取同步模块；作用：直接测试生产配置转换函数；理由：外部转换脚本和 getai 同步都应复用同一逻辑。
        qdrant_sync = conversion.qdrant_sync
        # 2026-06-12 00:18:30 修改：构造默认 dense 配置；作用：模拟当前最容易忘记 --enable-hybrid 的命令行；理由：红测必须覆盖真实漏配根因。
        qdrant_config = qdrant_sync.QdrantSyncConfig(
            # 2026-06-12 00:18:30 修改：使用外部 Qdrant 地址；作用：保持测试语义和隔离服务一致；理由：不触碰主 agent Qdrant。
            url="http://127.0.0.1:6334",
            # 2026-06-12 00:18:30 修改：故意给空 collection；作用：要求 profile 负责补目标 collection；理由：外部库目标应由 profile 决定。
            collection_name="",
            # 2026-06-12 00:18:30 修改：设置距离度量；作用：满足配置对象；理由：该测试不关注距离算法。
            distance="Cosine",
            # 2026-06-12 00:18:30 修改：关闭重建标记；作用：只验证配置转换；理由：不访问真实 Qdrant。
            recreate_collection=False,
            # 2026-06-12 00:18:30 修改：设置批量大小；作用：满足配置对象；理由：该测试不关注写入性能。
            upsert_batch_size=64,
            # 2026-06-12 00:18:30 修改：关闭 dry-run；作用：满足配置对象；理由：该测试不执行写入。
            dry_run=False,
            # 2026-06-12 00:18:30 修改：显式保持 False；作用：证明 profile 能自动启用 hybrid；理由：真实错误就是命令行没开导致 dense-only。
            enable_hybrid=False,
            # 2026-06-12 00:18:30 修改：绑定外部 profile；作用：让 apply 函数读取 external_database.yml；理由：外部库应默认 hybrid 输出。
            source_profile="external_database",
        )
        # 2026-06-12 00:18:30 修改：加载外部 profile；作用：提供 qdrant.vector_mode 和模型配置；理由：Qdrant 输出形态必须配置化。
        profile = qdrant_sync.qdrant_mapping_profile.load_source_profile("external_database")
        # 2026-06-12 00:18:30 修改：应用 profile 到 Qdrant 配置；作用：把字段策略和向量库结构绑定；理由：避免 Qdrant 写入层忘记 hybrid。
        applied_config = qdrant_sync.apply_source_profile_to_qdrant_config(qdrant_config, profile)
        # 2026-06-12 00:18:30 修改：断言目标 collection 来自 profile；作用：外部库不会写进主 collection；理由：保护原 agent 链路。
        self.assertEqual(applied_config.collection_name, "sql_External_database")
        # 2026-06-12 00:18:30 修改：断言自动启用 hybrid；作用：新 collection 会创建 text-dense + text-sparse-new；理由：修复 LlamaIndex hybrid 查询报错。
        self.assertTrue(applied_config.enable_hybrid)
        # 2026-06-12 00:18:30 修改：断言 dense 名；作用：匹配外部 QdrantVectorStore；理由：全量参数启动时能找到 dense vector。
        self.assertEqual(applied_config.dense_vector_name, qdrant_sync.LLAMAINDEX_DEFAULT_DENSE_VECTOR_NAME)
        # 2026-06-12 00:18:30 修改：断言 sparse 名；作用：匹配外部 QdrantVectorStore；理由：全量参数启动时能找到 text-sparse-new。
        self.assertEqual(applied_config.sparse_vector_name, qdrant_sync.LLAMAINDEX_DEFAULT_SPARSE_VECTOR_NAME)
        # 2026-06-12 00:18:30 修改：断言 BM25 模型；作用：和 fastembed_sparse_model="Qdrant/bm25" 对齐；理由：稀疏向量模型名必须可审计。
        self.assertEqual(applied_config.fastembed_sparse_model, qdrant_sync.LLAMAINDEX_BM25_FASTEMBED_SPARSE_MODEL)

    # 2026-06-10 18:01:50 修改：测试 External_database 默认隔离库名和 collection，理由是不能与 getai 冲突。
    def test_external_database_defaults_to_isolated_database_and_collection(self) -> None:
        # 2026-06-10 18:01:50 修改：解析空参数，作用是验证脚本默认值就是模拟外部库。
        args = conversion.parse_args([])
        # 2026-06-10 18:01:50 修改：断言外部数据库默认名，理由是用户指定新库名必须固定。
        self.assertEqual(args.sql_database, "External_database")
        # 2026-06-10 18:01:50 修改：断言外部 Qdrant collection 默认名，理由是不能写回现有 collection。
        self.assertEqual(args.collection, "sql_External_database")
        # 2026-06-10 18:01:50 修改：断言 adapter 常量同步，作用是避免 CLI 与 adapter 名称漂移。
        self.assertEqual(external_database_adapter.EXTERNAL_DATABASE_NAME, "External_database")
        # 2026-06-10 18:01:50 修改：断言 Qdrant collection 常量同步，作用是明确外部向量库目标。
        self.assertEqual(external_database_adapter.EXTERNAL_QDRANT_COLLECTION, "sql_External_database")
        # 2026-06-11 08:23:49 修改：断言外部库默认不启用 hybrid。理由：保护当前 agent dense collection 逻辑。
        self.assertFalse(args.enable_hybrid)
        # 2026-06-11 08:23:49 修改：断言外部库 dense 向量名默认匹配 LlamaIndex。理由：显式 hybrid 时无需另配。
        self.assertEqual(args.dense_vector_name, conversion.qdrant_sync.LLAMAINDEX_DEFAULT_DENSE_VECTOR_NAME)
        # 2026-06-11 08:23:49 修改：断言外部库 sparse 向量名默认匹配 LlamaIndex。理由：显式 hybrid 时无需另配。
        self.assertEqual(args.sparse_vector_name, conversion.qdrant_sync.LLAMAINDEX_DEFAULT_SPARSE_VECTOR_NAME)

    # 2026-06-10 18:01:50 修改：测试外部库建表种子数据和 CanonicalChunk 转换，理由是第三准信点不能另拉链路。
    def test_external_database_adapter_builds_schema_seed_rows_and_canonical_chunks(self) -> None:
        # 2026-06-10 18:01:50 修改：生成建库建表脚本，作用是验证字段与截图一致。
        schema_sql = external_database_adapter.build_external_database_schema_sql()
        # 2026-06-10 18:01:50 修改：断言建库名，理由是必须创建 External_database。
        self.assertIn("CREATE DATABASE [External_database]", schema_sql)
        # 2026-06-12 14:40:11 修改：断言新增普通序号字段 id，作用：确保关系型 External_database 表结构先满足用户要求；理由：后续向量化要读取 standard_question + id。
        self.assertIn("[id] INT NOT NULL", schema_sql)
        # 2026-06-10 18:01:50 修改：断言问题字段，作用是覆盖截图字段。
        self.assertIn("[question] NVARCHAR(MAX) NOT NULL", schema_sql)
        # 2026-06-10 18:01:50 修改：断言场景字段，作用是覆盖截图字段。
        self.assertIn("[question_scene] NVARCHAR(MAX) NOT NULL", schema_sql)
        # 2026-06-10 18:01:50 修改：断言答案字段，作用是覆盖截图字段。
        self.assertIn("[answer] NVARCHAR(MAX) NOT NULL", schema_sql)
        # 2026-06-10 18:01:50 修改：断言标准问题字段，作用是覆盖截图字段。
        self.assertIn("[standard_question] NVARCHAR(MAX) NOT NULL", schema_sql)
        # 2026-06-10 18:01:50 修改：断言完整度字段，作用是覆盖截图字段。
        self.assertIn("[answer_completeness] NVARCHAR(50) NOT NULL", schema_sql)
        # 2026-06-10 18:01:50 修改：断言客户证据字段，作用是覆盖截图 evidence.customer_text。
        self.assertIn("[customer_text] NVARCHAR(MAX) NOT NULL", schema_sql)
        # 2026-06-10 18:01:50 修改：断言客服证据字段，作用是覆盖截图 evidence.service_text。
        self.assertIn("[service_text] NVARCHAR(MAX) NOT NULL", schema_sql)
        # 2026-06-10 18:01:50 修改：断言种子数据三条，理由是用户要求生成三条数据。
        self.assertEqual(schema_sql.count("INSERT INTO [dbo].[external_qa_samples]"), 3)
        # 2026-06-12 14:40:11 修改：断言 INSERT 显式写入 id 字段，作用：保证三条样例序号不是运行时猜测；理由：关系型库必须真实存储 id。
        self.assertIn("([id], [external_id], [question]", schema_sql)
        # 2026-06-12 14:40:11 修改：断言样例 id 是 1/2/3，作用：固定三条序号值；理由：用户要求给三条 id 数据配上序号值。
        self.assertEqual([row.get("id") for row in external_database_adapter.EXTERNAL_SAMPLE_ROWS], [1, 2, 3])
        # 2026-06-10 18:01:50 修改：把 adapter 样例行转成 CanonicalChunk，作用是复用现有 Qdrant 同步链路。
        chunks = external_database_adapter.external_rows_to_canonical_chunks(external_database_adapter.EXTERNAL_SAMPLE_ROWS)
        # 2026-06-10 18:01:50 修改：断言三条样例转换成功，理由是截图四就是三条数据。
        self.assertEqual(len(chunks), 3)
        # 2026-06-10 18:01:50 修改：断言转换类型是现有 CanonicalChunk，作用是不新拉 Qdrant 写入逻辑。
        self.assertIsInstance(chunks[0], conversion.qdrant_sync.CanonicalChunk)
        # 2026-06-10 18:01:50 修改：断言第一条问题映射正确，作用是验证截图字段进入检索文本。
        self.assertEqual(chunks[0].question, "二次工艺流程不对，是后补的，不是发出去的时候做")
        # 2026-06-10 18:01:50 修改：断言标准问题映射到 canonical_question，作用是统一现有 RAG 契约。
        self.assertEqual(chunks[0].canonical_question, "二次工艺的正确操作流程是什么？")
        # 2026-06-12 14:40:11 修改：断言第一条向量文本包含 standard_question 和 id，作用：覆盖从 adapter 到 CanonicalChunk 的完整路径；理由：不能只改 YAML 而真实转换不生效。
        self.assertEqual(conversion.qdrant_sync.build_embedding_text(chunks[0]), "二次工艺的正确操作流程是什么？\n1")
        # 2026-06-10 18:01:50 修改：断言所有 chunk 标记可入 Qdrant，理由是后续 validate_chunks_before_qdrant 必须通过。
        self.assertTrue(all(chunk.qdrant_ready for chunk in chunks))


# 2026-06-10 18:01:50 修改：允许直接运行当前测试文件，作用是本地快速验证新增契约。
if __name__ == "__main__":
    # 2026-06-10 18:01:50 修改：调用 unittest 主入口，理由是沿用仓库现有测试风格。
    unittest.main()
