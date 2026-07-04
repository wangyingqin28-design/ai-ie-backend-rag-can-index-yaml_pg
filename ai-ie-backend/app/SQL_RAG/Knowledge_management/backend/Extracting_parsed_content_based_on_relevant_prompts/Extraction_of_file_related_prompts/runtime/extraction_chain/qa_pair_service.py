# [2026-07-04 10:18:20] 作用：导入依赖 `import json`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
import json
# [2026-07-04 10:18:20] 作用：导入依赖 `import re`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
import re
# [2026-07-04 10:18:20] 作用：导入依赖 `from datetime import datetime`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from datetime import datetime
# [2026-07-04 10:18:20] 作用：导入依赖 `from json import JSONDecodeError`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from json import JSONDecodeError
# [2026-07-04 10:18:20] 作用：导入依赖 `from typing import Any`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from typing import Any
# [2026-07-04 10:18:20] 作用：导入依赖 `from sqlalchemy.orm import Session, sessionmaker`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from sqlalchemy.orm import Session, sessionmaker
# [2026-07-04 10:18:20] 作用：导入依赖 `from app.config import sync_engine`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from app.config import sync_engine
# [2026-07-04 10:18:20] 作用：导入依赖 `from extraction_chain.erp_ai_models import ErpWendaJilu`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from extraction_chain.erp_ai_models import ErpWendaJilu
# [2026-07-04 10:18:20] 作用：导入依赖 `from extraction_chain.snowflake_generator import generate_uuid7_id`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from extraction_chain.snowflake_generator import generate_uuid7_id
# [2026-07-04 10:18:20] 作用：声明同步函数 _strip_markdown_fence，封装可复用的处理步骤；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _strip_markdown_fence
def _strip_markdown_fence(text: str) -> str:
    # [2026-07-04 10:18:20] 作用：为 cleaned 构造并保存赋值结果；本行执行 `cleaned = (text or "").strip()`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _strip_markdown_fence
    cleaned = (text or "").strip()
    # [2026-07-04 10:18:20] 作用：为 cleaned 构造并保存赋值结果；本行执行 `cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _strip_markdown_fence
    cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
    # [2026-07-04 10:18:20] 作用：为 cleaned 构造并保存赋值结果；本行执行 `cleaned = re.sub(r"^```\s*", "", cleaned)`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _strip_markdown_fence
    cleaned = re.sub(r"^```\s*", "", cleaned)
    # [2026-07-04 10:18:20] 作用：为 cleaned 构造并保存赋值结果；本行执行 `cleaned = re.sub(r"\s*```$", "", cleaned)`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _strip_markdown_fence
    cleaned = re.sub(r"\s*```$", "", cleaned)
    # [2026-07-04 10:18:20] 作用：从 _strip_markdown_fence 返回表达式 `return cleaned.strip()` 的结果；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _strip_markdown_fence
    return cleaned.strip()
