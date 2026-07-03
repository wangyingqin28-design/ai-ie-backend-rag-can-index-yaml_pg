# [2026-07-03 14:26:27] 中文迁移说明：本文件完整复制自 app/ai/processors/processor.py；纳入依据为 文件解析链 的项目内传递依赖闭包。
"""
文件处理服务主模块

提供单文件 / 文件夹批处理的统一入口，支持：
- 图像识别 / OCR
- 文档解析（支持 OCR 回退）
- 长音频转录
- 纯文本读取
- 结果导出（可选）
- 结果转换为索引项（供 Qdrant 等向量库使用）
- Qdrant 索引便捷封装
"""

from typing import Any, Literal

# 各类型文件的处理函数
from .audio_long_service import transcribe_long_audio
from .document_service import process_document_file, process_text_file
from .file_utils import get_file_type, get_supported_files, validate_file
from .image_service import ocr_image, recognize_image

# 处理模式的类型别名
Mode = Literal["auto", "recognize", "ocr", "parse", "audio"]


async def process_file(
    file_path: str,
    mode: Mode = "auto",
    export: bool = False,
    output_dir: str | None = None,
    summary_prompt: str | None = None,
) -> dict[str, Any]:
    """解析一个受支持的文件，并返回一个规范化的处理结果。

    参数:
        file_path: 文件的本地路径。
        mode: 处理模式，可选值："auto"（自动识别）、"recognize"（图像识别）、
              "ocr"（OCR）、"parse"（文档解析）、"audio"（音频转录）。
        export: 是否导出处理结果（生成 Markdown、文本文件等）。
        output_dir: 导出目录，若为 None 则在文件所在目录下创建 "exports" 子目录。
        summary_prompt: 导出时使用的摘要提示词（可选）。

    返回:
        字典，包含处理状态、引擎、文本结果等字段。失败时 "success" 为 False。
    """
    # 1. 校验文件（返回 Path 对象）
    file = validate_file(file_path)
    file_path = str(file)
    # 2. 识别文件大类：image / document / audio / text
    file_type = get_file_type(file_path)

    result = None
    engine = ""          # 记录实际使用的引擎
    raw_text = ""        # 提取出的纯文本
    extra: dict[str, Any] = {}  # 额外信息

    # 3. 根据文件类型和 mode 分发处理
    if file_type == "image":
        if mode == "ocr":
            # 图像 OCR 模式
            result = await ocr_image(file_path)
            engine = "vision_ocr"
        else:
            # 默认图像识别（视觉大模型描述）
            result = await recognize_image(file_path)
            engine = "vision"
        raw_text = str(result or "")

    elif file_type == "document":
        # 文档（PDF、Word 等）：可选择是否强制 OCR
        parse_method = "ocr" if mode == "ocr" else "auto"
        result = await process_document_file(
            file_path=file_path,
            parse_method=parse_method,
        )
        engine = "docling_ocr" if parse_method == "ocr" else "docling"
        raw_text = result.get("markdown", "") if isinstance(result, dict) else ""
        extra["parse_method"] = parse_method

    elif file_type == "audio":
        # 长音频转录（自动分片 300s）
        result = await transcribe_long_audio(
            audio_path=file_path,
            chunk_seconds=300,
        )
        engine = "audio_asr_long"
        raw_text = result.get("text", "") if isinstance(result, dict) else ""

    elif file_type == "text":
        # 纯文本文件直接读取
        result = await process_text_file(file_path)
        engine = "text"
        raw_text = result.get("text", "") if isinstance(result, dict) else ""

    else:
        # 不支持的文件类型
        return {
            "success": False,
            "file_path": file_path,
            "file_name": file.name,
            "file_type": "unsupported",
            "engine": "unsupported",
            "mode": mode,
            "error": "Unsupported file type",
        }

    # 4. 组装标准化结果
    processed = {
        "success": True,
        "file_path": file_path,
        "file_name": file.name,
        "file_type": file_type,
        "engine": engine,
        "mode": mode,
        "result": result,
        **extra,
    }

    # 5. 如果需要导出，调用导出服务
    if export:
        from .export_service import export_processed_result

        processed["exports"] = await export_processed_result(
            processed=processed,
            raw_text=raw_text,
            output_dir=output_dir or str(file.parent / "exports"),
            summary_prompt=summary_prompt,
        )

    return processed


