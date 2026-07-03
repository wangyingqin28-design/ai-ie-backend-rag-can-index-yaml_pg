# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
import json
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
import re
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
from datetime import datetime
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
from json import JSONDecodeError
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
from typing import Any
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
from sqlalchemy.orm import Session, sessionmaker
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
from app.config import sync_engine
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
from extraction_chain.erp_ai_models import ErpWendaJilu
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
from extraction_chain.snowflake_generator import generate_uuid7_id
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _strip_markdown_fence
def _strip_markdown_fence(text: str) -> str:
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _strip_markdown_fence
    text = (text or "").strip()
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _strip_markdown_fence
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _strip_markdown_fence
    text = re.sub(r"^```\s*", "", text)
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _strip_markdown_fence
    text = re.sub(r"\s*```$", "", text)
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _strip_markdown_fence
    return text.strip()
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
def parse_ai_qa_result(analysis: str) -> list[dict[str, Any]]:
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
    if not analysis:
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
        return []
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
    text = _strip_markdown_fence(analysis)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
    # [2026-07-03 16:33:01] 作用：控制异常处理和资源清理；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
    try:
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
        data = json.loads(text)
    # [2026-07-03 16:33:01] 作用：控制异常处理和资源清理；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
    except JSONDecodeError:
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
        decoder = json.JSONDecoder()
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
        start_positions = [pos for pos in (text.find("["), text.find("{")) if pos != -1]
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
        if not start_positions:
            # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
            return []
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
        start = min(start_positions)
        # [2026-07-03 16:33:01] 作用：控制异常处理和资源清理；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
        try:
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
            data, _ = decoder.raw_decode(text[start:])
        # [2026-07-03 16:33:01] 作用：控制异常处理和资源清理；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
        except JSONDecodeError:
            # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
            return []
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
    if isinstance(data, dict):
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
        data = [data]
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
    if not isinstance(data, list):
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
        return []
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 parse_ai_qa_result
    return [item for item in data if isinstance(item, dict)]
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_evidence
def _extract_evidence(item: dict[str, Any]) -> tuple[str | None, str | None]:
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_evidence
    evidence = item.get("evidence") or {}
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_evidence
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_evidence
    if isinstance(evidence, str):
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_evidence
        return evidence, evidence
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_evidence
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_evidence
    if isinstance(evidence, dict):
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_evidence
        return evidence.get("customer_text"), evidence.get("service_text")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_evidence
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _extract_evidence
    return None, None
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _status_to_int
def _status_to_int(value: Any) -> int:
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _status_to_int
    if value is None:
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _status_to_int
        return 0
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _status_to_int
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _status_to_int
    if isinstance(value, int):
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _status_to_int
        return value
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _status_to_int
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _status_to_int
    mapping = {
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _status_to_int
        "待审核": 0,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _status_to_int
        "完整": 1,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _status_to_int
        "部分完整": 2,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _status_to_int
        "不完整": 3,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _status_to_int
        "未明确": 4,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _status_to_int
        "在用": 1,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _status_to_int
        "弃用": 2,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _status_to_int
    }
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 _status_to_int
    return mapping.get(str(value).strip(), 0)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.qa_pair_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
def save_qa_pairs(
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
    *,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
    analysis: str,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
    raw_data_id: str | None = None,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
    source_file_path: str | None = None,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
    file_type: str | None = None,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
    gs_id: str | None = None,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
    in_userid: str | None = None,
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
) -> list[str]:
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
    qa_items = parse_ai_qa_result(analysis)
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
    if not qa_items or not raw_data_id:
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
        return []
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
    SessionLocal = sessionmaker(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
        bind=sync_engine,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
        class_=Session,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
        expire_on_commit=False,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
    saved_ids: list[str] = []
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
    # [2026-07-03 16:33:01] 作用：限定文件、会话或异步资源生命周期；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
    with SessionLocal() as db:
        # [2026-07-03 16:33:01] 作用：控制异常处理和资源清理；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
        try:
            # [2026-07-03 16:33:01] 作用：逐项处理集合或重复任务；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
            for item in qa_items:
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                customer_text, service_text = _extract_evidence(item)
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                qa_id = generate_uuid7_id()
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                record = ErpWendaJilu(
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                    wdjl_id=qa_id,
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                    Yssj_id=raw_data_id,
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                    AI_WenTi=item.get("question"),
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                    AI_DaAn=item.get("answer"),
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                    AI_Biaozhu=item.get("question_scene") or item.get("description"),
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                    WenTiYuanWen=customer_text,
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                    DaAnYuanWen=service_text,
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                    WenTi_true=item.get("question"),
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                    DaAn_true=item.get("answer"),
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                    Biaozhu_true=item.get("description"),
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                    ZhuangTai=_status_to_int(item.get("status") or item.get("answer_completeness")),
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                    ZhuangTai_id=None,
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                    ZhuangTai_time=None,
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                    YinPinShiJian=item.get("time"),
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                    gsId=gs_id,
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                    in_userid=in_userid,
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                    in_time=datetime.now(),
                # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                db.add(record)
                # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
                saved_ids.append(qa_id)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
            db.commit()
            # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
            return saved_ids
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
        # [2026-07-03 16:33:01] 作用：控制异常处理和资源清理；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
        except Exception:
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
            db.rollback()
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 save_qa_pairs
            raise
