# -*- coding: utf-8 -*-
"""External_database 模拟外部关系型库适配器。"""

# 2026-06-10 18:01:50 修改：导入 hashlib，用于为外部扁平 QA 行生成稳定 chunk_id/hash。
import hashlib
# 2026-06-10 18:01:50 修改：导入 json，用于把外部库字段组织成现有 payload_json 契约。
import json
# 2026-06-10 18:01:50 修改：导入 Any，用于标注外部 SQL 行和字典行的动态字段。
from typing import Any

# 2026-06-10 18:01:50 修改：导入现有 Qdrant 同步模块，理由是外部库只能转换成 CanonicalChunk 后复用原链路。
from Qdrant import qdrant_sqlserver_sync as qdrant_sync
# 2026-06-11 15:54:56 修改：导入 source profile 解析器；作用：外部库字段映射由 external_database.yml 决定；理由：不能把所有外部库硬编码成同一套 QA 字段模板。
from Qdrant import qdrant_mapping_profile

# 2026-06-13 17:18:04 新增：导入通用外部库 adapter registry；作用：离线转换也能按 YAML connection.engine 读取 PG/SQLServer；理由：不能让 PG 只支持后台同步而命令行仍写死 SQL Server。
try:
    # 2026-06-13 17:18:04 新增：包内相对导入；作用是服务/测试按 integration 包加载时可用；理由是新增 adapter 层就在同目录下。
    from .external_db_adapters import build_default_external_adapter_registry
except ImportError:
    # 2026-06-13 17:18:04 新增：顶层导入兜底；作用是兼容旧脚本从 integration 目录外直接运行；理由是不能破坏既有执行方式。
    from external_db_adapters import build_default_external_adapter_registry


# 2026-06-10 18:01:50 修改：定义模拟外部库名，理由是用户指定新建库必须叫 External_database。
EXTERNAL_DATABASE_NAME = "External_database"
# 2026-06-10 18:01:50 修改：定义模拟外部库表名，作用是集中管理建表、读取和转换入口。
EXTERNAL_TABLE_NAME = "external_qa_samples"
# 2026-06-10 18:01:50 修改：定义模拟外部库表 schema，理由是 SQL Server 默认业务 schema 走 dbo。
EXTERNAL_SCHEMA_NAME = "dbo"
# 2026-06-10 18:01:50 修改：定义外部库目标 Qdrant collection，理由是不能和 sql_rag_qa_chunks_v1 冲突。
EXTERNAL_QDRANT_COLLECTION = "sql_External_database"
# 2026-06-10 18:01:50 修改：定义外部库默认 SQL Server 地址，理由是新服务端口必须与 getai 的 1433 区分。
EXTERNAL_SQL_SERVER_DEFAULT = "127.0.0.1,14333"
# 2026-06-10 18:01:50 修改：定义外部库默认 Qdrant URL，理由是新向量服务端口必须与现有 6333 区分。
EXTERNAL_QDRANT_URL_DEFAULT = "http://127.0.0.1:6334"


