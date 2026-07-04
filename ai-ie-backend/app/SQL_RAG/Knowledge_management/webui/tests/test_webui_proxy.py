# [2026-07-04 10:18:20] 作用：导入 HTTP 客户端；理由依据：通过真实本地端口验证代理请求字节。
import http.client
# [2026-07-04 10:18:20] 作用：导入线程组件；理由依据：测试中并行运行上游和 WebUI 两个 HTTP 服务。
import threading
# [2026-07-04 10:18:20] 作用：导入轻量 HTTP 服务器类；理由依据：构造记录 multipart 请求的本地上游。
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
# [2026-07-04 10:18:20] 作用：导入路径对象；理由依据：从测试位置定位 WebUI 源目录。
from pathlib import Path
# [2026-07-04 10:18:20] 作用：导入模块搜索路径控制；理由依据：webui_server.py 不在 Python 包目录中。
import sys
# [2026-07-04 10:18:20] 作用：导入处理器偏函数；理由依据：为静态 WebUI 处理器绑定目录参数。
from functools import partial
# [2026-07-04 10:18:20] 作用：计算 WebUI 根目录；理由依据：避免依赖测试启动工作目录。
WEBUI_ROOT = Path(__file__).resolve().parents[1]
# [2026-07-04 10:18:20] 作用：加入 WebUI 模块搜索路径；理由依据：允许导入待测 webui_server。
sys.path.insert(0, str(WEBUI_ROOT))
# [2026-07-04 10:18:20] 作用：导入待测 WebUI 代理模块；理由依据：读取超时常量并启动真实处理器。
import webui_server

# [2026-07-04 10:18:20] 作用：声明记录上游请求的处理器；理由依据：验证代理未改变 boundary 和文件字节。
class RecordingHandler(BaseHTTPRequestHandler):
    # [2026-07-04 10:18:20] 作用：保存最近请求内容类型；理由依据：断言 multipart boundary 原样转发。
    content_type = ""
    # [2026-07-04 10:18:20] 作用：保存最近请求主体；理由依据：断言文件字节逐字节一致。
    body = b""
    # [2026-07-04 10:18:20] 作用：处理代理转发的 POST；理由依据：真实上传接口使用 POST。
    def do_POST(self) -> None:
        # [2026-07-04 10:18:20] 作用：读取请求体长度；理由依据：精确读取 multipart 字节。
        length = int(self.headers.get("Content-Length", "0"))
        # [2026-07-04 10:18:20] 作用：记录完整内容类型；理由依据：boundary 参数不能丢失。
        type(self).content_type = self.headers.get("Content-Type", "")
        # [2026-07-04 10:18:20] 作用：记录完整请求体；理由依据：代理不能重新编码音频数据。
        type(self).body = self.rfile.read(length)
        # [2026-07-04 10:18:20] 作用：向代理返回成功状态；理由依据：完成往返协议验证。
        self.send_response(200)
        # [2026-07-04 10:18:20] 作用：设置 JSON 内容类型；理由依据：模拟 Knowledge 后端响应。
        self.send_header("Content-Type", "application/json")
        # [2026-07-04 10:18:20] 作用：设置固定响应长度；理由依据：客户端可完整读取 `{}`。
        self.send_header("Content-Length", "2")
        # [2026-07-04 10:18:20] 作用：结束响应头；理由依据：遵守 HTTP 协议。
        self.end_headers()
        # [2026-07-04 10:18:20] 作用：写入空 JSON 响应；理由依据：代理应原样返回成功体。
        self.wfile.write(b"{}")
    # [2026-07-04 10:18:20] 作用：关闭测试上游访问日志；理由依据：保持 pytest 输出干净。
    def log_message(self, format: str, *args: object) -> None:
        # [2026-07-04 10:18:20] 作用：显式忽略日志；理由依据：断言不依赖日志文本。
        return None

# [2026-07-04 10:18:20] 作用：在后台线程启动 HTTP 服务；理由依据：测试客户端需同步访问两个本地端口。
def _serve(server: ThreadingHTTPServer) -> threading.Thread:
    # [2026-07-04 10:18:20] 作用：创建守护线程；理由依据：测试异常时线程不阻止 Python 退出。
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    # [2026-07-04 10:18:20] 作用：启动服务器线程；理由依据：端口开始接受请求。
    thread.start()
    # [2026-07-04 10:18:20] 作用：返回线程句柄；理由依据：测试结束时等待干净退出。
    return thread

