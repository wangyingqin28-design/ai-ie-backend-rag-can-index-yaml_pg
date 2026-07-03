"""长音频转录结果必须保留实际调用模型的可审计元数据。"""

from __future__ import annotations

import importlib
from pathlib import Path

import pytest


@pytest.mark.asyncio
async def test_long_audio_result_propagates_transcription_model(
    first_runtime: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = importlib.import_module("app.ai.processors.audio_long_service")
    chunk = tmp_path / "chunk_001.wav"
    chunk.write_bytes(b"wave")
    monkeypatch.setattr(service, "split_audio", lambda **_: [chunk])

    async def fake_transcribe(_: str) -> dict[str, str]:
        return {"text": "真实转录内容", "model": "FunAudioLLM/SenseVoiceSmall"}

    monkeypatch.setattr(service, "transcribe_audio", fake_transcribe)
    result = await service.transcribe_long_audio("recording.mp3")

    assert result["model"] == "FunAudioLLM/SenseVoiceSmall"
    assert result["results"][0]["model"] == "FunAudioLLM/SenseVoiceSmall"
