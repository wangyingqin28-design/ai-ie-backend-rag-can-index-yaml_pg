# [2026-07-03 18:11:51] 作用：在 模块级初始化 中执行具体代码片段 `'文件上传处理服务。\n\n这个文件是“上传文件 -> 文件解析 -> 原文入库 -> AI 知识提取 -> 问答/意图入库 -> 可选导出”的总调度层。\n\n注意:\n 这里不直接做具体…`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
'文件上传处理服务。\n\n这个文件是“上传文件 -> 文件解析 -> 原文入库 -> AI 知识提取 -> 问答/意图入库 -> 可选导出”的总调度层。\n\n注意:\n    这里不直接做具体解析，也不直接写具体 ORM。\n    它负责把各个服务串起来：\n        - processor.py 负责解析文件\n        - raw_data_service.py 负责保存原始文本\n        - audio_knowledge_extract_service.py 负责调用三套提示词\n        - qa_pair_service.py 负责保存问答知识\n        - intent_service.py 负责保存意图知识\n        - export_service.py 负责导出 Markdown 文件\n'
# [2026-07-03 18:11:51] 作用：导入依赖 `import json`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
import json
# [2026-07-03 18:11:51] 作用：导入依赖 `import shutil`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
import shutil
# [2026-07-03 18:11:51] 作用：导入依赖 `import uuid`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
import uuid
# [2026-07-03 18:11:51] 作用：导入依赖 `from pathlib import Path`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from pathlib import Path
# [2026-07-03 18:11:51] 作用：导入依赖 `from typing import Literal`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from typing import Literal
# [2026-07-03 18:11:51] 作用：导入依赖 `from fastapi import HTTPException, UploadFile`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from fastapi import HTTPException, UploadFile
# [2026-07-03 18:11:51] 作用：导入依赖 `from app.ai.processors.export_service import export_knowledge_extract_result`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from app.ai.processors.export_service import  export_knowledge_extract_result
# [2026-07-03 18:11:51] 作用：导入依赖 `from app.ai.processors.file_utils import get_file_type`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from app.ai.processors.file_utils import get_file_type
# [2026-07-03 18:11:51] 作用：导入依赖 `from app.ai.processors.processor import Mode, process_file`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from app.ai.processors.processor import Mode, process_file
# [2026-07-03 18:11:51] 作用：为 Action 构造并保存赋值结果；本行执行 `Action = Literal["parse", "analyze", "both"]`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
Action = Literal["parse", "analyze", "both"]
# [2026-07-03 18:11:51] 作用：为 UPLOAD_DIR 构造并保存赋值结果；本行执行 `UPLOAD_DIR = Path("temp_uploads/vlm")`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
UPLOAD_DIR = Path("temp_uploads/vlm")
# [2026-07-03 18:11:51] 作用：为 DEFAULT_OUTPUT_DIR 构造并保存赋值结果；本行执行 `DEFAULT_OUTPUT_DIR = Path("temp_uploads/vlm_outputs")`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
DEFAULT_OUTPUT_DIR = Path("temp_uploads/vlm_outputs")
# [2026-07-03 18:11:51] 作用：声明同步函数 _safe_upload_name，封装可复用的处理步骤；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _safe_upload_name
def _safe_upload_name(filename: str) -> str:
    # [2026-07-03 18:11:51] 作用：在 _safe_upload_name 中执行具体代码片段 `'生成安全的临时文件名。\n\n 参数:\n filename: 前端上传的原始文件名。\n\n 返回:\n 随机 UUID 文件名 + 原始扩展名。\n\n 说明:\n 不直接使用用户上传…`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _safe_upload_name
    '生成安全的临时文件名。\n\n    参数:\n        filename: 前端上传的原始文件名。\n\n    返回:\n        随机 UUID 文件名 + 原始扩展名。\n\n    说明:\n        不直接使用用户上传的原文件名，避免中文、特殊字符、重名、路径注入等问题。\n    '
    # [2026-07-03 18:11:51] 作用：为 source 构造并保存赋值结果；本行执行 `source = Path(filename or "upload.bin")`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _safe_upload_name
    source = Path(filename or "upload.bin")
    # [2026-07-03 18:11:51] 作用：从 _safe_upload_name 返回表达式 `return f"{uuid.uuid4().hex}{source.suffix.lower()}"` 的结果；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _safe_upload_name
    return f"{uuid.uuid4().hex}{source.suffix.lower()}"