# [2026-07-04 10:18:20] 作用：声明同步函数 parse_ai_qa_result，封装可复用的处理步骤；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
def parse_ai_qa_result(analysis: str) -> list[dict[str, Any]]:
    # [2026-07-04 10:18:20] 作用：在 parse_ai_qa_result 中按条件 `if not analysis:` 选择执行分支；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
    if not analysis:
        # [2026-07-04 10:18:20] 作用：从 parse_ai_qa_result 返回表达式 `return []` 的结果；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
        return []
    # [2026-07-04 10:18:20] 作用：为 text 构造并保存赋值结果；本行执行 `text = _strip_markdown_fence(analysis)`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
    text = _strip_markdown_fence(analysis)
    # [2026-07-04 10:18:20] 作用：在 parse_ai_qa_result 中用 `try:` 控制异常处理或资源清理；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
    try:
        # [2026-07-04 10:18:20] 作用：为 data 构造并保存赋值结果；本行执行 `data = json.loads(text)`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
        data = json.loads(text)
    # [2026-07-04 10:18:20] 作用：在 parse_ai_qa_result 中用 `except JSONDecodeError:` 控制异常处理或资源清理；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
    except JSONDecodeError:
        # [2026-07-04 10:18:20] 作用：为 decoder 构造并保存赋值结果；本行执行 `decoder = json.JSONDecoder()`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
        decoder = json.JSONDecoder()
        # [2026-07-04 10:18:20] 作用：为 starts 构造并保存赋值结果；本行执行 `starts = [position for position in (text.find("["), text.find("{")) if position != -1]`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
        starts = [position for position in (text.find("["), text.find("{")) if position != -1]
        # [2026-07-04 10:18:20] 作用：在 parse_ai_qa_result 中按条件 `if not starts:` 选择执行分支；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
        if not starts:
            # [2026-07-04 10:18:20] 作用：从 parse_ai_qa_result 返回表达式 `return []` 的结果；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
            return []
        # [2026-07-04 10:18:20] 作用：为 start 构造并保存赋值结果；本行执行 `start = min(starts)`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
        start = min(starts)
        # [2026-07-04 10:18:20] 作用：在 parse_ai_qa_result 中用 `try:` 控制异常处理或资源清理；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
        try:
            # [2026-07-04 10:18:20] 作用：为 (data, _) 构造并保存赋值结果；本行执行 `data, _ = decoder.raw_decode(text[start:])`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
            data, _ = decoder.raw_decode(text[start:])
        # [2026-07-04 10:18:20] 作用：在 parse_ai_qa_result 中用 `except JSONDecodeError:` 控制异常处理或资源清理；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
        except JSONDecodeError:
            # [2026-07-04 10:18:20] 作用：从 parse_ai_qa_result 返回表达式 `return []` 的结果；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
            return []
    # [2026-07-04 10:18:20] 作用：在 parse_ai_qa_result 中按条件 `if isinstance(data, dict):` 选择执行分支；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
    if isinstance(data, dict):
        # [2026-07-04 10:18:20] 作用：为 data 构造并保存赋值结果；本行执行 `data = [data]`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
        data = [data]
    # [2026-07-04 10:18:20] 作用：在 parse_ai_qa_result 中按条件 `if not isinstance(data, list):` 选择执行分支；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
    if not isinstance(data, list):
        # [2026-07-04 10:18:20] 作用：从 parse_ai_qa_result 返回表达式 `return []` 的结果；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
        return []
    # [2026-07-04 10:18:20] 作用：从 parse_ai_qa_result 返回表达式 `return [item for item in data if isinstance(item, dict)]` 的结果；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_qa_result
    return [item for item in data if isinstance(item, dict)]
# [2026-07-04 10:18:20] 作用：声明同步函数 _extract_evidence，封装可复用的处理步骤；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _extract_evidence
def _extract_evidence(item: dict[str, Any]) -> tuple[str | None, str | None]:
    # [2026-07-04 10:18:20] 作用：为 evidence 构造并保存赋值结果；本行执行 `evidence = item.get("evidence") or {}`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _extract_evidence
    evidence = item.get("evidence") or {}
    # [2026-07-04 10:18:20] 作用：在 _extract_evidence 中按条件 `if isinstance(evidence, str):` 选择执行分支；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _extract_evidence
    if isinstance(evidence, str):
        # [2026-07-04 10:18:20] 作用：从 _extract_evidence 返回表达式 `return evidence, evidence` 的结果；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _extract_evidence
        return evidence, evidence
    # [2026-07-04 10:18:20] 作用：在 _extract_evidence 中按条件 `if isinstance(evidence, dict):` 选择执行分支；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _extract_evidence
    if isinstance(evidence, dict):
        # [2026-07-04 10:18:20] 作用：从 _extract_evidence 返回表达式 `return evidence.get("customer_text"), evidence.get("service_text")` 的结果；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _extract_evidence
        return evidence.get("customer_text"), evidence.get("service_text")
    # [2026-07-04 10:18:20] 作用：从 _extract_evidence 返回表达式 `return None, None` 的结果；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _extract_evidence
    return None, None
