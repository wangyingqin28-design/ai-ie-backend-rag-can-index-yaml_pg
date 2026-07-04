# [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `import http.client`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
import http.client
# [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `import threading`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
import threading
# [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
# [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `from pathlib import Path`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
from pathlib import Path
# [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `import sys`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
import sys
# [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `from functools import partial`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
from functools import partial
# [2026-07-04 10:18:20] 作用：为 `WEBUI_ROOT` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
WEBUI_ROOT = Path(__file__).resolve().parents[1]
# [2026-07-04 10:18:20] 作用：执行本行代码 `sys.path.insert(0, str(WEBUI_ROOT))`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
sys.path.insert(0, str(WEBUI_ROOT))
# [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `import webui_server`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
import webui_server

# [2026-07-04 10:18:20] 作用：声明 `RecordingHandler` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
class RecordingHandler(BaseHTTPRequestHandler):
    # [2026-07-04 10:18:20] 作用：为 `content_type` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    content_type = ""
    # [2026-07-04 10:18:20] 作用：为 `body` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    body = b""
    # [2026-07-04 10:18:20] 作用：声明 `do_POST` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
    def do_POST(self) -> None:
        # [2026-07-04 10:18:20] 作用：为 `length` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
        length = int(self.headers.get("Content-Length", "0"))
        # [2026-07-04 10:18:20] 作用：为 `type(self).content_type` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
        type(self).content_type = self.headers.get("Content-Type", "")
        # [2026-07-04 10:18:20] 作用：为 `type(self).body` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
        type(self).body = self.rfile.read(length)
        # [2026-07-04 10:18:20] 作用：执行本行代码 `self.send_response(200)`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        self.send_response(200)
        # [2026-07-04 10:18:20] 作用：执行本行代码 `self.send_header("Content-Type", "application/json")`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        self.send_header("Content-Type", "application/json")
        # [2026-07-04 10:18:20] 作用：执行本行代码 `self.send_header("Content-Length", "2")`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        self.send_header("Content-Length", "2")
        # [2026-07-04 10:18:20] 作用：执行本行代码 `self.end_headers()`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        self.end_headers()
        # [2026-07-04 10:18:20] 作用：执行本行代码 `self.wfile.write(b"{}")`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        self.wfile.write(b"{}")
    # [2026-07-04 10:18:20] 作用：声明 `log_message` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
    def log_message(self, format: str, *args: object) -> None:
        # [2026-07-04 10:18:20] 作用：执行控制结果 `return None`；理由依据：调用方必须获得明确返回值或可诊断失败。
        return None

# [2026-07-04 10:18:20] 作用：声明 `_serve` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
def _serve(server: ThreadingHTTPServer) -> threading.Thread:
    # [2026-07-04 10:18:20] 作用：为 `thread` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    # [2026-07-04 10:18:20] 作用：执行本行代码 `thread.start()`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    thread.start()
    # [2026-07-04 10:18:20] 作用：执行控制结果 `return thread`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return thread

# [2026-07-04 10:18:20] 作用：声明 `test_proxy_preserves_multipart_boundary_and_supports_long_processing` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
def test_proxy_preserves_multipart_boundary_and_supports_long_processing() -> None:
    # [2026-07-04 10:18:20] 作用：执行验收断言 `assert webui_server.PROXY_TIMEOUT_SECONDS >= 600`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
    assert webui_server.PROXY_TIMEOUT_SECONDS >= 600
    # [2026-07-04 10:18:20] 作用：为 `upstream` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    upstream = ThreadingHTTPServer(("127.0.0.1", 0), RecordingHandler)
    # [2026-07-04 10:18:20] 作用：为 `upstream_thread` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    upstream_thread = _serve(upstream)
    # [2026-07-04 10:18:20] 作用：为 `webui_server.KnowledgeWebUIHandler.backend_url` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    webui_server.KnowledgeWebUIHandler.backend_url = f"http://127.0.0.1:{upstream.server_port}"
    # [2026-07-04 10:18:20] 作用：为 `handler` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    handler = partial(webui_server.KnowledgeWebUIHandler, directory=str(WEBUI_ROOT))
    # [2026-07-04 10:18:20] 作用：为 `proxy` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    proxy = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    # [2026-07-04 10:18:20] 作用：为 `proxy_thread` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    proxy_thread = _serve(proxy)
    # [2026-07-04 10:18:20] 作用：为 `boundary` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    boundary = "----CodexKnowledgeBoundary"
    # [2026-07-04 10:18:20] 作用：为 `body` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    body = f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"audio.m4a\"\r\nContent-Type: audio/mp4\r\n\r\n".encode() + b"audio-bytes" + f"\r\n--{boundary}--\r\n".encode()
    # [2026-07-04 10:18:20] 作用：为 `connection` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    connection = http.client.HTTPConnection("127.0.0.1", proxy.server_port, timeout=5)
    # [2026-07-04 10:18:20] 作用：进入异常控制片段 `try:`；理由依据：真实网络、模型和数据库调用必须正确传播并清理异常状态。
    try:
        # [2026-07-04 10:18:20] 作用：为 `connection.request("POST", "/api/knowledge/parse", body` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
        connection.request("POST", "/api/knowledge/parse", body=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
        # [2026-07-04 10:18:20] 作用：为 `response` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
        response = connection.getresponse()
        # [2026-07-04 10:18:20] 作用：执行本行代码 `response.read()`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        response.read()
        # [2026-07-04 10:18:20] 作用：执行验收断言 `assert response.status == 200`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
        assert response.status == 200
        # [2026-07-04 10:18:20] 作用：执行验收断言 `assert RecordingHandler.content_type == f"multipart/form-data; boundary={boundary}"`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
        assert RecordingHandler.content_type == f"multipart/form-data; boundary={boundary}"
        # [2026-07-04 10:18:20] 作用：执行验收断言 `assert RecordingHandler.body == body`；理由依据：防止真实 multipart、错误传播或字段映射发生回归。
        assert RecordingHandler.body == body
    # [2026-07-04 10:18:20] 作用：进入异常控制片段 `finally:`；理由依据：真实网络、模型和数据库调用必须正确传播并清理异常状态。
    finally:
        # [2026-07-04 10:18:20] 作用：执行本行代码 `connection.close()`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        connection.close()
        # [2026-07-04 10:18:20] 作用：执行本行代码 `proxy.shutdown()`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        proxy.shutdown()
        # [2026-07-04 10:18:20] 作用：执行本行代码 `proxy.server_close()`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        proxy.server_close()
        # [2026-07-04 10:18:20] 作用：为 `proxy_thread.join(timeout` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
        proxy_thread.join(timeout=5)
        # [2026-07-04 10:18:20] 作用：执行本行代码 `upstream.shutdown()`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        upstream.shutdown()
        # [2026-07-04 10:18:20] 作用：执行本行代码 `upstream.server_close()`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        upstream.server_close()
        # [2026-07-04 10:18:20] 作用：为 `upstream_thread.join(timeout` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
        upstream_thread.join(timeout=5)
