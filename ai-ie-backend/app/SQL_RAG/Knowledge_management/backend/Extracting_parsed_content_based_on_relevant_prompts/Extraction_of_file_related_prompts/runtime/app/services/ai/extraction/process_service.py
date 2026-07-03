# [2026-07-03 14:26:28] 中文迁移说明：本文件完整复制自 app/services/ai/extraction/process_service.py；纳入依据为 DeepSeek 提取入库链 的项目内传递依赖闭包。
"""文件上传处理服务。

这个文件是“上传文件 -> 文件解析 -> 原文入库 -> AI 知识提取 -> 问答/意图入库 -> 可选导出”的总调度层。

注意:
    这里不直接做具体解析，也不直接写具体 ORM。
    它负责把各个服务串起来：
        - processor.py 负责解析文件
        - raw_data_service.py 负责保存原始文本
        - audio_knowledge_extract_service.py 负责调用三套提示词
        - qa_pair_service.py 负责保存问答知识
        - intent_service.py 负责保存意图知识
        - export_service.py 负责导出 Markdown 文件
"""

import json
import shutil
import uuid
from pathlib import Path
from typing import Literal

from fastapi import HTTPException, UploadFile

from app.ai.processors.export_service import  export_knowledge_extract_result
from app.ai.processors.file_utils import get_file_type
from app.ai.processors.processor import Mode, process_file


# action 表示本次上传后要执行什么动作:
# parse   = 只解析文件，不调用 AI
# analyze = 解析后调用 AI 分析
# both    = 解析并调用 AI 分析；当前逻辑里 analyze 和 both 效果基本一致
Action = Literal["parse", "analyze", "both"]


# 上传文件临时保存目录。
# 文件处理结束后，会在 finally 中删除临时文件。
UPLOAD_DIR = Path("temp_uploads/vlm")


# 导出 Markdown 文件的默认目录。
# 只有 export_files=True 时才会使用。
DEFAULT_OUTPUT_DIR = Path("temp_uploads/vlm_outputs")


def _safe_upload_name(filename: str) -> str:
    """生成安全的临时文件名。

    参数:
        filename: 前端上传的原始文件名。

    返回:
        随机 UUID 文件名 + 原始扩展名。

    说明:
        不直接使用用户上传的原文件名，避免中文、特殊字符、重名、路径注入等问题。
    """
    source = Path(filename or "upload.bin")
    return f"{uuid.uuid4().hex}{source.suffix.lower()}"


def _extract_raw_text(processed: dict) -> str:
    """从 process_file 返回结果中提取可用于 AI 分析的纯文本。

    参数:
        processed: processor.process_file() 返回的标准化解析结果。

    返回:
        可交给 AI 处理的文本内容。

    不同文件类型的解析结果结构不一样:
        document:
            result 通常是 dict，正文放在 markdown 字段中。

        text / audio:
            result 通常是 dict，正文放在 text 字段中。

        image:
            result 可能是 OCR 或视觉模型返回的字符串。
    """
    result = processed.get("result")
    file_type = processed.get("file_type")

    # 文档类文件，例如 PDF、Word、Excel 等，优先取 markdown
    if file_type == "document" and isinstance(result, dict):
        return result.get("markdown", "") or ""

    # 文本和音频文件，通常会返回 text
    if file_type in {"text", "audio"} and isinstance(result, dict):
        return result.get("text", "") or ""

    # 图片识别结果可能直接是字符串
    if file_type == "image":
        return str(result or "")

    # 其他情况视为没有提取到有效文本
    return ""


def _compact_processed(processed: dict) -> dict:
    """精简解析结果，只返回前端常用字段。

    参数:
        processed: 完整解析结果。

    返回:
        精简后的解析结果。

    说明:
        有些解析结果里可能包含较多内部字段。
        include_parse_result=True 时，接口才会把这个精简结果返回给前端。
    """
    return {
        "success": processed.get("success"),
        "file_name": processed.get("file_name"),
        "file_type": processed.get("file_type"),
        "engine": processed.get("engine"),
        "mode": processed.get("mode"),
        "parse_method": processed.get("parse_method"),
        "result": processed.get("result"),
    }


async def _save_upload(file: UploadFile) -> Path:
    """保存上传文件到临时目录。

    参数:
        file: FastAPI 接收到的上传文件对象。

    返回:
        临时文件路径。

    说明:
        后续 process_file() 需要通过文件路径读取文件。
        因此这里先把 UploadFile 落到本地临时目录。
    """
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    upload_path = UPLOAD_DIR / _safe_upload_name(file.filename)

    with upload_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return upload_path


