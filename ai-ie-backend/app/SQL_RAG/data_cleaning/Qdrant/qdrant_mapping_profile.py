# -*- coding: utf-8 -*-
"""数据源 mapping profile 解析器，用于把不同来源字段解释成统一 Qdrant 同步契约。"""

# 2026-06-11 15:54:56 修改：导入 hashlib，作用：为外部原始行生成稳定 hash；理由：外部库没有原清洗链路的 hash 字段。
import hashlib
# 2026-06-11 15:54:56 修改：导入 json，作用：解析列表字段和序列化 payload；理由：profile 字段可能来自 JSON 字符串。
import json
# 2026-06-11 15:54:56 修改：导入 dataclass 和 replace，作用：定义 profile 并安全复制 frozen CanonicalChunk；理由：不能原地改坏上游对象。
from dataclasses import dataclass, replace
# 2026-06-11 15:54:56 修改：导入日期类型，作用：把 SQL Server datetime 转成 Qdrant 可存字符串；理由：payload 必须可 JSON 化。
from datetime import date, datetime
# 2026-06-11 15:54:56 修改：导入 Path，作用：定位 source_profiles 配置目录；理由：profile 文件必须随 data_cleaning 迁移。
from pathlib import Path
# 2026-06-11 15:54:56 修改：导入 Any，作用：标注动态 row 和 payload 类型；理由：外部库字段结构不可预设。
from typing import Any

# 2026-06-11 15:54:56 修改：导入 PyYAML，作用：读取数据源 profile 配置；理由：字段策略应由配置管理而不是写死 Python。
import yaml


# 2026-06-11 15:54:56 修改：定义默认 profile 名称；作用：未显式配置时保护现有 getai 同步行为；理由：主 agent 链路不能被外部策略影响。
DEFAULT_SOURCE_PROFILE_NAME = "getai_rag_qa_chunks"
# 2026-06-12 09:52:34 修改：定义默认 dense-only Qdrant 输出模式；作用：保护当前主 agent 使用的旧 collection；理由：不能把 sql_rag_qa_chunks_v1 原地改成 hybrid。
QDRANT_VECTOR_MODE_DENSE = "dense"
# 2026-06-12 09:52:34 修改：定义 LlamaIndex hybrid Qdrant 输出模式；作用：让外部消费者可用 enable_hybrid=True；理由：需要同时生成 text-dense 和 text-sparse-new。
QDRANT_VECTOR_MODE_HYBRID = "hybrid"
# 2026-06-12 09:52:34 修改：定义 LlamaIndex 默认 dense 向量名；作用：profile 不写时仍能对齐官方 QdrantVectorStore；理由：别人全量参数默认会找 text-dense。
DEFAULT_QDRANT_DENSE_VECTOR_NAME = "text-dense"
# 2026-06-12 09:52:34 修改：定义 LlamaIndex 默认 sparse 向量名；作用：profile 不写时仍能对齐官方 QdrantVectorStore；理由：别人全量参数默认会找 text-sparse-new。
DEFAULT_QDRANT_SPARSE_VECTOR_NAME = "text-sparse-new"
# 2026-06-12 09:52:34 修改：定义外部消费者指定的 sparse 模型名；作用：文档侧 sparse encoder 与 fastembed_sparse_model="Qdrant/bm25" 对齐；理由：只建 sparse 向量名但模型不一致仍会影响 hybrid 召回。
DEFAULT_QDRANT_FASTEMBED_SPARSE_MODEL = "Qdrant/bm25"
# 2026-06-11 15:54:56 修改：定义当前模块目录；作用：推导 data_cleaning 路径；理由：避免依赖进程工作目录。
CURRENT_DIR = Path(__file__).resolve().parent
# 2026-06-11 15:54:56 修改：定义 data_cleaning 目录；作用：定位 source_profiles；理由：配置文件和 Qdrant 同步层同属 data_cleaning。
DATA_CLEANING_DIR = CURRENT_DIR.parent
# 2026-06-11 15:54:56 修改：定义 profile 目录；作用：集中管理每个数据源的字段映射；理由：不同外部库只换配置不换链路。
SOURCE_PROFILES_DIR = DATA_CLEANING_DIR / "source_profiles"
# 2026-06-11 15:54:56 修改：定义 profile payload 名称字段；作用：Qdrant payload 可看到使用了哪份配置；理由：排查多数据源接入时必须可追溯。
PROFILE_NAME_PAYLOAD_KEY = "mapping_profile_name"
# 2026-06-11 15:54:56 修改：定义契约模式字段；作用：区分 getai 严格 QA 校验和外部库泛化校验；理由：外部库可能只用问题做向量化。
PROFILE_CONTRACT_MODE_KEY = "profile_contract_mode"
# 2026-06-11 15:54:56 修改：定义向量文本字段；作用：让 build_embedding_text 优先读取 profile 结果；理由：外部库可动态选择向量化字段。
PROFILE_EMBEDDING_TEXT_KEY = "embedding_text"
# 2026-06-11 15:54:56 修改：定义 prompt 文本字段；作用：让 build_answer_first_text 优先读取 profile 结果；理由：避免全量 payload 进模型。
PROFILE_PROMPT_TEXT_KEY = "prompt_text"
# 2026-06-11 15:54:56 修改：定义来源 payload 字段；作用：嵌套保留外部库原始业务字段；理由：字段不参与向量化也要可回表和展示。
PROFILE_SOURCE_PAYLOAD_KEY = "source_payload"
# 2026-06-11 15:54:56 修改：定义来源名字段；作用：Qdrant point 可追溯数据源；理由：统一写入后必须区分 getai 和外部库。
PROFILE_SOURCE_NAME_KEY = "source_name"
# 2026-06-11 15:54:56 修改：定义来源表字段；作用：Qdrant point 可回表定位；理由：外部多表接入时不能只看 collection。
PROFILE_SOURCE_TABLE_KEY = "source_table"
# 2026-06-11 15:54:56 修改：定义来源主键字段；作用：Qdrant point 可定位原始行；理由：外部库需要稳定主键。
PROFILE_SOURCE_PK_KEY = "source_pk"
# 2026-06-11 15:54:56 修改：定义 profile 关键词字段；作用：把 profile 指定 keyword_index 字段转换成 list[str]；理由：Qdrant KEYWORD index 需要规范列表。
PROFILE_KEYWORD_TERMS_KEY = "profile_keyword_terms"
# 2026-06-11 15:54:56 修改：定义目标 collection 字段；作用：记录 profile 预期写入位置；理由：排查命令行 collection 覆盖时更清楚。
PROFILE_TARGET_COLLECTION_KEY = "profile_target_collection"
# 2026-06-12 14:40:11 修改：定义 payload 模式字段名；作用：把 legacy_qa/profile_strict 写进 chunk 契约；理由：Qdrant 写入层必须知道是否输出旧 QA 大 payload。
PROFILE_PAYLOAD_MODE_KEY = "payload_mode"
# 2026-06-12 14:40:11 修改：定义旧 QA payload 模式；作用：保护 getai/sql_rag_qa_chunks_v1 现有字段；理由：当前主 agent 完美问答链路不能被外部库隔离改动影响。
PAYLOAD_MODE_LEGACY_QA = "legacy_qa"
# 2026-06-12 14:40:11 修改：定义 profile 严格 payload 模式；作用：外部库只输出最小契约和嵌套 payload；理由：sql_External_database 不能混入 getai 专用字段。
PAYLOAD_MODE_PROFILE_STRICT = "profile_strict"
# 2026-06-12 15:30:17 修改：定义 YAML 渲染 payload 模式；作用：让每个外部库用 qdrant_payload 声明最终 Qdrant 字段；理由：未来接入新外部库时不能再为每种字段形态新增 Python 分支。
PAYLOAD_MODE_PROFILE_RENDERED = "profile_rendered"
# 2026-06-12 15:30:17 修改：定义 Qdrant payload 布局契约字段名；作用：把 YAML 的 qdrant_payload 原样带到 chunk 契约；理由：写入层只有 chunk 时也要知道该库的最终字段布局。
PROFILE_QDRANT_PAYLOAD_LAYOUT_KEY = "qdrant_payload_layout"


# 2026-06-11 15:54:56 修改：定义 profile dataclass；作用：把 YAML 转成稳定结构；理由：后续同步层只依赖清晰字段。
@dataclass(frozen=True)
class SourceMappingProfile:
    # 2026-06-11 15:54:56 修改：保存 profile 名称；作用：进入 payload 和日志；理由：多 profile 时需要识别来源策略。
    profile_name: str
    # 2026-06-11 15:54:56 修改：保存来源名称；作用：进入 Qdrant payload；理由：不同库统一写入后要可追溯。
    source_name: str
    # 2026-06-11 15:54:56 修改：保存来源表；作用：进入 Qdrant payload；理由：支持外部库回表定位。
    source_table: str
    # 2026-06-11 15:54:56 修改：保存目标 collection；作用：给 CLI 默认值和排查使用；理由：避免外部库写回主 collection。
    target_collection: str
    # 2026-06-13 17:18:04 新增：保存外部库连接配置；作用：让 SQL Server/PG/MySQL 等连接信息都从 YAML 读取；理由：后续外部库不能再靠 Python 分支硬编码。
    connection: dict[str, Any]
    # 2026-06-13 17:18:04 新增：保存实时同步配置；作用：让轮询间隔、状态回写、删除策略都由 YAML 声明；理由：后台同步 worker 要以不变代码适配不同外部库。
    sync: dict[str, Any]
    # 2026-06-12 14:40:11 修改：保存 Qdrant payload 输出模式；作用：让每个 source profile 决定 legacy_qa 或 profile_strict；理由：外部库必须隔离旧 QA 字段。
    payload_mode: str
    # 2026-06-12 15:30:17 修改：保存 Qdrant payload 布局；作用：让 YAML 决定顶层字段、嵌套对象和索引；理由：程序只做通用解释器，不按外部库写死字段。
    qdrant_payload_layout: dict[str, Any]
    # 2026-06-11 15:54:56 修改：保存主键字段；作用：生成 source_pk 和稳定 chunk_id；理由：外部库行必须有稳定标识。
    id_field: str
    # 2026-06-11 15:54:56 修改：保存契约模式；作用：选择 strict QA 或 generic 校验；理由：不同数据源文本结构不同。
    contract_mode: str
    # 2026-06-11 15:54:56 修改：保存 SQL 读取字段；作用：外部 adapter 动态生成 SELECT；理由：字段选择不能写死。
    select_fields: tuple[str, ...]
    # 2026-06-11 15:54:56 修改：保存向量化字段；作用：动态生成 embedding_text；理由：不同库召回字段不同。
    embedding_fields: tuple[str, ...]
    # 2026-06-11 15:54:56 修改：保存向量字段拼接符；作用：多字段向量化时保持格式可控；理由：避免字段无序拼接。
    embedding_joiner: str
    # 2026-06-11 15:54:56 修改：保存向量模板；作用：支持复杂 embedding_text 格式；理由：后续外部库可能需要带标签拼接。
    embedding_template: str
    # 2026-06-11 15:54:56 修改：保存 prompt 字段；作用：动态生成模型正文；理由：避免全量 payload 噪声。
    prompt_fields: tuple[str, ...]
    # 2026-06-11 15:54:56 修改：保存 prompt 拼接符；作用：无模板时稳定拼接；理由：保持输出可预测。
    prompt_joiner: str
    # 2026-06-11 15:54:56 修改：保存 prompt 模板；作用：生成 LlamaIndex 默认 text 正文；理由：外部消费者应只读干净 text。
    prompt_template: str
    # 2026-06-11 15:54:56 修改：保存 payload 字段；作用：动态保留外部业务字段；理由：不参与向量化的字段也要可展示。
    payload_include: tuple[str, ...]
    # 2026-06-11 15:54:56 修改：保存 keyword index 字段；作用：动态补齐 Qdrant KEYWORD index；理由：不同外部库过滤字段不同。
    keyword_index_fields: tuple[str, ...]
    # 2026-06-11 15:54:56 修改：保存 text index 字段；作用：动态补齐 Qdrant TEXT index；理由：不同外部库全文调试字段不同。
    text_index_fields: tuple[str, ...]
    # 2026-06-12 09:52:34 修改：保存 Qdrant 向量输出模式；作用：让 profile 决定 dense-only 或 hybrid；理由：不能再靠人工记 --enable-hybrid。
    qdrant_vector_mode: str
    # 2026-06-12 09:52:34 修改：保存 Qdrant dense 向量名；作用：创建和写入命名 dense vector；理由：LlamaIndex hybrid 默认使用 text-dense。
    qdrant_dense_vector_name: str
    # 2026-06-12 09:52:34 修改：保存 Qdrant sparse 向量名；作用：创建和写入命名 sparse vector；理由：LlamaIndex hybrid 默认使用 text-sparse-new。
    qdrant_sparse_vector_name: str
    # 2026-06-12 09:52:34 修改：保存 Qdrant sparse 编码模型；作用：把 Qdrant/bm25 从 profile 传到文档侧 encoder；理由：对齐外部 fastembed_sparse_model="Qdrant/bm25"。
    qdrant_fastembed_sparse_model: str


