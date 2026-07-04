# [2026-07-04 10:18:20] 作用：导入依赖 `import json`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
import json
# [2026-07-04 10:18:20] 作用：导入依赖 `from typing import Any`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from typing import Any
# [2026-07-04 10:18:20] 作用：导入依赖 `from app.ai.llm.llm_client import llm_model_func`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from app.ai.llm.llm_client import llm_model_func
# [2026-07-04 10:18:20] 作用：导入依赖 `from app.ai.prompts import (`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from app.ai.prompts import (
    # [2026-07-04 10:18:20] 作用：在 模块级初始化 中执行具体代码片段 `QA_EXTRACTION_PROMPT,`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
    QA_EXTRACTION_PROMPT,
    # [2026-07-04 10:18:20] 作用：在 模块级初始化 中执行具体代码片段 `OUTPUT_FORMAT_PROMPT,`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
    OUTPUT_FORMAT_PROMPT,
    # [2026-07-04 10:18:20] 作用：在 模块级初始化 中执行具体代码片段 `DESCRIPTION_PROMPT,`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
    DESCRIPTION_PROMPT,
    # [2026-07-04 10:18:20] 作用：在 模块级初始化 中执行具体代码片段 `YT_PROMPT,`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
    YT_PROMPT,
    # [2026-07-04 10:18:20] 作用：在 模块级初始化 中执行具体代码片段 `AUDIO_QA_USER_PROMPT_TEMPLATE,`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
    AUDIO_QA_USER_PROMPT_TEMPLATE,
# [2026-07-04 10:18:20] 作用：在 模块级初始化 中执行具体代码片段 `)`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
)
# [2026-07-04 10:18:20] 作用：导入依赖 `from extraction_chain.qa_pair_service import parse_ai_qa_result`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from extraction_chain.qa_pair_service import parse_ai_qa_result
# [2026-07-04 10:18:20] 作用：导入依赖 `from extraction_chain.intent_service import parse_ai_intent_result`，供 模块级初始化 使用；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from extraction_chain.intent_service import parse_ai_intent_result
# [2026-07-04 10:18:20] 作用：为 ANSWER_COMPLETENESS_PROMPT 构造并保存赋值结果；本行执行 `ANSWER_COMPLETENESS_PROMPT = '\n每个问答对象还必须包含以下字段：\n"answer_completeness": "完整/部分完整/不完整/未明确"\n完整表…`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
ANSWER_COMPLETENESS_PROMPT = '\n每个问答对象还必须包含以下字段：\n"answer_completeness": "完整/部分完整/不完整/未明确"\n完整表示原文已给出可执行或明确肯否答案；部分完整、不完整、未明确必须按原文判断，禁止补全。\n'
# [2026-07-04 10:18:20] 作用：声明异步函数 extract_audio_qa，提供可等待的链路处理入口；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_qa
async def extract_audio_qa(raw_text: str) -> str:
    # [2026-07-04 10:18:20] 作用：为 user_prompt 构造并保存赋值结果；本行执行 `user_prompt = AUDIO_QA_USER_PROMPT_TEMPLATE.format(raw_text=raw_text)`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_qa
    user_prompt = AUDIO_QA_USER_PROMPT_TEMPLATE.format(raw_text=raw_text)
    # [2026-07-04 10:18:20] 作用：为 system_prompt 构造并保存赋值结果；本行执行 `system_prompt = "\n\n".join([QA_EXTRACTION_PROMPT, OUTPUT_FORMAT_PROMPT, ANSWER_COMPLETENESS_PR…`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_qa
    system_prompt = "\n\n".join([QA_EXTRACTION_PROMPT, OUTPUT_FORMAT_PROMPT, ANSWER_COMPLETENESS_PROMPT])
    # [2026-07-04 10:18:20] 作用：从 extract_audio_qa 返回表达式 `return await llm_model_func(user_prompt, system_prompt=system_prompt)` 的结果；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_qa
    return await llm_model_func(user_prompt, system_prompt=system_prompt)
