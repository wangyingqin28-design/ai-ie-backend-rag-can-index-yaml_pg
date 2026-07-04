# [2026-07-04 10:18:20] 作用：导入依赖 `import json`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
import json
# [2026-07-04 10:18:20] 作用：导入依赖 `import re`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
import re
# [2026-07-04 10:18:20] 作用：导入依赖 `from datetime import datetime`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from datetime import datetime
# [2026-07-04 10:18:20] 作用：导入依赖 `from json import JSONDecodeError`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from json import JSONDecodeError
# [2026-07-04 10:18:20] 作用：导入依赖 `from typing import Any`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from typing import Any
# [2026-07-04 10:18:20] 作用：导入依赖 `from sqlalchemy.orm import Session, sessionmaker`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from sqlalchemy.orm import Session, sessionmaker
# [2026-07-04 10:18:20] 作用：导入依赖 `from app.config import sync_engine`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from app.config import sync_engine
# [2026-07-04 10:18:20] 作用：导入依赖 `from extraction_chain.erp_ai_models import ErpYitu`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from extraction_chain.erp_ai_models import ErpYitu
# [2026-07-04 10:18:20] 作用：导入依赖 `from extraction_chain.snowflake_generator import generate_uuid7_id`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from extraction_chain.snowflake_generator import generate_uuid7_id
# [2026-07-04 10:18:20] 作用：声明同步函数 _strip_markdown_fence，封装可复用的处理步骤；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _strip_markdown_fence
def _strip_markdown_fence(text: str) -> str:
    # [2026-07-04 10:18:20] 作用：为 cleaned 构造并保存赋值结果；本行执行 `cleaned = (text or "").strip()`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _strip_markdown_fence
    cleaned = (text or "").strip()
    # [2026-07-04 10:18:20] 作用：为 cleaned 构造并保存赋值结果；本行执行 `cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _strip_markdown_fence
    cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
    # [2026-07-04 10:18:20] 作用：为 cleaned 构造并保存赋值结果；本行执行 `cleaned = re.sub(r"^```\s*", "", cleaned)`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _strip_markdown_fence
    cleaned = re.sub(r"^```\s*", "", cleaned)
    # [2026-07-04 10:18:20] 作用：为 cleaned 构造并保存赋值结果；本行执行 `cleaned = re.sub(r"\s*```$", "", cleaned)`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _strip_markdown_fence
    cleaned = re.sub(r"\s*```$", "", cleaned)
    # [2026-07-04 10:18:20] 作用：从 _strip_markdown_fence 返回表达式 `return cleaned.strip()` 的结果；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _strip_markdown_fence
    return cleaned.strip()
