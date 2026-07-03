"""目标镜像访问真实硅基流动 DeepSeek 与 PostgreSQL 的端到端测试。"""

from __future__ import annotations

import importlib
import io
import json
import time
import uuid
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import pytest
from fastapi import UploadFile
from sqlalchemy import delete, func, select, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session


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
async def test_copied_pipeline_uses_live_deepseek_and_persists_screenshot_fields(
    second_runtime: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_module = importlib.import_module("app.config")
    process_service = importlib.import_module("extraction_chain.process_service")
    models = importlib.import_module("extraction_chain.erp_ai_models")
    marker = f"codex-live-{uuid.uuid4().hex[:12]}"
    filename = f"{marker}.txt"
    customer_id = int(time.time())
    raw_ids: set[str] = set()
    report_path = second_runtime.parent / "manifests/live_test_report.json"
    endpoint_host = urlparse(config_module.settings.embedding_service_url).hostname
    database_host = make_url(config_module.settings.database_url).host
    report: dict[str, object] = {
        "started_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "status": "running",
        "target_runtime": str(second_runtime),
        "model": config_module.settings.LLM_MODEL,
        "api_endpoint_host": endpoint_host,
        "database_host": database_host,
        "api_key_present": bool(config_module.settings.embedding_service_api_key),
        "marker": marker,
        "generated_ids": {},
        "row_counts": {},
        "field_presence": {},
        "cleanup_counts": {},
    }

    assert report["api_key_present"] is True
    assert endpoint_host == "api.siliconflow.cn"
    assert "deepseek" in config_module.settings.LLM_MODEL.lower()
    monkeypatch.setattr(process_service, "UPLOAD_DIR", tmp_path / "uploads")

    with config_module.sync_engine.connect() as connection:
        assert connection.execute(text("SELECT 1")).scalar_one() == 1

    upload_text = (
        f"测试标记：{marker}。\n"
        "客户原话：冷冻鸡胸应该怎样快速且安全地解冻？\n"
        "服务人员原话：把密封的冷冻鸡胸放入冷水中，每三十分钟换一次水，"
        "完全解冻后立即烹饪，不要使用热水。\n"
        "标准问题：冷冻鸡胸如何安全解冻？\n"
        "标准答案：密封后冷水浸泡并定时换水，解冻后立即烹饪。\n"
        "用户意图：咨询冷冻鸡胸的安全解冻方法。"
    )
    upload = UploadFile(filename=filename, file=io.BytesIO(upload_text.encode("utf-8")))

    try:
        result = await process_service.process_uploaded_file(
            file=upload,
            action="analyze",
            mode="auto",
            export_files=False,
            output_dir=None,
            include_parse_result=True,
            asset_type_id=None,
            customer_id=customer_id,
        )
        raw_data_id = result["raw_data_id"]
        raw_ids.add(raw_data_id)
        report["generated_ids"] = {
            "raw_data_id": raw_data_id,
            "qa_pair_ids": result["qa_pair_ids"],
            "intent_ids": result["intent_ids"],
        }
        assert result["success"] is True
        assert result["processed"]["result"]["text"] == upload_text
        assert result["qa_pair_ids"]
        assert result["intent_ids"]

        with Session(config_module.sync_engine) as session:
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

            report["row_counts"] = {
                "AI_YuanShishuju": len(raw_rows),
                "AI_Wendajilu": len(qa_rows),
                "AI_Yitu": len(intent_rows),
            }
            assert len(raw_rows) == 1
            assert qa_rows
            assert intent_rows
            assert raw_rows[0].WenJianName == filename
            assert str(raw_rows[0].GuanLianKeHu) == str(customer_id)
            assert all(row.Yssj_id == raw_data_id for row in qa_rows)
            assert all(row.Yssj_id == raw_data_id for row in intent_rows)

            field_presence = {
                field: any(bool(getattr(row, field)) for row in qa_rows)
                for field in SCREENSHOT_FIELDS
            }
            report["field_presence"] = field_presence
            assert all(field_presence.values())
            assert any(bool(row.AI_YiTu) for row in intent_rows)
            assert any(bool(row.YiTu) for row in intent_rows)
            assert any(bool(row.BiaoZhu) for row in intent_rows)

        report["status"] = "passed_before_cleanup"
    except Exception as exc:
        report["status"] = "failed"
        report["exception_type"] = type(exc).__name__
        raise
    finally:
        with Session(config_module.sync_engine) as session:
            if not raw_ids:
                raw_ids.update(
                    session.scalars(
                        select(models.ErpYuanShiShuJu.shuju_id).where(
                            models.ErpYuanShiShuJu.WenJianName == filename
                        )
                    ).all()
                )
            deleted_qa = deleted_intent = deleted_raw = 0
            for raw_id in raw_ids:
                deleted_qa += session.execute(
                    delete(models.ErpWendaJilu).where(
                        models.ErpWendaJilu.Yssj_id == raw_id
                    )
                ).rowcount
                deleted_intent += session.execute(
                    delete(models.ErpYitu).where(models.ErpYitu.Yssj_id == raw_id)
                ).rowcount
                deleted_raw += session.execute(
                    delete(models.ErpYuanShiShuJu).where(
                        models.ErpYuanShiShuJu.shuju_id == raw_id
                    )
                ).rowcount
            session.commit()
            remaining = 0
            for raw_id in raw_ids:
                remaining += session.scalar(
                    select(func.count()).select_from(models.ErpYuanShiShuJu).where(
                        models.ErpYuanShiShuJu.shuju_id == raw_id
                    )
                )
                remaining += session.scalar(
                    select(func.count()).select_from(models.ErpWendaJilu).where(
                        models.ErpWendaJilu.Yssj_id == raw_id
                    )
                )
                remaining += session.scalar(
                    select(func.count()).select_from(models.ErpYitu).where(
                        models.ErpYitu.Yssj_id == raw_id
                    )
                )
            report["cleanup_counts"] = {
                "AI_Wendajilu": deleted_qa,
                "AI_Yitu": deleted_intent,
                "AI_YuanShishuju": deleted_raw,
                "remaining_rows": remaining,
            }
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
    assert report["cleanup_counts"]["remaining_rows"] == 0
    assert list((tmp_path / "uploads").glob("*")) == []
