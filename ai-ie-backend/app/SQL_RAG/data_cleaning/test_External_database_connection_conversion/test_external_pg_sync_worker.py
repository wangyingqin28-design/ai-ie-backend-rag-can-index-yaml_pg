# -*- coding: utf-8 -*-
"""测试外部 PostgreSQL 实时同步 worker 的 YAML 驱动行为。"""

# 2026-06-13 17:18:04 新增：导入 importlib，作用是用断言方式检查新同步模块；理由是红测要先证明当前缺少通用 worker。
import importlib
# 2026-06-13 17:18:04 新增：导入 sys，作用是把 data_cleaning 放进模块搜索路径；理由是测试直接运行时也要加载本地源码。
import sys
# 2026-06-13 17:18:04 新增：导入 dataclass，作用是构造轻量假对象；理由是 worker 测试不应连接真实 Qdrant。
from dataclasses import dataclass
# 2026-06-13 17:18:04 新增：导入 Path，作用是稳定定位测试目录；理由是 Windows 下不能依赖启动目录。
from pathlib import Path
# 2026-06-13 17:18:04 新增：导入 Any，作用是标注假同步模块的动态参数；理由是测试只关心行为不关心具体 SDK 类型。
from typing import Any
# 2026-06-13 17:18:04 新增：导入 unittest，作用是沿用项目现有单测框架；理由是不额外引入 pytest。
import unittest

# 2026-06-13 17:18:04 新增：定位当前测试目录，作用是推导 data_cleaning 路径；理由是测试可从任意工作目录执行。
CURRENT_DIR = Path(__file__).resolve().parent
# 2026-06-13 17:18:04 新增：定位 data_cleaning 目录，作用是导入 Qdrant 和 integration 包；理由是新同步层位于这里。
DATA_CLEANING_DIR = CURRENT_DIR.parent
# 2026-06-13 17:18:04 新增：判断路径是否已注入，作用是避免重复污染 sys.path；理由是测试集可能多文件并行导入。
if str(DATA_CLEANING_DIR) not in sys.path:
    # 2026-06-13 17:18:04 新增：插入本地源码路径，作用是优先测试当前工作区代码；理由是不能误用已安装旧包。
    sys.path.insert(0, str(DATA_CLEANING_DIR))

# 2026-06-13 17:18:04 新增：导入生产 Qdrant 同步模块，作用是复用 CanonicalChunk 和 payload 构造；理由是测试不能复制核心映射逻辑。
from Qdrant import qdrant_sqlserver_sync as qdrant_sync
# 2026-06-13 17:18:04 新增：导入 profile 解析器，作用是验证 krauss PG YAML；理由是字段策略必须完全配置化。
from Qdrant import qdrant_mapping_profile


# 2026-06-13 17:18:04 新增：定义假 point，作用是模拟 Qdrant point 的最小结构；理由是 worker 只需要确认 upsert 和回写顺序。
@dataclass(frozen=True)
class FakePoint:
    # 2026-06-13 17:18:04 新增：保存 point id，作用是模拟 Qdrant 删除和 upsert 身份；理由是删除同步必须沿用确定性 point id。
    id: str
    # 2026-06-13 17:18:04 新增：保存向量，作用是满足 verify_qdrant_collection 的入参；理由是测试无需真实向量维度。
    vector: list[float]
    # 2026-06-13 17:18:04 新增：保存 payload，作用是断言最终 Qdrant 字段隔离；理由是不能混入其他库字段。
    payload: dict[str, Any]


# 2026-06-13 17:18:04 新增：定义假外部库 adapter，作用是模拟 PG 读取和 ZhuangTai 回写；理由是单测不能依赖别人局域网数据库。
class FakeExternalAdapter:
    # 2026-06-13 17:18:04 新增：初始化假 adapter，作用是注入外部 PG 行；理由是测试要覆盖新增和已删除两类变化。
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        # 2026-06-13 17:18:04 新增：保存待返回行，作用是模拟 SELECT 结果；理由是 worker 应只消费 adapter 抽象。
        self.rows = rows
        # 2026-06-13 17:18:04 新增：保存回写记录，作用是断言每条 point 入库后写回已入库；理由是用户明确要求逐条回写 ZhuangTai。
        self.status_updates: list[tuple[str, str]] = []

    # 2026-06-13 17:18:04 新增：模拟读取外部行，作用是给 worker 提供 PG 数据；理由是 SQL 细节应被 adapter 隔离。
    def fetch_rows(self, profile: Any) -> list[dict[str, Any]]:
        # 2026-06-13 17:18:04 新增：返回注入行，作用是保持测试可预测；理由是同步逻辑不应直接访问数据库。
        return list(self.rows)

    # 2026-06-13 17:18:04 新增：模拟回写状态，作用是记录 ZhuangTai 更新；理由是成功 upsert 后必须回写外部 PG。
    def mark_row_synced(self, profile: Any, source_pk: Any, status_value: str) -> None:
        # 2026-06-13 17:18:04 新增：追加回写调用，作用是断言写回值为已入库；理由是测试不真正修改 PG。
        self.status_updates.append((str(source_pk), status_value))


