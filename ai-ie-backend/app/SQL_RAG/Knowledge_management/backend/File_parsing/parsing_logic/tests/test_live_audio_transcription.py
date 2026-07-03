"""真实录音经公共文件解析链访问硅基流动语音模型的实测。"""

from __future__ import annotations

import hashlib
import importlib
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import pytest


REAL_AUDIO = Path(
    r"C:\Users\DELL\Documents\WeChat Files\wxid_ahul2j69cxzm22"
    r"\FileStorage\File\2025-12"
    r"\18859060061(18859060061)_20251217154314.mp3"
)


@pytest.mark.asyncio
async def test_real_audio_is_transcribed_by_siliconflow(
    first_runtime: Path,
) -> None:
    entry = importlib.import_module("file_parsing_chain.entry")
    config = importlib.import_module("app.config")
    report_path = first_runtime.parent / "manifests/live_audio_transcription_report.json"

    assert REAL_AUDIO.is_file()
    audio_bytes = REAL_AUDIO.read_bytes()
    assert len(audio_bytes) == 40704
    assert audio_bytes[:2] == b"\xff\xfb"
    ffmpeg = shutil.which("ffmpeg")
    assert ffmpeg
    ffmpeg_version = subprocess.run(
        [ffmpeg, "-version"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.splitlines()[0]

    result = await entry.parse_file(str(REAL_AUDIO), mode="audio")
    audio_result = result["result"]
    transcript = audio_result["text"]
    report = {
        "tested_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source_file_sha256": hashlib.sha256(audio_bytes).hexdigest(),
        "source_file_bytes": len(audio_bytes),
        "ffmpeg_version": ffmpeg_version,
        "siliconflow_host": urlparse(
            config.settings.embedding_service_url
        ).hostname,
        "transcription_model": audio_result["model"],
        "chunk_count": audio_result["chunk_count"],
        "transcript_length": len(transcript),
        "transcript_sha256": hashlib.sha256(
            transcript.encode("utf-8")
        ).hexdigest(),
        "success": result["success"],
    }
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    assert result["success"] is True
    assert result["file_type"] == "audio"
    assert result["engine"] == "audio_asr_long"
    assert transcript.strip()
    assert audio_result["model"] == "FunAudioLLM/SenseVoiceSmall"
    assert report["siliconflow_host"] == "api.siliconflow.cn"
