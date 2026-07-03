# [2026-07-03 14:26:28] 中文迁移说明：本文件完整复制自 app/services/ai/knowledge/raw_data_service.py；纳入依据为 DeepSeek 提取入库链 的项目内传递依赖闭包。
from datetime import datetime

from sqlalchemy.orm import Session, sessionmaker

from app.config import sync_engine
from app.models.erp_ai_models import ErpYuanShiShuJu
from app.utils.snowflake_generator import snowflake,generate_uuid7_id


def split_text(text: str, chunk_size: int = 2000) -> list[str]:
    if not text:
        return []
    return [text[index:index + chunk_size] for index in range(0, len(text), chunk_size)]


def _file_type_to_source(file_type: str | None) -> int | None:
    """把解析出来的文件类型转成原始数据表里的来源类型。"""
    mapping = {
        "document": 1,
        "text": 2,
        "audio": 3,
        "image": 4,
    }
    return mapping.get(file_type or "")


def save_raw_text(
    *,
    raw_text: str,
    source_file_path: str | None = None,
    file_type: str | None = None,
    source_file_name: str | None = None,
    guan_lian_ke_hu: int = 0,
    enterprise_id: int | None = None,
    in_userid: int | None = None,
    asset_type_id: str | None = None,
) -> str | None:
    """保存文件解析出的原始文本，返回第一条原始数据 ID。"""
    if not raw_text or not raw_text.strip():
        return None

    first_shuju_id = generate_uuid7_id()
    chunks = split_text(raw_text)

    SessionLocal = sessionmaker(
        bind=sync_engine,
        class_=Session,
        expire_on_commit=False,
    )

    with SessionLocal() as db:
        try:
            for index, chunk in enumerate(chunks):
                record = ErpYuanShiShuJu(
                    shuju_id=first_shuju_id,
                    ZcLeiXin=asset_type_id,
                    ShuJu=chunk,
                    WenJianDiZhi=source_file_path,
                    WenJianName=source_file_name,
                    LaiYuan=_file_type_to_source(file_type),
                    GuanLianKeHu=guan_lian_ke_hu,
                    gs_id=enterprise_id,
                    del_flag=False,
                    in_userid=in_userid,
                    in_time=datetime.now(),
                )
                db.add(record)

            db.commit()
            return first_shuju_id

        except Exception:
            db.rollback()
            raise
