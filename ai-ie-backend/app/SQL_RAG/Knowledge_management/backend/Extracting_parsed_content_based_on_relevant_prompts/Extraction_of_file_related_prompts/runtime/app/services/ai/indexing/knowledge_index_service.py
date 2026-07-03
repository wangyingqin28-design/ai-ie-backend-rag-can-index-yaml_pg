# [2026-07-03 14:26:28] 中文迁移说明：本文件完整复制自 app/services/ai/indexing/knowledge_index_service.py；纳入依据为 DeepSeek 提取入库链 的项目内传递依赖闭包。
from typing import Any

from app.ai.processors.processor import Mode, process_file, process_folder
from app.ai.rag.vector_index_service import upsert_items_to_qdrant


def to_index_item(processed: dict[str, Any]) -> dict[str, Any]:
    """Convert a processed file result into text payload for Qdrant indexing."""
    result = processed.get("result")

    if processed.get("file_type") == "document" and isinstance(result, dict):
        return {
            "file_path": processed.get("file_path", ""),
            "file_name": processed.get("file_name", ""),
            "file_type": "document",
            "engine": processed.get("engine", ""),
            "markdown": result.get("markdown", ""),
        }

    if processed.get("file_type") in {"text", "audio"} and isinstance(result, dict):
        return {
            "file_path": processed.get("file_path", ""),
            "file_name": processed.get("file_name", ""),
            "file_type": processed.get("file_type", ""),
            "engine": processed.get("engine", ""),
            "text": result.get("text", ""),
        }

    if processed.get("file_type") == "image":
        return {
            "file_path": processed.get("file_path", ""),
            "file_name": processed.get("file_name", ""),
            "file_type": "image",
            "engine": processed.get("engine", ""),
            "text": str(result or ""),
        }

    return {
        "file_path": processed.get("file_path", ""),
        "file_name": processed.get("file_name", ""),
        "file_type": processed.get("file_type", ""),
        "engine": processed.get("engine", ""),
        "text": "",
    }


def enrich_index_item(
    *,
    item: dict[str, Any],
    kb_id: str,
    file_id: str,
    mode: Mode,
) -> dict[str, Any]:
    item["kb_id"] = kb_id
    item["file_id"] = file_id
    item["mode"] = mode
    return item


async def index_file_to_qdrant(
    *,
    file_path: str,
    mode: Mode = "auto",
    collection_name: str = "vlmcopy_default",
    kb_id: str = "default",
    file_id: str | None = None,
    include_processed: bool = True,
) -> dict[str, Any]:
    """Parse one file and write its extracted text into a Qdrant hybrid index."""
    processed = await process_file(
        file_path=file_path,
        mode=mode,
    )

    if not processed.get("success"):
        return {
            "success": False,
            "scope": "file",
            "error": processed.get("error", "File processing failed"),
            "processed": processed,
        }

    item = enrich_index_item(
        item=to_index_item(processed),
        kb_id=kb_id,
        file_id=file_id or processed.get("file_name", ""),
        mode=mode,
    )

    index_result = upsert_items_to_qdrant(
        items=[item],
        collection_name=collection_name,
    )

    result = {
        "success": True,
        "scope": "file",
        **index_result,
    }

    if include_processed:
        result["processed"] = processed

    return result


async def index_folder_to_qdrant(
    *,
    folder_path: str,
    mode: Mode = "auto",
    recursive: bool = True,
    collection_name: str = "vlmcopy_default",
    kb_id: str = "default",
    include_processed: bool = False,
) -> dict[str, Any]:
    """Parse supported files in a folder and write them into a Qdrant hybrid index."""
    parsed = await process_folder(
        folder_path=folder_path,
        mode=mode,
        recursive=recursive,
    )

    success_results = [
        item for item in parsed["results"]
        if item.get("success")
    ]

    items = []
    for processed in success_results:
        item = enrich_index_item(
            item=to_index_item(processed),
            kb_id=kb_id,
            file_id=processed.get("file_name", ""),
            mode=mode,
        )
        items.append(item)

    index_result = upsert_items_to_qdrant(
        items=items,
        collection_name=collection_name,
    )

    result = {
        "success": True,
        "scope": "folder",
        "folder_path": folder_path,
        "recursive": recursive,
        "total": parsed["total"],
        "processed_total": len(success_results),
        **index_result,
    }

    if include_processed:
        result["processed"] = parsed

    return result