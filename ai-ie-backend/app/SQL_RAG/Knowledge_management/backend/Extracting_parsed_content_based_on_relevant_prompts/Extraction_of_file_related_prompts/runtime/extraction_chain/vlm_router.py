# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.vlm_router 的模块级声明
from fastapi import APIRouter, File, Form, UploadFile
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.vlm_router 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.vlm_router 的模块级声明
from extraction_chain.process_service import Action, process_uploaded_files
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.vlm_router 的模块级声明
from app.ai.processors.processor import Mode
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.vlm_router 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.vlm_router 的模块级声明
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.vlm_router 的模块级声明
router = APIRouter(prefix="/vlm", tags=["文件解析与AI分析"])
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.vlm_router 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.vlm_router 的模块级声明
# [2026-07-03 16:33:01] 作用：为下方定义注册装饰器行为；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.vlm_router 的模块级声明
@router.post("/process")
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
async def process_any_files(
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
    files: list[UploadFile] = File(..., description="可上传任意支持的文件，可单文件或多文件"),
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
    action: Action = Form("analyze", description="parse=只解析，analyze=解析后AI分析"),
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
    mode: Mode = Form("auto", description="auto/ocr/recognize/parse/audio"),
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
    export_files: bool = Form(False, description="是否导出 raw.md 和 summary.md"),
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
    output_dir: str | None = Form(None, description="导出目录，不传则使用默认临时输出目录"),
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
    include_parse_result: bool = Form(True, description="是否在响应中返回完整解析结果"),
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
    asset_type_id: str | None = Form(None, description="资产类型ID，对应 AI_YuanShishuju.ZcLeiXin"),
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
    customer_id: int = Form(0, description="涉及客户ID，对应 AI_YuanShishuju.GuanLianKeHu"),
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
):
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
    return await process_uploaded_files(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
        files=files,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
        action=action,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
        mode=mode,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
        export_files=export_files,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
        output_dir=output_dir,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
        custom_prompt=None,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
        include_parse_result=include_parse_result,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
        asset_type_id=asset_type_id,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
        customer_id=customer_id,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 process_any_files
    )