# 2026-06-11 15:54:56 修改：定义安全模板字典；作用：缺字段时返回空字符串；理由：外部库字段不完整时不要抛 KeyError 中断排查。
class SafeFormatDict(dict[str, str]):
    # 2026-06-11 15:54:56 修改：覆盖缺省读取；作用：模板缺字段时兜底为空；理由：profile 校验会单独报告缺文本。
    def __missing__(self, key: str) -> str:
        # 2026-06-11 15:54:56 修改：返回空值；作用：避免模板渲染硬失败；理由：让后续校验给出更明确业务错误。
        return ""


# 2026-06-11 15:54:56 修改：规范化 profile 名称；作用：从库名推导默认 profile；理由：CLI 不传 profile 时也能稳定落到 getai 或外部库。
def normalize_profile_name(raw_name: str) -> str:
    # 2026-06-11 15:54:56 修改：统一小写并替换非字母数字；作用：兼容 External_database 和 external-database 写法；理由：命令行输入不可控。
    normalized = "".join(character.lower() if character.isalnum() else "_" for character in str(raw_name or "").strip())
    # 2026-06-11 15:54:56 修改：折叠连续下划线；作用：生成稳定 profile 文件名；理由：避免不同输入命中不同文件。
    while "__" in normalized:
        # 2026-06-11 15:54:56 修改：替换重复下划线；作用：保持文件名简洁；理由：方便排查。
        normalized = normalized.replace("__", "_")
    # 2026-06-11 15:54:56 修改：去掉首尾下划线并兜底；作用：返回可用 profile 名；理由：空值必须回到默认 getai。
    return normalized.strip("_") or DEFAULT_SOURCE_PROFILE_NAME


# 2026-06-11 15:54:56 修改：根据数据库名选择默认 profile；作用：外部 demo 自动走 external_database；理由：不让 External_database 误用 getai 配置。
def default_profile_name_for_database(database_name: str) -> str:
    # 2026-06-11 15:54:56 修改：规范化数据库名；作用：兼容大小写和特殊字符；理由：SQL Server 库名输入可能不同。
    normalized_database = normalize_profile_name(database_name)
    # 2026-06-11 15:54:56 修改：判断 External_database；作用：自动使用外部库 profile；理由：用户明确指定该模拟库独立配置。
    if normalized_database == "external_database":
        # 2026-06-11 15:54:56 修改：返回外部库 profile；作用：避免走固定 QA 模板；理由：外部库只用 standard_question 向量化。
        return "external_database"
    # 2026-06-11 15:54:56 修改：默认返回 getai profile；作用：保护现有主库同步；理由：不传配置时必须保持原行为。
    return DEFAULT_SOURCE_PROFILE_NAME


# 2026-06-11 15:54:56 修改：解析 profile 路径；作用：支持名称或完整文件路径；理由：后续接新外部库时可指定自定义配置。
def resolve_profile_path(profile_name_or_path: str | None, database_name: str = "") -> Path:
    # 2026-06-11 15:54:56 修改：选择有效 profile 名；作用：空值时按数据库名推导；理由：兼容现有 CLI 默认行为。
    selected_profile = profile_name_or_path or default_profile_name_for_database(database_name)
    # 2026-06-11 15:54:56 修改：构造 Path 对象；作用：判断调用方是否传入文件路径；理由：允许 profile 放在默认目录以外。
    raw_path = Path(str(selected_profile))
    # 2026-06-11 15:54:56 修改：如果文件存在直接返回；作用：支持绝对路径或相对路径；理由：便于临时验证外部库配置。
    if raw_path.exists():
        # 2026-06-11 15:54:56 修改：返回显式文件路径；作用：尊重调用方输入；理由：不强制放在 source_profiles。
        return raw_path
    # 2026-06-11 15:54:56 修改：规范化 profile 文件名；作用：把 External_database 映射到 external_database.yml；理由：避免大小写差异。
    normalized_profile = normalize_profile_name(str(selected_profile))
    # 2026-06-11 15:54:56 修改：返回默认 profile 文件路径；作用：集中读取 data_cleaning/source_profiles；理由：不新增散落配置。
    return SOURCE_PROFILES_DIR / f"{normalized_profile}.yml"


# 2026-06-11 15:54:56 修改：把 YAML 列表字段转 tuple；作用：dataclass 使用不可变结构；理由：防止运行中被误改。
def tuple_from_config(section: dict[str, Any], key: str) -> tuple[str, ...]:
    # 2026-06-11 15:54:56 修改：读取原始字段；作用：兼容缺省配置；理由：不是所有 profile 都需要每个 section。
    raw_value = section.get(key, [])
    # 2026-06-11 15:54:56 修改：单字符串转列表；作用：允许简写配置；理由：降低后续外部库接入成本。
    if isinstance(raw_value, str):
        # 2026-06-11 15:54:56 修改：返回单字段 tuple；作用：保持下游统一处理；理由：避免分支判断。
        return (raw_value,)
    # 2026-06-11 15:54:56 修改：列表转字符串 tuple；作用：过滤空项；理由：Qdrant payload 字段名不能为空。
    return tuple(str(item).strip() for item in raw_value if str(item).strip())