# 2026-06-10 18:01:50 修改：定义三条截图样例数据，理由是 External_database 必须能模拟外部扁平 QA 表。
EXTERNAL_SAMPLE_ROWS: list[dict[str, Any]] = [
    # 2026-06-10 18:01:50 修改：第一条二次工艺流程样例，作用是覆盖截图中的完整问答字段。
    {
        # 2026-06-12 14:40:11 修改：设置普通序号 id，作用：参与 standard_question + id 向量化并进入 payload；理由：用户要求 External_database 新增 id 字段且三条数据配序号。
        "id": 1,
        # 2026-06-10 18:01:50 修改：设置外部行 ID，作用是生成稳定 chunk_id。
        "external_id": 1,
        # 2026-06-10 18:01:50 修改：设置原始问题，作用是映射 CanonicalChunk.question。
        "question": "二次工艺流程不对，是后补的，不是发出去的时候做",
        # 2026-06-10 18:01:50 修改：设置问题场景，作用是映射 scene 和 keyword_terms。
        "question_scene": "二次工艺外发流程，涉及到加工单的创建和收货",
        # 2026-06-10 18:01:50 修改：设置答案，作用是映射 answer/answer_text。
        "answer": "正常流程是发出去的时候先做好二次工艺单，把价格数量保存起来，打单给外发部门。等有差异再反馈。二次工艺应该由外发部门按流程反馈后再补差异。",
        # 2026-06-10 18:01:50 修改：设置标准问题，作用是映射 canonical_question。
        "standard_question": "二次工艺的正确操作流程是什么？",
        # 2026-06-10 18:01:50 修改：设置答案完整度，作用是保留业务质量字段。
        "answer_completeness": "完整",
        # 2026-06-10 18:01:50 修改：设置客户原话，作用是映射 evidence.customer_text。
        "customer_text": "那也就是相当于我们现在的二次公益，是相当于你们的流程之后对补的。他不是说再发出去的时候做。",
        # 2026-06-10 18:01:50 修改：设置客服原话，作用是映射 evidence.service_text。
        "service_text": "你要发出去的时候先做好那个二次公益单，然后把那个价格数量保存起来，先把那个单打起来，然后给到那个外发部门。",
    },
    # 2026-06-10 18:01:50 修改：第二条采购单权限样例，作用是覆盖部分完整答案场景。
    {
        # 2026-06-12 14:40:11 修改：设置普通序号 id，作用：参与 standard_question + id 向量化并进入 payload；理由：用户要求 External_database 新增 id 字段且三条数据配序号。
        "id": 2,
        # 2026-06-10 18:01:50 修改：设置外部行 ID，作用是生成稳定 chunk_id。
        "external_id": 2,
        # 2026-06-10 18:01:50 修改：设置原始问题，作用是映射 CanonicalChunk.question。
        "question": "系统里采购单导出来后，其他人看不到，导致漏下单",
        # 2026-06-10 18:01:50 修改：设置问题场景，作用是映射 scene 和 keyword_terms。
        "question_scene": "采购流程，采购订单单的创建和权限管理",
        # 2026-06-10 18:01:50 修改：设置答案，作用是映射 answer/answer_text。
        "answer": "可能是权限设置问题，设置了私有权导致单据不共享。需要检查权限设置，确保单据共享。",
        # 2026-06-10 18:01:50 修改：设置标准问题，作用是映射 canonical_question。
        "standard_question": "采购单导出后其他人看不到怎么办？",
        # 2026-06-10 18:01:50 修改：设置答案完整度，作用是保留业务质量字段。
        "answer_completeness": "部分完整",
        # 2026-06-10 18:01:50 修改：设置客户原话，作用是映射 evidence.customer_text。
        "customer_text": "小兵呢，他以为我没下，因为我的单就没导嘛，然后呢去系统，其实我有一张单就导出来了。在我的电脑里面系统能看到。",
        # 2026-06-10 18:01:50 修改：设置客服原话，作用是映射 evidence.service_text。
        "service_text": "有可能是设置了私有私有权了，就是单据不共享。知道吧？那这个就是另外一回事了，就不是说看不到，所以说要检查权限。",
    },
    # 2026-06-10 18:01:50 修改：第三条 BOM 刷新样例，作用是覆盖 BOM 变更流程问答。
    {
        # 2026-06-12 14:40:11 修改：设置普通序号 id，作用：参与 standard_question + id 向量化并进入 payload；理由：用户要求 External_database 新增 id 字段且三条数据配序号。
        "id": 3,
        # 2026-06-10 18:01:50 修改：设置外部行 ID，作用是生成稳定 chunk_id。
        "external_id": 3,
        # 2026-06-10 18:01:50 修改：设置原始问题，作用是映射 CanonicalChunk.question。
        "question": "BOM表变更频繁，刷新单据很繁琐",
        # 2026-06-10 18:01:50 修改：设置问题场景，作用是映射 scene 和 keyword_terms。
        "question_scene": "BOM管理和采购流程，销售订单单和采购申请单的变更",
        # 2026-06-10 18:01:50 修改：设置答案，作用是映射 answer/answer_text。
        "answer": "系统设计上不能自动刷新，必须人为主动刷新，以避免不可控的变更。操作繁琐是必要的，为了确保变更的可控性和可追踪性。",
        # 2026-06-10 18:01:50 修改：设置标准问题，作用是映射 canonical_question。
        "standard_question": "BOM变更频繁导致刷新单据繁琐怎么办？",
        # 2026-06-10 18:01:50 修改：设置答案完整度，作用是保留业务质量字段。
        "answer_completeness": "完整",
        # 2026-06-10 18:01:50 修改：设置客户原话，作用是映射 evidence.customer_text。
        "customer_text": "系统不智能的，就是随便改了一个东西，就要刷很多单，不能不能就刷两三个地方要刷三三个销售订单单、采购申请单。",
        # 2026-06-10 18:01:50 修改：设置客服原话，作用是映射 evidence.service_text。
        "service_text": "系统你就刷最新的嘛。所以你没办法去说哎，我要让你人为的主观的去判断，我是要改这张去下这张？是不是对吧。",
    },
]


# 2026-06-10 18:01:50 修改：封装 SQL 字符串转义，理由是建种子数据脚本不能被单引号截断。
def sql_literal(value: Any) -> str:
    # 2026-06-10 18:01:50 修改：None 转 SQL NULL，作用是兼容可选字段。
    if value is None:
        # 2026-06-10 18:01:50 修改：返回 NULL 字面量，理由是 SQL Server 可直接执行。
        return "NULL"
    # 2026-06-10 18:01:50 修改：统一转字符串并替换单引号，作用是避免 SQL 注入式截断。
    escaped_value = str(value).replace("'", "''")
    # 2026-06-10 18:01:50 修改：返回 NVARCHAR 字面量，理由是样例包含中文。
    return f"N'{escaped_value}'"