async def _run_fixed_audio_knowledge_extract(
    *,
    raw_text: str,
    raw_data_id: str | None,
    upload_path: Path,
    file_type: str,
) -> tuple[dict | None, str | None, str | None, list, list, list]:
    """固定执行三套 AI 知识提取，并完成问答和意图入库。

    参数:
        raw_text:
            文件解析出的原始文本。

        raw_data_id:
            原始数据表 ID。
            问答表、意图表会通过这个 ID 关联原始数据。

        upload_path:
            当前上传文件的临时路径。
            入库时会保存为来源文件路径。

        file_type:
            文件类型，例如 document、audio、image、text。

    返回:
        analysis:
            汇总后的 AI 分析结果。

        qa_analysis:
            问答提取结果，通常是 JSON 字符串。

        intent_analysis:
            意图提取结果，通常是 JSON 字符串。

        description_items:
            描述提示词生成的结果列表。

        qa_pair_ids:
            问答知识入库后生成的 ID 列表。

        intent_ids:
            意图知识入库后生成的 ID 列表。

    说明:
        这里固定执行:
            1. 问答提取
            2. 问答描述生成
            3. 意图提取

        不再根据前端选择 prompt_type 切换提示词。
    """
    from app.services.ai.extraction.audio_knowledge_extract_service import extract_audio_knowledge
    from app.services.ai.knowledge.intent_service import save_intents
    from app.services.ai.knowledge.qa_pair_service import save_qa_pairs

    # 调用三套提示词，得到结构化提取结果
    extract_result = await extract_audio_knowledge(raw_text)

    # 问答结果，后续保存到问答知识表
    qa_analysis = extract_result.get("qa_analysis")

    # 意图结果，后续保存到意图表
    intent_analysis = extract_result.get("intent_analysis")

    # 描述结果，主要用于前端展示和问答结果补充
    description_items = extract_result.get("description_items") or []

    # 汇总返回给前端，也可用于导出 summary 文件
    analysis = {
        "qa_analysis": qa_analysis,
        "intent_analysis": intent_analysis,
    }

    qa_pair_ids = []
    intent_ids = []

    # 保存问答知识
    if qa_analysis:
        qa_pair_ids = save_qa_pairs(
            analysis=qa_analysis,
            raw_data_id=raw_data_id,
            source_file_path=str(upload_path),
            file_type=file_type,
            gs_id=None,
            in_userid=None,
        )

    # 保存意图知识
    if intent_analysis:
        intent_ids = save_intents(
            analysis=intent_analysis,
            raw_data_id=raw_data_id,
            source_file_path=str(upload_path),
            file_type=file_type,
            gs_id=None,
            in_userid=None,
        )

    return analysis, qa_analysis, intent_analysis, description_items, qa_pair_ids, intent_ids