# 2026-06-13 17:18:04 新增：定义假 Qdrant/embedding 同步模块，作用是隔离网络；理由是 worker 单测只验证节点顺序和字段。
class FakeSyncModule:
    # 2026-06-13 17:18:04 新增：复用真实 CanonicalChunk 类型，作用是让 profile 转换走生产结构；理由是不能另建假 chunk 契约。
    CanonicalChunk = qdrant_sync.CanonicalChunk

    # 2026-06-13 17:18:04 新增：初始化调用记录，作用是断言 worker 行为；理由是同步节点必须可审计。
    def __init__(self) -> None:
        # 2026-06-13 17:18:04 新增：保存调用记录，作用是检查 upsert/delete/embedding；理由是测试要证明没有绕开现有 Qdrant 链路。
        self.calls: list[tuple[Any, ...]] = []
        # 2026-06-13 17:18:04 新增：保存向量化文本，作用是断言只向量化 MiaoShu；理由是其他字段必须只进 payload。
        self.embedding_texts: list[str] = []
        # 2026-06-13 17:18:04 新增：保存 upsert 的 payload，作用是断言顶层字段隔离；理由是不能混入 getai 字段。
        self.upserted_payloads: list[dict[str, Any]] = []

    # 2026-06-13 17:18:04 新增：模拟校验，作用是保持生产流程节点；理由是 worker 不应跳过契约检查。
    def validate_chunks_before_qdrant(self, chunks: list[Any]) -> dict[str, Any]:
        # 2026-06-13 17:18:04 新增：记录校验调用，作用是证明 upsert 前先检查；理由是防止坏数据进入 Qdrant。
        self.calls.append(("validate", len(chunks)))
        # 2026-06-13 17:18:04 新增：返回通过结果，作用是让测试进入后续写入；理由是本测试不覆盖坏数据。
        return {"checked_chunk_count": len(chunks), "error_count": 0}

    # 2026-06-13 17:18:04 新增：模拟 collection 准备，作用是保持现有 Qdrant 节点；理由是 worker 不直接操作低层 schema。
    def ensure_qdrant_collection(self, client: Any, qdrant_config: Any, embedding_config: Any) -> None:
        # 2026-06-13 17:18:04 新增：记录 collection 名称，作用是验证写入独立 collection；理由是不能污染主 QA collection。
        self.calls.append(("ensure", qdrant_config.collection_name))

    # 2026-06-13 17:18:04 新增：模拟 embedding 客户端，作用是避免真实模型请求；理由是单测只验证同步编排。
    def create_embedding_client(self, embedding_config: Any) -> str:
        # 2026-06-13 17:18:04 新增：记录模型名，作用是确认流程到了 embedding 节点；理由是向量化不能被跳过。
        self.calls.append(("embedding_client", embedding_config.model))
        # 2026-06-13 17:18:04 新增：返回假客户端，作用是供 embed_texts 接收；理由是测试不需要真实客户端。
        return "fake-embedding-client"

    # 2026-06-13 17:18:04 新增：复用真实向量文本构造，作用是测试 MiaoShu profile 生效；理由是不能在测试里重写规则。
    def build_embedding_text(self, chunk: Any) -> str:
        # 2026-06-13 17:18:04 新增：调用真实函数，作用是读取 profile 生成的 retrieval_text；理由是验证生产行为。
        text = qdrant_sync.build_embedding_text(chunk)
        # 2026-06-13 17:18:04 新增：保存文本，作用是后续断言只包含 MiaoShu；理由是用户要求只向量化 MiaoShu。
        self.embedding_texts.append(text)
        # 2026-06-13 17:18:04 新增：返回文本，作用是交给 embedding 模拟器；理由是保持生产函数签名。
        return text

    # 2026-06-13 17:18:04 新增：模拟 embedding，作用是给每条文本返回向量；理由是避免外部模型网络。
    def embed_texts(self, client: Any, texts: list[str], embedding_config: Any) -> list[list[float]]:
        # 2026-06-13 17:18:04 新增：记录待向量化文本，作用是审计字段；理由是同步必须只向量化 YAML 声明字段。
        self.calls.append(("embed", tuple(texts)))
        # 2026-06-13 17:18:04 新增：返回固定向量，作用是让后续 point 构造可继续；理由是本测试不验证向量质量。
        return [[1.0, 0.0] for _ in texts]

    # 2026-06-13 17:18:04 新增：构造假 point，作用是保留真实 payload 生成；理由是 payload 隔离必须用生产函数验证。
    def build_qdrant_points(self, chunks: list[Any], embeddings: list[list[float]], embedding_config: Any, qdrant_config: Any) -> list[FakePoint]:
        # 2026-06-13 17:18:04 新增：记录 point 构造调用，作用是验证每条 row 都进入 Qdrant；理由是不能只回写状态。
        self.calls.append(("build_points", tuple(chunk.chunk_id for chunk in chunks)))
        # 2026-06-13 17:18:04 新增：返回假 point 列表，作用是模拟生产 point；理由是 Qdrant SDK 对象不是本测试重点。
        return [
            FakePoint(
                # 2026-06-13 17:18:04 新增：使用真实确定性 point id，作用是删除和 upsert 身份一致；理由是状态持久化要能反推 Qdrant point。
                id=qdrant_sync.build_qdrant_point_id(chunk.chunk_id),
                # 2026-06-13 17:18:04 新增：写入对应向量，作用是模拟真实 point；理由是保持参数结构完整。
                vector=embedding,
                # 2026-06-13 17:18:04 新增：使用真实 payload 构造，作用是验证 YAML 渲染；理由是不能混入其他库顶层字段。
                payload=qdrant_sync.build_qdrant_payload(chunk, embedding_config),
            )
            # 2026-06-13 17:18:04 新增：逐条绑定 chunk 和向量，作用是保持顺序一致；理由是回写状态按 row 粒度执行。
            for chunk, embedding in zip(chunks, embeddings)
        ]

    # 2026-06-13 17:18:04 新增：模拟 Qdrant upsert，作用是记录已写入 payload；理由是每条成功后才允许回写 ZhuangTai。
    def upsert_points_to_qdrant(self, client: Any, qdrant_config: Any, points: list[FakePoint]) -> None:
        # 2026-06-13 17:18:04 新增：记录 upsert 数量，作用是验证 worker 逐条写入；理由是用户要求每条 point 写完后回写状态。
        self.calls.append(("upsert", qdrant_config.collection_name, len(points)))
        # 2026-06-13 17:18:04 新增：保存 payload，作用是后续断言字段隔离；理由是 Qdrant 顶层结构必须来自 YAML。
        self.upserted_payloads.extend(point.payload for point in points)

    # 2026-06-13 17:18:04 新增：模拟 Qdrant 删除，作用是覆盖本地状态识别硬删除；理由是别人 PG 删除行后 Qdrant point 也要清理。
    def delete_points_from_qdrant(self, client: Any, qdrant_config: Any, point_ids: list[str]) -> None:
        # 2026-06-13 17:18:04 新增：记录删除 point id，作用是断言 snapshot_diff 生效；理由是没有 CDC 时也要有近实时删除兜底。
        self.calls.append(("delete", qdrant_config.collection_name, tuple(point_ids)))


