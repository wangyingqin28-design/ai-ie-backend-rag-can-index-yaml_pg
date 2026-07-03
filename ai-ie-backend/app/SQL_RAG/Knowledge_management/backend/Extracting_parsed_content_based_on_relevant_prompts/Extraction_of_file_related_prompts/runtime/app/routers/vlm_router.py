# [2026-07-03 14:26:28] 中文迁移说明：本文件完整复制自 app/routers/vlm_router.py；纳入依据为 DeepSeek 提取入库链 的项目内传递依赖闭包。
from fastapi import APIRouter, File, Form, UploadFile

from app.services.ai.extraction.process_service import Action, process_uploaded_files
from app.ai.processors.processor import Mode


router = APIRouter(prefix="/vlm", tags=["文件解析与AI分析"])


@router.post("/process")
async def process_any_files(
    files: list[UploadFile] = File(..., description="可上传任意支持的文件，可单文件或多文件"),
    action: Action = Form("analyze", description="parse=只解析，analyze=解析后AI分析"),
    mode: Mode = Form("auto", description="auto/ocr/recognize/parse/audio"),
    export_files: bool = Form(False, description="是否导出 raw.md 和 summary.md"),
    output_dir: str | None = Form(None, description="导出目录，不传则使用默认临时输出目录"),
    include_parse_result: bool = Form(True, description="是否在响应中返回完整解析结果"),
    asset_type_id: str | None = Form(None, description="资产类型ID，对应 AI_YuanShishuju.ZcLeiXin"),
    customer_id: int = Form(0, description="涉及客户ID，对应 AI_YuanShishuju.GuanLianKeHu"),
):
    return await process_uploaded_files(
        files=files,
        action=action,
        mode=mode,
        export_files=export_files,
        output_dir=output_dir,
        custom_prompt=None,
        include_parse_result=include_parse_result,
        asset_type_id=asset_type_id,
        customer_id=customer_id,
    )
