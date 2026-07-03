# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
'\n文档处理服务\n\n基于 Docling 实现文档解析（PDF、Word 等），支持：\n- 自动 / OCR 模式\n- 导出 Markdown 与 JSON\n- 临时使用 LlamaIndex 进行问答\n- 纯文本文件读取\n'
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
from pathlib import Path
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
from typing import Any
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
from docling.datamodel.base_models import InputFormat
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
from docling.datamodel.pipeline_options import OcrAutoOptions, PdfPipelineOptions
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
from docling.document_converter import DocumentConverter, PdfFormatOption
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 _safe_export_to_markdown
def _safe_export_to_markdown(document: Any) -> str:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 _safe_export_to_markdown
    '安全地将 Docling 文档导出为 Markdown 字符串。\n\n    参数:\n        document: Docling 解析后的文档对象。\n\n    返回:\n        Markdown 文本，如果对象不支持该方法则返回空字符串。\n    '
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 _safe_export_to_markdown
    if hasattr(document, "export_to_markdown"):
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 _safe_export_to_markdown
        return document.export_to_markdown()
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 _safe_export_to_markdown
    return ""
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 _safe_export_to_dict
def _safe_export_to_dict(document: Any) -> dict[str, Any]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 _safe_export_to_dict
    '安全地将 Docling 文档导出为字典。\n\n    参数:\n        document: Docling 解析后的文档对象。\n\n    返回:\n        文档的字典表示，如果对象不支持该方法则返回空字典。\n    '
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 _safe_export_to_dict
    if hasattr(document, "export_to_dict"):
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 _safe_export_to_dict
        return document.export_to_dict()
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 _safe_export_to_dict
    return {}
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
def build_docling_converter(parse_method: str = "auto") -> DocumentConverter:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
    '创建配置好的 Docling 转换器，并针对 PDF 设置 OCR 选项。\n\n    参数:\n        parse_method: 解析方式，"auto" 表示自动识别，"ocr" 表示强制使用 OCR。\n\n    返回:\n        配置完成的 Docling DocumentConverter。\n    '
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
    pipeline_options = PdfPipelineOptions()
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
    pipeline_options.do_ocr = parse_method == "ocr"
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
    pipeline_options.do_table_structure = True
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
    pipeline_options.do_formula_enrichment = True
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
    pipeline_options.generate_picture_images = True
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
    pipeline_options.generate_page_images = True
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
    if parse_method == "ocr":
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
        pipeline_options.ocr_options = OcrAutoOptions(
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
            lang=["ch_sim", "en"],
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
            force_full_page_ocr=True,
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
        )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
    return DocumentConverter(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
        format_options={
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
            InputFormat.PDF: PdfFormatOption(
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
                pipeline_options=pipeline_options,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
            ),
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
        }
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 build_docling_converter
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
async def parse_document_with_docling(
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
    file_path: str,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
    parse_method: str = "auto",
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
) -> dict[str, Any]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
    """使用 Docling 解析文档，并返回 Markdown 与 JSON 两种结果。"""
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
    file = Path(file_path)
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
    converter = build_docling_converter(parse_method=parse_method)
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
    result = converter.convert(str(file))
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
    document = result.document
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
    markdown = _safe_export_to_markdown(document)
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
    document_json = _safe_export_to_dict(document)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
    return {
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
        "file_path": str(file),
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
        "file_name": file.name,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
        "engine": "docling",
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
        "parse_method": parse_method,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
        "markdown": markdown,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
        "json": document_json,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 parse_document_with_docling
    }
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：公共程序层所有；本行属于异步函数 process_document_file
async def process_document_file(
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_document_file
    file_path: str,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_document_file
    parse_method: str = "auto",
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 process_document_file
) -> dict[str, Any]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 process_document_file
    """文档解析入口，供 processor.py 调用。"""
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于异步函数 process_document_file
    return await parse_document_with_docling(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_document_file
        file_path=file_path,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_document_file
        parse_method=parse_method,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 process_document_file
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
async def query_document_with_llamaindex(
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
    file_path: str,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
    question: str,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
    parse_method: str = "auto",
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
    similarity_top_k: int = 3,
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
) -> dict[str, Any]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
    """先用 Docling 解析单个文档，再通过 LlamaIndex 执行检索问答。"""
    # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
    parsed = await process_document_file(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
        file_path=file_path,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
        parse_method=parse_method,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
    # [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
    from .llamaindex_service import query_items_with_llamaindex
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
    result = query_items_with_llamaindex(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
        items=[{
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
            "file_path": parsed["file_path"],
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
            "file_name": parsed["file_name"],
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
            "file_type": "document",
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
            "engine": parsed["engine"],
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
            "markdown": parsed["markdown"],
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
        }],
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
        question=question,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
        similarity_top_k=similarity_top_k,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
    return {
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
        "file_path": parsed["file_path"],
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
        "file_name": parsed["file_name"],
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
        "engine": "docling+llamaindex",
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
        "parse_method": parse_method,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
        **result,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 query_document_with_llamaindex
    }
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.document_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：公共程序层所有；本行属于异步函数 process_text_file
async def process_text_file(file_path: str) -> dict[str, str]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 process_text_file
    """读取 UTF-8 纯文本类文件内容，例如 txt、md、csv 和 json。"""
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_text_file
    content = Path(file_path).read_text(encoding="utf-8", errors="ignore")
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于异步函数 process_text_file
    return {"text": content}