# 2026-06-11 15:54:56 修改：加载 source profile；作用：把 YAML 转成 SourceMappingProfile；理由：同步层只消费结构化配置。
def load_source_profile(profile_name_or_path: str | None = None, database_name: str = "") -> SourceMappingProfile:
    # 2026-06-11 15:54:56 修改：解析 profile 路径；作用：支持默认、名称、文件路径三种用法；理由：兼容主库和外部库。
    profile_path = resolve_profile_path(profile_name_or_path, database_name)
    # 2026-06-11 15:54:56 修改：检查 profile 是否存在；作用：提前给出明确错误；理由：避免后续同步误用默认字段。
    if not profile_path.exists():
        # 2026-06-11 15:54:56 修改：抛出文件不存在异常；作用：阻断错误同步；理由：字段策略缺失时不能猜。
        raise FileNotFoundError(f"source profile 不存在：{profile_path}")
    # 2026-06-11 15:54:56 修改：读取 YAML 原文；作用：加载字段映射配置；理由：profile 是数据源字段策略的唯一入口。
    raw_config = yaml.safe_load(profile_path.read_text(encoding="utf-8")) or {}
    # 2026-06-11 15:54:56 修改：读取 select section；作用：外部 adapter 动态生成 SELECT；理由：不同外部库字段不同。
    select_section = raw_config.get("select") or {}
    # 2026-06-11 15:54:56 修改：读取 embedding section；作用：生成 embedding_text；理由：召回字段必须配置化。
    embedding_section = raw_config.get("embedding") or {}
    # 2026-06-11 15:54:56 修改：读取 prompt section；作用：生成 prompt_text；理由：模型正文必须配置化。
    prompt_section = raw_config.get("prompt_text") or {}
    # 2026-06-11 15:54:56 修改：读取 payload section；作用：保留业务字段；理由：metadata 字段必须配置化。
    payload_section = raw_config.get("payload") or {}
    # 2026-06-11 15:54:56 修改：读取 keyword index section；作用：动态创建 KEYWORD index；理由：过滤字段因库而异。
    keyword_index_section = raw_config.get("keyword_index") or {}
    # 2026-06-11 15:54:56 修改：读取 text index section；作用：动态创建 TEXT index；理由：全文调试字段因库而异。
    text_index_section = raw_config.get("text_index") or {}
    # 2026-06-12 09:52:34 修改：读取 qdrant section；作用：让每个数据源独立声明 dense/hybrid 输出形态；理由：外部库和主库不能共用一个硬编码向量结构。
    qdrant_section = raw_config.get("qdrant") or {}
    # 2026-06-13 17:18:04 新增：读取 connection section；作用：外部库引擎、主机、端口、账号全部进入 profile；理由：SQL Server/PG 不能各写一套入口。
    connection_section = raw_config.get("connection") or {}
    # 2026-06-13 17:18:04 新增：兜底 connection 类型；作用：错误 YAML 不让 dataclass 类型漂移；理由：同步 worker 只消费 dict。
    if not isinstance(connection_section, dict):
        # 2026-06-13 17:18:04 新增：把非法 connection 降为空字典；作用：保留主库兼容；理由：后续校验给出明确配置错误。
        connection_section = {}
    # 2026-06-13 17:18:04 新增：读取 sync section；作用：后台同步策略由 YAML 管理；理由：不同外部库的状态字段和删除策略不同。
    sync_section = raw_config.get("sync") or {}
    # 2026-06-13 17:18:04 新增：兜底 sync 类型；作用：避免非 dict 配置破坏 worker；理由：主库 profile 没有 sync 时必须安全。
    if not isinstance(sync_section, dict):
        # 2026-06-13 17:18:04 新增：把非法 sync 降为空字典；作用：保持 SourceMappingProfile 稳定；理由：配置错误应可诊断。
        sync_section = {}
    # 2026-06-12 15:30:17 修改：读取 qdrant_payload section；作用：让 YAML 声明最终 Qdrant payload 结构；理由：不同外部库顶层字段和嵌套字段千变万化，不能靠 Python 分支枚举。
    qdrant_payload_layout = raw_config.get("qdrant_payload") or {}
    # 2026-06-12 15:30:17 修改：防御非字典布局配置；作用：错误 YAML 不会把同步层拖进类型异常；理由：后续校验会按空布局给出更清晰的失败结果。
    if not isinstance(qdrant_payload_layout, dict):
        # 2026-06-12 15:30:17 修改：非字典布局降为空字典；作用：保持 SourceMappingProfile 类型稳定；理由：配置入口必须有安全兜底。
        qdrant_payload_layout = {}
    # 2026-06-11 15:54:56 修改：构造 profile 对象；作用：把原始 YAML 固化成类型化配置；理由：下游不直接碰 YAML 字典。
    return SourceMappingProfile(
        # 2026-06-11 15:54:56 修改：写入 profile 名称；作用：payload 和日志可见；理由：多 profile 排查需要。
        profile_name=str(raw_config.get("profile_name") or profile_path.stem),
        # 2026-06-11 15:54:56 修改：写入来源名；作用：Qdrant payload 可追溯；理由：多数据源统一写入。
        source_name=str(raw_config.get("source_name") or profile_path.stem),
        # 2026-06-11 15:54:56 修改：写入来源表；作用：支持回表；理由：外部库必须保留来源表。
        source_table=str(raw_config.get("source_table") or ""),
        # 2026-06-11 15:54:56 修改：写入目标 collection；作用：给 CLI 默认和排查使用；理由：避免写错库。
        target_collection=str(raw_config.get("target_collection") or ""),
        # 2026-06-13 17:18:04 新增：写入连接配置副本；作用：worker 和 adapter registry 可以统一读取 engine/env；理由：不在业务逻辑里写 PG/SQLServer 死分支。
        connection=dict(connection_section),
        # 2026-06-13 17:18:04 新增：写入同步配置副本；作用：worker 获取 interval/status/delete/hash 策略；理由：实时同步行为必须跟着 YAML 走。
        sync=dict(sync_section),
        # 2026-06-12 14:40:11 修改：写入 payload 模式；作用：控制 Qdrant point 顶层字段输出；理由：外部库严格隔离，getai 保持旧 payload。
        payload_mode=str(raw_config.get("payload_mode") or PAYLOAD_MODE_LEGACY_QA).strip().lower(),
        # 2026-06-12 15:30:17 修改：写入 Qdrant payload 布局；作用：让写入层按 YAML 渲染最终字段；理由：一库一配置，一库一结构，程序不再关心库的字段形态。
        qdrant_payload_layout=qdrant_payload_layout,
        # 2026-06-11 15:54:56 修改：写入主键字段；作用：生成 source_pk；理由：point 必须稳定。
        id_field=str(raw_config.get("id_field") or "chunk_id"),
        # 2026-06-11 15:54:56 修改：写入契约模式；作用：控制校验强度；理由：QA 主库和外部泛化库不同。
        contract_mode=str(raw_config.get("contract_mode") or "qa"),
        # 2026-06-11 15:54:56 修改：写入 SELECT 字段；作用：外部库读取层可用；理由：字段不写死。
        select_fields=tuple_from_config(select_section, "fields"),
        # 2026-06-11 15:54:56 修改：写入向量字段；作用：生成 embedding_text；理由：字段策略配置化。
        embedding_fields=tuple_from_config(embedding_section, "fields"),
        # 2026-06-11 15:54:56 修改：写入向量拼接符；作用：多字段可控拼接；理由：不让字段无序混杂。
        embedding_joiner=str(embedding_section.get("joiner", "\n")),
        # 2026-06-11 15:54:56 修改：写入向量模板；作用：支持复杂文本格式；理由：后续扩展不改代码。
        embedding_template=str(embedding_section.get("template", "")),
        # 2026-06-11 15:54:56 修改：写入 prompt 字段；作用：生成 prompt_text；理由：避免全 payload 入 prompt。
        prompt_fields=tuple_from_config(prompt_section, "fields"),
        # 2026-06-11 15:54:56 修改：写入 prompt 拼接符；作用：无模板时可控拼接；理由：保持通用格式。
        prompt_joiner=str(prompt_section.get("joiner", "\n")),
        # 2026-06-11 15:54:56 修改：写入 prompt 模板；作用：生成干净正文；理由：外部消费应读 text。
        prompt_template=str(prompt_section.get("template", "")),
        # 2026-06-11 15:54:56 修改：写入 payload 字段；作用：保留业务 metadata；理由：字段保留由 profile 决定。
        payload_include=tuple_from_config(payload_section, "include"),
        # 2026-06-11 15:54:56 修改：写入 keyword index 字段；作用：动态建 KEYWORD index；理由：不同库过滤字段不同。
        keyword_index_fields=tuple_from_config(keyword_index_section, "fields"),
        # 2026-06-11 15:54:56 修改：写入 text index 字段；作用：动态建 TEXT index；理由：全文字段也应配置化。
        text_index_fields=tuple_from_config(text_index_section, "fields"),
        # 2026-06-12 09:52:34 修改：写入 Qdrant 输出模式；作用：同步层可据此自动开启 hybrid；理由：修复实际落库忘记 --enable-hybrid 的根因。
        qdrant_vector_mode=str(qdrant_section.get("vector_mode") or QDRANT_VECTOR_MODE_DENSE).strip().lower(),
        # 2026-06-12 09:52:34 修改：写入 dense 向量名；作用：保证 profile 驱动的 collection schema 和 point vector 同名；理由：外部 LlamaIndex 默认查 text-dense。
        qdrant_dense_vector_name=str(qdrant_section.get("dense_vector_name") or DEFAULT_QDRANT_DENSE_VECTOR_NAME).strip(),
        # 2026-06-12 09:52:34 修改：写入 sparse 向量名；作用：保证 profile 驱动的 collection schema 和 point vector 同名；理由：外部 LlamaIndex 默认查 text-sparse-new。
        qdrant_sparse_vector_name=str(qdrant_section.get("sparse_vector_name") or DEFAULT_QDRANT_SPARSE_VECTOR_NAME).strip(),
        # 2026-06-12 09:52:34 修改：写入 sparse 模型名；作用：后续 sparse encoder 按 profile 选择 Qdrant/bm25；理由：和别人 fastembed_sparse_model 参数保持一致。
        qdrant_fastembed_sparse_model=str(qdrant_section.get("fastembed_sparse_model") or DEFAULT_QDRANT_FASTEMBED_SPARSE_MODEL).strip(),
    )


# 2026-06-11 15:54:56 修改：读取对象单层字段；作用：支持 dict、pyodbc.Row、CanonicalChunk；理由：profile 解析器要服务多来源。
def read_single_value(container: Any, field_name: str, default: Any = "") -> Any:
    # 2026-06-11 15:54:56 修改：空容器直接返回默认值；作用：避免 None 报错；理由：外部库字段可能缺失。
    if container is None:
        # 2026-06-11 15:54:56 修改：返回默认值；作用：保持字段读取稳定；理由：缺字段由校验阶段处理。
        return default
    # 2026-06-11 15:54:56 修改：支持 dict 字段读取；作用：测试样例和 JSON payload 可直接读取；理由：EXTERNAL_SAMPLE_ROWS 是 dict。
    if isinstance(container, dict):
        # 2026-06-11 15:54:56 修改：从字典取值；作用：读取原始字段；理由：字段名来自 profile。
        return container.get(field_name, default)
    # 2026-06-11 15:54:56 修改：支持对象属性读取；作用：兼容 CanonicalChunk 和 pyodbc.Row；理由：SQL 查询返回对象式字段。
    if hasattr(container, field_name):
        # 2026-06-11 15:54:56 修改：返回对象属性；作用：读取生产 dataclass 字段；理由：不复制业务对象。
        return getattr(container, field_name)
    # 2026-06-11 15:54:56 修改：读取 payload_json 字段；作用：兼容已清洗入库的新契约字段；理由：retrieval_text/llm_text 可能来自 payload_json。
    payload_json = getattr(container, "payload_json", None)
    # 2026-06-11 15:54:56 修改：判断 payload_json 是否为 dict；作用：避免非结构化值报错；理由：历史数据可能为空。
    if isinstance(payload_json, dict):
        # 2026-06-11 15:54:56 修改：从 payload_json 取值；作用：让 profile 能读取扩展字段；理由：不修改 SQL 表结构。
        return payload_json.get(field_name, default)
    # 2026-06-11 15:54:56 修改：兜底返回默认值；作用：字段缺失时不中断；理由：后续文本校验会报业务错误。
    return default


# 2026-06-11 15:54:56 修改：读取字段值；作用：支持 evidence.customer_text 这类点号路径；理由：外部 payload 可能是嵌套结构。
def row_value(row: Any, field_name: str, default: Any = "") -> Any:
    # 2026-06-11 15:54:56 修改：拆分点号路径；作用：逐层读取嵌套字段；理由：配置层要支持复杂外部结构。
    parts = [part for part in str(field_name).split(".") if part]
    # 2026-06-11 15:54:56 修改：空字段名直接返回默认值；作用：防止配置误填；理由：字段名不能为空。
    if not parts:
        # 2026-06-11 15:54:56 修改：返回默认值；作用：保持读取稳定；理由：避免无意义字段进入 payload。
        return default
    # 2026-06-11 15:54:56 修改：初始化当前读取对象；作用：从 row 开始逐层深入；理由：兼容嵌套 payload。
    current_value = row
    # 2026-06-11 15:54:56 修改：逐层读取字段；作用：支持 dict/object 混合结构；理由：pyodbc.Row 和 dict 都可能出现。
    for part in parts:
        # 2026-06-11 15:54:56 修改：读取当前层字段；作用：推进点号路径；理由：统一字段访问。
        current_value = read_single_value(current_value, part, None)
        # 2026-06-11 15:54:56 修改：遇到空值就返回默认值；作用：避免继续读取报错；理由：外部字段可能缺失。
        if current_value is None:
            # 2026-06-11 15:54:56 修改：返回默认值；作用：缺字段不中断；理由：校验层统一判断是否可同步。
            return default
    # 2026-06-11 15:54:56 修改：返回读取结果；作用：给文本和 payload 构造使用；理由：字段访问已完成。
    return current_value


