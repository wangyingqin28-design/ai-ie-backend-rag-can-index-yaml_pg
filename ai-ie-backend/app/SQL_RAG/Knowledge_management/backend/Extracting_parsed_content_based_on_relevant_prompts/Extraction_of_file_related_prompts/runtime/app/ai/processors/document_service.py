# [2026-07-03 14:26:28] 中文迁移说明：本文件完整复制自 app/ai/processors/document_service.py；纳入依据为 DeepSeek 提取入库链 的项目内传递依赖闭包。
"""
文档处理服务

基于 Docling 实现文档解析（PDF、Word 等），支持：
- 自动 / OCR 模式
- 导出 Markdown 与 JSON
- 临时使用 LlamaIndex 进行问答
- 纯文本文件读取
"""

from pathlib import Path
from typing import Any

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import OcrAutoOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption


def _safe_export_to_markdown(document: Any) -> str:
    """安全地将 Docling 文档导出为 Markdown 字符串。

    参数:
        document: Docling 解析后的文档对象。

    返回:
        Markdown 文本，如果对象不支持该方法则返回空字符串。
    """
    if hasattr(document, "export_to_markdown"):
        return document.export_to_markdown()
    return ""


def _safe_export_to_dict(document: Any) -> dict[str, Any]:
    """安全地将 Docling 文档导出为字典。

    参数:
        document: Docling 解析后的文档对象。

    返回:
        文档的字典表示，如果对象不支持该方法则返回空字典。
    """
    if hasattr(document, "export_to_dict"):
        return document.export_to_dict()
    return {}


def build_docling_converter(parse_method: str = "auto") -> DocumentConverter:
    """创建配置好的 Docling 转换器，并针对 PDF 设置 OCR 选项。

    参数:
        parse_method: 解析方式，"auto" 表示自动识别，"ocr" 表示强制使用 OCR。

    返回:
        配置完成的 Docling DocumentConverter。
    """
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = parse_method == "ocr"
    pipeline_options.do_table_structure = True
    pipeline_options.do_formula_enrichment = True
    pipeline_options.generate_picture_images = True
    pipeline_options.generate_page_images = True

    if parse_method == "ocr":
        pipeline_options.ocr_options = OcrAutoOptions(
            lang=["ch_sim", "en"],
            force_full_page_ocr=True,
        )

    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
            ),
        }
    )


async def parse_document_with_docling(
    file_path: str,
    parse_method: str = "auto",
) -> dict[str, Any]:
    """使用 Docling 解析文档，并返回 Markdown 与 JSON 两种结果。"""
    file = Path(file_path)
    converter = build_docling_converter(parse_method=parse_method)
    result = converter.convert(str(file))
    document = result.document
    markdown = _safe_export_to_markdown(document)
    document_json = _safe_export_to_dict(document)

    return {
        "file_path": str(file),
        "file_name": file.name,
        "engine": "docling",
        "parse_method": parse_method,
        "markdown": markdown,
        "json": document_json,
    }


async def process_document_file(
    file_path: str,
    parse_method: str = "auto",
) -> dict[str, Any]:
    """文档解析入口，供 processor.py 调用。"""
    return await parse_document_with_docling(
        file_path=file_path,
        parse_method=parse_method,
    )


async def query_document_with_llamaindex(
    file_path: str,
    question: str,
    parse_method: str = "auto",
    similarity_top_k: int = 3,
) -> dict[str, Any]:
    """先用 Docling 解析单个文档，再通过 LlamaIndex 执行检索问答。"""
    parsed = await process_document_file(
        file_path=file_path,
        parse_method=parse_method,
    )

    from .llamaindex_service import query_items_with_llamaindex

    result = query_items_with_llamaindex(
        items=[{
            "file_path": parsed["file_path"],
            "file_name": parsed["file_name"],
            "file_type": "document",
            "engine": parsed["engine"],
            "markdown": parsed["markdown"],
        }],
        question=question,
        similarity_top_k=similarity_top_k,
    )

    return {
        "file_path": parsed["file_path"],
        "file_name": parsed["file_name"],
        "engine": "docling+llamaindex",
        "parse_method": parse_method,
        **result,
    }


async def process_text_file(file_path: str) -> dict[str, str]:
    """读取 UTF-8 纯文本类文件内容，例如 txt、md、csv 和 json。"""
    content = Path(file_path).read_text(encoding="utf-8", errors="ignore")
    return {"text": content}
