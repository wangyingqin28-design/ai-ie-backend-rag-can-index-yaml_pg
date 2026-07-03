"""截图字段到三个 ORM 表的全量映射测试。"""

from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest


class FakeSession:
    def __init__(self) -> None:
        self.records: list[object] = []
        self.committed = False
        self.rolled_back = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        return None

    def add(self, record: object) -> None:
        self.records.append(record)

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True


def _sessionmaker_for(session: FakeSession):
    return lambda **_: lambda: session


def test_qa_save_maps_every_screenshot_field(
    second_runtime: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = importlib.import_module("app.services.ai.knowledge.qa_pair_service")
    session = FakeSession()
    monkeypatch.setattr(service, "sessionmaker", _sessionmaker_for(session))
    monkeypatch.setattr(service, "generate_uuid7_id", lambda: "qa-id")
    analysis = json.dumps(
        [{
            "question": "冷冻鸡胸怎么解冻？",
            "answer": "放入冷水中解冻",
            "question_scene": "烹饪准备",
            "description": "冷冻鸡胸解冻方法",
            "evidence": {
                "customer_text": "我想用冷冻鸡胸",
                "service_text": "建议冷水解冻",
            },
            "status": "完整",
            "time": None,
        }],
        ensure_ascii=False,
    )

    ids = service.save_qa_pairs(analysis=analysis, raw_data_id="raw-id")
    record = session.records[0]

    assert ids == ["qa-id"]
    assert session.committed is True
    assert record.Yssj_id == "raw-id"
    assert record.AI_WenTi == "冷冻鸡胸怎么解冻？"
    assert record.AI_DaAn == "放入冷水中解冻"
    assert record.AI_Biaozhu == "烹饪准备"
    assert record.WenTiYuanWen == "我想用冷冻鸡胸"
    assert record.DaAnYuanWen == "建议冷水解冻"
    assert record.WenTi_true == "冷冻鸡胸怎么解冻？"
    assert record.DaAn_true == "放入冷水中解冻"
    assert record.Biaozhu_true == "冷冻鸡胸解冻方法"
    assert record.ZhuangTai == 1


def test_intent_save_maps_intent_fields(
    second_runtime: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = importlib.import_module("app.services.ai.knowledge.intent_service")
    session = FakeSession()
    monkeypatch.setattr(service, "sessionmaker", _sessionmaker_for(session))
    monkeypatch.setattr(service, "generate_uuid7_id", lambda: "intent-id")
    analysis = json.dumps(
        [{
            "intent": "咨询解冻方法",
            "description": "用户询问食材处理",
            "evidence": "冷冻鸡胸怎么解冻",
            "time": "00:00",
        }],
        ensure_ascii=False,
    )

    ids = service.save_intents(analysis=analysis, raw_data_id="raw-id")
    record = session.records[0]

    assert ids == ["intent-id"]
    assert record.Yssj_id == "raw-id"
    assert record.AI_YiTu == "咨询解冻方法"
    assert record.YiTu == "用户询问食材处理"
    assert record.BiaoZhu == "冷冻鸡胸怎么解冻"
    assert record.ShiJian == "00:00"


def test_raw_text_is_split_and_each_chunk_keeps_source_fields(
    second_runtime: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = importlib.import_module("app.services.ai.knowledge.raw_data_service")
    session = FakeSession()
    monkeypatch.setattr(service, "sessionmaker", _sessionmaker_for(session))
    monkeypatch.setattr(service, "generate_uuid7_id", lambda: "raw-id")

    raw_id = service.save_raw_text(
        raw_text="A" * 2001,
        source_file_path="source.txt",
        source_file_name="原文.txt",
        file_type="text",
        guan_lian_ke_hu=9,
        asset_type_id="asset-id",
    )

    assert raw_id == "raw-id"
    assert len(session.records) == 2
    assert {record.shuju_id for record in session.records} == {"raw-id"}
    assert all(record.WenJianName == "原文.txt" for record in session.records)
    assert all(record.LaiYuan == 2 for record in session.records)
    assert all(record.GuanLianKeHu == 9 for record in session.records)
    assert all(record.ZcLeiXin == "asset-id" for record in session.records)