# 2026-06-10 18:01:50 修改：生成建库建表和三条种子数据 SQL，理由是能手动或程序化初始化 External_database。
def build_external_database_schema_sql() -> str:
    # 2026-06-10 18:01:50 修改：创建 SQL 片段列表，作用是逐段拼接可读脚本。
    statements: list[str] = []
    # 2026-06-10 18:01:50 修改：追加建库语句，理由是数据库不存在时自动创建。
    statements.append(f"IF DB_ID(N'{EXTERNAL_DATABASE_NAME}') IS NULL CREATE DATABASE [{EXTERNAL_DATABASE_NAME}];")
    # 2026-06-10 18:01:50 修改：追加切库语句，作用是后续建表落在 External_database。
    statements.append(f"USE [{EXTERNAL_DATABASE_NAME}];")
    # 2026-06-10 18:01:50 修改：追加建表语句，理由是字段必须覆盖截图最后一张的 QA/evidence 字段。
    statements.append(
        f"""
IF OBJECT_ID(N'[{EXTERNAL_SCHEMA_NAME}].[{EXTERNAL_TABLE_NAME}]', N'U') IS NULL
CREATE TABLE [{EXTERNAL_SCHEMA_NAME}].[{EXTERNAL_TABLE_NAME}] (
    [id] INT NOT NULL,
    [external_id] INT NOT NULL PRIMARY KEY,
    [question] NVARCHAR(MAX) NOT NULL,
    [question_scene] NVARCHAR(MAX) NOT NULL,
    [answer] NVARCHAR(MAX) NOT NULL,
    [standard_question] NVARCHAR(MAX) NOT NULL,
    [answer_completeness] NVARCHAR(50) NOT NULL,
    [customer_text] NVARCHAR(MAX) NOT NULL,
    [service_text] NVARCHAR(MAX) NOT NULL,
    [created_at] DATETIME2(0) NOT NULL DEFAULT SYSUTCDATETIME(),
    [updated_at] DATETIME2(0) NOT NULL DEFAULT SYSUTCDATETIME()
);
""".strip()
    )
    # 2026-06-12 14:40:11 修改：追加已有表 id 列迁移脚本，作用：旧 External_database 卷不重建也能补齐 id；理由：用户要求现在就在关系型库新增 id 字段。
    statements.append(
        """
-- 2026-06-12 14:40:11 新增原因：兼容已经存在但缺少 id 的 external_qa_samples 表，作用是不中断旧容器数据卷。
IF COL_LENGTH(N'dbo.external_qa_samples', N'id') IS NULL
BEGIN
    -- 2026-06-12 14:40:11 新增原因：先用可空列落地，作用是允许旧表已有数据时安全补列。
    ALTER TABLE [dbo].[external_qa_samples] ADD [id] INT NULL;
END;
-- 2026-06-12 14:40:11 新增原因：用 external_id 回填旧数据，作用是后续改 NOT NULL 前没有空值。
UPDATE [dbo].[external_qa_samples] SET [id] = [external_id] WHERE [id] IS NULL;
-- 2026-06-12 14:40:11 新增原因：把 id 固化为非空，作用是和新建表结构保持一致。
IF EXISTS (
    SELECT 1
    FROM sys.columns
    WHERE object_id = OBJECT_ID(N'dbo.external_qa_samples')
      AND name = N'id'
      AND is_nullable = 1
)
BEGIN
    ALTER TABLE [dbo].[external_qa_samples] ALTER COLUMN [id] INT NOT NULL;
END;
""".strip()
    )
    # 2026-06-11 19:57:10 修改：追加 Qdrant 同步状态表建表语句，理由是外部库跳过原清洗入库也要复用 update_sqlserver_sync_state。
    statements.append(
        """
IF OBJECT_ID(N'[dbo].[rag_rag_sync_state]', N'U') IS NULL
CREATE TABLE [dbo].[rag_rag_sync_state] (
    [sync_id] NVARCHAR(80) NOT NULL PRIMARY KEY,
    [document_id] NVARCHAR(80) NOT NULL,
    [content_hash] NVARCHAR(64) NOT NULL,
    [sync_target] NVARCHAR(120) NOT NULL,
    [sync_status] NVARCHAR(40) NOT NULL,
    [chunk_count] INT NOT NULL,
    [needs_reindex] BIT NOT NULL,
    [sync_message] NVARCHAR(MAX) NULL,
    [created_at] DATETIME2(0) NOT NULL DEFAULT SYSUTCDATETIME(),
    [updated_at] DATETIME2(0) NOT NULL DEFAULT SYSUTCDATETIME()
);
""".strip()
    )
    # 2026-06-10 18:01:50 修改：追加清空语句，作用是重复初始化时保持三条样例稳定。
    statements.append(f"DELETE FROM [{EXTERNAL_SCHEMA_NAME}].[{EXTERNAL_TABLE_NAME}];")
    # 2026-06-10 18:01:50 修改：遍历三条样例，理由是用户要求生成三条数据。
    for row in EXTERNAL_SAMPLE_ROWS:
        # 2026-06-10 18:01:50 修改：追加 INSERT 语句，作用是把截图字段写入外部关系型库。
        statements.append(
            "INSERT INTO [dbo].[external_qa_samples] "
            "([id], [external_id], [question], [question_scene], [answer], [standard_question], [answer_completeness], [customer_text], [service_text]) "
            f"VALUES ({int(row['id'])}, {int(row['external_id'])}, {sql_literal(row['question'])}, {sql_literal(row['question_scene'])}, "
            f"{sql_literal(row['answer'])}, {sql_literal(row['standard_question'])}, {sql_literal(row['answer_completeness'])}, "
            f"{sql_literal(row['customer_text'])}, {sql_literal(row['service_text'])});"
        )
    # 2026-06-10 18:01:50 修改：返回完整脚本，理由是 CLI 或人工都可以复用。
    return "\n".join(statements)


