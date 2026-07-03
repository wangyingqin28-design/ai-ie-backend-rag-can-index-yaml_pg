# [2026-07-03 18:11:51] 作用：导入依赖 `from datetime import datetime`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from datetime import datetime
# [2026-07-03 18:11:51] 作用：导入依赖 `from sqlalchemy.orm import Session, sessionmaker`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from sqlalchemy.orm import Session, sessionmaker
# [2026-07-03 18:11:51] 作用：导入依赖 `from app.config import sync_engine`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from app.config import sync_engine
# [2026-07-03 18:11:51] 作用：导入依赖 `from extraction_chain.erp_ai_models import ErpYuanShiShuJu`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from extraction_chain.erp_ai_models import ErpYuanShiShuJu
# [2026-07-03 18:11:51] 作用：导入依赖 `from extraction_chain.snowflake_generator import snowflake,generate_uuid7_id`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from extraction_chain.snowflake_generator import snowflake,generate_uuid7_id
# [2026-07-03 18:11:51] 作用：声明同步函数 split_text，封装可复用的处理步骤；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 split_text
def split_text(text: str, chunk_size: int = 2000) -> list[str]:
    # [2026-07-03 18:11:51] 作用：在 split_text 中按条件 `if not text:` 选择执行分支；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 split_text
    if not text:
        # [2026-07-03 18:11:51] 作用：从 split_text 返回表达式 `return []` 的结果；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 split_text
        return []
    # [2026-07-03 18:11:51] 作用：从 split_text 返回表达式 `return [text[index:index + chunk_size] for index in range(0, len(text), chunk_size)]` 的结果；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 split_text
    return [text[index:index + chunk_size] for index in range(0, len(text), chunk_size)]
# [2026-07-03 18:11:51] 作用：声明同步函数 _file_type_to_source，封装可复用的处理步骤；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _file_type_to_source
def _file_type_to_source(file_type: str | None) -> int | None:
    # [2026-07-03 18:11:51] 作用：在 _file_type_to_source 中执行具体代码片段 `"""把解析出来的文件类型转成原始数据表里的来源类型。"""`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _file_type_to_source
    """把解析出来的文件类型转成原始数据表里的来源类型。"""
    # [2026-07-03 18:11:51] 作用：为 mapping 构造并保存赋值结果；本行执行 `mapping = {`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _file_type_to_source
    mapping = {
        # [2026-07-03 18:11:51] 作用：为 mapping 构造并保存赋值结果；本行执行 `"document": 1,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _file_type_to_source
        "document": 1,
        # [2026-07-03 18:11:51] 作用：为 mapping 构造并保存赋值结果；本行执行 `"text": 2,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _file_type_to_source
        "text": 2,
        # [2026-07-03 18:11:51] 作用：为 mapping 构造并保存赋值结果；本行执行 `"audio": 3,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _file_type_to_source
        "audio": 3,
        # [2026-07-03 18:11:51] 作用：为 mapping 构造并保存赋值结果；本行执行 `"image": 4,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _file_type_to_source
        "image": 4,
    # [2026-07-03 18:11:51] 作用：为 mapping 构造并保存赋值结果；本行执行 `}`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _file_type_to_source
    }
    # [2026-07-03 18:11:51] 作用：从 _file_type_to_source 返回表达式 `return mapping.get(file_type or "")` 的结果；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _file_type_to_source
    return mapping.get(file_type or "")
