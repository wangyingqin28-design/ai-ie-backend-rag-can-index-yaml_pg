"""真实录音经硅基流动转录、DeepSeek 提取并写入三张业务表的端到端测试。"""

from __future__ import annotations

import importlib
import hashlib
import io
import json
import shutil
import time
import uuid
from datetime import datetime
from pathlib import Path

import pytest
from fastapi import UploadFile
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session


REAL_AUDIO = Path(
    r"C:\Users\DELL\Documents\WeChat Files\wxid_ahul2j69cxzm22"
    r"\FileStorage\File\2025-12"
    r"\18859060061(18859060061)_20251217154314.mp3"
)
SCREENSHOT_FIELDS = (
    "AI_WenTi",
    "AI_DaAn",
    "AI_Biaozhu",
    "WenTiYuanWen",
    "DaAnYuanWen",
    "WenTi_true",
    "DaAn_true",
    "Biaozhu_true",
)


@pytest.mark.asyncio
async def test_real_audio_runs_asr_deepseek_and_database(
    second_runtime: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """严禁用手写文本替代录音转录结果作为 DeepSeek 的输入。"""

    config = importlib.import_module("app.config")
    process_service = importlib.import_module("extraction_chain.process_service")
    models = importlib.import_module("extraction_chain.erp_ai_models")
    marker = f"codex-audio-{uuid.uuid4().hex[:12]}"
    filename = f"{marker}.mp3"
    customer_id = int(time.time())
    raw_ids: set[str] = set()
    report_path = second_runtime.parent / "manifests/live_audio_database_report.json"
    report: dict[str, object] = {
        "started_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "status": "running",
        "source_audio": str(REAL_AUDIO),
        "source_audio_bytes": REAL_AUDIO.stat().st_size,
        "ffmpeg_executable": shutil.which("ffmpeg"),
        "transcription_model": None,
        "deepseek_model": config.settings.LLM_MODEL,
        "raw_data_id": None,
        "qa_pair_ids": [],
        "intent_ids": [],
        "screenshot_field_presence": {},
        "cleanup_remaining_rows": None,
    }
    assert REAL_AUDIO.is_file()
    assert REAL_AUDIO.stat().st_size == 40704
    monkeypatch.setattr(process_service, "UPLOAD_DIR", tmp_path / "uploads")

    try:
        upload = UploadFile(filename=filename, file=io.BytesIO(REAL_AUDIO.read_bytes()))
        result = await process_service.process_uploaded_file(
            file=upload,
            action="analyze",
            mode="audio",
            export_files=False,
            output_dir=None,
            include_parse_result=True,
            asset_type_id=None,
            customer_id=customer_id,
        )
        raw_data_id = result["raw_data_id"]
        raw_ids.add(raw_data_id)
        audio_result = result["processed"]["result"]
        transcript = audio_result["text"]
        report.update(
            {
                "transcription_model": audio_result["model"],
                "transcript_length": len(transcript),
                "transcript_sha256": hashlib.sha256(
                    transcript.encode("utf-8")
                ).hexdigest(),
                "raw_data_id": raw_data_id,
                "qa_pair_ids": result["qa_pair_ids"],
                "intent_ids": result["intent_ids"],
            }
        )

        assert result["success"] is True
        assert result["processed"]["file_type"] == "audio"
        assert audio_result["model"] == "FunAudioLLM/SenseVoiceSmall"
        assert "私募证券" in transcript
        assert result["qa_pair_ids"]
        assert result["intent_ids"]

        with Session(config.sync_engine) as session:
            raw_rows = session.scalars(
                select(models.ErpYuanShiShuJu).where(
                    models.ErpYuanShiShuJu.shuju_id == raw_data_id
                )
            ).all()
            qa_rows = session.scalars(
                select(models.ErpWendaJilu).where(
                    models.ErpWendaJilu.Yssj_id == raw_data_id
                )
            ).all()
            intent_rows = session.scalars(
                select(models.ErpYitu).where(models.ErpYitu.Yssj_id == raw_data_id)
            ).all()
            presence = {
                field: any(bool(getattr(row, field)) for row in qa_rows)
                for field in SCREENSHOT_FIELDS
            }
            report["row_counts"] = {
                "AI_YuanShishuju": len(raw_rows),
                "AI_Wendajilu": len(qa_rows),
                "AI_Yitu": len(intent_rows),
            }
            report["screenshot_field_presence"] = presence

            assert raw_rows and qa_rows and intent_rows
            assert raw_rows[0].WenJianName == filename
            assert all(presence.values())
            assert any(bool(row.AI_YiTu) for row in intent_rows)
        report["status"] = "passed_before_cleanup"
    except Exception as exc:
        report["status"] = "failed"
        report["exception_type"] = type(exc).__name__
        report["exception_message"] = str(exc)
        raise
    finally:
        with Session(config.sync_engine) as session:
            if not raw_ids:
                raw_ids.update(
                    session.scalars(
                        select(models.ErpYuanShiShuJu.shuju_id).where(
                            models.ErpYuanShiShuJu.WenJianName == filename
                        )
                    ).all()
                )
            for raw_id in raw_ids:
                session.execute(
                    delete(models.ErpWendaJilu).where(
                        models.ErpWendaJilu.Yssj_id == raw_id
                    )
                )
                session.execute(
                    delete(models.ErpYitu).where(models.ErpYitu.Yssj_id == raw_id)
                )
                session.execute(
                    delete(models.ErpYuanShiShuJu).where(
                        models.ErpYuanShiShuJu.shuju_id == raw_id
                    )
                )
            session.commit()
            remaining = sum(
                session.scalar(
                    select(func.count()).select_from(table).where(column == raw_id)
                )
                for raw_id in raw_ids
                for table, column in (
                    (models.ErpYuanShiShuJu, models.ErpYuanShiShuJu.shuju_id),
                    (models.ErpWendaJilu, models.ErpWendaJilu.Yssj_id),
                    (models.ErpYitu, models.ErpYitu.Yssj_id),
                )
            )
            report["cleanup_remaining_rows"] = remaining
            if report["status"] == "passed_before_cleanup" and remaining == 0:
                report["status"] = "passed"
            report["finished_at"] = datetime.now().astimezone().isoformat(
                timespec="seconds"
            )
            report_path.write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

    assert report["status"] == "passed"
    assert report["cleanup_remaining_rows"] == 0
    assert list((tmp_path / "uploads").glob("*")) == []