# 2026-06-13 17:18:04 新增：定义 PG 同步 worker 测试类，作用是锁定用户这次三个目标；理由是实现前先红测。
class ExternalPostgresSyncWorkerTest(unittest.TestCase):
    # 2026-06-13 17:18:04 新增：构造外部 PG 行，作用是模拟截图里的 AI_erp_Wendajilu；理由是测试字段名必须贴近真实库。
    def build_pg_row(self, pk: int, miao_shu: str, status: str = "") -> dict[str, Any]:
        # 2026-06-13 17:18:04 新增：返回完整业务行，作用是覆盖向量字段、payload 字段、状态回写字段；理由是 YAML 不能漏字段。
        return {
            "wdjl_id": pk,
            "WenTi": f"问题{pk}",
            "DaAn": f"答案{pk}",
            "WenTiYuanWen": f"原问{pk}",
            "DaAnYuanWen": f"原答{pk}",
            "WenTi_2": f"问题二{pk}",
            "DaAn_2": f"答案二{pk}",
            "MiaoShu": miao_shu,
            "ZhuangTai": status,
            "ShenHeRen": "审核人",
            "DiZhi": "车间",
            "ShiJian": "2026-06-13 17:18:04",
            "LeiXing": "问答",
            "ShenHeTime": "2026-06-13 17:18:04",
            "XiuGaiYuanYin": "",
            "gsId": "krauss",
            "del_flag": False,
        }

    # 2026-06-13 17:18:04 新增：验证新模块存在并可加载，作用是红测锁定新增 worker 入口；理由是后端服务生命周期要调用它。
    def test_external_sync_worker_module_is_available(self) -> None:
        # 2026-06-13 17:18:04 新增：查找新 worker 模块，作用是避免 import error 直接中断测试；理由是红测要给出明确断言。
        spec = importlib.util.find_spec("integration.external_sync_worker")
        # 2026-06-13 17:18:04 新增：断言模块存在，作用是要求实现通用外部源同步层；理由是不能继续靠离线转换脚本。
        self.assertIsNotNone(spec, "缺少 integration.external_sync_worker 通用外部源同步模块")

    # 2026-06-13 17:18:04 新增：验证 krauss PG profile 只用 MiaoShu 向量化且其他字段打包；理由是用户指定最后一张截图字段策略。
    def test_krauss_profile_vectors_only_miaoshu_and_packs_other_fields(self) -> None:
        # 2026-06-13 17:18:04 新增：加载 krauss PG profile，作用是读取真实 YAML；理由是字段策略必须配置化。
        profile = qdrant_mapping_profile.load_source_profile("krauss_ai_ie_dev")
        # 2026-06-13 17:18:04 新增：构造 PG 行，作用是模拟真实 AI_erp_Wendajilu 数据；理由是测试不能依赖现场库。
        row = self.build_pg_row(1, "用户在排产管理或PMC排产页面中，需要频繁手工导入订单和BOM数据")
        # 2026-06-13 17:18:04 新增：转换 canonical chunk，作用是复用生产 profile 解释器；理由是不能新拉一条 PG 专用映射链。
        chunk = qdrant_mapping_profile.row_to_canonical_chunk(row, profile, qdrant_sync)
        # 2026-06-13 17:18:04 新增：构造向量文本，作用是验证只使用 MiaoShu；理由是其他字段不得参与向量化。
        embedding_text = qdrant_sync.build_embedding_text(chunk)
        # 2026-06-13 17:18:04 新增：断言向量文本等于 MiaoShu，作用是锁定召回内容；理由是用户明确要求只向量化 MiaoShu。
        self.assertEqual(embedding_text, row["MiaoShu"])
        # 2026-06-13 17:18:04 新增：构造 payload，作用是验证 Qdrant 最终字段；理由是隔离目标在 payload 层体现。
        payload = qdrant_sync.build_qdrant_payload(
            chunk,
            qdrant_sync.EmbeddingConfig("http://embedding.local/v1", "fake", "fake-model", 2, 1),
        )
        # 2026-06-13 17:18:04 新增：断言顶层只有 retrieval_text 和 payload，作用是保护新库隔离；理由是不能混入 getai 专用字段。
        self.assertEqual(set(payload), {"retrieval_text", "payload"})
        # 2026-06-13 17:18:04 新增：断言 retrieval_text 等于 MiaoShu，作用是让 WebUI 可核对向量化内容；理由是向量字段必须可见。
        self.assertEqual(payload["retrieval_text"], row["MiaoShu"])
        # 2026-06-13 17:18:04 新增：断言业务 payload 保存 WenTi，作用是证明其他字段被打包；理由是用户要求其他字段进 payload。
        self.assertEqual(payload["payload"]["WenTi"], row["WenTi"])
        # 2026-06-13 17:18:04 新增：断言业务 payload 保存 ZhuangTai，作用是保留回写字段；理由是同步状态要可审计。
        self.assertEqual(payload["payload"]["ZhuangTai"], row["ZhuangTai"])
        # 2026-06-13 17:18:04 新增：断言 MiaoShu 不在嵌套 payload，作用是避免向量字段重复存储；理由是当前 YAML 声明其他字段才打包。
        self.assertNotIn("MiaoShu", payload["payload"])

    # 2026-06-13 17:18:04 新增：验证 worker upsert 成功后逐条回写 ZhuangTai；理由是用户要求每存好一条 point 就写回已入库。
    def test_worker_upserts_each_changed_row_then_writes_back_synced_status(self) -> None:
        # 2026-06-13 17:18:04 新增：延迟导入 worker，作用是让红测先检查模块；理由是实现前模块不存在时给出清晰失败。
        from integration.external_sync_state import InMemoryExternalSyncStateStore
        # 2026-06-13 17:18:04 新增：延迟导入 worker，作用是测试真实同步编排；理由是不能用离线转换脚本代替后台同步。
        from integration.external_sync_worker import ExternalSourceSyncWorker

        # 2026-06-13 17:18:04 新增：加载 krauss PG profile，作用是驱动字段和状态配置；理由是 worker 不硬编码表字段。
        profile = qdrant_mapping_profile.load_source_profile("krauss_ai_ie_dev")
        # 2026-06-13 17:18:04 新增：构造两条变化行，作用是验证逐条 upsert 和逐条回写；理由是批处理不能掩盖单条失败。
        rows = [self.build_pg_row(1, "第一条描述"), self.build_pg_row(2, "第二条描述")]
        # 2026-06-13 17:18:04 新增：创建假 adapter，作用是隔离 PG 网络；理由是单测不依赖局域网。
        adapter = FakeExternalAdapter(rows)
        # 2026-06-13 17:18:04 新增：创建内存状态库，作用是模拟实时状态持久化接口；理由是生产会换成 SQLite。
        state_store = InMemoryExternalSyncStateStore()
        # 2026-06-13 17:18:04 新增：预置一个旧 key，作用是验证 snapshot_diff 删除；理由是 PG 行被删除后 Qdrant point 也要删除。
        state_store.save_row_synced(profile.profile_name, "99", "old-hash", "old-point-id", "synced")
        # 2026-06-13 17:18:04 新增：创建假同步模块，作用是捕获 Qdrant 写入和删除；理由是测试不启动 Qdrant。
        fake_sync = FakeSyncModule()
        # 2026-06-13 17:18:04 新增：构造 embedding 配置，作用是满足 worker 参数；理由是测试不访问真实 embedding。
        embedding_config = qdrant_sync.EmbeddingConfig("http://embedding.local/v1", "fake", "fake-model", 2, 1)
        # 2026-06-13 17:18:04 新增：构造 Qdrant 配置，作用是指定独立 collection；理由是不能污染主问答 collection。
        qdrant_config = qdrant_sync.QdrantSyncConfig("http://qdrant.local:6333", "sql_krauss_ai_ie_dev", "Cosine", False, 1, False)
        # 2026-06-13 17:18:04 新增：创建 worker，作用是把 adapter、state、Qdrant 编排串起来；理由是后台服务只应调用统一入口。
        worker = ExternalSourceSyncWorker(
            profile=profile,
            adapter=adapter,
            state_store=state_store,
            sync_module=fake_sync,
            qdrant_client_factory=lambda url: "fake-qdrant-client",
            qdrant_config=qdrant_config,
            embedding_config=embedding_config,
        )
        # 2026-06-13 17:18:04 新增：执行单轮同步，作用是模拟后台 worker 的一次轮询；理由是单测不启动无限循环。
        summary = worker.sync_once()
        # 2026-06-13 17:18:04 新增：断言两条变化行都写入，作用是验证新增/修改同步；理由是实时联动必须更新 Qdrant。
        self.assertEqual(summary["upserted_count"], 2)
        # 2026-06-13 17:18:04 新增：断言旧 key 被删除，作用是验证 snapshot_diff 删除兜底；理由是对方硬删行时 Qdrant 不能留旧 point。
        self.assertEqual(summary["deleted_count"], 1)
        # 2026-06-13 17:18:04 新增：断言向量化文本只包含 MiaoShu，作用是防止其他字段进入 embedding；理由是用户要求只向量化 MiaoShu。
        self.assertEqual(fake_sync.embedding_texts, ["第一条描述", "第二条描述"])
        # 2026-06-13 17:18:04 新增：断言逐条回写已入库，作用是证明每个 point 成功后写回 PG 状态；理由是用户指定写回 ZhuangTai。
        self.assertEqual(adapter.status_updates, [("1", "已入库"), ("2", "已入库")])
        # 2026-06-13 17:18:04 新增：断言 payload 顶层隔离，作用是防止 getai 字段混入 krauss collection；理由是新外部库必须独立。
        self.assertEqual(set(fake_sync.upserted_payloads[0]), {"retrieval_text", "payload"})
        # 2026-06-13 17:18:04 新增：断言删除调用出现，作用是证明同步层包含 Qdrant 删除能力；理由是实时同步不应只有 upsert。
        self.assertTrue(any(call[0] == "delete" for call in fake_sync.calls))


# 2026-06-13 17:18:04 新增：提供直接运行入口，作用是方便本地单文件验证；理由是项目当前使用 unittest 风格。
if __name__ == "__main__":
    # 2026-06-13 17:18:04 新增：启动 unittest，作用是执行当前文件全部测试；理由是开发调试无需额外测试框架。
    unittest.main()