# [2026-07-03 18:11:51] 作用：声明同步函数 save_raw_text，封装可复用的处理步骤；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
def save_raw_text(
    # [2026-07-03 18:11:51] 作用：完善 同步函数 save_raw_text 的签名或多行表达式片段 `*,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
    *,
    # [2026-07-03 18:11:51] 作用：完善 同步函数 save_raw_text 的签名或多行表达式片段 `raw_text: str,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
    raw_text: str,
    # [2026-07-03 18:11:51] 作用：完善 同步函数 save_raw_text 的签名或多行表达式片段 `source_file_path: str | None = None,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
    source_file_path: str | None = None,
    # [2026-07-03 18:11:51] 作用：完善 同步函数 save_raw_text 的签名或多行表达式片段 `file_type: str | None = None,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
    file_type: str | None = None,
    # [2026-07-03 18:11:51] 作用：完善 同步函数 save_raw_text 的签名或多行表达式片段 `source_file_name: str | None = None,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
    source_file_name: str | None = None,
    # [2026-07-03 18:11:51] 作用：完善 同步函数 save_raw_text 的签名或多行表达式片段 `guan_lian_ke_hu: int = 0,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
    guan_lian_ke_hu: int = 0,
    # [2026-07-03 18:11:51] 作用：完善 同步函数 save_raw_text 的签名或多行表达式片段 `enterprise_id: int | None = None,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
    enterprise_id: int | None = None,
    # [2026-07-03 18:11:51] 作用：完善 同步函数 save_raw_text 的签名或多行表达式片段 `in_userid: int | None = None,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
    in_userid: int | None = None,
    # [2026-07-03 18:11:51] 作用：完善 同步函数 save_raw_text 的签名或多行表达式片段 `asset_type_id: str | None = None,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
    asset_type_id: str | None = None,
# [2026-07-03 18:11:51] 作用：在 save_raw_text 中执行具体代码片段 `) -> str | None:`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
) -> str | None:
    # [2026-07-03 18:11:51] 作用：在 save_raw_text 中执行具体代码片段 `"""保存文件解析出的原始文本，返回第一条原始数据 ID。"""`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
    """保存文件解析出的原始文本，返回第一条原始数据 ID。"""
    # [2026-07-03 18:11:51] 作用：在 save_raw_text 中按条件 `if not raw_text or not raw_text.strip():` 选择执行分支；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
    if not raw_text or not raw_text.strip():
        # [2026-07-03 18:11:51] 作用：从 save_raw_text 返回表达式 `return None` 的结果；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
        return None
    # [2026-07-03 18:11:51] 作用：为 first_shuju_id 构造并保存赋值结果；本行执行 `first_shuju_id = generate_uuid7_id()`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
    first_shuju_id = generate_uuid7_id()
    # [2026-07-03 18:11:51] 作用：为 chunks 构造并保存赋值结果；本行执行 `chunks = split_text(raw_text)`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
    chunks = split_text(raw_text)
    # [2026-07-03 18:11:51] 作用：为 SessionLocal 构造并保存赋值结果；本行执行 `SessionLocal = sessionmaker(`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
    SessionLocal = sessionmaker(
        # [2026-07-03 18:11:51] 作用：为 SessionLocal 构造并保存赋值结果；本行执行 `bind=sync_engine,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
        bind=sync_engine,
        # [2026-07-03 18:11:51] 作用：为 SessionLocal 构造并保存赋值结果；本行执行 `class_=Session,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
        class_=Session,
        # [2026-07-03 18:11:51] 作用：为 SessionLocal 构造并保存赋值结果；本行执行 `expire_on_commit=False,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
        expire_on_commit=False,
    # [2026-07-03 18:11:51] 作用：为 SessionLocal 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
    )
    # [2026-07-03 18:11:51] 作用：在 save_raw_text 中用 `with SessionLocal() as db:` 管理资源生命周期；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
    with SessionLocal() as db:
        # [2026-07-03 18:11:51] 作用：在 save_raw_text 中用 `try:` 控制异常处理或资源清理；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
        try:
            # [2026-07-03 18:11:51] 作用：在 save_raw_text 中通过 `for index, chunk in enumerate(chunks):` 迭代处理数据；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
            for index, chunk in enumerate(chunks):
                # [2026-07-03 18:11:51] 作用：为 record 构造并保存赋值结果；本行执行 `record = ErpYuanShiShuJu(`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
                record = ErpYuanShiShuJu(
                    # [2026-07-03 18:11:51] 作用：为 record 构造并保存赋值结果；本行执行 `shuju_id=first_shuju_id,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
                    shuju_id=first_shuju_id,
                    # [2026-07-03 18:11:51] 作用：为 record 构造并保存赋值结果；本行执行 `ZcLeiXin=asset_type_id,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
                    ZcLeiXin=asset_type_id,
                    # [2026-07-03 18:11:51] 作用：为 record 构造并保存赋值结果；本行执行 `ShuJu=chunk,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
                    ShuJu=chunk,
                    # [2026-07-03 18:11:51] 作用：为 record 构造并保存赋值结果；本行执行 `WenJianDiZhi=source_file_path,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
                    WenJianDiZhi=source_file_path,
                    # [2026-07-03 18:11:51] 作用：为 record 构造并保存赋值结果；本行执行 `WenJianName=source_file_name,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
                    WenJianName=source_file_name,
                    # [2026-07-03 18:11:51] 作用：为 record 构造并保存赋值结果；本行执行 `LaiYuan=_file_type_to_source(file_type),`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
                    LaiYuan=_file_type_to_source(file_type),
                    # [2026-07-03 18:11:51] 作用：为 record 构造并保存赋值结果；本行执行 `GuanLianKeHu=guan_lian_ke_hu,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
                    GuanLianKeHu=guan_lian_ke_hu,
                    # [2026-07-03 18:11:51] 作用：为 record 构造并保存赋值结果；本行执行 `gs_id=enterprise_id,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
                    gs_id=enterprise_id,
                    # [2026-07-03 18:11:51] 作用：为 record 构造并保存赋值结果；本行执行 `del_flag=False,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
                    del_flag=False,
                    # [2026-07-03 18:11:51] 作用：为 record 构造并保存赋值结果；本行执行 `in_userid=in_userid,`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
                    in_userid=in_userid,
                    # [2026-07-03 18:11:51] 作用：为 record 构造并保存赋值结果；本行执行 `in_time=datetime.now(),`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
                    in_time=datetime.now(),
                # [2026-07-03 18:11:51] 作用：为 record 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
                )
                # [2026-07-03 18:11:51] 作用：完善 同步函数 save_raw_text 的签名或多行表达式片段 `db.add(record)`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
                db.add(record)
            # [2026-07-03 18:11:51] 作用：完善 同步函数 save_raw_text 的签名或多行表达式片段 `db.commit()`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
            db.commit()
            # [2026-07-03 18:11:51] 作用：从 save_raw_text 返回表达式 `return first_shuju_id` 的结果；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
            return first_shuju_id
        # [2026-07-03 18:11:51] 作用：在 save_raw_text 中用 `except Exception:` 控制异常处理或资源清理；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
        except Exception:
            # [2026-07-03 18:11:51] 作用：完善 同步函数 save_raw_text 的签名或多行表达式片段 `db.rollback()`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
            db.rollback()
            # [2026-07-03 18:11:51] 作用：在 save_raw_text 中执行具体代码片段 `raise`；理由依据：源模块 extraction_chain.raw_data_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_raw_text
            raise
