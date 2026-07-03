# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.services.ai.indexing.knowledge_index_service 的模块级声明
from typing import Any
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.services.ai.indexing.knowledge_index_service 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.services.ai.indexing.knowledge_index_service 的模块级声明
from app.ai.processors.processor import Mode, process_file, process_folder
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.services.ai.indexing.knowledge_index_service 的模块级声明
from app.ai.rag.vector_index_service import upsert_items_to_qdrant
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.services.ai.indexing.knowledge_index_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.services.ai.indexing.knowledge_index_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 to_index_item
def to_index_item(processed: dict[str, Any]) -> dict[str, Any]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 to_index_item
    """Convert a processed file result into text payload for Qdrant indexing."""
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 to_index_item
    result = processed.get("result")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 to_index_item
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 to_index_item
    if processed.get("file_type") == "document" and isinstance(result, dict):
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 to_index_item
        return {
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
            "file_path": processed.get("file_path", ""),
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
            "file_name": processed.get("file_name", ""),
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
            "file_type": "document",
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
            "engine": processed.get("engine", ""),
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
            "markdown": result.get("markdown", ""),
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 to_index_item
        }
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 to_index_item
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 to_index_item
    if processed.get("file_type") in {"text", "audio"} and isinstance(result, dict):
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 to_index_item
        return {
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
            "file_path": processed.get("file_path", ""),
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
            "file_name": processed.get("file_name", ""),
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
            "file_type": processed.get("file_type", ""),
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
            "engine": processed.get("engine", ""),
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
            "text": result.get("text", ""),
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 to_index_item
        }
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 to_index_item
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 to_index_item
    if processed.get("file_type") == "image":
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 to_index_item
        return {
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
            "file_path": processed.get("file_path", ""),
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
            "file_name": processed.get("file_name", ""),
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
            "file_type": "image",
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
            "engine": processed.get("engine", ""),
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
            "text": str(result or ""),
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 to_index_item
        }
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 to_index_item
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 to_index_item
    return {
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
        "file_path": processed.get("file_path", ""),
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
        "file_name": processed.get("file_name", ""),
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
        "file_type": processed.get("file_type", ""),
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
        "engine": processed.get("engine", ""),
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 to_index_item
        "text": "",
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 to_index_item
    }
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.services.ai.indexing.knowledge_index_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.services.ai.indexing.knowledge_index_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 enrich_index_item
def enrich_index_item(
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 enrich_index_item
    *,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 enrich_index_item
    item: dict[str, Any],
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 enrich_index_item
    kb_id: str,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 enrich_index_item
    file_id: str,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 enrich_index_item
    mode: Mode,
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 enrich_index_item
) -> dict[str, Any]:
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 enrich_index_item
    item["kb_id"] = kb_id
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 enrich_index_item
    item["file_id"] = file_id
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 enrich_index_item
    item["mode"] = mode
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 enrich_index_item
    return item
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.services.ai.indexing.knowledge_index_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.services.ai.indexing.knowledge_index_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
async def index_file_to_qdrant(
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    *,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    file_path: str,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    mode: Mode = "auto",
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    collection_name: str = "vlmcopy_default",
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    kb_id: str = "default",
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    file_id: str | None = None,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    include_processed: bool = True,
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
) -> dict[str, Any]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    """Parse one file and write its extracted text into a Qdrant hybrid index."""
    # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    processed = await process_file(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
        file_path=file_path,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
        mode=mode,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    if not processed.get("success"):
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
        return {
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
            "success": False,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
            "scope": "file",
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
            "error": processed.get("error", "File processing failed"),
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
            "processed": processed,
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
        }
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    item = enrich_index_item(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
        item=to_index_item(processed),
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
        kb_id=kb_id,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
        file_id=file_id or processed.get("file_name", ""),
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
        mode=mode,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    index_result = upsert_items_to_qdrant(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
        items=[item],
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
        collection_name=collection_name,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    result = {
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
        "success": True,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
        "scope": "file",
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
        **index_result,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    }
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    if include_processed:
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
        result["processed"] = processed
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    return result
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.services.ai.indexing.knowledge_index_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.services.ai.indexing.knowledge_index_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
async def index_folder_to_qdrant(
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    *,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    folder_path: str,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    mode: Mode = "auto",
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    recursive: bool = True,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    collection_name: str = "vlmcopy_default",
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    kb_id: str = "default",
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    include_processed: bool = False,
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
) -> dict[str, Any]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    """Parse supported files in a folder and write them into a Qdrant hybrid index."""
    # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    parsed = await process_folder(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        folder_path=folder_path,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        mode=mode,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        recursive=recursive,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    success_results = [
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        item for item in parsed["results"]
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        if item.get("success")
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    ]
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    items = []
    # [2026-07-03 16:33:01] 作用：逐项处理集合或重复任务；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    for processed in success_results:
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        item = enrich_index_item(
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
            item=to_index_item(processed),
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
            kb_id=kb_id,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
            file_id=processed.get("file_name", ""),
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
            mode=mode,
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        )
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        items.append(item)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    index_result = upsert_items_to_qdrant(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        items=items,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        collection_name=collection_name,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    result = {
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        "success": True,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        "scope": "folder",
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        "folder_path": folder_path,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        "recursive": recursive,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        "total": parsed["total"],
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        "processed_total": len(success_results),
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        **index_result,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    }
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    if include_processed:
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        result["processed"] = parsed
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    return result