# [2026-07-03 18:11:51] 作用：声明同步函数 _extract_raw_text，封装可复用的处理步骤；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _extract_raw_text
def _extract_raw_text(processed: dict) -> str:
    # [2026-07-03 18:11:51] 作用：在 _extract_raw_text 中执行具体代码片段 `'从 process_file 返回结果中提取可用于 AI 分析的纯文本。\n\n 参数:\n processed: processor.process_file() 返回的标准化解析结果。…`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _extract_raw_text
    '从 process_file 返回结果中提取可用于 AI 分析的纯文本。\n\n    参数:\n        processed: processor.process_file() 返回的标准化解析结果。\n\n    返回:\n        可交给 AI 处理的文本内容。\n\n    不同文件类型的解析结果结构不一样:\n        document:\n            result 通常是 dict，正文放在 markdown 字段中。\n\n        text / audio:\n            result 通常是 dict，正文放在 text 字段中。\n\n        image:\n            result 可能是 OCR 或视觉模型返回的字符串。\n    '
    # [2026-07-03 18:11:51] 作用：为 result 构造并保存赋值结果；本行执行 `result = processed.get("result")`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _extract_raw_text
    result = processed.get("result")
    # [2026-07-03 18:11:51] 作用：为 file_type 构造并保存赋值结果；本行执行 `file_type = processed.get("file_type")`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _extract_raw_text
    file_type = processed.get("file_type")
    # [2026-07-03 18:11:51] 作用：在 _extract_raw_text 中按条件 `if file_type == "document" and isinstance(result, dict):` 选择执行分支；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _extract_raw_text
    if file_type == "document" and isinstance(result, dict):
        # [2026-07-03 18:11:51] 作用：从 _extract_raw_text 返回表达式 `return result.get("markdown", "") or ""` 的结果；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _extract_raw_text
        return result.get("markdown", "") or ""
    # [2026-07-03 18:11:51] 作用：在 _extract_raw_text 中按条件 `if file_type in {"text", "audio"} and isinstance(result, dict):` 选择执行分支；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _extract_raw_text
    if file_type in {"text", "audio"} and isinstance(result, dict):
        # [2026-07-03 18:11:51] 作用：从 _extract_raw_text 返回表达式 `return result.get("text", "") or ""` 的结果；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _extract_raw_text
        return result.get("text", "") or ""
    # [2026-07-03 18:11:51] 作用：在 _extract_raw_text 中按条件 `if file_type == "image":` 选择执行分支；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _extract_raw_text
    if file_type == "image":
        # [2026-07-03 18:11:51] 作用：从 _extract_raw_text 返回表达式 `return str(result or "")` 的结果；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _extract_raw_text
        return str(result or "")
    # [2026-07-03 18:11:51] 作用：从 _extract_raw_text 返回表达式 `return ""` 的结果；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _extract_raw_text
    return ""
# [2026-07-03 18:11:51] 作用：声明同步函数 _compact_processed，封装可复用的处理步骤；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _compact_processed
def _compact_processed(processed: dict) -> dict:
    # [2026-07-03 18:11:51] 作用：在 _compact_processed 中执行具体代码片段 `'精简解析结果，只返回前端常用字段。\n\n 参数:\n processed: 完整解析结果。\n\n 返回:\n 精简后的解析结果。\n\n 说明:\n 有些解析结果里可能包含较多内部字段…`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _compact_processed
    '精简解析结果，只返回前端常用字段。\n\n    参数:\n        processed: 完整解析结果。\n\n    返回:\n        精简后的解析结果。\n\n    说明:\n        有些解析结果里可能包含较多内部字段。\n        include_parse_result=True 时，接口才会把这个精简结果返回给前端。\n    '
    # [2026-07-03 18:11:51] 作用：从 _compact_processed 返回表达式 `return {` 的结果；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _compact_processed
    return {
        # [2026-07-03 18:11:51] 作用：完善 同步函数 _compact_processed 的签名或多行表达式片段 `"success": processed.get("success"),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _compact_processed
        "success": processed.get("success"),
        # [2026-07-03 18:11:51] 作用：完善 同步函数 _compact_processed 的签名或多行表达式片段 `"file_name": processed.get("file_name"),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _compact_processed
        "file_name": processed.get("file_name"),
        # [2026-07-03 18:11:51] 作用：完善 同步函数 _compact_processed 的签名或多行表达式片段 `"file_type": processed.get("file_type"),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _compact_processed
        "file_type": processed.get("file_type"),
        # [2026-07-03 18:11:51] 作用：完善 同步函数 _compact_processed 的签名或多行表达式片段 `"engine": processed.get("engine"),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _compact_processed
        "engine": processed.get("engine"),
        # [2026-07-03 18:11:51] 作用：完善 同步函数 _compact_processed 的签名或多行表达式片段 `"mode": processed.get("mode"),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _compact_processed
        "mode": processed.get("mode"),
        # [2026-07-03 18:11:51] 作用：完善 同步函数 _compact_processed 的签名或多行表达式片段 `"parse_method": processed.get("parse_method"),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _compact_processed
        "parse_method": processed.get("parse_method"),
        # [2026-07-03 18:11:51] 作用：完善 同步函数 _compact_processed 的签名或多行表达式片段 `"result": processed.get("result"),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _compact_processed
        "result": processed.get("result"),
    # [2026-07-03 18:11:51] 作用：在 _compact_processed 中执行具体代码片段 `}`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _compact_processed
    }
