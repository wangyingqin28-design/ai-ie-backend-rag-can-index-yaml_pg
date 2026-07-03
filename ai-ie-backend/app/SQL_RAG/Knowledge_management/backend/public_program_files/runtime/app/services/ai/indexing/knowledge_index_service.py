# [2026-07-03 18:11:51] 作用：导入依赖 `from typing import Any`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行属于模块级初始化
from typing import Any
# [2026-07-03 18:11:51] 作用：导入依赖 `from app.ai.processors.processor import Mode, process_file, process_folder`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行属于模块级初始化
from app.ai.processors.processor import Mode, process_file, process_folder
# [2026-07-03 18:11:51] 作用：导入依赖 `from app.ai.rag.vector_index_service import upsert_items_to_qdrant`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行属于模块级初始化
from app.ai.rag.vector_index_service import upsert_items_to_qdrant
# [2026-07-03 18:11:51] 作用：声明同步函数 to_index_item，封装可复用的处理步骤；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
def to_index_item(processed: dict[str, Any]) -> dict[str, Any]:
    # [2026-07-03 18:11:51] 作用：在 to_index_item 中执行具体代码片段 `"""Convert a processed file result into text payload for Qdrant indexing."""`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
    """Convert a processed file result into text payload for Qdrant indexing."""
    # [2026-07-03 18:11:51] 作用：为 result 构造并保存赋值结果；本行执行 `result = processed.get("result")`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
    result = processed.get("result")
    # [2026-07-03 18:11:51] 作用：在 to_index_item 中按条件 `if processed.get("file_type") == "document" and isinstance(result, dict):` 选择执行分支；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
    if processed.get("file_type") == "document" and isinstance(result, dict):
        # [2026-07-03 18:11:51] 作用：从 to_index_item 返回表达式 `return {` 的结果；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
        return {
            # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"file_path": processed.get("file_path", ""),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
            "file_path": processed.get("file_path", ""),
            # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"file_name": processed.get("file_name", ""),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
            "file_name": processed.get("file_name", ""),
            # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"file_type": "document",`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
            "file_type": "document",
            # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"engine": processed.get("engine", ""),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
            "engine": processed.get("engine", ""),
            # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"markdown": result.get("markdown", ""),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
            "markdown": result.get("markdown", ""),
        # [2026-07-03 18:11:51] 作用：在 to_index_item 中执行具体代码片段 `}`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
        }
    # [2026-07-03 18:11:51] 作用：在 to_index_item 中按条件 `if processed.get("file_type") in {"text", "audio"} and isinstance(result, dict):` 选择执行分支；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
    if processed.get("file_type") in {"text", "audio"} and isinstance(result, dict):
        # [2026-07-03 18:11:51] 作用：从 to_index_item 返回表达式 `return {` 的结果；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
        return {
            # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"file_path": processed.get("file_path", ""),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
            "file_path": processed.get("file_path", ""),
            # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"file_name": processed.get("file_name", ""),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
            "file_name": processed.get("file_name", ""),
            # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"file_type": processed.get("file_type", ""),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
            "file_type": processed.get("file_type", ""),
            # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"engine": processed.get("engine", ""),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
            "engine": processed.get("engine", ""),
            # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"text": result.get("text", ""),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
            "text": result.get("text", ""),
        # [2026-07-03 18:11:51] 作用：在 to_index_item 中执行具体代码片段 `}`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
        }
    # [2026-07-03 18:11:51] 作用：在 to_index_item 中按条件 `if processed.get("file_type") == "image":` 选择执行分支；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
    if processed.get("file_type") == "image":
        # [2026-07-03 18:11:51] 作用：从 to_index_item 返回表达式 `return {` 的结果；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
        return {
            # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"file_path": processed.get("file_path", ""),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
            "file_path": processed.get("file_path", ""),
            # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"file_name": processed.get("file_name", ""),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
            "file_name": processed.get("file_name", ""),
            # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"file_type": "image",`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
            "file_type": "image",
            # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"engine": processed.get("engine", ""),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
            "engine": processed.get("engine", ""),
            # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"text": str(result or ""),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
            "text": str(result or ""),
        # [2026-07-03 18:11:51] 作用：在 to_index_item 中执行具体代码片段 `}`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
        }
    # [2026-07-03 18:11:51] 作用：从 to_index_item 返回表达式 `return {` 的结果；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
    return {
        # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"file_path": processed.get("file_path", ""),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
        "file_path": processed.get("file_path", ""),
        # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"file_name": processed.get("file_name", ""),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
        "file_name": processed.get("file_name", ""),
        # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"file_type": processed.get("file_type", ""),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
        "file_type": processed.get("file_type", ""),
        # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"engine": processed.get("engine", ""),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
        "engine": processed.get("engine", ""),
        # [2026-07-03 18:11:51] 作用：完善 同步函数 to_index_item 的签名或多行表达式片段 `"text": "",`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
        "text": "",
    # [2026-07-03 18:11:51] 作用：在 to_index_item 中执行具体代码片段 `}`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 to_index_item
    }