# [2026-07-04 10:18:20] 作用：声明同步函数 parse_ai_intent_result，封装可复用的处理步骤；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
def parse_ai_intent_result(analysis: str) -> list[dict[str, Any]]:
    # [2026-07-04 10:18:20] 作用：在 parse_ai_intent_result 中按条件 `if not analysis:` 选择执行分支；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
    if not analysis:
        # [2026-07-04 10:18:20] 作用：从 parse_ai_intent_result 返回表达式 `return []` 的结果；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
        return []
    # [2026-07-04 10:18:20] 作用：为 text 构造并保存赋值结果；本行执行 `text = _strip_markdown_fence(analysis)`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
    text = _strip_markdown_fence(analysis)
    # [2026-07-04 10:18:20] 作用：在 parse_ai_intent_result 中用 `try:` 控制异常处理或资源清理；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
    try:
        # [2026-07-04 10:18:20] 作用：为 data 构造并保存赋值结果；本行执行 `data = json.loads(text)`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
        data = json.loads(text)
    # [2026-07-04 10:18:20] 作用：在 parse_ai_intent_result 中用 `except JSONDecodeError:` 控制异常处理或资源清理；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
    except JSONDecodeError:
        # [2026-07-04 10:18:20] 作用：为 decoder 构造并保存赋值结果；本行执行 `decoder = json.JSONDecoder()`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
        decoder = json.JSONDecoder()
        # [2026-07-04 10:18:20] 作用：为 starts 构造并保存赋值结果；本行执行 `starts = [position for position in (text.find("["), text.find("{")) if position != -1]`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
        starts = [position for position in (text.find("["), text.find("{")) if position != -1]
        # [2026-07-04 10:18:20] 作用：在 parse_ai_intent_result 中按条件 `if not starts:` 选择执行分支；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
        if not starts:
            # [2026-07-04 10:18:20] 作用：从 parse_ai_intent_result 返回表达式 `return []` 的结果；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
            return []
        # [2026-07-04 10:18:20] 作用：为 start 构造并保存赋值结果；本行执行 `start = min(starts)`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
        start = min(starts)
        # [2026-07-04 10:18:20] 作用：在 parse_ai_intent_result 中用 `try:` 控制异常处理或资源清理；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
        try:
            # [2026-07-04 10:18:20] 作用：为 (data, _) 构造并保存赋值结果；本行执行 `data, _ = decoder.raw_decode(text[start:])`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
            data, _ = decoder.raw_decode(text[start:])
        # [2026-07-04 10:18:20] 作用：在 parse_ai_intent_result 中用 `except JSONDecodeError:` 控制异常处理或资源清理；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
        except JSONDecodeError:
            # [2026-07-04 10:18:20] 作用：从 parse_ai_intent_result 返回表达式 `return []` 的结果；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
            return []
    # [2026-07-04 10:18:20] 作用：在 parse_ai_intent_result 中按条件 `if isinstance(data, dict):` 选择执行分支；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
    if isinstance(data, dict):
        # [2026-07-04 10:18:20] 作用：为 data 构造并保存赋值结果；本行执行 `data = [data]`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
        data = [data]
    # [2026-07-04 10:18:20] 作用：在 parse_ai_intent_result 中按条件 `if not isinstance(data, list):` 选择执行分支；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
    if not isinstance(data, list):
        # [2026-07-04 10:18:20] 作用：从 parse_ai_intent_result 返回表达式 `return []` 的结果；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
        return []
    # [2026-07-04 10:18:20] 作用：从 parse_ai_intent_result 返回表达式 `return [item for item in data if isinstance(item, dict)]` 的结果；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 parse_ai_intent_result
    return [item for item in data if isinstance(item, dict)]
# [2026-07-04 10:18:20] 作用：声明同步函数 _status_to_int，封装可复用的处理步骤；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _status_to_int
def _status_to_int(value: Any) -> int:
    # [2026-07-04 10:18:20] 作用：在 _status_to_int 中按条件 `if value is None:` 选择执行分支；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _status_to_int
    if value is None:
        # [2026-07-04 10:18:20] 作用：从 _status_to_int 返回表达式 `return 0` 的结果；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _status_to_int
        return 0
    # [2026-07-04 10:18:20] 作用：在 _status_to_int 中按条件 `if isinstance(value, int):` 选择执行分支；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _status_to_int
    if isinstance(value, int):
        # [2026-07-04 10:18:20] 作用：从 _status_to_int 返回表达式 `return value` 的结果；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _status_to_int
        return value
    # [2026-07-04 10:18:20] 作用：为 mapping 构造并保存赋值结果；本行执行 `mapping = {"待审核": 0, "完整": 1, "部分完整": 2, "不完整": 3, "未明确": 4, "在用": 1, "弃用": 2}`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _status_to_int
    mapping = {"待审核": 0, "完整": 1, "部分完整": 2, "不完整": 3, "未明确": 4, "在用": 1, "弃用": 2}
    # [2026-07-04 10:18:20] 作用：从 _status_to_int 返回表达式 `return mapping.get(str(value).strip(), 0)` 的结果；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 _status_to_int
    return mapping.get(str(value).strip(), 0)