# [2026-07-04 10:18:20] 作用：声明异步函数 extract_qa_description，提供可等待的链路处理入口；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_qa_description
async def extract_qa_description(qa_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    # [2026-07-04 10:18:20] 作用：在 extract_qa_description 中按条件 `if not qa_items:` 选择执行分支；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_qa_description
    if not qa_items:
        # [2026-07-04 10:18:20] 作用：从 extract_qa_description 返回表达式 `return []` 的结果；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_qa_description
        return []
    # [2026-07-04 10:18:20] 作用：为 user_prompt 构造并保存赋值结果；本行执行 `user_prompt = json.dumps(qa_items, ensure_ascii=False, indent=2)`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_qa_description
    user_prompt = json.dumps(qa_items, ensure_ascii=False, indent=2)
    # [2026-07-04 10:18:20] 作用：为 result 构造并保存赋值结果；本行执行 `result = await llm_model_func(user_prompt, system_prompt=DESCRIPTION_PROMPT)`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_qa_description
    result = await llm_model_func(user_prompt, system_prompt=DESCRIPTION_PROMPT)
    # [2026-07-04 10:18:20] 作用：从 extract_qa_description 返回表达式 `return parse_ai_qa_result(result)` 的结果；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_qa_description
    return parse_ai_qa_result(result)
# [2026-07-04 10:18:20] 作用：声明同步函数 merge_qa_description，封装可复用的处理步骤；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 merge_qa_description
def merge_qa_description(
    # [2026-07-04 10:18:20] 作用：完善 同步函数 merge_qa_description 的签名或多行表达式片段 `qa_items: list[dict[str, Any]],`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 merge_qa_description
    qa_items: list[dict[str, Any]],
    # [2026-07-04 10:18:20] 作用：完善 同步函数 merge_qa_description 的签名或多行表达式片段 `description_items: list[dict[str, Any]],`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 merge_qa_description
    description_items: list[dict[str, Any]],
# [2026-07-04 10:18:20] 作用：在 merge_qa_description 中执行具体代码片段 `) -> list[dict[str, Any]]:`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 merge_qa_description
) -> list[dict[str, Any]]:
    # [2026-07-04 10:18:20] 作用：为 description_map 构造并保存赋值结果；本行执行 `description_map: dict[str, Any] = {}`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 merge_qa_description
    description_map: dict[str, Any] = {}
    # [2026-07-04 10:18:20] 作用：在 merge_qa_description 中通过 `for item in description_items:` 迭代处理数据；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 merge_qa_description
    for item in description_items:
        # [2026-07-04 10:18:20] 作用：为 key 构造并保存赋值结果；本行执行 `key = item.get("standard_question") or item.get("question")`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 merge_qa_description
        key = item.get("standard_question") or item.get("question")
        # [2026-07-04 10:18:20] 作用：在 merge_qa_description 中按条件 `if key:` 选择执行分支；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 merge_qa_description
        if key:
            # [2026-07-04 10:18:20] 作用：为 description_map[str(key).strip()] 构造并保存赋值结果；本行执行 `description_map[str(key).strip()] = item.get("description")`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 merge_qa_description
            description_map[str(key).strip()] = item.get("description")
    # [2026-07-04 10:18:20] 作用：为 merged 构造并保存赋值结果；本行执行 `merged: list[dict[str, Any]] = []`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 merge_qa_description
    merged: list[dict[str, Any]] = []
    # [2026-07-04 10:18:20] 作用：在 merge_qa_description 中通过 `for item in qa_items:` 迭代处理数据；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 merge_qa_description
    for item in qa_items:
        # [2026-07-04 10:18:20] 作用：为 new_item 构造并保存赋值结果；本行执行 `new_item = dict(item)`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 merge_qa_description
        new_item = dict(item)
        # [2026-07-04 10:18:20] 作用：为 key 构造并保存赋值结果；本行执行 `key = new_item.get("standard_question") or new_item.get("question")`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 merge_qa_description
        key = new_item.get("standard_question") or new_item.get("question")
        # [2026-07-04 10:18:20] 作用：在 merge_qa_description 中按条件 `if key:` 选择执行分支；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 merge_qa_description
        if key:
            # [2026-07-04 10:18:20] 作用：为 description 构造并保存赋值结果；本行执行 `description = description_map.get(str(key).strip())`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 merge_qa_description
            description = description_map.get(str(key).strip())
            # [2026-07-04 10:18:20] 作用：在 merge_qa_description 中按条件 `if description:` 选择执行分支；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 merge_qa_description
            if description:
                # [2026-07-04 10:18:20] 作用：为 new_item['description'] 构造并保存赋值结果；本行执行 `new_item["description"] = description`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 merge_qa_description
                new_item["description"] = description
        # [2026-07-04 10:18:20] 作用：完善 同步函数 merge_qa_description 的签名或多行表达式片段 `merged.append(new_item)`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 merge_qa_description
        merged.append(new_item)
    # [2026-07-04 10:18:20] 作用：从 merge_qa_description 返回表达式 `return merged` 的结果；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于同步函数 merge_qa_description
    return merged
# [2026-07-04 10:18:20] 作用：声明异步函数 extract_audio_intent，提供可等待的链路处理入口；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_intent
async def extract_audio_intent(raw_text: str) -> str:
    # [2026-07-04 10:18:20] 作用：为 user_prompt 构造并保存赋值结果；本行执行 `user_prompt = AUDIO_QA_USER_PROMPT_TEMPLATE.format(raw_text=raw_text)`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_intent
    user_prompt = AUDIO_QA_USER_PROMPT_TEMPLATE.format(raw_text=raw_text)
    # [2026-07-04 10:18:20] 作用：从 extract_audio_intent 返回表达式 `return await llm_model_func(user_prompt, system_prompt=YT_PROMPT)` 的结果；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_intent
    return await llm_model_func(user_prompt, system_prompt=YT_PROMPT)
# [2026-07-04 10:18:20] 作用：声明异步函数 extract_audio_knowledge，提供可等待的链路处理入口；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_knowledge
async def extract_audio_knowledge(raw_text: str) -> dict[str, Any]:
    # [2026-07-04 10:18:20] 作用：为 qa_analysis 构造并保存赋值结果；本行执行 `qa_analysis = await extract_audio_qa(raw_text)`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_knowledge
    qa_analysis = await extract_audio_qa(raw_text)
    # [2026-07-04 10:18:20] 作用：为 qa_items 构造并保存赋值结果；本行执行 `qa_items = parse_ai_qa_result(qa_analysis)`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_knowledge
    qa_items = parse_ai_qa_result(qa_analysis)
    # [2026-07-04 10:18:20] 作用：为 description_items 构造并保存赋值结果；本行执行 `description_items = await extract_qa_description(qa_items)`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_knowledge
    description_items = await extract_qa_description(qa_items)
    # [2026-07-04 10:18:20] 作用：为 qa_with_description 构造并保存赋值结果；本行执行 `qa_with_description = merge_qa_description(qa_items, description_items)`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_knowledge
    qa_with_description = merge_qa_description(qa_items, description_items)
    # [2026-07-04 10:18:20] 作用：为 intent_analysis 构造并保存赋值结果；本行执行 `intent_analysis = await extract_audio_intent(raw_text)`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_knowledge
    intent_analysis = await extract_audio_intent(raw_text)
    # [2026-07-04 10:18:20] 作用：为 intent_items 构造并保存赋值结果；本行执行 `intent_items = parse_ai_intent_result(intent_analysis)`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_knowledge
    intent_items = parse_ai_intent_result(intent_analysis)
    # [2026-07-04 10:18:20] 作用：从 extract_audio_knowledge 返回表达式 `return {` 的结果；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_knowledge
    return {
        # [2026-07-04 10:18:20] 作用：完善 异步函数 extract_audio_knowledge 的签名或多行表达式片段 `"qa_analysis": json.dumps(qa_with_description, ensure_ascii=False),`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_knowledge
        "qa_analysis": json.dumps(qa_with_description, ensure_ascii=False),
        # [2026-07-04 10:18:20] 作用：完善 异步函数 extract_audio_knowledge 的签名或多行表达式片段 `"qa_items": qa_with_description,`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_knowledge
        "qa_items": qa_with_description,
        # [2026-07-04 10:18:20] 作用：完善 异步函数 extract_audio_knowledge 的签名或多行表达式片段 `"description_items": description_items,`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_knowledge
        "description_items": description_items,
        # [2026-07-04 10:18:20] 作用：完善 异步函数 extract_audio_knowledge 的签名或多行表达式片段 `"intent_analysis": intent_analysis,`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_knowledge
        "intent_analysis": intent_analysis,
        # [2026-07-04 10:18:20] 作用：完善 异步函数 extract_audio_knowledge 的签名或多行表达式片段 `"intent_items": intent_items,`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_knowledge
        "intent_items": intent_items,
    # [2026-07-04 10:18:20] 作用：在 extract_audio_knowledge 中执行具体代码片段 `}`；理由依据：源模块 app.services.ai.extraction.audio_knowledge_extract_service 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于异步函数 extract_audio_knowledge
    }
