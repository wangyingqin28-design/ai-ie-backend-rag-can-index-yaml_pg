# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.raw_data_service 的模块级声明
from datetime import datetime
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.raw_data_service 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.raw_data_service 的模块级声明
from sqlalchemy.orm import Session, sessionmaker
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.raw_data_service 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.raw_data_service 的模块级声明
from app.config import sync_engine
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.raw_data_service 的模块级声明
from extraction_chain.erp_ai_models import ErpYuanShiShuJu
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.raw_data_service 的模块级声明
from extraction_chain.snowflake_generator import snowflake,generate_uuid7_id
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.raw_data_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.raw_data_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 split_text
def split_text(text: str, chunk_size: int = 2000) -> list[str]:
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 split_text
    if not text:
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 split_text
        return []
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 split_text
    return [text[index:index + chunk_size] for index in range(0, len(text), chunk_size)]
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.raw_data_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.raw_data_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _file_type_to_source
def _file_type_to_source(file_type: str | None) -> int | None:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _file_type_to_source
    """把解析出来的文件类型转成原始数据表里的来源类型。"""
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _file_type_to_source
    mapping = {
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _file_type_to_source
        "document": 1,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _file_type_to_source
        "text": 2,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _file_type_to_source
        "audio": 3,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _file_type_to_source
        "image": 4,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _file_type_to_source
    }
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _file_type_to_source
    return mapping.get(file_type or "")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.raw_data_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.raw_data_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
def save_raw_text(
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
    *,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
    raw_text: str,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
    source_file_path: str | None = None,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
    file_type: str | None = None,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
    source_file_name: str | None = None,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
    guan_lian_ke_hu: int = 0,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
    enterprise_id: int | None = None,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
    in_userid: int | None = None,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
    asset_type_id: str | None = None,
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
) -> str | None:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
    """保存文件解析出的原始文本，返回第一条原始数据 ID。"""
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
    if not raw_text or not raw_text.strip():
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
        return None
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
    first_shuju_id = generate_uuid7_id()
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
    chunks = split_text(raw_text)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
    SessionLocal = sessionmaker(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
        bind=sync_engine,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
        class_=Session,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
        expire_on_commit=False,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
    # [2026-07-03 16:33:01] 作用：限定文件、会话或异步资源生命周期；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
    with SessionLocal() as db:
        # [2026-07-03 16:33:01] 作用：控制异常处理和资源清理；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
        try:
            # [2026-07-03 16:33:01] 作用：逐项处理集合或重复任务；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
            for index, chunk in enumerate(chunks):
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
                record = ErpYuanShiShuJu(
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
                    shuju_id=first_shuju_id,
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
                    ZcLeiXin=asset_type_id,
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
                    ShuJu=chunk,
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
                    WenJianDiZhi=source_file_path,
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
                    WenJianName=source_file_name,
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
                    LaiYuan=_file_type_to_source(file_type),
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
                    GuanLianKeHu=guan_lian_ke_hu,
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
                    gs_id=enterprise_id,
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
                    del_flag=False,
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
                    in_userid=in_userid,
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
                    in_time=datetime.now(),
                # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
                )
                # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
                db.add(record)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
            db.commit()
            # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
            return first_shuju_id
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
        # [2026-07-03 16:33:01] 作用：控制异常处理和资源清理；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
        except Exception:
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
            db.rollback()
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_raw_text
            raise