# [2026-07-03 18:11:51] 作用：声明同步函数 enrich_index_item，封装可复用的处理步骤；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 enrich_index_item
def enrich_index_item(
    # [2026-07-03 18:11:51] 作用：完善 同步函数 enrich_index_item 的签名或多行表达式片段 `*,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 enrich_index_item
    *,
    # [2026-07-03 18:11:51] 作用：完善 同步函数 enrich_index_item 的签名或多行表达式片段 `item: dict[str, Any],`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 enrich_index_item
    item: dict[str, Any],
    # [2026-07-03 18:11:51] 作用：完善 同步函数 enrich_index_item 的签名或多行表达式片段 `kb_id: str,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 enrich_index_item
    kb_id: str,
    # [2026-07-03 18:11:51] 作用：完善 同步函数 enrich_index_item 的签名或多行表达式片段 `file_id: str,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 enrich_index_item
    file_id: str,
    # [2026-07-03 18:11:51] 作用：完善 同步函数 enrich_index_item 的签名或多行表达式片段 `mode: Mode,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 enrich_index_item
    mode: Mode,
# [2026-07-03 18:11:51] 作用：在 enrich_index_item 中执行具体代码片段 `) -> dict[str, Any]:`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 enrich_index_item
) -> dict[str, Any]:
    # [2026-07-03 18:11:51] 作用：为 item['kb_id'] 构造并保存赋值结果；本行执行 `item["kb_id"] = kb_id`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 enrich_index_item
    item["kb_id"] = kb_id
    # [2026-07-03 18:11:51] 作用：为 item['file_id'] 构造并保存赋值结果；本行执行 `item["file_id"] = file_id`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 enrich_index_item
    item["file_id"] = file_id
    # [2026-07-03 18:11:51] 作用：为 item['mode'] 构造并保存赋值结果；本行执行 `item["mode"] = mode`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 enrich_index_item
    item["mode"] = mode
    # [2026-07-03 18:11:51] 作用：从 enrich_index_item 返回表达式 `return item` 的结果；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 enrich_index_item
    return item