# [2026-07-04 10:18:20] 作用：验证长超时及 multipart 透明转发；理由依据：真实音频解析不能因代理改写或三秒超时失败。
def test_proxy_preserves_multipart_boundary_and_supports_long_processing() -> None:
    # [2026-07-04 10:18:20] 作用：断言代理超时覆盖完整外部调用链；理由依据：FFmpeg、语音和三轮 DeepSeek 可能耗时数分钟。
    assert webui_server.PROXY_TIMEOUT_SECONDS >= 600
    # [2026-07-04 10:18:20] 作用：创建随机空闲端口的上游服务器；理由依据：避免与本机现有服务冲突。
    upstream = ThreadingHTTPServer(("127.0.0.1", 0), RecordingHandler)
    # [2026-07-04 10:18:20] 作用：启动上游服务器；理由依据：接收代理转发请求。
    upstream_thread = _serve(upstream)
    # [2026-07-04 10:18:20] 作用：配置代理目标 URL；理由依据：把 WebUI 指向本测试上游。
    webui_server.KnowledgeWebUIHandler.backend_url = f"http://127.0.0.1:{upstream.server_port}"
    # [2026-07-04 10:18:20] 作用：绑定 WebUI 静态目录处理器；理由依据：匹配生产启动方式。
    handler = partial(webui_server.KnowledgeWebUIHandler, directory=str(WEBUI_ROOT))
    # [2026-07-04 10:18:20] 作用：创建随机空闲端口的 WebUI 服务器；理由依据：避免测试端口冲突。
    proxy = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    # [2026-07-04 10:18:20] 作用：启动 WebUI 代理服务器；理由依据：通过真实网络层执行 `_proxy_request`。
    proxy_thread = _serve(proxy)
    # [2026-07-04 10:18:20] 作用：定义 multipart boundary；理由依据：断言内容类型参数原样到达上游。
    boundary = "----CodexKnowledgeBoundary"
    # [2026-07-04 10:18:20] 作用：构造包含音频字节的 multipart 主体；理由依据：模拟浏览器 FormData 上传。
    body = f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"audio.m4a\"\r\nContent-Type: audio/mp4\r\n\r\n".encode() + b"audio-bytes" + f"\r\n--{boundary}--\r\n".encode()
    # [2026-07-04 10:18:20] 作用：创建到 WebUI 的 HTTP 连接；理由依据：测试 `/api` 代理入口。
    connection = http.client.HTTPConnection("127.0.0.1", proxy.server_port, timeout=5)
    # [2026-07-04 10:18:20] 作用：开始确保服务器资源最终清理；理由依据：测试成功或失败均不能遗留监听端口。
    try:
        # [2026-07-04 10:18:20] 作用：发送 multipart POST；理由依据：路径与生产前端完全一致。
        connection.request("POST", "/api/knowledge/parse", body=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
        # [2026-07-04 10:18:20] 作用：读取代理响应；理由依据：等待转发完整完成。
        response = connection.getresponse()
        # [2026-07-04 10:18:20] 作用：消费响应体；理由依据：释放 HTTP 连接。
        response.read()
        # [2026-07-04 10:18:20] 作用：断言代理返回成功；理由依据：上游成功应透明传回。
        assert response.status == 200
        # [2026-07-04 10:18:20] 作用：断言 boundary 原样转发；理由依据：FastAPI 依赖该参数解析文件。
        assert RecordingHandler.content_type == f"multipart/form-data; boundary={boundary}"
        # [2026-07-04 10:18:20] 作用：断言主体字节完全一致；理由依据：音频不得被代理重编码或截断。
        assert RecordingHandler.body == body
    # [2026-07-04 10:18:20] 作用：清理客户端和两个服务器；理由依据：保持测试可重复运行。
    finally:
        # [2026-07-04 10:18:20] 作用：关闭 HTTP 客户端连接；理由依据：释放套接字。
        connection.close()
        # [2026-07-04 10:18:20] 作用：请求 WebUI 服务停止；理由依据：释放代理测试端口。
        proxy.shutdown()
        # [2026-07-04 10:18:20] 作用：关闭 WebUI 服务套接字；理由依据：立即回收端口资源。
        proxy.server_close()
        # [2026-07-04 10:18:20] 作用：等待 WebUI 线程退出；理由依据：避免后台线程泄漏。
        proxy_thread.join(timeout=5)
        # [2026-07-04 10:18:20] 作用：请求上游服务停止；理由依据：释放上游测试端口。
        upstream.shutdown()
        # [2026-07-04 10:18:20] 作用：关闭上游服务套接字；理由依据：立即回收端口资源。
        upstream.server_close()
        # [2026-07-04 10:18:20] 作用：等待上游线程退出；理由依据：保证测试结束后无残留进程。
        upstream_thread.join(timeout=5)
