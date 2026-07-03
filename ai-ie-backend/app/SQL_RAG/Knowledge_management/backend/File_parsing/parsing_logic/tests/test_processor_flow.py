"""processor.py 文件分发、批处理、导出和索引项转换测试。"""

from __future__ import annotations

import importlib
from pathlib import Path
from unittest.mock import AsyncMock

import pytest


@pytest.mark.asyncio
async def test_business_facade_delegates_to_the_single_public_processor(
    first_runtime: Path,
    tmp_path: Path,
) -> None:
    entry = importlib.import_module("file_parsing_chain.entry")
    source = tmp_path / "facade.txt"
    source.write_text("薄入口调用公共解析器", encoding="utf-8")

    result = await entry.parse_file(str(source))
    item = entry.to_index_item(result)

    assert result["engine"] == "text"
    assert item["text"] == "薄入口调用公共解析器"


@pytest.mark.asyncio
async def test_text_file_runs_real_validation_and_text_reader(
    first_runtime: Path,
    tmp_path: Path,
) -> None:
    processor = importlib.import_module("app.ai.processors.processor")
    source = tmp_path / "sample.txt"
    source.write_text("测试文本内容", encoding="utf-8")

    result = await processor.process_file(str(source), mode="auto")

    assert result["success"] is True
    assert result["file_type"] == "text"
    assert result["engine"] == "text"
    assert result["result"]["text"] == "测试文本内容"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("suffix", "mode", "patched_name", "patched_result", "expected_engine"),
    [
        (".png", "auto", "recognize_image", "视觉描述", "vision"),
        (".png", "ocr", "ocr_image", "图片文字", "vision_ocr"),
        (".pdf", "auto", "process_document_file", {"markdown": "文档正文"}, "docling"),
        (".pdf", "ocr", "process_document_file", {"markdown": "扫描正文"}, "docling_ocr"),
        (".wav", "audio", "transcribe_long_audio", {"text": "音频正文"}, "audio_asr_long"),
    ],
)
async def test_dispatches_every_external_file_branch(
    first_runtime: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    suffix: str,
    mode: str,
    patched_name: str,
    patched_result: object,
    expected_engine: str,
) -> None:
    processor = importlib.import_module("app.ai.processors.processor")
    source = tmp_path / f"sample{suffix}"
    source.write_bytes(b"test")
    boundary = AsyncMock(return_value=patched_result)
    monkeypatch.setattr(processor, patched_name, boundary)

    result = await processor.process_file(str(source), mode=mode)

    assert result["success"] is True
    assert result["engine"] == expected_engine
    boundary.assert_awaited_once()
    if suffix == ".pdf":
        assert result["parse_method"] == ("ocr" if mode == "ocr" else "auto")


@pytest.mark.asyncio
async def test_unsupported_file_returns_structured_failure(
    first_runtime: Path,
    tmp_path: Path,
) -> None:
    processor = importlib.import_module("app.ai.processors.processor")
    source = tmp_path / "sample.bin"
    source.write_bytes(b"binary")

    result = await processor.process_file(str(source))

    assert result == {
        "success": False,
        "file_path": str(source),
        "file_name": "sample.bin",
        "file_type": "unsupported",
        "engine": "unsupported",
        "mode": "auto",
        "error": "Unsupported file type",
    }


@pytest.mark.asyncio
async def test_folder_processing_isolates_single_file_failure(
    first_runtime: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    processor = importlib.import_module("app.ai.processors.processor")
    (tmp_path / "good.txt").write_text("good", encoding="utf-8")
    (tmp_path / "bad.txt").write_text("bad", encoding="utf-8")

    async def fake_process_file(*, file_path: str, **_: object) -> dict[str, object]:
        if file_path.endswith("bad.txt"):
            raise RuntimeError("单文件失败")
        return {"success": True, "file_path": file_path}

    monkeypatch.setattr(processor, "process_file", fake_process_file)
    result = await processor.process_folder(str(tmp_path))

    assert result["success"] is True
    assert result["total"] == 2
    assert len([item for item in result["results"] if item["success"]]) == 1
    failures = [item for item in result["results"] if not item["success"]]
    assert failures[0]["error"] == "单文件失败"


@pytest.mark.asyncio
async def test_export_branch_creates_raw_and_summary_files(
    first_runtime: Path,
    tmp_path: Path,
) -> None:
    processor = importlib.import_module("app.ai.processors.processor")
    source = tmp_path / "export.txt"
    source.write_text("需要导出的原文", encoding="utf-8")
    output = tmp_path / "exports"

    result = await processor.process_file(
        str(source),
        export=True,
        output_dir=str(output),
    )

    assert Path(result["exports"]["raw_output_file"]).is_file()
    assert Path(result["exports"]["summary_output_file"]).is_file()


def test_to_index_item_covers_document_text_audio_image_and_fallback(
    first_runtime: Path,
) -> None:
    processor = importlib.import_module("app.ai.processors.processor")

    document = processor.to_index_item(
        {"file_type": "document", "result": {"markdown": "md"}}
    )
    text = processor.to_index_item(
        {"file_type": "text", "result": {"text": "plain"}}
    )
    audio = processor.to_index_item(
        {"file_type": "audio", "result": {"text": "voice"}}
    )
    image = processor.to_index_item({"file_type": "image", "result": "vision"})
    fallback = processor.to_index_item({"file_type": "unsupported", "result": None})

    assert document["markdown"] == "md"
    assert text["text"] == "plain"
    assert audio["text"] == "voice"
    assert image["text"] == "vision"
    assert fallback["text"] == ""