# 2026-06-11 15:54:56 修改：规范化文本；作用：把字段值变成可拼接字符串；理由：embedding 和 prompt 都需要文本。
def normalize_text(value: Any) -> str:
    # 2026-06-11 15:54:56 修改：None 转空字符串；作用：避免字符串里出现 None；理由：外部库字段可能为空。
    if value is None:
        # 2026-06-11 15:54:56 修改：返回空字符串；作用：保持拼接干净；理由：空字段不应污染文本。
        return ""
    # 2026-06-11 15:54:56 修改：日期时间转 ISO 字符串；作用：可读且可 JSON 化；理由：SQL Server datetime 不能直接进 JSON。
    if isinstance(value, (datetime, date)):
        # 2026-06-11 15:54:56 修改：返回 ISO 格式；作用：保持时间字段稳定；理由：Qdrant payload 展示需要可读。
        return value.isoformat()
    # 2026-06-11 15:54:56 修改：列表转文本；作用：兼容关键词数组；理由：字段可能是 list[str]。
    if isinstance(value, (list, tuple, set)):
        # 2026-06-11 15:54:56 修改：拼接非空子项；作用：避免空值噪声；理由：embedding/prompt 需要干净文本。
        return " ".join(text for text in (normalize_text(item) for item in value) if text)
    # 2026-06-11 15:54:56 修改：字典转 JSON；作用：保留结构信息；理由：嵌套 payload 进入文本时需要可读。
    if isinstance(value, dict):
        # 2026-06-11 15:54:56 修改：序列化字典；作用：避免 Python dict 表示不稳定；理由：Qdrant 调试更清晰。
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    # 2026-06-11 15:54:56 修改：普通值转字符串并去空白；作用：统一文本格式；理由：减少向量化噪声。
    return str(value).strip()


# 2026-06-11 15:54:56 修改：规范化 payload 值；作用：确保可写入 Qdrant payload；理由：Qdrant 不接受任意 Python 对象。
def normalize_payload_value(value: Any) -> Any:
    # 2026-06-11 15:54:56 修改：日期时间转 ISO 字符串；作用：保持 payload 可序列化；理由：SQL datetime 需要转换。
    if isinstance(value, (datetime, date)):
        # 2026-06-11 15:54:56 修改：返回 ISO 时间；作用：兼容 Qdrant payload；理由：避免序列化异常。
        return value.isoformat()
    # 2026-06-11 15:54:56 修改：tuple/set 转 list；作用：Qdrant payload 支持数组；理由：保持结构字段可写。
    if isinstance(value, (tuple, set)):
        # 2026-06-11 15:54:56 修改：递归规范化数组值；作用：处理内部时间或对象；理由：payload 必须干净。
        return [normalize_payload_value(item) for item in value]
    # 2026-06-11 15:54:56 修改：list 递归规范化；作用：保留数组语义；理由：keyword_terms 等字段需要 list。
    if isinstance(value, list):
        # 2026-06-11 15:54:56 修改：递归处理列表项；作用：避免嵌套不可序列化值；理由：Qdrant 写入安全。
        return [normalize_payload_value(item) for item in value]
    # 2026-06-11 15:54:56 修改：dict 递归规范化；作用：保留嵌套 source_payload；理由：外部原始字段需要可追溯。
    if isinstance(value, dict):
        # 2026-06-11 15:54:56 修改：递归处理键值；作用：保证嵌套 payload 可 JSON 化；理由：避免 Qdrant 写入失败。
        return {str(key): normalize_payload_value(inner_value) for key, inner_value in value.items()}
    # 2026-06-11 15:54:56 修改：其他值原样返回；作用：保留字符串、数字、布尔；理由：Qdrant 原生支持这些类型。
    return value


# 2026-06-11 15:54:56 修改：构造字段值字典；作用：给模板 format 使用；理由：模板渲染需要字段名到字符串的映射。
def build_field_text_map(row: Any, fields: tuple[str, ...]) -> dict[str, str]:
    # 2026-06-11 15:54:56 修改：生成字段文本字典；作用：模板和拼接共用；理由：避免重复读取字段。
    return {field: normalize_text(row_value(row, field)) for field in fields}


# 2026-06-11 15:54:56 修改：按 profile 生成文本；作用：统一处理 embedding_text 和 prompt_text；理由：两者都是字段+模板策略。
def build_text_from_profile(row: Any, fields: tuple[str, ...], joiner: str, template: str) -> str:
    # 2026-06-11 15:54:56 修改：构造字段文本映射；作用：给模板和拼接使用；理由：字段读取逻辑统一。
    field_text_map = build_field_text_map(row, fields)
    # 2026-06-11 15:54:56 修改：优先使用模板；作用：支持“问题：{x}\n答案：{y}”格式；理由：prompt 正文应可控。
    if template:
        # 2026-06-11 15:54:56 修改：渲染模板并去空白；作用：得到最终文本；理由：避免模板缺字段导致异常。
        return template.format_map(SafeFormatDict(field_text_map)).strip()
    # 2026-06-11 15:54:56 修改：无模板时按字段顺序拼接；作用：支持纯字段向量化；理由：standard_question 可单独成为 embedding_text。
    return joiner.join(text for text in field_text_map.values() if text).strip()


# 2026-06-11 15:54:56 修改：把字段值转关键词列表；作用：profile keyword_index.fields 需要进入 keyword_terms；理由：Qdrant KEYWORD index 依赖 list[str]。
def value_to_terms(value: Any) -> list[str]:
    # 2026-06-11 15:54:56 修改：None 返回空列表；作用：避免空关键词；理由：过滤字段不能为空。
    if value is None:
        # 2026-06-11 15:54:56 修改：返回空列表；作用：保持 keyword_terms 干净；理由：None 不应进入 Qdrant。
        return []
    # 2026-06-11 15:54:56 修改：列表递归展开；作用：兼容 query_aliases 等数组字段；理由：关键词过滤需要逐项可见。
    if isinstance(value, (list, tuple, set)):
        # 2026-06-11 15:54:56 修改：递归合并数组项；作用：支持嵌套列表；理由：外部字段结构不固定。
        return [term for item in value for term in value_to_terms(item)]
    # 2026-06-11 15:54:56 修改：字符串尝试解析 JSON 列表；作用：兼容旧 keywords 字符串字段；理由：getai 里 keywords 常是 JSON 字符串。
    if isinstance(value, str):
        # 2026-06-11 15:54:56 修改：去掉两侧空白；作用：过滤空字符串；理由：减少 payload 噪声。
        stripped = value.strip()
        # 2026-06-11 15:54:56 修改：空字符串返回空列表；作用：避免空关键词；理由：Qdrant filter 不需要空值。
        if not stripped:
            # 2026-06-11 15:54:56 修改：返回空列表；作用：保持 keyword_terms 干净；理由：空值无过滤意义。
            return []
        # 2026-06-11 15:54:56 修改：判断是否像 JSON；作用：避免普通中文误解析；理由：减少异常分支。
        if stripped.startswith("[") or stripped.startswith("{"):
            # 2026-06-11 15:54:56 修改：捕获 JSON 解析异常；作用：兼容历史脏字符串；理由：关键词解析不应中断同步。
            try:
                # 2026-06-11 15:54:56 修改：解析 JSON；作用：把数组字符串转成多个关键词；理由：兼容旧 payload。
                return value_to_terms(json.loads(stripped))
            # 2026-06-11 15:54:56 修改：解析失败时走普通字符串；作用：保持鲁棒；理由：历史字段可能不是严格 JSON。
            except Exception:
                # 2026-06-11 15:54:56 修改：继续返回原字符串；作用：不丢失字段内容；理由：可见性优先。
                pass
        # 2026-06-11 15:54:56 修改：普通字符串作为单个关键词；作用：保留原值；理由：字段本身可能就是关键词。
        return [stripped]
    # 2026-06-11 15:54:56 修改：其他类型转文本；作用：兼容数字主键等字段；理由：关键词字段可能不是字符串。
    normalized = normalize_text(value)
    # 2026-06-11 15:54:56 修改：非空时返回单项列表；作用：保持 keyword_terms 类型稳定；理由：Qdrant KEYWORD index 需要数组。
    return [normalized] if normalized else []


# 2026-06-11 15:54:56 修改：按字段去重构造 keyword_terms；作用：动态合并 profile 关键词字段；理由：不同库过滤字段不同。
def build_keyword_terms(row: Any, fields: tuple[str, ...]) -> list[str]:
    # 2026-06-11 15:54:56 修改：初始化结果列表；作用：保留字段出现顺序；理由：WebUI 展示更可读。
    terms: list[str] = []
    # 2026-06-11 15:54:56 修改：遍历 profile 字段；作用：按配置读取关键词来源；理由：字段策略不能写死。
    for field in fields:
        # 2026-06-11 15:54:56 修改：读取字段值并展开；作用：兼容字符串、列表、JSON 字符串；理由：各库字段类型不同。
        for term in value_to_terms(row_value(row, field)):
            # 2026-06-11 15:54:56 修改：跳过重复项；作用：减少 payload 噪声；理由：关键词重复不提升过滤能力。
            if term not in terms:
                # 2026-06-11 15:54:56 修改：追加唯一关键词；作用：构造 Qdrant KEYWORD list；理由：字段过滤需要稳定列表。
                terms.append(term)
    # 2026-06-11 15:54:56 修改：返回关键词列表；作用：供 payload 和 sparse/filter 使用；理由：统一输出 list[str]。
    return terms


# 2026-06-11 15:54:56 修改：按 profile 构造 source_payload；作用：保留外部业务字段；理由：payload 字段由 profile 决定。
def build_source_payload(row: Any, profile: SourceMappingProfile) -> dict[str, Any]:
    # 2026-06-11 15:54:56 修改：初始化 payload 字典；作用：按 include 字段填充；理由：不把全量未知字段都塞进 Qdrant。
    payload: dict[str, Any] = {}
    # 2026-06-11 15:54:56 修改：遍历配置字段；作用：按顺序保存；理由：WebUI 展示和测试都更稳定。
    for field in profile.payload_include:
        # 2026-06-11 15:54:56 修改：读取字段原始值；作用：保留数字、布尔、时间等类型；理由：payload 不一定只需要字符串。
        raw_value = row_value(row, field)
        # 2026-06-11 15:54:56 修改：写入规范化值；作用：避免不可序列化对象；理由：Qdrant payload 写入需要安全类型。
        payload[field] = normalize_payload_value(raw_value)
    # 2026-06-11 15:54:56 修改：返回 source_payload；作用：作为 Qdrant payload 的嵌套字段；理由：外部原始字段可追溯。
    return payload


