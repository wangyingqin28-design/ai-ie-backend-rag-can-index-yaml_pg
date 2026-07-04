# [2026-07-04 10:18:20] 作用：导入 JSON 组件；理由依据：构造模拟问答和意图返回。
import json
# [2026-07-04 10:18:20] 作用：导入模块缓存控制；理由依据：pytest 父包收集会预先缓存主应用 `app`，测试需切换到 Knowledge 公共运行时。
import sys
# [2026-07-04 10:18:20] 作用：导入异步模拟对象；理由依据：隔离真实外部 API 验证 multipart 协议。
from unittest.mock import AsyncMock
# [2026-07-04 10:18:20] 作用：导入 FastAPI 测试客户端；理由依据：通过真实 ASGI 路由执行上传测试。
from fastapi.testclient import TestClient
# [2026-07-04 10:18:20] 作用：声明伪数据库结果上下文；理由依据：健康测试不连接外部数据库。
class FakeConnection:
    # [2026-07-04 10:18:20] 作用：进入伪连接上下文；理由依据：匹配 SQLAlchemy connection 用法。
    def __enter__(self):
        # [2026-07-04 10:18:20] 作用：返回伪连接自身；理由依据：允许调用 execute。
        return self
    # [2026-07-04 10:18:20] 作用：退出伪连接上下文；理由依据：匹配资源清理协议。
    def __exit__(self, exc_type, exc, traceback) -> None:
        # [2026-07-04 10:18:20] 作用：显式不吞掉异常；理由依据：健康失败必须传播到路由处理。
        return None
    # [2026-07-04 10:18:20] 作用：接受 SELECT 1；理由依据：模拟数据库探活成功。
    def execute(self, statement):
        # [2026-07-04 10:18:20] 作用：返回固定探活结果；理由依据：测试只关心调用成功。
        return 1

# [2026-07-04 10:18:20] 作用：声明伪数据库引擎；理由依据：向健康路由提供 connect 接口。
class FakeEngine:
    # [2026-07-04 10:18:20] 作用：创建伪连接；理由依据：匹配 SQLAlchemy Engine.connect。
    def connect(self):
        # [2026-07-04 10:18:20] 作用：返回成功连接上下文；理由依据：模拟 SELECT 1 可用。
        return FakeConnection()

# [2026-07-04 10:18:20] 作用：声明运行时模块缓存清理函数；理由依据：确保 API 导入的是 public_program_files/runtime/app。
def _purge_runtime_modules() -> None:
    # [2026-07-04 10:18:20] 作用：遍历当前模块缓存名称；理由依据：安全复制键列表后才能删除匹配项。
    for name in list(sys.modules):
        # [2026-07-04 10:18:20] 作用：识别公共 app 和专属 extraction_chain 模块；理由依据：两者都可能被其他测试提前导入。
        if name == "app" or name.startswith("app.") or name == "extraction_chain" or name.startswith("extraction_chain.") or name == "knowledge_api.app":
            # [2026-07-04 10:18:20] 作用：移除冲突模块缓存；理由依据：让 Python 按 runtime_paths 的新顺序重新解析。
            sys.modules.pop(name, None)

# [2026-07-04 10:18:20] 作用：验证健康接口同时检查配置和数据库；理由依据：PS1 不能把仅端口可访问误判为全链可用。
def test_health_requires_configured_models_and_database(monkeypatch) -> None:
    # [2026-07-04 10:18:20] 作用：清理 pytest 预载主应用模块；理由依据：避免误导入 SQL Server 配置。
    _purge_runtime_modules()
    # [2026-07-04 10:18:20] 作用：在测试执行阶段导入 API 模块；理由依据：避免收集阶段公共 `app` 包遮蔽 pytest 的父包解析。
    import knowledge_api.app as app_module
    # [2026-07-04 10:18:20] 作用：替换数据库引擎；理由依据：测试不访问真实 PostgreSQL。
    monkeypatch.setattr(app_module, "sync_engine", FakeEngine())
    # [2026-07-04 10:18:20] 作用：创建 API 测试客户端；理由依据：通过真实路由序列化响应。
    client = TestClient(app_module.app)
    # [2026-07-04 10:18:20] 作用：调用健康接口；理由依据：验证启动脚本依赖的合同。
    response = client.get("/health")
    # [2026-07-04 10:18:20] 作用：断言 HTTP 成功；理由依据：配置和伪数据库均可用。
    assert response.status_code == 200
    # [2026-07-04 10:18:20] 作用：断言服务 ready；理由依据：PS1 最终 ready 判定读取该字段。
    assert response.json()["ready"] is True