# 2026-06-10 18:01:50 修改：生成稳定短 hash，理由是外部库没有原清洗链路的 content_hash/question_hash。
def stable_hash(*parts: Any) -> str:
    # 2026-06-10 18:01:50 修改：用分隔符拼接输入，作用是避免字段边界混淆。
    raw_text = "\u241f".join(str(part or "") for part in parts)
    # 2026-06-10 18:01:50 修改：返回 SHA256 十六进制，理由是和现有链路 hash 字段风格一致。
    return hashlib.sha256(raw_text.encode("utf-8")).hexdigest()


# 2026-06-10 18:01:50 修改：从 dict 或 pyodbc.Row 读取字段，理由是 adapter 同时服务测试样例和真实 SQL 读取。
def row_value(row: Any, field_name: str, default: Any = "") -> Any:
    # 2026-06-10 18:01:50 修改：dict 直接按 key 取值，作用是支持 EXTERNAL_SAMPLE_ROWS。
    if isinstance(row, dict):
        # 2026-06-10 18:01:50 修改：返回字典值，理由是测试和种子数据用 dict 表示。
        return row.get(field_name, default)
    # 2026-06-10 18:01:50 修改：对象按属性取值，作用是支持 pyodbc.Row。
    return getattr(row, field_name, default)


# 2026-06-10 18:01:50 修改：把单条外部 QA 行转换为 CanonicalChunk，理由是 Qdrant 写入链路只接收 CanonicalChunk。
def external_row_to_canonical_chunk(row: Any, source_profile: Any | None = None) -> qdrant_sync.CanonicalChunk:
    # 2026-06-11 15:54:56 修改：优先使用调用方传入 profile；作用：同一 adapter 可服务不同外部库配置；理由：外部库字段千变万化，不能在函数内写死。
    resolved_profile = source_profile or qdrant_mapping_profile.load_source_profile("external_database")
    # 2026-06-11 15:54:56 修改：委托 profile 解析器生成 CanonicalChunk；作用：按配置生成 embedding_text/prompt_text/payload；理由：外部库转换必须融入统一 Qdrant 写入链路而不是新拉一条。
    return qdrant_mapping_profile.row_to_canonical_chunk(row, resolved_profile, qdrant_sync)
    # 2026-06-10 18:01:50 修改：读取外部行 ID，作用是生成稳定主键。
    external_id = int(row_value(row, "external_id", 0) or 0)
    # 2026-06-10 18:01:50 修改：读取问题，作用是映射 CanonicalChunk.question。
    question = qdrant_sync.normalize_text(row_value(row, "question"))
    # 2026-06-10 18:01:50 修改：读取场景，作用是映射 CanonicalChunk.scene。
    question_scene = qdrant_sync.normalize_text(row_value(row, "question_scene"))
    # 2026-06-10 18:01:50 修改：读取答案，作用是映射 CanonicalChunk.answer。
    answer = qdrant_sync.normalize_text(row_value(row, "answer"))
    # 2026-06-10 18:01:50 修改：读取标准问题，作用是映射 canonical_question。
    standard_question = qdrant_sync.normalize_text(row_value(row, "standard_question") or question)
    # 2026-06-10 18:01:50 修改：读取答案完整度，作用是保留业务质量信息。
    answer_completeness = qdrant_sync.normalize_text(row_value(row, "answer_completeness"))
    # 2026-06-10 18:01:50 修改：读取客户原话，作用是构造 evidence 和来源摘录。
    customer_text = qdrant_sync.normalize_text(row_value(row, "customer_text"))
    # 2026-06-10 18:01:50 修改：读取客服原话，作用是构造 evidence 和来源摘录。
    service_text = qdrant_sync.normalize_text(row_value(row, "service_text"))
    # 2026-06-10 18:01:50 修改：生成外部文档 ID，理由是 LlamaIndex doc_id 和 document_id 要有稳定值。
    document_id = f"{EXTERNAL_DATABASE_NAME}:{EXTERNAL_TABLE_NAME}"
    # 2026-06-10 18:01:50 修改：生成 chunk ID，作用是 Qdrant point id 能稳定复现。
    chunk_id = f"{EXTERNAL_DATABASE_NAME}:{EXTERNAL_TABLE_NAME}:{external_id}"
    # 2026-06-10 18:01:50 修改：生成完整来源摘录，理由是 validate_chunks_before_qdrant 要能看到完整答案。
    source_excerpt_full = f"客户原话：{customer_text}\n客服原话：{service_text}\n答案：{answer}"
    # 2026-06-10 18:01:50 修改：生成清洗文本，作用是兼容现有 cleaned_text 字段。
    cleaned_text = f"问题：{question}\n场景：{question_scene}\n答案：{answer}"
    # 2026-06-10 18:01:50 修改：生成 LLM 消费文本，理由是 Qdrant payload 的 text 字段保持答案优先。
    llm_text = f"问题：{standard_question}\n答案：{answer}\n证据：{source_excerpt_full}"
    # 2026-06-10 18:01:50 修改：生成检索文本，作用是复用现有 build_embedding_text 逻辑的优先入口。
    retrieval_text = f"业务场景：{question_scene}\n问题：{question}\n规范问题：{standard_question}\n答案：{answer}\n证据：{source_excerpt_full}"
    # 2026-06-10 18:01:50 修改：生成 query aliases，作用是让外部标准问题和原问法都进入关键词索引。
    query_aliases = [standard_question, question]
    # 2026-06-10 18:01:50 修改：生成关键词 JSON，理由是旧 keywords 字段仍然保持字符串契约。
    keywords = json.dumps([question_scene, standard_question, answer_completeness], ensure_ascii=False)
    # 2026-06-10 18:01:50 修改：生成 payload_json，作用是对齐现有 canonical chunk 新契约字段。
    payload_json = {
        # 2026-06-10 18:01:50 修改：写入问题，作用是现有 loader 优先读取 payload_json.question。
        "question": question,
        # 2026-06-10 18:01:50 修改：写入答案，作用是现有 loader 优先读取 answer_text。
        "answer_text": answer,
        # 2026-06-10 18:01:50 修改：写入规范问题，作用是现有 payload 保持 canonical_question。
        "canonical_question": standard_question,
        # 2026-06-10 18:01:50 修改：写入别名问法，作用是进入 keyword_terms。
        "query_aliases": query_aliases,
        # 2026-06-10 18:01:50 修改：写入完整来源，理由是同步前契约校验要包含答案。
        "source_excerpt_full": source_excerpt_full,
        # 2026-06-10 18:01:50 修改：写入 LLM 文本，作用是 Qdrant text payload 直接消费。
        "llm_text": llm_text,
        # 2026-06-10 18:01:50 修改：写入检索文本，作用是 embedding 输入保持统一。
        "retrieval_text": retrieval_text,
        # 2026-06-10 18:01:50 修改：写入 evidence，理由是保留截图中的 customer_text/service_text 结构。
        "evidence": {"customer_text": customer_text, "service_text": service_text},
        # 2026-06-10 18:01:50 修改：写入 ready 标记，作用是让现有校验通过。
        "qdrant_ready": True,
        # 2026-06-10 18:01:50 修改：写入 payload 版本，作用是后续排查外部扁平表来源。
        "payload_schema_version": "external-flat-qa-v1",
        # 2026-06-10 18:01:50 修改：写入 RAG 契约版本，作用是保持现有下游筛选字段。
        "rag_contract_version": "qa-rag-contract-v1",
    }
    # 2026-06-10 18:01:50 修改：返回 CanonicalChunk，理由是后续必须复用现有 Qdrant 同步函数。
    return qdrant_sync.CanonicalChunk(
        # 2026-06-10 18:01:50 修改：写入 chunk_id，作用是稳定生成 Qdrant point id。
        chunk_id=chunk_id,
        # 2026-06-10 18:01:50 修改：写入 document_id，作用是兼容 LlamaIndex doc_id。
        document_id=document_id,
        # 2026-06-10 18:01:50 修改：外部库无音频编号，使用 0 保持字段类型。
        audio_no=0,
        # 2026-06-10 18:01:50 修改：写入音频标题为外部库名，作用是便于 Qdrant UI 排查来源。
        audio_title=EXTERNAL_DATABASE_NAME,
        # 2026-06-10 18:01:50 修改：写入 chunk_index，作用是保持外部行顺序。
        chunk_index=external_id,
        # 2026-06-10 18:01:50 修改：写入业务场景，作用是支持 scene filter。
        scene=question_scene,
        # 2026-06-10 18:01:50 修改：写入问题，作用是支持问答检索。
        question=question,
        # 2026-06-10 18:01:50 修改：写入答案，作用是支持答案优先 RAG。
        answer=answer,
        # 2026-06-10 18:01:50 修改：写入清洗文本，作用是兼容旧字段。
        cleaned_text=cleaned_text,
        # 2026-06-10 18:01:50 修改：外部样例无步骤表，写空 JSON 列表。
        resolution_steps="[]",
        # 2026-06-10 18:01:50 修改：写入关键词字符串，作用是兼容旧 payload。
        keywords=keywords,
        # 2026-06-10 18:01:50 修改：写入实体 JSON，作用是兼容旧 payload。
        entities_json="{}",
        # 2026-06-10 18:01:50 修改：写入来源摘录，作用是支持回溯证据。
        source_excerpt=source_excerpt_full,
        # 2026-06-10 18:01:50 修改：写入内容 hash，作用是支持幂等和排查。
        content_hash=stable_hash(chunk_id, question, answer),
        # 2026-06-10 18:01:50 修改：写入 QA 对 ID，作用是兼容同步状态。
        qa_pair_id=f"external-qa-{external_id}",
        # 2026-06-10 18:01:50 修改：写入 QA 对序号，作用是兼容同步状态。
        qa_pair_index=external_id,
        # 2026-06-10 18:01:50 修改：写入相似度分数，理由是外部样例默认可信。
        qa_similarity_score=1.0,
        # 2026-06-10 18:01:50 修改：写入相似度阈值，作用是保持字段类型稳定。
        qa_similarity_threshold=0.0,
        # 2026-06-10 18:01:50 修改：标记 QA 已校验，理由是外部样例跳过原清洗流程但要入 Qdrant。
        qa_pair_validated=True,
        # 2026-06-10 18:01:50 修改：写入文档内聚类 ID，作用是保留过滤字段。
        cluster_id=f"external-cluster-{external_id}",
        # 2026-06-10 18:01:50 修改：写入文档内聚类标签，作用是保留过滤字段。
        cluster_label=question_scene,
        # 2026-06-10 18:01:50 修改：写入文档内层级，作用是保留过滤字段。
        cluster_level="external",
        # 2026-06-10 18:01:50 修改：写入文档内路径，作用是保留过滤字段。
        cluster_path=f"{EXTERNAL_DATABASE_NAME}/{question_scene}",
        # 2026-06-10 18:01:50 修改：写入全局聚类 ID，作用是保留过滤字段。
        global_cluster_id="external-global",
        # 2026-06-10 18:01:50 修改：写入全局聚类标签，作用是保留过滤字段。
        global_cluster_label="外部库模拟问答",
        # 2026-06-10 18:01:50 修改：写入全局层级，作用是保留过滤字段。
        global_cluster_level="external",
        # 2026-06-10 18:01:50 修改：写入全局路径，作用是保留过滤字段。
        global_cluster_path=f"{EXTERNAL_DATABASE_NAME}/外部库模拟问答",
        # 2026-06-10 18:01:50 修改：写入问题 hash，作用是兼容同问消歧。
        question_hash=stable_hash(question),
        # 2026-06-10 18:01:50 修改：写入答案 hash，作用是兼容同答融合。
        answer_hash=stable_hash(answer),
        # 2026-06-10 18:01:50 修改：写入 canonical_chunk_id，作用是保持融合字段。
        canonical_chunk_id=chunk_id,
        # 2026-06-10 18:01:50 修改：标记 canonical，理由是 duplicate 不进入 Qdrant。
        fusion_status="canonical",
        # 2026-06-10 18:01:50 修改：写入 payload schema 版本，作用是排查来源。
        payload_schema_version="external-flat-qa-v1",
        # 2026-06-10 18:01:50 修改：写入 payload_json，作用是复用现有同步契约。
        payload_json=payload_json,
        # 2026-06-10 18:01:50 修改：写入 RAG 契约版本，作用是兼容现有下游筛选。
        rag_contract_version="qa-rag-contract-v1",
        # 2026-06-10 18:01:50 修改：写入规范问题，作用是支持标准问法检索。
        canonical_question=standard_question,
        # 2026-06-10 18:01:50 修改：写入答案优先字段，作用是保持回答精准链路。
        answer_text=answer,
        # 2026-06-10 18:01:50 修改：写入别名问法，作用是支持关键词字段生成。
        query_aliases=query_aliases,
        # 2026-06-10 18:01:50 修改：写入完整来源摘录，理由是同步校验必须包含答案。
        source_excerpt_full=source_excerpt_full,
        # 2026-06-10 18:01:50 修改：写入 LLM 文本，作用是 Qdrant text payload。
        llm_text=llm_text,
        # 2026-06-10 18:01:50 修改：写入检索文本，作用是 embedding 输入。
        retrieval_text=retrieval_text,
        # 2026-06-10 18:01:50 修改：外部样例无 duplicate，写空列表。
        duplicate_contexts=[],
        # 2026-06-10 18:01:50 修改：外部样例无 merged duplicate，写空列表。
        merged_duplicate_chunk_ids=[],
        # 2026-06-10 18:01:50 修改：标记可同步，理由是后续 validate_chunks_before_qdrant 需要通过。
        qdrant_ready=True,
        # 2026-06-10 18:01:50 修改：外部样例无校验错误，写空列表。
        validation_flags=[],
    )