# [2026-07-04 10:18:20] 作用：声明同步函数 _status_to_int，封装可复用的处理步骤；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _status_to_int
def _status_to_int(value: Any) -> int:
    # [2026-07-04 10:18:20] 作用：在 _status_to_int 中按条件 `if value is None:` 选择执行分支；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _status_to_int
    if value is None:
        # [2026-07-04 10:18:20] 作用：从 _status_to_int 返回表达式 `return 0` 的结果；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _status_to_int
        return 0
    # [2026-07-04 10:18:20] 作用：在 _status_to_int 中按条件 `if isinstance(value, int):` 选择执行分支；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _status_to_int
    if isinstance(value, int):
        # [2026-07-04 10:18:20] 作用：从 _status_to_int 返回表达式 `return value` 的结果；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _status_to_int
        return value
    # [2026-07-04 10:18:20] 作用：为 mapping 构造并保存赋值结果；本行执行 `mapping = {"待审核": 0, "完整": 1, "部分完整": 2, "不完整": 3, "未明确": 4, "在用": 1, "弃用": 2}`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _status_to_int
    mapping = {"待审核": 0, "完整": 1, "部分完整": 2, "不完整": 3, "未明确": 4, "在用": 1, "弃用": 2}
    # [2026-07-04 10:18:20] 作用：从 _status_to_int 返回表达式 `return mapping.get(str(value).strip(), 0)` 的结果；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _status_to_int
    return mapping.get(str(value).strip(), 0)
