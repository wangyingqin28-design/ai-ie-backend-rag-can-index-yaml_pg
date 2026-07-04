# -*- coding: utf-8 -*-
# [2026-07-04 10:18:20] 作用：执行本行代码 `"""Knowledge management static WebUI server with reserved API proxy support."""`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
"""Knowledge management static WebUI server with reserved API proxy support."""

# [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `import argparse`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
import argparse
# [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `import json`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
import json
# [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `import os`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
import os
# [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `import sys`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
import sys
# [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `from functools import partial`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
from functools import partial
# [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
# [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `from pathlib import Path`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
from pathlib import Path
# [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `from typing import Sequence`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
from typing import Sequence
# [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `from urllib.error import HTTPError, URLError`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
from urllib.error import HTTPError, URLError
# [2026-07-04 10:18:20] 作用：导入或组合本行依赖 `from urllib.request import Request, urlopen`；理由依据：该依赖直接支持知识库真实上传、代理或回归测试。
from urllib.request import Request, urlopen

# [2026-07-04 10:18:20] 作用：按条件 `if hasattr(sys.stdout, "reconfigure"):` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
if hasattr(sys.stdout, "reconfigure"):
    # [2026-07-04 10:18:20] 作用：为 `sys.stdout.reconfigure(encoding` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    sys.stdout.reconfigure(encoding="utf-8")

# [2026-07-04 10:18:20] 作用：为 `WEBUI_DIR` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
WEBUI_DIR = Path(__file__).resolve().parent
# [2026-07-04 10:18:20] 作用：为 `DEFAULT_BACKEND_URL` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
DEFAULT_BACKEND_URL = os.environ.get("KNOWLEDGE_BACKEND_URL", "http://127.0.0.1:18290").rstrip("/")
# [2026-07-04 10:18:20] 作用：为 `API_PREFIX` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
API_PREFIX = "/api"
# [2026-07-04 10:18:20] 作用：为 `PROXY_TIMEOUT_SECONDS` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
PROXY_TIMEOUT_SECONDS = 600


