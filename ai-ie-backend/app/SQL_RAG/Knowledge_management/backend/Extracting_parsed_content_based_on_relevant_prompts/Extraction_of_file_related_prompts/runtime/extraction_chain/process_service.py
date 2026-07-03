# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
'文件上传处理服务。\n\n这个文件是“上传文件 -> 文件解析 -> 原文入库 -> AI 知识提取 -> 问答/意图入库 -> 可选导出”的总调度层。\n\n注意:\n    这里不直接做具体解析，也不直接写具体 ORM。\n    它负责把各个服务串起来：\n        - processor.py 负责解析文件\n        - raw_data_service.py 负责保存原始文本\n        - audio_knowledge_extract_service.py 负责调用三套提示词\n        - qa_pair_service.py 负责保存问答知识\n        - intent_service.py 负责保存意图知识\n        - export_service.py 负责导出 Markdown 文件\n'
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
import json
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
import shutil
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
import uuid
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
from pathlib import Path
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
from typing import Literal
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
from fastapi import HTTPException, UploadFile
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
from app.ai.processors.export_service import  export_knowledge_extract_result
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
from app.ai.processors.file_utils import get_file_type
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
from app.ai.processors.processor import Mode, process_file
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# action 表示本次上传后要执行什么动作:
# [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# parse   = 只解析文件，不调用 AI
# [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# analyze = 解析后调用 AI 分析
# [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# both    = 解析并调用 AI 分析；当前逻辑里 analyze 和 both 效果基本一致
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
Action = Literal["parse", "analyze", "both"]
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# 上传文件临时保存目录。
# [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# 文件处理结束后，会在 finally 中删除临时文件。
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
UPLOAD_DIR = Path("temp_uploads/vlm")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# 导出 Markdown 文件的默认目录。
# [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# 只有 export_files=True 时才会使用。
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
DEFAULT_OUTPUT_DIR = Path("temp_uploads/vlm_outputs")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _safe_upload_name
def _safe_upload_name(filename: str) -> str:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _safe_upload_name
    '生成安全的临时文件名。\n\n    参数:\n        filename: 前端上传的原始文件名。\n\n    返回:\n        随机 UUID 文件名 + 原始扩展名。\n\n    说明:\n        不直接使用用户上传的原文件名，避免中文、特殊字符、重名、路径注入等问题。\n    '
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _safe_upload_name
    source = Path(filename or "upload.bin")
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _safe_upload_name
    return f"{uuid.uuid4().hex}{source.suffix.lower()}"
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_raw_text
def _extract_raw_text(processed: dict) -> str:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_raw_text
    '从 process_file 返回结果中提取可用于 AI 分析的纯文本。\n\n    参数:\n        processed: processor.process_file() 返回的标准化解析结果。\n\n    返回:\n        可交给 AI 处理的文本内容。\n\n    不同文件类型的解析结果结构不一样:\n        document:\n            result 通常是 dict，正文放在 markdown 字段中。\n\n        text / audio:\n            result 通常是 dict，正文放在 text 字段中。\n\n        image:\n            result 可能是 OCR 或视觉模型返回的字符串。\n    '
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_raw_text
    result = processed.get("result")
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_raw_text
    file_type = processed.get("file_type")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_raw_text
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_raw_text
    # 文档类文件，例如 PDF、Word、Excel 等，优先取 markdown
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_raw_text
    if file_type == "document" and isinstance(result, dict):
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_raw_text
        return result.get("markdown", "") or ""
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_raw_text
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_raw_text
    # 文本和音频文件，通常会返回 text
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_raw_text
    if file_type in {"text", "audio"} and isinstance(result, dict):
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_raw_text
        return result.get("text", "") or ""
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_raw_text
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_raw_text
    # 图片识别结果可能直接是字符串
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_raw_text
    if file_type == "image":
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_raw_text
        return str(result or "")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_raw_text
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_raw_text
    # 其他情况视为没有提取到有效文本
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_raw_text
    return ""
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _compact_processed
def _compact_processed(processed: dict) -> dict:
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _compact_processed
    '精简解析结果，只返回前端常用字段。\n\n    参数:\n        processed: 完整解析结果。\n\n    返回:\n        精简后的解析结果。\n\n    说明:\n        有些解析结果里可能包含较多内部字段。\n        include_parse_result=True 时，接口才会把这个精简结果返回给前端。\n    '
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _compact_processed
    return {
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _compact_processed
        "success": processed.get("success"),
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _compact_processed
        "file_name": processed.get("file_name"),
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _compact_processed
        "file_type": processed.get("file_type"),
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _compact_processed
        "engine": processed.get("engine"),
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _compact_processed
        "mode": processed.get("mode"),
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _compact_processed
        "parse_method": processed.get("parse_method"),
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _compact_processed
        "result": processed.get("result"),
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _compact_processed
    }
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _save_upload
async def _save_upload(file: UploadFile) -> Path:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _save_upload
    '保存上传文件到临时目录。\n\n    参数:\n        file: FastAPI 接收到的上传文件对象。\n\n    返回:\n        临时文件路径。\n\n    说明:\n        后续 process_file() 需要通过文件路径读取文件。\n        因此这里先把 UploadFile 落到本地临时目录。\n    '
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _save_upload
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _save_upload
    upload_path = UPLOAD_DIR / _safe_upload_name(file.filename)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _save_upload
    # [2026-07-03 16:33:01] 作用：限定文件、会话或异步资源生命周期；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _save_upload
    with upload_path.open("wb") as buffer:
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _save_upload
        shutil.copyfileobj(file.file, buffer)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _save_upload
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _save_upload
    return upload_path
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
async def _run_fixed_audio_knowledge_extract(
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    *,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    raw_text: str,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    raw_data_id: str | None,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    upload_path: Path,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    file_type: str,
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
) -> tuple[dict | None, str | None, str | None, list, list, list]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    '固定执行三套 AI 知识提取，并完成问答和意图入库。\n\n    参数:\n        raw_text:\n            文件解析出的原始文本。\n\n        raw_data_id:\n            原始数据表 ID。\n            问答表、意图表会通过这个 ID 关联原始数据。\n\n        upload_path:\n            当前上传文件的临时路径。\n            入库时会保存为来源文件路径。\n\n        file_type:\n            文件类型，例如 document、audio、image、text。\n\n    返回:\n        analysis:\n            汇总后的 AI 分析结果。\n\n        qa_analysis:\n            问答提取结果，通常是 JSON 字符串。\n\n        intent_analysis:\n            意图提取结果，通常是 JSON 字符串。\n\n        description_items:\n            描述提示词生成的结果列表。\n\n        qa_pair_ids:\n            问答知识入库后生成的 ID 列表。\n\n        intent_ids:\n            意图知识入库后生成的 ID 列表。\n\n    说明:\n        这里固定执行:\n            1. 问答提取\n            2. 问答描述生成\n            3. 意图提取\n\n        不再根据前端选择 prompt_type 切换提示词。\n    '
    # [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    from extraction_chain.audio_knowledge_extract_service import extract_audio_knowledge
    # [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    from extraction_chain.intent_service import save_intents
    # [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    from extraction_chain.qa_pair_service import save_qa_pairs
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    # 调用三套提示词，得到结构化提取结果
    # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    extract_result = await extract_audio_knowledge(raw_text)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    # 问答结果，后续保存到问答知识表
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    qa_analysis = extract_result.get("qa_analysis")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    # 意图结果，后续保存到意图表
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    intent_analysis = extract_result.get("intent_analysis")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    # 描述结果，主要用于前端展示和问答结果补充
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    description_items = extract_result.get("description_items") or []
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    # 汇总返回给前端，也可用于导出 summary 文件
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    analysis = {
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
        "qa_analysis": qa_analysis,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
        "intent_analysis": intent_analysis,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    }
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    qa_pair_ids = []
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    intent_ids = []
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    # 保存问答知识
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    if qa_analysis:
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
        qa_pair_ids = save_qa_pairs(
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
            analysis=qa_analysis,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
            raw_data_id=raw_data_id,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
            source_file_path=str(upload_path),
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
            file_type=file_type,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
            gs_id=None,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
            in_userid=None,
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
        )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    # 保存意图知识
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    if intent_analysis:
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
        intent_ids = save_intents(
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
            analysis=intent_analysis,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
            raw_data_id=raw_data_id,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
            source_file_path=str(upload_path),
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
            file_type=file_type,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
            gs_id=None,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
            in_userid=None,
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
        )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 _run_fixed_audio_knowledge_extract
    return analysis, qa_analysis, intent_analysis, description_items, qa_pair_ids, intent_ids
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
async def process_uploaded_file(
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
    *,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
    file: UploadFile,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
    action: Action,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
    mode: Mode,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
    export_files: bool,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
    output_dir: str | None,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
    include_parse_result: bool,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
    asset_type_id: str | None = None,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
    customer_id: int = 0,
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
) -> dict:
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
    '处理单个上传文件。\n\n    参数:\n        file:\n            前端上传的文件。\n\n        action:\n            处理动作。\n            parse   = 只解析\n            analyze = 解析后 AI 分析\n            both    = 解析并 AI 分析\n\n        mode:\n            解析模式。\n            例如 auto、ocr、recognize、parse、audio 等。\n\n        export_files:\n            是否导出 raw.md 和 summary.md。\n\n        output_dir:\n            导出目录。\n            如果为空，则使用 DEFAULT_OUTPUT_DIR。\n\n        include_parse_result:\n            是否把解析结果返回给前端。\n\n        asset_type_id:\n            资产类型 ID。\n            保存原始数据时写入 AI_YuanShishuju.ZcLeiXin。\n\n        customer_id:\n            关联客户 ID。\n            保存原始数据时写入 AI_YuanShishuju.GuanLianKeHu。\n\n    返回:\n        当前文件的解析、AI 分析、入库 ID、导出文件等信息。\n    '
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
    # 先把上传文件保存到本地临时目录
    # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
    upload_path = await _save_upload(file)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
    # 只有 analyze / both 才执行 AI 分析
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
    should_analyze = action in {"analyze", "both"}
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
    # [2026-07-03 16:33:01] 作用：控制异常处理和资源清理；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
    try:
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # 判断文件类型，不支持的文件直接返回 400
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        file_type = get_file_type(str(upload_path))
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        if file_type == "unsupported":
            # [2026-07-03 16:33:01] 作用：阻止无效状态继续传播；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            raise HTTPException(
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                status_code=400,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                detail=f"不支持的文件类型: {file.filename}",
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # 调用统一文件解析入口。
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # 注意这里 export=False，因为导出由当前 service 的 export_files 控制。
        # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        processed = await process_file(
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            file_path=str(upload_path),
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            mode=mode,
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            export=False,
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # 如果解析失败，直接返回失败信息，不继续入库和 AI 分析
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        if not processed.get("success"):
            # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            return {
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                "success": False,
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                "file_name": file.filename,
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                "error": processed.get("error", "文件处理失败"),
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                "processed": processed,
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            }
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # 从解析结果中提取可用于 AI 分析和原始数据保存的文本
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        raw_text = _extract_raw_text(processed)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # 保存原始数据后的 ID。
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # 后续问答和意图会通过 raw_data_id 关联到原始数据。
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        raw_data_id = None
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # 只有解析出文本才保存原始数据
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        if raw_text:
            # [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            from extraction_chain.raw_data_service import save_raw_text
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            raw_data_id = save_raw_text(
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                raw_text=raw_text,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                source_file_path=str(upload_path),
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                file_type=processed.get("file_type", ""),
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                source_file_name=file.filename,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                asset_type_id=asset_type_id,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                guan_lian_ke_hu=customer_id,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                enterprise_id=None,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                in_userid=None,
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # 初始化 AI 分析结果和入库结果
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        analysis = None
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        qa_analysis = None
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        intent_analysis = None
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        description_items = []
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        qa_pair_ids = []
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        intent_ids = []
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # 需要 AI 分析，并且原文不为空时，执行三套提示词和入库
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        if should_analyze and raw_text.strip():
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            (
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                analysis,
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                qa_analysis,
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                intent_analysis,
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                description_items,
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                qa_pair_ids,
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                intent_ids,
            # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            ) = await _run_fixed_audio_knowledge_extract(
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                raw_text=raw_text,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                raw_data_id=raw_data_id,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                upload_path=upload_path,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                file_type=processed.get("file_type", ""),
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # 可选导出 Markdown 文件
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        exports = None
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        if export_files:
            # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            exports = await export_knowledge_extract_result(
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                processed=processed,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                raw_text=raw_text,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                output_dir=output_dir or str(DEFAULT_OUTPUT_DIR),
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                qa_analysis=qa_analysis,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
                intent_analysis=intent_analysis,
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # 组装单文件处理结果
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        item = {
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            "success": True,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            "source_file_name": file.filename,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            "file_name": processed.get("file_name"),
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            "file_type": processed.get("file_type"),
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            "engine": processed.get("engine"),
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            "mode": processed.get("mode"),
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            "action": action,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            "raw_text": raw_text,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            "raw_data_id": raw_data_id,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            "analysis": analysis,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            "qa_analysis": qa_analysis,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            "intent_analysis": intent_analysis,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            "description_items": description_items,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            "qa_pair_ids": qa_pair_ids,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            "intent_ids": intent_ids,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            "exports": exports,
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        }
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # 如果前端需要解析详情，则附带精简后的 processed
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        if include_parse_result:
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            item["processed"] = _compact_processed(processed)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        return item
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
    # [2026-07-03 16:33:01] 作用：控制异常处理和资源清理；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
    finally:
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        # 无论成功还是失败，都删除临时上传文件，避免临时目录越来越大
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
        if upload_path.exists():
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_file
            upload_path.unlink()
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.process_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
async def process_uploaded_files(
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    *,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    files: list[UploadFile],
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    action: Action,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    mode: Mode,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    export_files: bool,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    output_dir: str | None,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    custom_prompt: str | None,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    include_parse_result: bool,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    asset_type_id: str | None = None,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    customer_id: int = 0,
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
) -> dict:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    '批量处理上传文件。\n\n    参数:\n        files:\n            前端上传的文件列表。\n\n        action:\n            当前批次的处理动作。\n\n        mode:\n            文件解析模式。\n\n        export_files:\n            是否导出 Markdown 文件。\n\n        output_dir:\n            导出目录。\n\n        custom_prompt:\n            旧参数，目前固定三套提示词后已经不再使用。\n            保留这个参数只是为了兼容旧接口调用。\n\n        include_parse_result:\n            是否返回解析结果。\n\n        asset_type_id:\n            资产类型 ID。\n\n        customer_id:\n            关联客户 ID。\n\n    返回:\n        批量处理结果。\n    '
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    if not files:
        # [2026-07-03 16:33:01] 作用：阻止无效状态继续传播；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
        raise HTTPException(status_code=400, detail="请至少上传一个文件")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    results = []
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    # 逐个处理上传文件。
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    # 这里是串行处理，如果后续文件很多，可以再考虑并发处理。
    # [2026-07-03 16:33:01] 作用：逐项处理集合或重复任务；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    for file in files:
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
        results.append(
            # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
            await process_uploaded_file(
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
                file=file,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
                action=action,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
                mode=mode,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
                export_files=export_files,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
                output_dir=output_dir,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
                include_parse_result=include_parse_result,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
                asset_type_id=asset_type_id,
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
                customer_id=customer_id,
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
            )
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
        )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    return {
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
        "success": True,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
        "action": action,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
        "mode": mode,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
        "total": len(files),
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
        "results": results,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_uploaded_files
    }