# 2026-06-10 18:01:50 修改：批量转换外部行，理由是转换入口要返回 list[CanonicalChunk] 给现有链路。
def external_rows_to_canonical_chunks(rows: list[Any], source_profile: Any | None = None) -> list[qdrant_sync.CanonicalChunk]:
    # 2026-06-11 15:54:56 修改：解析默认外部库 profile；作用：批量转换只加载一次配置；理由：减少重复读取 YAML 并保持整批字段策略一致。
    resolved_profile = source_profile or qdrant_mapping_profile.load_source_profile("external_database")
    # 2026-06-10 18:01:50 修改：逐行转换，作用是复用单行映射逻辑。
    return [external_row_to_canonical_chunk(row, resolved_profile) for row in rows]


# 2026-06-10 18:01:50 修改：初始化 External_database，理由是模拟外部库可由脚本一键创建。
def initialize_external_database(config: qdrant_sync.SqlServerConfig) -> None:
    # 2026-06-10 18:01:50 修改：构造 master 连接配置，理由是 CREATE DATABASE 必须先连到已有库。
    master_config = qdrant_sync.SqlServerConfig(
        # 2026-06-10 18:01:50 修改：复用外部 SQL Server 地址，作用是同一个模拟服务端口。
        server=config.server,
        # 2026-06-10 18:01:50 修改：连接 master，理由是目标库可能尚不存在。
        database="master",
        # 2026-06-10 18:01:50 修改：复用用户名，作用是保持连接权限一致。
        user=config.user,
        # 2026-06-10 18:01:50 修改：复用密码，作用是保持连接权限一致。
        password=config.password,
        # 2026-06-10 18:01:50 修改：复用 ODBC driver，作用是保持连接方式一致。
        driver=config.driver,
    )
    # 2026-06-10 18:01:50 修改：连接 master，作用是创建 External_database。
    with qdrant_sync.pyodbc.connect(qdrant_sync.sqlserver_connection_string(master_config), autocommit=True) as connection:
        # 2026-06-10 18:01:50 修改：执行建库语句，理由是不存在时才创建。
        connection.cursor().execute(f"IF DB_ID(N'{EXTERNAL_DATABASE_NAME}') IS NULL CREATE DATABASE [{EXTERNAL_DATABASE_NAME}];")
    # 2026-06-10 18:01:50 修改：连接 External_database，作用是建表和写入种子数据。
    with qdrant_sync.pyodbc.connect(qdrant_sync.sqlserver_connection_string(config), autocommit=True) as connection:
        # 2026-06-10 18:01:50 修改：创建 cursor，作用是执行初始化 SQL。
        cursor = connection.cursor()
        # 2026-06-10 18:01:50 修改：执行建表语句，理由是表不存在时创建。
        cursor.execute(
            f"""
IF OBJECT_ID(N'[{EXTERNAL_SCHEMA_NAME}].[{EXTERNAL_TABLE_NAME}]', N'U') IS NULL
CREATE TABLE [{EXTERNAL_SCHEMA_NAME}].[{EXTERNAL_TABLE_NAME}] (
    [id] INT NOT NULL,
    [external_id] INT NOT NULL PRIMARY KEY,
    [question] NVARCHAR(MAX) NOT NULL,
    [question_scene] NVARCHAR(MAX) NOT NULL,
    [answer] NVARCHAR(MAX) NOT NULL,
    [standard_question] NVARCHAR(MAX) NOT NULL,
    [answer_completeness] NVARCHAR(50) NOT NULL,
    [customer_text] NVARCHAR(MAX) NOT NULL,
    [service_text] NVARCHAR(MAX) NOT NULL,
    [created_at] DATETIME2(0) NOT NULL DEFAULT SYSUTCDATETIME(),
    [updated_at] DATETIME2(0) NOT NULL DEFAULT SYSUTCDATETIME()
);
"""
        )
        # 2026-06-12 14:40:11 修改：给已有 External_database 表补 id 列；作用：重复运行初始化时不需要删卷；理由：用户要求当前关系型库立即新增 id 字段。
        cursor.execute(
            """
IF COL_LENGTH(N'dbo.external_qa_samples', N'id') IS NULL
BEGIN
    ALTER TABLE [dbo].[external_qa_samples] ADD [id] INT NULL;
END;
UPDATE [dbo].[external_qa_samples] SET [id] = [external_id] WHERE [id] IS NULL;
IF EXISTS (
    SELECT 1
    FROM sys.columns
    WHERE object_id = OBJECT_ID(N'dbo.external_qa_samples')
      AND name = N'id'
      AND is_nullable = 1
)
BEGIN
    ALTER TABLE [dbo].[external_qa_samples] ALTER COLUMN [id] INT NOT NULL;
END;
"""
        )
        # 2026-06-11 19:57:10 修改：创建外部库同步状态表，理由是 Qdrant 写入后必须回写 rag_rag_sync_state。
        cursor.execute(
            """
IF OBJECT_ID(N'[dbo].[rag_rag_sync_state]', N'U') IS NULL
CREATE TABLE [dbo].[rag_rag_sync_state] (
    [sync_id] NVARCHAR(80) NOT NULL PRIMARY KEY,
    [document_id] NVARCHAR(80) NOT NULL,
    [content_hash] NVARCHAR(64) NOT NULL,
    [sync_target] NVARCHAR(120) NOT NULL,
    [sync_status] NVARCHAR(40) NOT NULL,
    [chunk_count] INT NOT NULL,
    [needs_reindex] BIT NOT NULL,
    [sync_message] NVARCHAR(MAX) NULL,
    [created_at] DATETIME2(0) NOT NULL DEFAULT SYSUTCDATETIME(),
    [updated_at] DATETIME2(0) NOT NULL DEFAULT SYSUTCDATETIME()
);
"""
        )
        # 2026-06-10 18:01:50 修改：清空旧样例，作用是重复执行保持三条数据稳定。
        cursor.execute(f"DELETE FROM [{EXTERNAL_SCHEMA_NAME}].[{EXTERNAL_TABLE_NAME}];")
        # 2026-06-10 18:01:50 修改：遍历样例行，理由是用户要求生成三条数据。
        for row in EXTERNAL_SAMPLE_ROWS:
            # 2026-06-10 18:01:50 修改：参数化插入样例，作用是避免中文和引号破坏 SQL。
            cursor.execute(
                f"""
INSERT INTO [{EXTERNAL_SCHEMA_NAME}].[{EXTERNAL_TABLE_NAME}]
([id], [external_id], [question], [question_scene], [answer], [standard_question], [answer_completeness], [customer_text], [service_text])
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
""",
                int(row["id"]),
                int(row["external_id"]),
                row["question"],
                row["question_scene"],
                row["answer"],
                row["standard_question"],
                row["answer_completeness"],
                row["customer_text"],
                row["service_text"],
            )


