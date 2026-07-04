# [2026-07-04 10:18:20] 作用：导入路径对象；理由依据：从 Knowledge 测试目录稳定定位 SQL_RAG 启动脚本。
from pathlib import Path
# [2026-07-04 10:18:20] 作用：计算 Knowledge_management 根目录；理由依据：测试不能依赖当前工作目录。
KNOWLEDGE_ROOT = Path(__file__).resolve().parents[1]
# [2026-07-04 10:18:20] 作用：定位 start-latest-full-stack.ps1；理由依据：Knowledge 根目录与脚本同属 SQL_RAG。
LAUNCHER = KNOWLEDGE_ROOT.parent / "start-latest-full-stack.ps1"

# [2026-07-04 10:18:20] 作用：验证 Knowledge 前后端完整接入全量启动脚本；理由依据：用户只执行这一条 PS1 命令验收。
def test_full_stack_launcher_contains_knowledge_services_and_health_gates() -> None:
    # [2026-07-04 10:18:20] 作用：读取启动脚本文本；理由依据：静态检查端口、命令和 ready 条件不启动外部服务。
    source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-07-04 10:18:20] 作用：声明必须存在的 Knowledge 集成标记；理由依据：覆盖端口、进程、日志和健康链。
    required = (
        # [2026-07-04 10:18:20] 作用：要求独立后端端口变量；理由依据：避免与现有 18180/18190 冲突。
        "$KnowledgeBackendPort=18320",
        # [2026-07-04 10:18:20] 作用：要求独立 WebUI 端口变量；理由依据：避免与现有 18181/18191 冲突。
        "$KnowledgeWebPort=18321",
        # [2026-07-04 10:18:20] 作用：要求启动 Knowledge API 入口；理由依据：真实后端必须由全量脚本拉起。
        "Knowledge_management\\backend\\knowledge_api\\run_server.py",
        # [2026-07-04 10:18:20] 作用：要求启动 Knowledge WebUI 入口；理由依据：用户需通过同源 `/api` 上传。
        "Knowledge_management\\webui\\webui_server.py",
        # [2026-07-04 10:18:20] 作用：要求后端日志前缀；理由依据：便于定位语音、DeepSeek 和数据库错误。
        "knowledge-backend-",
        # [2026-07-04 10:18:20] 作用：要求 WebUI 日志前缀；理由依据：便于定位代理错误。
        "knowledge-webui-",
        # [2026-07-04 10:18:20] 作用：要求后端 ready 状态变量；理由依据：最终成功条件必须包含真实 API 健康。
        "$knowledgeBackendReady",
        # [2026-07-04 10:18:20] 作用：要求 WebUI ready 状态变量；理由依据：最终成功条件必须包含页面可访问。
        "$knowledgeWebReady",
        # [2026-07-04 10:18:20] 作用：要求代理 ready 状态变量；理由依据：最终成功条件必须包含 `/api` 转发可用。
        "$knowledgeProxyReady",
        # [2026-07-04 10:18:20] 作用：要求 WebUI 代理健康路径；理由依据：确认 18321 能转发到 18320。
        "$KnowledgeWebUrl/api/health",
    # [2026-07-04 10:18:20] 作用：结束必需标记集合；理由依据：逐项检查缺失内容。
    )
    # [2026-07-04 10:18:20] 作用：遍历每个必需标记；理由依据：失败信息精确显示遗漏项。
    for marker in required:
        # [2026-07-04 10:18:20] 作用：断言标记存在于脚本；理由依据：任一缺失都不能宣称全量服务 ready。
        assert marker in source, marker
    # [2026-07-04 10:18:20] 作用：定位最终失败保护语句；理由依据：检查 all-ready 谓词而非仅变量声明。
    final_guard = source[source.rfind("if(!("):]
    # [2026-07-04 10:18:20] 作用：断言最终条件包含 Knowledge 后端；理由依据：后端失败时脚本必须抛错。
    assert "$knowledgeBackendReady" in final_guard
    # [2026-07-04 10:18:20] 作用：断言最终条件包含 Knowledge WebUI；理由依据：页面失败时脚本必须抛错。
    assert "$knowledgeWebReady" in final_guard
    # [2026-07-04 10:18:20] 作用：断言最终条件包含 Knowledge 代理；理由依据：代理失败时脚本必须抛错。
    assert "$knowledgeProxyReady" in final_guard