# [2026-07-03 18:11:51] 作用：声明异步函数 _save_upload，提供可等待的链路处理入口；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _save_upload
async def _save_upload(file: UploadFile) -> Path:
    # [2026-07-03 18:11:51] 作用：在 _save_upload 中执行具体代码片段 `'保存上传文件到临时目录。\n\n 参数:\n file: FastAPI 接收到的上传文件对象。\n\n 返回:\n 临时文件路径。\n\n 说明:\n 后续 process_file()…`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _save_upload
    '保存上传文件到临时目录。\n\n    参数:\n        file: FastAPI 接收到的上传文件对象。\n\n    返回:\n        临时文件路径。\n\n    说明:\n        后续 process_file() 需要通过文件路径读取文件。\n        因此这里先把 UploadFile 落到本地临时目录。\n    '
    # [2026-07-03 18:11:51] 作用：完善 异步函数 _save_upload 的签名或多行表达式片段 `UPLOAD_DIR.mkdir(parents=True, exist_ok=True)`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _save_upload
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    # [2026-07-03 18:11:51] 作用：为 upload_path 构造并保存赋值结果；本行执行 `upload_path = UPLOAD_DIR / _safe_upload_name(file.filename)`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _save_upload
    upload_path = UPLOAD_DIR / _safe_upload_name(file.filename)
    # [2026-07-03 18:11:51] 作用：在 _save_upload 中用 `with upload_path.open("wb") as buffer:` 管理资源生命周期；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _save_upload
    with upload_path.open("wb") as buffer:
        # [2026-07-03 18:11:51] 作用：完善 异步函数 _save_upload 的签名或多行表达式片段 `shutil.copyfileobj(file.file, buffer)`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _save_upload
        shutil.copyfileobj(file.file, buffer)
    # [2026-07-03 18:11:51] 作用：从 _save_upload 返回表达式 `return upload_path` 的结果；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _save_upload
    return upload_path