# 2026-06-10 18:01:50 修改：从 External_database 读取扁平 QA 行，理由是跳过原清洗入库也能进入统一 CanonicalChunk。
def load_external_rows_from_sqlserver(config: qdrant_sync.SqlServerConfig, source_profile: Any | None = None) -> list[Any]:
    # 2026-06-11 15:54:56 修改：解析外部库 profile；作用：SELECT 字段和来源表都从配置读取；理由：后续接入 MySQL/PostgreSQL/API 风格字段时不能改转换链路。
    resolved_profile = source_profile or qdrant_mapping_profile.load_source_profile("external_database")
    # 2026-06-11 15:54:56 修改：按 profile 生成读取 SQL；作用：只读取 select.fields 声明字段；理由：外部库字段选择必须动态配置。
    sql = qdrant_mapping_profile.build_select_sql(resolved_profile)
    # 2026-06-10 18:01:50 修改：打开外部 SQL Server 连接，作用是读取模拟外部库数据。
    with qdrant_sync.pyodbc.connect(qdrant_sync.sqlserver_connection_string(config)) as connection:
        # 2026-06-10 18:01:50 修改：执行查询并返回行，理由是后续转换函数支持 pyodbc.Row。
        return list(connection.cursor().execute(sql).fetchall())


# 2026-06-10 18:01:50 修改：读取 External_database 并转换成 CanonicalChunk，理由是后续 Qdrant 同步链路保持一套。
def load_external_canonical_chunks_from_sqlserver(config: qdrant_sync.SqlServerConfig, source_profile: Any | None = None) -> list[qdrant_sync.CanonicalChunk]:
    # 2026-06-11 15:54:56 修改：解析外部库 profile；作用：读取和转换使用同一份字段策略；理由：避免 SELECT 字段和 payload/embedding 字段不一致。
    resolved_profile = source_profile or qdrant_mapping_profile.load_source_profile("external_database")
    # 2026-06-10 18:01:50 修改：读取外部表行，作用是获取截图字段数据。
    rows = load_external_rows_from_sqlserver(config, resolved_profile)
    # 2026-06-10 18:01:50 修改：转换为 CanonicalChunk，理由是现有 Qdrant 同步函数只消费 CanonicalChunk。
    return external_rows_to_canonical_chunks(rows, resolved_profile)


