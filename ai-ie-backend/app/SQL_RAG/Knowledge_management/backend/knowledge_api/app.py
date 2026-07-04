# [2026-07-04 10:18:20] 作用：导入 FastAPI 应用与表单上传组件；理由依据：服务需提供健康检查和真实 multipart 音频入口。
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
# [2026-07-04 10:18:20] 作用：导入 SQL 文本构造器；理由依据：健康接口执行只读 SELECT 1。
from sqlalchemy import text
# [2026-07-04 10:18:20] 作用：导入 SQLAlchemy 基础异常；理由依据：数据库不可用时健康结果必须明确为 false。
from sqlalchemy.exc import SQLAlchemyError
# [2026-07-04 10:18:20] 作用：导入运行时路径初始化；理由依据：加载公共 app 和专属 extraction_chain 前必须配置搜索路径。
from knowledge_api.runtime_paths import configure_runtime_paths
# [2026-07-04 10:18:20] 作用：执行一次运行时初始化；理由依据：随后导入依赖会读取公共 runtime/.env。
configure_runtime_paths()
# [2026-07-04 10:18:20] 作用：导入真实配置和同步引擎；理由依据：健康检查需验证模型配置与 PostgreSQL。
from app.config import settings, sync_engine
# [2026-07-04 10:18:20] 作用：导入原有批量 VLM 路由；理由依据：独立服务保留迁移链既有 `/vlm/process` 能力。
from extraction_chain.vlm_router import router as vlm_router
# [2026-07-04 10:18:20] 作用：导入单文件总调度入口；理由依据：新路由必须复用文件解析、三轮 DeepSeek 和三表入库链。
from extraction_chain.process_service import process_uploaded_file
# [2026-07-04 10:18:20] 作用：导入 WebUI 响应映射函数；理由依据：业务返回和前端展示合同保持分离。
from knowledge_api.response_mapper import map_process_result
# [2026-07-04 10:18:20] 作用：创建独立 Knowledge FastAPI 应用；理由依据：按方案 A 使用新端口隔离主业务后端。
app = FastAPI(title="Knowledge Management API")
# [2026-07-04 10:18:20] 作用：注册原有 VLM 批量路由；理由依据：避免因新增单文件接口丢失已有链路入口。
app.include_router(vlm_router)

# [2026-07-04 10:18:20] 作用：声明健康检查接口；理由依据：PS1 需验证配置和数据库而非仅端口监听。
@app.get("/health")
# [2026-07-04 10:18:20] 作用：执行 Knowledge 服务健康判定；理由依据：返回可用于启动脚本的 ready 布尔值。
def health() -> dict[str, object]:
    # [2026-07-04 10:18:20] 作用：检查语音、LLM 模型及 API Key 配置；理由依据：缺任一项都无法完成真实两条链路。
    configured = bool(settings.embedding_service_api_key and settings.LLM_MODEL and settings.AUDIO_TRANSCRIPTION_MODEL)
    # [2026-07-04 10:18:20] 作用：初始化数据库健康状态；理由依据：只有 SELECT 1 成功才可置为 true。
    database_ready = False
    # [2026-07-04 10:18:20] 作用：开始数据库探活；理由依据：不写入数据且能验证连接和认证。
    try:
        # [2026-07-04 10:18:20] 作用：获取短生命周期同步连接；理由依据：探活结束立即归还连接池。
        with sync_engine.connect() as connection:
            # [2026-07-04 10:18:20] 作用：执行只读 SELECT 1；理由依据：验证目标 PostgreSQL 实际可访问。
            connection.execute(text("SELECT 1"))
        # [2026-07-04 10:18:20] 作用：标记数据库可用；理由依据：连接与查询均已成功。
        database_ready = True
    # [2026-07-04 10:18:20] 作用：捕获 SQLAlchemy 数据库异常；理由依据：健康接口不得因外部故障返回未处理 traceback。
    except SQLAlchemyError:
        # [2026-07-04 10:18:20] 作用：保持数据库不可用状态；理由依据：PS1 必须阻止假 ready。
        database_ready = False
    # [2026-07-04 10:18:20] 作用：返回健康明细；理由依据：日志需区分配置失败和数据库失败。
    return {"ready": configured and database_ready, "configured": configured, "database": database_ready, "service": "knowledge_backend"}

# [2026-07-04 10:18:20] 作用：声明单文件知识解析接口；理由依据：WebUI 需上传真实音频并串联解析、提取和入库。
@app.post("/knowledge/parse")
# [2026-07-04 10:18:20] 作用：接收上传文件和关联元数据；理由依据：ZcLeiXin 与 GuanLianKeHu 必须从表单准确传递。
async def parse_knowledge(
    # [2026-07-04 10:18:20] 作用：接收 multipart 文件主体；理由依据：不能只传文件名和大小。
    file: UploadFile = File(...),
    # [2026-07-04 10:18:20] 作用：接收真实资产类型 ID；理由依据：原始表 ZcLeiXin 需要可追溯来源。
    asset_type_id: str | None = Form(None),
    # [2026-07-04 10:18:20] 作用：接收客户 ID 字符串；理由依据：HTTP 表单为文本且下游原接口当前接收整数。
    customer_id: str = Form("0"),
# [2026-07-04 10:18:20] 作用：结束路由签名并声明 JSON 字典返回；理由依据：FastAPI 自动序列化给 WebUI。
) -> dict[str, object]:
    # [2026-07-04 10:18:20] 作用：拒绝缺少文件名的上传；理由依据：无法确定扩展名时统一解析器不能选择音频分支。
    if not file.filename:
        # [2026-07-04 10:18:20] 作用：返回 400 客户端错误；理由依据：明确指出上传协议缺失。
        raise HTTPException(status_code=400, detail="上传文件名不能为空")
    # [2026-07-04 10:18:20] 作用：把客户 ID 转为原处理服务类型；理由依据：拒绝非数字客户 ID 防止错误写入复合主键。
    try:
        # [2026-07-04 10:18:20] 作用：执行十进制整数转换；理由依据：沿用 process_uploaded_file 现有签名。
        customer_number = int(customer_id)
    # [2026-07-04 10:18:20] 作用：捕获无效客户 ID；理由依据：格式错误属于可解释的客户端输入问题。
    except ValueError as exc:
        # [2026-07-04 10:18:20] 作用：返回 400 并保留异常链；理由依据：禁止静默改写为默认客户。
        raise HTTPException(status_code=400, detail="customer_id 必须是整数") from exc
    # [2026-07-04 10:18:20] 作用：调用现有完整处理链；理由依据：必须真实执行文件解析、三轮 DeepSeek 和三表入库。
    result = await process_uploaded_file(file=file, action="analyze", mode="auto", export_files=False, output_dir=None, include_parse_result=True, asset_type_id=asset_type_id, customer_id=customer_number)
    # [2026-07-04 10:18:20] 作用：检查业务处理是否成功；理由依据：解析失败不能映射成 WebUI 成功页面。
    if not result.get("success"):
        # [2026-07-04 10:18:20] 作用：返回 502 真实处理错误；理由依据：向前端明确外部解析或提取链失败。
        raise HTTPException(status_code=502, detail=result.get("error", "文件解析或知识提取失败"))
    # [2026-07-04 10:18:20] 作用：返回真实处理结果的 WebUI 映射；理由依据：保留全文、知识项和三类数据库 ID。
    return map_process_result(result)
