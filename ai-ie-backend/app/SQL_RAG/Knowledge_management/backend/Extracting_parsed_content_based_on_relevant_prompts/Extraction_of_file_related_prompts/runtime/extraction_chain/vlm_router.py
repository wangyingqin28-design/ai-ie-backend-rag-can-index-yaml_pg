# [2026-07-03 18:11:51] 作用：导入依赖 `from fastapi import APIRouter, File, Form, UploadFile`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from fastapi import APIRouter, File, Form, UploadFile
# [2026-07-03 18:11:51] 作用：导入依赖 `from extraction_chain.process_service import Action, process_uploaded_files`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from extraction_chain.process_service import Action, process_uploaded_files
# [2026-07-03 18:11:51] 作用：导入依赖 `from app.ai.processors.processor import Mode`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from app.ai.processors.processor import Mode
# [2026-07-03 18:11:51] 作用：为 router 构造并保存赋值结果；本行执行 `router = APIRouter(prefix="/vlm", tags=["文件解析与AI分析"])`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
router = APIRouter(prefix="/vlm", tags=["文件解析与AI分析"])
# [2026-07-03 18:11:51] 作用：应用装饰器 `@router.post("/process")`，配置紧随其后的定义；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
@router.post("/process")
# [2026-07-03 18:11:51] 作用：声明异步函数 process_any_files，提供可等待的链路处理入口；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
async def process_any_files(
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_any_files 的签名或多行表达式片段 `files: list[UploadFile] = File(..., description="可上传任意支持的文件，可单文件或多文件"),`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
    files: list[UploadFile] = File(..., description="可上传任意支持的文件，可单文件或多文件"),
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_any_files 的签名或多行表达式片段 `action: Action = Form("analyze", description="parse=只解析，analyze=解析后AI分析"),`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
    action: Action = Form("analyze", description="parse=只解析，analyze=解析后AI分析"),
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_any_files 的签名或多行表达式片段 `mode: Mode = Form("auto", description="auto/ocr/recognize/parse/audio"),`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
    mode: Mode = Form("auto", description="auto/ocr/recognize/parse/audio"),
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_any_files 的签名或多行表达式片段 `export_files: bool = Form(False, description="是否导出 raw.md 和 summary.md"),`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
    export_files: bool = Form(False, description="是否导出 raw.md 和 summary.md"),
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_any_files 的签名或多行表达式片段 `output_dir: str | None = Form(None, description="导出目录，不传则使用默认临时输出目录"),`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
    output_dir: str | None = Form(None, description="导出目录，不传则使用默认临时输出目录"),
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_any_files 的签名或多行表达式片段 `include_parse_result: bool = Form(True, description="是否在响应中返回完整解析结果"),`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
    include_parse_result: bool = Form(True, description="是否在响应中返回完整解析结果"),
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_any_files 的签名或多行表达式片段 `asset_type_id: str | None = Form(None, description="资产类型ID，对应 AI_YuanShishuju.ZcLeiXin"),`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
    asset_type_id: str | None = Form(None, description="资产类型ID，对应 AI_YuanShishuju.ZcLeiXin"),
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_any_files 的签名或多行表达式片段 `customer_id: int = Form(0, description="涉及客户ID，对应 AI_YuanShishuju.GuanLianKeHu"),`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
    customer_id: int = Form(0, description="涉及客户ID，对应 AI_YuanShishuju.GuanLianKeHu"),
# [2026-07-03 18:11:51] 作用：在 process_any_files 中执行具体代码片段 `):`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
):
    # [2026-07-03 18:11:51] 作用：从 process_any_files 返回表达式 `return await process_uploaded_files(` 的结果；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
    return await process_uploaded_files(
        # [2026-07-03 18:11:51] 作用：完善 异步函数 process_any_files 的签名或多行表达式片段 `files=files,`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
        files=files,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 process_any_files 的签名或多行表达式片段 `action=action,`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
        action=action,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 process_any_files 的签名或多行表达式片段 `mode=mode,`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
        mode=mode,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 process_any_files 的签名或多行表达式片段 `export_files=export_files,`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
        export_files=export_files,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 process_any_files 的签名或多行表达式片段 `output_dir=output_dir,`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
        output_dir=output_dir,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 process_any_files 的签名或多行表达式片段 `custom_prompt=None,`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
        custom_prompt=None,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 process_any_files 的签名或多行表达式片段 `include_parse_result=include_parse_result,`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
        include_parse_result=include_parse_result,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 process_any_files 的签名或多行表达式片段 `asset_type_id=asset_type_id,`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
        asset_type_id=asset_type_id,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 process_any_files 的签名或多行表达式片段 `customer_id=customer_id,`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
        customer_id=customer_id,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 process_any_files 的签名或多行表达式片段 `)`；理由依据：源模块 extraction_chain.vlm_router 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 process_any_files
    )