# [2026-07-04 10:18:20] 作用：验证 multipart 上传参数和真实结果返回；理由依据：WebUI 必须把文件内容送入现有总调度链。
def test_parse_route_forwards_real_upload_and_metadata(monkeypatch) -> None:
    # [2026-07-04 10:18:20] 作用：清理前一测试和 pytest 预载模块；理由依据：确保测试隔离且使用 Knowledge 配置。
    _purge_runtime_modules()
    # [2026-07-04 10:18:20] 作用：在测试执行阶段导入 API 模块；理由依据：父包收集完成后再加载公共 `app` 运行时。
    import knowledge_api.app as app_module
    # [2026-07-04 10:18:20] 作用：构造成功处理结果；理由依据：隔离外部 API 只测试路由协议。
    parser = AsyncMock(return_value={"success": True, "source_file_name": "新录音 4.m4a", "raw_text": "转录", "raw_data_id": "raw-id", "qa_pair_ids": ["qa-id"], "intent_ids": ["intent-id"], "qa_analysis": json.dumps([{"standard_question": "问题", "answer": "答案"}], ensure_ascii=False), "intent_analysis": json.dumps([{"intent": "意图", "description": "说明", "evidence": "原文"}], ensure_ascii=False)})
    # [2026-07-04 10:18:20] 作用：替换真实文件处理入口；理由依据：避免单元测试调用硅基流动和数据库。
    monkeypatch.setattr(app_module, "process_uploaded_file", parser)
    # [2026-07-04 10:18:20] 作用：创建 API 测试客户端；理由依据：执行真实 multipart 解码。
    client = TestClient(app_module.app)
    # [2026-07-04 10:18:20] 作用：上传音频字节及业务元数据；理由依据：验证 asset_type_id/customer_id 无错位传递。
    response = client.post("/knowledge/parse", files={"file": ("新录音 4.m4a", b"audio-bytes", "audio/mp4")}, data={"asset_type_id": "asset-1", "customer_id": "9"})
    # [2026-07-04 10:18:20] 作用：断言路由成功；理由依据：模拟处理结果完整。
    assert response.status_code == 200
    # [2026-07-04 10:18:20] 作用：读取处理调用参数；理由依据：逐项核对总调度合同。
    kwargs = parser.await_args.kwargs
    # [2026-07-04 10:18:20] 作用：断言执行真实分析动作；理由依据：必须同时解析、DeepSeek 提取和入库。
    assert kwargs["action"] == "analyze"
    # [2026-07-04 10:18:20] 作用：断言自动解析模式；理由依据：由统一文件类型识别选择音频分支。
    assert kwargs["mode"] == "auto"
    # [2026-07-04 10:18:20] 作用：断言返回解析细节；理由依据：WebUI 需显示全文和引擎信息。
    assert kwargs["include_parse_result"] is True
    # [2026-07-04 10:18:20] 作用：断言资产类型原值传递；理由依据：ZcLeiXin 不得错写。
    assert kwargs["asset_type_id"] == "asset-1"
    # [2026-07-04 10:18:20] 作用：断言客户 ID 转为处理服务所需整数；理由依据：保持原接口签名兼容。
    assert kwargs["customer_id"] == 9
    # [2026-07-04 10:18:20] 作用：断言返回原始数据 ID；理由依据：端到端脚本需据此查询三表。
    assert response.json()["rawDataId"] == "raw-id"
