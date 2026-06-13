# -*- coding: utf-8 -*-
"""验证数据源 mapping profile 能统一管理 getai 和外部库转 Qdrant 的字段策略。"""

# 2026-06-11 15:54:56 修改：导入 sys，作用：把 data_cleaning 加入模块搜索路径；理由：测试要直接调用现有 Qdrant 同步层。
import sys
# 2026-06-11 15:54:56 修改：导入 Path，作用：稳定定位测试目录；理由：Windows 直接运行单测时相对路径不可靠。
from pathlib import Path
# 2026-06-11 15:54:56 修改：导入 unittest，作用：沿用项目现有单测风格；理由：不引入新的测试框架。
import unittest

# 2026-06-11 15:54:56 修改：定位当前测试文件目录，作用：推导 data_cleaning 目录；理由：避免依赖调用方工作目录。
CURRENT_DIR = Path(__file__).resolve().parent
# 2026-06-11 15:54:56 修改：定位 data_cleaning 目录，作用：导入 Qdrant 和 integration 包；理由：新功能必须落在 data_cleaning 内。
DATA_CLEANING_DIR = CURRENT_DIR.parent
# 2026-06-11 15:54:56 修改：判断 data_cleaning 是否已在 sys.path，作用：避免重复污染模块搜索路径；理由：保持测试环境干净。
if str(DATA_CLEANING_DIR) not in sys.path:
    # 2026-06-11 15:54:56 修改：插入 data_cleaning 路径，作用：优先读取当前工作区代码；理由：验证本次修改而不是安装包。
    sys.path.insert(0, str(DATA_CLEANING_DIR))

# 2026-06-11 15:54:56 修改：导入 Qdrant 同步模块，作用：复用生产 CanonicalChunk 和 payload 构造函数；理由：测试不能复制生产逻辑。
from Qdrant import qdrant_sqlserver_sync as qdrant_sync
# 2026-06-11 15:54:56 修改：导入待实现 mapping profile 模块，作用：驱动红测；理由：先证明当前缺少动态字段策略。
from Qdrant import qdrant_mapping_profile
# 2026-06-11 15:54:56 修改：导入外部库 adapter，作用：复用截图要求的三条样例；理由：测试要覆盖真实 External_database 字段。
from integration import external_database_adapter