# [2026-07-03 18:11:51] 作用：声明异步函数 index_file_to_qdrant，提供可等待的链路处理入口；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
async def index_file_to_qdrant(
    # [2026-07-03 18:11:51] 作用：完善 异步函数 index_file_to_qdrant 的签名或多行表达式片段 `*,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
    *,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 index_file_to_qdrant 的签名或多行表达式片段 `file_path: str,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
    file_path: str,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 index_file_to_qdrant 的签名或多行表达式片段 `mode: Mode = "auto",`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
    mode: Mode = "auto",
    # [2026-07-03 18:11:51] 作用：完善 异步函数 index_file_to_qdrant 的签名或多行表达式片段 `collection_name: str = "vlmcopy_default",`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
    collection_name: str = "vlmcopy_default",
    # [2026-07-03 18:11:51] 作用：完善 异步函数 index_file_to_qdrant 的签名或多行表达式片段 `kb_id: str = "default",`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
    kb_id: str = "default",
    # [2026-07-03 18:11:51] 作用：完善 异步函数 index_file_to_qdrant 的签名或多行表达式片段 `file_id: str | None = None,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
    file_id: str | None = None,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 index_file_to_qdrant 的签名或多行表达式片段 `include_processed: bool = True,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
    include_processed: bool = True,
# [2026-07-03 18:11:51] 作用：在 index_file_to_qdrant 中执行具体代码片段 `) -> dict[str, Any]:`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
) -> dict[str, Any]:
    # [2026-07-03 18:11:51] 作用：在 index_file_to_qdrant 中执行具体代码片段 `"""Parse one file and write its extracted text into a Qdrant hybrid index."""`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
    """Parse one file and write its extracted text into a Qdrant hybrid index."""
    # [2026-07-03 18:11:51] 作用：为 processed 构造并保存赋值结果；本行执行 `processed = await process_file(`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
    processed = await process_file(
        # [2026-07-03 18:11:51] 作用：为 processed 构造并保存赋值结果；本行执行 `file_path=file_path,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
        file_path=file_path,
        # [2026-07-03 18:11:51] 作用：为 processed 构造并保存赋值结果；本行执行 `mode=mode,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
        mode=mode,
    # [2026-07-03 18:11:51] 作用：为 processed 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
    )
    # [2026-07-03 18:11:51] 作用：在 index_file_to_qdrant 中按条件 `if not processed.get("success"):` 选择执行分支；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
    if not processed.get("success"):
        # [2026-07-03 18:11:51] 作用：从 index_file_to_qdrant 返回表达式 `return {` 的结果；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
        return {
            # [2026-07-03 18:11:51] 作用：完善 异步函数 index_file_to_qdrant 的签名或多行表达式片段 `"success": False,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
            "success": False,
            # [2026-07-03 18:11:51] 作用：完善 异步函数 index_file_to_qdrant 的签名或多行表达式片段 `"scope": "file",`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
            "scope": "file",
            # [2026-07-03 18:11:51] 作用：完善 异步函数 index_file_to_qdrant 的签名或多行表达式片段 `"error": processed.get("error", "File processing failed"),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
            "error": processed.get("error", "File processing failed"),
            # [2026-07-03 18:11:51] 作用：完善 异步函数 index_file_to_qdrant 的签名或多行表达式片段 `"processed": processed,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
            "processed": processed,
        # [2026-07-03 18:11:51] 作用：在 index_file_to_qdrant 中执行具体代码片段 `}`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
        }
    # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `item = enrich_index_item(`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
    item = enrich_index_item(
        # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `item=to_index_item(processed),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
        item=to_index_item(processed),
        # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `kb_id=kb_id,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
        kb_id=kb_id,
        # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `file_id=file_id or processed.get("file_name", ""),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
        file_id=file_id or processed.get("file_name", ""),
        # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `mode=mode,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
        mode=mode,
    # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
    )
    # [2026-07-03 18:11:51] 作用：为 index_result 构造并保存赋值结果；本行执行 `index_result = upsert_items_to_qdrant(`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
    index_result = upsert_items_to_qdrant(
        # [2026-07-03 18:11:51] 作用：为 index_result 构造并保存赋值结果；本行执行 `items=[item],`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
        items=[item],
        # [2026-07-03 18:11:51] 作用：为 index_result 构造并保存赋值结果；本行执行 `collection_name=collection_name,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
        collection_name=collection_name,
    # [2026-07-03 18:11:51] 作用：为 index_result 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
    )
    # [2026-07-03 18:11:51] 作用：为 result 构造并保存赋值结果；本行执行 `result = {`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
    result = {
        # [2026-07-03 18:11:51] 作用：为 result 构造并保存赋值结果；本行执行 `"success": True,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
        "success": True,
        # [2026-07-03 18:11:51] 作用：为 result 构造并保存赋值结果；本行执行 `"scope": "file",`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
        "scope": "file",
        # [2026-07-03 18:11:51] 作用：为 result 构造并保存赋值结果；本行执行 `**index_result,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
        **index_result,
    # [2026-07-03 18:11:51] 作用：为 result 构造并保存赋值结果；本行执行 `}`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
    }
    # [2026-07-03 18:11:51] 作用：在 index_file_to_qdrant 中按条件 `if include_processed:` 选择执行分支；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
    if include_processed:
        # [2026-07-03 18:11:51] 作用：为 result['processed'] 构造并保存赋值结果；本行执行 `result["processed"] = processed`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
        result["processed"] = processed
    # [2026-07-03 18:11:51] 作用：从 index_file_to_qdrant 返回表达式 `return result` 的结果；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_file_to_qdrant
    return result