async def process_uploaded_file(
    *,
    file: UploadFile,
    action: Action,
    mode: Mode,
    export_files: bool,
    output_dir: str | None,
    include_parse_result: bool,
    asset_type_id: str | None = None,
    customer_id: int = 0,
) -> dict:
    """处理单个上传文件。

    参数:
        file:
            前端上传的文件。

        action:
            处理动作。
            parse   = 只解析
            analyze = 解析后 AI 分析
            both    = 解析并 AI 分析

        mode:
            解析模式。
            例如 auto、ocr、recognize、parse、audio 等。

        export_files:
            是否导出 raw.md 和 summary.md。

        output_dir:
            导出目录。
            如果为空，则使用 DEFAULT_OUTPUT_DIR。

        include_parse_result:
            是否把解析结果返回给前端。

        asset_type_id:
            资产类型 ID。
            保存原始数据时写入 AI_YuanShishuju.ZcLeiXin。

        customer_id:
            关联客户 ID。
            保存原始数据时写入 AI_YuanShishuju.GuanLianKeHu。

    返回:
        当前文件的解析、AI 分析、入库 ID、导出文件等信息。
    """
    # 先把上传文件保存到本地临时目录
    upload_path = await _save_upload(file)

    # 只有 analyze / both 才执行 AI 分析
    should_analyze = action in {"analyze", "both"}

    try:
        # 判断文件类型，不支持的文件直接返回 400
        file_type = get_file_type(str(upload_path))
        if file_type == "unsupported":
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件类型: {file.filename}",
            )

        # 调用统一文件解析入口。
        # 注意这里 export=False，因为导出由当前 service 的 export_files 控制。
        processed = await process_file(
            file_path=str(upload_path),
            mode=mode,
            export=False,
        )

        # 如果解析失败，直接返回失败信息，不继续入库和 AI 分析
        if not processed.get("success"):
            return {
                "success": False,
                "file_name": file.filename,
                "error": processed.get("error", "文件处理失败"),
                "processed": processed,
            }

        # 从解析结果中提取可用于 AI 分析和原始数据保存的文本
        raw_text = _extract_raw_text(processed)

        # 保存原始数据后的 ID。
        # 后续问答和意图会通过 raw_data_id 关联到原始数据。
        raw_data_id = None

        # 只有解析出文本才保存原始数据
        if raw_text:
            from app.services.ai.knowledge.raw_data_service import save_raw_text

            raw_data_id = save_raw_text(
                raw_text=raw_text,
                source_file_path=str(upload_path),
                file_type=processed.get("file_type", ""),
                source_file_name=file.filename,
                asset_type_id=asset_type_id,
                guan_lian_ke_hu=customer_id,
                enterprise_id=None,
                in_userid=None,
            )

        # 初始化 AI 分析结果和入库结果
        analysis = None
        qa_analysis = None
        intent_analysis = None
        description_items = []
        qa_pair_ids = []
        intent_ids = []

        # 需要 AI 分析，并且原文不为空时，执行三套提示词和入库
        if should_analyze and raw_text.strip():
            (
                analysis,
                qa_analysis,
                intent_analysis,
                description_items,
                qa_pair_ids,
                intent_ids,
            ) = await _run_fixed_audio_knowledge_extract(
                raw_text=raw_text,
                raw_data_id=raw_data_id,
                upload_path=upload_path,
                file_type=processed.get("file_type", ""),
            )

        # 可选导出 Markdown 文件
        exports = None
        if export_files:
            exports = await export_knowledge_extract_result(
                processed=processed,
                raw_text=raw_text,
                output_dir=output_dir or str(DEFAULT_OUTPUT_DIR),
                qa_analysis=qa_analysis,
                intent_analysis=intent_analysis,
            )

        # 组装单文件处理结果
        item = {
            "success": True,
            "source_file_name": file.filename,
            "file_name": processed.get("file_name"),
            "file_type": processed.get("file_type"),
            "engine": processed.get("engine"),
            "mode": processed.get("mode"),
            "action": action,
            "raw_text": raw_text,
            "raw_data_id": raw_data_id,
            "analysis": analysis,
            "qa_analysis": qa_analysis,
            "intent_analysis": intent_analysis,
            "description_items": description_items,
            "qa_pair_ids": qa_pair_ids,
            "intent_ids": intent_ids,
            "exports": exports,
        }

        # 如果前端需要解析详情，则附带精简后的 processed
        if include_parse_result:
            item["processed"] = _compact_processed(processed)

        return item

    finally:
        # 无论成功还是失败，都删除临时上传文件，避免临时目录越来越大
        if upload_path.exists():
            upload_path.unlink()


async def process_uploaded_files(
    *,
    files: list[UploadFile],
    action: Action,
    mode: Mode,
    export_files: bool,
    output_dir: str | None,
    custom_prompt: str | None,
    include_parse_result: bool,
    asset_type_id: str | None = None,
    customer_id: int = 0,
) -> dict:
    """批量处理上传文件。

    参数:
        files:
            前端上传的文件列表。

        action:
            当前批次的处理动作。

        mode:
            文件解析模式。

        export_files:
            是否导出 Markdown 文件。

        output_dir:
            导出目录。

        custom_prompt:
            旧参数，目前固定三套提示词后已经不再使用。
            保留这个参数只是为了兼容旧接口调用。

        include_parse_result:
            是否返回解析结果。

        asset_type_id:
            资产类型 ID。

        customer_id:
            关联客户 ID。

    返回:
        批量处理结果。
    """
    if not files:
        raise HTTPException(status_code=400, detail="请至少上传一个文件")

    results = []

    # 逐个处理上传文件。
    # 这里是串行处理，如果后续文件很多，可以再考虑并发处理。
    for file in files:
        results.append(
            await process_uploaded_file(
                file=file,
                action=action,
                mode=mode,
                export_files=export_files,
                output_dir=output_dir,
                include_parse_result=include_parse_result,
                asset_type_id=asset_type_id,
                customer_id=customer_id,
            )
        )

    return {
        "success": True,
        "action": action,
        "mode": mode,
        "total": len(files),
        "results": results,
    }