# 2026-06-12 15:30:17 修改：读取 YAML 渲染上下文中的字段；作用：支持 qdrant_payload.top_level 的 from 表达式；理由：外部库顶层字段必须由配置取值。
def read_qdrant_payload_layout_value(source_path: Any, render_context: dict[str, Any], default: Any = "") -> Any:
    # 2026-06-12 15:30:17 修改：规范化来源表达式；作用：兼容 from 缺省或非字符串；理由：YAML 配置需要防御式读取。
    normalized_source_path = normalize_text(source_path)
    # 2026-06-12 15:30:17 修改：空来源直接返回默认值；作用：避免误填 from 时抛异常；理由：校验层会捕获缺字段。
    if not normalized_source_path:
        # 2026-06-12 15:30:17 修改：返回默认值；作用：保持渲染器稳定；理由：外部库配置不能让程序崩掉。
        return default
    # 2026-06-12 15:30:17 修改：支持直接读取特殊上下文字段；作用：from: embedding_text/prompt_text/keyword_terms 可直接生效；理由：这些不是原始 payload 字段。
    if normalized_source_path in render_context:
        # 2026-06-12 15:30:17 修改：返回上下文字段值；作用：让 YAML 能引用向量文本等派生结果；理由：当前 sql_External_database 需要 retrieval_text 来自 embedding_text。
        return render_context.get(normalized_source_path, default)
    # 2026-06-12 15:30:17 修改：支持 payload.xxx 路径；作用：顶层字段可从打包 payload 中提升；理由：未来外部库可能需要 tenant_id/supplier_code 顶层过滤。
    if normalized_source_path.startswith("payload."):
        # 2026-06-12 15:30:17 修改：截取 payload 内部路径；作用：复用 row_value 支持嵌套读取；理由：payload 可能有多层结构。
        payload_path = normalized_source_path[len("payload.") :]
        # 2026-06-12 15:30:17 修改：从 source_payload 读取；作用：按 YAML 选择业务字段；理由：顶层字段不再写死。
        return row_value(render_context.get("payload", {}), payload_path, default)
    # 2026-06-12 15:30:17 修改：支持 chunk.xxx 路径；作用：需要时可从 CanonicalChunk 读取兼容字段；理由：少数外部库可能仍要暴露 document_id 等内部字段。
    if normalized_source_path.startswith("chunk."):
        # 2026-06-12 15:30:17 修改：截取 chunk 内部路径；作用：复用对象属性读取；理由：CanonicalChunk 是 dataclass。
        chunk_path = normalized_source_path[len("chunk.") :]
        # 2026-06-12 15:30:17 修改：从 chunk 读取字段；作用：未来 YAML 可显式声明保留内部字段；理由：程序不再自动补字段，但配置可选择。
        return row_value(render_context.get("chunk"), chunk_path, default)
    # 2026-06-12 15:30:17 修改：默认按 payload 字段读取；作用：简化 from: id 这类写法；理由：大多数外部字段都来自打包 payload。
    return row_value(render_context.get("payload", {}), normalized_source_path, default)


# 2026-06-12 15:30:17 修改：从 YAML 字段条目读取输出键名和来源路径；作用：同时支持字符串字段和 {key, from} 映射；理由：未来外部库字段布局需要灵活重命名。
def parse_qdrant_payload_layout_field_entry(field_entry: Any, default_prefix: str = "payload.") -> tuple[str, Any, Any]:
    # 2026-06-12 15:30:17 修改：处理字典条目；作用：支持 key/from/default 完整配置；理由：顶层字段和嵌套对象都可能需要重命名。
    if isinstance(field_entry, dict):
        # 2026-06-12 15:30:17 修改：读取输出 key；作用：决定 Qdrant payload 中的字段名；理由：字段名必须由 YAML 声明。
        output_key = normalize_text(field_entry.get("key"))
        # 2026-06-12 15:30:17 修改：读取来源路径；作用：决定值从哪里来；理由：同一个字段名可能来自 embedding_text/payload/chunk。
        source_path = field_entry.get("from") or output_key
        # 2026-06-12 15:30:17 修改：读取默认值；作用：缺字段时保持可控输出；理由：外部库字段可能为空。
        default_value = field_entry.get("default", "")
        # 2026-06-12 15:30:17 修改：返回解析结果；作用：供渲染器统一消费；理由：避免多处重复解析 YAML。
        return output_key, source_path, default_value
    # 2026-06-12 15:30:17 修改：处理字符串条目；作用：兼容 include: [id, name] 简写；理由：常见外部库不需要冗长映射。
    output_key = normalize_text(field_entry)
    # 2026-06-12 15:30:17 修改：按默认前缀生成来源路径；作用：对象 include 默认从 payload 读取；理由：payload 对象字段最常见。
    source_path = f"{default_prefix}{output_key}" if default_prefix and output_key and "." not in output_key else output_key
    # 2026-06-12 15:30:17 修改：返回简写解析结果；作用：统一给渲染器处理；理由：减少分支。
    return output_key, source_path, ""


# 2026-06-12 15:30:17 修改：按 YAML 字段列表渲染一个对象；作用：支持 qdrant_payload.objects.payload.include；理由：不同外部库打包字段完全由配置决定。
def render_qdrant_payload_object_from_layout(field_entries: Any, render_context: dict[str, Any]) -> dict[str, Any]:
    # 2026-06-12 15:30:17 修改：初始化对象 payload；作用：保存当前对象的字段；理由：对象字段不能摊平成顶层。
    rendered_object: dict[str, Any] = {}
    # 2026-06-12 15:30:17 修改：确保字段条目可遍历；作用：兼容 include 缺省；理由：YAML 可选择不声明对象字段。
    entries = field_entries if isinstance(field_entries, list) else []
    # 2026-06-12 15:30:17 修改：逐个渲染字段条目；作用：按 YAML 顺序输出；理由：WebUI 展示和测试都更稳定。
    for field_entry in entries:
        # 2026-06-12 15:30:17 修改：解析对象字段条目；作用：获得输出 key、来源路径和默认值；理由：支持字符串和字典两种写法。
        output_key, source_path, default_value = parse_qdrant_payload_layout_field_entry(field_entry, "payload.")
        # 2026-06-12 15:30:17 修改：跳过空 key；作用：避免空字段污染 Qdrant payload；理由：配置错误不应产生无意义字段。
        if not output_key:
            # 2026-06-12 15:30:17 修改：继续下一项；作用：保持渲染器宽容；理由：让校验集中处理真正缺失字段。
            continue
        # 2026-06-12 15:30:17 修改：读取字段值；作用：从 payload/embedding/chunk 上下文取值；理由：对象字段也可能需要重命名或派生。
        raw_value = read_qdrant_payload_layout_value(source_path, render_context, default_value)
        # 2026-06-12 15:30:17 修改：写入规范化字段值；作用：保证 Qdrant 可序列化；理由：SQL datetime 等对象不能原样写入。
        rendered_object[output_key] = normalize_payload_value(raw_value)
    # 2026-06-12 15:30:17 修改：返回渲染对象；作用：供顶层 payload 使用；理由：对象字段配置化完成。
    return rendered_object


# 2026-06-12 15:30:17 修改：按 YAML qdrant_payload 布局渲染最终 Qdrant payload；作用：统一控制顶层字段、嵌套对象和派生字段；理由：程序只做解释器，未来外部库只改 YAML。
def render_qdrant_payload_from_layout(chunk: Any, qdrant_payload_layout: Any, embedding_text: str, prompt_text: str, source_payload: dict[str, Any], keyword_terms: list[str]) -> dict[str, Any]:
    # 2026-06-12 15:30:17 修改：规范化布局对象；作用：防御 payload_json 中的异常类型；理由：外部配置需要安全兜底。
    layout = qdrant_payload_layout if isinstance(qdrant_payload_layout, dict) else {}
    # 2026-06-12 15:30:17 修改：构造渲染上下文；作用：集中暴露 YAML 可引用的数据源；理由：from 表达式不能直接碰同步层内部变量。
    render_context = {
        # 2026-06-12 15:30:17 修改：暴露向量文本；作用：支持 from: embedding_text；理由：当前外部库 retrieval_text 必须等于 standard_question + id。
        "embedding_text": embedding_text,
        # 2026-06-12 15:30:17 修改：暴露 prompt 文本；作用：需要时可显式存 text；理由：是否保留 text 应由 YAML 决定。
        "prompt_text": prompt_text,
        # 2026-06-12 15:30:17 修改：暴露嵌套业务 payload；作用：支持 payload.xxx 读取；理由：外部库字段主要来自 YAML include。
        "payload": source_payload,
        # 2026-06-12 15:30:17 修改：暴露关键词列表；作用：未来库可显式声明 keyword_terms 顶层；理由：当前库不声明就不输出。
        "keyword_terms": keyword_terms,
        # 2026-06-12 15:30:17 修改：暴露原 chunk；作用：未来库可显式引用 chunk.document_id 等内部字段；理由：不自动补字段但保留配置能力。
        "chunk": chunk,
    }
    # 2026-06-12 15:30:17 修改：初始化最终 payload；作用：只写 YAML 声明的顶层字段；理由：deny_extra_top_level 要求不自动补字段。
    rendered_payload: dict[str, Any] = {}
    # 2026-06-12 15:30:17 修改：读取顶层字段布局；作用：决定 Qdrant payload 顶层长什么样；理由：顶层字段必须完全由 YAML 控制。
    top_level_entries = layout.get("top_level") if isinstance(layout.get("top_level"), list) else []
    # 2026-06-12 15:30:17 修改：逐项渲染顶层字段；作用：支持 retrieval_text、tenant_id 等任意顶层字段；理由：一万个外部库也不需要新增程序分支。
    for field_entry in top_level_entries:
        # 2026-06-12 15:30:17 修改：解析顶层字段条目；作用：获得输出 key、来源路径和默认值；理由：顶层字段可能来自 embedding_text 或 payload.xxx。
        output_key, source_path, default_value = parse_qdrant_payload_layout_field_entry(field_entry, "")
        # 2026-06-12 15:30:17 修改：跳过空 key；作用：避免无效顶层字段；理由：配置错误不应污染 Qdrant。
        if not output_key:
            # 2026-06-12 15:30:17 修改：继续下一项；作用：保持渲染器健壮；理由：让后续 verify 报缺字段。
            continue
        # 2026-06-12 15:30:17 修改：读取顶层字段值；作用：按 from 表达式取值；理由：YAML 是字段布局唯一来源。
        raw_value = read_qdrant_payload_layout_value(source_path, render_context, default_value)
        # 2026-06-12 15:30:17 修改：写入规范化顶层值；作用：保证 Qdrant 可写；理由：时间和复杂对象需要转成安全类型。
        rendered_payload[output_key] = normalize_payload_value(raw_value)
    # 2026-06-12 15:30:17 修改：读取对象布局；作用：支持 payload、metadata 等任意嵌套对象；理由：未来外部库可能有多个打包对象。
    object_layouts = layout.get("objects") if isinstance(layout.get("objects"), dict) else {}
    # 2026-06-12 15:30:17 修改：逐个渲染嵌套对象；作用：把 include 字段打包进指定对象名；理由：业务字段不能自动摊平成顶层。
    for object_name, object_config in object_layouts.items():
        # 2026-06-12 15:30:17 修改：规范化对象名；作用：避免空对象名进入 payload；理由：Qdrant 顶层字段名必须明确。
        normalized_object_name = normalize_text(object_name)
        # 2026-06-12 15:30:17 修改：跳过空对象名；作用：保持最终 payload 干净；理由：配置错误不应生成无意义字段。
        if not normalized_object_name:
            # 2026-06-12 15:30:17 修改：继续下一对象；作用：防御错误 YAML；理由：同步不应被空 key 打断。
            continue
        # 2026-06-12 15:30:17 修改：读取对象 include 列表；作用：兼容 objects.payload.include 写法；理由：截图方案用 include 声明打包字段。
        include_entries = object_config.get("include") if isinstance(object_config, dict) else object_config
        # 2026-06-12 15:30:17 修改：渲染嵌套对象；作用：按 YAML include 输出字段；理由：不同外部库 payload 内容由配置决定。
        rendered_payload[normalized_object_name] = render_qdrant_payload_object_from_layout(include_entries, render_context)
    # 2026-06-12 15:30:17 修改：返回最终渲染 payload；作用：交给 Qdrant 写入层直接使用；理由：不再追加任何未声明顶层字段。
    return rendered_payload


