# -*- coding: utf-8 -*-
"""外部关系型数据库到 Qdrant 的后台同步 worker。"""

# 2026-06-13 17:18:04 新增：导入 hashlib，作用是计算外部行内容 hash；理由是没有变更的行不应重复写 Qdrant。
import hashlib
# 2026-06-13 17:18:04 新增：导入 json，作用是稳定序列化外部行；理由是 hash 必须跟字段顺序无关。
import json
# 2026-06-13 17:18:04 新增：导入 os，作用是读取后台同步开关和服务配置；理由是后端启动后同步行为要可配置。
import os
# 2026-06-13 17:18:04 新增：导入 time，作用是后台轮询等待；理由是外部库没有 CDC 时用稳定 poll 模式兜底。
import time
# 2026-06-13 17:18:04 新增：导入 replace，作用是安全替换 frozen QdrantSyncConfig；理由是 profile 要覆盖 collection/source_profile。
from dataclasses import replace
# 2026-06-13 17:18:04 新增：导入 Path，作用是定位 SQL_RAG/.env 和状态文件；理由是服务启动不依赖当前工作目录。
from pathlib import Path
# 2026-06-13 17:18:04 新增：导入 Event/Thread/Lock，作用是实现后台常驻同步；理由是后端拉起后要持续联动外部 PG。
from threading import Event, Lock, Thread
# 2026-06-13 17:18:04 新增：导入 Any/Callable，作用是标注可替换依赖；理由是测试要注入假 Qdrant/embedding 模块。
from typing import Any, Callable

# 2026-06-13 17:18:04 新增：导入 dotenv 加载器，作用是读取 SQL_RAG/.env；理由是 PG 密码和服务地址不能硬编码在代码。
from dotenv import load_dotenv
# 2026-06-13 17:18:04 新增：导入 Qdrant 客户端，作用是生产环境写入/删除 point；理由是 worker 复用现有官方客户端链路。
from qdrant_client import QdrantClient

# 2026-06-13 17:18:04 新增：兼容 data_cleaning 顶层运行和 SQL_RAG 包运行；作用是导入现有 Qdrant 写入器；理由是新增同步不能另起写入链路。
try:
    # 2026-06-13 17:18:04 新增：按 data_cleaning 顶层导入；作用是兼容 unittest 和旧脚本；理由是测试把 data_cleaning 插入 sys.path。
    from Qdrant import qdrant_mapping_profile
    # 2026-06-13 17:18:04 新增：导入现有 Qdrant 同步模块；作用是复用 validate/embed/build/upsert；理由是保护现有完美问答链路。
    from Qdrant import qdrant_sqlserver_sync as default_qdrant_sync
except ImportError:
    # 2026-06-13 17:18:04 新增：按 SQL_RAG 包路径导入；作用是兼容 FastAPI 服务运行；理由是服务从 SQL_RAG 根目录启动。
    from data_cleaning.Qdrant import qdrant_mapping_profile
    # 2026-06-13 17:18:04 新增：导入现有 Qdrant 同步模块；作用是复用生产 Qdrant 写入能力；理由是不能复制第二套 point 构造逻辑。
    from data_cleaning.Qdrant import qdrant_sqlserver_sync as default_qdrant_sync

# 2026-06-13 17:18:04 新增：导入 adapter registry；作用是按 YAML connection.engine 选择 PG/SQLServer；理由是业务编排不写数据库 if 分支。
from .external_db_adapters import ExternalDbAdapter, ExternalAdapterRegistry, build_default_external_adapter_registry
# 2026-06-13 17:18:04 新增：导入状态存储；作用是保存 row_hash/point_id；理由是重启后仍要增量同步和删除 stale point。
from .external_sync_state import InMemoryExternalSyncStateStore, SQLiteExternalSyncStateStore


# 2026-06-13 17:18:04 新增：解析布尔值；作用是兼容 env/YAML 的 true/1/yes；理由是配置维护者写法可能不同。
def parse_bool(raw_value: Any, default: bool = False) -> bool:
    # 2026-06-13 17:18:04 新增：处理空值；作用是返回默认值；理由是未配置时不能误开启破坏主链路。
    if raw_value in (None, ""):
        # 2026-06-13 17:18:04 新增：返回默认布尔；作用是保持兼容；理由是旧配置没有外部同步字段。
        return default
    # 2026-06-13 17:18:04 新增：规范化文本；作用是识别常见真值；理由是 YAML/env 都可能是字符串。
    normalized = str(raw_value).strip().lower()
    # 2026-06-13 17:18:04 新增：返回是否为真值；作用是驱动 sync.enabled/write_back.enabled；理由是开关必须明确。
    return normalized in {"1", "true", "yes", "y", "on"}


# 2026-06-13 17:18:04 新增：解析整数配置；作用是读取 interval/batch 等数字；理由是 env/YAML 字符串要安全转换。
def parse_int(raw_value: Any, default: int) -> int:
    # 2026-06-13 17:18:04 新增：尝试转换 int；作用是得到稳定数字；理由是坏配置不能让服务启动崩掉。
    try:
        # 2026-06-13 17:18:04 新增：返回转换值；作用是供轮询和批量参数使用；理由是配置统一入口。
        return int(raw_value)
    except (TypeError, ValueError):
        # 2026-06-13 17:18:04 新增：返回默认值；作用是防御错误配置；理由是错误会在状态摘要里体现。
        return default


# 2026-06-13 17:18:04 新增：把配置值归一为字符串集合；作用是匹配 del_flag 等删除标记；理由是外部库布尔/数字/字符串形态不同。
def normalized_value_set(values: Any) -> set[str]:
    # 2026-06-13 17:18:04 新增：列表缺省兜底；作用是允许单值或列表；理由是 YAML 维护更灵活。
    raw_values = values if isinstance(values, (list, tuple, set)) else [values]
    # 2026-06-13 17:18:04 新增：返回规范化集合；作用是进行大小写无关匹配；理由是删除标记来源不统一。
    return {qdrant_mapping_profile.normalize_text(value).strip().lower() for value in raw_values if qdrant_mapping_profile.normalize_text(value)}


# 2026-06-13 17:18:04 新增：读取外部行主键文本；作用是统一 source_pk；理由是 Qdrant point 和状态表都必须稳定定位。
def row_source_pk(row: dict[str, Any], profile: Any) -> str:
    # 2026-06-13 17:18:04 新增：从 profile.id_field 读取值；作用是支持 wdjl_id/external_id 等任意主键；理由是不能写死 id。
    source_pk = qdrant_mapping_profile.normalize_text(qdrant_mapping_profile.row_value(row, profile.id_field))
    # 2026-06-13 17:18:04 新增：主键缺失时报错；作用是阻断不可幂等数据；理由是没有主键无法 upsert/delete。
    if not source_pk:
        # 2026-06-13 17:18:04 新增：抛出明确错误；作用是定位 YAML 或源表问题；理由是静默跳过会造成漏同步。
        raise ValueError(f"profile {profile.profile_name} 的行缺少主键字段：{profile.id_field}")
    # 2026-06-13 17:18:04 新增：返回主键文本；作用是后续状态和 point id 使用；理由是跨数据库类型统一为字符串。
    return source_pk


