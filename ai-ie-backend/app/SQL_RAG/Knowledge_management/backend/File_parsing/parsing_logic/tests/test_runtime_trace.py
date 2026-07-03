"""第一条链核心纯本地路径的运行时调用轨迹测试。"""

from __future__ import annotations

import asyncio
import importlib
import json
import sys
from pathlib import Path


REQUIRED_LOCAL_CALLS = {
    "app.ai.processors.processor.process_file",
    "app.ai.processors.processor.process_folder",
    "app.ai.processors.processor.to_index_item",
    "app.ai.processors.file_utils.validate_file",
    "app.ai.processors.file_utils.get_file_type",
    "app.ai.processors.file_utils.get_supported_files",
    "app.ai.processors.document_service.process_text_file",
}


def test_runtime_trace_records_core_local_execution_order(
    first_runtime: Path,
    tmp_path: Path,
) -> None:
    processor = importlib.import_module("app.ai.processors.processor")
    (tmp_path / "trace.txt").write_text("调用轨迹", encoding="utf-8")
    calls: list[str] = []

    def profiler(frame, event: str, _argument):
        if event != "call":
            return profiler
        module = frame.f_globals.get("__name__", "")
        if module.startswith("app."):
            calls.append(f"{module}.{frame.f_code.co_name}")
        return profiler

    sys.setprofile(profiler)
    try:
        processed = asyncio.run(processor.process_file(str(tmp_path / "trace.txt")))
        processor.to_index_item(processed)
        asyncio.run(processor.process_folder(str(tmp_path)))
    finally:
        sys.setprofile(None)

    assert REQUIRED_LOCAL_CALLS <= set(calls)
    chain_root = first_runtime.parent
    manifest = json.loads(
        (chain_root / "manifests/definitions.json").read_text(encoding="utf-8")
    )
    report = {
        "chain": "文件解析链",
        "generated_at": manifest["generated_at"],
        "ordered_calls": calls,
        "required_calls": sorted(REQUIRED_LOCAL_CALLS),
        "missing_required_calls": sorted(REQUIRED_LOCAL_CALLS - set(calls)),
    }
    (chain_root / "manifests/runtime_trace.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