# 2026-06-11 15:54:56 修改：定义测试类，作用：集中验证 profile 对外部库和 getai 的兼容性；理由：防止后续改动破坏主 agent 链路。
class QdrantMappingProfileTest(unittest.TestCase):
    # 2026-06-11 15:54:56 修改：封装 embedding 配置，作用：给 build_qdrant_payload 提供必需参数；理由：单测不访问真实 embedding 服务。
    def build_embedding_config(self) -> qdrant_sync.EmbeddingConfig:
        # 2026-06-11 15:54:56 修改：返回假 embedding 配置，作用：只验证 payload 结构；理由：字段映射不需要网络请求。
        return qdrant_sync.EmbeddingConfig(
            # 2026-06-11 15:54:56 修改：设置假 API 地址，作用：满足 dataclass 参数；理由：测试不实际调用。
            api_base="http://embedding.local/v1",
            # 2026-06-11 15:54:56 修改：设置假 API key，作用：满足 dataclass 参数；理由：避免依赖真实密钥。
            api_key="fake-key",
            # 2026-06-11 15:54:56 修改：设置模型名，作用：进入 payload 元数据；理由：验证字段映射不关心真实模型。
            model="fake-embedding-model",
            # 2026-06-11 15:54:56 修改：设置向量维度，作用：满足配置对象；理由：不影响本测试断言。
            dimension=2,
            # 2026-06-11 15:54:56 修改：设置批大小，作用：满足配置对象；理由：不影响本测试断言。
            batch_size=2,
        )

    # 2026-06-12 14:40:11 修改：验证外部库 profile 只用 standard_question 加普通序号 id 向量化；理由：用户要求新 id 参与召回但不混入 QA 答案字段。
    def test_external_profile_uses_standard_question_as_embedding_text_without_answer_noise(self) -> None:
        # 2026-06-11 15:54:56 修改：加载外部库 profile，作用：读取 external_database.yml 的字段策略；理由：字段选择必须配置化。
        profile = qdrant_mapping_profile.load_source_profile("external_database")
        # 2026-06-11 15:54:56 修改：读取第一条外部样例，作用：覆盖截图里的 standard_question 字段；理由：这是用户指定的泛化场景。
        row = external_database_adapter.EXTERNAL_SAMPLE_ROWS[0]
        # 2026-06-11 15:54:56 修改：按 profile 转 CanonicalChunk，作用：复用现有 Qdrant 写入链路；理由：不能新增分叉链路。
        chunk = qdrant_mapping_profile.row_to_canonical_chunk(row, profile, qdrant_sync)
        # 2026-06-11 15:54:56 修改：构造向量化文本，作用：验证 build_embedding_text 优先使用 profile 结果；理由：避免 answer/evidence 噪声进入向量。
        embedding_text = qdrant_sync.build_embedding_text(chunk)
        # 2026-06-12 14:40:11 修改：构造期望向量文本，作用：锁定 standard_question + id 的字段顺序；理由：新 id 只是普通序号但必须参与向量化。
        expected_embedding_text = f"{row['standard_question']}\n{row.get('id', '<missing-id>')}"
        # 2026-06-12 14:40:11 修改：断言向量化文本等于标准问题加 id，作用：锁定外部库动态策略；理由：不能再强制拼接 QA/evidence。
        self.assertEqual(embedding_text, expected_embedding_text)
        # 2026-06-11 15:54:56 修改：断言向量化文本不包含答案，作用：证明外部库可只按指定字段召回；理由：避免多字段带偏召回方向。
        self.assertNotIn(row["answer"], embedding_text)
        # 2026-06-11 15:54:56 修改：构造 Qdrant payload，作用：验证 prompt_text 与 payload 仍完整；理由：只改召回字段不丢业务字段。
        payload = qdrant_sync.build_qdrant_payload(chunk, self.build_embedding_config())
        # 2026-06-11 15:54:56 修改：断言 payload 嵌套保留原字段，作用：支持回表、展示和调试；理由：业务字段不应被固定模板吞掉。
        self.assertEqual(payload["payload"]["customer_text"], row["customer_text"])
        # 2026-06-12 14:40:11 修改：断言 payload 嵌套保留普通序号 id，作用：支持 WebUI/回表时看到用户新增序号；理由：id 参与向量化也必须作为业务字段打包。
        self.assertEqual(payload["payload"].get("id"), row.get("id"))
        # 2026-06-12 15:30:17 修改：定义外部库 YAML 渲染 payload 允许的顶层字段，作用：只保留向量文本和打包 payload；理由：用户要求 sql_External_database 不再混入 doc_id/text/source_* 等固定字段。
        allowed_top_level_keys = {"retrieval_text", "payload"}
        # 2026-06-12 15:30:17 修改：断言顶层字段完全来自 qdrant_payload.top_level/objects 声明，作用：证明新增外部库只需改 YAML；理由：不能每种外部库都加 Python if 分支。
        self.assertEqual(set(payload), allowed_top_level_keys)
        # 2026-06-12 15:30:17 修改：断言 YAML 顶层 retrieval_text 来自 embedding_text，作用：让截图中的向量化字段可见；理由：标准问题加 id 是当前库的唯一向量正文。
        self.assertEqual(payload["retrieval_text"], expected_embedding_text)
        # 2026-06-12 15:30:17 修改：列出必须排除的历史/兼容顶层字段，作用：把截图中没用字段固定成回归保护；理由：sql_External_database 要与 getai 主库字段隔离。
        forbidden_top_level_keys = {"doc_id", "text", "source_name", "source_table", "source_pk", "keyword_terms", "mapping_profile_name"}
        # 2026-06-12 15:30:17 修改：断言禁止字段不存在，作用：防止通用渲染器继续自动补旧字段；理由：外部库最终结构必须完全受 YAML 控制。
        self.assertTrue(forbidden_top_level_keys.isdisjoint(payload))
        # 2026-06-11 15:54:56 修改：执行同步前校验，作用：证明 generic profile 不要求 embedding_text 包含答案；理由：外部库召回字段可能只有问题。
        validation = qdrant_sync.validate_chunks_before_qdrant([chunk])
        # 2026-06-11 15:54:56 修改：断言校验通过，作用：锁定外部泛化契约；理由：避免旧 QA 校验误伤外部库。
        self.assertEqual(validation["error_count"], 0)

    # 2026-06-11 15:54:56 修改：验证 getai profile 保持原 QA 消费契约；理由：主 agent 完美问答链路不能受外部泛化影响。
    def test_getai_profile_preserves_existing_qa_embedding_and_prompt_text(self) -> None:
        # 2026-06-11 15:54:56 修改：定义答案，作用：验证 QA 契约仍要求答案进入 prompt 和 retrieval_text；理由：保护现有问答精度。
        answer = "可以先让财务反审，再让预付款状态退回。"
        # 2026-06-11 15:54:56 修改：构造现有 getai 风格 chunk，作用：模拟已清洗入库后的 QA 数据；理由：不依赖真实 SQL Server。
        chunk = qdrant_sync.CanonicalChunk(
            # 2026-06-11 15:54:56 修改：设置 chunk_id，作用：生成稳定 point id；理由：生产对象必填。
            chunk_id="qachunk_profile_1",
            # 2026-06-11 15:54:56 修改：设置 document_id，作用：兼容 LlamaIndex doc_id；理由：现有 RAG 依赖文档过滤。
            document_id="qadoc_profile",
            # 2026-06-11 15:54:56 修改：设置音频编号，作用：满足 CanonicalChunk 字段；理由：保持生产对象完整。
            audio_no=1,
            # 2026-06-11 15:54:56 修改：设置音频标题，作用：保留来源展示字段；理由：现有 payload 需要该字段。
            audio_title="profile.m4a",
            # 2026-06-11 15:54:56 修改：设置 chunk 顺序，作用：保持排序字段；理由：现有回表逻辑需要。
            chunk_index=1,
            # 2026-06-11 15:54:56 修改：设置业务场景，作用：生成关键词；理由：现有检索过滤依赖 scene。
            scene="财务反审",
            # 2026-06-11 15:54:56 修改：设置问题，作用：构造 QA 契约；理由：现有 RAG 以问题召回。
            question="入账单为什么要反审？",
            # 2026-06-11 15:54:56 修改：设置答案，作用：构造 QA 契约；理由：现有校验要求答案完整。
            answer=answer,
            # 2026-06-11 15:54:56 修改：设置清洗文本，作用：保留旧字段；理由：现有 payload 仍要输出。
            cleaned_text=f"问题：入账单为什么要反审？\n答案：{answer}",
            # 2026-06-11 15:54:56 修改：设置处理步骤，作用：保留旧字段；理由：现有 payload 仍要输出。
            resolution_steps="[]",
            # 2026-06-11 15:54:56 修改：设置关键词，作用：生成 keyword_terms；理由：兼容关键词过滤。
            keywords='["财务反审"]',
            # 2026-06-11 15:54:56 修改：设置实体 JSON，作用：保留旧字段；理由：兼容现有 payload。
            entities_json="{}",
            # 2026-06-11 15:54:56 修改：设置来源摘录，作用：保留证据字段；理由：现有校验需要答案可见。
            source_excerpt=f"答案：{answer}",
            # 2026-06-11 15:54:56 修改：设置内容 hash，作用：满足同步状态字段；理由：生产对象必填。
            content_hash="hash-profile",
            # 2026-06-11 15:54:56 修改：设置 QA pair id，作用：满足同步状态字段；理由：生产对象必填。
            qa_pair_id="pair-profile",
            # 2026-06-11 15:54:56 修改：设置 QA pair 序号，作用：满足同步状态字段；理由：生产对象必填。
            qa_pair_index=1,
            # 2026-06-11 15:54:56 修改：设置相似度分数，作用：保留质量字段；理由：现有 payload 仍要输出。
            qa_similarity_score=0.95,
            # 2026-06-11 15:54:56 修改：设置相似度阈值，作用：保留质量字段；理由：现有 payload 仍要输出。
            qa_similarity_threshold=0.08,
            # 2026-06-11 15:54:56 修改：设置 QA 已校验，作用：保持可入库状态；理由：现有同步只消费通过校验数据。
            qa_pair_validated=True,
            # 2026-06-11 15:54:56 修改：设置聚类 ID，作用：保留过滤字段；理由：现有 payload 仍要输出。
            cluster_id="cluster-profile",
            # 2026-06-11 15:54:56 修改：设置聚类标签，作用：保留过滤字段；理由：现有 payload 仍要输出。
            cluster_label="财务反审",
            # 2026-06-11 15:54:56 修改：设置聚类层级，作用：保留过滤字段；理由：现有 payload 仍要输出。
            cluster_level="scene",
            # 2026-06-11 15:54:56 修改：设置聚类路径，作用：保留过滤字段；理由：现有 payload 仍要输出。
            cluster_path="[]",
            # 2026-06-11 15:54:56 修改：设置全局聚类 ID，作用：保留过滤字段；理由：现有 payload 仍要输出。
            global_cluster_id="global-profile",
            # 2026-06-11 15:54:56 修改：设置全局聚类标签，作用：保留过滤字段；理由：现有 payload 仍要输出。
            global_cluster_label="财务",
            # 2026-06-11 15:54:56 修改：设置全局聚类层级，作用：保留过滤字段；理由：现有 payload 仍要输出。
            global_cluster_level="global",
            # 2026-06-11 15:54:56 修改：设置全局聚类路径，作用：保留过滤字段；理由：现有 payload 仍要输出。
            global_cluster_path="[]",
            # 2026-06-11 15:54:56 修改：设置问题 hash，作用：保留去重字段；理由：现有 payload 仍要输出。
            question_hash="question-hash-profile",
            # 2026-06-11 15:54:56 修改：设置答案 hash，作用：保留去重字段；理由：现有 payload 仍要输出。
            answer_hash="answer-hash-profile",
            # 2026-06-11 15:54:56 修改：设置 canonical id，作用：保留融合字段；理由：现有 payload 仍要输出。
            canonical_chunk_id="qachunk_profile_1",
            # 2026-06-11 15:54:56 修改：设置融合状态，作用：保持 canonical 可入 Qdrant；理由：现有同步过滤依赖。
            fusion_status="canonical",
            # 2026-06-11 15:54:56 修改：设置 payload 版本，作用：保留契约字段；理由：现有 payload 仍要输出。
            payload_schema_version="qa-rag-payload-v3",
            # 2026-06-11 15:54:56 修改：设置空 payload_json，作用：验证 profile 能补齐字段；理由：兼容旧行。
            payload_json={},
            # 2026-06-11 15:54:56 修改：设置 RAG 契约版本，作用：保持 QA 严格校验；理由：保护主 agent 链路。
            rag_contract_version="qa-rag-contract-v1",
            # 2026-06-11 15:54:56 修改：设置规范问题，作用：保留 QA 字段；理由：现有 payload 仍要输出。
            canonical_question="入账单反审怎么处理？",
            # 2026-06-11 15:54:56 修改：设置答案优先字段，作用：驱动 prompt_text；理由：现有问答精度依赖完整答案。
            answer_text=answer,
            # 2026-06-11 15:54:56 修改：设置别名，作用：驱动 keyword_terms；理由：兼容关键词过滤。
            query_aliases=["入账单反审怎么处理？"],
            # 2026-06-11 15:54:56 修改：设置完整来源，作用：通过 QA 校验；理由：现有同步校验要求答案可见。
            source_excerpt_full=f"答案：{answer}",
            # 2026-06-11 15:54:56 修改：设置 LLM 文本，作用：验证 profile 不改变原 prompt 正文；理由：主 agent prompt 不能受影响。
            llm_text=f"问题：入账单反审怎么处理？\n答案：{answer}",
            # 2026-06-11 15:54:56 修改：设置检索文本，作用：验证 profile 不改变原向量文本；理由：主 agent 召回不能受影响。
            retrieval_text=f"问题：入账单反审怎么处理？\n答案：{answer}",
            # 2026-06-11 15:54:56 修改：设置重复上下文，作用：满足生产对象字段；理由：本测试不覆盖重复融合。
            duplicate_contexts=[],
            # 2026-06-11 15:54:56 修改：设置重复 chunk id，作用：满足生产对象字段；理由：本测试不覆盖重复融合。
            merged_duplicate_chunk_ids=[],
            # 2026-06-11 15:54:56 修改：设置可同步，作用：通过校验；理由：现有同步只入可同步数据。
            qdrant_ready=True,
            # 2026-06-11 15:54:56 修改：设置校验标记，作用：满足生产对象字段；理由：本测试不覆盖错误标记。
            validation_flags=[],
        )
        # 2026-06-11 15:54:56 修改：加载 getai profile，作用：验证现有库也纳入 profile 管理；理由：用户要求不是只管外部库。
        profile = qdrant_mapping_profile.load_source_profile("getai_rag_qa_chunks")
        # 2026-06-11 15:54:56 修改：对 getai chunk 应用 profile，作用：走统一字段解释器；理由：写入链路不分叉。
        profiled_chunk = qdrant_mapping_profile.apply_profile_to_chunk(chunk, profile)
        # 2026-06-11 15:54:56 修改：断言向量化文本不变，作用：保护现有 RAG 召回；理由：主 agent collection 不能被外部策略污染。
        self.assertEqual(qdrant_sync.build_embedding_text(profiled_chunk), chunk.retrieval_text)
        # 2026-06-11 15:54:56 修改：断言 prompt 文本不变，作用：保护现有问答精准度；理由：主 agent prompt 消费不应变化。
        self.assertEqual(qdrant_sync.build_answer_first_text(profiled_chunk), chunk.llm_text)
        # 2026-06-11 15:54:56 修改：执行 QA 校验，作用：确认 getai 仍走严格答案完整性校验；理由：外部泛化不能放松主库质量门槛。
        validation = qdrant_sync.validate_chunks_before_qdrant([profiled_chunk])
        # 2026-06-11 15:54:56 修改：断言校验通过，作用：证明 profile 化不破坏现有 QA 契约；理由：保护完美问答链路。
        self.assertEqual(validation["error_count"], 0)

    # 2026-06-12 15:30:17 修改：验证 payload index 能读取 qdrant_payload 布局；作用：索引字段也由 YAML 控制；理由：外部库不能继承 getai 或 strict 固定索引。
    def test_create_payload_indexes_reads_rendered_layout_indexes_from_profile(self) -> None:
        # 2026-06-11 15:54:56 修改：定义假 Qdrant client，作用：捕获 create_payload_index 调用；理由：单测不启动真实 Qdrant。
        class FakePayloadIndexClient:
            # 2026-06-11 15:54:56 修改：初始化调用记录，作用：后续断言字段名；理由：验证动态 index 逻辑。
            def __init__(self) -> None:
                # 2026-06-11 15:54:56 修改：保存索引调用，作用：检查字段和 schema；理由：不依赖 Qdrant 服务。
                self.calls: list[tuple[str, str, object]] = []

            # 2026-06-11 15:54:56 修改：模拟 Qdrant create_payload_index，作用：记录参数；理由：隔离外部服务。
            def create_payload_index(self, collection_name: str, field_name: str, field_schema: object) -> None:
                # 2026-06-11 15:54:56 修改：追加调用记录，作用：供断言使用；理由：验证 profile 字段进入 index。
                self.calls.append((collection_name, field_name, field_schema))

        # 2026-06-11 15:54:56 修改：加载外部库 profile，作用：读取 keyword_index.fields；理由：动态 index 来源应是配置。
        profile = qdrant_mapping_profile.load_source_profile("external_database")
        # 2026-06-11 15:54:56 修改：创建假 client，作用：执行生产索引函数；理由：不访问真实 Qdrant。
        client = FakePayloadIndexClient()
        # 2026-06-11 15:54:56 修改：调用生产索引函数，作用：验证新增参数兼容 profile；理由：不能为外部库单独写索引链路。
        qdrant_sync.create_payload_indexes(client, "sql_External_database", profile)
        # 2026-06-11 15:54:56 修改：抽取字段名集合，作用：简化断言；理由：索引 schema 类型不是本测试重点。
        indexed_fields = {field_name for _, field_name, _ in client.calls}
        # 2026-06-12 15:30:17 修改：断言只给 YAML 声明的 retrieval_text 建全文索引，作用：保持当前 sql_External_database collection 干净；理由：截图要求不再出现无用顶层字段。
        self.assertEqual(indexed_fields, {"retrieval_text"})
        # 2026-06-12 15:30:17 修改：断言 doc_id 不建索引，作用：证明当前外部库没有继承 LlamaIndex 固定字段；理由：是否保留 doc_id 应由未来外部库 YAML 自己声明。
        self.assertNotIn("doc_id", indexed_fields)
        # 2026-06-12 15:30:17 修改：断言 source_pk 不建索引，作用：防止 strict 模式固定来源字段残留；理由：当前 YAML 没声明就不能出现在 collection。
        self.assertNotIn("source_pk", indexed_fields)
        # 2026-06-12 15:30:17 修改：断言 keyword_terms 不建索引，作用：防止旧 QA 关键词字段污染外部库；理由：qdrant_payload.indexes.keyword 当前为空。
        self.assertNotIn("keyword_terms", indexed_fields)
        # 2026-06-12 14:40:11 修改：断言旧 QA 索引不进入外部库，作用：防止 sql_External_database 出现 getai 专用索引；理由：用户要求新外部向量库字段隔离。
        self.assertNotIn("cluster_id", indexed_fields)

    # 2026-06-12 15:30:17 修改：验证 Qdrant 自检支持 YAML 渲染外部 payload；作用：避免转换摘要误把缺少 doc_id/source_pk/text 当成失败；理由：profile_rendered 的验收也必须跟随 YAML。
    def test_verify_qdrant_collection_accepts_profile_rendered_payload_contract(self) -> None:
        # 2026-06-12 15:30:17 修改：加载外部库 profile；作用：生成 YAML 渲染 payload 样例；理由：测试要覆盖真实 external_database.yml。
        profile = qdrant_mapping_profile.load_source_profile("external_database")
        # 2026-06-12 14:40:11 修改：读取第一条外部样例；作用：构造可命中的 point payload；理由：自检必须使用真实字段组合。
        row = external_database_adapter.EXTERNAL_SAMPLE_ROWS[0]
        # 2026-06-12 14:40:11 修改：生成 CanonicalChunk；作用：复用生产 profile 映射；理由：不在测试里复制转换逻辑。
        chunk = qdrant_mapping_profile.row_to_canonical_chunk(row, profile, qdrant_sync)
        # 2026-06-12 15:30:17 修改：构造 YAML 渲染 Qdrant payload；作用：模拟真实写入后的第一条命中；理由：verify 只消费 payload 结构。
        payload = qdrant_sync.build_qdrant_payload(chunk, self.build_embedding_config())

        # 2026-06-12 14:40:11 修改：定义 fake count 结果；作用：隔离真实 Qdrant 服务；理由：单测只验证自检口径。
        class FakeCountResult:
            # 2026-06-12 14:40:11 修改：保存 point 数；作用：模拟 Qdrant count 返回值；理由：verify 需要读取 count 属性。
            count = 3

        # 2026-06-12 15:30:17 修改：定义 fake 命中点；作用：携带 YAML 渲染 payload；理由：query_points 返回 points 列表。
        class FakePoint:
            # 2026-06-12 14:40:11 修改：初始化 payload；作用：让 verify 读取第一条命中；理由：无需真实 PointStruct。
            def __init__(self, point_payload: dict[str, object]) -> None:
                # 2026-06-12 14:40:11 修改：保存 payload；作用：模拟 Qdrant ScoredPoint.payload；理由：verify 只关心 payload。
                self.payload = point_payload

        # 2026-06-12 14:40:11 修改：定义 fake 查询结果；作用：返回一条命中；理由：验证 first_hit 字段。
        class FakeQueryResult:
            # 2026-06-12 14:40:11 修改：初始化 points；作用：模拟 Qdrant query_points 结果；理由：生产函数读取 points[0]。
            def __init__(self, point_payload: dict[str, object]) -> None:
                # 2026-06-12 14:40:11 修改：保存命中列表；作用：提供严格 payload point；理由：验证 contract_ready。
                self.points = [FakePoint(point_payload)]

        # 2026-06-12 14:40:11 修改：定义 fake Qdrant client；作用：让 verify_qdrant_collection 可运行；理由：单测不访问 6334 服务。
        class FakeVerifyClient:
            # 2026-06-12 14:40:11 修改：实现 count；作用：模拟 collection 点数统计；理由：verify 需要先统计 point_count。
            def count(self, **_: object) -> FakeCountResult:
                # 2026-06-12 14:40:11 修改：返回固定计数；作用：证明自检读取 count；理由：测试重点不是 Qdrant API。
                return FakeCountResult()

            # 2026-06-12 15:30:17 修改：实现 query_points；作用：返回 YAML 渲染 payload 命中；理由：verify 需要检查第一条 payload。
            def query_points(self, **_: object) -> FakeQueryResult:
                # 2026-06-12 15:30:17 修改：返回 fake 查询结果；作用：驱动 profile_rendered payload ready 判断；理由：无需真实向量检索。
                return FakeQueryResult(payload)

        # 2026-06-12 14:40:11 修改：构造 hybrid Qdrant 配置；作用：覆盖 using=text-dense 的自检路径；理由：External_database 默认 hybrid。
        config = qdrant_sync.QdrantSyncConfig(
            url="http://127.0.0.1:6334",
            collection_name="sql_External_database",
            distance="Cosine",
            recreate_collection=False,
            upsert_batch_size=1,
            dry_run=False,
            enable_hybrid=True,
            source_profile="external_database",
        )
        # 2026-06-12 15:30:17 修改：执行生产自检函数；作用：验证 profile_rendered payload 不被旧 QA/strict ready 规则误判；理由：转换摘要必须可信。
        verify = qdrant_sync.verify_qdrant_collection(FakeVerifyClient(), config, [0.1, 0.2])
        # 2026-06-12 15:30:17 修改：断言命中 ready；作用：证明 YAML 声明字段满足自检；理由：不能因为没有 doc_id/source_pk/text 顶层字段误报失败。
        self.assertTrue(verify["first_hit_contract_ready"])
        # 2026-06-12 15:30:17 修改：断言来源主键不再作为固定顶层摘要字段，作用：证明自检不依赖 source_pk；理由：当前 YAML 没声明 source_pk 顶层字段。
        self.assertEqual(verify["first_hit_source_pk"], "")
        # 2026-06-12 15:30:17 修改：断言向量文本进入自检摘要；作用：直接证明 standard_question + id 写入 Qdrant；理由：用户要求测试到向量化字段。
        self.assertEqual(verify["first_hit_retrieval_text"], "二次工艺的正确操作流程是什么？\n1")
        # 2026-06-12 15:30:17 修改：断言契约版本来自 YAML 渲染模式，作用：摘要可区分当前通用渲染器；理由：以后多外部库排查要看到实际 payload 模式。
        self.assertEqual(verify["first_hit_contract_version"], "profile_rendered")

    # 2026-06-12 00:18:30 修改：验证外部库 profile 明确声明 hybrid 和 BM25；作用：防止 External_database 落库仍是 dense-only；理由：别人用 QdrantVectorStore(enable_hybrid=True, fastembed_sparse_model="Qdrant/bm25") 时必须能消费。
    def test_external_profile_declares_llamaindex_hybrid_bm25_qdrant_contract(self) -> None:
        # 2026-06-12 00:18:30 修改：加载外部库 profile；作用：读取 qdrant 输出形态；理由：hybrid 不能再靠命令行临时记忆。
        profile = qdrant_mapping_profile.load_source_profile("external_database")
        # 2026-06-12 00:18:30 修改：断言外部库启用 hybrid；作用：确保 collection 创建时有 dense+sparse schema；理由：修复 text-sparse-new 不存在的根因。
        self.assertEqual(profile.qdrant_vector_mode, "hybrid")
        # 2026-06-12 00:18:30 修改：断言 dense 名称；作用：匹配 LlamaIndex QdrantVectorStore 默认 dense_vector_name；理由：别人全量参数启动时不会找错 dense 向量。
        self.assertEqual(profile.qdrant_dense_vector_name, qdrant_sync.LLAMAINDEX_DEFAULT_DENSE_VECTOR_NAME)
        # 2026-06-12 00:18:30 修改：断言 sparse 名称；作用：匹配 LlamaIndex QdrantVectorStore 默认 sparse_vector_name；理由：修复 text-sparse-new 查不到的问题。
        self.assertEqual(profile.qdrant_sparse_vector_name, qdrant_sync.LLAMAINDEX_DEFAULT_SPARSE_VECTOR_NAME)
        # 2026-06-12 00:18:30 修改：断言 sparse 模型；作用：文档侧 BM25 sparse 与查询侧 fastembed_sparse_model="Qdrant/bm25" 保持一致；理由：避免 collection 有 sparse 但模型不一致导致召回偏差。
        self.assertEqual(profile.qdrant_fastembed_sparse_model, qdrant_sync.LLAMAINDEX_BM25_FASTEMBED_SPARSE_MODEL)

    # 2026-06-12 00:18:30 修改：验证 getai hybrid 影子 profile 独立存在；作用：让别人消费 getai 数据时走新 hybrid collection；理由：不能原地改动当前 agent 使用的 sql_rag_qa_chunks_v1。
    def test_getai_hybrid_shadow_profile_targets_separate_bm25_collection(self) -> None:
        # 2026-06-12 00:18:30 修改：加载 getai 影子 profile；作用：确认新增 collection 不覆盖主 collection；理由：保护现有完美问答链路。
        profile = qdrant_mapping_profile.load_source_profile("getai_rag_qa_chunks_hybrid")
        # 2026-06-12 00:18:30 修改：断言影子 collection 名；作用：隔离外部 hybrid 消费；理由：原 sql_rag_qa_chunks_v1 必须保持 dense-only。
        self.assertEqual(profile.target_collection, "sql_rag_qa_chunks_v1_hybrid")
        # 2026-06-12 00:18:30 修改：断言影子 profile 启用 hybrid；作用：生成 text-dense + text-sparse-new；理由：别人 enable_hybrid=True 时不再报错。
        self.assertEqual(profile.qdrant_vector_mode, "hybrid")
        # 2026-06-12 00:18:30 修改：断言影子 profile 使用 BM25；作用：匹配外部 fastembed_sparse_model="Qdrant/bm25"；理由：文档侧和查询侧 sparse 模型必须同源。
        self.assertEqual(profile.qdrant_fastembed_sparse_model, qdrant_sync.LLAMAINDEX_BM25_FASTEMBED_SPARSE_MODEL)

    # 2026-06-12 00:18:30 修改：验证原 getai profile 保持 dense；作用：防止新 hybrid 逻辑误伤主 agent collection；理由：当前完美问答链路依赖旧 collection 结构。
    def test_getai_default_profile_remains_dense_for_current_agent_collection(self) -> None:
        # 2026-06-12 00:18:30 修改：加载原 getai profile；作用：检查默认同步目标；理由：不传 profile 时必须保护旧行为。
        profile = qdrant_mapping_profile.load_source_profile("getai_rag_qa_chunks")
        # 2026-06-12 00:18:30 修改：断言原 collection 不变；作用：确认主 agent 仍消费 sql_rag_qa_chunks_v1；理由：避免牵一发动全身。
        self.assertEqual(profile.target_collection, "sql_rag_qa_chunks_v1")
        # 2026-06-12 00:18:30 修改：断言原 profile 默认 dense；作用：确保不会自动把主 collection 改成命名向量；理由：business_brain_runtime 当前吃的是旧未命名 dense。
        self.assertEqual(profile.qdrant_vector_mode, "dense")


# 2026-06-11 15:54:56 修改：允许直接运行本测试文件，作用：本地快速验证；理由：符合现有 unittest 文件风格。
if __name__ == "__main__":
    # 2026-06-11 15:54:56 修改：启动 unittest 主入口，作用：执行本文件测试；理由：方便独立回归。
    unittest.main()