# 2026-06-13 17:18:04 新增：判断行是否软删除；作用是支持 del_flag/ZhuangTai 等删除策略；理由是实时同步不能只 upsert。
def row_is_deleted(row: dict[str, Any], profile: Any) -> bool:
    # 2026-06-13 17:18:04 新增：读取 sync 配置；作用是拿删除字段和值；理由是删除策略由 YAML 决定。
    sync_config = getattr(profile, "sync", {}) or {}
    # 2026-06-13 17:18:04 新增：读取删除字段名；作用是判断是否启用软删除；理由是有些外部库没有删除字段。
    delete_flag_field = qdrant_mapping_profile.normalize_text(sync_config.get("delete_flag_field"))
    # 2026-06-13 17:18:04 新增：没有删除字段时返回 false；作用是只靠 snapshot_diff 处理硬删除；理由是不能猜业务删除语义。
    if not delete_flag_field:
        # 2026-06-13 17:18:04 新增：返回未删除；作用是保持默认同步；理由是源库行存在就应入库。
        return False
    # 2026-06-13 17:18:04 新增：读取当前删除字段值；作用是与配置列表匹配；理由是 PG 可能是 bool/int/text。
    raw_value = qdrant_mapping_profile.row_value(row, delete_flag_field)
    # 2026-06-13 17:18:04 新增：读取删除值集合；作用是支持 true/1/已删除 等；理由是不同外部库删除标记不统一。
    delete_values = normalized_value_set(sync_config.get("delete_flag_values") or [True, "true", 1, "1", "Y", "y", "已删除"])
    # 2026-06-13 17:18:04 新增：返回是否匹配删除值；作用是决定删 Qdrant point；理由是软删除也要同步到向量库。
    return qdrant_mapping_profile.normalize_text(raw_value).strip().lower() in delete_values


# 2026-06-13 17:18:04 新增：计算外部行内容 hash；作用是变化检测；理由是没有更新的行不应重复嵌入和 upsert。
def build_row_hash(row: dict[str, Any], profile: Any) -> str:
    # 2026-06-13 17:18:04 新增：读取 sync 配置；作用是拿 hash 排除字段；理由是 ZhuangTai 回写不应触发下轮重复同步。
    sync_config = getattr(profile, "sync", {}) or {}
    # 2026-06-13 17:18:04 新增：读取状态字段；作用是默认排除回写字段；理由是自己写回的“已入库”不是业务内容变化。
    status_field = qdrant_mapping_profile.normalize_text(sync_config.get("status_field"))
    # 2026-06-13 17:18:04 新增：读取显式排除字段；作用是允许 YAML 排除更新时间或同步状态；理由是外部库字段策略不同。
    exclude_fields = {qdrant_mapping_profile.normalize_text(field) for field in sync_config.get("state_hash_exclude_fields") or []}
    # 2026-06-13 17:18:04 新增：把状态字段加入排除；作用是避免回写后马上又变更；理由是用户要求回写 ZhuangTai。
    if status_field:
        # 2026-06-13 17:18:04 新增：排除状态字段；作用是幂等同步；理由是状态字段由我们自己写。
        exclude_fields.add(status_field)
    # 2026-06-13 17:18:04 新增：构造 hash 输入；作用是只保留业务内容字段；理由是非业务状态不能触发向量更新。
    filtered_row = {
        # 2026-06-13 17:18:04 新增：字段名转字符串；作用是稳定 JSON key；理由是外部 row key 可能不是 str。
        str(key): qdrant_mapping_profile.normalize_payload_value(value)
        # 2026-06-13 17:18:04 新增：遍历 row 字段；作用是纳入所有未排除字段；理由是 payload 任意字段变化都应更新 Qdrant。
        for key, value in row.items()
        # 2026-06-13 17:18:04 新增：过滤排除字段；作用是跳过同步状态字段；理由是避免自触发循环。
        if qdrant_mapping_profile.normalize_text(key) not in exclude_fields
    }
    # 2026-06-13 17:18:04 新增：稳定序列化；作用是字段顺序不影响 hash；理由是数据库返回列顺序可能变化。
    raw_text = json.dumps(filtered_row, ensure_ascii=False, sort_keys=True, default=str)
    # 2026-06-13 17:18:04 新增：返回 SHA256；作用是作为状态表 row_hash；理由是短文本比较足够稳定。
    return hashlib.sha256(raw_text.encode("utf-8")).hexdigest()


# 2026-06-13 17:18:04 新增：构造默认 Qdrant 客户端；作用是禁用系统代理污染；理由是本地 127.0.0.1 Qdrant 曾受 no_proxy 影响。
def create_default_qdrant_client(url: str) -> QdrantClient:
    # 2026-06-13 17:18:04 新增：返回 QdrantClient；作用是供 worker 访问 Qdrant；理由是生产默认走官方 SDK。
    return QdrantClient(url=url, trust_env=False)