# [2026-07-04 10:18:20] 作用：声明同步函数 save_intents，封装可复用的处理步骤；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
def save_intents(
    # [2026-07-04 10:18:20] 作用：完善 同步函数 save_intents 的签名或多行表达式片段 `*,`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
    *,
    # [2026-07-04 10:18:20] 作用：完善 同步函数 save_intents 的签名或多行表达式片段 `analysis: str,`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
    analysis: str,
    # [2026-07-04 10:18:20] 作用：完善 同步函数 save_intents 的签名或多行表达式片段 `raw_data_id: str | None = None,`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
    raw_data_id: str | None = None,
    # [2026-07-04 10:18:20] 作用：完善 同步函数 save_intents 的签名或多行表达式片段 `source_file_path: str | None = None,`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
    source_file_path: str | None = None,
    # [2026-07-04 10:18:20] 作用：完善 同步函数 save_intents 的签名或多行表达式片段 `file_type: str | None = None,`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
    file_type: str | None = None,
    # [2026-07-04 10:18:20] 作用：完善 同步函数 save_intents 的签名或多行表达式片段 `gs_id: str | None = None,`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
    gs_id: str | None = None,
    # [2026-07-04 10:18:20] 作用：完善 同步函数 save_intents 的签名或多行表达式片段 `in_userid: str | None = None,`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
    in_userid: str | None = None,
# [2026-07-04 10:18:20] 作用：在 save_intents 中执行具体代码片段 `) -> list[str]:`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
) -> list[str]:
    # [2026-07-04 10:18:20] 作用：为 intent_items 构造并保存赋值结果；本行执行 `intent_items = parse_ai_intent_result(analysis)`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
    intent_items = parse_ai_intent_result(analysis)
    # [2026-07-04 10:18:20] 作用：在 save_intents 中按条件 `if not intent_items or not raw_data_id:` 选择执行分支；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
    if not intent_items or not raw_data_id:
        # [2026-07-04 10:18:20] 作用：从 save_intents 返回表达式 `return []` 的结果；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
        return []
    # [2026-07-04 10:18:20] 作用：为 SessionLocal 构造并保存赋值结果；本行执行 `SessionLocal = sessionmaker(bind=sync_engine, class_=Session, expire_on_commit=False)`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
    SessionLocal = sessionmaker(bind=sync_engine, class_=Session, expire_on_commit=False)
    # [2026-07-04 10:18:20] 作用：为 saved_ids 构造并保存赋值结果；本行执行 `saved_ids: list[str] = []`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
    saved_ids: list[str] = []
    # [2026-07-04 10:18:20] 作用：在 save_intents 中用 `with SessionLocal() as db:` 管理资源生命周期；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
    with SessionLocal() as db:
        # [2026-07-04 10:18:20] 作用：在 save_intents 中用 `try:` 控制异常处理或资源清理；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
        try:
            # [2026-07-04 10:18:20] 作用：在 save_intents 中通过 `for item in intent_items:` 迭代处理数据；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
            for item in intent_items:
                # [2026-07-04 10:18:20] 作用：为 intent_id 构造并保存赋值结果；本行执行 `intent_id = generate_uuid7_id()`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
                intent_id = generate_uuid7_id()
                # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `record = ErpYitu(`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
                record = ErpYitu(
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `yt_id=intent_id,`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
                    yt_id=intent_id,
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `Yssj_id=raw_data_id,`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
                    Yssj_id=raw_data_id,
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `AI_YiTu=item.get("intent"),`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
                    AI_YiTu=item.get("intent"),
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `YiTu=item.get("description"),`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
                    YiTu=item.get("description"),
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `BiaoZhu=item.get("evidence"),`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
                    BiaoZhu=item.get("evidence"),
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `ZhuangTai=0,`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
                    ZhuangTai=0,
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `ZhuangTai_id=None,`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
                    ZhuangTai_id=None,
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `ZhuangTai_time=None,`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
                    ZhuangTai_time=None,
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `ShiJian=item.get("time"),`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
                    ShiJian=item.get("time"),
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `gsId=gs_id,`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
                    gsId=gs_id,
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `del_time=None,`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
                    del_time=None,
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `in_userid=in_userid,`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
                    in_userid=in_userid,
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `in_time=datetime.now(),`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
                    in_time=datetime.now(),
                    # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `yima=None,`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
                    yima=None,
                # [2026-07-04 10:18:20] 作用：为 record 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
                )
                # [2026-07-04 10:18:20] 作用：完善 同步函数 save_intents 的签名或多行表达式片段 `db.add(record)`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
                db.add(record)
                # [2026-07-04 10:18:20] 作用：完善 同步函数 save_intents 的签名或多行表达式片段 `saved_ids.append(intent_id)`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
                saved_ids.append(intent_id)
            # [2026-07-04 10:18:20] 作用：完善 同步函数 save_intents 的签名或多行表达式片段 `db.commit()`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
            db.commit()
            # [2026-07-04 10:18:20] 作用：从 save_intents 返回表达式 `return saved_ids` 的结果；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
            return saved_ids
        # [2026-07-04 10:18:20] 作用：在 save_intents 中用 `except Exception:` 控制异常处理或资源清理；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
        except Exception:
            # [2026-07-04 10:18:20] 作用：完善 同步函数 save_intents 的签名或多行表达式片段 `db.rollback()`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
            db.rollback()
            # [2026-07-04 10:18:20] 作用：在 save_intents 中执行具体代码片段 `raise`；理由依据：源模块 app.services.ai.knowledge.intent_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 save_intents
            raise