async def process_folder(
    folder_path: str,
    mode: Mode = "auto",
    recursive: bool = False,
    export: bool = False,
    output_dir: str | None = None,
    summary_prompt: str | None = None,
) -> dict[str, Any]:
    """解析文件夹中所有受支持的文件。

    参数:
        folder_path: 文件夹路径。
        mode: 处理模式，同 process_file。
        recursive: 是否递归处理子文件夹。
        export: 是否导出每个文件的处理结果。
        output_dir: 导出根目录。
        summary_prompt: 导出摘要提示词。

    返回:
        包含总数和结果列表的字典。
    """
    # 1. 获取所有受支持文件的列表
    files = get_supported_files(folder_path, recursive=recursive)
    results = []

    # 2. 逐个处理，捕获异常避免中断整体流程
    for file_path in files:
        try:
            result = await process_file(
                file_path=file_path,
                mode=mode,
                export=export,
                output_dir=output_dir,
                summary_prompt=summary_prompt,
            )
            results.append(result)
        except Exception as exc:
            results.append({
                "success": False,
                "file_path": file_path,
                "mode": mode,
                "error": str(exc),
            })

    return {
        "success": True,
        "folder_path": folder_path,
        "mode": mode,
        "recursive": recursive,
        "total": len(files),
        "results": results,
    }


def to_index_item(processed: dict[str, Any]) -> dict[str, Any]:
    """将处理后的结果转换为用于索引或问答的文本负载。

    根据文件类型提取对应的文本字段：
    - 文档：markdown 文本
    - 文本/音频：text 字段
    - 图像：result 转字符串

    参数:
        processed: process_file 返回的字典。

    返回:
        扁平化的字典，包含 file_path、file_name、file_type、engine 和文本内容。
    """
    result = processed.get("result")

    # 文档类型：提取 markdown
    if processed.get("file_type") == "document" and isinstance(result, dict):
        return {
            "file_path": processed.get("file_path", ""),
            "file_name": processed.get("file_name", ""),
            "file_type": "document",
            "engine": processed.get("engine", ""),
            "markdown": result.get("markdown", ""),
        }

    # 文本或音频类型：提取纯文本
    if processed.get("file_type") in {"text", "audio"} and isinstance(result, dict):
        return {
            "file_path": processed.get("file_path", ""),
            "file_name": processed.get("file_name", ""),
            "file_type": processed.get("file_type", ""),
            "engine": processed.get("engine", ""),
            "text": result.get("text", ""),
        }

    # 图像类型：使用识别结果的字符串形式
    if processed.get("file_type") == "image":
        return {
            "file_path": processed.get("file_path", ""),
            "file_name": processed.get("file_name", ""),
            "file_type": "image",
            "engine": processed.get("engine", ""),
            "text": str(result or ""),
        }

    # 其他未识别类型：返回空文本
    return {
        "file_path": processed.get("file_path", ""),
        "file_name": processed.get("file_name", ""),
        "file_type": processed.get("file_type", ""),
        "engine": processed.get("engine", ""),
        "text": "",
    }


# 为旧调用方提供的向后兼容别名。
_to_index_item = to_index_item


async def index_file_to_qdrant(
    file_path: str,
    mode: Mode = "auto",
    collection_name: str = "vlmcopy_default",
    kb_id: str = "default",
    file_id: str | None = None,
) -> dict[str, Any]:
    """处理单个文件并直接索引到 Qdrant 向量数据库。

    实际上是调用 knowledge_index_service 中的同名函数。
    参数:
        file_path: 文件路径。
        mode: 处理模式。
        collection_name: Qdrant 集合名称。
        kb_id: 知识库 ID。
        file_id: 自定义文件 ID，若为 None 则自动生成。
    """
    from app.services.ai.indexing.knowledge_index_service import index_file_to_qdrant as index_file

    return await index_file(
        file_path=file_path,
        mode=mode,
        collection_name=collection_name,
        kb_id=kb_id,
        file_id=file_id,
    )


async def index_folder_to_qdrant(
    folder_path: str,
    mode: Mode = "auto",
    recursive: bool = True,
    collection_name: str = "vlmcopy_default",
    kb_id: str = "default",
) -> dict[str, Any]:
    """处理文件夹内所有支持的文件并索引到 Qdrant。

    参数:
        folder_path: 文件夹路径。
        mode: 处理模式。
        recursive: 是否递归。
        collection_name: Qdrant 集合名称。
        kb_id: 知识库 ID。
    """
    from app.services.ai.indexing.knowledge_index_service import index_folder_to_qdrant as index_folder

    return await index_folder(
        folder_path=folder_path,
        mode=mode,
        recursive=recursive,
        collection_name=collection_name,
        kb_id=kb_id,
    )