# 2026-06-13 17:18:04 新增：定义外部源同步 worker；作用是单 profile 单轮/循环同步；理由是后台服务启动后要长期联动外部库。
class ExternalSourceSyncWorker:
    # 2026-06-13 17:18:04 新增：初始化 worker；作用是注入 profile、adapter、状态和 Qdrant 依赖；理由是测试和生产共用同一编排。
    def __init__(
        self,
        profile: Any,
        adapter: ExternalDbAdapter,
        state_store: Any,
        sync_module: Any = default_qdrant_sync,
        qdrant_client_factory: Callable[[str], Any] = create_default_qdrant_client,
        qdrant_config: Any | None = None,
        embedding_config: Any | None = None,
    ) -> None:
        # 2026-06-13 17:18:04 新增：保存 profile；作用是读取字段/同步/Qdrant 布局；理由是所有策略都来自 YAML。
        self.profile = profile
        # 2026-06-13 17:18:04 新增：保存 adapter；作用是读取外部 rows 和回写状态；理由是 worker 不关心 SQL 方言。
        self.adapter = adapter
        # 2026-06-13 17:18:04 新增：保存状态存储；作用是幂等判断和删除；理由是重启后仍需增量同步。
        self.state_store = state_store
        # 2026-06-13 17:18:04 新增：保存 Qdrant 写入模块；作用是复用现有 validate/embed/build/upsert；理由是不能复制主链路。
        self.sync_module = sync_module
        # 2026-06-13 17:18:04 新增：保存 Qdrant 客户端工厂；作用是测试可替换；理由是单测不启动真实 Qdrant。
        self.qdrant_client_factory = qdrant_client_factory
        # 2026-06-13 17:18:04 新增：准备 Qdrant 配置；作用是把 source_profile 固定为当前 YAML；理由是 ensure_qdrant_collection 要按 profile 建索引。
        self.qdrant_config = self._prepare_qdrant_config(qdrant_config)
        # 2026-06-13 17:18:04 新增：保存 embedding 配置；作用是调用模型生成向量；理由是每次 upsert 必须有真实 embedding。
        self.embedding_config = embedding_config
        # 2026-06-13 17:18:04 新增：读取轮询间隔；作用是 manager 循环等待；理由是实时同步频率由 YAML 控制。
        self.interval_seconds = max(1, parse_int((getattr(profile, "sync", {}) or {}).get("interval_seconds"), 10))
        # 2026-06-13 17:18:04 新增：延迟保存 Qdrant client；作用是首次同步才连接；理由是服务启动不被 Qdrant 瞬时抖动阻断。
        self._qdrant_client: Any | None = None
        # 2026-06-13 17:18:04 新增：延迟保存 embedding client；作用是首次 upsert 才创建；理由是无变化时不请求模型。
        self._embedding_client: Any | None = None

    # 2026-06-13 17:18:04 新增：准备 Qdrant 配置；作用是把 profile collection/vector_mode 应用到运行配置；理由是外部库隔离靠 profile。
    def _prepare_qdrant_config(self, qdrant_config: Any | None) -> Any:
        # 2026-06-13 17:18:04 新增：要求配置存在；作用是避免生产漏传 Qdrant 目标；理由是同步不能猜 Qdrant 地址。
        if qdrant_config is None:
            # 2026-06-13 17:18:04 新增：抛出明确错误；作用是提示 manager 构造配置；理由是 worker 只编排不读全局 env。
            raise ValueError("ExternalSourceSyncWorker 缺少 qdrant_config")
        # 2026-06-13 17:18:04 新增：确保 source_profile 指向当前 profile；作用是 collection/index 校验按当前 YAML；理由是不能误读 getai 默认 profile。
        try:
            # 2026-06-13 17:18:04 新增：替换 source_profile；作用是兼容 frozen dataclass；理由是 QdrantSyncConfig 不应原地修改。
            qdrant_config = replace(qdrant_config, source_profile=self.profile.profile_name)
        except TypeError:
            # 2026-06-13 17:18:04 新增：忽略非 dataclass 配置；作用是兼容测试假对象；理由是单测只关心行为。
            pass
        # 2026-06-13 17:18:04 新增：如果同步模块有 profile 应用函数就调用；作用是自动切换 collection/hybrid；理由是 YAML 是最终结构来源。
        if hasattr(self.sync_module, "apply_source_profile_to_qdrant_config"):
            # 2026-06-13 17:18:04 新增：应用 profile 到 Qdrant 配置；作用是隔离目标 collection；理由是不能写进主 QA collection。
            qdrant_config = self.sync_module.apply_source_profile_to_qdrant_config(qdrant_config, self.profile)
        # 2026-06-13 17:18:04 新增：返回配置；作用是后续 ensure/build/upsert 共用；理由是避免配置漂移。
        return qdrant_config

    # 2026-06-13 17:18:04 新增：获取 Qdrant client；作用是懒连接；理由是 worker 创建不等于马上可访问 Qdrant。
    def _get_qdrant_client(self) -> Any:
        # 2026-06-13 17:18:04 新增：首次创建客户端；作用是复用连接对象；理由是每轮同步不必重复初始化 SDK。
        if self._qdrant_client is None:
            # 2026-06-13 17:18:04 新增：调用工厂；作用是生产或测试创建不同 client；理由是依赖注入保持可测试。
            self._qdrant_client = self.qdrant_client_factory(self.qdrant_config.url)
        # 2026-06-13 17:18:04 新增：返回 client；作用是 upsert/delete 使用；理由是统一入口。
        return self._qdrant_client

    # 2026-06-13 17:18:04 新增：获取 embedding client；作用是懒初始化模型客户端；理由是无变化轮询不应调用模型。
    def _get_embedding_client(self) -> Any:
        # 2026-06-13 17:18:04 新增：要求 embedding 配置存在；作用是避免生成假向量；理由是生产 Qdrant 必须真实向量。
        if self.embedding_config is None:
            # 2026-06-13 17:18:04 新增：抛出明确错误；作用是提示配置缺失；理由是不能静默写入空向量。
            raise ValueError("ExternalSourceSyncWorker 缺少 embedding_config")
        # 2026-06-13 17:18:04 新增：首次创建 embedding client；作用是复用模型连接；理由是多条行 upsert 不重复初始化。
        if self._embedding_client is None:
            # 2026-06-13 17:18:04 新增：调用现有创建函数；作用是复用 OpenAI-compatible embedding 逻辑；理由是保持主链路一致。
            self._embedding_client = self.sync_module.create_embedding_client(self.embedding_config)
        # 2026-06-13 17:18:04 新增：返回 embedding client；作用是 embed_texts 使用；理由是统一入口。
        return self._embedding_client

    # 2026-06-13 17:18:04 新增：删除一批 point；作用是处理源库硬删/软删；理由是实时同步不能只新增修改。
    def _delete_points(self, point_ids: list[str]) -> int:
        # 2026-06-13 17:18:04 新增：空列表直接返回；作用是避免无意义 SDK 调用；理由是无删除时保持轻量。
        if not point_ids:
            # 2026-06-13 17:18:04 新增：返回 0；作用是统计删除数量；理由是 summary 需要数字。
            return 0
        # 2026-06-13 17:18:04 新增：调用现有删除函数；作用是把删除也纳入 Qdrant SDK 层；理由是 worker 不直接写 SDK 细节。
        self.sync_module.delete_points_from_qdrant(self._get_qdrant_client(), self.qdrant_config, point_ids)
        # 2026-06-13 17:18:04 新增：返回删除数量；作用是写 summary；理由是健康检查要可见。
        return len(point_ids)

    # 2026-06-13 17:18:04 新增：把单行 upsert 到 Qdrant；作用是每条 point 成功后才能回写状态；理由是用户要求逐条确认。
    def _upsert_single_row(self, row: dict[str, Any]) -> str:
        # 2026-06-13 17:18:04 新增：把外部行转 canonical chunk；作用是复用现有 Qdrant 写入器；理由是不新建第二套 payload/point 逻辑。
        chunk = qdrant_mapping_profile.row_to_canonical_chunk(row, self.profile, self.sync_module)
        # 2026-06-13 17:18:04 新增：执行现有契约校验；作用是阻断缺字段数据；理由是坏 YAML 或空 MiaoShu 不能进入 Qdrant。
        validation = self.sync_module.validate_chunks_before_qdrant([chunk])
        # 2026-06-13 17:18:04 新增：兼容返回 error_count 的假模块；作用是测试和生产都能发现错误；理由是有错就不能回写已入库。
        if isinstance(validation, dict) and validation.get("error_count"):
            # 2026-06-13 17:18:04 新增：抛出校验错误；作用是中断当前行；理由是不能把不合格 point 写入 Qdrant。
            raise RuntimeError(f"外部行 {chunk.chunk_id} Qdrant 契约校验失败：{validation}")
        # 2026-06-13 17:18:04 新增：确保 collection 存在；作用是按 profile 建 collection 和索引；理由是每个外部库隔离写入。
        self.sync_module.ensure_qdrant_collection(self._get_qdrant_client(), self.qdrant_config, self.embedding_config)
        # 2026-06-13 17:18:04 新增：构造向量文本；作用是送给 embedding 服务；理由是用户要求只向量化 MiaoShu。
        embedding_text = self.sync_module.build_embedding_text(chunk)
        # 2026-06-13 17:18:04 新增：调用 embedding；作用是得到真实向量；理由是 Qdrant point 必须有向量。
        embeddings = self.sync_module.embed_texts(self._get_embedding_client(), [embedding_text], self.embedding_config)
        # 2026-06-13 17:18:04 新增：构造 Qdrant point；作用是复用 profile_rendered payload；理由是字段隔离由现有写入器保证。
        points = self.sync_module.build_qdrant_points([chunk], embeddings, self.embedding_config, self.qdrant_config)
        # 2026-06-13 17:18:04 新增：写入 Qdrant；作用是 upsert 单条 point；理由是成功后才能回写 ZhuangTai。
        self.sync_module.upsert_points_to_qdrant(self._get_qdrant_client(), self.qdrant_config, points)
        # 2026-06-13 17:18:04 新增：返回 point id；作用是状态表保存；理由是后续删除需要同一个 id。
        return str(points[0].id)

    # 2026-06-13 17:18:04 新增：同步单轮；作用是后台循环和测试都调用；理由是无限循环必须拆成可验证的一次行为。
    def sync_once(self) -> dict[str, Any]:
        # 2026-06-13 17:18:04 新增：从外部库读取 rows；作用是拿到最新源数据；理由是 PG/SQLServer CRUD 要反映到 Qdrant。
        rows = [dict(row) for row in self.adapter.fetch_rows(self.profile)]
        # 2026-06-13 17:18:04 新增：初始化当前活跃 key；作用是 snapshot_diff 比较；理由是硬删除只能通过本轮结果缺失发现。
        current_active_pks: set[str] = set()
        # 2026-06-13 17:18:04 新增：初始化待删 point；作用是收集软删行；理由是删除应先从 Qdrant 清理。
        point_ids_to_delete: list[str] = []
        # 2026-06-13 17:18:04 新增：初始化待处理行；作用是只 upsert 未删除行；理由是软删除不应再写入 Qdrant。
        active_rows: list[dict[str, Any]] = []
        # 2026-06-13 17:18:04 新增：遍历源库 rows；作用是分类 active/deleted；理由是不同删除策略统一在 worker 处理。
        for row in rows:
            # 2026-06-13 17:18:04 新增：读取 source_pk；作用是统一定位；理由是状态表和 Qdrant point 都靠它。
            source_pk = row_source_pk(row, self.profile)
            # 2026-06-13 17:18:04 新增：判断软删除；作用是发现 del_flag 删除；理由是外部库可能保留删除行。
            if row_is_deleted(row, self.profile):
                # 2026-06-13 17:18:04 新增：优先读取历史 point id；作用是删除已同步 point；理由是状态里保存最准确。
                point_id = self.state_store.get_point_id(self.profile.profile_name, source_pk)
                # 2026-06-13 17:18:04 新增：没有历史 point id 时按 chunk_id 推导；作用是仍可删除幂等 point；理由是 point id 由 source_pk 稳定生成。
                if not point_id:
                    # 2026-06-13 17:18:04 新增：转换 chunk 只为拿 chunk_id；作用是推导 point id；理由是删除不需要 embedding。
                    chunk = qdrant_mapping_profile.row_to_canonical_chunk(row, self.profile, self.sync_module)
                    # 2026-06-13 17:18:04 新增：生成稳定 point id；作用是删除 Qdrant point；理由是 upsert/delete 必须同源。
                    point_id = self.sync_module.build_qdrant_point_id(chunk.chunk_id)
                # 2026-06-13 17:18:04 新增：追加删除 point id；作用是稍后批量删除；理由是删除也要走 Qdrant SDK。
                point_ids_to_delete.append(point_id)
                # 2026-06-13 17:18:04 新增：标记本地删除；作用是 active 列表不再包含；理由是下轮不重复删除。
                self.state_store.mark_deleted(self.profile.profile_name, source_pk)
                # 2026-06-13 17:18:04 新增：跳过 upsert；作用是软删除行不再入库；理由是源库标记已删除。
                continue
            # 2026-06-13 17:18:04 新增：记录活跃 key；作用是后续 snapshot_diff；理由是本轮存在的行不应被当 stale。
            current_active_pks.add(source_pk)
            # 2026-06-13 17:18:04 新增：保存活跃 row；作用是后续 upsert；理由是删除分类和 upsert 分开更清晰。
            active_rows.append(row)
        # 2026-06-13 17:18:04 新增：读取删除策略；作用是判断是否做 snapshot_diff；理由是有些只读大表不希望全量比对删除。
        deletion_strategy = qdrant_mapping_profile.normalize_text((getattr(self.profile, "sync", {}) or {}).get("delete_strategy") or "snapshot_diff").lower()
        # 2026-06-13 17:18:04 新增：snapshot_diff 时删除源库已消失的历史 key；作用是支持 PG 硬删除；理由是别人 DELETE 不会主动通知我们。
        if deletion_strategy == "snapshot_diff":
            # 2026-06-13 17:18:04 新增：读取历史活跃 key；作用是和当前活跃 key 做差；理由是找出 stale point。
            previous_active_pks = self.state_store.list_active_source_pks(self.profile.profile_name)
            # 2026-06-13 17:18:04 新增：遍历 stale key；作用是删除 Qdrant 旧 point；理由是外部行消失后向量库也必须清理。
            for stale_pk in sorted(previous_active_pks - current_active_pks):
                # 2026-06-13 17:18:04 新增：读取 stale point id；作用是删除 Qdrant；理由是状态表保存了 point 身份。
                point_id = self.state_store.get_point_id(self.profile.profile_name, stale_pk)
                # 2026-06-13 17:18:04 新增：有 point id 才追加；作用是避免无效删除；理由是状态可能残缺。
                if point_id:
                    # 2026-06-13 17:18:04 新增：追加删除 point；作用是批量删除；理由是和软删除统一出口。
                    point_ids_to_delete.append(point_id)
                # 2026-06-13 17:18:04 新增：标记本地删除；作用是状态持久化；理由是下轮不重复处理。
                self.state_store.mark_deleted(self.profile.profile_name, stale_pk)
        # 2026-06-13 17:18:04 新增：执行 Qdrant 删除；作用是清理软删/硬删 point；理由是实时同步必须包含删除。
        deleted_count = self._delete_points(point_ids_to_delete)
        # 2026-06-13 17:18:04 新增：初始化计数；作用是生成 summary；理由是健康检查要可观测。
        upserted_count = 0
        # 2026-06-13 17:18:04 新增：初始化跳过计数；作用是生成 summary；理由是判断幂等是否生效。
        skipped_count = 0
        # 2026-06-13 17:18:04 新增：读取状态回写配置；作用是决定是否写 ZhuangTai；理由是不同外部库权限不同。
        sync_config = getattr(self.profile, "sync", {}) or {}
        # 2026-06-13 17:18:04 新增：读取 write_back 小节；作用是允许 YAML 关闭回写；理由是只读源库不能 UPDATE。
        write_back_config = sync_config.get("write_back") if isinstance(sync_config.get("write_back"), dict) else {}
        # 2026-06-13 17:18:04 新增：判断是否回写；作用是有 status_field 时默认开启；理由是用户要求 krauss 每条写回已入库。
        write_back_enabled = bool(sync_config.get("status_field")) and parse_bool(write_back_config.get("enabled"), True)
        # 2026-06-13 17:18:04 新增：读取回写状态值；作用是写入 ZhuangTai；理由是 krauss 目标值是“已入库”。
        synced_status_value = qdrant_mapping_profile.normalize_text(sync_config.get("synced_status_value") or write_back_config.get("status_value") or "已入库")
        # 2026-06-13 17:58:33 新增：读取状态字段名；作用是让 Qdrant payload 和 PG 回写状态保持同轮一致；理由是不能出现 PG 已入库但 point payload 仍是旧状态。
        status_field = qdrant_mapping_profile.normalize_text(sync_config.get("status_field"))
        # 2026-06-13 17:18:04 新增：遍历活跃行；作用是同步新增/修改；理由是源库 CRUD 的新增和更新要进 Qdrant。
        for row in active_rows:
            # 2026-06-13 17:18:04 新增：读取 source_pk；作用是状态和回写定位；理由是逐条入库逐条回写。
            source_pk = row_source_pk(row, self.profile)
            # 2026-06-13 17:18:04 新增：计算 row hash；作用是判断是否变更；理由是避免重复 embedding。
            row_hash = build_row_hash(row, self.profile)
            # 2026-06-13 17:18:04 新增：读取历史 hash；作用是幂等跳过；理由是服务常驻轮询不能无限消耗模型。
            previous_hash = self.state_store.get_row_hash(self.profile.profile_name, source_pk)
            # 2026-06-13 17:18:04 新增：未变化时跳过；作用是保护模型和 Qdrant；理由是只同步新增或修改。
            if previous_hash == row_hash:
                # 2026-06-13 17:18:04 新增：增加跳过计数；作用是 summary 可见；理由是证明幂等生效。
                skipped_count += 1
                # 2026-06-13 17:18:04 新增：继续下一行；作用是避免重复 upsert；理由是没有业务变化。
                continue
            # 2026-06-13 17:58:33 新增：复制当前行用于 Qdrant 渲染；作用是只调整本次 point payload，不提前污染 hash 和源 row；理由是状态字段由我们回写，不应触发下一轮重复同步。
            row_for_qdrant = dict(row)
            # 2026-06-13 17:58:33 新增：把即将回写的状态写入 point payload 副本；作用是让 payload.ZhuangTai 直接显示“已入库”；理由是截图目标要求字段存储和回写同步联动。
            if write_back_enabled and status_field:
                row_for_qdrant[status_field] = synced_status_value
            # 2026-06-13 17:18:04 新增：upsert 当前行；作用是写入 Qdrant；理由是新增或修改必须更新向量库。
            point_id = self._upsert_single_row(row_for_qdrant)
            # 2026-06-13 17:18:04 新增：如配置开启则回写源库状态；作用是设置 ZhuangTai=已入库；理由是用户明确要求每条 point 存好后回写。
            if write_back_enabled:
                # 2026-06-13 17:18:04 新增：调用 adapter 回写；作用是数据库方言由 adapter 处理；理由是 worker 不写 PG/SQLServer UPDATE 分支。
                self.adapter.mark_row_synced(self.profile, source_pk, synced_status_value)
            # 2026-06-13 17:18:04 新增：保存本地同步状态；作用是重启后增量继续；理由是 Qdrant 和源库状态都成功后才算完成。
            self.state_store.save_row_synced(self.profile.profile_name, source_pk, row_hash, point_id, "synced")
            # 2026-06-13 17:18:04 新增：增加 upsert 计数；作用是 summary 可见；理由是健康检查要知道本轮写了几条。
            upserted_count += 1
        # 2026-06-13 17:18:04 新增：返回同步摘要；作用是后台 manager 和测试断言使用；理由是不能只看日志判断成败。
        return {
            "profile": self.profile.profile_name,
            "collection": self.qdrant_config.collection_name,
            "fetched_count": len(rows),
            "upserted_count": upserted_count,
            "skipped_count": skipped_count,
            "deleted_count": deleted_count,
            "write_back_enabled": write_back_enabled,
            "synced_status_value": synced_status_value,
        }