# [2026-07-03 18:11:51] 作用：声明异步函数 index_folder_to_qdrant，提供可等待的链路处理入口；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
async def index_folder_to_qdrant(
    # [2026-07-03 18:11:51] 作用：完善 异步函数 index_folder_to_qdrant 的签名或多行表达式片段 `*,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    *,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 index_folder_to_qdrant 的签名或多行表达式片段 `folder_path: str,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    folder_path: str,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 index_folder_to_qdrant 的签名或多行表达式片段 `mode: Mode = "auto",`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    mode: Mode = "auto",
    # [2026-07-03 18:11:51] 作用：完善 异步函数 index_folder_to_qdrant 的签名或多行表达式片段 `recursive: bool = True,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    recursive: bool = True,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 index_folder_to_qdrant 的签名或多行表达式片段 `collection_name: str = "vlmcopy_default",`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    collection_name: str = "vlmcopy_default",
    # [2026-07-03 18:11:51] 作用：完善 异步函数 index_folder_to_qdrant 的签名或多行表达式片段 `kb_id: str = "default",`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    kb_id: str = "default",
    # [2026-07-03 18:11:51] 作用：完善 异步函数 index_folder_to_qdrant 的签名或多行表达式片段 `include_processed: bool = False,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    include_processed: bool = False,
# [2026-07-03 18:11:51] 作用：在 index_folder_to_qdrant 中执行具体代码片段 `) -> dict[str, Any]:`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
) -> dict[str, Any]:
    # [2026-07-03 18:11:51] 作用：在 index_folder_to_qdrant 中执行具体代码片段 `"""Parse supported files in a folder and write them into a Qdrant hybrid index."""`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    """Parse supported files in a folder and write them into a Qdrant hybrid index."""
    # [2026-07-03 18:11:51] 作用：为 parsed 构造并保存赋值结果；本行执行 `parsed = await process_folder(`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    parsed = await process_folder(
        # [2026-07-03 18:11:51] 作用：为 parsed 构造并保存赋值结果；本行执行 `folder_path=folder_path,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
        folder_path=folder_path,
        # [2026-07-03 18:11:51] 作用：为 parsed 构造并保存赋值结果；本行执行 `mode=mode,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
        mode=mode,
        # [2026-07-03 18:11:51] 作用：为 parsed 构造并保存赋值结果；本行执行 `recursive=recursive,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
        recursive=recursive,
    # [2026-07-03 18:11:51] 作用：为 parsed 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    )
    # [2026-07-03 18:11:51] 作用：为 success_results 构造并保存赋值结果；本行执行 `success_results = [`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    success_results = [
        # [2026-07-03 18:11:51] 作用：为 success_results 构造并保存赋值结果；本行执行 `item for item in parsed["results"]`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
        item for item in parsed["results"]
        # [2026-07-03 18:11:51] 作用：为 success_results 构造并保存赋值结果；本行执行 `if item.get("success")`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
        if item.get("success")
    # [2026-07-03 18:11:51] 作用：为 success_results 构造并保存赋值结果；本行执行 `]`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    ]
    # [2026-07-03 18:11:51] 作用：为 items 构造并保存赋值结果；本行执行 `items = []`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    items = []
    # [2026-07-03 18:11:51] 作用：在 index_folder_to_qdrant 中通过 `for processed in success_results:` 迭代处理数据；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    for processed in success_results:
        # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `item = enrich_index_item(`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
        item = enrich_index_item(
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `item=to_index_item(processed),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
            item=to_index_item(processed),
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `kb_id=kb_id,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
            kb_id=kb_id,
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `file_id=processed.get("file_name", ""),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
            file_id=processed.get("file_name", ""),
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `mode=mode,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
            mode=mode,
        # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
        )
        # [2026-07-03 18:11:51] 作用：完善 异步函数 index_folder_to_qdrant 的签名或多行表达式片段 `items.append(item)`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
        items.append(item)
    # [2026-07-03 18:11:51] 作用：为 index_result 构造并保存赋值结果；本行执行 `index_result = upsert_items_to_qdrant(`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    index_result = upsert_items_to_qdrant(
        # [2026-07-03 18:11:51] 作用：为 index_result 构造并保存赋值结果；本行执行 `items=items,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
        items=items,
        # [2026-07-03 18:11:51] 作用：为 index_result 构造并保存赋值结果；本行执行 `collection_name=collection_name,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
        collection_name=collection_name,
    # [2026-07-03 18:11:51] 作用：为 index_result 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    )
    # [2026-07-03 18:11:51] 作用：为 result 构造并保存赋值结果；本行执行 `result = {`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    result = {
        # [2026-07-03 18:11:51] 作用：为 result 构造并保存赋值结果；本行执行 `"success": True,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
        "success": True,
        # [2026-07-03 18:11:51] 作用：为 result 构造并保存赋值结果；本行执行 `"scope": "folder",`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
        "scope": "folder",
        # [2026-07-03 18:11:51] 作用：为 result 构造并保存赋值结果；本行执行 `"folder_path": folder_path,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
        "folder_path": folder_path,
        # [2026-07-03 18:11:51] 作用：为 result 构造并保存赋值结果；本行执行 `"recursive": recursive,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
        "recursive": recursive,
        # [2026-07-03 18:11:51] 作用：为 result 构造并保存赋值结果；本行执行 `"total": parsed["total"],`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
        "total": parsed["total"],
        # [2026-07-03 18:11:51] 作用：为 result 构造并保存赋值结果；本行执行 `"processed_total": len(success_results),`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
        "processed_total": len(success_results),
        # [2026-07-03 18:11:51] 作用：为 result 构造并保存赋值结果；本行执行 `**index_result,`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
        **index_result,
    # [2026-07-03 18:11:51] 作用：为 result 构造并保存赋值结果；本行执行 `}`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    }
    # [2026-07-03 18:11:51] 作用：在 index_folder_to_qdrant 中按条件 `if include_processed:` 选择执行分支；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    if include_processed:
        # [2026-07-03 18:11:51] 作用：为 result['processed'] 构造并保存赋值结果；本行执行 `result["processed"] = parsed`；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
        result["processed"] = parsed
    # [2026-07-03 18:11:51] 作用：从 index_folder_to_qdrant 返回表达式 `return result` 的结果；理由依据：源模块 app.services.ai.indexing.knowledge_index_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 index_folder_to_qdrant
    return result