# [2026-07-03 18:11:51] 作用：声明异步函数 _run_fixed_audio_knowledge_extract，提供可等待的链路处理入口；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
async def _run_fixed_audio_knowledge_extract(
    # [2026-07-03 18:11:51] 作用：完善 异步函数 _run_fixed_audio_knowledge_extract 的签名或多行表达式片段 `*,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    *,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 _run_fixed_audio_knowledge_extract 的签名或多行表达式片段 `raw_text: str,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    raw_text: str,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 _run_fixed_audio_knowledge_extract 的签名或多行表达式片段 `raw_data_id: str | None,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    raw_data_id: str | None,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 _run_fixed_audio_knowledge_extract 的签名或多行表达式片段 `upload_path: Path,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    upload_path: Path,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 _run_fixed_audio_knowledge_extract 的签名或多行表达式片段 `file_type: str,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    file_type: str,
# [2026-07-03 18:11:51] 作用：在 _run_fixed_audio_knowledge_extract 中执行具体代码片段 `) -> tuple[dict | None, str | None, str | None, list, list, list]:`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
) -> tuple[dict | None, str | None, str | None, list, list, list]:
    # [2026-07-03 18:11:51] 作用：在 _run_fixed_audio_knowledge_extract 中执行具体代码片段 `'固定执行三套 AI 知识提取，并完成问答和意图入库。\n\n 参数:\n raw_text:\n 文件解析出的原始文本。\n\n raw_data_id:\n 原始数据表 ID。\n 问答…`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    '固定执行三套 AI 知识提取，并完成问答和意图入库。\n\n    参数:\n        raw_text:\n            文件解析出的原始文本。\n\n        raw_data_id:\n            原始数据表 ID。\n            问答表、意图表会通过这个 ID 关联原始数据。\n\n        upload_path:\n            当前上传文件的临时路径。\n            入库时会保存为来源文件路径。\n\n        file_type:\n            文件类型，例如 document、audio、image、text。\n\n    返回:\n        analysis:\n            汇总后的 AI 分析结果。\n\n        qa_analysis:\n            问答提取结果，通常是 JSON 字符串。\n\n        intent_analysis:\n            意图提取结果，通常是 JSON 字符串。\n\n        description_items:\n            描述提示词生成的结果列表。\n\n        qa_pair_ids:\n            问答知识入库后生成的 ID 列表。\n\n        intent_ids:\n            意图知识入库后生成的 ID 列表。\n\n    说明:\n        这里固定执行:\n            1. 问答提取\n            2. 问答描述生成\n            3. 意图提取\n\n        不再根据前端选择 prompt_type 切换提示词。\n    '
    # [2026-07-03 18:11:51] 作用：导入依赖 `from extraction_chain.audio_knowledge_extract_service import extract_audio_knowledge`，供 _run_fixed_audio_knowledge_extract 使用；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    from extraction_chain.audio_knowledge_extract_service import extract_audio_knowledge
    # [2026-07-03 18:11:51] 作用：导入依赖 `from extraction_chain.intent_service import save_intents`，供 _run_fixed_audio_knowledge_extract 使用；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    from extraction_chain.intent_service import save_intents
    # [2026-07-03 18:11:51] 作用：导入依赖 `from extraction_chain.qa_pair_service import save_qa_pairs`，供 _run_fixed_audio_knowledge_extract 使用；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    from extraction_chain.qa_pair_service import save_qa_pairs
    # [2026-07-03 18:11:51] 作用：为 extract_result 构造并保存赋值结果；本行执行 `extract_result = await extract_audio_knowledge(raw_text)`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    extract_result = await extract_audio_knowledge(raw_text)
    # [2026-07-03 18:11:51] 作用：为 qa_analysis 构造并保存赋值结果；本行执行 `qa_analysis = extract_result.get("qa_analysis")`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    qa_analysis = extract_result.get("qa_analysis")
    # [2026-07-03 18:11:51] 作用：为 intent_analysis 构造并保存赋值结果；本行执行 `intent_analysis = extract_result.get("intent_analysis")`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    intent_analysis = extract_result.get("intent_analysis")
    # [2026-07-03 18:11:51] 作用：为 description_items 构造并保存赋值结果；本行执行 `description_items = extract_result.get("description_items") or []`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    description_items = extract_result.get("description_items") or []
    # [2026-07-03 18:11:51] 作用：为 analysis 构造并保存赋值结果；本行执行 `analysis = {`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    analysis = {
        # [2026-07-03 18:11:51] 作用：为 analysis 构造并保存赋值结果；本行执行 `"qa_analysis": qa_analysis,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
        "qa_analysis": qa_analysis,
        # [2026-07-03 18:11:51] 作用：为 analysis 构造并保存赋值结果；本行执行 `"intent_analysis": intent_analysis,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
        "intent_analysis": intent_analysis,
    # [2026-07-03 18:11:51] 作用：为 analysis 构造并保存赋值结果；本行执行 `}`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    }
    # [2026-07-03 18:11:51] 作用：为 qa_pair_ids 构造并保存赋值结果；本行执行 `qa_pair_ids = []`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    qa_pair_ids = []
    # [2026-07-03 18:11:51] 作用：为 intent_ids 构造并保存赋值结果；本行执行 `intent_ids = []`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    intent_ids = []
    # [2026-07-03 18:11:51] 作用：在 _run_fixed_audio_knowledge_extract 中按条件 `if qa_analysis:` 选择执行分支；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    if qa_analysis:
        # [2026-07-03 18:11:51] 作用：为 qa_pair_ids 构造并保存赋值结果；本行执行 `qa_pair_ids = save_qa_pairs(`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
        qa_pair_ids = save_qa_pairs(
            # [2026-07-03 18:11:51] 作用：为 qa_pair_ids 构造并保存赋值结果；本行执行 `analysis=qa_analysis,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
            analysis=qa_analysis,
            # [2026-07-03 18:11:51] 作用：为 qa_pair_ids 构造并保存赋值结果；本行执行 `raw_data_id=raw_data_id,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
            raw_data_id=raw_data_id,
            # [2026-07-03 18:11:51] 作用：为 qa_pair_ids 构造并保存赋值结果；本行执行 `source_file_path=str(upload_path),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
            source_file_path=str(upload_path),
            # [2026-07-03 18:11:51] 作用：为 qa_pair_ids 构造并保存赋值结果；本行执行 `file_type=file_type,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
            file_type=file_type,
            # [2026-07-03 18:11:51] 作用：为 qa_pair_ids 构造并保存赋值结果；本行执行 `gs_id=None,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
            gs_id=None,
            # [2026-07-03 18:11:51] 作用：为 qa_pair_ids 构造并保存赋值结果；本行执行 `in_userid=None,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
            in_userid=None,
        # [2026-07-03 18:11:51] 作用：为 qa_pair_ids 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
        )
    # [2026-07-03 18:11:51] 作用：在 _run_fixed_audio_knowledge_extract 中按条件 `if intent_analysis:` 选择执行分支；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    if intent_analysis:
        # [2026-07-03 18:11:51] 作用：为 intent_ids 构造并保存赋值结果；本行执行 `intent_ids = save_intents(`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
        intent_ids = save_intents(
            # [2026-07-03 18:11:51] 作用：为 intent_ids 构造并保存赋值结果；本行执行 `analysis=intent_analysis,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
            analysis=intent_analysis,
            # [2026-07-03 18:11:51] 作用：为 intent_ids 构造并保存赋值结果；本行执行 `raw_data_id=raw_data_id,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
            raw_data_id=raw_data_id,
            # [2026-07-03 18:11:51] 作用：为 intent_ids 构造并保存赋值结果；本行执行 `source_file_path=str(upload_path),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
            source_file_path=str(upload_path),
            # [2026-07-03 18:11:51] 作用：为 intent_ids 构造并保存赋值结果；本行执行 `file_type=file_type,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
            file_type=file_type,
            # [2026-07-03 18:11:51] 作用：为 intent_ids 构造并保存赋值结果；本行执行 `gs_id=None,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
            gs_id=None,
            # [2026-07-03 18:11:51] 作用：为 intent_ids 构造并保存赋值结果；本行执行 `in_userid=None,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
            in_userid=None,
        # [2026-07-03 18:11:51] 作用：为 intent_ids 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
        )
    # [2026-07-03 18:11:51] 作用：从 _run_fixed_audio_knowledge_extract 返回表达式 `return analysis, qa_analysis, intent_analysis, description_items, qa_pair_ids, intent_ids` 的结果；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 _run_fixed_audio_knowledge_extract
    return analysis, qa_analysis, intent_analysis, description_items, qa_pair_ids, intent_ids
