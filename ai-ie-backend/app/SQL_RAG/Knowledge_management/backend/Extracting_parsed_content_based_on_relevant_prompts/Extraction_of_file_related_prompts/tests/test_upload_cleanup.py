"""上传流程异常时仍删除临时文件的回归测试。"""

from __future__ import annotations

import importlib
import io
from pathlib import Path

import pytest
from fastapi import UploadFile


@pytest.mark.asyncio
async def test_temporary_upload_is_removed_when_parser_raises(
    second_runtime: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = importlib.import_module("app.services.ai.extraction.process_service")
    upload_dir = tmp_path / "uploads"
    monkeypatch.setattr(service, "UPLOAD_DIR", upload_dir)

    async def failing_parser(**_: object):
        raise RuntimeError("解析失败")

    monkeypatch.setattr(service, "process_file", failing_parser)
    upload = UploadFile(filename="source.txt", file=io.BytesIO(b"content"))

    with pytest.raises(RuntimeError, match="解析失败"):
        await service.process_uploaded_file(
            file=upload,
            action="parse",
            mode="auto",
            export_files=False,
            output_dir=None,
            include_parse_result=False,
        )

    assert list(upload_dir.glob("*")) == []
