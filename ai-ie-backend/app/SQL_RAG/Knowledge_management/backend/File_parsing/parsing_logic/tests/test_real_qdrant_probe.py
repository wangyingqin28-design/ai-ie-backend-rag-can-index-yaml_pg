"""探测源链配置的真实 Qdrant 端点并记录客观状态。"""

from __future__ import annotations

import importlib
import json
import socket
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from qdrant_client import QdrantClient


def test_configured_qdrant_endpoint_probe_is_recorded(first_runtime: Path) -> None:
    vector = importlib.import_module("app.ai.rag.vector_index_service")
    parsed = urlparse(vector.QDRANT_URL)
    report: dict[str, object] = {
        "tested_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "endpoint_host": parsed.hostname,
        "endpoint_port": parsed.port,
        "dns_resolved": False,
        "resolved_address": None,
        "tcp_connected": False,
        "connected": False,
        "collection_count": None,
        "exception_type": None,
    }

    try:
        resolved_address = socket.gethostbyname(parsed.hostname)
        report["dns_resolved"] = True
        report["resolved_address"] = resolved_address
        with socket.create_connection((resolved_address, parsed.port), timeout=5):
            report["tcp_connected"] = True
        client = QdrantClient(
            url=vector.QDRANT_URL,
            timeout=5,
            check_compatibility=False,
        )
        try:
            collections = client.get_collections().collections
            report["connected"] = True
            report["collection_count"] = len(collections)
        finally:
            client.close()
    except Exception as exc:
        report["exception_type"] = type(exc).__name__

    report_path = first_runtime.parent / "manifests/real_qdrant_probe.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    assert report["endpoint_host"] == "yulith"
    assert report_path.is_file()