# [2026-07-04 10:18:20] 作用：声明 `KnowledgeWebUIHandler` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
class KnowledgeWebUIHandler(SimpleHTTPRequestHandler):
    # [2026-07-04 10:18:20] 作用：为 `backend_url` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    backend_url = DEFAULT_BACKEND_URL

    # [2026-07-04 10:18:20] 作用：声明 `do_GET` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
    def do_GET(self) -> None:
        # [2026-07-04 10:18:20] 作用：按条件 `if self.path == "/health":` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
        if self.path == "/health":
            # [2026-07-04 10:18:20] 作用：为 `payload` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
            payload = json.dumps({"ready": True, "service": "knowledge_webui"}, ensure_ascii=False).encode("utf-8")
            # [2026-07-04 10:18:20] 作用：为 `self._write_response(200, "application/json; charset` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
            self._write_response(200, "application/json; charset=utf-8", payload)
            # [2026-07-04 10:18:20] 作用：执行控制结果 `return`；理由依据：调用方必须获得明确返回值或可诊断失败。
            return
        # [2026-07-04 10:18:20] 作用：按条件 `if self.path.startswith(API_PREFIX):` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
        if self.path.startswith(API_PREFIX):
            # [2026-07-04 10:18:20] 作用：执行本行代码 `self._proxy_request("GET")`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
            self._proxy_request("GET")
            # [2026-07-04 10:18:20] 作用：执行控制结果 `return`；理由依据：调用方必须获得明确返回值或可诊断失败。
            return
        # [2026-07-04 10:18:20] 作用：按条件 `if self.path == "/":` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
        if self.path == "/":
            # [2026-07-04 10:18:20] 作用：为 `self.path` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
            self.path = "/index.html"
        # [2026-07-04 10:18:20] 作用：执行本行代码 `super().do_GET()`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        super().do_GET()

    # [2026-07-04 10:18:20] 作用：声明 `do_POST` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
    def do_POST(self) -> None:
        # [2026-07-04 10:18:20] 作用：按条件 `if self.path.startswith(API_PREFIX):` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
        if self.path.startswith(API_PREFIX):
            # [2026-07-04 10:18:20] 作用：执行本行代码 `self._proxy_request("POST")`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
            self._proxy_request("POST")
            # [2026-07-04 10:18:20] 作用：执行控制结果 `return`；理由依据：调用方必须获得明确返回值或可诊断失败。
            return
        # [2026-07-04 10:18:20] 作用：执行本行代码 `self.send_error(404, "Not Found")`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        self.send_error(404, "Not Found")

    # [2026-07-04 10:18:20] 作用：声明 `do_PUT` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
    def do_PUT(self) -> None:
        # [2026-07-04 10:18:20] 作用：按条件 `if self.path.startswith(API_PREFIX):` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
        if self.path.startswith(API_PREFIX):
            # [2026-07-04 10:18:20] 作用：执行本行代码 `self._proxy_request("PUT")`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
            self._proxy_request("PUT")
            # [2026-07-04 10:18:20] 作用：执行控制结果 `return`；理由依据：调用方必须获得明确返回值或可诊断失败。
            return
        # [2026-07-04 10:18:20] 作用：执行本行代码 `self.send_error(404, "Not Found")`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        self.send_error(404, "Not Found")

    # [2026-07-04 10:18:20] 作用：声明 `do_DELETE` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
    def do_DELETE(self) -> None:
        # [2026-07-04 10:18:20] 作用：按条件 `if self.path.startswith(API_PREFIX):` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
        if self.path.startswith(API_PREFIX):
            # [2026-07-04 10:18:20] 作用：执行本行代码 `self._proxy_request("DELETE")`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
            self._proxy_request("DELETE")
            # [2026-07-04 10:18:20] 作用：执行控制结果 `return`；理由依据：调用方必须获得明确返回值或可诊断失败。
            return
        # [2026-07-04 10:18:20] 作用：执行本行代码 `self.send_error(404, "Not Found")`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        self.send_error(404, "Not Found")

    # [2026-07-04 10:18:20] 作用：声明 `end_headers` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
    def end_headers(self) -> None:
        # [2026-07-04 10:18:20] 作用：执行本行代码 `self.send_header("Cache-Control", "no-store")`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        self.send_header("Cache-Control", "no-store")
        # [2026-07-04 10:18:20] 作用：执行本行代码 `super().end_headers()`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        super().end_headers()

    # [2026-07-04 10:18:20] 作用：声明 `_proxy_request` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
    def _proxy_request(self, method: str) -> None:
        # [2026-07-04 10:18:20] 作用：为 `upstream_path` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
        upstream_path = self.path[len(API_PREFIX):]
        # [2026-07-04 10:18:20] 作用：为 `upstream_url` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
        upstream_url = f"{self.backend_url}{upstream_path}"
        # [2026-07-04 10:18:20] 作用：为 `content_length` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
        content_length = int(self.headers.get("Content-Length", "0") or "0")
        # [2026-07-04 10:18:20] 作用：为 `body` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
        body = self.rfile.read(content_length) if content_length else None
        # [2026-07-04 10:18:20] 作用：为 `request` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
        request = Request(
            # [2026-07-04 10:18:20] 作用：执行本行代码 `upstream_url,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
            upstream_url,
            # [2026-07-04 10:18:20] 作用：为 `data` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
            data=body,
            # [2026-07-04 10:18:20] 作用：为 `method` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
            method=method,
            # [2026-07-04 10:18:20] 作用：为 `headers` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
            headers={"Content-Type": self.headers.get("Content-Type", "application/json")},
        # [2026-07-04 10:18:20] 作用：执行本行代码 `)`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        )
        # [2026-07-04 10:18:20] 作用：进入异常控制片段 `try:`；理由依据：真实网络、模型和数据库调用必须正确传播并清理异常状态。
        try:
            # [2026-07-04 10:18:20] 作用：为 `with urlopen(request, timeout` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
            with urlopen(request, timeout=PROXY_TIMEOUT_SECONDS) as response:
                # [2026-07-04 10:18:20] 作用：为 `data` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
                data = response.read()
                # [2026-07-04 10:18:20] 作用：执行本行代码 `self._write_response(response.status, response.headers.get("Content-Type", "application/`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
                self._write_response(response.status, response.headers.get("Content-Type", "application/json; charset=utf-8"), data)
        # [2026-07-04 10:18:20] 作用：进入异常控制片段 `except HTTPError as exc:`；理由依据：真实网络、模型和数据库调用必须正确传播并清理异常状态。
        except HTTPError as exc:
            # [2026-07-04 10:18:20] 作用：执行本行代码 `self._write_response(exc.code, exc.headers.get("Content-Type", "application/json; charse`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
            self._write_response(exc.code, exc.headers.get("Content-Type", "application/json; charset=utf-8"), exc.read())
        # [2026-07-04 10:18:20] 作用：进入异常控制片段 `except URLError as exc:`；理由依据：真实网络、模型和数据库调用必须正确传播并清理异常状态。
        except URLError as exc:
            # [2026-07-04 10:18:20] 作用：为 `payload` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
            payload = json.dumps({"detail": f"Backend connection failed: {exc.reason}"}, ensure_ascii=False).encode("utf-8")
            # [2026-07-04 10:18:20] 作用：为 `self._write_response(502, "application/json; charset` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
            self._write_response(502, "application/json; charset=utf-8", payload)
        # [2026-07-04 10:18:20] 作用：进入异常控制片段 `except Exception as exc:`；理由依据：真实网络、模型和数据库调用必须正确传播并清理异常状态。
        except Exception as exc:
            # [2026-07-04 10:18:20] 作用：为 `payload` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
            payload = json.dumps({"detail": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False).encode("utf-8")
            # [2026-07-04 10:18:20] 作用：为 `self._write_response(500, "application/json; charset` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
            self._write_response(500, "application/json; charset=utf-8", payload)

    # [2026-07-04 10:18:20] 作用：声明 `_write_response` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
    def _write_response(self, status: int, content_type: str, data: bytes) -> None:
        # [2026-07-04 10:18:20] 作用：执行本行代码 `self.send_response(status)`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        self.send_response(status)
        # [2026-07-04 10:18:20] 作用：执行本行代码 `self.send_header("Content-Type", content_type)`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        self.send_header("Content-Type", content_type)
        # [2026-07-04 10:18:20] 作用：执行本行代码 `self.send_header("Content-Length", str(len(data)))`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        self.send_header("Content-Length", str(len(data)))
        # [2026-07-04 10:18:20] 作用：执行本行代码 `self.end_headers()`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        self.end_headers()
        # [2026-07-04 10:18:20] 作用：执行本行代码 `self.wfile.write(data)`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        self.wfile.write(data)

    # [2026-07-04 10:18:20] 作用：声明 `log_message` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
    def log_message(self, format: str, *args: object) -> None:
        # [2026-07-04 10:18:20] 作用：执行本行代码 `sys.stdout.write("[knowledge_webui] " + (format % args) + "\n")`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        sys.stdout.write("[knowledge_webui] " + (format % args) + "\n")


# [2026-07-04 10:18:20] 作用：声明 `build_arg_parser` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
def build_arg_parser() -> argparse.ArgumentParser:
    # [2026-07-04 10:18:20] 作用：为 `parser` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    parser = argparse.ArgumentParser(description="Start Knowledge Management WebUI.")
    # [2026-07-04 10:18:20] 作用：为 `parser.add_argument("--host", default` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    parser.add_argument("--host", default="127.0.0.1")
    # [2026-07-04 10:18:20] 作用：为 `parser.add_argument("--port", type` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    parser.add_argument("--port", type=int, default=18291)
    # [2026-07-04 10:18:20] 作用：为 `parser.add_argument("--backend-url", default` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    parser.add_argument("--backend-url", default=DEFAULT_BACKEND_URL)
    # [2026-07-04 10:18:20] 作用：执行控制结果 `return parser`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return parser


# [2026-07-04 10:18:20] 作用：声明 `run_webui` 处理节点；理由依据：该节点属于已跑通的知识库前后端执行链。
def run_webui(argv: Sequence[str] | None = None) -> int:
    # [2026-07-04 10:18:20] 作用：为 `parser` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    parser = build_arg_parser()
    # [2026-07-04 10:18:20] 作用：为 `args` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    args = parser.parse_args(list(argv) if argv is not None else None)
    # [2026-07-04 10:18:20] 作用：为 `KnowledgeWebUIHandler.backend_url` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    KnowledgeWebUIHandler.backend_url = str(args.backend_url).rstrip("/")
    # [2026-07-04 10:18:20] 作用：为 `handler` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    handler = partial(KnowledgeWebUIHandler, directory=str(WEBUI_DIR))
    # [2026-07-04 10:18:20] 作用：为 `server` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    server = ThreadingHTTPServer((args.host, args.port), handler)
    # [2026-07-04 10:18:20] 作用：执行本行代码 `print(json.dumps({`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
    print(json.dumps({
        # [2026-07-04 10:18:20] 作用：执行本行代码 `"ready": True,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        "ready": True,
        # [2026-07-04 10:18:20] 作用：执行本行代码 `"webui": f"http://{args.host}:{args.port}",`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        "webui": f"http://{args.host}:{args.port}",
        # [2026-07-04 10:18:20] 作用：执行本行代码 `"backend_url": KnowledgeWebUIHandler.backend_url,`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        "backend_url": KnowledgeWebUIHandler.backend_url,
        # [2026-07-04 10:18:20] 作用：执行本行代码 `"static_dir": str(WEBUI_DIR),`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        "static_dir": str(WEBUI_DIR),
    # [2026-07-04 10:18:20] 作用：为 `}, ensure_ascii` 计算并保存本行结果；理由依据：后续上传、页面状态、代理或断言复用该确定值。
    }, ensure_ascii=False, indent=2))
    # [2026-07-04 10:18:20] 作用：进入异常控制片段 `try:`；理由依据：真实网络、模型和数据库调用必须正确传播并清理异常状态。
    try:
        # [2026-07-04 10:18:20] 作用：执行本行代码 `server.serve_forever()`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        server.serve_forever()
    # [2026-07-04 10:18:20] 作用：进入异常控制片段 `except KeyboardInterrupt:`；理由依据：真实网络、模型和数据库调用必须正确传播并清理异常状态。
    except KeyboardInterrupt:
        # [2026-07-04 10:18:20] 作用：执行本行代码 `print("knowledge_webui stopped.")`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        print("knowledge_webui stopped.")
    # [2026-07-04 10:18:20] 作用：进入异常控制片段 `finally:`；理由依据：真实网络、模型和数据库调用必须正确传播并清理异常状态。
    finally:
        # [2026-07-04 10:18:20] 作用：执行本行代码 `server.server_close()`；理由依据：本行是知识库真实前后端链路或其回归验证的必要步骤。
        server.server_close()
    # [2026-07-04 10:18:20] 作用：执行控制结果 `return 0`；理由依据：调用方必须获得明确返回值或可诊断失败。
    return 0


# [2026-07-04 10:18:20] 作用：按条件 `if __name__ == "__main__":` 选择执行分支；理由依据：必须显式处理成功、失败或可选输入以避免伪成功。
if __name__ == "__main__":
    # [2026-07-04 10:18:20] 作用：执行控制结果 `raise SystemExit(run_webui())`；理由依据：调用方必须获得明确返回值或可诊断失败。
    raise SystemExit(run_webui())
