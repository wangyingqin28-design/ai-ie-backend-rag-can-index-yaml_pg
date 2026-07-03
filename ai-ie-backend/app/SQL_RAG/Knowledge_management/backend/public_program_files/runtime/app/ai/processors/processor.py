# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
'\n文件处理服务主模块\n\n提供单文件 / 文件夹批处理的统一入口，支持：\n- 图像识别 / OCR\n- 文档解析（支持 OCR 回退）\n- 长音频转录\n- 纯文本读取\n- 结果导出（可选）\n- 结果转换为索引项（供 Qdrant 等向量库使用）\n- Qdrant 索引便捷封装\n'
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
from typing import Any, Literal
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
# [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
# 各类型文件的处理函数
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
from .audio_long_service import transcribe_long_audio
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
from .document_service import process_document_file, process_text_file
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
from .file_utils import get_file_type, get_supported_files, validate_file
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
from .image_service import ocr_image, recognize_image
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
# [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
# 处理模式的类型别名
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
Mode = Literal["auto", "recognize", "ocr", "parse", "audio"]
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：公共程序层所有；本行属于异步函数 process_file
async def process_file(
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_file
    file_path: str,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
    mode: Mode = "auto",
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
    export: bool = False,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
    output_dir: str | None = None,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
    summary_prompt: str | None = None,
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 process_file
) -> dict[str, Any]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 process_file
    '解析一个受支持的文件，并返回一个规范化的处理结果。\n\n    参数:\n        file_path: 文件的本地路径。\n        mode: 处理模式，可选值："auto"（自动识别）、"recognize"（图像识别）、\n              "ocr"（OCR）、"parse"（文档解析）、"audio"（音频转录）。\n        export: 是否导出处理结果（生成 Markdown、文本文件等）。\n        output_dir: 导出目录，若为 None 则在文件所在目录下创建 "exports" 子目录。\n        summary_prompt: 导出时使用的摘要提示词（可选）。\n\n    返回:\n        字典，包含处理状态、引擎、文本结果等字段。失败时 "success" 为 False。\n    '
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于异步函数 process_file
    # 1. 校验文件（返回 Path 对象）
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
    file = validate_file(file_path)
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
    file_path = str(file)
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于异步函数 process_file
    # 2. 识别文件大类：image / document / audio / text
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
    file_type = get_file_type(file_path)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 process_file
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
    result = None
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
    engine = ""          # 记录实际使用的引擎
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
    raw_text = ""        # 提取出的纯文本
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
    extra: dict[str, Any] = {}  # 额外信息
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 process_file
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于异步函数 process_file
    # 3. 根据文件类型和 mode 分发处理
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于异步函数 process_file
    if file_type == "image":
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于异步函数 process_file
        if mode == "ocr":
            # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于异步函数 process_file
            # 图像 OCR 模式
            # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：公共程序层所有；本行属于异步函数 process_file
            result = await ocr_image(file_path)
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
            engine = "vision_ocr"
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于异步函数 process_file
        else:
            # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于异步函数 process_file
            # 默认图像识别（视觉大模型描述）
            # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：公共程序层所有；本行属于异步函数 process_file
            result = await recognize_image(file_path)
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
            engine = "vision"
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
        raw_text = str(result or "")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 process_file
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于异步函数 process_file
    elif file_type == "document":
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于异步函数 process_file
        # 文档（PDF、Word 等）：可选择是否强制 OCR
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 process_file
        parse_method = "ocr" if mode == "ocr" else "auto"
        # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：公共程序层所有；本行属于异步函数 process_file
        result = await process_document_file(
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
            file_path=file_path,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
            parse_method=parse_method,
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 process_file
        )
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 process_file
        engine = "docling_ocr" if parse_method == "ocr" else "docling"
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
        raw_text = result.get("markdown", "") if isinstance(result, dict) else ""
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
        extra["parse_method"] = parse_method
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 process_file
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于异步函数 process_file
    elif file_type == "audio":
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于异步函数 process_file
        # 长音频转录（自动分片 300s）
        # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：公共程序层所有；本行属于异步函数 process_file
        result = await transcribe_long_audio(
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
            audio_path=file_path,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
            chunk_seconds=300,
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 process_file
        )
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
        engine = "audio_asr_long"
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
        raw_text = result.get("text", "") if isinstance(result, dict) else ""
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 process_file
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于异步函数 process_file
    elif file_type == "text":
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于异步函数 process_file
        # 纯文本文件直接读取
        # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：公共程序层所有；本行属于异步函数 process_file
        result = await process_text_file(file_path)
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
        engine = "text"
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
        raw_text = result.get("text", "") if isinstance(result, dict) else ""
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 process_file
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于异步函数 process_file
    else:
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于异步函数 process_file
        # 不支持的文件类型
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于异步函数 process_file
        return {
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_file
            "success": False,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_file
            "file_path": file_path,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_file
            "file_name": file.name,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_file
            "file_type": "unsupported",
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_file
            "engine": "unsupported",
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_file
            "mode": mode,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_file
            "error": "Unsupported file type",
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 process_file
        }
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 process_file
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于异步函数 process_file
    # 4. 组装标准化结果
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
    processed = {
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_file
        "success": True,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_file
        "file_path": file_path,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_file
        "file_name": file.name,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_file
        "file_type": file_type,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_file
        "engine": engine,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_file
        "mode": mode,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_file
        "result": result,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_file
        **extra,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 process_file
    }
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 process_file
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于异步函数 process_file
    # 5. 如果需要导出，调用导出服务
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于异步函数 process_file
    if export:
        # [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于异步函数 process_file
        from .export_service import export_processed_result
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 process_file
        # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：公共程序层所有；本行属于异步函数 process_file
        processed["exports"] = await export_processed_result(
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
            processed=processed,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
            raw_text=raw_text,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
            output_dir=output_dir or str(file.parent / "exports"),
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_file
            summary_prompt=summary_prompt,
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 process_file
        )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 process_file
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于异步函数 process_file
    return processed
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：公共程序层所有；本行属于异步函数 process_folder
async def process_folder(
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_folder
    folder_path: str,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_folder
    mode: Mode = "auto",
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_folder
    recursive: bool = False,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_folder
    export: bool = False,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_folder
    output_dir: str | None = None,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_folder
    summary_prompt: str | None = None,
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 process_folder
) -> dict[str, Any]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 process_folder
    '解析文件夹中所有受支持的文件。\n\n    参数:\n        folder_path: 文件夹路径。\n        mode: 处理模式，同 process_file。\n        recursive: 是否递归处理子文件夹。\n        export: 是否导出每个文件的处理结果。\n        output_dir: 导出根目录。\n        summary_prompt: 导出摘要提示词。\n\n    返回:\n        包含总数和结果列表的字典。\n    '
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于异步函数 process_folder
    # 1. 获取所有受支持文件的列表
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_folder
    files = get_supported_files(folder_path, recursive=recursive)
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_folder
    results = []
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 process_folder
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于异步函数 process_folder
    # 2. 逐个处理，捕获异常避免中断整体流程
    # [2026-07-03 16:33:01] 作用：逐项处理集合或重复任务；理由依据：公共程序层所有；本行属于异步函数 process_folder
    for file_path in files:
        # [2026-07-03 16:33:01] 作用：控制异常处理和资源清理；理由依据：公共程序层所有；本行属于异步函数 process_folder
        try:
            # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：公共程序层所有；本行属于异步函数 process_folder
            result = await process_file(
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_folder
                file_path=file_path,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_folder
                mode=mode,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_folder
                export=export,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_folder
                output_dir=output_dir,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 process_folder
                summary_prompt=summary_prompt,
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 process_folder
            )
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 process_folder
            results.append(result)
        # [2026-07-03 16:33:01] 作用：控制异常处理和资源清理；理由依据：公共程序层所有；本行属于异步函数 process_folder
        except Exception as exc:
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_folder
            results.append({
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_folder
                "success": False,
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_folder
                "file_path": file_path,
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_folder
                "mode": mode,
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_folder
                "error": str(exc),
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 process_folder
            })
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 process_folder
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于异步函数 process_folder
    return {
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_folder
        "success": True,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_folder
        "folder_path": folder_path,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_folder
        "mode": mode,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_folder
        "recursive": recursive,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_folder
        "total": len(files),
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 process_folder
        "results": results,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 process_folder
    }
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 to_index_item
def to_index_item(processed: dict[str, Any]) -> dict[str, Any]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 to_index_item
    '将处理后的结果转换为用于索引或问答的文本负载。\n\n    根据文件类型提取对应的文本字段：\n    - 文档：markdown 文本\n    - 文本/音频：text 字段\n    - 图像：result 转字符串\n\n    参数:\n        processed: process_file 返回的字典。\n\n    返回:\n        扁平化的字典，包含 file_path、file_name、file_type、engine 和文本内容。\n    '
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 to_index_item
    result = processed.get("result")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 to_index_item
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 to_index_item
    # 文档类型：提取 markdown
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
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 to_index_item
    # 文本或音频类型：提取纯文本
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
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 to_index_item
    # 图像类型：使用识别结果的字符串形式
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
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 to_index_item
    # 其他未识别类型：返回空文本
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
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
# [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
# 为旧调用方提供的向后兼容别名。
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
_to_index_item = to_index_item
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
async def index_file_to_qdrant(
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
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
) -> dict[str, Any]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    '处理单个文件并直接索引到 Qdrant 向量数据库。\n\n    实际上是调用 knowledge_index_service 中的同名函数。\n    参数:\n        file_path: 文件路径。\n        mode: 处理模式。\n        collection_name: Qdrant 集合名称。\n        kb_id: 知识库 ID。\n        file_id: 自定义文件 ID，若为 None 则自动生成。\n    '
    # [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    from app.services.ai.indexing.knowledge_index_service import index_file_to_qdrant as index_file
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    return await index_file(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
        file_path=file_path,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
        mode=mode,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
        collection_name=collection_name,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
        kb_id=kb_id,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
        file_id=file_id,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_file_to_qdrant
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.processor 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
async def index_folder_to_qdrant(
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
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
) -> dict[str, Any]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    '处理文件夹内所有支持的文件并索引到 Qdrant。\n\n    参数:\n        folder_path: 文件夹路径。\n        mode: 处理模式。\n        recursive: 是否递归。\n        collection_name: Qdrant 集合名称。\n        kb_id: 知识库 ID。\n    '
    # [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    from app.services.ai.indexing.knowledge_index_service import index_folder_to_qdrant as index_folder
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    return await index_folder(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        folder_path=folder_path,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        mode=mode,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        recursive=recursive,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        collection_name=collection_name,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
        kb_id=kb_id,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 index_folder_to_qdrant
    )