# [2026-07-04 10:18:20] 作用：声明同步函数 save_qa_pairs，封装可复用的处理步骤；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
def save_qa_pairs(
    # [2026-07-04 10:18:20] 作用：完善 同步函数 save_qa_pairs 的签名或多行表达式片段 `*,`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
    *,
    # [2026-07-04 10:18:20] 作用：完善 同步函数 save_qa_pairs 的签名或多行表达式片段 `analysis: str,`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
    analysis: str,
    # [2026-07-04 10:18:20] 作用：完善 同步函数 save_qa_pairs 的签名或多行表达式片段 `raw_data_id: str | None = None,`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
    raw_data_id: str | None = None,
    # [2026-07-04 10:18:20] 作用：完善 同步函数 save_qa_pairs 的签名或多行表达式片段 `source_file_path: str | None = None,`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
    source_file_path: str | None = None,
    # [2026-07-04 10:18:20] 作用：完善 同步函数 save_qa_pairs 的签名或多行表达式片段 `file_type: str | None = None,`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
    file_type: str | None = None,
    # [2026-07-04 10:18:20] 作用：完善 同步函数 save_qa_pairs 的签名或多行表达式片段 `gs_id: str | None = None,`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
    gs_id: str | None = None,
    # [2026-07-04 10:18:20] 作用：完善 同步函数 save_qa_pairs 的签名或多行表达式片段 `in_userid: str | None = None,`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
    in_userid: str | None = None,
# [2026-07-04 10:18:20] 作用：在 save_qa_pairs 中执行具体代码片段 `) -> list[str]:`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
) -> list[str]:
    # [2026-07-04 10:18:20] 作用：为 qa_items 构造并保存赋值结果；本行执行 `qa_items = parse_ai_qa_result(analysis)`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
    qa_items = parse_ai_qa_result(analysis)
    # [2026-07-04 10:18:20] 作用：在 save_qa_pairs 中按条件 `if not qa_items or not raw_data_id:` 选择执行分支；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
    if not qa_items or not raw_data_id:
        # [2026-07-04 10:18:20] 作用：从 save_qa_pairs 返回表达式 `return []` 的结果；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
        return []
    # [2026-07-04 10:18:20] 作用：为 SessionLocal 构造并保存赋值结果；本行执行 `SessionLocal = sessionmaker(bind=sync_engine, class_=Session, expire_on_commit=False)`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
    SessionLocal = sessionmaker(bind=sync_engine, class_=Session, expire_on_commit=False)
    # [2026-07-04 10:18:20] 作用：为 saved_ids 构造并保存赋值结果；本行执行 `saved_ids: list[str] = []`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
    saved_ids: list[str] = []
    # [2026-07-04 10:18:20] 作用：在 save_qa_pairs 中用 `with SessionLocal() as db:` 管理资源生命周期；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
    with SessionLocal() as db:
        # [2026-07-04 10:18:20] 作用：在 save_qa_pairs 中用 `try:` 控制异常处理或资源清理；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
        try:
            # [2026-07-04 10:18:20] 作用：在 save_qa_pairs 中通过 `for item in qa_items:` 迭代处理数据；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
            for item in qa_items:
                # [2026-07-04 10:18:20] 作用：为 (customer_text, service_text) 构造并保存赋值结果；本行执行 `customer_text, service_text = _extract_evidence(item)`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                customer_text, service_text = _extract_evidence(item)
                # [2026-07-04 10:18:20] 作用：为 qa_id 构造并保存赋值结果；本行执行 `qa_id = generate_uuid7_id()`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                qa_id = generate_uuid7_id()
                # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `record = ErpWendaJilu(`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                record = ErpWendaJilu(
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `wdjl_id=qa_id,`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                    wdjl_id=qa_id,
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `Yssj_id=raw_data_id,`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                    Yssj_id=raw_data_id,
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `AI_WenTi=item.get("question"),`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                    AI_WenTi=item.get("question"),
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `AI_DaAn=item.get("answer"),`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                    AI_DaAn=item.get("answer"),
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `AI_Biaozhu=item.get("question_scene"),`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                    AI_Biaozhu=item.get("question_scene"),
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `WenTiYuanWen=customer_text,`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                    WenTiYuanWen=customer_text,
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `DaAnYuanWen=service_text,`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                    DaAnYuanWen=service_text,
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `WenTi_true=item.get("standard_question") or item.get("question"),`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                    WenTi_true=item.get("standard_question") or item.get("question"),
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `DaAn_true=item.get("answer"),`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                    DaAn_true=item.get("answer"),
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `Biaozhu_true=item.get("description"),`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                    Biaozhu_true=item.get("description"),
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `ZhuangTai=_status_to_int(item.get("answer_completeness") or item.get("status")),`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                    ZhuangTai=_status_to_int(item.get("answer_completeness") or item.get("status")),
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `ZhuangTai_id=None,`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                    ZhuangTai_id=None,
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `ZhuangTai_time=None,`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                    ZhuangTai_time=None,
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `YinPinShiJian=item.get("time"),`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                    YinPinShiJian=item.get("time"),
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `gsId=gs_id,`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                    gsId=gs_id,
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `in_userid=in_userid,`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                    in_userid=in_userid,
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `in_time=datetime.now(),`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                    in_time=datetime.now(),
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `yima=None,`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                    yima=None,
                # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                )
                # [2026-07-04 10:18:20] 作用：完善 同步函数 save_qa_pairs 的签名或多行表达式片段 `db.add(record)`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                db.add(record)
                # [2026-07-04 10:18:20] 作用：完善 同步函数 save_qa_pairs 的签名或多行表达式片段 `saved_ids.append(qa_id)`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
                saved_ids.append(qa_id)
            # [2026-07-04 10:18:20] 作用：完善 同步函数 save_qa_pairs 的签名或多行表达式片段 `db.commit()`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
            db.commit()
            # [2026-07-04 10:18:20] 作用：从 save_qa_pairs 返回表达式 `return saved_ids` 的结果；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
            return saved_ids
        # [2026-07-04 10:18:20] 作用：在 save_qa_pairs 中用 `except Exception:` 控制异常处理或资源清理；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
        except Exception:
            # [2026-07-04 10:18:20] 作用：完善 同步函数 save_qa_pairs 的签名或多行表达式片段 `db.rollback()`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
            db.rollback()
            # [2026-07-04 10:18:20] 作用：在 save_qa_pairs 中执行具体代码片段 `raise`；理由依据：源模块 app.services.ai.knowledge.qa_pair_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_qa_pairs
            raise