# 2026-06-11 15:54:56 修改：生成短 hash；作用：补齐外部库内容 hash；理由：外部库跳过原清洗链路时仍需稳定标识。
def stable_hash(*parts: Any) -> str:
    # 2026-06-11 15:54:56 修改：拼接 hash 输入；作用：避免字段边界混淆；理由：不同字段组合要稳定。
    raw_text = "\u241f".join(normalize_text(part) for part in parts)
    # 2026-06-11 15:54:56 修改：返回 SHA256；作用：提供稳定内容 hash；理由：同步状态和排查需要。
    return hashlib.sha256(raw_text.encode("utf-8")).hexdigest()


# 2026-06-11 15:54:56 修改：构造 profile 契约 payload；作用：把动态解析结果写回 chunk.payload_json；理由：现有 Qdrant 写入函数从 chunk 读取。
def build_profile_contract(row: Any, profile: SourceMappingProfile) -> dict[str, Any]:
    # 2026-06-11 15:54:56 修改：生成向量文本；作用：后续 embedding 直接使用；理由：外部库向量字段由 profile 决定。
    embedding_text = build_text_from_profile(row, profile.embedding_fields, profile.embedding_joiner, profile.embedding_template)
    # 2026-06-11 15:54:56 修改：生成 prompt 文本；作用：后续 Qdrant payload text 使用；理由：模型正文由 profile 决定。
    prompt_text = build_text_from_profile(row, profile.prompt_fields, profile.prompt_joiner, profile.prompt_template)
    # 2026-06-11 15:54:56 修改：生成 source_payload；作用：保留外部业务字段；理由：metadata 不应硬编码。
    source_payload = build_source_payload(row, profile)
    # 2026-06-11 15:54:56 修改：生成 profile 关键词；作用：补充 Qdrant keyword_terms；理由：字段过滤由 profile 决定。
    keyword_terms = build_keyword_terms(row, profile.keyword_index_fields)
    # 2026-06-11 15:54:56 修改：读取来源主键；作用：生成 source_pk；理由：外部库回表定位需要。
    source_pk = normalize_text(row_value(row, profile.id_field))
    # 2026-06-11 15:54:56 修改：返回契约字典；作用：统一传递到 Qdrant 同步层；理由：不改变现有函数链路。
    return {
        # 2026-06-11 15:54:56 修改：写入 profile 名称；作用：payload 可见；理由：排查字段策略。
        PROFILE_NAME_PAYLOAD_KEY: profile.profile_name,
        # 2026-06-11 15:54:56 修改：写入契约模式；作用：校验函数选择 QA/generic；理由：保护主库严格校验。
        PROFILE_CONTRACT_MODE_KEY: profile.contract_mode,
        # 2026-06-11 15:54:56 修改：写入向量文本；作用：build_embedding_text 优先读取；理由：支持外部库只用 standard_question。
        PROFILE_EMBEDDING_TEXT_KEY: embedding_text,
        # 2026-06-11 15:54:56 修改：写入 prompt 文本；作用：build_answer_first_text 优先读取；理由：下游模型只吃干净正文。
        PROFILE_PROMPT_TEXT_KEY: prompt_text,
        # 2026-06-11 15:54:56 修改：写入原始业务 payload；作用：Qdrant payload 嵌套保留；理由：支持展示和回表。
        PROFILE_SOURCE_PAYLOAD_KEY: source_payload,
        # 2026-06-11 15:54:56 修改：写入来源名；作用：Qdrant payload 顶层可见；理由：多数据源追溯。
        PROFILE_SOURCE_NAME_KEY: profile.source_name,
        # 2026-06-11 15:54:56 修改：写入来源表；作用：Qdrant payload 顶层可见；理由：支持回表。
        PROFILE_SOURCE_TABLE_KEY: profile.source_table,
        # 2026-06-11 15:54:56 修改：写入来源主键；作用：Qdrant payload 顶层可见；理由：定位原始行。
        PROFILE_SOURCE_PK_KEY: source_pk,
        # 2026-06-11 15:54:56 修改：写入 profile 关键词；作用：合并进 keyword_terms；理由：支持外部字段过滤。
        PROFILE_KEYWORD_TERMS_KEY: keyword_terms,
        # 2026-06-11 15:54:56 修改：写入目标 collection；作用：排查命令行覆盖；理由：避免误写主库。
        PROFILE_TARGET_COLLECTION_KEY: profile.target_collection,
        # 2026-06-12 14:40:11 修改：写入 payload 输出模式；作用：让 build_qdrant_payload 能选择严格或旧 QA 格式；理由：不同 collection 需要不同字段隔离策略。
        PROFILE_PAYLOAD_MODE_KEY: profile.payload_mode,
        # 2026-06-12 15:30:17 修改：写入 Qdrant payload 布局；作用：build_qdrant_payload 可按 YAML 渲染顶层字段和嵌套对象；理由：外部库结构要配置化而不是 if 分支化。
        PROFILE_QDRANT_PAYLOAD_LAYOUT_KEY: profile.qdrant_payload_layout,
    }


# 2026-06-11 15:54:56 修改：判断 chunk 是否为 generic profile；作用：校验函数切换规则；理由：外部库可能没有 QA 严格答案契约。
def is_generic_profile_chunk(chunk: Any) -> bool:
    # 2026-06-11 15:54:56 修改：读取 payload_json；作用：判断 profile_contract_mode；理由：不新增 CanonicalChunk 字段。
    payload_json = getattr(chunk, "payload_json", {}) or {}
    # 2026-06-11 15:54:56 修改：返回是否 generic；作用：区分外部库泛化契约；理由：外部库 embedding_text 可不含答案。
    return isinstance(payload_json, dict) and payload_json.get(PROFILE_CONTRACT_MODE_KEY) == "generic"


# 2026-06-12 14:40:11 修改：判断 chunk 是否要求严格 profile payload；作用：Qdrant 写入层据此只输出最小契约；理由：外部库不能混入 getai QA 顶层字段。
def is_profile_strict_payload_chunk(chunk: Any) -> bool:
    # 2026-06-12 14:40:11 修改：读取 payload_json；作用：检查 profile 写入的 payload_mode；理由：不修改 CanonicalChunk 结构也能携带模式。
    payload_json = getattr(chunk, "payload_json", {}) or {}
    # 2026-06-12 14:40:11 修改：返回是否为 profile_strict；作用：隔离外部库 payload 输出；理由：legacy_qa 仍保持原行为。
    return isinstance(payload_json, dict) and payload_json.get(PROFILE_PAYLOAD_MODE_KEY) == PAYLOAD_MODE_PROFILE_STRICT


# 2026-06-11 15:54:56 修改：从 chunk 读取 profile 字段；作用：build_embedding_text/build_answer_first_text 复用；理由：避免同步层重复解析 payload_json。
def profile_payload_value(chunk: Any, key: str, default: Any = "") -> Any:
    # 2026-06-11 15:54:56 修改：读取 payload_json；作用：查找 profile 写入的契约字段；理由：不修改 CanonicalChunk 结构。
    payload_json = getattr(chunk, "payload_json", {}) or {}
    # 2026-06-11 15:54:56 修改：确认 payload_json 为 dict；作用：兼容历史空字符串；理由：旧数据不能报错。
    if isinstance(payload_json, dict):
        # 2026-06-11 15:54:56 修改：返回字段值；作用：供同步层优先读取；理由：profile 是字段策略入口。
        return payload_json.get(key, default)
    # 2026-06-11 15:54:56 修改：非 dict 时返回默认值；作用：保持兼容；理由：历史数据可能没有结构化 payload。
    return default


# 2026-06-11 15:54:56 修改：把 profile 结果应用到 CanonicalChunk；作用：getai 也进入统一 profile 管理；理由：写入链路不分叉。
def apply_profile_to_chunk(chunk: Any, profile: SourceMappingProfile) -> Any:
    # 2026-06-11 15:54:56 修改：基于 chunk 构造 profile 契约；作用：生成 embedding_text/prompt_text/source_payload；理由：现有 getai 数据也按配置解释。
    profile_contract = build_profile_contract(chunk, profile)
    # 2026-06-11 15:54:56 修改：复制原 payload_json；作用：保留上游清洗字段；理由：不能覆盖现有完美链路信息。
    payload_json = dict(getattr(chunk, "payload_json", {}) or {})
    # 2026-06-11 15:54:56 修改：合并 profile 契约；作用：让后续 build 函数优先读 profile 字段；理由：不新增分叉链路。
    payload_json.update(profile_contract)
    # 2026-06-11 15:54:56 修改：读取 profile 向量文本；作用：决定是否覆盖 chunk.retrieval_text；理由：外部库需要只用指定字段向量化。
    embedding_text = normalize_text(profile_contract.get(PROFILE_EMBEDDING_TEXT_KEY))
    # 2026-06-11 15:54:56 修改：读取 profile prompt 文本；作用：决定是否覆盖 chunk.llm_text；理由：外部库需要干净 prompt 正文。
    prompt_text = normalize_text(profile_contract.get(PROFILE_PROMPT_TEXT_KEY))
    # 2026-06-11 15:54:56 修改：返回复制后的 chunk；作用：保留 dataclass frozen 语义；理由：不原地修改上游对象。
    return replace(
        # 2026-06-11 15:54:56 修改：指定原 chunk；作用：只覆盖必要字段；理由：保护现有 QA 字段。
        chunk,
        # 2026-06-11 15:54:56 修改：写回 payload_json；作用：保存 profile 契约；理由：后续 Qdrant payload 构造要读取。
        payload_json=payload_json,
        # 2026-06-11 15:54:56 修改：写回 retrieval_text；作用：让旧 build_embedding_text 也能兜底读取；理由：保持向后兼容。
        retrieval_text=embedding_text or getattr(chunk, "retrieval_text", ""),
        # 2026-06-11 15:54:56 修改：写回 llm_text；作用：让旧 build_answer_first_text 也能兜底读取；理由：保持向后兼容。
        llm_text=prompt_text or getattr(chunk, "llm_text", ""),
    )


