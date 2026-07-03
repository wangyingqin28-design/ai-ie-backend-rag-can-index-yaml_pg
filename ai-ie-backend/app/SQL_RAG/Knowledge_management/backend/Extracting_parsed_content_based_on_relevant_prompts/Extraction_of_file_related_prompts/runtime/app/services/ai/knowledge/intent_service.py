# [2026-07-03 14:26:28] 中文迁移说明：本文件完整复制自 app/services/ai/knowledge/intent_service.py；纳入依据为 DeepSeek 提取入库链 的项目内传递依赖闭包。
import json
import re
from datetime import datetime
from json import JSONDecodeError
from typing import Any

from sqlalchemy.orm import Session, sessionmaker

from app.config import sync_engine
from app.models.erp_ai_models import ErpYitu
from app.utils.snowflake_generator import generate_uuid7_id


def _strip_markdown_fence(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def parse_ai_intent_result(analysis: str) -> list[dict[str, Any]]:
    if not analysis:
        return []

    text = _strip_markdown_fence(analysis)

    try:
        data = json.loads(text)
    except JSONDecodeError:
        decoder = json.JSONDecoder()
        start_positions = [pos for pos in (text.find("["), text.find("{")) if pos != -1]
        if not start_positions:
            return []

        start = min(start_positions)
        try:
            data, _ = decoder.raw_decode(text[start:])
        except JSONDecodeError:
            return []

    if isinstance(data, dict):
        data = [data]

    if not isinstance(data, list):
        return []

    return [item for item in data if isinstance(item, dict)]


def _status_to_int(value: Any) -> int:
    if value is None:
        return 0

    if isinstance(value, int):
        return value

    mapping = {
        "待审核": 0,
        "完整": 1,
        "部分完整": 2,
        "不完整": 3,
        "未明确": 4,
        "在用": 1,
        "弃用": 2,
    }

    return mapping.get(str(value).strip(), 0)


def save_intents(
    *,
    analysis: str,
    raw_data_id: str | None = None,
    source_file_path: str | None = None,
    file_type: str | None = None,
    gs_id: str | None = None,
    in_userid: str | None = None,
) -> list[str]:
    intent_items = parse_ai_intent_result(analysis)
    if not intent_items:
        return []

    if not raw_data_id:
        return []

    SessionLocal = sessionmaker(
        bind=sync_engine,
        class_=Session,
        expire_on_commit=False,
    )

    saved_ids: list[str] = []

    with SessionLocal() as db:
        try:
            for item in intent_items:
                intent_id = generate_uuid7_id()

                record = ErpYitu(
                    yt_id=intent_id,
                    Yssj_id=raw_data_id,

                    AI_YiTu=item.get("intent"),
                    YiTu=item.get("description"),
                    BiaoZhu=item.get("evidence"),

                    ZhuangTai=0,
                    ZhuangTai_id=None,
                    ZhuangTai_time=None,
                    ShiJian=item.get("time"),

                    gsId=gs_id,
                    del_time=None,
                    in_userid=in_userid,
                    in_time=datetime.now(),
                )

                db.add(record)
                saved_ids.append(intent_id)

            db.commit()
            return saved_ids

        except Exception:
            db.rollback()
            raise