# [2026-07-03 18:11:51] 作用：声明异步函数 process_uploaded_file，提供可等待的链路处理入口；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
async def process_uploaded_file(
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_file 的签名或多行表达式片段 `*,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
    *,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_file 的签名或多行表达式片段 `file: UploadFile,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
    file: UploadFile,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_file 的签名或多行表达式片段 `action: Action,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
    action: Action,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_file 的签名或多行表达式片段 `mode: Mode,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
    mode: Mode,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_file 的签名或多行表达式片段 `export_files: bool,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
    export_files: bool,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_file 的签名或多行表达式片段 `output_dir: str | None,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
    output_dir: str | None,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_file 的签名或多行表达式片段 `include_parse_result: bool,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
    include_parse_result: bool,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_file 的签名或多行表达式片段 `asset_type_id: str | None = None,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
    asset_type_id: str | None = None,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_file 的签名或多行表达式片段 `customer_id: int = 0,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
    customer_id: int = 0,
# [2026-07-03 18:11:51] 作用：在 process_uploaded_file 中执行具体代码片段 `) -> dict:`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
) -> dict:
    # [2026-07-03 18:11:51] 作用：在 process_uploaded_file 中执行具体代码片段 `'处理单个上传文件。\n\n 参数:\n file:\n 前端上传的文件。\n\n action:\n 处理动作。\n parse = 只解析\n analyze = 解析后 AI 分析\n…`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
    '处理单个上传文件。\n\n    参数:\n        file:\n            前端上传的文件。\n\n        action:\n            处理动作。\n            parse   = 只解析\n            analyze = 解析后 AI 分析\n            both    = 解析并 AI 分析\n\n        mode:\n            解析模式。\n            例如 auto、ocr、recognize、parse、audio 等。\n\n        export_files:\n            是否导出 raw.md 和 summary.md。\n\n        output_dir:\n            导出目录。\n            如果为空，则使用 DEFAULT_OUTPUT_DIR。\n\n        include_parse_result:\n            是否把解析结果返回给前端。\n\n        asset_type_id:\n            资产类型 ID。\n            保存原始数据时写入 AI_YuanShishuju.ZcLeiXin。\n\n        customer_id:\n            关联客户 ID。\n            保存原始数据时写入 AI_YuanShishuju.GuanLianKeHu。\n\n    返回:\n        当前文件的解析、AI 分析、入库 ID、导出文件等信息。\n    '
    # [2026-07-03 18:11:51] 作用：为 upload_path 构造并保存赋值结果；本行执行 `upload_path = await _save_upload(file)`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
    upload_path = await _save_upload(file)
    # [2026-07-03 18:11:51] 作用：为 should_analyze 构造并保存赋值结果；本行执行 `should_analyze = action in {"analyze", "both"}`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
    should_analyze = action in {"analyze", "both"}
    # [2026-07-03 18:11:51] 作用：在 process_uploaded_file 中用 `try:` 控制异常处理或资源清理；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
    try:
        # [2026-07-03 18:11:51] 作用：为 file_type 构造并保存赋值结果；本行执行 `file_type = get_file_type(str(upload_path))`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        file_type = get_file_type(str(upload_path))
        # [2026-07-03 18:11:51] 作用：在 process_uploaded_file 中按条件 `if file_type == "unsupported":` 选择执行分支；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        if file_type == "unsupported":
            # [2026-07-03 18:11:51] 作用：在 process_uploaded_file 抛出 `raise HTTPException(`，阻止无效状态继续传播；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            raise HTTPException(
                # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_file 的签名或多行表达式片段 `status_code=400,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                status_code=400,
                # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_file 的签名或多行表达式片段 `detail=f"不支持的文件类型: {file.filename}",`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                detail=f"不支持的文件类型: {file.filename}",
            # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_file 的签名或多行表达式片段 `)`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            )
        # [2026-07-03 18:11:51] 作用：为 processed 构造并保存赋值结果；本行执行 `processed = await process_file(`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        processed = await process_file(
            # [2026-07-03 18:11:51] 作用：为 processed 构造并保存赋值结果；本行执行 `file_path=str(upload_path),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            file_path=str(upload_path),
            # [2026-07-03 18:11:51] 作用：为 processed 构造并保存赋值结果；本行执行 `mode=mode,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            mode=mode,
            # [2026-07-03 18:11:51] 作用：为 processed 构造并保存赋值结果；本行执行 `export=False,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            export=False,
        # [2026-07-03 18:11:51] 作用：为 processed 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        )
        # [2026-07-03 18:11:51] 作用：在 process_uploaded_file 中按条件 `if not processed.get("success"):` 选择执行分支；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        if not processed.get("success"):
            # [2026-07-03 18:11:51] 作用：从 process_uploaded_file 返回表达式 `return {` 的结果；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            return {
                # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_file 的签名或多行表达式片段 `"success": False,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                "success": False,
                # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_file 的签名或多行表达式片段 `"file_name": file.filename,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                "file_name": file.filename,
                # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_file 的签名或多行表达式片段 `"error": processed.get("error", "文件处理失败"),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                "error": processed.get("error", "文件处理失败"),
                # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_file 的签名或多行表达式片段 `"processed": processed,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                "processed": processed,
            # [2026-07-03 18:11:51] 作用：在 process_uploaded_file 中执行具体代码片段 `}`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            }
        # [2026-07-03 18:11:51] 作用：为 raw_text 构造并保存赋值结果；本行执行 `raw_text = _extract_raw_text(processed)`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        raw_text = _extract_raw_text(processed)
        # [2026-07-03 18:11:51] 作用：为 raw_data_id 构造并保存赋值结果；本行执行 `raw_data_id = None`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        raw_data_id = None
        # [2026-07-03 18:11:51] 作用：在 process_uploaded_file 中按条件 `if raw_text:` 选择执行分支；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        if raw_text:
            # [2026-07-03 18:11:51] 作用：导入依赖 `from extraction_chain.raw_data_service import save_raw_text`，供 process_uploaded_file 使用；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            from extraction_chain.raw_data_service import save_raw_text
            # [2026-07-03 18:11:51] 作用：为 raw_data_id 构造并保存赋值结果；本行执行 `raw_data_id = save_raw_text(`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            raw_data_id = save_raw_text(
                # [2026-07-03 18:11:51] 作用：为 raw_data_id 构造并保存赋值结果；本行执行 `raw_text=raw_text,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                raw_text=raw_text,
                # [2026-07-03 18:11:51] 作用：为 raw_data_id 构造并保存赋值结果；本行执行 `source_file_path=str(upload_path),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                source_file_path=str(upload_path),
                # [2026-07-03 18:11:51] 作用：为 raw_data_id 构造并保存赋值结果；本行执行 `file_type=processed.get("file_type", ""),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                file_type=processed.get("file_type", ""),
                # [2026-07-03 18:11:51] 作用：为 raw_data_id 构造并保存赋值结果；本行执行 `source_file_name=file.filename,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                source_file_name=file.filename,
                # [2026-07-03 18:11:51] 作用：为 raw_data_id 构造并保存赋值结果；本行执行 `asset_type_id=asset_type_id,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                asset_type_id=asset_type_id,
                # [2026-07-03 18:11:51] 作用：为 raw_data_id 构造并保存赋值结果；本行执行 `guan_lian_ke_hu=customer_id,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                guan_lian_ke_hu=customer_id,
                # [2026-07-03 18:11:51] 作用：为 raw_data_id 构造并保存赋值结果；本行执行 `enterprise_id=None,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                enterprise_id=None,
                # [2026-07-03 18:11:51] 作用：为 raw_data_id 构造并保存赋值结果；本行执行 `in_userid=None,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                in_userid=None,
            # [2026-07-03 18:11:51] 作用：为 raw_data_id 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            )
        # [2026-07-03 18:11:51] 作用：为 analysis 构造并保存赋值结果；本行执行 `analysis = None`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        analysis = None
        # [2026-07-03 18:11:51] 作用：为 qa_analysis 构造并保存赋值结果；本行执行 `qa_analysis = None`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        qa_analysis = None
        # [2026-07-03 18:11:51] 作用：为 intent_analysis 构造并保存赋值结果；本行执行 `intent_analysis = None`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        intent_analysis = None
        # [2026-07-03 18:11:51] 作用：为 description_items 构造并保存赋值结果；本行执行 `description_items = []`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        description_items = []
        # [2026-07-03 18:11:51] 作用：为 qa_pair_ids 构造并保存赋值结果；本行执行 `qa_pair_ids = []`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        qa_pair_ids = []
        # [2026-07-03 18:11:51] 作用：为 intent_ids 构造并保存赋值结果；本行执行 `intent_ids = []`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        intent_ids = []
        # [2026-07-03 18:11:51] 作用：在 process_uploaded_file 中按条件 `if should_analyze and raw_text.strip():` 选择执行分支；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        if should_analyze and raw_text.strip():
            # [2026-07-03 18:11:51] 作用：为 (analysis, qa_analysis, intent_analysis, description_items, qa_pair_ids, intent_ids) 构造并保存赋值结果；本行执行 `(`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            (
                # [2026-07-03 18:11:51] 作用：为 (analysis, qa_analysis, intent_analysis, description_items, qa_pair_ids, intent_ids) 构造并保存赋值结果；本行执行 `analysis,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                analysis,
                # [2026-07-03 18:11:51] 作用：为 (analysis, qa_analysis, intent_analysis, description_items, qa_pair_ids, intent_ids) 构造并保存赋值结果；本行执行 `qa_analysis,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                qa_analysis,
                # [2026-07-03 18:11:51] 作用：为 (analysis, qa_analysis, intent_analysis, description_items, qa_pair_ids, intent_ids) 构造并保存赋值结果；本行执行 `intent_analysis,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                intent_analysis,
                # [2026-07-03 18:11:51] 作用：为 (analysis, qa_analysis, intent_analysis, description_items, qa_pair_ids, intent_ids) 构造并保存赋值结果；本行执行 `description_items,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                description_items,
                # [2026-07-03 18:11:51] 作用：为 (analysis, qa_analysis, intent_analysis, description_items, qa_pair_ids, intent_ids) 构造并保存赋值结果；本行执行 `qa_pair_ids,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                qa_pair_ids,
                # [2026-07-03 18:11:51] 作用：为 (analysis, qa_analysis, intent_analysis, description_items, qa_pair_ids, intent_ids) 构造并保存赋值结果；本行执行 `intent_ids,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                intent_ids,
            # [2026-07-03 18:11:51] 作用：为 (analysis, qa_analysis, intent_analysis, description_items, qa_pair_ids, intent_ids) 构造并保存赋值结果；本行执行 `) = await _run_fixed_audio_knowledge_extract(`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            ) = await _run_fixed_audio_knowledge_extract(
                # [2026-07-03 18:11:51] 作用：为 (analysis, qa_analysis, intent_analysis, description_items, qa_pair_ids, intent_ids) 构造并保存赋值结果；本行执行 `raw_text=raw_text,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                raw_text=raw_text,
                # [2026-07-03 18:11:51] 作用：为 (analysis, qa_analysis, intent_analysis, description_items, qa_pair_ids, intent_ids) 构造并保存赋值结果；本行执行 `raw_data_id=raw_data_id,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                raw_data_id=raw_data_id,
                # [2026-07-03 18:11:51] 作用：为 (analysis, qa_analysis, intent_analysis, description_items, qa_pair_ids, intent_ids) 构造并保存赋值结果；本行执行 `upload_path=upload_path,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                upload_path=upload_path,
                # [2026-07-03 18:11:51] 作用：为 (analysis, qa_analysis, intent_analysis, description_items, qa_pair_ids, intent_ids) 构造并保存赋值结果；本行执行 `file_type=processed.get("file_type", ""),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                file_type=processed.get("file_type", ""),
            # [2026-07-03 18:11:51] 作用：为 (analysis, qa_analysis, intent_analysis, description_items, qa_pair_ids, intent_ids) 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            )
        # [2026-07-03 18:11:51] 作用：为 exports 构造并保存赋值结果；本行执行 `exports = None`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        exports = None
        # [2026-07-03 18:11:51] 作用：在 process_uploaded_file 中按条件 `if export_files:` 选择执行分支；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        if export_files:
            # [2026-07-03 18:11:51] 作用：为 exports 构造并保存赋值结果；本行执行 `exports = await export_knowledge_extract_result(`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            exports = await export_knowledge_extract_result(
                # [2026-07-03 18:11:51] 作用：为 exports 构造并保存赋值结果；本行执行 `processed=processed,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                processed=processed,
                # [2026-07-03 18:11:51] 作用：为 exports 构造并保存赋值结果；本行执行 `raw_text=raw_text,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                raw_text=raw_text,
                # [2026-07-03 18:11:51] 作用：为 exports 构造并保存赋值结果；本行执行 `output_dir=output_dir or str(DEFAULT_OUTPUT_DIR),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                output_dir=output_dir or str(DEFAULT_OUTPUT_DIR),
                # [2026-07-03 18:11:51] 作用：为 exports 构造并保存赋值结果；本行执行 `qa_analysis=qa_analysis,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                qa_analysis=qa_analysis,
                # [2026-07-03 18:11:51] 作用：为 exports 构造并保存赋值结果；本行执行 `intent_analysis=intent_analysis,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
                intent_analysis=intent_analysis,
            # [2026-07-03 18:11:51] 作用：为 exports 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            )
        # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `item = {`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        item = {
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `"success": True,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            "success": True,
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `"source_file_name": file.filename,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            "source_file_name": file.filename,
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `"file_name": processed.get("file_name"),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            "file_name": processed.get("file_name"),
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `"file_type": processed.get("file_type"),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            "file_type": processed.get("file_type"),
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `"engine": processed.get("engine"),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            "engine": processed.get("engine"),
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `"mode": processed.get("mode"),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            "mode": processed.get("mode"),
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `"action": action,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            "action": action,
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `"raw_text": raw_text,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            "raw_text": raw_text,
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `"raw_data_id": raw_data_id,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            "raw_data_id": raw_data_id,
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `"analysis": analysis,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            "analysis": analysis,
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `"qa_analysis": qa_analysis,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            "qa_analysis": qa_analysis,
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `"intent_analysis": intent_analysis,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            "intent_analysis": intent_analysis,
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `"description_items": description_items,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            "description_items": description_items,
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `"qa_pair_ids": qa_pair_ids,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            "qa_pair_ids": qa_pair_ids,
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `"intent_ids": intent_ids,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            "intent_ids": intent_ids,
            # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `"exports": exports,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            "exports": exports,
        # [2026-07-03 18:11:51] 作用：为 item 构造并保存赋值结果；本行执行 `}`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        }
        # [2026-07-03 18:11:51] 作用：在 process_uploaded_file 中按条件 `if include_parse_result:` 选择执行分支；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        if include_parse_result:
            # [2026-07-03 18:11:51] 作用：为 item['processed'] 构造并保存赋值结果；本行执行 `item["processed"] = _compact_processed(processed)`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            item["processed"] = _compact_processed(processed)
        # [2026-07-03 18:11:51] 作用：从 process_uploaded_file 返回表达式 `return item` 的结果；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        return item
    # [2026-07-03 18:11:51] 作用：在 process_uploaded_file 中用 `finally:` 控制异常处理或资源清理；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
    finally:
        # [2026-07-03 18:11:51] 作用：在 process_uploaded_file 中按条件 `if upload_path.exists():` 选择执行分支；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
        if upload_path.exists():
            # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_file 的签名或多行表达式片段 `upload_path.unlink()`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_file
            upload_path.unlink()
