"""三套提示词与上传总调度链的隔离测试。"""

from __future__ import annotations

import importlib
import io
import json
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from fastapi import UploadFile


@pytest.mark.asyncio
async def test_three_prompt_pipeline_merges_description_and_intent(
    second_runtime: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    extraction = importlib.import_module(
        "app.services.ai.extraction.audio_knowledge_extract_service"
    )
    responses = iter(
        [
            json.dumps(
                [{"question": "怎么操作？", "answer": "按步骤操作", "status": "完整"}],
                ensure_ascii=False,
            ),
            json.dumps(
                [{"question": "怎么操作？", "description": "操作指导"}],
                ensure_ascii=False,
            ),
            json.dumps(
                [{"intent": "咨询操作", "description": "用户需要操作指导"}],
                ensure_ascii=False,
            ),
        ]
    )
    calls: list[str] = []

    async def fake_llm(prompt: str, *, system_prompt: str, **_: object) -> str:
        calls.append(system_prompt)
        return next(responses)

    monkeypatch.setattr(extraction, "llm_model_func", fake_llm)
    result = await extraction.extract_audio_knowledge("客户询问怎么操作")

    qa_items = json.loads(result["qa_analysis"])
    assert len(calls) == 3
    assert qa_items[0]["description"] == "操作指导"
    assert result["description_items"][0]["description"] == "操作指导"
    assert result["intent_items"][0]["intent"] == "咨询操作"


@pytest.mark.asyncio
async def test_uploaded_file_runs_parse_raw_save_analysis_and_export_in_order(
    second_runtime: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    process_service = importlib.import_module("app.services.ai.extraction.process_service")
    raw_service = importlib.import_module("app.services.ai.knowledge.raw_data_service")
    events: list[str] = []
    monkeypatch.setattr(process_service, "UPLOAD_DIR", tmp_path / "uploads")
    monkeypatch.setattr(process_service, "DEFAULT_OUTPUT_DIR", tmp_path / "outputs")

    async def fake_process_file(**_: object) -> dict[str, object]:
        events.append("parse")
        return {
            "success": True,
            "file_name": "temp.txt",
            "file_type": "text",
            "engine": "text",
            "mode": "auto",
            "result": {"text": "测试原文"},
        }

    def fake_save_raw_text(**_: object) -> str:
        events.append("raw_save")
        return "raw-id"

    async def fake_extract(**_: object):
        events.append("analysis")
        return (
            {"qa_analysis": "qa", "intent_analysis": "intent"},
            "qa",
            "intent",
            [{"description": "desc"}],
            ["qa-id"],
            ["intent-id"],
        )

    async def fake_export(**_: object) -> dict[str, str]:
        events.append("export")
        return {"raw_output_file": "raw.md"}

    monkeypatch.setattr(process_service, "process_file", fake_process_file)
    monkeypatch.setattr(raw_service, "save_raw_text", fake_save_raw_text)
    monkeypatch.setattr(process_service, "_run_fixed_audio_knowledge_extract", fake_extract)
    monkeypatch.setattr(process_service, "export_knowledge_extract_result", fake_export)
    upload = UploadFile(filename="source.txt", file=io.BytesIO("测试原文".encode()))

    result = await process_service.process_uploaded_file(
        file=upload,
        action="both",
        mode="auto",
        export_files=True,
        output_dir=None,
        include_parse_result=True,
        asset_type_id="asset-id",
        customer_id=7,
    )

    assert events == ["parse", "raw_save", "analysis", "export"]
    assert result["raw_data_id"] == "raw-id"
    assert result["qa_pair_ids"] == ["qa-id"]
    assert result["intent_ids"] == ["intent-id"]
    assert result["processed"]["result"]["text"] == "测试原文"
    assert list((tmp_path / "uploads").glob("*")) == []