# 2026-06-11 15:54:56 修改：批量应用 profile；作用：同步入口一次性处理所有 chunk；理由：保持原 validate/embed/build/upsert 顺序。
def apply_profile_to_chunks(chunks: list[Any], profile: SourceMappingProfile) -> list[Any]:
    # 2026-06-11 15:54:56 修改：逐条应用 profile；作用：把所有数据统一成 profile-aware chunk；理由：写入链路不分叉。
    return [apply_profile_to_chunk(chunk, profile) for chunk in chunks]


# 2026-06-11 15:54:56 修改：把外部 row 转成 CanonicalChunk；作用：外部库接入复用现有同步链路；理由：不能另起 Qdrant 写入逻辑。
def row_to_canonical_chunk(row: Any, profile: SourceMappingProfile, qdrant_sync_module: Any) -> Any:
    # 2026-06-11 15:54:56 修改：构造 profile 契约；作用：得到 embedding_text/prompt_text/source_payload；理由：外部 row 字段由 profile 解释。
    profile_contract = build_profile_contract(row, profile)
    # 2026-06-11 15:54:56 修改：读取来源主键；作用：生成稳定 chunk_id；理由：外部库 point id 必须稳定可复现。
    source_pk = normalize_text(profile_contract.get(PROFILE_SOURCE_PK_KEY))
    # 2026-06-11 15:54:56 修改：生成来源表安全名；作用：chunk_id 中避免 schema 点号歧义；理由：多表接入时标识要稳定。
    source_table_token = profile.source_table.replace(".", ":")
    # 2026-06-11 15:54:56 修改：生成 document_id；作用：兼容 LlamaIndex doc_id 和 Qdrant filter；理由：同一外部表可视为一份文档来源。
    document_id = f"{profile.source_name}:{source_table_token}"
    # 2026-06-11 15:54:56 修改：生成 chunk_id；作用：作为 Qdrant point 稳定业务 ID；理由：upsert 重跑不能生成新点。
    chunk_id = f"{document_id}:{source_pk}"
    # 2026-06-11 15:54:56 修改：读取问题字段；作用：兼容外部 QA 表；理由：CanonicalChunk 仍需填充问题字段。
    question = normalize_text(row_value(row, "question") or row_value(row, "standard_question") or profile_contract.get(PROFILE_EMBEDDING_TEXT_KEY))
    # 2026-06-11 15:54:56 修改：读取答案字段；作用：兼容外部 QA 表；理由：prompt_text 可包含答案但 CanonicalChunk 也要保留。
    answer = normalize_text(row_value(row, "answer") or row_value(row, "answer_text"))
    # 2026-06-11 15:54:56 修改：读取场景字段；作用：兼容截图 question_scene；理由：scene 仍是通用过滤字段。
    scene = normalize_text(row_value(row, "scene") or row_value(row, "question_scene") or profile.source_table)
    # 2026-06-11 15:54:56 修改：读取标准问题；作用：填充 canonical_question；理由：外部库标准问法是核心字段。
    canonical_question = normalize_text(row_value(row, "standard_question") or row_value(row, "canonical_question") or question)
    # 2026-06-11 15:54:56 修改：读取 prompt 文本；作用：填充 text/llm_text；理由：模型消费正文由 profile 决定。
    prompt_text = normalize_text(profile_contract.get(PROFILE_PROMPT_TEXT_KEY))
    # 2026-06-11 15:54:56 修改：读取向量文本；作用：填充 retrieval_text；理由：向量化字段由 profile 决定。
    embedding_text = normalize_text(profile_contract.get(PROFILE_EMBEDDING_TEXT_KEY))
    # 2026-06-11 15:54:56 修改：读取关键词列表；作用：填充 keywords/query_aliases；理由：Qdrant keyword_terms 要有业务字段。
    keyword_terms = list(profile_contract.get(PROFILE_KEYWORD_TERMS_KEY) or [])
    # 2026-06-11 15:54:56 修改：复制 profile payload；作用：写入 CanonicalChunk.payload_json；理由：后续 build_qdrant_payload 读取。
    payload_json = dict(profile_contract)
    # 2026-06-11 15:54:56 修改：补充 qdrant_ready 标记；作用：让校验函数明确是否可同步；理由：外部 row 缺文本时要阻断。
    payload_json["qdrant_ready"] = bool(source_pk and embedding_text and prompt_text)
    # 2026-06-11 15:54:56 修改：构造 CanonicalChunk；作用：复用现有 validate/embed/build/upsert；理由：不新增第二条 Qdrant 链路。
    return qdrant_sync_module.CanonicalChunk(
        # 2026-06-11 15:54:56 修改：写入 chunk_id；作用：稳定生成 Qdrant point id；理由：支持幂等 upsert。
        chunk_id=chunk_id,
        # 2026-06-11 15:54:56 修改：写入 document_id；作用：兼容 doc_id 过滤；理由：LlamaIndex 默认 index_doc_id 需要。
        document_id=document_id,
        # 2026-06-11 15:54:56 修改：外部库无音频编号时写 0；作用：保持字段类型稳定；理由：兼容 CanonicalChunk 必填字段。
        audio_no=0,
        # 2026-06-11 15:54:56 修改：音频标题写来源名；作用：Qdrant WebUI 可见来源；理由：外部库不是音频清洗产物。
        audio_title=profile.source_name,
        # 2026-06-11 15:54:56 修改：chunk_index 尽量取来源主键；作用：保持排序稳定；理由：外部样例主键是整数。
        chunk_index=int(source_pk) if source_pk.isdigit() else 0,
        # 2026-06-11 15:54:56 修改：写入场景；作用：保留通用过滤字段；理由：外部库也可能按场景过滤。
        scene=scene,
        # 2026-06-11 15:54:56 修改：写入问题；作用：保留 QA 兼容字段；理由：下游展示仍可读。
        question=question,
        # 2026-06-11 15:54:56 修改：写入答案；作用：保留 QA 兼容字段；理由：prompt_text 通常需要答案。
        answer=answer,
        # 2026-06-11 15:54:56 修改：写入清洗文本；作用：使用 prompt_text 作为干净正文；理由：外部库跳过清洗链路。
        cleaned_text=prompt_text or embedding_text,
        # 2026-06-11 15:54:56 修改：写入空步骤；作用：满足 CanonicalChunk 字段；理由：外部库没有原清洗步骤。
        resolution_steps="[]",
        # 2026-06-11 15:54:56 修改：写入关键词 JSON；作用：兼容旧 keywords 字段；理由：build_qdrant_keyword_terms 仍会读取。
        keywords=json.dumps(keyword_terms, ensure_ascii=False),
        # 2026-06-11 15:54:56 修改：写入空实体；作用：满足旧字段；理由：外部库没有实体抽取结果。
        entities_json="{}",
        # 2026-06-11 15:54:56 修改：写入来源摘录；作用：保留 prompt_text；理由：模型消费正文可回溯。
        source_excerpt=prompt_text or embedding_text,
        # 2026-06-11 15:54:56 修改：写入内容 hash；作用：支持同步状态和幂等排查；理由：外部库没有原 content_hash。
        content_hash=stable_hash(chunk_id, embedding_text, prompt_text, profile_contract.get(PROFILE_SOURCE_PAYLOAD_KEY)),
        # 2026-06-11 15:54:56 修改：写入 QA pair id；作用：兼容旧同步状态字段；理由：外部库仍走 CanonicalChunk。
        qa_pair_id=f"{profile.profile_name}:{source_pk}",
        # 2026-06-11 15:54:56 修改：写入 QA pair 序号；作用：兼容旧字段；理由：外部库主键可映射为序号。
        qa_pair_index=int(source_pk) if source_pk.isdigit() else 0,
        # 2026-06-11 15:54:56 修改：写入默认质量分；作用：兼容旧字段；理由：外部库跳过 evaluator。
        qa_similarity_score=1.0,
        # 2026-06-11 15:54:56 修改：写入默认阈值；作用：兼容旧字段；理由：外部库没有相似度阈值。
        qa_similarity_threshold=0.0,
        # 2026-06-11 15:54:56 修改：标记已验证；作用：允许进入 Qdrant；理由：profile 校验替代原 QA evaluator。
        qa_pair_validated=True,
        # 2026-06-11 15:54:56 修改：写入聚类 ID；作用：兼容旧过滤字段；理由：外部库没有聚类结果时用来源字段兜底。
        cluster_id=f"{profile.profile_name}:{scene or source_pk}",
        # 2026-06-11 15:54:56 修改：写入聚类标签；作用：兼容旧过滤字段；理由：WebUI 可读。
        cluster_label=scene,
        # 2026-06-11 15:54:56 修改：写入聚类层级；作用：兼容旧过滤字段；理由：标记这是 profile 生成。
        cluster_level="source_profile",
        # 2026-06-11 15:54:56 修改：写入聚类路径；作用：兼容旧过滤字段；理由：外部来源可读。
        cluster_path=f"{profile.source_name}/{profile.source_table}/{scene}",
        # 2026-06-11 15:54:56 修改：写入全局聚类 ID；作用：兼容旧过滤字段；理由：外部库统一归属。
        global_cluster_id=f"{profile.profile_name}:global",
        # 2026-06-11 15:54:56 修改：写入全局聚类标签；作用：兼容旧过滤字段；理由：WebUI 可读。
        global_cluster_label=profile.source_name,
        # 2026-06-11 15:54:56 修改：写入全局聚类层级；作用：兼容旧过滤字段；理由：标记来源级别。
        global_cluster_level="source_profile",
        # 2026-06-11 15:54:56 修改：写入全局聚类路径；作用：兼容旧过滤字段；理由：多库排查清晰。
        global_cluster_path=f"{profile.source_name}/{profile.source_table}",
        # 2026-06-11 15:54:56 修改：写入问题 hash；作用：兼容去重字段；理由：外部库仍可按问题排查。
        question_hash=stable_hash(question),
        # 2026-06-11 15:54:56 修改：写入答案 hash；作用：兼容去重字段；理由：外部库仍可按答案排查。
        answer_hash=stable_hash(answer),
        # 2026-06-11 15:54:56 修改：写入 canonical id；作用：兼容融合字段；理由：外部库没有 duplicate 时自身即 canonical。
        canonical_chunk_id=chunk_id,
        # 2026-06-11 15:54:56 修改：写入融合状态；作用：允许入 Qdrant；理由：现有同步只消费 canonical。
        fusion_status="canonical",
        # 2026-06-11 15:54:56 修改：写入 payload schema 版本；作用：标记 profile 产物；理由：排查时能区分清洗链路。
        payload_schema_version=f"{profile.profile_name}-profile-v1",
        # 2026-06-11 15:54:56 修改：写入 payload_json；作用：传递 profile 契约；理由：后续同步层优先读取。
        payload_json=payload_json,
        # 2026-06-11 15:54:56 修改：写入 RAG 契约版本；作用：标记泛化契约；理由：外部库不套用 QA 严格答案向量校验。
        rag_contract_version="mapping-profile-contract-v1" if profile.contract_mode == "generic" else "qa-rag-contract-v1",
        # 2026-06-11 15:54:56 修改：写入规范问题；作用：兼容 QA 字段；理由：外部 QA 表仍有标准问法。
        canonical_question=canonical_question,
        # 2026-06-11 15:54:56 修改：写入答案文本；作用：兼容 QA 字段；理由：prompt_text 通常包含答案。
        answer_text=answer,
        # 2026-06-11 15:54:56 修改：写入别名列表；作用：兼容 keyword_terms；理由：profile 关键词可参与过滤。
        query_aliases=keyword_terms,
        # 2026-06-11 15:54:56 修改：写入完整来源摘录；作用：兼容 payload 字段；理由：外部库 prompt_text 是最干净证据。
        source_excerpt_full=prompt_text or embedding_text,
        # 2026-06-11 15:54:56 修改：写入 LLM 文本；作用：build_answer_first_text 可兜底；理由：保持旧函数兼容。
        llm_text=prompt_text,
        # 2026-06-11 15:54:56 修改：写入检索文本；作用：build_embedding_text 可兜底；理由：profile 控制向量化字段。
        retrieval_text=embedding_text,
        # 2026-06-11 15:54:56 修改：写入空 duplicate 上下文；作用：兼容旧字段；理由：外部库跳过融合。
        duplicate_contexts=[],
        # 2026-06-11 15:54:56 修改：写入空 duplicate id；作用：兼容旧字段；理由：外部库跳过融合。
        merged_duplicate_chunk_ids=[],
        # 2026-06-11 15:54:56 修改：写入可同步标记；作用：校验函数读取；理由：缺关键文本时阻断。
        qdrant_ready=bool(source_pk and embedding_text and prompt_text),
        # 2026-06-11 15:54:56 修改：写入校验标记；作用：兼容旧字段；理由：外部库初始无校验错误。
        validation_flags=[],
    )