# 2026-06-13 17:18:04 新增：定义后台同步管理器；作用是接入 FastAPI 启停生命周期；理由是用户要求后端拉起后持续同步。
class ExternalSourceSyncManager:
    # 2026-06-13 17:18:04 新增：初始化 manager；作用是准备 registry、状态库和线程控制；理由是服务生命周期要集中管理。
    def __init__(
        self,
        sql_rag_dir: Path,
        registry: ExternalAdapterRegistry | None = None,
        state_store: Any | None = None,
        sync_module: Any = default_qdrant_sync,
    ) -> None:
        # 2026-06-13 17:18:04 新增：保存 SQL_RAG 根目录；作用是定位 .env/source_profiles/runtime_logs；理由是服务可从任意目录启动。
        self.sql_rag_dir = sql_rag_dir
        # 2026-06-13 17:18:04 新增：加载 SQL_RAG/.env；作用是拿 PG 密码和 Qdrant/embedding 配置；理由是敏感信息不写 YAML。
        load_dotenv(self.sql_rag_dir / ".env", override=True)
        # 2026-06-13 17:18:04 新增：保存 adapter registry；作用是 engine 到 adapter 的分发；理由是新增数据库类型只注册 adapter。
        self.registry = registry or build_default_external_adapter_registry()
        # 2026-06-13 17:18:04 新增：保存 Qdrant 同步模块；作用是复用现有写入器；理由是 manager 不直接构造 point。
        self.sync_module = sync_module
        # 2026-06-13 17:18:04 新增：保存状态存储；作用是生产用 SQLite，测试可注入内存；理由是同步状态必须持久化。
        self.state_store = state_store or SQLiteExternalSyncStateStore(self.sql_rag_dir / "runtime_logs" / "external_sync_state.sqlite3")
        # 2026-06-13 17:18:04 新增：创建停止事件；作用是优雅停止后台线程；理由是 FastAPI shutdown 要释放同步循环。
        self._stop_event = Event()
        # 2026-06-13 17:18:04 新增：初始化线程引用；作用是避免重复启动；理由是服务 reload 或健康检查不能开启多个 worker。
        self._thread: Thread | None = None
        # 2026-06-13 17:18:04 新增：创建状态锁；作用是保护 last summaries；理由是后台线程和健康接口并发访问。
        self._lock = Lock()
        # 2026-06-13 17:18:04 新增：初始化 workers；作用是缓存每个 profile 的 worker；理由是启动后循环复用。
        self._workers: list[ExternalSourceSyncWorker] = []
        # 2026-06-13 17:18:04 新增：初始化状态摘要；作用是健康检查可读；理由是同步不能只靠控制台日志。
        self._status: dict[str, Any] = {"enabled": self.enabled, "running": False, "profiles": {}}

    # 2026-06-13 17:18:04 新增：读取全局启用开关；作用是默认不影响旧部署；理由是没有配置外部同步时主 QA 不应变。
    @property
    def enabled(self) -> bool:
        # 2026-06-13 17:18:04 新增：读取 env 开关；作用是控制后台同步是否启动；理由是部署时可单独关闭。
        return parse_bool(os.getenv("EXTERNAL_SOURCE_SYNC_ENABLED"), False)

    # 2026-06-13 17:18:04 新增：读取 profile 名称列表；作用是决定哪些外部库进入后台同步；理由是一台服务可接多个外部库。
    def _profile_names(self) -> list[str]:
        # 2026-06-13 17:18:04 新增：读取显式 env 列表；作用是让部署指定要同步的库；理由是不扫描未准备好的 profile。
        raw_names = os.getenv("EXTERNAL_SOURCE_SYNC_PROFILES", "")
        # 2026-06-13 17:18:04 新增：如果显式配置则按逗号拆分；作用是稳定启动范围；理由是生产环境要可控。
        if raw_names.strip():
            # 2026-06-13 17:18:04 新增：返回清理后的 profile 名；作用是支持多库同步；理由是配置可读。
            return [name.strip() for name in raw_names.split(",") if name.strip()]
        # 2026-06-13 17:18:04 新增：定位 source_profiles；作用是兜底扫描 sync.enabled 的 profile；理由是减少手工配置。
        profiles_dir = self.sql_rag_dir / "data_cleaning" / "source_profiles"
        # 2026-06-13 17:18:04 新增：初始化名称列表；作用是收集启用的 YAML；理由是未显式配置时仍可发现。
        names: list[str] = []
        # 2026-06-13 17:18:04 新增：遍历 YAML 文件；作用是找 sync.enabled；理由是 profile 是同步策略入口。
        for profile_path in profiles_dir.glob("*.yml"):
            # 2026-06-13 17:18:04 新增：尝试加载 profile；作用是读取 sync 配置；理由是坏 YAML 不应阻断其他库。
            try:
                # 2026-06-13 17:18:04 新增：加载 profile；作用是判断是否启用后台同步；理由是每库独立开关。
                profile = qdrant_mapping_profile.load_source_profile(str(profile_path))
            except Exception:
                # 2026-06-13 17:18:04 新增：跳过坏 profile；作用是保护主服务启动；理由是健康状态会另行暴露错误。
                continue
            # 2026-06-13 17:18:04 新增：判断 sync.enabled；作用是收集要启动的外部库；理由是旧 profile 不应自动后台同步。
            if parse_bool((getattr(profile, "sync", {}) or {}).get("enabled"), False):
                # 2026-06-13 17:18:04 新增：加入 profile 名；作用是后续创建 worker；理由是 profile 名是稳定入口。
                names.append(profile.profile_name)
        # 2026-06-13 17:18:04 新增：返回扫描结果；作用是 manager 启动使用；理由是多外部库统一处理。
        return names

    # 2026-06-13 17:18:04 新增：构造 embedding 配置；作用是提供真实向量化参数；理由是外部库同步不能写假向量。
    def _build_embedding_config(self) -> Any:
        # 2026-06-13 17:18:04 新增：返回现有 EmbeddingConfig；作用是复用 SQL_RAG embedding 环境变量；理由是模型配置全局一致。
        return self.sync_module.EmbeddingConfig(
            # 2026-06-13 17:18:04 新增：读取 embedding API base；作用是连接现有 embedding 服务；理由是和主 Qdrant 写入一致。
            api_base=os.getenv("EMBEDDING_SERVICE_URL", "https://api.siliconflow.cn/v1"),
            # 2026-06-13 17:18:04 新增：读取 embedding key；作用是认证；理由是生产向量化必须有 key。
            api_key=os.getenv("EMBEDDING_SERVICE_API_KEY", ""),
            # 2026-06-13 17:18:04 新增：读取 embedding 模型；作用是生成向量；理由是要和查询阶段模型一致。
            model=os.getenv("MODEL_EMBED", "Qwen/Qwen3-Embedding-0.6B"),
            # 2026-06-13 17:18:04 新增：读取向量维度；作用是建 collection；理由是 Qdrant schema 必须匹配模型输出。
            dimension=parse_int(os.getenv("EMBEDDING_DIMENSIONS"), 1024),
            # 2026-06-13 17:18:04 新增：读取批量大小；作用是控制 embedding 请求；理由是避免服务压力过大。
            batch_size=parse_int(os.getenv("EMBEDDING_MAX_CHUNKS_IN_BATCH"), 10),
        )

    # 2026-06-13 17:18:04 新增：构造 Qdrant 配置；作用是让外部库写入独立 Qdrant/collection；理由是不能污染主 QA collection。
    def _build_qdrant_config(self, profile: Any) -> Any:
        # 2026-06-13 17:18:04 新增：读取外部同步 Qdrant URL；作用是优先使用外部隔离 Qdrant；理由是原 External_database 已有 6334 隔离服务。
        qdrant_url = os.getenv("EXTERNAL_SOURCE_QDRANT_URL") or os.getenv("EXTERNAL_QDRANT_URL") or os.getenv("QDRANT_URL", "http://127.0.0.1:6333")
        # 2026-06-13 17:18:04 新增：返回 QdrantSyncConfig；作用是交给 worker；理由是写入器只接受现有 config 类型。
        return self.sync_module.QdrantSyncConfig(
            # 2026-06-13 17:18:04 新增：写入 URL；作用是连接 Qdrant；理由是不同环境可能端口不同。
            url=qdrant_url,
            # 2026-06-13 17:18:04 新增：写入 collection；作用是默认取 profile.target_collection；理由是每个外部库隔离 collection。
            collection_name=os.getenv("EXTERNAL_SOURCE_QDRANT_COLLECTION") or getattr(profile, "target_collection", "") or os.getenv("QDRANT_COLLECTION", "sql_rag_qa_chunks_v1"),
            # 2026-06-13 17:18:04 新增：写入距离；作用是创建 collection；理由是沿用现有 Cosine 配置。
            distance=os.getenv("EXTERNAL_SOURCE_QDRANT_DISTANCE") or os.getenv("QDRANT_DISTANCE", "Cosine"),
            # 2026-06-13 17:18:04 新增：写入重建开关；作用是需要时重建外部 collection；理由是正常启动不应清空向量库。
            recreate_collection=parse_bool(os.getenv("EXTERNAL_SOURCE_QDRANT_RECREATE"), False),
            # 2026-06-13 17:18:04 新增：写入 upsert 批量；作用是控制 Qdrant 写入；理由是外部库数据量可能变大。
            upsert_batch_size=parse_int(os.getenv("EXTERNAL_SOURCE_QDRANT_UPSERT_BATCH_SIZE"), 64),
            # 2026-06-13 17:18:04 新增：写入 dry-run；作用是调试可只跑链路不写库；理由是生产默认真实写入。
            dry_run=parse_bool(os.getenv("EXTERNAL_SOURCE_QDRANT_DRY_RUN"), False),
            # 2026-06-13 17:18:04 新增：写入 hybrid 显式开关；作用是 profile 可进一步覆盖；理由是不同外部库可声明 hybrid。
            enable_hybrid=parse_bool(os.getenv("EXTERNAL_SOURCE_QDRANT_ENABLE_HYBRID"), False),
            # 2026-06-13 17:18:04 新增：写入 source_profile；作用是 ensure_qdrant_collection 按当前 YAML 建索引；理由是不能回到默认 getai。
            source_profile=getattr(profile, "profile_name", ""),
        )

    # 2026-06-13 17:18:04 新增：构建 worker 列表；作用是把 YAML profile 转成运行对象；理由是 manager 循环只调 worker。
    def _build_workers(self) -> list[ExternalSourceSyncWorker]:
        # 2026-06-13 17:18:04 新增：初始化列表；作用是收集可运行 worker；理由是部分 profile 失败不影响其他库。
        workers: list[ExternalSourceSyncWorker] = []
        # 2026-06-13 17:18:04 新增：构造 embedding 配置；作用是所有 worker 共用；理由是模型服务一致。
        embedding_config = self._build_embedding_config()
        # 2026-06-13 17:18:04 新增：遍历 profile 名；作用是创建每个外部库同步任务；理由是支持多库扩展。
        for profile_name in self._profile_names():
            # 2026-06-13 17:18:04 新增：加载 profile；作用是读取连接/字段/sync/qdrant_payload；理由是策略全部在 YAML。
            profile = qdrant_mapping_profile.load_source_profile(profile_name)
            # 2026-06-13 17:18:04 新增：创建 adapter；作用是按 connection.engine 连接 PG/SQLServer；理由是 worker 不写 if 分支。
            adapter = self.registry.create_from_profile(profile)
            # 2026-06-13 17:18:04 新增：创建 worker；作用是加入后台同步；理由是每个 profile 独立处理。
            workers.append(
                ExternalSourceSyncWorker(
                    # 2026-06-13 17:18:04 新增：传入 profile；作用是驱动字段映射；理由是 YAML 是单一真相。
                    profile=profile,
                    # 2026-06-13 17:18:04 新增：传入 adapter；作用是读源库和回写；理由是数据库差异隔离在 adapter。
                    adapter=adapter,
                    # 2026-06-13 17:18:04 新增：传入状态存储；作用是持久化增量状态；理由是重启后继续同步。
                    state_store=self.state_store,
                    # 2026-06-13 17:18:04 新增：传入 Qdrant 写入模块；作用是复用现有链路；理由是保护主 QA 逻辑。
                    sync_module=self.sync_module,
                    # 2026-06-13 17:18:04 新增：传入 Qdrant 配置；作用是隔离 collection；理由是不能写主 collection。
                    qdrant_config=self._build_qdrant_config(profile),
                    # 2026-06-13 17:18:04 新增：传入 embedding 配置；作用是生产真实向量；理由是 Qdrant point 必须可检索。
                    embedding_config=embedding_config,
                )
            )
        # 2026-06-13 17:18:04 新增：返回 worker 列表；作用是 start 使用；理由是构建与运行分开。
        return workers

    # 2026-06-13 17:18:04 新增：启动后台同步；作用是 FastAPI startup 调用；理由是服务启动后自动联动外部库。
    def start(self) -> dict[str, Any]:
        # 2026-06-13 17:18:04 新增：全局未启用则只记录状态；作用是保护旧部署；理由是没有配置时不影响完美问答链路。
        if not self.enabled:
            # 2026-06-13 17:18:04 新增：写禁用状态；作用是健康检查可见；理由是用户能知道为什么没跑。
            with self._lock:
                # 2026-06-13 17:18:04 新增：更新状态；作用是返回给健康检查；理由是禁用不是错误。
                self._status = {"enabled": False, "running": False, "status": "disabled", "profiles": {}}
            # 2026-06-13 17:18:04 新增：返回状态；作用是 startup 可忽略；理由是主服务继续启动。
            return self.status()
        # 2026-06-13 17:18:04 新增：避免重复启动；作用是一个 manager 只开一个线程；理由是重复线程会重复写 Qdrant。
        if self._thread is not None and self._thread.is_alive():
            # 2026-06-13 17:18:04 新增：返回当前状态；作用是不重复构建；理由是幂等 start。
            return self.status()
        # 2026-06-13 17:18:04 新增：清理停止标记；作用是允许重新启动；理由是服务 reload 后可再跑。
        self._stop_event.clear()
        # 2026-06-13 17:18:04 新增：构建 workers；作用是加载所有启用 profile；理由是启动时绑定配置。
        try:
            # 2026-06-13 17:18:04 新增：加载 worker 列表；作用是把 YAML 绑定到 adapter/Qdrant 配置；理由是启动阶段只做轻量准备。
            self._workers = self._build_workers()
        except Exception as exc:
            # 2026-06-13 17:18:04 新增：捕获启动配置错误；作用是外部同步失败不阻断主 FastAPI；理由：用户要求现有完美问答链路不受影响。
            with self._lock:
                # 2026-06-13 17:18:04 新增：写启动错误状态；作用是健康检查给出明确原因；理由：不能静默失败也不能拖垮主服务。
                self._status = {
                    "enabled": True,
                    "running": False,
                    "status": "startup_error",
                    "profiles": {},
                    "last_error": f"{type(exc).__name__}: {exc}",
                }
            # 2026-06-13 17:18:04 新增：返回错误状态；作用是调用方可见；理由：startup 不抛异常。
            return self.status()
        # 2026-06-13 17:18:04 新增：没有 worker 时记录状态；作用是避免空线程；理由是启用但无 profile 是配置问题。
        if not self._workers:
            # 2026-06-13 17:18:04 新增：写 no_profiles 状态；作用是健康检查可见；理由是用户能立刻发现配置问题。
            with self._lock:
                # 2026-06-13 17:18:04 新增：更新状态；作用是说明没有同步对象；理由是避免静默。
                self._status = {"enabled": True, "running": False, "status": "no_profiles", "profiles": {}}
            # 2026-06-13 17:18:04 新增：返回状态；作用是 startup 不阻断主服务；理由是主 QA 链路不能受影响。
            return self.status()
        # 2026-06-13 17:18:04 新增：创建后台线程；作用是持续轮询外部库；理由是用户要求实时联动。
        self._thread = Thread(target=self._run_loop, name="external-source-sync", daemon=True)
        # 2026-06-13 17:18:04 新增：启动线程；作用是异步运行；理由是 FastAPI startup 不能被长轮询阻塞。
        self._thread.start()
        # 2026-06-13 17:18:04 新增：写运行状态；作用是健康检查立即可见；理由是启动成功要有反馈。
        with self._lock:
            # 2026-06-13 17:18:04 新增：更新状态；作用是标记 running；理由是后台线程已启动。
            self._status.update({"enabled": True, "running": True, "status": "running"})
        # 2026-06-13 17:18:04 新增：返回状态；作用是 startup 日志/健康可用；理由是调用方不需要等第一轮完成。
        return self.status()

    # 2026-06-13 17:18:04 新增：后台循环；作用是按 interval 轮询所有 worker；理由是源库变化要持续进入 Qdrant。
    def _run_loop(self) -> None:
        # 2026-06-13 17:18:04 新增：循环直到停止事件；作用是常驻同步；理由是后端服务生命周期内都要联动。
        while not self._stop_event.is_set():
            # 2026-06-13 17:18:04 新增：初始化本轮最小间隔；作用是多 profile 下按最短间隔等待；理由是简单可靠。
            sleep_seconds = min((worker.interval_seconds for worker in self._workers), default=10)
            # 2026-06-13 17:18:04 新增：遍历 worker；作用是逐库同步；理由是每个 profile 独立连接/collection。
            for worker in list(self._workers):
                # 2026-06-13 17:18:04 新增：执行单轮同步并捕获异常；作用是一个库失败不杀后台线程；理由是外部网络可能抖动。
                try:
                    # 2026-06-13 17:18:04 新增：执行同步；作用是读源库、写 Qdrant、回写状态；理由是核心目标。
                    summary = worker.sync_once()
                    # 2026-06-13 17:18:04 新增：读取状态摘要；作用是补充 tracked/active 统计；理由是健康检查更完整。
                    state_summary = self.state_store.summary(worker.profile.profile_name)
                    # 2026-06-13 17:18:04 新增：加锁写成功状态；作用是健康检查可读；理由是后台线程不能只打印日志。
                    with self._lock:
                        # 2026-06-13 17:18:04 新增：写 profile 状态；作用是暴露本轮结果；理由是用户要准信。
                        self._status.setdefault("profiles", {})[worker.profile.profile_name] = {
                            "ready": True,
                            "last_summary": summary,
                            "state": state_summary,
                            "last_error": "",
                        }
                except Exception as exc:
                    # 2026-06-13 17:18:04 新增：加锁写错误状态；作用是服务不崩但健康能看到；理由是外部库不可控。
                    with self._lock:
                        # 2026-06-13 17:18:04 新增：记录异常；作用是定位 PG/Qdrant/embedding 失败；理由是不能假装同步完成。
                        self._status.setdefault("profiles", {})[worker.profile.profile_name] = {
                            "ready": False,
                            "last_summary": {},
                            "state": self.state_store.summary(worker.profile.profile_name),
                            "last_error": f"{type(exc).__name__}: {exc}",
                        }
            # 2026-06-13 17:18:04 新增：等待下一轮或停止；作用是可快速 shutdown；理由是后台线程不能卡住服务退出。
            self._stop_event.wait(max(1, sleep_seconds))

    # 2026-06-13 17:18:04 新增：停止后台同步；作用是 FastAPI shutdown 调用；理由是关闭服务时要停线程。
    def stop(self) -> None:
        # 2026-06-13 17:18:04 新增：设置停止事件；作用是通知循环退出；理由是 daemon 线程也要尽量优雅。
        self._stop_event.set()
        # 2026-06-13 17:18:04 新增：等待线程退出；作用是避免关闭时仍在写状态；理由是资源清理要稳。
        if self._thread is not None and self._thread.is_alive():
            # 2026-06-13 17:18:04 新增：短等待；作用是不阻塞太久；理由是外部库连接可能正在 timeout。
            self._thread.join(timeout=5)
        # 2026-06-13 17:18:04 新增：写停止状态；作用是健康检查可见；理由是生命周期状态要明确。
        with self._lock:
            # 2026-06-13 17:18:04 新增：更新 running；作用是标记后台已停；理由是避免误判仍在同步。
            self._status.update({"running": False, "status": "stopped" if self.enabled else "disabled"})

    # 2026-06-13 17:18:04 新增：读取状态；作用是健康检查和调试接口使用；理由是同步情况必须可观测。
    def status(self) -> dict[str, Any]:
        # 2026-06-13 17:18:04 新增：加锁复制状态；作用是防止外部修改内部 dict；理由是健康响应应是快照。
        with self._lock:
            # 2026-06-13 17:18:04 新增：通过 JSON 深拷贝；作用是复制嵌套结构；理由是状态里只有可 JSON 化对象。
            return json.loads(json.dumps(self._status, ensure_ascii=False, default=str))