# [2026-07-03 18:11:51] 作用：声明异步函数 process_uploaded_files，提供可等待的链路处理入口；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
async def process_uploaded_files(
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `*,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
    *,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `files: list[UploadFile],`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
    files: list[UploadFile],
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `action: Action,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
    action: Action,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `mode: Mode,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
    mode: Mode,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `export_files: bool,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
    export_files: bool,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `output_dir: str | None,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
    output_dir: str | None,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `custom_prompt: str | None,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
    custom_prompt: str | None,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `include_parse_result: bool,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
    include_parse_result: bool,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `asset_type_id: str | None = None,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
    asset_type_id: str | None = None,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `customer_id: int = 0,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
    customer_id: int = 0,
# [2026-07-03 18:11:51] 作用：在 process_uploaded_files 中执行具体代码片段 `) -> dict:`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
) -> dict:
    # [2026-07-03 18:11:51] 作用：在 process_uploaded_files 中执行具体代码片段 `'批量处理上传文件。\n\n 参数:\n files:\n 前端上传的文件列表。\n\n action:\n 当前批次的处理动作。\n\n mode:\n 文件解析模式。\n\n expor…`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
    '批量处理上传文件。\n\n    参数:\n        files:\n            前端上传的文件列表。\n\n        action:\n            当前批次的处理动作。\n\n        mode:\n            文件解析模式。\n\n        export_files:\n            是否导出 Markdown 文件。\n\n        output_dir:\n            导出目录。\n\n        custom_prompt:\n            旧参数，目前固定三套提示词后已经不再使用。\n            保留这个参数只是为了兼容旧接口调用。\n\n        include_parse_result:\n            是否返回解析结果。\n\n        asset_type_id:\n            资产类型 ID。\n\n        customer_id:\n            关联客户 ID。\n\n    返回:\n        批量处理结果。\n    '
    # [2026-07-03 18:11:51] 作用：在 process_uploaded_files 中按条件 `if not files:` 选择执行分支；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
    if not files:
        # [2026-07-03 18:11:51] 作用：在 process_uploaded_files 抛出 `raise HTTPException(status_code=400, detail="请至少上传一个文件")`，阻止无效状态继续传播；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
        raise HTTPException(status_code=400, detail="请至少上传一个文件")
    # [2026-07-03 18:11:51] 作用：为 results 构造并保存赋值结果；本行执行 `results = []`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
    results = []
    # [2026-07-03 18:11:51] 作用：在 process_uploaded_files 中通过 `for file in files:` 迭代处理数据；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
    for file in files:
        # [2026-07-03 18:11:51] 作用：在 process_uploaded_files 中执行具体代码片段 `results.append(`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
        results.append(
            # [2026-07-03 18:11:51] 作用：在 process_uploaded_files 等待异步代码 `await process_uploaded_file(` 完成；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
            await process_uploaded_file(
                # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `file=file,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
                file=file,
                # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `action=action,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
                action=action,
                # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `mode=mode,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
                mode=mode,
                # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `export_files=export_files,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
                export_files=export_files,
                # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `output_dir=output_dir,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
                output_dir=output_dir,
                # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `include_parse_result=include_parse_result,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
                include_parse_result=include_parse_result,
                # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `asset_type_id=asset_type_id,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
                asset_type_id=asset_type_id,
                # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `customer_id=customer_id,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
                customer_id=customer_id,
            # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `)`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
            )
        # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `)`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
        )
    # [2026-07-03 18:11:51] 作用：从 process_uploaded_files 返回表达式 `return {` 的结果；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
    return {
        # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `"success": True,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
        "success": True,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `"action": action,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
        "action": action,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `"mode": mode,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
        "mode": mode,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `"total": len(files),`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
        "total": len(files),
        # [2026-07-03 18:11:51] 作用：完善 异步函数 process_uploaded_files 的签名或多行表达式片段 `"results": results,`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
        "results": results,
    # [2026-07-03 18:11:51] 作用：在 process_uploaded_files 中执行具体代码片段 `}`；理由依据：源模块 extraction_chain.process_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_uploaded_files
    }