# 2026-06-11 15:54:56 修改：解析 SQL Server schema/table；作用：外部 adapter 生成 SELECT；理由：profile.source_table 使用 dbo.table 写法。
def split_source_table(source_table: str) -> tuple[str, str]:
    # 2026-06-11 15:54:56 修改：按点号拆分来源表；作用：提取 schema 和 table；理由：SQL Server 查询需要分开加方括号。
    parts = [part.strip("[] ") for part in source_table.split(".") if part.strip("[] ")]
    # 2026-06-11 15:54:56 修改：只有表名时默认 dbo；作用：兼容简写配置；理由：SQL Server 常用 dbo。
    if len(parts) == 1:
        # 2026-06-11 15:54:56 修改：返回 dbo 和表名；作用：构造 SQL；理由：缺省 schema 仍可工作。
        return "dbo", parts[0]
    # 2026-06-11 15:54:56 修改：返回前两个片段；作用：构造 SQL；理由：当前只支持 schema.table。
    return parts[0], parts[1]


# 2026-06-13 17:18:04 新增：规范 SQL 方言名称；作用：把 postgresql/postgres/pg 归一；理由：YAML 写法需要宽容但执行逻辑要稳定。
def normalize_sql_dialect(raw_dialect: str | None) -> str:
    # 2026-06-13 17:18:04 新增：清理输入方言；作用：避免大小写和空格影响判断；理由：外部 profile 由人工维护。
    normalized = str(raw_dialect or "").strip().lower()
    # 2026-06-13 17:18:04 新增：识别 PostgreSQL 别名；作用：支持 pg/postgres/postgresql 三种常见写法；理由：减少新增外部库配置成本。
    if normalized in {"pg", "postgres", "postgresql"}:
        # 2026-06-13 17:18:04 新增：返回标准 postgresql；作用：让 adapter 和 SQL builder 统一判断；理由：避免到处写别名分支。
        return "postgresql"
    # 2026-06-13 17:18:04 新增：识别 SQL Server 别名；作用：兼容原有 sqlserver/mssql 写法；理由：主库链路不能被新方言支持破坏。
    if normalized in {"mssql", "sqlserver", "sql_server", "sql-server"}:
        # 2026-06-13 17:18:04 新增：返回标准 sqlserver；作用：保持原有方括号 SQL；理由：兼容现有 External_database。
        return "sqlserver"
    # 2026-06-13 17:18:04 新增：默认 SQL Server；作用：没有 connection.engine 的 getai/external_database 保持旧行为；理由：不能影响现有完美问答链路。
    return "sqlserver"


# 2026-06-13 17:18:04 新增：按 SQL 方言引用标识符；作用：PostgreSQL 用双引号，SQL Server 用方括号；理由：AI_erp_Wendajilu 这类大小写表名必须正确引用。
def quote_sql_identifier(identifier: str, dialect: str) -> str:
    # 2026-06-13 17:18:04 新增：清理标识符外层旧引用符；作用：兼容 YAML 手写 [x] 或 "x"；理由：避免重复引用导致 SQL 错误。
    cleaned = str(identifier or "").strip().strip("[]").strip('"')
    # 2026-06-13 17:18:04 新增：判断 PostgreSQL 方言；作用：生成 "field"；理由：PG 大小写敏感字段需要双引号保留原样。
    if normalize_sql_dialect(dialect) == "postgresql":
        # 2026-06-13 17:18:04 新增：转义双引号后返回；作用：防止字段名包含引号破坏 SQL；理由：标识符引用也要安全。
        return '"' + cleaned.replace('"', '""') + '"'
    # 2026-06-13 17:18:04 新增：默认 SQL Server 方括号；作用：保持原有 [field] 语法；理由：主库和旧外部库不能变。
    return f"[{cleaned.replace(']', ']]')}]"


# 2026-06-13 17:18:04 新增：按 SQL 方言解析 schema/table；作用：PG 默认 public，SQL Server 默认 dbo；理由：两种关系库默认 schema 不同。
def split_source_table_for_dialect(source_table: str, dialect: str) -> tuple[str, str]:
    # 2026-06-13 17:18:04 新增：清理来源表文本；作用：兼容 YAML 空格；理由：外部库配置可能人工粘贴。
    raw_source_table = str(source_table or "").strip()
    # 2026-06-13 17:18:04 新增：按点拆分 schema/table；作用：支持 public.AI_erp_Wendajilu；理由：PG 截图表在 public schema 下。
    parts = [part.strip("[] ").strip('"') for part in raw_source_table.split(".") if part.strip("[] ").strip('"')]
    # 2026-06-13 17:18:04 新增：读取标准方言；作用：判断默认 schema；理由：不同引擎不能共用 dbo。
    normalized_dialect = normalize_sql_dialect(dialect)
    # 2026-06-13 17:18:04 新增：处理只有表名的情况；作用：自动补默认 schema；理由：降低 YAML 配置成本。
    if len(parts) == 1:
        # 2026-06-13 17:18:04 新增：PG 默认 public，SQL Server 默认 dbo；作用：生成可执行 SQL；理由：两类库惯例不同。
        return ("public" if normalized_dialect == "postgresql" else "dbo", parts[0])
    # 2026-06-13 17:18:04 新增：返回 schema/table；作用：供 SQL builder 引用；理由：当前同步按单表或单 view 接入。
    return parts[0], parts[1]


# 2026-06-11 15:54:56 修改：构造 SELECT 字段列表；作用：外部读取层按 profile 取字段；理由：字段不能写死在 adapter。
def build_select_sql(profile: SourceMappingProfile, dialect: str | None = None, where_clause: str | None = None) -> str:
    # 2026-06-11 15:54:56 修改：选择 select.fields 或 payload.include；作用：profile 简写时仍可读取；理由：外部库至少要读 payload 字段。
    fields = profile.select_fields or profile.payload_include
    # 2026-06-11 15:54:56 修改：校验字段列表非空；作用：避免生成无效 SQL；理由：外部库读取层必须明确字段。
    if not fields:
        # 2026-06-11 15:54:56 修改：抛出明确错误；作用：阻断错误 profile；理由：不能猜外部库字段。
        raise ValueError(f"source profile {profile.profile_name} 缺少 select.fields 或 payload.include")
    # 2026-06-13 17:18:04 新增：确定 SQL 方言；作用：没有显式参数时读取 profile.connection.engine；理由：PG/SQL Server 都靠同一函数生成 SQL。
    resolved_dialect = normalize_sql_dialect(dialect or (profile.connection or {}).get("engine"))
    # 2026-06-13 17:18:04 修改：按方言解析来源表；作用：PG 默认 public，SQL Server 默认 dbo；理由：不能把 PG 表写成 [dbo]。
    schema_name, table_name = split_source_table_for_dialect(profile.source_table, resolved_dialect)
    # 2026-06-13 17:18:04 修改：按方言构造 SELECT 字段片段；作用：PG 用双引号保留大小写；理由：截图字段 MiaoShu/ZhuangTai 大小写敏感。
    select_columns = ",\n    ".join(quote_sql_identifier(field, resolved_dialect) for field in fields)
    # 2026-06-11 15:54:56 修改：构造 ORDER BY 字段；作用：同步顺序稳定；理由：point 生成和测试要可复现。
    order_field = profile.id_field if profile.id_field in fields else fields[0]
    # 2026-06-13 17:18:04 新增：按方言构造表名；作用：PG public."AI_erp_Wendajilu" 可执行；理由：大小写表名必须引用。
    table_sql = f"{quote_sql_identifier(schema_name, resolved_dialect)}.{quote_sql_identifier(table_name, resolved_dialect)}"
    # 2026-06-13 17:18:04 新增：按配置拼接 WHERE；作用：未来可按租户/状态筛选；理由：不同外部库同步范围应在 YAML 控制。
    where_sql = f"\nWHERE {where_clause.strip()}" if where_clause and str(where_clause).strip() else ""
    # 2026-06-13 17:18:04 修改：返回完整 SQL；作用：外部 adapter 执行读取；理由：读取层只负责拿 row。
    return f"""
SELECT
    {select_columns}
FROM {table_sql}{where_sql}
ORDER BY {quote_sql_identifier(order_field, resolved_dialect)};
""".strip()
