# -*- coding: utf-8 -*-
"""Knowledge management static WebUI server with reserved API proxy support."""

import argparse
import json
import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Sequence
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WEBUI_DIR = Path(__file__).resolve().parent
DEFAULT_BACKEND_URL = os.environ.get("KNOWLEDGE_BACKEND_URL", "http://127.0.0.1:18290").rstrip("/")
API_PREFIX = "/api"
# [2026-07-04 10:18:20] 作用：允许代理等待十分钟完成真实音频解析和三轮 DeepSeek；理由依据：三秒会在后端正常处理期间错误中断上传。
PROXY_TIMEOUT_SECONDS = 600


class KnowledgeWebUIHandler(SimpleHTTPRequestHandler):
    backend_url = DEFAULT_BACKEND_URL

    def do_GET(self) -> None:
        if self.path == "/health":
            payload = json.dumps({"ready": True, "service": "knowledge_webui"}, ensure_ascii=False).encode("utf-8")
            self._write_response(200, "application/json; charset=utf-8", payload)
            return
        if self.path.startswith(API_PREFIX):
            self._proxy_request("GET")
            return
        if self.path == "/":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self) -> None:
        if self.path.startswith(API_PREFIX):
            self._proxy_request("POST")
            return
        self.send_error(404, "Not Found")

    def do_PUT(self) -> None:
        if self.path.startswith(API_PREFIX):
            self._proxy_request("PUT")
            return
        self.send_error(404, "Not Found")

    def do_DELETE(self) -> None:
        if self.path.startswith(API_PREFIX):
            self._proxy_request("DELETE")
            return
        self.send_error(404, "Not Found")

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _proxy_request(self, method: str) -> None:
        upstream_path = self.path[len(API_PREFIX):]
        upstream_url = f"{self.backend_url}{upstream_path}"
        content_length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(content_length) if content_length else None
        request = Request(
            upstream_url,
            data=body,
            method=method,
            headers={"Content-Type": self.headers.get("Content-Type", "application/json")},
        )
        try:
            with urlopen(request, timeout=PROXY_TIMEOUT_SECONDS) as response:
                data = response.read()
                self._write_response(response.status, response.headers.get("Content-Type", "application/json; charset=utf-8"), data)
        except HTTPError as exc:
            self._write_response(exc.code, exc.headers.get("Content-Type", "application/json; charset=utf-8"), exc.read())
        except URLError as exc:
            payload = json.dumps({"detail": f"Backend connection failed: {exc.reason}"}, ensure_ascii=False).encode("utf-8")
            self._write_response(502, "application/json; charset=utf-8", payload)
        except Exception as exc:
            payload = json.dumps({"detail": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False).encode("utf-8")
            self._write_response(500, "application/json; charset=utf-8", payload)

    def _write_response(self, status: int, content_type: str, data: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args: object) -> None:
        sys.stdout.write("[knowledge_webui] " + (format % args) + "\n")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Start Knowledge Management WebUI.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=18291)
    parser.add_argument("--backend-url", default=DEFAULT_BACKEND_URL)
    return parser


def run_webui(argv: Sequence[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    KnowledgeWebUIHandler.backend_url = str(args.backend_url).rstrip("/")
    handler = partial(KnowledgeWebUIHandler, directory=str(WEBUI_DIR))
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(json.dumps({
        "ready": True,
        "webui": f"http://{args.host}:{args.port}",
        "backend_url": KnowledgeWebUIHandler.backend_url,
        "static_dir": str(WEBUI_DIR),
    }, ensure_ascii=False, indent=2))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("knowledge_webui stopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(run_webui())