# 2026-06-13 17:18:04 新增：按 source profile 读取任意外部关系库行；作用：PG/SQLServer 离线转换共享 adapter registry；理由：新增外部库不能再改一次 Python 分支。
def load_external_rows_from_profile(source_profile: Any) -> list[dict[str, Any]]:
    # 2026-06-13 17:18:04 新增：创建默认 adapter registry；作用：按 connection.engine 分发到 PG/SQLServer；理由：读取逻辑由 adapter 隔离。
    registry = build_default_external_adapter_registry()
    # 2026-06-13 17:18:04 新增：创建 profile 对应 adapter；作用：连接目标外部库；理由：profile 是连接和字段策略入口。
    adapter = registry.create_from_profile(source_profile)
    # 2026-06-13 17:18:04 新增：读取 rows；作用：返回 dict 行；理由：后续 canonical 转换不关心数据库类型。
    return adapter.fetch_rows(source_profile)


# 2026-06-13 17:18:04 新增：按 source profile 读取并转换任意外部关系库；作用：PG/SQLServer 都转成 CanonicalChunk；理由：Qdrant 写入链路只消费统一 chunk。
def load_external_canonical_chunks_from_profile(source_profile: Any) -> list[qdrant_sync.CanonicalChunk]:
    # 2026-06-13 17:18:04 新增：读取外部库 dict rows；作用：拿到 YAML select.fields 的结果；理由：字段选择不写死。
    rows = load_external_rows_from_profile(source_profile)
    # 2026-06-13 17:18:04 新增：转换 canonical chunks；作用：复用现有 validate/embed/build/upsert；理由：不新增第二套 Qdrant 链路。
    return external_rows_to_canonical_chunks(rows, source_profile)
